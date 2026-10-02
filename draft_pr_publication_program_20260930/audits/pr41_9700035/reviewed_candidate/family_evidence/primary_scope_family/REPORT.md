# Independent primary/Poisson audit of PR41, AMR-096-0035

**Verdict: PASS_QUALIFIED_UNSOLVED_PARTIAL.** The submitted in-square law and
the full-length law with its explicitly added tail hypothesis withstand this
audit. The full original standard-axiom problem remains **unsolved**. No
mathematical repair of the submitted `PROOF.md` is required. A current source
qualification must accompany the ancillary Kahn model applicability claim;
the exact qualifications and independent repairs are in
`SOURCE_PROOF_QUALIFICATIONS.md`. This is not a novelty certificate and does
not justify a solved label, a paper, or a DOI.

## Independence, literal scope, and provenance

The original head is `292b95ca601f166e6d246e609cf7ed5ca5653e25`, base
`c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; the root-frozen snapshot manifest is
`feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6`.
Before opening the proposed proof, old review, body, or code, I read the whole
literal source record, actual nonempty prior report, provenance, and fresh
operative primary definitions and target. I sealed the interpretation at
2026-10-02T12:54:01.465896+00:00 in `LITERAL_PRIMARY_SCOPE_SEAL.json`.
The assignment and filename inventory exposed the ID, head/base and expected
audit subject; literal imported summaries exposed their interpretations. Full
blindness is not claimed. I did not read a sibling mathematical report before
this substantive conclusion.

For independent iid uniform endpoints in a square of area k, the target is
the **expected Euclidean union length of every prescribed pair route**,
including every excursion outside the square, asymptotic to ell*k. Shared
edges count once. Zero or one endpoint gives zero length. Ell is the length
intensity of the network sampled by an independent whole-plane unit-rate
Poisson process, not an optimization or Steiner constant. The underlying
feasible compatible route laws are measurable and invariant under translation,
rotation and scaling; Delta=E D, ell, and p(1) are finite. Sampling is
independent of the route process, but pair routes are not independent.

The actual imported prior misidentifies span as minimal/Steiner-type. The
submitted proof and source audit already correct that mistake while preserving
the actual prior bytes. The [2012 author manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf)
asks the original unconditional question as Problem35. The
[published EJP2014 paper](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf)
renumbers it Problem9, p38, and asks what additional assumptions, if any,
suffice. Answering the latter with a sufficient extra condition does not
settle the stronger literal dataset target.

## Independent deduction of the unconditional partial result

Write Q_n for a square of side n, S_Q(lambda) for routes between a rate-lambda
Poisson sample inside Q, and S(lambda) for the whole-plane sampled network.
Scaling c sends S(lambda) in law to S(lambda/c^2). Length scales by c and
area by c^2, hence its stationary intensity is ell(lambda)=sqrt(lambda)*ell.
This follows from the published definitions and their intensity derivation;
neither spatial ergodicity nor independent tile lengths are required.

For a fixed unit tile T and an expanding concentric endpoint square Q_r,
define a_lambda(r)=E len(S_Q_r(lambda) intersect T). Couple the Poisson sample
and the compatible route laws on their countable sampled endpoints. Every
endpoint pair enters Q_r eventually. The clipped all-pair union therefore
increases to S(lambda) intersect T. Continuity from below gives
a_lambda(r) increasing to ell*sqrt(lambda). Its expectation is finite because
the full sampled network has finite local intensity.

Tile Q_n by unit tiles whose translated Q_r lies inside Q_n. For fixed r their
count is n^2+O_r(n), including noninteger n. The local unions are contained in
S_Q_n(lambda); stationarity gives the same a_lambda(r) for each tile.
Boundaries have expected length zero because their planar Lebesgue area is
zero under the stationary expected length measure. The upper bound comes
from containment in S(lambda). Taking n to infinity first, then r to infinity,
proves

    E len(S_Q_n(lambda) intersect Q_n) / n^2 -> ell*sqrt(lambda).

For deterministic x,y, translation, rotation and scaling give
len R(x,y) equal in law to |x-y| D. Conditioning on independent sampled
endpoints is legitimate even when routes share randomness. For m endpoints
in Q_n, union length is at most the sum of pair lengths, giving

    E len(span_m) <= sqrt(2)*n*Delta*binom(m,2).

For any monotone all-pair union functional F_m (whole or clipped), take a
count N independent of an infinite iid endpoint sequence and its route
randomness. Pointwise monotonicity yields

    P(N>=k) E F_k <= E F_N,
    E F_N <= E F_k + sqrt(2)*n*Delta/2 * E[N(N-1) 1_{N>k}].

For N~Poisson(mu), the last factorial expectation is exactly
mu^2 P(Poisson(mu)>k-2), including k=0,1. Use mu=(1+epsilon)k for the upper
count sandwich, and mu=(1-epsilon)k for the lower. The relevant count tails
decay exponentially; polynomial n*k^2 factors cannot obstruct the limit.
For the lower tail, epsilon+log(1-epsilon)<0 is the strict exponential rate.
Thus, with n=sqrt(k),

    E len(span_k intersect Q_n)/k -> ell,
    liminf E len(span_k)/k >= ell.

Conditioning the count on the network would invalidate the factorization;
the proof does not do that. Endpoint independence, all-pair monotonicity and
the finite Delta bound are the essential ingredients. Compatibility supplies
consistent routes; it does not supply confinement to Q_n or its convex hull.

## Independent deduction of the conditional exterior estimate

Let Q_n^R be the square enlarged by distance R in each coordinate. The strip
Q_n^1 minus Q_n has area 4n+4 and expected route-union length at most
ell*sqrt(lambda)*(4n+4), by containment in S(lambda).

For r=2^j, an element in Q_n^(2r) minus Q_n^r is strictly farther than r from
each endpoint inside Q_n. It therefore belongs to the major-road network
E(lambda,r). Published Sections6.1–6.3 give p(lambda,r)<=p(1)/r. The annulus
area is 4nr+12r^2, giving the expected-length bound p(1)*(4n+12r).
The primary definition removes closed endpoint discs, hence uses >r. The
submitted >=r notation is harmless: circles intersect the countable jagged
straight segments in a set of length zero; alternatively fixed annulus
boundaries have zero expected length by stationary area intensity.

For R>=1, set J=floor(log2 R). The strip and annuli j=0,...,J cover the needed
near exterior, possibly with overcoverage. Since sum_j 2^j<=2R, their bound is

    ell*sqrt(lambda)*(4n+4)
      +4p(1)n*(1+log2 R)+24p(1)R.

A route with both endpoints inside Q_n that reaches outside Q_n^R has total
length at least 2R. If c=|x-y|<=sqrt(2)n and h(t)=E[D 1_{D>=t}], then

    E[cD 1_{cD>=2R}] <= sqrt(2)n*h(sqrt(2)R/n).

The independent Poisson endpoint process has expected unordered pair count
lambda^2 n^4/2. Summing the overestimate over pairs, without assuming route
independence, bounds the far exterior by

    lambda^2 n^5/sqrt(2) * h(sqrt(2)R/n).

The added hypothesis t^4 P(D>t)->0 implies h(t)=o(t^-3): use the layer-cake
identity for E[D 1_{D>t}], and h(t)<=E[D 1_{D>t/2}] to handle atoms. A finite
fourth moment is sufficient by dominated convergence. Fix delta>0 and choose
R=delta*n^2. After division by n^2, the far bound tends to zero for fixed
delta; the near bound has limsup at most 24p(1)delta. Only afterwards take
delta down to zero. No simultaneous or unjustified exchange of limits is
needed. The Poisson full-length law and the upper count sandwich, together
with the unconditional clipped lower law, give E len(span_k)/k->ell.

The little-o condition is essential to this argument. Merely h(t)=O(t^-3)
leaves a nonzero normalized far bound proportional to lambda^2/(4delta^3).
Finite first moment alone does not imply the fourth-order tail condition.
The independent scalar atomic example P(D=2^j)=(3/4)4^-j has mean3/2 and fails
that condition. This is an example about scalar laws, **not a construction of
a SIRSN counterexample**. The exact original gap is expected exterior length
o(k), or another mechanism implying the whole-length law under the original
axioms. No such deduction or counterexample has been established here.

## Primary literature and repairable ancillary qualifications

The bounded audit found no located general resolution; that is a search
finding, not proof of absence. The submitted file already disclaims novelty.
`SOURCE_PRIORITY_AUDIT.json` and `READ_COVERAGE.json` state actual coverage and
limits. The [author's problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/sirsn.html)
points to the framework and line-process constructions without giving this
general asymptotic.

For Aldous's bounded-stretch model I read the complete Proposition3.1 proof
with Lemmas3.2–3.4, containment3.3, and continuum Proposition3.8 with
Lemmas3.9–3.10 and the randomization/limit passage. Some underlying construction
proofs, including all of Lemma3.5, were not wholly recertified. For
[Kahn's2016 paper](https://arxiv.org/abs/1503.03976), I read the full operative
Theorem3.1,5.1 and6.1 proofs and Theorem6.2 summary, and inspected the relevant
printed pages as pixels. Existence/uniqueness foundations remain credited
external imports. Theorem5.1's printed conditional bounds need joint-event
bounds, and its radius must depend on T_n; the exact repair preserves the
moment range delta<gamma-1, so gamma>5 suffices for a fourth moment in the
planar model. Theorem3.1 contains reversed geometric inequality signs and a
reciprocal constant issue; the qualification note supplies a positive-constant
empty-forbidden-set time-tail reconstruction. Theorem6.1's slow length uses
speed times time, despite its printed quotient. These are ancillary source
precision repairs, not a defect in the submitted conditional theorem, which
does not depend on this model citation. Stronger conjectural moments in
Remark5.1 remain conjectural.

[Blanc–Curien–Kahn's preprint](https://arxiv.org/abs/2407.07887) has only v1
listed, dated10 July2024; publisher-deposited Crossref metadata identifies
PLMS131(1), e70070, DOI10.1112/plms.70070, online14 July2025. I read its entire
introduction/main statements and searched its full extracted text for the
target, not its entire57-page proof. Its local-geodesic results are not being
certified as a proof of the general spanning law. The two Kendall records
were read for metadata/context only; their proofs were not audited here.

Required current treatment: retain UNSOLVED status and the precise extra
hypothesis, bind `SOURCE_PROOF_QUALIFICATIONS.md` if retaining the model
applicability observation, and disclose these source-proof limits. Retain the
original historical model-selection/runtime claims as archival declarations;
their actual runtime is unverified, and no current actual model is inferred
from a historical selected-model field or PR-body assertion.

## Actual original/data and independent check executions

`audit_original_data.py` is independently authored and was actually executed
with full prelaunch source, arguments, stdout, stderr, exit code and all
read-only Git streams retained in `data_audit_actual_capture`. It consumed the
full16 original files and full201709-byte17-path diff; every original size,
SHA256, Git blob and100644 mode matched the frozen original. All8 original
JSON files were fully parsed. Both submitted Python programs were fully read
and AST-parsed but **never imported or executed**. The stored211/3809 PASS
receipts were fully parsed and their declared counts and every PASS value
checked; that is not a fresh replay of their writers or an independent proof
of the theorem.

The data audit consumed all149266659 bytes of the two pinned raw corpus files,
all15458 records and6701 reports, and compared every SQLite payload/report
join. The actual target source and nonempty prior matched whole objects; the
problem code is unique. The actual independently authored connection used
`mode=ro&immutable=1` and explicitly set and checked `PRAGMA query_only=ON`.
Target state/history entries were absent at original base, original head,
and HEAD at that execution. These are historical/native read checks, not a
claim that our worker mutated native state or froze a future current head.

The independent `finite_controls.py` V2 actually passed1326 controls with
complete source and streams retained in `finite_controls_actual_capture_v2`.
Its weighted-star union/count sandwiches, exact Poisson factorial coefficients,
strict annulus geometry, dyadic coefficients, atom handling and critical
little-o countercontrols use separate finite mechanisms. A generic correlated
count counterexample takes F_m=X for m>=2, F_0=F_1=0, X fair Bernoulli,
N=0 when X=1 and N=2 otherwise: E F_N=0 while P(N>=2)E F_2=1/4. Likewise
P(A|A)=1>P(A) disproves the Kahn conditional inference rule. Neither is a
stationary SIRSN construction. The final finite V/tree height assertion is
only an arithmetic illustration of an outside route through (0,100), not a
computational test of the SIRSN axioms or convexity theorem. No Monte Carlo or
theorem certification is inferred from these controls.

V1's actual1307-PASS capture is retained. One of its finite-mean equalities was
vacuous; V2 replaced it with exact unbounded atomic-law normalization, finite
mean, and divergent fourth-order tail controls. This strengthening affected
only our own checker. There were no failed actual executions of these own
data/finite programs. An HTTP406 source acquisition failure and browser/API
fetch limitations are preserved and distinguished from successful retries.

The first own closure checker exited1 because it inspected a deliberate
symlink fixture inside the old PR40 family's excluded scratch root before
applying that exclusion. Its complete failed capture is retained. Applying
the declared root exclusion first fixed the bookkeeping error; the corrected
actual preclosure check passed and confirmed every old included member
unchanged. `CLOSURE_CHECK_QUALIFICATION.md` records the precise limitation.
No source, proof, or old closed family was changed.

The original attempt and complete two-entry turns file agree on **2/5**
substantive attempts. This audit adds **0 new substantive target attempts and
0 native audit-attempt records**. Full resolution and novelty are explicitly
false in the original metadata. The historical25% full-target estimate is
archival, not our certificate of a percentage solved. This independent audit
is100% complete for its assigned scope; the unconditional research goal remains
open. We made no canonical, native, Git, remote, or external-human writes.

Root remains responsible for any original-writer replay, global current
qualification, final independent integration review, and merge decision.
Unsolved partial findings may be merged under the user's current process;
no paper or DOI is warranted for this unresolved target.
