# Attempt 4: a central double cover produces a counterexample candidate

The obstruction from Attempt 3 suggests using characteristic two, where a quaternionic ordinary constituent can be invisible in the modular central quotient. Take

    G = SL(2,5), p=2, Z={I,-I}, H=G/Z=A_5.

Let k=F_2. This attempt produces a full candidate counterexample; exact arithmetic and independent checking are required before certification.

## Central doubling lemma

For a finite group with central subgroup Z=<z> of order two, put t=z-1 in kG. Then t^2=0, kG/tkG=k(G/Z), and multiplication by t identifies kG/tkG with tkG. Indeed, choose one representative for each coset of Z; on its two-element basis {g,zg}, t has kernel and image both spanned by g+zg.

Let P be a projective kG-module. As a direct summand of a free module, it inherits the identity ker(t:P->P)=tP. Hence multiplication by t gives a G/Z-module isomorphism

    P/tP -> tP.

If P is a projective indecomposable, then P/tP is the corresponding projective indecomposable for k(G/Z). For example, represent P=kG e with e primitive; the ideal (t) is nilpotent, so primitivity descends and idempotents lift. Thus, in G_0(kG),

    [P]=2[Infl(P/tP)].

This proves that the positive rational-reduction condition passes from the quotient to any central double cover in characteristic two. Inflate rational quotient witnesses and double them. No statement that coinvariants induce a map on G_0 is used.

## All PIMs meet the positive condition

For A_5 over F_2, denote the three F_2-simple modules by S_1 (dimension one), T_4 (the Frobenius orbit of the two absolutely irreducible two-dimensional simples), and S_4 (the absolutely irreducible four-dimensional module). The verified primary paper of Johnston–Rumynin, Example 3.4, gives

    [P_H(S_1)]=4[S_1]+2[T_4],
    [P_H(T_4)]=4[S_1]+3[T_4],
    [P_H(S_4)]=[S_4].

Rational A_5 irreducibles V_1,V_4,V_5 of the indicated dimensions have reductions

    d(V_1)=S_1, d(V_4)=S_4, d(V_5)=S_1+T_4.

Consequently the three G-PIM classes are respectively the reductions of the following actual rational G-modules (all inflated from H):

    4 V_1 + 4 V_5,
    2 V_1 + 6 V_5,
    2 V_4.

Their dimensions are 24,32,8. In particular, the hypothesis holds for EVERY projective indecomposable over F_2, including the nonsplit four-dimensional T_4 case.

## The eight-dimensional PIM cannot lift

Let E=P_G(S_4). Its Brauer character on odd-order elements is twice that of the quotient degree-four character chi_+ of A_5. A lift to Z_(2)G, if it existed, would be projective, and its ordinary character Psi would vanish on all even-order elements. This determines Psi.

The ordinary characters chi_+ (inflated quotient) and chi_- (faithful) of G have values listed by element order below. The two order-five classes and two order-ten classes have identical values in these rows:

    order        1    2    3    4    5    6    10
    class total  1    1   20   30   24   20    24
    chi_+        4    4    1    0   -1    1    -1
    chi_-        4   -4    1    0   -1   -1     1

Therefore Psi=chi_++chi_-. The faithful chi_- is irreducible and quaternionic. It is the symmetric cube of the natural complex degree-two representation of the binary icosahedral group; equivalently it is the faithful degree-four row in the character table of SL(2,5). Its Frobenius–Schur indicator is explicitly

    (4+4+20-120-24+20-24)/120 = -1.

Every rational representation is a real representation after extending scalars to R, and every quaternionic complex irreducible occurs with even multiplicity in the complexification of a real representation. But chi_- occurs in Psi exactly once. Hence no rational representation affords Psi, so E cannot lift. It follows that Z_(2)SL(2,5) is not semiperfect.

If these steps withstand the forthcoming exact checks, this disproves the converse in KOU-21.60. It also explains why merely finding a positive rational module with the right Brauer character is inadequate: the witness 2V_4 has the right composition vector but misses the quaternionic generic-fibre constituent forced on a projective lift.
