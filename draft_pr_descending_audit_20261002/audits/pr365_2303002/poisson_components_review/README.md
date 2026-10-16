# Review inventory and replay

Read FINAL_REPORT.md for the verdict, INDEPENDENT_BASELINE.md for the independent
mechanism, and ANALYTICAL_ASSESSMENT.md for the complete candidate-step audit.
The two seals establish source-first derivation and assessment-before-execution.

Run the standalone read-only closure check from any directory:

    python /absolute/path/to/poisson_components_review/verify_readonly.py

It uses only the standard library, reads the frozen snapshot and review files,
validates public/private inventories, both early seals, source gzip logical
hashes, whole captured outputs and nested candidate manifests, and writes
nothing. It performs no network or candidate program execution.

To independently reproduce the final canonical checks in a separate scratch
copy of this review, use standard-library Python on replay_and_scope.py. It
uses the original repository only for read-only Git commands, a fresh gh API
read, and the frozen snapshot. It writes only its own private/ and receipts/
subtrees. All candidate programs are copied byte-identically before execution.
The exact commands, cwd, times, full stream lengths/hashes, exit codes and
comparisons are recorded in receipts/commands.json and receipts/driver.json.
Do not rerun a writing driver in the sealed review if preserving its closure.
The existing Python executable used here is recorded in those receipts; no
runtime was installed or modified.

Original source recipe: use urllib.request.urlopen on each exact URL in
receipts/primary_fetch.json, read the complete response, check bytes and SHA256
against SOURCE_MANIFEST.json, and store gzip.compress(data,compresslevel=9,
mtime=0). Temporarily decompress only inside the scratch private subtree.
Run /opt/homebrew/bin/pdftotext -layout <temporary.pdf> - and retain the complete
stdout as gzip with logical/stored hashes. Hayman-Lingham PDF61 is text-page
index60 after splitting on formfeed; Carleson uses all five pages. Exact
pdftoppm page/render commands and hashes are in receipts/primary_render.json.
Those receipts record complete source/header/extraction facts; the public
inventory never redistributes the PDFs or raw API bodies.

PUBLIC_MANIFEST.json inventories every public file except itself and
FINAL_SEAL.json. FINAL_SEAL.json binds that manifest, which binds the complete
private inventory receipt; this explicitly defines the closure without a
self-hash cycle. Private files and Python cache files are ignored by .gitignore.
Any extra public file makes the read-only verifier fail.
