# Reproduction and trust boundaries

The author packet is source-free. Start with PROOF_AND_STATUS.md. Status is unsolved, five distinct approaches. All qualifications and rejected examples are part of the result.

With Python 3 and only the standard library, run:

    python3 -I -S -B verify.py
    python3 -I -S -B -O verify.py
    python3 -I -S -B -OO verify.py

Each command must emit DIAGNOSTICS.json exactly. The 390 finite checks cover normalized rank-two matrices, local cubic formulas, an explicit nine-point separable critical-value grid, tensor interpolation and rectangle constraints, marginal scaling weights, and scope/turn flags. No numerical approximation, external package, network request or file write is used. Analytic/geometric proofs are not formally verified by this script. The author source does not use assert statements for validation.

The adjoining AUTHOR_MANIFEST.json binds the exact payload inventory, lengths, hashes, problem status and turn count. Its independently supplied SHA-256 is hardcoded in bootstrap.py. Authenticate bootstrap.py by an independently received hash before running it; do not execute a changed bootstrap merely because it reports its own success. After authentication, run from any working directory:

    python3 -I -S -B /trusted/path/bootstrap.py /path/to/author

The bootstrap first checks the manifest anchor and every payload file, rejects symlinks/special files and unexpected inventory, strictly parses all JSON, then launches the pinned verifier using the same optimization mode. Its expected output is bound by the authenticated DIAGNOSTICS.json. Hashes prove byte identity relative to a trusted pin, not mathematical truth or arbitrary-hostile-code safety. No filesystem-race, separate network namespace, or general sandbox guarantee is claimed.

Read-only tests use complete source-free copies at genuinely unwritable directory/file modes, running as UID 1000. Both attempted creation in the payload directory and append to an existing payload file must fail. All bytes are checked unchanged afterward. Malformed-input and hostile-verifier controls mutate separate disposable copies only; the frozen author directory and its trust anchors are never made writable for those tests.

Portable source-byte reverification is explicitly NOT_RUN because source PDFs/HTML are excluded. A separate invocation may check the six actual external sources listed in SOURCE_METADATA.json:

    python3 -I -S -B verify.py --source-dir /external/source-directory

The expected basenames are vassiliev2015-published.pdf, vassiliev2015.pdf, quartic-v12.pdf, j10v5.pdf, parabolic-v6.pdf and vassiliev2015.html. This optional run produces six additional byte checks, not the portable DIAGNOSTICS.json receipt. Its success verifies bytes only, not the accuracy of quotations, claimed inspection, or theorem applicability.

The full source versions and their inspection extents are stated in SOURCE_METADATA.json. The referenced original Jaworski proof was not independently inspected. The known global real parabolic conclusions are reported with attribution, not presented as a new solution or a reconstruction from first principles. Retained corpus information supplied search leads only.
