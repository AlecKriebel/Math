# Independent review: inner focal-inversion invariant k905 / 5100064

**PASS for the complete source target on its natural quotient domain. No mandatory correction.** The two signed areas are equal for every primitive even elliptical-caustic billiard; all inverted vertices are finite and distinct. The exact convex four-orbit genuinely has common zero signed area, so the raw quotient requires its stated nonzero-denominator condition. Historical novelty is not certified.

This review binds `PROOF.md` SHA-256 `687de80a403e43f06dfe3e8be34e41d49cafe2493f0ea75369918979739ea6ce` and `MANIFEST.json` SHA-256 `8c8de7f17e17bace6b2486b63cf029361b6fb1896e2f8d8082e3f6e731b84220`. All ten author files and four primary PDFs were hash-verified. Review date: 2026-10-01.

The reviewer is the separate author of the neighboring outer-antipedal k608 work. The two candidates were independently derived and frozen before exchange for review; neither author supplied the other's construction. They use the same openly credited classical central symmetry. This is not independence from that published mathematical input, and no new symmetry theorem is claimed.

## Source, object and period

The visually inspected [arXiv v11 Table 10, printed p12](https://arxiv.org/abs/2004.12497v11) has double-prime dagger areas in k905. Double primes refer to the inner caustic-contact polygon. The dagger denotes ordinary unit-circle inversion about the original foci. The candidate inverts vertices and then joins the images with straight edges; it does not integrate areas bounded by images of the original arcs. Its shoelace convention matches the source's signed-area definition.

The [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) omits the 900-series table. Its Table 9 is a differently organized table of inversive quantities, not an alternative k905 statement. The edition distinction and correction to the imported desk report are sound.

[Stachel's geometry paper](https://doi.org/10.1007/s00022-021-00606-2), Definition 4.1 and Corollary 4.2(i), and the [canonical motion paper](https://doi.org/10.1007/s40879-021-00524-2), Theorem 4.3, support the half-period pairing. With a primitive even period, the reduced turning number is odd, so the half-orbit canonical shift is an odd multiple of 2K. This negates both coordinates. The source's separate hyperbolic-caustic symmetry cases are not imported.

## Contact points and regularity

A tangent to a strict ellipse has a unique contact. Central inversion sends an orbit chord to the half-period-shifted chord and therefore sends its contact to the opposite contact. In canonical coordinates the contacts have the same primitive step, shifted by half a step relative to vertices. The real parametrization is one-to-one modulo 4K, so all N contacts are distinct. This canonical argument establishes distinctness without assuming that arbitrary unordered tangent lines distinguish an oriented orbit.

The original and caustic foci coincide. For a caustic with semiaxes alpha>beta>0, the focal distance satisfies `c²=alpha²-beta²<alpha²`; both foci are strictly interior. Thus no contact equals an inversion center, and all squared-distance denominators are positive. Ordinary inversion is injective away from its center, proving the stated finite distinct image vertices. Nonzero polygon area does not follow from this regularity and is not assumed.

The elementary identity `I_(-F)(-X)=-I_F(X)` is correct including the translation back by the focus. Combining it with contact pairing gives a cyclic shift of the negated vertex list. A planar central inversion has determinant +1 and does not reverse the index list, so the signed areas agree. This argument is valid for primitive stars and for reverse traversal. Repeated even primitive orbits multiply both areas by the same repetition number; the theorem does not obtain an even-period hypothesis by repeating an odd primitive orbit.

## Exact four-orbit certificate

The four points on `x²/2+y²=1` are a convex diamond in proper traversal order. All chord lengths are sqrt(3). At every axis vertex, the difference of incoming and outgoing unit velocities is a positive multiple of the outward normal; the checker tests all four rather than relying on an axis swap that would not preserve a noncircular ellipse. The orbit has four distinct vertices and least period four.

Subtracting lambda=2/3 from the two squared semiaxes yields the strict confocal caustic with axes squared 4/3 and 1/3. The stated contacts `(±2sqrt(2)/3,±1/3)` are on their actual corresponding chord segments, on the caustic, and have tangent direction equal to that chord direction. The direct segment parameters lie strictly between zero and one. The universal contact construction has therefore not been replaced by arbitrary symmetric points.

Every contact has squared norm one and is different from either `(±1,0)`. Direct inversion about `(1,0)` gives x=1/2 and the four listed distinct finite y-values; the other focus gives x=-1/2. Joining those images in the inherited order gives zero shoelace area. The original orbit and caustic remain strict, and all inversion denominators remain positive. This is a genuine raw 0/0 case, not a failed inversion or an unsigned-area assertion.

## Optional axis-family formula

The general axis four-orbit has caustic parameter `a²b²/(a²+b²)`, giving contact rectangle half-sides `u=a³/(a²+b²)` and `v=b³/(a²+b²)`. All four line and conic tangency conditions check directly.

For a rectangle about the origin inverted about `(c,0)`, its two image vertical lines are separated by

`2u(r²-c²)/D`, where `D=(r²+c²)²-4c²u²`,

and the sum of their positive-coordinate half-heights is `2v(r²+c²)/D`. Their product is exactly the signed shoelace area, including a possible negative sign in the width. Moreover

`D=((u-c)²+v²)((u+c)²+v²)>0`

because v>0. This independently derives the first expression in equation (13), with its squared denominator and factor 4. Reducing with `c²=a²-b²` gives the candidate's second expression. Since `2a²-b²>0` in the strict a>b range, its unique zero within this axis-orbit subclass is `a²=2b²`. The candidate correctly refrains from treating this as a formula for every phase of the fixed four-period family.

## Domain and verification

The raw real quotient is 1 wherever its denominator is nonzero, and is undefined at common zeros. A constant extension is an additional convention. No nonempty defined locus for every exceptional fixed family is required, and none is claimed. The example changes no conclusion about a defined ratio varying over a family.

Independent controls passed **12,491 exact assertions**, including symbolic inversion equivariance, direct named-chord contact incidence, the full signed rectangle formula, the physical four-orbit reflection and contact checks, and exact collinearity/zero-area tests. These finite controls supplement the universal proof rather than establish it by sampling.

The author's **33,540 exact assertions** and separate **15,666 80-digit diagnostic checks** were replayed in a separate copy; the complete receipt is byte-identical. All ten frozen artifacts and four source PDFs matched their pinned hashes. The portable review packet excludes source PDFs and page renders.

The proof, optional subclass formula, source qualification, and common-zero certificate pass unchanged. Preserve classical credit, primitive elliptical-caustic scope, signed straight-edge area, original-focus inversion and the quotient-domain qualification in publication.
