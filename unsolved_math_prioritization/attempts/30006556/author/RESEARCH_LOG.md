# Research log: ID 30006556

All times UTC, 2026-10-05. Tool calls do not constitute extra proof turns.
The five entries below are the five distinct substantive approaches; source
triage and packaging are recorded separately. Completion estimates are
subjective estimates toward the universal discovery goal, not probabilities.

## Source and prior-work gate, 18:59–19:03

Requested the numeric UnsolvedMath page first; it was inaccessible in the web
reader and HTTP retrieval returned 403. Verified the supplied complete corpus
hashes against the current repository's pinned public manifest. Exactly one
record has ID30006556; its statement hash matches the catalog. The exact
research-results key is absent. The official report was retrieved, and its
printed p.69 independently matches the target. The current CDL v5 still
presents the general assertion as a conjecture. Repository main's actual
62-entry attempt directory and research logs, related-target groups, and
all-state PR searches were inspected. No target attempt was located under
30006556 or equivalent ID1949/EP-132. This is a bounded absence finding,
not a claim about deleted branches, unindexed work or private working trees.
No remote mutation occurred. Universal discovery completion estimate: 0%.

## Approach 1: total pair budget and collinear rigidity, 19:03–19:07

Mechanism: force enough distinct distances that all non-diameter classes
cannot exceed n. Proved (1), then strengthened the elementary large-line
criterion by analyzing the equality case of l collinear points with l−1
distances. A hypothetical off-line extension cannot have all those distances
because adjacent integer multiples differ by strictly less than one unit.
Result: Proposition 1. Gap: arbitrary configurations can have far fewer than
n/2 distances. No universal lower bound at the needed threshold was proved.
Universal discovery completion estimate: 5%.

## Approach 2: outer-layer accounting, 19:03–19:08

Mechanism: use the published second-largest-distance control on L1∪L2,
while keeping every occurrence accounted for. Applied the actual CDL bound,
rather than assuming a hull-only graph misses no interior pairs. Derived
Corollary 2 from h1+h2≤(n−l)+4 for a large collinear subset.
Gap: the remaining high-layer-size region is not covered, and the convex
case alone cannot control an arbitrary number of interior points.
Universal discovery completion estimate: 5%.

## Approach 3: minimum versus second-largest distance, 19:04–19:09

Mechanism: try to make a dichotomy between small-distance planarity and
large-distance hull structure. CDL already shows this dichotomy can fail.
Constructed an exact, concrete 61-point specialization: both proposed
candidate distances occur 63 times, while the diameter occurs 21 times.
Rational interval bounds certify the exact distance ordering; integer
triangular-lattice counts certify the short-distance multiplicity.
Gap: this approach cannot prove the desired second sparse distance by
selecting only these two candidates. It is blocked, not a new counterexample
to the actual conjecture. Universal discovery completion estimate: 3%.

## Approach 4: one circle plus one point, 19:06–19:13

Mechanism: a noncentral outlier has at most two incidences at each distance.
Failure would saturate every non-diameter circle graph. Proved radial
reflection symmetry, regular-polygon rigidity and two moment identities.
The resulting equations force m≤3, contradicting m=n−1≥4. Treated the
central outlier separately, including the four- and five-vertex boundary
cases. Result: Theorem 4 for every n≥5 with n−1 cocircular points.
This is a complete scoped argument, but does not solve the universal target
or establish new priority. Universal discovery completion estimate: 10%.

## Approach 5: multiple-outlier defect accounting, 19:10–19:14

Mechanism: extend the successful saturation argument to k outliers. Proved
bounds (6)–(7) when none is the circle center. For k=2 the allowed missing
incidences already invalidate exact radial reflection closure; a center
requires another exception. A stability result or another mechanism would
be needed to recover the moment constraints. No such result was obtained.
General target remains unsolved. Five approaches are exhausted here.
Universal discovery completion estimate: 10%.

## Author checks and freeze, 19:14 onward

The standard-library checker passed complete 4×4 integer-grid subset tests
for cardinalities 5–16, rational circle-plus-point controls, exact moment
algebra checks, and the rigorous 61-point extremum certificate. See the exact
counts in CHECK_RESULTS.json. These finite tests are not evidence of a
complete planar classification. No fresh proof search is delegated as an
audit. The next permitted stage is independent adversarial review of the
frozen claims and exact remaining gap. Packaging completion: 100% at freeze;
universal discovery completion remains 10%.
