# Every diverging coarse scale in one transverse dimension

**30001321 / OWR-4081-005. Full candidate, author turn 3/5; independent review pending.**

## Statement and source relation

Let `(p_(s,x))_(s>=0,x in Z)` be independent identically distributed random
variables with `0<p_(s,x)<1` almost surely. Given the environment, the walk
starts at zero and, from x at time s, jumps to x+1 with probability p_(s,x)
and to x−1 otherwise. Let `mu_n^omega` be its quenched distribution and
`alpha_n=E_env mu_n^omega` its averaged distribution. For every deterministic
sequence of positive integers `M_N→infinity` and every deterministic choice
of an alignment of the partition `P_N` of Z into M_N-site intervals, we claim
that for every epsilon>0 and K>0,

    P_env(sum_(I in P_N) |mu_N^omega(I)−alpha_N(I)|>epsilon)
          <= C_(epsilon,K) N^(−K)                         (A)

for all sufficiently large N. The threshold may depend on the chosen
sequence M_N; constants may depend on the fixed environment law. There is
no assertion uniform over laws as they approach a deterministic-arrow law.
There is no uniform ellipticity hypothesis and no requirement on the rate
at which M_N diverges. The constants in the intermediate bounds are uniform
in the deterministic alignment.

This is the affirmative d=1 analogue of Berger's Theorem 1, OWR 38/2009,
printed page 2151, under its i.i.d. nearest-neighbor elliptic hypotheses.
It would **disprove the following Conjecture 1**, which says that the same
conclusion does not hold for d=1. This is not an inference from a degenerate
deterministic environment: (A) is asserted for every law above, including
nondegenerate ones. Its novelty or priority has not been established.

The proof uses the full elementary estimates in the frozen `TURN_1.md` and
`TURN_2.md`; their exact hashes are in the manifests. Those files remain
historical partial checkpoints. The present third turn supplies the
small-scale closure missing there. A source audit and full primary reading
copies are recorded separately; no literature theorem asserting (A) is
assumed.

Put q=E p, a=q(1−q), delta=E[p(1−p)]>0, v=2q−1. All constants below may
depend on q and delta. The averaged increments are independent signs with
mean v. Let F_s be the environment sigma field of layers before time s.

## 1. Precisely stated inputs proved in the earlier turns

Write `I_s=sum_x mu_s(x)^2`. The common-environment two-replica difference
chain, scaled by 1/2, has step probabilities a to each neighbor away from
zero, and delta to each neighbor at zero. Its return probabilities satisfy
`g_t<=C/sqrt(t+1)`. The backward hitting profile is maximized at zero.
Consequently

    E[I_(s+t)|F_s]<=g_t,
    E[(sum_(j=0)^(L−1) I_(s+j))^k | F_s]
           <=k! C^k L^(k/2).                              (B)

These are proved in TURN_1 Sections 2–3 and TURN_2 Sections 2–3, respectively.
All time indices s,L in (B) are deterministic. In particular, for fixed
eta>0,

    P(sum_(s<m) I_s>N^eta sqrt(N))=O(N^(−K))               (C)

for every K whenever m<=N. Choosing the moment order depending on K is
permitted; no constants are asserted uniform in K.

For a deterministic function f with Lipschitz constant at most 1/r and
values in [0,1], the layer-exposure martingale for mu_m(f) has increments
bounded by 2/r and predictable quadratic variation bounded by

    C r^(−2) sum_(s<m) I_s.                               (D)

Indeed, the averaged semigroup preserves that Lipschitz constant, and the
increment formula is

 sum_x mu_s(x)(p_(s,x)−q)
   [T_(m−s−1)f(x+1)−T_(m−s−1)f(x−1)].

The independent centered variables within layer s give (D). The scalar
exponential-supermartingale estimate proved in TURN_2 Section 4 is

 P(|Z−E Z|>u, Q<=w)<=2 exp(−u^2/[4(w+bu)]),               (E)

where b bounds increments and Q is predictable quadratic variation.
It is always applied to joint events, not by conditioning the martingale
on a future good event.

Two coarse-scale consequences are needed:

(i) TURN_1 Section 6 proves, for a walk of length n and an M-site interval
partition, uniformly in alignment,

 E_env L_(n,M)
 <= C sqrt((R/M+n^(−1/2))
             (1+log(1+min(M,sqrt(n))))) + C/R^2,           (F)

for fixed R>=1. Thus there is a deterministic bound rho(n,M) such that
`rho(n,M)→0` whenever n→infinity and M→infinity. For example take the
infimum of the right side over R>=1, capped above by 2. This convergence
uses first a fixed sufficiently large R and then n,M→infinity; it imposes
no quantitative lower rate on M.

(ii) TURN_2 proves that for every fixed gamma>1/4 and fixed u>0,

 P(L_(n,H)>u)=O(n^(−K)) for every K,
 uniformly over all H>=n^gamma and deterministic alignments.             (G)

The statement (G) does not itself imply (A); the rest of this proof is the
additional argument.

## 2. A polynomially small concentration function for the old law

Fix, for this proof only,

    ell=floor(N^(3/4)),  m=N−ell,
    H=ceil(N^(5/16)),
    r=N^(3/8),  R=ceil(N^(3/8) log N),
    eta=1/32,  kappa=1/32.                                (H)

Eventually m>=N/2. Let J range over any deterministic collection of at most
C N intervals, each of length at most 10R+10. Then

 P(max_J mu_m(J)>N^(−kappa))=O(N^(−K)) for every K.         (I)

To prove this, choose a real piecewise-linear majorant f_J that equals one
on J, tapers to zero over distance r on both sides, and restrict it to Z.
It is [0,1]-valued and 1/r-Lipschitz. The maximal averaged m-step point mass
is at most C/sqrt(m), with the same statement on the parity sublattice.
Hence

    E mu_m(f_J)<=C (R+r+1)/sqrt(m)
                <=C N^(−1/8)log N=o(N^(−kappa)).          (J)

On the single common event in (C), (D) bounds its predictable variance by
`C N^(eta+1/2−3/4)=C N^(−7/32)`. Its increment bound is `2N^(−3/8)`.
Take u=(1/2)N^(−1/32) in (E). Each joint tail is at most
`2 exp(−c N^(5/32))`. The union over J costs at most C N. The failure of
(C) is charged once. This proves (I).

The statement is about finitely many prescribed intervals, not a claim of
uniform control over environment-dependent intervals. In the application
they will be the fixed moving-strip influence intervals below.

## 3. Coalescing coupling erases within-cell starting information

For any two starting positions x,y with the same parity, let
K_ell^omega(x,.) denote the last-ell-step quenched transition kernel in a
fresh space-time environment. There is a quenched coupling of the two walks
that uses independent transition coins until their first meeting and common
coins thereafter. The paths remain ordered until that meeting: two positions
of the same parity at distance two can meet but cannot cross in a single
nearest-neighbor step.

Before meeting, the two current sites are different, so their environment
variables are independent when the environment is averaged. Their half-gap
is therefore a symmetric lazy walk with probabilities a,a,1−2a, killed at
zero. By reflection, if this walk starts at d>=1, its survival probability
through ell steps is

    sum_(z>=1) [p_ell(z−d)−p_ell(z+d)]
      = sum_(j=1−d)^d p_ell(j)
      <=C d/sqrt(ell+1),                                  (K)

where p_ell is the homogeneous lazy walk's mass function. Reflection also
holds with holding steps, which are left unchanged by reflecting the path.
The bound on its maximum mass follows from its characteristic function
`1−2a+2a cos(theta)` or elementary binomial estimates. Therefore

 E_env ||K_ell^omega(x,.)−K_ell^omega(y,.)||_1
      <=C |x−y|/sqrt(ell+1).                              (L)

For x=y the bound is zero. Both sides may be capped by 2. No coupling of
opposite parity is asserted or needed. The annealed coupling calculation
does not say that two quenched paths in different sites have independent
environments after conditioning on a fixed environment; it averages those
fresh variables only after the quenched coupling has been defined.

Let P_H be a fixed H-site partition. For any probability measure mu supported
on the reachable parity sites at time m, replace its conditional law in each
cell by the conditional averaged law alpha_m in that cell, keeping mu's cell
mass. Call the replacement mu'. Null alpha_m cells also have zero mu mass
when mu=mu_m; all reachable sites have positive annealed mass. Within each
cell the initial coupling has distance at most H, so convexity and (L) give

 E_future ||mu K_ell−mu' K_ell||_1<=C H/sqrt(ell).          (M)

Moreover,

    ||mu'−alpha_m||_1=sum_(J in P_H)|mu(J)−alpha_m(J)|.    (N)

Markov kernels contract L1 distance. Finally, convexity applied to the
mixture over starting sites and (F), with the actual target partition P_N,
gives

 E_future ||alpha_m K_ell(coarse)−alpha_N(coarse)||_1
      <=rho(ell,M_N).                                     (O)

Translation of the starting site changes only the deterministic alignment
in (F), so this bound is uniform in every starting site.

Combining (M)–(O), for the actual old law mu=mu_m and
`F(omega_future)=||mu_m K_ell(coarse)−alpha_N(coarse)||_1`, we have

 E[F|F_m] <= L_(m,H)+C H/sqrt(ell)+rho(ell,M_N).            (P)

Here H/sqrt(ell)=O(N^(−1/16)), and rho tends to zero even for arbitrarily
slowly diverging M_N. By (G), the first term exceeds any fixed positive
constant only with superpolynomially small probability. All uses of (G)
are at the auxiliary scale H, never at the unknown scale M_N.

## 4. Independent moving strips concentrate the last segment

Set W=R from (H). For a path starting at x at time m, kill it on its first
time t in {1,...,ell} such that

    |X_(m+t)−x−v t|>R.

Write K^dagger for the resulting subprobability kernel at time ell. The
annealed maximal bounded-increment estimate gives, uniformly in x,

    E_future [1−K^dagger(x,Z)]
          <=d_N:=C exp(−c R^2/ell)
          <=C exp(−c(log N)^2).                           (Q)

For clarity, this is a maximal estimate over the entire segment. It follows
by applying the exponential-supermartingale inequality to centered sums of
the independent averaged increments and optimizing its parameter, for each
of the positive and negative maxima. It is not merely an endpoint estimate.

Partition the fresh environment into independent moving strips indexed by
integers k:

    S_k={(t,y): 0<=t<ell,
                    kW<=y−v t<(k+1)W}.                  (R)

Each input consists of all p_(m+t,y) in one strip that are reachable by the
finite walk. These finite input vectors are mutually independent and
independent of F_m; the strip geometry is deterministic, even when v is not
rational.

If the path from x is alive at time t, its used site satisfies
`y−v t in [x−R,x+R]`. Changing only strip S_k can therefore affect
K^dagger(x,.) only for starting sites in

    J_k=[kW−R−1,(k+1)W+R+1] intersect Z.

The extra one is harmless protection at endpoints. Put w_k=mu_m(J_k).
Only O(N) strips can matter, every J_k has length at most 10R+10, and every
integer x belongs to at most six of these influence intervals. Thus

    sum_k w_k<=6,
    sum_k w_k^2<=6 max_k w_k.                             (S)

Consider

    F^dagger=||mu_m K^dagger(coarse)−alpha_N(coarse)||_1.

It is bounded by 2. When one strip input is changed, the L1 difference
between the two subprobability outputs is at most `2w_k`, so the oscillation
of F^dagger is at most 2w_k. Conditional on F_m, the independent-input
bounded-differences estimate gives, for t>0,

 P(F^dagger−E[F^dagger|F_m]>t | F_m)
      <=exp(−c t^2/(max_k w_k)).                          (T)

One can obtain (T) directly by exposing the strip vectors successively:
each martingale increment has conditional range at most 2w_k; the ordinary
Hoeffding exponential bound and (S) apply. Constants are immaterial. No
independence of endpoint masses, or of overlapping start cones, is assumed.
The independent objects are precisely the disjoint environment strips.

By (I), except on a superpolynomially small old-environment event,
`max_k w_k<=N^(−1/32)`. Therefore every fixed positive upper deviation in
(T) has probability at most `exp(−c_t N^(1/32))` on that event.

The lost mass

    D(omega)=1−mu_m K^dagger(Z)

satisfies `E[D|F_m]<=d_N` by (Q), for every old environment. Positivity
of the kernels gives `|F−F^dagger|<=D`, and hence

    E[F^dagger|F_m]<=E[F|F_m]+d_N,
    P(D>t | F_m)<=d_N/t.                                  (U)

Both estimates are uniform in mu_m. This justifies using the killed kernel
for independence and then restoring the original unrestricted walk.

## 5. Completion and exact scope

Fix epsilon>0. Choose N large enough that
`C H/sqrt(ell)+rho(ell,M_N)+d_N<epsilon/8`.
By (G), outside a superpolynomially small event,
`L_(m,H)<=epsilon/8`, so (P) and (U) give
`E[F^dagger|F_m]<=epsilon/4`.
By (I), outside another superpolynomially small event the strip mass bound
holds. If in addition `D<=epsilon/4`, then `F>epsilon` forces
`F^dagger−E[F^dagger|F_m]>epsilon/2`. Equations (T)–(U) now yield

 P(F>epsilon)
 <= O(N^(−K)) + exp(−c_epsilon N^(1/32)) + 4d_N/epsilon

for every K. This is (A).

All steps use only fixed-law q in (0,1), delta>0, bounded nearest-neighbor
increments, and independence of fresh space-time variables. In particular,
no inverse-moment bound on p or 1−p, no uniform ellipticity, no symmetry q=1/2,
and no quantitative divergence of M_N have entered. If the environment law
is deterministic, the conclusion follows trivially as well; that case is
not being used to evade the source conjecture. Same-parity coupling and
parity-adjusted binomial bounds are explicit throughout.

The new closure mechanism is a conditional, mesoscopic final-segment
argument, not an unsupported high-moment estimate for instantaneous I_N.
The replica method and martingale exposure inputs have the classical credit
recorded in the source audit and earlier turns; the author makes no novelty
or priority claim. This full candidate must undergo separate adversarial
review before any claimed-result publication.

## 6. If interval length is read as a real geometric length

The lattice convention above uses integer M. The source does not explicitly
spell out that convention. The same conclusion also holds if P_N consists
of the intersections with Z of consecutive real half-open intervals of a
common real length M_N→infinity and arbitrary deterministic real alignment.
Only input (F) in this closure argument uses the target partition; (G) is
used at the separate integer auxiliary scale H. In the proof of (F), each
real interval has at most M+1 lattice sites, the number intersecting a
window of length 2R sqrt(n) is at most 2R sqrt(n)/M+2, and telescoping over
the parity lattice is unchanged. Thus its bound becomes

 C sqrt((R/M+n^(−1/2))
          (1+log(1+min(M+1,sqrt(n)))) ) + C/R^2.

It again tends to zero for n,M→infinity. All subsequent operations are
Markov-kernel contraction and norms on partition cells, with no integrality
requirement on this target partition. The all-scale conclusion therefore
does not depend on imposing an unstated integer-length restriction.
