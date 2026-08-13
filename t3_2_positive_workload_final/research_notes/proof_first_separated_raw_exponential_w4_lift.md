# Raw exponential entropy implies fourth-power drift

**Proof-first interface lemma, 2026-08-12 PDT.**  This note isolates the
last deterministic-probabilistic step in the separated carrier proof.  It
does not use a Taylor expansion of a stopped increment and therefore needs
no unweighted terminal population moment.  The only inputs are a raw
exponential transform at every included terminal label and a first physical
time moment.

## 1. Statement

Let

\[
 G=G_\ell(x)\ge1,
 \qquad Y=G_\ell(X_\tau)-G_\ell(x),
 \qquad W_\ell=G_\ell^4,                                  \tag{1.1}
\]

where the shift in \(G_\ell\) is chosen so that
\(G_\ell\ge1\) on the population lattice.  Suppose \(h=h(x)\to\infty\),
\(h=o(G)\), and the included stopping time terminates almost surely in the
disjoint union

\[
                         \Omega=S\,\dot\cup\,E\,\dot\cup\,B. \tag{1.2}
\]

Assume that for some fixed \(\theta,c>0\),

\[
 \mathbb E_x[e^{\theta Y};S]
  +\mathbb E_x[e^{\theta Y};E]
       \le C e^{-ch},                                      \tag{1.3}
\]

and that, for every fixed \(N\),

\[
                    \mathbb E_x[e^{\theta Y};B]
                       \le C_Na^{-N},                       \tag{1.4}
\]

where \(h\le C_0\log a\).  Finally suppose

\[
                         \mathbb E_x\tau=o(G^3h).            \tag{1.5}
\]

Then there is \(c_*>0\) such that, along the separated sequence,

\[
 \boxed{
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)+\tau]
                    \le-c_*G^3h.}                           \tag{1.6}
\]

The same conclusion holds if (1.4) is stated with any nonnegative
polynomial endpoint mark, since the choice of the constant mark one is a
special case.

## 2. A high-probability entropy decrease

Choose

\[
                         r={c\over4\theta}.                  \tag{2.1}
\]

Equations (1.3)--(1.4) and Markov's inequality give

\[
\begin{split}
 \mathbb P_x\{Y>-rh\}
 &\le e^{\theta rh}\mathbb E_xe^{\theta Y}\\
 &\le C e^{-3ch/4}+C_Na^{-N+C_0c/4}.                        \tag{2.2}
\end{split}
\]

Take \(N>C_0c/4+2\).  Since \(h\to\infty\), the right side is
\(o(1)\).
On the event

\[
                              A=\{Y\le-rh\},                 \tag{2.3}
\]

monotonicity of \(t\mapsto t^4\) on \([1,\infty)\), together with
\(h=o(G)\), yields

\[
\begin{split}
 W_\ell(X_\tau)-W_\ell(x)
 &\le (G-rh)^4-G^4\\
 &\le-2rG^3h                                                   \tag{2.4}
\end{split}
\]

for all sufficiently large entrances.  If \(Y\) is even more negative,
the left side only decreases; no lower-tail moment is required.

## 3. The exceptional positive tail

For fixed \(\theta>0\), elementary calculus gives, for \(g\ge1\) and
\(y\ge0\),

\[
                 ((g+y)^4-g^4)^+
                     \le C_\theta(1+g^3)e^{\theta y/2}.      \tag{3.1}
\]

By Cauchy--Schwarz and (1.3)--(1.4),

\[
\begin{split}
 \mathbb E_x[e^{\theta Y/2};S\cup E]
 &\le \bigl(\mathbb E_x[e^{\theta Y};S\cup E]\bigr)^{1/2}
       \le Ce^{-ch/2},\\
 \mathbb E_x[e^{\theta Y/2};B]
 &\le \bigl(\mathbb E_x[e^{\theta Y};B]\bigr)^{1/2}
       \le C_Na^{-N/2}.                                    \tag{3.2}
\end{split}
\]

Consequently

\[
 \mathbb E_x[(W_\ell(X_\tau)-W_\ell(x))^+;A^c]
       \le C(1+G^3)\{e^{-ch/2}+a^{-N/2}\}
       =o(G^3h).                                            \tag{3.3}
\]

This estimate pays the actual first-crossing endpoint on \(B\); no
fictional cleanup, endpoint re-centering, or terminal spectator moment is
inserted.

## 4. Conclusion and exact scope

Combining (2.2)--(2.4) with (3.3) gives

\[
 \mathbb E_x[W_\ell(X_\tau)-W_\ell(x)]
       \le-2rG^3h\{1-o(1)\}+o(G^3h)
       \le-rG^3h                                             \tag{4.1}
\]

for all sufficiently large entrances.  Equation (1.5) absorbs the
physical duration and proves (1.6).

The lemma is deliberately agnostic about how the raw transforms are
proved.  In the separated carrier application they come from a normalized
open-phase weight which agrees exactly with \(e^{\theta G_\ell}\) on
completed \(C=0\) returns, together with an edgewise charge for every
included open boundary.  This note does not certify those upstream
operator estimates or the almost-sure termination of their stopping rule.
