# Problem 3341 / OPG-37448: balanced-picture MSO alternation

**Unsolved, five substantive approaches used.** The arbitrary-level balanced hierarchy remains unresolved. The first-level square separation is known mathematics, reconstructed here with proofs and finite controls; no discovery or full-resolution claim is made.

Read [the corrected proof packet](corrected-release/PARTIAL_RESULTS.md). It applies the three small corrections/clarifications from [the independent audit](independent-audit/AUDIT.md): actual separating zero strips, exact-format balance conventions, and the one-way successor-signature bridge. Mathematical claims, the five-turn classification, and control code/results are unchanged.

- [Corrected packet](corrected-release/README.md) and [its manifest](corrected-release/SHA256SUMS)
- [Original audited freeze](release/README.md) and [its manifest](release/SHA256SUMS), retained unchanged as historical evidence
- [Complete independent audit](independent-audit/AUDIT.md), [correction instructions](independent-audit/CORRECTIONS.md), and [audit manifest](independent-audit/SHA256SUMS)
- [Exact manuscript diff](CORRECTION_PATCH.diff) and [correction record](CORRECTIONS_APPLIED.md)
- [Final-layout replay results](REPRODUCTION.json)

From this directory, run:

    python3 corrected-release/controls/check.py
    python3 independent-audit/rerun/controls/check.py
    python3 independent-audit/independent_checks.py
    (cd release && sha256sum -c SHA256SUMS)
    (cd corrected-release && sha256sum -c SHA256SUMS)
    (cd independent-audit && sha256sum -c SHA256SUMS)
    sha256sum -c BUNDLE_SHA256SUMS

All tests are bounded controls. No general tableau compiler or infinite hierarchy theorem is certified. Original frozen documents describing a pending publication are historical records, not assertions about the later PR state. Downloaded source PDFs, raw corpus files, private coordination, and unrelated repository files are not part of this package.

The accompanying queue diff changes only problem 3341's Status to unsolved and Turns to 5/5. Findings and all other row bytes are preserved. No merge or release is included.
