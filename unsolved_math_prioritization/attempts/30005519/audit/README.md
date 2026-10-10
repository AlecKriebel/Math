# Independent audit packet: 30005519

Verdict: PASS. Recommend already_solved after one reconstruction approach, explicitly crediting Ferudun's 30 September 2026 unrefereed preprint. The exact real all-n/even-r dimension theorem and the maximum-dimensional coordinate classification were independently reconstructed. No change to the frozen author proof is required.

- AUDIT.md: full mathematical audit and source-scope analysis
- CORRECTIONS.md: qualifications and audit-code development correction
- INDEPENDENT_RESULTS.json: 391,846 independent exact controls
- AUTHOR_REPLAY_RESULTS.json: the unchanged frozen verifier's 710,862 controls
- PROVENANCE.json: full-file identities, public source URLs and retrieval limits
- INPUT_RESULTS.json: exact full-input verification result
- AUDIT_RESULTS.json: replay and integrity summary
- independent_verify.py: independent bounded mathematical controls
- verify_inputs.py: optional complete-input provenance replay
- verify_manifest.py and AUDIT_MANIFEST.json: exact payload integrity

Run with Python 3.10+ (standard library only for the independent audit code):

    python independent_verify.py
    python -O independent_verify.py
    python verify_manifest.py
    python -O verify_manifest.py

The first two outputs must match INDEPENDENT_RESULTS.json byte-for-byte. The mathematical theorem is proved in AUDIT.md, not inferred from finite tests. The original author verifier additionally needs SymPy 1.14.0 and is supplied in the separate, unchanged author packet.

For optional full-input replay, provide local paths without publishing the inputs:

    python verify_inputs.py --author-zip AUTHOR.zip --problems problems.json --reports research_results.json --catalog catalog.json --source-dir SOURCE_DIRECTORY

Its output must match INPUT_RESULTS.json. The source directory must contain the eight filenames identified in PROVENANCE.json. These are external inputs, deliberately excluded from this archive. The command does not download or alter them.

The audit checked the stored deposited source bytes and record metadata. Fresh Zenodo retrieval failed; this packet makes no successful-new-download, later-version, peer-review, or editorial-acceptance claim. No remote repository or queue writes were performed. No PDFs, extracts, screenshots, raw corpora, source archives or private coordination files are included.
