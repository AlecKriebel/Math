# First-turn checkpoint — k403,a

**Unreviewed candidate mechanism, one substantive author turn in progress.** No result PR or QUEUE promotion. The target is the unprimed origin-pedal times origin-antipedal signed area for odd primitive ellipse-caustic billiard periods. Both source editions agree (arXiv v11 Table5 p7; final Table5 p348). All exact-ID/prior-PR/branch/main-attempt history checks are empty. Upstream triage is not a prior campaign attempt.

## New antipedal mechanism

For real nonzero consecutive vertex normals P,Q, put h(P)=P dot P and

F(P,Q)=[h(P)h(Q)−(h(P)+h(Q))(P dot Q)/2]/det(P,Q).

The origin-antipedal line at P is P dot X=h(P). Its polygon's signed area is the cyclic sum of F(P_i,P_(i+1)); this follows from the support-line area identity and will be verified against direct line intersections. In complex continuation dot products are bilinear, not Hermitian.

Use Stachel's canonical coordinates P(w)=(-a sn w,b cn w), delta=2v=4K tau/N, a=alpha dn v/cn v,b=beta/cn v, modulus k=sqrt(alpha²−beta²)/alpha. Let p=iK' and ell=2K/N for odd N. Then v=tau ell.

A critical distinction: the cross-product denominator vanishes at two different complex midpoint types. With u=w+v,

det(P(u−v),P(u+v))=2ab sn(v)cn(v)dn(u)/(1−k²sn²(v)sn²(u)).

At u=K+p and its translates, the endpoints coincide; the numerator has a quadratic zero in their difference, so the apparent simple denominator zero is removable. At u=p and its translates, the endpoints are opposite, not equal; those are genuine possible simple poles. They cannot be discarded. The quotient real-period identification v=tau ell places these midpoint-pole classes at the same two classes p,3p as the vertex poles when N is odd. For even N the classes need not coincide; a direct four-periodic check disproves an unqualified all-parity area-ratio extension.

At a vertex pole w=p, P(p+z) is odd in z. A single incident F term has at most a double pole because its numerator has order at most three and its denominator a simple pole. The two incident terms are H(z)−H(−z), using F(-P,-Q)=F(P,Q), F(Q,P)=-F(P,Q), and P(p−delta+z)=-P(p+delta−z). Thus the double Laurent coefficient cancels and the cyclic area has at most a simple pole. Neighbor coordinates are regular because0<delta<2K.

The cyclic antipedal area is ell-periodic and anti-periodic under2iK': simultaneous P->diag(1,-1)P reverses every determinant while preserving dot products. It has only the two permitted simple pole classes p,3p on C/(ell Z+4iK' Z). The nonzero cyclic sum S(w)=sum_j dn(w+jdelta) has exactly those poles and the same character. Matching one residue and using compactness/anti-periodicity gives A*_O(w)=c_* S(w), with c_* possibly zero.

## Pedal factor and conclusion to be fully packaged

The origin foot on the caustic-tangent chord at midphase u is

Q(u)=(-alpha k'^2 sn(u)/dn²(u), beta cn(u)/dn²(u)).

The already reviewed campaign origin-pedal proof (5100012, PR204) supplies a credited mechanism that will be restated self-contained: its cyclic signed area has at most simple poles at K+p, K+3p. Apparent double poles cancel between incident area terms because Q is even about K+p. Periodicity and the same anti-period force T(u)=c_p S(u+K). Actual pedal area uses u=w+v.

S is even and has precisely two simple poles. Its two zeros are p+ell/2 and3p+ell/2; hence S(w)S(w+ell/2) is constant. Since K+v is a half-integer multiple ofell for odd N, A_O(w)A*_O(w)=c_p c_* S(w+ell/2)S(w) is constant.

For real phases all consecutive P determinants are positive by the explicit chord identity (strict elliptical caustic,0<v<K), so every antipedal intersection is finite and unique. Origin projections are always defined. Vanishing signed areas cause no division in the asserted product. Circle families require a separate elementary regular-star calculation or justified limit; no hyperbolic/collapsed caustic extension is intended.

## Current checks and remaining packaging

Exploratory40-digit direct line-intersection diagnostics for odd periods3,5,7,9 support the ratio and product; these are not proof or a certified exact checker. The N4 diagnostic correctly rejects the overbroad all-parity statement and exposed the essential opposite-endpoint pole class above. Next: formal support-line identity, exact lattice/pole bookkeeping controls, independent direct geometric diagnostics for primitive stars and circular boundary case, source manifest and full proof, then separate adversarial review. No historical novelty claim; source Jacobi/elliptic and previous campaign mechanisms credited.
