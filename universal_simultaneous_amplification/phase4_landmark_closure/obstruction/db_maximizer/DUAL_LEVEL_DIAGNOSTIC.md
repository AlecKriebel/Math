# Complementary stationary levels in the dB dual

Status: **CONJECTURE OPEN; LISTED EXAMPLES EXACTLY VERIFIED.**

## 1. Forward recovery identity

Let `Pi` be the stationary law of the exact dB branching--coalescing dual at
fitness `r`, and write

\[
 \pi_k=\Pi(|A|=k).
\]

Let `F_s(r)` be forward dB fixation probability averaged uniformly over all
mutant sets of cardinality `s`.  Boolean duality says

\[
 \phi_r(S)=\Pr_\Pi(A\cap S\ne\varnothing).
\]

Conditional on `|A|=k`, a uniformly chosen `s`-set misses `A` with probability
`C(n-k,s)/C(n,s)`.  Therefore

\[
 1-F_s(r)=\sum_{k=1}^{n-s}\pi_k
 {\binom{n-k}{s}\over\binom ns}.
\]

Putting `s=n-t` gives the triangular identity

\[
 1-F_{n-t}(r)
 =\sum_{k=1}^t\pi_k
 {\binom{n-k}{t-k}\over\binom nt}.
\tag{1}
\]

Thus exact forward orbit values determine every dual level mass without
building the dual generator.  The recurrence used by the verifier is

\[
 \pi_t=\binom nt\{1-F_{n-t}(r)\}
 -\sum_{k<t}\pi_k\binom{n-k}{t-k}.
\tag{2}
\]

Type complementation gives `1-F_(n-t)(r)=F_t(1/r)`.  Binomial inversion of
(1) therefore also yields

\[
 \pi_k=\binom nk\sum_{t=0}^k(-1)^{k-t}
 \binom kt F_t(1/r).
\tag{3}
\]

## 2. Open complementary-level inequality

The conjecture is

\[
 k\pi_k\le(n-k)(r-1)^{2k-n}\pi_{n-k},
 \qquad k>{n\over2}.
\tag{4}
\]

The full-level case is the structural equality `pi_n=0`: because there are
no self-loops in the population graph, updating any occupied dual target
removes that target and cannot return it in the same burst.

For the complete graph at `r=2`,

\[
 \pi_k={\binom{n-1}{k}\over2^{n-1}-1},\qquad1\le k\le n-1,
\]

and (4) is an equality at every complementary pair.

At `r=2`, (4) has a useful but insufficient consequence.  The size-biased
level masses `k*pi_k` are skewed toward the lower member of each complementary
pair, so

\[
 E|A|^2\le {n\over2}E|A|.
\]

Jensen then gives `E|A|<=n/2`, or `rho_dB(G,2)<=1/2`.  This does not reach the
strictly smaller finite complete-graph value and therefore is not a universal
maximizer theorem.

## 3. Open degree-marked and hole-marked strengthenings

Let `delta_v` be weighted degree.  For either marker
`a_v=delta_v` or `a_v=1/delta_v`, define

\[
 O_k^{(a)}=\sum_{|A|=k}\Pi(A)\sum_{v\in A}a_v,
 \qquad
 H_k^{(a)}=\sum_{|A|=k}\Pi(A)\sum_{v\notin A}a_v.
\]

The occupied- and hole-marked conjectures are

\[
 O_k^{(a)}\le(r-1)^{2k-n}O_{n-k}^{(a)},
\tag{5}
\]

and

\[
 H_k^{(a)}\le
 \left({n-k\over k}\right)^2
 (r-1)^{2k-n}H_{n-k}^{(a)},
 \qquad k>n/2.
\tag{6}
\]

The squared prefactor in the hole version is forced by equality on `K_n`.
For a weighted-regular graph, both displays reduce exactly to (4).  For an
irregular graph they are genuinely different.  At `r=2`, the inverse-degree
occupied quantity has `O_1=D_H` and `sum_k O_k=C_H` in the arbitrary-module
reduction.  It therefore aligns with the open module invariant (M2), but has
not yet been shown to imply it.  The degree marker may be more compatible
with edge reversal because `delta_v P_vu=w_vu` is symmetric.

## 4. Exact audit

`verify_dual_level_windmills.py` solves exact forward orbit chains, applies
(2), verifies nonnegativity and normalization of every recovered `pi_k`, and
checks (4) over the rationals.

| graph and fitness | smallest non-full slack in (4) |
|---|---:|
| seven-vertex windmill, `r=3/2` | `0.00623526910322...` |
| seven-vertex windmill, `r=2` | `0.04664445934...` |
| nine-vertex windmill, `r=7/4` | `0.00263727115086...` |
| nine-vertex windmill, `r=2` | `0.00656387236261...` |
| eleven-vertex windmill, `r=9/5` | `0.00035938781578...` |
| eleven-vertex windmill, `r=2` | `0.000826992318089...` |
| `K_60` core plus three extreme pairs, `n=66,r=2` | `1.09446551161...e-27` |

Every entry is the decimal display of an exact nonnegative rational.  These
tests include all certified dB-amplifying windmills in this folder and the
closest floating-point false positive at `r=2`.  They are strong diagnostics,
not a proof of (4).

For the six windmill rows, the same verifier expands the exact orbit fixation
values to all labelled sets, uses Möbius inversion to recover `Pi(A)`, and
checks all four marker variants.  For inverse-degree occupied marks, the
smallest non-full slacks are respectively

    5.02956568555e-6,  3.58942778044e-5,
    4.51352823983e-10, 1.09796127829e-9,
    5.50574987622e-11, 1.2534157294e-10.

All are decimal displays of exact positive rationals.  Every degree-occupied,
inverse-degree-hole, and degree-hole slack is positive as well.  All four
marked conjectures also survived a discovery-only floating-point screen of
18,500 connected weighted graphs through seven vertices at each of
`r=3/2,2,3,5`.  Neither the exact finite audit nor the numerical screen is a
universal proof.

## 5. Exact failed likelihood-ratio route

The sequence

\[
 a_k={\pi_k\over\binom{n-1}{k}}
\]

is constant for `K_n` and appeared unimodal in the windmill examples.  It is
not universally unimodal.  At `r=2`, take the six-vertex weighted path in
vertex order `1-0-2-4-5-3`, with consecutive edge weights

    (30, 4, 64, 1, 1860).

Exact forward solution and binomial inversion give, in decimals,

    a = (0.1425372729, 0.0139149020, 0.0143349314,
         0.0009613481, 0.0000085613).

In particular, `a_1>a_2<a_3`, with exact positive difference
`a_3-a_2=0.0004200294...`.  Thus a monotone-likelihood-ratio or unimodality
argument cannot be used to strengthen (4).  The verifier checks this failure
over the rationals.
