# Problem 30000120: scoped Chern-generator results

Status: UNSOLVED_SCOPED_PARTIAL; five approaches completed. Independent audit pending.

REPORT.md gives the proofs, source-scope checks, and precise general gap. The positive family consists of complete conics and products with projective planes, equipped with the specified adjoint symmetric actions. The tangent/logarithmic Chern-generator shortcut is disproved on complete conics. These reconstruct classical geometry; no novelty claim is made.

Only authored text, code, exact results, and public source verification metadata are included. No source PDFs, extracts, raw records, or private coordination files are included.

Verify from this directory with the manifest hash supplied outside this package:

    python3 verify.py --expected-manifest MANIFEST_SHA256 --self-test
    python3 -O verify.py --expected-manifest MANIFEST_SHA256 --self-test

Both commands must emit RESULTS.json byte-for-byte. The script checks an exact inventory and hashes before its finite algebra controls. It has no network or non-standard-library dependencies. A changed verifier can lie, so retain the external manifest pin and review the code. The checks do not establish the geometric proof or a general resolution.
