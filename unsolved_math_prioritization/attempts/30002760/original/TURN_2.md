# Approach 2: optimal-test residual minimization

## Aim and disposition

Change the variational norm to eliminate the convection-dependent condition number, then examine whether finite test spaces provide the required certificate. The ideal method is exactly best approximation. Stable discrete trial/test pairs alone do not make the computed residual a reliable error estimator.

## Proposition 2.1 (ideal isometry)

Let X and Y_0 be real Hilbert spaces and B:X -> Y_0' a bounded bijection with bounded inverse. Write b(w,v)=(Bw)(v). Let R_X:X -> X' be the Riesz isometry and T=R_X^-1 B*:Y_0 -> X. The adjoint B*:Y_0 -> X' is a bounded bijection, by Hilbert reflexivity and invertibility of B. Give Y_0 the equivalent norm ||v||_Y=||Tv||_X. Then T:Y -> X is an onto isometry and

b(w,v)=(w,Tv)_X.

For F=Bu and every w in X,

||F-Bw||_{Y'}=sup_{v!=0}|(u-w,Tv)_X|/||Tv||_X=||u-w||_X.

The upper bound is Cauchy-Schwarz; equality uses v=T^-1(u-w) when u!=w. Hence exact minimization of the full dual residual over any finite-dimensional U subset X gives the X-orthogonal projection of u onto U. Its best-approximation factor is one. All claims follow from the displayed identity, including the case u=w.

## Proposition 2.2 (finite test reduction)

Let U be nonzero and Y_T subset Y be finite-dimensional, Z=T(Y_T), and P_Z the X-orthogonal projection. The computable restricted residual is

r_T(w)=sup_{v in Y_T, v!=0}|F(v)-b(w,v)|/||v||_Y=||P_Z(u-w)||_X.

Assume beta=inf_{v in U, ||v||_X=1}||P_Zv||_X>0. There is a unique minimizer u_T in U of r_T. Indeed P_Z is injective on U, and P_Zu_T is the orthogonal projection of P_Zu onto the finite-dimensional space P_ZU. For every w in U,

beta ||u_T-w||_X <= ||P_Z(u_T-w)||_X <= ||u-w||_X.

The second inequality holds because P_Z(u_T-w) is the orthogonal projection of P_Z(u-w) onto P_ZU. The triangle inequality proves

||u-u_T||_X <= (1+beta^-1) inf_{w in U}||u-w||_X.

This deliberately non-sharp bound is sufficient here. If a Fortin map Pi:Y -> Y_T satisfies b(v,y-Pi y)=0 for v in U and ||Pi y||_Y <= C_F||y||_Y, then
||v||_X=sup_y |b(v,Pi y)|/||y||_Y <= C_F r_T(v;F=0),
so beta>=C_F^-1. This proves same-space quasi-optimality, not mesh-selection optimality.

## Proposition 2.3 (certificate gap, exactly)

For e=u-u_T, orthogonal decomposition gives

||e||_X^2=r_T(u_T)^2+||(I-P_Z)e||_X^2.

If a separately certified upper bound d_T >= ||(I-P_Z)e||_X satisfies d_T<=delta r_T(u_T), then
||e||_X<=sqrt(1+delta^2) r_T(u_T).

A finite test solve cannot certify its own tail merely from beta>0. Set X=Y=R^2, B=I, U=Y_T=span{(1,0)}, and u=(0,1). Here beta=1; the orthogonal Fortin projection has C_F=1; u_T=0; r_T(u_T)=0; and ||u-u_T||=1. The hidden tail is exactly one. This is a finite-dimensional counterexample to the proposed estimator inference, not to parabolic PDE solvability or the use of properly enriched test spaces.

## Remaining gap and credit

Optimal-test norms, residual minimization, Fortin operators, and double adaptivity are established techniques, including Cohen-Dahmen-Welper (2012) and Stevenson-Westerdiep (2021). The proofs above are elementary reconstructions and carry no novelty claim. For transport-dominated FEM one must still construct and evaluate the test norm or a robust equivalent, certify the unobserved residual, bound enrichment/solve costs, and prove the trial-mesh rate. Gantner-Smeets-Stevenson (September 2026) directly illustrates why test enrichment and its complexity need separate analysis; see SOURCE_SCOPE.md. None of those PDE-specific assertions is presumed here.
