# k818: a credited constant ratio with an essential domain exception

**5100061 / AMR-050-0061. Already solved as a shared-proof corollary, 1/5 substantive author turns.** Independent source/dependency review passes with the qualification below. This is not a new independent discovery or a claim of historical priority.

## The exceptional family must remain explicit

For the genuine primitive six-periodic family in an ellipse with aspect ratio a/b = 2 and the specified strict confocal elliptical caustic, the focal antipedal signed area is identically zero while the focal inverse signed area is nowhere zero. The ordinary quotient is therefore **undefined at every phase of that family**. There is no removable 0/0 cancellation and no everywhere-finite invariant is claimed.

At the exact phase with a = 2 and b = 1 in [TURN_1.md](TURN_1.md), the original, inverse and antipedal signed areas are respectively

    A = 20 sqrt(5)/9,    V = 15 sqrt(5)/8,    B = 0.

The six distinct vertices satisfy reflection and have a strict confocal caustic with squared semiaxes 32/9 and 5/9. This is not a repeated lower-period orbit or a degenerate caustic. The source's Table 11 already records the zero-area phenomenon, which is credited.

## Natural-domain theorem and dependencies

Fix a strict noncircular confocal ellipse pair and a primitive billiard family of least period N congruent to 2 modulo 4, including coprime star windings. Use signed traversal areas, unit inversion about either original focus, and the antipedal constructed from the original vertices.

The prior reviewed proofs give constants c > 0 and k, depending on the family, with

    V = c A,    B = k A,    A > 0

in the positive caustic orientation. Therefore, if k is nonzero, V/B = c/k is finite and constant throughout the family. If k is zero, its ordinary domain is empty. The projective value [V:B] = [c:k] remains defined, but is explicitly an extension of the source's finite-ratio expression.

- [k805 / PR 257](https://github.com/AlecKriebel/Math/pull/257) supplies the inverse/original proportionality and positivity, using the generic mechanism already credited to PR 207
- [k404 / PR 255](https://github.com/AlecKriebel/Math/pull/255), Sections 3–5, supplies antipedal/original proportionality for all primitive even periods, allowing k = 0
- Both complete proofs and their reviews are preserved unchanged in [inputs/](inputs/)

The exact source is [arXiv:2004.12497v11, Table 9, printed p. 11](https://arxiv.org/pdf/2004.12497v11), with signed-area and geometric definitions in Sections 2, 3.5 and 3.9. The independent review accepts the natural-domain corollary; a literal assertion of an everywhere-defined finite quotient is refuted by the six-periodic example.

## Review, reproducibility and preservation

Read the frozen [author proof](TURN_1.md), [independent review](independent_review/INDEPENDENT_REVIEW.md), [current state](REVIEWED_STATE.json), and [publication manifest](PUBLICATION_MANIFEST.json).

The 66 author exact controls replay byte-for-byte. A separate 165-assertion checker uses homogeneous line intersections and signed triangulation, and verifies primitivity, reflection, tangency with contacts inside segments, both original foci and the exact areas. Run with Python 3 and SymPy:

    python verify_turn1.py
    python independent_review/independent_controls.py

These finite checks establish the exceptional orbit; the universal corollary relies on the two full prior proofs. This is AI-assisted mathematical review, not human peer review or formal verification.

All eleven public author-checkpoint files at commit 2b217388b6d5d745f6a7a666b9572bc80679d597 and all six files of the new independent-review packet are preserved byte-for-byte. Historical pending-review text is unchanged. The original author manifest also binds two local-only imported records; those raw records and all source PDFs, extracts and images remain excluded as declared in REMOTE_SCOPE.json. The current disposition is additive.

Circular, hyperbolic or degenerate caustics, unsigned filled areas, outer-polygon foci and artificial changes of primitive parity by repetition are outside this theorem. There is no remaining mathematical gap in the stated natural-domain corollary, and no historical-priority claim.
