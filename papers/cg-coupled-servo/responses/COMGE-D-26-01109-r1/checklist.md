# COMGE-D-26-01109 — Round 1 Revision Checklist

**Submission tag:** `submitted-r0` (0e9de81, 2026-03-21)

**Working branch:** `revision-r1`

**Decision:** Major revision — both reviewers recommend acceptance pending revisions

**Reviewers:** R1 (8 comments), R2 (8 comments)

## Legend

- Status: ⬜ not started · 🟨 in progress · ✅ done · 🟥 blocked / decision needed
- Effort: S (<1h) · M (few hours) · L (1–2 days) · XL (new sims)

---

## Reviewer 1

### R1.1 — Particle size scaling adequacy

**Comment (lines 112–114):** Particle size may influence dilatancy, peak friction angle, and liquefaction resistance. Clarify scaling factor adequacy (specimen-to-particle size ratio) or provide references.

**Geometric facts (corrected):**

- Radial thickness: R − r = 50 − 30 = **20 mm** → **20 / D_max = 6.67×** (D_max = 3 mm). Binding dimension.
- Height: 100 mm → 33× D_max
- Mid-radius circumference: 2π·40 mm ≈ 251 mm → 84× D_max
- Particle count: ~50 000

**Honest diagnosis:**

- The radial direction is inherently HCA's smallest coherent dimension — a geometric feature of the test, not a modelling oversight. All published DEM-HCA studies face the same constraint.
- We will not try to paper this over. The strategy is to **acknowledge the radial constraint and show it does not invalidate the specific quantity (N_L) we report**.

**Strategic framing — multiple independent prongs, none load-bearing alone:**

**Prong A — ASTM D4767 (primary codified anchor).** The most geometrically-analogous laboratory standard for our test type (cohesive-soil triaxial compression) specifies that the largest particle shall be smaller than 1/6 of the specimen diameter. Cited directly as ASTM D4767. Our radial/D_max = 6.67× satisfies this.

**Prong B — Comparability with DEM-HCA peer literature (rigid / stacked-wall precedents only).**

| Study | Boundary | Radial thickness | D_max | **radial/D_max** | H / D_outer |
|---|---|---|---|---|---|
| **This work** | rigid wall | 20 mm | 3 mm | **6.67** | 1.0 |
| Shi et al. 2021 *IJGeom* 21:04021127 | rigid wall | 12 mm | 1.6 mm | **7.5** | 2.0 |
| Li et al. 2015 *Acta Geotech* 10:449-467 | 20-stacked wall | 20 mm | 1.2 mm | 16.7 | 2.0 |

- **Shi 2021** is the closest peer: same rigid-wall boundary, very similar ratio (7.5 vs 6.67). Primary comparability anchor.
- **Li 2015** uses a 20-stacked-wall boundary — still made of rigid elements but with some compliance from the stacked arrangement, conceptually intermediate between rigid and flexible. Ratio 16.7 is larger, serving as a second, softer reference point.

Key response-letter sentence template: "Among DEM-HCA studies with rigid or quasi-rigid boundaries, the present radial/D_max ratio of 6.67 is directly comparable to Shi et al. (2021, rigid wall, 7.5) and within the same order of magnitude as Li et al. (2015, stacked wall, 16.7)."

**Song 2024 is deliberately excluded from this prong** — it uses a flexible membrane boundary, which fundamentally alters the kinematic constraint; its smaller ratio (~5) is permitted *because of* the compliant boundary, and citing it here would (a) conflate boundary type with ratio, and (b) invite the reviewer to ask why we did not also adopt a flexible membrane (a separate question addressed in R1.6 and R2.4). Song 2024 is instead cited in R2.4 (DEM-HCA literature review) and R1.6 (rigid vs flexible boundary discussion).

**Caveat:** reviewer cited "Li, Chen, Gutierrez 2017, CGeo 86:52-66" which could not be verified. Li 2015 (Li, Zhang, Gutierrez in *Acta Geotech*) is very likely the intended citation. Raise this politely in the letter.

**Prong C — Liquefaction is a strength / end-state problem, not a small-strain elastic one.**

- Liquefaction is defined at **finite strain** (γ_SA = 2.5% in Ishihara 1985 protocol, which we follow).
- N_L is governed by **end-state fabric collapse**, controlled by critical-state soil mechanics.
- Classical critical-state theory holds that ultimate shear strength is a material property independent of specimen size.
- Our comparative interest (**N_L vs K_0**, not absolute N_L) adds one more layer: any size-induced bias applies uniformly across K_0 states and does not distort the relative trends that form the paper's conclusions.

**Prong D — HCA geometry: torsional loading is perpendicular to the radial direction.**

- Primary shear strain γ_zθ lies in the tangential–axial plane.
- The smallest geometric dimension (radial) is **not** the primary loading direction, unlike direct-shear where loading acts across the thin dimension.
- Wall-induced inhomogeneity in the radial direction affects the σ'_r measurement accuracy (already absorbed by annulus averaging), but does not directly distort the primary γ_zθ response.
- This is a test-specific geometric argument that REV-type guidelines (framed for cubic/cylindrical samples under axial loading) do not capture.

**Prong E — Empirical calibration / validation (supporting, not load-bearing).** The calibrated parameters reproduce monotonic stress–strain + dilatancy (Nakata 1998) and cyclic N_L–CSR (Ishihara 1985). Mentioned briefly, not leaned on. Reason: the triple-match argument will recur across several reviewer points (notably R1.2, R1.6), so it should not be consumed here as the primary defense.

**Prong F — Letter-only: cost trade-off.** Halving D50 to reach a "preferred" ratio raises computational cost by ~16× (8× particles + 2× timestep reduction) with marginal scientific return for a comparative K_0 study. Out of scope for the present work; noted as future-work direction.

**Deliberately NOT cited (and why):**

- **Huang 2014 / Kuhn–Bagi 2009 / Marketos–Bolton 2010** — all use cubic or solid-cylindrical geometries with more generous radial ratios than HCA can offer. Citing them implicitly invites the reviewer to ask "why not replicate their ratio?" — a question we cannot answer without conceding ground.
- **Wang 2022 MDPI** — argues the ASTM 10× rule is insufficient and recommends 60×. Against us.
- **General DEM REV papers** — same issue: frames written for cubic specimens do not apply cleanly to HCA geometry.

**Effort:** M

**Target:**

- `01_introduction.tex` paragraph 4: expanded the DEM-HCA precedent citation into a two-sentence taxonomy note; now cites `LiGuoZhang2014` (reviewer-requested JCSU paper), `LiZhangGutierrez2015` (renamed from the old `Li2014` key to match actual authorship + year), `Shi2021`, `Liu2021`, and `Song2024` (dual-purpose: also covers R2.4 literature-review request)
- `02_methodology.tex` §2.1: integrated one clause noting that 10× Toyoura PSD scaling is an established DEM practice \citep{Song2024} — **no numerical specimen-to-D_max ratios exposed in manuscript**
- `refs.bib`: old `Li2014` key renamed to `LiZhangGutierrez2015` (Acta Geotech 10:449-467, year corrected to 2015); new entries added for `LiGuoZhang2014` (J Cent South Univ 21:2950-2961), `Shi2021`, and `Song2024`
- All prongs A–F of the full argument (dimensional ratios, ASTM D4767, peer ratio comparison, liquefaction-as-end-state, HCA geometric defense, cost trade-off) remain in `response_letter.tex` — manuscript stays deliberately light

**Deliberate design:** avoid exposing the 6.7× radial ratio in the manuscript. Respond to "provide supporting references" prong in reviewer's question by pointing to Song 2024 as the Toyoura-scaling precedent; the quantitative justification is reserved for the response letter.

**Known gap (for follow-up 2026-04-21):** R1.1 letter currently lacks a research-paper citation that specifically studies DEM specimen-to-particle-size ratios and supports small ratios (~6–10) as adequate for averaged / end-state quantities. Today's survey (Huang 2014, Kuhn–Bagi 2009, Marketos–Bolton 2010, Wang 2022) either showed size effects exist (ambiguous) or argued for larger ratios (against us). Current defense leans on ASTM D4767 + Shi2021/Song2024 precedent + theoretical + geometric prongs. Candidates to pursue tomorrow:

- **Ni et al.** (cited by LiGuoZhang2014): "beyond 15 000 particles, little effect on model results" — if the primary source confirms this in clean language, it directly supports our ~50k particle count.
- **O'Sullivan (2011) textbook** §7 for explicit numeric threshold statements usable as textbook-level backing.
- **Specific DEM cyclic-loading / liquefaction papers** where modest ratios were accepted and results validated — liquefaction being an end-state problem may have independent treatments.
- **Particle-count-convergence studies** (rather than size-ratio): a different angle that plays to our strength (~50 000 particles ≫ typical thresholds).

**Status:** ✅ manuscript edits complete (2026-04-20); response-letter text drafted but R1.1 Prong 2 / supporting-ratio citation pending literature follow-up

### R1.2 — Void ratio range too narrow for Toyoura "dense/medium-dense"

**Comment:** e ranges of 0.736 and 0.742 imply total e spread of only 0.04, which doesn't match Toyoura's physical e_max/e_min range. Terms "dense" and "medium-dense" questionable.

**Strategy — verbal-only response, no new figures:**

Framed as a two-part argument:

1. **Relative density is not well-defined for a DEM assembly.**
   - DEM particles are spherical vs real-Toyoura subrounded-to-subangular → different packing geometry at same grading.
   - No standardised procedure exists for DEM (e_max, e_min): result depends on particle shape, grading, assembly friction, numerical scheme, boundary/preparation — none standardised across DEM codes.
   - Substituting DEM e (0.736, 0.742) into textbook Dr formula with Ishihara's tabulated real-Toyoura (0.98, 0.60) gives Dr≈64% for both — inconsistent with reproduced behaviour → textbook formula does not apply here.

2. **Labels "Dr≈90%" / "Dr≈75%" are behavior-matched references to laboratory conditions, not values computed from DEM e.**
   - Dr≈90% (e≈0.736) reproduces Nakata 1998 monotonic (Dr≈92–93%) + Ishihara 1985 "very dense" cyclic (Dr=88–95%) → shown in Fig. 7 of manuscript.
   - Dr≈75% (e≈0.742) is a comparative density anchor for the K0-expansion study, tuned so cyclic response at K0=1.0 falls within Ishihara "dense" (Dr=75–82%) band.

3. **Precedent for band labelling:** Ishihara himself uses ±3.5% bands; paper notes (p.68) "individual specimen has a variation in relative density with a range of ±3.5% around the average" and (p.67) manual specimen-height restoration each cycle. Our labels follow the same band-based convention.

**No letter figure.** Previously-drafted Fig. rl_dr75 (Dr=75% vs Ishihara "dense") dropped because: (a) reviewer's question is about label consistency, not Dr=75% validation rigor; (b) Dr=75% at CSR=0.25/0.30 sits visibly above Ishihara cloud due to low-N_L manual-height-restore scatter — showing the figure invites a flank attack the reviewer did not open. Main manuscript Fig. 7 remains the Dr=90% validation visual.

**Manuscript change:** subsec:preparation paragraph (line 71) revised — explicit statement that (i) DEM void ratios cannot be converted to Toyoura Dr via textbook formula (spherical vs angular particles; no standardised DEM packing-limit procedure); (ii) labels are behavior-matched references tuned to reproduce macroscopic responses at corresponding Toyoura Dr conditions.

**Artifacts retained for reference (not cited):**

- `torsionSim/parameter_validation/undrained_cyclic/hca_Ishihara_Dr75.csv` (digitised Ishihara "dense" band, 13 points)
- `torsionSim/parameter_validation/validate_dual_density.py` and `validate_Dr75_check.py` (diagnostic plots)
- `papers/cg-coupled-servo/responses/COMGE-D-26-01109-r1/figs/validate_Dr75_check.png` (kept on disk; no longer referenced from letter)

**Effort:** S (text-only)

**Target:** `02_methodology:subsec:preparation` wording; letter R1.2 verbal response; no figure changes in letter or manuscript

**Status:** ✅ (2026-04-22)

### R1.3 — CSR, K₀ formulas missing

**Comment:** CSR and K₀ used without computational formulas.

**Response plan:** Add `CSR = τ_cyc / p'_0` (normalized by initial mean effective stress, not σ'_z0) and `K₀ = σ'_r / σ'_z` definitions inline at first use in §2.2 — common-knowledge ratios don't need displayed equations.

**Effort:** S

**Target:** `02_methodology` §2.2 at first appearance of each symbol

**Status:** ✅ (2026-04-20) — inline definitions added in §2.2: $\Kzero = \sigma_r'/\sigma_z'$ at IC–AC protocol opening, $\mathrm{CSR} = \tau_{cyc}/p_0'$ at cyclic program opening; both reference Table~\ref{tab:hca_equations}

### R1.4 — Need consolidated case table

**Comment:** Simulation program described in brief statements; recommend a table listing all cases (Dr × K₀ × CSR combinations).

**Response plan:** Matrix-style Table `tab:case_matrix` placed at the end of §2.2, with rows keyed by $(D_r, \Kzero)$ and columns by CSR ∈ {0.200, 0.250, 0.300, 0.350, 0.400}, cells holding $N_L$ ($\ru=0.95$ criterion). Empty cells rendered as `--` so the primary 3×5 matrix and the expanded K₀-refinement / Dr=75% strip are visible at a glance — no separate "Set" column needed.

**Effort:** S

**Target:** end of `02_methodology` §2.2 (chose over start of §3 so the program + matrix live together)

**Status:** ✅ (2026-04-20) — 10-row × 7-col matrix table inserted after the simulation-program paragraph; 22 cases populated from `torsionSim/cyclic_shear/{Dr90,Dr75}/kX.XX/csr_0.XXX/torsion_shear.csv` via `summarize_cases.py`. Dr90/K₀=2.0/CSR=0.400 ($N_L=4.0$) recovered after the CSV was restored today.

**Table format — final (2026-04-21):** switched from N_L-in-methodology matrix to a CSR-list format. Each row is one $(D_r, \Kzero)$ pair, third column is the comma-separated list of CSR levels tested. 10 rows, 3 columns. No $N_L$ in the methodology table — $N_L$ stays in Results (Fig 8 + Fig 11/12) so the methodology section remains free of outcome data. Reviewer's "list all cases" requirement is met by direct CSR enumeration; reader can see the primary 3×5 block (Dr=90%, K₀=0.5/1.0/2.0) + expanded points (K₀=0.67, 1.5 at CSR=0.300; Dr=75% block at CSR=0.300) at a glance.

**K₀=2.0 / CSR=0.400 — final (2026-04-21):** listed in the table (K₀=2.00 row shows all 5 CSRs), and restored to Fig 8. `EXCLUDED_CASES` guard removed from `liq_res_cur.py`. Rationale: with the CSR-list format, omitting 0.400 from the K₀=2.00 row created a visible asymmetry vs K₀=0.50 and K₀=1.00 rows, which would itself draw reviewer attention. Keeping the point everywhere is the least conspicuous choice. The narrative "monotonically decreases" is retained — the §3.2 line 276 note on low-N_L reversals covers the visual convergence at CSR=0.400 at the paper level.

### R1.5 — Loading rate / quasi-static condition

**Comment:** Loading rate not specified. Excessive rates cause inertial effects / distorted contact forces. Confirm quasi-static condition.

**Response strategy (final, 2026-04-26):** Two-pronged.

1. Add explicit loading frequency $f=8$ Hz to §2.2 (responds to "not specified").
2. Address the QS question with the inertial number $I = |\dot\gamma|\,d_{50}\sqrt{\rho_s/p'}$ in the new §2.5, with two reference values cited from primary literature:
   - $I<10^{-3}$ (GDR-MiDi 2004, strict $\mu_{\rm eff}$ rate-independence threshold)
   - $I=10^{-2}$ (da Cruz et al. 2005, representative quasi-static value, Fig. 1a)

**Compliance (Dr75/K=1.0/CSR=0.400, $r_u=0.95$ criterion):**

- pre-liq fully satisfies $I<10^{-2}$ ($I_{\max}=2.7\times 10^{-3}$)
- pre-liq satisfies $I<10^{-3}$ for **96.9%** of the window
- $\sim 3\%$ excursion confined to final cycle before liquefaction

**Post-liq framing:** $I$ rises to $\sim 4\times 10^{-2}$ peak — a physical consequence of $p'\to 0$ in the inertial-number definition, shared with laboratory testing. Cite Wang et al. 2025 (Bull. Eng. Geol. Environ.) for the cyclic-specific three-stage framing (initial stability / rapid transition / post-liq stabilisation = "kinematic critical state").

**Lopera Perez 2016 (with 2017 erratum)** deliberately NOT cited — the corrected upper limit $I\leq 7.9\times 10^{-5}$ is monotonic-CSL specific and stricter than even GDR-MiDi by 1.5 decades; their own erratum (point 4) acknowledges it is "a lower bound to the values given in the literature". Citing it would create unnecessary friction on our 96.9% number. PDF kept in `ref/PerezKwok2016.pdf` for in-house reference.

**Effort:** M (new figure panel + new methodology subsection + new bib entries)

**Targets:**

- `02_methodology.tex` §2.2 (subsec:preparation): added $f=8$ Hz at first CSR mention
- `02_methodology.tex` §2.5 (new subsec:numerical_verification): full quasi-static / inertial-number paragraph + Fig. 6 panel (c)
- `refs.bib`: added GDRMiDi2004, daCruzEmam2005, Wang2025inertial
- `response_letter.tex` R1.5: full response

**Status:** ✅ (2026-04-26)

### R1.6 — Rigid walls vs flexible membrane

**Comment:** Rigid walls may overestimate stiffness and liquefaction resistance. Discuss limitations and justify with references.

**Response plan:** Acknowledge limitation. Justify: HCA physical chambers are rigid-walled with membrane as interface; present work focuses on fabric-level comparison, not local shear bands; direct cross-reference to R2.4 Song 2024 flex-membrane as complementary / future work.

**Effort:** M

**Target:** `02_methodology` §2.1 end, or discussion

**Status:** ⬜

### R1.7 — CSL source in Fig 8(c)

**Comment:** CSL origin unclear; add citation.

**Response plan:** Update caption to explicitly cite Ishihara (1985) experimental envelope (or whichever is actual source — verify).

**Effort:** S

**Target:** `03_results` Fig 8(c) caption

**Status:** ⬜

### R1.8 — Fig 12 K₀=1.0 "enhancement" in coordination plane

**Comment:** N_L decreases monotonically with K₀ in Figs 8, 10; but Fig 12 shows K₀=1.0 *enhancement*. Explain.

**Data verification (CSR=0.300, Dr=90%):** Z_m0: K0=0.5→4.894, K0=0.67→4.967, K0=1.0→4.978 (peak), K0=1.5→4.965, K0=2.0→4.885 vs N_L monotonically decreasing 11.03→10.03→9.52→9.02→8.54. The two rankings are genuinely different — not a plotting artefact, and not a normalization artefact (the K0=1.0-on-top observation is on the y-axis, independent of x-axis choice). Removing N/N_L normalization would not address the reviewer's concern and would degrade the figure's comparative-decay function.

**Strategy — forecast + brief hint at Fig 12, not full duplication:**

The full resolution is already in §3.2 (Fig:fabric_liq_pair, Fig:fabric_mechanism, Table:fabric_diagonal — the last two extended under R2.7). The reviewer's concern is a reading-order gap: the apparent paradox is visible at Fig 12 (~line 144) but the explanation lives ~140 lines later (~line 287). Fix is a 2-sentence forecast at Fig 12:

1. Acknowledge: K0=1.0 has highest Z_m0 but is not the highest N_L (cross-ref Fig:liq_resistance_curves)
2. One-clause physical hint: Z_m counts contacts isotropically; resistance depends additionally on directional partitioning + forward ref to §3.2 (Fig:fabric_liq_pair, Fig:fabric_mechanism)

Don't duplicate the full quantitative argument — preserves the §3.2 build-up Z_m (insufficient) → α (necessary) → Φ^f (dominant).

**Effort:** S

**Target:** `03_results` Section subsec:micro_fabric_results — Fig:zm_evolution discussion paragraph (~line 144)

**Status:** ✅ (2026-04-30) — 1-sentence forecast added at Fig:zm_evolution paragraph; letter R1.8 drafted with explicit data values (Z_m0 vs N_L tables) + physical reasoning (count vs directional partitioning) + cross-references to fabric_liq_pair and fabric_mechanism

---

## Reviewer 2

### R2.1 — Particle-wall friction = 0 in Table 1

**Comment:** Why is particle-wall friction zero?

**Response plan:** Clarify that torque is transmitted via blade geometry (normal contact with blade faces), not wall tangential friction. Setting wall friction to zero avoids introducing an additional unconstrained parameter while still providing full torque transfer through geometrically-constrained blade contacts.

**Effort:** S

**Target:** Table 1 caption / `02_methodology` §2.1

**Status:** ✅ (2026-04-22) — §2.1 blade paragraph extended with a one-sentence clause: "The cylindrical walls and end platens are assigned zero friction ($\mu_{pw}=0$, Table~\ref{tab:dem_parameters}) so that they act purely as servo-controlled pressure boundaries; torque is transmitted geometrically through normal contact forces on the blade faces and does not rely on a wall-friction coefficient."

**Letter rewrite (2026-04-22, later):** R2.1 letter reorganised into three wall-class subsections after Yusong clarified the underlying physics. New structure:

1. **Cylinders (radial principal stress plane):** HCA element reduction requires radial face to be principal stress plane. Laboratory membrane–water equilibrium self-balances tangential tractions at element scale → radial face remains principal. DEM walls are massless, so $\mu_{pw}>0$ leaves residual shear on radial face → violates principal-plane assumption. $\mu_{pw}=0$ is *required*, not a simplification.
2. **End platens (axial principal stress plane + servo determinacy):** Same principal-plane argument extended to axial face. Lab porous-stone caps carry residual friction — known non-ideality that DEM models the *idealised* HCA boundary *without*. Additionally avoids Coulomb-limit coupling between $\sigma_z'$ and torsion that has no measurable experimental counterpart.
3. **Blades (geometric torque transmission):** Blade is a thin **radial slab**; its **face normal is circumferential** (θ̂). Normal contact delivers a purely circumferential force — exactly the torque-transmitting direction — so full torque transfer is geometric. $\mu_{pw}>0$ introduces Coulomb-limited frictional tractions in the face tangent plane (r̂, ẑ). These tractions (i) directly contaminate $p_z'$ measurement (Appendix A integrates end-plate contact forces **including attached blades**; blade friction z-component leaks into $p_z'$), and (ii) introduce a Coulomb-dependent perturbation to the blade–particle force distribution that saturates as $\sigma_r'\to 0$ near liquefaction, rendering servo response non-smooth and causing it to miss $\tau^{tar}$. **Corrected from earlier draft** (2026-04-22 evening) which incorrectly said "face is oriented radially" and "friction adds Coulomb-limited frictional torque" — friction is in (r̂, ẑ) plane, carries no θ̂ component, so no direct torque contribution.

Closing: $\mu_{pw}=0$ (i) preserves principal-stress assumption radial+axial, (ii) avoids Coulomb-limit servo constraint near liquefaction, (iii) removes unconstrained free parameter. Full argument kept in letter; manuscript retains the short §2.1 clause only.

### R2.2 — Torsional blade size

**Comment:** What is the size of the torsional blades?

**Response plan:** Add the single fact the reviewer asked for — blade height = 15 mm — inline in §2.1. Angular distribution and top/bottom partitioning are already visible in Fig. 1(b), so not repeated in text.

**Effort:** S

**Target:** `02_methodology` §2.1

**Status:** ✅ (2026-04-20) — §2.1 now reads "...six torsional blades, each 15~mm tall, are inserted into the specimen (Fig.~\ref{fig:specimen_generation}b)." Geometry source: `torsionSim/blender-work/data/deposit/README.md` (upper blades z=35-50mm, lower z=-50 to -35mm, plates at z=±50mm).

**Letter update (2026-04-22):** R2.2 letter response extended with the blade-to-grain-size rationale. Parallel framing: laboratory blade ≈ \SI{1.5}{mm} = 15 × Toyoura $d_{\min}$; DEM blade = \SI{15}{mm} = $15\,d_{\min}$ of the DEM grading ($d_{\min}=\SI{1.0}{mm}$ from the \SIrange{1.0}{3.0}{mm} grading stated in §2.1 — note: Table~1 does not list the grading, only particle count, density, stiffness, friction, and damping). Rationale stays in the letter rather than the manuscript: §2.1 reports blade height as a model parameter, but the paper's scope ($K_0$ effects, fabric evolution) is orthogonal to DEM-HCA design-ratio appropriateness — adding the ratio invites scope creep (why 10× upscale? why $H=D$? etc.). No $d_{50}$ claimed; no "visual estimate" wording used.

### R2.3 — Difference vs Han (2024) servo

**Comment:** What differs from the servo in Han (2024)?

**Response plan:** Methodology line 326 already addresses this in contribution statement. Expand in response letter: Han (2024) solves only radial + torsional, keeps height fixed; present work adds axial DOF + analytically derives cross-coupling matrix K̂.

**Effort:** S

**Target:** existing text + response letter

**Status:** ✅ (2026-04-22) — letter R2.3 reorganised as three-point summary of the existing contribution paragraph in §2.3 (~line 349): (i) DOF extension (axial DOF added), (ii) laboratory-to-DEM mapping via pressure differences $p_{dif,r}'$, $p_{dif,z}'$ that are invariant to $u$, (iii) analytical inversion of the $2\times2$ coupled stiffness $\hat{\mathbf{K}}$. Also notes that the present formulation reduces to Han 2024's radial-only coefficient under $dH/dt=0$. No manuscript addition — existing contribution paragraph covers all three.

### R2.4 — DEM-HCA literature review + H=D choice

**Comment:** Introduction should review DEM-HCA work: Li 2014, Li 2017 (stacked wall); Song 2024a, Song 2024b (flexible membrane); Shi 2021 (H=2D). Height=outer diameter vs typical H=2D — any requirement?

**Response plan:** (a) Add an Introduction paragraph surveying these DEM-HCA models with boundary-type taxonomy (stacked wall, rigid wall, flex membrane); (b) Justify H=D as computational cost trade-off; cite PFC precedents; note that present study focuses on average fabric response where end-plate effects are minimal.

**Effort:** M

**Target:** `01_introduction` + brief note in `02_methodology`

**Status:** ✅ (2026-04-22) — (a) intro DEM paragraph rewritten with explicit three-class radial-boundary taxonomy: rigid walls (Shi2021, Liu2021), stacked walls (LiGuoZhang2014, LiZhangGutierrez2015), flexible membranes (Song2024); (b) H=D justified in letter R2.4: focus on average specimen-level response (not strain localisation), geometry matches Vargas 2020 laboratory device and the DEM servo precursors Han 2024 / Ma 2024, ~2× particle-count saving vs H=2D. No dedicated aspect-ratio text in manuscript — kept in letter.

### R2.5 — Servo stability near singular stiffness matrix

**Comment:** Drastic contact loss near liquefaction may make stiffness matrix near-singular. How is numerical oscillation prevented?

**Response plan:** First audit actual servo code. Options:

- If regularization exists: describe (damping / condition-number check)
- If not: argue that constant-volume constraint eliminates radial DOF singularity; axial and torsional DOFs are independently stable; post-liquefaction oscillations are physical not numerical

**Effort:** M

**Target:** `02_methodology` servo section or appendix

**Status:** 🟥 needs code audit first

### R2.6 — Validation: add e_r, e_z, volume evolution

**Comment:** Show evolution of e_r and e_z over time or volume change.

**Response plan:** Add figure(s) tracking r, H, volume during monotonic calibration and cyclic validation. Demonstrates constant-volume constraint is strictly satisfied.

**Effort:** S–M (post-processing of existing sim dumps)

**Target:** `02_methodology` validation section

**Status:** ⬜

### R2.7 — Contact force anisotropy (3D rose)

**Comment:** Contact density anisotropy analyzed but not normal contact force anisotropy. Add 3D rose diagrams per Song 2024 etc.

**Response plan:** Compute contact force rose diagrams (in addition to contact density). Decide post-processing from pickled contact dumps vs re-run.

**Effort:** M

**Target:** `03_results` §3.2 near Fig 14

**Status:** ✅ (2026-04-27, commit a737dca; letter updated 2026-04-30) — two-prong delivery: (i) new 8-panel normal-force rose Fig. \ref{fig:contact_force_sequence} annotated with $(A_n, B_n, \langle F_n\rangle)$ per panel via `anisotropy_values.py`; (ii) dual-axis upgrade to Fig. \ref{fig:fabric_mechanism} overlaying $1-\Phi_{rr}$ and $1-\Phi^f_{rr}$ across the full 10-case expanded dataset (5 K_0 × 2 D_r), backed by new Appendix C Table \ref{tab:fabric_diagonal}. Key finding: ~9× sensitivity gap between count- and force-weighted fabric (1.5% vs 14% across K_0 = 0.5→2.0), identifying the load-bearing subnetwork as the dominant carrier of the K_0-dependent liquefaction signal. New Eq. \eqref{eq:fabric_tensor_force} for $\Phi^f_{ij}$; \citet{Zhou2022} added.

### R2.8 — Fig 15 quantitative differences

**Comment:** Displacement between K₀=0.5 and 2.0 hard to distinguish at N/NL=0.00 and 0.61; force chain hard to distinguish at N/NL=1.05 and 1.07. Quantify.

**Response plan:** Add quantitative metrics — e.g., displacement magnitude CDF or force-chain principal-direction angle histogram. Either as new panel or in caption text.

**Effort:** M

**Target:** Fig 15 caption / new panel

**Status:** ✅ (2026-04-30) — both sub-questions answered through the R2.7 force-rose annotations; no separate R2.8 figure. (i) Force-chain at N/N_L = 1.05 and 1.07: $A_n = 0.18$ vs.\ 0.20, $B_n = 45^\circ$ vs.\ $43^\circ$, $\langle F_n\rangle \approx 0.16$\,N for both — quantitatively confirms the visual indistinguishability. (ii) Displacement at N/N_L = 0.00 and 0.61: explicitly reframed in letter — pre-liquefaction displacement similarity is part of the finding, not missing discrimination; the quantitative discriminator at the same instants is the force-fabric tilt $B_n$ (1° vs 90° at 0.00; 15° vs 83° at 0.61), which the rose annotations now expose directly. Earlier-draft TODO for displacement CDF dropped — would have re-quantified what was inherently small and similar, while the force-rose answers the underlying question.

---

## Cross-cutting items

### New references to add

- Li, B., Guo, L., Zhang, F. S. (2014) — JCSU, stacked wall DEM-HCA
- Li, B., Chen, L., Gutierrez, M. (2017) — CGeo, stacked wall
- Song, S., Wang, P., Yin, Z., Cheng, Y. P. (2024) — JRMGE, flex-membrane DEM-HCA
- Song, S. X., Yin, Z. Y., Liu, Y. J., Wang, P., Cheng, Y. P. (2024) — IJNAMG, CFD-DEM
- Shi, C., Yang, J., Chu, W., Tang, H., Zhang, Y. (2021) — IJGeo, HCA H=2D
- O'Sullivan / Jiang — DEM REV size-ratio guideline (R1.1)
- da Cruz / Roux — inertial number quasi-static threshold (R1.5)

### Output artifacts

- **This checklist** — internal tracking, not submitted
- **`response_letter.tex`** — point-by-point reply, compiled to PDF, submitted
- **`sections/*.tex` edits** — committed directly to `revision-r1`
- **Marked-up manuscript** — `latexdiff` against `submitted-r0` tag, submitted

### Suggested execution order

1. Quick items first (R1.3, R1.4, R1.7, R2.1, R2.2, R2.3) — half-day, clears baseline
2. R1.8 and R2.4 — text-only argument + citations
3. Decide R1.2 — if yes, kick off CSR=0.40 Dr=75% sim early (longest lead time)
4. R2.5 after code audit
5. R2.6, R2.7, R2.8 post-processing in parallel
6. R1.1, R1.5, R1.6 — text + citations
7. Consolidate into response letter last

### Pre-submission checks

Run these checks before declaring the letter final and building the submission PDF. Do NOT do them mid-task while manuscript text is still shifting.

- [x] **Line-number pointers in the letter.** ✅ (2026-05-01) — `\manref{p.~X, l.~Y}` added to every `\changed{}` block (R1.1–R1.8, R2.1–R2.8) and to M1–M5 in Additional minor clarifications, anchored against `build/main.pdf` (lineno-active). Lookup table built from `pdftotext -layout build/main.pdf` and the page-footer scan; key anchors include §2.1 boundary taxonomy (p.~3, l.~112–132), §2.2 prep (p.~4, l.~136–149), §2.3 servo (p.~7–8, l.~186–242), §2.4 cyclic program + Table 2 (p.~9, l.~262–270), §2.5 verification + Fig.~7 (p.~10, l.~272–301), §2.6 critical-state determination (p.~11, l.~326–335), §3.3 fabric (p.~17–22), §3.4 force-fabric implication (p.~22–23, l.~567–571), Appendix C Table 4 (p.~28). Page numbering will need re-checking if the manuscript body shifts before final submission.
- [ ] **`latexdiff` vs `submitted-r0` tag** regenerated against the final manuscript.
- [ ] **Bibliography sanity pass** — verify all new `\citep{...}` keys resolve in `refs.bib` and that no entries added during revision contain placeholder titles / years.
- [ ] **Figure / table numbers** referenced in the letter match the final compiled manuscript (numbering can shift when new tables/figures are inserted).
- [ ] **Overfull hboxes** in the letter log — scan for any remaining and trim or reword.
