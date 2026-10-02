# PR36 execution revision: narrow static adversarial review

Checkpoint UTC: 2026-10-02T08:32:04Z. Requested source review100%; acceptance execution0%. Scope is the new sibling execution revision only. This report does not modify or relabel the closed17-member integration preparation package or transfer any scientific/final-gate verdict.

Read all changed source regions in the four revision helpers and compared them as text against the closed preparation sources. No helper was executed or imported; no Git command or remote request was made; no shared/canonical/foreign artifact was written. Only this new reviewer subfolder is written.

| Reviewed source | SHA256 |
| --- | --- |
| pr36_guards.py | 0aa7c99395ab744de042f2929019e640b0be4fcb0dd576d9af48b764796053a3 |
| integrate_reviewed_partial.py | 2d4841df107c521de467033344dc1e1214bcffa7984f15096d45e68238453943 |
| state_mirror_reconciliation.py | dc67d88ea3f97667df4e1a2f316043633ead7b1a3c4df4d182fddf3ff6b56e37 |
| verify_post_acceptance.py | 3e7c052b106a80af6e225b2fb641ab9c36f0b0679a98edf6d9fe1ea86769fcc8 |

## Remaining finding

**P1: Foreign staged bytes are not checked before publication.** `pr36_guards.py` lines217–226 require the two allowed foreign paths' working bytes and current HEAD hashes to remain exact, but do not compare their index blobs. Preflight starts from an empty index diff, but a later accidental broad staging operation during the in-progress merge can put the dirty foreign transcripts into the index without changing either their working bytes or HEAD. Therefore repeated `before_guard()` calls and the overlay PASS can still succeed. Root can then commit/push those staged bytes. The new actual-merge check at lines254–257 will detect the inclusion during finalize, after publication has occurred.

Static counterexample: preflight records dirty work W and clean HEAD H; root starts the expected merge; the foreign index blobs are staged to W while work remains W and HEAD remains H. Both checks in `foreign_tracked_unchanged()` pass, as do the unchanged owned-source/queue/state gates. A merge committed from that index contains W. Finalize rejects it, but cannot prevent the already-performed checkpoint/push. This is detection after publication, not prevention of accidental checkpoint.

Correction: reject any foreign conflict stage and require each foreign stage0/index blob to equal its recorded HEAD hash whenever `foreign_tracked_unchanged()` is called. Root must also perform an explicit index check **after all staging and before commit/push**, because no earlier helper check can authenticate a later index mutation. The helper need not write or restore these unrelated files.

## New guards confirmed by static reasoning

- `whole_scope=True` is confined to the exact resolved `whole_current_source_first_family` base. Its declaration must equal `['tmp/', '__pycache__/']` exactly; strict authored inventory ignores only these path components. Candidate/current/canonical checks permit zero declared exclusions and retain the no-symlink/path/byte/hash/exact-self-exclusion controls.
- Both exact historical malformed JSON paths must remain listed. Only these whole-scope paths get the special branch, and each must have exactly5202 bytes and SHA256 `2ba4c8c88686eeaa70cdb005658b3585a7b72cb5693a11d07e6fe046e52480af`. The branch expressly requires JSONDecodeError; successful parsing fails. All other JSON/JSONL parse failures remain fatal. A renamed, missing, altered, additionally malformed or candidate/canonical malformed file is not covered by this exception.
- Returned gate pins expressly include scratch exclusions and both dated malformed setup-artifact qualifications. These values propagate to preflight, overlay, acceptance and subsequent pin-equality checks rather than presenting the artifacts as successful receipts.
- The only allowed dirty tracked paths are the exact unrelated `commands.tsv` and `full_transcript.log`; preflight still requires no staged diff. Both are required to be tracked regular files. Current length/SHA, original HEAD SHA, dirty flag and explicit integration/checkpoint exclusion are recorded. Arbitrary dirty paths or exclusion-list changes fail.
- Repeated foreign work/HEAD checks are wired into integration `before_guard()`, preflight completion, mirror entry and locked prewrite/postwrite checks, and postvalidation entry/end. Actual merge blobs must match the foreign preflight HEAD SHA. These correctly detect working-byte changes and accidental foreign committed content; the remaining finding concerns staged content before publication.
- All previously corrected frozen candidate/source/ledger, queue live-preimage, actual committed overlay, inventory-ID-set, prior-state and exact-history-prefix controls remain unchanged by the textual diff.

## Limits and exact pending gate

This is static source reasoning only, with the previously explicit root-reviewed untouched automatic-queue hash and generated-receipt integrity assumptions. Checks do not atomically exclude noncooperating writers. No runtime controls or final schemas were reproduced. The new whole package is described as closed1795 members, but actual final root replay is still running; no final whole/root/live-execution PASS is issued or substituted here. No acceptance/push/proof/novelty verdict is transferred. The closed preparation source hashes remain the historical evidence for that earlier package.

## 2026-10-02T08:35:17Z — Preserved correction addendum

Correction re-review100%; acceptance execution0%. Independently read only the new index guard and associated root instruction. Revised `pr36_guards.py` SHA256 is `4f3a8c883581f6839b92c365d434d4e7aac23c2fd17a77d636b3f6085c154210`; revised `README.md` SHA256 is `6dcfe6b0e1ae5db3fadd942989f5ae6732865af4bcee9b86f37a9b654075cf7f`. The earlier reviewed hashes/finding remain the record of that earlier revision.

The staged-foreign finding is corrected within the called guards: lines229–234 require exactly one index-stage record for each exact excluded path, require its exact path, stage0 and regular mode100644/100755, and require the index blob SHA to equal captured HEAD. The original counterexample with foreign index bytes W and recorded HEAD H now fails before any guarded checkpoint result, while foreign missing/ambiguous/conflict/symlink stage records also fail.

README lines54–57 explicitly require root to inspect both exact foreign paths' staged diff after all staging and immediately before commit/push and confirm it is empty. This is the necessary human/root guard for staging performed after the last helper check; the helper does not itself run Git mutations or atomically authenticate future index states. Under that explicit final root check and the retained receipt-integrity/concurrency assumptions, no additional blocker was found in this narrowly requested correction. No helper execution/import, old-closed-folder write, shared/canonical/foreign mutation, Git/remote request, or final whole/root/live-execution verdict occurred.
