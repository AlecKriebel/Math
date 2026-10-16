# Correction context and scope

The original frozen manifest is externally pinned at SHA-256 `b4f6f9deb5689dbeddc837947eade82aa5ec4d9b532f299801fe35716c7d2f07`. Nothing in that directory is changed. This correction is an audit of the existing five mechanisms, not a sixth attempted solution.

The original full target remains equality of the source's two minimizing maps on every permitted finite ideal hyperbolic complex. The OWR statement's D, the full paper's weak closure D̄, an open-face diffeomorphism, and a diffeomorphism up to an undeleted edge are different notions. This derivative does not identify them by definition.

## Required changes

1. Sobolev edge values mean compatible traces, not freely assigned representatives on a set of area zero. The derivative spells out this convention.
2. Lemma 1's facewise geodesic interpolation must actually be admissible. The frozen proof silently infers that from quotient-cell preservation. The source permits self-identification of triangle sides, so the derivative makes admissibility an additional hypothesis of this partial lemma. Preservation of the same side incidence in each abstract face is sufficient. This is a hypothesis of the reduction, not an extra restriction on the full problem.
3. The compatible-facewise-isometry argument establishes equality of energies without invoking uniqueness. Identification of the particular maps now explicitly depends on the interpolation hypothesis. For identical metrics the identity supplies the energy minimum; identification with the identity is conditional as well.
4. The weak-closure postcomposition argument specifies the compactly supported smooth-flow and local Sobolev compactness mechanism. It does not infer weak continuity of arbitrary nonlinear operations.
5. The local flat target is explicitly a book of full half-planes; the half-disks are source domains. This prevents the formula from being misread as mapping each radius-two half-disk into itself.

## Exact local obstruction to the unqualified interpolation step

In the standard ideal triangle with ideal vertices 0, 1, and infinity, the two vertical sides can be identified by the isometry z ↦ z+1. Thus p=i and q=1+i represent the same point of the quotient edge. Their geodesic inside the abstract hyperbolic triangle has midpoint

m = 1/2 + i sqrt(5)/2.

Its real part is strictly between 0 and 1; its squared height is 5/4, larger than the bottom side's squared height 1/4 at that real part. Therefore m lies in the open face and not in the quotient edge. Equality of quotient-edge values does not suffice to keep facewise geodesics on the edge when their chosen side incidences differ.

This is a local obstruction to a proof inference. It is not a construction of two global minimizing maps, a counterexample to the conjecture, or an additional solution approach. The audit does not establish that the source's constructed u and v suffer this ambiguity; it records what this report must check before using its uniqueness lemma on all allowed gluings.

## Applying the patch

CORRECTION.patch is a unified diff from the frozen REPORT.md to current_derivative/REPORT.md. Its preimage and postimage are separately hashed in the audit manifest. Keep the original for provenance; use the current derivative for the accepted partial conclusions.
