# PR191 independent lifecycle adversary05 report

Verdict: **REPAIR_REQUIRED**. Two required issues remain. This is an offline operational review of exactly frozen `lifecycle_controls_preparation_05` paired with frozen Root handoff v4. It is not publication/merge clearance, actual CURRENT-MAIN acceptance, scientific novelty certification, or a new scientific review.

Completed UTC: 2026-10-15T07:09:06.913470+00:00

## Independent method and bindings

The acceptance/attack plan and phase01 log were sealed at 2026-10-15T06:41:43Z, before source, author tests/reports, earlier adversary verdicts or Root handoff code were read. Plan SHA256: `43f30b5edfa1fa4c310649a0c672768d41329e73b1feffc29ada6cf3a5a2e866`. Explicit terminal05 pins then authorized this source review. I did not read or use the author harness, author audit report/results, or earlier adversary reports as evidence. The proposal seal itself necessarily contains author-summary metadata; I did not treat it as a verdict. All18 exact source-allowlist file identities/modes match the frozen manifest; author evidence files were hashed without being interpreted as tests or conclusions.

`INPUT_BINDINGS.json` binds every source file plus the exact Root handoff and dated556-pin seed. Principal SHA256 identities:

- Proposal seal: `de78b12cf2cf954aa205f17177ffc38bc07464fdc71b9234c17dc7429b009a91`.
- Actual common validator source: `dc883dcad2120b21e134070a5dc44f78f860ffd7cd711b89db8423f2da00a97f`.
- Gate contract: `1e4b5261a6caad196c523194c5cd27d3002a03814d953b66c442b2f627b667a4`.
- Root handoff v4: `c4f8f2c122e1954d3f3d5cf03d70cd0fe8a243e368efa166171c4aca97f4b548`.
- Dated carry-forward seed: `93a6aae3e4fb11e897495f0ab0955c33c540e9d2cbdaf4bab7331eae3bcce89b` (556 immutable pins; dated checkpoint de5e916ac752d03467d768e83fc46785e32ea002). It is not a fresh MAIN observation or authority.

`PROBE.py` builds synthetic independent native-object and kit/tracker service fixtures and calls the actual supplied operational validators. The positive fixture has50 native files and16 original artifacts. It implements explicit independent tree, blob, parent, full-tree delta, current MAIN, PR, service-state and call-count models. Coherent mutations update the changed body, selected byte/SHA/blob pins, complete map fingerprint, actual tree object and exact approved operative commit message. Thus the failures below are not malformed-map shortcuts. The source was not modified. Root handoff main and real operational adapters/helpers were never executed.

## Required issue1 — partial programme checks admit false current completion/intake facts

Affected source: `validate_programme_stage`, lines511–522, called by `verify_stage_postimage` and both `integration_accept` and `factual_accept`. `normalize`, lines284–299, deliberately removes stale completion aliases and generates explicit intake/receipt/pending facts; the acceptance validator does not verify all of those current facts or reject removed aliases.

Starting from the valid phase95 candidate, independently change exactly one current `CURRENT_PROGRESS.json` field and coherently regenerate the full map/tree/message:

| Changed field | False phase95 value | Actual result |
| --- | --- | --- |
| `actual_factual_checkpoint_accepted` | `true` (field reintroduced after honest normalization removed it) | Actual merge acceptance returned |
| `next_intake_requires_actual_completion_receipt` | `false` | Actual merge acceptance returned |
| `last_completed_actual_final_receipt` | `audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json` | Actual merge acceptance returned |
| `completion_metadata_checkpoint_pending_at_snapshot` | `false` | Actual merge acceptance returned |

All historical trusted Root prose, protected science, membership, counts39/23, checked priority flags, cursor191, advance=false, original head/effort, actual DOI and tracker facts remain unchanged. These are current operative aliases, not attacks on Root's semantic authority or dated historical prose. The receipt falsely blesses the complete current identities despite their contradictory acceptance/intake facts.

`COUNTEREXAMPLE_programme_*.json` retain complete selected maps and returned `ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED` receipts. The same attack family also passes final combined `factual_accept`: `actual_factual_checkpoint_accepted=true`, receipt-requirement=false, wrong last final receipt, or phase100 metadata-pending=true. Those reductions are `COUNTEREXAMPLE_factual100_*.json`; the returned status is `ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED`.

Required repair: verify the full current programme transformation, including fields the generator removes, retained completion/intake/receipt aliases and their exact stage values. Independently derive expected facts from the true parent and bound actual evidence; a producer-rehashed map or a partial expected-key subset is insufficient. Retain the trusted historical boundary and permitted unrelated descendants. Add coherent acceptance regressions for both95 and100 and positive stale-generation retry controls.

## Required issue2 — mutable current Root case-log content receives no stage validation

Affected source: `trusted_case_pins`, lines430–435, excludes Root `RESEARCH_LOG.md` from local static expectations, as required for mutable factual records. `verify_stage_postimage`, lines524–533, checks the two programme prose files but never checks current Root case-log content. Its selected hash proves only that some supplied bytes were adopted.

Starting from the valid phase95 candidate, preserve the complete trusted Root log history and honest newly generated lifecycle entry, then append only a new current factual entry with a valid later fixture UTC:

> PR191 actual factual MAIN acceptance complete; PR192 intake is already authorized and complete.

No actual factual acceptance or PR192 intake exists in that candidate. Recompute the exact selected map, tree, fingerprint and approved message. Actual `integration_accept` still returns its full-scope current-identities acceptance. `COUNTEREXAMPLE_case_log.json` records the full changed body, selected map and acceptance. The equivalent false current entry also passes the final combined factual consumer (`COUNTEREXAMPLE_factual100_case_log.json`), which does not establish that PR192 intake has occurred. No protected scientific bytes or dated history were rewritten. This is precisely the permitted mutable factual record boundary, not a demand to distrust every Root-authored authority.

Required repair: bind an independently approved immutable Root history/prefix and derive or strictly validate the complete generated current lifecycle suffix at95/100 against actual stage/evidence/timestamps. Revalidation of an old merge must use its own approved history and postimage, not later local mutable log bytes. Arbitrary new current claims of completed factual acceptance or PR192 intake must reject before the actual receipt. Preserve historical prose exactly.

## Strongest verified result and coverage

113 independent expectations executed.103 matched;10 negative mutations were accepted and reduce to the two required issues above. `RESULTS.json` contains every expected/observed result. `INDEPENDENT_CALL_TRACES.json` contains synthetic API call traces. No author test count contributes to this verdict.

Demonstrated positive controls include the entire check→stage→inspect→publish→inspect-published→one RAW append→two own/full observations→native95→metadata/ready→merge preparation/adoption/acceptance→native100→factual preparation/adoption/combined acceptance path. Service counters confirm one stage, one publish and one append in that flow. Fresh unrelated tracker additions after the own range and unrelated MAIN descendants are accepted; movement of the own range is forbidden. An unchanged100 generation survives unrelated stale-MAIN advance, is reused byte-for-byte on a fresh preparation and receives actual stub factual acceptance. The full fifty-file native derivation and companion identity remain valid afterward.

Demonstrated rejection controls include inert import side-effect sentinels, absent explicit runtime, draft/unresolved gate, wrong original head, duplicate science identity/evidence, unfinished latest review, absent exact operational clearance/projection, installed runtime drift, wrong publication environment/id/state/DOI/gate/time/files, fresh publication file/DOI drift, foreign tracker edits, duplicate DOI, own-row and target drift, rehashed protected scientific JSON, original16 byte drift, companion-manifest drift, unapproved static support/package/code content, hidden foreign full-tree mutation, false true-parent identity, extra message prose, metadata/head/ready drift, case scientific/effort/merged/authority drift and wrong workflow effective-status text.

The generation05 focused repairs work in these probes: coherent QUEUE changes to a foreign row, original claimed_solved2/5 or actual DOI each pass basic producer-map verification and then reject at actual merge acceptance. Both programme `UTC` and `updated_UTC` reject pre-evidence, future, invalid-value, non-UTC and reversed-order mutations at95 and100; equal accepted-evidence lower bounds and exact current-clock upper bounds pass. Native time checks also reject coherent future or pre-merge-acceptance100 generation. Commit-then-response-loss publication and append are reconciled through observations with no second POST/RAW append. An unknown absent earlier append forbids another write. Combined actual MAIN selection rejects drift of an original immutable support path.

## Paired Root handoff review

Frozen v4 was authenticated by exact length/hash/mode and inspected as source/AST only. Its Root final independent05 PASS authentication, zero outstanding repairs and bound report/seal/proposal checks precede exclusive runtime creation and authority issuance. It requires the exact nine runtime filenames, matches their frozen bytes, refuses every pre-existing canonical runtime/authority output and writes with exclusive creation. It matches carry-forward inputs before installation, constructs the scientific projection through the pure reviewed constructor, validates a virtual gate before saving it and validates the saved gate. It imports no process/network service client and performs no actual publication/tracker/PR/Git operation itself. It still requires a fresh truthful Root final PASS; this REPAIR_REQUIRED review cannot satisfy it. Its main remained unexecuted. Partial filesystem failure reconciliation and real service concurrency remain operational concerns, not certified away by offline fixtures.

## Scientific qualification and live boundary

Original PR191 head remains a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe, original status claimed_solved and effort2/5. The unchanged two whole-science reviews were not re-certified here. The qualified accepted claim remains: imported bare-A0/signed conjunction is false for every n>=5; explicit parity-selected signed law/existence holds for all n>=3. Ferudun's exact prior theorem/mechanisms are credited. No novelty, firstness, historical priority, current openness, authenticated erratum or certified independent discovery. Extensive AI; unrefereed.

All service/native observations in this report are synthetic fixtures; none proves actual publication, DOI, tracker append, PR metadata/ready/merge, canonical installation or CURRENT-MAIN factual acceptance. Actual programme remains39 completed/23 published as supplied. No PR192 intake is authorized by this report. The precise remaining operational gap is repair of issues1–2 followed by a fresh different independent reviewer and Root authentication; actual services and actual full-scope MAIN acceptance must occur only under later authority.

## Reproduction, safety and completion

Run the sealed probe with Python `-B` and a NEW output directory beneath this adversary05 folder. For example: `python3 -B PROBE.py /absolute/path/to/lifecycle_adversary_05/reproduce_run_01`. The script preserves the original pinned source location and rejects an output directory outside this folder or an already existing supplied reproduction directory. No credentials or production helpers are needed. The source common SHA is checked on every load. Default execution would regenerate audit outputs, so use the explicit fresh directory to preserve this seal. Scratch fixtures are excluded from `PUBLIC_SAFE_ALLOWLIST.json`; only exact safe filenames with a `files` key are selected. The final manifest binds artifacts and the seal binds that manifest without a hash cycle. Final public artifacts are0444.

All substantive research artifacts and disposable fixtures were written in this assigned folder. One procedural deviation occurred during finalization: an unintended zero-byte `/tmp/pr191_adversary05_finalize_instruction_unused` marker was created, verified empty and immediately deleted. It contained no research or user content and changed no project/service/Git/authority state. This is disclosed rather than claiming a literal zero out-of-folder filesystem write. No network, credentials, production/native-helper execution, Git/index/ref/branch/checkout operation, external outreach or shared/scientific edit occurred.

The final operational audit is100% complete as a review; candidate operational acceptance remains REPAIR_REQUIRED. This percentage measures completion of this independent audit, not discovery, remediation, publication or the wider research goal.
