# Public projection specification

The exact checker and both complete outputs are copied byte-for-byte. checker_original.txt is a second exact copy of CHECK.py; validation compares the complete module AST, not selected functions. The original four-entry hash manifest is verified at build time; its path-bearing bytes are not distributed. Original authored-file hashes and sizes appear in ORIGINAL_AUDIT_RECEIPT.json. No dataset fingerprints are retained.

REPORT.md: remove the single task-authorization sentence in the opening paragraph. Replace the broad failure-safety sentence in section 5 with an explicit statement that only the named fixed-checker rejection tests were demonstrated; arbitrary derivative/coupling error safety is not established. All equations and five approaches remain unchanged.

INDEPENDENT_REVIEW.md: remove the opening sentence describing workflow actions; replace the execution-command block with a prose description of the same normal/optimized comparisons and four hash checks, without execution locations. Qualify the broad failure-safety discussion as referring to the original report, and explicitly state the public prose change is not a fresh independent review. Its original hash-bound input table contains only authored artifacts and is retained unchanged.

SOURCE_GATE.md: retain the primary-literature/status and analytic-audit sections, change the private-attempt attribution to a neutral prior-framework attribution, and replace other sections with a public identity/retrieval summary. No recovered source wording, copied source, private location, dataset fingerprint, or coordination history is distributed.

public_source_manifest.json: retain public identity, status, public PDF hashes/sizes/URLs and inspection depths; exclude dataset_files, all_state_pr_queries, no_publication and no_queue_edit. PDF_METADATA.json is unchanged public-source metadata. Source retrieval was historical; this packaging step performs no network operations.
