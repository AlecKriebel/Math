# Independent scope and partial-construction audit

Target: queue row 1832, catalogue 30003773, OWR-16158-016.
Date: 21 October 2026.
Outcome: **PARTIAL RESULTS ACCEPTED CONDITIONALLY; ORIGINAL QUESTION NOT SOLVED.**

This audit checks `partial_results.md` against the recovered primary text and checks its mathematical arguments independently. It does not identify Rodriguez's theory or the complex-manifold geometric theory with the arithmetic fibre.

## Source/convention check

The original OWR paragraph on printed p.1075 specifies a natural map of spectra from the motivic Thom spectrum to a pushforward of Hodge-filtered cobordism and defines the arithmetic theory by its homotopy fibre. It does not specify a coherent multiplicative enhancement. The Paris 2016 slides specify the schematic target eta_*(MU_D). Thus the fibre triangle is legitimate as the adopted setup, but its E-module enhancement must remain an assumption until supplied by an actual construction. The report is the 2018 workshop / 2019 publication, not a 2016 report; only the Paris slides are from 2016.

The original question does not demand a unital orientation on the fibre or universal fibre-valued lifts of ordinary Chern classes. Proving these demands impossible is not a counterexample to the question. Operations on a module are categorically different from classes obtained by applying those operations to a unit.

Hopkins–Quick, *Hodge filtered complex bordism*, local extracted §7, supplies target-side Chern compatibility (Proposition 7.8), a motivic-spectrum structure over C (Proposition 7.9), and projective transfers in §7.2. In particular the displayed smooth-divisor relation is i_*(1)=c_1(O_X(D)). These statements concern the target over complex varieties. They do not, merely by their existence, verify the arithmetic fibre enhancement, all base-change conventions, or an arithmetic geometric cycle equivalence.

## Formal audit of the five avenues

1. **Lifts and ambiguity: accepted.** For x in E^{p,q}(T), exactness gives existence exactly when r(x)=0. The set of lifts in the abelian group A^{p,q}(T), when nonempty, is a torsor for coker(E^{p-1,q}(T) -> B^{p-1,q}(T)). This is a statement about homotopy classes, not a claim that the higher space of choices is discrete. The P^1 example is valid under the stated orientation-compatible realization. If r is unital and 1_B is nonzero, the unit cannot lift. The result excludes a unit-preserving map A -> E, not every conceivable unital algebra structure on the underlying spectrum A.

2. **Module Chern operations: accepted under the enhancement hypothesis.** In a stable category of E-modules, the fibre of an E-linear map carries its inherited E-action. The diagonal on X supplies the cup action E^{*,*}(X) on A^{*,*}(X). Multiplication by the ordinary E-Chern classes then gives the claimed operations and Whitney/naturality identities. Formal-group-law expressions must be evaluated only under the indicated finiteness/nilpotence or convergence hypotheses. This is not yet a geometric interpretation of the fibre theory.

3. **Relative cocycles: accepted with the stated limitation.** The mapping-space homotopy-fibre statement is intrinsic. The displayed cochain differential squares to zero, and multiplication by a compatible closed even-degree element commutes with it. Such a chain-complex model is conditional; arbitrary integral MGL/MU spectra cannot be replaced by ordinary complexes without additional structure or loss of information.

4. **Green currents: accepted as a diagnostic, not a comparison theorem.** On a compact complex curve, evaluating d h against the constant test function gives zero. A point current has nonzero integral. Subtracting a normalized curvature form removes that obstruction but does not give a nullhomotopy of the Hodge-filtered class. Neither a metric nor a target-side current representative automatically supplies the nullhomotopy required by the arithmetic fibre.

5. **Vertical support: accepted integrally under the displayed adjunction.** Let T be the derived pointed cofiber of (X minus Z)_+ -> X_+. With Z having empty generic fibre, j^*T=0 because the derived pullback preserves cofibers and the pulled-back open immersion is an isomorphism. For the derived right adjoint j_*, the mapping spectrum from T to j_*D is contractible by adjunction. Equivalently all groups [T,Sigma^{p,q}j_*D] vanish, using the ordinary twist compatibility of j^*. Applying [T,-] to the fibre triangle gives the canonical supported isomorphism A_Z^{p,q}(X) -> E_Z^{p,q}(X) in all bidegrees.

There is no proper-base-change step, no rationalization, and no assertion that Z is smooth in this argument. It only needs the actual adjunction and the assumed factorization B=j_*D. It applies to quotient-defined support, so does not smuggle in an unproved localization identification for another arithmetic theory. It remains conditional on this being the pushforward model of the source's schematic construction. A generic point need not be an open immersion; openness was not used. If the base is reducible, one must first specify the generic-point convention rather than silently reuse a single j.

## Additional rigorous partial construction: sections with vertical zero locus

Assume the standard oriented MGL Thom class for vector bundles on smooth S-schemes. Let L be a line bundle on smooth X/S, and let s be an algebraic section with zero locus Z whose generic fibre is empty. The section defines a map of pairs

    (X, X minus Z) -> (L, L minus zero section),

and therefore a pointed motivic map

    s_bar: X/(X minus Z) -> Th(L).

If th_E(L) is the oriented Thom class in reduced E^{2,1}(Th(L)), define

    e_Z^E(L,s) = s_bar^* th_E(L) in E_Z^{2,1}(X).

The supported isomorphism from Avenue 5 gives a unique class e_Z^A(L,s) in A_Z^{2,1}(X) mapping to it. Forgetting support produces a class in A^{2,1}(X) whose E-image is c_1^E(L). Indeed, after forgetting support, the section s and the zero section are A1-homotopic via t*s in the total space of L. Pulling back the Thom class along the zero section gives the Euler class, which is c_1^E(L) by the chosen oriented convention.

This proves a precise geometric partial result for a line bundle supplied with a section that is nowhere zero on the generic fibre. It does not require a fundamental class or purity theorem for the possibly singular zero locus Z. The class is attached to the displayed section/support data; independence from arbitrary changes of section or support is not asserted. In particular it does not imply a canonical fibre lift for every line bundle whose generic restriction is trivial, or for every horizontal divisor.

The same construction gives the top Chern/Euler class c_r^E(V) for a rank-r vector bundle V with section whose zero locus is vertical: use its Thom class in degree (2r,r). Its underlying class is the top Chern class by the usual oriented Euler convention. Arbitrary lower Chern classes and a global arithmetic cycle presentation do not follow.

## Acceptance boundary

These formal results and section constructions are mathematically valid in their stated setup. They are useful partial progress, not a proof that the original open problem is solved, and not a proof that it is false. A complete answer still requires a precisely defined arithmetic regulator model and a geometric cycle/nullhomotopy comparison compatible with the intended Chern operations. Current-literature openness is not established by the absence of a solution in the inspected material.

Source locations inspected: recovered OWR text lines 2465–2495; Paris slide text lines 1500–1526; Hopkins–Quick text lines 1780–1855. Public provenance and verified URLs remain in the recovery source gate; no third-party source text is reproduced here.
