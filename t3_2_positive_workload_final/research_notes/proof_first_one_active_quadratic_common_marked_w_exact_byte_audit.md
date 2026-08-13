# Exact-byte hostile audit of the one-active quadratic common-\(W\) theorem

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes

\begingroup\scriptsize\ttfamily
research\_notes/proof\_first\_one\_active\_quadratic\_common\_marked\_w.md\par
SHA-256 7752373ac48894f009f635b056d80fd21265de7360601a11ad9ec0809002e534\par
259 lines, 9224 bytes
\endgroup

**Verdict: STRICT PASS at these exact bytes.**

The theorem is a genuine analytic replacement for the separate unmarked
quadratic potential.  It does not enumerate orientations, histories, or
populations.  It uses the same marked factorial \(W\) as the frozen
both-available and one-active Bellman branches, so transitions among those
branches incur no potential-switching toll.

## 1. Exact marked identity

At a reachable marked state \(x\ge t\), a labelled reaction \(e:y\to u\)
has endpoint and new mark \((x-y+u,u)\).  Therefore

\[
 F(x-y+u,u)-F(x,t)
 =\sum_i\log{(x_i-y_i)!\over(x_i-t_i)!}
 =\log{(x)_t\over(x)_y}.
\]

Writing \(\lambda_y=K_y(x)_y\), \(\Lambda=\sum_y\lambda_y\), and
\(p_y=\lambda_y/\Lambda\) gives

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-\log K_t+\sum_y p_y\log K_y.
\]

The finite entropy and rate menu give
\(D(x,t)\le\log p_t+C_K\).  Parallel labels do not alter the calculation:
labels with one source have the same factorial quotient and their rates sum
to \(K_y\).

For one source \(y\),

\[
 \left[\log{(x)_t\over(x)_y}\right]^+
 \le C+\log(1/p_y).
\]

Since \(s(C+\log(1/s))^r\) is bounded on \([0,1]\), summing over the finite
source set proves every stated fixed positive one-jump moment.  Disabled
sources have \(p_y=0\) and contribute zero; every carried target is enabled.

## 2. Quadratic dominance

In the binary universe, \(q=2X\) is the unique complex of \(X\)-degree two.
In a fixed padded inactive phase,

\[
 \lambda_q=K_qx_X(x_X-1)=\Theta(x_X^2),\qquad
 \lambda_y=O(x_X)\quad(y\ne q).
\]

These bounds are uniform over the finite phase.  Hence \(p_q\to1\) and
\(p_t=O(x_X^{-1})\) for every mark \(t\ne q\).  The one-jump rule for
\(t\ne q\) has

\[
 {\mathbb E}\Delta F=D(x,t)\le-\log x_X+O(1)\longrightarrow-\infty.
\]

This averages every enabled physical label; it does not condition on the
quadratic clock firing.

## 3. The nonrare mark \(t=q\)

Strong connectivity of the linkage containing \(q\), together with its
having at least two distinct vertices, supplies a fixed outgoing labelled
edge \(e:q\to u\) with \(u\ne q\).  Its exact first-jump probability is

\[
 a_e(x)={\kappa_e(x)_q\over\Lambda(x)}
        ={\kappa_e\over K_q}p_q(x)
        \longrightarrow{\kappa_e\over K_q}>0.
\]

There are two disjoint statewise cases.

1. If firing \(e\) is a named structural exit, the episode records an exit
   with probability bounded below for all sufficiently large \(x_X\).
2. If firing \(e\) is not an exit, its actual endpoint
   \(x'=x-q+u\) stays in the padded chart.  Since \(u_X\le1\),
   \(x'_X\to\infty\), \(q\) remains enabled, and
   \(p_u(x')=O(x_X^{-1})\).

In the second case the first ordinary jump is always taken and the second is
taken only on the literal event that label \(e\) fires.  The Markov property
therefore gives the exact all-clock recursion

\[
                    J(x,q)=D(x,q)+a_e(x)D(x',u).
\]

Here \(D(x,q)\le C_K\), whereas

\[
 a_e(x)D(x',u)
 \le a_e(x)\{-\log x_X+O(1)\}\longrightarrow-\infty.
\]

Thus \(J(x,q)\to-\infty\).  The proof does not apply this identity at a
state where \(e\) itself exits; those states use the first case.  Competing
labels remain present in the first \(D\), and the second \(D\) again
contains every clock at the actual endpoint.

Because the mark and padded phase range over finite sets, subselection
upgrades these alternatives to one uniform exterior finite set.  Equivalently,
the estimates on \(p_q\), \(a_e\), and \(p_u(x')\) are already uniform over
the finite phase.

## 4. Endpoints, moments, and physical time

Every rule contains at most two genuine population-changing reactions.
The exit-causing reaction is included once, and the endpoint is its actual
population with its actual physical target as mark.  Endpoint displacement
is bounded by two binary reaction increments.

The positive part of a two-jump increment is bounded by the sum of the
positive parts of its one-jump increments.  The inequality
\((a+b)^r\le2^{r-1}(a^r+b^r)\) and the one-jump bound prove all stated
fixed positive reward moments.  Independence between stages is unnecessary.

At each stage the carried target is enabled and has a positive outgoing
changing label.  Its falling factorial is an integer at least one, so the
total changing hazard is bounded below by the minimum positive labelled
rate.  Each holding time is dominated by one fixed exponential law; a sum
of at most two has all fixed moments uniformly.

After enlarging the finite exceptional set, embedded reward is at most
\(-2\).  Choosing \(\eta\) below the reciprocal of the uniform mean-duration
bound gives

\[
 {\mathbb E}[\Delta W+\eta\tau]\le-1.
\]

## 5. Common-potential scope

The function

\[
                  W(x,t)=1+\sum_i\log((x_i-t_i)!)
\]

is literally the same state function used by the both-available,
Bellman/Bellman, and repaired Bellman/Flat0 rules.  It is nonnegative and
proper because the finite mark cannot absorb an escaping population
coordinate.  Reclassification at an endpoint selects only the next episode
rule and does not change \(W\).  Hence no incoming chart seam charge arises
among this marked family.

The theorem correctly limits this conclusion.  It does not identify \(W\)
with the linear workload used by the separate all-active residual family,
and therefore does not by itself close the full T3-2 weighted seam.

## 6. Render verdict

The exact target was independently converted to MathJax HTML and compiled
through Tectonic using Pandoc's single-backslash TeX-math reader.  The result
was inspected page by page.  There is no compilation error, missing glyph,
clipped display, or overlap.

**FINAL VERDICT: STRICT PASS.**
