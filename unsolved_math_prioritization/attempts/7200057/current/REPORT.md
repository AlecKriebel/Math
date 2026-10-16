# Crossing minimizers and halving-line maximizers

## Disposition

The general implication remains **unresolved in this report**. Five proof-search mechanisms were investigated. They yield an exact sufficient criterion, a proof of the implication for 3 through 7 points, mutation and deletion lemmas, and a realizable obstruction to determining the halving count from the crossing count, even with triangular convex hull. None proves or disproves the general conjecture. No novelty or best-known claim is made.

The original formulation is located in Aichholzer, García, Orden and Ramos, *New lower bounds for the number of (≤ k)-edges and the rectilinear crossing number of K_n*, §4 [S1]. Their arXiv version predates the 2007 publication. A 2024 preprint, subsequently published in 2025, expressly restates the every-minimizer conjecture and distinguishes candidate evidence against it from an actual refutation [S3, S4]. Bounded searches through 8 October 2026 found no verified complete resolution of this exact implication. This is a literature-search limit, not certification of worldwide openness or priority.

## 1. Exact target and conventions

Fix an integer n ≥ 3. Let P be a set of n distinct points of the real plane with no three collinear. Draw every edge of K_n as its straight segment. Define C(P) to be the number of unordered pairs of edges meeting in their relative interiors. Equivalently, C(P) counts convex four-point subsets. Concurrent crossings are counted as pairs, not as distinct geometric intersection locations. Thus no extra prohibition on concurrence is needed.

For each unordered pair {a,b}, let j be the smaller of the numbers of other points on the two open sides of its supporting line. Put m = floor((n−2)/2), and let e_j(P) count the pairs with this value j, for 0 ≤ j ≤ m. Let H(P) = e_m(P). For n even the two sides each contain (n−2)/2 points. For n odd their cardinalities are (n−3)/2 and (n−1)/2. The odd case is therefore the almost-halving convention, not an impossible equal split. These are the nonoriented definitions of [S1, §3], also used in [S2, §1].

Write c_n = min_P C(P) and h_n = max_P H(P). The target is

> For every n and every admissible P, C(P) = c_n implies H(P) = h_n.

This implies existence of a common optimizer, but is stronger: finding one common optimizer at each n does not control all crossing minimizers. The reverse implication is a different assertion. Labels, Euclidean congruence and affine equivalence do not affect either count; quotienting by these equivalences does not change this universal question. Only realizable planar order types belong to the target. An abstract allowable sequence that is not stretchable cannot be used as a geometric counterexample.

The relevant extrema exist without a compactness assumption: the nonempty set of attainable integer pairs (C,H) is finite, since 0 ≤ C ≤ binom(n,4) and 0 ≤ H ≤ binom(n,2).

## 2. Mechanism one: positive-weight edge profiles

Set N = binom(n,2), w_j = j(n−2−j), and E_k = sum_{j=0}^k e_j. A standard identity, appearing as Lemma 6 in [S1], is

C(P) + sum_{j=0}^m w_j e_j(P) = 3 binom(n,4).                       (1)

Here is an independent counting derivation. The sum counts a supporting pair together with an unordered pair of other points on opposite sides. A convex four-point set contributes two such supporting pairs, its diagonals. A nonconvex four-point set contributes three, the segments joining its interior point to the hull vertices. Thus the sum is 2C + 3(binom(n,4)−C), giving (1). This argument also specifies the crossing multiplicities unambiguously.

Summation by parts yields

C(P) = A_n + sum_{k=0}^{m−1} a_k E_k(P),
A_n = 3 binom(n,4) − w_m N,
a_k = w_{k+1}−w_k = n−3−2k > 0.                                  (2)

Also H(P) = N − E_{m−1}(P) when m ≥ 1. Crossing minimization is therefore minimization of a positive weighted sum of cumulative edge counts; halving maximization is minimization of its last coordinate. Positivity alone does not make the minimizers coincide.

### A sufficient tightness criterion

In this paragraph assume n >= 4, so m >= 1. (The n=3 case is immediate and is handled in Section 3.) Suppose L_k are valid lower bounds E_k(P) ≥ L_k for all admissible P, and there is a configuration attaining

c_n = A_n + sum a_k L_k.                                           (3)

Then every crossing minimizer has E_k = L_k for every k. Indeed, (2) minus (3) is a sum of nonnegative terms a_k(E_k−L_k), so equality forces each term to vanish. In particular every crossing minimizer has H = N−L_{m−1}; because that value is attained and is a universal upper bound, it equals h_n. This proves the target whenever a simultaneously sharp lower-bound certificate (3) is available. No enumeration of minimizers is needed.

A quantitative version is useful when the crossing optimum exceeds this bound. If C(P) is at most U, E_k ≥ L_k, and L_{m−1} is an integer, then

E_{m−1}(P) − L_{m−1} ≤ floor((U−A_n−sum a_k L_k)/a_{m−1}).          (4)

The final coefficient is 1 for even n and 2 for odd n. Formula (4) bounds a slack relative to the chosen upper bound N−L_{m−1}; it does not identify h_n unless that bound is attained.

For arbitrary real lower bounds, the valid rounded form is

E_{m−1}(P) − L_{m−1} ≤ floor(L_{m−1} + (U−A_n−sum a_k L_k)/a_{m−1}) − L_{m−1}.  (4R)

Only E_{m−1} is necessarily integral; its slack relative to a real L_{m−1} need not be. For example, at n=4 an interior-point configuration has C=0 and E_0=3. The valid universal bound L_0=5/2 and U=0 would make the unqualified version of (4) falsely read 1/2≤0. The integer qualification and (4R) explicitly correct that rounding defect; the tightness theorem and all later mechanisms do not use the defective rounding.

**Gap.** We did not establish simultaneous sharpness for arbitrary n. Individually optimal edge bounds need not have a common realizer. Replacing the feasible geometric profile set by arbitrary integer vectors can introduce spurious configurations. Literature determining the two extremal numbers separately [S2] must not be silently promoted to classification of every optimizer.

## 3. Mechanism two: triangular-hull reduction and a complete small-order consequence

We use two established structural results, with their distinct quantifiers: every crossing-minimizing configuration has triangular convex hull [S1, Theorem 4], while at least one halving-maximizing configuration has triangular convex hull [S1, Theorem 7]. The latter does not say every halving maximizer is triangular.

For 3 ≤ n ≤ 7 the target follows from these results and (1), without needing exact numerical extremal values.

For n=3 all three pairs are halving and every crossing count is zero. For n=4, (1) gives C+H=3. For n=5 it gives C+2H=15. In these two cases the implication holds for every configuration directly.

For n=6 or 7, restrict to a triangular-hull configuration, so e_0=3. Since sum e_j = N, equation (1) gives respectively

n=6: C = 9−H;
n=7: C = 33−2H.                                                  (5)

For example, at n=6 the identity is C+3e_1+4e_2=45 and e_1+e_2=12, hence C=9−e_2. At n=7 it is C+4e_1+6e_2=105 and e_1+e_2=18, hence C=33−2e_2.

Let P be any crossing minimizer and Q a triangular-hull halving maximizer. Both are triangular by the stated structural facts. Comparing their values in (5), C(P) ≤ C(Q) implies H(P) ≥ H(Q)=h_n. The reverse inequality is definitional, so H(P)=h_n. This proves the universal implication for all 3 ≤ n ≤ 7. It is an elementary consequence of known structural results, not a new-resolution claim.

**Gap at n=8.** For triangular hull, the two relevant equations instead give

C = −15 + 4e_1 + e_2,
H = 25 − e_1 − e_2 = 10 − C + 3e_1.                              (6)

The extra e_1 parameter remains. Triangularity alone no longer makes H a function of C. Section 6 realizes this obstruction with integer coordinates.

## 4. Mechanism three: mutation descent and the missing global step

Consider a generic single-triple mutation: one point p crosses the relative interior of the segment joining q and r, and no other triple changes orientation. Before crossing, k of the other n−3 points are on p's side of qr. Exactly those n−3 four-point subsets containing p,q,r change convexity. The k points on p's side create convex quadrilaterals after the move; the other n−3−k destroy them. Hence

ΔC = 2k−n+3.                                                     (7)

This is the mutation formula of [S1, Lemma 1]. For k < (n−3)/2, the edge profile changes by e_k → e_k−1 and e_{k+1} → e_{k+1}+1. Only pq, pr and qr can change side counts, and before the move two are k-edges and one is a (k+1)-edge; afterward these multiplicities exchange. At the balanced odd-n value k=(n−3)/2, all three are halving edges before and after, so the entire profile is unchanged. The opposite mutations reverse these changes.

Consequently every crossing-decreasing mutation weakly increases H. More precisely:

- For even n, H increases by 1 exactly on a crossing decrease of 1; on larger single-mutation decreases it is unchanged.
- For odd n, H increases by 1 exactly on a crossing decrease of 2; on larger single-mutation decreases it is unchanged.
- A crossing-preserving generic mutation exists only for odd n and preserves H.

These assertions concern generic single-triple events; a simultaneous degeneracy must first be resolved into such events rather than assigned an unjustified formula.

Starting with an H-maximizer and repeatedly taking any available crossing-decreasing mutation preserves H=h_n and terminates after finitely many steps because C is a nonnegative integer. The endpoint is locally crossing-minimal with respect to available single mutations and is still H-maximal. This proves existence of a **local** common optimizer, not a global one.

A sufficient global condition is also immediate: if a fixed crossing minimizer P can be reached from every admissible Q by a path of realizable generic mutations along which C never increases, then H(P) ≥ H(Q) for every Q, proving H(P)=h_n. To prove the universal target by this route, such accessibility must hold for every crossing minimizer, or an additional argument must equate H across all global minimizers.

**Gap.** Neither descent to a global minimum from every start nor equality of H across different minimum-level components was established. Connectedness of the full configuration space does not supply a crossing-monotone path. For even n, there are no crossing-preserving generic mutations at all; merely proposing to connect all optimizers by zero-cost flips already fails as a general justification. We do not assert existence of a non-global local minimum without a separate certificate.

## 5. Mechanism four: vertex-deletion induction

Deleting a vertex preserves general position. Every crossing involves four vertices, so for n ≥ 5,

sum_{v in P} C(P\{v}) = (n−4) C(P).                              (8)

The corresponding halving identities depend on parity.

For odd n=2r+1 ≥ 5,

sum_v H(P\{v}) = r H(P).                                         (9)

An original halving pair splits the other points as r−1,r. It remains halving after deleting any of the r points on the larger side, and after no other deletion. No nonhalving pair can become halving by deleting one point. This proves (9), including the fact that deletions of the pair's own endpoints contribute nothing.

For even n=2r ≥ 4,

sum_v H(P\{v}) = (n−2)H(P) + r e_{r−2}(P).                       (10)

Every original halving pair survives as an almost-halving pair in every deletion of another vertex. A pair of type r−2 becomes almost-halving upon deletion of any of the r points on its larger side. All other pairs contribute zero. Formula (10) explains why parity-blind induction loses a crucial adjacent edge statistic.

### Conditional odd-order propagation theorem

Assume the target holds at n−1, n≥5 is odd, and the crossing deletion bound is exact:

(n−4)c_n = n c_{n−1}.                                            (11)

Then the target holds at n.

Proof: for any crossing minimizer P, every C(P\{v}) is at least c_{n−1}. Their sum, by (8) and (11), is exactly n c_{n−1}. Thus every deletion is a crossing minimizer. By the induction hypothesis every deletion has h_{n−1} halving pairs. Equation (9) yields H(P)=n h_{n−1}/r. Applying (9) to an arbitrary n-point set Q gives H(Q)≤n h_{n−1}/r. Therefore P reaches the global halving maximum. The resulting quotient must automatically be integral if the hypotheses hold.

A defect estimate makes the obstruction explicit. Put D=(n−4)c_n−n c_{n−1}≥0. For a crossing minimizer, the sum of the nonnegative integer crossing defects of its deletions is D, so at most D deletions can be nonoptimal. If the target holds at n−1, at least max(0,n−D) deletions have h_{n−1} halving pairs. Hence (for odd n)

r H(P) ≥ max(0,n−D) h_{n−1}.                                    (12)

This is usually much weaker than global optimality.

**Gap.** Equality (11) was not proved in the required generality and cannot be presumed from the averaging lower bound. At even orders the additional term in (10) prevents the same scalar conclusion. This mechanism supplies a conditional theorem, not an unrestricted induction.

## 6. Mechanism five: realizable equal-crossing profile exchange

Equation (6) suggests the profile exchange

Δ(e_0,e_1,e_2,e_3) = (0,1,−4,3),                                 (13)

which preserves C at n=8 while increasing H by 3. Rather than treating a formal integer profile as geometric, the following two configurations realize it. All share the outer vertices (0,0), (1000,0), (0,1000).

Add these five points for P:

(578,36), (72,693), (201,510), (52,473), (56,41).

Add these five points for Q:

(171,780), (189,153), (17,28), (421,229), (171,510).

Every added point lies strictly in the outer triangle. Exact determinant signs for all triples are nonzero. Their profiles and counts are

P: (3,6,13,6), C(P)=22, H(P)=6;
Q: (3,7,9,9), C(Q)=22, H(Q)=9.

Thus equality of crossing count and equality of hull size do not imply equality of halving count, even for realizable point sets. The coordinates are authored witnesses produced in this investigation, not copied dataset contents. The accompanying checker verifies each count by independent direct segment-pair and convex-four-subset methods, and verifies the full side-count profiles.

These sets are **not a counterexample to the target**. With the same three outer vertices, instead add

(81,398), (957,30), (78,650), (288,498), (77,202).

The resulting R has profile (3,6,10,9), C(R)=19 and H(R)=9. Therefore c_8≤19<22, proving that neither P nor Q is crossing-minimizing, without requiring any external table of c_8. In particular P fails the global-minimum premise, despite H(P)<H(Q).

This construction defeats the proposed extension of the affine small-order argument; it does not defeat the conjecture. The fact that a literature maximum h_8=9 is known is not needed for this obstruction, and no global-optimality claim for R is made here.

**Gap.** A target counterexample would require an admissible S with a rigorous certificate C(S)=c_n and an admissible T with H(T)>H(S). A proof of the exact value h_n would be stronger than necessary, but our conservative acceptance requirement would also seek an independently certified halving maximum before reporting a definitive finite counterexample. Here no candidate meeting even the logically sufficient first two conditions was obtained. Neither random search nor local optimization is a certificate of global crossing minimality.

## 7. Status, bounds on the investigation, and reproducibility

The complete target remains unresolved after these five mechanisms. Literature reading, source normalization, exact regression tests and packaging are not additional proof-search mechanisms. The source packet contains public bibliographic and verification metadata only. Public-source PDFs, extracted text, private input records and search/coordination material are excluded.

The code uses only integer/rational determinants and exact combinatorics. It validates the three witnesses, all their deletions, the edge-profile identities, both parity-specific deletion formulas, generic mutation fixtures of both parities, and the stated small-order algebra. Bounded auxiliary fixtures exercise the formulas; they do not enumerate all order types or prove new global extrema. All guards are explicit exceptions rather than Python assert statements, so optimization flags cannot erase them.

The strongest unconditional conclusion here about the target itself is the reconstructed implication for 3≤n≤7. The sufficient tightness and deletion theorems identify explicit missing hypotheses for larger n. The same-crossing witnesses and mutation analysis explain two invalid shortcuts. No general resolution, verified refutation, publication acceptance of this report, or mathematical novelty is claimed.

## References

[S1] O. Aichholzer, J. García, D. Orden and P. Ramos. *New lower bounds for the number of (≤ k)-edges and the rectilinear crossing number of K_n*. Discrete & Computational Geometry 38 (2007), 1–14. https://doi.org/10.1007/s00454-007-1325-8 . Inspected preprint: https://arxiv.org/abs/math/0608610v2 . Definitions and Lemma 5: printed p.6; Lemma 6 and Theorem 7: p.7; original question: §4, p.12. The author-hosted January 2007 revision was additionally inspected through web extraction: https://pedroramos.web.uah.es/papers/lb-k-edges.pdf . Numbering/page locations refer to the pinned arXiv PDF unless specified.

[S2] B. M. Ábrego, M. Cetina, S. Fernández-Merchant, J. Leaños and G. Salazar. *On ≤k-edges, crossings, and halving lines of geometric drawings of K_n*. Discrete & Computational Geometry 48 (2012), 192–215. Inspected arXiv v2, 16 March 2011: https://arxiv.org/abs/1102.5065v2 . Definitions: §1; exact small-order extremal values: §4. Its extremal bounds are credited, not claimed as results of this investigation.

[S3] J. Rodrigo, M. López, D. Magistrali and E. Alonso. *An Improvement of the Lower Bound on the Maximum Number of Halving Lines for Sets in the Plane with an Odd Number of Points*. Axioms 14 (2025), 62. https://doi.org/10.3390/axioms14010062 . Published 16 January 2025. Indexed primary text was inspected, including Conjecture 1 and the explicit non-refutation statement. Direct journal-PDF retrieval failed, so full journal-version inspection is not claimed.

[S4] Same authors and title as [S3]. Preprints.org v1, posted 26 November 2024, explicitly marked not peer reviewed. https://doi.org/10.20944/preprints202411.1953.v1 . Complete downloadable preprint was inspected; the conjecture is on printed p.1 and the non-refutation statement on p.2. Its status must not be confused with the subsequent journal article.

[S5] J. Rodrigo and M. D. López. *An improvement of the lower bound on the maximum number of halving lines in planar sets with 32 points*. Author-deposited paper: https://oa.upm.es/57576/7/INVE_MEM_2018_307610.pdf . Introduction and concluding discussion distinguish a halving lower-bound improvement from a conditional improvement of a crossing upper bound. This is not a certified counterexample.
