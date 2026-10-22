# Weak-order growth of Grothendieck Schubert support: bounded research report

Date: 2026-10-21. Target: row 1873, ID 30006522 / OWR-14299904-004.

## Outcome

**Not solved in general.** No counterexample was found. Exact exhaustive verification covers every permutation in S8 (and therefore every smaller symmetric group by stability). A rigorous skew-sum reduction and several explicit obstructions to stronger proof strategies were obtained. None is claimed to be a previously unknown published theorem. No publication or queue edit was performed.

The target is: if G_w = sum a_u S_u, a_u != 0, and length(u) < deg(G_w), then some length-increasing **left** simple reflection s_k u also has nonzero coefficient. This is not monomial-support augmentation or right-weak growth.

## Literature boundary

The primary source is Chiang–Weigandt's contribution to Oberwolfach Reports 23 (2026), printed pp.132–133, https://doi.org/10.4171/OWR/2026/2 . Its Conjecture 2 is the target. The report announces all three conjectures for Grassmannian and shifted-dominant permutations, and the first two for inverse fireworks permutations. These are prior results, not accomplishments of this investigation. Rows 30006520/21 duplicate the weaker existence-of-a-larger-support-element assertion; 30006523 is interval convexity, a separate assertion. The two monomial-support articles and September 2026 preprint in SOURCE_STATUS_GATE.md do not resolve this basis-dependent target.

We additionally inspected the full HTML of Weigandt, *Changing Bases with Pipe Dream Combinatorics*, https://arxiv.org/html/2506.07306v1 , especially Theorem 6.7(3). It represents the sign-corrected Schubert expansion by reduced admissible paths in a directed graph R_n from w to the longest permutation w0, with index w0 times the permutation of the reversed edge-label word. This supplies an exact combinatorial reduction below, not a proof of augmentation.

## Approach 1: exact recurrence and basis elimination

For the longest permutation, S_w0 = G_w0 = x1^(n-1)x2^(n-2)…x_(n-1). For a right ascent of w, compute S_w=∂i S_(w s_i) and G_w=∂i((1−x_(i+1))G_(w s_i)). All polynomial arithmetic uses Python integers and sparse monomial dictionaries.

The lexicographically smallest monomial of S_u has exponent equal to the Lehmer code of u and coefficient one. Repeated subtraction of this term's Schubert polynomial exactly determines the expansion. The staircase exponent bounds α_i≤n−i give an n!-dimensional polynomial module; its n! Schubert polynomials are unitriangular. Thus the computation does not silently discard indices outside S_n.

Results:

- S5: 120 inputs; 325 support incidences; 204 non-top incidences; zero failures.
- S7: 5,040 inputs; 62,048 support incidences; 56,715 non-top incidences; zero failures.
- S8: 40,320 inputs; 1,315,946 support incidences; 1,271,255 non-top incidences; zero failures. Maximum support size: 1,246.

Every supported coefficient also satisfied the expected alternating sign in each run. The S8 run took about 80 seconds. The program checks every left simple-reflection ascent, not just one heuristic choice. Finite evidence is not proof for arbitrary n.

Independent verification: a second implementation enumerated staircase pipe-dream subsets and their Demazure products, checking all S5 and S6 Schubert and Grothendieck polynomials, leading monomials, and exact reconstructions against the recurrence implementation. See audit_pipe_dreams.py, independent_pipe_audit_n5.json, and independent_pipe_audit_n6.json. The S6 check enumerates all 32,768 staircase subsets. The S8 computation itself uses the recurrence implementation, not a second exhaustive S8 implementation.

## Approach 2: transfer from monomial augmentation

This strategy fails without additional structure specific to Grothendieck polynomials. Consider P=S_213−S_231=x1−x1 x2. Its monomial support is the two comparable exponent vectors (1,0),(1,1), so it has one-step monomial augmentation, interval convexity, and saturated Newton polytope. Its Schubert expansion has alternating signs by degree. Nevertheless, its lower Schubert index 213 has no left ascent in its support: s1 sends it downward to 123 and s2 sends it to 312, not 231.

This is a rigorous counterexample to a generic implication from those properties, **not** to the Grothendieck conjecture. It explains why the recent monomial results cannot be substituted for the requested theorem.

## Approach 3: coefficientwise injection of combinatorial objects

A tempting proof would inject the objects counted by |a_u| into objects at one or more supported upward neighbors. That strengthening fails even for actual Grothendieck polynomials. The exact expansion is

G_12543 = S_12543 − 2 S_13542 − S_14523 + S_14532 + 3 S_23541 + S_24513 − 2 S_24531 − S_34512 + S_34521.

At u=23541, the coefficient magnitude is three. Its only supported left ascent is 24531, of coefficient magnitude two; that index in turn has only the supported ascent 34521, of magnitude one. Thus even an injection into the disjoint union of all immediate upper-neighbor fibers is impossible. A successful path/pipe-dream proof must allow many-to-one choices or prove existence without such an injection. This identity was independently verified by pipe-dream enumeration.

## Approach 4: induction through isobaric divided differences

The exact operator identity is π_i f=f+(1−x_i)∂i f. On a Schubert polynomial, ∂i S_u is either zero (right ascent) or S_(u s_i) (right descent). This does not give a support-preserving recurrence: the x_i multiplication introduces further Schubert terms and cancellation. Already π_1 S_21=1, because S_21=x1 and x1+1−x1=1. Thus a termwise support witness in the parent polynomial need not survive in the child.

This computation pinpoints why merely carrying an induction hypothesis for existence of supported left ascents is insufficient. No cancellation-controlled induction invariant was established. This is an obstruction to this direct strategy, not an impossibility theorem for all divided-difference arguments.

## Approach 5: poset convexity and rootedness

For any finite graded poset, interval convexity together with the property that every non-top element lies below a strictly larger supported element implies the one-step property: take a saturated chain to that larger element and use its first edge. This precisely explains the relationship between the weaker rows 30006520/21, the separate convexity row 30006523, and the target. It is not permissible to assume either unresolved assertion.

A direct exact check found no interval-convexity failures for any support in S7. The test checks every missing upward neighbor v of a supported u and whether any supported t lies above v. Any violation of convexity has such a first missing neighbor, so this is exhaustive for S7.

However, the stronger picture of support as a single weak-order upper region rooted at w is false: S_14523 occurs in G_12543, while 12543 is not below 14523 in left weak order. Specifically, the position inversion (4,5) is present in 12543 and absent in 14523. Thus a proof cannot simply connect every support element to the bottom index w by left-weak ascents. See check_posets.py and poset_n7.json.

## Approach 6: admissible path shortening

Let B_w be the set of permutations q represented by the reduced admissible paths in Theorem 6.7(3). Then A_w={w0 q:q∈B_w}. If N=length(w0), length(w0 q)=N−length(q). Hence the requested theorem is exactly the following statement about B_w:

Whenever q∈B_w has length greater than the minimum length occurring in B_w, some left simple descent s_j q also belongs to B_w.

Indeed, s_k(w0q)=w0 s_(n−k)q. A one-step increase in the support index is a one-step decrease in the path-word permutation. This is an exact reformulation, with length inequalities reversed, not an additional assumption.

Reduced-word deletion alone is inadequate: deleting a letter does not establish that the remaining word is realized by another admissible path with the same starting permutation w and ending permutation w0. The missing ingredient is an admissibility-preserving path rerouting/shortening lemma. We did not establish it. Coefficient-injection failure above also cautions that an injective shortening of all path fibers is too strong.

## Approach 7: rigorous skew-sum factorization reduction

For v∈S_m and z∈S_n, let v⊖z be the permutation consisting of v with n added to every value, followed by z. There are mn cross-block inversions. Both polynomial families satisfy

F_(v⊖z)=(x1⋯xm)^n F_v(x1,…,xm) F_z(x_(m+1),…,x_(m+n)),

where F is S or G. To prove this, start with the longest permutation in S_(m+n), which is the skew sum of the two block-longest permutations. Its staircase monomial has exactly the displayed factorization. Reach v⊖z by block-internal right-descent divided differences (ordinary or isobaric). The rectangular monomial is symmetric in the first block and independent of the second, so it factors out at every step. The operators act on the appropriate factor alone.

Expanding both factors gives a bijection

A_(v⊖z)={a⊖b:a∈A_v, b∈A_z},

with coefficients multiplying, and degree mn+deg(G_v)+deg(G_z). Uniqueness follows from the Schubert factorization and injectivity of (a,b)↦a⊖b. Internal left simple reflections act in one factor; the boundary reflection s_n is always a descent because n+1 occurs in the first block and n in the second.

Consequently, the target conjecture holds for v⊖z if and only if it holds for both factors. Forward: for a deficient support index in one factor, pair it with a top-degree index in the other factor; an ascent in the skew-sum support cannot occur in the top factor or across the boundary. Reverse: any deficient product index is deficient in at least one factor; apply that factor's property.

**Corollary:** every size-minimal counterexample is skew-indecomposable. The known structured-family cases extend to all iterated skew sums of those cases. This is a rigorous structural reduction, not a solution to the general conjecture, and literature novelty is unassessed. The independent checker verified both polynomial factorizations on 465 skew-sum instances of total size at most 6 (930 polynomial comparisons, zero failures). See audit_weak_growth_reductions.md and independent_skew_sum_audit.json.

## Acceptance boundary

The research outcome is bounded progress: exact small-rank evidence, independently verified algebraic examples, a structural reduction, and documented failure points for multiple proof strategies. No general theorem, disproof, or literature-resolution claim is warranted. Further work should focus on skew-indecomposable permutations and existence-preserving (not coefficient-injective) admissible-path shortening.

## Independent adversarial review verdict

PASS as bounded research, not as a general solution. The reviewer checked the displayed expansion, sign conventions, left/right orientation, finite-basis completeness, convexity test, path reversal, and skew-sum equivalence proof. The independent polynomial implementation covers S6, not S8. In the skew-sum argument all reflection indices are within S_(m+n); external S∞ ascents cannot appear in its finite support. Independent details and reproducible checks are in audit_weak_growth_reductions.md.
