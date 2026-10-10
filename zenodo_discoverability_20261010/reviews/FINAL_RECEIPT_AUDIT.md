# Independent receipt audit

Checkpoint: 2026-10-10T21:28:28.315384+00:00. Verified 23/72 completed public receipts; 49 pending and 0 failed. Completion estimate for the final receipt audit: 32%. Overall audit status: **pending**.

This independent audit reads local receipts, the original inventory/catalog and frozen approved proposal hashes. It uses no Zenodo/client imports, credentials, network operations, Git actions or patch writes. It validates public record/deposition state, full DOI/OAI PIDs, parent concept PIDs, complete version identities/count, full file entry/settings/link dictionaries, checksums/sizes, original inventory/source correspondence, access/custom fields and all unpatched native metadata. Changed native fields are independently reconstructed from the frozen scholarly proposal, while controlled-vocabulary display titles are ignored only inside intentionally changed vocabulary fields. Existing native relation objects and author structures remain protected exactly. Description preservation or exact reviewed-description equality binds the scientific scope to the content reviews.

The local snapshots represent the recorded authenticated public read-backs. This audit does not perform a new live query, download file bytes, re-certify the scientific proofs or close manuscript priority/access gaps. Pending receipts never count as completed.

Falsification controls: 12 controls; all passed=True; bound to current audit-tool bytes=True. Cloned-data mutants test DOI/concept/version/OAI/file-link/file-access/affiliation/scope/tag/language/patch alteration while optimistic receipt booleans remain true.

## First-record draft/public representation check

Record 23271172: **pass**. The raw first guard-stop snapshot contains precisely the original DOI PID with the original OAI PID omitted in the draft. The separate raw file comparison contains precisely omitted generated per-file links. The completed public receipt must restore the full original OAI/DOI dictionary and the full original file dictionary, including those links; no public-boundary normalization is allowed. Only keywords/language change.

## Completed receipts

| Record | Route | Status | Record DOI | Concept DOI | Full version IDs | Changed legacy fields |
|---|---|---|---|---|---|---|
| 23271172 | legacy-compatible | pass | 10.5281/zenodo.23271172 | 10.5281/zenodo.23271171 | 23271172 | keywords, language |
| 23231145 | legacy-compatible | pass | 10.5281/zenodo.23231145 | 10.5281/zenodo.23231144 | 23231145 | keywords, language |
| 23224103 | legacy-compatible | pass | 10.5281/zenodo.23224103 | 10.5281/zenodo.23224102 | 23224103 | keywords, language |
| 23220043 | legacy-compatible | pass | 10.5281/zenodo.23220043 | 10.5281/zenodo.23220041 | 23220043 | keywords, language |
| 23217863 | legacy-compatible | pass | 10.5281/zenodo.23217863 | 10.5281/zenodo.23217862 | 23217863 | keywords, language, related_identifiers |
| 23205305 | legacy-compatible | pass | 10.5281/zenodo.23205305 | 10.5281/zenodo.23205304 | 23205305 | keywords, language |
| 23205294 | legacy-compatible | pass | 10.5281/zenodo.23205294 | 10.5281/zenodo.23205293 | 23205294 | keywords, language |
| 23205181 | legacy-compatible | pass | 10.5281/zenodo.23205181 | 10.5281/zenodo.23205180 | 23205181 | keywords, language |
| 23205034 | legacy-compatible | pass | 10.5281/zenodo.23205034 | 10.5281/zenodo.23205033 | 23205034 | keywords, language |
| 23204952 | legacy-compatible | pass | 10.5281/zenodo.23204952 | 10.5281/zenodo.23204951 | 23204952 | keywords |
| 23204810 | legacy-compatible | pass | 10.5281/zenodo.23204810 | 10.5281/zenodo.23204809 | 23204810 | keywords, language |
| 23204591 | legacy-compatible | pass | 10.5281/zenodo.23204591 | 10.5281/zenodo.23204590 | 23204591 | keywords |
| 23204250 | legacy-compatible | pass | 10.5281/zenodo.23204250 | 10.5281/zenodo.23204249 | 23204250 | keywords, language |
| 23204212 | legacy-compatible | pass | 10.5281/zenodo.23204212 | 10.5281/zenodo.23204211 | 23204212 | keywords, language |
| 23204176 | legacy-compatible | pass | 10.5281/zenodo.23204176 | 10.5281/zenodo.23204175 | 23204176 | keywords, language, related_identifiers |
| 23203334 | legacy-compatible | pass | 10.5281/zenodo.23203334 | 10.5281/zenodo.23203333 | 23203334 | keywords, language |
| 23203323 | legacy-compatible | pass | 10.5281/zenodo.23203323 | 10.5281/zenodo.23203322 | 23203323 | keywords, language |
| 23203270 | legacy-compatible | pass | 10.5281/zenodo.23203270 | 10.5281/zenodo.23203269 | 23203270 | keywords, language |
| 23203143 | legacy-compatible | pass | 10.5281/zenodo.23203143 | 10.5281/zenodo.23203142 | 23203143 | keywords, related_identifiers |
| 23203100 | legacy-compatible | pass | 10.5281/zenodo.23203100 | 10.5281/zenodo.23203099 | 23203100 | description, keywords, language |
| 23203081 | legacy-compatible | pass | 10.5281/zenodo.23203081 | 10.5281/zenodo.23203080 | 23203081 | keywords |
| 23202994 | legacy-compatible | pass | 10.5281/zenodo.23202994 | 10.5281/zenodo.23202993 | 23202994 | keywords, language |
| 23202966 | legacy-compatible | pass | 10.5281/zenodo.23202966 | 10.5281/zenodo.23202965 | 23202966 | keywords, language |

## Pending and failures

Pending IDs: 23203732, 23196750, 23191301, 23191247, 23181280, 22929486, 22770864, 22729545, 22729537, 22729355, 22395326, 22178672, 22168797, 22136869, 22089807, 22089748, 22089551, 22089373, 22013710, 21699161, 23129302, 23127955, 23127646, 23124601, 23088066, 23074543, 22983513, 22983519, 22983147, 22983161, 22983138, 22982894, 22929857, 22929556, 23180194, 23174283, 23174156, 23171212, 23157237, 23153134, 23149775, 23147866, 23146753, 23137834, 23133607, 23131374, 23131001, 23130727, 21699069.

The JSON companion contains every individual check, exact exception paths, receipt/source-review SHA-256 values, frozen patch hashes and full version counts.
