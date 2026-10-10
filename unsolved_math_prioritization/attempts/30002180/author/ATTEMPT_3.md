# Attempt 3: total curvature, bigness, and transverse directions

## Objective
Try to apply global positivity of the tautological line and the known canonical-ampleness theorem. Identify precisely whether its hypotheses follow.

## What the inspected prior theorem says
Golota, arXiv:1708.02866v3, Theorem 1.0.2, proves ampleness of K_X for smooth projective X with nondegenerate negative **total** k-jet curvature. Question 1.0.1 in that manuscript asks for the version with directed negativity. Its introductory discussion explicitly separates partial positivity from existence of jet sections. We use this theorem only under its stronger hypothesis. No claim that this manuscript resolves the original question is made.

Under that stronger hypothesis, c1(T_X)_R≠0 follows immediately: an ample K_X has a positive curvature representative beta, so integral_X c1(K_X)^n=integral_X beta^n>0. If c1(T_X)_R=0 this integral would vanish.

## Retained bigness-to-section lemma
Let Y=X_k and L=L_k^*. If L is big, then for any ample A on X there is an m>0 with
H^0(Y,L^m tensor pi_{k,0}^*A^-1)≠0.

Proof using the standard Kodaira-lemma characterization of bigness: take r>0, an ample line bundle B on Y, and an effective divisor D with L^r=B tensor O_Y(D). For sufficiently large q, B^q tensor pi_{k,0}^*A^-1 has a nonzero section. For completeness this last fact follows from Serre vanishing and the Hilbert polynomial, whose leading term is (B^dim Y)/(dim Y)! times q^dim Y>0. Multiply such a section by the q-th power of the canonical section of O_Y(D). This yields the asserted section for m=rq.

By the standard invariant-jet direct-image identity pi_{k,0*}O_{X_k}(m)=E_{k,m}T_X^*, this is an ample-negatively-twisted invariant jet differential. Attempt 4 proves that no such section exists when c1(T_X)_R=0. This is a second route to the target under the additional bigness assumption, without needing canonical ampleness.

## Exact pointwise obstruction
In dimension n>=2, N=dim X_k=n+k(n-1)>rank V_k=n. At a point split C^N=V⊕W with dim V=n. The Hermitian form
Q=I_V⊕(-M I_W), M>0,
is strictly positive on V and negative on W. Therefore positivity on V does not imply total positivity. For n=2,k=1,M=3, its eigenvalues are (1,1,-3), its trace is -1, and its determinant is -3. Its top wedge has the wrong sign for an everywhere-positive curvature form. The verifier checks these exact values and ranks for several tower dimensions.

This local algebraic model is not claimed to be a globally realized curvature metric on the Semple tower or a counterexample to the conjecture. It refutes only the proposed pointwise inference. In particular vertical positivity cannot automatically control transverse horizontal directions; V_1 contains the vertical directions and just one horizontal line at each (x,[v]).

## Exact gap
We have no argument upgrading alpha|V_k>0 to total positivity, a Kähler current in c1(L_k^*), or bigness of L_k^*. Modifying h by a weight adds an exact dd^c term, whose uncontrolled transverse components cannot simply be declared positive. Even granting bigness, the nondegeneration requirement is a separate issue for the ampleness theorem. None of these added hypotheses is present in the original question.
