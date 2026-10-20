# Partial results on fixed-triangle three-color avoidance

Prepared 2026-10-20. Problem identifier: AMR-030-0003 (3100003).

**Not a solution.** The unrestricted Euclidean three-color conjecture remains unresolved by this work. These notes provide exact partial results, counterexamples to particular constructions, and a mathematical audit. They make no novelty-priority claim.

For each fixed non-equilateral, nondegenerate triangle T in the Euclidean plane, the target asks for a coloring of every plane point with at most three colors and no monochromatic congruent copy of T. The coloring may depend on T. Congruence includes translations, rotations, and reflections, with scale fixed. See [SCOPE.md](SCOPE.md) for precise quantifiers, implementation boundaries, and public references.

## Contents

- [STRIPES.md](STRIPES.md): exact equal-width stripe criterion; a proven finite all-width decision procedure; fixed-width examples and limitations.
- [TILINGS.md](TILINGS.md): exact square-cell counterexamples and a finite-menu obstruction for regular colorings.
- [FINITE_OBSTRUCTIONS.md](FINITE_OBSTRUCTIONS.md): square-lattice and rational-coordinate limitations; finite-hypergraph reductions.
- [CERTIFICATION.md](CERTIFICATION.md): a mathematical decision procedure for supplied algebraic periodic polygonal colorings, not an implemented general verifier.
- [AUDIT.md](AUDIT.md): review of the stated partial results and historical reviewed-version hashes.
- `stripe_exact.py` and `stripe_exact_results.json`: rational fixed-width implementation and its five exact test results.
- `check_square_grid.py` and `square_grid_results.txt`: finite sanity check for the dyadic lattice coloring.
- `REPLAY.md`: execution results and packaging integrity qualifications.
- `MANIFEST.json` and `SHA256SUMS`: byte counts and SHA-256 integrity records.

## Reproduce

With Python 3 and its standard library, from this directory:

```sh
python3 stripe_exact.py
python3 check_square_grid.py
sha256sum -c SHA256SUMS
```

Both scripts use exact arithmetic. Their finite checks support implementation sanity, not full-plane coverage. No source PDFs, source images, copied source text, or datasets are included.
