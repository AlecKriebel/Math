# Sharp rank-weighted posterior reflection at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note proves a **sharp arithmetic--harmonic reduction** of the open
finite-baseline posterior collision inequality.  It replaces the raw
collision excess by a rank-weighted conditional-variance gain with an exact
best coefficient at every rank.

The remaining stationary inequality is

\[
 \boxed{
 E_\Pi\{c_{n,|B|}G(B)\}\le m_K-E_\Pi|B|,}             \tag{1}
\]

where, for `k=|B|`, `h=n-k`,

\[
 \begin{split}
 G(B)&=\sum_{v\notin B}{1\over1+e_v(B)}-{h^2\over n}, \tag{2}\\
 c_{n,k}&=
 \begin{cases}
 0,&h=1,\\[1mm]
 (k+1)/h,&h\ge2\text{ and }k\le h-2,\\[1mm]
 n^2/\{4h(h-1)\},&h\ge2\text{ and }k\ge h-2.
 \end{cases}                                          \tag{3}
 \end{split}
\]

Inequality (1) is **OPEN**.  It is stronger than the collision-reflection
target, but it retains the exact finite complete-graph baseline and has
survived the full deterministic hostile corpus.  No finite screen is used
as a proof.

The note also derives an exact active-channel Brier-risk decomposition of
(1).  It proves that the obvious centered Cayley contraction and both
separated law-of-total-variance signs are false.  Thus the new reduction is
not another disguised fixed-reference contraction.

## 1. Posterior variables and the Hilbert variational form

Let `Pi` be the stationary law of the fair-geometric union dual.  For a
fixed target `v`, let

\[
 R_v(B)=\Pi(B)1_{\{v\notin B\}},\qquad
 \nu_v(B)=\hbox{effective incoming mass},
\]

and, for a hole `v` of `B`, put

\[
 e_v(B)={\nu_v(B)\over\Pi(B)}.
\]

Stationarity gives the pointwise identity

\[
 \sum_{v\notin B}e_v(B)=k.                            \tag{4}
\]

The collision excess is

\[
 J(B)=\sum_{v\notin B}\left(e_v(B)-{k\over h}\right)^2. \tag{5}
\]

It has the exact variational representation

\[
 \boxed{
 E_\Pi J(B)=
 \sup_{\substack{a_v(B)\in\mathbb R\\
                  \sum_{v\notin B}a_v(B)=0}}
 \left\{
 2\sum_{B,v\notin B}\nu_v(B)a_v(B)
 -\sum_B\Pi(B)\sum_{v\notin B}a_v(B)^2
 \right\}.}                                          \tag{6}
\]

The optimizer is

\[
 a_v(B)=e_v(B)-k/h.                                   \tag{7}
\]

Thus the target-centered projection suggested by the product-chain route
is exact.  Section 5 shows that the one-sample Cayley operator expands,
rather than contracts, this norm on exact graph witnesses.

## 2. A sharp arithmetic--harmonic variance lemma

The following elementary lemma is the main proved result of this branch.

### Lemma 1 (sharp lower-bounded arithmetic--harmonic reflection)

Let `h>=2`, `k>=1`, `n=h+k`, and let

\[
 x_1,\ldots,x_h\ge1,\qquad \sum_i x_i=n.
\]

Then

\[
 \boxed{
 \sum_i x_i^2-{n^2\over h}
 \le n c_{n,k}\left(\sum_i{1\over x_i}-{h^2\over n}\right),} \tag{8}
\]

with `c_(n,k)` given by (3).  The coefficient is best possible.

In the first regime an extremizer is

\[
 (x_1,\ldots,x_h)=(k+1,1,\ldots,1).                  \tag{9}
\]

In the second regime, for `h>2`, an extremizer is

\[
 \left({n\over2},{n\over2(h-1)},\ldots,
                    {n\over2(h-1)}\right).           \tag{10}
\]

For `h=2`, (10) is the diagonal and the best coefficient is approached by
nonconstant vectors tending to the diagonal.

### Proof

Write

\[
 V=\sum_i x_i^2-{n^2\over h},\qquad
 H=\sum_i{1\over x_i}-{h^2\over n}.
\]

Both are nonnegative and vanish together only at the diagonal.  The exact
pair identities are

\[
 hV=\sum_{i<j}(x_i-x_j)^2,
 \qquad
 nH=\sum_{i<j}{(x_i-x_j)^2\over x_ix_j}.              \tag{11}
\]

It remains to maximize `V/(nH)` on the compact simplex, with the value at
the diagonal understood by continuity along rays.

Here is a complete extremal reduction.  At a nonconstant interior maximizer
of the ratio `rho`, the Lagrange equation for

\[
 V-\rho nH
\]

has the form

\[
 2x_i+{\rho n\over x_i^2}=\gamma.                    \tag{12}
\]

The left side decreases and then increases, so there are at most two
positive roots.  Its second derivative in the separable objective is

\[
 2-{2\rho n\over x_i^3}.
\]

It is positive at the larger root.  Hence the larger root can have
multiplicity only one: varying two coordinates at that root in opposite
directions would give a positive second variation at a maximum.

If a boundary coordinate `1` and a smaller interior root `B>1` both
occurred, the one-sided variation which increases the boundary coordinate
and decreases `B` would also increase the objective.  Indeed the derivative
in (12) is strictly decreasing from `1` to the smaller root.  Therefore a
maximizer has, after permutation, the one-outlier form

\[
 (A,B,\ldots,B),\qquad A+(h-1)B=n,quad B\ge1.         \tag{13}
\]

For a two-level vector, (11) gives exactly

\[
 {V\over nH}={AB\over h}.                             \tag{14}
\]

The product

\[
 AB=B\{n-(h-1)B\}
\]

is maximized at `B=n/[2(h-1)]`, unless that point lies below the constraint
`B>=1`.  The constrained maximum is consequently

\[
 {AB\over h}=
 \begin{cases}
 (k+1)/h,&n\le2(h-1),\\[1mm]
 n^2/\{4h(h-1)\},&n\ge2(h-1).
 \end{cases}
\]

Since `n<=2(h-1)` is exactly `k<=h-2`, this is (3).  Equations
(9)--(10) prove sharpness.  This proves the lemma.  \(\square\)

## 3. The weighted harmonic-reflection reduction

For a fixed stationary output `B`, set

\[
 x_v=1+e_v(B)\qquad(v\notin B).
\]

Equation (4) gives

\[
 x_v\ge1,\qquad \sum_{v\notin B}x_v=h+k=n.           \tag{15}
\]

Moreover,

\[
 J(B)=\sum x_v^2-{n^2\over h},\qquad
 G(B)=\sum{1\over x_v}-{h^2\over n}.                 \tag{16}
\]

Lemma 1 therefore proves the pointwise sharp inequality

\[
 \boxed{J(B)\le n c_{n,k}G(B).}                      \tag{17}
\]

Consequently (1) implies

\[
 E_\Pi J(B)\le n\{m_K-E_\Pi|B|\},                   \tag{18}
\]

which is the exact finite-baseline collision reflection.  In particular,
(1) would prove

\[
 E_\Pi|B|\le m_K
 ={(n-1)2^{n-2}\over2^{n-1}-1},                     \tag{19}
\]

and hence the universal dB upper bound at fitness two.

The implication is one-way: (17) is a pointwise envelope, so (1) is a
stronger sufficient statement, not an equivalent reformulation of (18).

## 4. Exact law-of-total-variance and active-channel decomposition

Draw the stationary target experiment

\[
 A\sim\Pi,qquad V\sim\operatorname{Unif}(V),qquad
 B\sim K_V(A),qquad C=1_{\{V\in A\}}.               \tag{20}
\]

Conditionally on `B`,

\[
 \Pr(C=1\mid B)={k\over n},\qquad
 \Pr(C=1\mid B,V=v)={e_v(B)\over1+e_v(B)}.           \tag{21}
\]

Therefore

\[
 \begin{split}
 \operatorname{Var}(C\mid B)&={kh\over n^2},\\
 E\{\operatorname{Var}(C\mid B,V)\mid B\}
 &= {1\over n}\sum_{v\notin B}{e_v(B)\over1+e_v(B)},\\
 \operatorname{Var}(E[C\mid B,V]\mid B)&={G(B)\over n}.
                                                               \tag{22}
 \end{split}
\]

Before the update, observing `V` resolves `C` completely, so the corresponding
input variance gain conditional on `A` is `|A|(n-|A|)/n^2`.  Equality of the
rank laws of `A` and `B` turns (22) into an exact transported
law-of-total-variance identity.  Discarding the residual term is far too
weak; the finite complete correction is contained in that residual.

To retain it, put

\[
 D=A\setminus\{V\},\qquad
 \sigma_v(D)=\Pi(D\cup\{v\}).                        \tag{23}
\]

For nonnegative families `Y_v(B)`, define the weighted harmonic overlap

\[
 \mathcal O_c(R,Y)=
 \sum_{B,v\notin B}c_{n,|B|}
 {R_v(B)Y_v(B)\over R_v(B)+Y_v(B)}.                  \tag{24}
\]

Zero-over-zero terms are omitted.  The two exact Brier risks are

\[
 E\operatorname{Var}(C\mid D,V)={1\over n}\mathcal O_1(R,\sigma),
 \qquad
 E\operatorname{Var}(C\mid B,V)={1\over n}\mathcal O_1(R,\nu). \tag{25}
\]

Using (2), the weighted-reflection slack has the exact decomposition

\[
 \boxed{
 \begin{split}
 m_K-m-E(cG)
 ={}&\underbrace{m_K-m-E\!\left(c{k h\over n}\right)
                 +\mathcal O_c(R,\sigma)}_{\text{static Boolean term}}\\
 &+\underbrace{\mathcal O_c(R,\nu)-
                 \mathcal O_c(R,\sigma)}_{\text{active-channel Brier loss}}.
                                                               \tag{26}
 \end{split}}
\]

The first bracket is negative on every displayed hostile witness.  The
second bracket supplies the missing compensation.  For example,

\[
\begin{array}{c|ccc}
 &\text{static}&\text{active}&\text{total}\\ \hline
P_3&-169/1440&239/1440&7/144\\
K_{2,2}&-1180/3591&172/513&8/1197\\
\text{regular weighted }K_4&-50249/253708&240463/1196052&368/123123.
\end{array}                                             \tag{27}
\]

Thus rank-law stationarity alone cannot prove (1).  A proof must use the
fair-geometric active channel.

There is an exact one-sample form of that remaining compensation.  Put

\[
 \lambda_v={\sigma_v+\nu_v\over2},\qquad
 \nu_v=\lambda_vA_v,                                  \tag{28}
\]

where `A_v` adjoins one `P_v` sample.  The Cayley identity gives

\[
 \sigma_v-\nu_v=(\sigma_v+\nu_v)(I-A_v).              \tag{29}
\]

Define

\[
 q_v(B)=c_{n,|B|}
 {R_v(B)^2\over\{R_v(B)+\nu_v(B)\}
                  \{R_v(B)+\sigma_v(B)\}}.           \tag{30}
\]

Then

\[
 \boxed{
 \mathcal O_c(R,\nu)-\mathcal O_c(R,\sigma)
 =\sum_{v,C}\{\sigma_v(C)+\nu_v(C)\}
       \{A_vq_v(C)-q_v(C)\}.}                        \tag{31}
\]

Equation (31) is the precise active-channel variance term.  Its aggregate
is positive on the exact corpus, but its individual target summands can be
negative.  No sign is claimed universally.

### 4.1 Reversible original-edge pairing is still not termwise

The whole slack in (26), not just its active bracket, has an exact expansion
over original directed edges.  Assign to target `v` the static mass

\[
 s_v={m_K\over n}-\Pr(v\in B)
 +\sum_{B:v\notin B}c_{n,k}
 \left\{{R_v(B)\sigma_v(B)\over R_v(B)+\sigma_v(B)}
              -{k\over n}R_v(B)\right\}.             \tag{31a}
\]

With `q_v` from (30), put

\[
 L_{vi}=s_v+\sum_C\{\sigma_v(C)+\nu_v(C)\}
                 \{q_v(C\cup\{i\})-q_v(C)\}.        \tag{31b}
\]

Then

\[
 \boxed{m_K-m-E(cG)=\sum_{v,i}P_{vi}L_{vi}.}         \tag{31c}
\]

For an undirected weighted graph, detailed balance pairs the two
orientations of `vi` as

\[
 P_{vi}L_{vi}+P_{iv}L_{iv}
 =w_{vi}\left({L_{vi}\over d_v}+{L_{iv}\over d_i}\right). \tag{31d}
\]

The hoped-for edgewise sign is exactly false.  On the weighted triangle
`(1,1,5)`, each light edge contributes

\[
 -{24292724\over11580319359}<0,                       \tag{31e}
\]

while the heavy edge compensates.  On the regular weighted `K_4`, four
edges contribute `-253349/17729712` each.  In the exact deterministic
corpus, 24 of 54 three-vertex graphs and 544 of 624 four-vertex graphs have
at least one negative paired edge.  Thus reversibility is essential only
after a genuinely global aggregation; detailed-balance pairing by itself
does not factor the numerator into nonnegative local terms.

Cycle circulation cannot supply the missing local compensation: already on
the unweighted four-path, the middle edge contributes
`-20641618/374699325`, while the two leaf edges compensate.  Any successful
Laplacian argument must therefore be nonlocal even on a tree.

## 5. Exact failures of tempting strengthenings

### 5.1 Centering does not repair Cayley contraction

For a family of target measures `eta_v`, define its conditional centered
collision

\[
 \mathcal C(\eta)=\sum_B\left\{
 {h\sum_v\eta_v(B)^2\over\sum_v\eta_v(B)}-
 \sum_v\eta_v(B)\right\}.                            \tag{32}
\]

The sums are over holes.  On the unweighted three-path,

\[
 \mathcal C(\nu)={1\over3},\qquad
 \mathcal C(\lambda)={103\over756}.                 \tag{33}
\]

On the regular weighted `K_4` with weights `(1,1,2)` at every vertex,

\[
 \mathcal C(\nu)={64\over1435},\qquad
 \mathcal C(\lambda)={8\over4387}.                  \tag{34}
\]

Thus the one-sample operator strongly expands even the target-centered
aggregate norm.  With the fixed `Pi` denominator, the path also has a
nonzero centered source mass at the empty set, where `Pi` is zero.  Hence no
fixed-`Pi` centered contraction is even well-defined without an explicit
empty-rank defect.

### 5.2 The unweighted variance split has incompatible exact witnesses

The identity

\[
 n(m_K-m)-EJ=n\{m_K-m-EG\}+\{nEG-EJ\}               \tag{35}
\]

does not split into two nonnegative terms.

On the weighted triangle `(w_01,w_02,w_12)=(1,1,5)`,

\[
 EJ={3456\over20291},\qquad
 EG={105472\over1976501},\qquad nEG-EJ<0,            \tag{36}
\]

while `m_K-m-EG>0` and the total target slack is `3136/20291`.

Conversely, on unweighted `K_(2,2)`,

\[
 m_K-m={4\over133},\qquad EJ={4\over57},\qquad
 EG={2\over57},                                      \tag{37}
\]

so `m_K-m-EG=-2/399<0`, while `nEG-EJ=4/57>0` and the
total target slack is `20/399`.

No graph-independent constant `alpha` inserted between these two terms can
repair this particular separation.  The triangle forces

\[
 \alpha\ge {EJ\over nEG}={90297\over84872}>1,
\]

whereas `K_(2,2)` forces

\[
 \alpha\le {m_K-m\over EG}={6\over7}.
\]

The rank-dependent coefficient (3) is forced by the sharp pointwise
geometry, and the active compensation in (26) must remain intact.

## 6. Verification and exact boundary

Run

~~~text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_weighted_reflection.py
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_reversible_edge_pairing.py
~~~

The verifier reconstructs every labelled one-target chain and stationary
law over exact rationals.  It checks the posterior, Cayley, variational,
pair, and Brier identities; certifies the counterexamples above; checks the
sharp extremizer families; and replays

* all 54 connected three-vertex graphs with weights in `{0,1,2,5}`;
* all 624 connected four-vertex graphs with weights in `{0,1,2}`;
* 48 deterministic sparse/extreme five-vertex graphs;
* the frozen six-vertex split witness.

Every graph in that corpus has nonnegative target slack and nonnegative
weighted-reflection slack.  Random reversible and directed geometric-union
kernels through seven vertices also had positive weighted slack; this is
**NUMERICAL EVIDENCE ONLY**.

Classification:

* **PROVED:** (4)--(8), the sharp coefficient (3), the sufficient reduction
  `(1) => (18)`, the variance identities (22), and decompositions
  (26), (31), and (35).
* **EXACTLY FALSIFIED:** centered Cayley contraction, the two separate signs
  in the unweighted variance split, componentwise active-channel
  monotonicity, reversible edge-pair positivity, and any proof which
  discards the active residual in (26).
* **EXACTLY COMPUTED:** positive target and weighted-reflection slack on the
  stated finite corpus; positive aggregate active Brier loss there.
* **NUMERICALLY OBSERVED:** no weighted-reflection violation in broader
  reversible or directed searches through seven vertices.
* **OPEN:** the universal stationary inequality (1), the aggregate
  transported Brier-risk inequality encoded by (26), and hence the
  universal finite dB baseline at fitness two.
