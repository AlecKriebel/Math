# Turn 3: the critical beta=3 case from the ordinary first moment

**New scope: beta=3 is affirmative under (JM) with only the ordinary SIRSN moments. The full beta>3 question remains unresolved. Author turn 3 of 5.**

This turn removes the extra D log(1+D) assumption used for the beta=3 endpoint in Turn 1. The proof distinguishes almost-sure local finiteness from finite expectation: the critical traffic is locally finite almost surely, has all moments of order less than one on bounded windows, and has infinite first moment. A road-size band decomposition makes these statements compatible.

## 1. Setup and cutoff convention

Use the jointly measurable continuum realization (JM) from Turn 1, with the ordinary assumptions

    d := E len R(0,(1,0)) < infinity,    p := p(1) < infinity.

The major-road process E_r has intensity p/r, is nested decreasing in r, and scales jointly with routes: spatial dilation by c sends E_r to E_{cr}. These are the source definitions and established scaling, not an extra speed model. Write

    F_r := E_r minus E_{2r}.                                    (1)

All expectations and traffic integrals below are nonnegative, so Tonelli applies even before finiteness is proved.

The source uses truncation at distance at least r; the earlier proof used greater than r for convenient strict inequalities. Both conventions are covered. Indeed E_open(r) is the increasing union of E_closed(r+1/n) (after restricting to positive n), hence has the same intensity p/r by monotone convergence. Also

    E_open(r) subset E_closed(r) subset E_open(r') for 0<r'<r.

Thus a local-finiteness result for all positive open cutoffs implies the closed-cutoff source result. We use one convention consistently in (1); changes at isolated cutoff values do not affect the integrals over r below. This clarifies the source convention without changing any frozen earlier proof bytes.

## 2. Major-road size is bounded on every bounded window

**Lemma.** For R>0 and M>6R,

    P(E_M intersects B_R) ≤ 8 pi p R/M.                          (2)

Consequently, almost surely, every bounded window B_R has a finite random M_R such that E_M intersect B_R is empty for all M≥M_R.

**Proof.** If w belongs to E_M intersect B_R, it lies on a sampled route with both endpoints at distance at least M from w. Follow the route from w until its first exit from B_{2R}. This connector has length at least R. Every point v on it satisfies |v−w|≤3R, so its distance from each endpoint is at least M−3R>M/2. The connector is therefore in E_{M/2} intersect B_{2R}, apart from an irrelevant exit endpoint. Thus

    {E_M intersects B_R}
       subset {H^1(E_{M/2} intersect B_{2R})≥R}.

The latter random length has expectation 8 pi p R^2/M. Markov's inequality proves (2). Apply Borel–Cantelli to M=2^j and use nestedness. The same conclusion holds simultaneously on a countable exhaustion by R. QED.

This lemma concerns the sampled major-road sets themselves, whose points have witnessing routes. It is stronger than merely saying their lengths tend to zero in expectation. It is not an assertion about arbitrary routes inserted into the network without the support argument.

## 3. A typical route lies on positive, finite road-size levels

Turn 1's independent-sample superposition and Campbell argument shows that, almost surely, for almost every endpoint pair, its route image apart from its endpoints is supported up to length-null sets on E_{0+}:=union_{r>0}E_r. On every bounded window, intersection_{r>0}E_r is empty almost surely by the preceding lemma. A finite-length route has bounded image. Therefore its length is partitioned, up to null sets, by

    { F_{2^j u} : j in Z }                                    (3)

for every u>0. For almost every endpoint pair this holds in the realized network.

It also holds in expectation for the planted route from 0 to (1,0), used below. One justification is the source planted-point property (Aldous, Section 6.3, equation (6.4)). Alternatively, starting with the preceding almost-every-pair statement, the expected length of the omitted route portion is translation invariant, rotation invariant and homogeneous of degree one in endpoint distance. Thus it is c|y−x| for a fixed c≥0, and its integral over bounded endpoint windows is zero by Campbell/Tonelli; hence c=0. The nonnegative omitted length of the planted unit route is zero almost surely. This argument applies to the measurable sampled-road coupling and does not assert an automatic (JM) version from bare finite-dimensional laws.

Define

    ell(u) := E H^1(R(0,(1,0)) intersect F_u),   u>0.

Partition (3) gives for every u>0

    sum_{j in Z} ell(2^j u) = d.                               (4)

Integrate (4) over 1≤u<2 against du/u and use Tonelli. The intervals [2^j,2^(j+1)) partition (0,infinity), so

    integral_0^infinity ell(u) du/u = d log 2.                  (5)

No logarithmic route-length moment is present.

## 4. Exact expected traffic of a band at beta=3

For a bounded Borel A, let X_{beta,r}(A) be the traffic restricted to F_r:

    X_{beta,r}(A) = integral integral |y−x|^(−beta)
                       H^1(R(x,y) intersect F_r intersect A) dx dy.

Joint translation invariance of the routes and sampled major roads gives the mass-transport identity

    E integral H^1(R(x,x+z) intersect F_r intersect A) dx
       = |A| E H^1(R(0,z) intersect F_r).                       (6)

To see this without an independence assumption, translate the entire rooted route and major-road set by −x inside the expectation; then the integral over x of the indicator that any fixed translated route point lands in A is |A|.

By rotation and scale invariance, for |z|=t,

    E H^1(R(0,z) intersect F_r) = t ell(r/t).                   (7)

Consequently, at beta=3, polar integration and u=r/t yield the exact identity

    E X_{3,r}(A)
       = 2 pi |A| integral_0^infinity ell(r/t) dt/t
       = 2 pi |A| d log 2.                                    (8)

This is finite and independent of r. In particular every fixed-band traffic measure is almost surely locally finite.

## 5. Critical local finiteness, sigma-finiteness and scaling

**Theorem.** Under the ordinary SIRSN assumptions and (JM), T_{3,r} is almost surely locally finite, simultaneously for every r>0. Therefore the unrestricted beta=3 traffic is sigma-finite and obeys the source scaling law (sigma_c)_#T_3 equal in law to c^(−2)T_3.

**Proof.** Fix r>0 and R. The bands F_r,F_{2r},F_{4r},... partition E_r except for the intersection of all these sets. By Section 2 that intersection is empty on B_R, and in fact all sufficiently high bands are empty there. Thus, in each admissible realization,

    T_{3,r}(B_R) = sum_{j=0}^{J−1} X_{3,2^j r}(B_R)            (9)

for some finite random J. Each summand is finite almost surely by (8), simultaneously over the countable values of j. Thus the sum is finite. Countably many R and r, followed by nestedness, give all positive r and all bounded windows. The support and scaling conclusions now follow exactly as in Turn 1, Section 7. QED.

Combined with Turn 1, this settles the range **2<beta≤3** under (JM), using only E D<infinity and p(1)<infinity.

## 6. Infinite mean and finite subunit moments

For every r>0 and bounded A of positive area, Tonelli and the disjoint bands give

    E T_{3,r}(A)
      = sum_{j=0}^infinity 2 pi |A| d log 2
      = infinity.                                             (10)

This is consistent with almost-sure finiteness: the number and traffic sizes of the contributing bands are random and correlated. No finite-mean conclusion for T_{3,r} is being made.

There is nevertheless a universal fractional-moment estimate on B_R. Set

    C = 2 pi |B_R| d log 2.

Choose an integer J0≥0 with 2^J0 r>6R. For x≥1, take J=J0+ceil(log_2 x). Outside the event E_{2^J r} intersects B_R, equation (9) contains at most J terms. Markov's inequality, (8), and (2) therefore give

    P(T_{3,r}(B_R)>x)
      ≤ [ C(J0+1+log_2 x) + 8 pi p R/(2^J0 r) ] / x.          (11)

This bound need not be below one, which causes no problem. In particular, for every 0<a<1,

    E[T_{3,r}(B_R)^a] < infinity.                              (12)

Indeed the tail formula a integral_0^infinity x^(a−1)P(T>x)dx is finite by (11), since integral_1^infinity x^(a−2)log x dx=1/(1−a)^2. This is an a.s. local-finiteness theorem with quantitative heavy-tail control, not a finite first-moment theorem.

## 7. Exact reformulation of the beta>3 annealed obstruction

There is a useful intrinsic mark on the sampled road set:

    S(w) := sup{u>0 : w belongs to E_u}.

For length-almost every point of a typical unit route, 0<S(w)<infinity by Sections 2–3. Endpoint membership of the interval {u:w in E_u} does not matter in du integrals. Define, for alpha>0,

    M_alpha := E integral_{R(0,(1,0))} S(w)^alpha dH^1(w),

allowing infinity. The same scaling and mass transport, followed by Tonelli, gives, for beta=3+alpha>3,

    E T_{beta,r}(A)
       = [2 pi |A|/(beta−3)] r^(3−beta) M_{beta−3}.             (13)

For clarity, set h(u)=E H^1(R(0,(1,0)) intersect E_u). The left side equals

    2 pi |A| r^(3−beta) integral_0^infinity u^(beta−4)h(u)du.

For each route point the inner integral runs from 0 to S(w) and equals S(w)^(beta−3)/(beta−3), proving (13). Thus a finite positive moment of this road-size mark is an exact finite-expectation criterion, and is sufficient for the original almost-sure local-finiteness claim in that beta range.

This is **not** asserted to be necessary for almost-sure local finiteness. The beta=3 result itself warns against confusing infinite expectation with failure of local finiteness.

The ordinary first-moment route assumption only gives M_0=d. It does not by itself yield any positive M_alpha in this argument. Earlier route-length moment bounds imply a sufficient positive-alpha range, but no new positive intrinsic-mark moment has been proved here. This is the surviving beta>3 obstruction, stated more sharply than a generic lack of estimates.

## 8. Status and attribution

The tools are source major-road intensity/scaling, sampled-route support, stationarity, Tonelli, Markov and Borel–Cantelli. The band identity and its application are supplied as an explicit proof, without historical-priority certification. Exact scalar controls supplement this proof; they do not formally certify its continuum geometry.

**Original-axiom target remains unresolved for 3<beta<4, as does automatic construction of (JM) from bare FDDs. Author count 3/5.** No complete all-SIRSN claim is made. Uncalibrated progress estimate for the full target: 60%. All earlier frozen files remain unchanged; the present theorem strengthens their beta=3 scope.
