# Semantic queue-row proposal — inert version 2

Target only **30004563 / OWR-2654831-006**, not rank 193 or PR number 193. No actual queue patch is prepared or applied here.

The immutable original submitted HEAD b9a399eeac816dbb8f0e50e81b498c26e5acef81 records **claimed_solved**, recovered author effort **2/5**, and earlier historical effort unknown. That original claim/eligibility state is separate from the actual shared MAIN preimage. Root reports MAIN currently and legitimately **queued, 0/5** until this original PR is integrated. Root must freshly read/authenticate the actual MAIN parent and target row at the eventual merge gate; this preparation has not read it.

| target state or cell | proposed semantics |
|---|---|
| Original submitted status / effort | claimed_solved / 2/5, immutable provenance |
| Actual MAIN preimage | UNRESOLVED_FRESH_MAIN_TARGET_STATUS / UNRESOLVED_FRESH_MAIN_TARGET_EFFORT; fresh read required; currently queued / 0/5 according to Root |
| Status after gated integration | restore original claimed_solved and retain it through publication |
| Effort after gated integration | restore original 2/5; earlier historical count remains unknown |
| PR/reference cell | Root may update this target's authorized PR/reference cell from verified evidence; no invented identifier |
| Claim/findings | use proposed_findings in QUEUE_PROPOSAL.json after substituting verified receipts |
| DOI | UNRESOLVED_VERIFIED_DOI_URL until actual verified DOI and landing-page readback |

Only this target's **status, effort/turns, PR/reference, claim/findings and DOI** cells may change. Every other target field and all foreign rows/content must remain exact from the freshly authenticated parent. Do not restore a stale whole row. No actual queue patch may occur before actual DOI/publication, verified tracker readback and the Root merge gate. This is no actual mutation, completion counter update or intake advance.
