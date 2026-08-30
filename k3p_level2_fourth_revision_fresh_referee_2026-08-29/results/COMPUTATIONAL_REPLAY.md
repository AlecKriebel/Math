# Fresh portable replay: exact execution record

Date: 2026-08-29

## Bottom line

The documented `all` route was launched **exactly once** in a sealed-only
copied package under an externally enforced network-denying, credential-free
macOS sandbox.  It was never duplicated or restarted.

- Fresh verification: **PASS, 4/4 commands**, 2,977.293 seconds, empty
  undeclared workspace drift and empty virtual-environment drift.
- Fresh regeneration: **38/55 commands passed**.  Command 39,
  `probe_hour_scale_producer`, then failed exclusively with
  `OSError: [Errno 28] No space left on device` while closing its gzip ledgers.
- Commands 40--55 were not invoked.  The runner failed closed and returned 1;
  it did not create a regeneration report, postflight summary, or PASS sentinel.
- In accordance with the user's instruction, the failed long process was
  **not rerun**.

This is an external resource failure, not an observed semantic or mutation
failure.  It prevents me from claiming a fresh complete 55-command
regeneration in this audit.  It does not negate the 4-command current verifier
PASS, the 38 current regeneration passes, or the other evidence described
below.

Machine-readable summary:
`official_replay/REPLAY_SUMMARY.json`, SHA-256
`437d8a6ab464e6c4cd7650342d386a0bc75c5a3cdbdfcba68711b7af46e90583`.

## Isolation and environment

The clean execution copy omitted the supplied folder's pre-existing unsealed
`review_runs/` and `.venv`.  It passed package integrity before execution.  The
outer process ran inside a Seatbelt profile denying network access and allowing
writes only within the copied package's runtime area.  Its child environment
had the runner's exact ten-key allowlist.

Runtime:

- macOS 26.5.2, arm64;
- Python 3.14.6, executable SHA-256
  `b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf`;
- mpmath 1.3.0;
- networkx 3.5;
- numpy 2.5.2;
- sympy 1.14.0; and
- pinned requirements SHA-256
  `5a731eb61d5928e5b724c065e64d64af03804d25e25b49928f369d9d6b4da95b`.

The plan-only route was run beforehand and reconstructed the exact ordered
55-command mathematical plan.  The Git-bound 37-case release-engineering suite
is deliberately outside that plan and was reproduced separately in a clean
exact-commit worktree.

## Verification phase

All four commands passed with exit code zero and their required sentinels:

| Command | Seconds | Result |
|---|---:|---|
| `release_input_semantic_bindings` | 0.213 | PASS |
| `integrated_artifact_binding` | 0.321 | PASS |
| `integrated_fresh_independent_replay` | 2,961.961 | PASS |
| `integrated_classification_mutations` | 13.374 | PASS |

The fresh integrated report certifies all 20 child checks and has logical
payload SHA-256
`4574c1e5b4c373e909e77aba792d3e2b3189c8ea8aaa7bd1e0948f5ced2c5f80`.
The runner restored the canonical location-dependent report to mode `0644`.
The mode control passed, including all six enumerated existing/new cases and the
negative unsafe replacement mutation.

Evidence hashes:

- report:
  `df3fc24df0f7a42a70506e4118bd00d033038f9af93acff4cd6bd3a1010da457`;
- transcript:
  `98b7bc561e8900074e12bc8f0d925237915d331dddf5d2fbf66f58cec301a99f`;
- copied detailed fresh report:
  `a0465b6bcbda499b263748039e45e5b9a501a9e5ddec49616a32d5f93c9dce2d`;
- mode-control stdout:
  `309da296289aa8552c06354a333e6f55547c1f0fa5abfb4419a708b96e04d5a0`.

The before/after inventories show no undeclared workspace change and no
virtual-environment change.  The sole declared runtime addition is
`release/work/referee_integrated_fresh_report.json`.

## Regeneration phase before the resource failure

The first 38 commands all produced a `RESULT` row with exit code zero,
`status=PASS`, and required sentinel observed.  Their child-time sum was
2,138.644 seconds.  This includes the entire revised cut cone, ordinary and
optimized typed cut verifiers, all cut mutations, the literal tree--sunlet
suite, the complete four-port producer, the graph-only non-four anchor
producer, the complete restoration producer and independent replay, and the
four-port structure/mutation checks.

Notable fresh results were:

- cut topology graph regeneration: 275.912 seconds;
- four-port 405,216-presentation producer: 741.778 seconds;
- 133-row non-four anchor universe: 194.373 seconds;
- 36,824-edge restoration producer: 621.173 seconds;
- independent restoration replay: 76.185 seconds with zero unresolved rows;
- restoration mutations: 20/20 rejected; and
- full four-port coherent mutations: 6/6 rejected.

The revised direct/adversarial cut cone, including ordinary and optimized
semantic checks, passed before the failure.  Thus the commands most directly
changed to repair the third-revision certificate defect were freshly executed
in this run.

## Exact failure boundary

Command 39 started normally.  It completed all 176 one-port anchors and
reported:

```text
one-port raw=29964 survivors=2107
counts={'displayed_quartet_mismatch': 27758,
        'isomorphic': 1915,
        'k3p_tree_sunlet_sos': 99,
        'triangle': 192}
```

It progressed through two-port parent 600 of 2,107.  It then emitted repeated
`Errno 28` failures while flushing `two_port_ledger.jsonl.gz`,
`exact_transport_ledger.jsonl.gz`, and `parent_restriction_ledger.jsonl.gz`,
ending with:

```text
CORRECTED_PROBE_FAIL:[Errno 28] No space left on device
```

No mathematical assertion, invariant check, mutation, or equality comparison
failed before the `ENOSPC` stop; later checks were not reached.  The runner
correctly converted the child exit to
`K3P_REFEREE_ACTIVE_VERIFIERS_FAIL` and stopped.  The complete partial
transcript has SHA-256
`9eaeaf563fd1ee219e533142addb893db90f4191ac12747a86042facd2e80153`;
the outer log has SHA-256
`7e27eff75f0bdf47fa225cd7a2f70ef674676e31de562334d1dc177e9f5aa03d`.

The transcript establishes an OS-level capacity failure.  Free-space spot
checks varied sharply (947 MiB after one cleanup and 139 MiB later), but no
synchronized measurement at the exact failing write or attribution of the
missing space to another process was preserved.  I therefore classify the
observed exit as environmental `ENOSPC`, without assigning its cause to
simultaneous external pressure or treating it as an observed producer-logic
failure.

The 16 commands not invoked were:

1. `probe_independent_replay`;
2. `probe_full_semantic_replay`;
3. `probe_mutations`;
4. `probe_manifest_seal`;
5. `sharpness_krawczyk_producer`;
6. `sharpness_topology_alln_producer`;
7. `sharpness_build`;
8. `sharpness_adversarial`;
9. `global_infrastructure_build`;
10. `global_infrastructure_verify`;
11. `global_infrastructure_mutations`;
12. `clean_room_hardened_adversarial`;
13. `primary_rebind`;
14. `release_inputs`;
15. `integrated_fresh_independent_replay`; and
16. `integrated_classification_mutations`.

## Evidence reconciliation without a prohibited rerun

I did not substitute stored PASS fields for the failed run.  I used the
following independent facts to assess what the external failure leaves open:

1. The current package's fresh 4-command verification had already run the
   integrated 20-child current-code replay and current 27-case classification
   mutation suite to completion, with no drift.  Its children include the full
   probe independent replay and semantic reconstruction of all 574,535 rows;
   that semantic child passed and rejected all seven coherent mutations.
2. The `probes/`, `restoration/`, `anchor_universe/`, `four_port_atlas/`, and
   `sharpness/` directories are byte-for-byte identical between the third- and
   fourth-revision sealed packages.  In particular,
   `probes/regenerate_k3p_probes.py` has SHA-256
   `f5b9f186d5d443158a7fa6a073f5a2fbdf21996f346d6e73e04f01a1f470fd00`
   in both.
3. The prior independent third-revision exact-once run executed all 55 command
   bodies; the probe/restoration/anchor/four-port/sharpness components relevant
   to the present unexecuted tail are byte-identical.  Its probe producer passed in
   2,842.743 seconds, the all-row semantic replay passed in 369.945 seconds,
   and all 55 bodies passed; only the now-repaired final mode-drift gate failed.
   That retained outer log has SHA-256
   `14a78aab5b9e8dc19108fc0def8f2694385b26492472239cbf0e390e597003b3`.
4. Referee-owned current checks independently streamed the full restoration
   and probe census, reconstructed representative semantic rows, and passed all
   seven check families.
5. The supplied fourth folder contains an internally consistent author-run
   record claiming 4/4+55/55 with the current code and a 2,886.752-second probe
   producer.  Because that record lives entirely under excluded `review_runs/`,
   I treat it only as unsealed corroboration, not authenticated evidence.

These points strongly support the theorem and show that the failed producer is
not a newly changed mathematical component.  They do **not** turn this audit's
partial regeneration into a fresh complete PASS.  Computational
reproducibility is therefore recorded as: current verification PASS; current
regeneration incomplete for an external disk-capacity reason; complete
the command bodies in the unexecuted fourth-revision tail are byte-identical to,
and were completely executed in, the immediately preceding independent audit;
newly changed current command bodies had already executed in verification or
commands 1--38; current supplied complete run only corroborative.

## Postfailure state

After the process exited, I preserved the reports, transcripts, and before
inventories.  A fresh package-integrity check again passed all 635 sealed files
and 597 inner members; its log SHA-256 is
`52c9e24c8da98a935fdb6ab8dac44d02090720ce671d66b8bbc2afcaae4b1cf7`.
An independent inventory comparison found zero added, removed, or changed
entries in the 6,635-entry virtual environment.  Only then did I delete the
failed disposable workspace.  The submitted package was never modified.

## Disposition

The external `ENOSPC` event is an **unresolved fresh-regeneration limitation**,
not a package or theorem defect.  Under the user's no-rerun instruction, no
additional long execution is appropriate.  The report's final verdict must
state this limitation explicitly and must not claim a fresh 55/55 fourth-run
PASS.
