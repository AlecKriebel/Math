# Audited partial research: projective characters and square roots

**Problem:** 30005508 / OWR-13750328-013, rank 489.  
**Disposition:** Unsolved, five substantive approaches completed.  
**Review:** Fresh independent AI audit passed the scoped partial results. This is not journal peer review.  
**Claims:** No general proof, counterexample, full resolution, or novelty claim.

## Mathematical record

The [frozen research packet](release/README.md) proves a central-quotient reduction from the local square-root formula to the involution-orbit conjecture, retaining the necessary multiplier 1 or 2. It also proves the formula in the standard C₃⋊E family for every index-two pair of 2-groups, establishes a direct-product transfer result, and checks all six involution classes of an explicit nonnilpotent order-864 block.

The general involution-orbit conjecture remains unresolved. Scalar Frobenius–Schur identities are not substituted for this orbitwise assertion.

Read the [complete independent audit](audit/AUDIT_REPORT.md), including its scope and limitations. The independent controls verify a finite-field block certificate, actual defect pair and projective character, all six order-864 involution classes, 124 root tests in nine model pairs, and 66 positive actual-block quotient tests. These finite checks supplement the proofs; they do not establish the universal conjecture.

## Reproduction and byte preservation

Run from this directory:

    python3 verify_publication.py

The verifier checks every file in RELEASE_MANIFEST.json, all frozen author hashes, all audited file hashes, and reruns both exact programs against their recorded complete outputs. It uses the Python standard library only. AUTHOR_MANIFEST.json records the earlier author freeze, before independent audit; its historical pending-audit status is retained unchanged. AUDIT_MANIFEST.json records the subsequent completed audit.

All ten frozen author files and all four public audit files are preserved byte for byte. Full scholarly PDFs, source caches, and operational records are not part of this publication. Only this problem's queue status, turn count, and findings cell are updated; other queue content and links are preserved.

## Queue-provenance correction

The frozen SOURCE_GATE.md identifies `c87c275c638939b8008fd58db80657491d14971e` as the queue blob SHA. Publication preflight found that this string is an old metadata-like line embedded in the actual queue text. It is not the verified current blob identity. That frozen statement is therefore corrected here without rewriting the historical author packet.

The publication base is main commit `f63a97ada19c9b377e7aa2073d30e301f94a4c45`. At that commit, the actual queue blob is `e2b391103c4ca67341aa41fcb36c648a96fd77c8`, confirmed by exact blob retrieval and independent Git-object hashing. Its embedded header is retained, not repaired. This provenance clarification changes no mathematics, finding, or attempt count.
