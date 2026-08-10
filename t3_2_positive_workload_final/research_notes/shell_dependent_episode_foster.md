# Shell-dependent physical episodes

## 1. Why uniform service is stronger than necessary

The nested-entry regression in
*one_active_nested_entry_obstruction.md* shows that a valid one-active
network may have service probability of order \(N^{-m}\), even though the
physical episode is stabilizing.  A uniform service minorization is
therefore not an admissible global hypothesis for T3-2.

What random-time Foster theory actually needs is a uniform **expected
potential drop**.  A rare event can provide that drop when its successful
endpoint moves a shell-adapted potential by order \(N^m\).  The elementary
lemma below records the exact bookkeeping.  It is an abstract analytic
lemma, not a recurrence claim for any unresolved support pair.

## 2. Rare macroscopic service

Let \(Z\) be a nonexplosive CTMC and let \(W\geq0\) be a proper function.
Assume also that the shell map \(n\) has finite sublevel sets on the bad
region (equivalently for this lemma, that the estimates below hold outside
one finite set).  For every state \(z\) in a bad region, let
\(n=n(z)\geq1\), let \(\tau_z\)
be a strong-Markov-compatible stopping time, and let \(G_z\in
\mathcal F_{\tau_z}\).  Suppose that, as \(n\to\infty\) through the bad
region, there are constants \(b,d,T>0\) and an integer \(m\geq1\) such
that

\[
 \mathbb P_z(G_z)\geq b n^{-m},                         \tag{2.1}
\]

\[
 W(Z_{\tau_z})-W(z)\leq-dn^m\quad\hbox{on }G_z,         \tag{2.2}
\]

\[
 \mathbb E_z\!\left[(W(Z_{\tau_z})-W(z))^+;
                     G_z^c\right]=o(1),                \tag{2.3}
\]

and

\[
 \sup_z\mathbb E_z\tau_z\leq T.                       \tag{2.4}
\]

Then

\[
 \mathbb E_z\{W(Z_{\tau_z})-W(z)\}
 \leq-bd+o(1).                                         \tag{2.5}
\]

Consequently, after deleting a finite set and multiplying \(W\) by a
fixed constant \(M\), the same episodes satisfy

\[
 \mathbb E_z\!\left[
   MW(Z_{\tau_z})-MW(z)+\tau_z
 \right]\leq-1.                                       \tag{2.6}
\]

Indeed, (2.5) is obtained by splitting on \(G_z\).  Eventually its
right-hand side is at most \(-bd/2\); the finite-sublevel hypothesis makes
the states excluded by “eventually” a finite set.  Any
\(M>2(T+1)/(bd)\) proves (2.6).  Thus a probability of order \(n^{-m}\)
is harmless when the successful potential drop is of order \(n^m\).

The bounded-duration hypothesis can be replaced by
\(\mathbb E_z\tau_z=O(n^q)\) if the successful potential drop in (2.2)
is strengthened to order \(n^{m+q}\), or if a separate proper time-cost
term supplies that scale.  The displayed bounded version is the one
needed for a single primary-entry attempt in the nested-entry regression.

## 3. Two useful polynomial corollaries

Let \(H\geq1\) be an integer shell coordinate.

### Unit service

If

\[
 \mathbb P_z\{H(Z_{\tau_z})\leq H(z)-1\}
 \geq bH(z)^{-m},                                      \tag{3.1}
\]

then the successful drop of

\[
 W(z)=H(z)^{m+1}                                       \tag{3.2}
\]

is at least \(H(z)^m\).  Hence (2.1)--(2.2) hold with
\(n=H(z)\) and \(d=1\).  The load-bearing remaining condition is the
positive-endpoint estimate (2.3); a service probability by itself does
not imply it.

### Fractional service

If, for some \(\rho\in(0,1)\),

\[
 \mathbb P_z\{H(Z_{\tau_z})\leq(1-\rho)H(z)}
 \geq bH(z)^{-m},                                      \tag{3.3}
\]

then \(W=H^m\) has successful drop at least

\[
 \{1-(1-\rho)^m\}H(z)^m.                              \tag{3.4}
\]

Again, recurrence follows only after (2.3), duration integrability, and
the global common-potential interface have been proved.

## 4. Exact quadratic sign in the nested-entry model

For the regression network, condition on the primary entry from the base
\((A,B,C)=(0,0,N)\).  Its activation probability has the expansion

\[
 p_N={\gamma\over N^2}+O(N^{-3}),\qquad
 \gamma={\alpha\kappa_4\over\beta^2}>0.               \tag{4.1}
\]

Suppose a stopped post-activation averaging theorem gives

\[
 {C_{\rm end}\over N}\Longrightarrow R,qquad
 0\leq R\leq1,\qquad \mathbb P\{R<1\}>0,              \tag{4.2}
\]

with the uniform integrability needed to multiply (4.2) by the rare
activation indicator.  Then

\[
 \mathbb E\{C_{\rm end}^2-N^2\}
 =\gamma\,\mathbb E(R^2-1)+o(1)<0.                    \tag{4.3}
\]

In the formal fast limit

\[
 R=\exp\!\left\{-2\kappa_1\int_0^T B(s)\,ds\right\}, \tag{4.4}
\]

possibly stopped on a bounded-core or promotion boundary.  Since the
integral is positive with positive probability when the activated phase
starts at \(B=1\), the sign in (4.3) is strictly negative for every
positive rate vector.  This explains why the counterexample to uniform
minorization is not a leading-order counterexample to T3-2.

The unresolved analytic work is precisely the hypothesis suppressed in
(4.2): stopped averaging, positive-endpoint uniform integrability, and
composition with promotion returns.  Those obligations must be proved
before (4.3) is promoted from a repair target to a network theorem.

## 5. The replacement gate for one-active debt

A valid replacement for the false uniform old-debt lemma must establish,
for every exact one-active source-rate flag, one of the following.

1. A unit service whose probability is bounded below by \(cN^{-m}\),
   together with (2.3) for \(H^{m+1}\) or a globally compatible marked
   potential.
2. A macroscopic service satisfying (3.3), with (2.3) for \(H^m\).
3. Promotion to a previously controlled higher-dimensional descriptor,
   with the promotion endpoint and return cost included in the same
   potential.
4. An affine invariant or finite class that makes the flag nonescaping.

Because the complex menu is finite and bimolecular, a finite certificate
can enumerate the slow-before-fast depth \(m\).  The analytic theorem must
still prove that positive unresolved entries have strictly smaller
weighted cost than the chosen service and that all endpoint tails are
uniformly integrable.  Merely finding a reverse reaction path or a
pointwise positive service rate is insufficient.
