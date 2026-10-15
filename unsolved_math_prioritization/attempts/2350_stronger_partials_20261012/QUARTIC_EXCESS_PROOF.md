# A forced unpaired quartic excess at the endpoint packing profile

12 October 2026. Erdős 864 / problem 2350 / queue row 1741.

## Scope and main result

This is a new finite arithmetic constraint and its consequence for the previously accepted endpoint-core/central-unpaired relaxation profile. It does not prove that the profile is impossible, improve the unrestricted leading constant, or settle the conjecture. No publication or remote mutation is part of this work. No novelty or current-literature claim is made.

Let A be an integer set in [1,N] with at most one repeated unordered sum, with equal summands allowed. Let T be that exceptional sum, C=A∩(T−A), and U=A\C. Define

    P_T(U) = #{(u1,u2,u3,u4) in U^4 : u1+u2+u3−u4=T}.

All four entries are ordered and repetitions are allowed. The new conclusion is the following. If, after centering at T/2 and scaling by N, the empirical core and unpaired measures tend respectively to

    g = sqrt(2) 1_([-1/2,−b/2] union [b/2,1/2]),
    v = 1_[−b/2,b/2],

where b=1−sqrt(2/3), then

    liminf P_T(U)/N >= b^2/(7−2sqrt(2))
                       = 0.00807213629443446... .       (A)

The macroscopic uniform central-interval model gives only

    (2/3)b^3 = 0.00411946884333636... .                  (B)

Thus an actual integer realization of the relaxed maximizer must exhibit a positive quartic excess of at least

    0.00395266745109810... N + o(N).

Equivalently, its centered unpaired Fourier residual must have a normalized signed fourth-order phase correlation with lower limit at least 0.0625149642449024... . A precise subcritical-phase hypothesis therefore excludes this profile. That hypothesis is NOT proved here. The required phase is compatible with scalar norm bounds, and explicit finite countercontrols below show that Sidonicity and the absence of reflected unpaired points do not by themselves forbid the relevant equations.

A localized version further forces almost every sufficiently short unpaired sum to land on an occupied unpaired difference; its required local collision density is 3+sqrt(6) times the four-variable mixing prediction. This mixing prediction is an additional hypothesis, not a consequence of the limiting profile.

The gain over the earlier marginal relaxation is a forced count of exact integer equations. No disjointness of weak convolution densities is asserted or used.

## 1. Additional finite occupied-site identities

For any integer d≠0, define:

- c(d): the indicator that d is a signed difference of two core points;
- r(d): the number of ordered pairs (u,u') in U² with u−u'=d;
- m(d): the number of pairs (c,u) in C×U with c+u=T+d;
- q(d): the number of unordered U-pairs, equal entries allowed, with sum T+d.

All four numbers belong to {0,1}. Moreover

    c(d)+r(d)+m(d)+m(−d) <= 1,                         (1)
    c(d)+m(d)+q(d) <= 1.                               (2)

Here c(d)=c(−d) and r(d)=r(−d). Also U∩(T−U)=∅, so q(0)=0.

For completeness, a collision of distinct nonzero-difference representations yields a repeated unordered sum. Its value must be T, and the two difference representations are reflected core pairs. Thus every difference involving U is unique and cannot collide with a core difference. Reflection of C converts its two orientations of mixed differences at d into the two mixed sum counts m(d) and m(−d), proving (1).

A core unordered sum at T+d corresponds, by reflection of one endpoint, to an occupied signed core difference d. Conversely, every such difference gives that core sum. Since d≠0, this sum is nonexceptional and has exactly one unordered representation. This remains true when that representation has equal entries. Consequently the number of unordered core representations at T+d is exactly c(d). Nonexceptional sum uniqueness now gives (2), and in particular proves the claimed binary bounds for m and q. The same uniqueness proves that U itself is a strong Sidon set.

These two capacities imply the exact identity

    q(d)r(d) = [q(d)+c(d)+m(d)+r(d)−1]_+,             (3)

where [x]_+=max(x,0). Indeed if c(d)=1 or m(d)=1, both r(d) and q(d) are zero. Otherwise the right side is [q+r−1]_+=qr for binary q,r.

The left side records an actual equality between a U-pair sum and a U-pair difference. It was absent from the earlier marginal inequalities.

### Exact quartic counting and a coarse-block inequality

Put

    delta(d) = #{u in U : 2u=T+d}.

The number of ordered U-pairs with sum T+d is 2q(d)−delta(d). Orthogonality of the two integer counts, or direct matching, gives

    P_T(U) = 2 sum_(d≠0) q(d)r(d) − Delta,
    Delta = sum_(d≠0) delta(d)r(d),
    0 <= Delta <= |U|.                                 (4)

There is no contribution from d=0, because q(0)=0. In the last bound each u supplies at most one d, and r(d)≤1.

For any finitely supported test weight 0≤phi(d)≤1, (3)–(4) give

    P_T(U) >= 2 sum_(d≠0) phi(d)
                  [q(d)+c(d)+m(d)+r(d)−1] − |U|.       (5)

In particular, for any disjoint finite blocks J_j of nonzero integers,

    P_T(U) >= 2 sum_j [ sum_(d in J_j)
                  (q(d)+c(d)+m(d)+r(d)) − |J_j| ]_+
                  − |U|.                              (6)

Thus the result can be evaluated from coarse counts without guessing which individual sum sites meet difference sites. All statements in this section are exact and finite.

## 2. General continuum consequence for an integer quartic count

Assume a sequence of admissible inputs with an exceptional sum T=T_N. Use centered empirical measures

    gamma_N = N^(−1/2) sum_(c in C) delta_((c−T/2)/N),
    upsilon_N = N^(−1/2) sum_(u in U) delta_((u−T/2)/N).

Suppose they converge weakly to g dx and v dx, with compactly supported nonnegative L² densities. These density properties follow from the accepted difference domination for subsequential limits; they may instead be assumed for this theorem. The core density g is even. No symmetry of v is assumed in this section. Let tilde(v)(x)=v(−x), and define

    J_(g,v)(t) = (1/2)(g*tilde(g))(t) + (g*v)(t)
                   + (v*tilde(v))(t) + (1/2)(v*v)(t) − 1.

**Theorem 1.** Under these hypotheses,

    liminf P_T(U)/N >= 2 integral_R [J_(g,v)(t)]_+ dt.   (7)

**Proof.** The empirical measures of the four counts, with coefficient 1/N at d/N, converge respectively as follows:

    c -> (1/2)g*tilde(g),
    m -> g*v,
    r -> v*tilde(v),
    q -> (1/2)v*v.

For c, the core difference count is halved except at self-reflected representations. Their total correction is O(|C|), and the zero-difference atom has the same negligible order after division by N. For q, converting unordered counts to half ordered counts has total diagonal correction O(|U|). The r zero atom is also O(|U|)/N. Products of weakly convergent compactly supported measures converge, so these assertions follow directly. The known difference multiplicity bound gives |C|+|U|=O(sqrt(N)).

Apply (5) with phi(d)=phi_0(d/N), where phi_0 is any compactly supported continuous function taking values in [0,1]. Divide by N and pass to the lower limit. The lattice constant term converges by Riemann sums, and the diagonal error vanishes. The result is

    liminf P_T(U)/N >= 2 integral phi_0(t) J_(g,v)(t) dt.

Convolution of two compactly supported L² functions is continuous. Outside a fixed compact interval J_(g,v)=−1. Taking the supremum over these continuous test functions gives exactly the positive-part integral in (7). This does not pass any product of lattice occupancy indicators through weak convergence. Instead, it passes a finite linear lower bound on their product. QED.

## 3. Evaluation at the endpoint-core/central-unpaired profile

Write A0=7−2sqrt(2), and for 0<b<1 use

    E=[−1/2,−b/2] union [b/2,1/2],
    V=[−b/2,b/2],
    g=sqrt(2)1_E,       v=1_V.

For 0≤t≤min(b,(1−b)/2), elementary interval overlaps give

    (1/2)(g*g)(t) = 1−b−2t,
    (g*v)(t) = sqrt(2)t,
    (v*v)(t) = b−t.

Both functions are even, so tilde(g)=g and tilde(v)=v. Consequently

    J_(g,v)(t) = b/2 − (7/2−sqrt(2))|t|               (8)

in this short-shift range.

If b/A0≤(1−b)/2, equivalently b≤A0/(A0+2), its positive triangle fits inside that range. Theorem 1 therefore gives

    liminf P_T(U)/N >= b²/A0.                          (9)

This follows by integrating (8) over |t|≤b/A0 and multiplying by two, as required by (7). For the relevant b=1−sqrt(2/3), one has b<(1−b)/2. Thus (8) applies on all |t|≤b; for |t|≥b the unpaired convolution vanishes, and the already proved difference domination implies J≤0. Hence b²/A0 is exactly the full positive-part functional in (7), rather than merely the contribution of a small subinterval.

The relevant constants are

    b                     = 0.183503419072273967...,
    b/A0                  = 0.043989023938868410...,
    b²/A0                 = 0.008072136294434462...,
    (2/3)b³               = 0.004119468843336364...,
    b²/A0 − (2/3)b³       = 0.003952667451098097... .

The ratio between the forced count and the uniform-model count is 1.95950900502425... . This is a strict arithmetic excess requirement for any actual realization. It is not a contradiction on its own.

More generally, the bound in (9) exceeds the uniform-model count whenever

    0<b<3/(2A0) = 0.359576602124860613... .             (10)

This whole range also obeys the cutoff condition needed for (9).

### 3.1 Near-total alignment of sufficiently short unpaired sums

There is a stronger local description. Let P_N(delta) count the ordered quadruples in P_T(U) subject to

    0 < |u1+u2−T| <= delta N.

For every fixed 0<delta<=b/A0 at the relevant endpoint profile, the same proof restricted to |d|<=delta N gives

    2b delta−A0 delta² <= liminf P_N(delta)/N
                       <= limsup P_N(delta)/N
                       <= 2b delta−delta².             (10a)

For the lower bound, integrate (8) on [−delta,delta] and use the localized version of (4). For the upper bound, each nonzero U-difference has at most one representation, so the restricted quartic count is at most the number of ordered U-pairs with sum offset in that band. The latter, divided by N, tends to the integral of v*v, namely 2b delta−delta². The diagonal corrections are O(|U|)=o(N); interval endpoints carry no mass in the limiting convolution.

In particular,

    lim_(delta down to 0) liminf_N P_N(delta)/(2delta N)
      = lim_(delta down to 0) limsup_N P_N(delta)/(2delta N)
      = b.                                             (10b)

The proportion of short ordered U-sums which fail to land on occupied U-differences is therefore at most

    [(A0−1)delta²+o(1)]/[2b delta−delta²]

for each fixed delta, and this upper bound tends to zero as delta tends to zero. This is a proved near-total alignment of exact occupied sites; it is not a claim that their weak densities have disjoint support.

By contrast, a local four-variable mixing hypothesis would predict the normalized count

    integral_[−delta,delta] (v*v)(t)(v*tilde(v))(t) dt
       = 2b² delta−2b delta²+(2/3)delta³.

Its local density is b² rather than b. Thus any theorem bounding that local collision density by a value strictly below b would exclude the endpoint profile. At b=1−sqrt(2/3), the required enhancement over the mixing prediction is

    1/b = 3+sqrt(6) = 5.449489742783178... .

The local mixing upper bound is not established. Equation (10b) instead specifies exactly how any actual endpoint realization must fail it. Optimizing the lower bound in (10a) over delta gives delta=b/A0 and recovers the global bound (9).

## 4. An explicit signed-phase structural obstruction

This section converts the arithmetic count into an exact missing hypothesis, rather than assuming four-variable transfer from weak convergence.

Suppose U has the central uniform limit v=1_[−b/2,b/2]. Define centered Fourier sums on alpha in [−1/2,1/2], with probability Lebesgue measure,

    F_N(alpha) = sum_(u in U) exp(2 pi i (u−T/2)alpha).

Let L_N be the symmetric set of points of Z−T/2 lying in [−bN/2,bN/2], and put

    G_N(alpha) = N^(−1/2) sum_(z in L_N) exp(2 pi i z alpha),
    R_N = F_N−G_N.

G_N is real. If T is odd the individual functions may be antiperiodic; all fourth-degree integrands below are periodic, so ordinary integer orthogonality still gives

    integral |F_N|^4 = 2|U|²−|U|,
    P_T(U) = integral F_N^3 conjugate(F_N).             (11)

The first equality follows from strong Sidonicity of U. The second follows from the centered exponent u1+u2+u3−u4−T. Thus parity introduces no change of constant.

The interval has M_N=bN+O(1) lattice points. Its exact ordered additive energy is (2M_N³+M_N)/3. Since G_N is real,

    integral |G_N|^4 = integral G_N^3 conjugate(G_N)
                     = ((2/3)b³+o(1))N.               (12)

### Mixed terms really do vanish; the pure residual does not

For j=1,2,3,

    integral |G_N|^(4−j)|R_N|^j = o(N).               (13)

Here is the justification. Weak convergence on a bounded support and equicontinuity give R_N(t/N)=o(sqrt(N)), uniformly for each bounded t interval. The derivative of F_N(t/N)/sqrt(N) is bounded using the bounded rescaled support and |U|=O(sqrt(N)); the analogous bound holds for G_N. Therefore the mixed integral on |alpha|≤K/N is o_K(N). Strong Sidonicity and (12) give integral |R_N|⁴=O(N). The geometric-series estimate for the centered interval gives

    integral_(||alpha||>K/N) |G_N|⁴ = O(N K^(−3)).

Hölder bounds the outer mixed integral by O(N K^(−3(4−j)/4)). First let N tend to infinity for fixed K, then let K tend to infinity. This proves (13) without controlling the pure residual fourth moment.

Expanding the two quartics and using (11)–(13) yields

    E_N := integral |R_N|⁴
        = (2b²−(2/3)b³+o(1))N,                         (14)

    P_T(U) = ((2/3)b³+o(1))N
              + Re integral R_N³ conjugate(R_N).      (15)

Define Psi_N=Re integral R_N³ conjugate(R_N)/E_N. The denominator is positive eventually. Combining (9), (14), and (15) proves:

**Theorem 2 (necessary residual phase bound).** Every actual admissible sequence with the endpoint profile and b≤A0/(A0+2) satisfies

    liminf Psi_N >= rho(b),
    rho(b) = [1/A0−(2/3)b]/[2−(2/3)b].                (16)

The bound rho(b) is positive precisely when 0<b<3/(2A0). Inequality (16) remains valid throughout the stated cutoff range.

At b=1−sqrt(2/3), this threshold is

    rho(b)=0.0625149642449024... .

Consequently any structural theorem proving limsup Psi_N<rho(b) for these sequences would exclude the relaxed maximizer. In particular a nonpositive upper limit, or four-variable equidistribution P_T(U)=((2/3)b³+o(1))N, would suffice. Neither assertion follows from weak density, and neither is established here.

The exact needed gap in the unnormalized signed residual is at least 0.00395266745109810... N. Its total fourth energy is 0.0632275407790928... N. Thus the elementary bound −1≤Psi_N≤1 leaves substantial room for the required positive phase. Norm estimates alone do not contradict (16).

## 5. Countercontrols and the remaining microscopic issue

### 5.1 Exact admissible integer control

Take centered integer sets

    C={−25,−10,10,25},       U={1,2,4}.

Their union has exactly one repeated unordered sum, namely 0, represented by the two opposite core pairs. Its U is strong Sidon and U∩(−U)=∅. Nevertheless P_0(U)=3, coming from the three orderings of 1+1+2=4. Translating the entire input by 26 gives the positive integer example

    A={1,16,27,28,30,36,51},       T=52.

This refutes a proposed exact rule that the full reflected-core hypotheses forbid unpaired triple-to-single equations. It does not settle their asymptotic frequency under the endpoint weak profile.

### 5.2 Perfect modular alignment without reflected pairs

In Z/7Z, U={1,2,4} is strong Sidon: its six unordered sums are precisely the six nonzero residues. Its six ordered nonzero differences are also those six residues. Moreover U∩(−U)=∅. Every unordered U-sum therefore lies in the occupied U-difference set, and there are nine ordered solutions to u1+u2+u3=u4 modulo 7.

This shows that Sidonicity and lack of reflected pairs permit complete microscopic sum/difference alignment in a finite group. Integer interval carries and the coupled core remain essential extra structure; modular alignment alone cannot disprove or prove the interval claim.

### 5.3 Sharpness of the one-site occupancy lower bound

The exact bound in Theorem 1 uses the additional simultaneous site capacities, but those capacities alone cannot force a larger intersection at the endpoint profile. To see this, for a fixed short positive shift t consider an abstract probability space of sites with disjoint categories of masses

    core: c=1−b−2t,
    U-difference: r=b−t,
    positive mixed: m=sqrt(2)t,
    negative mixed: m=sqrt(2)t,
    hole: h=(3−2sqrt(2))t.

These masses add to one and are nonnegative throughout the short range. Each U-sum orientation has prescribed mass q=(b−t)/2. A positive U-sum may use the negative mixed category, holes, and the U-difference category; a negative U-sum has the analogous choices. For either orientation the capacity outside U-differences is m+h. Allocate sums there first, and then in U-differences. The minimum overlap per orientation is exactly

    [q−m−h]_+ = [b/2−(7/2−sqrt(2))t]_+.

Both allocations can be made simultaneously: there is no further one-site restriction against the two sum orientations sharing a hole or a U-difference. The condition q≤m+h+r ensures feasibility. This is only an abstract occupancy coupling, not an integer construction. It demonstrates that improving (A) requires a relation between different sites, or some other arithmetic information, rather than sharper use of these same one-site capacities.

## 6. Verification, provenance, and precise unresolved lemma

The companion finite diagnostic independently builds the sum and difference counts from every subset of [1,N] for 1≤N≤17. It verifies (1)–(4), including odd T and core midpoints, the coarse-block lower bound (6), and localized quartic-count lower bounds. It directly counts the quartic equation by enumerating U⁴. It also checks the two explicit countercontrols, all binary one-site patterns permitted by (1)–(2), and the needed short-shift interval-overlap formulas using exact rational arithmetic. The irrational decimal values are diagnostics; the mathematical constants above are exact expressions.

The verifier imports no code from earlier packets. It uses explicit RuntimeError checks, not assertions, so optimization does not disable its tests. Recorded normal, −O, and −OO results are summarized as aggregate checks; no diagnostic-file identity is distributed. Enumeration is a diagnostic, not a proof of the asymptotic statements.

The accepted asymmetric proof and its independent acceptance were read; their already-published editions are identified in PUBLIC_DEPENDENCIES.json. The earlier symmetric-core modular/carry note and fourth-order endpoint note were also read as controls against the known modular and norm-transfer shortcuts. No fresh external theorem or source-status assertion is needed for this packet.

The unresolved discrete lemma can now be stated quantitatively: for an actual admissible sequence with the displayed endpoint profile, prove a uniform upper limit on the unpaired signed residual phase strictly below rho(1−sqrt(2/3)), or equivalently an upper bound on P_T(U)/N strictly below b²/(7−2sqrt(2)). The finite hypotheses currently proved do not give that upper bound. The present result identifies a necessary arithmetic excess and an explicit exclusion threshold; it does not eliminate the profile or reduce the original problem to this one profile alone.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
