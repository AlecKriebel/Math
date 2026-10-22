# PR239 portable verification preparation

Completed only the assigned verification subtree. Its93 positively selected files total354693 bytes, including the19265-byte MANIFEST.json. All files are0444. The32 historical input files preserve their native blob pins; all family payloads/manifests/seals and the priority-v2 selection remain exact.

The actual clean relocated command used --with-sympy and ran each selected checker once: the8-script standard-library subsuite passed376020 assertions, and the optional SymPy1.14.0 checker passed486, total376506. It returned exit0 with empty stderr in27.113147 seconds. This is an actual combined run with a separately accounted standard-library subsuite, not a claim that the no-option command was separately executed. The runner's default selects precisely those same8 standard-library checkers.

The portable runner authenticates the finite tree before any checker or optional dependency, then copies only reviewed source bytes to owned temporary folders. Replica output JSON files remain temporary. Exact archived absolute-path replay drivers are provenance only, never executed by the portable runner. New validation uses actual JSON schemas/counts/properties, not time/path-dependent byte comparison.

The source and relocated93-file trees were rehashed after execution and unchanged. Actual execution receipts, log, source selection, index and seal remain outside verification/ to avoid self-hash cycles. No parent manuscript/README, source snapshot or original family artifact was edited.

Finite assertions include repeated parameter instances and excluded-hypothesis controls. They do not establish the infinite-time theorem, priority or historical reviewer/source-access independence. The parent must complete whole-package review and publishing steps.
