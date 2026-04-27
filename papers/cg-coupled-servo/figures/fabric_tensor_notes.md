# Count fabric vs force fabric — what each one means and how they connect to the rose diagrams

A self-contained walkthrough for `anisotropy_values.py`, `bin_contacts.py`,
`torsion_resisting_force.py`, and the four rose-related figures
(Fig 14 count rose, Fig 15 force rose, Fig:fabric_mechanism panel b).

## 0. What's a contact, what's its force?

For each ball-ball contact $c$ in the assembly, PFC gives us:

- $\bm{n}^c = (n_x, n_y, n_z)$ — the **unit** contact normal, $\|\bm{n}^c\| = 1$
- $f_n^c$ — the scalar magnitude of the normal force at that contact (units: N)

The full normal-force vector is $f_n^c \, \bm{n}^c$. We rotate $\bm{n}^c$ from the
global frame to the local cylindrical frame $(\hat\theta, \hat r, \hat z)$ via
the contact position; from now on $n_\theta^c, n_r^c, n_z^c$ are the components
in that local frame.

## 1. Two fabric tensors

### 1a. Count fabric

$$
\Phi_{ij} = \frac{1}{N_c} \sum_{c=1}^{N_c} n_i^c\, n_j^c
$$

Every contact contributes equally (weight 1). $\Phi$ is the **second moment of
contact orientation** — a purely geometric / topological object. Trace = 1
because $n_i n_i = |\bm{n}|^2 = 1$.

### 1b. Force-weighted fabric

$$
\Phi^f_{ij} = \frac{\sum_c f_n^c\, n_i^c\, n_j^c}{\sum_c f_n^c}
$$

Each contact contributes with weight $f_n^c$ (its normal-force magnitude). Trace
also = 1.

### 1c. Where is the force in $\Phi^f$?

The force $f_n^c$ appears as a **weight in front of $n_i n_j$ in every term of
the sum**:

$$
\sum_c f_n^c (n_r^c)^2 = f_n^{(1)}(n_r^{(1)})^2 + f_n^{(2)}(n_r^{(2)})^2 + \cdots
$$

Force is _not_ ignored in the sum; it controls how loudly each contact speaks.

The denominator $\sum_c f_n^c$ is just the total normal-force budget, used to
make $\Phi^f$ dimensionless and to sum to 1 along its diagonal.

## 2. A 4-contact toy that makes it concrete

| $c$ | $\hat{\bm n}^c$ | $f_n^c$ (N) | $(n_r^c)^2$ | $f_n^c (n_r^c)^2$ |
|---|---|---|---|---|
| 1 | $\hat r$ | 0.1 | 1 | 0.1 |
| 2 | $\hat r$ | 0.1 | 1 | 0.1 |
| 3 | $\hat z$ | 1.0 | 0 | 0 |
| 4 | $\hat z$ | 1.0 | 0 | 0 |

Count fabric:

$$
\Phi_{rr} = \tfrac{1+1+0+0}{4} = 0.50 \quad \text{(half the contacts are radial)}
$$

Force fabric:

$$
\Phi^f_{rr} = \tfrac{0.1+0.1+0+0}{0.1+0.1+1+1} = \tfrac{0.2}{2.2} \approx 0.09
\quad \text{(only 9\% of the load is in the radial direction)}
$$

The two metrics differ by 5×. They differ exactly because $f_n^c$ is _correlated_
with $\bm{n}^c$ here: radial contacts carry small force, axial contacts carry
large force. If the forces were uniform ($f_n^c = f$ for all $c$), the $f$
would factor out of both numerator and denominator and we'd recover
$\Phi^f_{rr} = \Phi_{rr}$ — that's the "constant-force limit" used as a sanity
check, not as a typical state of affairs.

## 3. How $\Phi^f$ connects to the rose diagrams

The 36×18 binning produces, per bin (a small angular patch on the sphere):

- $N_{\text{bin}}$ — number of contacts whose normal lands in that bin
- $\bar{f}_n^{\text{bin}} = (\sum_{c \in \text{bin}} f_n^c) / N_{\text{bin}}$ — mean normal force per contact in that bin

The two rose figures visualise these two quantities **separately**:

- **Count rose** (Fig 14, `distCount_<t>.csv`): $\rho_c \propto N_{\text{bin}}/\sin v$
- **Force rose** (Fig 15, `distForce_<t>.csv`): $\bar{f}_n^{\text{bin}}$

Now rewrite the per-contact sum in $\Phi^f$ as a per-bin sum (regrouping the
$N_c$ contacts by which bin they land in):

$$
\sum_c f_n^c (n_r^c)^2 \;=\; \sum_{\text{bin}} N_{\text{bin}} \, \bar{f}_n^{\text{bin}} \, (n_r^{\text{bin}})^2
$$

So the integrand of $\Phi^f$ pairs **count rose × force rose** at each angular
bin, then weights by direction. **Neither rose alone equals $\Phi^f$**; you need
the product.

This is why the force rose by itself doesn't visually equal $\Phi^f$ — the rose
shows you only the $\bar{f}_n^{\text{bin}}$ factor. The other factor
($N_{\text{bin}}$, i.e., the count rose) is also needed to assemble $\Phi^f$.

## 4. So how _does_ Fig 15 connect to the new mechanism plot?

Through the scalar invariants of $\Phi^f$:

| Object | Where it appears | What it is |
|---|---|---|
| $A_n = \sqrt{3/2}\,\|\Phi^f - I/3\|_F$ | Fig 15 panel annotations | deviator invariant of $\Phi^f$ |
| $B_n = \arccos\|\bm v_{\max}\!\cdot\!\hat z\|$ | Fig 15 panel annotations | tilt of $\Phi^f$'s top eigenvector |
| $\Phi^f_{rr}$ | Fig:fabric_mechanism panel b | $(r,r)$ diagonal of $\Phi^f$ |

All three are **scalars derived from the same tensor** $\Phi^f$ — different
projections of the same object. Fig 15 communicates $\Phi^f$ via $A_n, B_n$ in
text annotations; the mechanism plot communicates $\Phi^f$ via the $(r,r)$
projection across the K0–Dr grid. They are consistent by construction.

If we wanted Fig 15's _colormap_ to directly correspond to $\Phi^f$'s
integrand, we'd plot per-bin **sum** of force ($N_{\text{bin}} \bar{f}_n^{\text{bin}}$)
instead of per-bin **mean**. We deliberately chose the mean so the colormap
isolates "angular force pattern" from "angular count pattern" — a diagnostic
choice that trades off direct visual correspondence with $\Phi^f$ for cleaner
separation of concerns.

## 5. Why the force fabric is more sensitive to $K_0$ than the count fabric

In the expanded dataset (`torsion_resisting_force.csv`), at $N/N_L = 0$:

| | $K_0=0.5$ | $K_0=2.0$ | range |
|---|---|---|---|
| $1 - \Phi_{rr}$ | 0.683 | 0.673 | 0.010 (1.5%) |
| $1 - \Phi^f_{rr}$ | 0.733 | 0.642 | 0.091 (14%) |

The force fabric responds ~9× more strongly. Why: $K_0$ consolidation produces
**force chains** along the major principal stress direction. Force chains mean
that the per-bin mean force $\bar{f}_n^{\text{bin}}$ is itself strongly
anisotropic, even when the per-bin contact count $N_{\text{bin}}$ is nearly
isotropic. The count rose is nearly featureless across $K_0$; the force rose
has clear directional structure. Multiplying the two amplifies the directional
signal in $\Phi^f$ relative to $\Phi$.

## 6. The (r,r) projection and torsion resistance

Applied torsion $\tau_{z\theta}$ acts in the $(z, \theta)$ plane. A contact's
normal projection onto that plane has length $\sqrt{n_z^2 + n_\theta^2}$;
purely radial contacts ($n_z = n_\theta = 0$) have zero projection and cannot
participate in transmitting $\tau_{z\theta}$. So the **torsion-resisting share**
of force is

$$
\Phi^f_{zz} + \Phi^f_{\theta\theta} = 1 - \Phi^f_{rr},
$$

which is the y-axis of Fig:fabric_mechanism panel b. Reading the table above:
the $K_0 = 0.5$ specimen has 73% of its load already in the working plane of
$\tau_{z\theta}$; the $K_0 = 2.0$ specimen has only 64%. The remaining fraction
($\Phi^f_{rr}$) is locked in the radial direction — geometrically inert with
respect to the applied shear.

## 7. Files

- `anisotropy_values.py` — computes $A_c, B_c, A_n, B_n, \langle f_n\rangle$ for the 8 panels of Figs 14 and 15
- `bin_contacts.py` — builds the 36×18 histograms for the rose renderer
- `torsion_resisting_force.py` — computes $\Phi_{rr}, \Phi^f_{rr}$ for the 10-case expanded set
- `fig_fabric_schematic.py` — renders the mechanism figure (panel a + dual-axis panel b)
- `torsion_resisting_force.csv` — full numerical output
- `torsion_resisting_force.tex` — LaTeX `\newcommand` macros for inclusion in the manuscript
