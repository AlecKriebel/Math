# Adversarial H21 Audit Work Log

Scope: independent adversarial audit of the historical H21-01 failure, the corrected clean-room verifier, all fourteen locked relation orbits, and the two pre-lock sink swaps. All writes for this subtask are confined to `clean_room/adversarial/`. Parent clean-room files and root logs/manifests are read-only for this audit.

## 2026-08-24 21:53 PDT — Baseline replay and first adversarial finding

- Re-ran the untouched historical-failure wrapper and obtained the exact expected `H21-01` source-automorphism assertion followed by `HISTORICAL_H21_01_FAILURE_REPRODUCED_EXACTLY` (exit 0).
- Re-ran the corrected verifier and regression under ordinary Python 3.14.6. Both reached their documented terminal sentinels (exit 0).
- Confirmed the preserved historical verifier and frozen input are byte-identical at SHA-256 `ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91`.
- Adversarially ran the corrected module with Python optimization enabled and passed it a deliberately truncated three-member `H21-01` raw orbit. Because all certification predicates are Python `assert` statements, the invalid record was accepted and `reconstruct_record` returned the true four-member coset without rejecting the claimed three-member list.
- Strongest verified result: the mathematical replay passes in the documented ordinary runtime, but the verifier is not fail-closed under `python -O` / `PYTHONOPTIMIZE`.
- Exact gap: independently recompute the mixed automorphism groups, conjugations, double cosets, and Fourier transports; determine whether any mathematical counterexample exists in addition to the optimized-mode certification weakness.
- Completion estimate: **35%**.

## 2026-08-24 21:59 PDT — Independent topology and transport reconstruction

- Implemented a materially independent graph engine in `adversarial_h21_audit.py` using NetworkX 3.5 on a colored incidence expansion. Endpoint arrowheads, explicit vertex roles, and physical port labels are separately represented.
- Independently reconstructed the fixed one-root suppression and validated binary mixed incidences on every audited source/base target/displayed target.
- Recovered the H21-01 groups:

  ```text
  rooted DAG:            { id }
  root-suppressed mixed: { id, (0 2) }
  ```

- Recovered the nontrivial vertex map `S <-> sub4`, `incoming <-> segment-4 leaf`, fixing everything else and preserving the two heads at each of `V` and `X`.
- Independently reconstructed all seven H21 double cosets. The six frozen H21 orbit sets are exact, and the omitted class is precisely the two-member isomorphic group.
- Used H21-03 and H21-04 non-involutive representatives to discriminate `p a p^-1` from the wrong `p^-1 a p`; direct displayed-target groups select the corrected formula in both cases.
- Evaluated the physical switching map with exact fractions for all 24 port permutations and all 64 K3P coordinates at a strict rational physical point. Every transport matched both the independent coordinate rule and the corrected symbolic physical-edge expression.
- Strongest result: no mathematical defect was found in root suppression, arrowhead incidence, labels, automorphism groups, conjugation, double cosets, raw coverage, or Fourier transport.
- Exact gap: finish the mutation campaign and audit whether the all-fourteen rank/polynomial claims are genuinely reconstructed rather than trusted.
- Completion estimate: **75%**.

## 2026-08-24 22:02 PDT — All-fourteen and rank-gate adversarial audit

- Independently checked all fourteen source/displayed-target mixed nonisomorphisms, 42 source/base/displayed groups, all 38 raw-member assignments, and all 38 witness equations.
- Replayed the corrected certificate routine and confirmed the disjoint coverage accounting `5 H14 quartics + 4 remaining quartics + 5 rank records = 14` and two distinct pre-lock sink swaps.
- Found a second high-priority certification defect: the corrected rank routine verifies nonzero source/target minors but accepts `target_dimension_upper_bound` directly from JSON. It does not replay the referenced target factorization.
- Confirmed a normal-mode mutation is accepted: the H21-02 certificate can claim ranks `101 > 100 = 100` while retaining only its original `11x11` and `10x10` minors. This proves rank labels are not bound to minor sizes and the upper bound is not reconstructed.
- Ran the separate standard-library `reproducibility/exact_four_port.py` (SHA-256 `f85c1a77ee88ab265b5a6d0adab80c45ff5642c3c1258aa991d7b94a1c3c5816`). Its independent ten-/twelve-generator factorizations pass all five inequalities `11>10`, `14>12`, `11>10`, `11>10`, `14>12`. Thus the clean-room coverage gap did not expose an underlying rank counterexample.
- Also found low-severity binding gaps: inconsistent redundant `port_permutation` and `target_incoming_role` fields are accepted while the bound graph/representative remain unchanged.
- Strongest result: the H21 repair is mathematically sound, but the corrected file's unconditional full-certificate `PASS` claim is overstated.
- Exact gap: package the evidence, validate hashes/JSON, and rerun from clean state.
- Completion estimate: **93%**.

## 2026-08-24 22:04 PDT — Final adversarial package

- Added:
  - `adversarial_h21_audit.py`;
  - `optimized_bypass_probe.py`;
  - `ADVERSARIAL_H21_AUDIT.md`;
  - `ADVERSARIAL_H21_AUDIT.json`; and
  - this log.
- Mutation results under ordinary Python:
  - missing H21 raw member: rejected;
  - false source symmetry: rejected;
  - wrong target frame: rejected;
  - wrong representative: rejected;
  - wrong witness equation: rejected;
  - identity coordinate map: rejected;
  - inconsistent redundant port/incoming metadata: accepted;
  - fictitious `101>100` rank metadata: accepted.
- Optimized-mode probe deterministically prints:

  ```text
  OPTIMIZED_ASSERT_BYPASS_CONFIRMED claimed=3 reconstructed=4
  ```

- Final audit status: **qualified PASS for H21 mathematics; certification repairs required for fail-closed/full-fourteen clean-room claims**.
- Residual mathematical H21 gap: **none found**.
- Residual certification gaps: explicit optimized-mode refusal; exact target rank upper-bound replay and rank/minor-size binding; redundant metadata and immutable-input binding improvements.
- Completion estimate: **100%** for the assigned adversarial audit.

## 2026-08-24 22:43 PDT — Hardened-gate re-audit opened

- Parent requested a fresh audit of hardened verifier SHA-256 `becacec117734248047cded6f84d5996ad91c7531be36b1d8db8eec57653740b` and regression SHA-256 `aa3a97442854d7df8b6d4b3bfa02e9f2d18d4eaa4a0838fdd33738e00ea6a063`.
- Ordinary full gate and regression both passed, now including the sentinel `PASS five independently reconstructed directed-rank upper bounds`.
- Both the direct `python -O` gate command and the historical optimized bypass probe abort during module import with the explicit optimized-Python refusal.
- Initial code inspection confirms:
  - active hashes for all five lock/certificate files are embedded and checked before parsing;
  - `require` raises a non-optimizable `CertificationError`;
  - `port_permutation`, incoming roles, and repair indices are explicitly bound;
  - all raw-member Fourier transports are replayed;
  - claimed rank equals both minor dimensions; and
  - H21 and sunlet target upper bounds are reconstructed before the strict inequality is accepted.
- New adversarial control finding: `verify_all(run_certificates=False)` skips the certificate/rank layer but still emits the exact full terminal PASS sentinel. The parent was notified immediately.
- Strongest result: both previously reported vulnerabilities appear closed, but the public skip-control must be repaired or clearly made noncertifying before an unconditional final verdict.
- Exact gap: complete mutation tests and audit the upper-bound dependency counts for circularity/undercounting.
- Completion estimate: **45%** of the hardened-gate re-audit.

## 2026-08-24 22:48 PDT — Skip-control blocker repaired

- Located the intermediate blocker at `verify_h21_transport_and_fourteen_orbits.py:1680`: `verify_all(run_certificates=False)` bypassed lines 1720--1724 but the old line 1725 unconditionally emitted the full sentinel.
- Recommended either removing the argument or requiring it to be exactly `True` before work. Parent applied the exact fail-closed requirement without asking this subtask to edit parent files.
- Final hardened verifier SHA-256 became `bf69fce87b26376597efa1be221fe7b8ddc303b4054c6ee22fa861e781d2051a`.
- Re-test: `run_certificates=False` now raises `CertificationError` before any PASS output and cannot emit the full terminal sentinel.
- Strongest result: the only new blocker found during re-audit was repaired and independently closed.
- Exact gap: finish target-factorization noncircularity and full mutation campaign against the final hash.
- Completion estimate: **70%**.

## 2026-08-24 22:53 PDT — Final hardened mutation and circularity audit

- Added `hardened_cleanroom_reaudit.py`, a deterministic adversarial driver bound to the final verifier.
- Final campaign results:

  ```text
  25 / 25 ordinary mutations rejected
   3 /  3 optimized-mode controls rejected
   5 /  5 active JSON one-byte mutations rejected before parse
   5 /  5 target rank upper bounds independently reconstructed
  52 / 52 raw-plus-representative Fourier calls reached
  ```

- Confirmed `python -O`, `PYTHONOPTIMIZE=1`, and the old optimized-bypass probe all fail during verifier import and emit no PASS/bypass sentinel.
- Confirmed explicit binding/rejection for port permutation, source/target incoming roles, source/target repair tags, raw omission/duplication, witness omission/frame confusion, and a wrong coordinate action.
- Confirmed the prior `101>100=100` rank mutation, mismatched minor dimensions, changed upper-bound integer, altered generator/saturation metadata, wrong map direction, and malformed sunlet mechanisms all fail.
- Noncircularity audit poisoned both rank dictionaries and the stated upper-bound integer before running target factorization alone:
  - H21 still produced ten rational generators and eleven exact identities on a nonempty saturation open set;
  - sunlet cases still produced counts `12,10,10,12`;
  - an independent composite-variable occurrence implementation reproduced every sunlet count; and
  - independent `reproducibility/exact_four_port.py` agreed on all five strict inequalities.
- Historical rooted-DAG failure remained exactly replayable.
- Added final reports `HARDENED_H21_REAUDIT.md` and `HARDENED_H21_REAUDIT.json`.
- Final status: **PASS — zero remaining hardening gaps in the assigned H21/fourteen-orbit scope**.
- Completion estimate: **100%**.

## 2026-08-24 22:57 PDT — Release-candidate replay

- Re-ran the final patched release gate end to end, including the historical-failure replay, fourteen-orbit verifier, H21 regression, ten hardened mutations, two gate controls, and optimized-mode refusal.
- The release gate exited 0 at `CLEAN_ROOM_FULL_GATE_PASS`; its mutation suite reported `rejected=10 controls=2`.
- Re-ran the independent adversarial driver against verifier SHA-256 `bf69fce87b26376597efa1be221fe7b8ddc303b4054c6ee22fa861e781d2051a`.
- The driver again rejected all 25 adversarial mutations, all three optimized-mode controls, and all five active-input byte mutations, then exited 0 at `HARDENED_CLEANROOM_ADVERSARIAL_REAUDIT_PASS`.
- Validated `HARDENED_H21_REAUDIT.json` with the standard-library JSON parser.
- Final status remains **PASS — zero remaining hardening gaps in the assigned scope**.
- Completion estimate: **100%**.
