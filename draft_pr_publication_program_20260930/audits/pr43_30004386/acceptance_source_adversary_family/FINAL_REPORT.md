# Independent adversarial review of PR43 acceptance sources

**The closed preparation needs two repairs before execution.** This review
binds `acceptance_preparation_family/PREPARATION_MANIFEST.json`, SHA256
4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9,
with 108 authored members and its literal self-excluded manifest. Neither
defect changes the mathematical result or the frozen current packet. They
are deterministic inconsistencies between the proposed administrative source
and its actual inputs or its own exact contract.

## Mandatory findings

**M1 — Correct the overlay's original snapshot filename.**
`integrate_reviewed_partial.py`, line 62, loads
`g.A/'snapshot_manifest_v2.json'`. That file does not exist in PR43's audit.
The actual original snapshot is `snapshot_manifest.json`, SHA256
88b43b2944883c0c528e02911303bf4a0370b6df44a5196f6bd515956045d23c.
The contract, input binding, original-source guard and other original-head
checks correctly use that file. After a genuine original-head merge reaches
the overlay branch, this read necessarily raises FileNotFoundError before
the canonical overlay is applied. My independent source control extracts the
literal from the syntax tree and actually attempts the named read, recording
the missing-file rejection. Replace this single literal in a separate repair
family; do not invent or duplicate a v2 snapshot as a workaround.

**M2 — Make the mirror's proposed scope exactly match its guard.**
`state_mirror_reconciliation.py`, line 40, constructs this scope:

    Incremental present accepted primary PR43; source-status correction; original0/5, no new proof turn or historical reconstruction.

`pr43_guards.py`, line 652, reconstructs the required scope as:

    Incremental present accepted primary PR43 source-status correction; original0/5, no new proof turn or historical reconstruction.

The extra semicolon after PR43 makes the complete typed proposal comparison
fail for every genuine proposal. This stops the mirror before its proposal,
plan, intent or live history/state writes. My independent control extracts
both literal arguments from their syntax trees and demonstrates their exact
inequality without importing or executing either function. Adopt one literal
consistently in a separate repair family, with the original closed family and
this finding retained. Removing the whole-object guard would lose required
evidence protection and is not a satisfactory repair.

The parent accepted both findings and requested a narrow adjacent revision.
This report reviews the original closed family only. It supplies no PASS to
the repaired family and certifies no future acceptance. A new different source
adversary and genuine ROOT inspection must review the repaired bytes.

## Scientific and acceptance scope

I read the complete five current production sources, ROOT's five-member
capture operator, execution contract, exact scientific scope, false/null
drafts, original SOURCE_STATUS, source audit and historical review, complete
ROOT proof notes and scope certificate, global source qualifications, and the
new independent whole report, verdict and complete ROOT inspection. Every
manifest member and individual dependency was also read in full, hash checked
and structurally inspected by a newly authored reader. Source syntax inspection
created syntax trees only, not executable bytecode or a code object.

The intended status is correctly **already_solved** in credited prior work:
Johnston, Kabluchko and Prochno's Theorem A, Studia Mathematica 264 (2022),
103–119, DOI 10.4064/sm210413-16-9. The literal object is a random conditional
probability law on weak P(R), with probability over a Haar unit direction,
independent Uniform[-1,1] coordinates, fixed projection dimension one and
speed N. The companion target is the whole Prohorov limit set, including
norm-one laws whose LDP rate is infinite. The Gaussian missing variance is
(1-||a||²)/3; all parameter laws have variance 1/3. Coordinate topology rather
than coefficient-norm topology, no l1 assumption, and every-N attainability
are retained. No scalar or direction-averaged LDP is substituted.

The operative qualifications preserve the variance-one prose correction,
finite-head-times-tail continuity at characteristic-function zeros, ordered
assignments 2^m(N)_m in sorting, OWR heuristic display corrections, zero/tie
lower-bound handling, and the compact-W proof that bypasses the false
unrestricted full-LDP-implies-exponential-tightness converse. Finite historical
527/current 527/independent 664 diagnostic checks are not treated as an LDP
proof. Their exact receipts and the single historical source-hash difference
are individually bound. The original research ledger is literally zero bytes,
0/5. New substantive attempts and audit turns remain zero.

This source review does not conduct a new exhaustive literature search or
certify the entire typeset journal proof. The existing explicitly bounded
reading covers the complete 12-page arXiv v2 manuscript and operative OWR
pp.411–413, with publisher metadata and abstract; the typeset proof, the full
40-page workshop volume and every foundational work are not claimed as fully
read. Full external source bodies were byte-bound here; I do not promote a
mechanical body read into a new personal full-proof certification. No new
project solution, novelty, priority, paper, DOI, tracker, release or human
referee claim is authorized by this source-status correction.

## Independent full-input checks and actual controls

The successful new input reader was actual child **32160**, UTC
2026-10-03T01:43:44.893710+00:00 through 01:43:46.900095+00:00, exit 0.
It recorded 1,866,043 demands and 1,588 complete reads totaling 376,265,941
cumulative bytes, including repeated individual bindings. It checked:

- The preparation's 108 members plus manifest; frozen current packet's 347
  members plus manifest; all 274 anchored dependencies; the new whole family's
  30 members plus manifest; all 756 separately named foreign input identities;
  all 16 original files and their candidate archive copies.
- Exact recursive files and directories, no symlinks or special nodes, complete
  hashes and typed byte counts, and literal full S_IMODE 0444 for each frozen
  closure. Full permission bits include sticky, setgid and setuid bits.
- Every critical JSON/JSONL body with duplicate-key and nonfinite-number
  rejection, explicit empty original ledger, saved prior {}, and the exact
  equality between ROOT's complete nested whole verdict and the real verdict.
- Four historical native bodies from immutable Git head
  c61dc0cb572de281b871264819c8b80d647d0373, with actual saved Git query PIDs,
  complete stdout/stderr and exact regular 100644 blob paths. These match the
  actual dated freeze pins. The other 752 outside identities are checked live.
  Historical bodies never authorize present shared state.

The reading observed actual main head 861e32d873763c47c5bbf39ed30b84f3464f95a5
before and after its operation. This is a dated observation, not a future
integration preimage. No source reader writes the repository's native state,
queue, inventory, index, branch or remote.

Independent controls were actual child **35798**, UTC
2026-10-03T01:48:06.951804+00:00 through 01:48:07.235498+00:00, exit 0:
4,724 predicates and 40 negative controls, including the concrete M1/M2 source
witnesses. These use only new handwritten code and private fixtures. The work
checked strict typed schemas, duplicate/nested duplicate JSON, NaN, infinity
and numeric overflow; nonempty/whitespace/invented JSONL ledgers and boolean,
float, string or wrong original budgets; every one of the 4,096 permission
patterns and five real private files with exact permission observations;
symlink ancestors and final nodes, missing components, escape-and-return,
non-directory traversal, final directories, private Git components, doubled
separators, backslashes and NUL; existing-target regular-file publication; and
actual macOS RENAME_EXCL directory refusal/success with private targets.

Separate complete typed inventory and native-plan fixtures checked preservation
of all 179 other inventory entries, all 33 prior states, the complete history
prefix, exactly one present zero-turn event, unchanged 41 consumed turns,
33 primaries and one old duplicate. These fixtures are explicitly synthetic
contracts for the future post-PR42 state; they certify no actual PR42 completion.
Mutants with extra events, lost prefixes, changed old states, boolean counts,
unknown fields and invented new turns were rejected. Whole-queue inverse
replacement verified only Status/Findings change; original Turns, Chat/DOI
and every other byte remain exact. Proposed native code was read, never run.

The source requires genuine current ROOT approval outside its closed packages,
complete exact references, actual final capture PID/argv/UTC/stdout/stderr,
prelaunch source and reviewed operator, fresh main/native13 authority and
full modes, exact original Git head/base/diff/archive and no prior selected
native event. Full saved prepush fields derive from the actual merge tree,
parents, queue, overlay and remote; a hash alone is insufficient. Saved native
plans are wholly rebuilt with only the two exact historical state/history
read paths substituted, then the module Path binding is restored. Prior
original ledgers are byte-bound without inferring research usage.

All three future PR42 predecessor references remain null in the source-only
drafts. Production guards require their genuine completed literal PR42 files,
the entire predecessor post object, ROOT's entire inspected post and correct
UTC ordering. PR41 or invented future receipts cannot substitute. The required
current completed bindings and ROOT execution remain future work, even though
the mathematical current/whole gates were completed independently earlier.

## Preserved failures, ownership and result

The preparer's original authoring, failed token repair, partial source state,
corrected revisions, final literal repair, own controls and source closure
captures are preserved and individually checked. Historically invalid newline
drafts remain archival; the five current sources parse as syntax trees.
The prior current freeze's 40-command prefix and actual final 42-command index
retain their different meanings. Old PASS, model/reasoning/deadline, access and
human-review claims are dated history, not present acceptance authority.

My initial own reader **31301** failed while trying to syntax-parse an expressly
archived invalid historical drafting literal, after full binding reads. That
was an overly broad own inspection predicate, not a third production defect.
Its source, complete actual capture and stderr remain. A distinct V2 reader
explicitly records that archival SyntaxError and successfully checks the current
sources. My initial own control **35357** failed before creating private fixtures
because its AST export enumeration omitted tuple-unpacked ID/CODE/PR. The actual
production definitions exist. Its source and complete failure remain; the
separately authored V2 control corrects that enumeration. No failure is relabeled
as a PASS, erased or backdated.

Only this family's own programs, reports, fixture bodies and actual capture
records belong to its self-only closure. All outside members are individually
excluded and bound as inputs; no foreign PDF, full source derivative or raw
cache body is copied into authored research. Saved project Git-query streams
are attributed evidence, with no novelty claim. Private special permission
observations are dated before final closure, which freezes all retained files
to literal 0444; Git does not preserve these complete worktree bits.

Mandatory corrections: **M1 and M2**. Optional refinements: none required by this
review. Acceptance-source review completion is 100%; new discovery 0%.
The original closed source has **no execution approval**. The mathematical
already_solved classification remains supported by its separately bound prior
theorem and audits. After narrow repairs, a new different source review and
genuine ROOT approval are required before final reconciliation, original-head
merge, publication and native mirror verification.
