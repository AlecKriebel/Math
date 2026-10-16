# Shortest round-trip orientation: accepted partial results

Problem 3000061 / AMR-029-0061, first substantive attempt, 10 October 2026.
The accompanying independent mathematical audit accepts the scoped partial
results. The general deterministic exact polynomial-time question remains
unresolved by this work. No NP-hardness theorem for the target is claimed.

## Exact results and model

The complete report proves exact decomposition at articulation vertices;
an undirected two-edge-disjoint-path lower bound with a sound, sometimes
successful optimum certificate; a deterministic exact polynomial algorithm
when every relevant underlying block has at most one fixed arc; the cactus
specialization with arbitrary fixed arcs; a three-state exact algorithm for
valid supplied two-terminal series-parallel expressions; a four-vertex
shared-edge obstruction with unbounded relaxation gap and a zero-weight
equality limitation; and a per-orientation, value-preserving equivalence
with arbitrary mixed two-pair min-sum orientation.

The model is an explicit finite mixed multigraph with nonnegative
binary-encoded rational lengths, including zero. Parallel physical edge
identities and fixed directions are preserved. Both paths may reuse the
same edge in the same direction. Equal terminals have value zero;
nonnegative loops can be discarded for optimization; infinite distance
means infeasibility. Global strong connectivity is not required.

The series-parallel theorem requires the stated valid supplied expression
with only the prescribed terminal identifications and otherwise disjoint
child vertices and edge identities. It is no recognition claim for arbitrary
terminal placements. Failure of the cycle-chain certificate means unknown,
not infeasibility. General mixed blocks can force repeated same-direction
edges and need not satisfy either tractable hypothesis. No polynomial bound
on their compatibility states or target hardness reduction is established.

This AI-assisted manuscript is unrefereed. Acceptance denotes the
accompanying audit, not external human peer review, journal acceptance,
formal proof-assistant certification, priority, novelty, or a certification
of current worldwide openness. Prior literature is credited with its exact
undirected/weighted/randomized/feasibility scope.

## Contents

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): complete analytic partial
  proofs, construction recovery, bit complexity, obstructions and residual
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): independent analytic audit
  of the exact accepted claims and recorded aggregate supporting checks
- [ACCEPTANCE.json](ACCEPTANCE.json): partial decision, public mathematical
  file identities, preconditions, aggregate checks and explicit review limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public citations and recorded
  source hashes, sizes, retrieval and inspection history from the report
- [SOURCE_REVIEW.json](SOURCE_REVIEW.json): recorded independent source-scope
  audit, inspected portions, retrieval limits and bounded-literature caveats
- [STATUS.json](STATUS.json): precise accepted partial scope and remaining gap
- [MANIFEST.json](MANIFEST.json): all eight members and exact identities of
  the seven other files; the draft PR body independently pins the manifest

## Editorial record and exclusions

The report removes its queue-rank label, adds completed partial acceptance
and review disclosures, removes one trailing space, and replaces unavailable
program/output references with recorded aggregate metadata. Its model,
all analytic sections, and residual are preserved; the trailing-space
removal is the sole difference within its full analytic span.

The audit replaces private frozen-input bindings with the exact public report
identity, removes an omitted function name, and makes supporting evidence and
source-inspection chronology explicit. Its entire mathematical verification
is preserved apart from those recorded designation and historical-tense
changes. Acceptance retains every accepted claim, precondition, residual and
aggregate count, binds the distributed report and audit, and removes private
input/program references. Source metadata retains all public bibliographic
facts and historical limits. The source-review records are unchanged except
for added provenance fields. Status preserves partial first-attempt accounting.
No mathematical proof correction is required.

Finite checks are supplementary metadata only. The full analytic arguments
depend on no omitted executable. Programs, raw generated outputs, datasets,
copied third-party source bodies, PDFs and images, and private coordination
material are excluded. Edition preparation performs no new scholarly-source
retrieval, source-file rehash, source inspection, literature search, or
mathematical test rerun. QUEUE.md and unrelated repository content remain
unchanged. This editorial preparation adds no substantive proof response
and resets no historical accounting. No merge, release, DOI, journal
submission, or outside outreach is requested.
