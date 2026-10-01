# Independent full review: 5100020 / k403,a

## Verdict and exact version

**PASS_COMPLETE_SOURCE_TARGET. No mandatory correction.**

This verdict binds the unchanged `PROOF.md` SHA-256 `ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e` and `FROZEN_MANIFEST.json` SHA-256 `f278871cea589c62313b550825567fb46e9c61a400c0ee406420ca7b8e76c0fa`. All twelve author files and three primary PDFs match their pinned hashes. The review checks the analytic argument independently; finite controls are supplemental. This reviewer did not contribute to the author's proof route.

The accepted theorem is constancy of the product of the signed origin-pedal and origin-antipedal areas of the **original orbit**, for primitive odd periods, including stars, in the strict nondegenerate confocal elliptical-caustic setting. Real intersections are finite. Zero signed areas are allowed. The circle case is proved separately. Neither even periods nor outer/inner derived polygons are substituted. No priority or novelty certification is given.

## 1. Source and coordinates

I read the definitions and visually inspected Table5 in both the [arXiv v11 source](https://arxiv.org/pdf/2004.12497v11), printed7, and the [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), printed348. Both specify the unprimed product A_m A*_m, odd N and M=O. The opening source definition explicitly uses two confocal ellipses. Its area convention is signed cross-product area. Sections3.3 and3.5 distinguish feet on original supporting lines from intersections of perpendicular lines through original vertices. The dropped star in one prose label does not alter the table or geometric definition.

The published Stachel Theorem4.3 and equation4.9 were checked: its modulus is the numerical eccentricity of the caustic, the parametrization is (-a sn w,b cn w), and the phase step is twice v=2K tau/N. Thus 0<v<K, delta=2v, and N delta=4K tau. The caustic axes are alpha,beta, not the outer axes. Confocality follows directly from the Jacobi quadratic identities. The [DLMF period/pole tables](https://dlmf.nist.gov/22.4) and [addition formulas](https://dlmf.nist.gov/22.8) confirm all shifts used. Complex dot products must be bilinear, as in the candidate.

The [credited prior PR204](https://github.com/AlecKriebel/Math/pull/204) concerns 5100012, the original area times origin-pedal area. Its title/body and stated scope were independently verified. The present proof restates the needed pedal argument rather than assuming that earlier review proves it. No neighboring k403,b or primed-object result is used.

## 2. Real geometry and support-line identity

For consecutive original vectors P,Q, the antipedal lines are P dot X=H(P), Q dot X=H(Q). I independently reconstructed their intersections by homogeneous line cross-products, preserving each named line and its sign. The candidate's expressions in the basis P,JP satisfy both equations. The cyclic shoelace sum combines the two coefficients incident to each original vertex into precisely

    F(P,Q)=[H(P)H(Q)-(H(P)+H(Q))(P dot Q)/2]/det(P,Q).

There is no missing factor of two and no convexity assumption in this identity.

The chord determinant is B(u)=2ab sn(v)cn(v)dn(u)/D(u), D(u)=1-k²sn²(v)sn²(u). On the real axis every factor in its numerator is positive and D>=1-k²sn²(v)>0. Thus consecutive normal vectors are independent and every real antipedal intersection is finite. The caustic tangent n(u) dot X=1 is the actual original chord. Its perpendicular foot n/(n dot n) gives the stated Q(u); its real denominator is positive. Direct named-side incidence controls accompany the review, so an opposite-line sign error cannot be hidden by equal areas.

These arguments allow self-crossing traversals and use their signed shoelace area. There is no division by either polygon area.

## 3. Complete complex chord divisor

Let p=iK'. The Jacobi functions have the common simple-pole lattice stated in the proof. The function D is elliptic for 2K and2p, with one double pole in that cell. The p-shift identities give simple roots at p+v and p-v. For example D'(p+v)=2cn(v)dn(v)/sn(v), nonzero under the strict hypotheses. At those roots dn is finite and nonzero, giving simple poles of B. This accounts for both roots of D, including multiplicities.

At u=p, dn has a simple pole and D a double pole; B consequently has a simple zero. At u=K+p, dn has a simple zero and D=cn²(v) is nonzero, giving the other simple zero. There are no omitted poles or zeros. The endpoint vectors at these two zero types are finite, because v is strictly between0 andK.

The reflection identities distinguish their geometry. About K+p the endpoints coincide; about p they are opposite. For coincident endpoints, the numerator identity

    4 numerator=(H(P)+H(Q))H(P-Q)-(H(P)-H(Q))²

is quadratic in Q-P. Hence the simple determinant zero is removable even if an individual complex norm is zero. For opposite endpoints the numerator generally does not vanish, and at most a simple pole remains. The proof correctly retains it.

## 4. Vertex cancellation, odd quotient and uniqueness

A single antipedal edge term incident to a simple vertex pole can have order two: its numerator has order at most three and its determinant denominator a simple pole. Its neighboring vertex is regular because delta is not0 modulo2K. The reflection about p and antisymmetry of F turn the sum of the two incident terms into G(z)-G(-z). This eliminates the double Laurent coefficient and leaves at most a simple pole. The identity is exact, rather than a cancellation inferred from a numerical residue.

For odd primitive N, delta/ell=2tau is coprime to N, where ell=2K/N. Thus the cyclic sums have real period ell. A common imaginary shift2p reflects the y coordinate of every P, reversing F; hence the area is anti-periodic2p and periodic4p. The opposite-endpoint midpoint poles have phases p-v-j delta and3p-v-j delta. Since v=tau ell, all of them are exactly the same two classes p,3p on C/(ell Z+4p Z). This parity step is indispensable. Even if an opposite-endpoint term shares a phase with the canceled vertex pair, it has only order one, so their sum remains of order at most one. This also covers N=3.

The trace S=sum dn(w+j delta) is even and has exactly two simple poles p,3p on that torus. At a representative pole only one summand is singular, with nonzero residue. Its anti-period forces opposite residues. Evenness and the anti-period force zeros at p+ell/2 and3p+ell/2. Neither is a pole; equality of total zero and pole orders makes these the complete simple zero divisor. The shifted product S(w)S(w+ell/2) therefore has no poles and is constant.

A function with at most those two simple poles and that anti-period is a scalar multiple of S: matching one residue matches the second; the difference is a holomorphic constant and the anti-period kills that constant. This establishes the claimed antipedal trace formula without an unproved constant term.

## 5. Credited pedal argument and product

I separately checked the restated pedal calculation. Q has no pole at the common Jacobi poles: its numerator is order one and denominator order two, so it vanishes there. Only the zeros r=K+p of dn can give double poles. The exact symmetry Q(2r-z)=Q(z) makes Q even about r. The two area terms incident to that vertex combine into det(Q(r+z),Q(r+delta+z)-Q(r-delta+z))/2. The second factor is O(z), the first O(z^-2), leaving at most a simple pole. The neighbors are regular. The same reflection character gives the requisite anti-period and residue uniqueness, so T(u) is a scalar multiple of S(u+K).

The actual feet have midphase u=w+v. Since (v+K)/ell=tau+N/2 is a half-integer, the product of the two areas is a fixed scalar times S(w)S(w+ell/2). This proves constancy. The scalars are real by real-phase evaluation; they may be zero. The compact-torus argument is only used for0<k<1. The separate circle computation gives (N²R^4/4)sin²(theta), with finite antipedal radius R/cos(theta/2). No degenerate-torus limit is silently taken.

## 6. Even-period control and reproducibility

I reconstructed the two convex four-periodic orbits with a²=5,b²=3 and common caustic axes squared25/8,9/8. Their supporting lines satisfy the same caustic dual tangency equation. Reflection holds at the diamond's axes by symmetry; at a rectangle corner the ellipse-normal components are equal, bisecting the horizontal/vertical directions. Both are genuine primitive four-orbits. Direct homogeneous projections and intersections give products225/4 and289/4. All denominators are finite. This disproves an all-parity extension, not the odd source theorem.

Both unchanged author receipts replay byte-identically: **14,940 exact assertions** and **19,296 separate95-digit diagnostics**. Independent controls pass **15,698 exact assertions**, including240 rational polygons with unmasked named-line incidence,1510 odd lattice families, divisor coefficients and the exact four-orbit products. A separately authored direct-geometry diagnostic passes **1,820 checks** in14 primitive families at80 digits. Numerical observations are not interval certificates and do not replace the universal proof.

## Disposition

The full source-target proof passes after one author turn. Preserve the odd primitive/star scope, strict elliptical caustic, signed product/zero-area domain, explicit circular case, prior pedal credit and classical source citations. No mandatory author revision is required. Publication approval remains with the campaign owner.
