# Independent audit: Problem 30001405 / OWR-4196-003

Date: 7 October 2026. Rank: 975. Unrefereed mathematical audit; no novelty claim.

## Decision

**Accept the explicit counterexample to the literal set-approximant formulation. Do not record a solution or disproof of the intended open-approximant or continuous-projection problem.**

The frozen packet is mathematically sound within its stated scope. Its first-order transfer argument proves the required nonvanishing without using the disputed comparison. All three bridge lemmas are valid under the stated smallness and saturation assumptions. No mathematical correction is required. A supplied optional patch improves only the OWR pagination: the mathematical body occupies printed pages 27–28, while its last reference continues onto page 29.

The reviewed original manifest has SHA-256 `10a8affedf81c5d559356b842c6d7216f88c1fb143d66dce667f62804b4d013b`. It lists eight other public files. Every digest, the exact nine-file public allowlist, and the stored diagnostics were independently verified. The original packet was not edited.

## 1. Literal hypotheses and the full original context

I read the complete Berarducci contribution, including the final reference on printed page 29, and inspected the source pages visually. The report first restricts its **groups** to the definably compact, definably connected case, then explicitly passes to arbitrary definable sets and bounded type-definable quotients. In that generalized discussion, the listed fiber condition omits openness. The higher-homotopy conjecture strengthens simple connectedness to contractibility. No separate continuity requirement or global connectedness requirement on the quotient is imposed there. This is a wording finding, not evidence about an author's unexpressed intention. [Official OWR report](https://ems.press/content/serial-article-files/46259?nt=1), printed pp. 27–29; [DOI](https://doi.org/10.4171/owr/2010/01).

The example therefore tests the displayed generalized formulation, rather than a decontextualized group theorem. Its source space is itself definably connected and definably compact. The target is disconnected, but local contractibility does not imply global connectedness. Based homotopy groups remain defined at the specified point, and failure in degree 2 suffices regardless of conventions about degree 0.

## 2. Construction and every hypothesis

Choose a sufficiently saturated elementary extension M of the real ordered field in the pure ordered-field language. The language restriction is important to the transfer proof below. Put X = S²(M), N = (0,0,1), and partition X into A = {N} and B = X minus {N}. The relation that identifies precisely pairs in the same part is definable, so it is type-definable and has bounded index 2.

The singleton is definably contractible. For B, the stereographic map

    Q(u,v) = (2u/(1+r), 2v/(1+r), (r-1)/(1+r)),  r = u²+v²,

has positive denominator, satisfies the sphere equation, and never has last coordinate 1. Its inverse is P(x,y,z) = (x/(1-z), y/(1-z)). On B, 1-z is nonzero; the sphere relation gives the inverse identities. These are continuous rational maps on their stated domains. Thus Q((1-t)P(b)) contracts B to the south pole and fixes that endpoint throughout. No limiting argument at N is needed or asserted.

The two constant sequences A_j = A and B_j = B meet the fiber requirement. The weak-inclusion meaning of decreasing is conventional and explicitly fixed in the packet. It is not concealing a failed limit construction: the saturation lemma proves that any countable decreasing definable representation of either definable class eventually equals the class.

Every subset of the two-point quotient has a definable inverse image. Therefore every subset is logic-closed and logic-open. This target is discrete, compact Hausdorff, second countable, locally contractible, and a finite polyhedron. Every continuous based map from an ordinary connected positive-dimensional sphere to it is constant. All its positive-degree based homotopy groups vanish.

The map q is discontinuous because the inverse image of the open north-pole class is the nonopen singleton A. The displayed rational curve approaching N verifies this over M as well as over the reals. Its positive-parameter points lie in B, so B is not closed. The argument does not confuse the logic topology with the final topology of q.

## 3. The degree-2 obstruction, independently checked

In the sphere definition of the definable second homotopy group, the based identity of S²(M) can be zero only if it admits a definable continuous nullhomotopy H on X × [0,1]. Such a nullhomotopy would in particular contract the sphere, even if the based condition were dropped.

Choose the single ordered-field graph formula φ(p,b;c) actually defining this hypothetical H, with its finite tuple c of parameters. The following conditions are first-order for that fixed formula:

1. On D = X × [0,1], every input has exactly one output b in X.
2. The values at time 0 and time 1 are respectively the identity and the chosen constant; the basepoint may also be required to stay fixed.
3. For each p in D and each ε > 0 there is δ > 0 such that, whenever p' is in D and the two outputs are related to their inputs by φ, squared input distance less than δ² implies squared output distance less than ε².

All variables here range over the field. Domain, target, distances, and endpoints are given by polynomial formulas, and the parameter tuple is existentially quantified. This is a single first-order sentence, not a first-order quantification over all functions or graph formulas. Its truth in M would imply its truth in R, producing an ordinary continuous contraction of S²(R).

For the boundary of a tetrahedron, with ordered two-faces 012, 013, 023, 123, the integral boundary equations force every two-cycle to have coefficients (-d,d,-d,d). There are no three-simplices. Hence the second simplicial homology is infinite cyclic, generated by (-1,1,-1,1). The rational-rank computation in the script alone would not prove this integral assertion; the explicit integer coefficient equations in the written proof do. The generator is primitive, and the written calculation rules out any integral ambiguity.

Simplicial-to-singular comparison and homotopy invariance then contradict the contraction: the identity acts nontrivially on H₂ while a constant map factors through a point and acts by zero. The foundational references can be sharpened to Hatcher, Theorems 2.10 and 2.27. [Author's Chapter 2](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf).

Thus the definable second homotopy group is nonzero and cannot be isomorphic to the zero target group. The supplementary computation that it is Z is not needed for this contradiction. In particular, the counterexample does not reason circularly through a claimed quotient-comparison theorem.

## 4. Scope lemmas

### Definable decreasing intersections

If C = intersection_j D_j is definable and each D_j properly contains C, then the formulas x in D_j together with x not in C form a finitely satisfiable small partial type. Finite satisfiability uses the largest index among any finite list. Saturation realizes this type, contradicting the intersection equality. Hence some D_j equals C and every later term does too. The union of the parameter sets must remain smaller than the saturation cardinal, as stipulated.

Consequences: no countable decreasing family of definable open subsets can have a nonisolated definable singleton as intersection. Likewise, the nonclosed definable class B cannot admit a countable decreasing presentation by definable closed subsets. Requiring strict decrease at every index would exclude every definable intersection, not repair this example in a natural weak-inclusion reading.

### Finite definable quotients

Each class is definable using a representative, and the inverse image of every subset of a finite quotient is a finite union of classes. Thus its logic topology is discrete. Continuity of q is equivalent to all classes being open; finiteness then makes them clopen. For definably connected X, any nontrivial such finite definable partition contradicts continuity. Definable connectedness, rather than ordinary connectedness of a non-Archimedean space, is the correct notion in that last step.

### Countable fiber presentations

For a definable D, its E-saturation is type-definable. Indeed, express E by a small family closed under finite conjunction. Membership in the saturation is equivalent to having, for each such finite conjunction, a witness in D; saturation supplies a single witness for all conjuncts. Thus q(D) is logic-closed.

For C_y = intersection_j D_(y,j), put U_j = Y minus q(X minus D_(y,j)). Each U_j is an open neighborhood of y and its inverse image lies in D_(y,j). If V is any neighborhood of y, its complementary inverse image T is type-definable and disjoint from C_y. If every D_(y,j) met T, their formulas and those for T would be finitely satisfiable, hence jointly realizable. Therefore some D_(y,j) is disjoint from T, and U_j is contained in V. This proves first countability.

The proof supplies local countable bases only. It supplies no common countable global base and no triangulation. Those missing conclusions cannot be inserted into an application of a later theorem without further argument.

## 5. Version-sensitive literature control

The 2009 arXiv v2 is genuinely different from the 2011 publication: the saved preprint's Assumption 4.1 omits openness, whereas the indexed published page 567 includes it in part (3), and Theorem 4.4 includes continuity. I reproduced that published-page search result independently. Direct access did not yield a complete publisher PDF: OUP returned metadata/abstract HTML marked available for purchase, and CiteSeer returned a cache-miss error. These are my observed outcomes; the earlier packet separately reports raw 403/404 outcomes. No authentication barrier was bypassed, no complete BM11 PDF was inspected, and no BM11 PDF hash is supplied. [Published-page index](https://citeseerx.ist.psu.edu/document?doi=5c5cf00ea6a3ab873d9b64164fd117e9a7e204bb&repid=rep1&type=pdf); [publisher endpoint](https://academic.oup.com/jlms/article-pdf/83/3/563/2511415/jdq080.pdf); [preprint record](https://arxiv.org/abs/0905.1069).

The accepted 2018 Achille-Berarducci manuscript was inspected in its ambient setup, Sections 2–3, the triangulability definition in Section 8, Assumption 11.1, and Section 12 through the proof of Theorem 12.2. Its comparison requires a finite-polyhedron quotient and countable decreasing contractible open approximants. Proposition 3.4 derives continuity from the latter. Theorem 12.2 includes pointed comparison and positive-degree groups, also over open target subsets. Corollary 12.3 justifies the optional sphere computation through standard part. These statements do not establish that local contractibility alone implies the finite-polyhedron hypothesis. [Accepted postprint](https://arpi.unipi.it/retrieve/e0d6c92a-cebc-fcf8-e053-d805fe0aa794/selecta-2nd-revision.pdf); [DOI](https://doi.org/10.1007/s00029-018-0413-3).

## 6. Controls, integrity, and limitations

The complete authored proof, bridge note, source audit, metadata, README, turn ledger, verifier, and result file were read. The 20 original diagnostic checks were rerun and their complete JSON matched the frozen record. Five independent negative controls were rejected: wrong stereographic scale, reversed contraction parameter, wrong tetrahedron cycle coefficient, merged formal quotient classes, and an in-memory one-byte-content change to the proof. No negative control edited the original packet.

Four locally saved scholarly PDFs match the recorded byte counts, hashes, and page counts. Two complete local public-corpus files also match their recorded byte counts and hashes. Their exact target match and missing exact research-result keys were independently checked; only metadata is emitted. This is not an exhaustive historical repository search or proof that every semantic duplicate is absent.

The public audit contains authored analysis, citations, check code/results, and metadata only. It contains no source PDFs, source-page images, copied third-party passages, corpus contents, queue contents, or private coordination records. The calculations are diagnostics, not a formally checked proof of model theory or topology. Literature inspection is not a claim that no subsequent theorem exists.

## 7. Recommended disposition and remaining gap

Recommended label: **Literal formulation disproved; intended strengthened problem unresolved here.** Recommended turn count: **1/5**, reflecting one substantive mathematical approach. Algebra checks, source inspection, the three supporting scope lemmas, packaging, and independent review are not four additional attempts.

Suggested concise finding: “Two contractible definable classes on S² give a discrete logic quotient with π₂ = 0 while π₂^def is nonzero. The projection is discontinuous. This disproves the literal set-approximant wording only. Open approximants plus local contractibility remain unresolved in this packet; Achille-Berarducci covers the triangulable subclass.”

To resolve the strengthened target, one still needs either a verified theorem applying under exactly its weaker hypotheses or a valid new comparison argument. A proof of the necessary finite-polyhedron implication would be one sufficient route, but this audit does not assert that implication is true. Continuity with nonopen approximants is another distinct variant and has not been identified with the open-approximant version. No unconditional “solved,” “five attempts completed,” first-resolution, or priority claim is warranted.
