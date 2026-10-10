# Fractional infinity eigenfunctions: a representation counterexample

Problem 30002288 / OWR-12336-004, rank 840.

## Read first

PROOF.md gives a complete elementary candidate counterexample to the first of
the problem's two questions. Finite weighted maxima of point-ridge profiles
satisfy the full nonlocal viscosity eigenfunction equation. With two ridge
points and unequal weights they escape every unweighted subset representation.
An explicit example uses a connected convex rectangle and works for every
0<alpha<=1.

The compound problem is only partially resolved. The general selection of the
maximal solution by finite-p eigenfunctions is not proved or disproved here.
The explicit asymmetric examples are excluded from finite-p limits by symmetry.
The familiar transitive-ridge special case is explained without claiming novelty.

Independent mathematical audit is required before publication. No external
specialist acceptance, novelty, priority, proof-assistant certification or
complete literature survey is asserted.

## Files

- PROOF.md: complete analytic argument and exact mathematical scope
- STATUS.json: machine-readable bounded outcome and approach count
- SOURCES.json: public provenance and inspection metadata, without source text
- verify_math.py: finite exact-arithmetic and numerical corroboration
- RESULTS.json: deterministic expected output of that checker

The checker does not prove the infinite continuum statement. The proof does
not rely on numerical tests.

## Frozen verification

Use the separately supplied external manifest and independently pinned bootstrap
with Python's isolated/no-site flags:

    python -I -S FRACTIONAL_INFINITY_30002288_AUTHOR_BOOTSTRAP.py \
      EXTRACTED_DIRECTORY FRACTIONAL_INFINITY_30002288_AUTHOR_SAFE_FREEZE.zip \
      FRACTIONAL_INFINITY_30002288_AUTHOR_EXTERNAL_MANIFEST.json

Append --optimized to replay the checker with -O. The bootstrap verifies the
pinned external manifest, archive, full flat inventory, regular-file status,
file digests and byte counts before executing the named checker. It verifies
the output against RESULTS.json. Relocation is supported. Extra files,
directories, caches, symlinks and altered entry points are rejected.

The separate validation receipt records normal, optimized and relocated runs
and negative controls. A pass means finite tests and artifact checks passed,
not independent mathematical acceptance.

The frozen payload contains only authored work and public verification metadata.
No downloaded sources, source extracts, corpus records or private coordination
material are included. No repository publication was performed by the author.
