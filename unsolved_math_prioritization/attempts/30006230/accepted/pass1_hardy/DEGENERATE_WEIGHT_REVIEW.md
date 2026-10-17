# Independent check of the degenerate-weight addendum

14 October 2026. This is a mathematical check of the authored addendum, not human peer review or a novelty certification.

Reviewed artifact: DEGENERATE_WEIGHT_ADDENDUM.md, 3692 bytes, SHA-256
e87230321f98f219db6cf0528561c314045494c7b706cb77db3ec77bf197f09f.

**Verdict: pass for all three stated scope results. No repair requested.**

## 1. Positive-potential Hardy counterexample

With $s=r-a$, expansion gives
\[
\int(sv'+v/2)^2
=\int s^2v'^2+\int svv'+\tfrac14\int v^2
=\int s^2v'^2-\tfrac14\int v^2.
\]
Compact support eliminates the outer boundary term, and the coefficient $s$ is smooth through zero, so there is no inner boundary term at $a$. The identity therefore holds for every compactly supported smooth one-dimensional test, including tests crossing $a$.

The one-dimensional inequality can be integrated on every gauge-polar ray, independently of strict positivity of $V$, giving the radial-gradient Hardy display for all original spatial tests. Pointwise radial-gradient domination and $V\geq0$ give the full-gradient display. Both passages include the historical $n=1$ case through counting measure on $S^0$.

For a $C^1$ flux-classical solution, $[(r-a)^2f']'(a)=0$, so the proposed equation forces $f(a)=0$. This contradicts strict positivity. The declared regularity convention is essential to the claimed obstruction and is stated correctly.

The example does not meet the global Hardy–Rellich side condition:
$V(a)=V'(a)=0$, $V''(a)=2a^{1-Q}>0$, so
$S_Q[V](a)=-2a^{1-Q}<0$. This is explicitly excluded in the addendum.

## 2. Dichotomy under the classical side condition

For $U(t)=e^{-2t}V(e^t)$ and $k=\sqrt{Q-1}$, the exact identity is
$S_Q[V]=(Q-1)U-U''$. If $U\geq0$ vanishes at $t_0$, then $U'(t_0)=0$. Set $F=U''-k^2U\leq0$.

For $t\geq t_0$,
\[
U(t)=\int_{t_0}^t\frac{\sinh(k(t-s))}{k}F(s)\,ds\leq0.
\]
For $t\leq t_0$,
\[
U(t)=\int_t^{t_0}\frac{\sinh(k(s-t))}{k}F(s)\,ds\leq0.
\]
These formulas hold on every finite interior interval. Nonnegativity then gives $U\equiv0$ on its entire connected domain. Hence the asserted dichotomy $V>0$ everywhere or $V\equiv0$ is valid under the stated $C^2$ convention.

## 3. Exact zero-leading-weight classification

On every off-axis point, the quotient in the Hardy–Rellich integral is finite before multiplication by $V=0$, so the announced integral convention gives zero, without an indeterminate $0\cdot\infty$ operation. All derivative corrections and independent-function remainders vanish as asserted.

If $W>0$ at one radius, continuity gives a small spatial neighborhood of an off-axis point on which $W>0$. A nonzero smooth compact test there has strictly positive $\int W\psi u^2$. It also has strictly positive $\int W|\nabla_Gu|^2$: the neighborhood is off the axis, so the Grushin gradient is uniformly elliptic there, and a nonzero compact test cannot have identically zero gradient. Thus all the asserted necessity implications to $W\leq0$ hold. Sufficiency when $W\leq0$ is immediate.

Finally, with $V=0$, a strictly positive solution of $r^{Q-1}Wf=0$ exists exactly when $W\equiv0$. The comparison between the premise classification and the Bessel equation is therefore exact.

## Consequence for the separately proved nonnegative-potential branch

Combining this dichotomy with the accepted regular-weight nonnegative-$W$ Hardy–Rellich theorem extends that theorem from $V>0$ to the literal $V\geq0$, $V\in C^2$, side-conditioned class for $Q\geq4$: either $V>0$ and the regular theorem applies, or $V=0$ and the premise plus $W\geq0$ forces $W=0$, when any positive constant solves the equation.

This consequence remains specific to the proposed remainder-free antecedent with the source side condition and nonnegative $W$. It does not resolve other formulations or the historical $Q=3$ remainder-free branch.
