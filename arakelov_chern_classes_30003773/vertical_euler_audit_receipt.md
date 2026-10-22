# Independent acceptance receipt: supported Euler construction

Date: 21 October 2026.
Audited file: vertical_euler_classes.md.
Audited byte count: 8513.
Audited SHA-256: 92d71e5db90e2b71b4d4d509ab73769840b564e71b84cd8a6089c0220f3770b1.

**Verdict: ACCEPTED as conditional partial mathematics, not a solution of the original problem.** The standard imports and the schematic regulator setup remain explicit hypotheses. The K-theory detector below does not require a mixed-characteristic MGL-to-motivic-cohomology comparison.

## 1. Geometric and support arguments

The rank-r section construction, its zero-section homotopy after forgetting support, contravariant naturality for maps of pairs, compatibility with support enlargement, and invariance under bundle isomorphisms all pass. GL-oriented Thom classes are invariant under bundle automorphisms, so multiplying a line-bundle section by an invertible global function preserves the supported class. This would require different care for an SL-only orientation; MGL is GL-oriented here.

The homotopy criterion in §3 is sufficient: a family of sections with all zeroes in W times A1 defines a map from (X/(X minus W)) smash A1_+ to Th(V), hence equal endpoint pullbacks. Unrestricted interpolation need not satisfy this criterion. Equality of globally forgotten MGL classes does not identify their supported MGL classes or their globally forgotten A classes. The difference statement as an element of the image of B^{2r-1,r}, equivalently the indicated cokernel subgroup, follows exactly from the fibre long exact sequence.

The principal-divisor example correctly separates three groups: supported MGL, supported A, and globally forgotten A. The supported comparison is an isomorphism; forgetting support is not asserted injective. Thus supported nonvanishing does not prove global A nonvanishing or a logarithmic formula.

## 2. Mixed-characteristic K-theory detector

The example uses S=Spec(Z), which is regular, noetherian, separated, and finite-dimensional. It is within the base hypotheses of the standard motivic K-theory representation and orientation, not merely a field case.

Fix the usual K-theory orientation and Bott identification KGL_Z^{2,1}(S) with K_0^Z(S) so that the first Chern class corresponds to 1-[L^dual]. This explicit normalization makes the sign in the length computation unambiguous. A different Bott sign convention changes an intermediate sign, not nonvanishing.

The relevant represented target is the Grothendieck group of perfect complexes on Spec(Z) acyclic on Spec(Z[1/p]), not ordinary K_0(Z) and not a group of vector bundles supported at p. The latter distinction matters: a nonzero vector bundle cannot itself have this support, but a perfect complex can.

The usual Thom class for the trivial line is represented in this supported K-theory by the Koszul complex of its fibre coordinate. This can also be checked from the standard Thom construction: on the projective compactification P(O plus O), the prescribed class is the first Chern class of O(1), hence 1-[O(-1)]; the complex O(-1) -> O of the coordinate section represents precisely this class and is acyclic off its zero section. The injective support-extension map in the standard Thom construction identifies it with the supported Thom class. Restricting to A1 and pulling back the coordinate along the section p gives the complex below.

Put the complex Z --p--> Z in cohomological degrees -1 and 0. Its cohomology is H^0=Z/p and zero otherwise. For a perfect complex C supported at p, every H^i(C) has finite length over Z_(p), and

    chi_p(C) = sum_i (-1)^i length_(Z_(p))(H^i(C))

is invariant under quasi-isomorphism and additive in distinguished triangles, by the finite long exact sequence in cohomology and additivity of module length. It therefore induces a homomorphism K_0^{(p)}(Z) -> Z. For the displayed Koszul complex chi_p=1. This proves its supported K-class is nonzero. Consequently the corresponding supported MGL class is nonzero, and its unique supported A lift is nonzero.

After forgetting support the K-class is [Z]-[Z]=0. Independently, the globally forgotten MGL class is c_1(O)=0 by the oriented theory axioms. The zero K-image alone would not prove the latter MGL assertion; the text correctly supplies the stronger independent argument. Nothing determines the globally forgotten A class.

## 3. Primary-source verification and conventions

The following primary mathematical sources were inspected through their public PDFs on 21 October 2026:

- Panin, Pimenov and Röndigs, *On Voevodsky's algebraic K-theory spectrum BGL*, https://www.math.uni-bielefeld.de/lag/man/251.pdf. Corollary 1.2.7 identifies cohomology of quotients with Thomason–Trobaugh K-theory with support, including the bigraded formula. Section 2.6, especially Example 2.6.5, fixes an orientation and explains the normalization to the usual K-theoretic Chern class. Section 2.7, formulas (25)–(26), constructs Thom classes with an injective support-extension map.
- Naumann, Spitzweck and Østvær, *Chern classes, K-theory and Landweber exactness over nonregular base schemes*, https://epub.uni-regensburg.de/13773/1/MP38.pdf. Theorem 3.1 states the oriented universality of MGL over finite-dimensional noetherian bases. Thus the required orientation-preserving map to KGL is available over Spec(Z).

The older preprint's BGL notation is the algebraic K-theory motivic spectrum used here as KGL. Its Bott convention is not to be silently copied into a different convention: the explicit normalized identification above is what yields positive length one.

A separate attempted publisher PDF fetch for the original universality paper returned HTTP 403; it was not used as successfully inspected evidence. The accessible general-base universality source suffices. No full source text has been copied into this receipt.

## 4. Remaining limits

The motivic-integral-cohomology detector in §4 remains explicitly an imported comparison/divisor statement; it is unnecessary for the accepted K-theory nonvanishing proof. The audit does not upgrade that optional detector to a newly proved mixed-characteristic comparison. The specialization paragraph correctly avoids claiming arbitrary absolute purity or a generic-to-special specialization operation. The original arithmetic regulator and intended global geometric Chern interpretation remain unresolved.
