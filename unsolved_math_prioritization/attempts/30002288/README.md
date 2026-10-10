# Fractional infinity eigenfunctions: audited partial resolution

Problem 30002288 / OWR-12336-004, rank 840. Canonical status: **unsolved, 5/5**. Compound outcome: **PARTIAL**.

## Accepted mathematical scope

The first representation question has a negative answer: for every fixed `0 < alpha <= 1`, finite positive weighted maxima of point-ridge profiles solve the full-space, zero-exterior fractional infinity-eigenfunction equation. On a nonsingleton high ridge, unequal weights yield eigenfunctions outside the unweighted ridge-subset family. A connected convex planar rectangle gives an explicit example. Read [the corrected proof](corrected/PROOF.md).

Two independent AI reviews accept the corrected core: [first mathematical audit](audit/MATHEMATICAL_AUDIT.md) and [second review](review2/REVIEW.md). These are AI checks, not human specialist or journal review, and numerical tests are finite corroboration rather than continuum proofs.

The second review **separately** accepts [the V2 supplement](supplement/SELECTION_LIMITS.md) for fractional Sobolev admissibility and root-level Rayleigh asymptotics. The exact full-space kernel uses exponent alpha*p and ordinary product-Lebesgue measure. Root-level energy coincidence does not establish the unrooted quotient limit or convergence of minimizers. General finite-p maximal selection is unresolved by this work.

## Immutable history and correction

All five ZIP archives and all original member bytes are preserved. The only core correction changes a viscosity paragraph in PROOF.md to the source's admissible C_0^1 global test class and explains tail finiteness. The [actual patch](audit/VISCOSITY_TEST_CLASS.patch) is applied with zero fuzz to a fresh original extraction during verification; every resulting byte must match the corrected archive.

Original `PENDING`, `PARTIAL_CANDIDATE`, three-approach and prepublication fields are historical snapshots. This README, PUBLICATION_METADATA.json and the two acceptance reports supply the later decisions. The V2 supplement completes five approaches; none is added by publication verification. See [separate acceptance](review2/SEPARATE_ACCEPTANCE.json).

No novelty, priority, worldwide open-status, human review, or full compound resolution is claimed. No source PDFs, source excerpts, rendered source pages, dataset contents or private coordination files are included.

## Hardened verification

Authenticate bootstrap.py and PUBLICATION_MANIFEST.json against independently recorded SHA-256 values before executing anything. Use a trusted Python interpreter and standard library, with a stable nonhostile filesystem. Then, with an absolute package path:

    python -I -S -B /trusted/bootstrap.py /absolute/package MANIFEST_SHA
    python -I -S -B -O /trusted/bootstrap.py /absolute/package MANIFEST_SHA
    python -I -S -B /trusted/bootstrap.py /absolute/package MANIFEST_SHA test_publication.py

The gate validates strict root/directory/file inventory, regular-file types, ancestry, byte counts, hashes, archives and every member before executing verified bytes in a private snapshot. Historical bootstrap bytes remain unchanged. A verified dispatcher adds -B to nested executions and rejects requested omission of -I or -S before interpreter startup; archived missing-isolation controls therefore receive the expected rejection without unsafe startup. The outer gate separately tests actual missing flags. No valid mathematical checker executes without -I -S -B. The tests include original audit controls, independent diagnostics, normal/optimized runs, relocation, hostile import paths, altered entrypoints, caches, symlinks, hardlinks, FIFO and bad-root controls.

Hashes establish artifact identity, not mathematical correctness. No defense against a malicious interpreter, standard library, operating system or concurrent filesystem mutation is claimed.
