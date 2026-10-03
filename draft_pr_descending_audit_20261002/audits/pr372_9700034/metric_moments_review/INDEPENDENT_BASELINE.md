# Independent source-first baseline

Sealed before any candidate TURN, proof, code, receipt, root audit, or sibling audit was read. Primary PDFs were freshly downloaded; the relevant displayed formulas were rendered and inspected. This document contains original audit derivations, not copied source excerpts.

## Exact target and universal finite controls

Aldous's 2012 long version, PDF page 50, Open Problem 34, becomes the 2014 published version, PDF page 38, Open Problem 8. The target is finite expectation of M = sup_i len R(0,U_i), with iid uniform points in the unit disc independent of the network. Length means Euclidean arclength. It does not mean the minimum travel-time metric of a construction. The question expressly permits identifying additional assumptions; it does not assert that all SIRSNs have the property.

Aldous's axioms impose route compatibility, finite feasible routes, similarity invariance of finite-dimensional distributions, measurability, finite E D_1, and finite major-road intensity p(1). None of these assumptions explicitly supplies an integrable uniform route-length envelope. For a single independent uniform U, invariance and scaling give E len R(0,U) = (2/3) E D_1. Consequently E max_{i<=n} len R(0,U_i) <= (2n/3) E D_1. This is a finite-n bound only. In the jointly measurable environment representation, conditional iid sampling gives sup_i L(omega,U_i) = ess sup_u L(omega,u) almost surely. Thus the exact missing condition is integrability of this conditional essential supremum. A scalar function with an integrable singularity can have infinite essential supremum; this illustrates the quantifier gap but is not a SIRSN counterexample.

The major-road intensity identity bounds expected truncated-road length within a fixed bounded region. It does not by itself confine complete routes, control near-endpoint portions uniformly, or interchange a countable sampled union with an all-point union. A source theorem about a fixed deterministic endpoint pair cannot be used as an all-pair theorem. Countable iid pairs permit countable intersection after conditioning/Fubini; exceptional environment-dependent destinations do not follow from such an argument.

## Poisson-line model and usable dependencies

For dimension d>=2 and gamma>d, write q=gamma-1 and a=gamma-d>0. The marked-line intensity is mu_d(dl) q v^(-q-1) dv. If V_r is the largest speed of a line hitting B(0,r), then

P(V_r <= v) = exp(-c_d r^(d-1) v^(-q)).

Thus E V_r^p is finite exactly for 0<p<q; all inverse-speed moments exist. Euclidean lengths scale linearly, speeds with exponent (d-1)/q, and travel times with exponent a/q. A uniform travel-time bound is still not a uniform Euclidean-length bound without an additional path confinement or multiscale argument.

Kahn 2016 Theorem 3.1 is a uniform bound over all x,y in a deterministic precompact connected region, using only lines hitting a specified widening and avoiding a forbidden set with sufficiently small solid angle. With no forbidden set, it yields a common random variable T_B bounding all travel times in a ball and a tail P(T_B>t)<=C exp(-c t^q). It supplies finite polynomial moments of every order. Kendall's foundational Theorem 2.6 supplies pathwise confinement of all paths of a fixed duration begun in a compact set, and Theorem 3.6 supplies simultaneous finite-time connectivity; planar uniqueness Theorem 4.4 is stated for each specified pair almost surely, not simultaneous uniqueness of all pairs. Kahn's Theorem 5.1 is stated for one specified pair. Its proof has a mechanism that can be applied to a common time envelope, but the extension must be proved.

## Independent uniform Euclidean-length derivation

Every admissible path from 0 whose total arclength exceeds r spends at least arclength r in B(0,r): either it exits the ball, requiring this much arclength before its first exit, or its entire path remains in the ball. Its total time therefore exceeds or equals r/V_r. This observation applies simultaneously to all paths, and needs no uniqueness of geodesics.

Let M be the supremum of lengths of any collection of minimum-time routes from 0 to destinations in B(0,1). On the common event T_B<=t, M>r implies V_r>=r/t. A one-radius union bound gives P(M>r)<=C exp(-c t^q)+c_d r^(-a)t^q. Optimizing with t of order (log r)^(1/q) proves E M^p<infinity for p<a only. In dimension two it proves the desired mean only for gamma>3. The boundary gamma=3 is not settled by this bound.

A stronger multiscale proof uses the actual nested-ball dependence rather than a fictitious independence of V_r values. Set r_j=2^j r_0 and v_j=r_j/t. Let H_m be the event V_{r_j}>=v_j for every 0<=j<=m. On H_m, greedily list 0=l_0<...<l_k<=m by recording the first threshold above V_{r_{l_i}}, with l_{k+1}=m+1. For each nonterminal record,

v_{l_{i+1}-1} <= V_{r_{l_i}} < v_{l_{i+1}},

and the final record satisfies V_{r_{l_k}}>=v_m. For i>=1, conditional on the preceding record events, the threshold v_{l_{i+1}-1} cannot be attained by a line hitting B(0,r_{l_{i-1}}). The qualifying line must lie in the disjoint marked-line-space increment [B(0,r_{l_i})] minus [B(0,r_{l_{i-1}})]. Poisson independence applies to this increment and the previous filtration. Therefore each record factor is bounded by

2^(-q(l_{i+1}-l_i)) p_0, where p_0=2^q c_d r_0^(-a)t^q.

The same bound holds for the first record directly. Summing over the binomially many compositions yields

P(H_m) <= 2^(-q(m+1)) p_0(1+p_0)^m <= [2^(-q)(1+p_0)]^(m+1).

Crucially, the event inclusion gives P(M>r_m, T_B<=t)<=P(H_m). It does NOT give P(M>r_m | T_B<=t)<=P(H_m). No independence from T_B is assumed.

Choose 0<kappa<q, p_0=2^(q-kappa)-1, and r_0(t)=[2^q c_d t^q/p_0]^(1/a). Choose t_n=C(n+1)^(1/q) with P(T_B>t_n)<=2^(-(n+1)), and m_n=floor((n+1)/kappa). The preceding joint-event estimate gives

P(M>R_n)<=2^(-n), with R_n<=C_kappa 2^((n+1)/kappa)(n+1)^(1/a).

Since sum_n 2^(-n) R_n^p converges for 0<p<kappa, E M^p<infinity for every 0<p<q=gamma-1. In dimension two gamma>2, choose p=1<q. This verifies the desired expected supremum for this Poisson-line construction throughout its parameter range, conditional only on its common uniform time-envelope theorem and measurability of the sampled routes. It does not prove the assertion for every SIRSN, nor a failure example for another SIRSN.

## Source printing and proof corrections observed visually

Kahn PDF page 9 equation (2) prints T(g)=sum_l v(l)L_g(l), incompatible with its preceding identity L_g(l)=v(l)T_g(l). The correct expression is sum_l L_g(l)/v(l). PDF page 12 has reversed inequality signs in the cone/line-measure lower-bound chain. The angle bound must provide a positive lower bound on the available hitting-line measure. PDF page 13 gives a speed-threshold constant that does not cancel as printed, and its exponential-moment integration/threshold has an incorrect exponent on the constant. The usable tail (3) implies E exp(delta T_B^q)<infinity for delta<C^(-q). The exact value printed for delta is not needed. PDF pages 26-27 equations (18),(21),(22) use a conditional probability without dividing by the conditioning-event probability. Replacing it with the joint probability and subsequently adding P(T_B>t) repairs the length mechanism. These are source errors, not evidence that the asserted qualitative model theorems are false. General-dimensional cone normalization also deserves independent geometric treatment; only existence of a positive scale-correct two-ball hitting measure is needed here.

## Status

Strongest independently verified scoped result: the multiscale Poisson-record argument, with joint events, extends a common stretched-exponential travel-time envelope to uniform Euclidean-route-length moments p<gamma-1, hence an integrable sampled maximum for planar gamma>2. Exact universal gap: the SIRSN axioms alone have not furnished such an envelope or a counterexample. No candidate claim has yet been read. No computation establishes any of these quantifier claims.
