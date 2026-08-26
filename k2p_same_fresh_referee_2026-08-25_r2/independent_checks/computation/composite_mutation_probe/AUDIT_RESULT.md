# Independent corrected-composite mutation audit

Date: 2026-08-25 PDT
Scope: bounded mutation execution only; no full suite; isolated tree read-only.

## Verdict

Overall bounded execution: **PASS**.

- Four complete deterministic mutant ledgers were created in scratch and sent
  to the untouched production independent verifier.
- All four returned exit code 1 at the intended row-semantic diagnostic, before
  any final ledger/checksum diagnostic, and none created a verifier success
  report.
- The explicit `source_to_target` -> `target_to_source` transport attack was
  rejected. This confirms the verifier's direction constant is live, not merely
  decorative.
- Parent identity, physical port assignment, and theta2 inherited-child census
  were likewise rejected at their intended semantic gates.
- The isolated source hashes were identical before and after execution.

Qualification: the frozen production suite has no dedicated explicit
reverse-direction mutation. Its `broken_transport` case swaps in another valid
transport hash, and its rank case checks a directed source/target inequality.
Thus production-verifier direction binding is **PASS** by this independent
probe, while dedicated direction-specific coverage in the frozen mutation
artifact is **FAIL (absent)**. The official inheritance mutation changes the
child count; other descendant tuple leaves are equality-bound by the verifier
but do not each have dedicated frozen mutations (**UNVERIFIED individually**).

## Exact production route

Production mutation runner:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee/work/corrected_composite_ledgers/run_composite_mutations.py`

- lines 23 and 668 resolve the support module and verifier;
- lines 510-538 construct and run the production verifier argv;
- lines 565-595 require nonzero exit, the intended diagnostic, and no report;
- lines 601-642 define the two non-ledger guards;
- lines 723-758 enumerate semantic cases, then the two guards.

Production verifier:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee/work/corrected_composite_ledgers/verify_corrected_composites_independent.py`

- lines 29-33 resolve project/package roots;
- lines 112-119 dynamically import the atlas from
  `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee/package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py`;
- lines 322-335 reconstruct raw4 parent/transport evidence, including
  `direction: source_to_target` at line 328;
- lines 253-265 reconstruct theta2 restoration-descendant inheritance data and
  lines 386-394 require the complete evidence tuple;
- lines 440-464 enforce canonical row order, coordinates, ports, quartet data,
  and family-specific evidence;
- final byte/hash gates occur only later, at lines 473-477;
- lines 523-527 add the `CORRECTED_COMPOSITE_REPLAY_FAIL:` process-exit prefix.

The exact argv for every executed case is stored in
`bounded_probe_report.json`. The common form was:

```text
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B
/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee/work/corrected_composite_ledgers/verify_corrected_composites_independent.py
--family FAMILY
--ledger /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp/composite_mutation_probe/CASE/complete-mutant-ledger.jsonl.gz
--summary /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee/work/corrected_composite_ledgers/artifacts/FAMILY_corrected_composite_summary.json
--report /Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/tmp/composite_mutation_probe/CASE/unexpected-verifier-report.json
--skip-heavy-full-map
```

Working directory for every verifier process:

`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-25_r2/isolated/k2p_principal_d_plus_submission_referee`

## Fresh bounded executions

| Case | Raw ID | Exact diagnostic | Mutant SHA-256 | Rewrite / verifier / total seconds | Status |
|---|---:|---|---|---:|---|
| raw4 wrong port permutation | 0 | `CORRECTED_COMPOSITE_REPLAY_FAIL:PORT_PERMUTATION:0` | `fcd2f649befe0175b30d47c87d421826e613f465a5a31dd22e6a97d1931ad66f` | 2.314900 / 3.522315 / 5.837550 | PASS |
| raw4 wrong restoration parent | 2185 | `CORRECTED_COMPOSITE_REPLAY_FAIL:RAW4_RESTORATION_EVIDENCE:2185` | `fbf0ddf28ec78f8bf1b1a6d07c132f43ff98d774d8089f1a07e78520e6aec3fe` | 2.340508 / 5.846434 / 8.187266 | PASS |
| raw4 reversed transport direction | 2185 | `CORRECTED_COMPOSITE_REPLAY_FAIL:RAW4_RESTORATION_EVIDENCE:2185` | `7794d2642b93c3a23f7c9ddefdccbcf6f2fc592298ff5ab4a016558fdaeb3be2` | 2.258647 / 6.242249 / 8.501306 | PASS |
| theta2 missing inherited child | 166201 | `CORRECTED_COMPOSITE_REPLAY_FAIL:THETA2_ISOMORPHISM_EVIDENCE:166201` | `37701995f32077958f7033f582e1750d07cea33bd3bbdd60daa9cedcfe5a7faf` | 17.250386 / 45.205449 / 62.456625 | PASS |

The explicit reversed-direction transport hash changed from
`b400540b0422a32135ebc851f6363d48ec0715b9f9c03872b19a99fb67d7f39f`
to
`2285a98b03c0a13e661f348a4d4a951072ce2641f3cf7eaf4c08d42884ee238f`.

For each case: verifier exit 1; intended diagnostic present; checksum marker
list empty; verifier report absent. Classification:
`semantic_row_validation_before_checksum`.

Probe command, from this directory:

```text
/usr/bin/time -p /usr/bin/python3 -B run_bounded_probe.py 2>&1 | tee bounded_probe_console.log
```

Observed outer runtime: real 85.23 s, user 81.08 s, sys 1.32 s. Internal
case-loop runtime: 85.094670 s.

## Frozen mutation diagnostics (integrity checked, not fully rerun)

Raw4 report file SHA-256
`83196bc33504fd1e17c8784d2c7530f358e85cff8161c8e5f14ba04a60c42d76`;
payload
`dc265e02da504666197320fcab90226fa44cfc5c5906bb4ef5b6f1ab35d44f02`.
Its payload recomputes, status is PASS, survivors are 0, and all 12 semantic
cases record nonzero exit, intended marker, absent verifier report, and
rejection. Exact markers:

| Mutation | Marker |
|---|---|
| omitted_raw_row | `RAW_ID_ORDER:0` |
| duplicate_raw_id | `RAW_ID_ORDER:1` |
| wrong_port_permutation | `PORT_PERMUTATION:0` |
| reassigned_category | `QUARTET_CATEGORY:0` |
| reassigned_evidence_binding | `QUARTET_WITNESS:0` |
| false_rank_exclusion | `RAW4_RANK_EVIDENCE:97` |
| rooted_restriction_reintroduction | `FORBIDDEN_ROOTED_TOKEN:0` |
| wrong_restoration_parent | `RAW4_RESTORATION_EVIDENCE:2185` |
| broken_transport | `RAW4_RESTORATION_EVIDENCE:2185` |
| reassigned_cubic_certificate | `RAW4_TERMINAL_EVIDENCE:357409` |
| reassigned_quartic_certificate | `RAW4_TERMINAL_EVIDENCE:154800` |
| reassigned_quintic_certificate | `RAW4_TERMINAL_EVIDENCE:69457` |

Theta2 report file SHA-256
`ec2c6ec092539048b4e7ab9d9cfea01caa985d0f35cae74ca56732dc4cfe4c84`;
payload
`5663b87d3f09eaac5e89db69ac5a1cf6069b308abf9bc4242650d0897ded1ff7`.
Its payload recomputes, status is PASS, survivors are 0, and all 10 semantic
cases record the same fail-closed conditions. Exact markers:

| Mutation | Marker |
|---|---|
| omitted_raw_row | `RAW_ID_ORDER:0` |
| duplicate_raw_id | `RAW_ID_ORDER:1` |
| wrong_port_permutation | `PORT_PERMUTATION:0` |
| reassigned_category | `QUARTET_CATEGORY:0` |
| reassigned_evidence_binding | `QUARTET_WITNESS:0` |
| false_rank_exclusion | `THETA2_RANK_EVIDENCE:19161` |
| rooted_restriction_reintroduction | `FORBIDDEN_ROOTED_TOKEN:0` |
| missing_restoration_child | `THETA2_ISOMORPHISM_EVIDENCE:166201` |
| reassigned_quadratic_certificate | `THETA2_QUADRATIC_EVIDENCE:166200` |
| broken_transport | `THETA2_ISOMORPHISM_EVIDENCE:166201` |

The remaining two cases in each frozen report are deliberately non-ledger
guards: `python_optimized_mode` and `source_tree_immutability`. The former is a
verifier optimized-mode guard; the latter does not invoke the verifier. They
are wrapper/guard checks by design. No frozen semantic ledger attack is recorded
as checksum-only or wrapper-only. Fresh execution of the 18 semantic cases not
selected for this bounded probe is **UNVERIFIED in this audit**.

## Hashes and immutability

| Role | SHA-256 |
|---|---|
| production mutation runner | `0d5f43ffe827015fe43404d627ef962b930f059752491fe77fdef5a1f4c7ec34` |
| production verifier | `67ddf315b400a0a96f4a5901e6a340a158d9d4fd1111e8ee17193de5d78b5690` |
| support module | `6fad3ac902653659ab69b53c1e9f61908e760d2fcd72cc4d88aa58e8072fc35a` |
| atlas import | `37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad` |
| raw4 source ledger | `431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96` |
| raw4 summary | `9a2b340eb10e73abf0ea7c7aba5ae7c69942eea0f75402408f52277d960d648e` |
| theta2 source ledger | `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659` |
| theta2 summary | `cf4ee4c23068cbc644474ad0161510a99106d3235f28e722fd3340b5bbbb3fdb` |

All eight hashes matched before and after the probe: **PASS**. Full mutant
ledgers and unexpected report paths were deleted after each case. The retained
machine report file SHA-256 is
`1ea89890987b6b675da080bd38fe8bcedb409c9c40466ab275d7c116bbc3612a`;
its internal payload recomputes to
`055ef32f589d7ec941120d5bf8f60ea58ec23066ed3db6e9f4b36c2d0123ca60`.
