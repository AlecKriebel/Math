# Reproducing the finite checks

## What the evidence establishes

The all-size mathematical arguments are in the proof notes. The included finite programs check exact identities, finite avoidance classes, reconstruction, coefficient calculations, and examples. They do not establish asymptotic claims by finite extrapolation. An audit that compared supplied output records is not described as independently rerunning their programs.

The frozen verification outputs sit beside their checkers. The analytic audit groups also contain `FINAL_CHECKER_RECEIPT.json`, identifying normal, optimized, and double-optimized runs and the precise comparison rules. Some outputs are byte-identical; others differ only in declared elapsed time, interpreter, or optimization fields. The general-cut transfer checks explore the graph observed within the finite horizon, rather than exhaustively constructing an all-size graph.

The packaging check replayed three existing diagnostics in all three modes: tree-series verification, two-ended window-certificate checks, and the near-empty construction check. All nine processes succeeded and regenerated the original JSON bytes unchanged. [Packaging smoke receipt](PACKAGING_SMOKE_CHECKS.json) records that limited scope. The whole checker collection was not rerun during packaging. No new mathematical argument was undertaken to assemble this reader.

## Optimization-mode qualification

Six retained checkers contain Python `assert` statements. Python removes those statements under `-O` and `-OO`. Use a normal-mode run for their assertion-based validation; an optimized replay establishes process/output compatibility but does not show that the removed assertions executed. Explicit failure checks elsewhere may remain active. The retained programs are unchanged. The six script paths and assertion counts are listed in [the package-review checks](PACKAGE_REVIEW_CHECKS.json).

The independent package review additionally replayed nine original diagnostics in all three modes, for 27 successful processes. Every regenerated mathematical report matched; the only changed fields were elapsed seconds or the declared optimization level. This includes normal-mode assertion validation for the sampled tree-series checker. The complete 35-script suite was not rerun. See [the scoped package review](PACKAGE_REVIEW.md).

## Environment

The scripts use Python 3.12 syntax. The independent family re-audit also imports SymPy and mpmath; the remaining checkers use the standard library. Packaging smoke checks used Python 3.12.14. The available symbolic environment was SymPy 1.14.0 and mpmath 1.3.0. Those versions are recorded for reproduction, not a claim that other versions fail.

A fresh environment may install the two dependencies with:

```sh
python -m pip install sympy==1.14.0 mpmath==1.3.0
```

No network access or source download is needed by the mathematical checkers once their dependencies are installed. No external dataset is needed.

## Integrity first

From this reader's root:

```sh
python verify_package.py
```

This verifies the exact file set, byte counts and SHA-256 values against `PACKAGE_MANIFEST.json`; it also checks that mapped original proof/checker bytes were not changed. Editorially derived audit reports are checked against their public hashes. Their original hashes in historical receipts remain provenance and should not be mistaken for current public-file hashes.

## Replay without changing frozen evidence

Some original scripts write JSON beside themselves. Do not execute them in the frozen package if preserving its manifest matters. The supplied runner makes a disposable copy for each run, then saves stdout, stderr, and changed/generated JSON in a new directory outside the package.

List the 35 original checkers:

```sh
python replay_checks.py --list
```

Replay the fresh independent family re-audit in all optimization modes:

```sh
python replay_checks.py --match 'independent_family_reaudit/check_family_proofs.py' --modes 0,1,2 --output ../family-replay
```

Replay the complete finite suite in all modes:

```sh
python replay_checks.py --all --modes 0,1,2 --output ../all-checks-replay
```

The destination must be new and outside this package. Full enumeration can take materially longer than the small smoke suite. A zero exit code is a successful program run; the run's actual scope and generated records still govern what was tested. The runner does not silently replace or update the original accepted outputs.

## Selected meaningful coverage

- **Fresh family re-audit:** all 1342 avoiders through n=8, exact labeled and forest-shape multiplicities, independent tree enumeration through n=9, closed-form coefficients through n=30, 80 marked-depth coefficient inequalities, 53,217 minima-deletion pattern cases, and 146,047 ambient merge triples.
- **General frontier:** 24,621 insertion parents, 151,916 valid edges, 607,244 deletion checks, 30,610 descendant bounds and 9,084 tail bounds.
- **Exact 1324 kernel:** normalized canonical state-chain distributions through n=8, not just total counts; actual counts 1, 2, 6, 23, 103, 513, 2,762, 15,793 for sizes 1 through 8.
- **Kernel obstruction and isolation:** 19,204 parity-collapse objects through n=8, 12,082 unrestricted domino guard tests, and 159,069 marked blocks in 360 finite inequalities.
- **Window and endpoint checks:** 1,023 composition profiles, 81,435 finite mountain windows, and the terminal-lift factor-two fibre, which actually occurs in the finite cases.
- **General packing and exact cuts:** 41,965 packing cases, 305,110 crossing rectangles, 96 perfect-packing examples; 53,226 exposure histories, 274,001 prefix-edge observations and 288 finite observed-transfer comparisons.
- **Low-chain and rectangles:** 919 row-shuffle tests, 28 dense-edge tests, 56 height-three coefficient comparisons and 216 marked-run inequalities; 213,162 marked-pair deletion round trips and 30,570 reconstruction allocations, including 1,524 inadmissible allocations correctly rejected.
- **Folding:** 780 distinct source paths and 16 full permutation reconstructions. This diagnostic does not contain an embedded proof pin and is not represented as a test of the later all-size source-coordinate entropy argument.

The canonical 1342 and 1324 count sequences are different. Their finite reports must not be conflated.
