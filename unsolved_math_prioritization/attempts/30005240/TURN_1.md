# Turn 1: a source-prefactor correction and the real uniformity obstruction

**Original problem unresolved. Substantive author turn 1 of 5.** The source gate and live branch were checked before this turn; no earlier proof turn existed. This attempt tests whether the known optical-amplitude formulas and fixed-reflection expansions actually imply the requested rate for true densities. They do not supply that implication on their own.

Three results are retained: an algebraic correction to the printed two-period shortcut, a precise sufficient one-period remainder condition, and an exact counterexample to interchanging the high-frequency and large-reflection limits in an abstract two-mode model. The abstract model is not a scattering counterexample.

## 1. Exact two-period multiplier forced by the source recurrence

For two disjoint strictly positively curved obstacles, let d>0 be the distance between their nearest points and let kappa_0,kappa_1>0 be the curvatures there. At those two points the connecting segment is normal to the boundaries. The source continued-fraction recurrence therefore has c_j=1 and d_j=2(1+d kappa_(j−1)). Its limiting two-cycle, with an immaterial interchange of indices, satisfies

    L_0=2a−1/L_1,   L_1=2b−1/L_0,   L_0,L_1>1,
    a=1+d kappa_0,  b=1+d kappa_1.                              (1)

This is the n=2 specialization of the source recurrence, not a new asymptotic PDE input. Put A=ab>1 and P=L_0 L_1. Multiplication of (1) gives

    P+1=2aL_1=2bL_0,
    (P+1)^2=4AP,
    P^2+(2−4A)P+1=0.                                           (2)

Since P>1, only the larger root is allowed:

    P=2A−1+2sqrt(A(A−1))=(sqrt(A)+sqrt(A−1))^2.                 (3)

Thus the magnitude of the source's optical multiplier product is

    q=P^(−1/2)=sqrt(A)−sqrt(A−1)
                 =1/[sqrt(A)+sqrt(A−1)].                       (4)

The complex multiplier for the full density, with the source outgoing-phase convention, is

    R_(2,k)=exp(2ikd) q.                                       (5)

The phase cannot be dropped from a statement about the complex quotient eta_(m+2)/eta_m. The positive number q is appropriate for its modulus or a precisely phase-corrected quantity.

### The printed shortcut disagrees with that recurrence

The OWR formula on printed p.2547 is

    q_print=1/sqrt(A(1+sqrt(1−1/A))).                           (6)

The earlier primary manuscript also prints P_print=A+sqrt(A(A−1)) for L_0L_1 immediately after its recurrence; that page was visually inspected as well as the OWR page. This is not a text-extraction uncertainty. Substituting P_print into (2) gives

    P_print^2+(2−4A)P_print+1
       =−(A−1)[2A+1+2sqrt(A(A−1))] < 0.                        (7)

So P_print cannot satisfy the same recurrence for any A>1. Indeed P=2P_print−1, and

    1 < q_print/q < sqrt(2).                                  (8)

For d kappa_0=d kappa_1=1, the two-cycle has L_0=L_1=2+sqrt(3), yielding q=2−sqrt(3), whereas (6) gives 1/sqrt(4+2sqrt(3)). They differ by a fixed positive quantity, independent of frequency.

This is an algebraic correction of one printed simplification. The general product over the source continued-fraction limits remains the appropriate optical rate. It does **not** prove that actual PDE densities have either rate, and it does not resolve the intended uniform-remainder question by exploiting a misprint. No external correction notice or historical-priority claim is made.

## 2. What one-period control is sufficient for actual densities

Fix a period n and a compact region K inside the jointly illuminated portions of the return obstacle, on which the nonzero optical currents A_m are defined. Use the source normalization

    eta_m(x,k)=2ik A_m(x,k) v_m(x,k),
    v_m=1+P_m/k.                                               (9)

The factor 2ik is common to m and m+n. Suppose on K, for the range of m,k under consideration,

    |A_(m+n)/A_m−R_(n,k)| ≤ E_(m,k),
    |R_(n,k)| ≤ Q.                                            (10)

No bound on eta_m is derived until its denominator is controlled. Assume further

    |k+P_m|≥c k,          |P_(m+n)−P_m|≤C_0,                   (11)

for constants c>0,C_0 independent of m,k in that range. These are additional sufficient hypotheses, not established properties of the source PDE densities in this turn.

**Lemma.** Under (9)–(11),

    |eta_(m+n)/eta_m−R_(n,k)|
      ≤ (1+C_0/(ck)) E_(m,k) + Q C_0/(ck).                    (12)

**Proof.** Equation (11) implies eta_m is nonzero and

    |v_(m+n)/v_m−1|
       = |P_(m+n)−P_m|/|k+P_m| ≤ C_0/(ck).

In particular |v_(m+n)/v_m|≤1+C_0/(ck). The exact factorization

    eta_(m+n)/eta_m−R
      = (v_(m+n)/v_m)(A_(m+n)/A_m−R)
          +R(v_(m+n)/v_m−1)

and the triangle inequality give (12). QED.

This condition is weaker than requiring P_m itself to stay uniformly bounded: for example P_m=m gives |k+P_m|≥k and a fixed increment P_(m+n)−P_m=n for each fixed period. Such an example illustrates the distinction only; it is not asserted to be the actual scattering remainder.

The decisive general condition is small **relative one-period change** of v_m, together with nonvanishing, rather than a fixed-m asymptotic expansion of v_m. Uniform bounded increments as in (11) are one concrete sufficient route.

## 3. The logarithmic reflection scale cannot be omitted

The source's approximate-current estimate has a bound of the form

    E_(m,k) ≤ C_K [delta^(n/2) min{2,exp(C k delta^(m/2))−1}
                        + C delta^((m−n)/2)],                 (13)

where 0<delta<1. The division by the source incidence factor gamma_m is absorbed in C_K only when K stays a uniformly positive distance inside the stabilized illuminated region. This is not a bound valid automatically at the shadow boundary.

For k≥1 and fixed n, take

    m≥4 log(k)/|log(delta)|+M_n,                               (14)

with M_n also ensuring the source requirement m>2n. Then k delta^(m/2)≤delta^(M_n/2)/k. The elementary inequality exp(u)−1≤exp(C')u for 0≤u≤C' shows the first term of (13) is O(k^−1); the second is O(k^−2), with constants fixed once K,n,M_n are fixed. Combining (12) with (13) therefore yields the desired O(k^−1) actual-current ratio on K **if** (11) holds uniformly for that joint range.

Neither (11) nor a whole-boundary transfer is proved by this calculation. It states precisely what is missing. Taking k→infinity at a fixed m does not make the phase-stabilization contribution in (13) small. A statement that suppresses the joint m,k regime is therefore not justified by this bound.

## 4. An exact two-mode obstruction to a tempting limit exchange

Fix 0<rho<sigma<1 and put, for real k≥1 and integer j≥0,

    u_j(k)=rho^j+2^(−k)sigma^j.                                (15)

Interpret j as a count of complete periods. The sequence is positive and exponentially decreasing in j. Its entire iteration series converges uniformly for k≥1:

    sum_(j≥0) u_j(k)=1/(1−rho)+2^(−k)/(1−sigma).                (16)

For every fixed j and every N>0,

    u_j(k)/rho^j=1+O_(j,N)(k^(−N)) as k→infinity.               (17)

Indeed 2^(−k) decays faster than every inverse power and (sigma/rho)^j is fixed. Thus the full fixed-period high-frequency expansion agrees, to all algebraic orders, with the single optical mode rho^j.

Nevertheless, with t=2^(−k)(sigma/rho)^j,

    u_(j+1)(k)/u_j(k)
       =rho+(sigma−rho)t/(1+t),
    lim_(j→infinity) u_(j+1)(k)/u_j(k)=sigma                    (18)

for every fixed k. Hence

    lim_(j→infinity) lim_(k→infinity) u_(j+1)/u_j =rho,
    lim_(k→infinity) lim_(j→infinity) u_(j+1)/u_j =sigma.         (19)

In particular the supremum over j of the difference from rho is sigma−rho, not O(k^−1).

For the exact rational choice rho=1/4,sigma=1/2 and integer k, the transition t=1 occurs at j=k and the quotient there is 3/8, a fixed distance 1/8 from rho. This obstruction persists despite positivity, uniform summability and all-orders fixed-j asymptotics. It is the observation of powers of the bounded diagonal matrix diag(rho,sigma) on the initial vector (1,2^(−k)), with the observation functional adding the two coordinates.

This is an abstract linear-iteration counterexample, not a family of Helmholtz obstacles or a counterexample to the actual-density question. It identifies a proof obligation: an exponentially small component with a larger modulus eigenvalue must be excluded or controlled if a uniform-in-reflection statement is desired. Fixed-reflection symbolic asymptotics alone do not exclude it.

## 5. Remaining task and next route

The first attempted route, transferring the known expansion directly to all reflection counts, fails without extra uniform or spectral information. The source's printed two-period simplification also needs the correction proved in Section 1; this is kept separate from the deeper analytic gap.

To resolve the intended problem one must establish sufficient relative remainder control for the actual boundary-density transfer, or an appropriate spectral statement that controls its dominant modes, with the source geometry and boundary regions fully specified. A compact illuminated-subarc theorem would still need a justified passage through transition/shadow regions to establish the strongest global quotient formulation. None of these analytic steps is supplied here.

**Status: scoped correction, conditional stability lemma and abstract obstruction; original unresolved, 1/5 turns.** The next genuine attempt will study normalized one-period transfer rather than assume fixed-m errors are uniform. The source geometry and optical formulas are credited; no novelty certification. Uncalibrated progress estimate toward the complete actual-density theorem: 15%.
