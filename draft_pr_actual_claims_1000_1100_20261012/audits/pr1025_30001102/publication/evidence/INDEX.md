# Portable evidence index and historical-stage mapping

Links are relative to this file. Current theorem and contribution are stated
in the paper, supplement and metadata. Original reports, holds, environment
paths and review counts are preserved as stage history. Those records do not
override the current package gate. No third-party source PDF/text/image bodies
are included; public URLs and retrieved-byte hashes identify inspected versions.

## Immutable submitted stage

[PR#1025](https://github.com/AlecKriebel/Math/pull/1025), head
7769e6872c3d2f4267706dc2400be3519186cf3d, problem30001102/OWR-2489-008.
[The35-file pins](SUBMITTED_PINS.json) use `snapshot_path`; interpret that path
relative to this evidence directory, e.g. `submitted/current/CURRENT_PROOF.md`.

- [Submitted proof](submitted/current/CURRENT_PROOF.md),
  [stage acceptance](submitted/ACCEPTANCE.md),
  [stage status](submitted/STATUS.json),
  [original finite contract](submitted/FINITE_CONTRACT.json).
- [Submitted exact checker](submitted/current/exact_checks.py),
  [historical independent checker](submitted/current/independent_checks.py),
  [historical checker receipts](submitted/CHECK_RUNS.json).

Original file relationships under `submitted/` are retained. Some old patch
base files and external sealed replay receipts were intentionally absent
already at submission; they are not invented here. The old UID1000 read-only
permission harness is historical and **not** replayed by the portable kit.
Use the current runner below, not historical sealed-environment scripts.

## New independent mathematics

- [Proximity/bit derivation](proximity_review_01/REVIEW.md),
  [verdict](proximity_review_01/VERDICT.json),
  [independent source](proximity_review_01/independent_exact_check.py),
  [baseline receipts](proximity_review_01/CHECK_RUNS.json),
  [five actual-source fault families](proximity_review_01/SOURCE_MUTATIONS.json).
- [Ring/hull derivation](ring_hull_review_01/REVIEW.md),
  [verdict](ring_hull_review_01/VERDICT.json),
  [independent source](ring_hull_review_01/independent_ring_value_checks.py),
  [exact runs](ring_hull_review_01/RUN_MANIFEST.json).
- [Root independent deductions](ROOT_MATH_AUDIT.md),
  [root priority adoption](ROOT_PRIORITY_ADOPTION.json).

Adjacent raw `.stdout`/`.stderr` records are unchanged. Proximity trial records
preserve two early anticipated-error corrections: the first reconstruction or
distance guard rejected the faults sooner than initially expected. Corrected
intended first-error receipts are separately labelled; reruns are not counted
as additional mathematical coverage. Neither family imported candidate code
or used historical acceptance as a premise.

## Source interfaces and bounded priority

- [Proximity source versions](proximity_review_01/SOURCE_INSPECTION_MANIFEST.json),
  [ring/hull source versions](ring_hull_review_01/SOURCE_PINS.json).
- [Bounded priority report](priority_review_01/REPORT.md),
  [body inspection locators](priority_review_01/BODY_INSPECTIONS.md),
  [source URL/hash manifest](priority_review_01/SOURCE_MANIFEST.json).

Classical proximity, partial minimization, ring lineage, LP/SFM and GLS are
credited globally in current paper, supplement and metadata. The original
question and later restricted comparators were inspected in primary bodies.
Historical absolute paths to `sources/raw` identify local inspection copies;
use public URLs to retrieve them. Their bodies are omitted for redistribution.
Priority is bounded and does not certify worldwide novelty or continued openness.

## Portable reproduction and current publication gate

- [Current runner](../run_checks.py),
  [complete24-execution receipt](PACKAGE_REPRODUCTION.json).
- [Original full output contract](../expected/ORIGINAL_FINITE_CONTRACT.json),
  [fresh proximity baseline](../expected/independent_exact_check.json),
  [actual fault definitions](../checks/SOURCE_MUTATIONS.json).
- [Current review state](CURRENT_REVIEW_STATE.json),
  [PDF layout receipt](PDF_LAYOUT_RECEIPT.json),
  [paper](../research_note.pdf), [source](../research_note.tex),
  [supplement](../SUPPLEMENT.md), [metadata](../metadata.json),
  [inventory](../PACKAGE_MANIFEST.json).

Nine baselines and fifteen actual-source faults run in normal/-O/-OO.
Complete stdout/stderr and exits match pinned expectations with exact JSON
types; faults must reject for intended mathematical reasons. All three
arithmetic sources are unchanged. The submitted exact-checker baseline is
reproduced; the historical independent UID1000 environmental checker and
remaining historical contract cases are preserved as evidence and not claimed
to be replayed by this kit. Current finite checks do not implement polynomial
LP/SFM/GLS, certify universal complexity or supply a formal/human-review proof.

[First fresh package review](package_review_01/REVIEW.md),
[verdict](package_review_01/VERDICT.json),
[unchanged copied records](PACKAGE_REVIEW_01_COPY.json) and
[two P3 repairs](REPAIR_RECORD_01.json) are stage evidence. Raw third-party
bodies, own-PDF render images and duplicate extracted input packages are omitted;
source URL/hash metadata and complete execution receipts remain. The review
manifest hashes describe that original stage, not the repaired current note.
A NEW second whole-package review remains pending. This draft is not yet
approved for immutable publication.
