# Attempt 2: descend the completed projective, rather than the monoid witness

Write A=Z_(p)G, Ahat=Z_p G, and k=F_p. The completion Ahat is semiperfect. If P is a finite-dimensional projective kG-module, let Phat be a projective Ahat-lift and U=Q_p tensor Phat. Its ordinary character is denoted Psi_P.

## Rational descent lemma

The module P lifts to an A-lattice if and only if U has a QG-form: there is a finite-dimensional QG-module V with Q_p tensor_Q V isomorphic to U.

The forward implication follows by taking the rational generic fibre of an A-lift. For the converse, identify V with a dense rational subspace of U. Choose a Z_p-basis u_1,...,u_d of Phat, and choose rational vectors v_i in V sufficiently close to u_i that v_1,...,v_d are again a Z_p-basis of Phat. Density of Q in Q_p and invertibility of a matrix congruent to the identity modulo p justify this choice. Set L_0=sum_i Z_(p) v_i and

    L = sum_{g in G} g L_0.

Every summand lies in Phat. Thus L is a finitely generated, G-stable, torsion-free Z_(p)-module spanning V. Its completion contains Z_p L_0=Phat and is contained in Phat, so its completion equals Phat. Hence L/pL is isomorphic to P. The reduction criterion for projectivity (Johnston–Rumynin, Lemma 1.3) makes L projective over A. This proves the lemma. No approximation of a proposed nonprojective witness is involved.

## Exact character criterion

Fix an embedding of algebraic characteristic-zero character values into an algebraic closure of Q_p. Let m_Q(chi) denote the Schur index over Q of an absolutely irreducible ordinary character chi. A nonnegative ordinary character Psi is afforded by a QG-module exactly when:

1. its multiplicities are constant on each Gal(Qbar/Q)-orbit of chi; and
2. m_Q(chi) divides the multiplicity of chi.

This is the direct description of simple modules in the Wedderburn decomposition of QG: the character of a rational simple is m_Q(chi) times the sum of all distinct Galois conjugates of chi.

It follows from the descent lemma and the projective-cover criterion for semiperfectness that A is semiperfect exactly when every Psi_P, for P a projective indecomposable kG-module, satisfies those two conditions. The character of a projective p-adic lattice vanishes on p-singular elements and agrees with its reduction's Brauer character on p-regular elements. These standard projective-character facts also show that its character is determined by the Brauer character of P.

## Consequence for the target conjecture

Assume the positive-monoid condition of KOU-21.60. For each P there is a rational ordinary character theta_P whose restriction to p-regular elements equals the Brauer character of P. That restriction is rational-valued. Therefore Psi_P is rational-valued on every element of G: it has the same values on p-regular elements and is zero elsewhere. Its multiplicities are consequently constant on full Galois orbits, by character orthogonality.

Thus the only remaining obstruction in this reduction is the divisibility

    m_Q(chi) divides <Psi_P,chi>.

In particular, the conjecture holds for any finite group G for which every ordinary irreducible character has rational Schur index one. Here the monoid condition gives the Galois-orbit condition, the divisibility is automatic, and the lemma supplies actual projective Z_(p)G-lifts. The necessary direction is the already published one.

More generally it suffices that m_Q(chi)=m_Qp(chi) for every chi: U is already a Q_pG-module, so m_Qp(chi) divides its multiplicity, and equality supplies the needed global divisibility. Here m_Qp(chi) is computed for the fixed embedding of the character field in Qpbar.

This is a proved restricted-case argument within these notes, subject to independent audit. It is not a proof of the full question, and no claim of novelty is made. A possible counterexample must involve at least one genuine global-to-p-adic Schur-index drop and a PIM whose multiplicity fails the global divisibility test, despite the existence of some other positive rational character with the same p-regular restriction.

Outcome: a concrete arithmetic bottleneck, plus a complete proof under the Schur-index-one (or equal global/local index) hypothesis. The next attempt tests whether the missing divisibility follows from the monoid equations themselves.
