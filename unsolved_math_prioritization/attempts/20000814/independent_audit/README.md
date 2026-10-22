# Independent audit of Problem 20000814

Verdict: **PASS at the author's stated partial-progress scope**. No mandatory
correction found. The general AIM question remains unresolved by this packet.

- AUDIT.md: claim-by-claim mathematical review and limits
- VERDICT.json: machine-readable disposition and frozen-input identity
- verify_independent.py: separately authored exact algebra/integrity verifier
- verification_results.json: full-input verification result
- REPLAY_AND_NEGATIVE_CONTROLS.json: optimization and tamper-rejection checks
- SOURCE_AUDIT.json: source inspection scopes and public verification metadata
- MANIFEST.json: hashes of this audit's seven payload files

Run from any directory with Python 3 and SymPy 1.14.0:

    python verify_independent.py --author-dir AUTHOR_DIRECTORY --archive AUTHOR_ARCHIVE

For the recorded full-input output, also supply the local public-source files:

    --problems PROBLEMS_JSON --research RESEARCH_RESULTS_JSON
    --catalog CATALOG_JSON --dgf-pdf DGF_PDF

These optional inputs are verified in memory; their contents and local paths
are not included in the result. The script prints JSON to standard output and
does not modify the author directory or archive. It copies the author control
program into a temporary unrelated directory for normal and optimized replays.
Normal and optimized independent runs also produced byte-identical results.

The 183,459-check full-input run includes metadata/integrity tests as well as
arithmetic controls. Finite test counts do not prove the geometric theorems.
The theoretical review is in AUDIT.md. This is not a human peer-review or
formal proof-assistant certificate and makes no novelty claim.

The audit manifest does not hash itself. The separately supplied receipt hashes
the manifest and audit archive. No source PDF, extracted source text, corpus
content, selected dataset record, or private coordination is packaged here.
