# Exact endpoint target for a growing-rank integrated module

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note does **not** exclude another graph class.  It freezes the exact
constructive variational problem exposed by the bounded growing-rank search.
It is the weakest local target currently known that would create a response
generator at fitness two after every uniform-start, core-recovery, successful
core-mark, and far-field term is included.

The search object is a finite connected loopless weighted gadget `H` with
internal weights `a_ij=a_ji>=0`, positive portal loads `x_i`, and

\[
                        d_i=x_i+\sum_j a_{ij}.         \tag{1}
\]

Unlike a separated satellite, the core portal remains active throughout
every polymorphic gadget state.  The order of `H` is allowed to grow.

## 1. Exact local success probabilities at `r=2`

For `U` in `{Bd,dB}`, let `u_U(S)` be the probability that the integrated
local trace produces a *surviving* mutant core lineage before the gadget
becomes empty, starting with mutant set `S`.  Thus `u_U(empty)=0`.  The trace
is defined directly from the update rules as follows.

For Bd, an internal ordered replacement `i -> j` has rate

\[
 {f_i a_{ij}\over d_i},\qquad
 f_i=\begin{cases}2&i\in S,\\1&i\notin S,\end{cases}   \tag{2}
\]

whenever `i,j` have different types.  A mutant `i` is erased by the resident
core at rate `x_i`.  A successful core mark occurs at rate

\[
                        m_B(S)=\sum_{i\in S}{x_i\over d_i}.  \tag{3}
\]

For dB, when vertex `j` dies its mutant and resident neighbour masses are

\[
 M_j(S)=2\sum_{i\in S\setminus\{j\}}a_{ij},\qquad
 R_j(S)=x_j+\sum_{i\notin S}a_{ij}.                \tag{4}
\]

It changes type with the corresponding probability
`M_j/(M_j+R_j)` or `R_j/(M_j+R_j)`.  A successful core mark has rate

\[
                        m_D(S)=\sum_{i\in S}x_i.       \tag{5}
\]

The factors in (3) and (5) are `rp=1` at `r=2`, where
`p=1-1/r`.  Consequently the exact finite harmonic system is

\[
 0=\sum_TL^U_{ST}\{u_U(T)-u_U(S)\}
      +m_U(S)\{1-u_U(S)\}.                         \tag{6}
\]

Write `u_U(i)=u_U({i})`.  Solving (6) is a finite rational operation whenever
the weights are rational.

## 2. Endpoint response scores

The full integrated-gadget response from the exact response library is

\[
 B_H={\sum_i u_B(i)\over p}-s+{s_B\over(r-1)^2},
 \qquad
 D_H={\sum_i u_D(i)\over p}-s+1+{s_D\over(r-1)^2}, \tag{7}
\]

where `s=|H|` and

\[
 s_B=r\sum_i x_i u_B(i)-(r-1)\sum_i{x_i\over d_i}, \tag{8}
\]

\[
 s_D=r\sum_i{x_i u_D(i)\over d_i}
             -(r-1)\left(\sum_i x_i+r-1\right).     \tag{9}
\]

Specializing (7)--(9) to `r=2` gives the vertexwise formulas

\[
 \boxed{\mathcal B(H,x)=
 \sum_i\left[2(1+x_i)u_B(i)-1-{x_i\over d_i}\right],} \tag{10}
\]

\[
 \boxed{\mathcal D(H,x)=
 \sum_i\left[2\left(1+{x_i\over d_i}\right)u_D(i)
                         -1-x_i\right].}             \tag{11}
\]

An ordinary leaf has endpoint response `(1,-1)`.  Therefore some
nonnegative density of ordinary leaves can balance `H` to make both endpoint
coordinates positive if and only if

\[
             \boxed{\mathcal D(H,x)>0,qquad
                    \mathcal S(H,x):=\mathcal B(H,x)+\mathcal D(H,x)>0.}
                                                               \tag{12}
\]

Equivalently, the exact leaf-eliminated score is

\[
 \boxed{\mathcal S(H,x)=\sum_i\left[
 2(1+x_i)u_B(i)
 +2\left(1+{x_i\over d_i}\right)u_D(i)
 -2-x_i-{x_i\over d_i}\right].}                  \tag{13}
\]

Indeed, adding leaf density `lambda` changes the endpoint response to
`(mathcal B+lambda, mathcal D-lambda)`.  Such a `lambda` exists precisely
when (12) holds.  This is the endpoint version of the exact general-fitness
conditions `D>0` and `D+(r-1)B>0`.

## 3. Constructive variational target

The next lower-bound milestone is now explicit:

> Find rational gadgets `(H_k,a^(k),x^(k))`, preferably with
> `|H_k| -> infinity`, for which (6) has endpoint singleton solutions obeying
> `mathcal D_k>0` and `mathcal S_k>0`, with margins large enough to dominate
> the compact-uniform finite-trace errors.

A robust version asks for a normalization `c_k>0` such that

\[
 \liminf_k{\mathcal D_k\over c_k}>0,
 \qquad
 \liminf_k{\mathcal S_k\over c_k}>0.                \tag{14}
\]

By continuity, any fixed strict witness gives a simultaneous response on a
left neighbourhood of two.  A sequence satisfying (14), together with the
already proved interval-cone diagonal and a finite overlap with the current
lower construction, would give one fitness-independent family reaching
every fixed `r<2`.  The overlap and uniform trace errors remain separate
proof obligations; an endpoint score alone is not asserted to prove
`R_sim>=2`.

Formula (13) is deliberately sharper than optimizing local fixation alone.
It shows exactly what a successful growing module must buy: its dB-weighted
singleton success must pay both the uniform vertex cost and total portal
load, while the combined Bd--dB success must also pay the reciprocal-degree
portal cost.

## 4. Bounded constructive cycle

As discovery triage, the exact two-count local chain was implemented for
integrated complete-bipartite gadgets `K_{a,b}` with independent portal
loads.  Searches through `a,b<=40` at fitness `1.7`, `1.9`, and `1.99`
converged to the zero-internal-weight portal-clone boundary; no positive
score was observed.  A positive-density clique--antenna block at order 25
was also dB-suppressing in the optimized screen.  These are numerical
observations only.  They do not prove a bipartite or antenna obstruction and
are not used in (10)--(14).

The useful outcome of the cycle is the exact target (12)--(13).  Further
search should optimize those rational harmonic scores directly over
growing-rank singular profiles, rather than accumulate more finite orbit
no-go examples.

## 5. Exact replay

`verify_endpoint_integrated_target.py` reconstructs (10)--(13) from the
general response, independently builds (6) for a rational two-vertex module,
and checks the endpoint scores by exact arithmetic.
