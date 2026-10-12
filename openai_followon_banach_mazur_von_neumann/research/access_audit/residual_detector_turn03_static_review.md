# Residual detector turn 03: independent static review

Review checkpoint: 2026-10-07T06:20:48Z. Bounded static review: 100%; scan execution and complete-article retrieval/read were not performed or certified.

Only `local_pdf_residual_detector_turn03.py` was read. No PDF, earlier mathematical manuscript, scan source, or local output was read; no detector execution, download, Git action, or source edit was performed.

Reviewed source SHA-256: `f5d376cd36f7729d02c9f1ca88660a97a77d7d9f760caaf250afa961d16060c3`.

## Pre-run finding

**Accounting blocker:** the final PNG inventory and deletion operations can raise an uncaught filesystem exception. Because `future.result()` is also unguarded, a single such exception aborts aggregate accounting before the 49-row metadata and receipt are written. Guard final inventory/stat/unlink operations, record cleanup failures, and preserve a terminal record for every submitted byte group.

## Verified structure and limits

- The selected original statuses are restricted to `no_first_page_text` and `extraction_failed`. Count and SHA uniqueness are checked; hash strings are validated before they enter filenames. The default expected count is 49, but the caller can override it.
- The resolved source path must be inside the supplied root, and the bytes are rehashed before extraction. Scope remains dependent on an authorized caller-supplied root and stable filesystem paths; a path can be replaced after validation.
- Worker count is limited to six. The total timer now starts before source loading and tool-version checks. Each worker uses the earlier of the total deadline and its eight-second deadline, and external extraction/render/OCR calls use the remaining budget.
- **A hard whole-command wall limit is not proved.** File opening, hashing reads, directory/stat/deletion calls, and final output writes are synchronous and cannot be interrupted by those checks. Rejecting non-regular input files removes the concrete FIFO/device hang case. A true strict wall limit additionally requires an outer watchdog. Report the present mechanism as a scheduling/subprocess budget.
- Text extraction requests physical page 2 first. Rendering requests pages 1 through at most 2, and OCR admits only physical pages 1 or 2. All subprocess text is captured in memory; saved fields contain counts, booleans, exit codes, or categorical diagnostics, not raw extracted page text.
- A fresh run directory prevents stale images from entering this run's evidence. The final inventory now accounts for partial images written by a timed-out renderer. Images for unresolved or candidate records are intentionally retained, so the actual temporary and metadata destinations must be confirmed ignored separately; the script itself does not enforce Git ignore status.
- The receipt excludes per-path records, root, and temporary-directory paths. It retains aggregate counts and provenance hashes. Tool versions are unsanitized first lines from the installed tools; the path-free assertion assumes their ordinary version output.
- PDF metadata can trigger a candidate, but it cannot establish complete text access. The receipt explicitly denies a global absence conclusion and OCR completeness. If "metadata ignored" instead meant that PDF metadata must not influence candidate selection, the current metadata candidate logic must be removed.

The post-run source digest should preferably be captured before workers start; otherwise an edit during execution could make the receipt identify a different source revision. This review authorizes no broader scan or source-gate conclusion.


## Repair-verification addendum

Checkpoint: 2026-10-07T06:22:34.895432+00:00. Repair verification: 100% of the requested static checks. The original review above remains tied to source hash `f5d376cd36f7729d02c9f1ca88660a97a77d7d9f760caaf250afa961d16060c3`; this addendum applies only to the operator-specified executed source hash `0229a5dfed81eb431b4dd49eec1ae49d0aaf49860949a65d630605983be7188f`, independently matched to the current source bytes.

Static inspection verifies the regular-file check before hashing; source hash captured before workers; pre-setup total timer; fresh run image directory; timeout image inventory; and `OSError` guards around final glob/stat/unlink operations. Cleanup failures now remain in the per-record fields, resolving the earlier identified accounting blocker for filesystem exceptions. The needed `stat` and `tempfile` imports are present. The receipt now explicitly records that ordinary local filesystem calls are cooperative rather than forcibly interrupted by subprocess deadlines; the earlier strict-wall-limit qualification remains.

The operator confirms that the actual derived metadata output is Git-ignored; this script-only review did not inspect Git ignore rules. PDF metadata signals are intentionally candidate-only and do not establish complete-primary-text access. No PDFs, scan outputs, or earlier mathematical material were read, and no detector execution or source edit was performed for this addendum.
