# Independent adversarial audit: Poisson dynamics and invariant-law uniqueness

PR246 / 9700040 / AMR-096-0040. Audit date: 2026-10-15 UTC. Native head supplied by the parent and revalidated there: `0b4db59eb5515f2d90d8b8df33b6b729b78b48f1`. The original twenty-file attempt is the immutable snapshot under `initial_review_20261014/submitted/unsolved_math_prioritization/attempts/9700040/`.

**Dynamics-family disposition: verified, with no mandatory correction to the submitted proof.** This clearance concerns the process construction, stochastic identification, and uniqueness in Sections 1 and 3, plus the exact count-event link needed by Section 4. It does not clear the determinant weights, error certificate, qualitative meaning of explicitness, historical priority, or publication status. Those require the other fresh audit families and the later priority phase.

The strongest exact claim independently verified here is: on the state space of strictly positive, strictly ordered finite coordinates, the submitted generator has a pathwise unique nonexplosive driving-Poisson realization and a unique invariant probability. These invariant laws are consistent in the number of coordinates and are the finite projections of a unique invariant probability on strictly increasing infinite sequences diverging to infinity. That probability is obtained from quadrant-Poisson longest-chain inverse levels. Each fixed finite projection, started from any initial probability independently of future driving events, converges to its invariant law in total variation by almost surely finite synchronous coupling. No uniform mixing rate or global finite-time coupling of infinitely many coordinates is asserted.

## 1. Independence, exact inputs, and primary source authentication

I read the submitted `PROOF.md` first. The independent derivation was sealed before reading either prior independent-review verdict file, at `2026-10-15T03:38:24.369634+00:00`, in `INDEPENDENT_DERIVATION_20261015T0340Z.md`, mode 0444, SHA-256 `ef4c67a732cc82845e72e3a3235c32a90faab685fcce6fe78837fce70a15215e`. The filename uses a rounded timestamp; the precise receipt time is authoritative. `INDEPENDENCE_RECEIPT.json` records the inputs read before sealing. The old reviews were consulted afterward only for comparison, documented separately.

All twenty original files independently match both their supplied SHA-256 hashes and native Git blob object identifiers, recomputed directly from bytes without using Git. `INPUT_BINDING_RECEIPT.json` records all identities. The head, PR state, and queue classification are inherited from the parent's intake and live revalidation; this family made no independent live GitHub fetch and no provider mutation.

The [original problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html) specifies positive ordered finite coordinates, drift equal to position, and unit Poisson nearest-right jumps. It explicitly discusses consistency as the number of coordinates varies. The authoritative finite-coordinate paragraph, rather than its introductory discussion of another Hammersley system, is the target here.

The [unfinished 1993 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf), dated July 8, 1993 on their title page, contain the model and transformation discussion on printed page 36 and synchronous-coupling Lemma 33 on printed page 37. Both pages were directly rendered and visually inspected. Source text extraction was used only as an aid. The notes' existence and coupling statements are not accepted as substitutes for the proofs below.

Both directly retrieved sources match the submission's exact pins:

| Source | Bytes | SHA-256 |
|---|---:|---|
| problem page | 3,171 | `1a208ce3851d65022ecc998bedcfe97fd8afe5240e52cec3172aef0d9a89b2b6` |
| 1993 notes | 379,915 | `7d7457424b2f1422e30900692e1626b9fe07d172e8b1cfe12c3470f418ac717c` |

The retrieval receipt includes final URLs, status, headers, retrieval timestamps, byte sizes, and hashes. Whole third-party files, extracted text, and page renders are private reading copies and are excluded from the public authored manifest. No outside person was contacted, and no outreach draft was prepared.

## 2. Finite rectangle construction and the inverse-level count identity

Let a finite list of distinct positive values arrive in increasing time order. For each positive integer i, let a_i be the minimum possible terminal value of a strictly increasing subsequence of length i, whenever one exists. These minima are strictly increasing in i. Suppose a new value u lies between a_(i-1) and a_i, taking a_0=0 and allowing a new final index. It extends a length i-1 subsequence and improves exactly the terminal minimum for length i. It cannot terminate a length i+1 subsequence, because the old minimum terminal value for length i is greater than u. The other minima are unchanged. Hence the update replaces the first top strictly greater than u, or appends u when none exists.

An arrival with u>M cannot change any pile top at or below M. Deleting all arrivals above M therefore leaves exactly the same pile tops inside (0,M]. Also, later time arrivals cannot affect an earlier time slice. Consequently constructions from finite rectangles are exactly consistent under increasing the spatial or temporal bound. One never needs a time ordering of all the infinitely many quadrant points in a positive time strip.

For a unit quadrant PPP, define L(x,t) as the longest strict northeast chain in (0,x] times (0,t], and

    Z_i(t) = inf{x>0 : L(x,t)>=i}.

The finite identity proves

    #{i : Z_i(t)<=x} = L(x,t).

The infimum is attained. Any finite rectangle containing an i-chain restricts the first level crossing to one of its finitely many spatial coordinates. Each crossing raises the maximum chain length by at most one, because only one new rightmost point is added and deleting that point from a chain reduces its length by at most one. Distinct Poisson spatial coordinates therefore imply distinct Z_i(t).

For t>0 and fixed i, divide (0,t] into i positive-height time strips. Each strip has points arbitrarily far to the right almost surely; select a point to the right of its predecessor in each successive strip. This yields an i-chain in a finite rectangle and proves Z_i(t)<infinity. Every bounded rectangle has finitely many points, so Z_1(t)>0 and Z_i(t) tends to infinity as i grows. To make these statements simultaneous in t, first use a countable set of rational q,T with 0<q<t<T. Monotonicity gives Z_i(t)<=Z_i(q)<infinity and Z_1(t)>=Z_1(T)>0; local counts at t are bounded by those at T. Globally distinct Poisson spatial marks give distinctness at all times.

Thus every finite coordinate has already entered from spatial infinity at every positive ordinary time t. At t=0 there is an empty local configuration, but at any positive t there are infinitely many coordinates, all finite and locally finite. This entrance construction does not insert particles into a fixed finite projection after a positive starting time.

## 3. Unit intensity, adaptedness, generator, and finite nonexplosion

Use the exact transformation

    x=uv, s=log v,  u=x exp(-s), v=exp(s).

The inverse derivative matrix is

    [ exp(-s)   -x exp(-s) ]
    [    0         exp(s)  ],

whose determinant is +1. The transformed field is therefore a unit-intensity PPP on positive space times all real s, with no missing time-dependent factor.

Set Y_i(s)=exp(s)Z_i(exp(s)). Between relevant events Z_i is constant, so dY_i/ds=Y_i. At an original event (u,v), every coordinate is multiplied by the same positive v; the nearest coordinate strictly to the right of u is exactly the nearest transformed coordinate strictly to the right of uv. Its new value is uv. The spatial order is preserved.

The natural filtration contains all original points with v<=exp(s), equivalently all transformed points with time at most s. Every current coordinate is measurable from those past points through finite rectangle constructions. Future transformed PPP points are independent of that sigma-field. Therefore the construction is adapted and has the claimed time-homogeneous Markov transition kernel. A random initial configuration must be independent of future driving events, or be measurable from the past in an equivalent adapted construction. Allowing an arbitrary anticipative dependence on future noise would change the problem.

For the first k coordinates, events above Y_k do nothing and events below Y_k are handled entirely within that projection. This proves autonomy. Given initial x in E_k at s_0, downward jumps and positive drift imply

    Y_k(s_0+h) <= x_k exp(h),  0<=h<=T.

All effective events lie in the finite rectangle (0,x_k exp(T)] times [s_0,s_0+T]. Only finitely many occur, yielding nonexplosion and a pathwise unique event construction. With a random x_k finite almost surely, use conditioning or the union of events x_k<=m. The submission's word "deterministic" for this bound is literally correct after fixing the starting configuration; it does not obstruct random starts.

The generator is consequently

    Lf = sum_i x_i partial_i f
         + sum_i integral_{x_(i-1)}^{x_i} [f(x with x_i=y)-f(x)]dy,

for smooth functions in an appropriate local or compactly supported domain. The total effective jump rate is sum_i(x_i-x_(i-1))=x_k. There is no finite-k immigration term.

The consistent finite projections also give a well-defined process from any state in E_infinity. On a finite horizon, the number of particles in (0,M] can increase only at an event there, because the deterministic motion is to the right. Thus

    N_s(M) <= N_0(M) + Pi'((0,M] times [0,T]),  0<=s<=T.

The right side is finite almost surely. The infinite sequence remains locally finite, so coordinate consistency is compatible with the stated infinite state space, not merely with a formal sequence of finite generators.

## 4. Direction of the stationary shift

Let S_a map a quadrant point (u,v) to (exp(a)u,exp(-a)v). It preserves area and the quadrant. The inverse levels in the transformed sample satisfy

    Z_i^(S_a Pi)(t)=exp(a)Z_i^Pi(exp(a)t).

Therefore

    Y_i^(S_a Pi)(s)
      = exp(s)exp(a)Z_i^Pi(exp(a)exp(s))
      = Y_i^Pi(s+a).

This checks the sign directly. Since S_a preserves the PPP law, all joint distributions across finitely many times and indices are invariant under a common shift a. This is strict stationarity of the process. At s=0 the one-time count function is exactly L(x,1).

A wrong spatial sign would fail even for the first particle. Since P(Z_1(t)>z)=exp(-tz), the candidate gives

    P(exp(s)Z_1(exp(s))>y)=exp(-y).

By contrast exp(-s)Z_1(exp(s)) has survival exp(-y exp(2s)), nonconstant in time; its drift between jumps is negative and the event intensity would be exp(2s). This negative control distinguishes the exact candidate transform from superficially similar formulas.

## 5. Synchronous coupling, random stopping times, and moving strips

Take two finite-k initial configurations, with no coordinatewise comparability assumption, and use the same future event field. Equality of an initial segment persists because that segment is autonomous. Define successive stopping times tau_i at which the first i coordinates have coalesced, starting with tau_0=0. These can be taken as first equality times or as the recursively constructed coalescing event times below. Paths have finitely many relevant jumps on bounded intervals, and equality cannot first appear between events unless it was present initially, so the stopping-time claim follows from adapted finite-event evolution.

At tau=tau_(i-1)<infinity, put

    a=min(X_i(tau),X'_i(tau)),
    b=X_(i-1)(tau)=X'_(i-1)(tau),

with b=0 for i=1. Strict order gives a>b. Before the i-th coordinates coalesce, a jump of the smaller coordinate can only occur at an event above the common lower neighbor and below both i-th coordinates. That event moves both to the same location, which would coalesce them. Thus on noncoalescence the smaller i-th coordinate remains a exp(h). The larger one can jump and remain larger; it cannot cross the smaller one without meeting it. The common lower neighbor can jump, but only downward, and is bounded above by b exp(h).

Every point in the future strip

    A_H={(y,tau+h): 0<h<=H, b exp(h)<y<a exp(h)}

therefore forces coalescence if it has not happened earlier. The lower neighbor need not remain fixed. Its downward jumps only strengthen the strip inclusion. The strip's area is

    |A_H|=(a-b)(exp(H)-1).

Condition on the sigma-field at tau. The strict future shifted PPP is independent unit-intensity noise by its strong Markov property, while a and b are now fixed. Hence

    P(tau_i-tau>H | F_tau)
       <= exp(-(a-b)(exp(H)-1)).

This tends to zero. The conditional argument is valid for random tau, random gap a-b, and arbitrary random adapted initial states. It does not replace a random strip with an unconditioned deterministic one. The PPP strong Markov property follows, if needed, by approximating tau from above by dyadic stopping times on bounded rectangles and exhausting space. The event that defines tau is already consumed; the strip uses strict future times.

Induction yields tau_k<infinity almost surely for every fixed k. In particular, the same argument covers crossing configurations: it only compares the current pair at the next unmatched index after lower coordinates have already coupled.

To obtain uniqueness without a separate recurrence theorem, start independent samples of any two finite invariant laws and use common future noise independent of both. For each t the total-variation distance between their marginals is at most P(tau_k>t), which tends to zero. Invariance keeps these marginals fixed in t, so the invariant laws are equal. Coupling any initial law against the stationary law proves total-variation convergence in the same way. No finite mean of initial coordinates is required.

On E_infinity, every invariant probability has these unique finite invariant marginals because each finite projection is autonomous. Coordinate cylinders determine the Borel law on this countable-coordinate state space. Thus the infinite invariant law is unique. There is no inference of one finite time when every coordinate has coalesced.

## 6. Boundary conventions, count-to-LIS link, and low-index checks

The quadrant PPP is countable on a compact exhaustion. Almost surely all spatial coordinates are distinct and all time coordinates are distinct. A fixed deterministic spatial or time line has zero PPP mass. The relevant moving boundary is the pre-event particle location, which is predictable; the compensator of events on its graph is zero because each spatial section is a singleton. Post-jump equality with the event position is, of course, part of the update and is not a forbidden boundary event.

The inverse-level definition gives the exact event equivalence

    {Y_r(0)>x} = {L(x,1)<=r-1}.

The closed upper spatial edge in L and strict survival inequality are compatible even at an actual particle coordinate. No approximation by continuity is needed for this equivalence. At a fixed deterministic x, the probability of a particle exactly at x is zero, because its coordinate would have to be a PPP spatial mark on that fixed line. Thus all deterministic query thresholds are continuity points.

An independent one-particle semigroup check is available without any partition formula. Starting from x at time zero, every event at (y,s) contributes possible terminal upper bound y exp(t-s). Therefore

    P(X(t)>z | X(0)=x)
       = 1_{x>z exp(-t)} exp(-z(1-exp(-t))).

Averaging x~Exp(1) gives exp(-z), exactly stationary. Independently, for p>=0,

    L x^p = p x^p - p x^(p+1)/(p+1).

Its expectation under Exp(1) is zero by the factorial moments. The provided control checks p=0 through 12 exactly and checks the semigroup identity at several times and thresholds. These are calibrations; the full all-k theorem is supported by the preceding analytic construction and coupling.

## 7. Adversarial findings: mandatory versus optional

**Mandatory findings for the submitted proof: none in this family's scope.** No central difficulty is transferred to an unsupported equivalent claim. The required randomness, path construction, invariant existence, and coupling uniqueness have independent checkable proofs above.

Optional clarification 1: explicitly state E_infinity={0<x_1<x_2<... and x_i tends to infinity} when asserting infinite invariant uniqueness. If one enlarges the state space to all locally finite configurations, including the empty state, uniqueness is false: the empty configuration remains empty and gives another invariant law. Finite-k stationary configurations also remain finite under the no-insertion rule. The source and candidate's indexed infinite process already select the intended state space, so this is a boundary clarification rather than a defect.

Optional clarification 2: the phrases "deterministic bound" and "strong Markov" may be expanded for random starts. The correct statements are the conditional bound at a fixed starting configuration and the conditional moving-strip estimate at a stopping time. The candidate uses them correctly; the expanded versions above make the dependencies explicit.

Optional clarification 3: do not transplant the 1993 source's displayed scaling or numerical mean-time bound into a future exposition. Direct inspection of printed pages 36-37 reveals that those particular displays are unsafe. The candidate derives its own correct transform and strip bound, so its use of the notes for classical credit is sound.

Here is an explicit falsification of the printed mean bound. For k=1, start the coupled copies at a=0.01 and A=100. They meet at the first point below a exp(s), so

    P(T>h)=exp(-a(exp(h)-1)).

Consequently E[T]>=P(T>1)>49/50>100/9999=1/(A-a): use e<3 and exp(-z)>=1-z to get the fully exact contradiction. The displayed decimal values P(T>1) approximately 0.982964 and 1/(A-a) approximately 0.010001 are diagnostic only. A sharper rational factorial-series certificate in the independent control also verifies a contradiction factor exceeding 98. The corrected strip gives the valid bound E[T]<=1/a here, or generally E[tau_i-tau | F_tau]<=1/(a-b), and the sharper conditional tail already derived. The source-level error does not propagate into the submitted proof.

## 8. Reproducibility and limits of the finite controls

Run `python3 independent_dynamics_checks.py --output INDEPENDENT_CHECKS.json` from this folder. The script uses only the Python standard library and imports no submitted implementation. It checks every permutation through size eight, every prefix, and all integer spatial cutoffs against an independent quadratic-time terminal-minimum recurrence. It also checks exact rational transformed-event paths, finite projection autonomy, a forced coupling after lower coordinates jump, and many crossing initial configurations with intermediate coupling-stage states.

`INDEPENDENT_CHECKS.json` records the exact counts, seed values, script hash, analytic one-particle controls, and the source-mean-bound counterexample.

| Final control | Verified count |
|---|---:|
| permutations through size eight | 46,234 |
| all prefixes checked | 409,113 |
| rectangle restrictions and matching count identities | 3,628,799 each |
| exact rational post-initial transformed events | 60,000 |
| finite projection autonomy comparisons | 240,000 |
| crossing initial pairs among 1,000 exact path trials | 660 |
| intermediate coupling-stage starts | 4,484 |
| common lower-coordinate jumps during those stages | 1,882 |

 `CHECK_DEVELOPMENT_LOG.md` preserves the first run's failure: a generated spatial value duplicated an initial value, entering a null boundary case outside the proof assumptions. The fixture was corrected to keep all spatial marks distinct. This did not change the candidate or conceal a valid-input counterexample.

These finite controls cannot prove a Poisson strong Markov theorem, all-time stationarity, or all-index uniqueness. Their role is to catch sign, ordering, boundary, projection, and moving-strip mistakes. The analytic argument supplies the infinite and stochastic steps. Determinant counting and certificate verification remain deliberately outside this clearance.

## 9. Final narrow conclusion and remaining gap

The candidate's stationary construction really realizes the source finite-k drift-jump process, its future driving field has the correct independent unit intensity, its first k coordinates are autonomous with no immigration, and the coupling proves uniqueness for each finite k and then the intended infinite law. There is no remaining stochastic-dynamics gap identified in this audit.

The overall PR's remaining gates are the other independent mathematical families, the source's qualitative explicitness requirement, and historical priority. This report makes no novelty or priority claim and does not independently promote `claimed_solved`. No source, queue, PR, tracker, Git index/ref/checkout, or provider publication was changed.
