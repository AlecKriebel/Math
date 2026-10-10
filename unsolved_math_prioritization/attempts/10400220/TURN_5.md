# Substantive turn 5: an explicit candidate certificate and a finite-type obstruction

**Original mutation question remains unresolved after five substantive author turns.** This final turn tested an actual small mutant pair beyond the earlier four-knot false lead, constructed a checkable upper certificate, and examined whether mutation-sensitive finite-type information could supply the missing unrestricted lower bound. It does not claim new exact unknotting values or a mutation counterexample.

## 1. The actual candidate screen and its provenance limit

The complete public KnotInfo workbook was downloaded through its official Database Download page on 2026-10-01 and byte-pinned. A self-authored read-only parser joined its knot labels to all 91 through-12 and 774 thirteen-crossing groups in the pinned Stoimenow tables. Combined numbering was converted with the published alternating offsets 367,1288,4878 for crossing numbers11,12,13. Mirrors are not distinguished in that mutation table; ordinary unknotting number is unchanged by mirroring.

All865 groups and1841 member rows joined. No group's displayed intervals are disjoint. Exactly one group has unequal displayed intervals:

    11n76: 3
    11n78: [2,3].

This is a statement about the downloaded cells, not an independent theorem about their values or completeness of the mutant list. Both reference cells for unknotting number are blank. Kanenobu–Matsumura's primary OCAMI2014 preprint, Remark3.1, explicitly flags the 11n76 value among entries exceeding the elementary lower bounds without a reference. The bounded search in this turn did not supply the missing original lower-bound proof. That is not proof that the cell is wrong or that no later proof exists. In particular, the candidate cannot be reported as a known3-versus2 pair, and the other864 matching intervals cannot be reported as independently solved values.

The downloaded workbook identifies 11n78 by the four-strand braid word

    W=(-1,-1,2,2,2,-1,3,2,2,2,3),

where i denotes the Artin generator sigma_i and -i its inverse. Its stored signed DT code is (4,8,-14,2,-20,-16,-18,-6,-12,-22,-10), matching the n78 row of the published mutant pair. The braid-to-tabulated-knot identification is credited to the database, not recomputed by numerical recognition here. The theorem below is unconditional for the explicitly specified braid closure.

## 2. A fully checkable three-change upper certificate

**Proposition 5.1.** The closure of W can be unknotted by at most three ordinary crossing changes.

**Proof.** Change the third, fourth and eighth letters of W, using one-based indexing. The resulting four-strand braid is the first word below. The subsequent words have isotopic closures:

    B4: (-1,-1,-2,-2,2,-1,3,-2,2,2,3)
    B4: (-1,-1,-2,-1,3,-2,2,2,3)          cancel positions4–5
    B4: (-1,-1,-2,-1,3,2,3)               cancel the adjacent -2,2
    B4: (-1,-2,-1,-2,3,2,3)               inverse Artin relation
    B4: (-2,-1,-2,-2,3,2,3)               inverse Artin relation
    B4: (-2,-1,-2,3,2,-3,3)               mixed Artin relation
    B4: (-2,-1,-2,3,2)                    cancel -3,3
    B3: (-1,-1,2,1)                        left-end destabilization
    B2: (-1,-1,1)                          right-end destabilization
    B2: (-1)                               cancel -1,1
    B1: ()                                 destabilization.

The first two nontrivial equalities are sigma_i^-1 sigma_(i+1)^-1 sigma_i^-1 = sigma_(i+1)^-1 sigma_i^-1 sigma_(i+1)^-1. The mixed equality used is sigma_2^-1 sigma_3 sigma_2 = sigma_3 sigma_2 sigma_3^-1; it follows by multiplying the usual Artin relation on the appropriate sides.

An end destabilization is valid when the extreme generator occurs exactly once and all other letters lie in the remaining-strand subgroup. Cyclic conjugation moves that occurrence to the end before the usual Markov destabilization. The left-end version is the same operation at the other outside strand, followed by index relabeling. Each application above meets this condition. The one-strand empty braid closes to the unknot. Only the initial three sign switches are crossing changes; every subsequent step preserves the closure. ∎

The full machine-readable trace retains every state, strand count and move. A separate verifier checks it, including the Artin equalities through their exact free-group action. No external knot software or source executable was used. This supplies an upper bound already compatible with the tabulated interval, not a new exact unknotting number.

The exploratory search also exhausted its stated non-length-increasing move graph for all55 two-letter sign-switch subsets of W, visiting33,250 states in total and finding no reduction to the one-strand braid. This is **not** a proof of u>=3, nor even a complete unknot-recognition theorem for those diagrams. The move set omits length increases and most nonminimal presentations. It only describes the precise failed search. The earlier Bernhard–Jablan examples show why extending that negative result to an unrestricted lower bound would be invalid.

## 3. Why a bounded finite-type lower-bound route cannot finish the job

A natural attempt is to use finite-type invariants that can distinguish mutants, rather than unmarked-cover data that mutation preserves. The following limitation is decisive for any bound based only on bounded-order values.

Write J_n(K) for the complete equivalence class of values of Vassiliev invariants of degree at most n, using the coefficient convention of the realization theorem. Stoimenow, *Vassiliev invariants and rational knots of unknotting number one*, Theorem1.2 (author version18February2002, printed p.2; proof in Section4, pp.9–10), proves that for every K, every positive n and every positive integer m, there is a prime knot J with J_n(J)=J_n(K) and u(J)=m. It extends the earlier Ohyama–Taniyama–Yamada realization for m=1. The theorem and its exact quantifiers were checked in the full primary text, including the rendered theorem and final proof pages. It is credited prior work.

**Corollary 5.2.** If a real-valued function L of J_n is a valid lower bound L(J_n(K))<=u(K) for every knot, then L is at most1 on every realized class. No finite real-valued function of J_n can be an upper bound for u on every knot in that class.

**Proof.** For the lower bound, realize the same class by the theorem with m=1. For any proposed finite upper value U on a class, choose an integer m>U and use the same theorem. Both conclusions follow without any assumption that L or U is linear, continuous or itself finite type. ∎

Thus replacing an unmarked-cover obstruction by a nonlinear function of finitely many bounded-order finite-type numbers cannot provide a universal u>=3 certificate for the candidate. Merely distinguishing two mutants is not enough to compare their Gordian distances to the unknot.

The limitation is exact. The realization theorem does not preserve a given Conway-mutant class, crossing number, marked cover, Alexander polynomial, signature, or an independently constrained family. It does not rule out stronger joint information, infinitely many finite-type coefficients, full polynomial invariants, or mutation-sensitive geometric/Floer obstructions. No simultaneous preservation of those extra data is inferred here. The constructed comparison knot J is not claimed to be a mutant of K.

## 4. Final gap

No nonlocal two-change certificate for the candidate, certified unequal pair, or general transport theorem for unrestricted optimal crossing disks has been found. The marked-cover characterization of turn3 still requires the involution and quotient data. The displayed-cube theorem of turn4 does not remove that requirement, and the genuine EM localization defects occur even when mutant unknotting numbers agree.

The retained packet therefore consists of scoped theorems, exact certificates and explicitly bounded failed routes. The original Problem12.15 / alias2662(b) is **unsolved5/5**. The independent connected-sum question2662(a) has not been attempted or resolved by this work. No sixth author search or historical novelty claim is made; subsequent work is limited to independent review, corrections and authorized publication.
