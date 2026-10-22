# Corrected publication slice

The original packet was preserved unchanged. Use `corrected/packet/`, `corrected/freeze/`, `corrected/audit_tools/`, and `corrected/source_free_packet.tar.gz` for publication.

Implemented changes:

- REPORT.md: replace the primary-source conjecture quotation with authored paraphrase, retaining the version/domain/counting distinction and public citations.
- STATUS.json: replace the pending independent-audit field with the completed unresolved-scope audit result.
- verify.py: require exact integer types for all five ledger turn numbers and both aggregate turn-count fields; require both aggregate values to equal five.
- FREEZE_MANIFEST.json, bootstrap.py and BOOTSTRAP_PINS.json: regenerate and pin the corrected packet and verifier.

The pure code change is published in `LEDGER_TYPE_HARDENING.patch`. The source-bearing quotation-removal diff is excluded. The corrected files and `CORRECTION_PINS.json` provide a checkable replacement without redistributing the removed text. All mathematical conclusions, the source identities, and the five-route ledger remain unchanged.

The archive includes packet, freeze and audit_tools only. Replayed acceptance receipts are external to that archive so they can name the final archive digest without a circular hash dependency.
