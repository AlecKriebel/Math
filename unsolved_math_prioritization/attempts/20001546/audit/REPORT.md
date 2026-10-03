# Independent adversarial audit: rank 456 / problem 20001546

Audit date: 2026-10-03 UTC. Frozen nine-file package audited without modification.

## Verdict

**PASS as a five-attempt, explicitly unresolved partial-results package.** No substantive error was found in its asserted model-specific results or the proper-hull reduction. **HOLD any claim that AIM Problem 4.2 has been solved, that all geometric Helly actions are excluded, or that a torsion-free direct-factor theorem has been disproved.** Those claims are not in the frozen package and would not follow from it.

No mandatory mathematical correction is needed. Three small documentation improvements are recommended below. No sixth attempt, remote write, or new all-scale obstruction was undertaken.

## Integrity and independent controls

All nine filenames, byte counts, and SHA-256 hashes match FROZEN_MANIFEST.json. Running the frozen verifier with ordinary Python 3 succeeds and produces JSON structurally identical to checks_turn2.json.

The independent_controls.py supplied beside this report imports no code from the frozen verifier. It uses a different free-reduction implementation, enumerates every signed generator word through each tested radius, constructs translated balls directly, and includes both positive and negative controls. Its output is independent_controls.json.

- Radius 1: 19 enumerated words, 19 distinct images.
- Radius 2: 343 enumerated words, 211 distinct images.
- Radius 3: 6,175 enumerated words, 2,089 distinct images.
- In each case all three pairwise image intersections have cardinality one and the triple image intersection is empty.
- All generator/inverse tests, the three Artin braid relations, the nine dual products, the advertised pairwise witnesses, and the distinctness of the a^n and p^n images pass.
- Negative controls verify that each adjacent pair of standard generators does not commute in the representation. Positive controls verify that repeated-center balls do intersect.

These are image counts, not claims about the exact cardinalities of larger balls in A. Nothing uses faithfulness of A -> Aut(F4).

## 1. Exact target and source gate

I independently retrieved the specified [archived AIM page](https://web.archive.org/web/20240828224700/http://aimpl.org/geomartingp/4/) through ordinary public HTTP after web extraction failed. Both its visible HTML and embedded record identify 4.2 as the question whether the affine A2 Artin group admits a proper cocompact Helly-graph action. The embedded status is empty. The RAAG/2-dimensional/(2,4,4) remark belongs to the separate systolicity problem 4.25.

The [AIM workshop report](https://aimath.org/pastworkshops/geomartingprep.pdf), printed page 2, distinguishes A from A x Z and discusses a possible negative strategy rather than a proof. The currently retrieved [Haettel lecture notes](https://imag.umontpellier.fr/~haettel/Lecture_Notes_Helly.pdf), Section 13, question 3, printed page 55, still ask the same question. The frozen page citation is correct: physical PDF page 55 also bears printed number 55.

This supports the stated bounded literature status. It does not prove worldwide openness or novelty. I did not independently authenticate every historical queue/blob search in SOURCE_GATE.md; those provenance claims remain the originating investigators' bounded search record, rather than new independent findings of this audit. The release omits nonpublic history-search bookkeeping; no mathematical findings or audit limitations have been removed.

## 2. Attempts 1–2: natural Cayley graph and its first three powers

The generating set is consistent with the cyclic orientation a,b,c. In the rank-two dual interval, ab=bd=da and d=b^-1ab=aba^-1; the other two intervals follow cyclically. Their union, excluding the identity, has the stated nine positive elements.

[Haettel–Huang, New Garside structures](https://arxiv.org/html/2305.11622v2), Section 5.2 and the proof of Corollary 4.5, identifies the Bestvina complex of the constructed A x Z Garside structure with the flag Cayley complex for this lifted union. Thus the tested Q is the intended specific proper cocompact model, not a different convenient graph. Theorem D and Corollary G concern the product's Helly property and the factor's weaker geometric conclusions.

The finite exclusion logic is valid. If x were in the three radius-n balls of Q, its homomorphic image would be in the three computed image balls. Their empty total intersection therefore excludes x even when distinct elements of A have the same image. At n=1 the 19 candidate images are distinct, so the two asserted singleton intersections in A itself follow. At n=2,3 the report correctly makes the weaker image-intersection claim needed for non-Hellyness.

The positive witnesses are group identities, not inverse inferences from equal images. In particular p^2=a^2ba. The all-scale connecting word follows from a^-1p=b, a^-2p^2=ba, a^-3p^3=bad and centrality of z=p^3: write m=3k+r and commute z with a. This gives (bad)^k followed by the length-r prefix. Splitting the resulting length-2n word at n proves pairwise intersection at every n.

Radius-one balls of Q^n are exactly radius-n balls of Q, proving non-Hellyness for n=1,2,3. The package does not infer arbitrary-power failure or unbounded enlargement from these calculations. That restriction is essential and correctly stated. No unbounded coarse-Helly defect is proved.

## 3. Attempt 3: complete real-tree fibers

The retraction A -> B3 given by c -> a respects all three relations and proves the required embedding of P=<a,b>. Exponent sum proves z=(ab)^3 has infinite order. Direct matrix multiplication independently gives ABA=BAB and [A,B]=((1,1),(1,2)); trace 3 proves that h=[a,b] has infinite order.

The real-tree argument is sound. An isometry of a real tree is elliptic or axial. If z is elliptic, its infinite cyclic subgroup fixes a point. If z is axial, centrality forces P to preserve its unique axis; commuting with a nontrivial translation excludes reflections on that axis. The restriction is therefore abelian, and the infinite-order commutator fixes the axis pointwise. In either case the action has an infinite point stabilizer and is not proper.

For an equivariant projection, P preserves the fiber over the coset P. Applying the preceding argument there proves the asserted global nonproperness. This requires the stated nonempty tree fiber and isometric stabilizer action. It does not require a product metric or a global character. The line-cocycle specialization also checks: the braid relation forces equal orientation signs and then equal translation/reflection parameters.

[Haettel's published extended-Deligne construction](https://imag.umontpellier.fr/~haettel/Helly_Kpi1.pdf), Theorem 4.4 and Corollary 4.5, verifies the Helly/injective source geometry; its quotient construction on printed page 4040 retains parabolic stabilizers. No inference from these stabilizers to the impossibility of unrelated actions is justified or made.

## 4. Attempt 4: direct-factor permanence

The king graph on Z^3 is Helly because its balls are products of integer intervals. The proof includes infinite families legitimately: fix one bounded ball and use finiteness. The displayed W x Z action is by graph automorphisms. Its translation subgroup has index 3, and the permutation group is finite, proving cocompactness and properness. The action is faithful as well: a trivial affine map forces the permutation to be identity and ell=-n(1,1,1), hence n=0 by summing coordinates.

W has rank-two translation lattice and faithful point group S3 on the sum-zero plane. Its order-three rotation cannot occur in the order-eight signed-permutation isometry group of the two-dimensional supremum norm. [Hoda, Theorem 7.1 and Corollary 7.2](https://arxiv.org/html/2010.07407v2) therefore apply exactly and exclude W from being Helly.

This is a valid counterexample to unrestricted inheritance by direct factors, central quotients, and algebraic retracts. W has torsion, so it does not settle any torsion-free analogue. The sufficient 1-Lipschitz-retraction criterion is correct: inclusion and retraction prove isometry, and retracting a common point preserves all radius bounds. Cocompactness of the restricted A action remains a separate necessary input.

## 5. Attempt 5: weak modularity, properness and cocompactness

The precise additional source for weak modularity is [Haettel–Huang, Lattices, Garside structures and weakly modular graphs, Theorem 5.7](https://arxiv.org/html/2211.03257v2): the weak Cayley graph and its Garside-automorphism quotient are weakly modular. Combined with the preceding Bestvina/Cayley identification, this applies to the specific Q.

I retrieved the [published Helly groups PDF](https://msp.org/gt/2025/29-1/gt-v29-n1-p01-p.pdf). Lemma 6.5 states the needed 1-stable-interval implication, and Theorem 6.4 states the proper-hull theorem with exactly local finiteness and stable intervals. [Lang, Theorem 1.1](https://arxiv.org/abs/1107.5971) requires a discretely geodesic space with finite bounded sets; finite-degree Q satisfies both. No coarse-Helly hypothesis is needed for this properness theorem.

The integer hull is an isometrically embedded, 1-separated subset of E(Q). Properness of E(Q) therefore makes every bounded vertex set of H(Q) finite. The supplied action-properness proof works without a bounded-hull assumption: d(o,go)<=2d(o,y)+d(y,gy), and a compact set can be bounded around y. It thus avoids misusing Proposition 6.7, whose stated assumptions also include bounded distance.

The cocompactness equivalence is valid for this canonical action. Its base orbit is exactly Q. Finite orbit representatives give a uniform distance to Q; conversely a uniform distance bound puts representatives in one finite H(Q)-ball. Local finiteness then also supplies finitely many edge orbits. The bounded-hull/coarse-Helly equivalence is provided by Proposition 3.12 of Helly groups and, directly for integer hulls, [Haettel, Proposition 9.14](https://imag.umontpellier.fr/~haettel/Lecture_Notes_Helly.pdf). The finite-family formulation extends to all families using one finite enlarged Q-ball.

Accordingly, the remaining gap for this particular action is exactly coarse Hellyness of Q. Showing that Q is not coarsely Helly would exclude this completion only. The general existence question remains unresolved.

## Recommended documentation improvements, not correctness blockers

1. Add the explicit weak-modularity citation and identification chain in Attempt 5: Haettel–Huang 2024, Theorem 5.7, followed by the Bestvina-complex identification in New Garside structures, proof of Corollary 4.5. The current citation is directionally correct but unnecessarily indirect.
2. In the motivational stable-norm paragraph of Attempt 2, make normalization explicit: for a^u z^k set v=3k, so the claimed intrinsic norm reads max(|u|,|3k|,|u+3k|). Cite the standard dual-Garside infimum/supremum word-length formula or delete this nonessential motivational statement. It is not an established statement about distances or possible centers in Q, as the package already emphasizes.
3. Optionally add explicit image-distinctness and empty-triple-intersection assertions to the frozen verifier's next permitted revision. They already follow from its unique image representatives and two asserted different singleton representative lists, but explicit assertions would make the certificate easier to audit. Do not assert exact ball sizes or unique actual centers in A at n=2,3 without additional justification.

The audit artifacts are separate from the frozen public package. Source PDFs/HTML remain outside the public package. Final accepted status is UNSOLVED, 5/5, with the scoped partial conclusions above.
