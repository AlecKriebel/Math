# H21-01 Clean-Room Work Log

Scope: H21-01 graph/transport failure, corrected independent verifier, regression, and full 14-orbit plus two-sink-swap replay. All writes are confined to `clean_room`; immutable inputs are read from `input_frozen/k3p_cloud_artifacts`. Root research logs, manifests, reproducibility, and sharpness files were not edited. No commit or push was performed by this subtask.

## 2026-08-24 21:31:41 PDT — Historical verifier preserved

- Copied the frozen clean-room verifier byte-for-byte using the patch workflow as `HISTORICAL_cleanroom_verify_fourteen_orbits.py`.
- Verified:

  ```text
  shasum -a 256 clean_room/HISTORICAL_cleanroom_verify_fourteen_orbits.py input_frozen/k3p_cloud_artifacts/cleanroom_verify_fourteen_orbits.py
  ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91  (both files)
  cmp exit 0
  ```

- Strongest result: the historical code is preserved exactly; no proposed repair has contaminated the evidence of failure.
- Exact gap: reconstruct the intended graph category and test whether the frozen transport witnesses are correct there.
- Completion estimate: **35%**.

## 2026-08-24 21:38:32 PDT — Independent reconstruction and corrected verifier

- Reconstructed, without importing the primary atlas:
  - the ordered cycle/four-theta core census needed by the frozen indices;
  - all six source supports;
  - all 831 selected-incoming and 1,983 dummy-incoming four-port target completions;
  - H21-01 source `S1` and base target `T80`;
  - rooted literal serialization and hashes;
  - root-suppressed mixed graphs with endpoint arrowheads;
  - exact mixed automorphism groups by standard-library backtracking;
  - permutation composition, conjugation, double cosets, and raw witness equations;
  - all physical-edge K3P switching expressions and 64-coordinate transports;
  - canonical K3P descriptors, exact polynomial pullbacks, exact evaluations, Jacobians, and determinants.
- First full run exposed a non-H21 census-frame nuance at `L23-01`: the lower-to-rank24 frozen family fixes its canonical source presentation and quotients only by the target group. The code was corrected to represent that explicit family frame while still computing the full geometric source group. No certificate or membership check was dropped.
- Command:

  ```text
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/verify_h21_transport_and_fourteen_orbits.py
  ```

- Result after the census-frame correction:

  ```text
  PASS H21-01 ... H21-06 graph/map binding, mixed groups, double coset, Fourier transport
  PASS L20-01 ... L23-02 graph/map binding, mixed groups, double coset, Fourier transport
  PASS two sink-swap and fourteen exact separation certificate replays
  CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS
  exit 0
  ```

- Strongest result: representatives, map hashes, all frozen raw memberships, Fourier transports, quartics, and rank minors pass an independent full replay.
- Exact gap: turn the semantic distinction between rooted and semi-directed automorphisms, and the base/displayed target frames, into a fail-closed regression.
- Completion estimate: **85%**.

## 2026-08-24 21:38:57 PDT — Regression locked

- Added `test_h21_transport_regression.py`.
- The test positively requires all of the following:
  - rooted directed isomorphism rejects the H21-01 `(0 2)` swap;
  - root-suppressed mixed isomorphism accepts it;
  - the target base group contains `(0 2)`;
  - the displayed target group contains its conjugate `(0 3)` and not `(0 2)`;
  - the four-member double coset equals the frozen raw membership;
  - all 64 physical-edge Fourier formulas transport exactly;
  - the complete 14-orbit and two-sink-swap certificate replay still passes.
- Command/result:

  ```text
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/test_h21_transport_regression.py
  CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS
  H21_01_TRANSPORT_REGRESSION_PASS
  exit 0
  ```

- Strongest result: the repair cannot regress to either historical category/frame error without failing.
- Exact gap: package an exact replay of the untouched failure and publish the audit records.
- Completion estimate: **93%**.

## 2026-08-24 21:39:40 PDT — Historical failure replay made deterministic

- Added `replay_historical_failure.py`. It verifies the preserved and frozen SHA-256 values, adapts only flattened read paths, executes the preserved bytes, and demands the exact original exception payload.
- Command/result:

  ```text
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python clean_room/replay_historical_failure.py
  AssertionError: ('source automorphism', 'H21-01', {'permutation': [2, 1, 3, 0], 'source_automorphism': [2, 1, 0, 3], 'target_automorphism': [0, 1, 2, 3]})
  HISTORICAL_H21_01_FAILURE_REPRODUCED_EXACTLY
  exit 0
  ```

- Strongest result: the original failure and the corrected pass are both deterministic and coexist without alteration of historical code.
- Exact gap: final machine-readable and narrative audit, hash validation, and clean rerun.
- Completion estimate: **97%**.

## 2026-08-24 21:42:33 PDT — Audit checkpoint

- Added:
  - `H21_01_TRANSPORT_AUDIT.json` with schema `k3p-h21-01-transport-audit-v1`;
  - `H21_01_TRANSPORT_AUDIT.md` with the complete diagnosis and replay instructions;
  - this work log.
- Validated the JSON with the standard-library parser and confirmed its 64-entry transport vector and empty `exact_remaining_gaps` list.
- Diagnosis recorded:
  - representative mismatch: **false**;
  - primary transport defect: **false**;
  - historical clean-room logic defect: **true**;
  - exact remaining H21-01 audit gaps: **none**.
- Completion estimate: **100%** for the assigned H21-01 transport audit and full clean-room replay.

## 2026-08-24 22:39:08 PDT — Adversarial hardening checkpoint

- Reopened the prior unconditional clean-room `PASS` after the independent
  adversarial audit found two certification defects:
  - optimized Python erased every load-bearing `assert`;
  - the five target rank upper bounds were accepted as JSON integers rather
    than reconstructed in this verifier.
- Replaced every load-bearing `assert` in the corrected verifier with explicit
  `CertificationError` gates and added an immediate optimized-mode refusal.
  An AST control confirms zero `Assert` nodes remain.
- Bound the five active frozen inputs to fixed SHA-256 values before parsing.
- Reconstructed and bound `port_permutation`, `source_incoming_role`, and
  `target_incoming_role` from the presentations.
- Extended Fourier transport replay from fourteen representatives to all 38
  raw orbit members.
- Reconstructed the five directed-rank target upper bounds without importing
  the primary verifier:
  - `H21-02`: eleven exact coordinate identities through ten rational
    generators on the declared saturation open set;
  - `L20-02` and `L23-01`: exact ordinary-sunlet compression to twelve
    generators;
  - `L21a-02` and `L21b-02`: exact selected sunlet compression to ten
    generators, with `A_G,B_G` absent.
- Bound every claimed rank to a square minor of the same size, the selected
  observable set, exact coordinate labels, parameter-column range, strict
  physical point, and exact determinant.
- Added `test_clean_room_mutations.py` and a deterministic result ledger. All
  nine mutations were rejected; two positive controls passed. The former
  `101 > 100 = 100` bypass, nonsquare-minor bypass, metadata bypasses,
  optimized-mode bypass, and active-input hash mutation are all killed.
- Added mandatory runner `verify_clean_room.sh`. Observed full-run checkpoint:

  ```text
  historical replay                 0.09 s
  corrected full replay             1.73 s
  transport regression              1.80 s
  mutation suite                    2.73 s
  mandatory runner total            6.78 s
  peak RSS                     95,846,400 bytes
  CLEAN_ROOM_FULL_GATE_PASS
  ```

- Historical verifier remains byte-for-byte unchanged at SHA-256
  `ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91`.
- Strongest result: the H21 transport and all fourteen four-port separation
  certificates now pass a fail-closed, hash-bound, exact clean-room gate that
  independently proves all five target rank upper bounds.
- Exact gap within assigned scope: **none**. This checkpoint makes no claim
  about the separate cut-recovery, probe/gluing, manuscript, or release gates.
- Completion estimate: **100%** for the hardened H21/fourteen-orbit clean-room
  certification goal.
