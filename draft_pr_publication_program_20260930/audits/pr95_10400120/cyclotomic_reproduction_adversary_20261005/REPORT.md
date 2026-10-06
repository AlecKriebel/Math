# PR95 cyclotomic reproduction and implementation adversary

Closed UTC: 2026-10-05T20:43:23.022832+00:00. Audited incoming head `6534ad01e519c719628a18984b108e73cf2e8ead`, problem10400120 / AMR-103-0120. Original author effort remains **2/5**. **Zero new central proof-search turns.** All work is within this audit folder. No source, branch, Git index, PR, publication, spreadsheet, or UI mutation; no outside contact. This audit grants no priority or publication authority.

## Verdict

**The exact arithmetic claims are independently verified, conditional on the stated ordinary SU(5) modular and surgery inputs. The original executable certificates have a real, repairable optimized-execution defect.** Both original programs reproduce their preserved outputs exactly in ordinary Python. Both also print a success claim on a deliberately false target when run with `-O`, because their decisive `assert` statements disappear. Positive private repairs change only those assertions into explicit guards and add the guard function. They reproduce both correct outputs ordinarily and with `-O`; false target and invalid divisibility controls fail with explicit errors in both modes.

No arithmetic counterexample to the two claimed values was found. The strongest verified result is an independent computation of all seven finite certificate vectors, exact nonvanishing of the vacuum denominator, exact positive-embedding selection and exact cross-product derivations of

    |tau(L(5,1))|² = 3475 + 1550 sqrt(5),
    |tau(L(5,2))|² = 4025 + 1800 sqrt(5).

Their positive difference is `550+250 sqrt(5)`. The quantum-group construction and general surgery theorems are imported mathematical inputs, rather than independently rebuilt by this arithmetic audit. Source applicability/priority/publication gates belong to the parent review.

## Independence and read order

[INDEPENDENT_OBLIGATIONS.md](INDEPENDENT_OBLIGATIONS.md) was written before reading the submitted proof, verifier or prior review. It independently derived the 126-label count, integer-coordinate scaling, primitive-root exponents, field and nonvanishing obligations, surgery-word obligations and hostile-execution controls. The entire submitted `COUNTEREXAMPLE.md`, `verify.py` and `independent_checks.py` were then read. [INDEPENDENT_JUDGMENT_BEFORE_PRIOR_REVIEW.md](INDEPENDENT_JUDGMENT_BEFORE_PRIOR_REVIEW.md) was recorded after new checks and before opening the old `REVIEW.md`. [READ_ORDER.json](READ_ORDER.json) preserves UTC events and file hashes.

The prior review agrees with the mathematical calculation and the S3 normalization. Its statement that no mandatory correction was identified misses the optimized-execution defect demonstrated here. The prior review correctly writes the unsquared sine-product identity; the original checker has a minor misleading squared-product comment discussed below. Novelty remains unestablished.

## Authentication and native runtime

All17 incoming files were copied byte-for-byte into `private_original/`. Before any runs, each was checked against the authenticated head manifest for SHA256, Git blob SHA1 and byte length. They were checked again at closure. The protected incoming paths and private original files remain unchanged. The source-authentication manifest, PR metadata, selected queue row and process journal are copied into `preserved_authentication_receipts/`; their historical process claims have not been upgraded to newly observed execution. [COPY_BYTE_EQUALITY.json](COPY_BYTE_EQUALITY.json) and [FINAL_ORIGINAL_BYTE_EQUALITY.json](FINAL_ORIGINAL_BYTE_EQUALITY.json) contain the checks.

Controlled runs use `/usr/bin/python3 -E -B`, with `-O` added only for optimized controls. The actual native runtime is Python3.9.6, SymPy1.14.0 and NumPy1.24.3. Both libraries are natively available in the user-site environment. There was no `PYTHONPATH` injection, downloaded runtime, package installation or fabricated receipt. The executable resolves to the Xcode Python installation; [runs/runtime/stdout.txt](runs/runtime/stdout.txt) records exact origins and flags.

Every controlled child has actual argv, PID, cwd, UTC start/end, exit code, source hashes, full stdout and full stderr in `runs/<label>/`. The receipt runner itself always completes after recording the child, including a child exit1; the mathematical process exit is the `exit_code` in its receipt. Later clean-run receipts also record pre/post JSON artifacts, mtimes and hashes, so an old retained success JSON cannot be treated as a fresh result. Initial filesystem exploration is described as exploration, not retroactively assigned invented process receipts.

## Exact mathematical controls

The fresh [independent_controls.py](independent_controls.py) imports neither submitted verifier. It performs **134,012 exact explicit checks plus three floating aggregate diagnostics** (134,015 checks total). The repeated check count measures guard evaluations, not distinct mathematical theorems. [runs/independent_controls_v3/stdout.txt](runs/independent_controls_v3/stdout.txt) and the optimized replay preserve the complete results.

* **Index set and scaling.** A different enumeration chooses four distinct elements of `{1,...,9}`, sorts them descending and appends0. Consecutive gaps minus1 yield exactly the same 126 Dynkin labels as the submitted product filter, with a unique vacuum. Stars-and-bars gives `C(9,4)=126`. Coordinates `Y=5r-sum(r)` have sum0 and a common residue mod5. `Y·Z` is divisible by5. The Weyl phase is `zeta100^(-2(Y·wZ)/5)`, and the relative T exponent is `(||Y||²-250)/5`. Every valid-label T division is checked exactly. All120 Weyl permutations are distinct, with sixty of each sign; inversion signs agree with cycle-parity signs.
* **Independent determinant mechanism.** All15,876 matrix entries are calculated separately by a subset determinant recurrence, without enumerating120 Weyl terms and without filling a symmetric half by assignment. The five-by-five entries use `zeta500^(-2 Yi Zj)`. Calculation in the cyclic group algebra `Z[C500]` preserves exact integer coefficients; each final determinant exponent is proved divisible by5 before conversion to `zeta100`. This avoids any floor division in the determinant algorithm. Full exact symmetry is checked afterwards. Eight representative entries are also compared to direct120-term Weyl sums; row swaps, five-row reversal and negation/conjugation are checked independently.
* **Field and operations.** Native SymPy independently generates the irreducible `Phi100=X40-X30+X20-X10+1`, degree40 and every monomial remainder. The new ring multiplication is checked against SymPy polynomial remainders; conjugation is an involutive homomorphism. `X100=1`, `X50=-1` and radical relations are exact. A separate [submitted_ring_oracle.py](submitted_ring_oracle.py) extracts only the original arithmetic functions and checks500 cases against SymPy: all100 monomials plus50 randomized high-degree reductions, products, conjugations and five signed/large cyclic shifts each. This is finite adversarial evidence for implementation correctness; it accompanies the algebraic reduction argument rather than replacing it.
* **Complete finite certificate.** The new determinant computation gives exactly the incoming `D00`, `A`, `B`, `DD`, `AA`, `BB` and cross-multiplied difference. The final vectors match the preserved incoming JSON, coefficient-for-coefficient. Thus the result does not rely on the incoming expected constants alone.
* **Denominators and equality.** SymPy extended Euclid verifies the exact inverse

      D00^(-1) = (2 X30 - 2 X20 - 3)/5.

  Hence division by `D00` and its squared modulus is justified. Two exact cross products separately verify the denominator powers50000 and50000² and the claimed radical expressions. The numerator squared norms and their difference are nonzero. Removing one S normalization factor would fail these checks.
* **Positive real embedding.** `u=X20-X30=2 cos(2pi/5)` is positive in the specified primitive-root embedding because `0<2pi/5<pi/2`. Its relation `u²+u=1` therefore selects `u=(sqrt5-1)/2`, with the positive square root. The exact rational isolating interval `2236/1000 < sqrt5 < 2237/1000` follows by squaring its endpoints. It implies `0<u<5/8`, a positive `125-200u` denominator, positive numerators and strictly positive `550+250sqrt5`. Floating root evaluation is unnecessary.
* **Surgery words and small theory.** Exact integer matrices give `ST5S=[[-1,0],[5,-1]]`, `ST3ST2S=[[-2,1],[5,-3]]` and the reversed chain `[[-3,1],[5,-2]]`. The chain linking matrix `[[3,1],[1,2]]` has determinant5 and inverse(0,0)=2/5. The sign/convention of the lower-left entry and continued fraction are explicit; the order-reversed q=3 is inverse to q=2 modulo5. Exact SU(2) level1 controls use `S=Hadamard/sqrt2`, relative `T=diag(1,i)`, physical vacuum phase `exp(-i pi/12)`, and `(STphys)³=I`; p=1,...,8 surgery Gauss sums equal `(1+i^p)/sqrt2`.

The copied old independent checker is a materially distinct root-lattice mechanism in `Q(zeta10)`: 625 root-lattice residues,120 Weyl elements and five survivors. Its actual positive stdout reports **2,005**, exactly as the preserved incoming JSON, and is byte-identical. Our fresh determinant method does not assume that root-lattice formula. Replaying the checker verifies its computation, conditional on its imported Hansen–Takata theorem.

## Floating diagnostics and their limits

A separate complex construction uses direct five-by-five NumPy determinants for all126² entries, then tests full126-state modular relations. These are diagnostic controls, not exact proofs. All computed entries are checked finite. The maximum residuals are:

| Diagnostic | Maximum residual |
|---|---:|
| `SS*=I` | 1.042e-15 |
| `S²=C` | 1.111e-15 |
| `(STphys)³=C` | 1.084e-15 |
| Symmetry | 2.586e-16 |

Charge conjugation reverses Dynkin labels. For SU(5)5, `c=5*24/10=12`; the physical vacuum T phase is−1. Direct surgery diagnostics give squared magnitudes6940.905365124694 and8049.9223594996165. NumPy emits divide-by-zero/invalid intermediate warnings for singular five-by-five determinant factorizations, retained in full stderr. The final entries are finite and all residual/tolerance checks pass. These warnings do not enter the exact integer certificate.

## Optimized-execution attack and concrete repairs

The original author script has five `assert` statements, including divisibility, seven target identities, cardinalities and nonvanishing. The old checker has its decisive `assert p,name` in `ck`; it increments its counter even when optimization removes the assertion. Both scripts ultimately print success without an independent surviving guard.

The author false control changes only expected `D00` constant5→6. Its source SHA256 is `2c7321ff91a3512ae1750cba4cac78098e1fc3d71dc9cfdd9f8aa7db437eeb94`. The checker false control changes only `scale(ab[0],one)`→`scale(ab[0]+1,one)`. Its source SHA256 is `d4bcbd9c8d95484ca95ce78e25c521b63ff3d5fee89e56a6d249e03a4851226b`. Exact diffs are [author_false_original.patch](author_false_original.patch) and [checker_false_original.patch](checker_false_original.patch).

| Control | Ordinary child exit | Optimized child exit | Optimized stdout |
|---|---:|---:|---|
| Original author, correct target | 0 | 0 | `all_pass:true` |
| Original author, false target | 1 | 0 | `all_pass:true` |
| Original checker, correct target | 0 | 0 | `status:PASS`, count2005 |
| Original checker, false target | 1 | 0 | `status:PASS`, count2005 |
| Explicit-guard author, correct target | 0 | 0 | correct positive receipt |
| Explicit-guard author, false target | 1 | 1 | empty |
| Explicit-guard checker, correct target | 0 | 0 | correct positive receipt |
| Explicit-guard checker, false target | 1 | 1 | empty |

The false optimized checker stdout is byte-identical to the positive original output, SHA256 `ec9b094f6634178229b7f6af9d0e630810f897f2c53d79e511d6b593c083c058`. That observed value is **2005**. An early internal progress message said1910; this was a reporting mistake, not an observed source/output count. It was promptly corrected against captured stdout and is recorded in the log.

Additional probes execute untouched original S and T arithmetic AST excerpts on deliberately invalid coordinates. Both normal originals raise; optimized originals accept an inexact division and print `INVALID_DIVISIBILITY_ACCEPTED`. Both repaired modes raise. These probe inputs are outside the valid-label domain; they demonstrate guard robustness and do not falsify the valid-label arithmetic. The fresh independent-control script also rejects a deliberately false Phi100 target under `-O`.

The positive repairs add

    def require(condition, message="explicit guard failed"):
        if not condition: raise AssertionError(message)

and replace each original `assert` statement with a `require(...)` call preserving its expression/message. They change no mathematics, targets, index set, formulas or output schema. All positive author receipts are byte-identical to the original verification JSON; all positive checker stdout is byte-identical to its original independent-results JSON. The false clean author runs start without `verification.json`, fail with exit1 and create no success JSON. Failed checker runs produce zero stdout. Preserved historical files in older copied runs are inputs, not evidence of a new success; consumers must require the captured fresh process exit/output.

Exact original-to-positive-repair artifacts:

| Script | Original SHA256 | Positive repair SHA256 |
|---|---|---|
| `verify.py` | `608b10d88b1c57a05a230dd7b4ed954e6cc3305d810ccc804bd58754bcfebf1b` | `1294068a5202c9f05ededf864887b7ce7bcb979319bd8f32827df5c88191a6e8` |
| `independent_checks.py` | `2267d374524bfc77380d736b1cb45a6d66c48130e53152909e5b0406dd84b980` | `47a6a532df1fc38db969e76ab6a21a13d5fba108a54e89d789cc0d86fcab0095` |

[author_explicit_guard.patch](author_explicit_guard.patch), [checker_explicit_guard.patch](checker_explicit_guard.patch) and [POSITIVE_REPAIR_MANIFEST.json](POSITIVE_REPAIR_MANIFEST.json) give exact patch hashes, paths, ordinary/optimized positive receipts and hostile failure receipts. The repaired copies are proposals for later preparation. The17 incoming original bodies have not been modified.

## Preserved reviewer failures and textual issue

Two failures belong to the fresh reviewer implementation, rather than the submitted mathematics. The first exact inverse check compared SymPy `Poly(1)` objects over QQ and ZZ using structural equality; the computed product was1 but the domain comparison returned false. Its source is retained as `independent_controls_v1.py`, with the exit1 receipt/stdout/stderr in `runs/independent_controls/`. The repair compares the exact remainder expression to1. The second SU(2) physical modular check used an insufficient symbolic simplification of unit complex phases; `independent_controls_v2.py` and its complete exit1 receipt are retained. The final control expands complex components before exact simplification. Ordinary and optimized v3 complete successfully. No failed run was relabeled a success or omitted.

A comment in the old checker states that the product of the two **squared** sine factors is sqrt5. As written it is wrong: `(2-u)(3+u)=5`; the unsquared positive factors have product sqrt5. Its actual root-product code and the old REVIEW's displayed explanation use the correct unsquared identity. This is an explanatory correction, with no effect on the reproduced certificate.

## Closure

[FINAL_REPRODUCTION_AND_FALSE_GUARD_CHECKS.json](FINAL_REPRODUCTION_AND_FALSE_GUARD_CHECKS.json) records output equality and clean negative controls. [CLOSED_PROCESS_MANIFEST.json](CLOSED_PROCESS_MANIFEST.json) indexes every controlled receipt and full capture; [CLOSED_MANIFEST.json](CLOSED_MANIFEST.json) indexes all artifacts with hashes and sizes. Source versions backing historical run hashes remain available. A controlled process-closure probe confirms that all40 earlier child PIDs were gone; the closure probe itself subsequently completed with exit0. No running receipt is left. Final closure comprises41 completed controlled runs.

Completion estimate is100% for this assigned arithmetic/implementation audit, not for novelty, peer review or public release. The exact mathematical result stands within its explicitly imported theorem scope. Runtime guards should be repaired before publishing the programs as executable certificates. Priority and publication authority remain with the human and parent gates.
