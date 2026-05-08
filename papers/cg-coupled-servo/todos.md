# Computers and Geotechnics (CG) Paper: Task List

Paper: *Influence of Initial Stress Anisotropy on Liquefaction Resistance in Undrained Cyclic Torsional Shear: DEM Simulation of Hollow Cylinder Tests*

Manuscript: COMGE-D-26-01109 | Status: Under Review (2026-03-25)

---

## TODO (for revision)

- [x] **Clarify servo targets as laboratory total-stress differences**
  - §2.3 Radial condition: state $p_{dif,r}^{tar} = p_o - p_i$
  - §2.3 Axial condition: state $p_{dif,z}^{tar} = p_z - \sigma_r$
  - Narrative paragraph already explains "because $u$ drops out",
    but formal definitions lack this explicit link
  - Done in r1: appended `=p_o-p_i` / `=p_z-\sigma_r$` in where-clauses

- [x] **Clarify $p_i = p_o$ in AC protocol (§2.2)**
  - K0 anisotropy achieved solely through $p_z$, not radial
    pressure difference
  - State $p_{dif,r}^{tar} = 0$ when describing the AC stress path
  - Done in r1: line 51 appended "with $p_o^{\prime}=p_i^{\prime}$
    held throughout (so $p_{dif,r}^{tar}=0$)"

- [x] **Remove misleading "CSR = 0.300" from Table 3 (Appendix C)**
  - These are post-consolidation / pre-shear values shared by all
    CSR cases
  - Replace with "after anisotropic consolidation" or similar
  - Fig. 13 subcaptions with "CSR = 0.300" are correct (those show
    results at that specific CSR)
  - Done in r1: dropped from narrative; caption now reads "after
    anisotropic consolidation"

- [x] **Flowchart steps 4--5: add constant-height branch**
  - Step 4: under constant height only $S_{rr}$ is needed
  - Step 5: $dH/dt = 0$, only $dr/dt = S_{rr} \cdot e_r / \Delta t$
  - Add branch or annotation to reflect both modes
  - Done in r1: footnote-size italic annotation in steps 4 and 5

- [x] **Unify increment notation in coupled stiffness equation**
  - Eq. (8) left side: $\delta p$ (variational) → $dp$ (differential)
  - Both sides are actual increments (tangent stiffness), not
    virtual work
  - Update Eq. 12 and Appendix B accordingly
  - Done in r1: all `\delta p`, `\delta\sigma` → `dp`, `d\sigma` in
    §2.3 and Appendix B

- [x] **Prepare for potential question: full coupling only in
  monotonic case**
  - Monotonic validation: stress-control, variable height, full
    2x2 matrix active
  - All cyclic simulations: constant height, matrix degenerates
  - Line 342 already notes both modes but could be more explicit
  - If reviewer asks: option to add one stress-control cyclic case
  - Caveat: requires deviatoric strain criterion, not $r_u = 0.95$
  - Covered in r1 by R1.7 + new §2.6 verification subsection
    (CSR=0.400 stress-control case exercises full $2\times 2$)

- [x] **Fix bibliography metadata errors (refs.bib)**
  - WuYang2022: issue 11→12, pages 04022099→04022112
  - YangTaiebat2024: added missing pages=04024028
  - Xie2023: added missing pages=04022312
  - Verified all other entries against Crossref (2026-04-01)

---

## Reference

- CG Guide for Authors: <https://www.sciencedirect.com/journal/computers-and-geotechnics/publish/guide-for-authors>
- CAS template docs: `els-cas-templates/doc/`
- Thesis source: `thesis/04_1_anisotropic_consolidation_sim.md`
