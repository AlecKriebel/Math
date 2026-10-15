# PR12 artifact-integrity and current-document consistency

Final candidate proof SHA256:
`2d2e394d83ab96a6aee9b022d375fb1520499ed4aa360de51f7d1ed04f5b75ea`.
Frozen original PR head:
`19dfaccb52a7640eec79af28a778b4f22f93479a`.

**Verdict: PASS in the assigned scope. Mandatory issues: none. Completion: 100%.**
This report covers file integrity, current publication claims, and preservation
of historical labels. It does not infer mathematical correctness or priority
from any historical verdict and does not independently validate the cited
source theorem or the correction's mathematics.

## Checkable integrity evidence

`check_integrity.py` independently recomputes the hashes rather than reusing
prior pass flags. `integrity_results.json` records each target, declared and
actual digest, size where supplied, and result. The audit covers all 20
manifest/provenance JSON files then present outside `final_adversary/`, including
the current temporary replay. Its literal-hash coverage check has no omissions.

- All 273 file/canonical hash checks pass. These include current candidate
  hashes, the original snapshot and original internal manifest, every source
  and artifact manifest, root cached sources, both source-record canonical JSON
  hashes, source-PDF aliases, current metadata proof pins, and root raw/compact
  evidence-packaging hashes.
- All 21 frozen original files are byte-identical to the actual Git objects at
  the specified PR head, including the original `MANIFEST.json` and hidden
  `.gitignore`. The frozen directory exactly equals both its declared
  inventory and the Git tree; no original file is added, removed, or changed.
- The current candidate has exactly 22 files: its 21 manifest-covered files
  plus `MANIFEST.json`. Its manifest contains the corrected proof digest.
- All 11 current relative or repository-main document references resolve to
  the intended workspace artifacts. This checks destination existence locally,
  without asserting that unpublished files already exist on the public remote.
- `ROOT_EQ33_PRECISION.md` is pinned at SHA256
  `55816eb6e9b362ac4a568ddea23ce93575af022fc3c53de47dcba03e123bb1ca`
  (2347 bytes).

`original_candidate_delta.json` distinguishes the 12 identical original/current
files, nine revised current files, and the added `PRIORITY_AUDIT.md`. In
particular, all seven original `review/` files, source record/provenance, and
verification artifacts are unchanged. The originals of the revised files also
remain fully recoverable in the Git-matched frozen directory.

## Current claims and historical labeling

The current documents consistently classify the result as a credited
known-method corollary and propose `already_solved`, with fresh complete
acceptance still pending. They do not claim that an earlier paper printed the
exact composition-operator question or that this project first solved it:

- `reviewed_candidate/PROOF.md:3–7,384–416`;
- `reviewed_candidate/PRIORITY_AUDIT.md:3–4,9–10,16–20,54–68`;
- `reviewed_candidate/README.md:1–15`;
- `reviewed_candidate/SOURCE_AUDIT.md:149–163`;
- `reviewed_candidate/attempt.json:10,21,51–61` and
  `reviewed_candidate/attempt_status.json:5,18,34–43`;
- `reviewed_candidate/pr_draft.md:3–21`.

The old open-status/source-search/novelty judgments remain dated history,
expressly superseded by current reconciliation. `README.md:11–15` labels the
preserved review and upstream source metadata; `SOURCE_AUDIT.md:149–163`
supersedes its original conclusion; `review_request.md:1` labels the original
request historical. No historical mathematical verdict is used here as a
current proof premise.

The precision correction distinguishes the operator countercheck from the
published norm equality (`ROOT_EQ33_PRECISION.md:4–8`), and describes the broader
counterexample as an identity issue rather than a refutation of the spectral
conclusion (`:24–26,32–38`). Current `PROOF.md:465`, `SOURCE_AUDIT.md:165`, and
`PRIORITY_AUDIT.md:70` link this exact correction and state that the older
theorem is not refuted and the sufficient priority route avoids the identity.
The status files retain the same qualification. The frozen family reports
remain preserved; the addendum explicitly supplements them (`:3`).

An independent document-claims agent repeated its audit on the final proof
hash at `2026-10-01T13:53:31.640860+00:00` and found no mandatory issue, no
current novelty claim, and no claim that the older spectral theorem is invalid.
Its final report and 12 passing history-preservation checks are retained in
`document_claims/`, alongside its earlier dated pass on the superseded proof.

## Pin transition and reproducibility

The originally supplied proof pin began with `782a9271`. During this audit,
the root's source-precision correction changed the proof and manifest. The
parent then explicitly confirmed the final pin above. The initial byte-run
result is preserved as `superseded_requested_pin_results.json`; its single
obsolete-pin failure is historical evidence of this transition, not an issue
against the corrected final candidate.

Rerun from any directory with Python 3:

`python3 /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr12_30005897/final_adversary/integrity_consistency/check_integrity.py`

The script has no Git mutation or network action. Its outputs are restricted
to this audit directory. Passing this limited audit does not settle the
separate mathematical and source-priority acceptance checks.
