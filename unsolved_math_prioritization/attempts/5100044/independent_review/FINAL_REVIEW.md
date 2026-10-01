# Independent review: 5100044 / arXiv k804,a

Date: 2026-10-01. Verdict: **PASS for the complete original area-product target**.

Reviewed frozen `PROOF.md` SHA-256:

    d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8

The proof establishes constancy of signed orbit area times signed focal-inverse polygon area for every primitive period divisible by four in the source's nested confocal-ellipse setting, including primitive stars. It treats N=4 separately where the generic pole argument changes. No revision is required. No novelty, priority, hyperbolic-caustic extension, or claim about a different published k804 label is certified.

## 1. Exact source and edition audit

I independently read and visually checked all three source tables:

- arXiv2004.12497v11, Table 9 printed p.11: k804,a is A A_j^dagger for N=0 mod4; the adjacent k804,b gives the N=4 value4.
- The published *Fifty New Invariants*, Table 9 printed p.350: k804 is a cosine-sum assertion, not this area product. The candidate correctly rejects the imported report's implied unchanged label.
- Garcia–Reznik, *Exploring self-intersected N-periodics*, Table 1 printed p.7: the same product is k805,a, with low-N derivations4,4i,8 listed and no general proof cited in that column. Proposition 4.9 gives the simple N=4 value4. The package credits the N=4 and listed N=8 work rather than treating those cases as new.

The original inverse vertices use unit-radius circles about the original foci. The area is the signed shoelace area of straight segments joining the inverted vertices, not the area bounded by circular images of complete orbit edges. The source's confocal ellipse pair and primitive-period convention are retained. The later paper's broader discussion of hyperbolic caustics is not silently imported.

Stachel's published canonical theorem and its caustic-eccentricity modulus were checked independently during this review series. The needed Jacobi shifts were checked directly in DLMF22.4, including sn(z+K+iK')=dn(z)/(k cn(z)). Addition formulas are supplied by DLMF22.8.

## 2. Independent real-algebra reconstruction

The canonical coordinates and step satisfy the confocal relation and the least-period/turning-number condition. For N=4n, the half-orbit displacement is 2K times an odd integer, so the half orbit is genuinely antipodal.

The orbit-area identity has the correct factor2 relative to the m=N/2 term cyclic sum. The coefficient is positive, and the argument uses signed cross products, so it remains valid for primitive stars.

The focal distance is a+c sn(w), whose strict lower bound a−c>0 fixes its real sign. I reconstructed the focal distance product and shifted cross-product directly from the addition formulas. Expanding the distance-product numerator gives

    U + k(U+V)s + k²Vs² = (1+ks)(U+kVs).

The translated cross-product gives the factor 1+ks with the sign stated by the author. Dividing by the two squared distances yields equation(10) with the stated normalization. Antipodal fraction addition gives equation(14); the dn in its denominator comes from the factor 1−k²sn²u=dn²u. Thus the formula is a meromorphic continuation of ordinary real inversion, with no conjugation or missing power of distance.

The identities U−V>0, U+V>0 and U²−k²V²>0 hold on the real parameter range. None of the original real inversions is singular.

## 3. Complete generic pole audit

Let p=iK' and r=K+iK'. For V≠0:

1. At r and its imaginary translate, dn has a simple zero. The other denominator becomes U²−V²=(U−V)(U+V)>0. These poles have order at most one.
2. The other denominator factor is a constant times dn²δ−k²cn²δ sn²u. On the sn² torus it has one double pole. Its zeros at r±δ are supplied by the checked quarter-period identity. They are distinct unless δ=K; that is exactly V=0. They do not coincide with p or r. Degree counting makes both zeros simple.
3. Squaring that factor creates poles of order at most two at r±δ and their imaginary translates. Any numerator cancellation only reduces their order.
4. At the common Jacobi poles p, the numerator has order at worst four and the denominator order five, so B is removable there and vanishes. The above list is exhaustive on the compact torus.

The reflection B(2r−u)=−B(u) follows from the parity of sn about r and the odd reflection of dn there. Reflecting a local Laurent series changes the sign of its quadratic principal coefficient and preserves its simple-pole coefficient. Since r+δ and r−δ lie in the same cyclic δ orbit, exactly one translated contribution of each type occurs at each corresponding sum pole. Their quadratic coefficients cancel. Real-period translations introduce no additional sign. The imaginary anti-period applies to both coefficients and preserves cancellation there as well.

The surviving r-family is only simple. Thus the cyclic sum has at most two simple poles on the reduced torus. This is a cancellation in the sum, not an unjustified claim about individual summands.

## 4. The exceptional case is correctly isolated

V=0 is equivalent to cnδ=0, hence δ=K for 0<δ<2K. Primitivity forces N=4 and turning number1. The separately simplified formula is a linear combination of dn and 1/dn, with only simple poles. Since the reduced real period is K, their p and r pole classes agree. The same two-pole conclusion therefore holds without applying the invalid generic degree/order argument in this case.

The axial N=4 shoelace computation independently gives A=2ab and inverse area2/(ab), hence product4. This agrees with the credited published result. Repetition of a shorter excluded primitive orbit is not used to manufacture an admissible N.

## 5. Residue matching and final half-period product

Both the inverse-area cyclic sum R and S(u+K) have real period ell and imaginary anti-period2iK'. The latter has two simple poles with nonzero residues. Matching one residue and using the anti-period matches the other. Their difference is holomorphic on the compact torus, hence constant, and its anti-period forces zero. No division by a potentially vanishing inverse area or proportionality constant is required.

For the cyclic dn sum itself, the pole residues cannot cancel: contributions at a fixed imaginary pole differ only by real periods. Evenness and the anti-period force exactly two half-real-period zeros, exhausting the degree-two zero divisor. Therefore S(w)S(w+ell/2) is constant.

The final shift satisfies (K+v)/ell=(m+tau)/2, a half-integer because m is even and tau odd. This completes the product identity. The other focus is handled by a cyclic antipodal shift followed by a central reflection, which preserves signed area. Reversal changes the signs of both areas and leaves their product unchanged.

## 6. Reproducibility and independent controls

All 11 files in the frozen manifest were hash-verified. The author checker was inspected and rerun in a copied review directory, avoiding changes to frozen inputs. Its output matches the supplied JSON byte-for-byte: 25,098 exact assertions over 4,181 primitive rotations, plus 1,494 separate 80-digit diagnostics.

My independently authored checker imports no author modules. It passes 5,900 exact integer/lattice assertions over 1,475 primitive rotations and 318 high-precision diagnostics at 110 digits. The numerical part uses actual Euclidean inversion of vertices for both foci and signed shoelace areas. Its complex checks likewise form inversions directly rather than importing the author's edge formula. They test opposite double principal parts, simple summed poles, and proportionality at nonreal phases. Six excluded-parity examples have nonconstant products. The largest scaled discrepancy is about 9.97e−18 from a finite-distance double-principal-part comparison; the tests have explicitly different tolerances for these asymptotic diagnostics.

These finite exact controls and non-certified numerical diagnostics support the written analytic proof; they are not substitutes for it.

## 7. Disposition

**Full mathematical and source-scope PASS.** Retain the edition map, primitive elliptical-caustic domain, signed straight-edge area, separate N=4 calculation, and credit for prior low-period work. No mathematical correction is required to the frozen proof.

The author reuses a cyclic-sum organization from k203,b but proves the necessary facts in this candidate. I did not coauthor either argument; the focal-inversion algebra and pole cancellation were checked independently here. Publication remains under the parent gate. This review makes no historical-first or exhaustive-literature claim.
