"""
Schematic figure for fabric tensor decomposition mechanism.
Panel (a): Cylindrical element showing τ_zθ and active/neutral contact directions
Panel (b): Dual-axis comparison of count- and force-weighted torsion-resisting
           fractions across the expanded simulation set (2 D_r x 5 K_0).
           Numerical values are read from torsion_resisting_force.csv (bb-only).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ── Style ──
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'mathtext.fontset': 'cm',
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
})

# Colors
C_ACTIVE = '#2166AC'    # blue - torsion-resisting (z, θ)
C_NEUTRAL = '#D6604D'   # red  - mechanically neutral (r)
C_STRESS = '#333333'    # dark gray for stress arrows
C_ZZ = '#4393C3'
C_TT = '#92C5DE'
C_RR = '#D6604D'

fig = plt.figure(figsize=(6.5, 3.0))

# ═══════════════════════════════════════════════════════════════
# Panel (a): 3D cylindrical element with stress and contact info
# ═══════════════════════════════════════════════════════════════
ax1 = fig.add_axes([0.0, 0.0, 0.45, 1.0], projection='3d')
ax1.set_box_aspect([1.0, 1.0, 1.3])

# Draw a curved cylindrical element (sector of annulus)
# Parameters
r_in, r_out = 0.6, 1.0
theta_start, theta_end = 0, np.pi / 3
z_bot, z_top = 0.6, 1.2
n_arc = 20

theta = np.linspace(theta_start, theta_end, n_arc)

def arc_points(r, th, z):
    return r * np.cos(th), r * np.sin(th), np.full_like(th, z)

# Bottom face
x_in_b, y_in_b, z_in_b = arc_points(r_in, theta, z_bot)
x_out_b, y_out_b, z_out_b = arc_points(r_out, theta, z_bot)

# Top face
x_in_t, y_in_t, z_in_t = arc_points(r_in, theta, z_top)
x_out_t, y_out_t, z_out_t = arc_points(r_out, theta, z_top)

# Draw curved surfaces as wireframe
alpha_wire = 0.5
lw = 0.7
c_wire = '#555555'

# Inner curved surface
for i in range(n_arc - 1):
    verts = [
        [x_in_b[i], y_in_b[i], z_in_b[i]],
        [x_in_b[i+1], y_in_b[i+1], z_in_b[i+1]],
        [x_in_t[i+1], y_in_t[i+1], z_in_t[i+1]],
        [x_in_t[i], y_in_t[i], z_in_t[i]],
    ]
    poly = Poly3DCollection([verts], alpha=0.05, facecolor='#cccccc',
                            edgecolor=c_wire, linewidth=lw * 0.3)
    ax1.add_collection3d(poly)

# Outer curved surface
for i in range(n_arc - 1):
    verts = [
        [x_out_b[i], y_out_b[i], z_out_b[i]],
        [x_out_b[i+1], y_out_b[i+1], z_out_b[i+1]],
        [x_out_t[i+1], y_out_t[i+1], z_out_t[i+1]],
        [x_out_t[i], y_out_t[i], z_out_t[i]],
    ]
    poly = Poly3DCollection([verts], alpha=0.05, facecolor='#cccccc',
                            edgecolor=c_wire, linewidth=lw * 0.3)
    ax1.add_collection3d(poly)

# Side faces (radial cuts)
for th_idx in [0, -1]:
    verts = [
        [x_in_b[th_idx], y_in_b[th_idx], z_in_b[th_idx]],
        [x_out_b[th_idx], y_out_b[th_idx], z_out_b[th_idx]],
        [x_out_t[th_idx], y_out_t[th_idx], z_out_t[th_idx]],
        [x_in_t[th_idx], y_in_t[th_idx], z_in_t[th_idx]],
    ]
    poly = Poly3DCollection([verts], alpha=0.05, facecolor='#cccccc',
                            edgecolor=c_wire, linewidth=lw)
    ax1.add_collection3d(poly)

# Top face
verts_top = list(zip(x_out_t, y_out_t, z_out_t)) + \
            list(zip(x_in_t[::-1], y_in_t[::-1], z_in_t[::-1]))
poly = Poly3DCollection([verts_top], alpha=0.06, facecolor='#cccccc',
                        edgecolor=c_wire, linewidth=lw * 0.3)
ax1.add_collection3d(poly)

# Bottom face
verts_bot = list(zip(x_out_b, y_out_b, z_out_b)) + \
            list(zip(x_in_b[::-1], y_in_b[::-1], z_in_b[::-1]))
poly = Poly3DCollection([verts_bot], alpha=0.06, facecolor='#cccccc',
                        edgecolor=c_wire, linewidth=lw * 0.3)
ax1.add_collection3d(poly)

def draw_arrow_3d(ax, start, direction, perp, length=0.28, head_frac=0.25,
                  lw=1.2, color='k'):
    """Draw a 3D arrow with controllable arrowhead orientation.
    perp: vector perpendicular to direction, defines the arrowhead plane."""
    end = start + direction / np.linalg.norm(direction) * length
    shaft_end = start + direction / np.linalg.norm(direction) * length * (1 - head_frac)
    ax.plot(*zip(start, shaft_end), color=color, linewidth=lw)
    head_half = np.linalg.norm(direction) * length * head_frac * 0.18
    perp_unit = perp / np.linalg.norm(perp)
    tip = end
    base1 = shaft_end + perp_unit * head_half
    base2 = shaft_end - perp_unit * head_half
    tri = Poly3DCollection([[tip, base1, base2]], alpha=0.9,
                            facecolor=color, edgecolor=color, linewidth=0.5)
    ax.add_collection3d(tri)

# ── Coordinate axes ──
r_mid = (r_in + r_out) / 2
th_mid = (theta_start + theta_end) / 2
z_mid = (z_bot + z_top) / 2
origin = np.array([r_mid * np.cos(th_mid), r_mid * np.sin(th_mid), z_mid])

# r direction (outward radial)
r_dir = np.array([np.cos(th_mid), np.sin(th_mid), 0])
# θ direction (tangential, counterclockwise)
t_dir = np.array([-np.sin(th_mid), np.cos(th_mid), 0])
# z direction (vertical)
z_dir = np.array([0, 0, 1])

arrow_len = 0.45
arrow_kw = dict(arrow_length_ratio=0.15, linewidth=1.5)

# r-axis (neutral - red)
ax1.quiver(*origin, *(r_dir * arrow_len), color=C_NEUTRAL, **arrow_kw)
ax1.text(*(origin + r_dir * (arrow_len + 0.12)),
         r'$r$', color=C_NEUTRAL, fontsize=11, fontweight='bold',
         ha='center', va='center')

# θ-axis (active - blue)
ax1.quiver(*origin, *(t_dir * arrow_len), color=C_ACTIVE, **arrow_kw)
ax1.text(*(origin + t_dir * (arrow_len + 0.12)),
         r'$\theta$', color=C_ACTIVE, fontsize=11, fontweight='bold',
         ha='center', va='center')

# z-axis (active - blue) — custom arrow so head face is visible
draw_arrow_3d(ax1, origin, z_dir, r_dir, length=arrow_len,
              head_frac=0.15, lw=1.5, color=C_ACTIVE)
ax1.text(*(origin + z_dir * (arrow_len + 0.10)),
         r'$z$', color=C_ACTIVE, fontsize=11, fontweight='bold',
         ha='center', va='center')

# ── τ_zθ stress arrows on top face (θ direction) ──
n_stress = 4

top_starts = []
for i, frac in enumerate(np.linspace(0.2, 0.8, n_stress)):
    r_pos = r_in + frac * (r_out - r_in)
    pos = np.array([r_pos * np.cos(th_mid), r_pos * np.sin(th_mid), z_top])
    top_starts.append(pos)
    draw_arrow_3d(ax1, pos, t_dir, z_dir, color=C_STRESS)
# Baseline connecting arrow tails (distributed stress convention)
top_starts = np.array(top_starts)
ax1.plot(top_starts[:, 0], top_starts[:, 1], top_starts[:, 2],
         color=C_STRESS, linewidth=1.0)

# Label τ_zθ — at the tip of the top-face arrows (θ direction end)
r_label = r_in + 0.8 * (r_out - r_in)  # align with last arrow
arrow_tip = np.array([r_label * np.cos(th_mid), r_label * np.sin(th_mid), z_top])
label_offset = t_dir * 0.32 - r_dir * 0.15  # past arrowhead, shifted inward
stress_label_pos = arrow_tip + label_offset
ax1.text(*stress_label_pos, r'$\tau_{z\theta}$', color=C_STRESS,
         fontsize=11, ha='left', va='center')

# ── Arrows along z direction on the θ-face (side), distributed along r ──
th_side = theta_end
r_dir_side = np.array([np.cos(th_side), np.sin(th_side), 0])
z_pos = z_bot + 0.35 * (z_top - z_bot)
side_starts = []
for frac in np.linspace(0.2, 0.8, n_stress):
    r_pos = r_in + frac * (r_out - r_in)
    pos = np.array([r_pos * np.cos(th_side), r_pos * np.sin(th_side), z_pos])
    side_starts.append(pos)
    draw_arrow_3d(ax1, pos, z_dir, r_dir_side, length=0.22, color=C_STRESS)
# Baseline connecting arrow tails
side_starts = np.array(side_starts)
ax1.plot(side_starts[:, 0], side_starts[:, 1], side_starts[:, 2],
         color=C_STRESS, linewidth=1.0)

# ── Legend / annotation (compact) ──
ax1.text2D(0.02, 0.14,
           r'Resisting: $z, \theta$ contacts'
           r'  |  Neutral: $r$ contacts'
           '\n'
           r'Count: $1 - \Phi_{rr}$    Force: $1 - \Phi_{rr}^{f}$',
           transform=ax1.transAxes, fontsize=6.5, color='#333333',
           va='top', linespacing=1.6)

# Clean up 3D axes
ax1.set_xlim(0.25, 1.05)
ax1.set_ylim(0.0, 0.85)
ax1.set_zlim(0.42, 1.32)
ax1.set_axis_off()
ax1.view_init(elev=30, azim=-0)
ax1.set_title('(a)', fontsize=8, loc='left', pad=-12)

# ═══════════════════════════════════════════════════════════════
# Panel (b): Dual y-axis line plot — count vs force torsion-resisting
# Data source: torsion_resisting_force.csv (bb-only, expanded set)
# ═══════════════════════════════════════════════════════════════
ax2 = fig.add_axes([0.55, 0.18, 0.40, 0.72])

data = pd.read_csv(Path(__file__).resolve().parent / 'torsion_resisting_force.csv')
data = data.sort_values(['Dr', 'K0']).reset_index(drop=True)
K0_vals = sorted(data['K0'].unique())
x = np.arange(len(K0_vals))

C_COUNT = '#666666'
C_FORCE = C_ACTIVE

def series(Dr: int, key: str) -> np.ndarray:
    return data[data['Dr'] == Dr].sort_values('K0')[key].to_numpy()

# Left axis: count-weighted 1 - Phi_rr
ax2.plot(x, series(90, 'one_minus_Phi_r'), color=C_COUNT, marker='o',
         markersize=4, linewidth=1.0, label=r'$1 - \Phi_{rr}$, $D_r$=90%')
ax2.plot(x, series(75, 'one_minus_Phi_r'), color=C_COUNT, marker='o',
         markerfacecolor='white', markersize=4, linewidth=1.0,
         label=r'$1 - \Phi_{rr}$, $D_r$=75%')
ax2.set_ylabel(r'Count $1 - \Phi_{rr}$', fontsize=8, color=C_COUNT)
ax2.tick_params(axis='y', labelsize=7, colors=C_COUNT)
ax2.spines['left'].set_color(C_COUNT)
ax2.set_ylim(0.660, 0.690)

# Right axis: force-weighted 1 - \Phi_{rr}^{f}
ax2b = ax2.twinx()
ax2b.plot(x, series(90, 'one_minus_Fn_r'), color=C_FORCE, marker='s',
          markersize=4, linewidth=1.0, label=r'$1 - \Phi_{rr}^{f}$, $D_r$=90%')
ax2b.plot(x, series(75, 'one_minus_Fn_r'), color=C_FORCE, marker='s',
          markerfacecolor='white', markersize=4, linewidth=1.0,
          label=r'$1 - \Phi_{rr}^{f}$, $D_r$=75%')
ax2b.set_ylabel(r'Force $1 - \Phi_{rr}^{f}$', fontsize=8, color=C_FORCE)
ax2b.tick_params(axis='y', labelsize=7, colors=C_FORCE)
ax2b.spines['right'].set_color(C_FORCE)
ax2b.spines['left'].set_color(C_COUNT)
ax2b.set_ylim(0.62, 0.75)

ax2.set_xticks(x)
ax2.set_xticklabels([f'{k0:.2g}' for k0 in K0_vals])
ax2.set_xlabel(r'$K_0$', fontsize=8)
ax2.tick_params(axis='x', labelsize=7)

# Combined legend
h1, l1 = ax2.get_legend_handles_labels()
h2, l2 = ax2b.get_legend_handles_labels()
ax2.legend(h1 + h2, l1 + l2, loc='lower left', fontsize=6.5,
           framealpha=0.9, handlelength=2.0)
ax2.set_title('(b)', fontsize=8, loc='left')
plt.savefig('/Users/hanyusong/thesis/MicroLiq/papers/cg-coupled-servo/figures/fabric_mechanism_schematic.png',
            dpi=600, bbox_inches='tight', facecolor='white')
print("Saved to figures/fabric_mechanism_schematic.png")
plt.show()
