# KP-4.18 independent audit package

Decision: accept the corrected derivative as an unsolved split-status literature result, 1/5 turns. Part (a) follows from HU and KNV as cited theorem inputs; part (b) remains unresolved. The audit does not independently certify the underlying L-theory.

Start with AUDIT_REPORT.md and MATH_AUDIT.md. The current accepted mathematical packet is FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_SAFE.zip, with its matching corrected external manifest. The original author ZIP and manifest are retained only as immutable historical inputs.

Run the pinned exact-packet acceptance replay:

    python verify_acceptance.py
    python -O verify_acceptance.py

These commands pin both nested manifests and archives, safely extract their eight-file packets, and run both bound packet verifiers in both Python modes. The separately retained encompassing audit manifest/receipt must be trusted and used to verify this audit package before running code from it. Hashes are integrity references, not signatures.

Run the independent local group checks:

    python check_hu_parity.py --check HU_PARITY_RESULTS.json
    python -O check_hu_parity.py --check HU_PARITY_RESULTS.json

For full packet-negative testing, first extract either eight-file packet to its own empty directory, then run:

    python replay_integrity.py PACKET_DIR MATCHING_EXTERNAL_MANIFEST MATCHING_ZIP LABEL OUTPUT_JSON

The checker runs normal and optimized modes, relocated positives, twelve original-style negative controls, and thirty additional adversarial controls. The supplied results are separate for original and corrected packets.

To reproduce complete-corpus and PDF identities, supply the three complete inputs and the directory holding the five exact pinned PDFs:

    python validate_inputs.py --catalog CATALOG --problems PROBLEMS --reports REPORTS --pdf-dir PDF_DIRECTORY

The expected PDF filenames are k3.pdf, hu_v1.pdf, knv_v2.pdf, kp_v2.pdf and nnp_v4.pdf. The script requires pdftotext, reads the full supplied JSON inputs, verifies hashes, and emits only verification metadata. None of those external datasets or PDFs is bundled.

correction.patch was replayed with zero fuzz; all resulting file hashes match the corrected manifest. No publication or queue mutation was performed. No source documents, source extracts, dataset contents, private coordination, or private personal data are included.
