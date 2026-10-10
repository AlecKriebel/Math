# Source gate and conventions

## Original question

Hannes Meinlschmidt, joint work with Karl Kunisch, *Optimal Control of a Semilinear Critical Wave Equation*, in *Challenges in Optimization with Complex PDE-Systems*, Oberwolfach Report9/2021, printed438–440. [Official report](https://publications.mfo.de/bitstream/handle/mfo/3850/OWR_2021_09.pdf), [DOI](https://doi.org/10.4171/OWR/2021/9). The imported record calls the publication2022, but the workshop/report identifier is2021; this is not a different target.

The source's displayed objective on439 includes terminal displacement tracking, optional scaled terminal velocity in H^-1, quartic L^4L^12 state regularization, L^1L^2 sparsity cost and quadratic L^2L^2 control cost. The pointwise-in-time spatial norm constraint is ||u(t)||_L2<=omega(t). The PDE is the defocusing quintic wave equation in three dimensions with homogeneous Dirichlet boundary and energy initial data. Page440 explicitly raises beta_2=0 after a strict critical-cone positivity implication to strong L^2-squared growth. Both pages were visually inspected.

The imported numeric ID30004630 / OWR-4990378-001 is this exact question. Pinned dataset revision37e53eabe540fb458758e198be61634bd02ee008. No upstream research_results entry was present for this code in the cached research report; the problem record contains literature triage. That triage is not a prior campaign proof.

## Full referenced analysis and exact differences

Kunisch–Meinlschmidt, *Optimal control of an energy-critical semilinear wave equation in 3D with spatially integrated control constraints*, Journal de Mathématiques Pures et Appliquées138(2020),46–87, [publisher metadata and abstract](https://doi.org/10.1016/j.matpur.2020.03.006). Full proof access here is [arXiv1907.02744v1](https://arxiv.org/pdf/1907.02744v1), dated July2019, and the [author-hosted preprint](https://hannes.meinlschmidt.eu/preprint/KunischMeinlschmidt2020.pdf), whose title page is March2019. These are distinguished from an uninspected publisher final typesetting.

- Introduction, printed2: gamma,beta_1,beta_2 are nonnegative, with positivity requirements announced as needed; omega need not be bounded below. The paper's objective omits the OWR nu term. The counterexample retains gamma=beta_1=1, a positive constant omega, and proves the assertions for any fixed nu>=0, including both displayed versions.
- Lemma2.9, printed8: linear energy/Strichartz bounds L^1L^2 forcing -> energy plus L^4L^12. The interpolation (2.2)/(4.4) gives L^5L^10, hence the quintic is L^1L^2. These credited estimates support a direct small-data contraction argument in the candidate.
- Theorem4.1, printed16: global optimal controls exist for gamma>0 and either beta_2>0 or omega integrable. The candidate also supplies the direct-method extension for the additional OWR terminal velocity cost in its uniform small-data setting.
- Theorem4.3, printed19–20: control-to-state differentiability; Lemma4.6, printed22–23: smooth objective derivatives. No new PDE well-posedness theorem is claimed.
- Section4.2.2, printed26: critical cone C(u_bar) consists of tangent directions with zero first directional derivative; the convention for j'' at u_bar=0 is zero. There is no requirement that the critical cone contain a nonzero direction.
- Theorem4.17, printed35, condition(4.28) and estimate(4.29): assumes beta_2>0 and strict positivity on C(u_bar) minus zero; growth is L^2-squared for controls close in L^infinity. The theorem page was visually inspected. OWR instead writes an L^2 neighborhood. The candidate converges in L^infinity and therefore refutes the unmodified implication in either neighborhood.

The target is not a claim that every beta_2=0 problem fails, nor a request to disprove every possible adapted sufficient condition. The negative answer here is to retaining the source's strict-on-critical-cone criterion and its strong quadratic-growth conclusion after simply removing beta_2>0. The critical cone is zero and that vacuity is prominent throughout. A concrete non-Lipschitz terminal-target perturbation result is also proved; no claim about all weaker stability exponents is made.

## Prior-attempt and literature checks

On October1,2026, all-state PR and branch searches for30004630 returned no results. Main commit history for its attempt directory was empty, and the recovered queue row remained queued0/5. The author/publisher source checks and targeted critical-wave/quadratic-growth searches did not locate a later primary resolution. This is a bounded search, not novelty certification. The failure mechanism uses classical concentration near a sparsity threshold and standard wave estimates; all such inputs are credited.

Source PDFs, full extracted text, imported records and rendered pages are reading copies outside the public artifact packet. source_manifest.json pins their public URLs and hashes.
