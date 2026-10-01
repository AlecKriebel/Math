# Independent review: k203,b / 5100012

Date: 2026-10-01. Verdict: **PASS for the complete original source theorem**.

Reviewed frozen `PROOF.md` SHA-256:

    d1e04cf42d4358243365969487348887f3451f9b3fcef63b5215e7389af0e039

The proof establishes constancy of the product of the signed orbit area and the signed origin-pedal area for primitive elliptic-billiard periods that are odd or divisible by four, including primitive stars. The restored source setting is a strictly nested, nondegenerate pair of confocal ellipses. No arbitrary-M result or hyperbolic-caustic extension is required or certified here. No novelty or historical priority is certified.

## 1. Independent source and scope checks

I read and visually inspected Table3 in both the arXiv v11 paper (printed p6) and the published companion (printed p346). The k203,b row gives exactly A A_M, M=O, and N not congruent to 2 modulo 4. Section2 explicitly defines all areas by signed cross products. Thus stars are not to be replaced by the area of a filled-in region, and the feet belong to the consecutive side lines rather than an outer or contact polygon.

The source introduction specifies two confocal ellipses. Stachel's published Theorem4.3 and equation4.9 (printed p1614, visually checked) give the canonical parametrization and coprime turning-number condition used by the author. Its modulus is the eccentricity of the caustic, not the outer ellipse. The parameter v lies in (0,K), and the chord step is 2v. These factors of two are correct.

The theorem uses least period. Repeating an excluded primitive orbit cannot change its admissible parity by relabeling its number of traversals. Preserve that condition when describing the result. The same applies to signed areas and the elliptical-caustic restriction; the shorter imported wording must be read in its verified source setting.

## 2. Real geometry and area formulas

I independently substituted the addition formulas into the claimed caustic tangent line. Both chord endpoints satisfy it, with the common denominator 1−k²sn²u sn²v. The stated contact phase is correct.

The Euclidean pedal foot is n/(n·n), and the norm denominator reduces to dn²u/(α²k'²). This yields the displayed Q. Its complex continuation is bilinear rather than Hermitian; that is the meromorphic continuation of the real formula, as needed.

The cross-product identity and the dn addition identity give

    A = [ab sn(v)cn(v)/dn(v)] S(w).

The coefficient and the side-to-vertex counting are correct: every vertex dn term occurs twice before division by 2dn(v). The actual pedal phase is w+v. The argument does not insert absolute values, assume a simple polygon, or divide by the pedal area.

## 3. Pole divisor of the cyclic dn sum

I checked the Jacobi periods, shifts, zeros, and pole orders against DLMF22.4 and22.8. For dn the real period is 2K, the imaginary period is 4iK', and 2iK' is an anti-period. Its basic poles are at iK' and its basic zero at K+iK'.

With m=N for odd N and m=N/2 for even N, the orbit of jδ modulo 2K has exactly m members. Coprimality gives the reduced real period ell=2K/m. On the quotient torus with periods ell and 4iK', exactly N/m copies contribute to each pole of S. At a fixed imaginary level their arguments differ by real periods, so their nonzero residues have the same sign and cannot cancel. The second imaginary pole has the opposite residue.

Thus there are exactly two simple poles. Evenness together with the anti-period forces zeros at iK'+ell/2 and 3iK'+ell/2. These points are distinct and are not poles. The divisor degree forces these to be the entire zero divisor and makes them simple. Consequently S(w)S(w+ell/2) has zero divisor and is constant on the compact torus. This does not assume a generic modulus or hide an exceptional-period case.

## 4. The critical pedal-pole cancellation

At the common sn/cn/dn poles the map Q is holomorphic and vanishes. Its only other possible poles are the zeros of dn, where its order is at most two. At r=K+iK', the shifts and parity give

    Q(2r−z)=Q(z).

Hence the Laurent series has only even powers, in particular no first-order pole term. The two incident area contributions at a pole combine with their correct cyclic orientations to

    (1/2) det(Q(r+ε), Q(r+δ+ε)−Q(r−δ+ε)).

The second vector vanishes at ε=0, reducing the pole order to at most one. This cancellation is between adjacent area terms; it would not follow from inspecting an individual determinant.

There are no adjacent singular vertices because 0<δ<2K. For even N, the repeated pole indices are separated by m≥2, so their incident pairs do not produce an unexamined double-pole product. In N=4 the holomorphic neighbors happen to vanish, but the same order estimate remains valid. Wrapping the cyclic indices is legitimate because Nδ=4Kτ is a true period of Q.

Q changes sign under 2K and transforms by diag(1,−1) under 2iK'. Therefore its area sum T is periodic under 2K, anti-periodic under 2iK', and periodic under δ by reindexing. Its reduced torus is the same one as S. Its two possible simple poles coincide with those of S(u+K). Matching the residue at one pole and using the anti-period matches the other. Their difference is a holomorphic constant on the torus; the anti-period forces that constant to vanish. Thus T=C_T S(u+K). The proof correctly allows C_T=0 and never needs division by it.

## 5. Final phase and parity

The product is proportional to S(w)S(w+K+v). The shift (K+v)/ell is a half-integer exactly when N is odd or 0 modulo4. For N=2 modulo4 it is an integer. The desired cases therefore use the half-period divisor identity, while the excluded cases give a square of S and are not silently included.

Reversal changes both signed areas by a sign and preserves their product. Primitive star rotations satisfy the same identities. The circular limit, outside the strict a>b setup of the complex argument, also follows directly from rigid rotation of regular star polygons and their central pedals.

## 6. Independent controls and replay

The author checker was inspected and rerun from a copied review directory. Its output reproduces the frozen JSON byte-for-byte: 37,393 exact assertions over 6,231 primitive rotations, plus 4,092 separately labeled 75-digit diagnostics. Its verification-file SHA is d50714f5a5cc7c50be418a90d8f4ef0fd131d4b605231b7aa872849f03e7dd49.

My independently authored checker imports no author modules. It passes 13,712 exact lattice assertions over 3,428 primitive rotations and 348 high-precision diagnostics at 95 digits. The numerical tests construct pedal feet directly from the real chord normal, cover odd and divisible-by-four primitive stars, test complex proportionality away from the real line, and approach the alleged double poles to check their simple-pole cancellation. Nine excluded-parity examples show nonconstant products. All diagnostics pass; their largest reported scaled discrepancy is about 3.69e−34, coming from the finite-distance residue tests.

These are finite controls and non-certified numerical diagnostics. They corroborate, but do not replace, the written universal analytic proof above.

## 7. Approval boundary

No mathematical revision to the frozen candidate is needed. This PASS is independent of the sibling k203,a author contribution: I did not participate in that argument and did not use its arbitrary-M lemma here. Preserve the collaboration disclosure and require its separate review.

This is a full mathematical/source PASS for k203,b, not a novelty certificate. Publication and queue updates remain subject to the parent's gate. No remote mutation or external outreach was performed as part of this review.
