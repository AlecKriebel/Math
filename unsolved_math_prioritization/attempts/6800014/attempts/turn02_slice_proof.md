# Attempt 2: an explicit local-slice counterexample

This is a substantive proof attempt. Its purpose is to turn Attempt 1's semidefinite Hessian into a genuine local maximum on the entire space of left-invariant metrics.

## Theorem

Fix `u₀` with `0<u₀<1/2`. On the Lie algebra with orthonormal basis `e₀,e₁,e₂,e₃,e₄`, impose

\[
[e_0,e_1]=e_2,\qquad [e_0,e_2]=-e_1,
\qquad [e_0,e_4]=u_0e_3,
\]

and let all other brackets vanish except those forced by skew symmetry. The associated left-invariant metric on the simply connected group is a local maximum of

\[
F(g)=\frac{\operatorname{Scal}(g)^2}{\lVert\operatorname{Ric}(g)\rVert^2},
\]

but is not a solvsoliton. Its value is `1/3`. It is not a global maximum on this same group.

## 1. Curvature and algebraic reduction

For any real `4×4` matrix `A`, define an almost-abelian metric Lie algebra by `[e₀,v]=Av` on the abelian ideal `V=span(e₁,…,e₄)`. Let `S(A)=(A+Aᵀ)/2` and use the Frobenius norm. When `tr A=0`, the standard curvature formula is

\[
\operatorname{Ric}|_V=\frac12[A,A^T],\qquad
\operatorname{Ric}(e_0)=-\lVert S(A)\rVert^2e_0,
\qquad \operatorname{Ric}(e_0,V)=0.
\]

This is Lauret–Will, equation (3), with the complementary basis vector placed first. Put

\[
s=\lVert S(A)\rVert^2,\qquad q=\lVert[A,A^T]\rVert^2.
\]

Then

\[
\operatorname{Scal}=-s,\quad
\lVert\operatorname{Ric}\rVert^2=s^2+q/4,\quad
F(A)=\frac{s^2}{s^2+q/4}.
\]

Where `s>0`, the inequality `F(A)≤1/3` is equivalent to

\[
P(A):=q-8s^2\ge0. \tag{1}
\]

For `A_u=J⊕uE₁₂`, we have `s=u²/2`, `q=2u⁴`, so `P(A_u)=0` and `F(A_u)=1/3`.

Every left-invariant metric sufficiently close to the given metric is represented by a matrix `c T⁻¹ A_{u₀} T`, with `c>0` and `T∈GL₄(R)` close to the identity. Indeed, choose a nearby orthonormal basis of the fixed abelian ideal and let the unit orthogonal complement be `c e₀+v`, with `v∈V`. Since `V` is abelian, its adjoint action on `V` is precisely `c A_{u₀}` before changing the ideal basis. This construction varies smoothly near the original metric.

The functional is unchanged by nonzero scalar multiplication of `A`, and also by orthogonal conjugation. Consequently, it suffices to establish (1) for every matrix in the conjugacy class of `A_{u₀}` sufficiently close to `A_{u₀}`.

## 2. A local normal form covering every conjugate

Let `A` be such a nearby conjugate. Its generalized zero eigenspace

\[
W=\ker A^2
\]

has dimension two, is invariant, and is close to `span(e₃,e₄)`. Its continuous local dependence is especially explicit: `E(A)=I+A²` is an idempotent with image `W`, since `A` is conjugate to `J⊕u₀E₁₂`. Orthonormal frames can therefore be chosen smoothly by local projection and Gram–Schmidt. The restriction `A|W` is nonzero rank-one nilpotent with square zero.

Choose a unit vector `f₃` in `im(A|W)=ker(A|W)`, close to `e₃`; choose its orthogonal companion `f₄` in `W`, close to `e₄`. With these continuous local choices,

\[
A f_3=0,\qquad A f_4=v f_3,
\]

where `v>0` and `v→u₀` as `A→A_{u₀}`. Complete with an orthonormal frame `f₁,f₂` of `W⊥`, close to `e₁,e₂`.

In this orthonormal frame the matrix has the form

\[
M=\begin{pmatrix}
a&b-k&0&0\\
b+k&-a&0&0\\
x&y&0&v\\
z&w&0&0
\end{pmatrix},
\qquad k=\sqrt{1+a^2+b^2}. \tag{2}
\]

To see the stated upper-left block, its induced action on the quotient by `W` has eigenvalues `±i`; hence its trace is zero and determinant one. Write its symmetric traceless part as `[[a,b],[b,-a]]` and skew part as `kJ`. The determinant equation is `k²−a²−b²=1`, and proximity to `J` selects `k>0`.

The six transverse parameters

\[
\xi=(a,b,x,y,z,w)
\]

tend to zero, while `v→u₀`. No restriction to a block-diagonal family has been imposed: the entire lower-left block is retained. Nor is a simultaneous invariant orthogonal splitting assumed; only `W` is invariant.

## 3. The transverse quadratic form

For (2), set `P(v,ξ)=||[M,Mᵀ]||²−8||S(M)||⁴`. This is a real-analytic function near `(u₀,0)` because the positive square root in (2) is analytic there. Direct multiplication gives

\[
P(v,0)=0,\qquad D_\xi P(v,0)=0,
\]

and the quadratic part in `ξ` is

\[
\begin{split}
Q_v(\xi)={}&16(2-v^2)(a^2+b^2)\\
&+2\left[x^2+y^2+(1-3v^2)(z^2+w^2)
+2v(wx-yz)\right]. \tag{3}
\end{split}
\]

A transparent positive decomposition is

\[
Q_v(\xi)=16(2-v^2)(a^2+b^2)
+2(x+vw)^2+2(y-vz)^2
+2(1-4v^2)(z^2+w^2). \tag{4}
\]

Therefore `Q_v` is positive definite for every `0<v<1/2`.

For a fully checkable expansion, put `r²=x²+y²+z²+w²`. The exact remainder after (3) is

\[
\begin{split}
P-Q_v={}&-12(a^2+b^2)r^2
-24ak(wz+xy)\\
&+12bk(x^2+z^2-y^2-w^2)\\
&+4v\{a(wy-xz)-b(wx+yz)\}\\
&+4v(k-1)(wx-yz)-4(wx-yz)^2. \tag{5}
\end{split}
\]

Because `k−1=O(a²+b²)`, every term in (5) has order at least three in `ξ`, uniformly for `v` in a compact interval contained in `(0,1/2)`.

Choose such a compact interval `I` with `u₀` in its interior. Positivity in (4) and compactness give a constant `c>0` with

\[
Q_v(\xi)\ge c\lVert\xi\rVert^2 \quad(v\in I).
\]

Equation (5) gives constants `C,δ>0` with

\[
|P(v,\xi)-Q_v(\xi)|\le C\lVert\xi\rVert^3
\quad(v\in I,\ \lVert\xi\rVert<\delta).
\]

Thus, after decreasing `δ` if necessary,

\[
P(v,\xi)\ge \tfrac c2\lVert\xi\rVert^2\ge0.
\]

The normal-form reduction and (1) prove local maximality of `F`, including all nearby left-invariant metrics. The flat `v` direction causes no gap: the function is exactly constant on `ξ=0`, and the estimate is uniform in `v`.

## 4. Failure of the solvsoliton equation

For `A=A_{u₀}`, in the order `e₀,e₁,e₂,e₃,e₄`,

\[
\operatorname{Ric}=\operatorname{diag}
\left(-\tfrac{u_0^2}{2},0,0,\tfrac{u_0^2}{2},-\tfrac{u_0^2}{2}\right).
\]

Suppose `D=Ric−cI` were a derivation. It is necessarily diagonal in this basis. Write its diagonal entries as `d₀,…,d₄`. The relation `[e₀,e₁]=e₂` forces `d₂=d₀+d₁`. Since `d₁=d₂=−c`, this implies `d₀=0`, hence `c=−u₀²/2`.

Now `d₃=u₀²` and `d₄=0`. But `[e₀,e₄]=u₀e₃` forces `d₃=d₀+d₄=0`, a contradiction. Thus the metric is not a solvsoliton.

## 5. Explicit nonglobal comparison on the same group

Set

\[
B=\begin{pmatrix}
0&-1&0&0\\1&0&0&0\\1&0&0&1\\0&-1&0&0
\end{pmatrix}.
\]

It is conjugate to `A₁` and hence to `A_{u₀}`. An explicit conjugation is

\[
B=T A_1T^{-1},\qquad
T=\begin{pmatrix}I_2&0\\Y&I_2\end{pmatrix},\qquad
Y=\begin{pmatrix}0&2\\1&0\end{pmatrix}.
\]

Also `A₁=H A_{u₀}H⁻¹` for `H=diag(1,1,1/u₀,1)`. Direct calculation gives `s(B)=3/2`, `q(B)=8`, and therefore

\[
F(B)=\frac{9}{17}>\frac13.
\]

This comparison is not needed to disprove the listed assertion, but it separately verifies the local-versus-global distinction.

## Conclusion and limits

Subject to independent audit of the algebra and the all-metrics normal-form argument, this proves the listed universal statement false in dimension five. Choosing `u₀=1/4` gives a wholly rational explicit example.

The construction is consistent with the existence assertion in Lauret's July 2018 slides, but the slides give no construction or proof, and Lauret–Will's later final paper explicitly treats existence as open. We make no novelty claim and do not infer why those sources differ. The result is proved here directly rather than certified from the slides.
