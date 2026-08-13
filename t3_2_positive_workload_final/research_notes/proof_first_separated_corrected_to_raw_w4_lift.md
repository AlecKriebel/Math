# Corrected-to-raw transform and one-sided fourth-power lift

**Proof-only interface lemma, 2026-08-12 PDT.**  This note supplies the
terminal transform needed after the phase-corrected separated resolvent.
It assumes the corrected service transform and the required endpoint
ratio moment; it does not prove the underlying Green kernel, physical
duration, or localization tail.  No certification flag is changed.

## 1. Corrected service transform

Let (x) be a cofactor-free entrance, put

\[
             g=G_\ell(x),\qquad
             h=h(x)\longrightarrow\infty,                    \tag{1.1}
\]

and let (S) be the completed service event.  At a cofactor-free base
define

\[
 {cal M}(z)=M_z(dB)=(z_B+1)^d,qquad
 w_\theta(z)={e^{\theta G_\ell(z)}\over{cal M}(z)^\theta},    \tag{1.2}
\]

where (d\in\{0,1,2\}) is fixed by the support.  Suppose that, for fixed
(0<\theta<1), the corrected terminal estimate is

\[
 \mathbb E_x\!\left[{w_\theta(X_\tau)\over w_\theta(x)};S\right]
       \le C e^{-c_0\theta h_*},                              \tag{1.3}
\]

where

\[
                         h_*\ge c_1h-C_1                     \tag{1.4}
\]

for fixed (c_1>0,C_1<\infty).  Assume also the scale-relative divisor
moment

\[
 \mathbb E_x\!\left[
   \left({{cal M}(X_\tau)\over{cal M}(x)}\right)^r;S\right]
       \le C_r                                                \tag{1.5}
\]

for every fixed (r) needed below.  It is enough for the right side of
(1.5) to be (e^{o(h)}).

Condition (1.5), not merely the statement that some unscaled endpoint
moment is finite, is the exact moment used by the transform.  It follows,
for example, from

\[
 \mathbb E_x\left[
   \left({1+B_\tau\over1+B_0}\right)^p;S\right]\le C_p        \tag{1.6}
\]

for sufficiently large fixed (p).  If an available polynomial estimate
loses a factor (a^c), it cannot be inserted here: its logarithmic loss
can dominate an arbitrarily slowly divergent (h).

### Lemma 1.1 (raw terminal exponential transform)

For every fixed (0<\theta'<\theta),

\[
 \boxed{\quad
 \mathbb E_x[e^{\theta'\Delta G};S]
      \le C_{\theta'}e^{-c_0\theta'h_*}
      \le C'_{\theta'}e^{-c_2\theta'h},\quad}                 \tag{1.7}
\]

where

\[
                     \Delta G=G_\ell(X_\tau)-G_\ell(x),
 \qquad c_2=c_0c_1.                                          \tag{1.8}
\]

#### Proof

Put \(\alpha=\theta'/\theta\in(0,1)\).  The identity

\[
 e^{\theta'\Delta G}
 =\left({w_\theta(X_\tau)\over w_\theta(x)}\right)^\alpha
   \left({{cal M}(X_\tau)\over{cal M}(x)}\right)^{\theta'} \tag{1.9}
\]

is exact.  Hölder with conjugate exponents (1/\alpha) and
(1/(1-\alpha)) gives

\[
\begin{aligned}
 \mathbb E_x[e^{\theta'\Delta G};S]
 &\le
 \left(\mathbb E_x\left[
       {w_\theta(X_\tau)\over w_\theta(x)};S\right]\right)^\alpha\\
 &\quad\times
 \left(\mathbb E_x\left[
   \left({{cal M}(X_\tau)\over{cal M}(x)}\right)^r;S
                         \right]\right)^{1-\alpha},          \tag{1.10}
\end{aligned}
\]

with

\[
             r={\theta'\over1-\alpha}
               ={\theta\theta'\over\theta-\theta'}.         \tag{1.11}
\]

Equations (1.3)--(1.5) prove the first inequality in (1.7), because
(\alpha\theta=\theta'\).  Equation (1.4) proves the second after absorbing
a fixed constant. \(\square\)

## 2. Raw transform to common fourth power

Let (B) denote all included localization endpoints, and assume the
terminal partition is (S\mathbin{\dot\cup}B).  The same proof works with
several exceptional endpoint labels by replacing (B) with their union.
Assume

\[
 \mathbb P_x(B)=o(1),\qquad
 \mathbb E_x[(W_\ell(X_\tau)-W_\ell(x))^+;B]
       =o(g^3h).                                               \tag{2.1}
\]

The second condition is exactly the endpoint-weighted boundary estimate.
For a more elementary sufficient condition, fixed binary dimension gives

\[
                       W_\ell(z)\le C_\ell(1+|z|_1)^8,        \tag{2.2}
\]

so it suffices that

\[
              \mathbb E_x[(1+|X_\tau|_1)^8;B]=o(g^3h).       \tag{2.3}
\]

Superpolynomial boundary probability together with endpoint-weighted
moments of sufficiently high fixed order implies (2.3) by Hölder.

### Lemma 2.1 (one-sided (W=G^4) lift)

Suppose (1.7), (2.1), and

\[
                              h=o(g).                         \tag{2.4}
\]

Then, for all sufficiently large entrances,

\[
 \boxed{\quad
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)]
             \le-cg^3h.\quad}                                \tag{2.5}
\]

#### Proof

Fix \(\lambda=\theta'\) and let \(\kappa=c_2\) in (1.7).  Put

\[
                         a_0={\kappa\over2}.                  \tag{2.6}
\]

Markov's inequality applied to the raw exponential transform gives

\[
\begin{aligned}
 \mathbb P_x\{S,\ \Delta G>-a_0h\}
 &\le e^{\lambda a_0h}
       \mathbb E_x[e^{\lambda\Delta G};S]\\
 &\le C e^{-\lambda\kappa h/2}=o(1).                         \tag{2.7}
\end{aligned}
\]

Consequently the good service event

\[
                         A=S\cap\{\Delta G\le-a_0h\}        \tag{2.8}
\]

has probability (1-o(1)), by (2.1).  Since (G_\ell\ge1), the map
(t\mapsto t^4) is increasing at every attainable value.  By (2.4),
(a_0h\le g/2) eventually, and hence on (A)

\[
\begin{aligned}
 W_\ell(X_\tau)-W_\ell(x)
 &\le(g-a_0h)^4-g^4\\
 &=-\int_{g-a_0h}^{g}4t^3\,dt
 \le-{a_0\over2}g^3h.                                       \tag{2.9}
\end{aligned}
\]

This estimate becomes only more favorable when \(\Delta G\) is very
negative; no symmetric moment of the negative part is used.

It remains to control the positive service contribution.  For (u>0),
the exact fourth-power identity and the elementary bounds
(u^j\le C_{j,\lambda}e^{\lambda u}) give, uniformly for (g\ge1),

\[
                   ((g+u)^4-g^4)^+
                      \le C_\lambda g^3e^{\lambda u}.        \tag{2.10}
\]

Therefore (1.7) yields

\[
 \mathbb E_x[(W_\ell(X_\tau)-W_\ell(x))^+;S]
       \le Cg^3e^{-\lambda\kappa h}=o(g^3h).                 \tag{2.11}
\]

Service outcomes outside (A) with \(\Delta G\le0) contribute
nonpositively and may be discarded.  Combining (2.7)--(2.11) gives

\[
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x);S]
       \le-c'g^3h.                                           \tag{2.12}
\]

Finally, the positive part on (B) is (o(g^3h)) by (2.1), while its
negative part is favorable.  This proves (2.5). \(\square\)

## 3. Scope and obstruction warning

The proof uses neither a terminal Taylor expansion nor an absolute moment
of the negative entropy increment.  Its two load-bearing inputs are:

1. a corrected service transform at exponent \(\theta\), together with a
   relative divisor moment sufficient for Hölder; and
2. an endpoint-weighted bound on the included localization event.

If “polynomial endpoint moments” means only

\[
                    \mathbb E(1+B_\tau)^p\le C(1+b)^{p+c}
                                                                    \tag{3.1}
\]

with a fixed (c>0), then the Hölder factor may cost (c\log b), which
can dominate the separated gap (h\).  Such an estimate does not imply
Lemma 1.1.  A scale-relative moment such as (1.5), or more generally an
(e^{o(h)}) loss, is required.
