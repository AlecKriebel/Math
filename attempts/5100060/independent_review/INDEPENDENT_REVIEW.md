# Independent review of k817 / 5100060

**Verdict: PASS_COMPLETE_SOURCE_TARGET_AS_CREDITED_COROLLARY. No mandatory correction.**

This verdict binds PROOF.md SHA-256 `8bd1c99799212abe1b72d6b80f883702f0b9006697c8eb226f898a0b4cdb76d7` and author manifest `495d11d0d8b59d3d878a7b03c5126db9a4eaf96bd0862a2746daa7f6a47394d7`. All thirteen entries and four reading PDFs were verified. The reviewer did not author either inherited proof or contribute to this corollary. Prior independent review of k404 is disclosed below. Publication remains subject to the repository owner's gate. No novelty, minimality, or human-peer-review claim is certified.

## 1. Source and conclusion

The exact target is the arXiv-v11 Table 9 k817 product of the original polygon's unit focal-inverse area and its focal-antipedal area, with the same original focus and primitive period divisible by four. The published companion omits this row. The signed straight-edge polygon conventions, strict noncircular ellipse and strictly nested nondegenerate confocal elliptical caustic, coprime primitive winding and admissible stars are retained. SOURCE_AUDIT.md records the primary locators.

The source target follows completely from the two correctly matched statements `A V_F=C_F` and `B_F=kappa_F A`. Multiplication gives `V_F B_F=kappa_F C_F`, without dividing by either derived area. The subsequent 2-modulo-4 ratio theorem in the k404 input is not being imported: only its earlier general-even proportionality is used. Normalizing the caustic axes in that input scales both areas equally.

## 2. Independent audit of the entire inverse input

The copied PR207 proof has SHA-256 `d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8`. Its bytes were compared against the pinned public head `a7f8486548122c7d545430821afeedbccf48b3e7`; the Git blob is `d4968f8ddfe7a5f8393252e4473132612cd4224c`. The proof was re-audited mathematically, rather than accepted solely because it had an earlier review.

Stachel's canonical parametrization uses the caustic modulus, with `delta=2v=4K tau/N`, `N=2m`, and here m even, tau odd. The original signed area is `2 C_A S(w)`, where S is the m-term dn trace. The quotient lattice is `(ell,4iK')`, ell=2K/m. Its two simple pole classes have nonzero residues: at a representative pole only one half-trace summand contributes before the real quotient identification. Evenness and imaginary anti-periodicity force the two distinct half-real-period zeros. Pole/zero degree and compactness then prove the positive real half-shift product identity.

I reconstructed the actual focal-inverse edge formula from the endpoint coordinates and positive ordinary distances. In the input's notation, the focal distance product, focal determinant, squared-distance normalization, and antipodal rational formula all agree identically. The identity `U^2-k^2 V^2=k'^2 W^2>0` excludes real inversion poles. In particular, no squared signed distance or complex conjugation is substituted into the meromorphic continuation.

For V nonzero, the paired summand's full pole list consists of dn zeros at r=K+iK' and the shifted points r±delta, with their imaginary translates. At the dn zeros, `U^2-V^2=(U-V)(U+V)>0` for the real parameters. The other factor's zeros are exactly r±delta, by the Jacobi quarter-shift and addition identities; they are simple and distinct in this generic case. At common Jacobi poles the numerator has order at most four and denominator order five, hence no omitted pole exists.

Reflection around r changes the sign of the paired summand. Consequently the double Laurent coefficients at r+delta and r-delta are opposite. In the cyclic trace they meet the same pole class and cancel, with one of each contribution. A possible remaining simple pole is allowed. On the quotient torus only the two simple pole classes remain. Matching a residue to `S(u+K)` and using imaginary anti-periodicity removes the possible holomorphic additive constant.

The exceptional V=0 case is treated separately and correctly: cn(delta)=0 and 0<delta<2K imply delta=K, and primitivity forces N=4. The summand becomes a linear combination of dn and its reciprocal. With ell=K the two apparent real pole types coincide in the quotient; they remain simple, so the same residue-matching conclusion applies. No generic distinct-pole argument is used at this collision.

Finally `(K+v)/ell=(m+tau)/2` is a half-integer, giving the required original/inverse product. This argument includes primitive stars and does not replace least period by an arbitrary repeated indexing length.

## 3. Independent audit of the general-even antipedal input

The exact copied k404 proof has SHA-256 `b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462`. It is byte-identical to the separately fully reviewed candidate; that review is SHA-256 `a9340d01012ef6a26e09c99bdd7b26bbf375b2fe0437e0e24a7b46a87e5e4523`. That was an independent review by this reviewer, not authorship.

Its actual intersection formula solves both named lines `(P_i-F)·(X-P_i)=0`. The apparent focal factor is canceled by an exact numerator identity. Complex vertex poles are only the two shifted zeros of the remaining denominator; common Jacobi poles are removable. Thus the area has poles of order at most two in the vertex classes. Real reflection with traversal reversal, central symmetry for even primitive periods, and the imaginary reflection give an odd Laurent expansion at the relevant pole. This removes the double coefficient. On the full real-period quotient the dn trace has two contributing residues of the same sign; they add, rather than cancel. Residue matching and imaginary anti-periodicity prove `B_F=kappa_F A` for all primitive even N, allowing kappa_F=0. No focal-pedal denominator or later parity specialization is required here.

The independent k404 review also directly checked all focal intersections, real finiteness, and the canonical modulus convention. Its general-even lemma therefore supplies exactly the input used by this corollary.

## 4. Domain, orientation and zero cases

The original focal distances are bounded below by a-c>0. Consecutive antipedal normals could be dependent only on a chord through the focus; such a chord cannot be tangent to a strict elliptical caustic containing the focus in its interior. Every vertex of both derived polygons is finite. This is an existence statement for the constructions, not a nonzero-area assumption.

Central inversion maps one original focus to the other and cyclically permutes every primitive even orbit. It preserves planar signed area and both constructions, proving equality of the two focal constants. Reversing traversal negates both factors. Repeating an already admissible primitive orbit scales the product by the square of the repetition count, without creating a new primitive parity case. Changing inversion radius to rho scales its signed area and the product by rho^4. These statements agree with the actual geometric formulas.

The axial primitive four-orbit gives A=2ab, B_F=4ab and V_F=2/(ab), hence product 8. Direct exact focal inversion and both specific antipedal-line incidences were checked for rational 3-4-5 type parameter families. A possibly zero antipedal scalar causes no failure: the proof never divides by it. The theorem does not assert positivity of the product, and signed negative values in some larger-period families are consistent.

## 5. Reproducible controls and limitations

The author receipt replayed byte-for-byte: 2,004 exact controls and 45,821 separately labeled numerical diagnostics. Independent standard-library/SymPy exact controls passed 5,433 assertions covering the inverse identities, exceptional case, pole-index arithmetic, no-division corollary and named N=4 geometry. A separate direct-geometry mpmath diagnostic ran 3,822 assertions over fourteen primitive families at eighty digits, with maximum scaled residual `1.828351e-79`. It verifies both named antipedal lines and the actual unit inversion, not merely symmetry-invariant areas.

Numerical runs are finite unverified diagnostics. Exact finite pole-index enumeration is a consistency control, not a substitute for the all-index number-theoretic and meromorphic arguments above. The complete proof is the independently audited pair of inputs and the hypothesis-matched multiplication. The reading copies, PDFs and rendered pages are excluded from the portable review manifest.
