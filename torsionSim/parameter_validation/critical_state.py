"""Identify the critical state line (CSL) from the
to-critical-state monotonic-undrained torsional run.

Two-panel diagnostic figure:
  (a) p'-q effective stress path with CSL fit overlaid
  (b) q/p vs gamma, showing where the plateau locks in

Used as the source for Fig. 8(c) CSL slope (response letter R1.7),
and as a self-contained justification of M_cs in the manuscript.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DEFAULT_CSV = (
    "/Users/hanyusong/thesis/MicroLiq/torsionSim/parameter_validation/"
    "undrained_monotonic/to_critical_state/torsion_shear.csv"
)
LOCAL_OUT = Path(__file__).parent / "critical_state"

# Match validate_combined.py / numerical_verification.py typography.
AXLABEL_FS = 18
TICK_FS = 15
LEGEND_FS = 14
PANEL_FS = 16
GRID_KW = dict(color='grey', linestyle='--', lw=0.35, alpha=0.8)

# Critical-state range for the M_cs fit (deviatoric strain eps_q in %).
EPSQ_LO = 20.0    # %
EPSQ_HI = 40.0    # %
# Plot range cap: the run was carried further as a numerical-stability
# check, but the figure is restricted to the fit window since extending
# past 40% adds no information about M_cs and invites questions about
# strain ranges that lie outside any laboratory envelope.
EPSQ_PLOT_MAX = 40.0  # %


def add_panel_label(ax, label):
    ax.text(-0.0, 1.005, label, transform=ax.transAxes,
            ha='left', va='bottom',
            fontsize=PANEL_FS, fontweight='bold', clip_on=False)


def style(ax):
    ax.tick_params(axis='both', which='major', labelsize=TICK_FS)
    ax.grid(axis='both', which='major', **GRID_KW)


def hca_invariants(df: pd.DataFrame):
    sz = df['stress_z'] / 1e3
    so = df['stress_outer'] / 1e3
    si = df['stress_inner'] / 1e3
    R = df['rad_outer']
    r = df['rad_inner']
    tau = df['stress_shear'] / 1e3
    s_r = (so * R + si * r) / (R + r)
    s_th = (so * R - si * r) / (R - r)
    s1 = (sz + s_th) / 2.0 + np.sqrt(((sz - s_th) / 2.0) ** 2 + tau ** 2)
    s3 = (sz + s_th) / 2.0 - np.sqrt(((sz - s_th) / 2.0) ** 2 + tau ** 2)
    s2 = s_r
    p = (si + so + sz) / 3.0
    q = np.sqrt(0.5 * ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s3 - s2) ** 2))
    return p.to_numpy(), q.to_numpy()


def make_figure(csv_path: str, out_stem: Path):
    df = pd.read_csv(csv_path)
    p, q = hca_invariants(df)
    eps_q = df['strain_dev'].to_numpy() * 100.0   # %
    eta = q / p

    # Restrict to the visible/fit range; the M_cs estimate is unchanged
    # (the plateau is steady) but downstream plotting is bounded.
    keep = eps_q <= EPSQ_PLOT_MAX
    p, q, eps_q, eta = p[keep], q[keep], eps_q[keep], eta[keep]

    mask = (eps_q >= EPSQ_LO) & (eps_q <= EPSQ_HI)
    M_cs = float(eta[mask].mean())
    M_std = float(eta[mask].std())
    phi_cs = float(np.degrees(np.arcsin(M_cs / np.sqrt(3.0))))
    print(f'plateau eps_q in [{EPSQ_LO},{EPSQ_HI}] %  (N={mask.sum()})')
    print(f'  M_cs   = {M_cs:.4f} +/- {M_std:.4f}')
    print(f'  phi_cs = {phi_cs:.2f} deg (pure shear, sqrt(3)*sin(phi))')

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.0, 4.9))

    # --- (a) p-q path with CSL ---
    ax_a.plot(p, q, color='tab:blue', lw=1.6,
              label=r'$DEM\ monotonic\ undrained$')
    ax_a.plot(p[mask], q[mask], color='tab:red', lw=2.4,
              label=fr'$Critical\ state:\ \epsilon_q\in[{EPSQ_LO:.0f},{EPSQ_HI:.0f}]\%$')

    p_max = float(np.max(p)) * 1.05
    p_csl = np.linspace(0.0, p_max, 50)
    ax_a.plot(p_csl, M_cs * p_csl, color='black', lw=1.4, ls='--',
              label=fr'$CSL:\ q={M_cs:.3f}\,p^{{\prime}}$')

    ax_a.set_xlim(0.0, p_max)
    ax_a.set_ylim(0.0, max(q.max(), M_cs * p_max) * 1.10)
    ax_a.set_xlabel(r"$Mean\ effective\ stress\ p^{\prime}\ (kPa)$",
                    fontsize=AXLABEL_FS)
    ax_a.set_ylabel(r"$Deviatoric\ stress\ q\ (kPa)$",
                    fontsize=AXLABEL_FS)
    ax_a.legend(fontsize=LEGEND_FS - 1, loc='upper left',
                frameon=False)
    style(ax_a)
    add_panel_label(ax_a, '(a)')

    # --- (b) q/p vs eps_q ---
    ax_b.plot(eps_q, eta, color='tab:blue', lw=1.4,
              label=r'$q/p^{\prime}\ (DEM)$')
    ax_b.plot(eps_q[mask], eta[mask], color='tab:red', lw=2.4,
              label=fr'$Critical\ state:\ \epsilon_q\in[{EPSQ_LO:.0f},{EPSQ_HI:.0f}]\%$')
    ax_b.axhline(M_cs, color='black', ls='--', lw=1.4,
                 label=fr'$M_{{cs}}={M_cs:.3f}$')

    # Annotate phi_cs (upper-right, vacated by the relocated legend)
    ax_b.text(0.97, 0.97,
              fr'$\varphi_{{cs}}={phi_cs:.1f}^{{\circ}}$'
              '\n'
              fr'$(pure\ shear,\ b\!=\!0.5)$',
              transform=ax_b.transAxes,
              ha='right', va='top', fontsize=LEGEND_FS,
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='grey',
                        alpha=0.85))

    ax_b.set_xlim(0.0, eps_q.max())
    ax_b.set_ylim(0.0, max(1.4, eta.max() * 1.08))
    ax_b.set_xlabel(r"$Deviatoric\ strain\ \epsilon_q\ (\%)$",
                    fontsize=AXLABEL_FS)
    ax_b.set_ylabel(r"$Stress\ ratio\ q/p^{\prime}$",
                    fontsize=AXLABEL_FS)
    ax_b.legend(fontsize=LEGEND_FS - 1, loc='lower right',
                frameon=False)
    style(ax_b)
    add_panel_label(ax_b, '(b)')

    plt.tight_layout()
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    pdf = out_stem.with_suffix('.pdf')
    png = out_stem.with_suffix('.png')
    plt.savefig(pdf, bbox_inches='tight')
    plt.savefig(png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {pdf}')
    print(f'wrote {png}')
    return pdf, png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default=DEFAULT_CSV)
    ap.add_argument('--out', default=str(LOCAL_OUT))
    args = ap.parse_args()
    make_figure(args.csv, Path(args.out))


if __name__ == '__main__':
    main()
