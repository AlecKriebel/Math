# Initial independent source and mechanism seal

Sealed at 2026-10-02T22:09:42.546433+00:00, before any candidate, sibling-family, root interpretation, or previous review was read. Audit completion estimate: 20%. This records an audit mechanism, not an additional substantive or audit attempt and not a solution of EP653.

## Exposure ledger

Read `/Users/alec/Documents/Math/AGENTS.md` and the raw `draft_pr_publication_program_20260930/audits/pr42_2233/pinned_problem.json` only. The JSON identifies database problem 2233, EP-653. It already contains dated literature triage checked 2026-08-17; that triage exposure is disclosed, not treated as a current or independently proved status determination. Its malformed imported background and newline in `j\\neq i` must not serve as mathematical evidence.

Independently fetched the official maintained primary tracker, <https://www.erdosproblems.com/653>, on 2026-10-02. The web fetch failed with HTTP 403; a command-line HTTP fetch succeeded. Saved raw response headers, raw HTML, and a plain-text extraction under `sources/`. Viewed the statement and following background/metadata excerpt only. That excerpt contains the heading `Proof claims (2)` but no proof-claim content was examined. The full raw page is preserved but has not been read for claims or interpretations. This is source-definition checking, not a literature-priority claim.

## Literal source and exact object

The official statement defines `R(x_i)` as the number of distinct Euclidean distances to points with index `j != i`; `g(n)` is the maximum number of distinct integer values among those local counts. Ordering the counts is bookkeeping and has no effect on their set. The source asks whether `g(n) >= (1-o(1)) n`.

The intended working finite-set model uses `n` distinct planar points. The literal displayed source does not separately spell out distinctness. Repeated coordinates require an explicit convention: excluding the same index does not remove other labels at the same coordinate, so zero distance may appear. I will check candidate handling and cardinality rather than silently identify labelled multisets and finite sets.

For a finite distinct set `P`, define `D_p = {||p-q||^2 : q in P, q != p}`, `R_P(p)=|D_p|`, `S(P)={R_P(p):p in P}`, and `M(P)=|S(P)|`. Squaring is injective on nonnegative real distances, so exact squared-distance equality gives exactly the original distinct-distance counts. Rational coordinates permit exact integer/Fraction arithmetic. The multiplicity histogram of counts has total mass `n`; `M` counts its support, not its mass. Empty `P` is outside the positive-integer problem; a singleton has `R=0` and `M=1`.

For `n>=2`, `1<=R_P(p)<=n-1`, hence `M(P)<=n-1`. Computing one `M(P)` gives a lower bound on `g(n)`, not its exact value. Finite examples cannot decide the asymptotic source claim without a proved arbitrarily-large family and a quantified limit argument.

## Independent mechanism and controls

The private `exact_controls.py` constructs each local squared-distance set directly. It rejects duplicate coordinates before computing a requested finite-set cardinality. It uses no scientific helper, candidate code, imported geometry oracle, or float equality.

1. **Arithmetic progression.** For `P={(i,0):0<=i<n}`, the local distance set is `{1,...,max(i,n-1-i)}` (before squaring). Therefore `R_i=max(i,n-1-i)` and `M(P)=ceil(n/2)`. The first private run rejected my mistaken initial `floor(n/2)` guess at `n=3`; the failed source, stderr, process metadata, and correction are preserved. The corrected controls pass `n=1,...,32` with full count vectors.
2. **Powers.** For integer `q>=2`, `P={(q^i,0):0<=i<n}` has globally distinct positive pair distances. If `q^a(q^{b-a}-1)=q^c(q^{d-c}-1)` with `a<b`, `c<d`, the largest power of `q` dividing each side gives `a=c`, and then `b=d`. Thus every local count is `n-1` and `M=1`. The exact controls cover `q=2,3,6` and `n=1,...,32`. An added origin or negative/reflected arm changes the family and requires fresh checks.
3. **Circle.** The four axis points of the unit circle plus the origin have counts `(1,3,3,3,3)`, spectrum `{1,3}`, and `M=2`. The origin is not an extra point on the circle. More generally rational unit-circle parameters `t` give `((1-t^2)/(1+t^2),2t/(1+t^2))`; the squared chord distance is `4(t-u)^2/((1+t^2)(1+u^2))`. Exact rational samples with `t=0,...,n-1`, `2<=n<=16`, are diagnostic samples only.
4. **Parabola.** Points `(t,t^2)` have squared distance `(t-u)^2*(1+(t+u)^2)`. Samples with `t=0,...,n-1`, `2<=n<=16`, expose collision behavior through exact arithmetic. A collision-free generic sample yields constant `R=n-1`, which gives only `M=1`; globally many distances must not be confused with many different local counts.
5. **Small incidence controls.** A pair has counts `(1,1)`; a scalene 3-4-5 triangle has `(2,2,2)`; a unit square has `(2,2,2,2)`. The scalene triangle therefore has more local distinct distances but a smaller count spectrum than a three-term progression `(2,1,2)`.

## Planned adversarial rejection checks

Require controls actually to reject a wrong expected `M`, wrong local multiplicity, degree substituted for distinct-distance count, duplicate coordinates, and mistaken union/cardinality addition. Already executed explicit rejected mutations of a progression's `M`, the pair's local vector, the square's local vector, and duplicate cardinality. Check special dimensions, `n=1,2,3`, parity, overlapping components, exact shared distance levels, family-parameter dependence, and constants uniform in `n`. After full candidate-code reading and immutable disclosure, independently implement its constructions and compare exact count vectors, count-spectrum unions, cardinality, normalized deficits, and any proposed analytic identities.

For disjoint component coordinates, `|P union Q|=|P|+|Q|`, but local distances in the union incorporate cross-component distances; the old local counts cannot simply be unioned. Even the union of the component count-value sets has size at most the sum and may have overlap. For overlapping components, both point cardinality and set-value cardinality require duplicate subtraction.

## Proof gaps and promotion rule

The controls verify finite examples and the independently derived elementary progression/power formulas. They do not establish optimality, a sharp asymptotic bound, novelty, or priority. A candidate construction attaining a fraction `c<1` cannot alone imply the source's `1-o(1)` target. A claimed zero error at finitely many sizes does not give an eventual or uniform error bound. An arbitrary-large family with ratio tending to one would require a complete cardinality proof, local-distance collision proof, and limit proof. Any route that merely restates these unsupported central claims is blocked. No scientific candidate helper will be imported or executed before disclosure and full reading; root owns original execution. No canonical/Git/index/remote changes or external human contact are authorized for this family.
