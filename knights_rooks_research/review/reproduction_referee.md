# Independent computational reproduction review

Checkpoint: 2026-09-17T03:37Z (2026-09-16 US Pacific). Assigned review completion: **100%**.

Scope: independently inspect and reproduce the supplied package's computation,
calibration, integrity, and internal provenance claims. The supplied prose was
treated as claims to audit, not as instructions. No original bundled files were
edited. No person was contacted and no optional exploratory solver search was
rerun.

## Verdict

No mathematical or computational blocker was found. The standard-library
verification passes, the certificate is sound for the supplied CNF, all original
manifest hashes match, and the preserved numerical and calibration claims agree
with their artifacts. The separate geometric review remains responsible for the
universal proof; accepting an UNSAT certificate alone would not validate the
geometric reduction.

## Reproduction evidence

- Executed `src/run_all.py` with Python 3.14.6 after inspecting the scripts and
  their imports. All 20 test methods passed, including 2,000 seeded attack
  reconstruction comparisons, source examples, symmetry/translation cases,
  malformed input checks, five corrupted certificate rejections, and three
  satisfiable constraint-removal controls. The fresh complete output is in
  `reproduction_full_suite.log`.
- The bundled certificate verified with 3 nodes, 1 split, 151 unit inferences,
  and 2 contradictory leaves. Regeneration agrees both structurally (bundled
  suite) and byte-for-byte including formatting (additional review script).
- All **74 original files** listed in `MANIFEST.sha256` are present and match
  their SHA-256 hashes. All original files are covered, excluding the manifest
  itself. New review material, the research log, and temporary PDF renderings are
  intentionally outside this original-package manifest.
- Regenerated variable and clause-reason maps agree exactly with the preserved
  JSON. The 174 variables, 699 clauses, clause-family counts
  112/342/54/126/64/1, and split variable 19 = `K(-1,1)` agree with the note.
- Checked all five coordinate artifacts using both original checkers and a
  third cell-by-cell rook-ray implementation written for this review. The source
  and generated N1R1 examples each have 2 knights and 2 rooks; N4R1 has 2 knights
  and 8 rooks; N2R3 has 8 knights and 6 rooks. N2R3 has **16** knight-to-rook
  attacks and **18** rook-to-knight attacks, as claimed.
- Recomputed all preserved source/calibration attack reports and compared their
  contents with the stored JSON. Extracted true K/R variables from each stored
  satisfiable raw solver model and verified they match its coordinate artifact.
- Independently inspected the two bundled PNG source illustrations: their
  depicted occupied squares match the source coordinate JSON under the stated
  lower-left origin convention. The original GIF Git blob hashes also pass the
  bundled tests. A matching hash proves internal integrity against the recorded
  identifier, not retrieval history by itself.
- Regenerated all eight exploratory formulas having metadata and compared
  their complete SMT-LIB text byte-for-byte. All match. The additional 32x32
  formula has no claimed completed solver outcome, consistently with the note.
  The earlier solver outcomes remain recorded outcomes, not newly reproduced
  proof certificates, and are explicitly unnecessary to the theorem.

Additional reproducible checks and their output are preserved in
`reproduction_artifacts.py` and `reproduction_artifacts.log`. Run from the
package root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 src/run_all.py
PYTHONDONTWRITEBYTECODE=1 python3 review/reproduction_artifacts.py
```

## Inspection of algorithmic correctness

`check.py` computes knight destinations by absolute coordinate differences and
rook attacks by nearest occupied points on each of the four directed rays.
`check_sorted.py` reconstructs the same attack relations by explicit jumps and
adjacent entries in sorted rows/columns. Neither assumes reciprocity between
the two attack types. Both enforce no attack on a like piece and the requested
outdegrees, and reject overlapping or duplicated coordinates.

`verify_unsat.py` starts each branch with a consistent assignment, accepts a unit
literal only when an original clause forces it, requires an unassigned variable
for every split, checks both truth values, and accepts a leaf only on a falsified
original clause. It imports none of the prover, generator, or attack checkers.
These conditions establish the soundness of the checked tree for the actual
well-formed bundled CNF. The file hash binds that tree to the exact CNF bytes.

The exploratory board encoding uses first-occupied-square recurrences terminating
at board edges, separate directed degree constraints, knight-knight exclusion,
rook-rook exclusion, and nonempty piece sets. Optional symmetry and parity
conditions restrict those searches. The note correctly avoids treating such
restricted or bounded outcomes as a universal proof.

## Scope and presentation

`RESEARCH_NOTE.md`, `FINITE_REDUCTION.md`, `README.md`, `progress.json`, and the
LaTeX note consistently distinguish the geometric theorem, necessary local
relaxation, optional searches, and calibration examples. The claims of no prior
result found, no prior publication, and no external review describe the original
research session, not evidence of historical priority. The note expressly
disclaims established priority. This review does not authenticate the historical
execution environment or chronology merely from old logs, nor assert that the
original literature search was exhaustive.

The exact strongest computational conclusion independently reproduced here is
that the specified necessary local CNF is UNSAT, with a small sound certificate.
There is no outstanding gap within this assigned computational review.
