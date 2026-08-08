# The fair-geometric tree-reflection reduction at fitness two

Date: 2026-08-08 (America/Los_Angeles)

Status: the transition formula, Markov-chain tree reduction, complement
path-reversal identity, and counterexamples to the natural local transports
are **PROVED / EXACTLY COMPUTED**.  The resulting global arborescence
root-rank inequality is **OPEN**.  No counterexample to the actual stationary
mean bound was found.

This cycle deliberately attacks the exact target

\[
 E_\Pi |A|\le m_K,
 \qquad
 m_K={ (n-1)2^{n-2}\over 2^{n-1}-1},                 \tag{1}
\]

and does not use the stronger posterior-collision or Brier inequalities.

## 1. Exact fair-geometric subset kernel

Let `P` be the loopless vertex transition matrix,

\[
 P_{vi}={w_{vi}\over d_v},\qquad
 d_vP_{vi}=w_{vi}=d_iP_{iv}.                         \tag{2}
\]

At fitness two, the dual burst at target `v` takes an independent number
`N` of samples from row `P_v`, where

\[
 \Pr(N=j)=2^{-j},\qquad j\ge1.                       \tag{3}
\]

The sampled vertices are unioned after deleting `v`.  Uniformizing by a
uniform target gives a stochastic chain `Q` on

\[
 \Omega=\{A: \varnothing\ne A\subsetneq V\}.
\]

For a set of row mass `x`, put

\[
 F(x)=E[x^N]={x\over2-x}.                            \tag{4}
\]

For disjoint sets `C,D` not containing `v`, define

\[
 \Gamma_v(C,D)
 =\sum_{L\subseteq D}(-1)^{|L|}
 F\!\left(P_v(C\mathbin\cup(D\setminus L))\right). \tag{5}
\]

This is nonnegative: it is exactly the probability that every member of
`D` is sampled, no vertex outside `C union D` is sampled, and samples in
`C` are ignored as redundant.

If `A` and `B` are distinct, the exact transition formula is

\[
 Q(A,B)=
 \begin{cases}
 n^{-1}\Gamma_v(C,D),
 &A\setminus B=\{v\},\ C=A\setminus\{v\}\subseteq B,
   \ D=B\setminus C,\\[2mm]
 0,&\text{otherwise}.
 \end{cases}                                        \tag{6}
\]

Because the graph is loopless, a burst at an occupied target cannot restore
that target.  Hence

\[
 Q(A,A)={n-|A|\over n}.                              \tag{7}
\]

Equations (5)--(7) are derived directly from the update rule and are checked
edge by edge by the verifier.

### Complement path reversal

Write

\[
 A=C\cup\{v\},\quad B=C\cup D,\quad
 R=V\setminus(C\cup D\cup\{v\}).
\]

Then

\[
 \bar B=R\cup\{v\},\qquad \bar A=R\cup D,
\]

and therefore

\[
 \boxed{Q(\bar B,\bar A)={1\over n}\Gamma_v(R,D).} \tag{8}
\]

Thus complementing the states and reversing a state edge exchanges the two
redundant regions `C` and `R`, while retaining the target `v` and mandatory
new set `D`.

For one addition of row mass `p`, if `a=P_v(C)` and
`b=P_v(R)=1-a-p`, then

\[
 \Gamma_v(C,\{i\})
 ={2p\over(2-a-p)(2-a)},                             \tag{9}
\]

so

\[
 {Q(A,B)\over Q(\bar B,\bar A)}
 =\phi(a)\phi(a+p),
 \qquad \phi(x)={1+x\over2-x}.                      \tag{10}
\]

This ratio is not a rank-only potential and does not telescope around a
state arborescence.  Formula (2) remains available after expanding a burst
into its labelled vertex-walk samples, but the collapsed likelihood in
(10) involves subset masses from one row rather than pairwise reversible
edge products.

## 2. Markov-chain tree theorem: exact global reduction

Let `L` be the row Laplacian of the off-diagonal state rates,

\[
 L_{AB}=-Q(A,B)\quad(A\ne B),\qquad
 L_{AA}=\sum_{B\ne A}Q(A,B).                        \tag{11}
\]

For `A in Omega`, let

\[
 \tau_A=\det L^{(A)}
 =\sum_{T\in\mathcal T_A^{\rm in}}\prod_{X\to Y\in T}Q(X,Y),             \tag{12}
\]

where the sum is over directed spanning arborescences oriented toward root
`A`.  The Markov-chain tree theorem gives

\[
 \Pi(A)={\tau_A\over Z_P(1)},\qquad
 Z_P(t)=\sum_{A\in\Omega}\tau_A t^{|A|}.            \tag{13}
\]

Consequently

\[
 E_\Pi|A|={Z_P'(1)\over Z_P(1)}.                    \tag{14}
\]

For the complete graph, direct substitution into (6), or the known exact
complete stationary law already established in the project, gives

\[
 \tau_A^K=c_n(n-|A|).
\]

Therefore its root polynomial is

\[
 Z_K(t)=c_n\sum_{\varnothing\ne A\subsetneq V}(n-|A|)t^{|A|}
 =c_n n\{(1+t)^{n-1}-1\},                            \tag{15}
\]

and (14) gives exactly `m_K` in (1).

It follows that the desired finite-baseline theorem is **equivalent** to
the following single classical directed-tree inequality.

### Tree-Reflection Inequality `TR_n`

For every loopless irreducible reversible `P`, with `Q` defined by
(5)--(7),

\[
 \boxed{
 (n-1)2^{n-2}Z_P(1)
 -(2^{n-1}-1)Z_P'(1)\ge0.}                          \tag{TR_n}
\]

Equivalently,

\[
 \sum_{T\in\mathcal T^{\rm in}}w_Q(T)
 \left\{(n-1)2^{n-2}-(2^{n-1}-1)|r(T)|\right\}\ge0. \tag{16}
\]

This is not a sufficient surrogate: `(TR_n)` is exactly (1).  It is a
positive-arborescence root-rank inequality with explicit local edge weights
(5).

There is also a compact determinantal form.  If
`D(t)=diag(t^{|A|}:A in Omega)`, multilinearity gives

\[
 Z_P(t)=[\epsilon]\det\{L+\epsilon D(t)\}.           \tag{17}
\]

Thus `(TR_n)` is one signed first-derivative inequality for a standard
directed matrix-tree polynomial.  The obstacle is that `L` is generally
nonsymmetric even though the original vertex walk `P` is reversible.

## 3. Equivalent complement/out-tree likelihood inequality

Complementing every state and reversing every arrow maps an in-tree rooted
at `A` bijectively to an **out-tree** rooted at `bar A`.  For an out-tree
`U`, define its pulled-back positive weight

\[
 \widehat w(U)=\prod_{X\to Y\in U}Q(\bar Y,\bar X). \tag{18}
\]

Let

\[
 \theta_n=n-m_K
 ={(n+1)2^{n-2}-n\over2^{n-1}-1}.                   \tag{19}
\]

Then `(TR_n)` is equivalently

\[
 \boxed{
 \sum_{U\in\mathcal T^{\rm out}}
 \widehat w(U)\{|r(U)|-\theta_n\}\ge0.}             \tag{20}
\]

For positive original support, complement-reversed state support agrees and
one may divide by the ordinary out-tree weight.  With

\[
 \Lambda(U)=\prod_{X\to Y\in U}
 {Q(\bar Y,\bar X)\over Q(X,Y)},                    \tag{21}
\]

(20) becomes the likelihood--root-rank correlation inequality

\[
 E_{\rm out}\big[\Lambda(U)(|r(U)|-\theta_n)\big]\ge0.                    \tag{22}
\]

The cross-weight form (20), unlike (21), remains valid with zero original
edges.  A proof of (20) would close the exact `r=2` mean bound.

## 4. Exact failure of local root moving on `K_3`

The complement operation explains why the first involution attempts fail:
it converts an in-tree to an out-tree, not to an in-tree at the complementary
root.  Reversing the out-tree again would preserve the orientation class but
would require reverse state edges, and the state chain is not bidirected.

This obstruction is exact even for the unweighted triangle.  Label states by
their binary masks `1,...,6`.  Consider the in-tree rooted at mask `3`:

\[
 1\to6,\quad2\to5,\quad4\to3,\quad5\to3,\quad6\to3. \tag{23}
\]

Its five edge rates are

\[
 {1\over9},{1\over9},{1\over9},{2\over9},{2\over9},
\]

so its weight is

\[
 w(T)={4\over59049}.                                \tag{24}
\]

Complementing masks and reversing arrows gives the out-tree

\[
 1\to6,\quad2\to5,\quad4\to3,\quad4\to2,\quad4\to1, \tag{25}
\]

whose five rates are all `1/9`, hence

\[
 w(\mathcal C T)={1\over59049}.                     \tag{26}
\]

Thus even the maximally symmetric graph has a factor-four failure of
individual complement-path weight domination.

There is a stronger same-skeleton obstruction.  Take the undirected state
tree which is the star centered at mask `1`, with the other five masks as
leaves.  Among its six possible in-root orientations, the only one with
positive state-edge weight is rooted at mask `6`.  Its conditional root
mean is therefore

\[
 2>{4\over3}=m_K(K_3).                              \tag{27}
\]

So grouping arborescences by an undirected state-tree skeleton cannot prove
the target either.  Complementing (23) without reversing arrows immediately
creates the forbidden transition `6 to 1` of rate zero.

These are failures of proposed strengthenings, not counterexamples to
`(TR_3)`: the other state-tree skeletons compensate globally.

## 5. The labelled burst-history lift also needs global cancellation

A labelled burst history records the target `v`, length `N`, and ordered
sample sequence `(i_1,...,i_N)`.  Its edge weight is

\[
 {1\over n},2^{-N}\prod_{j=1}^N P_{v i_j}.          \tag{28}
\]

Microscopically reversing `v to i_j` uses (2):

\[
 {P_{vi}\over P_{iv}}={d_i\over d_v}.               \tag{29}
\]

Along genuine vertex paths the intermediate degree factors telescope.
However, a burst is a star: after reversal the arrows `i_j to v` generally
have several different targets and no longer form one admissible burst.
One might still hope to regroup all reversed microscopic arrows globally.

Regular `K_3` removes every degree-ratio issue and gives a decisive exact
screen.  Let `T_k(z)` count all labelled in-arborescence histories rooted at
rank `k`, with `z` marking the total number of vertex samples over the five
state-tree edges.  Direct enumeration and rational simplification give

\[
 T_1(z)=
 {18z^5(4z^2-10z+5)^2\over(1-z)^5(1-2z)^4},
\]

\[
 T_2(z)=
 {18z^6(4z^2-10z+5)^2\over(1-z)^5(1-2z)^5},         \tag{30}
\]

and therefore

\[
 \boxed{
 T_1(z)-2T_2(z)=
 {18z^5(1-4z)(4z^2-10z+5)^2
  \over(1-z)^5(1-2z)^5}.}                           \tag{31}
\]

The actual fair-geometric/walk weight is obtained at `z=1/4`, apart from
the common target factor `3^{-5}`.  Equation (31) vanishes there, as it must
at the complete-graph equality case.  But it is not coefficientwise
nonnegative:

\[
 [z^9](T_1-2T_2)=22248,
 \qquad
 [z^{10}](T_1-2T_2)=-197532.                        \tag{32}
\]

Hence there is no two-copy high-root-to-low-root injection which preserves
the total number of microscopic arrows.  Any successful labelled-history
transport must mix different geometric lengths or use a genuinely global
signed cancellation.  Ordinary path reversal, even after fully labelling
the bursts, does not supply the proof.

## 6. Exact hostile screens

The independent verifier constructs `Q` from the burst definition, checks
every row sum, verifies (5)--(8), solves stationarity, evaluates directed
tree cofactors, and checks (31)--(32) by direct labelled-history counting.

The actual mean bound, equivalently `(TR_n)`, passes exactly on:

- unweighted `P_3`, with `m=11/9 < 4/3`;
- regular weighted `K_4` with weights `(1,1,2)` at every vertex, with
  `m=70/41 < 12/7` and slack `2/287`;
- the frozen complete-support six-vertex split witness with edge weights
  `(3,300,2,5,1,3,3,1,300,1,1,1,20,1,1)`;
- the four stored complementary-level witnesses;
- all 54 connected weighted triangles with edge alphabet `{0,1,2,5}`;
- all 624 connected four-vertex graphs with edge alphabet `{0,1,2}`;
- 24 deterministic sparse/extreme five-vertex graphs.

These are **EXACT FINITE COMPUTATIONS**, not a universal proof.

## 7. What remains

The tree cycle leaves one sharply stated all-graph problem and rules out the
most direct ways of proving it.

> **OPEN TREE INEQUALITY.** Prove `(TR_n)`, equivalently (20), for the
> explicit fair-geometric edge weights (5) of every loopless irreducible
> reversible vertex kernel `P`.

The `K_3` labelled identity (31) shows that the fair value `z=1/4` is
essential: positivity appears only after cancellations across burst lengths.
A viable next step must therefore exploit the geometric recurrence itself,
not merely reverse a fixed labelled sample history.  Original reversibility
(2) can then control vertex-edge products, but a new length-changing or
forest-level operation is still required.

No actual counterexample to (1) or `(TR_n)` was found in this cycle.
