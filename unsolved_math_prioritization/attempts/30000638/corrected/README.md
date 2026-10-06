# Volume Bounds for Symmetric Lattice Polytopes

30000638 / OWR-1394-015. **Partial; original conjecture unresolved.**

Read `PROOF.md` for the exact hypotheses, credited earlier results, complete
partial proofs, five approaches, and precise remaining gap. `SOURCES.json`
contains public provenance and retrieval metadata without source-document text.

The mathematical contributions here are elementary verified partial arguments:
a quotient-lattice proof of the known crosspolytope case, the 3D case with
at most five interior lattice points, boundary-sensitive certificates,
product/free-sum closure statements, and precise obstructions to
several incomplete proof routes. Novelty is not asserted.

## Reproduce

Requires Python 3.10 or later, standard library only. No network access,
external datasets, package installation, or source PDFs are needed.

    python verify.py
    python -O verify.py
    python test_fail_closed.py

The verifier is independent of the working directory and accepts no bypass
flags. It checks the frozen manifest before importing the geometry engine,
then recomputes all finite certificates. It does not mechanically verify
the general mathematical prose. A fresh mathematical audit remains appropriate.

The 37 specified 3D cases are a small deterministic stress suite, not a search
over all polytopes. Passing finite checks is not a proof of the conjecture.

The archive contains only authored proof, code, results, and public metadata.
It excludes downloaded PDFs, extracts, the source corpora, and private
coordination material. `MANIFEST.json` binds every other delivered member;
the outer ZIP hash is supplied separately.
