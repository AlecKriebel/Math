# Hausdorff gauges for parabolic elliptic conformal measures

Problem 30001397 / OWR-4137-017. Author investigation, 2026-10-04.

**Disposition: unresolved after five substantive approaches.** This document proves reductions and obstructions to particular approaches, not a proof or counterexample to the full source question. The arguments are AI-assisted and have not yet had independent audit or human peer review. No novelty is asserted for standard measure-theoretic reductions or consequences of the cited results.

## 1. Exact target and conventions

Let f be a nonconstant doubly periodic meromorphic function on C. All its finite critical points are attracted to attracting or parabolic cycles, and at least one parabolic cycle exists. Write J=J(f), and h=dim_H J. The question is whether a scalar gauge g can make H_s^g restricted to J equal to the atomless spherical h-conformal probability m_s. A gauge here is positive and nondecreasing on (0,r0), with g(r) tending to zero at zero; continuous gauges are sufficient for the classes tested below. Covers are charged g(diam_s U), with no dimensional normalization factor.

The source is Urbański's Problem 10, OWR 54/2009, printed p.2961 [S1]. It asks for equality of measures on all Borel subsets, not just positive mass or equivalence. Multiplying a gauge by c multiplies its Hausdorff measure by c, so proportionality can be normalized to equality. This note follows the spherical convention of the cited paper [S2]. The Euclidean conformal measure is a different, generally infinite measure. Neither the radial Julia set nor an f-invariant probability is substituted for J and m_s.

Here attraction is interpreted in its usual basin sense, so finite critical points lie in the Fatou set. Under this interpretation the source class is included in the parabolic elliptic class in [S3, Observation 14.4.18, Corollary 16.3.2]. A broader interpretation that permits critical points landing exactly on a parabolic cycle requires the separate scope caveat in LIMITATIONS.md; no full assertion for that broader class is made. The conclusions used below are: 1<h<2; m_s exists, is atomless, unique among spherical conformal probabilities without atoms, and has full topological support; H_s^h(J)=0; and m_s-almost every point is transitive. The parabolic basin is nonempty, so J is not all of C; the implication h=2 => J=C gives h<2. If q_max is the maximal pole multiplicity then h>2q_max/(q_max+1). These are prior results, not new results of this investigation. References and exact inspection locations are in SOURCE_VERIFICATION.json.

## 2. Approach 1: power and logarithmic gauge comparison

### Proposition 1 (elementary comparison)

For any metric space and set E, if g(r)<=C k(r) for all sufficiently small r, then H^g(E)<=C H^k(E). Indeed apply the inequality term by term to every sufficiently fine cover and then take infima and the limit of covering scales.

Consequently every g=O(r^h) gives H_s^g(J)=0 and cannot represent m_s. Every pure power fails: g=r^s gives zero if s>=h and infinity if s<h. The latter is the defining critical-exponent property of Hausdorff dimension. More generally, if lim_{r->0} log(g(r))/log(r)=s exists and s differs from h, choose an exponent strictly between s and h. The logarithmic limit bounds g above or below that intermediate power, proving the same zero/infinity alternative.

For g(r)=r^h (log(1/r))^a (log log(1/r))^b near zero, all a<0, and a=0,b<=0, are excluded by the O(r^h) criterion. Larger corrections survive this test. This is not a construction of a successful correction. The test does not exclude an arbitrary oscillating gauge merely because g(r)/r^h is small along some sequence. Without control of covering scales, replacing an eventual bound by a subsequential bound is unjustified.

**Outcome:** all pure powers and bounded-above h-power corrections are rigorously eliminated. Positive logarithmic corrections and irregular gauges remain.

## 3. Approach 2: regular variation reduces equality to total mass

Say g is regularly varying at zero with index h if g(ar)/g(r)->a^h for every fixed a>0. All the logarithmic gauges above satisfy this condition.

### Proposition 2 (conformal change of variables)

Let F be a C^1 conformal diffeomorphism between open subsets of a smooth Riemannian surface, with positive metric dilation lambda(x). For a regularly varying gauge g of index h and any Borel E on which H^g is finite,

H^g(F(E)) = integral_E lambda(x)^h dH^g(x).

Here the measures on the two sides use their respective surface metrics.

**Proof.** If F is L-Lipschitz on A, push forward a fine cover of A. Its costs are at most sup_{0<r<=delta} g(Lr)/g(r) times the original costs. Regular variation makes this supremum tend to L^h. Thus H^g(F(A))<=L^h H^g(A). If F is also l-co-Lipschitz, application to F^{-1} gives the opposite bound l^h H^g(A).

On a relatively compact chart on which F is a diffeomorphism, continuity of its derivative, and of the derivative of its inverse, produces arbitrarily small neighborhoods where these two constants are as close as desired to lambda at the center. Partition the chart into countably many disjoint Borel pieces subordinate to such neighborhoods. The bounds on each piece squeeze the image measure between lower and upper simple-function integrals approximating lambda^h. Let the maximum oscillation tend to zero. Exhaust the domain by relatively compact charts. This proves the formula; localization also gives it for sigma-finite H^g. This is the standard covering argument underlying [S4, Lemma 4.3], here stated for local conformal maps rather than a group action. QED.

### Corollary 2.1 (conditional solution within the regular-variation class)

If g is regularly varying with index h and 0<H_s^g(J)<infinity, then

H_s^g|J / H_s^g(J) = m_s.

**Proof.** A singleton has zero H^g measure because g(r)->0. Delete the countable poles and critical points and cover the remaining part of J by countably many local injectivity neighborhoods. Proposition 2 on a disjoint Borel refinement gives the spherical h-conformality identity for H_s^g|J wherever f is injective. The deleted points and their images have zero mass. Normalize and apply uniqueness of the atomless spherical conformal probability. QED.

This handles equality, not only equivalence, once positive finite total mass is known. It does not prove that such a gauge exists. It also does not show every possible exact gauge is regularly varying. The full question allows gauges outside this class.

### Metric warning

Use spherical line element rho(z)|dz| with rho(z)=(1+|z|^2)^(-1). For an index-h regularly varying gauge, multiplying the metric by a constant c multiplies its Hausdorff measure by c^h. For an arbitrary gauge, the corresponding exact representation is preserved by replacing g(r) with g(r/c); it need not be a scalar rescaling of the fixed-gauge measure. The spherical derivative is f#(z)=|f'(z)|rho(f(z))/rho(z). If m_s is spherical h-conformal, then

dm_e(z)=rho(z)^(-h) dm_s(z)

is Euclidean h-conformal. The identity follows directly by substituting f# in the conformality integral. In the regularly varying case Proposition 2 also gives dH_s^g=rho^h dH_e^g locally. Equal dimensions do not mean these measures are equal. An argument disproving equality between m_s and a translation-invariant Euclidean Hausdorff measure would address an inconsistent metric normalization, not the source question.

**Outcome:** the regular-variation subclass is reduced precisely to positive finite total Hausdorff mass. No such total-mass estimate is obtained.

## 4. Approach 3: lattice tails and incompatible uniform ball laws

### Proposition 3 (translation invariance and spherical tails)

The Euclidean measure m_e above is invariant under translations by the period lattice Lambda. It is finite on compact sets and infinite on C. Moreover

m_e({R<=|z|<2R}) asymp R^2, and m_s({|z|>=R}) asymp R^(2-2h)

as R tends to infinity. Constants may depend on f and normalization, not R.

**Proof.** Let w be a period. On any injectivity neighborhood for f away from a pole or critical point, f(A+w)=f(A) and f'(z+w)=f'(z). Euclidean conformality for every Borel A in that neighborhood says the measures |f'|^h dm_e and |f'|^h d(T_{-w})_*m_e agree. Their weights are positive, so the measures agree there. A countable partition and atomlessness remove the exceptional points, proving translation invariance.

The weight rho^(-h) is bounded on every compact set, so m_e is locally finite. Choose a bounded Borel fundamental cell Q. It has a finite positive mass: finiteness follows from boundedness, and positivity from the countable partition of C into translates and nonzeroness of m_e. The number of whole lattice cells in {R<=|z|<2R} is bounded above and below by positive multiples of R^2, using the finite cell diameter and lattice area. This proves the annulus estimate and infinite total mass. On that annulus rho^h is comparable to R^(-2h). Sum the annulus masses over R,2R,4R,...; the geometric sum converges because h>1. QED.

### Proposition 4 (pole ball law)

At a pole b of multiplicity q,

m_s(B_s(b,r)) asymp r^alpha, where alpha=(q+1)h-2q.

In particular 0<alpha<h. The same exponent holds for Euclidean balls and m_e at a fixed finite b.

**Proof.** Near b, f(z)=a(z-b)^(-q)(1+O(z-b)), a nonzero. The component V_R of {|f|>R} near b has inner and outer radii comparable to R^(-1/q). Divide R<=|w|<2R into finitely many simply connected angular sectors and use the q inverse branches near b. On each branch |(f^{-1})'(w)| is comparable to R^(-1-1/q). By Euclidean conformality and Proposition 3,

m_e(V_R minus V_{2R}) asymp R^(2-h(1+1/q)).

Boundary sectors can be chosen disjoint and assigned by a Borel partition; the estimates apply by restriction to such pieces. Summing over dyadic R yields m_e(V_R) asymp R^(2-h(1+1/q)), since 2-h(1+1/q)<0. The mass of b is zero. The radius comparison and monotonicity of ball mass give the asserted exponent. Passing to spherical balls and m_s at a fixed finite center multiplies radii and masses by bounded factors. Finally alpha>0 follows from h>2q/(q+1), and alpha-h=q(h-2)<0. QED.

This also follows by combining both estimates in [S3, Lemma 16.3.8] at t=h. The geometric proof is included to expose the signs and the role of the metric.

### Proposition 5 (no globally uniform gauge ball estimates)

At a parabolic periodic point a, pass to a local iterate F fixing a with multiplier one and write F(z)=a+(z-a)+c(z-a)^(p+1)+higher terms, c nonzero and p>=1. The local parabolic conformal-measure law [S3, Lemma 12.10.1], applied to this iterate, is

m_s(B_s(a,r)) asymp r^beta, where beta=(p+1)h-p.

Thus beta>h. The assumption that m_s is atomless removes the singleton in the cited law. Because beta-alpha=p(h-1)+q(2-h)>0, the ratio

m_s(B_s(b,r))/m_s(B_s(a,r)) asymp r^(alpha-beta)

tends to infinity. Therefore there do not exist any gauge g, constants 0<c<=C<infinity and r0>0 such that

c g(r)<=m_s(B_s(x,r))<=C g(r)

for every x in J and every 0<r<r0. Indeed such bounds would keep that ratio at most C/c. QED.

This obstruction invalidates a route demanding globally uniform two-sided density estimates, even for gauges outside regular variation. It is **not** a counterexample to the actual problem. Equality to a Hausdorff measure does not entail such uniform bounds. A countable set of pole/parabolic centers has zero m_s mass, so their exceptional local exponents alone cannot settle an almost-everywhere density question.

**Outcome:** the uniform-density strategy is blocked by a proved incompatibility; the source question survives.

## 5. Approach 4: parabolic inducing and finite versus infinite invariant mass

The conformal probability m_s and the invariant measure mu are distinct objects. Prior theory gives a sigma-finite invariant mu equivalent to m_s; it need not be finite [S3, Theorem 18.1.1]. For the parabolic class its finiteness criterion is h>2p_max/(p_max+1) [S3, Theorem 18.7.1]. Thus ordinary probability recurrence cannot be used uniformly over the source class without inducing.

Here is the elementary tail calculation behind the two different exponents. If the n-th inverse parabolic excursion has scale n^(-1/p), derivative comparable to n^(-(p+1)/p), and conformal mass comparable to n^(-a), where a=h(p+1)/p, then

sum_{n>=N} n^(-a) asymp N^(1-a), because a>1.

Setting r=N^(-1/p) gives r^((p+1)h-p), the exponent beta of Proposition 5. By contrast, the tower mass involves the first moment sum n*n^(-a), which is finite exactly when a>2, equivalently h>2p/(p+1). These calculations concern different quantities. The first cannot be replaced by the second to choose a Hausdorff gauge for m_s.

An exact one-dimensional control is phi(x)=x/(1+x). Induction and differentiation give

phi^n(x)=x/(1+nx), and (phi^n)'(x)=(1+nx)^(-2).

For I=[1/2,1], phi^n(I)=[1/(n+2),1/(n+1)]; these intervals have disjoint interiors. A toy allocation of mass proportional to n^(-2h) has cumulative tail comparable to r^(2h-1), while its tower first moment changes convergence at h=1. This is a local parabolic model, not an elliptic counterexample or an exact model of the full induced system.

A promising induced construction would require simultaneous control of parabolic waiting times, pole branches, and geometric contractions when returning to a compact base. The published existence of a strongly regular induced graph-directed system does not by itself identify a finite positive gauge Hausdorff measure in the original metric. We do not have the requisite estimates for arbitrary gauge covering costs.

**Outcome:** the tower mechanism explains why invariant-measure tail calculations do not answer the conformal gauge question; no gauge is constructed.

## 6. Approach 5: upper-density obstruction and an exact extreme-value model

For a doubling gauge g, a finite Borel measure m, and E on which

limsup_{r->0} m(B(x,r))/g(r)=infinity for every x in E,

one has H^g(E)=0. For completeness, choose at each x arbitrarily small balls satisfying m(B)>M g(r). A disjoint 5r-covering selection covers E by the enlarged balls. Doubling bounds the total g-cost of that cover by a fixed constant times m(the ambient space)/M. Send the cover scale to zero and then M to infinity. Localize for an unbounded space. This is the familiar density obstruction; no exact equality follows from mere comparability of densities.

The pole argument in the proof of H^h(J)=0 transports small balls around a pole back along inverse branches. More precisely, put d_j=|f^(n_j)(x)-b| and D_j=|(f^(n_j))'(x)| at visits avoiding postcritical obstructions. Bounded distortion provides radii r_j=K d_j/D_j and the lower bound

m_e(B_e(x,r_j))/r_j^h >= c d_j^(-gamma), gamma=q(2-h)>0.

The radii tend to zero, as required for the density argument. The inverse branches in this construction are defined on disks of a fixed radius R>0 centered at f^(n_j)(x), and their images omit a fixed pole c. Since each branch maps its disk center to the fixed finite point x, Koebe's quarter theorem gives R/(4D_j)<=|x-c|. Thus 1/D_j is bounded, and d_j->0 implies r_j=K d_j/D_j->0. This supplies no quantitative relation between the contraction D_j and the return distance d_j.

For g(r)=r^h L(1/r), this yields

m_e(B_e(x,r_j))/g(r_j) >= c d_j^(-gamma)/L(1/r_j).

The formula is quantitative about d_j and D_j but transitivity only says d_j->0 along a subsequence; it provides no comparison with L(D_j/(K d_j)). This is the exact missing estimate. Since x is fixed and finite, spherical and Euclidean comparisons preserve the obstruction for regularly varying g. No such preservation is assumed for arbitrary wildly varying g.

### Proposition 6 (a genuine zero/infinity model, not an elliptic theorem)

Let X_n be independent identically distributed variables with P(X_n>t)=t^(-kappa) for t>=1, kappa>0. Let a_n>=1 tend to infinity. Almost surely,

limsup X_n/a_n = 0 if sum a_n^(-kappa)<infinity,
and limsup X_n/a_n = infinity if that sum diverges.

**Proof.** In the convergent case, for each epsilon>0 all but finitely many epsilon*a_n exceed 1, and sum P(X_n>epsilon*a_n)=epsilon^(-kappa) sum a_n^(-kappa)<infinity up to finitely many terms. First Borel-Cantelli gives an eventual upper bound epsilon; intersect over epsilon=1/k. In the divergent case, for every positive integer K the independent events X_n>K*a_n have a divergent sum of probabilities, so second Borel-Cantelli gives infinitely many occurrences. Intersect over K. QED.

Thus a polynomial-tail independent-excursion model admits no deterministic normalization with a finite positive upper limit. If all X_n instead equal one variable X, their one-dimensional marginal tails are unchanged but X_n/a_n->0. This proves why local ball-tail exponents alone cannot justify an independent-excursion conclusion.

The Kleinian-group analogue [S4, Theorem 1.1] rigorously implements a density/recurrence mechanism. Its actual theorem requires a differentiable monotone log-gauge correction with a limiting derivative and group-specific global measure and Khinchin laws. It cannot be imported for elliptic maps, nor cited here as a theorem about every irregular gauge. In the source setting we have not proved the necessary all-scale measure law or the corresponding shrinking-target zero-one theorem, in either finite or infinite invariant-mass regimes.

**Outcome:** the probabilistic obstruction is rigorous only in the explicitly stated independent model. Transfer to the elliptic system remains unsupported. This fifth approach therefore ends without a complete solution.

## 7. Boundary cases and conclusion

- h=2 is excluded by the source dynamics; it would erase the pole anomaly.
- h=1 is excluded by the elliptic dimension bound; it would erase the parabolic anomaly.
- A hyperbolic elliptic map without parabolic points is outside the question; its finite packing measure is not a solution here.
- The source quantifies over parabolic elliptic maps satisfying the critical-orbit hypothesis. An arbitrarily selected h,p,q triple in an arithmetic check is not a realized elliptic parameter.
- Full-mass transitive or radial subsets cannot replace J unless the complementary H^g mass is controlled. m_s-null sets need not be H^g-null before the desired representation is established.
- A dimension computation, invariant-measure theorem, density comparison, or failure of uniform Ahlfors estimates is not a full gauge solution.

The strongest partials are the regular-variation reduction in Corollary 2.1 and the global uniform-gauge obstruction in Proposition 5. Neither resolves the existence of an arbitrary exact gauge. The final state is **UNSOLVED, 5/5 approaches used**. The packet is frozen for a fresh independent audit, and no remote writes were made.

## References

[S1] Mini-Workshop: The Escaping Set in Transcendental Dynamics, OWR 54/2009, Problem 10, p.2961. https://doi.org/10.4171/OWR/2009/54

[S2] J. Kotus and M. Urbański, Geometry and ergodic theory of non-recurrent elliptic functions, J. Analyse Math. 93 (2004), 35-102. https://doi.org/10.1007/BF02789304 . Author's 62-page PostScript version inspected; journal typesetting not claimed byte-identical.

[S3] J. Kotus and M. Urbański, Ergodic Theory, Geometric Measure Theory, Conformal Measures and the Dynamics of Elliptic Functions, arXiv:2007.13235v1 (2020). https://arxiv.org/abs/2007.13235v1 . The later Cambridge 2023 book has different chapter numbering; this note's theorem numbers refer to the inspected arXiv version.

[S4] D. Simmons, On interpreting Patterson-Sullivan measures of geometrically finite groups as Hausdorff and packing measures, arXiv:1408.4664v3; Ergodic Theory Dynam. Systems 36 (2016), 2675-2686. https://arxiv.org/abs/1408.4664v3 . The restricted hypothesis in Theorem 1.1, rather than its broad abstract wording, governs the analogy here.
