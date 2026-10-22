# Independent adversarial review: k906 / 5100065

## Verdict

**PASS_COMPLETE_DOMAIN_QUALIFIED_SOURCE_TARGET.** No mandatory correction was found in the exact frozen PROOF.md, SHA256 `d3dcff2851bc315e4c5605797fa830a966cb3b36e215ad8e160cd5f3c65ab242`, bound by FROZEN_MANIFEST.json SHA256 `11dbf3fe914962e2d28aacace8cee71f699f57d77b9626f56ea2957d606af80d`.

The proof establishes equality of the two signed inverse areas for primitive even periods with strictly nested nondegenerate confocal elliptical caustics. The ratio is one wherever its denominator is nonzero. It is everywhere defined for winding one. The exact primitive 8/3-star family proves that an everywhere-defined ratio cannot be extended to all stars: both areas vanish at an intermediate phase while all vertices and inversions remain finite.

This equality-versus-quotient distinction is part of the mathematical conclusion, not an optional disclaimer. Retain it in any claim or queue summary. No hyperbolic/collapsed caustic or even repetition of an odd orbit is certified. The reviewer did not contribute to the author proof and changed no frozen author file. No novelty or priority is certified.

## 1. Exact source object

The arXiv v11 source is *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, dated 29 October 2020. Section 2 defines signed shoelace area. Section 3.9 defines the outer vertices' inversion about the foci of their own ellipse locus. Table 10, printed p.12, lists k906 as the ratio of those two areas, value one, for even N. I checked the text and visually inspected that table. The own outer-locus foci must not be replaced by the original billiard foci from k904; the inverted vertices are also not the original vertices from k903.

The final *Fifty New Invariants* companion has no 900-series table or substitute k906 row. Its later Table 10 concerns videos, not the arXiv invariant table. The packet correctly uses the explicit arXiv target without pretending it survived unchanged in the published table.

The primary Stachel input is *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), 1602–1622, DOI 10.1007/s40879-021-00524-2. I checked Theorem 4.3 and equation (4.9), including a visual check of printed p.1614. The modulus is the caustic's eccentricity; software parameters are its square. The theorem includes the primitive turning number, not merely winding one. Standard half-period and addition identities were also checked against DLMF Sections 22.4 and 22.8.

All 12 author artifacts and all three primary PDF hashes match the supplied manifests. Full PDFs/text and rendered pages are reading material only; none belongs in the portable review packet.

## 2. Actual outer polygon and finite inversion

The tangent-intersection derivation is correct. Substitution of the proposed Q(u) into both original-ellipse tangent equations works under the Jacobi addition identities. The tangent determinant in equation (4) is positive for real u, because v is strictly between zero and K, dn(u)>0 and the remaining denominator is positive. There is no hidden parallel-tangent or infinite-vertex phase in the stated class.

The axes A,B need not have the same ordering as a,b. The proof correctly allows the outer major axis to be vertical and allows A=B. The own foci are strictly inside this nondegenerate outer ellipse, so no real outer vertex equals an inversion center. Coincident foci for the circular outer locus cause no division-by-distance singularity.

I independently constructed the two exact star polygons by solving pairs of tangent equations at the actual original billiard points. Fitting their axes recovers A=221/96 and B=1105/144, then gives the own vertical focal coordinate 221*sqrt(91)/288. This is independent of feeding the candidate's outer-vertex formula directly into shoelace evaluation.

## 3. Half-turn symmetry and signed area

For even least period N with coprime tau,N, tau is odd. The half-cycle shift is therefore an odd multiple of 2K, and both original and outer vertices change sign. Unit inversion satisfies I_(-f)(-Q)=−I_f(Q). Hence one inverse polygon is the central reflection of the other after a cyclic shift of its vertex order.

Central reflection has determinant +1 in the plane. It preserves signed shoelace area, as does a cyclic shift; it does not reverse the polygon indexing. The equality proof is therefore valid for stars and self-intersections and never divides by an area. Orientation reversal changes both area signs together.

This symmetry does not imply that either area is individually constant or nonzero. The author does not make either inference. The source already credits the same mechanism for neighboring even-period rows, and the outer-locus calculation from earlier campaign work is acknowledged rather than represented as a new discovery.

## 4. Winding-one nonvanishing

I independently expanded both focal-axis identities. With t=sn²(v), q=1−t and V=1−2t+k²t², equation (7) correctly expresses A²−B². When delta=2v<=K, cn(delta)>=0 and V>=0, so the outer foci lie on the horizontal axis or coincide. Equation (8) then shows c_o²<a² strictly. Consequently each focus is in the interior of the original billiard ellipse.

The eccentric angle increases strictly with u. Since delta<2K, every consecutive outer pair has an angular increment strictly between zero and pi, giving a positive determinant about the center. Its joining line is the actual common original-ellipse tangent. A point inside that ellipse lies on the same strict side of the line as its center, so translating the determinant center to either own focus preserves its positive sign.

Every inversion-edge cross product is that positive determinant divided by two positive squared distances. Their sum is positive, including the circular outer-locus case. This proves the nonzero denominator for winding one, and the slightly larger stated class tau/N<=1/4. It does not extend the positivity argument to stars whose outer foci can lie outside the original ellipse.

## 5. Exact star zero and domain failure

The quarter-period data satisfy the real branch conditions. Starting with sn²(h)=96/221 and positive cn(h),dn(h), the first doubling gives the positive real K/2 values. The second doubling gives sn=1, cn=0 and dn=25/144. Since the starting point is in (0,K), the positive intermediate cn fixes the branch and identifies h=K/4, not a different complex or real period representative. The K−h identities give the displayed 3h values.

The resulting billiard axes are strictly outside the caustic and have the same focal difference. With delta=3K/2 and gcd(8,3)=1 the least period is exactly eight. The tabulated phase sequences agree with arithmetic modulo 4K. This is one fixed confocal ellipse pair with varying starting phase, not a comparison between two different billiards.

Using the independently solved tangent intersections and fitted own foci, I obtain exactly

    B_+(0)=1473536/30525625,
    B_+(K/4)=−51985629184*sqrt(30)/12455533443925.

The minus-focus areas give the same two values. The signs are exact. Since every vertex remains on the same nondegenerate outer ellipse and its foci are strictly interior, inversion stays finite over the whole phase interval. The signed area is continuous; the intermediate value theorem therefore gives a genuine simultaneous zero of both areas. The quotient is undefined there. No degenerating caustic, touching inversion center or repeated odd polygon is involved.

This validates the author's qualified ratio statement and its obstruction to the broader everywhere-defined interpretation. The full even-star signed equality remains valid at the zero phase.

## 6. Replays and independent controls

The inspected author program reproduces its output byte-for-byte: 47 exact assertions and 440 floating-point cases. These are diagnostics supporting the written proof, not a substitute for it.

The fresh checker passes 129 exact assertions, including the double-angle branch data, direct original-tangent incidence, fitted outer axes and own foci, finite inversion at the two exact phases, both exact area signs and the focal-location identities. Its 80-digit physical-billiard implementation uses tangent-to-caustic initial directions, intersections with the original ellipse and the Euclidean reflection law, rather than repeated Jacobi evaluation of polygon vertices. Across 99 cases it passes 3,222 diagnostic checks, with maximum normalized residual about 1.44e−78; 54 winding-one cases have both areas positive. These numerical controls do not certify all periods or the intermediate zero on their own.

The frozen packet is suitable for a domain-qualified claimed-result draft after the coordinator's publication gate. Preserve the distinction between an everywhere finite inversion, a signed-area equality, and a quotient defined only where its denominator is nonzero. The original source, prior symmetry mechanism and Stachel input must remain credited.
