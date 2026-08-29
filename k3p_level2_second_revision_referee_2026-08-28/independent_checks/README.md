# Selected fresh independent checks

This directory carries forward six non-obsolete, reviewer-authored checks from
the 2026-08-27 review.  Each script was statically re-inspected and copied
byte-for-byte.  None imports a package producer, verifier, or atlas module.
The retired JC endpoint check is deliberately excluded.

The scripts are run with optimized Python disabled, isolated import behavior,
a fixed hash seed and locale, no network access, no credential access, and a
write boundary limited to `results/`.  The dependency-only interpreter is
Python 3.14.6 with SymPy 1.14.0 and NetworkX 3.5.

## Selected checks

- `check_three_leaf_geometry.py`: Fourier/domain identities, six tree--sunlet
  circuits, all six H14 leaf permutations, irreducibility, common rank-14
  point and smoothness, and the exact six-dimensional cherry map.
- `check_bridge_gluing.py`: marked/unmarked exponent ranks, pair-anchor inverse,
  gauge cancellation, and 2,000 exact-rational capped-gluing trials.
- `check_four_port_witnesses.py`: literal graph compilation, three quartic
  pullbacks, three rank witnesses, H21/sunlet upper factorizations, and an
  independent 40 = 38 + 2 residue quotient into fourteen double cosets.
- `check_restoration_probe_census.py`: all restoration and probe rows, hashes,
  cross-references, frozen-forest binding, exact Cartesian coverage, and strict
  witness margins.
- `check_probe_semantic_samples.py`: five literal semantic reconstructions
  covering every one-port disposition and a two-port equality/restriction.
- `check_krawczyk_box.py`: literal Fourier maps and Jacobians, rational interval
  Krawczyk inclusion/contraction, rank-15 Neumann bounds, and physical margins.

The source and package-input hashes, exact commands, elapsed times, exit codes,
and output hashes are recorded in
`results/fresh_selected_suite/SUITE_REPORT.json`.

## Independence limits

The four-port checker starts from the stored 40-row final residue and does not
redo the preceding 405,216-case reduction.  The restoration census binds and
streams the stored forest rather than regenerating it.  The semantic checker is
a five-row sample, not a replacement for the package's independent all-row
semantic replay.  The Krawczyk result proves uniqueness only in the supplied
15-dimensional pivot-coordinate slice box.
