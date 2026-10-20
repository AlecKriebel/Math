# Public sources and verification limits

Source-verification and audit date: 2026-10-20. This file records public references, inspection scope, and imported dependencies. It includes no copied paper, source PDF, dataset contents, or private research material. Inspection statements summarize the source checks recorded during the research and audits; package preparation is not a claim of a new literature search.

## Original problem

**Hermann Thorisson, Some Open Probability Problems.** Public preprint: https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf . Section 3, printed pp. 3–4, supplies the process definitions, equations, neighboring problems, and exact Problem 3.2. The whole section was read, and rendered pp. 3–4 were visually checked. The state space is general measurable; the separable-metric/Borel restriction starts only later, for the separate weak-convergence discussion.

The PDF was retrieved by ordinary HTTP after a web fetch timed out. Inspection metadata:

- Bytes: 107028.
- SHA-256: `efe6b6e78e36185a2b278ba0cf5593c2e92f43b479f80159d6f6b7ecc4f6efaf`.
- Target location: Problem 3.2 on printed p. 4.
- Verification scope: full Section 3 and its hypotheses, not merely the problem sentence.

**Hermann Thorisson, Open problems in renewal, coupling and Palm theory.** Queueing Systems 68, 313–319 (2011). DOI: https://doi.org/10.1007/s11134-011-9241-2 . The publisher's inspected record gives online publication July 1, 2011 and an August 2011 issue date; its abstract matches the preprint's four subject groups. The final journal full text was subscription-only in the inspected page. Exact numbering and wording in this package are therefore attributed to the public preprint, not independently verified in the final journal PDF.

The preceding source theorem distinguishes distributional exact coupling, which retains a time coordinate in the distributional identity, from distributional shift coupling, which does not. Its Cesàro-TV conclusion does not answer the nonaveraged setwise question. These source results are context, not new claims of this package.

## Rank-one obstruction and existence input

**V. V. Ryzhikov, Weakly homoclinic groups of ergodic actions.** Primary preprint: https://arxiv.org/pdf/1901.09028 . Theorem 8, pp. 9–11, was inspected. It treats graph automorphisms and motivates the tower argument. It is not cited as proving the arbitrary-bistochastic extension. That extension is explicitly proved in ATTEMPT_2.md and examined in AUDIT.md.

**Darren Creutz and C. E. Silva, Mixing on a Class of Rank One Transformations.** Primary preprint: https://arxiv.org/pdf/math/0109159 . The inspected locations are Section 2.1, Section 7.1, and Theorem 10 (Adams), printed p. 23. The setup uses invertible probability-preserving transformations on a standard nonatomic space; staircase spacers are s_{n,i}=i and restricted growth is r_n²/h_n→0. Attempt 2 uses r_n=n+2 and verifies finite total measure, r_n→∞, and restricted growth. The resulting mixing conclusion is imported from this theorem, not independently reproved.

An attempted original Ornstein PDF retrieval returned HTTP 403. No bypass was attempted and no claim depends on having inspected that inaccessible PDF. The accessible Creutz–Silva preprint supplies the stated existence dependency.

## Classical analytic inputs and comparison literature

**Robert Gardner, measure-theory lecture material, Section 18.5.** University exposition and proof of the applicable Vitali–Hahn–Saks theorem: https://faculty.etsu.edu/gardnerr/5210/Beamer-Proofs/Proofs-18-5.pdf . Used to identify the uniform-absolute-continuity input in COUPLING_CRITERIA.md. This is an exposition of a classical theorem, not a priority citation for a new result.

**Peletier, Rossi, Savaré, and Tse, Jump processes as generalized gradient flows.** Published open-access article: https://link.springer.com/article/10.1007/s00526-021-02130-2 . The inspected Section 2.1 uses a general measurable space; Section 2.2, equations (2.3)–(2.5), records the relation between setwise convergence and weak L1 convergence under a common dominating measure. This supports the classical nature of the analytic reduction. It is not represented as an exact prior statement of the present orbit-coupling theorem.

**Carmona, Tangpi, and Zhang, Conditional McKean-Vlasov control.** Primary preprint, version 1: https://arxiv.org/html/2510.06543v1 . The inspection of Lemma 5.4, Remark 5.5, and the lemma's proof records a use of Mazur's lemma to obtain TV convergence of finite tail convex combinations after weak L1/setwise convergence. The surrounding control result is neither audited nor used here. The comparison is evidence that the convexification step is established methodology, not a novelty conclusion about the full coupling formulation.

Radon–Nikodym, finite-measure L1 duality, Hahn–Banach separation, and countable products of probability measures are classical inputs. The proofs in this package spell out their applications and the necessary common-part or finite-cell constructions; no newly discovered functional-analytic theorem is claimed.

## Contemporary manuscript and bounded status search

**Rafik Zeraoulia, Setwise Asymptotic Stationarity Does Not Imply Total Variation Asymptotic Stationarity: An Explicit Counterexample.** DOI: https://doi.org/10.2139/ssrn.6361341 . Repository record: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6361341 . Search-indexed primary repository metadata reported seven pages and a March 6, 2026 posting. Its abstract claims a negative answer to Problem 3.1 using independent coordinates with oscillatory densities on [0,1], not a characterization for Problem 3.2.

Direct record retrieval failed; the delivery endpoint and direct download returned HTTP 403. No access-control bypass was attempted. The full proof, infinite-path setwise argument, peer-review status, and any implication for Problem 3.2 were not verified. The independent Bernoulli-orbit proof in Attempt 1 does not rely on that manuscript. Neither validation nor criticism of its uninspected proof is claimed.

**Hermann Thorisson, Coupling and convergence of random elements, processes, and regenerative processes** (1994). Public institutional record: https://iris.hi.is/en/publications/coupling-and-convergence-of-random-elements-processes-and-regener/ . DOI: https://doi.org/10.1007/BF00994259 . The inspected abstract concerns density-liminf and eventual-coincidence criteria among other topics; it does not by itself verify the present setwise characterization.

A bounded search did not find an inspected primary source establishing the intended or novel resolution of Problem 3.2, or exactly the complete formulation of Attempt 3. This is not proof of openness, exhaustive coverage, or priority. The final scope remains: a proved general auxiliary-copy random-time equivalence, accepted accompanying partial results, and no unqualified named-problem resolution claim.
