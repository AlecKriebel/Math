# Independent acceptance: exact local theta-symbol residue test

Date: 14 October 2026 UTC. Shared PASS 3/5; row 1777 / 30005572. This is independent verification, not an additional mathematical pass.

## Verdict and input versions

ACCEPT the exact local calculation for the specified rational function theta5=Delta^2/psi5, its legitimate R-coefficient normalization, and the restricted graph-potential result. The first reviewed input was `pass3_actual_residues/EXACT_THETA_RESIDUE_TEST.md`, SHA-256 `8e9aee84bdec01f3a7209cf36a0703257cb2dc799860274bf458b3b03eb5d240`.

The source identification of theta5 with Robert/Kato's normalization is accepted up to a twelfth root of unity, which is sufficient for the R=Z[1/6] symbol and, in this example, the exact tame-symbol calculation. The precisely fixed rational function has no normalization ambiguity. The paired clarification `NORMALIZATION_SOURCE_ADDENDUM.md`, SHA-256 `1c1882ad7fafcc70260b5de861c7b17534e8f447640e13468a7fd10b107800b7`, was also inspected and is accepted. It explicitly retains the mu12 qualification and leaves the fixed-function claims unchanged.

No value of the actual LSSW geometric cocycle has been computed in this report. No nonzero absolute residue, global relative map, or obstruction to the full construction is established. The original problem remains UNSOLVED.

## 1. Explicit function and source normalization

The standard division-polynomial recurrence independently confirms that psi5 has degree 12 in x, leading coefficient 5, and Weierstrass weight 24. Thus Delta^2/psi5 is coordinate-invariant, has divisor 25(0)-E[5], is even, and has formal expansion (Delta^2/5)T^24 times an integral unit series with constant term 1 at residue characteristic two.

Chida's accessible preprint, Section 5, pp.6–7, gives Robert's lattice-product normalization and its Kato comparison. Taking the lattice pair L subset L/5 in that product shows that the normalized function is epsilon Delta^2/psi5 with epsilon in mu12: the discriminant contribution is Delta^2/5 and the product denominator is psi5/5. This checks the constant up to the source's explicitly controlled root of unity, rather than inferring it from a divisor alone.

The chosen analytic theta quotient in the draft also has the asserted leading coefficient: the theta leading scalar has twelfth power Delta, so its 25-versus-5 quotient leads with Delta^2/5. This proves the displayed formula for that chosen prescription. Without separately resolving Robert's root-of-unity convention, an exact equality to every named normalization should not be inferred. This is immaterial in K_2 tensor R, because all symbols involving mu12 vanish there. In the local example below it is also immaterial to the exact raw tame symbol: both values receive the same epsilon and their downstairs valuation difference is 12, so the residue multiplier is epsilon^12=1.

## 2. The local CM field and formal group

The Hilbert polynomial in the draft was independently verified against the official Sage/Kohel documentation. Its reduction is J^3+J+1, irreducible over F2. Thus every chosen CM reduction has j-bar in F8 minus F2, necessarily of order seven. The residue field of K may be larger; the argument does not replace it by F2 or assume all Weierstrass coefficients lie in F8.

With w^2-w+6=0 and q=(2,w), one has v_q(w)=1 and O_F/q^2 is Z/4, with w mapping to 2. The chosen q-adic CM type has connected ordinary q-primary torsion. The coefficient check is valid: [w][1-w]=[6], the latter factor has unit tangent action modulo q, and the formal doubling coefficient is -a1. Therefore the coefficient of T^2 in [w](T) reduces to a1-bar, which is nonzero because j-bar is ordinary.

The Newton polygon gives valuation 1 to the one nonzero formal q-point. For a primitive q^2-point P, the equation [w]P=R then gives v_0(T(P))=1/2 and T(wP)/T(P)^2 reducing to a1-bar. Higher integral terms have strictly larger valuation, so there is no cancellation assumption hidden in this comparison.

Since all O_F endomorphisms are K-defined, the Galois orbit of a generator of O_F/q^2 has size at most two. Its half-integral parameter valuation forces a ramified extension of degree two. Therefore K(P)/K is totally ramified quadratic, with no residue extension, and the nontrivial automorphism sends P to -P. Evenness proves that the two theta values A,B descend to K, while P itself need not do so.

This is distinct from the q^2 ray field: its local ray-unit quotient is trivial because the two units modulo q^2 are supplied by ±1, so F(q^2) is the Hilbert class field. The draft correctly does not identify the marked-point field of the good-reduction model with that ray field.

## 3. Exact residue calculation and ramification descent

Upstairs the two theta valuations are 24 and 48. In the stated tame-symbol convention their sign is positive and their unit parts give

Delta-bar^48 a1-bar^(-576) = j-bar^(-48) = j-bar.

This identity uses c4-bar=a1-bar^4 in characteristic two; it does not require a1-bar itself to lie in F8.

The restriction formula for tame symbols raises the base residue to the ramification index 2. Squaring is an automorphism of the multiplicative group of a finite characteristic-two residue field, so the unique base residue is j-bar^4. Equivalently one can compute downstairs with valuations 12 and 24. This checks the ramification factor and rules out the incorrect value j-bar downstairs.

The coefficient 1/576 is permitted over Z[1/6]. Since 576 is 2 modulo seven, the normalized residue is j-bar^2. The alternative calibration coefficient 624/576 is only a candidate comparison scalar; its stated residue is likewise j-bar^2. The proof does not identify that candidate with a geometric cocycle value or treat a local class over K as already carrying a globally descended ray-field normalization.

## 4. Coordinate and potential scope

Every nonzero coordinate modulo q^2 is either a unit, giving ±P and hence theta value A, or the unique nonzero nonunit, giving wP and value B. Admissibility of a coordinate pair forces at least one unit. Thus the raw pair residue is exactly j-bar to the power 4(epsilon(d)-epsilon(c)), and the normalized version has exponent 2 instead of 4.

For the explicitly restricted graph of genuine unimodular cusp edges in one same-curve component, this is an endpoint-potential ratio. Global-unit scaling and the strict Gamma_1(q^2) congruence preserve that potential. Every endpoint-balanced finite chain in that graph therefore has trivial product residue. This is a valid local cancellation theorem; it does not generate the entire homology, identify all components, or establish a relative theta map.

In particular, the nonzero residue of one admissible edge is not a counterexample to integer-ring absolute integrality. The calculation simultaneously exhibits why represented cycles can cancel.

## 5. Reproducibility and sources

The exact checker was read and independently replayed, with the output retained in this audit's replay directory. It confirms the division-polynomial weights, finite-field exponents, coordinate cases and graph sanity checks. It does not certify global CM descent or evaluate the LSSW cocycle.

Primary sources independently opened for this audit:

- Chida, *On the equivariant Tamagawa number conjecture for Hecke characters over imaginary quadratic fields*, Section 5: https://www.math.kyoto-u.ac.jp/~tetsushi/mw200705/chida_preprint.pdf . The initially cited survey endpoint timed out in the web tool. The companion was inspected online, and the subsequently recovered complete RIMS survey was also inspected locally in Section 8, printed pp.211–213. Its PDF SHA-256 is 5d29e2cfc19ccee3540a7b75c666c157c2feffdbe52e9dd506a0c620013b4bcd.
- Official Sage/Kohel Hilbert-polynomial documentation: https://doc.sagemath.org/html/en/reference/databases/sage/databases/db_class_polynomials.html .
- LSSW, Sections 3.1, 3.4 and 4.2, for the definition-field and good-reduction setup: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf .

No copied source document or source text is included in this authored acceptance report.
