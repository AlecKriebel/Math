# Reproducibility and author freeze

Requirements: Python 3 standard library only. There are no network calls, downloads, external commands, symbolic-algebra packages, or writes in the mathematical verifier. Run from any working directory:

    python /path/to/packet/verify.py
    python -O /path/to/packet/verify.py

Both outputs must equal `expected_results.json` byte for byte. The script uses explicit exceptions, not Python assertions, so optimization does not disable its checks.

For bound-file integrity, exact normal/optimized replay, and six deliberate integrity mutations:

    python /path/to/packet/verify_manifest.py --replay --selftest

The manifest checker rejects extra or missing paths, symlinks, duplicate paths, path traversal, changed bytes, and size/digest mismatches. The manifest's own hash is recorded in the separate freeze receipt, not recursively in itself. Manifest verification proves preservation relative to that receipt, not the mathematical truth of any document.

## Exact controls

- Four-line dual frame has full rank on all triples; a concurrent variant fails that test.
- Fermat directions for 4<=n<=40 avoid the Jacobian ideal; the degree-n Jacobian monomial span has dimension 16.
- Embedded Kodaira–Spencer image dimension is binomial(n+3,3)-16. This is not asserted to equal total h^1 in every degree.
- The uniform disk smoothness bound is checked in integer arithmetic, in addition to its written proof for all n.
- The quadrangle n=3 character (2,2,2,1,1) has L=-K, four selected divisors, and residue-matrix rank four in Picard rank five.
- Every quadrangle character is enumerated for 2<=n<=10: 220,824 characters in total. Integral divisor classes, uniform coordinate bounds, and carry identities are checked. Different sheaf-type counts and a deterministic census hash are recorded.
- Five mathematical negative controls: one concurrent frame, a Jacobian-trivial direction, a wrong-degree direction, use of the Fermat witness outside its stated n-range, and a mutated exceptional character.

The result contains 4,858,415 explicit checks. These are repeated arithmetic consistency checks, not that many independent mathematical theorems. The finite census neither evaluates all cohomology groups nor establishes a universal rigidity result.

## Publication exclusions

The packet deliberately contains only author-written analysis, code, results, public-source metadata, and integrity records. Source PDFs, rendered source pages, extracted text, corpus rows, full datasets, private conversations, and coordination records are excluded.

This is a local author freeze. No independent audit is included or implied. No remote write or publication occurred during author preparation. Any later release must retain the controlling distinction: literal unrestricted formulation false; intended restricted problem unresolved here.
