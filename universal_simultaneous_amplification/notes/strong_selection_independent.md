# Strong-selection analysis from first principles

**Date:** 2026-08-01 (America/Los_Angeles)

This note derives the `r -> infinity` behavior directly from the two Markov
chains.  No literature search was used.

## Notation

Let `n=|V| >= 2`.  Write

\[
d_i=\sum_j w_{ij},\qquad p_{ij}=\frac{w_{ij}}{d_i},
\qquad N(i)=\{j:w_{ij}>0\},\qquad k_i=|N(i)|.
\]

The support graph, whose edges are the positive-weight edges, is connected.
Put `x=1/r`.  All big-O statements below are for a fixed finite graph as
`x -> 0+`.

## 1. Complete-graph baselines

### 1.1 Birth--death

On the unit-weight complete graph, mutant number `k` is a birth--death chain.
For `1 <= k <= n-1`, the ratio of its downward and upward transition
probabilities is `1/r=x`.  Solving the one-dimensional absorption recurrence
therefore gives

\[
 \rho_{\rm Bd}(K_n,r)=\frac{1-r^{-1}}{1-r^{-n}}
 =\frac{1-x}{1-x^n}.
\]

Thus, for `n>=3`,

\[
 \rho_{\rm Bd}(K_n,r)=1-x+O(x^3),
\]

(indeed the next nonzero term is `x^n`), while for `n=2` it is
`1/(1+x)=1-x+x^2+O(x^3)`.

### 1.2 Death--birth

For death--birth updating on `K_n`, at mutant number `k`, direct calculation
gives

\[
 P_k^+=\frac{n-k}{n}\frac{rk}{rk+n-k-1},
 \qquad
 P_k^-=\frac{k}{n}\frac{n-k}{r(k-1)+n-k}.
\]

Consequently

\[
 \gamma_k:=\frac{P_k^-}{P_k^+}
 =\frac{rk+n-k-1}{r\{r(k-1)+n-k\}}.
\]

If `A_k=r(k-1)+n-k`, then

\[
 \gamma_k=\frac{A_{k+1}}{rA_k},\qquad
 \prod_{k=1}^j\gamma_k
 =\frac{rj+n-j-1}{(n-1)r^j}.
\]

The usual absorption recurrence (obtained by summing successive differences,
not assumed externally) now yields

\[
 \begin{aligned}
 \rho_{\rm dB}(K_n,r)^{-1}
 &=1+\sum_{j=1}^{n-1}\prod_{k=1}^j\gamma_k\\
 &=\frac{n}{n-1}\sum_{m=0}^{n-2}x^m.
 \end{aligned}
\]

Hence the exact baseline is

\[
 \boxed{\displaystyle
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}\frac{1-x}{1-x^{n-1}}.}
\]

For `n>=3`,

\[
 \rho_{\rm dB}(K_n,r)
 =\frac{n-1}{n}-\frac{n-1}{n}x+O(x^2).
\]

For `n=2`, the expression is identically `1/2`.

## 2. Arbitrary graph: birth--death

For a nonempty proper mutant set `S`, discard holding steps and define

\[
 A_S=\sum_{u\in S,v\notin S}p_{uv},\qquad
 B_S=\sum_{u\notin S,v\in S}p_{uv}.
\]

In the embedded jump chain, total upward and downward weights are respectively
`A_S` and `xB_S`.  At `x=0`, every nonempty state can only gain mutants, and
connectedness implies eventual fixation.  Therefore

\[
 \lim_{r\to\infty}\rho_{\rm Bd}(G,r)=1.
\]

For a singleton `{i}`, `A_{\{i\}}=1`; set

\[
 B_i:=B_{\{i\}}=\sum_j p_{ji}.
\]

Extinction from a state with two mutants is `O(x^2)`, because at least two
downward jumps are needed and each downward jump has probability `O(x)`.
The singleton recurrence then gives

\[
 q_i^{\rm Bd}(x):=1-\rho_{\rm Bd}^{\{i\}}(G,1/x)
 =B_i x+O(x^2).
\]

Since

\[
 \frac1n\sum_iB_i
 =\frac1n\sum_j\sum_i p_{ji}=1,
\]

uniform single-mutant initialization gives the graph-independent first-order
formula

\[
 \boxed{\displaystyle
 \rho_{\rm Bd}(G,r)=1-\frac1r+O(r^{-2}).}
\]

For reference, an explicit second-order coefficient is also available when
`n>=3`.  For an edge `ij`, let

\[
 A_{ij}=2-p_{ij}-p_{ji}>0
\]

and

\[
 H_{ij}=\frac{(B_i-p_{ji})B_j+(B_j-p_{ij})B_i}{A_{ij}}.
\]

Two successive downward jumps give

\[
 q_{\{i,j\}}^{\rm Bd}(x)=H_{ij}x^2+O(x^3),
\]

and hence

\[
 q_i^{\rm Bd}(x)
 =B_ix+x^2\left(-B_i^2+\sum_jp_{ij}H_{ij}\right)+O(x^3).
\]

Thus there is no graph-independent sign at this order.  For example, direct
substitution for the unweighted `n`-vertex star gives the average coefficient
`-(n-2)^2/(n-1)`, so that this graph lies above the Bd complete-graph baseline
near strong selection.

## 3. Arbitrary graph: death--birth limit

At `x=0`, consider a singleton mutant at `i`.

* If `i` dies, it has no mutant neighbor and extinction occurs.
* If one of the `k_i` support-neighbors of `i` dies, the mutant wins the
  replacement competition with limiting probability one.  The resulting two
  mutants are adjacent.
* Deaths at all other vertices are holding events.

Once an adjacent mutant pair exists at `x=0`, neither mutant can be replaced
by a resident: each has a positive-weight mutant neighbor, whose fitness
dominates all resident competitors.  The mutant set subsequently gains every
boundary vertex when that vertex dies.  It remains support-connected, and
connectedness of the support graph implies eventual fixation with probability
one.

Conditioning on the first non-holding event from singleton `i` therefore gives

\[
 \lim_{r\to\infty}\rho_{{\rm dB},i}(G,r)=\frac{k_i}{k_i+1}.
\]

Uniform averaging yields the exact strong-selection limit

\[
 \boxed{\displaystyle
 L_{\rm dB}(G):=\lim_{r\to\infty}\rho_{\rm dB}(G,r)
 =\frac1n\sum_i\frac{k_i}{k_i+1}.}
\]

Because `k_i<=n-1`,

\[
 L_{\rm dB}(G)\le \frac{n-1}{n},
\]

with equality if and only if the support graph is complete.  Thus every graph
with incomplete support is strictly below the complete-graph dB baseline for
all sufficiently large finite `r`.

The limiting-chain argument is legitimate despite the singular-looking
`r=infinity` limit: from a singleton, the only limiting states reached before
absorption are support-connected mutant sets.  On this finite set of states,
the limiting transient chain reaches either extinction or fixation almost
surely.  Its fundamental matrix is therefore nonsingular, so the finite-`r`
hitting probabilities converge to those of the limiting chain.

## 4. Full support: exact death--birth coefficient at order `1/r`

Assume now `n>=3` and `w_{ij}>0` for all `i!=j`.  Define the oriented-edge
quantity

\[
 a_{vi}:=\frac{d_v-w_{vi}}{w_{vi}}
\]

and

\[
 T:=\sum_v\sum_{i\ne v}a_{vi}
 =\sum_v\sum_{i\ne v}\frac{d_v-w_{vi}}{w_{vi}}.
\]

Let `q_S(x)` be the extinction probability from mutant set `S`.  It is useful
to discard holding steps.  From singleton `{i}`:

* death of `i` has changing-event weight `1` and leads to extinction;
* when resident `v!=i` dies, its probability of mutant replacement is

\[
 f_{v|i}(x)
 =\frac{w_{vi}}{w_{vi}+x(d_v-w_{vi})}
 =1-a_{vi}x+O(x^2).
\]

Write `C_i=\sum_{v\ne i}a_{vi}`.  The total changing-event weight from the
singleton is therefore

\[
 1+\sum_{v\ne i}f_{v|i}(x)=n-C_ix+O(x^2).
\]

We next need extinction from a pair `{i,j}`.  If mutant `i` dies, the chance
that a resident replaces it is

\[
 g_{i|j}(x)
 =\frac{x(d_i-w_{ij})}{w_{ij}+x(d_i-w_{ij})}
 =a_{ij}x+O(x^2).
\]

The analogous probability for loss of `j` is `a_{ji}x+O(x^2)`.  At `x=0`
there are `n-2` upward changing-event weights, one for each resident vertex.
After one downward event, the remaining singleton has limiting extinction
probability `1/n`.  Extinction from a state with three mutants is `O(x^2)`,
since at least two rare downward events are needed before reaching a singleton.
It follows that

\[
 q_{\{i,j\}}(x)
 =\frac{a_{ij}+a_{ji}}{n(n-2)}x+O(x^2).
\]

The embedded singleton recurrence is

\[
 q_{\{i\}}(x)
 =\frac{1+\sum_{v\ne i}f_{v|i}(x)q_{\{i,v\}}(x)}
 {1+\sum_{v\ne i}f_{v|i}(x)}.
\]

Substitution gives

\[
 q_{\{i\}}(x)
 =\frac1n+x\left[
 \frac{C_i}{n^2}
 +\frac1{n^2(n-2)}\sum_{j\ne i}(a_{ij}+a_{ji})
 \right]+O(x^2).
\]

Averaging over `i`, using `\sum_i C_i=T` and
`\sum_i\sum_{j\ne i}(a_{ij}+a_{ji})=2T`, yields

\[
 \frac1n\sum_i q_{\{i\}}(x)
 =\frac1n+\frac{T}{n^2(n-2)}x+O(x^2).
\]

Therefore

\[
 \boxed{\displaystyle
 \rho_{\rm dB}(G,r)
 =\frac{n-1}{n}
 -\frac{T}{n^2(n-2)}\frac1r
 +O(r^{-2}).}
\]

### Equality case and comparison with `K_n`

For each fixed vertex `v`, Cauchy--Schwarz applied to its `n-1` positive
incident weights gives

\[
 d_v\sum_{i\ne v}\frac1{w_{vi}}\ge (n-1)^2.
\]

Consequently

\[
 \sum_{i\ne v}\frac{d_v-w_{vi}}{w_{vi}}
 =d_v\sum_{i\ne v}\frac1{w_{vi}}-(n-1)
 \ge(n-1)(n-2).
\]

After summing over vertices,

\[
 \boxed{\displaystyle T\ge n(n-1)(n-2).}
\]

Equality at a vertex holds exactly when all its incident edge weights are
equal.  Equality in the summed inequality therefore forces this at every
vertex.  Symmetry of edge weights then forces the common incident value at
adjacent vertices to agree; because the support is complete (indeed,
connectedness would suffice), all edge weights are one common positive
constant.  Conversely, constant weights give equality.

Combining the arbitrary full-support expansion with the baseline expansion,

\[
 \rho_{\rm dB}(G,r)-\rho_{\rm dB}(K_n,r)
 =-\frac{T-n(n-1)(n-2)}{n^2(n-2)}\frac1r+O(r^{-2}).
\]

Thus a nonconstant full-support weighting is strictly below the complete-graph
baseline for all sufficiently large finite `r`.  A constant full-support
weighting is merely a global rescaling of `K_n`, so its transition
probabilities equal those of `K_n` for every `r`.

## 5. Universal obstruction

For every finite connected undirected weighted graph:

1. if its support is incomplete, its dB fixation probability has a strictly
   smaller strong-selection limit than `K_n`;
2. if its support is complete but its weights are not all equal, its limit is
   the same but its `1/r` coefficient is strictly worse;
3. if its support is complete and its weights are all equal, it is exactly
   `K_n` up to irrelevant global scaling and never satisfies a strict
   inequality.

Therefore no finite connected undirected weighted graph is a strict dB
amplifier relative to `K_n` for every `r>1`.  In particular, no
fitness-independent graph, and hence no graph family, can be a strict
simultaneous Bd/dB amplifier for every beneficial fitness value.  The universal
failure endpoint is strong selection.
