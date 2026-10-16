# Independent derivation before consulting historical conclusions

Recorded: 2026-10-14T04:33:22.636613+00:00. Only the frozen manuscript and package inventory have been read so far. No first-review conclusions or archived historical proof/audit conclusions have been consulted.

## Exact hypothesis and falsification criterion

For each prime p and every existentially closed algebraically closed field expanded by a zero-preserving multiplicative group endomorphism theta, the unique pth-root map rho is parameter-free definable on the field, is a multiplicative endomorphism on the nonzero group, and is outside the evaluation image of Z[X]. A counterexample requires such an EC model and an integer polynomial P with P(theta)=rho, or a failure of the EC identification/embedding in the cited theory. A localization equality and characteristic-zero classification are not asserted.

## Independent algebraic argument

1. In an algebraically closed characteristic-p field, Frobenius is an injective and surjective field homomorphism. Its inverse has graph y^p=x. Uniqueness of the pth root proves multiplicativity, additivity, and theta(rho(x))=rho(theta(x)) for nonzero x; the zero convention supplies the last case. No additivity or injectivity of theta is used.
2. Suppose Q=sum b_i X^i is a nonzero integral polynomial. In an algebraic closure L of K(t_0,...,t_d), K^times and the multiplicatively independent t_0,...,t_(d-1) form an internal direct product. The homomorphism which extends theta on K^times and sends each t_i to t_(i+1) is therefore consistent. The divisible target L^times is injective as an abelian group, by the stated maximal-extension argument: the relation subgroup for adjoining one generator is either zero or nZ, and a root of the prescribed nth power resolves exactly the latter relation. Extending to all of L^times makes a legitimate T-extension regardless of torsion and whether theta is injective or surjective.
3. Q(theta_L)(t_0) is a nontrivial Laurent monomial, so is not 1. The positive/negative coefficient split writes this as an existential field formula without division. Existential closure transfers it into K. This proves injectivity of the evaluation map. When d=0 the subgroup is K^times, t_0 is still transcendental, and every nonzero b_0 is handled; empty products are 1.
4. If rho=P(theta), compose with Frobenius [p]. In the endomorphism ring, ring addition is pointwise multiplication, integer n is x->x^n, zero is x->1, and [p] is not zero. Thus (pP-1)(theta)=0. Faithfulness implies pP-1=0 in Z[X], impossible because p*a_0-1 is not divisible by p. This includes p=2, negative coefficients, zero and constant P, and all torsion elements. It does not confuse characteristic p of the field with characteristic of its group endomorphism ring.
5. [p] commutes with every group endomorphism; therefore its inverse rho is central. Clearing powers of p gives a ring homomorphism Z[1/p][X]->E, and faithfulness kills its kernel. This is an inclusion only, with strict containment of Z[theta].

## Independence and exact remaining checks

The proof uses no saturation, finite-field approximation, regularity assumption, classification theorem, or circular use of the desired exclusion. Classical inverse Frobenius and injectivity of the polynomial operator ring suffice. Every step above survived the first independent falsification attempt. Source verification must still confirm the original unrestricted question, the cited model-companion/EC statements, and source/credit boundaries. Archive, replay, metadata, priority search, source/PDF and layout checks remain. No novelty inference has been drawn.

## Adversarial boundary controls to require

- Arbitrary non-EC fields with theta=rho satisfy (pX-1)(theta)=0 and therefore invalidate a proof omitting EC.
- Finite fields have rho=[p^(n-1)] and cannot witness exclusion; finite tests must be labeled controls only.
- For the full multiplicative group other-prime torsion affects rational roots, but Frobenius is uniquely invertible and extends through the whole group. On the torsion quotient rho is just 1/p, so a quotient/vector result alone would not prove this full-group claim.
- Faithfulness must include constant integer polynomials, negative coefficients, empty products, and nonadditive/noninjective operators.

Provisional mathematical finding: no defect found in the exact scoped theorem; manuscript match and submission readiness remain unverified.
