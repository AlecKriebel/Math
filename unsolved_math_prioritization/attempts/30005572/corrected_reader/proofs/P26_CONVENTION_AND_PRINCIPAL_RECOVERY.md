# Convention checks and recovery of the accepted principal formula

Shared PASS 4; clarification of the frozen nonprincipal theorem. This file does not change its operator or hypotheses.

## 1. A pointed transport gives the exact central double coset

At a q-free level A, a simultaneous q-isogeny between the relevant products has local elementary divisors (q,q) at q and is a lattice isomorphism everywhere else. Assemble its target into the fixed standard determinant-class component by an O-linear lattice isomorphism which carries the marked point to the fixed standard point, with the coefficient/Galois factor already tracked in GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md.

At a prime dividing A, the class representative ideles are 1 and the marked torsion vector is the standard second vector. The marking condition says exactly that the resulting matrix has bottom row (0,1) modulo A, hence belongs to the strict level group there. At q, the level group is GL_2(O_q), and elementary divisors (q,q) say that the matrix belongs to nu I_2 times GL_2(O_q), the central double coset. At every remaining prime it is an integral lattice isomorphism, so belongs to the maximal compact group. These local conditions identify the assembled adelic double coset with U_A z_q U_A, not with a diamond-modified coset.

The marking condition must apply to the **composed map**, rather than asserting that an arbitrary isomorphism on its own is congruent to 1. One can achieve this by prescribing the appropriate target primitive vector modulo A. The determinant-one correction from Section 2 of the main note supplies that prescription. Any two such identifications differ by the strict level group, so the result is independent of the identification. The regular-coboundary comparison in that section permits this change of moved primitive before specialization.

This is also the local verification behind the source's factorization Z_q=<q>[q]^*: the diamond factor cancels the second-coordinate scalar on A-torsion. Omitting that cancellation would indeed produce a diamond-modified operator.

## 2. Principal local inverse versus rational inverse

Suppose q=(pi), and let beta=diag(pi,1) as a rational matrix. At q, beta differs from y=diag(nu,1) by diag(pi/nu,1), whose first entry is a local unit. At every other finite prime beta is diag(pi,1) with pi a unit. All these correction matrices belong to U_1(N), including at every tame prime dividing M, because their bottom row is exactly (0,1). Thus the finite-adelic double cosets of beta and y agree. The same check works for beta^{-1} and y^{-1}.

The rational matrix alpha=diag(1,pi) is pi times beta^{-1}. Multiplication by the **global rational** scalar pi acts trivially on the symmetric space and does not change the conjugation or transfer subgroup. Therefore alpha gives exactly the accepted principal inverse-U convention. This uses the full rational scalar, with its tame components included. It does not identify the local central idele z_q with that global scalar.

## 3. The two first-step norm formulas differ by the declared marking change

Let A=M be proper and q-free. Keep the same low point P_A. The old principal proof chooses P_old with pi P_old=P_A. Its A-primary component is pi^{-1}P_A.

The new recursion is phi_1(P_new)=sigma(P_A), where phi_1 agrees with sigma on A-torsion. Since phi_1 is an isomorphism on A-torsion, the A-primary component of P_new is P_A. Thus

    P_new=[d]P_old,   d=pi mod A,

for an element d which is a unit modulo Aq. Its residue at q is selected to match the chosen primitive q-component; CRT permits this independently of the congruence modulo A. Choose d'=d modulo Aq and d'=1 modulo f, and put tau=R_{Aqf}((d')). The marking formula gives

    g_new,Aq=tau g_old,Aq.

The restriction of tau to L_A is R_A((pi)). Hence, on the descended arithmetic norm,

    Cor f_new,Aq=R_A((pi)) Cor f_old,Aq.                 (P1)

For the upstairs comparison, choose the factorwise model isomorphism which identifies the principal CM q-isogeny phi_r with multiplication by pi. Its marked-point identity sends sigma(P_A) to pi P_A. Exact product-model transport therefore gives

    sigma g_A=kappa g_A,

where kappa=R_{Af}((a)), a=pi modulo A and a=1 modulo f. This equality does not assume arithmetic descent at A. It is simply Galois/model transport followed by the principal torsion marking rule.

Choose beta_r=diag(pi,1); the degeneracy D is then exactly the accepted old one. The new formula

    Cor g_new,Aq=sigma g_A D-g_A F

becomes, after undoing tau (whose restriction on these values is kappa),

    Cor g_old,Aq=g_A D-kappa^{-1}g_A F.                 (P2)

At an admissible lower level this is the source arithmetic formula with kappa restricted to L_A; at a nonadmissible lower level it is exactly the upstairs formula used in PASS 3. Thus the inverse Artin factor in the previously accepted principal theorem is recovered, rather than silently removed.

## 4. Scope

These checks use ideal Artin symbols only at moduli prime to the relevant ideal. The chosen sigma at a bad modulus is still an actual Galois lift, and the theorem still concerns the inverse-U double coset. No relation for the integral opposite local operator is asserted.
