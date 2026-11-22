# Gonality subdivision residual attempt: frozen authored package

Problem 3000040, ordered row 1871. **PARTIAL / OPEN RESIDUAL.** Local preparation only: no publication or queue edit is performed by this package. The five attempts and acceptance boundaries are in REPORT.md; AUDIT.md is the prior independent mathematical/computational audit.

## Established results are not new solutions

The primary source is van Dobben de Bruyn, Smit and van der Wegen, *Discrete and metric divisorial gonality can be different*, JCTA 189 (2022), 105619, https://doi.org/10.1016/j.jcta.2022.105619. Its Theorem 1.4 supplies known simple bipartite examples with gonality 6t and two-segment gonality 5t. Proposition 5.3 supplies the known upper bound dgon(G) <= 2 dgon(Gamma(G)) - 1; the sharp universal ratio remains between 6/5 and 2 in the inspected source. Theorem 1.3 supplies finite attainment. These are source dependencies, not new discoveries here. Literature searching was bounded and does not certify present-day openness.

No odd-segment drop or first-drop-beyond-two witness was found. No odd-invariance theorem, improved universal ratio, or solution of the residuals is claimed.

## Exact computational scope

- Uniform minimal tricycle: m=1 through 9, 3,024 candidates, all candidate positions retained. Gonality 6 for odd m and 5 for even m; the only degree-five successful positions at even m are the three midpoints.
- Asymmetric labelled bases: six cycle lengths all 1, six common spoke lengths s in {1,2}, three independently chosen transition lengths in {1,2,3}; exactly 54 bases, each at m=1,2,3, for 162 tests. Gonality triples have counts (5,5,5):42, (6,5,6):9, (6,6,6):3. Independent replay visits 10,541 candidates, stopping at the first witness where one exists. No isomorphism reduction or broader exhaustive claim.
- Completeness and five/six bounds depend on the cited tricycle lemmas. The independent implementation is not an independent full proof of those source lemmas.

## Reproduction and hardening

Run from any working directory:

    python -B /path/to/package/replay.py
    python -B /path/to/package/negative_controls.py
    python -O -B /path/to/package/negative_controls.py
    python -B /path/to/package/verify_inventory.py

Replay executes all three hardened checkers, once normally and once under -O, in isolated temporary directories and compares every generated JSON value to the packaged full evidence. REPLAY_RESULTS.json includes complete stdout/stderr and comparison results for both modes. The compact TRICYCLE_CHECKS.json, LENGTH_CHECKS.json, and AUDIT_CHECKS.json retain full outputs without truncation.

Four assertions were replaced by explicit if-not/raise AssertionError checks. Two fixed-root output paths were made relative to the script file. No mathematical algorithm or test range changed. originals/ contains only the original authored Python programs, not third-party sources. provenance/ includes complete original, path-adjusted, and hardened ASTs (with locations), all original assertion nodes and source hashes. negative_controls.py independently reconstructs and exactly compares the transformation, checks all four guards against valid/corrupted values, and tests known tree/cycle/parallel-edge ranks using both implementations. A deliberately wrong non-strict burning threshold is detected by the tree control. All controls pass in normal and optimized modes.

AUDIT.md and SOURCE_STATUS_GATE.md preserve their original stage-specific descriptions; references there to absent packaging or original script paths describe the earlier stage, not the hardened entry points here. Running check_lengths.py directly still writes its output and runs on import; replay avoids imports and isolates writes. Do not run any of the direct checkers against frozen evidence if preservation is desired.

## Inventory and public-data boundary

verify_inventory.py first lstat-checks the root and recursively checks every descendant without following links, rejecting root/nested symlinks, FIFO, sockets, device nodes, and other nonregular entries before reading the manifest or any payload. Tests cover real root/nested links and FIFO; socket/character/block coverage uses synthetic stat modes only. No socket fixture was created. This protects a stable local tree; no claim of race-proof protection against concurrent hostile filesystem replacement is made.

MANIFEST.json records every other regular file's byte count and SHA-256, rejecting missing or extra files. A sibling freeze receipt binds the manifest hash and full package inventory. The receipt is external to avoid self-hashing. Python bytecode is excluded by use of -B; a later cache or extra file causes verification failure.

Only authored reports/code/evidence and public verification metadata are included. Downloaded source PDFs, extracted source text, dataset contents, private corpus records, and private coordination material are excluded. The original source/status gate and public hashes are retained, without copied source documents. This package is ready for separate review, not a claim of remote publication or acceptance beyond the stated partial attempt.
