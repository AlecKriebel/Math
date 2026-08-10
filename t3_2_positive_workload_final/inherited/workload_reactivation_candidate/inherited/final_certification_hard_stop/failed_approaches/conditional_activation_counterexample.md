# Exact counterexample to the conditional terminal-payoff claim

## The failed claim

The proposed repair asserted that, after conditioning on the first reaction
from a selected linkage and appending a fixed target-following path, the
complete conditional payoff tends to minus infinity whenever the selected
terminal source is rare.  This is false.  Conditioning removes the
source-probability factor that drives the scalar envelope.

## Network

Consider the one-linkage bimolecular directed cycle, with all rates one,

\[
0\longrightarrow 2A\longrightarrow A\longrightarrow0.
\]

It is weakly reversible.  At population `n`, condition on the rare channel
`0 -> 2A`.  Use the state-buffered factorial potential

\[
\Phi(n)=\log((n+2)!).
\]

After the conditioned channel the population is `n+2`.  Follow the fixed
path

\[
2A\longrightarrow A\longrightarrow0,
\]

stopping on the first deviation, and after reaching `0` take one final
ordinary jump.  This is exactly the conditional activation block used in the
proposed G3 repair, specialized to one linkage.

At population `x`, the embedded source probabilities are

\[
p_0(x)=\frac1{x^2+1},\qquad
p_A(x)=\frac{x}{x^2+1},\qquad
p_{2A}(x)=\frac{x(x-1)}{x^2+1}.
\]

Let `J_n` be the expected complete change of `Phi`, including the conditioned
activation.  Direct branch enumeration gives

\[
J_n=\sum_{j=2}^{6}c_j(n)\log(n+j),
\]

where, with

\[
D=(n^2+1)(n^2+2n+2)(n^2+4n+5),
\]

\[
\begin{aligned}
c_2&=-\frac{n^2(n+1)^2(n+2)}D,\\
c_3&=\frac{n^5+6n^4+13n^3+18n^2+16n+10}D,\\
c_4&=\frac{2(n^4+3n^3+5n^2+5n+3)}D,\\
c_5&=\frac{2n^2+5n+4}{(n^2+2n+2)(n^2+4n+5)},\\
c_6&=\frac1{n^2+4n+5}.
\end{aligned}
\]

Writing `log(n+j)=log n+log(1+j/n)` and expanding rationally at infinity
shows

\[
J_n=\frac{7\log n+1}{n^2}
     +O\!\left(\frac{\log n}{n^3}\right).
\]

In particular,

\[
\lim_{n\to\infty}\frac{n^2J_n}{\log n}=7,
\qquad
J_n\to0^+.
\]

Thus the conditional payoff does not tend to minus infinity; it is eventually
positive.  The physical chain is nevertheless positive recurrent.  The
counterexample invalidates only the conditional activation lemma, not the
single-linkage theorem.

## What remains possible

A valid multi-linkage proof must retain the probability and reward of the
activation channel in one rate-weighted source-layer identity.  It may not
condition on the activation and then apply the old scalar envelope to the
post-activation target episode.
