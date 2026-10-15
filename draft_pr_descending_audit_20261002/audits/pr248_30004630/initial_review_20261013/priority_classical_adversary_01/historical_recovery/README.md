# Exact historical REPORT recovery

The recovered bytes in REPORT_as_read_7091d12b.md match the historical INPUT_PINS binding exactly: 10,340 bytes and SHA2567091d12b2ed3105451420fc39416d4b965ed3aff7600c2e685e45964b00d37e7.

Recovery was an exact reconstruction, not discovery of an old native file or Git blob. The earlier and final REPORT paragraphs remained verbatim in this agent's task context through the actual apply_patch call. Reversing those five replacements in the unchanged current REPORT reproduced the historical size and hash on the first candidate. reconstruct_report.py makes the operation repeatable; RECOVERY_RECEIPT.json records the result and unchanged current-report pin.

This is an obsolete provisional report recovered solely for the historical as-read provenance check. Its earlier categorical priority language was corrected in the current REPORT. Recovery authenticates its historical bytes; it does not restore its old recommendation or alter the current mathematical/priority assessment.

A read-only Git path-history query showed only the currently committed report revision. No native historical Git-object recovery is claimed. No existing report, INPUT_PINS, audit manifest, frozen paper or ZIP was edited. Every prior authored file pin in FINAL_AUDIT_MANIFEST.json was verified unchanged. All new work is confined to historical_recovery/.

