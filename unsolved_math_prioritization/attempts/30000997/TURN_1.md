# Author turn 1 — local geometric separation

2026-10-03 06:24 UTC. Status: partial; global conjecture unresolved. No novelty claim. This is one substantive author turn. Completion estimate for full global target: 5%, reflecting a rigorous local diagnostic rather than proximity to a global proof.

## Exact local statement

On M=R² with metric

g = dx² + f(x)² dy²,  f(x)=(1+x²)^(-1/2),

there is a sufficiently small geodesically convex neighborhood U of (0,0) such that c=d_g²/2 is smooth and strictly A3w on U×U but fails NNCC there. The ambient metric is smooth, analytic and complete. It does **not** satisfy global A3w, so this is not a counterexample to the main global target.

## Jacobi calculation

Fix a point p on a smooth Riemannian surface. For small v in T_pM let

A(v)(u,u)=Hess_p[d_g(·,exp_p(v))²/2](u,u).

The Hessian is taken in the first variable with its second endpoint fixed; v is then varied in the fixed tangent space. With w in T_pM, the unnormalized MTW expression in this tangent representation is

S(v;u,w)=-D²_v A(v)(u,u)[w,w].

The endpoint tangent vector in the original tensor is Dexp_p(v)w. Its null condition is g_p(u,w)=0. This identity follows by differentiating the identity -D_p c(p,exp_p(v))=v and the cost-segment definition; it includes the third-derivative cancellation in the coordinate tensor. It does not permit replacing endpoint orthogonality by ordinary parallel-transport orthogonality.

Put r=|v| and e=v/r. Along the unit-speed radial geodesic, solve

C''+K(s)C=0, C(0)=1,C'(0)=0;
J''+K(s)J=0, J(0)=0,J'(0)=1.

The transverse Hessian eigenvalue is H(v)=r C(r)/J(r), while the radial eigenvalue is 1. With K_j the j-th covariant directional derivative of Gaussian curvature along e at p, Taylor division gives

H(v)=1−K_0 r²/3−K_1 r³/12−(K_2/60+K_0²/45)r⁴+O(r⁵).

Consequently

A(v)(u,u)=|u|²−[K(p)/3+(∇_v K)(p)/12+(∇²_{v,v}K)(p)/60+K(p)²|v|²/45] |u∧v|²+O(|u|²|v|⁵).

The remainder is a Taylor remainder with two differentiable v-derivatives when the metric is smooth; its twice differentiated remainder is O(|v|³). The displayed formula can alternatively be obtained directly by the smooth Taylor expansion of A at zero, avoiding division by r at the origin.

At p=(0,0), let e1=∂x and e2=∂y. Here f=1, f'=0, so these are orthonormal and the relevant Christoffel symbols vanish. Direct differentiation gives

K(x)=−f''(x)/f(x)=(1−2x²)/(1+x²)²,
K(p)=1, ∇K(p)=0, (∇²K)_p(e1,e1)=−8, (∇²K)_p(e2,e2)=0.

For v=a e1+r e2 and u=w=e1, |u∧v|²=r² is independent of a. Therefore

S(r e2;e1,e1)=[K_xx(p)/30+2K(p)²/45]r²+O(r³)=−2r²/9+O(r³).

Reflections x↦−x and y↦−y are isometries fixing p, so the analytic expression is even in r; the remainder is in fact O(r⁴). For every sufficiently small nonzero r, S is negative. The pair is non-null: g_p(e1,e1)=1.

## Strict A3w on a small product neighborhood

At v=0 the same expansion gives S(0;u,w)=(2/3)K(p)|u∧w|². For unit u⊥w in a surface this is 2K(p)/3. The curvature is positive near p, and the compact unit orthogonal-pair bundle and smooth dependence of S give a uniform positive bound for source points and sufficiently short endpoints near p. Shrink to a relatively compact strongly convex normal neighborhood U so every connecting minimizer stays in the coordinate neighborhood. Then the squared-distance cost is smooth and all its normalized null pairs have S>0 on U×U. Twist and mixed-Hessian nondegeneracy hold there as usual for the normal exponential map. Since exp_p(r e2) belongs to U for sufficiently small r, the negative full pair above belongs to the same cost domain.

This establishes the local geometric separation; it is not merely an arbitrary algebraic curvature tensor.

## Completeness and failure of the global antecedent

A finite-length curve has bounded total x-variation. In a bounded x-strip f has a positive lower bound, so finite length also bounds total y-variation. Thus no finite-length curve escapes all compact subsets; the metric is complete. Equivalently, metric Cauchy sequences stay in a strip where the metric is uniformly equivalent to the Euclidean one.

However K(1)=−1/4. At a point with x=1, the diagonal MTW expression for a unit orthogonal pair is −1/6. Thus this complete surface violates A3w and is explicitly disqualified as a global counterexample.

## Audit and exact remaining gap

Symbolic recurrence for the scalar Jacobi equation independently checked coefficients 1/3, 1/12, 1/60 and 1/45; the resulting local MTW coefficient is −2/9. This is an algebraic check, not independent proof review. A global counterexample would need a different complete metric with A3w everywhere off-cut, retaining a negative non-null pair. The next route is to understand whether positive-curvature compact completions of this local mechanism force a weak-MTW violation elsewhere.
