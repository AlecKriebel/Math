# OPG-605 independent audit packet

Read `AUDIT_REPORT.md` first. The mathematical partial is accepted, with status unsolved / partial stalled and 3/5 approaches. A loader-only correction makes the accepted derivative work in isolated Python. The exact original archive is preserved alongside the patched derivative.

## Quick exact replay

From this directory, run:

    python -I accepted/verify.py
    python -I -O accepted/verify.py
    python -I independent_verifier.py
    python -I -O independent_verifier.py

The independent verifier does not import either author's geometry implementation. Its third exact construction compares every bounded-cell graph and rational polygon vertex, and all one-line deletion defects.

The accepted verifier also works from any unrelated working directory when invoked by its full path. The archive's external SHA-256 and the member manifest provide the integrity anchor. `ACCEPTANCE.json` identifies the exact accepted derivative and patch.

## Optional private-input replay

The corpus and scholarly-source files are deliberately not distributed. If the exact original input files are available, run:

    python -I -O accepted/verify_inputs.py CATALOG_FILE PROBLEMS_FILE REPORTS_FILE SOURCE_DIRECTORY

Read `CORPUS_AUDIT.json` and `SOURCE_RETRIEVAL_AUDIT.json` for expected sizes, hashes, and this review's match results. Omitting this command is not a new corpus/source verification by the recipient.

## Full artifact test matrix

Extract `OPG-605_author_packet.zip` into an original-packet directory. Then run:

    python -I audit_artifacts.py ORIGINAL_PACKET_DIRECTORY CORPUS_DIRECTORY SOURCE_DIRECTORY

The corpus directory must contain `catalog.json`, `problems.json`, and `research_results.json`; source filenames are listed in `accepted/SOURCE_PINS.json`. The driver uses temporary copies and writes only `ARTIFACT_AUDIT_RESULTS.json` beside itself. It reproduces 88 checks, including the two expected original isolated-mode failures. It exercises normal, optimized, isolated, and isolated-optimized runs, relocation, independent recomputation, and negative tamper tests. All acceptance conditions are explicit exceptions, not assertions.

The full audit ZIP contains no copied corpus records, third-party source documents, source text, or private coordination material. It is suitable for sharing only within the authorized publication scope. The audit makes no claim of mathematical novelty or resolution of the original conjecture.
