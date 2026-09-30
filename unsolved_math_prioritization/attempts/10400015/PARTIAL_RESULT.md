# Whitehead-double degree equality: normalization and the residual parity gap

**ID:** 10400015 / AMR-103-0015, Kidwell–Stoimenow Problem 1.15. **Status:** original target unsolved, 2/5 substantive approaches. Independent review pending. All known knot-theoretic ingredients below are credited; the additional statements are elementary algebraic diagnostics, not a realized knot counterexample or a novelty claim.

## Exact source and conventions

[Ohtsuki's problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed pp.391–392, asks whether every nontrivial knot K and Whitehead double W(K) satisfy

    deg_m P_W(K)(l,m) = 2 deg_z F_K(a,z) + 2.                    (1)

Degrees mean maximum exponent, not span. The unknot-normalized HOMFLYPT and Kauffman invariants are used. The adjacent remark records checks through eleven crossings and twist independence when the degree exceeds two; its update gives an alternating-knot upper bound. It does not assert a general theorem.

The full primary paper [Hermann Gruber, On knot polynomials of annular surfaces and their boundary links](https://arxiv.org/abs/math/0406106), published [online 1 July 2009](https://doi.org/10.1017/S0305004109002370), gives the Rudolph congruence, an annular reformulation, a composition formula, and the alternating odd-leading-coefficient criterion. Algebraic alternating links are covered. The universal equality is not proved there. The imported prior report was only open triage. Current searches located no authoritative general resolution; search absence is not a proof of continued openness.

## 1. Normalization conversion removes a spurious contradiction

Write P0 and F0 for unknot-normalized polynomials and PG, FG for Gruber's empty-diagram-normalized ones. Up to harmless changes of variables by signs or units, his definitions give

    PG = delta_P P0,       delta_P=(v^(-1)-v)/z,
    FG = delta_F F0,       delta_F=(a^(-1)+a)/x - 1.

Both coefficient rings are integral domains. Consequently for every nonzero polynomial

    deg_z PG = deg_z P0 - 1,       deg_x FG = deg_x F0.

The second equality holds because the x-degree of delta_F is zero with leading coefficient -1, not minus one. Thus Gruber's relation deg_z PG(W)-1=2deg_x FG(K) is exactly (1), after renaming the Alexander variable. It does not disprove (1). Multiplication by a framing monomial in v or a does not change these degrees. The degree conversions here are for knot/link values, not an assertion that the empty diagram has the usual unknot normalization.

## 2. Credited annular reduction and an explicit coefficient criterion

Let R_K(v,z) denote Gruber's zero-framed Rudolph polynomial. For a knot, R_K is the empty-normalized HOMFLYPT polynomial of the two-component annular boundary minus 1. His framing formula multiplies R_K by v^(2f), so its z-degree and coefficientwise parity are unchanged by integer framing f. His clasp skein formula is

    PG(W(K)) = v^2 delta_P + vz (R_(K,f) + 1)                  (2)

for the displayed clasp convention. If r=deg_z R_(K,f)>0, the second summand has top degree r+1>1 while the first has degree -1; no cancellation is possible. Hence

    deg_z P0(W(K)) = r+2.                                    (3)

This is the known reduction in Gruber's Lemma 7, with normalization made explicit. We do not silently extend it to r<=0, where subtraction of the constant or exceptional degrees must be handled separately. In particular we retain the d>0 hypothesis below; no general theorem about positivity of Kauffman degree for every nontrivial knot is used. For the opposite clasp, use the mirrored knot and the corresponding mirrored formula; mirroring changes coefficient-variable units/signs and preserves maximum Alexander degree.

Rudolph's congruence, in Gruber's Theorem 3, specializes for zero-framed knots to

    R_K(v,z) = FG_K(v^(-2),z^2)  (mod 2).                    (4)

Let d=deg_x FG_K>0. Suppose its degree-d coefficient is not zero modulo 2. The substitution a->v^(-2) is injective on Laurent polynomials over F2 and x->z^2 doubles degree. Equation (4) therefore gives

    deg_z R_K >= 2d.                                         (5)

An independently established upper bound deg_z R_K<=2d now proves equality and, by (3), the original degree formula for this K and all framings in this convention. This is a reproof of the algebraic mechanism behind the known odd-leading-coefficient criterion, not a new knot theorem.

For a nontrivial prime alternating c-crossing diagram, Gruber's Proposition 9 supplies the upper bound and his Theorem 17 combines it with parity; Theorem 18 covers algebraic alternating links. Their geometric proofs are cited, not independently reconstructed in this package. Gruber's discussion identifies 8_16 and 8_17 as early alternating knots whose top coefficient vanishes modulo 2; failure of this criterion is not a counterexample to (1).

## 3. What exactly is missing from the congruence argument?

The following propositions concern arbitrary Laurent polynomials, not knot realizations.

Let A=Z[v,v^(-1)] and let F in Z[a,a^(-1),x,x^(-1)] have degree d. Put S=F(v^(-2),z^2). Every R congruent to S modulo 2 has a unique form

    R = S + 2Q,       Q in A[z,z^(-1)].                       (6)

Uniqueness is because the Laurent polynomial ring over Z has no 2-torsion. For every exponent j>2d the z^j coefficient of R is 2 times that of Q. Therefore

    deg_z R <= 2d  iff  Q has no terms of degree >2d.          (7)

At degree 2d, its coefficient is S_(2d)+2Q_(2d). If S_(2d) has an odd coefficient, this expression cannot vanish. If S_(2d) is wholly even, cancellation is possible: take Q_(2d)=-S_(2d)/2. This proves precisely why parity supplies a lower bound in the first case but cannot settle the second case or supply the upper bound.

Concrete formal controls:
- F=x^d, R=z^(2d)+2z^(2d+2) obey (4) and have odd top coefficient in F, yet deg R>2d. Thus parity alone supplies no upper bound.
- For d>e>0, F=2x^d+x^e and R=z^(2e) obey (4), and R even satisfies the proposed upper bound, but deg R<2d. Thus an upper bound plus congruence cannot repair the even-leading-coefficient gap.

These pairs are not asserted to be Kauffman/Rudolph invariants of any link. Knot realizability imposes extra identities and topology; discarding those constraints cannot refute the original problem. The ring calculation identifies what an actual proof must add: a geometric upper-degree bound in the unrestricted case and an integer noncancellation mechanism where the top Kauffman coefficient is even.

## 4. Remaining target and verification

Neither an unrestricted upper bound nor an even-leading-coefficient noncancellation theorem is established. No actual knot counterexample is produced. General nonalternating companions and exceptional low-degree cases remain unresolved. The published composition reduction does not close the missing prime cases.

`verify.py` uses exact sparse integer Laurent polynomials to check normalization shifts, framing invariance, the congruence substitution, the odd-coefficient criterion and both formal failure mechanisms. These computations certify algebraic examples only; they do not compute a Whitehead-double invariant or verify a diagrammatic theorem. Primary-source pages 3 and 5 of Gruber were visually checked. All source PDFs remain outside the publication package.

The inherited native runtime was used without model or reasoning-setting changes; the exact model identifier was not exposed to this worker. No novelty or human peer-review claim is made.
