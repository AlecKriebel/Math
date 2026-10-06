# Independent acceptance and isolated correction

Problem 30001707 / OWR-4799-003. The mathematical outcome is partial. The original one-way conjecture is unresolved by this work; no novelty is claimed.

Read INDEPENDENT_AUDIT.md first. The author freeze is immutable historical evidence and has a reproduced hostile-import execution defect. Use the corrected derivative with the mandatory isolated bootstrap. AUTHOR_PATCH.diff is a real patch against the nine-file author archive; PATCH_APPLICATION.json records actual application and exact comparison.

Before execution, obtain the audit receipt/manifest through a trusted independent channel and verify the archive, all member hashes, and the ISOLATED_VERIFY.py entry-point hash. An attacker-controlled replacement receipt is not a trust anchor. Use a trusted Python interpreter; this workflow assumes a quiescent filesystem and is not an operating-system sandbox.

From the extracted audit directory:

    python -I -S -B ISOLATED_VERIFY.py corrected CORRECTED_EXTERNAL_MANIFEST.json
    python -I -S -O -B ISOLATED_VERIFY.py corrected CORRECTED_EXTERNAL_MANIFEST.json

To repeat the independent before/after diagnostics, first authenticate INDEPENDENT_TESTS.py and provide the unchanged original author archive (SHA-256 5b9f4bee72814a7311703414c959b9c467246ed034db4975a3ece7fa4cb44973):

    python -I -S -B INDEPENDENT_TESTS.py /path/to/MULTIPLICITY_FREE_30001707_AUTHOR_SAFE_FREEZE.zip
    python -I -S -O -B INDEPENDENT_TESTS.py /path/to/MULTIPLICITY_FREE_30001707_AUTHOR_SAFE_FREEZE.zip

The replay intentionally demonstrates the original defect using a benign temporary marker; it does not modify the original archive. Both recorded runner modes passed. Isolated/no-site flags must be present when starting the interpreter, not added after startup. Do not launch the historical author verifier directly from an untrusted directory.

This bundle contains only authored mathematics, authored code/patches, acceptance results, and public verification metadata. Source documents, their extracts/images, dataset contents, and private coordination are excluded. Primary-source and complete-corpus verification are recorded as bounded metadata; live problem-page contents and exhaustive literature status remain unverified.
