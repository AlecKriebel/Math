# Related results in OpenAI's mathematics collection

Comparison completed on **6 October 2026 (America/Los_Angeles)**. OpenAI snapshot: [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a), containing 722 manuscripts in 372 families.

**Yes: there are substantive connections, including two conditional consequences for our drafts.** The most consequential is a possible negative answer to the original Hopfian wreath-product question in PR #389. A planar Fourier certificate would also settle the dimension-two subcase of PR #487. Both implications were independently checked, but the underlying new OpenAI proofs were not audited in this comparison. No existing research status, proof, branch draft, or queue entry has been changed.

The [OpenAI README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) describes results at different verification stages. Here, “claims” means the pinned manuscript states the result. It does not mean this comparison certifies it. Manuscript dates also do not by themselves establish the date of public disclosure or priority.

## Two actionable conditional consequences

### 1. Family 197 would answer our Hopfian wreath-product question negatively

Our [draft PR #389](https://github.com/AlecKriebel/Math/pull/389), problem 2531 / Kourovka 21.22, asks whether the standard restricted regular wreath product of two finitely generated Hopfian groups is Hopfian. Its current packet records partial results and an unresolved abelian group-ring obstruction.

OpenAI's [A Torsion-Free Group Algebra That Is Not Directly Finite](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/direct-finiteness.pdf), Theorem 1.1, claims a finitely presented torsion-free group G and elements in F₂[G] with ab=1 but ba≠1.

Bradford–Fournier-Facio's published [Hopfian wreath products and the stable finiteness conjecture](https://d-nb.info/1355447615/34), Theorems 1.3/4.11, equates Kaplansky direct finiteness with universal Hopficity of abelian-base wreath products over finitely generated Hopfian acting groups. Thus the claimed counterexample would negate our original universal assertion. Their proof supplies the required embedding in a finitely generated Hopfian group, so the original OpenAI G need not itself be Hopfian. One can take the lamp group to be C₂.

This is **conditional resolution of the original question**, rather than just shared terminology. It does not resolve the separate nonabelian free-base subquestion. The short semidirect-product derivation is recorded in `direct_finiteness_wreath_derivation.md`; an independent adversarial review checked the hypothesis bridge and the noninjective epimorphism. A full audit of the OpenAI construction is required before revising our problem's status.

### 2. Family 090 would add dimension two to our sharp three-point bound

Our [draft PR #487](https://github.com/AlecKriebel/Math/pull/487), problem 20001754 / AIM 1.32, studies the triangle three-point lattice bound and its relation to the two-point Cohn–Elkies bound. Its retained proof identifies sharp equalities in dimensions 1, 8, and 24, leaving the all-dimensional question unresolved.

OpenAI's [A sharp Fourier certificate for planar circle packing](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/paper.pdf), Theorem 1.1, claims a real radial Schwartz function with Fourier transform nonnegative, f(x)≤0 for |x|≥1, f̂(0)=1, and f(0)=2/√3. These are exactly our L₂ conventions.

Combining that claimed function with our retained product-program upper bound and the triangular-lattice Poisson lower bound gives

\[
L_2=\frac{2}{\sqrt3},\qquad P(C_\triangle)=\frac43.
\]

An independent check found no Fourier-phase, regularity, sign-boundary, or density-normalization mismatch. The triangular lattice's **number density** is 2/√3; its covered-area density is π/(2√3). Confusing these would give the wrong objective. The derivation is in `combinatorics_overlap/planar_triangle_bound_derivation.md`.

This is **conditional resolution of a specific subcase**, not the general optimizer-conversion or all-dimensional equality question. The new analytic/interval certificate was not replayed.

## Closely related main projects and drafts

| OpenAI result | Our work | Precise relationship and boundary |
| --- | --- | --- |
| [149: Uniform permanence for weakly reversible mass-action systems](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/permanence.pdf) | `bimolecular_positive_recurrence_submission_v1_2_4`; deterministic reversible realizations and Turing programs | Claims deterministic ODE permanence for every finite weakly reversible fixed-rate network, with a common compact positive absorbing set per class. Our stochastic theorem proves nonexplosion and positive recurrence for integer-population chains with one linkage class and molecularity≤2. Neither statement implies the other as stated. Deterministic permanence permits equilibrium continua and does not settle diffusion-driven instability. The manuscript itself credits earlier single-linkage deterministic permanence. |
| [188: Sharp terminal leave in random triangle removal](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026.pdf) | [Draft #754](https://github.com/AlecKriebel/Math/pull/754) | Exactly the same uniform triangle-removal process from Kₙ. Claims terminal edges asymptotic to n^(3/2)/(2√2), with L² convergence. Our question controls joint inclusion probabilities of arbitrary prescribed triangle families at an earlier horizon. Terminal size and two moments do not supply the required spread bound. |
| [039: Nagata's conjecture for plane curves](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Nagatas-Conjecture-for-Plane-Curves-September-23-2026/main.pdf) | [Draft #712](https://github.com/AlecKriebel/Math/pull/712) | Claims the Nagata premise of our original question for r≥10 and gives multipoint Seshadri results. Our draft already credits recent preprints for irrational single-point constants on plane blowups for every r≥9. Multipoint constants on the plane are different from single-point constants on the blowup; r=9 is outside the strict Nagata statement. |
| [360: Global support and convex injectivity domains under weak MTW](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Global-Support-and-Convex-Injectivity-Domains-under-Weak-MTW-September-25-2026/paper.pdf) | [Draft #400](https://github.com/AlecKriebel/Math/pull/400) | Same weak MTW/A3w framework. Claims convex tangent injectivity domains on closed manifolds and transport regularity. Our unresolved implication requires full cross-curvature nonnegativity, including nonorthogonal directions. The checked theorem does not assert that stronger conclusion. |
| [291: Cuntz comparison and Jiang–Su absorption](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Cuntz-comparison-and-Jiang-Su-absorption-September-23-2026/paper.pdf) | [Draft #797](https://github.com/AlecKriebel/Math/pull/797) | Potential route from Cuntz-semigroup properties to absorption in separable nuclear cases. Our corrected ordinary-closeness result does not assume nuclearity or separability and stops at scaled-Cu transfer. The precise property-transfer bridge remains to be checked; this is not an established solution to general perturbation stability. |
| [156: Nine-dimensional Borsuk counterexample](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/paper.pdf) | `borsuk_dimension4` | Same covering conjecture, different dimension. The claimed projector example lives in the nine-dimensional trace-one symmetric-matrix space even though its lines are in R⁴. It does not answer our five-piece question in Euclidean R⁴. |
| [179: Circulant Hadamard conjecture](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-circulant-Hadamard-conjecture-September-23-2026/paper.pdf) | `hadamard_668_search` | Claims full circulant Hadamard matrices have orders only 1 and 4. Our target allows arbitrary order-668 Hadamards. Circulant blocks, cyclic difference families, and Legendre-pair constructions need not make the complete matrix circulant. The headline H(668) question is unaffected by the stated theorem. |
| [170: Sharp logarithmic exponent of r(5,t)](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Sharp-Logarithmic-Exponent-of-r-5-t-September-24-2026/paper.pdf) | `ramsey55`; `ramsey55_endpoint_capacity` and its retained branch | Claims r(5,t)=t⁴/(log t)^(3+o(1)) as t→∞. This supplies no decision at t=5 and does not improve our exact R(5,5) certificates. |
| [001/032: CM Hodge classes and specialization](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026/paper.pdf) | [Draft #799](https://github.com/AlecKriebel/Math/pull/799) | Shared CM-reduction setting. Our extra Tate classes are non-Lefschetz, which does not mean nonalgebraic. The claimed algebraicity theorem is compatible with four extra Tate dimensions represented by cycles beyond divisor products. |
| [167: Planar distances and unit-distance bounds](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-power-saving-for-planar-unit-distances-September-23-2026/paper.pdf) | [Draft #738](https://github.com/AlecKriebel/Math/pull/738), [draft #725](https://github.com/AlecKriebel/Math/pull/725) | Relevant repeated-distance estimates. A superlinear one-distance multiplicity bound does not force two distances of multiplicity≤n, and the checked pinned-distance statement does not improve our already imported n/log n diameter estimate. |
| [272: Entanglement with zero distillable secret key](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/paper.pdf) | `werner_npt_bound_entanglement`; Bell/privacy work | The claimed PPT-based example is outside our NPT Werner family. Secret key, singlet distillation, and Bell-value randomness have different operational definitions. It does not settle our all-copy two-block-positivity question. |
| [277: Threshold repetition for entangled games](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/paper.pdf) | Cyclic Bell values, qubit POVM/PVM setting minimality, quantum coloring | Shared finite-dimensional game framework; repetition takes the one-shot value as input. It does not determine our values, equality structure, or minimum input architecture. |

Additional selected connections, including billiards, Ricci flow, inverse diffusion, affine fibrations, disk embedding, and Artin groups, are documented in the three approach reports. Their mechanisms and missing hypotheses are recorded separately from the two direct conditional deductions.

## Catalogue nonmatches and excluded shortcuts

No direct counterpart was located in the pinned catalogue/abstract map for our 14-variable Keller/Special Image/every-order Vanishing constructions, iterated Keller monodromy, gamma–theta eternal-domination results, five-dimensional kissing-number target, exceptional local Yang–Baxter operator, or minimum qubit POVM/PVM input architecture. This is a bounded catalogue result, not proof that no related lemma occurs anywhere in the collection.

Nearby affine cancellation and stable-coordinate counterexamples (families 047/049) do not supply a Keller theorem. The MUB-count claim in dimension six (266) does not establish the private-reference hypotheses or measurement minimality in our Bell papers. Rokhlin mixing for one Z-action (145) does not answer our algebraic Z²-action mixing draft #578. Independent critical percolation on quasi-transitive graphs (213) does not answer our dependent FKG/finite-energy/random-cluster drafts. Shared names, subjects, or words were not treated as evidence of logical implication.

## Coverage and reproducibility

The comparison screened the complete pinned catalogue, current root project inventory, all **781 open PRs (780 drafts)** with their bodies and head hashes, all **942 live remote branch heads**, the complete 882-PR state inventory, and local branch tips. Sixty-one remote branches lacked any PR in that inventory, including main and retained variants of existing work. Relevant main-project and branch artifacts and selected immutable draft proofs were inspected; every file of every branch was not read.

Three independent approach families examined algebra/topology, combinatorics/probability, and analysis/physics. A fourth agent checked the two conditional deductions and sought false scope implications. The source tree's first recursive response was truncated; the preprints subtree was then fetched directly and was complete (12,785 entries, `truncated=false`). This correction matters for file-level coverage.

Captured source inputs, head inventories, hashes, and selected downloaded manuscripts are retained locally in ignored source folders. Authored evidence is in:

- `algebra_overlap/findings.md`;
- `combinatorics_overlap/findings.md` and `planar_triangle_bound_derivation.md`;
- `analysis_overlap/findings.md`;
- `adversarial_comparison/AUDIT.md`;
- `direct_finiteness_wreath_derivation.md` and `RESEARCH_LOG.md`.

This effort establishes which statements are related and checks the short conditional bridges. It does not certify the new OpenAI proofs, claim priority, merge drafts, register a DOI, or contact anyone. Full proof audits of families 197 and 090 are the most useful next mathematical work before updating our existing findings.
