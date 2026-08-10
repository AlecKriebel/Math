# Subpower tier regression for the rank-one physical phase

## 1. Why this regression is needed

The integral estimate in Proposition 4.2 of
`two_active_promotion_phase.md` is meaningful only when a sequence
**realizes the exact D-tier partition** of the displayed descriptor.  The
integer vector stored as `descriptor.weight` is a representative of an
order type; it is not necessarily the limit of normalized logarithms of a
realizing sequence.

For example, take

\[
 L_* = \{2A,A+B\},\qquad L_- = \{0,A,B\},
 \tag{1.1}
\]

and

\[
 A_n=\lfloor n/\log n\rfloor,\qquad B_n=n-A_n,
 \qquad C_n=c.
 \tag{1.2}
\]

Both active logarithmic exponents tend to one, but

\[
 (x_n)_{A+B}\gg (x_n)_{2A}\gg (x_n)_B\gg (x_n)_A\gg1.
 \tag{1.3}
\]

Thus (1.2) does **not** realize the flat face represented by
\(w=(1,1,0)\).  It realizes a proper-top order type, represented in the
finite arrangement by \(w=(4,5,0)\).  The exact tier certificate classifies
that refined descriptor by its descending-source gate.

This distinction is load-bearing.  If (1.2) were incorrectly assigned to
the flat face and \(y=A\) were selected while
\(a_n=\max\{1,A_n,B_n\}\asymp n\), then for top rates
\(A+B\to2A\) equal to \(\beta\) and \(2A\to A+B\) equal to
\(\alpha\),

\[
 {d\over dt}{\mathbb E}A(t)
 \le \beta n\,{\mathbb E}A(t),
\]

and hence

\[
 {mathbb E}\int_0^{T/a_n}A(t)\,dt
 \le {T A_n\over a_n}e^{\beta nT/a_n}
 =O((\log n)^{-1}).
 \tag{1.4}
\]

So the desired occupation estimate would fail under the normalized-log
misinterpretation.  Equation (1.4) is a regression guard, not a
counterexample to the exact-flat proposition.

## 2. Strongest presently justified one-clock statement

The rank-one calculation supports the following precise statement.

> **Exact-flat source occupation lemma.**  Let \(x_n\) realize an exact
> rank-one flat D-tier incidence. Equivalently, the surrogate D-monomials
> \((x_n\vee1)^u\) of every pair of complexes in the flat top linkage have
> a finite positive limiting ratio. For an enabled source the stochastic
> falling-factorial propensity differs only by a finite positive cap
> factor. Let \(y\) be an
> enabled complex in the maximal lower D-tier and put
> \(a_n=\max_{z\in L_-}(x_n\vee1)^z\).  After passage to a subsequence,
> \((x_n)_{y}/a_n\to c_y\in(0,\infty)\).  For the top-only chain there are
> sequence- and rate-dependent constants \(T,\eta,p>0\) such that
> \[
>  \mathbb P_{x_n}\left\{
>   \int_0^{T/a_n}(\widehat X_t^{(n)})_y\,dt\ge\eta
>  \right\}\ge p
> \]
> for all sufficiently large \(n\).

The statement applies directly to the 893 seeded rank-one incidences.  In
the two additional \(\{2A,B+C\}\) incidences with a missing inactive
cofactor, the same conclusion holds after the first top reaction creates
that cofactor.  It does not cover the 25 lower-layer activation incidences
or the ten identically disabled zero-boundary incidences.

The proof has three asymptotic templates.

1. For homogeneous quadratic supports, exact D-equivalence puts the active
   fractions in a compact subset of the appropriate accessible face.  The
   density process on time \(Nt\) has an inward quadratic fluid limit and
   martingale quadratic variation \(O(N^{-1})\).
2. For \(\{B,2A\}\), exact D-equivalence gives \(B/A^2\to b\in(0,\infty)\).
   On time \(At\), \(A/A_n\) has a positive Riccati limit and quadratic
   variation \(O(A_n^{-1})\).
3. For \(\{2A,B+C\}\), the top chain is exactly a one-dimensional
   birth--death chain, not literally an immigration--death chain.  On the
   relevant scale its birth rate is bounded above and below by constants
   times \(A_n^2\), while its death rate is comparable to
   \(A_n^2 I\), where \(I\) is the inactive population.  Stopped comparison
   with immigration--death chains gives uniform endpoint exponential
   moments and positive cofactor occupation on the \(1/A_n\) window.

The constants above are subsequence constants.  No compactness uniformity
over all possible within-tier limiting ratios is asserted.  The lemma also
installs only one lower killing clock.  Restoring every competing lower
reaction still requires the open carrier/resolvent theorem recorded in
Section 6 of `two_active_promotion_phase.md`.

## 3. Regression command

Run

```text
PYTHONPATH=src python3 -B -m unittest \
  tests/test_two_active_subpower_regression.py -v
```
