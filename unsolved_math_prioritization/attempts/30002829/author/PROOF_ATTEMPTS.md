# Ueno-type varieties: five retained approaches, not a solution

## Target and convention

Work over k = C. Let E be the smooth projective elliptic curve with affine equation y² = x³ − 1, let ω be a primitive cube root of unity, and let g(x,y) = (ωx,−y). For n = 4 or 5, write X_n for a smooth resolution of E^n/⟨g⟩, with g acting diagonally. In the 2015 sources this is X_{n,6}; n is the dimension and 6 is the automorphism order. Changing the smooth resolution does not change the function field or the rationality questions. An arbitrary product action, the order-three quotient, and the order-four Ueno–Campana threefold are different objects.

The original OWR questions on printed page 818 ask whether X_4 is rational and whether X_5 is unirational. COV additionally ask whether X_5 is rational. We retain that stronger question separately, without replacing the original unirationality question by it. No result here settles any of these outstanding conclusions. There is also no assertion about stable rationality.

All five approaches below were developed in this attempt. The formulas of Catanese–Oguiso–Verra (COV, arXiv:1506.01925v1) and the conditional curve-counting route of Mellit (arXiv:1705.02931v3) are prior work. The elementary derivations and route obstructions below are authored checks, not novelty claims.

## Approach 1. Diagonal invariants and a checked birational reduction

Let L = k(E^n), with coordinates (x_i,y_i). On the open locus x_1 y_1 ≠ 0 put

v_i = y_i/y_1,  w_i = x_i/x_1  (2 ≤ i ≤ n),
U_i = w_i³ − 1.

Every v_i and w_i is invariant. The equations of the elliptic curves give

(v_i² − 1) = U_i x_1³/y_1².

In particular the relations are

(v_i² − 1) U_2 = (v_2² − 1) U_i  (3 ≤ i ≤ n).       (1)

These generators give the whole invariant field. Indeed, for F = k(v_i,w_i),

T = x_1³ = (v_2² − 1)/(v_2² − w_2³),  y_1² = T − 1.

Thus L = F(x_1,y_1) has degree at most 3·2 = 6 over F. Since the faithful group ⟨g⟩ has order six and fixes F, Artin's fixed-field theorem gives [L:L^g] = 6. The tower law forces F = L^g. This argument does not confuse a dominant degree-six cover with a birational parametrization.

Now put q = v_2 − 1 and s_i = (v_i − 1)/q. Let s=s_3, t=s_4 and, when n=5, r=s_5. Equation (1), after removing the nonzero factor q, becomes

(s_i² U_2 − U_i)q + 2(s_i U_2 − U_i) = 0.          (2)

Write U=U_2 and V=U_3. Then

D = s² U − V,   q = 2(V − sU)/D.                 (3)

Substitution into (2) for i=4 gives exactly

F_t = (s−t)st U − (s−1)s U_4 + (t−1)t V = 0.    (4)

For n=5 there is also

F_r = (s−r)sr U − (s−1)s U_5 + (r−1)r V = 0.    (5)

An exact elimination identity is

D[(t²U−U_4)q + 2(tU−U_4)] = 2U F_t,

where q is (3). The same identity holds with (t,U_4) replaced by (r,U_5).

The rational inverse on the quotient is explicit: recover q from (3), then v_2=1+q and v_i=1+s_i q. Keep the w_i. These reproduce all invariant generators and all relations (1). Conversely, substituting s_i=(v_i−1)/(v_2−1) into (3), and using (1), recovers q=v_2−1. Consequently both compositions are the identity in the function field.

The required open locus has U D q (v_2²−w_2³) ≠ 0, together with the denominators in these formulas. It is nonempty: take v_2=2, v_3=3, v_4=4, v_5=5, U=1, V=8/3, U_4=5, U_5=8, using only the first n coordinates. Then s=2,t=3,r=4, D=4/3, q=1 and T=3/2. Choose cube roots for w_i³=U_i+1 and roots x_1³=3/2, y_1²=1/2. This gives points of E^n satisfying every required nonvanishing condition. Root choices here lift a quotient point; they are not part of the rational inverse on the quotient.

For n=4, (4) is geometrically irreducible over k(s,t), being a smooth diagonal cubic surface after projective completion (see Approach 2). For n=5, (4)–(5) give a geometrically integral complete intersection over k(s,t,r) (Approach 3). Thus the displayed models have the expected component and dimension, rather than an extraneous component created by clearing denominators.

Retained result: completely checked birational models for both dimensions, with inverse and open-domain conditions. Exact gap: these models are not parametrizations by n independent transcendental coordinates. Solving the displayed equations by adjoining cube roots does not prove rationality or unirationality.

## Approach 2. The fourfold's cubic-surface fibration

Over K=k(s,t), set

a=st(s−t), b=−s(s−1), c=t(t−1), d=−(a+b+c).

The projective completion of (4), in coordinate order (w_2,w_4,w_3,z), is

a w_2³ + b w_4³ + c w_3³ + d z³ = 0.           (6)

We have a+b+c=(s−1)(s−t)(t−1). All four coefficients are nonzero in K, so the gradient of (6) cannot vanish at a projective point. The surface is smooth. It has 27 distinct K-points of the form (ε_1,ε_2,ε_3,1), where ε_i³=1. COV Theorems 3.2 and 3.4 therefore supply a dominant rational map P²_K to this surface, of degree at most six. Since K is a two-variable rational field over k, this implies the known unirationality of X_4 over k. This is a verified prior result, not a new resolution of the target.

Could this same K-surface be rational? The diagonal-cubic criterion in COV Theorem 3.5 says that a smooth diagonal cubic with a K-point, over a field containing ω and of characteristic different from 2,3, is K-rational exactly when a pairing quotient of its four coefficients is a cube. There are three quotients, up to reciprocals:

ab/(cd)=s²/(t−1)²,
ac/(bd)=t²/(s−1)²,
ad/(bc)=(s−t)².

They have valuation 2 respectively at the irreducible divisors s=0, t=0 and s−t=0. Every cube in k(s,t) has valuation divisible by three at every prime divisor. None of these quotients is a cube; neither is its reciprocal. The criterion proves that (6) is not K-rational. This independently checks the algebraic application of COV Theorem 3.6.

A birational modification over this fixed K cannot repair that obstruction: it preserves the K-function field. What remains possible is a k-birational construction that changes or mixes the base coordinates. This distinction is essential when interpreting the neighboring formulation about changing the cubic surface.

Retained result: known k-unirationality, and a complete valuation verification of the fixed-base nonrationality obstruction. Exact gap: no k-birational parametrization or k-birational obstruction for the total fourfold has been obtained.

Negative control for the inference about total spaces: the rational plane A²_{x,y} maps to A¹_t by t=y²−x³. Its generic smooth projective fiber is the elliptic curve y²=x³+t over k(t). The total field k(x,y) is rational although its extension of k(t) is not a rational one-variable field. A nonrational generic fiber cannot by itself prove a nonrational total space.

## Approach 3. Why the same surface method fails in dimension five

Now take K=k(s,t,r), with s,t,r algebraically independent. Projectively complete (4)–(5) in P⁴_K with coordinates (w_2,w_3,w_4,w_5,z). The coefficient matrix of the two diagonal cubics is

M = [ st(s−t), t(t−1), −s(s−1), 0, −(s−1)(s−t)(t−1) ;
      sr(s−r), r(r−1), 0, −s(s−1), −(s−1)(s−r)(r−1) ].

Every column is nonzero. Every pair of columns is linearly independent. In zero-based column order, the ten 2×2 minors factor as follows:

01: rst(r−t)(s−1)
02: −rs²(r−s)(s−1)
03: −s²t(s−1)(s−t)
04: s(r−s)(r−t)(s−1)(s−t)
12: rs(r−1)(s−1)
13: −st(s−1)(t−1)
14: s(r−1)(r−t)(s−1)(t−1)
23: s²(s−1)²
24: −s(r−1)(r−s)(s−1)²
34: −s(s−1)²(s−t)(t−1).

All are nonzero elements of K. This proves smoothness of the complete intersection S. If a point of S were singular, a nonzero linear combination of the two gradient rows would vanish. For every nonzero coordinate Z_j, this forces the corresponding column of M into the one-dimensional kernel of a fixed nonzero row vector. Pairwise independence means at most one coordinate can be nonzero. The two defining equations would then force that nonzero column times Z_j³ to vanish, a contradiction.

The equations have codimension two: the first is an irreducible cone over a smooth cubic surface, while the second has a nonzero w_5³ term. They have no common component of codimension one. Their projective intersection is nonempty and two-dimensional. A projective complete intersection of positive dimension is geometrically connected; here this also follows from its Koszul resolution and the vanishing of intermediate cohomology of line bundles on P⁴. Smoothness and connectedness give geometric integrality.

Adjunction gives

ω_S ≅ O_S(3+3−5) = O_S(1).

Thus the canonical bundle is ample and K_S²=9. In particular S is a surface of general type. The twisted Koszul resolution shows H⁰(S,O_S(1)) has dimension 5, so S has nonzero regular two-forms. It is not geometrically unirational in characteristic zero: a dominant rational map from P² to S would, after resolving indeterminacy, pull back a nonzero top differential to a nonzero top differential on a smooth rational surface. The latter has none. The pullback is injective at the generic point because the extension is separable.

Retained result: this particular generic surface over k(s,t,r) is provably not even geometrically unirational. The cubic-surface parametrization argument for n=4 therefore cannot simply be repeated for this n=5 projection.

Exact gap: this is a relative obstruction only. It does not disprove unirationality or rationality of the total fivefold. A successful parametrization would have to interact with the base in a different way.

Negative control even for general-type fibers: A³_{x,y,z} is rational and maps to A¹_t by t=x⁵+y⁵+z⁵. Its generic projective fiber x⁵+y⁵+z⁵−t w⁵=0 is a smooth quintic surface in P³ over k(t), with canonical bundle O(1). Thus a rational total space can have general-type generic fibers.

## Approach 4. Exchange the base and the fiber coordinates

For n=4, instead project to the three coordinates (w_2,w_3,w_4). With A=w_2³−1, B=w_4³−1, C=w_3³−1, the projective generic fiber in coordinates [s:t:u] is the plane cubic

A st(s−t) − B su(s−u) + C tu(t−u) = 0.           (7)

The coefficients A,B,C are algebraically independent; the map from the three w-coordinates to them is dominant and generically finite. A general cubic in this family is smooth. A concrete certificate is the specialization (A,B,C)=(1,2,3): in each of the three projective affine charts, the ideal generated by the three homogeneous partial derivatives has reduced Gröbner basis [1] over Q. The exact script checks all three charts. Since the projective singular incidence has closed image in coefficient space, existence of this smooth specialization proves generic smoothness.

The point [0:0:1] lies on every member; its partial derivatives include B and −C, so it is smooth generically. A smooth plane cubic is geometrically integral of genus (3−1)(3−2)/2=1. Consequently this new generic fiber is an elliptic curve over k(w_2,w_3,w_4), not a rational curve. Any nonconstant map from P¹ to it over an algebraic closure is impossible by Riemann–Hurwitz in characteristic zero.

This independently identifies the genus-one obstruction behind attempting to solve for the original two base coordinates after treating the cube coordinates as free. A root of the resulting cubic, or a degree-two description through the coefficient map, is not a rational inverse.

Retained result: the swapped fibration has a smooth genus-one generic fiber, with a rational point and an exact smoothness certificate. Exact gap: a further change mixing both coordinate sets, or a different argument about the entire function field, is required. No claim about stable rationality follows.

## Approach 5. Curve counting, an exact conditional descent, and its missing input

Mellit's later method is not an unconditional solution. In arXiv v3 the relevant hypotheses are Conjectures 1, 2 and 3; in the published 2022 article they are numbered 6.2, 6.3 and 6.4. The journal abstract and the current arXiv landing page explicitly retain the conditional/experimental status. The author script works over finite fields and uses Gröbner-basis computations and auxiliary inverse variables for open conditions; this attempt inspected that script but did not execute it.

Here is the precise geometric mechanism, with the hypotheses isolated. Suppose an irreducible family of geometrically integral rational curves covers an irreducible n-fold X, and a general point of X lies on exactly one member. Let Z be an irreducible divisor with the same uniqueness property at its general point, not containing the corresponding general curve. Assume these incidences are represented by the stated family (not multiple parameters for one curve), and that the incidence section lifts to the normalization of the generic curve; for example, the generic incidence point can be required to be smooth on that curve. Then a dense open of Z maps rationally to the parameter space. Pull back the normalized generic family to k(Z). It is a genus-zero curve with the rational point supplied by that lifted section, hence is P¹ over k(Z). It follows that there is a dominant rational map Z×P¹ to X: its image contains a dense open of Z and also the associated curves, which are not contained in Z, so has dimension n.

If Z is unirational, this proves X unirational. If Z is rational and a general family member meets a suitable dense open of Z in exactly one point, the same map is generically one-to-one. The uniqueness of the curve through a general x fixes the family member, and uniqueness of its point in Z fixes the base point; normalization of that rational curve is generically one-to-one. In characteristic zero a dominant generically one-to-one rational map is birational. This proves the rationality conclusion under those additional hypotheses.

The divisors proposed by Mellit have the expected lower-dimensional quotient types. On E⁴,

D₄ = {p₂+2p₃+p₄=0}

is equivariantly isomorphic to E³ by freely choosing (p₁,p₂,p₃) and setting p₄=−p₂−2p₃. The isomorphism commutes with diagonal multiplication by the sixth root of unity because integer multiplication and addition are endomorphisms of E. Its quotient is consequently birational to X_{3,6}, whose rationality is a known theorem cited in COV. On E⁵,

D₅ = {p₁+ζp₃=p₅},

with ζ the relevant sixth root acting as a complex-multiplication endomorphism, is similarly equivariantly isomorphic to E⁴ and its quotient is birational to X_{4,6}. These are not arbitrary nonequivariant identifications.

The missing inputs are the characteristic-zero generic uniqueness statements for the actual specified curve families (H_144 in dimension four, H_13824 in dimension five), the necessary divisor-incidence statements (including a justified section on the normalized family for the version proved here), and the bounded-intersection hypotheses needed for birationality. We have not proved these inputs. In particular, finite-field experiments do not justify moving them into the conclusion. The theorem above is a conditional reduction, not an extra proof of the conjectures.

Two exact negative controls explain why the distinction matters:

1. For any fixed prime p, the family p z²+z−t=0 has exactly one reduced geometric solution in z for every t after reduction modulo p. Over Q(t), the polynomial is quadratic, with nonsquare discriminant 1+4pt. Its generic degree is two. Even exhaustive counts in that characteristic would not certify characteristic-zero generic degree one without a lifting argument controlling degree and flatness.
2. For a finite sample a₁,…,a_m of distinct complex parameter values, the dominant family z²=∏(t−a_i) has just one distinct geometric point over each sampled value and two over a general value. This second example concerns distinct-point counts and has nonreduced sampled fibers; it is not an attack on length calculations. It demonstrates why genericity must be proved rather than asserted.

Retained result: an explicit conditional proof mechanism, equivariant divisor identifications, and exact tests that reject two invalid experimental inferences. Exact gap: no generic curve-count certificate or replacement birational map has been supplied, so neither original question is answered.

## Boundary of every conclusion

Rationality implies unirationality, but a dominant map of degree two or six is not a birational inverse. Rational connectedness, Kodaira dimension −∞ and unirationality are different assertions. A nonrational/nonunirational generic fiber over a chosen subfield does not obstruct a rational/unirational total field over C. Results here neither establish nonrationality of X_4 or X_5 nor settle their stable rationality. No novelty or global-current-openness theorem is claimed.
