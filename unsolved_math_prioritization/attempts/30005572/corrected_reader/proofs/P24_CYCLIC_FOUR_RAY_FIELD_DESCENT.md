# Exact ray-field target for the cyclic-four relative theta map

14 October 2026. Shared PASS4/5, row 1777 / 30005572. Addendum to EXACT_SWAP_AND_CYCLIC_FOUR.md. This upgrades the coefficient field of the restricted relative construction; it does not prove its geometric absolute calibration.

## Theorem

Let F be imaginary quadratic with maximal order O, let N be a nonzero ideal such that O/N is isomorphic to Z/4, and put H = the Hilbert class field of F. Then F(N)=H. Choose a representative E/H of the desired CM isomorphism class, with its O-action defined over H. Let P have annihilator N over an algebraic closure of H.

The genuine normalized values

    A = theta_E(P),    B = theta_E(2P)

belong canonically to H^× tensor R, R=Z[1/6], even if P itself is not H-rational. They are independent of the choice of primitive P. Thus Q={A,B} is an actual class of K2(F(N)) tensor R, defined there as a symbol of descended units, rather than an invariant K2 class whose descent is presumed.

Consequently the full relative map on the same-curve component constructed in sections 5-6 of the companion note has the exact target K2(F(N)) tensor R. Its absolute restriction is zero. On the principal component of the -23/q² example, this relative map has a nonzero prescribed edge value Q.

## Proof

### 1. The ray field

The ray class exact sequence for an imaginary quadratic field is

    O^× -> (O/N)^× -> Cl_N(F) -> Cl(F) -> 1.

There is no real-place sign factor. Under O/N = Z/4, the middle unit group consists of 1 and -1, both images of global units. Therefore Cl_N(F) -> Cl(F) is an isomorphism. The ray field F(N), which contains H, consequently equals H.

This can equivalently be phrased without fixing an isomorphism of residue rings: a unital isomorphism with Z/4 is unique, and -1 has nontrivial image of order two. No class number or extension degree is inverted.

### 2. The CM marking up to sign

LSSW section 3.1 states that every maximal-O CM elliptic isomorphism class has a representative over H. Because H contains F, all its CM endomorphisms are defined over H, by the E=E' case of Lemma 3.1.1 quoted and proved there.

The subgroup E[N] is therefore Galois-stable and the Galois action is O-linear. It is free of rank one over O/N. In the present case it is a cyclic group of order four, with exactly two generators P and -P. Hence every sigma in Gal(overline(H)/H) satisfies

    sigma(P) = P or -P,

and fixes 2P. This is a statement about the actual torsion representation of an H-model; it does not assert that a ramified marked-point extension is the ray field.

### 3. Descent in K1 before forming K2 symbols

Choose a Weierstrass equation over H and form the actual rational function

    g5 = Delta^2 / psi5 in H(E)^×,

where psi5 is the standard fifth division polynomial. The accepted PASS3 normalization addendum identifies the normalized f5 with g5 in H(E)^× tensor R; its possible twelfth-root convention disappears over R. This equality is not inferred merely from their common divisor.

The function g5 is even: psi5 is a polynomial in x. The Galois action P -> ±P therefore gives x(P) in H, and 2P itself is H-rational. Consequently

    g5(P), g5(2P) are literal elements of H^×.

They are defined and nonzero because the nonzero four-torsion points lie outside E[5]. This proves actual image descent, rather than just reporting invariance in a tensor-valued group. The already accepted exact normalization gives

    A = (1/24) g5(P),    B = (1/24) g5(2P)

in H^× tensor R. Division by 24 is allowed. No division by [M:H], 5, 7, or the class number occurs; no K2 restriction or invariant-descent statement is used.

Replacing the primitive P by -P leaves A unchanged and leaves 2P unchanged. Under a Weierstrass isomorphism x=u²x'+r, psi5 scales by u²⁴ and Delta² by u²⁴, so g5 is model-invariant. This, or the accepted O-linear model functoriality, gives independence of a twist or model change representing the same marked CM isomorphism class. This proves the stated canonical meaning.

Only now form Q={A,B} in K2(H) tensor R, equivalently

    Q = (1/576) {g5(P),g5(2P)}.

Thus the arithmetic target is supplied by explicit H-valued entries before a K2 symbol is taken.

### 4. Relative map and an actual nonzero value

Use exactly the cusp potential in the companion note, now valued in K2(H) tensor R:

    p(v) = 0 for represented odd denominator,
    p(v) = Q for represented denominator 2 modulo 4.

Its invariance under primitive-vector rescaling and Gamma_1(N), the extension to unrepresented allowed cusps, and the map p_* composed with the full relative boundary are unchanged. They prove the prescribed genuine theta formula on every admissible unimodular edge in this component, without a generation assertion.

For F=Q(sqrt(-23)), q=(2,w), w=(1+sqrt(-23))/2, N=q², the accepted exact local calculation may be compared to this H-model by an embedding at q and an O-linear isomorphism over a common extension to the good-reduction model. Both choices of primitive point differ by sign; evenness and model functoriality identify the explicit descended theta values. On the good-model base K, the image of Q has standard tame symbol j-bar² of order seven. Thus Q in K2(H) tensor R is nonzero: a zero class would have zero image under field extension and the tame map.

The matrix with rows (0,-1) and (1,w) has determinant one, and its edge has lower coordinates (1,w). Since w is 2 modulo q², its theta value is Q. Both endpoints are in the allowed represented non-infinity cusp set. Their denominator types distinguish their Gamma_1(N)-orbits. Therefore this is a genuine nonzero relative value over the actual ray field H.

If the common comparison extension is used instead of K, one must not infer nonvanishing merely from an arbitrary extension whose ramification degree might kill seven-torsion. Here the values are already the same explicit elements of K^× tensor R: their identity follows at K1 from injectivity of the unit-group inclusion into the common extension. The given tame symbol is consequently computed in K itself. This distinction prevents a hidden K2-restriction assumption.

## Calibration boundary

This is an exact ray-field relative construction for a restricted level and fixed same-curve/principal component, including a nonzero relative value. It is not automatically an all-component construction: on a product E_r × E_1 with distinct factors, the two pairs of even theta values can differ, and the displayed single-Q endpoint-potential argument does not apply without further identities. It does not show that the canonical geometric map is zero on the balanced absolute classes represented by its edges, or that the moved auxiliary cocycle equals 624 times this map on absolute homology. Those are the precise remaining comparison statements. The frozen full construction contract remains UNSOLVED.

## Primary source and accepted inputs

- LSSW, *Eisenstein cocycles for imaginary quadratic fields*, section 3.1 and Lemma 3.1.1, retained arXiv-v1 text, https://arxiv.org/pdf/2504.19125v1 . The H-model and full endomorphism-definition assertions are used at their stated scope.
- Accepted PASS3 unpowered order-four normalization, evenness, model functoriality, and K1 descent: INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md, SHA-256 8c1b6b0877e0b99569da58f99bf7abc112056a5538c16f44d5ce5aec4b1a7534.
- Accepted PASS3 -23 local model and exact residue calculation: EXACT_THETA_RESIDUE_TEST.md and NORMALIZATION_SOURCE_ADDENDUM.md. The marked field and ray field remain distinct throughout.
