# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas"]
# ///
"""
Bin the per-contact data in ``contact_<t>.csv`` into the 36-by-18 sphere
histograms used by the Blender rose renderer.  Two histograms are
produced per timestep:

    distCount_<t>.csv   -- contact density per unit solid angle:
                             rho_c[m,n] = arr_count[m,n] / (N_p sin(v) du dv)
                           matching paper Eq. for rho_c (Section 2.5).
                           This is the probability-density quantity the
                           rose colorbar labels "Contact density rho_c".
                           (arr_count already counts each contact twice via
                            antipodal duplication, which absorbs the 2 in
                            the paper's 2N(theta,phi) numerator.)
    distForce_<t>.csv   -- mean |F_n| per contact within each bin,
                           = sum_fn[bin] / count[bin]  (force rose, R2.7)
                           Mean (not sum) so the angular pattern of force
                           magnitude is isolated from the angular pattern
                           of contact count, matching Zhou (2022) /
                           Song (2024).  Empty bins are written as 0.

Conventions match ``fabric_getter.py`` exactly so the resulting CSVs are
drop-in for the existing Blender pipeline:

  - Ball-ball contacts only (BallFacet excluded).
  - Contact normal n is rotated from global (x, y, z) to local cylindrical
    (cir, rad, z) by a per-contact frame built from the contact position.
  - Antipodal symmetry: each contact contributes its weight twice -- once
    at its own (u, v) bin and once at the diametrically opposite bin --
    consistent with the n <-> -n indistinguishability of the contact line.
  - Output is a single line of 36*18 = 648 comma-separated floats in
    row-major (C) order: element [m, n] at flat index m*18 + n.
    Blender reads the file with ``np.loadtxt(..., delimiter=',')`` and
    reshapes to (36, 18) as before.

Run:  uv run bin_contacts.py
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

DATA_ROOT = Path("/Users/hanyusong/thesis/MicroLiq/torsionSim/cyclic_shear")

NUMBER_U = 36           # azimuthal bins (u in [0, 2*pi])
NUMBER_V = 18           # polar bins     (v in [0, pi])
N_PARTICLES = 53764     # for converting bin counts to per-particle density

# 8 panels matching fig_contact_density_standalone.tex / anisotropy_values.py
PANELS = [
    ("Dr90/k0.50/csr_0.200", 0),
    ("Dr90/k0.50/csr_0.200", 302),
    ("Dr90/k0.50/csr_0.200", 523),
    ("Dr90/k0.50/csr_0.200", 529),
    ("Dr90/k2.00/csr_0.200", 0),
    ("Dr90/k2.00/csr_0.200", 226),
    ("Dr90/k2.00/csr_0.200", 379),
    ("Dr90/k2.00/csr_0.200", 386),
]


def to_local_cir_rad(n_global: np.ndarray, pos_xy: np.ndarray) -> np.ndarray:
    """Rotate unit normals from global (x, y, z) to local (cir, rad, z)
    using the same axis convention as fabric_getter.py:

        r_hat (inward radial)  = (-px, -py, 0) / sqrt(px^2 + py^2)
        cir_hat (CCW circ.)    = ( -py,  px, 0) / sqrt(px^2 + py^2)   (i.e.,
                                  ry * (-1) + rx * ... -- see derivation)
        z_hat                  = (0, 0, 1)

    Returns array of shape (N, 3) with columns [n_cir, n_rad, n_z], to
    match the ``vec = [vec_cir, vec_rad, vec_z]`` ordering in
    fabric_getter.get_data_num().
    """
    pxy = np.linalg.norm(pos_xy, axis=1)
    keep = pxy > 1e-12
    n_g = n_global[keep]; pos_xy = pos_xy[keep]; pxy = pxy[keep]
    # fabric_getter.py:
    #   vec_pos_x = -pos_x / r  (inward radial component)
    #   vec_pos_y = -pos_y / r
    #   vec_rad = vec_pos_x * vec_x + vec_pos_y * vec_y
    #   vec_cir = vec_pos_y * vec_x - vec_pos_x * vec_y
    inwx = -pos_xy[:, 0] / pxy
    inwy = -pos_xy[:, 1] / pxy
    n_rad = inwx * n_g[:, 0] + inwy * n_g[:, 1]
    n_cir = inwy * n_g[:, 0] - inwx * n_g[:, 1]
    n_z   = n_g[:, 2]
    return np.column_stack([n_cir, n_rad, n_z]), keep


def bin_histogram(n_local: np.ndarray, weight: np.ndarray,
                  n_u: int = NUMBER_U, n_v: int = NUMBER_V) -> np.ndarray:
    """Bin contact normals into (n_u, n_v) histogram with antipodal
    symmetry.  Reproduces fabric_getter.get_data_num() bin selection and
    the +1/+1 antipodal duplication, but with a generic per-contact
    weight (1 for count, |F_n| for force).
    """
    arr = np.zeros((n_u, n_v), dtype=float)

    # Edge case: pole (vec_x == 0 == vec_y) — distribute over polar caps.
    # Following fabric_getter.py: split the weight evenly across all u
    # at the two poles (n=0 and n=n_v-1).
    pole = (np.abs(n_local[:, 0]) < 1e-12) & (np.abs(n_local[:, 1]) < 1e-12)
    if pole.any():
        w_pole = weight[pole].sum() / n_u
        arr[:, 0]      += w_pole
        arr[:, n_v - 1] += w_pole
    nl = n_local[~pole]; w = weight[~pole]

    # Azimuthal angle u_con in [0, 2*pi)
    horiz = np.sqrt(nl[:, 0] ** 2 + nl[:, 1] ** 2)
    cos_u = nl[:, 0] / horiz
    sin_u = nl[:, 1] / horiz
    u_con = np.arccos(np.clip(cos_u, -1.0, 1.0))
    u_con = np.where(sin_u < 0, 2.0 * np.pi - u_con, u_con)

    # Polar angle v_con in [0, pi]
    v_con = np.arccos(np.clip(nl[:, 2], -1.0, 1.0))
    # Avoid v_con == pi exactly snapping to v-bin index n_v.
    v_con = np.where(np.isclose(v_con, np.pi), np.pi - (np.pi / n_v) * 0.1, v_con)

    # Bin indices
    m_idx = np.minimum((u_con / (2.0 * np.pi / n_u)).astype(int), n_u - 1)
    n_idx = np.minimum((v_con / (np.pi / n_v)).astype(int), n_v - 1)

    # Antipodal indices, matching fabric_getter.py:
    #   m' = (m + 1 + n_u/2) % n_u - 1
    #   n' = n_v - n - 1
    m_anti = (m_idx + 1 + n_u // 2) % n_u - 1
    n_anti = n_v - n_idx - 1

    # Accumulate (vectorised via np.add.at for repeated indices)
    np.add.at(arr, (m_idx, n_idx), w)
    np.add.at(arr, (m_anti, n_anti), w)

    return arr


def process_panel(sim_dir: str, t: int) -> None:
    csv_in = DATA_ROOT / sim_dir / "contact_full" / f"contact_{t}.csv"
    df = pd.read_csv(csv_in)
    df_bb = df[df["contact_type"] == "bb"].reset_index(drop=True)

    n_global = df_bb[["n_x", "n_y", "n_z"]].to_numpy()
    pos_xy   = df_bb[["pos_x", "pos_y"]].to_numpy()
    fn       = df_bb["fn"].to_numpy()

    n_local, keep = to_local_cir_rad(n_global, pos_xy)
    fn = fn[keep]
    w_count = np.ones_like(fn)

    arr_count    = bin_histogram(n_local, w_count)   # raw count per bin
    arr_fn_sum   = bin_histogram(n_local, fn)         # sum of F_n per bin
    # Mean F_n per contact in each bin; empty bins -> 0.
    with np.errstate(divide="ignore", invalid="ignore"):
        arr_fn_mean = np.where(arr_count > 0, arr_fn_sum / arr_count, 0.0)

    # Convert raw count into rho_c (paper Eq. for contact density per unit
    # solid angle).  v_center is the polar-angle center of each polar bin n;
    # azimuthal cross-section sin(v) varies along axis 1.
    du = 2.0 * np.pi / NUMBER_U
    dv = np.pi / NUMBER_V
    v_centers = (np.arange(NUMBER_V) + 0.5) * dv          # shape (n_v,)
    sinv      = np.sin(v_centers)
    domega    = sinv * du * dv                             # shape (n_v,)
    rho_c     = arr_count / (N_PARTICLES * domega[None, :])

    out_dir = csv_in.parent
    np.savetxt(out_dir / f"distCount_{t}.csv",
               rho_c.reshape(1, -1), fmt="%.6g", delimiter=",")
    np.savetxt(out_dir / f"distForce_{t}.csv",
               arr_fn_mean.reshape(1, -1), fmt="%.6g", delimiter=",")

    print(f"  {sim_dir} t={t:>4}  N_bb={len(df_bb):>6}  "
          f"max(rho_c)={rho_c.max():>5.2f}  "
          f"max(mean F_n)={arr_fn_mean.max():>6.3f} N")


def main() -> None:
    print(f"Binning to {NUMBER_U} x {NUMBER_V} = {NUMBER_U * NUMBER_V} bins; "
          f"antipodal symmetric.")
    for sim_dir, t in PANELS:
        process_panel(sim_dir, t)


if __name__ == "__main__":
    main()
