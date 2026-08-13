# Exact-byte hostile audit of the corrected tier-pass common-
# \(W\) theorem

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes

```text
research_notes/proof_first_corrected_tier_pass_common_marked_w_theorem.md
SHA-256 b9054d036609713a42728ea2a30db074aa09a4f48d505240dd92588c7721e1f5
288 lines, 10,973 bytes
```

**Verdict: STRICT PASS at these exact bytes, at the theorem's literal local
drift-or-exit scope.**

The target proves the marked, all-clock analytic estimate missing from the
bare corrected tier cut.  It does not infer recurrence from a finite
descriptor count and does not claim that unweighted terminal exit flux pays
an omitted entrance recharge.  Its final composition paragraph correctly
requires either a complete common-potential tiling or the separately proved
charged-seam condition.

## 1. Exact marked identity and positive moments

At a reachable marked state \(x\ge t\), a labelled reaction \(y\to u\) has
actual marked endpoint \((x-y+u,u)\).  Hence

\[
 F(x-y+u,u)-F(x,t)=\log{(x)_t\over(x)_y}.             \tag{1.1}
\]

Writing \(\lambda_y=K_y(x)_y\), \(\Lambda=\sum_y\lambda_y\), and
\(p_y=\lambda_y/\Lambda\) gives the exact one-jump expectation

\[
 D(x,t)=\log p_t-\sum_y p_y\log p_y-
          \log K_t+\sum_y p_y\log K_y
        \le \log p_t+C_K.                              \tag{1.2}
\]

This averages every physical label.  Parallel labels with one source have
the same factorial quotient and are aggregated only through \(K_y\).

For a positive sourcewise increment put
\(R=(x)_t/(x)_y\ge1\).  Since
\(p_y\le (K_y/K_t)R^{-1}\),

\[
 p_y(\log R)^q\le C R^{-1}(\log R)^q\le C_q.          \tag{1.3}
\]

The source set is finite, proving every stated fixed positive one-jump
moment.  Applying the same estimate at the possible second marked state
proves the episode moment bound without an independence assumption.

## 2. Literal top-S probability and the corrected edge

The proof uses the global top **stochastic** tier \(E\), not the possibly
disabled global top D-tier.  On a fixed tier/cap chart, after source-ratio
subselection, all enabled sources in \(E\) have mutually comparable falling
factorials, while every enabled source outside \(E\) is asymptotically
smaller.  Finiteness of the source set and positivity of the fixed \(K_y\)'s
therefore give

\[
                         \liminf_n p_y(x_n)>0
                         \qquad(y\in E).               \tag{2.1}
\]

Let \(r\) be the D-level occupied by \(E\).  The corrected cut supplies one
linkage with

\[
 \varnothing\ne U_L(r)\subsetneq L,
 \qquad U_L(r)\subseteq E.                              \tag{2.2}
\]

The first edge \(e:y\to z\) of a directed path leaving \(U_L(r)\) has
\(y\in E\) and target \(z\) strictly below D-level \(r\).  Consequently its
literal all-clock probability obeys

\[
 a_e(x_n)={\kappa_e\over K_y}p_y(x_n)\ge a_*>0.        \tag{2.3}
\]

This is why a vanishing designated-edge probability cannot obstruct this
theorem: such an edge would not be sourced in the fixed chart's top S-tier.
No reaction orientation is enumerated; strong connectivity and the proper
cut alone supply the edge.

## 3. Depth-two Bellman calculation

The episode takes one ordinary all-clock jump from an arbitrary actual mark
\(t\).  It continues for one final ordinary jump only if the literal label
\(e:y\to z\) fires and no named structural exit has occurred.  Thus, on a
nonexit sequence with \(x'=x-y+z\), first-step conditioning is exactly

\[
                  J(x,t)=D(x,t)+a_e(x)D(x',z).         \tag{3.1}
\]

The first term includes every competitor and every linkage; no path from
the current target to \(y\) is needed.  A competitor is the terminal jump
of the current episode and is not counted again by the next rule.

Bounded displacement preserves strict D-comparisons.  On the nonexit branch
the cap, enabled-source, active-set, and tier data are unchanged, so a
comparison source \(q\in E\) remains enabled.  Since \(z\) is strictly below
the D-level of \(q\),

\[
 p_z(x'_n)\le{\lambda_z(x'_n)\over\lambda_q(x'_n)}
                   \longrightarrow0.                  \tag{3.2}
\]

For large \(n\), the bracket
\(\log p_z(x'_n)+C_K\) is negative.  Combining (1.2), (2.3), and (3.2), the
inequality direction in the target is therefore correct:

\[
 J_n\le C_K+a_*\{\log p_z(x'_n)+C_K\}
                   \longrightarrow-\infty.             \tag{3.3}
\]

If the designated first jump exits the chart, (2.3) instead gives a fixed
positive physical exit probability.  The target gives exit tests first
priority at the first endpoint and explicitly tests and records a named
exit caused by the final second jump as well.

The finite statewise menu is literal: exit-causing labels receive priority;
otherwise the rule of least exact expected reward is selected, with fixed
tie-breaking.  Any failure of uniform exit probability and uniform negative
margin would yield an escaping subsequence with fixed mark, edge, cap phase,
and limiting source ratios, contradicting (2.3) or (3.3).  This is a proof
of uniformity, not an asymptotic rule guessed at run time.

## 4. Physical endpoints, duration, and properness

Every episode contains one or two genuine jumps.  At each stage its current
mark is enabled, its falling factorial is a positive integer, and its
linkage has a positive outgoing labelled rate.  The total hazard is thus at
least one fixed positive minimum rate.  Episode holding times are dominated
by a sum of two fixed exponential laws and have every stated fixed moment.

The last included reaction supplies the actual population endpoint and
actual target mark.  Endpoint displacement is bounded by two binary jumps,
and the positive potential increment is uniformly integrable by Section 1.
The function

\[
                 W(x,t)=1+\sum_i\log((x_i-t_i)!)       \tag{4.1}
\]

is nonnegative and proper because the mark ranges over a finite binary set.
Sequential coercivity gives embedded reward at most \(-2\) outside a finite
chart subset.  The uniform duration bound then permits one fixed \(\eta>0\)
with

\[
             \mathbb E[\Delta W+\eta\tau]\le-1,       \tag{4.2}
\]

unless the selected rule records the positive-probability structural exit.
There is no zero-time classifier handoff.

## 5. Exact composition boundary

The theorem is a local common-\(W\) drift-or-exit contract for descriptors
which pass the corrected cut.  It composes without a comparison toll when
the adjacent common-\(W\) episodes tile the complete relevant trace: the
same state function is evaluated at every actual endpoint.

If a chart exit is followed by an omitted reentry phase, zero normalized
*unweighted* exit flux does not control the value of \(W\) at rare incoming
starts.  The target now says this explicitly and pins the charged-seam
theorem at exact SHA-256

```text
899aa11e15d3e23f629bf06cdfac3a05a47915f5a90378bb8d91982ae0ed6211
```

Such a use must verify that theorem's weighted seam condition separately.
Accordingly, this strict pass does not certify a full two-linkage
composition that merely invokes a ``usual terminal chart argument.''  It
certifies the exact analytic component which that composition may use.

Descriptors failing the corrected cut, including the residual homogeneous
and anisotropic 336 family, remain outside this target and require their
separate classwise theorems.

## 6. Render verdict

The exact theorem and this audit were independently converted to MathJax
HTML and compiled with Pandoc and Tectonic.  Their PDFs were rendered to
page images and inspected.  There is no TeX error, missing glyph, clipped
display, overlap, or unreadable code block.

**FINAL VERDICT: STRICT PASS at the exact target SHA-256 below.**

```text
b9054d036609713a42728ea2a30db074aa09a4f48d505240dd92588c7721e1f5
```
