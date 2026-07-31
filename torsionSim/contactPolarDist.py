# Author: https://github.com/yusong652
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class PolarDist:

    def __init__(self, file_name='distContacts.csv',
                 number_u=36, number_v=18, n_particles=53764,
                 density_max=0.5, density_min=0.0, resolution=8):
        self.number_u = number_u
        self.number_v = number_v
        self.n_particles = n_particles
        self.density_max = density_max
        self.density_min = density_min
        self.resolution = resolution

        self.df = pd.read_csv(file_name, header=0).to_numpy()
        self._precompute_mesh()

    def _precompute_mesh(self):
        """Pre-compute angular mesh and trig values (constant across frames)."""
        nu, nv, f = self.number_u, self.number_v, self.resolution

        # Build 1D angle arrays: each bin gets `f` points
        u_1d = np.concatenate([
            np.linspace(2 * np.pi * m / nu, 2 * np.pi * (m + 1) / nu, f)
            for m in range(nu)
        ])
        v_1d = np.concatenate([
            np.linspace(np.pi * n / nv, np.pi * (n + 1) / nv, f)
            for n in range(nv)
        ])

        # 2D mesh via broadcasting
        U = u_1d[:, None]  # (nu*f, 1)
        V = v_1d[None, :]  # (1, nv*f)

        # Cache trig (reused every frame)
        self._cos_U = np.cos(U)
        self._sin_U = np.sin(U)
        self._sin_V = np.sin(V)
        self._cos_V = np.cos(V)

        # Bin index lookup: mesh point i -> bin index m (or n)
        self._bin_m = np.repeat(np.arange(nu), f)  # (nu*f,)
        self._bin_n = np.repeat(np.arange(nv), f)  # (nv*f,)

    def _get_density(self, row_index):
        """Extract and reshape density for one timestep."""
        n = self.number_u * self.number_v
        raw = self.df[row_index][:n]
        return (raw / self.n_particles).reshape(self.number_u, self.number_v)

    def _render_frame(self, density, filename):
        """Render one frame with a single plot_surface call."""
        color_scalar = np.clip(
            density / (self.density_max - self.density_min), 0, 1
        )

        # Map bin-level values to full mesh via index broadcasting
        R = density[self._bin_m[:, None], self._bin_n[None, :]]
        C = color_scalar[self._bin_m[:, None], self._bin_n[None, :]]

        # Cartesian coordinates (vectorized)
        X = R * self._cos_U * self._sin_V
        Y = R * self._sin_U * self._sin_V
        Z = R * self._cos_V

        # Facecolors
        facecolors = plt.cm.rainbow(C)

        # Plot
        fig = plt.figure(figsize=(6., 6.))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_box_aspect((1, 1, 1))

        # rcount/ccount default to 50, which silently downsamples the mesh and
        # cuts across bin boundaries -> misaligned steps / fuzzy edges. Pass the
        # full mesh size so every bin boundary is rendered exactly.
        ax.plot_surface(X, Y, Z, facecolors=facecolors,
                        rcount=X.shape[0], ccount=X.shape[1],
                        edgecolor='none', linewidth=0, antialiased=False,
                        alpha=0.7)

        # Axes
        ax.set_xlabel(r"$x$", fontsize=16, labelpad=1)
        ax.set_ylabel(r"$y$", fontsize=16, labelpad=1)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel(r"$z$", fontsize=16, rotation=90, labelpad=1)
        dmax = self.density_max
        ax.set_xlim(-dmax, dmax)
        ax.set_ylim(-dmax, dmax)
        ax.set_zlim(-dmax, dmax)
        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.yaxis.set_major_formatter(plt.NullFormatter())
        ax.zaxis.set_major_formatter(plt.NullFormatter())
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.view_init(elev=15, azim=-110)

        # Colorbar
        sm = plt.cm.ScalarMappable(cmap=plt.cm.rainbow)
        sm.set_array(np.array([self.density_min, self.density_max]))
        cbaxes = fig.add_axes([0.85, 0.35, 0.02, 0.3])
        fig.colorbar(sm, cax=cbaxes).set_label(
            r"$Contact\ Density$", fontsize=15)

        plt.tight_layout()
        fig.savefig(filename, dpi=500)
        plt.close(fig)

    def get_dist_fig(self, time_increment=0.01):
        """Render all frames."""
        n_frames = len(self.df)
        for row in range(n_frames):
            density = self._get_density(row)
            time = row * time_increment
            filename = f"contact_density_time_{time:.3f}.jpg"
            self._render_frame(density, filename)
            if row % 50 == 0:
                print(f"Frame {row}/{n_frames}")


if __name__ == "__main__":
    polar_dist = PolarDist()
    polar_dist.get_dist_fig()
