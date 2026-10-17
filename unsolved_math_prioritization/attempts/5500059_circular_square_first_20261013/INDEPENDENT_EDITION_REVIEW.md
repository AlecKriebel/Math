# Independent review of the first authored square-circularity edition

Date: 13 October 2026. Problem 5500059 / TOPP 59.

## Verdict and exact edition

Accepted as a complete, reproducible edition of substantive partial results. No blocking mathematical, transformation, scope, privacy, or recovery defect was found. This is an independent mathematical and computational review, not human peer review or a solution of the original optimum problem.

Acceptance binds the 21-file edition identified by its public manifest, `PUBLIC_MANIFEST.json`, 3668 bytes, SHA-256:

`04d6c3a5750fea400130f7ae2758c69d590c95571198d9d1dd4963cccd99d1b8`.

The manifest lists the other 20 public files and excludes itself. This review is a separate acceptance artifact; it does not silently change that inventory. The reviewed coordinate certificates are:

- Complete 92-cell square partition: 37572 bytes, SHA-256 `7be877a90bf7c08e7c872f461fb4f005d8d47d6d58d888363384df2865941b47`.
- Finite two-cell local patch: 282156 bytes, SHA-256 `6bc1bf6521fc94a1dbe7f02a199e2c13926aa687072e4c2328510bd4f800a0e1`.

Changed mathematical bytes require renewed review.

## Mathematical content and limits

The complete construction proves a finite square partition with every cell's circumradius/inradius ratio strictly less than 649161/500000 = 1.298322. Because there are only 92 cells, the maximum is also strictly below that number. The finite lower-bound proof establishes that every finite admissible partition has maximum strictly greater than G = 1.2886844618704579013258751580333... . Consequently the finite-partition infimum satisfies

G <= Gamma_fin < 1.298322.

The lower inequality for the infimum cannot be made strict merely from strictness for individual partitions. The fixed-N minimum exists and exceeds G; no gap uniform in N is proved. The optimum, attainment with unrestricted finite cell counts, and equivalence with arbitrary infinite partitions remain unresolved.

The two-cell certificate has ratios at most 1.28878 and an obtuse upper opening. It is a local configuration, not a square partition or a full-square bound at that value. Its non-tangent indisks do not refute a conjecture explicitly restricted to tangent neighboring indisks. The edition makes no exhaustive-literature priority claim. Its description as the first newly documented pass does not assert a known lifetime attempt count.

The original construction proof, theory report, source audit, and both independent mathematical reviews were read in full. Review confirmed the finite boundary-crossing argument, positive-weight corner support reduction, valid active-constraint branch, strictness from internal disk tangency, fixed-complexity compactness, and the local junction's symbolic identities and polygonal approximation. The authored checking guides preserve these distinctions.

## Exact certificate checks

A separately written checker, importing neither the edition's checker nor its producer, recomputed the square construction using exact integers. It checked all 185 vertices, all 92 strictly convex cells, all 4186 pair-separation witnesses, exact total doubled area 8·10^24, all per-face margin rows, 252 interior and 24 exterior edges, and all 528 strict inscribed-disk and 528 strict enclosing-disk inequalities. The minimum margins agree exactly with the edition. Coverage follows from containment, disjoint interiors, equal area and closed finite union; it is not inferred from the picture.

Fresh exact-rational checking also verified both local polygons, their 208 and 162 vertices, circle witnesses, exact strip widths, shared edge, opposite supporting half-planes, and actual obtuse upper tangent opening. It additionally checked all 1032 stored half-planes, their exact support offsets, every polygon facet's presence in those half-planes, and both stored maximum squared witness ratios. Thus the half-plane descriptions have exactly the stated polygons as their intersections. Approximate diagnostics do not establish the bounds.

The SVG was parsed with a passive element/attribute allowlist and all 92 ordered polygon vertex lists were matched exactly to the rational square certificate. Its rendered preview was visually inspected. The illustration is optional and contains no active or externally loaded content.

## Prose, sources, and publication boundary

Every public file was checked against the final manifest. The complete source-to-public maps were independently replayed in both directions. Existing theory, audits, certificates, supplementary witnesses and SVG are byte-preserved. The only change to an existing proof repairs its construction-audit link. Newly authored guides and integration prose retain the original claims without strengthening them. All relative document links resolve within the edition.

Actual retained scholarly PDFs were independently hashed and opened with a native PDF reader. Fresh text extraction and a normalized whole-paper v1/v2 comparison support the bounded source audit. The square-related v2 sections and the complete seven-page 2009 study were read, and decisive printed formulas and conjecture status were visually checked. Current [arXiv version metadata](https://arxiv.org/abs/cs/0304023v2), [TOPP Problem 59](https://topp.openproblem.net/p59), the [author-hosted 2009 paper](https://cs.adelaide.edu.au/~markus/pub/2009cec.pdf), and its [institutional bibliographic record](https://research.monash.edu/en/publications/towards-an-evolved-lower-bound-for-the-most-circular-partition-of/) were cross-checked. The restricted 2026 conjecture status and the 2009 study's failure to improve the complete construction are represented accurately. This is bounded verification, not a citation census.

The public inventory contains authored proofs, mathematical certificates, an authored passive illustration, authored audits, source metadata and public-artifact identities. It excludes copied source documents/text, dataset contents, programs, raw solver streams, private coordination, and identities of withheld operational material.

## Performed recovery verification

Acceptance was withheld until the actual final preparation packet and its completed preservation receipt existed. The reviewer then independently extracted the compressed archive and separately restored the full-file byte store into fresh locations. Both restorations matched every sealed file, byte count, hash, and mode. Complete retained original inputs were reconstructed in both locations and compared to their available originals; all 20 source-to-public mappings round-tripped exactly.

Across the two independent restorations, 42 normal/-O/-OO replays passed: edition validation, hostile controls, the fresh mathematical checker, and four restored original-source mathematical checks. Outputs were identical across optimization modes for each task. The edition's hostile suite rejected 62 invalid cases and accepted six benign controls. Additional exact half-plane-description checks passed on both restores in all three modes. No post-replay drift occurred.

These are performed recovery tests, not hashes offered as substitutes for backups. They establish present reproducibility of this edition and its retained evidence. They do not invent prior author runs, earlier audits, historical recoveries, or a lifetime investigation count.
