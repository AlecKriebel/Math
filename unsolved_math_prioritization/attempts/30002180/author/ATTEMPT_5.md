# Attempt 5: directed currents and flat regular jets

## Objective
Construct a directed current whose pairing with the tautological curvature must be both zero and positive. Test whether c1(T_X)_R=0 is enough for this construction.

## Retained theorem
No positive-dimensional compact complex torus A=C^n/Lambda has nondegenerate negative k-jet curvature for any k>=1. The same is true for any compact complex manifold covered by a torus by a finite étale map.

## Direct proof for every jet order
Fix a nonzero vector v∈C^n and its translation-invariant holomorphic vector field on A. Set j_0=id_A. Recursively define j_r:A→X_r by

j_r(a)=(j_{r-1}(a),[d j_{r-1}(v_a)]).

Each map is holomorphic, and d j_{r-1}(v) is nowhere zero, since its projection to T_A is v. It is exactly the r-jet direction of the affine holomorphic germ t→a+tv. Hence j_r(A)⊂X_r^reg and d j_r(v)∈V_r. Further, j_r^*L_r is holomorphically trivial, with the global frame e_r=d j_{r-1}(v).

Suppose the metric in the question exists at level k. Since j_k(A) misses its degeneration set, the logarithm of the squared norm of this frame is a globally defined locally bounded function phi on A. With dd^c chosen to match the dual curvature, j_k^*alpha=dd^c phi. Its restriction in the v direction satisfies

(dd^c phi)(v,bar v)>=epsilon omega_k(d j_k(v),overline{d j_k(v)})>=c>0

as a distribution; the positive uniform c exists by compactness and nonvanishing of d j_k(v).

Integrate against translation-invariant volume on A. A constant-direction second derivative of a periodic distribution pairs to zero with the constant test function 1: by the definition of distributional differentiation it equals phi paired with that derivative of 1, which is zero. This contradicts the lower bound c times the positive total volume. Thus the metric cannot exist. The proof works for merely locally bounded restricted potentials, so no unwarranted smoothness assumption was introduced.

For a finite étale cover p:A→X, the derivative identifies T_A=p^*T_X and inductively identifies the Semple towers by base change. Pullback preserves the curvature inequality, regular-jet locus and nondegeneration. A metric on X would therefore give the excluded one on A. This proves the quotient statement.

## Current formulation
The functional T_v(eta)=integral_A eta(v,bar v)dV on smooth (1,1)-forms, with the usual positive i convention, is a positive current of bidimension (1,1). It is closed: in constant coordinates all coefficients of its density are constant, so integration by parts kills the exterior derivative. Its pushforward under j_k is V_k-directed, supported entirely on regular jets, and pairs to zero with u_k because j_k^*L_k is trivial. Positivity along V_k would make that pairing positive. This recasts the same rigorous proof without claiming a current on a general Ricci-flat manifold.

## Relation to the current literature
Dinh–Nguyen–Vu, arXiv:2607.07054v1, Theorem 7.6, proves that the exact nondegenerate jet hypothesis yields positive geometric hyperbolic indices. Those indices concern lifted currents and tautological classes. They are not c1(T_X), and their positivity is not stated there as canonical bigness or as c1(T_X)_R≠0. The arXiv record labels the manuscript a first draft; this packet does not certify its full proof.

## Why Ricci-flatness does not finish this route
The vanishing real first Chern class yields a Ricci-flat Kähler metric, not a flat holomorphic tangent connection or a nonzero translation field. Without a global holomorphic affine-jet section j_k, the construction above cannot be transferred.

An exact algebraic negative control makes the lost information visible. In complex dimension two set
R_{1 bar1 1 bar1}=R_{2 bar2 2 bar2}=1,
R_{1 bar1 2 bar2}=R_{2 bar1 1 bar2}=R_{1 bar2 2 bar1}=R_{2 bar2 1 bar1}=-1,
and all other components zero. It obeys the Kähler curvature symmetries and has Ricci contraction zero, but
R(v,bar v,v,bar v)=|v_1|^4+|v_2|^4-4|v_1|^2|v_2|^2,
which is 1 at v=(1,0) and -1/2 at v=(1,1)/sqrt(2). Thus trace-zero curvature does not imply zero curvature or one sign on every line. This is an algebraic model, not a claimed compact Ricci-flat example with the prohibited jet metric. The verifier checks every symmetry and contraction exactly.

## Exact remaining gap
For arbitrary projective X with c1(T_X)_R=0, construct a nonzero V_k-directed closed (or suitably dd^c-closed) current, with an admissible regular-jet lifting and nonpositive tautological pairing, to contradict the jet metric. Neither Ricci-flatness alone nor the inspected hyperbolic-index theorem supplies that construction. The torus case and the algebraic trace control establish the scope of this attempt, not the original all-manifold assertion.
