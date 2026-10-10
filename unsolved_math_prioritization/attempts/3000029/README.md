# Minimum rigidity cut: accepted partial results

Problem 3000029 / AMR-029-0029. The general complexity question remains
unresolved by this work. These partial results passed the accompanying
independent mathematical audit on 10 October 2026; no hardness reduction
or novelty claim is made.

For finite simple graphs generically rigid in the Euclidean plane, with all
vertices retained, the report proves an exact rank-budgeted clique-cover
formulation of minimum edge deletion destroying rigidity. It gives exact
bounded-minimum-degree and bounded-nullity XP algorithms, including the
special case of topologically planar inputs. It disproves two structural
shortcuts: K6 defeats minimum fundamental cocircuit in one arbitrarily chosen
basis, and an infinite clique-inflated K2,q family has a unique prescribed-size
cut exposing arbitrarily many rigid components in a 2-vertex-connected residual.
The family's minimum degree and ordinary edge connectivity can be arbitrarily
larger than its rigidity-cut value. None of these obstructions is a hardness
proof or a solution of arbitrary-input optimization.

All arguments, edge cases and qualifications are retained. The classical
rank/component characterization, prior degree bound and deterministic pebble-game
oracle are credited. A narrow caveat about one printed Servatius condition is
preserved without claiming a replacement theorem or inferring author intent.
K2 has cut value one; a one-vertex input outside the stated domain has no
feasible rigidity-destroying edge deletion.

This is an AI-assisted, unrefereed manuscript. Acceptance means the accompanying
mathematical audit accepted the stated partial results. It does not mean external
human peer review, journal acceptance, formal proof-assistant certification,
or certification of novelty, priority or worldwide current openness.

## Contents

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): complete accepted partial
  proofs, exact unresolved boundary and recorded supporting evidence
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): independent analytic audit
  and carefully scoped aggregate finite checks
- [ACCEPTANCE.json](ACCEPTANCE.json): partial verdict, public report/audit
  identities, accepted scope, aggregate checks and limitations
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): classical credit, exact target and
  source-inspection history, including the narrow printed-condition caveat
- [SOURCE_METADATA.json](SOURCE_METADATA.json): bibliography, public URLs,
  historical source hashes/sizes and recorded retrieval/inspection metadata
- [STATUS.json](STATUS.json): accepted partial scope, remaining gap and limits
- [MANIFEST.json](MANIFEST.json): all eight members and exact hashes of the
  seven other files; the draft PR body independently pins the manifest

## Editorial scope

The full report's analytic Sections 2-5 and domain/edge-case statement are
byte-identical to the accepted corrected report. Audit Sections 2-5 are likewise
byte-identical. The report adds accepted status and review limits, spells out
the existing source-caveat boundary, credits all survey authors, and labels
recorded computational evidence. The audit replaces provisional package and
private coordination references with exact distributed-file identities and
historical evidence descriptions. Acceptance preserves the original partial
verdict and aggregate results while binding the public report and audit.
Source metadata retains all eight recorded identities and inspection history;
status, source review, this README and manifest are authored edition documents.
No mathematical proof correction was required.

Finite checks are supporting aggregate metadata only. Programs, raw generated
certificates or outputs, datasets, copied third-party source bodies, PDFs,
images and private coordination material are excluded. The analytic proofs
need no omitted executable. Edition preparation performed no new scholarly-source
retrieval, source-file rehash, source inspection, literature search or
mathematical test rerun.

No QUEUE entry or unrelated repository content changes. Editorial preparation
adds no substantive proof turn and resets no historical accounting. No merge,
release, DOI, journal submission or outside outreach is implied.
