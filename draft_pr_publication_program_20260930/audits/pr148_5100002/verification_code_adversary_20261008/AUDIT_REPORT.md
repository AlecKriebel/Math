# PR148 verification-code and adversarial reproduction audit

The preserved original computations are internally consistent and reproduce exactly. The original checkers are unsafe to treat as unconditional certificates: optimized Python removes all their `assert` rejection, and output metadata/proof bytes are not pinned or compared internally. The unchanged mathematical data pass; adversarially false conditions can also emit PASS. Audit-only explicit-guard candidates fix the demonstrated failures. This is no publication clearance.

## Scope and frozen identity

Assigned target: literal k108 = (A′/A)/∏ sin(θᵢ/2), with internal polygon angles and N ≡ 2 mod 4. The claimed counterexample compares two convex primitive hexagons on E: x²/4+y²=1, with common caustic squared semiaxes 32/9 and 5/9 and λ=4/9.

Original HEAD supplied in the assignment: `538fd2584f7dc7375e4eaa91d73daddde3d073cd`. This audit validates the 20 archive files directly; it has not changed any real Git index/ref/cache, research-program file outside this owned folder, or provider state. `original20_manifest_before.json` and `original20_manifest_after.json` bind all 20 files and establish that they remained unchanged. All mutations and reproductions are under this owned folder.

All 20 files were read, including top-level author checker/receipt, identical author replay checker/proof/receipt, inherited independent checker/results, source manifest, source verification and review receipts, proof, provenance records, and research log. The top-level and replay author sources and proofs are byte-identical. The proof SHA is `5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab`, author checker SHA is `ff77421cc3789a9ede0dec1982d8f4812c1e6ea498defa8ed7afcf072dcdd6c6`, and inherited checker SHA is `c93ada0c3d08b1e7ae117eeb5257eaf3284a1f0fc1882f89f7cc15953c86b221`. Every recorded local proof/report/author-verifier binding present in the original receipts matches the archived bytes; see `original_hash_binding_assessment.json`.

Original `turns.json` reports ONE direct-coordinate approach. It is not an actual timestamped chat-turn/native-transition ledger. Original accounting remains 1/5. This audit adds zero new central proof-search turns.

## Coverage and mathematical assessment

| Requirement | Author checker | Inherited checker | Assessment |
|---|---|---|---|
| Exact input | SymPy rationals/quadratic radicals; rejects Float in vertices | Fraction coordinates with metrics diag(1,5), diag(2,1) | Exact arithmetic for these fixtures, no numerical orbit solver |
| Same strictly nested confocal pair | Explicit λ, semiaxis and focal-difference checks | Fixed physical constants; quadratic caustic coefficients scaled by G | Correct for the unchanged constants |
| Six primitive convex counterclockwise vertices | Distinctness, positive turns, all nonincident vertices left | Distinctness, global strict left-side tests, period/parity | Closure and reflection plus six distinct vertices imply least period six |
| Finite-side caustic tangency | Exact support identity, reconstructed contact, 0<t<1 | Independent line-quadratic double root, reconstruction and 0<t<1 | No supporting-line-only or exterior-contact loophole |
| Physical reflection | Full unit-vector specular equation, J=±1/3 | Full vector reflection in scaled Euclidean metric | G-dot products correctly represent the physical geometry |
| Same directed family | Common caustic, positive left branch, J and perimeter | Same caustic, left branch, J and perimeter | Family membership uses the standard Poncelet family/porism premise; code does not itself compute a continuous path between seeds |
| Outer polygon | Solves consecutive tangent pairs, nonzero determinants, exact coordinates, vertex on finite outer side | Solves tangent pairs rationally, checks both equations and finite side | Correct source-style outer polygon, not contact or pedal polygon |
| Signed areas/internal angles | Positive shoelace areas; cosθ=−e_in·e_out and positive half-sine | Scaled areas, same internal cosine convention, exact square-root product | Correct signs and denominator positivity for convex fixtures |
| Unequal literal quotient | Each computed K checked against exact constants; final expected-constant difference | Each K checked, then actual stored K difference | Both give 11664/3125 and 3645/1024, difference 553311/3200000 > 0 |

In the inherited checker, physical points are D(u,v), with D=diag(1,√5) or diag(√2,1). Its G=D² dot products, B=diag(G₀/4,G₁) outer conic, and C=diag(9G₀/32,9G₁/5) caustic represent the same physical ellipses. Cross products/areas gain the positive factor det D; the area ratio cancels it and the area-product control multiplies by det G. These are correct transformations.

Direct Fraction rechecks are in `direct_fraction_rechecks.json`: H has A′/A=36/25 and sine product 125/324; V has 45/32 and 32/81. All square roots use the positive branch because every internal angle lies in (0,π). The ancillary product 5/9 and area product 320/9 are only two-example controls, not a repaired all-period theorem. I found no intrinsic arithmetic/geometric contradiction in the unchanged checker fixtures.

The inherited count 272 counts calls to ck; its 14 exact_sqrt assertions (12 lengths and two final products) are additional, uncounted guard calls. Reported check counts are not evidence of enforcement under optimization.

## Reproduction receipts and process closure

Required interpreter commands were used: `/Users/alec/Documents/Math/pr9_adversarial_review_20260929/algebra_env/bin/python -E -B -P` (SymPy 1.14.0), and `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P` (Python 3.14.6 standard library). Each also ran with `-O`. Exact executable/version outputs have their own raw receipts.

All six unchanged runs—top author 291, author replay 291, inherited 272, each normal/optimized—regenerated byte-identical frozen receipts and identical stdout. This reproduces the claimed arithmetic; unchanged `-O` success alone does not establish guard coverage.

The audit contains 62 bounded child runs total. Every `raw_runs/<label>/` directory contains complete raw stdout/stderr and a process receipt with exact argv, cwd, PID, PGID, start/end UTC, return code, output byte counts/hashes, wait/reaping confirmation, and a post-wait absent-process-group check. Each run had a 60-second time bound and 524288-byte combined raw-output cap; no timeout, truncation, or surviving group occurred. Aggregate results are in `AUDIT_SUMMARY.json`.

## Demonstrated robustness failures

| False condition | Original normal | Original -O | Repaired candidate normal / -O |
|---|---|---|---|
| Caustic squared x semiaxis changed 32/9→31/9, so original chords are not tangent and pair is not confocal | Nonzero exit: author strict_nested_confocal; inherited caustic_double_root | PASS for both | Nonzero exit, no PASS, both modes |
| Expected H k108 changed 11664/3125→11664/3126 | Nonzero exit: exact_k108 / literal_quotient | PASS for both | Nonzero exit, no PASS, both modes |
| Inherited exact_sqrt requested on 2 times the correct product square, which is not a rational square | AssertionError | PASS with truncated integer-square-root rational | Explicit exact-root rejection, both modes |
| Reported difference field changed to false zero while all mathematical computations remain unchanged | PASS for both | PASS for both | Computed-receipt mismatch rejection, both modes |
| Proof prose changed to falsely state difference zero | PASS with new proof hash | PASS with new proof hash | Frozen artifact hash mismatch, both modes |
| Prior/frozen receipt H value changed to zero | Original replaces its prior output and PASSes; it does not audit prior bytes | Same | Frozen expected receipt hash mismatch, both modes |

The first three rows are genuine false geometry/value failures of the original guard enforcement, not merely altered display text. Five optimized false-condition runs emitted PASS. The false computed receipt field demonstrates four additional PASSes under both modes without any mathematical guard failing. The proof/previous-receipt cases identify the distinction between recomputing values and validating a preserved mathematical/review artifact. Existing original artifacts themselves have correct hashes and fields; these tests establish attack/failure possibilities, not that the archived receipts are presently false.

Failed runs also leave an old PASS output file on disk because neither checker clears it or writes a failure receipt. `stale_receipt_assessment.json` records this. Consumers must require the current process return code and fresh stdout/output receipt. A copied historical PASS must never be treated as the result of a failed run.

## Precise repair nomination and remaining scope

`candidate_guards_original20/` and `candidate_guard_repairs.diff` are reviewable audit-only nominations. The mathematical calculations are unchanged. Replace the author/replay ck assert with an explicit conditional RuntimeError, replace inherited ck assert likewise, and replace its bare exact_sqrt assert with an explicit exact-square rejection. The candidate expected receipts are copies of the frozen originals. Explicit SHA guards pin both expected receipt and original proof; the computed result must match the frozen numerical/semantic receipt. Candidate author output retains its new actual verifier SHA; only that known repair-related field is normalized in the comparison. Its changed source hash is separately recorded in `candidate_repair_manifest.json` and each mutation run receipt. The author copies remain identical. Six candidate true baselines PASS; all candidate false cases fail with no emitted PASS in normal and optimized modes.

A ROOT repair can implement the same minimal mathematical guards and put frozen receipt/artifact/source pinning in a global wrapper instead of every checker. Such a wrapper should also bind all reviewed files, record current process completion/fresh output, and compare receipts explicitly. It must acknowledge changed checker SHA values rather than call repaired source byte-identical to the original.

The 20-file source manifest contains URL, PDF-digest, and visual-inspection declarations, but no PDF bytes or native execution transcript. Source table correctness/current literature/priority must be validated in the ROOT source audit; this code audit does not re-certify those claims. No primary-source correction, novelty, priority, human peer review, repaired all-period invariant, or publication eligibility follows from this report. No external communication, provider write, Git mutation, or original-file modification occurred.

Audit task completion estimate: 100%. Strongest verified result: the unchanged original291/inherited272 computations and exact values reproduce, while explicit guards plus frozen receipt binding reject the demonstrated adversarial conditions. Remaining global gap: ROOT must decide and apply the nominated repairs, update all changed source/receipt bindings consistently, complete independent mathematical/source/metadata checks, and decide publication status.
