# Strong-selection obstruction for death--birth updating

This note proves the obstruction directly from the dB transition rule.  Write

\[
 d_i=\sum_{j\ne i}w_{ij},
 \qquad
 k_i=|\{j:w_{ij}>0\}|.
\]

The number `k_i` is the degree in the unweighted positive-weight support.

## 1. Incomplete support: the limiting term

Start from the singleton mutant `{i}` and let `r` tend to infinity.  A death
at `i` causes extinction.  A death at any one of the `k_i` neighbors of `i`
is followed by mutant reproduction with limiting probability one.  Deaths at
nonneighbors are self-loops.  Therefore the probability of forming an
adjacent mutant pair before extinction is

\[
 \frac{k_i}{k_i+1}.
\]

Once an adjacent pair exists, the mutant set remains connected, cannot lose a
vertex in the infinite-fitness chain, and eventually grows across every edge
of the connected support.  It therefore fixates with probability one.  Thus

\[
 \boxed{
 \lim_{r\to\infty}\rho_{\rm dB}(G,r)
 =\frac1n\sum_{i=1}^n\frac{k_i}{k_i+1}.}
\]

Since `k_i <= n-1`, this is at most `(n-1)/n`, the complete-graph
limit.  Equality holds only when every `k_i=n-1`, that is, only when the
support is complete.  Every graph with a missing edge is consequently below
the complete baseline for all sufficiently large finite `r`.

The exact limiting gap is

\[
 \frac{n-1}{n}-L_{\rm dB}(G)
 =\sum_i\frac{n-1-k_i}{n^2(k_i+1)}.
\]

For a precise perturbation argument, restrict the limiting chain to the
singleton, the two absorbing states, and the support-connected mutant sets
reachable after an adjacent pair forms.  Its transient matrix has spectral
radius below one.  At `epsilon=1/r>0`, one-step leakage from this set is
`O(epsilon)`.  The inverse of the restricted state-change system remains
bounded near zero, so the total probability of leakage before absorption is
`O(epsilon)`.  Whatever happens after leakage changes fixation probability by
at most this amount.  This proves convergence to the limiting formula without
assuming a uniform bound on path length.

## 2. Complete support: the first correction

Assume now that every `w_ij>0`, that `n>=3`, and put
`epsilon=1/r`.  Let `h_S(epsilon)` be fixation probability from mutant set
`S`, and let `e_S=1-h_S`.

At `epsilon=0`, every set with at least two mutants fixates, while

\[
 h_{\{i\}}(0)=\frac{n-1}{n},\qquad e_{\{i\}}(0)=\frac1n.
\]

The limiting transient chain absorbs almost surely, so its transient matrix
`I-Q(0)` is invertible.  Hence all hitting probabilities are analytic in
`epsilon` near zero.  The first-order equations for sets of size at least
three have no forcing: a rare loss still leaves at least two mutants, whose
zeroth-order extinction probability vanishes.  Backward induction from the
full state therefore gives the next assertion.

For `|S|>=3`, a single resident-reproduction event can remove at most one
mutant, leaving at least two.  Expanding the first-step equations backward from
fixation gives

\[
 e_S=O(\epsilon^2)\qquad (|S|\ge3).
\]

For a pair `S={i,j}`, a death at `i` is followed by resident reproduction
with probability

\[
 \epsilon\frac{d_i-w_{ij}}{w_{ij}}+O(\epsilon^2),
\]

and similarly at `j`.  At leading order the pair waits through mutant deaths
and grows when any of the `n-2` residents dies.  Substitution in the exact
first-step equation yields

\[
 e_{\{i,j\}}
 =\epsilon b_{ij}+O(\epsilon^2),
 \qquad
 b_{ij}=\frac{d_i+d_j-2w_{ij}}{n(n-2)w_{ij}}.
\]

For a singleton `{i}`, death of resident `j` creates the pair `{i,j}`
with probability

\[
 t_{ij}
 =\frac1n\frac{w_{ij}}{w_{ij}+\epsilon(d_j-w_{ij})}
 =\frac1n\left(1-\epsilon\frac{d_j-w_{ij}}{w_{ij}}\right)
  +O(\epsilon^2).
\]

The only other non-self transition is extinction, of probability `1/n`.
Conditioning on the first non-self transition gives

\[
 h_{\{i\}}
 =\frac{\sum_{j\ne i}t_{ij}h_{\{i,j\}}}
 {n^{-1}+\sum_{j\ne i}t_{ij}}.
\]

Expanding and averaging over `i` gives

\[
 \boxed{
 \rho_{\rm dB}(G,r)
 =\frac{n-1}{n}-\frac{A(G)}r+O(r^{-2}),}
\]

where

\[
 A(G)=\frac{T(G)}{n^2(n-2)},
 \qquad
 T(G)=\sum_{i<j}\left(\frac{d_i+d_j}{w_{ij}}-2\right).
\]

Equivalently,

\[
 T(G)+n(n-1)
 =\sum_i d_i\sum_{j\ne i}\frac1{w_{ij}}.
\]

For each vertex, Cauchy--Schwarz gives

\[
 d_i\sum_{j\ne i}\frac1{w_{ij}}
 =\left(\sum_{j\ne i}w_{ij}\right)
  \left(\sum_{j\ne i}\frac1{w_{ij}}\right)
 \ge (n-1)^2.
\]

Summing over `i` shows

\[
 T(G)\ge n(n-1)(n-2),
 \qquad
 A(G)\ge\frac{n-1}{n}.
\]

This inequality has the explicit sum-of-squares certificate

\[
 A(G)-\frac{n-1}{n}
 =\frac1{n^2(n-2)}
 \sum_i\sum_{\substack{j<k\\j,k\ne i}}
 \frac{(w_{ij}-w_{ik})^2}{w_{ij}w_{ik}}.
\]

The right-hand side is exactly the complete-graph `1/r` coefficient.
Equality in every vertexwise Cauchy inequality requires all edges incident to
each vertex to have equal weight.  Symmetry and complete support then force
all edge weights globally equal.  Such a graph is merely a common rescaling
of `K_n` and has exactly the baseline fixation probability.

Every nonuniform complete-support graph therefore satisfies

\[
 \rho_{\rm dB}(G,r)<\rho_{\rm dB}(K_n,r)
\]

for all sufficiently large finite `r`.

## 3. Universal conclusion

For `n=2`, a connected loopless graph consists of one positive edge.  After
either vertex dies its unique neighbor must reproduce, so uniformly averaged
dB fixation is exactly `1/2` for every `r`; this equals the `K_2` baseline.
The complete-support coefficient involving `n-2` is used only for `n>=3`.

For every finite connected undirected weighted graph, one of the following
holds:

1. its support is incomplete and its dB strong-selection limit is strictly
   below the complete baseline;
2. its support is complete but its weights are nonuniform and its first
   strong-selection correction is strictly worse than the complete baseline;
3. it is a common rescaling of `K_n` and is exactly neutral relative to the
   baseline for every `r`.

Hence no such graph is a strict dB amplifier for every `r>1`; a fortiori no
fitness-independent graph family can be a strict simultaneous Bd/dB amplifier
for every `r>1`.

All asymptotics here are for one fixed finite graph; the suppressing threshold
may depend on the graph and on its index in a family.  This is sufficient:
fixing any proposed family member and then taking `r` beyond its own threshold
contradicts the required inequality for every `r>1`.  Graph weights that vary
with `r` would reverse the order of quantifiers and are outside the stated
fitness-independent problem.
