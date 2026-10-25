# Intake and scope review — Zenodo 23358014

**Disposition: SCOPE COMPLETE — mathematical clearance pending separate reviews.** This report authenticates the inventory item, maps its precise claims and primary interfaces, and supplies an unpublished editorial candidate. It is not a mathematical PASS, a scientific replay, a novelty certificate, or permission to promote the paper.

## 1. Eligible work and edition

Row 70 is *Failure of strong quadratic growth in unregularized sparse control of a critical wave equation*, Alec Kriebel, version 1.0, DOI `10.5281/zenodo.23358014`, concept record 23358013. The manuscript and Zenodo publication-date field both say 14 October 2026. The fresh record reports creation at `2026-10-14T05:39:12.680683+00:00`. The record is a published, open-access, CC BY 4.0 preprint with ORCID `0009-0001-9320-500X`. These facts identify this edition; they do not certify priority.

The saved programme objective was read before intake. This work is eligible because the named published Zenodo record contains its manuscript. No unrelated local or GitHub-only paper is included. No different work or reader manuscript is hidden inside the support archive.

Fresh API acquisition, independent SHA256, API/queue MD5 and exact byte sizes agree:

| Public asset | Bytes | SHA256 |
|---|---:|---|
| `critical_wave_growth.pdf` | 88702 | `a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988` |
| `critical_wave_verification.zip` | 241890 | `1da933750640177045808de748dd7f5732c33277377285b688a411f9f89771a0` |

The actual six-page PDF was read completely, as was `manuscript/critical_wave_growth.tex`. The PDF's complete abstract and its TeX source agree after typographical rendering. `abstract-source.tex` preserves the original source text; `content.json` retains every abstract sentence, with TeX-to-Unicode conversion only. The candidate is not a summary substituted for the abstract.

## 2. Full custody and reader coverage

The ZIP contains 113 regular members. Every archive member passed CRC validation and was extracted only after relative-path, traversal, duplicate-path, link and file-type checks. Original modes are recorded; all are `100644`. There are no hidden files, embedded PDFs or nested archives, also checked by file signatures rather than filename extensions alone. The single distinct reader PDF is the six-page public manuscript. Every extracted member was re-compared byte-for-byte with the public ZIP, and every entry in the package's own file manifest was hash-checked without executing a verifier.

`sources/record.json`, `receipt.json` and `archive-inventory.json` retain the public evidence. `custody-checks.json` records this scope pass's recheck. Source files were not repaired or altered. Raw external primary PDFs are separate cached references, not additional inventory papers or public download assets.

The support distribution includes the current TeX; seven standalone check scripts; expected reference receipts; a wrapper; dependency pins; and extensive historical submission, review and priority material. Historical assessment bodies were kept opaque. Merely retaining or hashing them does not constitute reading or adopting their judgments.

## 3. Exact analytic and control setting

The model is the real, defocusing, energy-critical quintic equation `y_tt − Δy + y^5 = u` on the three-dimensional unit ball B, with homogeneous Dirichlet trace, zero position and velocity initially, and final time T=1. The state is in the compatible energy/Strichartz class: position continuous in H₀¹(B), velocity continuous in L²(B), and position in L⁴(0,1;L¹²(B)). It is not assumed to remain in the first spatial eigenmode.

Controls lie in L²(0,1;H), H=L²(B), with `‖u(t)‖_H ≤ ρ` for almost every time, where ρ is a sufficiently small fixed positive number. This is a spatially integrated, pointwise-in-time Hilbert-ball cap. It is **not** a pointwise space-time amplitude bound. All appearances of control L¹ and L∞ refer to time with values in H; control L² is equivalently L² time-space. H⁻¹(B) is the dual of H₀¹(B).

The cost contains terminal-position tracking, the fourth power of the L⁴-time/L¹²-space state norm with coefficient 1/4, and the L¹-time/H control norm with coefficient 1. It removes only the quadratic control regularization (`β₂=0`); state regularization and sparsity remain (`γ=β₁=1`). Every fixed finite nonnegative terminal-velocity weight ν is permitted in the optional H⁻¹ terminal-velocity square. Setting ν=0 recovers the cited article's objective. No ν=∞ or arbitrary nonlinearity/boundary/domain assertion follows.

## 4. Claim and quantifier map

Theorem 1 asserts an existential cap ρ*>0, and then all `0<ρ≤ρ*` and fixed finite `ν≥0`. The selected target is `d=πe`, where e is the explicitly normalized first radial Dirichlet eigenfunction. The global optimization is over all admissible controls, not just radial or one-mode controls.

1. Zero is the unique global optimizer. The lower bound is `Δ(u) ≥ A³/(12ρ²)` for every feasible u, where `A=‖u‖_{L¹(0,1;H)}`. The cap and this base-target bound are independent of ν. No numerical value of ρ* or a hidden PDE constant is supplied.
2. The ordinary critical cone is `{0}`. Thus the source's strict substitute second-variation test on nonzero critical directions is vacuously satisfied. This is not positive coercivity of a Hessian on all control directions. The norm's substitute second variation is not presented as a classical second derivative of a norm.
3. Pulses `u_h=he 1{|t−1/2|<h}` are feasible for `0<h<min(ρ,1/2)`, converge in L∞(time;H), have squared L² norm `2h³`, and have objective gap `(π²/3+2/π²)h⁴+O(h⁶)`. Therefore no positive L² quadratic-growth constant works in either an L² or L∞ control neighborhood.
4. Global optimizers exist for every terminal target d∈H in the capped setting. Along the particular radial target ray `d_ε=(π+ε)e`, every choice of global optimizers has `‖u_ε‖₂/ε→∞`. This is a universal statement over optimizers along that ray, not merely a bad selection.

Corollary 3 separately retains local L¹ quadratic growth `Δ(u)≥‖u‖₁²/(4π²)`. Relative to the fixed base optimizer zero, arbitrary small target perturbations w have upper estimates `‖u‖₁=O(‖w‖_H)` and `‖u‖₂=O(√‖w‖_H)` for every global optimizer. Their constants and upper-bound neighborhood can be chosen uniformly in finite ν. On the radial ray, the claims sharpen to `‖u_ε‖₁=Θ(ε)` and `c ε^(3/4)≤‖u_ε‖₂≤C√ε`; the lower-comparison neighborhood can depend on the fixed ν.

The paper expressly does not assert sharpness of this exponent bracket, uniqueness of perturbed optimizers, pairwise Lipschitz selection, or L∞ convergence of perturbed optimizers. A failure of Lipschitz response relative to zero is compatible with the stated vanishing upper bounds. The example at target zero at the end of the paper also distinguishes the result from universal failure of all unregularized quadratic growth.

The most useful editorial point is the coexistence of a unique global optimizer and a vacuously satisfied ordinary cone test with concentrating controls that defeat strong L² growth, while weaker L¹ growth survives. This is an explicit realization in the stated nonlinear wave model of an established concentration/noncoercivity mechanism, not the discovery of that general mechanism.

## 5. Proof-support map, without mathematical clearance

The manuscript contains the full current proof. Its analytic chain is: bounded-domain linear energy/Strichartz estimates; small-input fixed point and a fifth-order nonlinear remainder; an eigenmode projection of the linear endpoint; a cap-constrained second-moment estimate yielding global uniqueness; concentration pulses giving the growth quotient; compactness/direct-method existence; a perturbed-target trial comparison; and the terminal tracking square yielding weaker-norm estimates.

Lemma 2 explicitly uses a compatible zero-data state space, and obtains smoothness locally through the residual `y+L(y⁵)−Lu`. Its argument does not require an inverse onto arbitrary continuous position/velocity pairs. The paper marks the eigenmode identity as a projection of the **linear** state and does not assume nonlinear invariant-span reduction. These distinctions must survive any editorial condensation.

I statically read all seven current `checks/` scripts and the `verify_all.py` wrapper. They check eigenfunction identities, interpolation exponents, pulse formulas, finite rational moment comparisons, threshold-cap formulas, normalized weak-null expressions, target exponents, and the weaker-norm algebra. One script additionally includes five high-precision diagnostics explicitly labeled noncertified. The two scripts with “bridge” names are finite symbolic identities, not a substitute for historical or PDE validation. Their comments sometimes refer to earlier analytic review; such incidental status language was not adopted.

The dependency file pins SymPy1.14.0 and mpmath1.3.0. The wrapper checks the file manifest, copies check scripts into temporary directories and compares complete emitted receipts, ignoring only time/runtime informational fields. It uses ordinary Python assertions, as do several scripts, so optimized-Python behavior should not be assumed from static inspection. I did not execute any mathematical script, validate reference-receipt counts, solve the PDE numerically or certify the unknown analytic constants. The wrapper's reported aggregate counts are package claims only. Separate mathematical reviewers own proof reconstruction and meaningful fresh controls/replays.

## 6. Original question and load-bearing primary interfaces

Nine full raw primary PDFs were freshly acquired with version, URL, size, SHA256 and timestamps recorded. Acquisition of a full body is distinct from reading every page: `primary-interface-map.json` records the actual passages read and the remaining limits.

**Kunisch–Meinlschmidt, arXiv1907.02744v1 (42 pages).** I read the model and cost definitions, uniqueness/linear estimates and local mild-solution interface, Theorem4.3's state-map discussion, the critical cone and substitute second variation, and Theorem4.17 with its coercivity proof. The domain is bounded smooth in ℝ³, with homogeneous Dirichlet conditions and L¹-time/L²-space forcing. Lemma2.9 provides the energy and L⁴-time/L¹²-space estimate. Theorem4.17 assumes positive β₂ and concludes control-L² quadratic growth in an L∞(time;L²(space)) neighborhood. That restriction is explicitly what the submitted paper removes in its counterexample. The local compatible-space proof in the submitted paper is important; this scope report does not recursively certify all of the source's global PDE analysis.

**Original Oberwolfach Report9/2021 (88-page report), Meinlschmidt contribution printed438–440.** The whole contribution was read. It includes the optional H⁻¹ velocity term and places the β₂=0 question immediately after the strong quadratic-growth implication. Its displayed growth neighborhood is L², whereas the inspected article's Theorem4.17 uses L∞. The submitted pulses address both. The exact historical statement supports “failure of retaining the implication unchanged.” It does not support a claim that all possible zero-regularization sufficient conditions are impossible, or that the question remained globally open until2026.

**Blair–Smith–Sogge, published Ann.IHP AN26(2009),1817–1829 (13 pages).** The model, Theorem1.1, Corollary1.2 and relevant estimate discussion were read. In dimension3, `(p,q,γ)=(4,12,1)` satisfies the displayed allowed range on a compact smooth-boundary manifold. This is the underlying classical estimate referred to by the wave-control source. The full microlocal proof and its older references were acquired but not recursively reviewed here.

**Earlier optimization mechanisms.** I read Casas–Tröltzsch2015 Example4.16's Dunn counterexample and the extended-cone discussion; Christof–Wachsmuth's NDC sufficient condition and Legendre-form criteria; Borchard–Wachsmuthv1's NDC condition and growth-implies-NDC proof; Herzog–Stadler–Wachsmuth's group-norm subgradient formula/proof; and relevant introductory/extended-cone scopes in the L¹-growth and parabolic sparse-control literature. These establish the need for explicit prior credit and explain why a weak-null sequence can escape an exact-cone test. They are not claims of an earlier identical wave counterexample.

A publisher erratum for Herzog–Stadler–Wachsmuth corrects Lemma3.6; its primary metadata/abstract were inspected, not its full body. The current attribution concerns group subgradients in Lemma2.2, not the corrected lemma. The 2012 Casas–Tröltzsch reference was not independently acquired in this pass; the directly inspected 2015 source suffices for the attributed Dunn example. Not every bibliography item or every primary page was reviewed. The bounded historical priority audits inside the ZIP were not read or adopted, and no absence-of-antecedent claim is made.

## 7. Editorial candidate and remaining gate

`content.json` provides the full original abstract, plain explanation, exact result and limits, credited primary background, professional collaboration wording, truthful AI/unrefereed status, version/date/DOI and both public assets. It is a local candidate only. It uses no public replay of internal verification steps. `follow_up` is null: neither the rate bracket nor generic PDE variations were promoted into a research question without a stronger case.

The public page, if independently cleared later, must retain the pointwise-in-time Hilbert cap; β₂-only regularization removal; zero critical cone; retained state/sparse costs; fixed finite ν and its uniform/nonuniform neighborhoods; all-optimizer versus fixed-basepoint distinctions; and unknown priority. Mathematical clearance, promotion and publication remain separate. No website, spreadsheet, Git, release, deployment or outreach action was taken. All previous sealed reviews remain untouched.
