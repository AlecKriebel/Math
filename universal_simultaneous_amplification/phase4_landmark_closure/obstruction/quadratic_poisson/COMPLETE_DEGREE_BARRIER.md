# Exact degree barrier for complete-graph Poisson certificates

Date: 2026-08-02 (America/Los_Angeles)

## Theorem

Let `n>=3`, let `D` be the `r=2` geometric-union dB-dual generator on the
unit complete graph `K_n`, and put

\[
 m_K=\frac{(n-1)2^{n-2}}{2^{n-1}-1}.
\]

Suppose a Boolean polynomial `g` satisfies

\[
 \mathcal Dg(A)\ge |A|-m_K                         \tag{1}
\]

for every nonempty proper set `A`.  Then the Boolean degree of `g` is at
least `n-2`.  Conversely, a certificate of degree at most `n-2` exists.
Thus the exact minimum degree is `n-2`.

In particular, no bounded-degree Poisson-certificate architecture can prove
the exact complete-graph mean ceiling uniformly in `n`: even the equality
case `G=K_n` forces the degree to diverge.

## Proof

### 1. Symmetrization turns `g` into a polynomial in the level

Average `g` over all permutations of the vertices.  This preserves Boolean
degree and preserves (1), because the graph, generator, and target are all
permutation invariant.  A symmetric Boolean polynomial of degree `d` has
the form

\[
 p(k)=\sum_{j=0}^d a_j\binom{k}{j},\qquad k=|A|.   \tag{2}
\]

The complete-graph dual restricted to the proper levels
`k=1,...,n-1` is irreducible.  Its stationary law gives positive mass to
every level and has mean `m_K`.  Taking stationary expectations in (1)
therefore gives equality, and positivity of every stationary level mass
forces

\[
 \mathcal Dp(k)=k-m_K,qquad k=1,\ldots,n-1.       \tag{3}
\]

### 2. Exact factorial moments of one geometric burst

Write `q=n-1`.  When one occupied target is updated at level `k`, there are
`q` possible sampled neighbors, of which `n-k` are outside the current
set.  Let `J` be the number of distinct outside vertices appearing in the
geometric burst.  The new level is `k-1+J`.

For `s` fixed named neighbor vertices, inclusion--exclusion and the
geometric probability generating function give

\[
 \Pr(\hbox{all }s\hbox{ appear})
 =\sum_{j=1}^s(-1)^{j+1}\binom{s}{j}\frac{2j}{q+j}
 =\frac{2}{\binom{q+s}{s}}.                         \tag{4}
\]

For completeness, the last identity follows from

\[
 \sum_{j=0}^s\frac{(-1)^j\binom{s}{j}}{q+j}
 =\int_0^1t^{q-1}(1-t)^s\,dt.
\]

Consequently

\[
 E\binom Js
 =\frac{2\binom{n-k}{s}}{\binom{q+s}{s}}.          \tag{5}
\]

Vandermonde's identity now gives, for `F_d(k)=binom(k,d)`,

\[
 \mathcal DF_d(k)
 =k\left[-\binom{k-1}{d-1}
 +2\sum_{s=1}^d
 \frac{\binom{k-1}{d-s}\binom{n-k}{s}}
      {\binom{q+s}{s}}\right].                       \tag{6}
\]

### 3. The generator raises polynomial degree

For every `d>=1`, the right side of (6) is a polynomial in `k` of degree
exactly `d+1`.  Its leading coefficient is

\[
 \frac2{d!}\sum_{s=1}^d
 \frac{(-1)^s\binom ds}{\binom{q+s}{s}}
 =-\frac{2}{(d-1)!(q+d)}\ne0.                        \tag{7}
\]

Indeed, after including the `s=0` term, the sum in (7) is evaluated by

\[
 \sum_{s=0}^d\frac{(-1)^s\binom ds}{\binom{q+s}{s}}
 =q\int_0^1t^{q-1}
   \sum_{s=0}^d\binom ds[-(1-t)]^s\,dt
 =\frac q{q+d}.                                      \tag{8}
\]

If `p` in (2) has degree `d>=1`, equation (7) shows that `Dp` has degree
exactly `d+1`.  If `d<=n-3`, then

\[
 \mathcal Dp(k)-(k-m_K)
\]

has degree at most `n-2` but, by (3), has the `n-1` distinct roots
`1,...,n-1`.  It must be the zero polynomial.  This is impossible because
`Dp` has nonzero degree `d+1>=2`.  A constant `p` is impossible as well,
since its generator is zero.  Therefore `d>=n-2`.

### 4. Sharpness

On the irreducible proper-level chain, the Poisson equation

\[
 \mathcal Dh(k)=k-m_K
\]

is solvable because the right side has stationary mean zero.  Its values on
the `n-1` levels can be interpolated by a polynomial of degree at most
`n-2`.  Expressing that polynomial in the binomial basis (2) realizes it as
a symmetric Boolean polynomial of degree at most `n-2`.  This proves
sharpness.  QED.

## Interpretation

The theorem does **not** refute the conjecture that `K_n` maximizes dB
fixation at `r=2`.  It refutes a proposed proof strategy: an exact
pointwise Poisson inequality with degree bounded independently of `n` cannot
work, because its degree must already grow linearly on the baseline graph.

