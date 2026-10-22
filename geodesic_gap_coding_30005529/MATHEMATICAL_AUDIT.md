# Independent audit: quadratic-root gaps and geodesic coding (row 1844)

Audit date: 2026-10-21 UTC. Verdict: **scoped partial results verified; no compatible geodesic coding established, and no impossibility theorem established.** No queue or repository changes made.

## Scope and primary sources

The actual question is Pohl's Question 2, OWR 22/2023, printed p.1255, https://doi.org/10.4171/OWR/2023/22. The supporting primary construction is Marklof–Welsh, *Fine-scale distribution of roots of quadratic congruences*, https://arxiv.org/abs/2105.02854, especially §§2.1, 3.1, 4.4–4.5 and Theorem 5.1; journal DOI https://doi.org/10.1215/00127094-2022-0081. I inspected the locally recovered text of those parts. This audit does not independently certify a comprehensive literature search or ongoing open status.

Pohl does not prescribe a finite alphabet, Hölder observable, particular section, or simultaneous conjugacy. These may be useful explicit construction objectives, but cannot be retroactively imposed as the question's hypotheses. Conversely, reconstructing every phase-space coordinate from a known symbolic presentation and then applying an unrelated measurable statistic is not an explained root-gap coding. An audit must state the exact compatibility actually proved.

## 1. Literal section reuse fails by tangency

Write a(w)=diag(sqrt(w),1/sqrt(w)). For

    g(s,v)=g_l a(s) k(-pi/2) a(1/v),

unit-speed geodesic flow is right multiplication by a(exp(t)). Direct multiplication gives

    g(s,v) a(exp(t)) = g(s,v exp(-t)).

For alpha<v<beta, all sufficiently small positive and negative times remain on the same sheet. Its first positive geodesic hitting-time infimum is consequently zero, not a positive roof. This is a local interior statement; boundary behavior does not rescue transversality. It rules out literal reuse of this sheet as a geodesic Poincare section, not all alternative sections or compatible codings. The script verifies the matrix identity symbolically without numerical approximation.

## 2. Exact arithmetic window and normalization

For D>1 squarefree, D not congruent to 1 modulo 4, Theorem 5.1 identifies root labels (m,mu mod m) with appropriately positively oriented geodesic tops

    x+i h = mu/m + i sqrt(D)/m.

For y=sqrt(D)/M, the height window alpha*y<=h<beta*y is exactly

    M/beta < m <= M/alpha,

with the lower inequality strict. For beta=infinity it imposes no positive lower bound. The full denominator cutoff m<=M is alpha=1,beta=infinity. The half-open boundaries must not be changed silently.

The elementary group identity a(y)n(u)=n(yu)a(y) shows that increasing horocycle time u corresponds to increasing horizontal position x=yu. Hence a circular horizontal gap delta corresponds to time delta/y. If N is the number of root labels, its empirical unit-mean normalization is N*delta, equivalently (N*y)*(delta/y), not just delta/y. The sum of the N circular gaps, including zeros and the wraparound gap, is one.

Let kappa be total closed-geodesic length divided by 2*pi*hyperbolic area. The transverse measure in §3.1 has total mass

    lambda = kappa*(1/alpha-1/beta).

Under normalized transverse/Palm measure, the mean return time is 1/lambda and unit-intensity gaps are lambda times return times. In the full window lambda=kappa, consistently with the spatial rescaling in §4.4 and N*y tending to kappa. Random Haar starting positions give the stationary entry process; random section points give the Palm process. They must not be interchanged to infer a nearest-neighbor law.

The locally extracted §4.5 display for recursively defined entry times appears to omit the cumulative addition, and its mean-return display needs normalization care. Do not reproduce these displays uncritically. Correct cumulative forward times obey T_0=0 and T_{j+1}=T_j+tau(g n(T_j)); the roof increments alone are not cumulative point locations. This is a mathematical normalization check, not a claim that extraction alone establishes a published erratum.

## 3. Finite multiplicity obstruction and its precise scope

At D=2,M=10, the roots as denominator-labelled points are 0/1,0/2,3/7,4/7. Their circular gaps are 0,3/7,1/7,3/7. An ordinary strict-positive first-return rule on an unlabelled set sees only three positions and cannot output the zero gap. At D=3,M=10, both 0 and 1/2 have multiplicity two. A claimed exact finite equality therefore needs labelled intersections or an explicit multiplicity convention. The paper's thin-window injectivity lemma cannot simply be promoted to global finite injectivity for the full height range.

However these coincidences do **not** obstruct the limiting gap result. Here is an elementary proof that all repeated positions are confined to finitely many denominators for fixed squarefree D>1.

Reduce a root fraction to p/q with 0<=p<q, gcd(p,q)=1; for zero use p=0,q=1. Then m=kq, mu=kp. The congruence implies k divides D and

    k^2*p^2 = D (mod q).

Moreover gcd(q,D)=1: if a prime r divided both q and D, the congruence would force r|k; then r^2|kq and r^2|k^2 p^2, forcing r^2|D, contrary to squarefreeness. For two distinct labels at this same reduced position, k differs from k'. Subtracting the congruences and cancelling the invertible p^2 modulo q gives

    q divides k^2-k'^2.

Thus q<=D^2-1 and every denominator in a repeated position satisfies m<=D*(D^2-1). There are only finitely many such positions and labels. Removing the excess copies removes only finitely many zero gaps; all positive gaps remain unchanged before renormalization. The count ratio tends to one whenever N tends to infinity, so this defect is asymptotically negligible. This is a finite-enumeration caveat, not a refutation of the primary limiting theorem.

Independent exact checks at M=500 for D=2,3,6,7,10,11,14,15,30 verify the congruences, collision divisibility, bound, window inequalities, circular sums, and normalized sums. These finite checks support implementation correctness; the proof above, not finite testing, establishes the bound.

## 4. Endpoint orientation and reconstruction

If an oriented semicircle has endpoints r_-<r_+, and h(z)=(az+b)/(cz+d) has determinant one, then

    h(r_+)-h(r_-) = (r_+-r_-)/((c*r_++d)*(c*r_-+d)).

A positive difference means a positive finite semicircle in the source's convention. A negative difference means reversed orientation; taking its absolute value as a radius and counting it anyway changes the selected family. A zero denominator gives a vertical exceptional geodesic, not an ordinary top. For example h(z)=-1/z sends oriented endpoints -1,1 to 1,-1, so the difference is -2. This elementary sign test is in the independent script.

Endpoint reconstruction can compute a center and radius, and a continued-fraction suspension can reconstruct a generic state. Neither fact alone proves that a next symbol or geodesic return corresponds to the next root in horizontal order. A useful proposed coding still needs a well-defined arithmetic observable/selection mechanism, labels or quotient rules, exceptional-set handling, measure and normalization, and a proof that its output is the relevant gap law or full point process. Equality of one marginal is weaker than equality of ordered gaps or full processes. No such compatibility proof was available in the material audited.

## Acceptance recommendation

Accept the tangency obstruction, exact dictionary/window/scaling, finite collision theorem, and orientation checks as partial progress. Reject a claim of resolution based solely on existing independent flow codings, coordinate reconstruction, endpoint enumeration, Farey/BCZ statistics, or an entropy obstruction to a stronger flow conjugacy. Keep the row unresolved unless an actual geodesic symbolic construction with the stated compatibility is supplied and verified.

Reproduce: python scripts/exact_audit.py. Outputs: exact_audit_results.json.

## Addendum: alignment audit of the five-approach report

I subsequently read REPORT.md. Its unresolved verdict, arithmetic decoder, sign restriction P>0, normalization, and finite-collision scope agree with this audit.

Three further claims were checked directly:

1. The finite states n(x)a(y), x rational, have oriented geodesic endpoints x and infinity. Both are rational cusps, so these escaping cusp-to-cusp orbits are not in the generic recurrent two-sided continued-fraction model. An almost-everywhere suspension chart is not an exact coding for these finite states without a boundary extension. This does not obstruct coding a limiting Haar-distributed state.
2. A variable geodesic-time shift of the original sheet maps (s,v) to (s,v exp(-f(s,v))) in the extended same sheet. At rank two the image remains tangent to geodesic flow; a rank drop does not give a two-dimensional section. This limited no-go is valid even if the displaced v leaves the original window.
3. At u=0, the alternative local surface g_l a(s)k(-pi/2)a(v0^-1)n(u) has tangent directions, expressed by g^{-1}delta g, proportional to N=[[0,1],[0,0]] and [[0,v0/2],[1/(2v0),0]]. These and H=diag(1/2,-1/2) are independent because v0>0. Thus it is locally transverse. The report's initial phrase 'right-trivialized' was flagged for correction: these formulas use left trivialization g^{-1}delta g. The substantive transversality calculation is correct. There is no demonstrated global return/coding property.

I did not independently source-verify the Arnoux–Schmidt suspension representatives and roof/domain in that report; acceptance of those quoted standard-model details remains conditional on the researcher's source check. This does not affect the independently established arithmetic or geometric partial results, nor the no-resolution verdict.
