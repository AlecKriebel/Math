# Independent mathematical review: exact low Heegaard-distance thresholds

Review date: 2026-10-21 UTC. Target: Birman Problem 2.5, ordered row 1892, ID 11000162.

## Exact artifact binding and verdict

This review applies to `ATTEMPT_REPORT.md`, 15,639 bytes, SHA-256:

`a6d98f3033f8b7a39840ec4bc248a48b5bee7180e54607f9970336d1e023aa63`

The initial supplied artifact had SHA-256 `8b0a6ce699cd65dd6bdcfcf2c0b6d5141b9910540fffbd4e98a7d1f76e9a42f0`. Before acceptance, its Casson–Gordon source attribution was corrected, and a primary-source example was added to make the failure of the hyperbolicity converse explicit inside the second promise. The final hash above was recomputed, and both changed passages and the added reference were reread. Neither change alters the semidecision proofs or the non-solving disposition.

**Verdict: PASS as a bounded, non-solving mathematical audit. NOT ACCEPTED as a solution of either promised decision problem.** No remaining mathematical error was found in the explicitly accepted partial results. The report correctly exposes, rather than conceals, the missing termination/completeness arguments. This verdict is about the bound artifact and its stated claims, not a proof of worldwide openness or an independent validation of the complete 2025 preprint.

## 1. Target, promises, and full disk sets

The retained Birman compilation, printed p.149, states the two successive promised threshold questions. The report preserves them: first assume d >= 1 and distinguish 1 from >= 2; then assume d >= 2 and distinguish 2 from >= 3. It uses closed orientable splitting surfaces of genus at least two and the ordinary disjointness curve graph.

The endpoint sets are the full disk sets A and B. The report never replaces them by the finitely many disks of an input cut system. Its inequality for finite subsets is correct: minimizing over fewer endpoints gives an upper bound on the full-set distance. Failure of finite-subset searches cannot establish a lower bound.

Both promises are essential to the labels returned by the proposed semialgorithms. Off promise, the same witness tests certify only d <= 1 or d <= 2, respectively. The report explicitly does not claim to verify the promises.

## 2. Effective enumeration and disk membership

PASS. With an effective boundary identification and a handlebody cut system, the inclusion-induced word in a free basis of pi_1(V) is computable. A simple essential boundary curve is a meridian exactly when that word freely reduces to the identity. The forward direction is immediate; the reverse direction uses the embedded-disk conclusion of Dehn's lemma, with properness at the boundary. The prior essentiality check ensures the disk is essential. This is not the invalid test of merely having zero homology class.

Normal-curve coordinates on a fixed surface triangulation give an effective enumeration; connectedness and essentiality must be filtered as stated. Every isotopy class has a finite representative, and each bounded coordinate range is finite. Duplicate representatives cause no logical problem. No running-time bound is claimed.

## 3. Fixed-curve minimization and the two semidecisions

PASS. Masur–Schleimer Lemma 21.4, printed p.58, explicitly provides a disk minimizing geometric intersection with one specified curve over all essential disks of the handlebody. Thus the report's m_V(c) and m_W(c) are exact computable integers. The theorem is used for its actual objective, not as an exact closest-point oracle in the curve graph. This review verifies the published lemma's statement and applicability, not a new proof of its underlying Whitehead/Zieschang algorithm.

For the first threshold, if a in A has m_W(a) = 0, a minimizing b in B has i(a,b) = 0. Equality of their isotopy classes would give d = 0, contrary to the promise. The distinct disjoint vertices therefore give d = 1. Conversely every distance-one pair supplies an a eventually enumerated. Each iteration terminates, so a positive instance reaches its witness; a negative instance need not halt.

For the second threshold, both minima vanishing supplies a in A and b in B with i(a,c) = i(c,b) = 0. If c were equal to a or b, the full disk sets would have distance at most one, contrary to d >= 2. Thus the two required edges exist and d <= 2, hence d = 2. The endpoints a and b cannot coincide or be disjoint under this promise either. There is no simultaneous-realization gap: on a closed genus-at-least-two surface, geodesic representatives in a hyperbolic metric realize these disjointness relations. Conversely the middle vertex of any length-two realizing path passes both tests.

These arguments prove precisely two lower-alternative semidecisions. The complementary universal disk-busting statement is not converted into a finite certificate. A computable bound on low witnesses would make each finite-prefix search total, as the report states conditionally. No such bound is established.

## 4. Normal surfaces and simultaneous constraints

PASS as a gap diagnosis, not as an impossibility result. The proposed finite reduction needs a theorem retaining the simultaneous boundary-disjointness conditions while replacing both disks by objects in uniform finite lists. Individual fundamental-surface results or an algorithm relative to one already fixed boundary curve do not by themselves prove that assertion. Adapting a triangulation to the unknown other witness would not supply the missing input-computable bound.

The punctured-torus slope example correctly illustrates that smoothing curves can destroy their separate geometric intersections with another curve. It is not a counterexample to a precise theorem about compatible fundamental normal disk summands. The report expressly makes that limitation; the review does not promote the illustration into such a counterexample.

For the second threshold, the unknown middle curve adds another unbounded variable. Finite train-track types do not mean finitely many carried curves, and carried curves need not be mutually disjoint. Euler characteristic and matching equations alone do not prove all required component, topology, essentiality, and simultaneous-avoidance conditions. These are missing arguments in the proposed route, not proofs that no normal-surface solution can exist.

## 5. Coarse distance and integer intervals

PASS. Masur–Schleimer Theorems 21.1 and 21.2 are additive approximation and approximate projection statements. The report correctly separates them from Lemma 21.4. A justified bound |d - N| <= R gives the integer interval [ceil(N-R), floor(N+R)]. Intersecting this interval with the appropriate promise yields the stated sufficient tests. A valid bound and a promised input cannot produce an empty intersection; emptiness would indicate inconsistent data or assumptions, not an additional distance certificate.

An interval containing both threshold alternatives decides neither. Repetition does not produce an accuracy parameter absent from the theorem. Likewise a bounded curve-graph radius is not a finite search: local infinitude prevents that inference. The finite marking-graph search in the cited algorithm is not silently transferred to an exact disk-set search. The report also does not pretend to have extracted a convenient numerical error constant from the source.

## 6. Rectangle certificates and the 2024/2025 scope distinction

PASS. Koda–Takao Theorem 1 gives a sufficient strong-irreducibility criterion. Its disk systems can be nonmaximal. Given finite diagrams, the stated finite combinatorial hypotheses can be checked, so enumerating qualifying diagrams is a sound high-side certificate search for the first threshold. Nothing in the inspected theorem states that every strongly irreducible splitting appears in that search.

Kwon–Kang–Lee Theorem 1.7 and Definition 3.1 concern the existence of a strongly irreducible genus-two splitting for which no pair of the specified maximal-system pants decompositions satisfies their classical rectangle condition. Their quantifier is over all such decompositions, not merely one chosen diagram. The report accurately identifies this as the preprint's claim and does not claim to have independently audited its proof.

Importantly, excluding classical maximal-system certificates does not automatically exclude the 2024 generalized certificates over arbitrary disk systems. The report does not make that invalid transfer. Nor does a counterexample to completeness of a certificate class imply undecidability.

For the second threshold, strong irreducibility establishes only the already-promised d >= 2. Koda–Takao's introduction also reports both finite and infinite Goeritz groups at distance two, so finiteness alone is not a d >= 3 certificate. The report's dovetailing terminates only on the stated certified subclasses unless a completeness theorem is added.

## 7. Topological partial cases and the attribution repair

PASS. Under d >= 1 the splitting is irreducible. Haken's lemma also rules out a reducible ambient manifold. If d = 1, the splitting is weakly reducible, and Casson–Gordon gives a closed incompressible positive-genus surface. Therefore verified non-Hakenity excludes d = 1 and, with the promise, proves d >= 2. Here non-Hakenity means the absence of the relevant two-sided closed incompressible positive-genus surface; it must be verified, not assumed from failure to find one.

The initial attribution to Birman's earlier summary was unsuitable: that retained passage uses the wrong irreducibility wording for the implication at issue. The final report instead cites Koda–Takao's introduction, printed p.2, which states the correct implication, and acknowledges the apparent wording error. This resolves the source-support defect without changing the correct mathematical argument.

For the second threshold, Haken's lemma, Hempel's toroidal/Seifert distance bounds, and geometrization give d >= 3 implies M hyperbolic in the stated closed orientable setting. Consequently verified nonhyperbolicity and d >= 2 force d = 2. This is a contrapositive, not an equivalence. Hempel's paper also records hyperbolic manifolds with distance-two splittings, so the converse fails even within the second promise. His introduction confirms that stabilization reduces distance to zero. These independent source checks support the final report's nonconverse and stabilization warnings. See [Hempel, introduction and Corollaries 3.7–3.8](https://arxiv.org/pdf/math/9712220).

The almost-normal-list and Heegaard-genus discussion remains appropriately conditional: existence of a list or a manifold invariant does not, without additional algorithms and proofs, recognize the distance class of the specified splitting. The report does not assert that those missing algorithms are impossible or nonexistent in all literature.

## 8. Sources checked and acceptance limits

The review checked the retained primary texts at the cited statements and recomputed their PDF hashes against the supplied public metadata:

- Birman/Farb compilation: `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`.
- Masur–Schleimer: `e227edb01b2ee5b0029889fa2eb62fa60ea5ccf008cc44d83a6eb6468a97e477`.
- Koda–Takao v2: `f15aef71401550047c478e993b28f3be9ea1ba11c61c2beb67d52d83a72a4e26`.
- Kwon–Kang–Lee v1: `a42694d90a1c8fb3fe22182a89bd97468e7a2ad39d851f1fc445d18681149cdd`.

Hempel's public arXiv page and PDF were additionally opened on the review date. No byte-equivalence claim is made for that supplemental web view. This review did not reperform the separate repository-duplicate search, full corpus identity audit, or worldwide literature search. It does not independently validate the 2025 proof beyond the theorem and definition scope just described.

Accepted: full-disk-set witness logic, the two promised semidecisions, the published fixed-curve minimization oracle, conditional bounded-witness reduction, safe interval filters, correctly scoped certificate dovetailing, and the two topological special cases.

Not accepted: totality of either universal decision procedure, completeness of either rectangle family, a general finite normal-surface reduction, an undecidability claim, or a claim that the original problem has been solved.

No source report, queue, repository branch, or publication was modified by this review. Any later substantive change to the reviewed report requires a new hash binding and review of the change.
