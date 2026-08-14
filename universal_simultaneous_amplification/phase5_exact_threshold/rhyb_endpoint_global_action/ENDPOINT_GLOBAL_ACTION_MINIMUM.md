# Global minimality of the nonconvex endpoint actions

Date: 2026-08-13 (America/Los_Angeles)

No graph search, parameter search, numerical optimization, literature search,
or external communication was used.

## 1. Result and scope

The natural Bd and dB endpoint actions are not convex on the full physical
cube.  Nevertheless, their positive fixed points are their unique global
minimizers.  More precisely, retain the notation

\[
 \Phi(z)=-z-\log(1-z),\qquad 0\leq z<1,
\]

\[
 J_B(z)={1\over r}E_\pi\{t\Phi(z)\}
          -{1\over2}\langle z,Pz\rangle_\pi,
\]

\[
 J_D(z)={1\over r}E_\pi\{a^2\Phi(z)\}
          -{1\over2}\langle az,P(az)\rangle_\pi,
\]

where `P` is a finite nonnegative row-stochastic kernel reversible under
`pi`, `a,t` are positive, and the
active endpoints satisfy

\[
 tb=r(1-b)Pb,\qquad P(as)={as\over r(1-s)}.             \tag{1}
\]

Put `q=1-b` and `h=1-s`.  For every physical label `z` one has the exact
positive decompositions

\[
\boxed{
\begin{aligned}
J_B(z)-J_B(b)
={}&{1\over r}E_\pi\!\left[t\left\{
 D_\Phi(z,b)-{(z-b)^2\over2q}\right\}\right]\\
&+{1\over2}\left\langle z-b,
 \left(D_{Pb/b}-P\right)(z-b)\right\rangle_\pi,
\end{aligned}}                                                   \tag{2}
\]

and

\[
\boxed{
\begin{aligned}
J_D(z)-J_D(s)
={}&{1\over r}E_\pi\!\left[a^2\left\{
 D_\Phi(z,s)-{(z-s)^2\over2h}\right\}\right]\\
&+{1\over2}\left\langle a(z-s),
 \left(D_{P(as)/(as)}-P\right)a(z-s)\right\rangle_\pi.
\end{aligned}}                                                   \tag{3}
\]

Every term on the right is nonnegative.  For vectors in `[0,1)^n` it follows
that

\[
                  J_B(z)\geq J_B(b),\qquad
                  J_D(z)\geq J_D(s),                         \tag{4}
\]

with equality only at the corresponding endpoint.  The same statement on
the closed cube uses the lower-semicontinuous convention `Phi(1)=+infinity`.

This strengthens the earlier local-Hessian statement.  It does not make
the actions convex, make them Fenchel conjugates, or prove the open support
inequality

\[
                         (r-1)E_pq-E_ps\geq0.              \tag{5}
\]

The cross-evaluations `z=s` in (2) and `z=b` in (3) are now certified
nonnegative globally, but an additional cross-rule comparison is still
needed to turn them into (5).

## 2. The sharp scalar Bregman inequality

The directed scalar divergence is

\[
 D_\Phi(x,y)
 ={1-x\over1-y}-1-\log\!\left({1-x\over1-y}\right).     \tag{6}
\]

The key lemma is

\[
 \boxed{
 D_\Phi(x,y)\geq{(x-y)^2\over2(1-y)}
 \qquad(0\leq x<1,\ 0<y<1).}                            \tag{7}
\]

To prove it, set

\[
 H=1-y,\qquad Z={1-x\over H}.
\]

Then `0<H<=1`, `HZ<=1`, and (7) becomes

\[
                         Z-1-\log Z\geq{H\over2}(Z-1)^2. \tag{8}
\]

If `0<Z<=1`, use `H<=1` and

\[
 2(Z-1-\log Z)-(Z-1)^2
 =-Z^2+4Z-3-2\log Z\geq0.                              \tag{9}
\]

The expression in (9) vanishes at one and has derivative
`-2(Z-1)^2/Z<=0`, hence it is nonnegative to the left of one.

If `Z>=1`, the constraint `HZ<=1` gives `H<=1/Z`, and it is enough to use

\[
 2Z(Z-1-\log Z)-(Z-1)^2
 =Z^2-1-2Z\log Z\geq0.                                 \tag{10}
\]

The last inequality is the elementary bound

\[
                         \log Z\leq{Z-Z^{-1}\over2},
\]

whose derivative difference is `(Z-1)^2/(2Z^2)>=0` on `[1,infinity)`.
Both branches are strict unless `Z=1`, equivalently `x=y`.

## 3. Exact Bd decomposition

Stationarity of `b` gives the standard remainder identity

\[
 J_B(z)-J_B(b)
 ={1\over r}E_\pi\{tD_\Phi(z,b)\}
 -{1\over2}\langle z-b,P(z-b)\rangle_\pi.              \tag{11}
\]

The Bd ground equation in (1) is

\[
                         {Pb\over b}={t\over rq}.         \tag{12}
\]

Add and subtract

\[
 {1\over2}E_\pi\!\left[{t(z-b)^2\over rq}\right]
 ={1\over2}\left\langle z-b,D_{Pb/b}(z-b)\right\rangle_\pi
\]

in (11).  This gives (2) exactly.  The first line is nonnegative by (7),
and the second is the ground-state Picone form

\[
 {1\over4}\sum_{i,j}\pi_iP_{ij}b_ib_j
 \left({z_i-b_i\over b_i}-{z_j-b_j\over b_j}\right)^2. \tag{13}
\]

If equality holds, the strict scalar lemma forces `z=b` at every vertex.

## 4. Exact dB decomposition

Likewise, stationarity of `s` gives

\[
 J_D(z)-J_D(s)
 ={1\over r}E_\pi\{a^2D_\Phi(z,s)\}
 -{1\over2}\langle a(z-s),P\{a(z-s)\}\rangle_\pi.      \tag{14}
\]

The dB ground in (1) obeys

\[
                         {P(as)\over as}={1\over rh}.     \tag{15}
\]

Adding and subtracting the corresponding diagonal ground term in (14)
gives (3).  Its second line is

\[
 {1\over4}\sum_{i,j}\pi_iP_{ij}(a_is_i)(a_js_j)
 \left({z_i-s_i\over s_i}-{z_j-s_j\over s_j}\right)^2, \tag{16}
\]

and the first line is nonnegative by (7).  Equality is possible only at
`z=s`.

## 5. Why nonconvexity is compatible with global minimality

On the homogeneous one-state system the common action is

\[
                         J(z)={1\over r}\Phi(z)-{z^2\over2}.
\]

It has a local maximum at zero and its unique active minimum at
`z=(r-1)/r`.  Thus (4) is fully compatible with the already proved failure
of global convexity.  What survives is not convexity of `J`, but the
endpoint-dependent Picone decomposition (2)--(3).

## 6. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_endpoint_global_action/verify_endpoint_global_action.py
```

The replay checks the scalar changes of variables, both branch derivatives,
the abstract Picone and add/subtract algebra, both full decompositions on an
exact physical reversible two-cycle, and the homogeneous
nonconvex/global-minimum consistency.
