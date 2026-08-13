# One-active quadratic charts with the common marked factorial potential

**Proof-first seam-avoidance theorem, 2026-08-12 PDT.**  This note replaces
the separate unmarked generator potential previously used for the
one-active quadratic branch.  The quadratic branch admits the same marked
factorial potential as the both-available, Bellman/Bellman, and repaired
Bellman/Flat0 branches.  The physical episode has at most two ordinary
jumps, retains every competing clock, and stops at an actual population and
target mark.

No orientation, rate vector, reaction history, or population box is
enumerated.  The proof is one application of the exact marked factorial
identity and the fact that $2X$ is the unique binary source with
$X$-degree two.

## 1. Scope and the common marked chain

Fix a reduced binary stochastic mass-action network with at most three
dynamic species.  Write them as $X,U,V$, allowing one or both of $U,V$
to be absent.  Fix a closed irreducible population class, arbitrary strongly
connected linkage orientations, and arbitrary fixed positive labelled rate
constants.  Work in one terminal one-active chart

\[
             x_X\longrightarrow\infty,
             \qquad (x_U,x_V)\in B,                         \tag{1.1}
\]

where $B$ is a fixed finite padded phase.  Every reaction which changes a
declared active set, inactive box, enabled-source flag, support, shell, or
ratio cell is retained as a named structural exit.

Assume one active linkage contains

\[
                              q=2X.                         \tag{1.2}
\]

After every ordinary population-changing labelled reaction, mark the
physical target $t$.  At a marked state $(x,t)$, necessarily $x\ge t$.
Put

\[
 F(x,t)=\sum_i\log((x_i-t_i)!),
 \qquad W(x,t)=1+F(x,t).                                  \tag{1.3}
\]

This is exactly the potential used in the current-target Bellman theorem.
It is nonnegative and proper on the reachable marked state space: the mark
ranges over a finite binary complex set, so $\lvert x\rvert_1\to\infty$
forces some $x_i-t_i\to\infty$.

For a source complex $y$, let

\[
 K_y=\sum_{e:s(e)=y}\kappa_e,
 \qquad \lambda_y(x)=K_y(x)_y,
 \qquad p_y(x)={\lambda_y(x)\over\sum_z\lambda_z(x)}.      \tag{1.4}
\]

If the next labelled reaction is $e:y\to u$, its marked endpoint is
$(x-y+u,u)$, and cancellation is exact:

\[
 F(x-y+u,u)-F(x,t)=\log{(x)_t\over(x)_y}.                 \tag{1.5}
\]

Consequently the expected increment of one ordinary all-clock jump is

\[
 D(x,t)=\log p_t(x)-\sum_y p_y(x)\log p_y(x)
        -\log K_t+\sum_y p_y(x)\log K_y,                  \tag{1.6}
\]

and finiteness of the source set gives

\[
                         D(x,t)\le \log p_t(x)+C_K.        \tag{1.7}
\]

For every fixed $r<\infty$, the positive one-jump reward also satisfies

\[
 \sup_{x,t}\sum_y p_y(x)
       \left[\log{(x)_t\over(x)_y}\right]_+^r<\infty.     \tag{1.8}
\]

Indeed, sourcewise (1.6) bounds the positive logarithm by a fixed constant
plus $\log(1/p_y)$, and
$s(1+\log(1/s))^r$ is bounded on $[0,1]$.

## 2. The quadratic dominance estimate

The binary universe has only one complex with $X$-degree two, namely
$q=2X$.  Uniformly for $(x_U,x_V)$ in the finite padded phase,

\[
 \lambda_q(x)=K_q x_X(x_X-1)=\Theta(x_X^2),
 \qquad
 \lambda_y(x)=O(x_X)\quad(y\ne q).                        \tag{2.1}
\]

Therefore

\[
 p_q(x)\longrightarrow1,
 \qquad
 p_t(x)=O(x_X^{-1})\quad(t\ne q).                         \tag{2.2}
\]

If the carried target is $t\ne q$, take one ordinary all-clock jump and
stop.  Equations (1.7) and (2.2) give

\[
                 \mathbb E_{x,t}\Delta F=D(x,t)
                    \longrightarrow-\infty.              \tag{2.3}
\]

It remains only to treat the nonrare mark $t=q$.

## 3. The two-jump rule from the mark $q$

Strong connectivity of the linkage containing $q$, whose support has at
least two distinct vertices, supplies one fixed nonzero labelled edge

\[
                              e:q\longrightarrow u,
                              \qquad u\ne q.               \tag{3.1}
\]

Starting from $(x,q)$, take the next ordinary all-clock jump.

1. If a competing label fires, stop at its actual endpoint and target mark.
2. If $e$ fires and causes a named structural exit, include it, record the
   exit, and stop at its actual endpoint and mark.
3. If $e$ fires without an exit, take one further ordinary all-clock jump
   from its marked endpoint and stop there, including any exit caused by
   that second jump.

Thus every episode contains one or two ordinary jumps, and every physical
clock competes at both stages.  Put

\[
 x'=x-q+u,
 \qquad
 a_e(x)={\kappa_e(x)_q\over\sum_z\lambda_z(x)}.            \tag{3.2}
\]

If case 2 persists along an escaping chart sequence, then by (2.2)

\[
                a_e(x)={\kappa_e\over K_q}p_q(x)
                      \longrightarrow{\kappa_e\over K_q}>0, \tag{3.3}
\]

so the episode records a structural exit with uniformly positive
probability.

Otherwise the endpoint $x'$ remains in the fixed padded chart.  Since
$u\ne q$, it has $X$-degree at most one.  Also
$x'_X=x_X-2+u_X\to\infty$, so the quadratic source remains enabled and

\[
                         p_u(x')=O(x_X^{-1}).              \tag{3.4}
\]

Let $J(x,q)$ be the expected total $F$-increment of the rule.  The first
ordinary jump contributes its full all-clock expectation $D(x,q)$.  Only
the literal event that $e$ fires launches the second jump.  Hence the
Markov property gives the exact Bellman identity

\[
                    J(x,q)=D(x,q)+a_e(x)D(x',u).           \tag{3.5}
\]

By (1.7), $D(x,q)\le C_K$.  By (1.7), (3.3), and (3.4), the second term in
(3.5) tends to minus infinity.  Therefore

\[
                              J(x,q)\longrightarrow-\infty. \tag{3.6}
\]

Together, (2.3) and (3.6) prove a uniform finite-menu alternative: outside
a finite subset of the fixed chart, the selected one- or two-jump rule
either records a named physical exit with a fixed positive probability, or

\[
                 \mathbb E_{x,t}[W(X_\tau,T_\tau)-W(x,t)]
                              \le-2.                       \tag{3.7}
\]

Uniformity follows without a quantitative compactness guess: if it failed,
a violating sequence has a fixed mark and fixed padded phase along a
subsequence, and the corresponding limit (2.3) or (3.6) contradicts it.

## 4. Endpoints, moments, duration, and nonoverlap

The endpoint in every case is the actual endpoint of the last included
physical reaction, with that reaction's actual target mark.  Its population
displacement from the start is bounded by two binary reaction increments.

Applying (1.8) at the first and possible second stage and using
$(a+b)^r\le 2^{r-1}(a^r+b^r)$ shows, for every fixed $1\le r<\infty$,

\[
       \sup\mathbb E_{x,t}
       \left([W(X_\tau,T_\tau)-W(x,t)]^+\right)^r<\infty.  \tag{4.1}
\]

At every stage the carried target is enabled.  Its falling factorial is a
positive integer, and its linkage has a positive outgoing labelled rate.
If $\kappa_*>0$ is the minimum positive labelled rate, the total hazard is
at least $\kappa_*$.  A sum of at most two such holding times has all fixed
moments, so

\[
                         \sup\mathbb E_{x,t}\tau^r<\infty. \tag{4.2}
\]

Choose $\eta>0$ smaller than the reciprocal of the uniform mean-duration
bound.  Shrinking the exterior finite set if necessary, (3.7) gives the
physical-time inequality

\[
 \mathbb E_{x,t}
   [W(X_\tau,T_\tau)-W(x,t)+\eta\tau]\le-1.               \tag{4.3}
\]

When episodes are concatenated, the last reaction of the current episode is
never counted as the first reaction of the next.  Its actual target merely
selects the next rule after the endpoint is reached.  A finite surrounding
chart cover may therefore reclassify that endpoint under the same function
$W$, without a comparison toll.  This is the exact common-potential
interface shared by the other marked Bellman branches.

## 5. The seam-avoidance theorem

> **Theorem 5.1 (quadratic branch with common marked \(W\)).**  In every
> fixed one-active chart (1.1) whose reduced support contains \(2X\), for
> every strongly connected orientation and every fixed positive labelled
> rate vector, the common marked factorial potential (1.3) admits a finite
> menu of one- or two-jump all-clock physical episodes satisfying the
> following alternative outside a finite set:
>
> 1. the episode obeys the physical-time drift inequality (4.3); or
> 2. it records a named structural-exit reaction with uniformly positive
>    probability.
>
> Every episode ends at its actual physical endpoint and mark, has bounded
> depth, all fixed positive reward moments, and all fixed duration moments.
> Episodes concatenate without overlap.  Hence the one-active quadratic
> branch may be composed with the both-available, Bellman/Bellman, and
> Bellman/Flat0 branches using the identical proper marked potential \(W\);
> no terminal-chart potential switch or weighted seam estimate occurs among
> those branches.

The theorem is local to the quadratic one-active branch.  It does not claim
that a direct linear workload used on a different all-active family agrees
with $W$; that separate interface must still be closed or avoided.
