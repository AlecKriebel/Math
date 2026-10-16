# PR952 candidate02 operations repair

This sealed revision repairs an operational source-identity bug detected by root's actual read-only preflight before any full review or acceptance. Candidate01 and the entire sealed operations_engineering_01 folder remain preserved. The paper, PDF, ZIP,173-file package, descriptor, exact target HEAD, statement, review hash and28 inherited finding IDs are unchanged. This family performed no real Git/service call or mutation.

## Exact repair

The previous core incorrectly assumed `prior_research == {}` for both the frozen private record and the raw SQLite report. That PR948-specific assumption is invalid for PR952. PR952's actual report is a nonempty dictionary, with canonical SHA256 `ad708f96865972507a28c13ba5425c1bf41bb2607c60e5ecfa4197328b629c25` under the existing `json.dumps(prior,sort_keys=True).encode()` convention.

The repaired actual `source_gate` requires:

- Unchanged entire private-record SHA `f7d80d30437d531fe6dab53b567032dd74253872420267b93d466c2aa93a1510`, exact target/review identity and a dictionary prior report.
- That entire frozen prior report has the exact canonical SHA above.
- The unchanged nested statement SHA `87dd83734fc8c51eb132f501c5d05947ed7057268dfba61627fb78f53da10af8`.
- Exactly one row from the same read-only/immutable SQLite query, with the raw problem **and full raw prior report** exactly equal to the frozen values.
- The existing review SHA `12e089388884a531bdc98f888e203ec0be06aa637e3ce342ac1e502a7af266f5` reconstructed from the exact `[raw_problem,raw_prior]` values.
- All existing current-catalog present/no-holds/statement/review and related-target checks.

There is no source normalization, metadata waiver, content deletion, turn-accounting change or scientific adjudication. The prior record's triage/search content remains source evidence for independent evaluation; matching it does not certify its conclusions. Successful source observations now include the prior-report SHA and `raw_prior_report_matched_frozen_report:true`, without publishing its body.

## One separate root operational finding

`REQUIRED_ROOT_FINDING_IDS` is exactly `{'R952-OPS-ROOT-01'}`. Every clean current whole-package review must separately verify that ID in `RESULT.prior_issue_resolution` using the existing `{verified:true,evidence:nonempty-string}` schema. It must **also** independently verify all28 unchanged inherited IDs in `RESULT.inherited_finding_dispositions` and every earlier required/optional review finding. Missing root disposition rejects. No inherited ID is added, renamed or removed.

Current freezes must include `A/ROOT_OPERATIONAL_FINDINGS.json` in `evidence_files`; the historical repair-pending record is immutable. There is **no additional FREEZE key**. The acceptance receipt additionally exposes `required_root_operational_findings:["R952-OPS-ROOT-01"]`; all later acceptance loads require that exact list. Historical candidate01 evidence is authenticated under its original snapshots without retroactively requiring a finding record that did not yet exist. Old candidates cannot count as clean current reviews.

Root may create a separate actual resolution observation after the fresh source preflight. Keep it outside the already-frozen candidate unless root intentionally produces a new candidate/review cycle. Neither this handoff nor inert tests resolve the finding on root's behalf.

## Integration and actual next step

Authenticate this folder's external MANIFEST SHA and its exact explicit public members first. As in revision01, `path_base` is `repository_root`; bytes/SHA/mode records include the six actual current top-level adapters plus unchanged kit. Only accept_pr952.py changed; the five thin wrappers remain byte-identical. Do not recursively publish private_tmp or source fixture bodies.

Run `python3 -I -S -B integration_inputs.py` from this folder. It is read-only and emits exact serialized `operations_inventory_json`, `freeze_json` and proposed settings. Candidate revision is now2. It binds the root operational record, candidate01 archive observation and immutable-object prefetch observation, alongside all previous current-family/source/protocol/package evidence. The final saved `INTEGRATION_PREVIEW.stdout.json` is the actual successful output for this repaired core and can be independently authenticated and used unchanged. Its exact strings, rather than a reserialized dictionary, go to the authoritative inventory/FREEZE paths **only by root**. Never replace candidate01's archived inventory, freeze, code or evidence.

The whole schemas, review own-attack/START/END/cold protocols and other adapter contracts described in the unchanged revision01 INTEGRATION.md remain applicable, except this precise source-report/root-finding repair and candidate2 setting. The revised test/code files in this seal are authoritative for current operations; the old01 manifest's former top-level core hash maps to the preserved candidate01/operations snapshot. PRESERVATION_CHECK.json verifies old01 MANIFEST SHA `3fc478015918320f37f980632b9f6aa78a012f5444a85404ccf56ab39e346c7e`, all48 of its own sealed payloads, and the exact archived old core. It does not claim the historical core equals the repaired root core.

Before any fresh full review, root must run and retain an actual successful current-source preflight through the repaired authenticated core:

```
python3 -I -S -B /ABS/accept_pr952.py --operations-sha256 EXTERNAL_CURRENT_INVENTORY_SHA --freeze EXTERNAL_CANDIDATE02_FREEZE_SHA --preflight-only --observation-dir /ABS/ROOT_OWN_EXISTING_FOLDER
```

Preflight remains read-only: observations only in the supplied own folder; fixed validator/source/history paths; no Git fetch; no service mutation or acceptance. Only root can observe whether the actual current source succeeds. The packet still needs fresh sequential independent ENTIRE current-freeze reviews before acceptance/merge/publication. A changed computed status is still an observation; changing live base inside source/path gates still rejects.

## Checkable evidence and limitations

The actual source_gate function runs unmodified in18 new controls under each of normal/O/OO. An ephemeral synthetic SQLite/cache fixture is populated from the actual pinned private problem/report; no private body is printed or retained. Two positive passes match the actual nonempty report and existing review hash. Negative cases test altered/empty/null raw reports, altered raw/private statement, private-byte identity, separately isolated canonical-report and recomputed-review guards, current catalog holds/absence/hashes, related membership, duplicate/missing rows. SQLite bytes and directory entries remain unchanged across every source_gate invocation. Test-only repins alter only the loaded harness namespace to reach deeper independent guards; no production constant is rewritten by tests.

The full inert operations suite now has61 controls per normal/O/OO run, including an explicit missing-root-finding rejection. All79 combined controls pass in all three outer modes. Preliminary passing runs are retained separately from final passing runs with exact core/test-source pins and raw stdout/stderr. The actual local candidate02 whole-freeze/descriptor validation also passes:183 payload paths,29 evidence pins, five original root family seals and28 inherited IDs. It gives no scientific/full-review credit.

No live source preflight, actual service behavior, scientific acceptance, or publication action is supplied by this family. Root's earlier failed preflight is retained as adverse history. Installed interpreter/stdlib/host, externally authenticated inputs and reviewer integrity remain trust roots. No claim is made that tests reproduce the historical Linux profile or remove priority/source coverage gaps.
