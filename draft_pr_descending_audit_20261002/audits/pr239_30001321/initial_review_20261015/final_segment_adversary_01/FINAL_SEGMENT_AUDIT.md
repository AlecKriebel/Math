# Independent adversarial audit: final-segment closure

PR239 / 30001321 / OWR-4081-005; submitted head
`7f17eef77c52b2d9b2ec3ad0803c016267fa6496`.
Completed 2026-10-15 04:26 UTC.

## Result and exact scope

I find **no blocking mathematical defect in the new final-segment closure**
in current `PROOF.md` Sections 2–5. The closure proves the claimed
all-diverging-scale tail assertion from the earlier precisely stated inputs
(B), (F), and (G). In particular, it does not replace an unresolved small
scale tail bound by an equivalent unsupported statement. It uses the earlier
small-scale *expectation* bound, while the actual probability amplification
comes from independent fresh moving strips and diffuseness of the old law.

The strongest exact result established in this lane is the following
universal analytic reduction, detailed below. For the proof's deterministic
parameters, let `w_* = max_k mu_m(J_k)`, and let `d` bound the conditional
mean killed mass. Once

    C H/sqrt(ell) + rho(ell,M_N) + d < epsilon/8,

the following bound holds for every `h>0`:

    P(F>epsilon)
      <= P(L_(m,H)>epsilon/8) + P(w_*>h)
         + exp(-epsilon^2/(48h)) + 4d/epsilon.             (1)

Here `F` is the original unrestricted coarse L1 error. One may take
`d = 2 exp(-R^2/(2ell))`. All target alignments, real interval lengths,
and fixed iid laws supported in `(0,1)` are covered by this reduction.
The earlier inputs give `h=N^-1/32` and superpolynomial bounds for the
first two probabilities. Thus (1) implies the asserted tail estimate.

This audit does not assign a priority verdict or change any paper, problem,
or review status. Earlier inputs B–G were read to check their sufficient
formulation and exact application; a full independent re-verification of
all their separate analytic estimates belongs to their assigned lanes.
There is no remaining gap identified *within this closure*. The whole
candidate still depends on those earlier inputs and the exact source-model
identification, rather than on the finite controls reported here.

## Independence and materials

`INITIAL_INDEPENDENT_RECONSTRUCTION.md` was written first. It records the
initial reconstruction after reading only current `PROOF.md`, `TURN_1.md`,
`TURN_2.md`, and `check_turn3.py`. No submitted `independent_review` verdict,
other lane's opinion, or other chat was read in this audit. No external
individual was contacted. No Git, index, ref, provider, or submitted-file
mutation was performed. All authored files are in this lane's folder.

For primary-source context, I read the relevant portion of [Berger's OWR
report](https://ems.press/content/serial-article-files/46239), printed
pp. 2151–2152. It states the iid elliptic nearest-neighbor space-time result
in transverse dimension at least two and conjectures failure in dimension
one. I also checked the coupled-process discussion in [Independent
Particles in a Dynamical Random Environment](https://www.math.utah.edu/~firas/Papers/walkers.pdf),
Section 2, as context for matching walks permanently after meeting. The
quantitative coalescing bound used here is independently derived below;
no source theorem asserting the audited all-scale result is assumed.
Full third-party reading copies and provider output are excluded from the
authored artifact manifest.

## 1. Old-law concentration and its conditional role

Let `V=sum_{s<m} I_s`. Input (B) implies, for any fixed integer `k`,

    P(V>N^(1/32)sqrt(N)) <= k! C^k N^(-k/32),

because `m<=N`. Choosing `k` separately for each desired final power is
legitimate. This is one common event, not a good event resampled separately
for the different interval tests.

For each prescribed influence interval, choose a deterministic majorant
with taper length `r=N^(3/8)`. The reachable-parity binomial point-mass
bound gives mean at most

    C(R+r+1)/sqrt(m) = O(N^(-1/8)log N),

which is smaller than `(1/2)N^(-1/32)` eventually. The layer martingale has
increment bound `2/r` and, on the common event, predictable variance

    C r^(-2) V <= C N^(-7/32).

For deviation `u=(1/2)N^(-1/32)`, its Bernstein denominator is at most
`C N^(-7/32)`; the other denominator term `bu` has smaller order
`N^(-13/32)`. The exponent is therefore `c N^(5/32)`. A union over the
deterministic O(N) intervals costs only O(N), with the occupation-event
failure charged once. This establishes (I) as used.

The resulting `mu_m(J_k)` values are random, but are measurable with respect
to `F_m`. There is no assertion that these weights or their intervals are
independent. The fresh-strip concentration is applied conditionally on
`F_m`; the weights are then fixed, while the fresh environment remains a
product measure. The high-probability old event is imposed *after* obtaining
the conditional bound. This is different from conditioning an exposure
martingale on a future good event, and avoids that invalid step.

## 2. Same-parity coalescence and replacement M–P

Define a quenched pair coupling with independent transition coins before
meeting, and a common transition coin after meeting. Each marginal uses
the prescribed quenched kernel. If starts have the same parity, their
distance is always even. From distance two they can meet, but cannot swap
order in one step. Thus crossing without meeting is impossible.

Before the meeting time, sites in each fresh time layer are distinct. That
layer is independent of the pair's past; averaging makes the two signs
independent Bernoulli(q). The positive half-gap consequently has transitions
`+1,-1,0` with probabilities `a,a,1-2a`, until absorption at zero. The
parameter is `a=q(1-q)`, not the same-site replica parameter `delta`.

For its unrestricted mass function `p_t`, reflecting a path at its first
zero gives the killed kernel

    P_d(D_t=z, tau_0>t) = p_t(z-d)-p_t(z+d),  z>=1.

Holding steps are unchanged by reflection, so no aperiodicity loophole
arises. Summing telescopes exactly to

    P_d(tau_0>t) = sum_{j=1-d}^d p_t(j).

The characteristic function `1-2a+2a cos(theta)` is nonnegative because
`a<=1/4`. Its absolute Fourier integral is bounded by `C_a/sqrt(t+1)`;
one can use `1-cos(theta)>=2theta^2/pi^2` on `[-pi,pi]` and `1-z<=e^-z`.
Thus survival is at most `2d C_a/sqrt(t+1)`. Coupling gives full L1 kernel
distance at most twice survival, proving (L), including the cap at 2.

Within an H-cell, independently couple its old conditional distribution
and the annealed conditional distribution; their positions differ by at
most H and share parity. Integrate (L) against this fixed initial coupling
and then over the fresh environment. Convexity proves (M), for every old
law supported on reachable sites. The environment expectation comes after
the quenched coupling construction; there is no claim of quenched spatial
independence of two paths.

For each nonnull cell J, write

    mu'(x) = mu(J) alpha_m(x)/alpha_m(J), x in J.

Then summing absolute differences over the cell yields exactly
`|mu(J)-alpha_m(J)|`. Cells meeting the finite reachable support only at an
edge are handled by the same formula. Null alpha cells have zero old mass,
since the old walk has no support outside the annealed reachable support.
One-site cells on the opposite parity are also null. No division by zero
is needed. This establishes (N) with all clipping and parity cases.

Finally `alpha_N = alpha_m T_ell` and

    alpha_m K_ell - alpha_N
      = sum_x alpha_m(x) [K_ell(x,.)-T_ell(x,.)].

Convexity of the coarse norm and (F) bound the expectation by rho. For each
fixed start, translating the lattice alters only the deterministic target
alignment, for which (F) is uniform. No simultaneous control over every
starting kernel is required. The triangle inequality and contraction now
give (P), conditional on every old environment.

The invocation of (G) is legitimate: use the fixed exponent `gamma=5/16`,
time `m`, and `H=ceil(N^(5/16))>=m^(5/16)`. Since `m>=N/2` eventually,
superpolynomial errors in m remain superpolynomial errors in N.

## 3. Moving-strip geometry, changed path sets, and finite inputs

For each start x, define the deterministic tube condition
`|X_{m+t}-x-vt|<=R` at every integer time up to ell. At departure time t,
any still-alive path uses a site with

    y-vt in [x-R,x+R].

At t=0 this holds because the site is x. The last environment layer used
is t=ell-1; the endpoint at ell is checked for killing but uses no new
environment variable. The process has no hidden input at t=ell.

The half-open moving strips `kR<=y-vt<(k+1)R` partition every site-time
coordinate uniquely. No rationality of v is involved: v is a deterministic
real number fixed by the law, and each finite coordinate is assigned by a
real inequality. Independent iid variables on disjoint deterministic
coordinate sets give independent vectors.

To remove any ambiguity in the word reachable, one may take the input
coordinates to be all `(t,y)` with `0<=t<ell`, `|y|<=m+t`, and `y` of
parity `m+t`. This finite set is deterministic and contains every site
accessible from the old walk. It can include variables that a particular
killed path never uses. Since `|v|<1`, all `y-vt` are in `[-2N,2N]`; at
most O(N) strips intersect this set, since R>=1. No random coordinate
selection or infinite-vector concentration is needed.

Suppose two environments differ only in strip k. If x lies outside

    J_k=[kR-R-1,(k+1)R+R+1] intersect Z,

then no path satisfying x's deterministic tube condition can use a variable
from that strip. Equivalently, expand each killed endpoint probability as
a sum over all nearest-neighbor paths satisfying the tube. The summation
set is deterministic and the same in both environments. Every monomial
for a start outside J_k uses only unchanged variables. This proves exact
kernel equality outside J_k, even though changing the strip can alter the
positive-mass path support and the killed mass for starts inside J_k.
This path expansion supplies the missing detail one would need if merely
following a single realized path were thought insufficient.

For an affected start, the two killed kernels are arbitrary subprobability
measures and therefore differ by at most 2 in L1. Summing with old weights
gives the claimed `2w_k` output bound. The reverse triangle inequality
then gives the same bound for the norm F-dagger. It does not matter how
many individual paths changed or where their new killing times lie.

Here J_k has at most `3R+3` integer sites, within the stated `10R+10`
allowance. Solving the two inequalities for k shows that one integer x
belongs to at most six J_k when R>=1. Hence `sum w_k<=6` and
`sum w_k^2<=6w_*`. The collection of J_k used in (I) is deterministic.

## 4. Conditional bounded differences and mass restoration

Condition on the entire old environment. Expose the finite independent
strip vectors in any deterministic order. For each strip, the conditional
range of the corresponding Doob martingale difference is at most `2w_k`.
Hoeffding's bounded-range estimate yields

    P(Fdag-E[Fdag|F_m]>t | F_m)
       <= exp(-2t^2/sum_k (2w_k)^2)
       <= exp(-t^2/(12w_*)).                              (2)

This explicit version of (T) proves (1) with its displayed constant.
Inputs may contain many sites; their dimensions never enter the bound.
The argument does not require equal strip sizes or independence of the
walk's endpoint-cell masses.

For completeness, under the annealed law the centered increments have
range length 2. Their exponential moment is at most `exp(lambda^2/2)`.
The exponential supermartingale and a first-crossing argument therefore
give

    P(max_{t<=ell} |X_{m+t}-x-vt|>R)
       <= 2 exp(-R^2/(2ell)),

uniformly over x, by choosing `lambda=R/ell` for each sign. This is an
all-times bound, exactly matching the killing definition. After mixing
over any old law it remains a bound for `E[D|F_m]`.

Pathwise, the killed kernel is a nonnegative subkernel of the unrestricted
kernel. Their mixed difference is a nonnegative measure of total mass D.
Its L1 norm, including after coarse projection onto any partition, is
exactly D. Thus `|F-Fdag|<=D`, conditional mean Fdag is at most conditional
mean F plus d, and `P(D>t|F_m)<=d/t`. These statements hold for every old
environment, so no extra conditioning issue arises during restoration.

If the old coarse error is at most epsilon/8 and the deterministic
expected errors are less than epsilon/8, then `E[Fdag|F_m]<=epsilon/4`.
When `D<=epsilon/4`, the event `F>epsilon` forces a deviation greater than
epsilon/2 in (2). Taking the union of the two old failures, (2), and the
restoration event proves (1).

## 5. Exponent and quantifier audit

The selected scales satisfy

    ell ~ N^(3/4),   H/sqrt(ell) = O(N^(-1/16)),
    R^2/ell >= (log N)^2,
    old mean = O(N^(-1/8)log N) = o(N^(-1/32)),
    old variance = O(N^(-7/32)),
    old interval tail <= O(N) exp(-c N^(5/32)) plus overlap failure,
    fresh strip tail <= exp(-c_epsilon N^(1/32)).

Floors and ceilings change only fixed multiplicative constants once N is
large. Both the fresh-strip exponential and `exp(-c log^2 N)` are smaller
than every power of N. The final old-event constants depend on the chosen
moment order, which may depend on K. None of these claims requires K to
remain uniform or to be chosen before the theorem is stated.

The only place the *target* scale M_N enters is `rho(ell,M_N)`, an expected
error. This tends to zero along every deterministic divergent sequence,
including nonmonotone sequences and ones that diverge more slowly than
any iterated logarithm. To make the order of quantifiers explicit, fix a
tolerance; choose one fixed window parameter R_0 large enough to control
the `C/R_0^2` term in (F). Its remaining square is bounded by constants
times

    R_0 log(1+M)/M + log(1+sqrt(n))/sqrt(n),

when `M<=sqrt(n)`; when `M>=sqrt(n)`, it is bounded by a constant times
`(R_0+1)log(1+sqrt(n))/sqrt(n)`. These bounds become uniformly small for
all sufficiently large n and M. Then `n=ell` and the selected divergent
M_N eventually exceed those two fixed thresholds. This uses no lower
growth rate, no N-dependent gamma, and no comparison of M_N with r or R.
The onset N may depend on M_N as allowed by (A).

For real lengths M_N and arbitrary real alignment, target coarse
projection is still a partition map. The variance proof of (F) changes
only its maximum number of sites per cell from M to M+1. The displayed
real-length extension retains the same joint convergence. Every later
operation is a triangle inequality, mixture, or contraction on this
partition. Auxiliary H remains integer; opposite parity cells may be
empty and are already addressed above.

All fixed-law constants are finite: `q in (0,1)` and `delta>0` follow
from `p in (0,1)` almost surely. The old overlap bounds can deteriorate
as delta approaches zero; the same-parity coupling constant depends on
a, and no inverse moment of p is used. Hence a fixed nonuniformly
elliptic law causes no hidden change in the closure hypotheses.

A useful adverse limiting example confirms why the fixed-law condition
must be retained. For the symmetric two-point law `p in {e,1-e}`, every
environment has a deterministic arrow path with quenched mass at least
`1-Ne`. Its endpoint cell has annealed mass at most the largest binomial
cell mass, so the coarse L1 error is at least

    2(1-Ne-max_cell alpha_N(cell)).

If one illegally allows `e=e_N=N^-3` while `M_N=o(sqrt(N))`, this lower
bound tends to 2 in every environment. This is a counterexample to an
unasserted law-uniform version, not to the actual fixed-law theorem.
The submitted proof expressly disclaims the uniform version.

## 6. Reproduction and new falsification controls

The unmodified submitted `check_turn3.py` ran with exit code zero. Its
complete output is `reproduced_turn3_receipt.json`: PASS, **17,148 exact
assertions**, byte-for-byte identical to submitted `turn3_receipt.json`.
The script was executed with bytecode writing disabled and output directed
only to this lane's folder.

The independently authored `independent_controls.py` also ran with exit
code zero. Its receipt records **44,470 exact assertions**. It imports
nothing from the submitted code. New controls include:

- Exact arithmetic in Q(sqrt(2)), using tilts `sqrt(2)-1` and its negative,
  real cell lengths, and irrational target alignments. Strip assignment
  and tube membership use exact comparisons rather than numerical rounding.
- Every `{0,1}` assignment of each changed strip's coordinates in the
  selected finite examples, with all resulting outputs compared pairwise.
  These vertex environments stress the deterministic sensitivity claim's
  extension to closed transition probabilities; they are not invoked as
  admissible elliptic counterexamples. Outside strips retain interior
  values, including probabilities within `10^-6` of arrows.
- Direct subkernel and exact restoration identities, including 50 examples
  where the changed strip actually changed killed mass. Thus the controls
  do not accidentally test only invariant killing sets.
- A concrete excursion `0,1,2,3,4,3,2,1,0` shows endpoint-only killing can
  depend on strip `[4,5)` although its start is outside that strip's
  enlarged influence interval. Actual all-times killing removes the
  dependence. This negative control distinguishes the proof's needed
  maximal estimate from an insufficient endpoint estimate.
- Opposite-parity simple symmetric kernels have L1 distance exactly 2 for
  20 positive time lengths, confirming that parity cannot be dropped.
- Sparse old weights, clipped reachable-support boundary cells, null
  annealed cells, and one-site opposite-parity cells satisfy the exact
  replacement identity. A separate negative control places old mass
  outside annealed support and detects the violated replacement hypothesis.
- Exact arithmetic for the near-arrow lower bound above, with 27 finite
  choices whose coarse error lower bound exceeds 1, confirms the necessity
  of allowing thresholds to deteriorate as the law varies.

These computations are falsification controls with explicit finite scope.
They do not establish any infinite-time assertion. The analytic derivation
of (1), not their assertion count, supplies this lane's closure verification.

## Remaining gap and completion estimate

No counterexample or unsupported analytic step was found within the final
segment family. The strongest verified implication is (1) and its
superpolynomial consequence under inputs (B), (F), and (G). The exact
remaining dependency is independent validation of those earlier inputs
and the full source/model scope; this lane does not substitute its passing
controls for that validation. No outside input or communication is needed
for this assigned audit.

Best-guess completion of the assigned final-segment audit: **100%**.
This is an audit completion estimate, not a claim of mathematical novelty
or a declaration that the entire multi-lane review is complete.
