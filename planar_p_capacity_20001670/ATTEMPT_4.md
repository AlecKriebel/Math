# Attempt 4: close the endpoint-collision gap locally

Status: a strict local theorem for ALL sufficiently thin triangles, at each fixed
`1<p<2`. The original global segment conjecture remains unresolved.

This attempt adds a genuinely new mechanism to Attempt 3: the precise
slit-endpoint growth exponent produces a logarithmic energy gain when a third
vertex approaches a base endpoint. No numerical PDE computation is used.

## 1. The primary endpoint input

Lundstrom--Singh, *Estimates of p-harmonic functions in planar sectors*,
Ark. Mat. 61 (2023), 141--175,
<https://doi.org/10.4310/ARKIV.2023.v61.n1.a8>,
author text <https://arxiv.org/html/2111.02721>, Lemma 3.1 and equation (1.6),
provide a positive homogeneous p-harmonic function on the slit plane. Its degree
is `lambda=(p-1)/p`; the angular profile vanishes linearly at both slit faces.
Lemma 2.5 of the same paper supplies the flat-boundary comparison used below.

Rotate their slit to the positive x-axis and write this function as
`Psi(r,theta)=r^lambda f(theta)` on `0<theta<2*pi`. The profile is positive
inside, zero at 0 and `2*pi`, has bounded derivative, and its derivative has
nonzero magnitude near the two faces. These are the only sector facts used.

## 2. A lower barrier for the actual segment potential

Again let `S=[0,1] x {0}`, let `u` be its equilibrium potential, and put `w=1-u`.
In a disk of radius `R<1/2` around the left endpoint, `w` is positive p-harmonic
off the slit and has zero values on its two faces. On the outer circle, the
ratio `w/Psi` is bounded below by a positive constant: away from `(R,0)` this
is compactness and positivity; near `(R,0)`, the flat-side boundary comparison
shows both functions vanish linearly in distance to the slit. This argument is
on the two faces separately and uses no regularity at the slit endpoint.

Choose `c>0` with `w>=c*Psi` on the outer circle. The comparison principle
then gives this inequality throughout the punctured slit disk. At the origin
the barrier tends to zero while `w>=0`, so no extra endpoint boundary datum is
needed. The profile properties imply, after reducing the radius, that there
are constants `A_p>0` and `R_p in (0,1/2)` such that

\[
 w(x,y)\geq A_p y x^{\lambda-1}
 \quad(0<x<R_p,\ 0<y\leq x).                                \tag{1}
\]

Indeed `sqrt(x^2+y^2)` is comparable to `x`, the polar angle is comparable
to `y/x`, and `f(theta)` is bounded below by a positive multiple of `theta`
on `[0,pi/4]`.

We do not infer a pointwise gradient estimate by differentiating a function
inequality. Instead, the next step uses a one-dimensional energy estimate.

## 3. Logarithmic energy gain

Take `T_{alpha,h}=conv{(0,0),(1,0),(alpha,h)}` with `0<=alpha<1/2`. If
`M=max(alpha,h)<R_p`, the rectangle with varying x-range

`M < x < R_p`, `0 < y < h/2`

is inside the triangle: on this range its roof is
`h*(1-x)/(1-alpha)>=h/2`. For almost every x, the Sobolev slicing property,
the zero trace `w(x,0)=0`, and Hölder's inequality give

\[
 \int_0^{h/2}|\partial_yw(x,y)|^p\,dy
 \geq\frac{w(x,h/2)^p}{(h/2)^{p-1}}
 \geq A_p^p\frac{h}{2}x^{p(\lambda-1)}
 =A_p^p\frac{h}{2x}.                                       \tag{2}
\]

The last equality uses the EXACT slit degree `lambda=(p-1)/p`. Integrating
and applying the enlargement defect proved in Attempt 3 yields

\[
 C_p(T_{\alpha,h})-c_p
 \geq\frac{(p-1)A_p^p}{2}\,h\log\frac{R_p}{\max(\alpha,h)}.  \tag{3}
\]

In contrast, `sqrt(t^2+h^2)<=t+h` gives `P(T)-2<=2h` uniformly, even at
`alpha=0`. Concavity of the power `q=2-p` therefore gives

\[
 C_p(I_{P(T)})-c_p\leq c_p(2-p)h.                            \tag{4}
\]

Choose `delta_p in (0,R_p)` small enough that

\[
 \frac{(p-1)A_p^p}{2}\log\frac{R_p}{\delta_p}>c_p(2-p).
\]

Then all `0<=alpha<=delta_p` and `0<h<=delta_p` satisfy strict segment
comparison. Reflection handles `1-delta_p<=alpha<=1`.

## 4. Uniform local theorem

For `delta_p<=alpha<=1-delta_p`, use the positive threshold in Attempt 3.
Taking the smaller of that threshold and `delta_p` proves:

**Theorem.** For every fixed `p in (1,2)`, there exists `epsilon_p>0` such that

\[
 C_p(T_{\alpha,h})>C_p(I_{P(T_{\alpha,h})})
 \quad\text{for every }\alpha\in[0,1],\quad0<h<\epsilon_p.     \tag{5}
\]

In particular, after normalizing the longest side to one, every nondegenerate
triangle sufficiently close to degeneration has strictly greater capacity than
its same-perimeter segment. With a longest side as base the projection indeed
lies in `[0,1]`: an exterior projection would make one other side longer.

## Remaining gap and limitations

The threshold is qualitative and depends on `p`; uniformity as `p` tends to an
endpoint is not claimed. This theorem confines any hypothetical counterexample
to triangles with a positive normalized altitude, but it gives no bound on the
capacity in that remaining compact family. The global conjecture is still
open. Novelty of the local theorem has not been established and the proof is
submitted for independent adversarial review before promotion.
