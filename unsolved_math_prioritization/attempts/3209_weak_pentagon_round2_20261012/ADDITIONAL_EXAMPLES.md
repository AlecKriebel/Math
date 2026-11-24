# Additional explicit authored non-global examples

These small graphs preserve the concrete meaning of the non-global observations in the switching audit. Their edge lists and vectors are mathematical proof content. They are not a raw sample collection, and displaying them does not increase any reported coverage count. Labels use vertices 0 through n−1, and cube labels are four-bit integers; unit differences are 1, 2, 4, 8 and the antipodal difference is 15.

## A. A 14-vertex small-defect example

The cut side is S={7, 8, 9, 10, 11, 12, 13}. The 21 edges are:

    (0,1) (2,3) (7,8) (9,10) (0,12) (0,11)
    (1,13) (1,8) (2,9) (2,7) (3,10) (3,11)
    (4,12) (4,13) (4,11) (5,8) (5,10) (5,13)
    (6,9) (6,7) (6,12)

Its complement is the matching M={(0,1), (2,3), (7,8), (9,10)}. A fixed-M witness in vertex order is

    (0,15,3,12,5,6,0,1,14,1,14,4,1,7).

Every cut edge has unit difference and every M-edge antipodal difference. The prescribed cut has 17 edges. Switching {2, 7, 9} gains one, so this cut is not globally maximum. The exact global maximum is 19; exhaustive direct edge counting over all 8,192 cuts normalized by keeping vertex 0 outside the chosen side gives precisely these maximizing masks: 4794, 6826, 15684. A mask is the ordinary sum of 2^v over vertices in the chosen side. This finite enumeration is a bounded certificate check, not a universal claim.

## B. A 16-vertex three/four-stable example

The cut side is S={8, 9, 10, 11, 12, 13, 14, 15}. The 24 edges are:

    (0,1) (2,3) (4,5) (8,9) (10,11) (12,13)
    (0,8) (0,15) (1,14) (1,10) (2,13) (2,14)
    (3,12) (3,15) (4,14) (4,11) (5,15) (5,9)
    (6,13) (6,8) (6,10) (7,11) (7,12) (7,9)

Its complement is the matching M={(0,1), (2,3), (4,5), (8,9), (10,11), (12,13)}. A fixed-M witness in vertex order is

    (0,15,5,10,3,12,5,6,1,14,13,2,2,13,7,8).

Every cut edge has unit difference and every M-edge antipodal difference. The prescribed cut has 18 edges. Switching {0, 2, 6, 8, 13} gains one, so this cut is not globally maximum. Its saturated-endpoint cut graph has maximum degree one, so it is three/four-stable by the exact theorem. The exact global maximum is 22; exhaustive direct edge counting over all 32,768 cuts normalized by keeping vertex 0 outside the chosen side gives precisely these maximizing masks: 39510. A mask is the ordinary sum of 2^v over vertices in the chosen side. This finite enumeration is a bounded certificate check, not a universal claim.

## C. The sharp density example

The full 16-vertex sharp example, its six-edge complement, improving five-switch, fixed-class witness, 22-edge maximizing cut, and two disjoint pentagons proving the upper bound are displayed in SWITCHING_PROOFS.md and checked in SWITCHING_AUDIT.md. Its original 18-edge cut is four-stable but not globally maximum. Its normalized maximizing mask is 26982.
