# Five-approach research log

Date: 2026-10-04 UTC. Source triage began 08:41; the following five analyses
were assembled and completed at the 08:53 checkpoint. These are substantive
approaches, not a count of tool calls. All five consume the allotted attempt
budget. No additional search attempt is reserved under another label.

## Source and prior-work gate

- Catalogue access returned HTTP 403; the selected immutable dataset record and
  the exact cited primary collection were read instead.
- The full upstream prior report is only OPEN-TRIAGE: statement read, web search,
  nothing located. It contains no proof or construction to salvage.
- Live queue row was queued, 0/5. No prior attempt directory, matching PR, or
  matching branch was found. No duplicate source statement was found.
- The 2017 specialist paper supplies relevant results omitted from the
  collection's “no progress” note. The full question remains explicitly open
  there. Later targeted searches did not locate a resolution.
- Discovery completion estimate after triage: **2%**. This is a subjective
  estimate toward resolving the full target, not a probability or certificate.

## Approach 1 of 5: zero-free derivative by exponential primitives

**Mechanism.** Parametrize f'=exp(g), removing the critical-point constraint
exactly, then attempt approximation of g and its primitive.

**Work.** Proved Proposition 1's exact reformulation using a holomorphic
logarithm and the imported derivative criterion. Proved the entire locally
univalent approximants of Proposition 2 and their explicit compact error bound.
Tested the tempting inference from polynomial approximation to boundary control.

**Result.** Zero-free differentiation is completely enforced. Neither compact
approximation nor exp(g) outside A proves that its primitive belongs to A.
The unknown has become the exact pair of opposing boundary-class conditions.

**Exact gap.** Construct g with F=int exp(g) in A and exp(g) outside A, including
an infinite boundary certificate for F. Rephrasing this demand is not progress
toward its satisfaction. **Blocked. Discovery estimate: 3%.**

## Approach 2 of 5: growth control and normal-family regularity

**Mechanism.** Bound the growth of an explicit primitive or derivative, hoping
that known boundary-limit criteria supply its MacLane membership.

**Work.** Derived and proved J(f') <= 2J(f)+1+log 2 from Cauchy's estimate.
Combined it with Hornblower's criterion and the derivative criterion, carefully
handling constant derivatives. Computed the exact alpha<1 integrability
threshold for double-exponential upper bounds, and checked divergent borderline
controls rather than treating them as constructions.

**Result.** This popular way to certify F in A also certifies F' in A whenever
J(F) is finite, and therefore excludes the desired arc tract.

**Exact gap.** A candidate must lie outside both integrability conditions.
Divergent integrals alone do not supply any of the missing boundary geometry.
**Blocked. Discovery estimate: 4%.**

## Approach 3 of 5: inverse covering and singular values

**Mechanism.** Use a simple zero-free inverse covering, or a controlled
singular-value model, to obtain local univalence and an infinity tract.

**Work.** Applied the published bounded-asymptotic-value exclusion with empty
critical-value set. Completely analyzed exp((1+z)/(1-z)), including arbitrary
boundary-path finite limits, infinite valence and exact horodisks.

**Result.** The explicit near-miss belongs to A and has no critical points, but
its tract end is one point. Its finite asymptotic values are exactly T. A
bounded-singular-value construction is excluded; no-critical-points alone
cannot replace a proof of inverse continuation through asymptotic values.

**Exact gap.** Produce an arc end while allowing unbounded finite asymptotic
values, without losing local univalence or A. **Blocked. Discovery estimate: 4%.**

## Approach 4 of 5: path straightening and barrier geometry

**Mechanism.** Turn escaping arcs into closed high-modulus contours or straighten
asymptotic paths so that local univalence yields a topological contradiction.

**Work.** Proved Proposition 6: no arbitrarily high compact Jordan barriers can
surround a fixed point for a nowhere-critical disk function. The proof includes
properness, the covering step, exhaustion and Liouville. Proved Proposition 7
by integration by parts for derivative-bounded-variation paths, with no finite
path-length assumption. Applied the published two-monotone-access-point
obstruction.

**Result.** Closed contours and derivative-BV access are genuinely excluded.
The actual high arcs have uncontrolled endpoints, and local univalence supplies
neither endpoint closing estimates nor finite derivative variation. Ordinary
asymptotic access does not imply the published monotone-access condition.

**Exact gap.** Deduce enough of this stronger geometry from the stated target
alone. No such deduction was established. **Blocked. Discovery estimate: 5%.**

## Approach 5 of 5: universal radial approximation

**Mechanism.** Exploit Runge/Baire-type universal radial approximation to create
arbitrarily high arcs, then hope to retain point asymptotic values densely.

**Work.** Read the 2025 Abel-universality paper. Proved Proposition 8 directly
from the definition: high arcs follow, while every path to any one boundary
point has subsequences of images tending to every prescribed finite constant.
The proof uses crossings of scaled boundary arcs and distinguishes point ends
from general boundary paths.

**Result.** Full Abel universality decisively defeats membership in A, even
before the no-critical-point requirement is considered. No claim about its
derivative follows from universality. This route cannot supply the target by
an unchecked genericity assertion.

**Exact gap.** A much more selective approximation scheme must preserve dense
point-asymptotic paths while building the high arcs and enforcing f'=exp(g).
No compatible infinite scheme was found. **Blocked. Discovery estimate: 5%.**

## Terminal checkpoint

**Unsolved, 5/5.** The full-target completion estimate remains **5%**; the
five-approach investigation itself is complete. All proved results are partial
or reconstructions of standard consequences. The source dependencies and
limits of computational verification are explicit. Publication requires a
fresh uninvolved audit of the frozen package and a separate release decision.
No remote modification was performed during this investigation.
