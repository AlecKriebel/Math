# Independent lifecycle adversary 04 — REPAIR_REQUIRED

Frozen generation: lifecycle_controls_preparation_04. Original PR191 HEAD: a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe. Original claimed_solved effort: 2/5.

Verdict: **REPAIR_REQUIRED**, with two concrete required repairs. No publication, DOI, tracker, PR metadata/ready transition, merge, CURRENT MAIN acceptance, intake192 authority, or live action is certified. The independent review is complete for this frozen generation; the lifecycle is not cleared.

## Evidence and independence

The independent acceptance plan and fixture design were sealed before reading the implementation. Standard-library raw native-object and service fixtures were then materialized before reading current source. No author harness/results or prior adversary reports/judgments were opened or used. Current proposal seal/allowlist metadata and SOURCE_BINDINGS metadata were read only to identify and verify inputs. The full current common runtime, eight adapters, contract, and Root v2 handoff were read.

The executed probe is `independent_probe_04.py`; its preinspection foundation is `independent_fixtures_preinspection_04.py`. It imports only the frozen proposed common runtime and standard-library/synthetic test objects. No production native helper module is imported. It substitutes an explicit synthetic clock, case directory, native API object store and actual-entrypoint service runners. The actual `gate`, publication/tracker consumers, preparation, merge acceptance and factual acceptance functions run without replacing their validators.

Final executed checks: **78**, of which **66 behaved as required** and **12 accepted inputs that should reject**. The 12 failures reduce to the two findings below. A second execution reproduced every per-probe result, including native object and receipt identities, exactly; only the run-level wall-clock field differed. See `PROBE_RESULTS_04.json`, `REPLAY_RESULTS_04.json`, and `REPLAY_VERIFICATION_04.json`. These are synthetic offline observations, not actual service receipts.

Trusted Root semantic assertions are honored. The tests do not arbitrarily rewrite Root's dated status authority or demand cryptographic attestation. The actual mutable Root CURRENT_CASE_STATUS/RESEARCH_LOG/current-template files were not used as fixture authority or treated as frozen review inputs. The 18 scientific/identity values are represented by independently constructed synthetic Root authority. Current source and handoff hashes were verified against the explicit terminal04 pins. The strongest announced 513-member immutable seed was verified by bytes/hash/count only; it is a dated seed, not a current MAIN observation or clearance.

## R1 — Prepared QUEUE content is not independently checked at acceptance [P1]

Frozen common runtime locations: `queue_update` starts at line467; `verify_stage_postimage` at523; `integration_accept` at541; `factual_prepare` at550; `factual_accept` at560.

`queue_update` enforces an own-row-only transformation while the honest producer prepares a merge. Its result is not independently rederived when the prepared merge is consumed. `verify_prepared` binds the selected map, actual true parent, full tree delta and exact operative message. `verify_merge_scope` independently binds the protected case/native/package inputs and exact path set. Those checks do not determine the permitted bytes of the shared QUEUE file. The queue guard receipt is selected but not consumed to check this postimage.

Independent reproduction:

1. Run the complete valid fixture through the actual gate, exact-kit stage/inspect/publish consumers, RAW tracker append/fresh own/full reads, native95 generation, original-head metadata/ready binding, final scope and two-parent preparation. Its selected set contains164 paths; the actual first parent and all qualified scientific/control/native bytes are intact.
2. Change only the selected `unsolved_math_prioritization/QUEUE.md` content. One test changes a foreign row cell; another changes PR191's own `claimed_solved`/`2/5` to `solved`/`5/5`.
3. Construct an independent native in-memory commit with the same true parents and exact expected path set. Recompute that file's blob/size/SHA256, the full selected-map fingerprint, exact approved operative message marker, tree, commit and full changed-path delta. No gate/protected/native/programme/case fact is altered.
4. Call actual `integration_accept` with the coherently bound candidate at synthetic current MAIN. Both mutations receive `ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED`.
5. For the foreign-row mutation, continue through actual `factual_prepare` and `factual_accept`. The corrupt foreign row remains and the runtime returns `ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED` with conditional40/24 and later192 authorization.

Failing probes:

- `coherent_refingerprinted_foreign_QUEUE_row_change`
- `coherent_refingerprinted_own_QUEUE_status_effort_change`
- `foreign_QUEUE_corruption_survives_both_factual_boundaries`

This is not a path-scope bypass or a hash collision. The wrong contents of a permitted shared path are faithfully fingerprinted and subsequently treated as accepted authority. It violates preservation of foreign research rows and the original historical status/effort.

Required repair: independently derive the exact approved QUEUE bytes from the prepared merge's actual first-parent QUEUE, original PR191 HEAD QUEUE, actual proof-parent BASE QUEUE, and accepted DOI/URL, using the existing bounded transformation. Compare the prepared commit's complete QUEUE body and selected identity to that result at the acceptance boundary. Revalidate the same original merge postimage at both factual stages. Keep all foreign row bytes unchanged and preserve claimed_solved/2/5. Add both coherent-content counterexamples and the whole factual continuation as regression cases. A producer-rehashed selected map alone must not authorize the QUEUE body.

## R2 — Programme JSON factual dates bypass the evidence interval [P2]

Frozen common runtime locations: `legal_fact_time` at494; `validate_programme_stage` at511; `verify_stage_postimage` at523. The same stage verifier is consumed by merge acceptance and both factual stages.

The runtime bounds native, case, workflow and new programme prose timestamps against accepted external facts and the current validation clock. It never validates the generated programme JSON `UTC` or `updated_UTC` fields in `validate_programme_stage`/`verify_stage_postimage`.

The independent clock is fixed at2026-10-15T05:00:00+00:00. Publication, tracker and merge evidence use that instant. A programme field changed to2026-10-16T05:00:00+00:00 is in the future;2026-10-14T05:00:00+00:00 predates the required evidence. Both values pass for either field at both95 and100. A malformed `UTC` of `not-a-timestamp` also passes at factual100.

Each probe changes only the relevant programme JSON field, coherently recomputes the native prepared map/tree/message/commit, and retains all scientific, census, cursor, authority, case, native and prose checks. Merge acceptance or factual acceptance returns its success receipt.

Failing probes:

- `programme_date_UTC_future`, `programme_date_updated_UTC_future`
- `programme_date_UTC_predates_evidence`, `programme_date_updated_UTC_predates_evidence`
- `factual_programme_date_UTC_future`, `factual_programme_date_updated_UTC_future`
- `factual_programme_date_UTC_predates_evidence`, `factual_programme_date_updated_UTC_predates_evidence`
- `factual_programme_date_UTC_malformed`

Required repair: validate both generated programme JSON date fields with the same UTC schema and evidence/current-clock bounds at the95 and100 consumption boundaries; phase100 must also respect actual merge-acceptance time. Enforce any intended ordering between the two fields. Revalidate them when the original95 merge is consumed by later factual stages. Preserve old historical dates and reuse of an unchanged immutable generation during a fresh-MAIN retry; do not add a blanket recency expiry. Add future, pre-evidence, malformed, boundary-equal and merge-lower-bound regression cases.

## Strongest independently verified positive result

The complete synthetic positive flow passes the actual frozen04 entrypoints: valid Root gate; two distinct science review identities; mandatory operational/runtime9 clearance and case projection; exact kit stage/inspect/publish with fresh read-only consumption; one RAW tracker append, two own/full reads, uniqueness, foreign preservation and sanitized evidence; native95; original-head PR metadata and ready-state binding; native true-parent two-parent preparation and merge acceptance; native100; factual preparation and combined-current factual acceptance.

Independent full-byte native oracles match all50 files at both95 and100. Every original16 artifact remains byte-identical. Rehashed modifications to proof, support, original, JSON, text and log native content reject. Direct prepared substitutions for protected support, paper, proof, scientific review, control and gate reject even after full coherent producer rehashing. Case novelty, original effort, actual publication alias and percentage attacks reject. Wrong operative messages, true-parent bindings, omitted selected QUEUE path, extra foreign tree paths and companion-manifest mismatch reject. Changes to original selected protected identities at descendant CURRENT MAIN reject. Original merge authority drift is revalidated at factual acceptance.

Unknown publication and tracker writes reconcile from fresh reads without a second write when the synthetic server committed. Unknown outcomes without an observed commit prevent blind retry. The accepted tracker consumer reobserves target/own/full state; altered foreign rows, duplicate DOI rows, header and own-cell drift reject. A private foreign-row sentinel is absent from generated public JSON receipts. A stale-MAIN retry preserves exactly the same generated100 bytes and selected map, then accepts after a synthetic unrelated descendant change. Both prepared stages retain live cursor191; actual factual receipt alone conditionally authorizes subsequent192 intake and requires the next own checkpoint to update the live programme.

## Root v2 handoff and limits

Pinned Root handoff:7821 bytes, SHA2566df49335d56f411836ca1206e2cfca04817bf84c6c5cf5e9d47750818c50aac5, mode0444. Its source/AST requires the exact nine runtime filenames, verifies accepted source bytes and distinct independent report/seal bindings, checks Root04 PASS semantics before the installation loop, rejects pre-existing canonical/authority files, installs with exclusive `xb`, invokes the pure case scientific projection constructor, and locally validates the virtual gate before writing the actual gate. Its standalone `fresh` helper was exercised in the dedicated sandbox: a repeated filename rejects and leaves the original0444 bytes unchanged.

The actual Root `main()` was never executed, in accordance with the explicit prohibition. Full Root issuance and interruption/recovery were inspected statically, not dynamically executed. No PASS for actual Root publication authority is inferred. A valid later Root semantic authentication would still need to bind a newly accepted repaired generation and a fresh independent review; this REPAIR_REQUIRED report cannot supply that authentication.

No external service, credential, production helper, Git executable/index/ref/branch/checkout, shared Root editor, or external individual was accessed or contacted by the probes. API paths named `git/...` are keys of the independent in-memory object service, not real Git or GitHub requests. No mathematical novelty/firstness/history/independence/current-openness claim is made. The qualified scientific result and existing Ferudun attribution supplied by Root remain the scientific boundary; this review did not redo the two whole-science reviews.

The sealed attack plan is broader than the executed probes. Unexecuted combinations and real-service concurrency remain limits; the concrete failures already prevent PASS. Hashes of synthetic receipts do not attest live facts. The safe publication allowlist names only this review's explicit public-safe artifacts and excludes every scratch service/native fixture under `work/`.

## Reproduction and next step

From this directory, run Python with bytecode disabled on `independent_probe_04.py`, giving `--results` a new filename such as `NEW_REPLAY_RESULTS_04.json` to preserve the sealed results. It writes only this dedicated review directory and uses injected services exclusively. Expected frozen04 outcome:78 checks,66 as required,12 failures in the two stated families.

Repair both findings in a new frozen generation, bind the repaired Root handoff to it, and obtain a new independent adversarial review. Retain this generation and its failure evidence unchanged. Actual baseline totals remain39 completed/23 published, and cursor191 remains active until actual factual CURRENT MAIN acceptance and its next own receipt checkpoint.
