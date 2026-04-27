# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pandas"]
# ///
"""
Compute fabric-tensor anisotropy invariants A_c, B_c, A_n, B_n on the
contact snapshots used by Fig. 14 (contact-density rose) and the
force-rose figure planned for R2.7, and emit them as LaTeX macros that
``fig_contact_density_standalone.tex`` (and the future force-rose
standalone) consume via ``\\input{anisotropy_values.tex}``.

Input: ``contact_<t>.csv`` files written by the PFC extraction script in
``torsionSim/cyclic_shear/.../contact_full/`` with columns

    contact_type, pos_x, pos_y, pos_z, n_x, n_y, n_z, fn, ft

where ``contact_type`` is 'bb' (ball-ball) or 'bf' (ball-facet),
``(n_x, n_y, n_z)`` is the unit contact normal from PFC's
``contact.normal()``, and ``fn``, ``ft`` are scalar normal and
tangential force magnitudes.  Following the standard fabric-anisotropy
literature (Satake 1982; Oda 1985) and matching ``fabric_getter.py``
(which already filters BallBallContact for ``distContacts.csv``), the
fabric tensor here is computed on **ball-ball contacts only**;
ball-facet contacts represent boundary loading rather than the
granular skeleton's structure and are excluded by default.

Definitions (local cylindrical frame ($\\theta$, $r$, $z$)):

    F_c = (1 / N_c)   sum_c n_c n_c^T              (count-weighted)
    F_n = (1 / sum f_n) sum_c f_n^c n_c n_c^T       (normal-force-weighted,
                                                     Zhou 2022 / Song 2024)
    A   = sqrt(3/2) || F - I/3 ||_F                 (deviator invariant)
    B   = arccos(|v_top . z_hat|)                   (tilt of largest eigvec)

Run:  uv run anisotropy_values.py
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

DATA_ROOT = Path("/Users/hanyusong/thesis/MicroLiq/torsionSim/cyclic_shear")
OUT_TEX = Path(__file__).resolve().parent / "anisotropy_values.tex"

# Eight (panel-row, panel-col, simulation-dir, timestep, N/N_L) tuples
# matching the layout of fig_contact_density_standalone.tex.
PANELS = [
    ("a", "i",   "Dr90/k0.50/csr_0.200", 0,   "0.00"),
    ("a", "ii",  "Dr90/k0.50/csr_0.200", 302, "0.61"),
    ("a", "iii", "Dr90/k0.50/csr_0.200", 523, "1.05"),
    ("a", "iv",  "Dr90/k0.50/csr_0.200", 529, "1.07"),
    ("b", "i",   "Dr90/k2.00/csr_0.200", 0,   "0.00"),
    ("b", "ii",  "Dr90/k2.00/csr_0.200", 226, "0.61"),
    ("b", "iii", "Dr90/k2.00/csr_0.200", 379, "1.05"),
    ("b", "iv",  "Dr90/k2.00/csr_0.200", 386, "1.07"),
]


def to_local_normals(n_global: np.ndarray, pos: np.ndarray) -> np.ndarray:
    """Rotate unit normals from global (x, y, z) to local cylindrical
    (theta, r, z), per fabric_getter.py / distContacts.csv convention.
    """
    pxy = np.linalg.norm(pos[:, :2], axis=1)
    keep = pxy > 1e-12
    n_g = n_global[keep]; p = pos[keep]; pxy = pxy[keep]
    rx, ry = p[:, 0] / pxy, p[:, 1] / pxy           # outward radial
    tx, ty = -p[:, 1] / pxy, p[:, 0] / pxy          # CCW circumferential
    n_theta = n_g[:, 0] * tx + n_g[:, 1] * ty
    n_r     = n_g[:, 0] * rx + n_g[:, 1] * ry
    n_z     = n_g[:, 2]
    return np.column_stack([n_theta, n_r, n_z]), keep


def fabric_invariants(n_local: np.ndarray, weight: np.ndarray | None):
    """(A, B_deg) for unit normals in (theta, r, z) frame."""
    if weight is None:
        F = np.einsum("ki,kj->ij", n_local, n_local) / len(n_local)
    else:
        F = np.einsum("k,ki,kj->ij", weight, n_local, n_local) / weight.sum()
    dev = F - np.eye(3) / 3.0
    A = float(np.sqrt(1.5 * np.sum(dev * dev)))
    eigvals, eigvecs = np.linalg.eigh(F)
    v_top = eigvecs[:, -1]
    B = float(np.degrees(np.arccos(np.clip(abs(v_top[2]), 0.0, 1.0))))
    return A, B


def compute_panel(sim_dir: str, t: int) -> dict:
    csv_path = DATA_ROOT / sim_dir / "contact_full" / f"contact_{t}.csv"
    df = pd.read_csv(csv_path)
    df_bb = df[df["contact_type"] == "bb"].reset_index(drop=True)

    n_global = df_bb[["n_x", "n_y", "n_z"]].to_numpy()
    pos      = df_bb[["pos_x", "pos_y", "pos_z"]].to_numpy()
    fn       = df_bb["fn"].to_numpy()

    n_local, keep = to_local_normals(n_global, pos)
    fn = fn[keep]

    Ac, Bc = fabric_invariants(n_local, weight=None)
    An, Bn = fabric_invariants(n_local, weight=fn)
    Fbar = float(fn.mean())  # specimen-mean |F_n| over all bb contacts

    # Diagnostic: include ball-facet for cross-check (NOT used in figure)
    n_g_all = df[["n_x", "n_y", "n_z"]].to_numpy()
    pos_all = df[["pos_x", "pos_y", "pos_z"]].to_numpy()
    fn_all  = df["fn"].to_numpy()
    nl_all, keep_all = to_local_normals(n_g_all, pos_all)
    fn_all = fn_all[keep_all]
    Ac_all, Bc_all = fabric_invariants(nl_all, weight=None)
    An_all, Bn_all = fabric_invariants(nl_all, weight=fn_all)

    return {
        "Nbb": len(df_bb), "Nbf": len(df) - len(df_bb),
        "Ac": Ac, "Bc": Bc, "An": An, "Bn": Bn, "Fbar": Fbar,
        "Ac_all": Ac_all, "Bc_all": Bc_all,
        "An_all": An_all, "Bn_all": Bn_all,
    }


def fmt_A(x: float) -> str:
    return f"{x:.2f}"


def fmt_B(x: float) -> str:
    return f"{int(round(x))}"


def main() -> None:
    rows = [(row, col, sim_dir, t, nnL, compute_panel(sim_dir, t))
            for row, col, sim_dir, t, nnL in PANELS]

    # Console: ball-ball reported values + ball-facet diagnostic
    hdr = (f"{'panel':>5} {'sim':>22} {'t':>5} {'N/N_L':>6} "
           f"{'N_bb':>7} {'N_bf':>5}  "
           f"|  ball-ball:    {'A_c':>6} {'B_c°':>6} {'A_n':>6} {'B_n°':>6} {'<|F_n|>':>7}  "
           f"|  bb+bf check:  {'A_c':>6} {'B_c°':>6} {'A_n':>6} {'B_n°':>6}")
    print(hdr)
    for row, col, sim_dir, t, nnL, r in rows:
        print(f"  {row}{col:<3} {sim_dir:>22} {t:>5} {nnL:>6} "
              f"{r['Nbb']:>7} {r['Nbf']:>5}  "
              f"|                "
              f"{r['Ac']:6.3f} {r['Bc']:6.1f} {r['An']:6.3f} {r['Bn']:6.1f} {r['Fbar']:7.3f}  "
              f"|                "
              f"{r['Ac_all']:6.3f} {r['Bc_all']:6.1f} "
              f"{r['An_all']:6.3f} {r['Bn_all']:6.1f}")

    # Emit LaTeX include — only the ball-ball values reach the figure.
    lines = [
        "% Auto-generated by anisotropy_values.py — do not edit by hand.",
        "% Source: contact_<t>.csv files written by the PFC extraction script.",
        "% Fabric tensor uses ball-ball contacts only (Satake 1982 / Oda 1985);",
        "% ball-facet contacts represent boundary loading and are excluded.",
        "%",
        "% Macro naming: \\<Quantity><row><col>",
        "%   Quantity in {Ac, Bc, An, Bn, Fbar}",
        "%     A   = sqrt(3/2) || F - I/3 ||_F           (deviator invariant)",
        "%     B   = arccos(|v_top . z_hat|)             (tilt from z, deg)",
        "%     Fbar = (1/N_bb) sum_c |F_n^c|             (specimen-mean |F_n|, N)",
        "%   row in {a (K0=0.5), b (K0=2.0)}",
        "%   col in {i, ii, iii, iv}  (panel index 1..4 across the row)",
        "%",
        "% Note: Fbar is a single scalar per panel (ensemble average over",
        "% every bb contact), distinct from the colorbar's per-orientation",
        "% mean F_n(theta, phi) which is a function of bin direction.",
        "",
    ]
    for row, col, sim_dir, t, nnL, r in rows:
        lines.append(f"% {sim_dir}, t={t} (N/N_L={nnL})")
        lines.append(f"\\newcommand{{\\Ac{row}{col}}}{{{fmt_A(r['Ac'])}}}")
        lines.append(f"\\newcommand{{\\Bc{row}{col}}}{{{fmt_B(r['Bc'])}}}")
        lines.append(f"\\newcommand{{\\An{row}{col}}}{{{fmt_A(r['An'])}}}")
        lines.append(f"\\newcommand{{\\Bn{row}{col}}}{{{fmt_B(r['Bn'])}}}")
        lines.append(f"\\newcommand{{\\Fbar{row}{col}}}{{{r['Fbar']:.2f}}}")
        lines.append("")

    OUT_TEX.write_text("\n".join(lines))
    print(f"\nWrote {OUT_TEX}")


if __name__ == "__main__":
    main()
