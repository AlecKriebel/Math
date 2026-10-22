# Independent review: k303,b / 5100015

2026-10-01. **Verdict: PASS for the full source target. No mathematical correction is required.** This is a review of the saved proof, not a novelty, priority, or human-peer-review certification.

## Frozen version and independence

- `PROOF.md` SHA-256: `4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2`
- `FROZEN_MANIFEST.json` SHA-256: `5cd81a68a71e96b1fd34f94babc72a63fe6404f5918214c58ae26fe0ff0c5caa`
- All sixteen frozen entries and all three primary PDF hashes match; see `FROZEN_INPUT_VERIFICATION.json`.

I did not contribute to this target's derivation. I read the frozen mathematical argument, reconstructed its algebra and meromorphic proof, checked the original sources, and wrote a separate checker using direct tangent intersections and orthogonal projections. My separate work on the different focal-pedal distance-sum target k601 shares classical Jacobi inputs but supplies no premise to this proof or review. Neither the parallel k303,a nor k203,a result is assumed here.

## 1. Exact source scope

I read the full imported target and prior report, and independently rendered and inspected [arXiv v11](https://arxiv.org/pdf/2004.12497v11) Table 4, page 6, and the [published Table 4](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), page 346. Both specify the product of the outer polygon's area and its pedal area, center M=O, for periods not divisible by four. The candidate covers both odd N and N congruent to two modulo four.

Section 3.4 supplies the outer-pedal definition, and the source's signed-shoelace convention applies. The feet are on tangent lines to the outer ellipse at the original billiard vertices, which are the sides of the outer polygon. They are not the feet on the original chords or the caustic contact points. The chosen cyclic indexing is correct up to a harmless overall cyclic shift. Stars retain traversal order; neither filled-lobe area nor a spatial re-sorting is used.

The nondegenerate nested confocal ellipse hypothesis is preserved. The source's a>b makes 0<k<1. Hyperbolic and degenerate caustics are excluded explicitly. The proof has no division by an area, so it does not need an unproved nonvanishing area or centroid hypothesis.

## 2. Canonical parametrization and signed area identities

[Stachel's published Theorem 4.3](https://doi.org/10.1007/s40879-021-00524-2), pages 1614–1615, gives exactly the parametrization used. The caustic eccentricity is the modulus k; software uses the parameter k². For a primitive winding class, 0<tau<N/2 puts v strictly between 0 and K, making cn(v), dn(v), sn(v) and the required real denominators nonzero with the stated signs. The outer axes have the same focal difference as the caustic and strictly exceed its axes.

I independently reduced the endpoint determinant in equation (6) using the Jacobi addition formulas and quadratic identities. Its denominator is positive on real arguments. Summing the endpoint dn terms counts each vertex twice, which cancels the shoelace factor one-half and gives equation (7) with the stated coefficient.

For edge vectors D_i=P_(i+1)−P_i, bilinearity gives `area(D)=2area(P)−(1/2)Σ det(P_i,P_(i+2))`. This identity holds for any ordered polygon, with no simplicity assumption. The skip-two determinant sum can be evaluated by the same Jacobi formula even when its index permutation splits into two cycles. Equation (8) therefore has neither a missing factor nor an implicit odd-period restriction.

The contact phase in equation (4) is checked directly by substitution into the caustic tangent line. The polarity calculation then gives the actual intersection of endpoint tangents, with the diagonal area scale in equation (10). Parallel endpoint tangents on a central ellipse would require antipodal endpoints; their chord passes through the center and cannot be tangent to a strictly interior nondegenerate confocal ellipse. Thus no real outer vertex at infinity has been silently discarded.

## 3. Center-pedal/edge-vector identity

The foot of the origin on a line n·X=1 is n/(n·n). Applying this to the outer ellipse's tangent gives exactly equation (11). Its denominator is bounded below by b²>0 for real parameters.

For w=K−v, the [classical quarter-period identities](https://dlmf.nist.gov/22.4) give dn(w)=b/a and cn(w)=k′sn(v)/dn(v)>0. I checked the common denominator and both coordinates of the claimed linear image of `P(z+w)+P(z−w)` separately. The resulting scale matrix is `diag(b/a,1)/(2cn(w))`, with determinant b/(4a cn²(w)).

Replacing one summand using P(z−2K)=−P(z) gives the difference of the two vertices separated by 2v at the shifted phase. It is the negative of that orbit's ordered edge vector. A global minus sign has determinant +1 in dimension two and leaves signed area unchanged. Equations (14) and (15) thus have the correct sign and factor. This is a pointwise identity for the actual center pedal, not a similarity inferred from area data.

## 4. Complete meromorphic audit of the trace lemma

The needed data were checked against [DLMF Tables 22.4.1–22.4.3](https://dlmf.nist.gov/22.4): dn has periods 2K and 4iK′, changes sign under 2iK′, is even, and has simple poles at iK′ modulo translations by 2K and 2iK′. Its zeros lie at K+iK′ under the same congruences. These signs are important; the candidate uses the correct ones.

Here is the pole accounting on the actual quotient. For odd q, the finite real subgroup H has order q modulo 2K. The sum U is periodic under H and under 4iK′, and remains anti-periodic under 2iK′. Its possible poles are the shifted dn poles, each of order at most one. One could use the smaller real period 2K/q; retaining 2K as in the proof gives a valid compact torus as well.

Let c=K+iK′. Since 2c=2K+2iK′ is an anti-period of dn, evenness gives dn(c+t)=−dn(c−t). The real subgroup H is stable under negation and, because q is odd, does not contain K modulo 2K. Hence each summand of U(c) is finite and the terms cancel in opposite pairs; the self-paired term is also zero. Thus U(c)=0 without evaluating a divergent expression.

Every possible pole p of U has p+K congruent to c modulo H and an integral imaginary anti-period. Consequently the second factor U(z+K) is holomorphic and vanishes at z=p. This removes the at-most-simple pole of the first factor. At a pole of the shifted factor, z=p−K, the first factor equals U(p+K) by its 2K real period and similarly vanishes. These are all possible poles. In particular, oddness prevents the two pole sets from coinciding; no pole-pole product is being called removable.

The product is therefore a holomorphic function on a compact nondegenerate torus and is constant. Its value on the real line is positive, since real dn is positive. The argument does not assume the residues or zero orders numerically; a zero of order at least one suffices against a simple pole. It also works for q=1, although the physical two-bounce nondegenerate ellipse case is excluded separately.

For primitive N and tau coprime to N, the dn shifts have order `q=N/gcd(N,2)` modulo 2K and multiplicity `r=N/q`. Thus T=rU exactly, and the parity condition N not divisible by four is equivalent to q odd. The multiplicity factor r² in the product is automatically retained in T(0)T(K). The period 2v aligns the two phase arguments in equations (10) and (15), proving equation (20) with the full coefficient (21).

## 5. Boundary and interpretation checks

- Reversing traversal reverses both signed areas, preserving their product.
- Repeating an orbit multiplies each area by the repetition number. An admissible listed period cannot have a primitive divisor divisible by four. Thus the stated repetition extension has no parity gap.
- N=2 with the stated caustic would require an inadmissible center-crossing tangent chord; it is correctly excluded.
- The elliptic curve is nondegenerate for 0<k<1. The circular limit is treated separately by rigid rotation, not by invoking a collapsed complex torus. A zero minor caustic axis is not covered.
- No arbitrary-point M theorem is asserted. The overlap with the center special case of a parallel even-period target is disclosed, and the odd-period argument is independently present here.
- The exact excluded four-period products 1152 and 1250 are useful negative controls, not counterexamples to the claimed range.

## 6. Independent controls and final disposition

My separately authored `independent_check.py` passes **6,195 exact assertions** and **6,615 high-precision diagnostics** over 45 families at 80 decimal digits. The maximum scaled residual is about 1.55e-79. The geometric diagnostics construct outer vertices by solving the actual tangent-line intersections and pedals by direct orthogonal projection. They cover odd and two-mod-four periods, all primitive winding classes for the sampled periods, orientation reversal, repeated traversals, and the pointwise pedal identity. Complex diagnostics check the trace product and reflected zero away from unexamined numerical singularities. Exact rational controls reproduce the two excluded four-period products.

The finite arithmetic range checks and high-precision evaluations are not a universal proof or interval certificates. The analytic proof above supplies the all-period, all-phase conclusion. I inspected the author's checker and receipt but did not execute its self-writing script or count its reported 5,660 exact / 4,512 numerical checks as my independent run.

The review is complete. All sixteen author inputs and three primary PDFs were hash-verified and no frozen author file was edited. The five portable review artifacts are this report, `independent_check.py`, `INDEPENDENT_CHECKS.json`, `FROZEN_INPUT_VERIFICATION.json`, and `REVIEW_SHA256SUMS.json`. The local rendered source pages are reading aids and must not be included.

**Final disposition:** the unchanged frozen proof may be presented as a separately reviewed full claim for k303,b with its exact source scope and classical attributions. No mathematical blocker or mandatory correction was found. Publication remains the coordinator's action; this review made no remote changes.
