# Independent adversarial review of the arbitrary-characteristic line theorem

2026-10-02. **Verdict: PASS for the complete stated theorem over every algebraically closed field.** No mathematical gap or counterexample was found. In particular, the Picard–Albanese argument supplies a valid characteristic-free replacement for the earlier vanishing step. The resulting classification rules out the non-ACM line configuration asked for in the exact source question.

This is an independent AI mathematical audit, not a formal proof-assistant certificate or a historical novelty certification. The supplemental finite algebra controls do not certify the geometric lemmas. No GitHub mutation or publication was performed by this review.

## 1. Frozen artifact and exact source

The reviewed public proof is `PUBLIC_TURN_2.md`, SHA-256

    56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1

The original frozen `TURN_2.md` is preserved unchanged with SHA-256

    4f2e4726724540def381aa3354925f38bf52e506bcf41df4a646a65395c98c61

The public copy differs only in its opening status paragraph and the final administrative review sentence. All mathematical statements, proofs, source links, hypotheses, and boundary-case discussion are identical. The review read the complete mathematical text, rather than relying on the earlier characteristic-zero audit.

The theorem concerns a nonempty finite reduced union of lines L in P^3 over an algebraically closed field k of arbitrary characteristic, its homogeneous radical ideal I, and the hypothesis alpha(I^(2))=alpha(I)+1. The conclusion is that L is coplanar or the complete pairwise-intersection pseudostar of distinct planes, with no triple-containing line, and therefore ACM.

The primary source was independently reopened: Janssen, *On the Fattening of Lines in P^3*, https://arxiv.org/pdf/1306.4387. Its opening field convention is arbitrary characteristic; Question 3.1 asks the non-ACM existence question. The corresponding OWR paragraph at printed p. 514, https://ems.press/content/serial-article-files/46557, asks the same question separately from the subsequent questions about general ACM configurations and reduced curves. This review certifies the line target, not those other questions.

Local source-record SHA-256:

    8ca13c1b3de8b0659f6d39eed5556bb2585abc4fccbf7eef66f7a869599600c5

Local source-gate SHA-256:

    804cf65a73fb8edb1dcace53c06f27699abf70c753f4f672004f7ecad2a003b1

## 2. Resolution, positivity of H, and the integral hyperplane curve

Surface resolution is available in arbitrary characteristic. This is the two-dimensional theorem, not a conjectural higher-dimensional resolution input. A projective normalization of a finite-type surface over a field has a projective regular resolution by normalized blowups. Over the perfect field k, regularity is smoothness. The resolution may be taken to be an isomorphism over the normal surface's regular locus. These precise hypotheses are covered by Stacks, Resolution of Surfaces, Theorem 54.14.5 and its introduction:

https://stacks.math.columbia.edu/tag/0BGJ

https://stacks.math.columbia.edu/tag/0ADX

For f:X->S birational and H=f^*O_S(1), global generation implies nefness. Birational projection formula gives H^2=deg S=e; no inseparable degree factor appears, since the function fields agree.

The assertion that C can be integral does not require smooth Bertini for the morphism f. A general plane cuts an integral E on S: geometric irreducibility follows from the ordinary hyperplane Bertini theorem, and the intersection with S_reg is generically smooth/reduced because S_reg embeds into P^3. The plane curve is a hypersurface and has no embedded components; irreducibility and generic reducedness therefore imply integrality. The source hypotheses were checked against Stacks:

https://stacks.math.columbia.edu/tag/0G4C

https://stacks.math.columbia.edu/tag/0FD4

Avoid the finitely many images of exceptional curves of X->Y, where Y is the normalization. The finite morphism Y->S contracts no curves. Consequently the total pullback C of E has no contracted curve component. Every curve component must dominate E. Its generic point is in S_reg, where f is an isomorphism; thus there is exactly one component and its multiplicity is one. A Cartier divisor on the smooth surface X is Cohen–Macaulay of pure dimension one, so it has no embedded components. Hence C is integral.

This remains valid if E meets the conductor in inseparable or non-smooth ways. Those are closed points on E and do not create another generic component or alter its generic multiplicity. The proof never calls C smooth. Its normalization, used later, is a smooth projective curve because k is perfect.

## 3. Lemma A: characteristic-free adjoint nonvanishing

### 3.1 The pg split is sound

If pg>0, a nonzero section of omega_X multiplied by the square of the section defining C is a nonzero section of omega_X(2H). Integrality of X prevents a product of nonzero sections from vanishing identically.

If pg=0, surface Serre duality gives H^2(O_X)=0. The obstruction to lifting a line bundle through a square-zero Artin extension lies in H^2(O_X) tensored with the extension ideal. Thus the Picard scheme is formally smooth at its identity, and, being locally of finite type, smooth there. Translation gives the same conclusion for the identity component. Its tangent dimension is h^1(O_X), and its reduced identity component is dual to Alb(X), so

    q=h^1(O_X)=dim Alb(X).

This equality is not true for arbitrary characteristic-p surfaces without the pg=0 condition; the proof uses it only where that condition has been established. The exact needed facts are explicitly corroborated in Liedtke's positive-characteristic exposition, printed pp. 13-14:

https://cims.nyu.edu/~tschinke/books/simons12/lectures.pdf

The tangent-space computation and the square-zero obstruction argument also appear in Conrad's primary lecture notes:

https://math.stanford.edu/~conrad/248BPage/handouts/pic.pdf

### 3.2 Albanese generation survives inseparability

Choose the Albanese basepoint on C. The map from the normalization C_tilde to A=Alb(X) factors through its Jacobian. The image B of the induced homomorphism is an abelian subvariety, and the image of C lies in B. Quotienting gives b:X->A/B, constant on C.

For an ample M on A/B, N=b^*M is nef and N.H=N.C=0. The algebraic Hodge index theorem applies over every algebraically closed field: since H^2>0, its perpendicular subspace in N^1(X)_R is negative definite. On the other hand N^2>=0 by nefness. Therefore N is numerically trivial. This uses the algebraic intersection theorem, not complex Hodge theory or a characteristic-zero vanishing theorem.

If b were nonconstant, an integral curve on X could be chosen whose image is a curve. The restriction of b to that curve has positive finite degree onto its image, so the degree of N on it is positive. This contradicts numerical triviality. The degree remains positive for purely inseparable morphisms. Thus b is constant; the universal property of the Albanese then forces A/B=0.

It follows that J(C_tilde)->A is surjective, giving

    q=dim A<=g(C_tilde)<=p_a(C).

No injection of tangent spaces, separability of a curve morphism, or characteristic-zero inequality q<=g was assumed. The last inequality is the normalization exact sequence for the integral curve. If C is rational, it correctly forces q=0.

### 3.3 Riemann–Roch signs and vanishing

Put g_a=p_a(C). Since C is an integral Cartier divisor linearly equivalent to H, arithmetic adjunction gives K.H=2g_a-2-e. In the pg=0 case, chi(O_X)=1-q. Hence

    chi(omega_X(2H))
      =1-q+K.H+2e
      =e+2g_a-1-q
      >=e+g_a-1>=1.

The adjunction and Riemann–Roch factors of two are integer intersection-number identities; they do not invert 2 in the ground field. Thus characteristic 2 causes no change.

Serre duality gives h^2(omega_X(2H))=h^0(-2H). A nonzero effective divisor of class -2H would have negative intersection with nef H, impossible. If the section had zero divisor, the line bundle would be trivial, also contradicting H^2>0. Therefore h^2=0, and h^0=chi+h^1>=1.

The lower bound e>=2 is essential and correctly present: on P^2 with H a line, e=1 and K+2H has no section. At the tight allowed boundary e=2,g_a=q=0, the Euler characteristic is exactly one. There is no gap at this boundary. Lemma A passes.

## 4. Lemma B: canonical forms, conductor, and lifting

The normal surface Y is Cohen–Macaulay and its canonical sheaf is reflexive. Because the chosen resolution is an isomorphism over Y_reg, a regular canonical form on X restricts to a canonical form there. It is determined by that restriction, and reflexivity extends it across the codimension-two complement. This gives an inclusion q_*omega_X into omega_Y. Equality, rational singularities, Grauert–Riemenschneider vanishing, or characteristic-zero trace arguments are not needed.

Finite normalization duality gives

    nu_*omega_Y = Hom_S(nu_*O_Y,omega_S)
                = c tensor omega_S.

Here S is a hypersurface, so omega_S=O_S(e-4) is invertible. The conductor identity and the finite-duality statement are present in Kollár's paper with Dao's appendix, Definition 46 and equation (48.1):

https://arxiv.org/html/1811.00042v2

The local conductor description is also directly valid in every characteristic. An A-linear map from a finite birational extension B to A becomes multiplication by an element t of the common fraction field; evaluation at 1 puts t in A, and its defining condition is tB subset A. A conductor element that is a unit at a point forces normalization to be an isomorphism there.

At a singular codimension-one point of S, the one-dimensional local ring is not regular. Over the perfect base field, this agrees with non-smoothness. A normal one-dimensional Noetherian local domain is a DVR and regular, so that point is nonnormal. Thus every conductor section vanishes generically on each singular curve and consequently along the whole reduced curve.

Projection formula twists the injection by O_S(2), so Lemma A gives a nonzero conductor section of degree e-2. The hypersurface sequence has kernel O_{P^3}(-2); its H^1 vanishes in every characteristic, and the section lifts to a nonzero homogeneous polynomial. It need not vanish at isolated normal singularities, which the theorem does not require. Neither inseparability along the conductor nor characteristic dividing e invalidates any of these steps. Lemma B passes.

## 5. Full configuration reduction, with edge cases

For each target line, its ideal is generated by two independent linear forms and its square is primary. Thus its symbolic square equals its ordinary square. The symbolic square of the reduced union is the intersection of these squares. All generic-to-global membership steps in the proof are therefore valid.

If a minimal witness F has a repeated factor, its squarefree radical already vanishes on L. Degree at most d-2 would contradict alpha(I)=d-1. A degree loss of exactly one is possible only for one doubled linear factor P and all other factors squarefree and coprime: F=P^2G. If G is constant, the configuration is coplanar; this exception must and does remain in the argument.

For nonconstant squarefree G, not all partial derivatives vanish in positive characteristic. Otherwise every exponent in every monomial is divisible by p; perfectness of k makes G a pth power, contradicting squarefreeness. The chosen nonzero partial derivative has degree deg G-1. For lines outside P, G belongs to the squared line ideal, hence its partial derivative belongs to the line ideal. Multiplication by P covers the remaining lines and yields the forbidden degree d-2. This is valid also in characteristic 2 and does not assume the converse derivative criterion for symbolic squares.

For a squarefree nonlinear component Q, a line lying in Q alone must lie in its squared ideal. All first partials of Q vanish on the line, so the hypersurface Jacobian criterion puts it in the singular locus. An integral hypersurface over the perfect field is generically smooth and its singular locus has dimension at most one; such a line is therefore a singular curve. Lemma B supplies the degree-lowering polynomial, and multiplying by F/Q yields the same forbidden degree. All components of F are consequently distinct planes.

Every target line belongs to at least two planes, by its required multiplicity. If a pair-intersection line is omitted, or if three planes contain a line, deleting the relevant two factors leaves a degree d-2 polynomial vanishing on every target line. Both possibilities contradict minimality. All and only the pair intersections therefore occur, with no triple-containing line. Concurrent intersection points of four or more planes are allowed; the proof does not impose full general position.

The displayed Hilbert–Burch matrix has maximal minors F/P_i up to sign. Their ideal has height two because its zero set is exactly the pair-intersection union. Hilbert–Burch gives a Cohen–Macaulay quotient with no embedded associated primes. At each line's generic prime all other plane equations are units, so the ideal localizes to that reduced line prime. Generic reducedness together with absence of embedded associated primes gives reducedness globally. Thus this is the actual radical line ideal, and its quotient is ACM. The coplanar alternative is independently a complete intersection. The one-line and arbitrary coplanar-union cases are included.

The proof of the stated classification and hence the negative answer to the non-ACM existence question is complete on this review.

## 6. Supplemental independent algebra controls

`check_small_characteristics.py` uses only standard-library exact modular linear algebra. It computes initial degrees by applying an invertible coordinate change to each line and testing every coefficient of normal monomial order below 1 or 2. It therefore tests actual squared-line membership even in characteristic 2, without confusing it with a derivative-only condition.

Run the portable checker with `python3 check_small_characteristics.py --proof PATH_TO_PUBLIC_TURN_2.md`. It checks eight configurations over each of F_2,F_3,F_5, hence also their algebraic closures: a single line; a coplanar union; two skew lines; a three-plane pseudostar; a tetrahedron; a four-plane cone; a five-plane star; and a tetrahedron with one missing edge. All exact alpha and alpha-symbolic-square values agree with the expected boundary behavior. It also checks 60 symbolic Hilbert–Burch minor identities, the small-characteristic derivative kernel on monomials, and the integer Riemann–Roch signs. Total: 3,888 assertions passed.

These computations supply falsification controls for algebra and small-characteristic edges. They do not prove resolution, Albanese generation, Hodge index, or conductor duality; the preceding analytic review checks those dependencies. The immutable public proof hash is recorded in the control receipt.

## Disposition

PASS_COMPLETE_ARBITRARY_CHARACTERISTIC_LINE_THEOREM. No mandatory mathematical revisions. Publication should preserve the exact field and reduced-union hypotheses, retain the coplanar exception, credit the existing pseudostar results, and describe novelty as a separate assessment. The first-turn characteristic-zero audit alone was insufficient; this verdict specifically reviews the new characteristic-free mechanism in the frozen public second-turn candidate.
