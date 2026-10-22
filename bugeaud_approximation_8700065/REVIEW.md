# Independent theorem-mapping review: row 1821 / ID 8700065

Date: 2026-10-20 UTC.

## Verdict and scope

**PASS: the original fixed-degree question has an affirmative published resolution.** Beresnevich's 2015 Theorem 3 supplies a full-dimensional set of polynomial-badly-approximable real numbers. Appendix B supplies the infinitely-often algebraic upper bound; an elementary complex-segment estimate supplies the lower bound even when the original question permits nonreal approximants. Real algebraic numbers of degree exactly n+1 belong to the target set, and removing the countable set of all algebraic numbers from the full-dimensional subset leaves full Hausdorff dimension. Thus containment is genuinely strict, not merely nonemptiness.

This review imports the published dimension theorem. It does not claim a new solution or a referee-level reproof of its deep manifold theorem. The elementary bridges below were independently checked and, where useful, rederived with noncritical constants.

## Evidence inspected

1. Waldschmidt, *Open Diophantine Problems*, arXiv:math/0312440v2, dated January 24, 2004: Question 5.2 on PDF page 46 and the height definitions in Section 4. The PDF was text-extracted and the relevant passages inspected. [Original version](https://arxiv.org/abs/math/0312440v2).
2. Beresnevich, *Badly approximable points on manifolds*, arXiv:1304.0571v3, dated March 30, 2016: Section 2.3, Theorem 3, equation (18), and Appendix B, PDF pages 9–10 and 29–31. The PDF was text-inspected. The [publisher record](https://link.springer.com/article/10.1007/s00222-015-0586-8) independently confirms Inventiones mathematicae 202 (2015), 1199–1240. The inspected arXiv version is later than publication; do not describe its file date as 2015.
3. Beresnevich–Nesharim–Yang, *Winning property of badly approximable points on curves*: [arXiv v3 full text](https://arxiv.org/html/2005.02128), Section 1.2, definitions, equation (1.9), Corollary 1.7 and its proof. [Institutional publication record](https://eprints.whiterose.ac.uk/id/eprint/177762/) confirms publication in Duke Mathematical Journal, 2022, pp. 2841–2880, DOI [10.1215/00127094-2022-0038](https://doi.org/10.1215/00127094-2022-0038).

## Exact target and hypothesis match

Fix an integer n≥2. Let X_n be the real ξ for which there are positive constants c_lower(ξ,n), c_upper(ξ,n), independent of the approximant α, such that

- |ξ−α| ≥ c_lower H(α)^(−n−1) for every algebraic α of degree at most n;
- |ξ−α| ≤ c_upper H(α)^(−n−1) for infinitely many distinct algebraic α of degree at most n.

Question 5.2 asks whether X_n strictly contains the real algebraic numbers of degree n+1. The word “real” in this last comparison is forced by X_n⊂R; reading it as including nonreal degree-(n+1) numbers would make literal containment impossible and is not the mathematical question being asked.

The original height is the maximum absolute coefficient of the integral minimal polynomial, conventionally chosen primitive and with positive leading coefficient. It is not logarithmic Weil height or Mahler measure. Both resolving papers use the same naive height. Sign normalization has no effect. The original notation suppresses n in the constants because n is fixed; it imposes no common constant across different n.

Beresnevich defines B_n using |P(ξ)|≥b H(P)^(−n) for all nonzero P∈Z[x] of degree ≤n. His B_n* uses the lower algebraic inequality for all **real** algebraic approximants; W_n* uses a strict upper inequality for infinitely many real algebraic approximants. All degree bounds are ≤n, not exactly n. Existential constants make the strict versus weak upper inequality irrelevant: increase a weak-bound constant to obtain a strict bound, and a strict bound immediately implies a weak one.

Theorem 3 states full Hausdorff dimension for finite intersections of B_k and of W_k*∩B_k* over 1≤k≤n in an interval. Use a nonempty open interval, avoiding degenerate single-point readings of “any interval.” In particular B_n has dimension one in each such interval. Equation (18) asserts B_n⊂W_n*∩B_n*; the upper-bound part is indispensable, and the mere existence of points in B_n* would not by itself settle the question.

## Independently checked bridge 1: complex lower bounds

Take ξ∈B_n with constant b>0. For an algebraic α∈C of degree d≤n, let P be its primitive integral minimal polynomial. Thus H(P)=H(α)≥1 and P(α)=0. Set

D = sum from j=1 to n of j(|ξ|+1)^(j−1).

If |ξ−α|≤1, every point z on the straight complex segment joining ξ and α satisfies |z|≤|ξ|+1. Integrating the polynomial derivative along that segment gives

|P(ξ)| = |P(ξ)−P(α)| ≤ |ξ−α| H(P) D.

Combining this with b H(P)^(−n)≤|P(ξ)| yields

|ξ−α| ≥ (b/D) H(α)^(−n−1).

If |ξ−α|>1, the same desired assertion holds with constant 1 since H(α)≥1. Therefore c_lower=min(1,b/D)>0 works simultaneously for every real or complex α of degree ≤n. No complex-valued mean-value theorem is invoked. The integral identity, or polynomial factorization of P(ξ)−P(α), is sufficient.

This completes the precise real/complex scope extension needed for the original wording. The published real upper approximants remain admissible when the pool of approximants is enlarged to C.

## Independently checked bridge 2: the Appendix B upper construction

The following is a constant-robust reconstruction of the published elementary bridge, importing Minkowski's convex-body theorem as a standard theorem. It avoids relying on exact numerical constants or two apparent presentation slips in the inspected preprint.

Fix ξ∈B_n and a lower-bound constant b>0. For each large integer Q, seek integral coefficients with

|P(ξ)|≤δ Q^(−n),  |P'(ξ)|≤LQ,  |a_j|≤Q for 2≤j≤n,

where δ>0 is small and L=2/δ. The linear map from (a_0,…,a_n) to (P(ξ),P'(ξ),a_2,…,a_n) has determinant 1. The symmetric box has volume 2^(n+1)δL=2^(n+2), greater than Minkowski's threshold. Hence a nonzero integral P exists.

If |P'(ξ)|≤Q, then

|a_1|≤Q+Q sum_{j=2}^n j|ξ|^(j−1),

and, using P(ξ)−ξP'(ξ),

|a_0|≤δQ^(−n)+|ξ|Q+Q sum_{j=2}^n (j−1)|ξ|^j.

For δ≤1 these give H(P)≤C Q with C depending only on ξ,n. Choose δ<b C^(−n). The polynomial lower bound would then give |P(ξ)|≥b C^(−n)Q^(−n), a contradiction. Thus |P'(ξ)|>Q. The construction also gives H(P)≤D_0Q for a constant D_0 depending on ξ,n,b, since the original derivative bound is LQ.

For h=±Q^(−n−1), the linear term P'(ξ)h has magnitude >Q^(−n), while |P(ξ)|≤δQ^(−n). The higher-order Taylor remainder is O_{ξ,n}(Qh²): all coefficients of degree at least 2 have size at most Q. Taking δ<1/4 and Q sufficiently large ensures P(ξ+h) has opposite signs at the two endpoints. The intermediate value theorem therefore supplies a **real** root α_Q with |ξ−α_Q|≤Q^(−n−1).

To relate the construction height to naive algebraic height, let F be the primitive minimal polynomial of α_Q. Gauss's lemma gives P=FR with nonzero R∈Z[x]. For bounded degree there is κ_n>0 such that H(FR)≥κ_n H(F)H(R). One elementary justification is compactness: normalize each factor to coefficient sup norm one; the set of such pairs of polynomials of degree ≤n is compact, multiplication is continuous, and its product is never the zero polynomial. Consequently its coefficient sup norm has positive minimum. Since H(R)≥1, H(α_Q)=H(F)≤κ_n^(−1)H(P)≤κ_n^(−1)D_0Q. Therefore

|ξ−α_Q|≤(κ_n^(−1)D_0)^(n+1) H(α_Q)^(−n−1).

Finally ξ cannot itself be algebraic of degree ≤n, since its minimal polynomial would violate membership in B_n. Any fixed α_Q can occur only for bounded Q because |ξ−α_Q|>0 and Q^(−n−1)→0. Thus the construction gives infinitely many distinct real approximants with a single uniform-in-α constant.

### Presentation cautions, not counterexamples

The inspected preprint's proof of Theorem 3 writes a comparison between H^(−1) and H(P)^(−k) with the wrong direction when H(P)<H^(1/k). The required conclusion follows by choosing H=(2H(P))^k, at the cost of the harmless factor 2^(−k), or by a limiting argument. Appendix B's displayed bound for a_0 is also not justified by naively bounding a_1 after its separate estimate; the exact identity P(ξ)−ξP'(ξ) used above supplies the needed bound. These are not a reason to reject the published dimension theorem or the independently verified bridge.

## Independently checked bridge 3: genuine strict containment

Let ξ be real algebraic of degree d=n+1, with primitive minimal polynomial A of leading coefficient a≠0 and conjugates ξ=ξ_1,…,ξ_d. For a nonzero integral P of degree m≤n, A and P have no common root. Their resultant is a nonzero integer, so

1≤|Res(A,P)|=|a|^m product_{i=1}^d |P(ξ_i)|.

For i≥2,

|P(ξ_i)|≤H(P) sum_{j=0}^n |ξ_i|^j.

Since |a|^m≤max(1,|a|^n), rearrangement proves |P(ξ)|≥c(ξ,n)H(P)^(−n). The same argument covers constant nonzero P, or those can be handled directly. Hence ξ∈B_n, and the preceding two bridges imply ξ∈X_n.

On the other hand, Theorem 3 gives dimension one for B_n∩I. Algebraic numbers form a countable set and have Hausdorff dimension zero. Since the dimension of a union is the maximum of the dimensions of its two constituents, the transcendental part of B_n∩I still has dimension one. It lies in X_n and is disjoint from the real degree-(n+1) algebraic numbers. This proves strict containment.

## Stronger countable-degree result and boundary of the audit

Beresnevich–Nesharim–Yang's Corollary 1.7 states that both countable intersections, of B_n and of B_n*∩W_n*, have full dimension on an open interval intersected with the support of an Ahlfors regular measure. Lebesgue measure gives dimension one. Its proof uses the Veronese maps and Corollary 1.6; equation (1.9) imports the same algebraic-approximation inclusion. Consequently one ξ can satisfy all positive degrees, with degree-dependent constants. Such ξ are necessarily transcendental, since a minimal polynomial would exclude an algebraic ξ from B_n at its own degree. This is stronger than the original fixed-n problem.

The present audit verifies definitions, quantifiers, real/complex scope, the elementary bridges, and the logical application of the published dimension results. It does not independently rederive the deep analytic nondegenerate-manifold/curve dimension and absolute-winning results, their quantitative nondivergence inputs, or every proof in either paper. Those are explicitly imported published theorems. The appropriate disposition is **already solved by published results**, not an original proof claim and not an unresolved all-degrees substitute.
