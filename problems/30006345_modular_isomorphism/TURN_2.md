# Turn 2: the center's radical layers recover Heisenberg-product parameters

Problem 30006345. Second substantive author turn. **Original all-field question unresolved, 2/5 turns completed.** The positive result below assumes that **both** groups belong to the displayed family. It does not prove that a group with an isomorphic algebra must belong to that family.

## 1. Theorem and invariant

Fix an odd prime p. Write H_e=H(F_(p^e)) for the three-coordinate Heisenberg group of turn 1, where e≥1. Let

    G=C_p^a × ∏_(i=1)^u H_(e_i),
    G′=C_p^b × ∏_(j=1)^v H_(f_j),

with a,b≥0 and all field degrees positive. For every field k of characteristic p,

    kG ≅ kG′ as k-algebras  ⇒  a=b and {e_i}_i={f_j}_j as multisets  ⇒  G≅G′.

Empty products may be allowed; the source's nonabelian case has at least one H factor. The invariant used is the dimension of kG together with the **radical Hilbert polynomial of the center algebra** Z(kG). This is not the Hilbert polynomial of the augmentation filtration on kG, nor the filtration induced on its center from that augmentation filtration.

Put A(t)=1+t+⋯+t^(p−1). If r=Σ_i e_i, then

    L_G(t) = Σ_(j≥0) dim_k(rad(Z(kG))^j / rad(Z(kG))^(j+1)) t^j
           = A(t)^a ∏_i [ A(t)^(e_i) + (p^(2e_i)−1)t ].             (1)

Here rad^0 is Z(kG), so the constant coefficient is1. All coefficients are nonnegative integers, not elements of k. The pair (|G|,L_G) determines the asserted parameters constructively. This restores the distinction lost by the scalar-extended associated graded algebra in turn 1, for the entire stated product family.

## 2. Center algebra of a single factor

Let q=p^e and Z=Z(H_e), an elementary abelian group of order q. Turn 1's explicit commutator law shows that every noncentral conjugacy class is a whole coset gZ and there are q²−1 such classes. Set N=Σ_(z∈Z)z in the group algebra. The class-sum basis therefore gives a vector-space decomposition

    Z(kH_e)=kZ ⊕ V,

where V has basis gN for the q²−1 nonidentity cosets gZ. No element of this basis has support on Z, so the sum is direct. Multiplication satisfies

    r v = ε(r)v  (r∈kZ, v∈V),       V²=0.                       (2)

Indeed zN=N for z∈Z, and N²=qN=0 in characteristic p. Products of any two elements gN,hN are ghN²=0, since N is central. This remains true when gh lies in Z. Thus (2) specifies the center algebra as the square-zero extension of kZ by a trivial augmentation module of dimension q²−1.

Choose an F_p-basis of Z. Then

    R_e=kZ ≅ k[T_1,…,T_e]/(T_1^p,…,T_e^p),

by sending T_i to z_i−1. The monomials with exponents0,…,p−1 form a basis: the binomial changes from the group basis are invertible triangular matrices. Its augmentation ideal m_e=(T_1,…,T_e) is nilpotent and the residue field is k.

From (2), the unique maximal ideal of the center algebra is m_e⊕V, its square is m_e², and every higher power is m_e^j. Consequently the radical Hilbert polynomial is

    h_e(t)=A(t)^e+(p^(2e)−1)t.                                  (3)

This calculation uses the multiplication of the **full** group algebra. Taking a center after passing to the associated graded algebra would be a different operation; no interchange of these operations is assumed.

## 3. Direct products and the correct tensor filtration

For finite-dimensional k-algebras B,C, one has Z(B⊗_k C)=Z(B)⊗_k Z(C). To check this without a splitting-field hypothesis, expand an element in a k-basis of C. Commuting with every b⊗1 forces each coefficient into Z(B); then expand in a basis of Z(B) and commute with 1⊗c to force the other coefficients into Z(C).

For finite-dimensional commutative local k-algebras with residue k and maximal ideals m,n, the radical of their tensor product is m⊗C+B⊗n. This ideal is nilpotent and the quotient is k, which proves the assertion. Its powers have the usual convolution filtration. Choosing vector-space complements successively to the powers of m and n gives a tensor basis adapted to that filtration, proving that radical Hilbert polynomials multiply. This argument does not require an algebraic closure or a perfect coefficient field.

Apply these observations to k(G_1×G_2)=kG_1⊗kG_2, to (3), and to the elementary abelian factor with Hilbert polynomial A(t)^a. This proves (1).

## 4. Reconstruction, including elementary abelian factors

Let n=log_p(dim_k kG)=a+3r. Because p is odd and e≥1, e(p−1)≥2. Thus h_e is monic of degree e(p−1): its extra linear term does not change the leading term. Formula (1) is monic of degree

    D=(p−1)(a+r).

Hence s=D/(p−1)=a+r is recovered from L_G, and

    r=(n−s)/2,          a=(3s−n)/2.                             (4)

This includes r=0, when G is elementary abelian. No cancellation of direct factors is assumed; these formulas reconstruct their parameter for the stated family. The separate all-field elementary-abelian cancellation theorem credited in SOURCE_GATE.md is compatible background, not a needed missing step.

Reverse the Hilbert polynomial: L*(t)=t^D L_G(t^−1). Since A is palindromic, define

    d_e=e(p−1)−1,      c_e=p^(2e)−1,
    h_e*(t)=A(t)^e+c_e t^(d_e).

All d_e are positive and strictly increase with e. As a formal power series over the integers,

    L*(t)/A(t)^(a+r) = ∏_e (1+c_e t^(d_e)/A(t)^e)^(m_e),        (5)

where m_e is the multiplicity of e. The division is legitimate because A has constant coefficient1. Suppose multiplicities below e have already been recovered and their factors on the right have been divided out. The coefficient of t^(d_e) in the remaining series is exactly m_e c_e: higher-index factors start in larger degrees, and powers of the e-factor have first nonconstant coefficient m_e c_e. Its other terms start after d_e. Thus m_e is recovered by dividing that integer coefficient by the positive integer c_e.

Continue up to e=r; no factor has index larger than r. This determines the multiset uniquely. Formal division by previously found factors uses units with constant coefficient1, so there is no pole, convergence or characteristic-p division issue. The integer coefficients are dimensions and are not reduced modulo p. Equations (4)–(5) prove the theorem.

An equivalent finite implementation repeatedly removes the reversed polynomial factors h_e* from L*, updates the remaining sum of field degrees, and computes the next required coefficient after division by the corresponding power of A. For input known to have the stated form, every removal is exact. We do not claim that an arbitrary algebra passing these numerical tests must be a Heisenberg product.

## 5. Scope and remaining difficulty

This proves that finite-field Heisenberg products, with any elementary abelian factors, cannot furnish an extension-field collision **against another member of the same family**. It is stronger than comparing center dimensions alone: it uses all radical layers of the center and a triangular recovery of field-degree multiplicities. It does not recover a general alternating commutator map and does not establish the family membership of an arbitrary group H from kH≅kG.

The group law, conjugacy-class basis, truncated polynomial algebra and radical tensor arguments are classical. Formula (1) and the explicit parameter-recovery proof are supplied here without historical novelty certification. Targeted current searches for modular isomorphism, Heisenberg direct products and center radical layers did not recover an exact matching primary statement; this limited search is not evidence of priority. The known prime-field Passi–Sehgal theorem and current all-field results remain separately credited in SOURCE_GATE.md.

The exact supplementary checker constructs small groups and their class-sum multiplication directly, computes center radical dimensions, and tests recovery on bounded parameter lists. It does not prove the theorem by a finite scan. The written argument covers every odd p, every field k of characteristic p, and arbitrarily many factors, under the displayed family assumptions.

Subjective completion estimate for the original unrestricted question: 2%. Completed author turns:2/5. Main unresolved step: move beyond the special-family hypothesis and recover full prime-field commutator data from an arbitrary all-field group-algebra isomorphism.
