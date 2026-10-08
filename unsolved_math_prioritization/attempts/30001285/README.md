# Motivic comparison: audited partial results

Problem 30001285 / OWR-3481-002, queue rank 972. Status: **unsolved, 5/5 author approaches**.

Read corrected/STATEMENT.md and corrected/RESULTS.md for the accepted mathematics, then audit/AUDIT_REPORT.md for the complete independent review. The five approaches cover lifting, multipliers, descent, generic detection, and a conditional SK2 suspension comparison. They do not resolve the general beta-versus-sigma problem. The known negative projection example is credited to Platonov–Suslin–Wouters; the distinct exponent-two comparison is also an imported result.

## Preservation

- original/ contains all 16 frozen author files, byte-for-byte.
- audit/ contains all 9 frozen audit files, including LOW_DEGREE_CORRECTION.patch.
- corrected/ contains all 16 frozen corrected files. Only STATEMENT.md and its manifest entry differ from original/.
- PUBLICATION_STATUS.json records the accepted scope and historical-status interpretation.

The correction requires degree > 2 for the positive-generator description of c_A. In division degrees 1 and 2, c_A is zero by Wang's square-free-index theorem over every extension. The correction does not extend any positive-generator theorem or settle the remaining comparison.

## Portable replay

Python 3.10+ and its standard library in a POSIX environment with writable /tmp suffice. No packages, network access, source documents, dataset contents, or original workspace are required. Obtain the SHA-256 of PUBLIC_MANIFEST.json independently from the PR description or a trusted receipt, and substitute it below:

    python3 -I -S -B verify_publication.py --manifest-sha256 TRUSTED_SHA256
    python3 -I -S -B -O verify_publication.py --manifest-sha256 TRUSTED_SHA256
    python3 -I -S -B mutation_tests.py --manifest-sha256 TRUSTED_SHA256

Commands work from another working directory when the script path is absolute. Redirect output outside this closed packet. PUBLIC_MANIFEST.json is the exact file allowlist, with byte counts and SHA-256 values. Its digest is deliberately supplied externally rather than authenticated by itself. Fixed author/audit/corrected anchors are checked as well.

The verifier checks all frozen records, closed inventory including directories, symlink/nonregular rejection, actual patch replay, the one-file correction boundary, and the exact author/independent recorded JSON outputs. Subprocesses inherit the explicit optimization mode. The mutation suite tests malformed inventory, altered content, false anchors, unsafe paths, directory and symlink substitutions, actual patch corruption, and explicit checker failures in normal and optimized execution. It uses temporary copies and does not alter the frozen packet.

These are integrity and finite-model controls, not a proof checker for imported motivic theorems. They do not replay public PDF inspection, prove worldwide literature completeness, establish novelty, or certify the generic beta-minus-sigma class. A coordinated malicious replacement of the verifier and all independently trusted digests is outside this threat model. Concurrent hostile filesystem races are not covered.

## Source boundary and disclosure

Public source titles, URLs, version status, hashes, byte counts, and inspection history are preserved in original/SOURCES.json and audit/SOURCE_AUDIT.json. No copied PDF, extracted third-party text, source image, dataset content, or private coordination material is published. Complete foundational proofs remain cited external dependencies. See the audit for all scope limits, including the uninspected final journal full text of Wouters and the conditional product-normalization step.

AI tools were used extensively. This packet is unrefereed, has not undergone human peer review, and is not proof-assistant formalization.
