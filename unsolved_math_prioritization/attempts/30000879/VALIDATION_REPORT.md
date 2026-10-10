# Verification of the nilpotent twist audit

## Reviewed version and result

The mathematical review covers the complete 19,481-byte research note with SHA-256 `734a12ebaa684e20feaba65d7e31db4dbb8892d58ffd02c2fc5b0a7315ab0807`. It includes the final twisted diagonal tensor argument. The result is acceptance as partial progress, with a two-word coset terminology clarification. No claim that the original conjecture has been resolved is accepted or made.

The separately supplied patch was applied to a temporary copy and verified byte-for-byte. The clarified note has the same byte count and SHA-256 `7fca262d2764d203a7a27793b218b4f98d3f5ab04e0350f78b928e84705735fa`. The sealed original was not edited.

## Independent exact arithmetic

An independently written sparse-matrix implementation uses integer arithmetic, with inverse matrices computed by a finite geometric series. It does not import the author's code. All checks pass identically under normal Python, -O, and -OO.

- Unitriangular families: classes 1 through 12, 120 generated triples per class, plus 729 exhaustive UT₃ triples in a finite coordinate box. Checks cover the cocycle identity, normalization, central section defect, quotient associativity, two-sided inverses, safe-depth commutation, the sharp pair, surviving and killed commutators, and the first-superdiagonal power formula. The two witness coordinates are checked on 49 signed exponent pairs per class.
- Isolator example: all 64 cocycle triples in (Z/2)², 2,000 integer-coordinate triples, 121 derived-subgroup and central-square tests, the power formula, parity homomorphism, and the nontrivial central commutator ratio.
- Subgroup modules: an S₃ example with a nonnormal order-two subgroup checks both coset partitions, 216 twisted associativity triples, and 16 bimodule-complement instances.
- Twisted diagonal action: 64 basis triples over a nontrivially twisted (Z/2)² test the equivariance identity and detect omission of the twist factor.
- Telescope: 84 finite vector-space systems with noninjective bonding maps verify injectivity, the colimit projection, and exactness by rational Gaussian elimination. The infinite telescope is justified by the proof, not by truncation.
- Rational augmentation: 40 cyclic-subgroup quotient obstructions check explicit nonzero cosets. Nonprojectivity and the infinite-dimensional conclusions are established by the proof.

The author's original dense-matrix checks were also rerun in all three modes and exactly reproduce the supplied outputs.

## Negative controls

The independent diagnostic suite rejects six deliberately corrupted mathematical formulas in each of the three Python modes: an omitted cocycle summand, an incorrect safe cutoff, failure to remove the central coordinate, an odd isolator group defect, an omitted diagonal twist factor, and an omitted telescope identity block. Including one baseline in each mode yields 21 controlled runs. These tests check the sensitivity of the diagnostics; they are not a formal theorem prover.

The author's 27 inventory controls were rerun on temporary copies. The independent audit verifier additionally checks the externally pinned inventory, exact file-set coverage, hashes, sizes, duplicate paths and JSON keys, canonical relative paths, symlink files/directories/roots, regular-file status, and scope flags. Its baseline and mutation receipts are generated outside the sealed package so that recording verification does not invalidate the inventory.

## Source verification

Both complete publisher PDFs were independently downloaded. Each has the same byte count and SHA-256 as the candidate's source record. The original problem page and Osofsky's two decisive pages were freshly rendered and visually inspected. Osofsky's right-module convention on the first page and the publisher's original 1968 bibliographic date were also checked. The 2016 online-posting date is not substituted for the print year.

Source metadata is supplied separately. Source text, PDF bytes, and page images are not part of the public payload. The author's uncited background sources are not imported as proof dependencies.

## What this verification establishes

The mathematical claims were checked by explicit argument at their stated generality. Finite diagnostics support formulas and catch specific errors. Hashes and inventories establish byte integrity and reviewed-version identity. None of these is a novelty search, an independent proof of the source's unnamed r = n result, or a resolution of the outstanding 2 ≤ r < n range.
