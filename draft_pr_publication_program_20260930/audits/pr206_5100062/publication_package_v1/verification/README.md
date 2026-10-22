# Portable finite exact verification

The current source is `portable_exact_verifier.py`, 21,804 bytes, SHA-256 `dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85`. It uses only Python's standard library. The recorded interpreter is Python 3.14.6. The documented isolation flags require Python 3.11 or later. No scientific dependency or bytecode is distributed.

## Scope and actual outcomes

The suite checks **four specified genuine convex primitive billiard polygons, all winding +1**, on x²/8+y²/5=1. H and V are triangles with lambda=40/9. The diamond and rectangle have period four with the same caustic parameter lambda=40/13. It recomputes their geometry, inversion and signed areas. Higher odd periods, admitted stars, and phase constancy are proved analytically in the paper; they are not inferred from these four examples.

Each positive run performs **245 mathematical checks in 27 fixed nonempty groups**. This count is neither a number of sampled general billiards nor a proof-coverage percentage. It includes arithmetic sanity checks, 14 vertex/edge incidences and tangencies, 28 coordinate reflection checks, the inversion equations, area/product expectations, signs, triple repetition, radius 2, physical similarity at s=3/2, and the exact inequality of the two even products. The exact expected group ledger is included in both the source and each successful receipt.

`results_normal.json` and `results_optimized.json` are the actual explicit receipts from successful executions, byte-identical to raw stdout. Both include the executed source SHA, Python version and `sys.flags`; their mathematical payloads agree, while optimization flags differ. `RUN_SUMMARY.json` records the arguments, exits, raw-output equality and hashes. The paper's finite-control table is reproduced from these runs.

## Execution and file safety

From the package directory:

```sh
python3 -E -S -B -P verification/portable_exact_verifier.py
python3 -E -S -B -P -O verification/portable_exact_verifier.py
python3 -E -S -B -P verification/run_negative_controls.py
```

Default behavior writes only JSON to stdout. Successful controls exit 0. Rejected inputs emit JSON with status FAIL and exit 1. No network access or implicit receipt output is present. To request a new receipt explicitly:

```sh
python3 -E -S -B -P verification/portable_exact_verifier.py --receipt chosen-new-file.json
```

Its parent directory must already exist. Exclusive create rejects an existing file, directory or symlink without overwrite. Use a new path, rather than the distributed receipt paths. Runtime/source bindings are included even on ordinary rejection paths. `--help` lists the finite fault interface.

## Exact arithmetic and guards

The field is Q(sqrt(2),sqrt(3),sqrt(5),sqrt(13)) with the positive real embedding. Each element has 16 rational `Fraction` coefficients. Products reduce repeated prime generators exactly. Division recursively conjugates a generator and verifies that the norm eliminates it; zero division rejects. Edge square roots are checked by squaring in this field. Unsupported radicals reject.

Exact signs use integer-square-certified rational lower/upper enclosures for each basis radical. An expression must be separated strictly from zero. The bounded 4096-bit enclosure budget fails closed if unresolved; there is no total sign-oracle claim for arbitrary inputs. Equality compares every rational coefficient exactly.

All guard conditions require actual booleans. Scalar inputs accept actual integers, `Fraction`, or the exact field class; bool values and every float, including finite floats, NaN and infinities, reject. Polygon inputs must contain at least three distinct exact coordinate pairs. Primitive period must be an actual integer matching the number of distinct vertices. Confocal parameters are exact rationals with strict inequalities. Zero edges, invalid square roots, colliding vertices, unsupported values and wrong results reject. Reflection uses normalized incoming/outgoing edge velocities and the unnormalized normal (x/a²,y/b²) in the standard reflection formula.

Tangency checks cover the actual cyclic closing edge, the common confocal equation, and contact strictly within the segment. The suite establishes convex positive winding for these four polygons. Inversion denominators must be strictly positive. Deliberate repeats use a separate positive-integer repetitions parameter and concatenate the primitive base list; repeated lists are not relabeled primitive. Both inversion equations are checked for every unit-radius vertex.

Every expected ledger group has an exact fixed positive count. Missing, extra or unknown groups, false results and empty data reject. Verification uses explicit exceptions, so checks survive `-O`. These contracts cover the documented finite API, rather than arbitrary hostile source mutation or caller monkeypatching.

## Distinct scaling tests

The suite separately recomputes the following:

* Reverse traversal: each signed area changes sign; the product is unchanged.
* Three indexed traversals: area factor 3, product factor 9.
* Inversion radius 2, with the physical orbit/foci fixed: area factor 16, product factor 256.
* Physical similarity s=3/2, scaling the orbit and both foci while fixing inversion radius 1: area factor 4/9, product factor 16/81.

The latter is not a radius substitution: its scaled squared axes are 18 and 45/4 and its foci are ±3sqrt(3)/2. Directly, I_(sf)(sP)=(1/s)I_f(P)+(s-1/s)F_f, so signed area scales by s^-2. The recomputed scaled products are 5/1296, 5/1296, 8/405 and 169/8100.

## Meaningful negative controls

`run_negative_controls.py` pins the verifier hash and executes each supported fault in both normal and optimized children. Its **26 attempts are expected rejection tests**, not extra mathematical checks. Every attempt records its actual flags, arguments, expected/actual exit, and raw stdout/stderr in `negative_control_results.json`. A PASS from the harness means all faults rejected, not that a false identity passed.

The 13 faults per mode are wrong area, wrong product, empty polygon, colliding polygon, NaN coordinate, infinite coordinate, bool coordinate, noninteger period type, bool repetition, Fraction-valued repetition, missing ledger count, wrong physical-similarity area, and wrong physical-similarity product. Every child must return FAIL, exit 1, matching source hash and empty stderr; otherwise the harness fails. The harness creates no receipt implicitly.

## Verification history and limits

The preserved original submission contained assertion-based check programs whose verification assertions disappear under `-O`; those historical programs and their old PASS receipts are not the current verification. The original archive remains unchanged outside this public package. The current exact source replaces those executable checks and was separately source-reviewed, including optimized execution and malformed-input rejection, before package authoring was frozen. Separate AI review is not independent human peer review.

The two even-period controls were derived during post-submission verification. Their source provenance does not establish novelty. Finite exact arithmetic validates these examples only; it neither formalizes nor proves the meromorphic all-period argument. No interval computation, human refereeing, proof-assistant certification, priority conclusion or whole-package acceptance is supplied by a successful run.
