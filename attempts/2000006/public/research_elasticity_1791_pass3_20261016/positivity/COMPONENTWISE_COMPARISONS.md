# Admissible one-component comparisons and inverse-Jacobian coercivity

E-6322, shared pass 3, 16 October 2026.

## 1. Exact scope

Let y be any global minimizer in the complete frozen finite-energy W^{1,6} class on the permitted smooth domain, with the prescribed complete trace. Let v be any member of the same class such that v_j=y_j almost everywhere for two of the three coordinate components. The component allowed to change is arbitrary. Write F_y=Dy, C_y=cof Dy and J_y=det Dy, and similarly for v.

Then the following quantitative inequality holds without any extra regularity, injectivity, or ordinary Euler equation:

I(v)-I(y) >= (a/32) integral |F_v-F_y|^6
             +(b/4) integral |C_v-C_y|^3
             +(c/2) integral |J_v-J_y|^2
             +d integral |J_v^{-1}-J_y^{-1}|^2.                 (1)

Every integral is over the entire original domain. The same assertion holds for a replacement supported in a subdomain, because such a replacement is a full-trace competitor. This is a genuinely minimizer-specific estimate in the original comparison class. It is an energy-gap coercivity statement, not an unconditional higher-integrability estimate.

## 2. Admissibility of the segment

For t in [0,1], put y_t=(1-t)y+t v. Its trace is g. Since only one gradient row changes, every matrix minor is affine in t. In particular,

Dy_t=(1-t)F_y+tF_v,
cof Dy_t=(1-t)C_y+tC_v,
det Dy_t=(1-t)J_y+tJ_v > 0 almost everywhere.

The convexity of the powers of the independent minor variables and of s -> s^{-2} on (0,infinity) gives

W(Dy_t) <= (1-t)W(F_y)+tW(F_v).

Thus the whole segment is in the full finite-energy class. There is no approximation by diffeomorphisms and no need to know that DW(Dy) is integrable. The same proof works for any fixed target direction e: v-y=e phi, because all minors are affine along rank-one matrix lines e tensor Dphi. The two-coordinate formulation is just the case e=e_i.

## 3. Midpoint proof and constants

For Euclidean vectors or matrices X,Y and any p>=2,

(|X|^p+|Y|^p)/2 - |(X+Y)/2|^p >= 2^{-p}|X-Y|^p.       (2)

Indeed convexity first bounds the left average below by ((|X|^2+|Y|^2)/2)^{p/2}; the parallelogram identity and (A+B)^{p/2}>=A^{p/2}+B^{p/2} finish the proof.

For u,v>0, the exact reciprocal-square deficit is

u^{-2}+v^{-2}-8/(u+v)^2
= (u-v)^2(u^2+4uv+v^2)/[u^2v^2(u+v)^2]
>= (u^{-1}-v^{-1})^2.                                  (3)

Apply (2) with p=6 to the gradients and p=3 to the cofactors. Twice the quadratic determinant midpoint gap is (c/2)(J_y-J_v)^2. Equation (3) gives the barrier contribution with coefficient d. Therefore

I(y)+I(v)-2I((y+v)/2)

is at least the right side of (1). Minimality gives I((y+v)/2)>=I(y), proving (1).

There is no differentiation through an infinite or nonintegrable stress. All quantities in this argument are finite energies of explicitly admissible maps.

## 4. Precise consequences

1. A minimizer is unique within any slice obtained by fixing two of its components and the complete trace. Indeed another equal-energy member of that slice has Dy=Dv by (1), and the trace eliminates the additive constant.
2. If v_n lies in that slice and I(v_n)->I(y), then its gradients converge to Dy in L^6, cofactors in L^3, determinants in L^2, and reciprocal determinants in L^2. No pointwise lower bound for J_y follows from this strong convergence.
3. If one constructs such a v with J_v>=j_0>0, then (1) gives the low-Jacobian repair-cost estimate

integral_{J_y<=j_0/2} J_y^{-2} <= (4/d)[I(v)-I(y)].       (4)

The estimate records what a successful controlled repair would have to overcome. The existence of a same-slice competitor with that lower bound and a useful quantitative energy gap is not asserted.

## 5. The localization bottleneck survives, in an exact transport form

For definiteness change the third component and hold y_1,y_2 fixed. Set

X=grad y_1 cross grad y_2,  J_y=X dot grad y_3.

A proposed replacement v=y+e_3 phi is admissible only if

J_y+X dot grad phi>0 almost everywhere,
(J_y+X dot grad phi)^{-2} is integrable.                 (5)

Here X belongs to L^3 and is divergence-free distributionally, but baseline finite energy supplies no smooth flow coordinates for X. For a cutoff interpolation toward a scalar comparison w_3,

v_3=(1-eta)y_3+eta w_3,

one obtains exactly

J_v=(1-eta)J_y+eta(X dot grad w_3)
       +(w_3-y_3)X dot grad eta.                         (6)

Thus positivity of both unlocalized row gradients does not control the last term. Even the simplest actual affine minimizer illustrates the problem: take y=(x_1,x_2,epsilon x_3), w_3=epsilon x_3+t, and a fixed smooth compactly supported eta with partial_3 eta=-1 on a small interior box. Then both endpoint maps have determinant epsilon, while the cutoff has determinant epsilon-t on that box. Taking epsilon=t/2 makes it negative for arbitrarily small t. The affine datum is allowed by the frozen target; the failed cutoff is not a competitor.

Nor can one simply demand X dot grad eta=0 to remove this term: for X=e_3, a smooth compactly supported eta with partial_3 eta=0 on a bounded domain is zero on each vertical interval component. A nontrivial local single-row repair must solve the positivity transport constraint, rather than treating it as a harmless cutoff error.

The componentwise convexity theorem therefore identifies a usable admissible class and quantitative coercivity, but it does not provide the missing Caccioppoli replacement, an L^{6+delta} estimate, or an all-boundary Jacobian lower bound.
