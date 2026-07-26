# Independent referee review: order-13 k=3 production workflow

## Verdict

**REJECT**

The frozen revision has strong fail-closed checks, and all six preserved v1
malformed-metadata regression cases are now rejected.  It nevertheless accepts
terminal-success metadata in which the proof concerns bytes other than the
frozen run formula, and it does not bind the retained LRAT bytes to the recorded
checker execution.  Either defect is enough to reject a mathematical
certificate workflow whose read-only audit is intended to establish exact
reproducibility.

No real SAT solver or proof checker was run.  Every child execution in the
referee fixtures was a deterministic in-process stub.

## Frozen review target

The independently observed hashes exactly match author A's freeze declaration:

| File | SHA-256 |
| --- | --- |
| `src/search/order13_k3/production.py` | `38beae789c25228f2411463f004645711821d340c16c6020fe22d2157b7de142` |
| `src/search/order13_k3/normalize_bdrat.py` | `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c` |
| `src/search/order13_k3/PRODUCTION_PROTOCOL.md` | `077b3328da5eab7645bafde079e0334c09b0e696179c9df893a0364a2d053de8` |
| `tests/test_order13_k3_production.py` | `46c8574a7a16a605784a24e8f8351b770e8e06ffd9202cd20b57f21ef5bb414a` |

## Decisive findings

### F1 — The attempt formula is not required to equal the frozen run formula

Severity: **critical**

The run-level formula is correctly checked against the expected template hash
at `production.py:1326-1332`.  The attempt audit, however, only compares
`config["instance"]` with a fresh binding of the current attempt-local file at
`production.py:770-805`.  It never compares that binding's size and SHA-256
with the frozen run-level instance.

Synthetic reproduction:

1. Create an accepted six-phase synthetic success for frozen `hole11`.
2. Replace `attempts/attempt-000001/instance.cnf` with the different local CNF
   `p cnf 1 2; 1 0; -1 0`.
3. Refresh only the attempt configuration, certificate, outcome artifact map,
   and checkpoint relational hashes.
4. Leave the frozen run-level CNF unchanged.
5. Run the read-only audit with the child launcher forbidden.

Observed result:

- frozen run CNF SHA-256:
  `1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901`;
- substituted attempt CNF SHA-256:
  `ac42a371b5a124286c410ed5dfa2e3be7ee7d5b1feac6f08e7e1715f0c3669a8`;
- audit result: `accepted: true`,
  `status: UNSAT_LRAT_VERIFIED_PENDING_HOSTILE_AUDIT`.

Thus a certificate labeled with the frozen template can structurally pass for
a different formula.  Require every attempt instance binding, candidate
instance binding, and certificate instance binding to equal the frozen
run-instance size and SHA-256, in addition to requiring its exact run-local
path.

### F2 — Recorded checker children do not bind their read-only input bytes

Severity: **critical**

`_run_phase` computes read-only bindings before a child and compares them after
the child (`production.py:1603-1636`), but those bindings are discarded.  The
persisted `child-<phase>.json` contains only the `ChildResult`
(`production.py:1637-1640`).  `_verify_child` binds argv, the executable,
stdout/stderr, limits, and resource fields, but no formula/proof input hashes
(`production.py:1500-1553`).

Synthetic reproduction:

1. Create an accepted six-phase synthetic success.
2. After the recorded `lrat_check` child, replace
   `proof.converted.lrat` with the bytes `not an LRAT proof`.
3. Refresh the certificate's current LRAT binding, outcome artifact map, and
   terminal checkpoint binding without changing the checker child record.
4. Run read-only audit with the child launcher forbidden.

Observed result:

- substituted LRAT SHA-256:
  `e88838645bee3060eb28b1cdab1a8bb4b71dbda072a46a86a871e3a8b59b2edb`;
- audit result: `accepted: true`,
  `status: UNSAT_LRAT_VERIFIED_PENDING_HOSTILE_AUDIT`.

The audit correctly says that it does not freshly replay LRAT, so its
cryptographic basis must establish which LRAT bytes the recorded child checked.
Persist exact pre/post read-only bindings in each phase record and require the
certificate's final bindings to equal the appropriate recorded child inputs.
This should cover the formula, raw proof, normalized proof, normalizer source,
and LRAT.

### F3 — Success certificates accept extra and altered claim metadata

Severity: **high**

The success-certificate audit checks selected fields but not an exact key set,
and it does not check the exact `claim_boundary`
(`production.py:1157-1191`).  The success outcome likewise checks only
`details.get("certificate")`, not the exact details shape.

The referee injected
`"asserted_global_order13_exclusion": true` and replaced the certificate
boundary with a false assertion of fresh independent replay and complete
template coverage.  After refreshing ordinary artifact/checkpoint hashes,
read-only audit still returned `accepted: true`.  Its own returned
`proof_freshly_replayed` field remained correctly `false`; the flaw is that it
accepted an embedded certificate that overclaimed.

Require the exact certificate key set, exact claim boundary, and exact success
details object.  The same exact-shape rule should be applied to normalization
reports and other nested claim-bearing records.

### F4 — One durable interruption state cannot be explicitly recovered

Severity: **high**

`run` writes `outcome.json` durably before appending the terminal checkpoint
(`production.py:2216-2228`).  A crash in that window leaves the latest
checkpoint at `RUNNING_UNFINISHED_NONCLAIM` with an outcome present.
`_audit_attempts` rejects exactly that state
(`production.py:810-819`), and `_recover_interrupted` also rejects any present
outcome (`production.py:2093-2097`).  Therefore
`run --recover-interrupted` cannot reach its recovery logic.

The synthetic crash-state fixture produced the stable error
`running attempt unexpectedly has an outcome`.  Recovery should recognize this
write-order window and conservatively seal it as a retryable nonclaim, never
promoting the uncheckpointed outcome.  The analogous pre-`RUN_STARTED`
orphan-attempt window should also have an explicit fail-closed recovery rule.

## Checks that passed

- Checkpoint event/count/path relations reject external paths, orphan counts,
  wrong recovery promotion, and malformed status mappings.
- All six cases preserved under
  `reviews/order13_k3_production_hostile/rejected_v1/` are rejected by the
  frozen revision.  In this review they are neutrally classified as
  **malformed-metadata regression cases**:
  external checkpoint path/count, CaDiCaL policy rebinding, normalizer-Python
  rebinding, retryable claim-label mutation, malformed SAT-candidate metadata,
  and interrupted-recovery status promotion.
- The actual local CaDiCaL, drat-trim, and lrat-check files match the three
  production policy hashes, are distinct executable single-link files, and
  their two source archives match the frozen archive hashes.  The
  human-readable identities and current-interpreter relation are enforced.
  The binaries were read and hashed, never executed.
- A complete SAT assignment is reparsed and checked against the frozen CNF.
  With that stage instrumented solely to reach the next layer, the actual
  direct graph/game validator independently rejected an empty eternal family.
- Six invalid resource-limit cases were rejected.  A failed prelaunch resource
  gate produced `RETRYABLE_NONCLAIM` with zero child calls.
- Explicit interruption recovery refused silent resume, wrote a retryable
  nonclaim with no child, and allowed a fresh attempt numbered 2.
- Binary normalization emitted the exact addition stream, retained the unique
  final empty addition, accepted deletions only under policy, rejected all 10
  malformed streams, and removed partial outputs on failure.
- Runtime-source mutation in an isolated source mirror made audit and run fail
  before any child; restoring the bytes restored acceptance.
- Read-only audit of the unmutated synthetic complete chain made zero child
  calls, changed no durable bytes or modes, and returned
  `proof_freshly_replayed: false` with the explicit structural/cryptographic
  claim boundary.
- Sixteen frozen upstream tests that do not write repository sources passed.
  The one upstream test that temporarily edits implementation sources was
  deliberately excluded by the referee's read-only constraint; its behavior
  was covered against the isolated mirror above.

## Deterministic evidence

Companion artifacts:

| Artifact | SHA-256 |
| --- | --- |
| `referee_regressions.py` | `5681a4672abf882b408de287ef781b72063915d31e6d068cef143face119e1f8` |
| `run_readonly_upstream_tests.py` | `713ec705aa77aa7f316ef7357473d7466fd00fdd82f84aff799fbc97f882b022` |
| `evidence.json` | `3d849ca9493dba7786a899ce9a0cf7c35101b7f342d531103cbc65c510db29fe` |

The evidence generator was run twice after its final edit and produced the
same `evidence.json` hash.

## Exact replay commands

Run from the campaign root:

```sh
cd /Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination

shasum -a 256 \
  src/search/order13_k3/production.py \
  src/search/order13_k3/normalize_bdrat.py \
  src/search/order13_k3/PRODUCTION_PROTOCOL.md \
  tests/test_order13_k3_production.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 reviews/order13_k3_production_referee/referee_regressions.py \
  --output reviews/order13_k3_production_referee/evidence.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 reviews/order13_k3_production_referee/run_readonly_upstream_tests.py

shasum -a 256 \
  reviews/order13_k3_production_referee/referee_regressions.py \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests.py \
  reviews/order13_k3_production_referee/evidence.json
```

Acceptance requires repairing F1 and F2 and adding direct regressions for both.
F3 and F4 should also be repaired before a production run is treated as
restartable, claim-safe certificate infrastructure.
