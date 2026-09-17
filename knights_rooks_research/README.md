# Knights and rooks: N=4, R=2 is impossible

**Result:** no finite placement satisfies the requested conditions. In fact,
if each rook sees exactly two knights and no rooks, some knight must attack
at most three rooks, even when knight-knight attacks are allowed.

The result is proved by the rightmost-knight argument in **PROOF.md** and
**research_note.pdf**. Bounded board searches are NOT the proof.

## Reproduce the final verification

Use Python 3.9 or newer. No pip packages, network access, paid service, or
external solver are required for these commands.

```sh
python3 src/run_all.py
```

For the minimal UNSAT certificate check:

```sh
python3 src/verify_unsat.py certificates/local_relaxation.cnf certificates/local_unsat_tree.json
```

Expected certificate statistics: 3 nodes, 1 split, 151 unit inferences,
2 contradictory leaves. The split is K(-1,1), the same two-case alternative
resolved by reflection in the geometric proof.

**FINITE_REDUCTION.md** explains why the 28-square local relaxation covers
every hypothetical finite solution, despite allowing arbitrary continuation
outside its window. The checker does not import or depend on the solver.

## Files

- `research_note.pdf`, `research_note.tex`, `RESEARCH_NOTE.md`: self-contained research note.
- `PROOF.md`: standalone universal geometric proof.
- `FINITE_REDUCTION.md`: complete finite reduction, encoding, certificate semantics.
- `src/check.py`, `src/check_sorted.py`: independent outgoing-attack reconstruction algorithms.
- `src/local_cnf.py`: necessary local relaxation generator.
- `src/dpll_prove.py`, `src/verify_unsat.py`: prover and independent proof checker.
- `src/test_check.py`, `src/test_verification.py`, `src/run_all.py`: tests and complete reproduction.
- `certificates/`: DIMACS, variable names, clause reasons, UNSAT tree, source attack reports.
- `data/`: source coordinates, reproduced calibration candidates, exploratory SMT-LIB instances.
- `sources/`: cited source images and reference/status log; image git blob hashes are tested.
- `logs/`: inspected calibration, search, and verification outputs.
- `progress.json`: final checkpoint and exact verification/resume command.
- `MANIFEST.sha256`: SHA-256 checksums for all other bundle files.

## Inspect the direct attack checker

The checker defaults to the actual target (knight degree 4, rook degree 2).
Because no target solution exists, the supplied coordinates are clearly
marked **calibration examples**, not target witnesses.

```sh
python3 src/check.py data/source_N4R1.json --knight-degree 4 --rook-degree 1
python3 src/check_sorted.py data/source_N4R1.json --knight-degree 4 --rook-degree 1
```

Each command prints every piece's outgoing attacks. Removing the final
rook-degree override correctly rejects this N4R1 example as an N4R2 witness.

## Optional exploratory searches

`src/search_board.py` uses a local Z3 shared library through `src/z3shim.py`.
The environment used Python 3.13.5 and Z3 4.13.3.0. These searches are not
required to verify the result. Optional symmetry and parity switches are
search restrictions, not justified universal reductions.

```sh
python3 src/search_board.py --width 6 --knight-degree 4 --rook-degree 1 --timeout 10
python3 src/search_board.py --width 8 --timeout 40
```

`Z3_LIBRARY` may be set to an explicit compatible shared-library path.
The 32x32 search was interrupted by the execution time limit; it has no
reported mathematical outcome and plays no role in the proof.

## Provenance and priority

The target is the N=4, R=2 cell of Erich Friedman's February 2007 Math Magic
page. That cell still displayed '?' when rechecked in this session.
Initial and final searches did not locate a prior exact-target resolution.
Historical priority is NOT claimed established by those searches. All new
proof and verification work here was performed in this conversation; no
external review, publication, or personal contact is claimed.

The final result is a mathematical nonexistence proof, not an unsuccessful
search re-labeled as an answer.
