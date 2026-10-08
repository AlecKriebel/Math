# Verification and trust boundary

This is a source-free credited-prior-result packet for problem 1900002.

First verify bootstrap.py against its SHA-256 supplied independently with the delivery. Do not trust a replacement bootstrap merely because its replacement PINS.json agrees. The bootstrap pins the external manifest and archive; the manifest binds every authored file. All artifact bytes are authenticated before executing the inner checker.

Run `python -I -S -B bootstrap.py`, optionally adding `-O` or `-OO` before bootstrap.py. Run `python -I -S -B controls.py` for disposable-copy tamper controls. The original distribution can remain read-only. Python standard library only; no packages or network are required.

Optional private replay: add `--problems PATH --reports PATH --sources DIRECTORY` to the bootstrap command. The first two files must be the exact pinned corpus bytes. The directory must contain the two PDF filenames recorded in SOURCE_METADATA.json. No source files are shipped. A run without private inputs explicitly reports that their bindings were not checked.

The checker implements finite exact-arithmetic and integrity controls. It is not a formal proof, a complete search over integer curvature witnesses, or a semantic verifier of the literature. Mathematical credit belongs to Dolan and Karpenkov.

Only disposable mutation copies should be made writable. Successful final validation receipts are stored outside this frozen distribution, so verification does not modify it.

This corrected v3 replaces the copied problem-statement passage with an authored paraphrase. The original frozen v1 remains unchanged. The source metadata also records the independently inspected preprint correction history. Use the new independent bootstrap pin for this release.
