# Independent mathematical audit: KP-1.74 / problem 2733

## Verdict and scope

ACCEPT the frozen package's mathematical deductions as a partial formulation audit. No substantive mathematical correction is required. Do not classify it as a solution or disproof of the intended nontrivial-summand conjecture. The intended part (a) and part (b) remain unresolved; two approaches have been used out of five. This is a written mathematical review, not a formal proof-assistant certification.

The reviewed archive is CONNECTED_SUM_ROPELENGTH_2733_AUTHOR_SAFE_FREEZE.zip, 16,395 bytes, SHA-256 f05d1acd29f9366fa08facff81b97e561bcadd60072584dce6037a001e273953. Its separate author manifest is 3,750 bytes, SHA-256 c715974ed45a383eb56086518b506887b340671025d532f3a33cf36f62cdeb44. Both pins were independently recomputed for this review. The original files were not edited. This document is separate acceptance evidence; it does not replace the frozen status or its historical independent-audit-pending field.

## 1. Normalization, domain, and source wording

The definition uses normal-tube radius/reach, not tube diameter. Scaling a curve by a positive factor scales its length and reach by that same factor. Consequently normalizing a positive finite reach to one turns its length into its ropelength. Smooth/tame knot types admit finite positive-thickness representatives, while admissible representatives may have only C1,1 regularity. The curvature bound is an almost-everywhere bound.

The actual K3 author-preliminary PDF has 436 pages. Its printed page 69 was visually inspected and contains the unrestricted quantifier “For any knot or link types” in both clauses. Printed page 67 was visually inspected and supplies radius-one tubes and curvature bound one. Its use of “infimal” for the unique-nearest-point radius is a wording error: the intended standard reach is the supremal such radius. The frozen report already identifies and repairs that reading consistently with the Hopf normalization on page 69. No factor-of-two correction is warranted. This review does not substitute an AIM workshop summary for K3.

The CKS02 arXiv v3 text was inspected for the three-point definition, Lemmas 1, 2 and 4, Theorem 7, and Figure 1. These supply the standard thickness/reach framework, curvature and global-distance requirements, C1,1 regularity, existence, and the chain family used in the report. The proof does not depend on attainment: epsilon competitors are sufficient everywhere attainment could otherwise be invoked. As usual, the regularity assertion is about embedded closed one-dimensional manifolds with positive thickness, not arbitrary positive-reach subsets.

For link connected sums, selected components and a separated ordinary sum are essential data. The frozen proof states these restrictions. None of its identities is being asserted for an arbitrary band sum, or for a band interacting with spectator components.

## 2. Unknot value and literal formulation obstruction

The round radius-r circle has reach r: its center has nonunique closest points at distance r, whereas points at distance less than r have unique closest points. Its ratio is therefore 2π.

The lower bound handles the C1,1 issue correctly. For a periodic unit-speed parametrization γ of length ℓ and thickness one, |γ''| is at most one almost everywhere. Periodic convolution preserves periodicity and bounds the smoothed second derivative by one. Uniform convergence of first derivatives gives mη = min|γ'η| tending to one, and mη is positive for small η. For the regular smooth approximant, its total curvature is

TC(γη) = integral |projection perpendicular to γ'η of γ''η| / |γ'η| dt,

which is at most ℓ/mη. Fenchel's bound gives 2π ≤ ℓ/mη and hence ℓ ≥ 2π. Smooth approximants need not preserve embedding: Fenchel's inequality for closed regular curves suffices. Milnor50 Theorem 3.4 (printed page 254) was independently located and gives the relevant total-curvature lower bound. Thus R(U)=2π with the correct normalization.

The ordinary unknot identity K#U=K holds for a selected component of a link as well as for a knot. Its saving is exactly 2π. For U#U, the frozen (a) statement requires 2π ≤ 4, which is false. The gap is 2π−4 > 0. This is solely a formulation obstruction under the literal inclusive quantifier. It is not a counterexample in the nontrivial-knot domain.

For knots, the corollary about (b) is valid. A positive constant for all knots cannot exceed 2π. Conversely a positive constant c0 for pairs of nontrivial knots extends to all knot pairs after replacement by min(c0,2π), because every excluded pair has an unknot summand. This equivalence concerns existence of a positive constant, not equality of the optimal constants, and does not establish existence. The frozen proof correctly does not silently promote this knot-domain argument to an undefined class of link sums.

## 3. Split unions and spectator cancellation

For the lower bound R(A disjoint-union B) ≥ R(A)+R(B), normalize the whole union to reach one. Removing whole components increases or preserves the three-point thickness, because the set over which the infimum is taken is reduced. If a remaining sublink has reach t ≥ 1 and length L, then R(type) ≤ L/t ≤ L. Summing this inequality yields the claimed lower bound. The fact used here is component deletion, not the false general proposition that taking any subset preserves reach.

For the reverse inequality, choose separate reach-one epsilon competitors. Translate them into disjoint balls at mutual distance greater than two. If a point at distance less than one from the union had equally near points on both sublinks, the two nearest points would be less than two apart, a contradiction. Each sublink already has unique nearest points inside its unit neighborhood. Thus the union has reach at least one and total length at most R(A)+R(B)+2ε. Letting ε tend to zero is legitimate. No common minimizer or exact attainment is needed.

The separated connected sum on components in A1 and A2 leaves B1 and B2 split. Additivity therefore cancels their contributions exactly. In particular, joining split unknotted components of J1 disjoint-union U and J2 disjoint-union U saves only 2π even when both Ji are nontrivial. Requiring the whole links to be nontrivial cannot repair the literal (a) quantifier. This does not refute the version with two nontrivial nonsplit selected blocks.

## 4. Conditional splice certificate

Let S=R(K1)+R(K2), ε≥0, and 0≤δ<1. Under the stated geometric hypotheses, Γ is an embedded representative of the required sum, its length L is at most S+ε−s, and its reach t is at least 1−δ. Since t and 1−δ are positive and L is nonnegative,

R(K1#K2) ≤ L/t ≤ L/(1−δ) ≤ (S+ε−s)/(1−δ).

The hypotheses automatically force the numerator to be positive for a nonempty closed output; no extra unspoken negative-numerator case is used. Subtracting this upper bound from S gives exactly (s−ε−δS)/(1−δ). Its comparison with c is equivalent to s−ε−δS ≥ c(1−δ). When S>c, rearrangement yields exactly δ ≤ (s−ε−c)/(S−c). This rearrangement must not be applied with its displayed inequality direction for S<c, or divided by zero when S=c. The frozen proof correctly limits it to S>c. The equality endpoint is allowed, while δ=1 is excluded because it supplies no positive reach lower bound.

A fixed positive reach loss δ and fixed raw saving s do not supply a uniform positive lower saving as S grows; the loss term δS is correctly retained. For fixed S, a sequence of valid constructions with ε and δ tending to zero and a positive uniform lower bound s0 on s would give R(K1#K2) ≤ S−s0 by taking infimum bounds. This would not require convergence or attainment of the constructed curves. The frozen proof does not claim to have such constructions.

Most importantly, a curvature bound alone cannot establish the reach hypothesis. For instance, two disjoint radius-r circles can be placed with centerline separation d tending to zero while maintaining curvature 1/r; the union's reach is at most d/2. CKS02 Lemma 1 accordingly retains doubly critical self-distance along with curvature. Topology, tangency, curvature, all nonlocal contacts, and length must be certified simultaneously after a splice. The frozen report names this missing construction rather than inferring it from minimizer existence, exposed points, or a numerical tightening procedure.

## 5. Prior family and intended reading

For the previously known m-ring simple chain, CKS02 Figure 1 gives R(Cm)=(4π+4)m−8 for m≥2. Taking an end-component sum produces C(m+n−1), so direct subtraction gives saving 4π−4. The indexing is correct: C2 is the Hopf link with ropelength 8π and C3 has ropelength 12π+4. This is a prior exact family, not new general progress.

CLR12's abstract and discussion of prime-factor composites were inspected in its local author PDF, with the arXiv abstract independently retrieved live. They support reading the computational conjecture in the nontrivial composite-knot setting. The authors' discussion of local minima also supports the frozen report's warning that upper-bound comparisons of three unknown infima do not prove their desired inequality. The intended-domain conclusion is an inference from this inspected primary study; it is not a verified claim about uninspected wording of the complete 1997 Nature article.

## 6. Acceptance limits

No mathematical patch is required, and no derivative proof packet was created for this review. Preserve the original archive, external manifest, and their historical contents byte-for-byte. The mathematics supports exactly the existing partial/stalled status, with no novelty claim and no resolution of intended (a) or (b). This report does not certify corpus reconciliation, the full software mutation suite, exhaustive literature absence, or retrieval failures it did not independently replay. Those require their own audit evidence.

## Primary references

- K3 author-preliminary PDF, Problem 1.74 and preceding thickness convention: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- Cantarella, Kusner, Sullivan, On the Minimum Ropelength of Knots and Links: https://arxiv.org/abs/math/0103224 ; https://doi.org/10.1007/s00222-002-0234-y
- Milnor, On the Total Curvature of Knots, Theorem 3.4: https://people.reed.edu/~ormsbyk/milnor-total-curvature.pdf ; https://www.jstor.org/stable/1969467
- Cantarella, LaPointe, Rawdon, The Shapes of Tight Composite Knots: https://arxiv.org/abs/1110.3262 ; https://jasoncantarella.com/downloads/tightcompositeknots.pdf
