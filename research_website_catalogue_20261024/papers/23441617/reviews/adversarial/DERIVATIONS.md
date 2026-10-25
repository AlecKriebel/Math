# Independent analytic derivations and exact negative controls

The mechanisms were fixed before primary bodies in the sealed early ledger. This expanded account verifies the complete original analytic implication, under its explicitly stated curve/density conventions. No finite mathematical computation substitutes for any step.

## D1. Quantifiers, conventions and finite-modulus reduction

E is an arbitrary compact subset of[0,1], F=R minus E and S2={|z|=2}. All connectors are continuous with the stated endpoint limits, locally rectifiable in the interior, with no prohibition on interior plate/axis contacts. Line integrals are increasing limits on interior compact subcurves; arclength counts multiplicity, constant portions have zero length, and an infinite endpoint value alone has zero mass. Densities are actual extended nonnegative Borel functions, not area-equivalence classes. The global-rectifiability variant uses that convention consistently in both families.

For empty E the circle family is empty and has modulus 0. Otherwise suppose the real-complement modulus is finite. The definition of an infimum then supplies SOME admissible finite-energy rho; it does not require an extremal density or attainment. If every admissible density had infinite energy, or there were none, the infimum would be infinite.

## D2. Pointwise finite-energy majorization, including infinity

On Q=[-2,3]×[-2,2] set h=rho² and A_k={h>2^k}. Relative outer regularity gives open O_k containing A_k with area(O_k)<=area(A_k)+2^(-2k-4). Define H=1+sum_(k>=0)2^(k+1)1_(O_k), g=sqrt(H). Open-set indicators and their increasing sums are lsc. If h<=1, H>=h. If2^K<h<=2^(K+1), the terms through K already dominate h; at dyadic equality the previous terms together with1 still suffice. If h=infinity, every term is present. Hence g>=rho at EVERY point.

For finite h, the corresponding dyadic sum is at most4h. Tonelli gives

    integral_Q g² <= area(Q)+4 integral_Q rho²+sum_(k>=0)2^(-k-3)
                 = area(Q)+4 integral_Q rho²+1/4 < infinity.

Thus g>=1 is an actual lsc majorant of finite energy, retaining all pointwise infinite values on their area-null set. No exceptional curves are lost through an a.e. replacement.

## D3. Weighted length is lsc and supplies compactness

For a continuous nonnegative weight a and rectifiable alpha, let S_P be the sum over a finite partition of minimum a along each subcurve times its chord length. Every S_P depends continuously on alpha under uniform convergence: a is uniformly continuous on compact Q, so both the minima and endpoint chords converge. Also S_P<=integral_alpha a ds.

To prove equality with the supremum, choose a coarse partition with weight oscillation at most epsilon on each piece, then refine it to make the sum of chord lengths within epsilon of the total variation L. The difference from weighted length is at most epsilon L+(max a)epsilon. Refinement preserves the oscillation bound. Thus integral_alpha a ds=sup_P S_P, making weighted length lsc under uniform convergence.

For lsc g use a_m(x)=min(m,inf_y(g(y)+m|x-y|)). These finite functions are m-Lipschitz (or constant m if the infimum is everywhere infinite), nonnegative and increasing in m. If their limit at x were below g(x), bounded near-minimizers would have |x-y_m|→0 and bounded g(y_m), contradicting lsc, also when g(x)=infinity. Hence a_m increases pointwise to g. Monotone convergence for the arclength measure gives integral_alpha g=sup_m integral_alpha a_m, which is lsc too. Multiplicity and constant portions are preserved by this measure.

Define d(z) by infimum of costs of globally rectifiable paths from compact E to z in Q. If z_j→z and liminf d(z_j)=L<infinity, choose near-minimal paths of costs<=d(z_j)+1/j along a subsequence. Because g>=1 their Euclidean lengths are bounded, including endpoints by continuity. Constant-speed parametrizations give a common Lipschitz bound on[0,1]. Ascoli supplies a uniform limit in compact Q, starting in E and ending at z. Its g-cost is at most L by the preceding lsc result, so d(z)<=L. This proves lsc without assuming minimizers or finite distances everywhere. Its truncation u=min(1,d) is lsc and Borel.

## D4. Exact plate values, all-path control and actual ACL trace

Concatenation with a rectifiable beta from x to y gives the distance inequalities when costs are finite. Reverse beta for the other direction and truncate to obtain |u(x)-u(y)|<=integral_beta g. If one distance is infinite and the other finite, any finite-cost beta would make both finite; thus the inequality still holds. If both are infinite their truncated values coincide.

For e in E, the constant auxiliary path has zero cost even if g(e)=infinity, so u(e)=0. Every auxiliary path to F∩Q is an original connector and has rho-cost>=1; pointwise majorization implies g-cost>=1, so u=1 there. These are actual point values obtained from admissibility on EVERY path, not a Sobolev representative altered on the axis.

By Fubini, g is integrable along almost every coordinate line in Q. On each good line the path inequality holds on every segment. Applied to disjoint intervals it gives absolute continuity of the actual u; its coordinate derivative is bounded by g a.e. Slice integration by parts and Fubini identify weak derivatives. Thus u is in W12(int Q), with |grad u|²<=2g² a.e.

Choose smooth eta compactly supported in int Q and equal1 near[0,1]×{0}. The actual w=eta(1-u), extended by zero, is compactly supported W12(R²). On almost every vertical line it is AC and its value at height0 equals1_E. Outside Q it is zero; inside Q off E, u=1. The exceptional set of vertical lines has one-dimensional measure0. No capacity or EVERY-endpoint conclusion is inferred from that exception set.

## D5. Critical trace with exact normalization and zero frequency

For smooth compactly supported w, use the unitary horizontal transform with kernel exp(-ix xi), W(xi,y). The derivative of |W|² integrated over y>0 gives

    |xi||W(xi,0)|² <=2|xi| integral |W||Wy|
                  <= integral (xi²|W|²+|Wy|²).

No division by xi occurs; xi=0 is harmless. Plancherel and integration in xi yield

    integral |xi||fhat(xi)|² <= integral_(y>0)|grad w|².

For a compactly supported ACL vertical slice v, FTC and2ab<=a²+b² give |v(x,0)|²<=integral_(y>0)(|v|²+|vy|²). Smooth mollification w_j→w in W12, applied to v=w_j-w and integrated in x, therefore makes the actual traces converge in L2. Fourier L2 convergence has an a.e. convergent subsequence; Fatou extends the preceding weighted inequality to w. The supports vanish far up the slices, justifying the FTC endpoint at infinity.

Plancherel and Tonelli now give

    integral_R ||f(.+h)-f||²_2 dh/h²
       = C integral_R |xi||fhat(xi)|²,
    C=integral_R |exp(it)-1|² dt/t² in(0,infinity).

C is finite since the integrand is bounded near0 and at most4/t² away from0; it is positive. Negative xi produces the same |xi| after substitution, and the zero-frequency contribution is0. Thus the translation seminorm is finite.

## D6. Characteristic-function rigidity is an all-scale deduction

For f=1_E and0<h<1 choose N=ceil(2/h)<=3/h. The supports of f(.+Nh) and f are disjoint because Nh>=2 and E⊂[0,1]. Translation invariance and telescoping yield

    2 length(E)=||f(.+Nh)-f||_1 <=N||f(.+h)-f||_1.

Characteristic differences have squared absolute value equal to their absolute value. Consequently ||f(.+h)-f||²_2>=2 length(E)h/3 for EVERY0<h<1. If length(E)>0, integrating against h^-2 gives a logarithmic divergence, contradicting D5. Hence any finite-energy real-complement separator forces length(E)=0, including for positive-length compacts with empty interior. This proves no capacity conclusion for null sets; D7–D9 are essential.

## D7. Every-endpoint circle selection, with the radial factor correct

Set q=rho+1_(B(0,3)). It is actual Borel, still admissible and finite-energy, since q²<=2rho²+2 1_(B(0,3)). Fix ANY e in null E. Its circle energy A_e(r)=integral_(|z-e|=r)q² ds satisfies

    integral_0^delta A_e(r)dr = integral_(B(e,delta))q² dA < infinity.

The arclength definition already contains the factor r; no additional radial weight is inserted in this identity. For THIS e, translation of the null set E implies e+r is in F for a.e. r>0. The set of r with this property and finite A_e has full measure.

For every epsilon,delta>0 there is such a good r<delta with rA_e(r)<epsilon. Otherwise A_e(r)>=epsilon/r on a full-measure interval and its integral would diverge. Recursively require r_j<min(1,r_(j-1)/2,1/j) and r_j A_e(r_j)<1/j. This supplies the sequence for every fixed e. No exceptional endpoint set is removed; a simultaneous sequence for all e is neither assumed nor needed.

The full-circle q-cost is at most sqrt(2pi r_j A_e(r_j))→0 by Cauchy–Schwarz. Its scale is dimensionless, as required for planar2-modulus.

## D8. Infinite endpoint length, retracing and first exits

Suppose a connector from e to S2 has finite q-cost. Stop at its first hit of S2. This exists by continuity and is at positive parameter time; its preceding image lies in B(0,2), where q>=1. Every compact interior subcurve has length bounded by the finite cost. Approximating partition endpoints by interior parameters and using continuity shows the full stopped curve has finite variation, including its initial endpoint.

Reparametrize by arclength on[0,L], removing constant portions while preserving order and multiplicity. The resulting curve is unit-speed a.e. and nonconstant on every initial interval of positive length. Its q integral equals the original increasing interior-subcurve integral, since endpoints have zero arclength measure. Hence q composed with the parametrized curve is integrable.

Its terminal distance from e is at least1. Let t_j be first hit of radius r_j. For every t>0 some point in[0,t] differs from e; every sufficiently small disk is exited before that point. Thus t_j→0, even with returns, winding and retracing. Absolute continuity of the finite cost integral makes the initial q-cost tend to0.

Append a circular arc from the first-exit point to the actual real point e+r_j in F. Its cost is bounded by the full-circle cost from D7. The concatenation is a genuine globally rectifiable E-to-F connector; interior plate contacts are permitted. For large j its q-cost is<1, contradicting admissibility. Thus EVERY E-to-S2 connector has infinite q-cost. The same proof works for the consistently globally rectifiable convention; the finite-cost reduction also handles initially only locally rectifiable curves.

## D9. Scaling completes the whole theorem

For each positive integer n, q/n has infinite integral on EVERY E-to-S2 connector, so is admissible without removing exceptional curves. Its area energy is n^-2 times a finite number. Thus Mod2 Gamma(E,S2)=0. Together with D1 this proves the exact contrapositive and the complete original implication.

The normalization E⊂[0,1] gives dist(E,S2)>=1. The ball indicator1_(B(0,2)) already gives a finite upper bound4pi on modulus to S2: every connector's initial portion to its first hit has length>=1. Similarities z↦a+lambda z preserve planar2-modulus under density rho_lambda=lambda^-1 rho((z-a)/lambda); area and density-square scaling cancel. The proof only needs the stated normalization and does not claim a new exponent/domain theorem.

## D10. Exact singleton and endpoint-value controls

For E={0}, define rho(z)=1/(|z|log(1/|z|)) when0<|z|<exp(-1), zero outside, with any value (including infinity) at0. Polar integration gives energy2pi integral_1^infinity t^-2 dt=2pi. Every nonconstant connector from0 to a nonzero endpoint has infinite cost. One precise all-curve verification uses truncated radial potentials

    v_K(r)=min(K,max(0,log(log(1/r)))) for r<exp(-1),
    v_K=0 outside, v_K(0)=K.

For fixed K this is a globally Lipschitz radial function with gradient norm<=rho a.e. and the corresponding path bound on each rectifiable interior subcurve. At its finitely many radial corners, an AC radius has derivative0 a.e. on a level set, so the same chain-rule bound holds. Take limits to the connector endpoints. The cost is at least K-v_K(|z_end|), which diverges as K→infinity. This proof uses all curves, not only radial segments. Scaling rho/n gives zero modulus to both the real complement and S2, illustrating why nonempty E cannot replace the positive-modulus hypothesis.

By contrast, the density infinite only at0 and zero elsewhere has zero integral on the straight segment from0 to1. Endpoint infinity alone is inadmissible, agreeing with the note's convention. Null length is not identified with zero conformal capacity anywhere in the proof; the every-endpoint argument treats any remaining null compact, including those to which a positive-modulus premise applies.

## D11. Findings and exact limits

Theorem 1 and Lemmas 1–5 survive independent reconstruction under both stated consistent curve conventions. Every null-set endpoint and every connector remains in the quantifiers. Classical trace/upper-gradient/compact-condenser sources support the acknowledged context, while the direct proof does not import a touching-plate capacity identity. No mathematical computation or finite grid was used.

There is one separate minor bibliographic error: reference [4], controlling TeX line 442 and PDF 7, gives Acta Math. 180. The actual Heinonen–Koskela first page and official publisher record for its correct DOI both give181(1998),1–61. This does not change the argument, and no source repair was made. Historical priority/current openness remain unknown; a 1982 program title is not a resolution body, and the full 2019 problem page remains unavailable.
