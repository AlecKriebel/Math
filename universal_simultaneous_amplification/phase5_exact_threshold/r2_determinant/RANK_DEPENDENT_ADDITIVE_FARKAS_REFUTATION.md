# Exact refutation of the rank-dependent additive ansatz

Date: 2026-08-08 (America/Los_Angeles)

## Status

The proposed rank-dependent additive potential at fitness two is **EXACTLY
REFUTED** by a connected 17-vertex undirected integer-weighted graph.  The
refutation uses a one-dimensional rational Farkas ray, all 48 of whose state
weights are strictly positive.

The same graph's 196-state quotient fixation system is also **EXACTLY
COMPUTED**.  The graph is death--Birth suppressing at fitness two.  Thus this
result closes only the additive-potential proof route; it does **not** refute
the universal fitness-two fixation inequality.

## 1. The ansatz and its exact drift system

For `n` vertices, consider

\[
 G(S)=1+{|S|\over n}+\sum_{v\in S}a_{|S|,v},                 \tag{1}
\]

where the correction is absent at ranks zero and `n`, and impose only

\[
 \sum_v a_{1,v}=0.                                          \tag{2}
\]

Let `P` be the row-stochastic replacement kernel, and for a mutant set `S`
put

\[
 x_v=P_{vS},\qquad g_v={2x_v\over1+x_v},\qquad
 \ell_v={1-x_v\over1+x_v}.                                  \tag{3}
\]

Thus, under dB updating at fitness two, an outside vertex `v` is added with
probability `g_v/n`, and an inside vertex is removed with probability
`ell_v/n`.  Write

\[
 G_{\rm out}=\sum_{v\notin S}g_v,\qquad
 L_{\rm in}=\sum_{v\in S}\ell_v,qquad k=|S|.                \tag{4}
\]

After the fixed positive scaling used in the determinant reduction, the
drift inequality is

\[
 B_S+\sum_{r,u}A_{S;(r,u)}a_{r,u}\ge0,                       \tag{5}
\]

where

\[
 B_S=-{n+k-1\over n}G_{\rm out}
       +{2(n+k-2)\over n}L_{\rm in},                         \tag{6}
\]

and the labelled columns are

\[
 A_{S;(r,u)}=
 \begin{cases}
 -2(G_{\rm out}+L_{\rm in})1_{\{u\in S\}},&r=k,\\
 G_{\rm out}1_{\{u\in S\}}+g_u1_{\{u\notin S\}},&r=k+1,\\
 4(L_{\rm in}-\ell_u)1_{\{u\in S\}},&r=k-1,\\
 0,&\text{otherwise}.
 \end{cases}                                                 \tag{7}
\]

The verifier derives `(3)--(7)` from the labelled replacement kernel and
checks every reduced row against the corresponding labelled row.

## 2. The graph and the exact quotient

Partition the vertices into three classes of sizes

\[
 (m_1,m_2,m_3)=(2,5,10).                                    \tag{8}
\]

For distinct vertices in classes `i,j`, assign edge weight `W_ij`, where

\[
 W=\begin{pmatrix}
 20000000&15&5\\
 15&9&4500\\
 5&4500&150
 \end{pmatrix}.                                               \tag{9}
\]

All off-diagonal vertex pairs have positive weight, so the graph is
connected and has complete support.  Its three weighted degrees are

\[
 20000125,\qquad 45066,\qquad 23860.                         \tag{10}
\]

The automorphism group contains
`S_2 x S_5 x S_10`.  An invariant state is the count triple
`(s_1,s_2,s_3)`, giving 196 transient state orbits.  An invariant coefficient
is indexed by `(r,c)`, with `1<=r<=16` and `1<=c<=3`, giving 48 variables.
Summing `(7)` over the vertices of class `c` gives the exact quotient row

\[
 A_{S;(r,c)}=
 \begin{cases}
 -2(G_{\rm out}+L_{\rm in})s_c,&r=k,\\
 s_cG_{\rm out}+(m_c-s_c)g_c,&r=k+1,\\
 4s_c(L_{\rm in}-\ell_c),&r=k-1,\\
 0,&\text{otherwise}.
 \end{cases}                                                  \tag{11}
\]

The boundary row is `E_(1,c)=m_c`, with all other entries zero.

This quotient loses no possible labelled solution.  Indeed, if labelled
coefficients satisfied `(2)` and every inequality `(5)`, averaging them over
`S_2 x S_5 x S_10` would preserve both the equality and every inequality,
while making the coefficients constant on each class.  Therefore
infeasibility of `(11)` implies infeasibility of the full labelled ansatz.

## 3. Exact Farkas certificate

Let `A` be the 196-by-48 matrix in `(11)`, `B=(B_S)`, and let `E` be the
boundary row.  The primal system is

\[
 -Aa\le B,\qquad Ea=0.                                      \tag{12}
\]

A Farkas obstruction consists of `y>=0` and a free scalar `z` such that

\[
 -A^Ty+E^Tz=0,\qquad B^Ty<0.                                \tag{13}
\]

The exact witness is supported on 48 state orbits, embedded explicitly in
`verify_rank_dependent_additive_farkas.py`.  Restricting `(13)` to that
support produces a 48-by-49 rational balance matrix.  Exact elimination
gives

\[
 \operatorname{rank}=48,\qquad \dim\ker=1.                  \tag{14}
\]

Normalize the unique ray by `z=-1`.  Direct exact substitution proves that
all 48 coordinates of `y` are strictly positive, every balance in `(13)` is
identically zero, and

\[
 B^Ty=-0.34734270358231461111\ldots<0.                       \tag{15}
\]

The value in `(15)` is held and tested as an exact rational number: its
absolute numerator and denominator each have 676 decimal digits.  Its
canonical `numerator/denominator` SHA-256 identifier is

```text
f87fa20154d7ee87a54d5f5d151acbeb4b435696bba6580efcba7c21cdc5cbbc
```

The strict exact sign in `(15)`, not the decimal display, proves by Farkas'
lemma that no potential of form `(1)` exists on this graph.

### 3.1 Rank telescoping structure

The ray is not merely an opaque elimination output.  Aggregate its gain and
loss masses by rank:

\[
 \mathcal A_k=\sum_{|S|=k}y_SG_{\rm out}(S),\qquad
 \mathcal R_k=\sum_{|S|=k}y_SL_{\rm in}(S),                  \tag{16}
\]

with `\mathcal A_0=\mathcal R_{17}=0`.  Summing the three class-column
balances at each rank
gives the exact recurrence

\[
 \mathcal A_{k-1}-2(\mathcal A_k+\mathcal R_k)
       +4\mathcal R_{k+1}=0,\qquad 2\le k\le16.              \tag{17}
\]

At rank one the same left side is `-17`, exactly accounting for the
normalization `z=-1`.  Weighted telescoping of `(17)` reduces the entire
Farkas objective to

\[
 B^Ty={32\mathcal R_1-(2^{16}\,18-34)\mathcal A_{16}\over17}.
                                                                    \tag{18}
\]

On the exact ray,

\[
 \mathcal R_1=4.4131019629893546565\ldots,\qquad
 \mathcal A_{16}=0.00012472223013338151073\ldots,             \tag{19}
\]

and exact rational comparison gives

\[
 {\mathcal A_{16}\over\mathcal R_1}
 =2.8261805682118649783\ldots\times10^{-5}
 >{32\over2^{16}\,18-34}
 =2.7127517984696688917\ldots\times10^{-5}.                  \tag{20}
\]

Equations `(17)--(20)` explain the strict negative sign.  They also identify
the limitation of `(1)`: it records one marked vertex, hence only a
first-moment rank balance.  A stronger forest or occupation-law dual would
need additional two-marked-vertex or collision information to rule out this
endpoint transfer.  This last sentence is a structural guide, not a theorem
about which enlarged certificate must succeed.

## 4. Independent exact fixation calculation

The verifier separately constructs the dB chain on all 196 transient count
triples.  From a state `s`, its only nontrivial transitions are

\[
 p(s,s+e_c)={m_c-s_c\over17}g_c,\qquad
 p(s,s-e_c)={s_c\over17}\ell_c.                              \tag{21}
\]

It solves the resulting rational absorbing equations with FLINT and checks
every equation again over exact fractions.  Uniform singleton initialization
gives

\[
 \rho_{\rm dB}(G,2)=0.41104395434060972695\ldots .            \tag{22}
\]

For comparison, an independent one-dimensional solution for the complete
graph gives

\[
 \rho_{\rm dB}(K_{17},2)={524288\over1114095}.                \tag{23}
\]

Exact cross-multiplication yields

\[
 {\rho_{\rm dB}(G,2)\over\rho_{\rm dB}(K_{17},2)}
 =0.87345507490368193387\ldots<1.                            \tag{24}
\]

The exact fraction in `(22)` has 2154 numerator digits and 2155 denominator
digits; its canonical SHA-256 identifier is

```text
58610aa6f12f6e383ce1758e9b3a04a01af69adbcd05f18cb122b380e3d94a8f
```

## 5. Scope

- **PROVED:** the 196-state quotient is exactly lumpable by class counts.
- **EXACTLY REFUTED:** universal feasibility of the rank-dependent additive
  ansatz `(1)`.
- **EXACTLY COMPUTED:** this graph's dB fixation probability at fitness two.
- **PROVED FOR THIS GRAPH:** it is dB-suppressing at fitness two.
- **OPEN:** the universal fitness-two fixation inequality.

The last point is essential: the Farkas counterexample eliminates a proposed
certificate class, not the target universal theorem.
