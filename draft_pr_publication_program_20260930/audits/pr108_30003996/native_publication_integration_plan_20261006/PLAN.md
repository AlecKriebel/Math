# PR108: conditional native publication integration plan

This is a **nonexecuted plan and helper draft**, prepared only within this audit's
`native_publication_integration_plan_20261006/` folder. It grants no authority to
integrate native files, merge, publish, mint a DOI, update a tracker, or mutate
Git. Priority remains pending for this plan. A fresh independent pre-execution
adversary must review the final helper and configuration before commissioning it.
The helper itself can produce only a review bundle within its own folder.

## Identity and strongest supported result

The only target is numeric ID **30003996**, code **OWR-16633-013**, PR **108**,
original draft branch `dot/math-30003996`, base `main`, authenticated original
head `3526d46bf143b08e5055ffa7728c6278e9f958ea`. Processing remains restricted to
the literal incoming status `claimed_solved`; this plan does not inspect or
process the bodies of other skipped PRs.

The exact source objective is one undirected spanning tree, with its induced
whole-tree arborescence for each root, and the sum of arbitrary root-specific
arc costs. The root mathematical gate reports 100% mathematical clearance for
the direct threshold reduction after routine preprocessing and explicit guard
repairs. The effective proof is `repaired_diagnostics_v1/PROOF.md`, SHA-256
`2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393`.
The original proof remains SHA-256
`1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615`.

The original target is hardness of this aggregate objective. A future package
may describe the checked strong NP-completeness decision formulation with the
proof's polynomially bounded nonnegative costs. It must retain the exact model,
input assumptions, trivial yes/no endpoints, and dense variable relabeling.
Finite diagnostics support the written proof; they do not establish complexity
hardness or novelty by enumeration. The root gate explicitly rejects an
unclaimed global optimum/minimum-unsatisfied-clause identity. The `B >= 2`
variation is robustness of the same mechanism, not an independent discovery.
No approximation or broader optimum identity should enter the package without
a separately scoped and reviewed claim.

The source bindings are:

| Binding | Value |
|---|---|
| Dataset revision | `37e53eabe540fb458758e198be61634bd02ee008` |
| Review hash | `9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d` |
| Statement hash | `65c107bf152773ed079cc344cfcf853c4f7da15a10453ca6f7fb411bbf5aab97` |
| Imported prior report | `{}`; absence of a joined report is preserved |
| Original author effort | `2/5`, authenticated from QUEUE and two-approach prose |
| New central proof-search turns | `0` |

An actual bounded readback at **2026-10-06T05:21:27.266625+00:00** observed main
parent `94cb59e6fd58202de143f98a642181184e8bc59c`, the original PR still
OPEN/draft at its authenticated head, no target state or native attempt, and
raw/SQL/submitted statement equality. The SQL prior report and selected raw
report were both `{}`. It found **48** preexisting unrelated stale catalog
projections. These are dated observations, not future execution preconditions;
main and remote readbacks must be renewed when integration is commissioned.
See `CONTEXT_SNAPSHOT.json`, `CONTEXT_INPUT_MANIFEST.json`, and the actual
`CONTEXT_PROCESS_JOURNAL.json` for bytes, hashes, commands, PIDs, times and exits.

## Historical effort without an original structured ledger

The authenticated original incoming native inventory has exactly **15 files**.
It includes no `status.json` and no `turns.jsonl`. The original QUEUE row records
literal `claimed_solved` and `2/5`; the original prose log describes Approach 1
and Approach 2. Main's curation `queued / 0/5` is not the author's effort.

At a future native import, create one explicitly dated import baseline with
`turns_used: 2`, `original_budget: "2/5"`,
`original_structured_ledger_present: false`, references and hashes for the
original QUEUE row and prose log, and `new_central_proof_search_turns: 0`.
Append one `dated_import_of_authenticated_historical_author_count` event to the
current native history. This is an import event at the actual future time. It
does not reconstruct the dates or structure of two original ledger entries.
Do not create original-looking turn events, invent a `candidate_turn`, reset
the count, call `turn`, or charge verification/priority/package curation as
new proof search. A target state already present on main requires separate
reconciliation; the helper refuses a second import.

Preserve all 15 original files, byte for byte, under the new native attempt's
`historical_original/`, including the original proof, original checks,
receipts, review, log, source record, source manifest and SHA256SUMS. Keep their
historical assertions and limitations intact. The current clarified proof and
guards occupy the active native locations; their original README is retained
as `EFFECTIVE_DIAGNOSTICS_README.md`, alongside a new native wrapper README.
The native imported report file is the exact authenticated `{}` byte payload.

## Why the native status flow is explicit

The pinned `queue.py` has no `claimed_solved` choice in its `STATES` command
list. Its `rank` function projects a status already present in `state.json`
literally; its `assess` function preserves that state and regenerates catalog
views. Therefore the helper imports the historical count and literal status
in its private backend, then calls the **source-pinned `queue.py:assess`
function**, the same function used by the `assess` CLI subcommand. It does not
guess an unsupported `status claimed_solved` command or promote to
`verified_solved` by fabricating candidate/readiness events.

The call uses a private native ROOT plus explicit read-only SQLite replacements
for `connect` and `require_cache`. The source SQLite is opened with
`mode=ro&immutable=1`, is never copied or downloaded, and its full byte pin is
checked before and after preparation. Existing WAL/SHM/journal files cause a
stop. The helper records the precise override and actual call if it ever runs.
It never calls `sync`, writes source SQL/raw JSON, or mutates the primary
checkout. This flow itself still needs adversarial review and an actual
commissioned reproduction; offline fixtures have not validated the full
native pipeline.

## Future gates and actual publication receipts

`CONFIG_TEMPLATE_DO_NOT_RUN.json` is intentionally unusable: `template_only`
is true, commissioning is false, and the main parent, package, gates, DOI
receipt and tracker receipt are absent. Current code/source pins and the ten
effective diagnostic file pins are supplied as dated reference inputs only.
They must be renewed if any byte changes. No actual approval or DOI appears in
the templates.

Before preparing a bundle, the parent must supply all of the following:

1. A frozen package rooted in a separate PR108 audit folder, with an explicit
   manifest naming each file and its bytes/SHA-256. The manifest binds this ID,
   original head, review hash, immutable dataset revision, empty imported
   report, effective proof SHA, and Alec Kriebel's ORCID. The exact effective
   proof source must be included. No directory-wide package copy is inferred.
2. Five fresh root gate files with schema `pr108-publication-root-gate/v1`:
   mathematics, priority, package, pre-execution adversary, and final. Every
   gate binds the same exact claim, original head, current main parent, source
   hashes, proof SHA and package-manifest SHA, dated checked-artifact pins,
   historical `2/5`, and audit proof turns `0`. Priority must explicitly
   establish a substantive new contribution; uncertainty does not pass this
   publication helper. Package clearance must include metadata and attribution.
3. The pre-execution adversary's gate must bind the exact current helper SHA.
   The final root gate must bind the SHA of the four antecedent gate files and
   explicitly clear mathematics, priority, package, native scope and adversary
   review. A false/missing gate, wrong identity/hash/parent, simulation marker,
   or invalid/future UTC fails closed. Merely filling a template is not evidence.
4. An **actual** publication receipt with schema
   `pr108-actual-publication-receipt/v1`, the same head/proof/package bindings,
   `published: true`, and an actual version DOI of the form
   `10.5281/zenodo.<record-id>`. Its pinned HTTP GET metadata response must be
   the published matching Zenodo record. Its `payload_readbacks` must cover
   every package file with an explicit `individual_file` or `zip_member`
   transport, a pinned actual GET receipt and downloaded bytes matching the
   frozen package exactly. A ZIP transport additionally pins the downloaded
   archive and names each exact member; the helper checks members in memory,
   rejects symlinks/duplicates/size mismatches, and never extracts paths. This
   supports a published archive containing the package. Artifacts/ZIP transports
   and the complete package are bounded at 50 MiB; no large archive fallback is
   attempted. No placeholder DOI or fixture receipt
   is accepted. The helper consumes these artifacts; it performs no upload,
   release or DOI creation.
5. A pinned **actual** tracker readback with schema
   `pr108-actual-tracker-readback/v1`, an explicitly allowed tracker path, the
   current main parent, full tracker bytes/SHA, and one exact row containing
   this numeric ID and DOI. The helper authenticates the row against
   `git show <main-parent>:<tracker-path>` and archives the receipt. It never
   edits the tracker. No tracker path is guessed by the template.
6. An explicit fresh native assessment note, rationale, remaining-gap account,
   first follow-up and sources. The helper inherits the current assessment and
   preserves its impact/probability scores, route, decision, resolution,
   holds and clearance entries. This task does not authorize rescoring or
   clearing an existing hold. Native `assess` still checks required content and
   matching source hashes, then appends its actual assessment-history entry.

The root gate template shows the full binding fields but has all clearance
booleans false. The helper has schema checks and byte checks, not an ability
to prove human authorship, literature completeness, mathematical truth, or
remote publication from an arbitrary locally authored JSON. The parent must
authenticate the substantive reports and actual service receipts independently
before commissioning it. No present priority or publication success is claimed.

If priority instead supports a prior-result classification, this publication
route stays blocked. The parent must commission a separate source-bound
disposition; this helper must not be loosened to publish an unestablished
contribution.

## Exact affected-path selection and preservation

`AFFECTED_PATH_RULES.json` describes the exact native allowlist. A future run
creates `candidate_<config-sha-prefix>/bundle/` **inside this plan folder** and
a `CANDIDATE_RECEIPT.json` containing every proposed destination, expected
baseline byte pin or required absence, and proposed byte pin. It excludes
byte-identical global outputs. There is no export/install/stage/commit/push,
branch change, PR mutation, release, tracker write or merge entry point.

Only the nine named native global outputs may be offered:
`assessments.json`, `state.json`, `history.jsonl`,
`assessment_history.jsonl`, `catalog.json`, `ranking.csv`, `summary.json`,
`SHORTLIST.md`, and `QUEUE.md`. All remaining destinations are under
`unsolved_math_prioritization/attempts/30003996/` and are selected from the
exact 15-file authenticated original inventory, exact ten-file effective
diagnostic inventory, explicit package manifest, and the named wrappers,
gates and receipt files. No sibling target, campaign file, global tracker,
historical desk-review collection, `.git`, cache, policy, manifest or queue
source code is an install destination.

The invariants are:

- Original head, live PR head/branch/base/draft/open state, local main parent,
  and remote main parent agree before and after preparation. A changed head or
  parent stops preparation; there is no automatic rebase or overwrite.
- Raw source manifest hashes, runtime SQL revision/count/byte pin, exact
  source record, review/statement hashes, and imported report `{}` agree.
- Target state is newly imported as `claimed_solved`, `2/5`, with exactly one
  dated import event. No new central proof-search turn or original structured
  ledger is fabricated. Every existing native state remains exactly intact.
- Every other assessment remains semantically identical. Both history files
  retain their exact old byte prefix and append only the single target event
  relevant to each file. Neither old history nor historical desk reviews are
  replayed or edited.
- Native regeneration may expose stale projections such as the observed 48.
  Only drift in local status/eligibility/turn count that is fully explained by
  unchanged existing native state is accepted for diagnosis. Any unrelated
  source, score, hold or identity drift aborts. The helper then restores each
  complete unrelated baseline catalog row, including its rank and position.
  It does not treat those rows as newly audited or resolved.
- `ranking.csv` retains every unrelated record's exact bytes, including
  quoted multiline fields. The campaign table changes only this row's status,
  count, findings and DOI; all other cells, row bytes, scores and format stay
  intact. The existing shortlist is retained byte for byte because the target
  is absent from its expanded blocks; a newly present target block would stop
  for a separately reviewed overlay. Summary counts are derived from the
  preserved catalog overlay.
- Strict preservation leaves the original unrelated rank labels in place,
  potentially with a gap after the target becomes ineligible. The candidate
  is a scoped campaign integration, not a global reranking. The independent
  pre-execution review must accept this interpretation before use.
- Every input read from a manifest must be a regular file with no symlink
  ancestors. Relative paths must be canonical and contained in their explicit
  allowed root. Native destination collisions and preexisting attempts fail.
  The helper needs sufficient free space for its small native backend and
  bundle; it has no large-cache copy/download fallback.

After a genuinely commissioned future prepare, the parent must review the
complete DIFF against the pinned main parent and the affected-path manifest,
and independently reproduce the native flow. Only then may a separately
authorized, single-writer integration install exactly those paths with fresh
baseline comparisons. The parent must retain the actual committed main,
remote main, PR and DOI/tracker readbacks. A staged or committed path absent
from the manifest, or any foreign edit that arose after preparation, is a
stop condition. No program completion credit follows merely from this draft
or a private candidate bundle.

## Verification performed for this draft

The actual context collector executed read-only Git/gh/source/SQL reads and
recorded their receipts. It made no backend copy, download, native change,
Git/index/branch mutation, merge, publication or outreach. Two obsolete sparse
file reads failed before collection, and an early unscoped read-only Git status
was truncated; these are not used as evidence. Authoritative context comes
from the bounded recorded collector.

Offline tests exercise scoped restoration of 48 **synthetic** stale rows,
rejection of unrelated score/state/identity drift, campaign and CSV preservation,
multiline CSV behavior, missing/failing gate bindings, uncommissioned config
rejection, path/symlink rejection, and explicit ZIP member verification without
filesystem extraction. They run normally and under Python `-O`.
Their exact results and source pins are recorded in
`OFFLINE_FIXTURE_RESULTS.json` and `OFFLINE_FIXTURE_PROCESS_JOURNAL.json`.
They are not actual native/runtime, publication, DOI or tracker evidence. The
real `prepare` path and native `assess` function have **not** been run.

The draft deliverable is complete after its sealed final byte manifest. Its
execution readiness remains conditional on fresh priority/package clearance,
authenticated actual publication/tracker receipts, the independent
pre-execution adversary, final main-parent reconciliation, and explicit
commissioning. Mathematical clearance is the existing root's reported 100%;
this subtask has made no new mathematical discovery claim.
