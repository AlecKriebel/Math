# Hostile audit of the strong-selection dB obstruction

**Date:** 2026-08-01 (America/Los_Angeles)
**Files audited:** `strong_db_obstruction.md` and
`strong_selection_independent.md`
**Scope:** death--birth updating only.  No literature search was performed.

## Verdict

**The mathematical obstruction is correct.**  I found no wrong asymptotic
coefficient, sign, equality condition, or counterexample.  For every fixed
finite connected undirected weighted graph on `n >= 2` vertices, either its
dB strong-selection limit is strictly below that of `K_n`, its first
`1/r` correction is strictly worse, or it is a global rescaling of `K_n` and
ties the baseline identically.  This is enough to rule out the proposed
fitness-independent all-`r` family.

The notes are not quite referee-proof as written.  They should add an explicit
`n=2` paragraph, make the perturbation/analyticity argument precise, and state
the family quantifiers and the order of limits explicitly.  These are proof
presentation gaps, not defects in the theorem or its formulas.

## 1. Complete-graph baseline

Put `x=1/r`.  On `K_n`, if there are `k` mutants, the two changing
probabilities are

\[
 P_k^+=\frac{n-k}{n}\frac{rk}{rk+n-k-1},\qquad
 P_k^-=\frac{k}{n}\frac{n-k}{r(k-1)+n-k}.
\]

Thus

\[
 \gamma_k:=\frac{P_k^-}{P_k^+}
 =\frac{rk+n-k-1}{r\{r(k-1)+n-k\}}.
\]

Writing `A_k=r(k-1)+n-k` gives

\[
 \gamma_k=\frac{A_{k+1}}{rA_k},\qquad
 \prod_{k=1}^j\gamma_k
 =\frac{rj+n-j-1}{(n-1)r^j}.
\]

Summing the usual one-dimensional absorption differences therefore gives

\[
 \rho_{\rm dB}(K_n,r)^{-1}
 =\frac{n}{n-1}\sum_{m=0}^{n-2}x^m
\]

and hence

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}\frac{1-x}{1-x^{n-1}}.
\]

Consequently, for `n >= 3`,

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}-\frac{n-1}{n}x+O(x^2).
\]

For `n=2` the formula has a removable cancellation and is exactly `1/2`.
The baseline formula and both stated asymptotics in
`strong_selection_independent.md` are correct.

## 2. Incomplete positive support

Let

\[
 k_i=|\{j:w_{ij}>0\}|.
\]

From singleton `{i}`, the limiting changing events have the following rates
before the common factor `1/n`:

* death of `i`, with rate `1`, gives extinction;
* death of any one of its `k_i` support-neighbors, each with rate `1`, creates
  an adjacent pair;
* death of a nonneighbor is a holding event.

The probability of reaching an adjacent pair before extinction is therefore
exactly `k_i/(k_i+1)` in the limiting chain.

Once a support-connected set with at least two mutants has formed, every
mutant has a mutant support-neighbor: this is immediate because the induced
support subgraph on the mutant set is connected and has at least two
vertices.  Mutant losses are therefore impossible at `x=0`, while adding a
boundary resident preserves support-connectedness and size at least two.
Each proper cluster has a nonempty boundary, and a boundary death occurs with
positive probability, so fixation occurs almost surely.  The connected-set
argument in the notes is correct.

It follows that

\[
 L_{\rm dB}(G)
 =\lim_{r\to\infty}\rho_{\rm dB}(G,r)
 =\frac1n\sum_i\frac{k_i}{k_i+1}.
\]

The deficit from the complete-support limit can be written termwise as

\[
 \frac{n-1}{n}-L_{\rm dB}(G)
 =\sum_i\frac{n-1-k_i}{n^2(k_i+1)}.
\]

It is nonnegative and vanishes exactly when every `k_i=n-1`.  Hence every
missing support edge gives a strict limiting deficit.  The limit formula,
strictness statement, and equality condition in both audited notes are
correct.

### Limiting-chain rigor

The conclusion is valid, but the brief fundamental-matrix sentence should be
expanded.  At `x=0`, restrict to the states reachable from a singleton: the
singleton, extinction, and support-connected sets containing an adjacent
pair.  The limiting transient chain on this finite set absorbs almost surely.
Indeed, the singleton has changing-event probability `(k_i+1)/n>0`, and from
any proper cluster a boundary death has probability at least `1/n`; at most
`n-2` boundary additions are needed after the first pair.  Its transient
matrix consequently has spectral radius below one.

For small positive `x`, transitions on this reachable set converge to the
limiting transitions.  Leakage caused by a resident replacing a mutant is
`O(x)` in every fixed state, and all hitting probabilities are bounded by
one.  Equivalently, the inverse of the limiting state-change system persists
under a small perturbation.  This supplies the missing step that rules out an
accumulation of rare losses over a diverging waiting time.  Merely mentioning
a fundamental matrix for the limiting reachable set, without accounting for
finite-`x` leakage out of that set, is too compressed for a final proof.

## 3. Full support: analyticity at `x=0`

Assume `n >= 3` and every off-diagonal weight is positive.  Let `q_S(x)` be
extinction probability.  The transition probabilities, after cancelling
removable factors in the singleton-death cases, are analytic in `x` near
zero.  The entire limiting transient chain absorbs:

* a singleton goes either to extinction or to a pair;
* a set of at least two mutants only gains mutants and reaches fixation.

Therefore its transient matrix `Q(0)` has spectral radius below one and

\[
 q(x)=(I-Q(x))^{-1}b(x)
\]

is analytic near `x=0`.  This is the clean justification for all of the
displayed `O(x^2)` remainders.  It also makes the rare-event argument rigorous:
from a state with at least three mutants, at least two downward changes are
needed before the process can reach a singleton, while the probability of a
downward change before the next gain is `O(x)`.  Hence

\[
 q_S(x)=O(x^2)\qquad (|S|\ge 3).
\]

The assertion is correct, but `strong_db_obstruction.md` currently states it
without first establishing analyticity or a uniform-in-state rare-event
bound.  The finite-state argument above should be inserted.

## 4. Audit of the doubleton coefficient

Define the oriented quantity

\[
 a_{vi}=\frac{d_v-w_{vi}}{w_{vi}}.
\]

For the doubleton `{i,j}`, loss of mutant `i` has one-step probability

\[
 \frac1n\frac{x(d_i-w_{ij})}{w_{ij}+x(d_i-w_{ij})}
 =\frac{x}{n}a_{ij}+O(x^2),
\]

and loss of `j` analogously has leading probability `(x/n)a_{ji}`.  The
leading total probability of a gain is `(n-2)/n`, and the extinction
probability of the singleton left after a loss is `1/n` at order zero.
Consequently

\[
 q_{\{i,j\}}(x)=xb_{ij}+O(x^2),\qquad
 b_{ij}=\frac{a_{ij}+a_{ji}}{n(n-2)}
 =\frac{d_i+d_j-2w_{ij}}{n(n-2)w_{ij}}.
\]

All factors of `n`, the orientation of `a`, and the denominator `n-2` are
correct.  In particular, the common factor `1/n` from choosing the dead
vertex cancels once against the leading pair-to-larger-set rate but not
against the singleton extinction value `1/n`; this is the most likely place
for an erroneous missing factor, and the notes have it right.

## 5. Audit of the singleton and averaged coefficients

For singleton `{i}`, when resident `v` dies, the probability that `i`
replaces it is

\[
 f_{v|i}(x)=\frac{w_{vi}}{w_{vi}+x(d_v-w_{vi})}
 =1-a_{vi}x+O(x^2).
\]

Put

\[
 C_i=\sum_{v\ne i}a_{vi}.
\]

After suppressing holdings and scaling all changing probabilities by `n`,
the exact extinction equation is

\[
 q_{\{i\}}(x)
 =\frac{1+\sum_{v\ne i}f_{v|i}(x)q_{\{i,v\}}(x)}
 {1+\sum_{v\ne i}f_{v|i}(x)}.
\]

Substitution of the doubleton coefficient gives

\[
 q_{\{i\}}(x)
 =\frac1n+x\left[
 \frac{C_i}{n^2}
 +\frac1{n^2(n-2)}\sum_{j\ne i}(a_{ij}+a_{ji})
 \right]+O(x^2).
\]

Now define

\[
 T=\sum_v\sum_{i\ne v}a_{vi}.
\]

Then `sum_i C_i=T`, while

\[
 \sum_i\sum_{j\ne i}(a_{ij}+a_{ji})=2T.
\]

Averaging the last singleton display over the `n` possible initial vertices
therefore gives

\[
 \frac1n\sum_iq_{\{i\}}(x)
 =\frac1n+\frac{T}{n^2(n-2)}x+O(x^2),
\]

so

\[
 \rho_{\rm dB}(G,r)
 =\frac{n-1}{n}-\frac{T}{n^2(n-2)}\frac1r+O(r^{-2}).
\]

This verifies the full coefficient, including the averaging factor.

The two audited notes use superficially different definitions of `T`, but
they agree:

\[
 \begin{aligned}
 T
 &=\sum_v\sum_{i\ne v}\frac{d_v-w_{vi}}{w_{vi}}\\
 &=\sum_{i<j}\left(\frac{d_i+d_j}{w_{ij}}-2\right),\\
 T+n(n-1)
 &=\sum_i d_i\sum_{j\ne i}\frac1{w_{ij}}.
 \end{aligned}
\]

Any merged manuscript should display these identities immediately and should
not reuse `T` for the last, unshifted sum; confusing the shifted and unshifted
versions would change the coefficient by `n(n-1)`.

### Exact spot check

For the weighted triangle

\[
 (w_{12},w_{13},w_{23})=(1,2,3),\qquad (d_1,d_2,d_3)=(3,4,5),
\]

the three doubleton coefficients are

\[
 b_{12}=\frac53,\qquad b_{13}=\frac23,\qquad b_{23}=\frac13.
\]

The predicted singleton-extinction `x` coefficients are

\[
 \frac{23}{18},\qquad \frac{26}{27},\qquad \frac{23}{54},
\]

whose average is `8/9`.  Direct exact solution of all six transient subset
equations gives the same three singleton coefficients and

\[
 \lim_{r\to\infty}r\left(\frac23-\rho_{\rm dB}(G,r)\right)=\frac89.
\]

This independently stress-tests both the orientation conventions and the
averaging.

## 6. Cauchy bound and equality case

At each vertex `v`, Cauchy--Schwarz gives

\[
 d_v\sum_{i\ne v}\frac1{w_{vi}}\ge(n-1)^2.
\]

Hence

\[
 T\ge n\bigl((n-1)^2-(n-1)\bigr)
 =n(n-1)(n-2),
\]

and therefore

\[
 \frac{T}{n^2(n-2)}\ge\frac{n-1}{n}.
\]

The right side is exactly the complete-graph coefficient.  The nonnegative
defect has the stronger termwise certificate

\[
 T-n(n-1)(n-2)
 =\sum_v\sum_{\substack{i<j\\i,j\ne v}}
 \frac{(w_{vi}-w_{vj})^2}{w_{vi}w_{vj}}.
\]

Equality forces all weights incident to each vertex `v` to be equal.  If that
common incident value is `c_v`, symmetry of an edge `uv` gives
`c_u=w_{uv}=c_v`.  Connectedness then forces one global value.  Conversely,
global constant weights give equality and cancel from every transition
probability.  The equality characterization in both notes is exact; complete
support is more than enough for the final propagation of the `c_v` values.

For nonconstant full support, write

\[
 \delta_G=\frac{T-n(n-1)(n-2)}{n^2(n-2)}>0.
\]

Then

\[
 \rho_{\rm dB}(G,r)-\rho_{\rm dB}(K_n,r)
 =-\frac{\delta_G}{r}+O(r^{-2}),
\]

which is strictly negative for every sufficiently large finite `r`.  The sign
in both notes is correct.

## 7. The `n=2` case

The coefficient calculation must not be applied when `n=2`, because of the
factor `n-2`.  A connected loopless undirected weighted graph on two vertices
has weight matrix

\[
 \begin{pmatrix}0&w\\w&0\end{pmatrix},\qquad w>0.
\]

From either singleton, death of the mutant causes extinction and death of the
resident causes fixation, each with probability `1/2`; there is only one
possible parent after a death.  Thus

\[
 \rho_{\rm dB}(G,r)=\frac12=\rho_{\rm dB}(K_2,r)
 \qquad\text{for every }r>0.
\]

This case is logically covered by the phrase "a rescaling of `K_n`", and
`strong_selection_independent.md` records the baseline value, but
`strong_db_obstruction.md` should include this separate paragraph before its
universal conclusion.  The theorem assumes no `n=1` case because the positive
weighted-degree hypothesis rules it out.

## 8. Logical quantifiers

What the argument proves is the following pointwise-in-graph statement:

\[
 \forall G\;\begin{cases}
   \exists R_G<\infty\;\forall r>R_G:\
   \rho_{\rm dB}(G,r)<\rho_{\rm dB}(K_n,r),
   &\text{if (G) is not a uniform complete graph},\\
   \forall r>0:\
   \rho_{\rm dB}(G,r)=\rho_{\rm dB}(K_n,r),
   &\text{if (G) is a uniform complete graph up to scale}.
 \end{cases}
\]

In the first line, "not uniform complete" includes both incomplete support
and nonuniform full support.  The threshold `R_G` may depend arbitrarily on
the graph and therefore on `N`; no uniform strong-selection expansion over a
family is claimed or needed.

Indeed, suppose a family satisfied

\[
 \exists N_0\ \forall N\ge N_0\ \forall r>1:\quad
 \rho_{\rm dB}(G_N,r)>\rho_{\rm dB}(K_{|V(G_N)|},r).
\]

Fix any one `N >= N_0`.  If `G_N` is uniform complete it ties, and otherwise
choosing `r>\max\{1,R_{G_N}\}` makes it strictly worse.  Either case is a
contradiction.  Thus graph-dependent thresholds cause no quantifier gap.

The proof does **not** by itself address a graph whose weights are allowed to
change with `r` while `r -> infinity`; that is a different order of limits.
The mission expressly requires the graph to be independent of `r`, so this is
not a limitation of the claimed obstruction.  Both notes should state this
order-of-limits point to prevent an accidental stronger claim.

## Required corrections before final use

1. **Handle `n=2` explicitly.**  Add the one-edge calculation above and state
   that the `1/(n-2)` expansion is only for `n >= 3`.
2. **Insert a finite-state perturbation lemma.**  For incomplete support,
   identify the limiting reachable set and control `O(x)` leakage.  For full
   support, state that `Q(0)` is transient, so `(I-Q(x))^{-1}` is analytic.
   This rigorously licenses the limit and every `O(x^2)` assertion.
3. **State fixed-graph asymptotics and the family quantifiers.**  The big-O
   constants and the suppression threshold depend on `G` (and may depend on
   `N`).  Explain why a graph-dependent threshold still contradicts
   `forall r>1` for each fixed `N`.
4. **Keep the `T` convention explicit when merging notes.**  Retain either
   the shifted oriented sum used here or the unshifted reciprocal-weight sum,
   but display the shift `n(n-1)` wherever the notation is introduced.  The
   present two definitions are already algebraically consistent; this is an
   editorial safeguard against a later coefficient error.

With these corrections, the strong-selection dB obstruction meets the stated
universal negative-result standard.
