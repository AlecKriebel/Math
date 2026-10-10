# Independent receipt audit

Checkpoint: 2026-10-10T21:52:58.499015+00:00. Verified 73/73 completed public receipts; 0 pending and 0 failed. Completion estimate for the final receipt audit: 100%. Overall audit status: **pass**.

This independent audit reads local receipts, the original inventory/catalog and frozen approved proposal hashes. It uses no Zenodo/client imports, credentials, network operations, Git actions or patch writes. It validates public record/deposition state, full DOI/OAI PIDs, parent concept PIDs, complete version identities/count, full file entry/settings/link dictionaries, checksums/sizes, original inventory/source correspondence, access/custom fields and all unpatched native metadata. Changed native fields are independently reconstructed from the frozen scholarly proposal, while controlled-vocabulary display titles are ignored only inside intentionally changed vocabulary fields. Existing native relation objects and author identifiers, affiliations, roles and other structure remain protected exactly. The sole source-reviewed name-order correction on 22770864 changes only the reversed given/family/name fields; other creator changes only add the reviewed missing ORCID. Description preservation or exact reviewed-description equality binds the scientific scope to the content reviews.

Four existing metadata drafts required restoration of an original selected preview that the legacy endpoint omitted. The audit hashes both raw preview-repair receipts and independently checks the exact original public snapshot, owned reviewed session, intended metadata, draft identity, full file dictionaries and payload. Only original writable display options accompany reviewed metadata/custom fields in the exact same-record draft PUT; PIDs, access, file entries/uploads and unreviewed metadata are forbidden. All final public file settings must equal the original exactly.

The local snapshots represent the recorded authenticated public read-backs. This audit does not perform a new live query, download file bytes, re-certify the scientific proofs or close manuscript priority/access gaps. Pending receipts never count as completed.

The separate original-baseline hash manifest is append-only for newly approved records. It freezes the unchanged recorded public snapshots when this independent audit is installed and prevents later coherent edits to both before/after receipts from escaping detection. Earlier native snapshot authenticity remains grounded in the recorded API provenance and inventory/native cross-checks, rather than a claim that local hashes retroactively authenticate an API response.

Falsification controls: 28 controls; all passed=True; bound to current audit-tool bytes=True. Cloned-data mutants test DOI/concept/version/OAI/file-link/file-access/affiliation/scope/tag/language/patch alteration while optimistic receipt booleans remain true, plus unauthorized creator renames, identifier/affiliation/role loss and unsafe or wrong-record preview-restoration evidence.

## First-record draft/public representation check

Record 23271172: **pass**. The raw first guard-stop snapshot contains precisely the original DOI PID with the original OAI PID omitted in the draft. The separate raw file comparison contains precisely omitted generated per-file links. The completed public receipt must restore the full original OAI/DOI dictionary and the full original file dictionary, including those links; no public-boundary normalization is allowed. Only keywords/language change.

## Completed receipts

| Record | Route | Status | Record DOI | Concept DOI | Full version IDs | Changed legacy fields |
|---|---|---|---|---|---|---|
| 23271172 | legacy | pass | 10.5281/zenodo.23271172 | 10.5281/zenodo.23271171 | 23271172 | keywords, language |
| 23231145 | legacy | pass | 10.5281/zenodo.23231145 | 10.5281/zenodo.23231144 | 23231145 | keywords, language |
| 23224103 | legacy | pass | 10.5281/zenodo.23224103 | 10.5281/zenodo.23224102 | 23224103 | keywords, language |
| 23220043 | legacy | pass | 10.5281/zenodo.23220043 | 10.5281/zenodo.23220041 | 23220043 | keywords, language |
| 23217863 | legacy | pass | 10.5281/zenodo.23217863 | 10.5281/zenodo.23217862 | 23217863 | keywords, language, related_identifiers |
| 23205305 | legacy | pass | 10.5281/zenodo.23205305 | 10.5281/zenodo.23205304 | 23205305 | keywords, language |
| 23205294 | legacy | pass | 10.5281/zenodo.23205294 | 10.5281/zenodo.23205293 | 23205294 | keywords, language |
| 23205181 | legacy | pass | 10.5281/zenodo.23205181 | 10.5281/zenodo.23205180 | 23205181 | keywords, language |
| 23205034 | legacy | pass | 10.5281/zenodo.23205034 | 10.5281/zenodo.23205033 | 23205034 | keywords, language |
| 23204952 | legacy | pass | 10.5281/zenodo.23204952 | 10.5281/zenodo.23204951 | 23204952 | keywords |
| 23204810 | legacy | pass | 10.5281/zenodo.23204810 | 10.5281/zenodo.23204809 | 23204810 | keywords, language |
| 23204591 | legacy | pass | 10.5281/zenodo.23204591 | 10.5281/zenodo.23204590 | 23204591 | keywords |
| 23204250 | legacy | pass | 10.5281/zenodo.23204250 | 10.5281/zenodo.23204249 | 23204250 | keywords, language |
| 23204212 | legacy | pass | 10.5281/zenodo.23204212 | 10.5281/zenodo.23204211 | 23204212 | keywords, language |
| 23204176 | legacy | pass | 10.5281/zenodo.23204176 | 10.5281/zenodo.23204175 | 23204176 | keywords, language, related_identifiers |
| 23203732 | legacy-with-preview-restoration | pass | 10.5281/zenodo.23203732 | 10.5281/zenodo.23203731 | 23203732 | keywords, language |
| 23203334 | legacy | pass | 10.5281/zenodo.23203334 | 10.5281/zenodo.23203333 | 23203334 | keywords, language |
| 23203323 | legacy | pass | 10.5281/zenodo.23203323 | 10.5281/zenodo.23203322 | 23203323 | keywords, language |
| 23203270 | legacy | pass | 10.5281/zenodo.23203270 | 10.5281/zenodo.23203269 | 23203270 | keywords, language |
| 23203143 | legacy | pass | 10.5281/zenodo.23203143 | 10.5281/zenodo.23203142 | 23203143 | keywords, related_identifiers |
| 23203100 | legacy | pass | 10.5281/zenodo.23203100 | 10.5281/zenodo.23203099 | 23203100 | description, keywords, language |
| 23203081 | legacy | pass | 10.5281/zenodo.23203081 | 10.5281/zenodo.23203080 | 23203081 | keywords |
| 23202994 | legacy | pass | 10.5281/zenodo.23202994 | 10.5281/zenodo.23202993 | 23202994 | keywords, language |
| 23202966 | legacy | pass | 10.5281/zenodo.23202966 | 10.5281/zenodo.23202965 | 23202966 | keywords, language |
| 23196750 | legacy | pass | 10.5281/zenodo.23196750 | 10.5281/zenodo.23196749 | 23196750 | keywords, language |
| 23191301 | legacy | pass | 10.5281/zenodo.23191301 | 10.5281/zenodo.23191300 | 23191301 | keywords, language |
| 23191247 | legacy | pass | 10.5281/zenodo.23191247 | 10.5281/zenodo.23191246 | 23191247 | keywords, language |
| 23181280 | legacy | pass | 10.5281/zenodo.23181280 | 10.5281/zenodo.23181279 | 23181280 | keywords, language |
| 22929486 | legacy-with-preview-restoration | pass | 10.5281/zenodo.22929486 | 10.5281/zenodo.22929485 | 22929486 | keywords, language |
| 22770864 | legacy-with-preview-restoration | pass | 10.5281/zenodo.22770864 | 10.5281/zenodo.22770863 | 22770864 | creators, keywords, language, related_identifiers |
| 22729545 | native-preserving | pass | 10.5281/zenodo.22729545 | 10.5281/zenodo.22729544 | 22729545 | keywords |
| 22729537 | native-preserving | pass | 10.5281/zenodo.22729537 | 10.5281/zenodo.22729536 | 22729537 | keywords |
| 22729355 | native-preserving | pass | 10.5281/zenodo.22729355 | 10.5281/zenodo.22729354 | 22729355 | keywords, language |
| 22395326 | native-preserving | pass | 10.5281/zenodo.22395326 | 10.5281/zenodo.22395325 | 22395326 | keywords |
| 22178672 | native-preserving | pass | 10.5281/zenodo.22178672 | 10.5281/zenodo.22178671 | 22178672 | keywords, language |
| 22168797 | native-rich | pass | 10.5281/zenodo.22168797 | 10.5281/zenodo.22168796 | 22168797 | description, keywords, language |
| 22136869 | native-rich | pass | 10.5281/zenodo.22136869 | 10.5281/zenodo.22136868 | 22136869 | keywords, language |
| 22089807 | native-preserving | pass | 10.5281/zenodo.22089807 | 10.5281/zenodo.22089806 | 22089807 | keywords, language |
| 22089748 | native-preserving | pass | 10.5281/zenodo.22089748 | 10.5281/zenodo.22089747 | 22089748 | keywords, language |
| 22089551 | native-preserving | pass | 10.5281/zenodo.22089551 | 10.5281/zenodo.22089550 | 22089551 | keywords, language |
| 22089373 | native-preserving | pass | 10.5281/zenodo.22089373 | 10.5281/zenodo.22089372 | 22089373 | keywords, language |
| 22013710 | native-rich | pass | 10.5281/zenodo.22013710 | 10.5281/zenodo.21971506 | 21971507, 22013710 | description, keywords |
| 21699161 | native-rich | pass | 10.5281/zenodo.21699161 | 10.5281/zenodo.21699160 | 21699161 | creators, keywords, language, related_identifiers |
| 23129302 | native-preserving | pass | 10.5281/zenodo.23129302 | 10.5281/zenodo.23129301 | 23129302 | keywords, language, related_identifiers |
| 23127955 | legacy | pass | 10.5281/zenodo.23127955 | 10.5281/zenodo.23127954 | 23127955 | keywords, language, notes, related_identifiers |
| 23127646 | native-preserving | pass | 10.5281/zenodo.23127646 | 10.5281/zenodo.23127645 | 23127646 | keywords, language, related_identifiers |
| 23124601 | legacy | pass | 10.5281/zenodo.23124601 | 10.5281/zenodo.23124600 | 23124601 | keywords, language, related_identifiers |
| 23088066 | legacy | pass | 10.5281/zenodo.23088066 | 10.5281/zenodo.23088065 | 23088066 | keywords |
| 23074543 | legacy | pass | 10.5281/zenodo.23074543 | 10.5281/zenodo.23074542 | 23074543 | keywords |
| 22983513 | legacy | pass | 10.5281/zenodo.22983513 | 10.5281/zenodo.22983512 | 22983513 | keywords |
| 22983519 | legacy | pass | 10.5281/zenodo.22983519 | 10.5281/zenodo.22983518 | 22983519 | keywords, notes |
| 22983147 | native-preserving | pass | 10.5281/zenodo.22983147 | 10.5281/zenodo.22983146 | 22983147 | keywords, related_identifiers |
| 22983161 | legacy | pass | 10.5281/zenodo.22983161 | 10.5281/zenodo.22983160 | 22983161 | keywords, language |
| 22983138 | legacy | pass | 10.5281/zenodo.22983138 | 10.5281/zenodo.22983137 | 22983138 | keywords |
| 22982894 | legacy | pass | 10.5281/zenodo.22982894 | 10.5281/zenodo.22982893 | 22982894 | keywords |
| 22929857 | native-preserving | pass | 10.5281/zenodo.22929857 | 10.5281/zenodo.22929856 | 22929857 | keywords, language |
| 22929556 | legacy-with-preview-restoration | pass | 10.5281/zenodo.22929556 | 10.5281/zenodo.22929555 | 22929556 | description, keywords, language, publication_type, related_identifiers, upload_type |
| 23180194 | legacy | pass | 10.5281/zenodo.23180194 | 10.5281/zenodo.23180193 | 23180194 | keywords, language |
| 23174283 | legacy | pass | 10.5281/zenodo.23174283 | 10.5281/zenodo.23174282 | 23174283 | keywords, language, related_identifiers |
| 23174156 | native-preserving | pass | 10.5281/zenodo.23174156 | 10.5281/zenodo.23174155 | 23174156 | keywords, language |
| 23171212 | native-preserving | pass | 10.5281/zenodo.23171212 | 10.5281/zenodo.23171211 | 23171212 | keywords, language |
| 23157237 | legacy | pass | 10.5281/zenodo.23157237 | 10.5281/zenodo.23157236 | 23157237 | keywords, language |
| 23153134 | native-preserving | pass | 10.5281/zenodo.23153134 | 10.5281/zenodo.23153133 | 23153134 | keywords, language |
| 23149775 | legacy | pass | 10.5281/zenodo.23149775 | 10.5281/zenodo.23149774 | 23149775 | keywords, language |
| 23147866 | native-preserving | pass | 10.5281/zenodo.23147866 | 10.5281/zenodo.23147865 | 23147866 | keywords, language |
| 23146753 | legacy | pass | 10.5281/zenodo.23146753 | 10.5281/zenodo.23146752 | 23146753 | keywords, language |
| 23137834 | legacy | pass | 10.5281/zenodo.23137834 | 10.5281/zenodo.23137833 | 23137834 | keywords, language, related_identifiers |
| 23133607 | legacy | pass | 10.5281/zenodo.23133607 | 10.5281/zenodo.23133606 | 23133607 | keywords, language, related_identifiers |
| 23131374 | native-preserving | pass | 10.5281/zenodo.23131374 | 10.5281/zenodo.23131373 | 23131374 | keywords, language |
| 23131001 | native-preserving | pass | 10.5281/zenodo.23131001 | 10.5281/zenodo.23131000 | 23131001 | keywords, language, related_identifiers |
| 23130727 | legacy | pass | 10.5281/zenodo.23130727 | 10.5281/zenodo.23130726 | 23130727 | keywords, language, related_identifiers |
| 21699069 | native-rich | pass | 10.5281/zenodo.21699069 | 10.5281/zenodo.21699068 | 21699069 | creators, keywords, language, related_identifiers |
| 21971507 | native-rich | pass | 10.5281/zenodo.21971507 | 10.5281/zenodo.21971506 | 21971507, 22013710 | keywords |

## Pending and failures

Pending IDs: .

The JSON companion contains every individual check, exact exception paths, receipt/source-review SHA-256 values, frozen patch hashes and full version counts.
