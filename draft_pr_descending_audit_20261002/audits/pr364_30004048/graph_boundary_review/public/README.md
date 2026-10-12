# Reproduce the graph/boundary audit

Start with FINAL_REVIEW.md and the two sealed analyses. GRAPH_CONTROLS.json is the complete stdout of check_graph_boundaries.py. A standard Python3 interpreter suffices:

    python3 check_graph_boundaries.py

Compare all output bytes with GRAPH_CONTROLS.json, retaining empty stderr and exit0. This checks finite controls; it does not replace the universal proof or compute exact psi values/order.

The frozen target is under `snapshot/unsolved_math_prioritization/attempts/30004048` at PR head0d07b06537aded3e76f5a71908f3546df574a691, baseefd29c05204703acca9a0860812f54b94fae54b1. FROZEN_EVIDENCE.json binds42 actual scope paths, all modes/blobs,135 nested entries,30 authorremote bindings and three first-introduction checkpoint commits. SOURCE_RECEIPTS.json identifies the three freshly fetched primary editions, private source/render hashes, exact retrieval/extraction/render recipes and read scopes. COMMAND_RECEIPTS.json contains command metadata through evidence verification; its full streams are private. Logical stream hash means SHA256(`STDOUT`+NUL+stdout+`STDERR`+NUL+stderr).

For a new audit BEFORE public closure, the writing acquisition driver check_frozen_evidence.py captures binding checks from a local Git repository and frozen snapshot:

    python3 check_frozen_evidence.py --audit /absolute/audit --repo /absolute/repo --capture-name new_evidence_capture

This is a **writing acquisition driver**, whose Git operations are read-only. It creates its own private capture directory and lossless gzip receipts. Do not launch it after this audit's public closure or use it as a standalone read-only verifier. Use a fresh capture basename only for a new, unclosed audit. `--require-private` additionally requires original private PDFs, recorded replay streams and byte-identical replay copies. Without those materials it reports NOT_CHECKED_PRIVATE_ABSENT and makes no new source/original-output verification claim. A later independent reader can execute the literal underlying Git argv in COMMAND_RECEIPTS.json from an external/root capture namespace and compare complete stream hashes; the closed packet is inspected by check_public_namespace.py without launching the acquisition driver.

The three author programs and frozen old-review program were copied with all adjacent certificates into private/replay and executed under the existing Python3.14 runtime. Every complete stdout equals its frozen CHECKS.json bytes. The public frozen programs can be copied with their certificates and rerun from their directory to regenerate this evidence; no package installation is needed.

The public namespace is precisely this public directory. PUBLIC_MANIFEST.json will cover every file here except itself after ROOT's preseal review. check_public_namespace.py validates that exact namespace, both analysis seals, the public receipts, available frozen snapshot bytes and optional collective private captures without modifying them. An extra file, symlink, missing file or hash mismatch is a failure. Private sources, command blobs and replay copies are excluded from public release. Original target files and other review families are outside this namespace and remain unchanged.

A public-only checkout can check public hashes and finite controls. Historical catalogue/prior-search raw inputs are absent from the target packet; their absence does not make a bounded negative search or novelty claim verified. This audit makes no priority claim. Root handles final closure and publication; no external person is contacted.
