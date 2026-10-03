# Problem 30005804: Dol'nikov's conjecture

Status: original unresolved after five substantive author turns; independent
review pending. No solved status or novelty claim is made. This directory is
a checkpointed research record, not a claim that the original problem is settled.

## Original target

Three finite color families are translates of one compact convex planar K.
Every two members from different colors intersect. Must some one color have
a transversal of at most three points? Translation vectors are arbitrary real
vectors, and closed-boundary contacts count. The original source is Roldan-
Pensado's contribution, OWR 3/2024, printed pages 172-174:
https://ems.press/content/serial-article-files/48651.

SOURCE_GATE.md records the exact imported-target distinction and the primary
literature. In particular the general four-point theorem is already known.
The imported projection-theory text preceding the Dol'nikov contribution is
not part of this problem.

## Preserved work and strongest claims

- TURN_1.md: A hypothetical counterexample can be replaced by rational polygon
  translates with strict cross intersections. Exact arrangement and Helly
  certificates decide finite instances. The resulting search is only a
  counterexample semidecision procedure.
- TURN_2.md: Exact collinear piercing formula, two-point collinear consequence,
  and a positive-width single-strip sufficient condition for arbitrary K.
- TURN_3.md: Exhaustive integer-lattice certificates for two nonsymmetric
  trapezoids. Only the two specified bodies and integer translations are covered.
- TURN_4.md: For any K, two cross-intersecting color families whose translation
  centers lie on r and s lines parallel to one common direction satisfy
  tau(A)<=r or tau(B)<=s. A separate argument gives a sharp two-color two-point
  bound when row spacing is at least K's perpendicular width. This covers all
  K_m=conv{(0,0),(m,0),(1,1),(0,1)}, m>=1, with centers in R x Z.
- TURN_5.md: A quantitative multiple-strip construction and a three-point
  theorem when all cross differences belong to (3/4)(K-K). A self-contained
  maximum-determinant normalization supplies the universal constant. The
  original hypothesis has factor 1, not 3/4. An explicit diamond proves the
  proposed unit-square three-cover extension false; it is not a counterexample
  to Dol'nikov.

## Exact remaining gap

The source imposes neither a three-row restriction nor a fixed positive
intersection margin. Strict rational approximation may have its best margin
arbitrarily close to 1. The two-coordinate rectangular relaxation loses
cross-color geometric constraints and can require four translates even for
a body whose original Dol'nikov case is already known. No mechanism here
recovers the full arbitrary-real-translation factor-one conclusion.

## Reproduction

Python 3 standard library only. From this directory run:

    python check_turn_1.py
    python check_turn_2.py
    python check_turn_3.py
    python check_turn_4.py
    python check_turn_5.py

Do not use Python's -O flag: the checkers intentionally use assertions.
Compare stdout with TURN_N_CHECKS.json. The third and fifth scripts regenerate
and compare their exact JSON certificates in memory. An optional --emit flag
writes the respective certificate; it is not needed for verification.

All calculations use fractions.Fraction. The controls for analytic theorems
are finite tests, not a replacement for the written proofs. The turn-3 lattice
claim itself has a justified finite exhaustive reduction, stated in that file.

The 21 original blobs recovered from commit 64a67d6 are unchanged. Author turns
1-3 were consumed before recovery, and turns 4-5 continue that budget. Historical
manifests record their respective checkpoints. TURN_5_MANIFEST.json snapshots
all final research files except itself and the later remote receipt. The receipt
records the exact remote commit after a non-force branch update.
