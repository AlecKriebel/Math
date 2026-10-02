# Turn 5: a genuine slow diagonal consequence and the logarithmic-window obstruction

**Substantive author turn 5 of 5. Original unresolved; the author budget is exhausted.** The final attempt asks what follows from the fixed-reflection results actually available, without imposing a new uniform spectral theorem. A slowly growing simultaneous-limit statement for actual density moduli does follow on illuminated compact sets. The phase and growth qualifications are indispensable.

## 1. Inputs retained from the primary fixed-iteration framework

Fix the two-dimensional source's periodic itinerary of period n and one residue class of return obstacles. Retain its geometric, visibility, no-occlusion and fixed-iteration expansion assumptions, including its explicitly stated Assumption C. Let E be a fixed compact subset strictly inside the stabilized illuminated region. Choose an initial reflection index m_0 in the chosen residue class sufficiently large that all subsequent returns are illuminated on E, with incidence factors bounded away from zero there. Write m_j=m_0+nj.

The source's fixed-iteration expansion and optical factors give, for each fixed j,

    eta_(m_j)(x,k)=2ik (−1)^(m_j) exp(ik phi_(m_j)(x))
                         a_j(x)[1+e_j(x,k)],                 (1)
    sup_E |e_j(x,k)|=O_j(k^(−1)),

where a_j is the real nonzero optical amplitude beta_(m_j) gamma_(m_j). Its sign is the same throughout this illuminated return class; only ratios of these amplitudes will be used. The source's beta-ratio estimate and convergence of gamma to a nonzero limiting incidence factor imply, for constants C_a and 0<theta<1,

    b_j(x):=a_(j+1)(x)/a_j(x)>0,
    sup_E |b_j−q|≤C_a theta^j,
    sup_(j,x) b_j≤Q<infinity,
    q=product_(r=0)^(n−1) L_r^(−1/2)>0.                     (2)

One may enlarge constants to cover the finitely many initial j. To see the amplitude step explicitly, the source bounds beta_(m+n)/beta_m−q geometrically and gamma_(m+n)−gamma_m geometrically. Dividing the latter by |gamma_m|≥c_E and multiplying the two ratios proves (2). This division would fail without the illuminated compact-set restriction.

The ray phase also satisfies

    sup_E |phi_(m_(j+1))−phi_(m_j)−Phi_n|≤C_phi theta^j,      (3)

after enlarging theta if necessary. These inputs are credited to Ecevit–Reitich's fixed-iteration and dispersing-ray analysis, as identified in SOURCE_GATE.md. In the earlier primary manuscript they are Theorem 3.1 with Corollary 3.3, Theorem 4.7 and Lemmas 4.6/4.12; the published numbering differs. The argument below is an elementary consequence, not a new derivation of their PDE expansion. For n=2, q is the recurrence-defined corrected number from Turn 1, not the incompatible printed shortcut.

## 2. Slow diagonal window for actual densities

Define the exactly ray-phase-corrected quotient

    Y_j(x,k)=(−1)^n exp(−ik[phi_(m_(j+1))−phi_(m_j)])
                           eta_(m_(j+1))(x,k)/eta_(m_j)(x,k).

Whenever |e_j|,|e_(j+1)|≤epsilon≤1/2, (1) gives a nonzero denominator and the exact identity

    Y_j=b_j(1+e_(j+1))/(1+e_j).

Therefore

    sup_E |Y_j−q|≤C_a theta^j+4Q epsilon.                    (4)

There exists a nondecreasing integer function L(k)→infinity such that, uniformly for integers L(k)≤j≤2L(k),

    sup_E |Y_j(x,k)−q| -> 0,
    sup_E | |eta_(m_(j+1))(x,k)|/|eta_(m_j)(x,k)|−q | -> 0.  (5)

All denominators in (5) are nonzero for sufficiently large k.

**Proof with the quantifiers made explicit.** For each integer l≥1, the finitely many fixed-iteration estimates for 0≤j≤2l+1 permit a frequency threshold K_l such that

    k≥K_l implies max_(0≤j≤2l+1) sup_E|e_j(x,k)|≤1/(l+2).

Choose the K_l strictly increasing and tending to infinity. For k≥K_1 let
L(k)=max{l:K_l≤k}. Then on L(k)≤j≤2L(k), equation (4) bounds the error by

    C_a theta^(L(k))+4Q/(L(k)+2),

which tends to zero. Taking absolute values cannot increase the distance from the positive number q, so the second assertion in (5) follows from the first. This proves the joint window for the actual densities under the source inputs, with no uniform-in-j bound on e_j silently assumed. QED.

The thresholds can be made as large as desired. In particular, given any prescribed nondecreasing G(k)→infinity, they may be chosen so that L(k)≤G(k) for all sufficiently large k: enlarge K_l until G(K_l)≥l. They may also be required to satisfy K_l≥exp(l²), giving L(k)≤sqrt(log k). This is an existence statement about some slowly increasing window. It supplies no computable lower growth rate, no prescribed logarithmic window, and no estimate for all larger reflection counts. It does not mean every slowly increasing function works.

It also proves the corresponding iterated limit of density moduli (first k→infinity at fixed j, then j→infinity). This familiar diagonal/iterated-limit reasoning is not claimed as a new general principle.

## 3. Why the limiting periodic phase is still missing

The original complex optical multiplier is

    R_(n,k)=(−1)^n exp(ik Phi_n) q.

Replacing the exact phase in Y_j by Phi_n costs, from (3), at most
q C_phi k theta^j. The diagonal construction gives no guarantee that this tends to zero. Indeed it can be chosen with L(k)≤sqrt(log k), whereas the available bound requires a reflection index exceeding a constant times log k. A diverging upper error bound is not a proof of failure for actual phases; it is a proof that this estimate alone has not justified the replacement.

Thus (5) is a valid actual-density modulus result and exact-ray-phase result, but it is weaker than a periodic-phase complex quotient estimate and weaker than uniform convergence at all sufficiently many reflections. It does not establish the global boundary statement, shadow transitions, or a prescribed rate in k.

## 4. A quantitative compatibility test for finite-window remainder growth

One can identify an intermediate missing estimate between fixed-j asymptotics and complete uniform control. Suppose, additionally, that for some sigma≥0 and all j≥0,

    sup_E |e_j(x,k)|≤C_e exp(sigma j)/k
          whenever k≥K_0 exp(sigma j).                      (6)

This is a new sufficient assumption, not a bound proved for the actual PDE here. Let a=−log theta>0. If sigma<a, choose

    c=2/(a+sigma),      tau=(a−sigma)/(a+sigma)>0,
    j(k)=ceil(c log k).

For all sufficiently large k, (6) applies to j(k) and j(k)+1 because
k exp(−sigma[j(k)+1])≥exp(−2sigma)k^tau→infinity. It makes both remainders less than 1/2. Equations (1)–(3) then yield

    sup_E |eta_(m_(j+1))/eta_(m_j)−R_(n,k)|=O(k^(−tau)).     (7)

To verify the exponent, the three errors are bounded by constant multiples of

    theta^j,             exp(sigma j)/k,             k theta^j.

With this choice of c their last two exponents are both −tau; the first decays faster. More explicitly the ratio-remainder term is at most
2Q C_e(1+exp sigma)exp(sigma j)/k, and the periodic phase term is at most q C_phi k theta^j. This proves (7), including the denominator control.

If sigma=0, the result gives tau=1, consistent with the uniform O(1/k) remainder route. If sigma≥a, no c can simultaneously make a c>1 and sigma c<1. That is a limitation of this growth-envelope argument, not a necessity theorem ruling out cancellation or a better physical estimate. The source fixed-iteration statement supplies no bound on sigma, or even a finite exponential envelope.

## 5. Compactness and all-orders finite-iteration agreement still do not fill the gap

The following exact model strengthens the warning from Turn 1. It is an abstract compact-operator family, not a Helmholtz counterexample.

Fix 0<rho<sigma<1, and for real k≥e put L=L_k=max(1,floor(sqrt(log k))). On the fixed Banach space l-infinity(N_0), define

    (T_k f)(j)=sigma f(j+1)       for 0≤j<L,
    (T_k f)(L)=sigma f(L),
    (T_k f)(j)=0                 for j>L.

This operator is positive, has finite rank L+1, is compact, and has norm exactly sigma independent of k. Its spectrum is {0,sigma}, with sigma algebraically simple. Take input

    f_k(j)=(rho/sigma)^j       for 0≤j≤L,
    f_k(j)=0                 for j>L,

of norm one, and observe coordinate zero. Direct iteration gives

    u_m(k)=(T_k^m f_k)(0)
          =rho^m                         if 0≤m≤L,
          =rho^L sigma^(m−L)             if m≥L.             (8)

For every fixed m, u_m(k)=rho^m for all sufficiently large k. Hence its fixed-m asymptotic expansion agrees with the optical sequence to every algebraic order, with eventual exact equality. Also

    0<u_m(k)≤sigma^m,       sum_(m≥0)u_m(k)≤1/(1−sigma)

uniformly in k. Nevertheless

    u_(m+1)(k)/u_m(k)=rho for m<L,
    u_(m+1)(k)/u_m(k)=sigma for m≥L.

For every fixed c>0, all m≥c log k eventually lie in the second regime. Thus all-orders fixed-iteration agreement, compactness at every frequency, positivity and uniform contraction/summability still do not certify a logarithmic window carrying the optical multiplier.

The family has a frequency-dependent finite-dimensional transient. Its full operator dependence is piecewise in k and is not asserted to be holomorphic or a physical boundary map. Each fixed observed iterate is eventually exactly constant in the normalized high-frequency variable, so the countermodel meets the fixed-iterate asymptotic claim being tested. Additional physical analytic structure may rule it out, but must actually be used and estimated. The model cannot be cited as a counterexample to the source conjecture.

## 6. Final disposition

The actual-density slow diagonal theorem (5), the conditional compatibility test (7), and the compact clock obstruction (8) are proved. Together with the previous turns, they identify several complete scoped statements, including a corrected source prefactor and an exact physical spectral reduction. None supplies the uniform physical high-frequency spectrum/remainder and excitation estimates required for the intended periodic-density rate.

The stronger global pointwise formulation also still needs shadow/transition analysis and a justified treatment of zeros. The printed prefactor mismatch is an algebraic source correction, not a substitute for resolving that analytic problem. The two-dimensional reductions do not silently settle the three-dimensional variant.

**Final original status: unresolved, five substantive author turns completed out of five.** No sixth author search is undertaken. Independent review should test all scoped statements and the source match before publication. No novelty certification or original-problem counterexample is claimed.
