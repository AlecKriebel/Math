# Loop invariant partial research packet

Problem 30006086 / OWR-14298797-002, queue rank 960. The full problem is **unsolved, 5/5**. Independent mathematical audit is pending at this freeze.

Start with RESULT.md. It contains direct proofs of the all-degree alternating obstruction and the sharp identity-class detection theorem, and a computer-assisted generation result through degree 8 in every dimension. TURNS.md identifies the five distinct mathematical approaches and their gaps.

## Replay

With Python 3.11 or newer and only its standard library:

    python3 -B verify.py

The verifier recomputes the multilinear rational ranks through degree 8, every binary multidegree through degree 13, PBW dimension/deletion checks, alternating-area pairings, finite matrix trace controls, and actual closed-path commutator leading terms. It compares the complete result with EXPECTED_RESULTS.json and prints deterministic JSON. A typical author run takes about one minute. No network or external data is required. It writes no files; -B avoids bytecode files. Optimized mode (-O) is explicitly rejected because algebra routines use assertions.

The arithmetic is exact over Q, not numerical or probabilistic. These checks certify the stated finite algebraic bounds; the all-degree conclusions depend on the written proofs, and the original unrestricted conjectures remain unresolved. This is not a formal proof-assistant certificate or external human peer review.

SOURCE_AUDIT.json records public source titles, URLs, precise locations, retrieval/inspection scope, public-input hashes and bounded duplicate/literature search metadata. It contains no source-document text or datasets. Source files are not distributed.

The separate SHA256SUMS.json binds every file in the frozen author packet except itself. No repository, PR, queue or publication-service changes are included in this author packet. A later independent audit and release decision must be recorded separately rather than silently changing this freeze.
