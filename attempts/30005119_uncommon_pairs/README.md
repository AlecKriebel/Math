# Uncommon pairs: source-correction audit

Row 1908, problem 30005119 (OWR-10252930-032).

This is a source-scope correction, not a new solution to the full maximum-girth large-cardinality conjecture. The literal rank-only statement is false by an established Sidorenko example; corrected large-prime results are prior work. Read REPORT.md for all qualifications, including prime-subfield coefficient restrictions on extension transfer.

The reviewed report, citations, mathematical review, checker, and recorded outputs are preserved bytewise. INDEPENDENT_REVIEW.md includes its final artifact cross-review. The finite checker records 1,316 test instances, 1,256 unique group/function cases, and 21 sparse direct-density checks. These are supplemental; Jensen proves the universal claim.

Run `python -B validate.py` or `python -O -B validate.py` using Python 3 and its standard library. No network is used. validate.py rejects nonregular members, links, extra inventory, malformed schemas, and altered bytes before replay. All member lstat checks, including the manifest, precede any content reads. Static AST provenance and explicit checks ensure -O does not remove checks. Full stdout/stderr from both replays is retained in validator output. Mutation tests operate only on disposable copies. The validator does not write to the bundle.

MANIFEST.json provides internal integrity, not authenticity. The separate frozen receipt pins all bytes, the manifest, archive, and external mutation/replay records. Rebuilding a manifest does not establish authenticity; compare the external receipt from a trusted channel. No copied third-party sources, corpus content, or private coordination material are included.
