# Independent initial derivation — before submitted proof

Recorded 2026-10-05T15:43:09.940089+00:00. This record precedes any reading of PUBLIC_TURN_2.md or previous reviewer reports. Completion estimate: 35% of the assigned surface audit; no final certification.

## Claim and hypotheses
Over an algebraically closed field of arbitrary characteristic, let X be a smooth integral projective surface, H a nef Cartier divisor, H^2=e>=2, and C an integral effective divisor linearly equivalent to H. Claim: h^0(X,omega_X(2H))>0.

## Independent route
Write p_g=h^2(O_X)=h^0(omega_X), q=h^1(O_X), a=p_a(C). If p_g>0, multiply a nonzero canonical section by the square of the section cutting C; integrality ensures a nonzero section of omega_X(2H). Thus the only delicate case is p_g=0.

Riemann–Roch and adjunction give chi(omega_X(2H))=chi(O_X)+2e+K_X.H=(1-q+p_g)+2e+(2a-2-e)=p_g-q+e+2a-1. Serre duality gives h^2(omega_X(2H))=h^0(O_X(-2H))=0: a nonzero effective divisor in |-2H| would meet nef H in -2e<0. Consequently h^0(omega_X(2H))>=p_g-q+e+2a-1.

An unqualified substitution q=dim Alb(X) is invalid in positive characteristic: Pic^0 may be nonreduced. In the remaining case p_g=0, however H^2(O_X)=0, so deformation obstructions of line bundles vanish; Picard is smooth and q=dim Pic^0=dim Alb. This needs primary-source confirmation.

The normalization Cbar must generate Alb(X): after translating a base point, if its image generated a proper abelian subvariety B, quotienting by B would give f:X->A/B nonconstant with f(C) a point. Pullback M of an ample divisor has M nef and M.H=0. Algebraic Hodge index (H^2>0) plus M^2>=0 forces M numerically zero. But a nonconstant projective morphism has some curve mapping nonconstantly, on which M has positive degree. Contradiction. Thus Jac(Cbar)->Alb(X) is surjective; q<=g(Cbar)<=p_a(C)=a. The RR lower bound is at least e+a-1>=1.

## Boundary and attempted attacks
The H^2>=2 threshold is sharp as stated: X=P^2, H=O(1) has e=1 and omega_X(2H)=O(-1) with no sections. On P^1xP^1 with H=(1,1), e=2 and omega_X(2H)=O, equality gives one section. On a ruled surface over a curve of genus g, normalization genus of a nonvertical C is at least g even for inseparable maps (purely inseparable maps over a perfect field are Frobenius twists, preserving genus); nevertheless this classification route is not needed. Singular C only improves a>=g(Cbar). H need not be ample/basepoint-free. Nonreduced Picard is explicitly handled by the p_g split, not dismissed. No Kodaira vanishing, characteristic-zero Hodge theory, or surface classification is used.

## Remaining verification
Check the primary-source facts Picard smoothness when H^2(O_X)=0, the Albanese/Jacobian factorization and abelian quotient, characteristic-free algebraic Hodge index with nef H of positive square, and existence of a curve detecting a nonconstant projective map. Then compare the submitted lemmas and the transfer to a possibly nonnormal surface. No prior proof or reviewer has been read.
