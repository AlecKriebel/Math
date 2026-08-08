# The factorial-moment route at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

Let `Pi_P` be the invariant law of the proper fair-geometric union dual and
put `K=|A|` for `A~Pi_P`.  Exact finite calculations support the hierarchy

\[
 M_j(P):=E\binom Kj\le
 M_j(K_n):={\binom{n-1}{j}2^{n-1-j}\over 2^{n-1}-1},
 \qquad 1\le j\le n-1.                         \tag{FM}
\]

The case `j=1` is precisely the open universal fitness-two theorem.  No
member of `(FM)` is proved here for arbitrary order.  The purpose of this
note is to record the exact stationarity recurrence, the positive coverage
kernel behind it, the hostile exact screen, and the obstruction to a naive
total-positivity induction.

The exact screen covers 54 connected weighted graphs of order three, 624 of
order four, 48 seeded sparse/extreme graphs of order five, and the frozen
order-six split and rank-tail witnesses.  Every factorial-moment slack is
nonnegative.  These are implementation checks and evidence, not a proof.

## 1. The proper geometric-union chain

Let `P` be a loopless irreducible row-stochastic kernel on `V`, `|V|=n`.
For the graph problem `P` is reversible, although the identities below do
not yet use reversibility.  Given a nonempty proper set `A`, choose `v`
uniformly.  If `v` is not in `A`, leave `A` unchanged.  If `v` is in `A`,
delete it and adjoin the distinct values among `J` independent samples from
row `P_v`, where

\[
 \Pr(J=q)=2^{-q},\qquad q\ge1.                    \tag{1}
\]

Looplessness guarantees that `v` is not immediately reinserted, so proper
sets map to proper sets.  The chain is irreducible for the admissible graph
kernels and has a unique invariant law `Pi_P`.

Write `N=n-1`.  On the complete kernel the invariant rank law is

\[
 \Pr(K=k)={\binom Nk\over 2^N-1},\qquad 1\le k\le N,              \tag{2}
\]

which gives the right side of `(FM)`.

## 2. Exact burst-coverage tensors

For a row `p=(p_i)` and a nonempty named set `T`, let

\[
 c_p(T)=\Pr(T\subseteq U),                         \tag{3}
\]

where `U` is the distinct-value set in the burst.  Inclusion--exclusion and
`E[x^J]=x/(2-x)` give

\[
 \begin{aligned}
 c_p(T)
 &=\sum_{R\subseteq T}(-1)^{|R|}
       {1-p(R)\over1+p(R)}\\
 &=2\sum_{R\subseteq T}{(-1)^{|R|}\over1+p(R)}\\
 &=2\int_0^\infty e^{-s}
       \prod_{i\in T}(1-e^{-sp_i})\,ds.            \tag{4}
 \end{aligned}
\]

Here `p(R)=sum_{i in R}p_i`; the second line uses `T` nonempty.  In
particular every coverage coefficient is nonnegative.  For `H subseteq V`
define

\[
 C_{p,0}(H)=1,
 \qquad
 C_{p,ell}(H)=\sum_{\substack{T\subseteq H\\|T|=ell}}c_p(T).      \tag{5}
\]

The conditional burst PGF is therefore absolutely monotone in `x=t-1>=0`:

\[
 E[t^{|U\cap H|}]
 =\sum_{ell\ge0}C_{p,ell}(H)(t-1)^{ell}.           \tag{6}
\]

There is also a useful Schur-concavity fact.  From `(4)`, for fixed `s>0`
and `t>=1`,

\[
 \log\{t-(t-1)e^{-sp}\}
\]

is concave in `p`.  Hence, with `p(H)` and `|H|` fixed, the integrand in
the PGF is maximized by equal masses on `H`.  This positivity is genuine,
but it is not by itself a comparison with the complete transition because
the total row mass `p(H)` is neither fixed nor independent of the stationary
state.

## 3. Exact falling-factorial stationarity recurrence

Fix `A`, put `k=|A|`, `H=V minus A`, and take an active target `v in A`.
After deleting `v`, the retained set has size `k-1`; the only new vertices
that affect the rank are the burst hits in `H`.  Vandermonde's identity and
`(5)` give

\[
 E\left[\binom{|A'|}{j}\mid A,v\right]
 =\sum_{ell=0}^j
   \binom{k-1}{j-ell}C_{P_v,ell}(H).               \tag{7}
\]

Average `(7)` over the uniform target and the stationary law.  The
`ell=0` term obeys

\[
 k\left\{\binom{k-1}{j}-\binom kj\right\}
 =-j\binom kj.
\]

Consequently the exact recurrence is

\[
 \boxed{
 jM_j(P)=E_{A\sim\Pi_P}
 \sum_{v\in A}\sum_{ell=1}^j
 \binom{|A|-1}{j-ell}C_{P_v,ell}(V\setminus A).}   \tag{8}
\]

For `j=1`, this reduces to the familiar exact rank-drift identity

\[
 \boxed{
 M_1(P)=E\sum_{v\in A}\sum_{i\notin A}
 {2P_{vi}\over1+P_{vi}}.}                         \tag{9}
\]

For the complete row, every `s`-set has coverage probability

\[
 c_K(T)={2\over\binom{N+s}{s}},\qquad s=|T|\ge1,                 \tag{10}
\]

and substituting `(10)` into `(8)` recovers `(2)` and the complete moments.

## 4. Why the recurrence does not yet give an induction

Equation `(8)` is triangular in the formal order `j`, but it is not a
closed recurrence for the scalar moments.  Its coefficients
`C_{P_v,ell}(V minus A)` depend jointly on the labelled state and the active
row.  In particular, the base equation `(9)` is already exactly the unknown
mean inequality; higher-order equations do not supply a downward induction
to it.

Nor is there a pointwise complete-transition comparison.  On the unweighted
path `0-1-2-3`, take `A={0,2,3}` and update `v=0`.  The path row samples the
unique hole `1` with probability one, so the new rank is three surely.  The
complete row hits that hole with probability one half, so its new rank is
three or two with equal probabilities.  Thus, for `1<=j<=3`,

\[
 E_P\binom{|A'|}{j}-E_K\binom{|A'|}{j}
 ={1\over2}\binom{2}{j-1}>0.                      \tag{11}
\]

The burst-coverage transform has positive coefficients and a useful
integral representation, but even every conditional factorial moment can
point in the wrong direction.  Any successful total-positivity proof must
therefore incorporate stationary labelled correlations (and, for the graph
problem, probably reversibility); positivity of the one-step burst kernel
alone cannot prove `(FM)`.

## 5. PGF interpretation and exact scope

Since

\[
 E[t^K]=\sum_{j=0}^{N}M_j(P)(t-1)^j,               \tag{12}
\]

the entire hierarchy `(FM)` implies

\[
 E_{\Pi_P}[t^K]
 \le{(1+t)^N-1\over2^N-1},\qquad t\ge1.           \tag{13}
\]

This is distinct from the marked-cache PGF conjecture on `0<=t<=1`, which
has an exact order-six counterexample in the sibling `r2_pgf_order`
package.  It is also distinct from rank-tail domination, already refuted.

Current classification:

- **PROVED:** coverage identities `(4)`--`(6)` and stationarity recurrence
  `(8)`;
- **EXACTLY REFUTED:** pointwise complete-transition factorial domination;
- **EXACTLY COMPUTED:** all members of `(FM)` on the stated finite corpus;
- **OPEN:** every universal member of `(FM)`, including the target `j=1`.

