# Centered quarter-grid K6 rank investigation

This folder tests one narrowly defined consistency question.

The existing exact K5 certificate is a symmetric distribution supported on
51 orbits of quarter-grid Gram matrices.  We ask whether it is the uniform
five-face marginal of a symmetric distribution on \(6\times6\) quarter-grid
Gram matrices that are positive semidefinite and have rank at most five.

The initial **fixed-support** test requires every five-face of a K6 atom to
belong to one of those same 51 K5 orbits.  Failure of this test would only
exclude an extension supported over those particular K5 atoms.  It would not
exclude:

- a different K5 distribution with the same triangle marginal;
- a K6 distribution whose five-face marginal uses additional K5 orbits;
- a 41-point spherical code.

`prepare_support.py` expands the 51 representatives into all their labeled
forms.  `enumerate_k6.cpp` adjoins a sixth vertex, checks all five-faces,
requires the exact scaled determinant to vanish, and canonicalizes under
\(S_6\).  The independent verifier tests the resulting exact marginal cone.

The fixed-support test is resolved exactly in
`fixed_support_proof.md`.  The independent verifier uses a much smaller
K4-gluing enumeration and the obstruction is the one-coordinate Farkas
witness \(-e_1\).

The broader triangle-marginal question has the opposite answer.
`direct_k6_triangle_extension.json` is an exact 51-atom distribution on
rank-five Gram-PSD K6 matrices with precisely the centered pair and triangle
marginals.  See `direct_k6_triangle_proof.md` and
`verify_direct_k6_triangle_extension.py`.

Thus the particular sparse K5 distribution does not extend, but its
pair/triple marginal does extend after changing the K5 marginal.  Neither
result is a global 41-point construction or obstruction.

The nested `k7/` folder repeats this phenomenon one level higher: the frozen
K6 distribution has no supported K7 extension, while an exact direct
rank-five K7 mixture realizes the same original pair/triple marginal after
changing the K6 marginal.

All Gram entries are scaled by four, so the diagonal is 4 and the edge
colors `0,...,6` represent `-1,-3/4,-1/2,-1/4,0,1/4,1/2`.
