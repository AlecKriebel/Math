# A moving-cutoff fourth-power endpoint lemma

## 1. Claim boundary

This note isolates the arithmetic needed to stop a one-active physical
episode at a genuine promotion boundary.  It is an abstract lemma.  It does
not prove that every support/orientation in the candidate 1,227-pair table
satisfies the required boundary estimate, and it does not certify pair
recurrence or T3-2.

Let

\[
 F(x)=K+\sum_i\log(x_i!)+\ell\cdot x,
 \qquad G=1+F\ge1,
 \qquad W=G^4.                                      \tag{1.1}
\]

At a one-active base with active population \(N\), suppose a completed
regenerative episode repeats raw attempts until the first of:

* a strict active-debt reduction \(D\);
* an unresolved active increase \(U\); or
* a promotion boundary \(P\), where an inactive population first reaches
  \(L_N=N^\delta\).

Neutral base returns are not stopped separately: their physical endpoint
increments telescope inside the completed episode.

## 2. The endpoint balance

Assume that, for some \(m\in\{0,1,2\}\), the completed episode satisfies

\[
 \begin{aligned}
 \mathbb P(D)&=1-O(N^{-1})-\mathbb P(P),\\
 \mathbb P(U)&=O(N^{-1}),\\
 \mathbb E\tau&=O(N^3),                              \tag{2.1}
 \end{aligned}
\]

and that its fourth-power endpoint bounds are

\[
 \begin{aligned}
 \mathbb E[W(X_\tau)-W(x);D]
   &\le -cN^3(\log N)^4+CN^3(\log N)^3,\\
 \mathbb E[(W(X_\tau)-W(x))^+;U]
   &\le CN^2(\log N)^4.                              \tag{2.2}
 \end{aligned}
\]

The second line already includes the \(O(N^{-1})\) probability of the
upward terminal endpoint.  Suppose further that a raw attempt reaches the
moving boundary with probability at most

\[
 C N^{-3+6\delta},                                   \tag{2.3}
\]

and that the expected number of raw attempts in the completed episode is
at most \(CN^2\).  Hence

\[
 \mathbb P(P)\le C N^{-1+6\delta}.                   \tag{2.4}
\]

Before the first debt reduction, unresolved increase, or boundary hit, all
reaction vectors are bounded and the inactive population is at most
\(L_N\).  The active overshoot is therefore at most \(CL_N\) on the
boundary event.  The factorial finite-difference estimate gives

\[
 (W(X_\tau)-W(x))^+\le
 C N^{3+\delta}(\log N)^4                            \tag{2.5}
\]

there.  Combining (2.4)--(2.5),

\[
 \mathbb E[(W(X_\tau)-W(x))^+;P]
 \le C N^{2+7\delta}(\log N)^4.                     \tag{2.6}
\]

> **Lemma 2.1 (moving-cutoff balance).**  If \(0<\delta<1/7\), then for
> all sufficiently large \(N\),
> \[
>  \mathbb E_x[W(X_\tau)-W(x)+\tau]\le-1.           \tag{2.7}
> \]

Indeed, the negative term in (2.2) has order
\(N^3(\log N)^4\).  The neutral corrector, upward endpoint, and duration
have orders at most \(N^3(\log N)^3\),
\(N^2(\log N)^4\), and \(N^3\), respectively.  Equation (2.6) is lower
order precisely when \(2+7\delta<3\).

For definiteness, \(\delta=1/8\) leaves a polynomial margin.  If the phase
maximum has a factorial tail
\(\mathbb P(P)\le \exp[-cL_N\log L_N]\), the conclusion is stronger and
does not rely on the third-interruption estimate (2.3).

## 3. Why the boundary is genuine promotion

The base active population tends to infinity and
\(L_N=N^\delta\to\infty\).  Thus every sequence of boundary states has at
least two divergent coordinates.  On the exact candidate branch, every
affine-feasible failed descriptor is one-active.  Consequently every tier
subsequence of boundary states is a passing multi-active descriptor, and
the fourth-power Anderson--Kim estimate gives

\[
 \mathcal LW\longrightarrow-\infty.                 \tag{3.1}
\]

After (2.7), the ordinary common-potential gluing theorem may therefore
append the physical generator-good motion from the boundary.  It is not
necessary to call a fixed inactive-box exit promotion or to prove a
separate same-axis return estimate.

## 4. Exact remaining network input

To use Lemma 2.1 for the candidate 1,227-pair selector, one must still prove
uniformly over every strong allowed orientation that:

1. the aggregate debt-reduction/upward resistances give (2.1)--(2.2);
2. every finite or countable neutral phase has the endpoint and occupation
   moments needed to repeat at most \(O(N^2)\) raw attempts; and
3. either the phase maximum has a factorial tail, or reaching \(L_N\)
   requires at least three suppressed lower-source interruptions so that
   (2.3) holds.

No recurrence flag is changed by this note.
