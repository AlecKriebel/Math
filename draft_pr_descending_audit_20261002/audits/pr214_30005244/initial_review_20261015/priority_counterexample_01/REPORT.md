# Independent priority and scope falsification: PR214 / 30005244

Audit date: 15 October 2026 UTC. This report concerns priority and interpretation, not a replacement for the separate proof audits. The early search was conducted independently before receiving the parent's Zhou lead. Only this folder was written; no outreach, Git mutation, queue mutation, or publication was performed.

## Finding

**No exact earlier theorem or counterexample covering the full submitted result was located in this bounded search. This is not a certification of novelty.** The proposed contribution must be stated narrowly as a justified application to the particular center-membership, diagonal-omitting cubic DDA, together with a compact-support scope obstruction. The ball spectrum, radiative nonreal-pole mechanism, compact analytic spectral machinery, and rational-point deletion are established ingredients.

The strongest additional primary continuum credit is Ammari–Li–Zou (2020), supplemented by Zhou's manuscript available by 2021. They substantially cover the claimed existence and qualitative structure of nonreal continuum poles. Neither inspected treatment establishes the discrete DDA convergence theorem or constructs the fixed compact particle sampled only at one anchor.

## Exact claims tested

1. For fixed complex frequency and bounded support satisfying mask-volume consistency (G), does an earlier source already prove uniform off-interval DDA resolvent stability, absence of pollution, preservation of algebraic multiplicity, and norm convergence of embedded Riesz projections?
2. Does an earlier source already give a positive-volume **compact** support with a nonreal continuum pole at a fixed real positive frequency, but only the point 0 on every lattice (1/n)Z³ and thus a nonempty 3-by-3 zero DDA matrix?
3. Even without the exact construction, which earlier results directly cover the ball perturbation or the functional-analytic transfer used to construct it?

Success at falsifying priority would require an actual earlier theorem/construction with matching hypotheses and normalization, not a title, abstract claim, numerical plot, or an assumed inverse bound. Mathematical validity and novelty remain separate.

## Four approach families and outcomes

| Family | Mechanism and evidence | Status and exact remaining gap |
|---|---|---|
| Direct DDA spectral/convergence literature | Full OWR discussion; full CDN v3; full relevant sections of Costabel's 1D convergence paper; full 2006 analysis; 2018 VIE continuity discussion; 2023 DDA chapter; current author publication listings | No covering theorem located. The nonzero-frequency paper advertised in 2023 as in preparation remains an unresolved priority/access lead. |
| Ball modes and small-frequency perturbation | Full ALZ 2020 spectral section; published Ammari–Millien 2019 volume-operator perturbation analysis; full relevant 2017 Mie expansion; historical AMV 2020 report | Strong classical coverage of nonreal poles, static decomposition, and radiative cubic coefficient. No exact published quartic certificate at κ=10^-4 identified. |
| Pathological sampling and compact supports | Countable-set invisibility to volume operators, standard rational-point deletion, and explicit 2018 discussion that pointwise DDA sees only cell-center material values | Sampling mechanism is elementary/classical. No earlier text located joining compact rational avoidance to persistence of an isolated nonreal DDA-comparison pole. |
| Abstract continuum and spectral persistence | ALZ meromorphic Fredholm theory; Zhou static-plus-Hilbert–Schmidt decomposition; standard compact multiplication and Riesz arguments | No new abstract spectral theorem should be claimed. The remaining candidate-specific work is proving the actual discrete consistency and applying these arguments to changing masks. |

## Primary-source coverage that must receive credit

### Ball radiation and pole structure

[Ammari–Li–Zou, *Superresolution in Recovering Embedded Electromagnetic Sources in High Contrast Media*](https://arxiv.org/abs/2001.07116), full ETH SAM report 2020-08 inspected, defines

\[
T_D^k=(k^2+\nabla\operatorname{div})\int_D g_k(x-y)(\cdot)(y)\,dy=-A_k.
\]

Theorem 3.2 gives strictly positive imaginary part for its eigenvalues other than -1 on smooth bounded domains. Theorem 3.7 gives its finite-type poles off essential spectrum \(\{-1,0,-1/2\}\). Section 3.3 and Theorem 3.13 describe the sphere through exact Mie determinant equations. Therefore the candidate's \(S_k=-T_D^k-I/3\) has the opposite radiation sign. Combining their sign theorem with standard norm-small persistence of the ball dipole cluster already gives nonreal poles for all sufficiently small positive k. This is a deduction from established results, not an exact explicit κ threshold asserted in that paper.

[Tzarouchis–Ylä-Oijala–Sihvola, *Resonant Scattering Characteristics of Homogeneous Dielectric Sphere*](https://arxiv.org/abs/1702.05883), v1, Section III, equations (9)–(11), gives the familiar small-sphere dipole pole expansion beginning

\[
\varepsilon=-2-\frac{12}{5}x^2-2ix^3+\cdots.
\]

Under the conventional material-pole relation \(a=(1-\varepsilon)^{-1}\), with \(a\) an eigenvalue of the candidate's \(A_k\), elementary series inversion yields

\[
a-\frac13=-\frac4{15}x^2-\frac{2i}{9}x^3+O(x^4).
\]

Thus the candidate's cubic trace coefficient \(-2i k^3/3\) across the three dipole modes matches the known radiation term. That source uses Padé approximants and does **not** furnish the candidate's rigorous norm remainder or fixed κ=10^-4 certificate. It supplies precise priority credit, not a substitute for the submitted error control.

[Rahola (2000)](https://doi.org/10.1137/S1064827598338962) is older direct sphere-spectrum/Mie-resonance credit. Its publisher abstract was inspected; the full PDF returned HTTP 403. It would be unsound to infer a rigorous general DDA convergence theorem from that abstract. CDN v3 discusses its numerical plots and leaves the relevant discrete-eigenvalue approximation unproved.

### Static decomposition and volume-operator perturbation

[Ammari–Millien (2019)](https://doi.org/10.1016/j.matpur.2018.12.001), published version inspected, Sections 3–4, is prior direct use of the static Helmholtz decomposition, constant-field ellipsoidal dipole modes, and perturbative dynamic volume-operator spectrum. The historical [AMV March 2020 report](https://www.sam.math.ethz.ch/sam_reports/reports_final/reports2020/2020-19.pdf), Sections 2.4–2.5 and Appendix B, explicitly presents this route and credits Friedman–Pasciak and Costabel–Darrigrand–Sakly for the static operator.

A caution is material when using the 2019 paper as a covering proof: its printed Proposition 3.4 asserts compactness of \(T_D^0\) on harmonic gradients. For the ball, the candidate's directly checkable eigenvalues \(\ell/(2\ell+1)\to1/2\) rule out that compactness. Its Section 4 also uses rank-one eigenprojection formulas without covering the rank-three sphere degeneracy in that formula. These observations do not erase its substantial prior approach credit; they prevent treating it as an independently verified replacement for the candidate's multiplicity-aware argument. A general new static spectral decomposition must not be claimed here.

### Earlier static-plus-Hilbert–Schmidt continuum framework

The parent's independently acquired [Zhou, arXiv:0911.4540v5](https://arxiv.org/abs/0911.4540v5), dated 1 November 2021 and published in CMS 20(5) (2022), was read at the introduction, Theorems 1.1–1.3, Section 2.1, and the later relevant Fredholm discussion. Section 2.1 decomposes its Green operator into a static longitudinal operator and an O(1/r) Hilbert–Schmidt dynamic correction; Proposition 2.1 proves the static quadratic-form bound. Theorems 1.1–1.3 supply continuum spectral and optical-sign results, with different function-space hypotheses in different parts.

Zhou uses \(e^{-ikr}\). For real k, its Green operator is \(G=-\overline{A_k}\), where the bar means conjugation by complex conjugation on fields. Consequently \(S_k=-\overline G-I/3\); equating the two operators without the sign and conjugation is incorrect. The article's actual program is continuum Born-operator spectral structure and polynomial compactness. It does not specify or analyze the submitted finite DDA cell-center matrices, prove their consistency, or establish their Riesz-projection convergence. This conclusion comes from reading its setup/results/arguments, not merely absence of DDA keywords.

## Closest apparent direct convergence claims do not close the target

[Yurkin–Maltsev–Hoekstra (2006)](https://doi.org/10.1364/JOSAA.23.002578), full published text inspected, equations (64)–(66), explicitly assumes the inverse-norm convergence needed for stability. Its discussion around equation (65) says the proof is outside that paper's scope. It cannot be cited as an unconditional proof of the submitted theorem. Its smooth-field and boundary-volume hypotheses also exclude the present pathological support.

[Yurkin–Mishchenko (2018)](https://doi.org/10.1103/PhysRevA.97.043824), Section IX, equations (69)–(78) and footnote 22, is especially close conceptual prior art: it discusses material approximation, spectral continuity and interchange of discretization/material limits, and observes that pointwise cubic DDA depends only on cell-center values. It labels the needed continuity/uniform-convergence assertions as conjectural. The candidate's masked compact-persistence argument is not contained as a proved special case there.

[Costabel (2023)](https://arxiv.org/abs/2303.13693), v2, Theorems 3.3–3.4, proves solution-error convergence for the finite Hilbert transform on an interval. Its introduction explains the difficulty of passing the delta-delta scheme through standard compact-perturbation frameworks; reference [3] lists the nonzero-frequency DDA paper as in preparation. It has neither the three-dimensional dynamic kernel nor the claimed DDA spectral result.

The 2023 DDA chapter's broad convergence and spectrum remarks point back to this older theoretical/empirical literature and do not state a proof with the candidate's conclusions. The current Costabel author publication list was acquired through 2026 entries; it lists the two 2023 papers but does not list the advertised nonzero-frequency DDA paper. This is a bounded public check, not evidence that an unpublished or differently titled result cannot exist.

## What is and is not special about the compact counterexample

The rational-point deletion is not itself a research novelty. Enumerating a countable sampling set, covering its points by balls with summable tiny volumes, and taking a closed complement is the standard measure/topology construction. Here it leaves compact \(F_j\) of almost full ball volume, empty interior and no rational points. Because 0 has its own deleted neighborhood, restoring \(\{0\}\) creates an isolated null anchor. The sampling identity follows immediately; a 3-by-3 zero matrix then follows from diagonal omission. No DDA spectral theory is needed for those steps.

The additional, nontrivial logical bridge in the submitted construction is that the fixed ball pole survives on one **fixed** compact \(F_j\). Measure closeness by itself would not justify norm closeness of the singular static operator. The submitted proof instead uses strong convergence of selfadjoint masked static operators, norm convergence of their Hilbert–Schmidt corrections, compact resolvent factors, and nonzero Riesz rank persistence off the real static bound. This is a standard spectral mechanism applied to this mask sequence; no earlier text explicitly joining it to the compact sampling example was located.

This only refutes an unrestricted pointwise compact-set formulation. It does not refute the physical regular-particle limit, establish that (G) is necessary, show an error under boundary-null/Lipschitz hypotheses, or establish a practically significant DDA failure for a material particle. Since the source describes a physical particle and does not explicitly quantify over all pathological measurable supports, the counterexample is best presented as a scope clarification/obstruction, not as the sole resolution of the intended numerical research problem.

## Bounded conclusion and remaining priority gap

The full off-interval DDA application remains a plausible candidate contribution after this search. The exact pathological compact-support example may be a new explicit assembly, but its elementary and classical components should be visible in the wording. A suitable description is: **a proved off-interval spectral-convergence theorem for geometrically consistent cubic center-sampling DDA, and an explicit compact-support obstruction showing why arbitrary pointwise masks cannot be covered without geometric control.**

The exact outstanding priority gap is a potentially unpublished or differently indexed DDA theorem beyond the static CDN paper, plus the inaccessible full Rahola text. No author contact was made or prepared; under project policy only the human can seek outside input. These access gaps do not block the mathematical audit but preclude an absolute novelty claim.

All external payloads and raw search responses are under ignored `private_evidence/`. `SOURCE_PINS.json` records URLs/versions/bytes/hashes, and `SAFE_AUTHORED_MANIFEST.json` lists only the authored export files.
