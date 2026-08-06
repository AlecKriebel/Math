# Complete-credit elimination by finite target-following paths

## 1. Augmented residual identity

At a jump epoch, record the target complex \(t\) of the most recent reaction
and write

\[
x=r+t.
\]

If the next reaction is \(s\to u\), then the new population and residual are

\[
x'=x-s+u,\qquad r'=x'-u=x-s.
\]

For

\[
V(x,t)=\log\prod_i(x_i-t_i)!,
\]

one has the exact identity

\[
\begin{aligned}
V(x-s+u,u)-V(x,t)
 &=\log\frac{\prod_i(x_i-s_i)!}{\prod_i(x_i-t_i)!}\\
 &=\log\frac{(x)_t}{(x)_s}.
\end{aligned}
\]

A reaction whose source is the carried target, \(s=t\), therefore has
exactly zero residual reward.  This is the complete-credit convention: the
product of a reaction remains fully credited until the chain switches to a
different source.

## 2. One-jump entropy bound

Write

\[
\bar\kappa_y=\sum_{y\to u,\ u\ne y}\kappa_{yu},
\qquad
\Lambda(x)=\sum_y\bar\kappa_y(x)_y
\]

and let

\[
p_x(y)=\frac{\bar\kappa_y(x)_y}{\Lambda(x)}
\]

for enabled source complexes.  Since the carried target is present,
\(p_x(t)>0\).  The expected one-jump residual reward is

\[
d(x,t)=\sum_s p_x(s)\log\frac{(x)_t}{(x)_s}.
\]

Substituting \((x)_s=p_x(s)\Lambda(x)/\bar\kappa_s\) gives exactly

\[
d(x,t)
 =\log p_x(t)+H(p_x)
  +\sum_sp_x(s)\log\bar\kappa_s-
   \log\bar\kappa_t.
\]

Consequently

\[
d(x,t)\le \log p_x(t)+C_0,
\]

where

\[
C_0=\log|\mathcal C|
   +\log\frac{\max_y\bar\kappa_y}{\min_y\bar\kappa_y}.
\]

This estimate is rate preserving.  No two independent rate monomials are
ordered or compared.

## 3. Terminal-complex episodes

For every ordered pair \((t,c)\), fix a simple directed complex path

\[
t=y_0\longrightarrow y_1\longrightarrow\cdots
 \longrightarrow y_L=c,
\qquad L\le |\mathcal C|-1.
\]

At phase \(y_k\), inspect the next reaction.  Continue only if the exact
designated edge \(y_k\to y_{k+1}\) fires; otherwise stop after that jump.  At
terminal phase \(c\), take one further jump and stop.

Along every designated edge, the state is \(r+y_k\), the designated source
is enabled, and the residual remains exactly \(r\).  The episode has at most
\(|\mathcal C|\) jumps.

Let

\[
q_k=\frac{\kappa_{y_k y_{k+1}}}{\bar\kappa_{y_k}}>0,
\qquad
p_k=p_{r+y_k}(y_k).
\]

If \(J_k\) is the expected remaining residual reward from phase \(k\), then

\[
J_L=d(r+c,c),
\qquad
J_k=d(r+y_k,y_k)+q_kp_kJ_{k+1}.
\]

The continuation reward is multiplied by \(q_kp_k\) because only the exact
designated edge continues; its immediate reward is zero.

## 4. Scalar elimination

For terminal probability \(\varepsilon=p_{r+c}(c)\), set

\[
M_L(\varepsilon)=\log\varepsilon+C_0
\]

and recursively

\[
M_k(\varepsilon)=
\sup_{0<p\le1}
\left\{\log p+C_0+q_kpM_{k+1}(\varepsilon)\right\}.
\]

Then \(J_k\le M_k\).  The maximized function is strictly concave.  If
\(M=-A<0\) and \(qA>1\), its unique maximizer is

\[
p_*=(qA)^{-1}
\]

and the maximum equals

\[
C_0-1-\log(qA).
\]

It follows by backward induction through the finite path that

\[
M_0(\varepsilon)\longrightarrow-\infty
\qquad(\varepsilon\downarrow0).
\]

Thus a terminal complex whose source probability tends to zero produces an
arbitrarily strong negative expected reward for the entire episode,
regardless of any number of intermediate source-propensity scales.  This is
the complete-credit elimination lemma.
