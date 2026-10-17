# Exact swap calibration and a cyclic-four relative theta map

14 October 2026. Shared PASS 4/5, row 1777 / 30005572. Authored partial result; no novelty claim. Coefficients are R = Z[1/6] throughout.

## 1. Results and limits

This note proves two restricted assertions with actual normalized theta values, retaining K2 constants.

1. On a diagonal CM product E × E, the value of the canonical **unshifted** geometric auxiliary cocycle at the coordinate swap is exactly the separated auxiliary-theta Steinberg symbol. The proof identifies a Gersten chain and proves that chain is trace-fixed, so equality is not inferred just from equality of residues. All its translates give exact changes between swapped ordered-basis primitives.
2. If O/N is Z/4 and P is a primitive N-point on one fixed CM curve, all admissible **unpowered** theta pairs are differences of a single cusp potential valued in K2. Their sum on every represented balanced chain is zero in K2 itself. This is stronger than cancellation of the local tame symbols proved previously. The potential gives a full relative-homology homomorphism on this component, without assuming that unimodular edges generate relative homology.

The second map has zero absolute restriction. Its agreement with the canonical geometric arithmetic map has **not** been proved. The first assertion does not fill that gap: swapping an ordered basis is different from traversing a Cremona edge, and the origin-based evaluation requires a moved primitive. In particular, the exact swap formula has raw factor 576 at level four, whereas the required three-term smoothing has factor 624. Both statements and their different meanings are retained.

No all-component map, unrestricted relative formula, arithmetic descent theorem, or new integer-ring absolute integrality theorem is asserted. The frozen construction contract remains UNSOLVED.

## 2. Conventions and inputs

Let E/k belong to the accepted number-field CM-model setup, with its O-action defined over k, and let A = E × E. The identities below then persist under the accepted base-field and model-isomorphism transport; arbitrary new characteristic-zero base-field uniqueness is not assumed. Write x,y for the two projections. For an auxiliary ideal c, put m = Norm(c), H = E[c], and let f = f_c be the accepted canonical one-curve auxiliary theta element. Thus

    div(f) = m[0] - [H].

Use the Gersten sign convention of PASS2 RIGHT_END_LIFTING, section 6:

    d{u(x),v(y)} = u(x) exterior div(v(y))
                    - div(u(x)) exterior v(y).                  (2.1)

This agrees with the standard Milnor tame symbol
(-1)^(v(a)v(b)) a^v(b)/b^v(a): at a divisor of the first entry, the second entry occurs with negative valuation exponent. The cocycle residue equation below and (2.1) are used together. If an inverse Gersten differential is used instead while eta is kept fixed, the cocycle determined by (2.3) changes sign; the positive formula below uses exactly (2.1). In particular, Sharifi–Venkatesh equation (2.4) uses the inverse tame map. For a source comparison in that convention, write Theta_inv = -Theta_eta: then d_inv Theta_inv(g) = g eta - eta and the source-sign swap value is -{f(x),f(y)}. This is a global sign conversion, not an omitted constant. We do not identify the two signed representatives without this conversion.

The accepted genuine product primitive is

    eta = f(x) exterior H_y + m[0]_x exterior f(y).              (2.2)

Its boundary is m^2[0,0] - [H × H]. Let w exchange x and y. Let Theta_eta be the normalized geometric cocycle with

    d Theta_eta(g) = g eta - eta.                                (2.3)

We use either of the following accepted normalization ranges:

- c is prime to 5: the PASS3 eventual-trace-fixed and T5-fixed lift, valid for every imaginary quadratic field;
- 5 is unramified in F: the PASS2 unique eventual-trace-fixed lift, allowing c divisible by 5.

This second range applies to F = Q(sqrt(-23)) and c = (5). For c prime to 5, the two normalizations agree when both apply.

For matrices g = ((a,b),(c,d)), use row-coordinate maps R_g(x,y) = (ax+cy,bx+dy) and their pullbacks as the left action. Then (gh) acts as g followed on functions by h, so the ordinary cocycle identity is

    Theta(gh) = Theta(g) + g Theta(h).

No swap between nonisomorphic factors is asserted as an automorphism of a fixed product. The result concerns E × E, or a product with a specified O-linear identification of its two factors.

## 3. Constant-sensitive swap theorem

### Theorem 3.1

In either normalization range in section 2,

    Theta_eta(w) = {f(x), f(y)}.                                 (3.1)

More generally, for every O-linear automorphism g of A,

    Theta_eta(gw) - Theta_eta(g)
       = {f(ax+cy), f(bx+dy)}.                                  (3.2)

### Proof: the actual chain

Set Z = {f(x),f(y)}. Formula (2.1) gives

    dZ = f(x) exterior (m[0]_y-H_y)
           - (m[0]_x-H_x) exterior f(y)
       = m f(x) exterior [0]_y + H_x exterior f(y)
           - f(x) exterior H_y - m[0]_x exterior f(y)
       = w eta - eta.                                          (3.3)

Thus Z is an actual K2 Gersten lift, rather than a symbol chosen only after specialization.

### Proof: the constants are fixed, not discarded

For an O-linear endomorphism alpha prime to c, the separate-coordinate projection formulas imply

    [alpha,alpha]_* {f(x),f(y)}
      = { [alpha]_* f(x), [alpha]_* f(y) }
      = {f(x),f(y)}.                                           (3.4)

For clarity, factor the finite map as [alpha] × id followed by id × [alpha]. In the first transfer, the second entry is pulled back from the target, so the K2 projection formula gives the norm of the first entry. Apply the projection formula again for the second transfer. This is the external-product transfer formula; there is no additional factor deg(alpha) in either entry. The accepted one-dimensional norm identity then gives the final equality.

Equation (3.4) proves full eventual trace invariance of Z. If c is prime to 5, it also proves T5 Z = Z literally. Consequently Z and Theta_eta(w) lie in the same accepted normalized coefficient submodule and have the same residue. Its injectivity into the Gersten C1 term proves (3.1). This does not discard a possible constant K2 class: uniqueness applies after the actual normalization of Z has been verified.

Since every scalar trace commutes with g, gZ is normalized too. Formula (3.2) now follows from the cocycle identity, or directly by applying g to (3.3). This proves the theorem.

### Specialization at two nonzero coordinates

Let N be prime to c and let P be a primitive N-point rational over k. If cP and dP are nonzero, each lies outside E[c]. Therefore the two functions in (3.2) are units near s = (0,P), and the right side specializes exactly to

    {f(cP),f(dP)} in K2(k) tensor R.                            (3.5)

Likewise eta_g and eta_gw avoid s. Thus the **difference** on the left of (3.2) has a valid specialization, even if its two displayed summands separately do not. This is an exact calibration of the swapped-basis transition. It does not declare either g or w to lie in the congruence stabilizer of s.

## 4. The moved primitive: the precise remaining chain term

Let mu be an allowed shear for which eta_mu = mu eta avoids the level orbit. Write B_mu = Theta_eta(mu). The identity between normalized geometric cocycles is

    Theta_(eta_mu)(gamma)
       = Theta_eta(gamma) + gamma B_mu - B_mu
       = Theta_eta(gamma mu) - Theta_eta(mu).                  (4.1)

Indeed, both sides are normalized, and their residues are gamma mu eta - mu eta. The ordinary cocycle identity gives the second equality. Uniqueness proves equality, including constants.

For gamma fixing s, the **whole** right side of (4.1) is regular at s. The separate terms need not be regular there. In particular, B_mu cannot be evaluated at s and canceled as though it were an arbitrary constant-valued coboundary: its residue mu eta - eta includes the original coordinate support through s.

One may choose a finite sequence of admissible ordered bases g_0 = mu,...,g_r = gamma mu. Then (4.1) telescopes as the sum of their successive normalized transitions. Section 3 computes every step g -> gw explicitly. It does not compute a general elementary shear step g -> gt. These still have the prescribed Gersten C1 difference

    g(t eta - eta),                                             (4.2)

and require an actual normalized K2 lift and its specialization. No equality between a sum of the known swap steps and the full arithmetic cocycle is claimed when shear steps are omitted.

This is the surviving calibration gap in the present chain calculation. It is not a residual constant in the swap formula: that constant is proved zero. Nor has the remaining arithmetic difference been proved to be a cusp potential.

## 5. Cyclic order four: the symbols themselves are a cusp potential

Assume O/N is isomorphic to Z/4 and identify it by the unique unital map. Let P have annihilator N. Then P has exact additive order four, and

    E[N] = {0,P,2P,-P}.

The accepted canonical unpowered values exist because this is 2-primary torsion. Put

    A = theta_E(P),   B = theta_E(2P),   Q = {A,B}
        in K2(k) tensor R,

using additive notation for k^× tensor R inside the symbols. Evenness gives theta_E(-P) = A.

For c not in N put epsilon(c) = 0 if c mod N is odd, and epsilon(c) = 1 if c mod N is 2. An admissible primitive pair has c,d nonzero mod N and at least one of c,d odd. Direct bilinearity and antisymmetry give

    {theta_E(cP),theta_E(dP)}
          = (epsilon(d)-epsilon(c)) Q.                         (5.1)

The three possibilities are {A,A}=0, {A,B}=Q and {B,A}=-Q. Over R, {A,A}=0 since its possible 2-torsion vanishes. No triangle argument, regulator, or local residue map is needed.

### The potential is well-defined on represented cusps

Work in the component with lattice O^2. Represent a principal cusp by a primitive vector (a,c)^t. Two primitive O-vectors spanning the same F-line differ by a unit of O: the ideal generated by their coordinates is O on both sides, forcing the scalar to lie in O^×. Every unit maps to ±1 in (O/N)^×, so epsilon(c) is unchanged.

The strict Gamma_1(N) action leaves the denominator c unchanged modulo N. Enlarging by central units again does not change epsilon. Thus the potential

    p(cusp represented by (a,c)^t) = epsilon(c) Q               (5.2)

is well-defined on the represented allowed cusps. A represented cusp has nonzero denominator modulo N precisely when it does not map to the designated infinity cusp on the corresponding Gamma_0(N) quotient: completion of its primitive vector gives the converse as well.

Every actual unimodular edge g with columns (a,c)^t,(b,d)^t has theta value p(second endpoint)-p(first endpoint). Hence every endpoint-balanced finite R-linear combination of such edges has theta sum zero in K2(k) tensor R. This includes balanced chains representing nonzero absolute homology classes; the assertion is about their **theta-symbol sum**, not the value of the independently constructed geometric map on those classes.

For F = Q(sqrt(-23)), N = q^2 with q above 2 as in PASS3, this applies to the fixed same-curve represented graph. In particular, the previous j-bar^2 residue potential is the tame image of the exact K2 potential Q, rather than only an accidental residue cancellation.

## 6. Full relative extension in this restricted component

Let X be this compactified component, C its specified allowed cusp set, and M = K2(k) tensor R. Extend p from its represented cusps to a function p:C -> M by setting p=0 on all other cusps. If every cusp is represented, as in a class-number-one component, no such extra choice is required. Define the linear map

    p_*: R[C] -> M,       sum a_v[v] |-> sum a_v p(v).

Then

    F_theta = p_* composed with boundary:
       H1(X,C;R) -> H0(C;R) -> M                              (6.1)

is an actual homomorphism on full relative homology. For each admissible unimodular edge e, (5.1) proves exactly

    F_theta(e) = {theta_E(cP),theta_E(dP)}.

Its restriction to H1(X;R) is zero because the relative boundary is zero there. No assertion that the edges generate H1(X,C;R) occurs in this construction. Giving values on unrepresented cusps is a harmless noncanonical extension of the already proved potential; it does not change any prescribed edge value.

This is a restricted genuine relative theta map in the marked-point field. It does not identify that field with F(N), and it does not prove that its zero absolute restriction agrees with the canonical unaugmented geometric map. The zero restriction here follows from the explicit genuine theta formula (5.1); it has not been chosen as a substitute for the contract's comparison test.

Equivalently, if an independent absolute map f:H1(X;R)->M has been constructed, the accepted saturated-edge criterion shows that it has a relative extension with these theta values **if and only if f vanishes on every absolute class represented by a balanced combination of the prescribed edges**. This condition is now particularly concrete, but remains to be proved for the geometric map. It is stronger than a local triangular relation.

## 7. Level-four numerical factors and what they imply

At this level, the accepted normalization gives f_5(P)=24 theta(P), and the same at every nonzero coordinate. For F=Q(sqrt(-23)), 5 is unramified, so Theorem 3.1 is applicable to c=(5). Thus the genuine swapped-basis specialization is

    {f_5(cP),f_5(dP)} = 576 S(c,d),                            (7.1)

where S(c,d) is the genuine unpowered pair in (5.1). Formula (7.1) uses the declared standard-tame cocycle; the inverse-tame source-sign swap value is its negative. In contrast, the required three-term smoothing is

    {f_5(cP),f_5(dP)} + {f_5(cP),theta(dP)}
       + {theta(cP),f_5(dP)} = 624 S(c,d).                     (7.2)

The difference is 48 S(c,d). By (5.1) this difference is the endpoint potential 48p(second)-48p(first) on the represented graph. Therefore the raw and correctly smoothed assignments agree on all balanced chains in this restricted graph: both sums are zero in K2. They do not agree edge by edge in general.

In the accepted local -23 test, the explicit even theta values, and hence the displayed pairs, are defined over the unramified good-model base K, although the point P itself is rational only over the ramified quadratic field K'. Over K, Q has standard tame residue j-bar^2, which is nontrivial of order seven. Consequently the raw pair has residue j-bar^4 and the 624-smoothed pair has residue j-bar^2. The mixed-term difference has residue j-bar^(2*48)=j-bar^5. The geometric evaluation at the K'-rational marked point is the restriction of this explicit K-symbol; its residues are the squares of the K-residues. No general K2 descent theorem or equality between the good-model base and the global ray field is used. Thus in that exact local realization the raw and smoothed **edge values really differ**. Their cycle sums still agree by the potential calculation.

There is an actual nonzero prescribed relative edge in this local realization. Use the accepted element w with wP=2P and w in q\q^2. The matrix with rows (0,-1) and (1,w) has determinant one. Its two cusp denominators have types 1 and 2, so its genuine theta value is Q. These cusps are distinct under the congruence action because epsilon is invariant. The local residue j-bar^2, or j-bar^4 after restriction to the marked field, proves that this value is nonzero. Thus the restricted relative map is not an arbitrarily chosen zero map; it has a proved nonzero relative value, although its absolute restriction is zero.

This provides a checked example where an actual unshifted geometric swap value is not the desired smoothed relative edge value. It does not contradict the desired calibration, which concerns the moved arithmetic cocycle on absolute cycles, not the unshifted swap transition at an unrelated torsion pair.

## 8. Dependencies, verification, and outstanding work

Inputs read in full or in their relevant proof sections:

- The construction target and accepted earlier symbol results summarized in this reader.
- PASS3 INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md, frozen SHA-256 8c1b6b0877e0b99569da58f99bf7abc112056a5538c16f44d5ce5aec4b1a7534, and RELATIVE_THETA_ACCEPTANCE.md.
- PASS2 RIGHT_END_LIFTING.md, GEOMETRIC_COCYCLES.md; PASS3 SCALAR_FIVE_NORMALIZATION.md.
- PASS1 RELATIVE_SYMBOL_DERIVATION.md, especially the exact saturated-edge extension criterion.
- PASS3 EXACT_THETA_RESIDUE_TEST.md and NORMALIZATION_SOURCE_ADDENDUM.md.
- Sharifi–Venkatesh, *Eisenstein cocycles in motivic cohomology*, equation (2.4), retained text, https://math.ucla.edu/~sharifi/eisensymbol.pdf : inverse-tame convention, explicitly converted in section 2.
- LSSW, *Eisenstein cocycles for imaginary quadratic fields*, section 3.4, retained arXiv-v1 text; public source: https://arxiv.org/pdf/2504.19125v1 . The paper specifies the shifted primitive and cocycle residue. The R-coefficient uniqueness used here is the accepted earlier authored proof, not an enlargement of the paper's coefficient ring by citation.

CHECK_EXACT_IDENTITIES.py verifies the Gersten coefficient expansion, the finite Z/4 pair table, the smoothing coefficients, graph-cycle telescoping on a finite test, and the finite-field exponents. It does not mechanically prove transfer in K-theory, geometric exactness, or global Bianchi homology generation. Those are not replaced by the finite checks.

The remaining substantive target is still to compare the moved arithmetic cocycle with the prescribed symbols on all balanced chains, including nonzero absolute classes, and then to establish all-component arithmetic descent and the integer-ring absolute target. The present note proves a genuine restricted chain calibration and a genuine restricted full relative map, but does not identify them on that remaining target.
