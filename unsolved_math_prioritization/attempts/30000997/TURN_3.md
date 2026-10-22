# Author turn 3 — exact global equatorial slice

2026-10-03 06:36 UTC. Partial result only. Completion estimate toward the unrestricted conjecture: 10%; the missing off-equator global sign remains substantial.

For the compact metric family of turn 2 and 0<a<1/6, **strict A3w holds at every pair of distinct non-antipodal equatorial points, for all nonzero null tangent pairs**. Nevertheless, for a>1/18, NNCC fails at equatorial pairs arbitrarily close to the diagonal. Thus these complete positively curved spheres pass a nontrivial entire off-cut slice of the global antecedent. They are still not certified global-A3w examples.

## The equatorial pairs are genuinely off-cut

The metric g_a dominates the round metric pointwise because f_a>=cos x. An equatorial arc of length r<π has exactly the round length r. The round distance is a lower bound for g_a-distance and equals r between these endpoints. Thus the arc is minimizing. Uniqueness follows from uniqueness of the round minimizing geodesic: equality in the length comparison forces that round geodesic. The Gaussian curvature along the equator is 1, so no conjugate point occurs before r=π. The squared-distance cost and its derivatives used below are therefore valid, not extensions beyond the cut locus.

## Exact tensor at a fixed equatorial source

At p=(0,0), use the orthonormal basis e1=∂x,e2=∂y and endpoint tangent v=r e2, 0<r<π. Write κ=K_xx(p)=−24a and h(r)=r cot r. Let H(b,r) be the transverse eigenvalue of A(b e1+r e2), where A is the first-variable cost Hessian from turn 1. Reflection in the equator makes H even in b. Then

H(0,r)=h(r),
H_bb(0,r)=−2 I0(r)−κ I1(r),

where

I0(r)=∫_0^1 [sin(r(1−t))/sin r]² dt,
I1(r)=∫_0^1 [sin(r(1−t))/sin r]² sin²(rt) dt.

To verify the second formula, use affine geodesic time t∈[0,1]. The geodesic starting with b e1+r e2 has latitude x_b(t)=b sin(rt)/r+O(b³). Its squared speed is r²+b² and its normal Jacobi potential is

V_b(t)=r²+b²[1+(κ/2)sin²(rt)]+O(b⁴).

The normalized boundary Jacobi solution Z_b satisfies Z_b''+V_b Z_b=0, Z_b(0)=1,Z_b(1)=0, and H(b,r)=−Z_b'(0). Differentiating this boundary problem and integrating the Wronskian gives δH=−∫_0^1 Z_0² δV dt. Since Z_0=sin(r(1−t))/sin r, the formula follows. There is no endpoint-normalization or arclength factor missing: the fixed interval uses total speed in V_b.

For v=(b,r), the Hessian matrix is exactly

A(v)=I+(H(v)−1)[I−vv^T/|v|²].

Taking two v-derivatives at b=0, and putting u=(cosθ,sinθ), w=(−sinθ,cosθ), gives

S(r e2;u,w)=P(r)cos⁴θ+Q(r)sin⁴θ+R(r)cos²θ sin²θ,

P=−h''=2 csc²r (1−h),
Q=2(1−h)/r²,
R=10 I0−6(1−h)/r²+κ I1.

This formula tests every normalized null pair at the pair of equatorial points, not only coordinate null pairs. Bilinearity then covers arbitrary lengths.

## Positivity proof on the whole interval

For 0<r<π, k(r)=1−r cot r is positive. Also

I0=−h'/(2r),  0<=I1<=I0,  k/r²<I0.

For the last strict inequality, clear the positive denominator 2r² sin²r. The desired numerator is

F(r)=r²+r sin r cos r−2sin²r.

It has F(0)=F'(0)=0 and

F''(r)=4sin r(sin r−r cos r)>0,

because sin r−r cos r has derivative r sin r>0. Thus F(r)>0.

Since κ=−24a lies in (−4,0),

R >= 10 I0−6 I0+κ I0 = (4+κ)I0 >0.

Both P and Q are strictly positive. Therefore S>0 for every θ, as claimed. The diagonal follows from positive sectional curvature, and y-translation covers all equatorial sources.

The non-null pair u=w=e1 has the exact expression

S(r e2;e1,e1)=2I0+κ I1−2(1−h)/r².

Expanding at r=0 recovers (2/45+κ/30)r²+O(r⁴), so it is negative for a>1/18. This is a second derivation of the key local sign, via an exact Jacobi variation rather than a truncated curvature expansion.

## What this does not prove

Off-equator source points have different geodesic potentials and a nontrivial cut domain. Positive curvature and the equatorial strict-A3w calculation do not control those points. The open task for this family remains global A3w throughout the actual squared-distance smooth domain. No full-resolution claim is made.
