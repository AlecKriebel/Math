# Reproducibility adversary: PR 436 / KOU-21.60 / 2569

The frozen computation package reproduces correctly in ordinary Python. It has a material verification robustness defect under Python optimization: every essential `assert` check disappears, but success labels and claimed check counts remain. This finding does not falsify the proposed mathematical counterexample. It does mean that optimized execution is not a successful verification, even when its output is byte-identical to the historical output.

The independent criterion was sealed at 2026-10-12T21:47:47.875395+00:00 before reading historical audit conclusions. The criterion SHA-256 is `a4f1e3a791f9d5c50f3227e4225d16d002ee21ecd33b36f3a58c69040a13efd6`. This review adds zero substantive proof-search turns. It concerns exactly the frozen claimed-solved PR 436 head `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2`.

## Actual source integrity

All 26 files in the root source receipt match recomputed byte lengths and SHA-256 hashes. The historical `MANIFEST.json` matches all 25 of its entries, and those entries plus the manifest itself are exactly the extant 26-file payload. There are no extra files in the payload. The historical manifest excludes itself; its own bytes are externally bound by the root receipt. No circular or impossible self-hash claim is needed.

The current root receipt SHA-256, every computed source hash, and the complete source inventory are in `INTEGRITY_RESULTS.json` and `SOURCE_HASHES.json`. The proof hash is independently recomputed as `3ceab2f387baa3d61c15805cdde7d8154c8350e2b3b4bf2ce187ec53b99ec299`. The initial and final full source hash maps agree after all executions and faults.

The historical portability report refers to an earlier private `PUBLICATION_FROZEN.local.json`, an original extracted source table, and an original pre-portability verifier. Those artifacts are not in this frozen payload. Therefore the historical claim of byte equality with the earlier private implementation is historical testimony here; this review does not pretend to reverify absent artifacts. The complete current portable package is independently executable without them.

## Replay and dependency evidence

All four original entry points were read in full and copied without byte changes into separate private fixture directories. Each was executed normally and with `-O`, giving eight full original-script runs. All eight exited zero, produced JSON byte-identical to the corresponding historical file, and printed stdout byte-identical to the generated JSON. These are eight successful reproduction runs, but only four are accepted ordinary-mode verifications; the four optimized runs removed their assertion checks.

| Entry point | Dependencies | Ordinary assertions in source | Ordinary replay | Optimized replay |
|---|---|---:|---|---|
| `verify_counterexample.py` | Python standard library | 15 | Output byte match | Output byte match; checks removed |
| `verify_controls.py` | Python standard library | 2 | Output byte match | Output byte match; checks removed |
| `contributor_checks/check_character_data.py` | SymPy | 18 | Output byte match | Output byte match; checks removed |
| `independent_audit/independent_audit.py` | SymPy, mathematical coefficient JSON, proof text for hash | 47 | Output byte match | Output byte match; checks removed |

The actual replay interpreter was Python 3.12.14 with SymPy 1.14.0 and mpmath 1.3.0, matching the reported historical Python/SymPy versions. Neither the default Python nor the unmodified bundled Python had SymPy, so a private virtual environment installed the pinned dependency. The dependency-install record is preserved privately. The README states the SymPy dependency accurately, but does not pin versions or discuss optimized mode.

Every executable reads/writes via its script-relative path. The independent verifier reads only the supplied `a5_idempotents.json` and `COUNTEREXAMPLE.md`; its mathematical computation does not parse a private PDF or extracted text. No executable contains embedded workspace/private absolute-path literals. There is no pseudorandom generator, sampling seed, or floating-point approximation in the author arithmetic or independent rational/finite-field arithmetic. SymPy expressions are symbolic and exact. Some iteration orders depend on sets, but the recorded aggregate/sorted outputs agreed in all actual runs. This review does not claim a cross-platform or all-version reproducibility theorem.

No script was run in the sealed source directory. All outputs and fault mutations stayed in private copies. Original script bytes, Git branch/index/state, remotes, queue/status data, and public services were not changed by this review.

## Five real negative controls

These are five distinct mechanisms, run once normally and once optimized: ten fault executions. They are not repetitions presented as extra coverage. The five ordinary executions all failed at an assertion; all five optimized executions accepted the fault.

| Fault introduced only in a private fixture/runtime | Ordinary outcome | Optimized outcome |
|---|---|---|
| Replace the author's augmentation matrix-rank function by a function returning zero | Rejects the span-dimension assertion | Returns span dimension 0 while still reporting absolute irreducibility `true` |
| Replace the controls' modular-rank function by a function returning zero | Rejects `rank = p−1` | Returns rank 0 for all five regular cyclic modules |
| Change the contributor's identity class size from 1 to 2 before its weight matrix is made | Rejects ordinary orthogonality | Emits a `PASS` label with class sizes totaling 121 for a claimed order-120 group |
| Add 1 to the first rational idempotent's identity coefficient in the independent input | Rejects rational idempotency | Emits `all_checks_passed: true`, with first reduced ideal rank 48 instead of 12 |
| Append a private marker to the proof bytes | Rejects the frozen-proof SHA-256 assertion | Emits `all_checks_passed: true` despite the changed proof hash |

Runtime monkeypatch/trace injection leaves original code bytes intact; the other two faults alter input copies only. Detailed timestamps, status, stdout/stderr hashes, and the actual incorrect fields are in `EXECUTION_RESULTS.json`. Exact raw stdout, stderr, generated JSON, executed wrappers and mutated inputs are retained in `private_sources/reproduction_adversary`. Raw failures are not discarded or normalized into passes.

There are 82 source `assert` statements across the four original scripts. Bytecode inspection with the replay interpreter confirms that optimized compilation emits no assertion-load opcodes. The ordinary compiler emits 84 assertion-load opcodes because two chained assertions have two failure branches; this is not 84 source checks or an execution count. An initial opcode probe on Python 3.14 used the older opcode name and incorrectly returned zero; the raw probe is preserved privately and the recorded result explicitly documents its correction. The negative controls, rather than a bytecode count alone, establish the practical defect.

In particular, the optimized author's `closure_products_checked: 14400` and independent verifier's `all_homomorphism_products_checked: 14400` remain hardcoded even though their assertion-based comparison expressions are not executed. They must not be cited as optimized verification evidence.

## Computation/proof boundary and historical controls

The ordinary runs substantiate the finite data actually checked: the quaternion group/product/isomorphism constructions, exact character orthogonality and Frobenius–Schur sums, finite-field matrix spans, rational idempotency, finite modular left-ideal ranks, positive witness equations, and code/output consistency. The full ordinary independent run reports the nonsplit underlying natural-module span dimension 8, augmentation span dimension 16, all three projective dimensions 24/32/8, and central nilpotent ranks 12/16/4. These are consistent with the frozen proof and do not omit the nonsplit `U` type.

The main author verifier assumes the quotient modular composition/reduction data in its monoid calculation; that calculation verifies three coefficient equations, not their source theorem. The contributor computes decomposition data from supplied character/Brauer rows, whose status as actual representations and exhaustive simples needs mathematical justification. The independent verifier adds actual finite constructions and idempotent arithmetic, but generic facts about simple-module exhaustion, projective covers, Frobenius–Schur parity, projective-lattice character vanishing, and semiperfectness still require proofs. No finite replay alone proves the unrestricted implication from semiperfectness or the general central-square-zero lemma. Those general steps are the theory reviewers' scope.

The contributor output's global Schur index 2 and local Schur index 1 are partly theorem/source interpretation: the code checks two odd-unit Hilbert-symbol values and prints the index values. The core candidate uses the real quaternionic parity obstruction, so the numerical output must not be represented as a self-contained verification of a global/local classification.

The historical control script has exactly five Jordan/coinvariant examples at primes 2,3,5,7,11 and twelve parity rows for odd primes 3,5,7,11 and exponents 1,2,3. The first computes ranks. The second verifies oddness of the cyclic group order and records a claimed representation-theoretic exclusion; it does not independently prove the uniform rational-module parity theorem. The `C_2` Ext assertion and its warning that `C_2` is not itself a semiperfectness counterexample occur in the written attempts/reviews; they are not additional automated Ext computations. These scopes are correctly distinguished in the frozen mathematical text.

## Focused repair and exact remaining gap

The suggested verification-only repair is to reject optimized Python explicitly before running any checker, or replace essential assertions by explicit runtime checks. An early guard is the smaller change and does not alter the mathematics. Success fields should mean that checks really executed. The proposed guard and its required negative test are in `PROPOSED_VERIFICATION_REPAIR.md`.

Required mathematical repair identified by this code audit: none. Required verification robustness repair for a mode-independent success claim: optimized mode must fail closed. The ordinary published command reproduces the frozen evidence correctly. The main mathematical acceptance decision remains with the separate theory and representation families, and historical priority has not been audited here.

Completion estimate: 100% of the assigned reproducibility/integrity/code audit. This percentage does not mean the original package's optimization defect is repaired or the mathematical result has been accepted.
