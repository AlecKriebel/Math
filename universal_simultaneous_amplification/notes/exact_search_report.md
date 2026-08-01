# Exact-search report: a universal strong-selection dB obstruction

Timestamp: 2026-08-01 (America/Los_Angeles)

This note uses only the update rules in the problem statement.  No literature
or external graph catalogue was consulted.

## Main finding

The dB rule alone rules out an all-fitness simultaneous amplifier.  In fact,
the following stronger statement holds.

**Theorem (strong-selection obstruction).**  Let `G` be a finite connected
undirected weighted graph on `n >= 2` vertices, without loops.  If its positive
edge support is not complete, then

```text
lim_{r -> infinity} rho_dB(G,r)
  < lim_{r -> infinity} rho_dB(K_n,r) = (n-1)/n.
```

If its positive edge support is complete, then

```text
rho_dB(G,r) = (n-1)/n - a_G/r + O(r^-2),
```

where, writing `d_i = sum_{j != i} w_ij`,

```text
T_G = sum_{i<j} (d_i+d_j)/w_ij
    = sum_i d_i sum_{j != i} 1/w_ij,

a_G = (T_G - n(n-1))/(n^2(n-2))                 (n >= 3).
```

Moreover,

```text
a_G >= (n-1)/n,
```

with equality exactly when all off-diagonal weights are equal.  Consequently,
every weighted graph other than the uniform complete graph has strictly lower
dB fixation probability than `K_n` for all sufficiently large finite `r`.
The uniform complete graph ties the baseline for every `r`.  Thus no finite
connected undirected weighted graph, and hence no fitness-independent family,
can be a strict dB amplifier for every `r>1`; simultaneous Bd/dB amplification
for every `r>1` is impossible.

The `n=2` case has only one edge up to a scale factor, hence is exactly `K_2`.

## Proof for noncomplete support

Let

```text
s_i = #{j : w_ij > 0}
```

be the degree of vertex `i` in the positive edge support.  Start dB updating
from the singleton mutant `{i}`.  At `r=infinity`, after suppressing self
transitions, there are only two kinds of first state change:

1. vertex `i` dies, at rate `1/n`, and the mutant becomes extinct;
2. one of the `s_i` neighbors of `i` dies, each at rate `1/n`, and the mutant
   at `i` certainly supplies the replacement, creating an adjacent mutant
   pair.

Deaths of nonneighbors leave the state unchanged.  Therefore the probability
of reaching an adjacent pair before extinction tends to

```text
s_i/(s_i+1).
```

Once an adjacent mutant pair exists, every mutant in the connected mutant
cluster has a mutant neighbor.  At `r=infinity` a mutant can therefore never
be replaced by a resident.  A boundary resident becomes mutant when it dies.
Connectedness of the support implies that a proper mutant cluster has a
nonempty boundary, so the cluster grows monotonically to fixation almost
surely.  Equivalently, for finite `r`, the probability of any loss before a
fixed monotone sequence of at most `n-2` gains tends to zero.  Hence

```text
lim_{r -> infinity} rho_dB(G,r)
  = (1/n) sum_i s_i/(s_i+1).
```

Since `s_i <= n-1` and `x/(x+1)` is increasing,

```text
(1/n) sum_i s_i/(s_i+1) <= (n-1)/n.
```

More explicitly, the limiting deficit is

```text
(n-1)/n - lim_{r -> infinity} rho_dB(G,r)
  = sum_i (n-1-s_i)/(n^2(s_i+1)).
```

Equality is possible only if every `s_i=n-1`, i.e. only for complete positive
support.  Any missing edge makes the inequality strict.  The fixation
probability is a rational function of `r` on `(0,infinity)`, so strict
separation of the limits gives strict suppression for all sufficiently large
finite `r`.

## First-order proof for complete support

Assume now `w_ij>0` for every `i != j`, let `epsilon=1/r`, and write `e_S` for
the extinction probability from mutant set `S`.

For `|S| >= 2`, every mutant has another mutant neighbor.  At `epsilon=0`,
singletons move to extinction or to a pair, while every state of size at least
two only gains mutants and eventually reaches fixation.  Thus the limiting
transient matrix still has spectral radius below one, so the extinction
probabilities are analytic in `epsilon` near zero.  Their order-zero terms
vanish for every `|S|>=2`.  In the order-one equations, a loss from a state of
size at least three lands in another state whose order-zero extinction
probability is zero, so there is no forcing; backward induction from the full
state shows that the order-one terms vanish too.  In particular,

```text
e_S = O(epsilon^2)  for |S| >= 3.
```

For the doubleton `{i,j}`, set

```text
e_{ij} = epsilon b_ij + O(epsilon^2).
```

The total leading gain probability is `(n-2)/n`.  If mutant `i` dies, it is
lost with probability

```text
(1/n) (d_i-w_ij)/(r w_ij+d_i-w_ij)
  = (epsilon/n)(d_i-w_ij)/w_ij + O(epsilon^2),
```

and analogously for `j`.  Since singleton extinction has leading value `1/n`,
the state-change equation gives

```text
b_ij = (d_i+d_j-2w_ij)/(n(n-2)w_ij).             (1)
```

For a singleton `{i}`, write

```text
e_i = 1/n + epsilon A_i + O(epsilon^2)
```

and define

```text
C_i = sum_{j != i} (d_j-w_ij)/w_ij.
```

When resident `j` dies, the transition `{i} -> {i,j}` has probability

```text
p_ij = (1/n) r w_ij/(r w_ij+d_j-w_ij)
     = (1/n)(1-epsilon(d_j-w_ij)/w_ij)+O(epsilon^2).
```

The mutant itself dies with probability exactly `1/n`.  Removing self
transitions, the extinction equation is

```text
(1/n + sum_j p_ij)e_i = 1/n + sum_j p_ij e_{ij}.
```

Comparison of the coefficients of `epsilon` yields

```text
A_i = C_i/n^2 + (1/n) sum_{j != i} b_ij.          (2)
```

Now let

```text
Delta = T_G - n(n-1).
```

Directly from the definitions and (1),

```text
sum_i C_i = Delta,
sum_i sum_{j != i} b_ij = 2 Delta/(n(n-2)).
```

Averaging (2) over the uniformly chosen initial vertex gives

```text
(1/n) sum_i A_i = Delta/(n^2(n-2)) = a_G,
```

which is the claimed expansion.

Finally, Cauchy--Schwarz at each vertex gives

```text
d_i sum_{j != i} 1/w_ij
 = (sum_j w_ij)(sum_j 1/w_ij)
 >= (n-1)^2.
```

Summing in `i` proves

```text
T_G >= n(n-1)^2
```

and therefore

```text
a_G >= [n(n-1)^2-n(n-1)]/[n^2(n-2)] = (n-1)/n.
```

The Cauchy defect also has the termwise nonnegative certificate

```text
T_G-n(n-1)^2
 = sum_i sum_{j<k; j,k != i}
     (w_ij-w_ik)^2/(w_ij w_ik),

a_G-(n-1)/n
 = 1/[n^2(n-2)] sum_i sum_{j<k; j,k != i}
     (w_ij-w_ik)^2/(w_ij w_ik).
```

Equality in every vertexwise Cauchy inequality says that all edges incident
to each vertex have one common weight.  Because an edge `ij` is incident to
both endpoints and `n>=3`, these common weights agree globally.  Thus equality
holds exactly for the uniform complete graph.

For an independently derived complete-graph check, the dB count-chain has

```text
u_k = (n-k)/n * rk/(rk+n-k-1),
d_k = k/n * (n-k)/(r(k-1)+n-k),

rho_dB(K_n,r)
 = 1 / (1 + sum_{j=1}^{n-1} product_{k=1}^j d_k/u_k).
```

Its first two strong-selection terms are

```text
rho_dB(K_n,r) = (n-1)/n - (n-1)/(nr) + O(r^-2),
```

in agreement with the equality case above.

## Exact state-space solver design

The independent verifier can use the following representation.

* Index every transient mutant set by an integer bit mask from `1` through
  `2^n-2`.
* Store all edge weights in `QQ` (or an algebraic number field) and `r` as an
  indeterminate.
* For each state, compute only single-vertex flips directly from the defining
  update rule.  For dB, if resident `v` dies, put

  ```text
  M_v(S) = sum_{u in S} w_uv,
  R_v(S) = sum_{u notin S, u != v} w_uv,
  p(S,S+v) = (1/n) r M_v/(r M_v+R_v).
  ```

  If mutant `v` dies, use

  ```text
  p(S,S-v) = (1/n) R_v/(r M_v+R_v),
  ```

  where now `M_v` excludes the dying vertex automatically because `w_vv=0`.
  The analogous Bd probabilities are obtained by summing
  `fitness(u) w_uv/(total fitness * d_u)` over reproducing vertices of the
  opposite type.
* Avoid constructing self-transition expressions.  Build the state-change
  Laplacian `A` with

  ```text
  A_SS = sum_{T != S} p(S,T),
  A_ST = -p(S,T)  (T transient),
  b_S  = p(S,V),
  ```

  and solve `A x=b` by exact fraction-free elimination.
* Average `x_{singleton i}` over all vertices.  Check every raw transition for
  nonnegativity and check that adding the inferred self probability makes each
  row sum exactly one.
* Validation identities are: neutral uniform-singleton average `1/n`; the Bd
  complete-graph formula `(1-r^-1)/(1-r^-n)`; and the dB count-chain formula
  displayed above.

For symbolic comparisons, cancel the rational function before extracting its
numerator and denominator.  Denominator positivity follows either termwise
from the original transient-chain system for `r>0` or by an exact real-root
certificate.  Full-interval polynomial signs can then be certified using a
Sturm chain after shifting `r=1+x`.  The present impossibility theorem needs
only the explicit strong-selection coefficient and the vertexwise Cauchy
certificate.

## Two-class lumped chain used during discovery

For completeness, consider classes `A,B` of sizes `p,q`; give each `A-A` edge
weight `alpha`, each `B-B` edge weight `beta`, and each cross edge weight
`gamma`.  The automorphism group `S_p x S_q` acts transitively on states with
the same mutant counts `(i,j)`.  Since every formula below depends only on
`(i,j)`, the orbit partition is strongly lumpable.

Put

```text
D_A = alpha(p-1)+gamma q,
D_B = beta(q-1)+gamma p,
F   = r(i+j)+p+q-i-j.
```

The Bd flip probabilities are

```text
P(i,j -> i+1,j) = r(p-i)/F [i alpha/D_A + j gamma/D_B],
P(i,j -> i-1,j) = i/F [(p-i)alpha/D_A + (q-j)gamma/D_B],
P(i,j -> i,j+1) = r(q-j)/F [j beta/D_B + i gamma/D_A],
P(i,j -> i,j-1) = j/F [(q-j)beta/D_B + (p-i)gamma/D_A].
```

For dB, for example,

```text
P(i,j -> i+1,j)
 = (p-i)/(p+q)
   * r(i alpha+j gamma)
     / [r(i alpha+j gamma)+(p-i-1)alpha+(q-j)gamma],

P(i,j -> i-1,j)
 = i/(p+q)
   * [(p-i)alpha+(q-j)gamma]
     / [r((i-1)alpha+j gamma)+(p-i)alpha+(q-j)gamma],
```

with the two `B` formulas obtained by interchanging
`(p,i,alpha,A)` and `(q,j,beta,B)`.

An exact rational sweep set `gamma=1`, took

```text
alpha,beta in {1/16,1/8,1/4,1/2,1,2,4,8,16},
```

and checked representative class sizes through total size seven at the exact
rational fitness values

```text
1001/1000, 101/100, 11/10, 3/2, 2, 3, 10, 100.
```

No sampled parameter pair beat the matching complete graph under both rules
at every checked value.  An exhaustive check of the 38 connected labeled
unweighted support graphs on four vertices likewise found none at a smaller
exact rational fitness grid.  A separate exact-rational sample of 500
four-vertex weighted support graphs found no graph improving both rules at
`r=1001/1000`.  These searches were diagnostic only, not used as proof.

## Independent algebra checks

The full symbolic bit-mask solver was run on two nonuniform complete-support
examples.  Exact rational-function limits agreed with the coefficient above:

* on three vertices with edge weights `(w_12,w_13,w_23)=(2,3,5)`, both the
  symbolic chain and the formula give `a_G=22/27` (baseline `2/3`);
* on four vertices with edge weights `(1,2,3,4,5,6)` in lexicographic edge
  order, both give `a_G=343/320` (baseline `3/4`).

The same solver gives strong-selection limits `7/12` for the unit-weight
four-vertex path and `9/16` for the unit-weight four-vertex star, exactly
matching `(1/n) sum_i s_i/(s_i+1)` in both cases (baseline `3/4`).

These checks are independent verification of the expansion, while the proof
itself is the state-equation derivation above.
