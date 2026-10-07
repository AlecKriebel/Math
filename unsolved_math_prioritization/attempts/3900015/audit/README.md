# Reciprocal rectangle independent audit packet

Problem 3900015 / AMR-038-0015, rank 928.

Accepted outcome: unresolved bounded partial, three approaches. The unchanged author packet is accepted exactly; no correction is required. No infinite packing theorem or external formalization claim is certified.

- AUDIT.md gives the complete mathematical, source, computation, and artifact audit.
- ACCEPTANCE.json pins the precise author archive and individual accepted members.
- AUTHOR_SAFE_FREEZE.zip and AUTHOR_EXTERNAL_MANIFEST.json are the unchanged safe authored input and its original external manifest.
- independent_checks.py and EXPECTED_INDEPENDENT_CHECKS.json give independent grid and separator-system exhaustions.
- author_artifact_tests.py and EXPECTED_AUTHOR_ARTIFACT_TESTS.json replay the author verifier and adversarial cases in isolation.
- SOURCE_CORPUS_AUDIT.json and SOURCE_INSPECTION.json record independent full-byte provenance checks and reading limits.
- verify_source_corpus.py optionally rechecks complete source inputs supplied separately. Raw corpora and third-party source documents are deliberately absent.
- verify_audit.py and MANIFEST.json verify the audit inventory and rerun the safe exact checks.

After checking this archive against its external manifest or a trusted archive SHA-256, extract it into an otherwise empty directory. Run:

    python -I -B /absolute/path/to/verify_audit.py
    python -I -B -O /absolute/path/to/verify_audit.py

The default audit replay is offline, uses only the standard library, and does not require source PDFs or corpora. To independently redo the recorded full-source input pins, separately supply the original complete inputs:

    python -I -B verify_source_corpus.py --corpus-dir CORPUS_DIRECTORY --source-dir SOURCE_DIRECTORY

Source inspection and mathematical review remain human judgments recorded in AUDIT.md; hash checks alone do not prove those judgments. There are no GitHub writes, queue writes, copied third-party source contents, private record contents, or private coordination in this packet.
