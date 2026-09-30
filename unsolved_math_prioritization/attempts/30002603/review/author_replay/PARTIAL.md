# A summable discrepancy-tail criterion for linear shape edges

**Status: partial result; the original problem remains unresolved (1/5 approaches). Independent adversarial review pending.** This note adapts the loop-removal argument of Bakhtin–Khanin–Mészáros–Voltz (BKMV), retaining its entropy estimate instead of replacing it by a power. It makes no priority claim.

The conclusion below covers some logarithmically vanishing spatial densities in the fair-sign model. It does not answer the original question for every mean-zero temporal law, and it does not settle even the uniform spatial-density case.

## 1. Original question and credited source relationship

The [original OWR contribution](https://ems.press/content/serial-article-files/46518), printed pp.1542–1543, uses lazy paths on the integers, minimum action, and a product potential V(x,i)=F(x)b(i). The two fields are independent and each is iid. The density assumption is stated for the product potential, with compact support and positive density in the interior; the temporal variable is required to have mean zero. The source also describes a corner at zero, so its proposed linear segment near zero is interpreted as a one-sided segment with endpoint zero, rather than an affine function across the corner.

[BKMV, arXiv:2310.08379v2](https://arxiv.org/abs/2310.08379v2), Theorem 2.4, proves the linear-edge conclusion for fair temporal signs and an even continuous spatial density whose endpoint asymptotic is q u^κ with κ>0. Remark 2.5 explicitly leaves other exponents outside that theorem. Its Section 4 supplies the discrepancy ordering and loop-removal mechanism used here. The source is listed as accepted/in press by an author and an institutional repository; this audit uses the complete v2 text, not an independently checked final journal version.

The proof below retains that mechanism and substitutes a general summability hypothesis. The shape-existence argument is the bounded-environment argument of BKMV Section 3 and Appendix A, with its hypotheses checked below. Neither the mechanism nor the power-law special case is presented as a discovery.

## 2. Statement

Let c>0. Let (F(x)) for x in Z be iid with an even density ρ continuous and positive on (−c,c), zero outside [−c,c], and with no endpoint atoms. Let (B(i)) for i≥1 be independent fair signs, independent of F. For integers T≥|z|, write

    A*(T,z) = min Σ(i=1 to T) B(i)F(γ(i)),

where γ(0)=0, γ(T)=z and |γ(i)−γ(i−1)|≤1. Define the concave shape Λ by

    A*(T,floor(αT))/T → −Λ(α),    −1≤α≤1.

The time-zero term in the original convention is the path-independent quantity B(0)F(0); it has no effect on this limit.

For a spatial realization f, put

    d_f(x) = 2c − f(x) + min{f(x−1), f(x), f(x+1)},
    p_k = P(d_F(0) ≤ 2c/k),    k≥1,
    S = Σ(k≥1) sqrt[p_k log(e/p_k)],

with a zero summand when p_k=0. We have 0≤d_f≤2c, hence p_1=1.

**Theorem.** If S<∞, then there are α_0>0 and K>0 such that

    Λ(α)=c−K|α|    for |α|≤α_0.

In particular, the theorem applies if, for some p>3/2 and finite C, the density satisfies

    ρ(c−u) ≤ C [log(ec/u)]^(−p)

for all sufficiently small positive u. The latter condition includes the normalized densities

    ρ_p(x) = Z_p^(−1) [log(ec/(c−|x|))]^(−p),   |x|<c,
    ρ_p(x) = 0,                                |x|≥c,

where Z_p is the positive finite normalizing integral. These densities vanish more slowly than every positive power at the support endpoints. The conclusion for them is therefore outside the positive-power hypothesis of the cited Theorem 2.4.

## 3. Shape facts needed in the proof

Under the bounded iid assumptions above, the shape exists, is deterministic, continuous, even and concave, with

    Λ(0)=c,    Λ(1)=Λ(−1)=0,
    Λ(α)≤c−(c−E|F(0)|)|α|.                         (1)

Here is why none of these facts needs a positive power-law endpoint assumption.

For an integer direction (t,x) with 0<|x|≤t, apply the subadditive ergodic theorem to minimum actions between (mt,mx) and (nt,nx). The field is stationary under this joint time/space shift. The shift is mixing: sufficiently separated translates of any finite cylinder depend on disjoint temporal and spatial coordinates. The actions are bounded in absolute value by c(n−m)t, so the integrability and lower-bound hypotheses hold. This gives a deterministic limit in that direction and convergence of the expectations. Subadditivity of the expected actions and integer rescaling give convexity and homogeneity on rational directions.

In the zero direction, almost surely some finite edge has one endpoint value at least c−ε and the other at most −c+ε. This follows from independence on disjoint edges and the positive endpoint-tail probabilities. A lazy path can reach that edge, choose its endpoint at each time according to B(i), and return to zero. Each step spent on the edge has action at most −c+ε; travel costs only a fixed number of steps. The universal lower bound −cT then proves the zero-direction limit −c. This argument does not assume ergodicity of the time-only shift with F held fixed.

The deterministic cone comparison

    A*(T_2,z_2) ≤ A*(T_1,z_1)+c(T_2−T_1)
    whenever T_2−T_1≥|z_2−z_1|

extends the rational directional limits to real interior directions by bracketing with nearby rational cones. The finite convex homogeneous function is continuous in the cone interior. Spatial reflection gives evenness. On the boundary rays the unique ballistic path has an iid, mean-zero action sequence, so the limit is zero.

Continuity up to these rays follows from the usual bounded entropy estimate. A path of length T ending at (1−ε)T has at most εT steps which are not East, so the number of such paths is at most exp[O(ε|log ε|)T]. For each fixed path, retain the first visit to each site 1 through (1−ε)T. The corresponding F-values and temporal signs are independent, bounded, and have mean zero. The remaining action is bounded below by −cεT. Hoeffding's inequality and the union bound therefore give

    Λ(1−ε) ≤ cε + O(c sqrt[ε|log ε|]) → 0.

Finally, the first-visit argument without probability gives

    A*(T,z) ≥ −Σ(j=1 to z)|F(j)|−c(T−z),    0≤z≤T.

The spatial strong law proves (1). In particular c−E|F(0)|>0.

We also need the following quenched expectation version. For almost every fixed f, simultaneously for every sequence T_n≥n with T_n/n→t≥1,

    E_B A*(B,f;T_n,n)/n → −tΛ(1/t).             (2)

Fubini gives the almost-sure conditional directional limits for all rational t on a common full-measure set of f. The function T↦A*(B,f;T,n)−cT is nonincreasing, since a path can be extended by staying at its endpoint. Squeezing T_n between rational multiples of n and using continuity gives the limit for every such sequence. Bounded convergence gives (2). Intersect this set of f with the spatial ergodic-theorem events

    #{1≤x≤n−1 : d_f(x)≤2c/k}/n → p_k           (3)

for every k≥1. The process d_F is a function of three adjacent iid coordinates and is ergodic. Fix one f in this intersection for the rest of the proof.

## 4. Uniform concentration retaining the entropy

Fix an integer ℓ≥2 and set N=ℓn. Let U_m be the subsets U of {1,…,N} of size at least n obtained by removing at most m+1 disjoint intervals, where 0≤m≤n. Write P_U b for the sign sequence retained in increasing order.

A subset is specified by at most m+1 pairs of interval endpoints. Padding with empty intervals, or counting all choices of start and end lists, gives

    #U_m ≤ (Σ(q=0 to m+1) binom(N+1,q))²
          ≤ (m+2)² [e(N+1)/(m+1)]^[2(m+1)].     (4)

The last bound uses that binom(N+1,q)≤[e(N+1)/q]^q and that the latter expression increases for q≤N+1. This slightly redundant bound avoids endpoint and empty-interval conventions.

Changing one temporal sign changes A* by at most 2c. For each deterministic U, McDiarmid's inequality therefore gives

    P(|A*(P_U B,f;|U|,n)−E_B A*(B,f;|U|,n)|≥a)
        ≤ 2 exp[−a²/(2c²N)].                  (5)

For q=m+1 define

    a_n(m)=2c sqrt{N[q log(e(N+1)/q)+4 log(N+1)]}.

Using (4), (5) and a union bound over all m, the probability of any failure of the two-sided bound with a=a_n(m) is at most

    2(n+1)(N+1)^(−6),

which tends to zero. Indeed the exponential cancels the endpoint count, while (m+2)²≤(N+1)². This also handles m=0; no zero error bound is asserted in that case.

For m_n/n→δ in [0,1],

    a_n(m_n)/n → E_ℓ(δ),
    E_ℓ(δ)=2c sqrt[ℓδ log(eℓ/δ)],   E_ℓ(0)=0.  (6)

The function E_ℓ is increasing on [0,1]. Unlike a replacement by a fractional power of δ, this bound preserves the logarithmic borderline.

We can consequently choose a deterministic sign sequence b_n of length N for each sufficiently large n such that all the above two-sided bounds hold, and also

    A*(b_n,f;N,n)/n → −ℓΛ(1/ℓ),               (7)
    #{1≤j<N : b_n(j)=−1, b_n(j+1)=+1}≥N/5.    (8)

For (7), combine (2) with (5) for the full interval, for instance using error n^(3/4). For (8), use the strong law for adjacent sign pairs. The intersection of these three events has probability tending to one, so the deterministic choice exists.

## 5. Loop deletion, with the needed inequality explicit

Take an optimal lazy path γ for (b_n,f;N,n). Order the spatial sites as v_0=0, v_1=n, followed by v_2,…,v_n, the interior sites in nondecreasing order of d_f. Ties may be resolved by the site coordinate. Initially retain U_(−1)={1,…,N}, together with time zero as the fixed starting point.

At stage i, let a_i and z_i be the first and last retained times at which the path is at v_i, allowing time zero. Remove L_i=U_(i−1)∩(a_i,z_i], and retain U_i=U_(i−1)\L_i. An empty L_i is allowed. The compressed path remains lazy from 0 to n: a removed piece starts and ends at the same site.

After the first two stages the remaining path is confined to [0,n]. At every later stage it visits each previously processed site exactly once. Its first-to-last-v_i segment cannot pass such a different site and return, because a one-dimensional nearest-neighbour lazy path would then visit that site twice. It follows inductively that L_i contains no earlier removed interval, hence is an interval in the original time order. It also contains no earlier processed spatial site. All L_i are disjoint, U_m is in U_m as defined above, and |U_m|≥n. At the final stage U_n has exactly n retained positive times, one at each site 1,…,n.

Let e_i count adjacent pairs (j,j+1) contained in L_i with signs (−1,+1), and let s_i be the action summed over L_i. Always s_i≥−c|L_i|. For i≥2,

    s_i ≥ −c|L_i|+e_i d_f(v_i).                (9)

Indeed such sign pairs do not overlap each other. For each pair, putting x=γ(j) and y=γ(j+1), we have

    −f(x)+f(y) ≥ −2c+d_f(x) ≥ −2c+d_f(v_i),

because y is x or an adjacent site and every visited site in L_i is unprocessed. All other terms are at least −c.

Every sign pair not contained in some L_i crosses a boundary in the ordered partition consisting of the at most n+1 nonempty intervals L_i and the n retained singleton times. Therefore at most 2(n+1) pairs are missed, and

    Σ(i=0 to n)e_i ≥ N/5−2(n+1).               (10)

Deleting the first m+1 loops gives an admissible compressed path and the inequality

    A*(P_(U_m)b_n,f;|U_m|,n)
      ≤ A*(b_n,f;N,n)+c(N−|U_m|)
          −Σ(i=2 to m)e_i d_f(v_i).           (11)

We only use this upper bound. The compressed path is not asserted to remain optimal, and no equality of minimum actions is needed.

## 6. Cost bound and summation over discrepancy levels

Put S_n(m)=Σ(i=2 to m)e_i d_f(v_i), interpreted as zero when m<2. If m_n/n has limsup δ, then

    limsup S_n(m_n)/n ≤ E_ℓ(δ).                (12)

To prove this, pass along a subsequence realizing the limsup, and then a further subsequence on which m_n/n and |U_(m_n)|/n converge, say to δ'≤δ and t in [1,ℓ]. The lower side of the concentration bound and (11) imply, using (2), (6), (7),

    −tΛ(1/t)−E_ℓ(δ')
        ≤ −ℓΛ(1/ℓ)+c(ℓ−t)−limsup S_n(m_n)/n.

Concavity and Λ(0)=c give

    ℓΛ(1/ℓ)−c(ℓ−t) ≥ tΛ(1/t).

Rearrangement and monotonicity of E_ℓ prove (12).

For each k, let m_(n,k) be the last interior index with d_f(v_i)≤2c/k, or 1 if there is none. Thus m_(n,1)=n and (3) gives m_(n,k)/n→p_k. By (12),

    limsup S_n(m_(n,k))/n ≤ E_ℓ(p_k).           (13)

For 2≤k≤h, all indices m_(n,k)<i≤m_(n,k−1) have d_f(v_i)>2c/k. Hence, summing the weighted partial sums for g=1,…,h−1,

    Σ(g=1 to h−1) S_n(m_(n,g))
      ≥ Σ(k=2 to h) [2c(k−1)/k]
                       Σ(i=m_(n,k)+1 to m_(n,k−1))e_i
      ≥ c Σ(i=m_(n,h)+1 to n)e_i.

Consequently, for every fixed h,

    limsup [Σ(i=m_(n,h)+1 to n)e_i]/n ≤ M_ℓ,
    M_ℓ=(1/c)Σ(k≥1)E_ℓ(p_k).                 (14)

The hypothesis S<∞ makes this finite and gives the useful uniform growth bound

    M_ℓ ≤ 2 sqrt(ℓ)(1+sqrt(log ℓ)) S = o(ℓ),  (15)

by splitting log(eℓ/p)=log(e/p)+log ℓ and using sqrt(a+b)≤sqrt(a)+sqrt(b). Also S<∞ implies p_k→0.

Choose an integer ℓ so large that

    ℓ/5−3−(M_ℓ+1) > ℓ/6.

A diagonal choice h_n→∞ in (3) and (14) gives

    m_(n,h_n)/n→0,
    Σ(i=m_(n,h_n)+1 to n)e_i ≤ (M_ℓ+1)n

for all sufficiently large n. Together with (10), this implies

    Σ(i=0 to m_(n,h_n))e_i ≥ ℓn/6.

The removed length is at least this sum. Thus, with m_n=m_(n,h_n),

    n≤|U_(m_n)|≤5ℓn/6,    a_n(m_n)/n→0.       (16)

Pass to a subsequence on which |U_(m_n)|/n→t in [1,5ℓ/6]. The lower concentration bound, (11) with its nonnegative last sum omitted, and (2), (7) give

    tΛ(1/t) ≥ ℓΛ(1/ℓ)−c(ℓ−t).

Concavity gives the reverse inequality. Thus Λ achieves equality with the chord joining its values at 0 and 1/t at the strictly interior point 1/ℓ. A concave function with equality at an interior chord point is affine on the whole chord interval. It follows that Λ is affine on [0,1/ℓ]. By evenness it has the asserted form on [−1/ℓ,1/ℓ]. Its slope parameter satisfies K≥c−E|F(0)|>0 by (1). This proves the theorem.

## 7. Logarithmic-density corollary and the unresolved borderline

For 0<h≤c, the event d_F(0)≤h requires F(0)≥c−h and at least one neighbour at most −c+h. Independence therefore gives

    P(d_F(0)≤h) ≤ 2 P(F(0)≥c−h)P(F(0)≤−c+h). (17)

The signs in (17) follow directly from the definition d_f; evenness makes the two endpoint tails equal. Under the displayed logarithmic density bound, each tail is at most

    C h [log(ec/h)]^(−p),

because the integrand bound increases with u. Hence, for large k,

    p_k ≤ C_1 k^(−2)[log(ek)]^(−2p).

The function q↦sqrt[q log(e/q)] increases for 0≤q≤1. Substitution of this upper bound shows that its k-th summand is at most

    C_2 k^(−1)[log(ek)]^(1/2−p).

The series converges for p>3/2 by the integral test. The stated density family has a finite positive normalizer, is continuous and positive in the interior, and satisfies this bound. For every κ>0 its ratio to (c−|x|)^κ tends to infinity at the endpoints. This proves the corollary without fitting it into a positive-power assumption.

For a uniform spatial density, the discrepancy probability is of order k^(−2), so the summands here are of order sqrt(log k)/k and the sufficient criterion fails. Failure of this series condition is not proof that the shape lacks a linear edge. The original general mean-zero temporal law, the uniform-density case in the sign model, and other nonsummable discrepancy tails remain unresolved by this argument. The source's separate conjecture about failure near κ=−1 is not promoted to a theorem.

## 8. Verification and limits

The accompanying bounded exact controls check the loop partition, valid compressed paths, sign-pair cost inequality, admissible-path upper bound, discrepancy levels, and entropy endpoint counts. They do not establish an infinite-volume limit or infer a linear edge from numerical simulation. Those conclusions depend on the written proof above and the standard subadditive and concentration theorems with the hypotheses explicitly verified.

The general summability argument is an adaptation of BKMV Section 4, not an alternative independent mechanism. Its explicit two-sided concentration estimate includes m=0 and its action comparison only uses an admissible-path inequality. The full original target remains **unsolved, 1/5**. Priority for the logarithmic-tail refinement has not been established.
