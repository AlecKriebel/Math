# Ordinary triangle move lock

Status: **VERIFIED for JC by primary and clean-room implementations**

The only positive local move admitted in the candidate final classification
is ordinary triangle redirection `T` as defined in `DEFINITIONS_LOCK.md`.

The active primary verifier constructs all three labelled three-sunlet
orientations, checks the locked `sd0` class, directly sums all 64 Fourier
coordinates at one strict rational interior point, and gives a nonzero
rank-four Jacobian minor.  Its complete tensor has SHA-256

```text
de5a240bc79bd3d5b5bf89df8f82aa46ceffed3b8a62b637568e7336b1a38324
```

and its effective-chart determinant is

```text
-3/23058430092136939520.
```

The clean-room referee imports no primary code.  It independently enumerates
the mixed graphs and all admissible rootings, recomputes displayed trees and
all Fourier coordinates, differentiates every physical orientation, and
rejects eleven semantic mutations.  The three physical rank determinants are
nonzero, so each orientation maps submersively onto the four-dimensional
normalized three-port JC tensor space at the common point.  Their stochastic
images therefore share a full-dimensional regular germ.  Positive arm
scaling descends this statement to the projective port-tensor quotient used
by bridge peeling.

This proves the local converse needed for `T`, including contraction with an
unchanged external context.  It does **not** claim equality of complete open
stochastic images, and it supplies no non-`T` equivalence.

Active artifacts:

- `primary/verify_triangle_redirection.py`;
- `primary/certificates/jc_triangle_redirection_active.json`;
- `reviews/triangle_redirection_cleanroom/REVIEW.md`;
- `reviews/triangle_redirection_cleanroom/verify_all.sh`.

Reproduce from the project root:

```sh
python3 primary/verify_triangle_redirection.py
bash reviews/triangle_redirection_cleanroom/verify_all.sh
```
