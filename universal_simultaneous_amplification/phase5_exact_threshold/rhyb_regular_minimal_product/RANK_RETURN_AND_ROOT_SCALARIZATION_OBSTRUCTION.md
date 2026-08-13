# Finite-depth return and root-scalarization obstructions

Date: 2026-08-13 (America/Los_Angeles)

No external communication or graph enumeration was used.

## Status

The regular vertexwise dB repayment inequality

\[
 \pi_D(\{i\})\ge r^2[\rho_D-p]_+,
 \qquad p={r-1\over r},                              \tag{VDR}
\]

remains **OPEN**.  This note proves two exact proof-route obstructions.

1. Even the full doubleton stationarity row, including its genuine
   triple-to-doubleton entrance current, is insufficient.  More generally,
   every fixed finite prefix of the state equations admits normalized
   pseudo-laws that violate `(VDR)` at `R_hyb`.
2. The honest stopped-chain identity is intrinsically root-marked.  Summing
   it to a scalar rank profile loses information that cannot be restored by
   the canonical root-average bound: that bound would force all singleton
   atoms to be equal, and an exact connected regular graph refutes this for
   every `r>1`.

Neither construction is a graph counterexample to `(VDR)`.  They show that
a proof must retain both the full high-excursion return and a marked root.

## 1. The dB dual falls by at most one rank

At a clock ring of an occupied target `v`, the dB dual update is

\[
 A\longmapsto (A\setminus\{v\})\cup U_v,             \tag{1}
\]

where `U_v` is the nonempty union of a geometric number of samples from row
`P_v`.  Consequently

\[
 |A'|\ge |A|-1.                                      \tag{2}
\]

This elementary support fact makes it possible to audit exactly what a
finite collection of low-rank stationarity equations can see.

## 2. No fixed rank prefix can prove VDR

Fix an integer `m>=1`, a complete regular kernel of order `s>=m+3`, and its
genuine stationary dB-dual law `pi`.  Put

\[
 \lambda_m=\sum_{1\le |A|\le m+1}\pi(A),             \tag{3}
\]

choose one set `R` of rank `m+2`, and, for `0<epsilon<1`, define

\[
 \widetilde\pi_\epsilon(A)=
 \begin{cases}
  \epsilon\pi(A),&1\le |A|\le m+1,\\
  1-\epsilon\lambda_m,&A=R,\\
  0,&\text{otherwise}.
 \end{cases}                                         \tag{4}
\]

This is a normalized nonnegative law.  If `|A|<=m`, then (2) says that no
state of rank at least `m+2` can enter `A` in one update.  Hence

\[
 \begin{aligned}
 (\widetilde\pi_\epsilon Q)(A)
 &=\epsilon\sum_{1\le |B|\le m+1}\pi(B)Q(B,A)\\
 &=\epsilon(\pi Q)(A)=0.                              \tag{5}
 \end{aligned}
\]

Thus **every individual stationary equation through rank `m` holds
exactly**, not merely its scalar rank sum.

For `m=2`, equation (5) includes every singleton and doubleton equation.
In particular it retains the complete triple-to-doubleton entrance current
in the second low-sector block row.  Therefore the immediate
rank-two/rank-three return row does not repair the earlier singleton-only
relaxation.

The obstruction is uniform in the depth.  Take

\[
                         s=2(m+2).                    \tag{6}
\]

As `epsilon` tends to zero, (4) gives

\[
 \widetilde\rho_\epsilon\longrightarrow {m+2\over s}
 ={1\over2},
 \qquad
 \widetilde\pi_\epsilon(\{i\})\longrightarrow0.     \tag{7}
\]

Throughout the exact isolating interval of `R_hyb`,

\[
 {3\over2}<r<{151\over100},\qquad
 p<{51\over151}<{1\over2}.                           \tag{8}
\]

The right side of `(VDR)` therefore tends to the strictly positive number
`r^2(1/2-p)`, while every singleton atom tends to zero.  For sufficiently
small `epsilon`, (4) violates `(VDR)` at every root.

This proves a finite-depth theorem, not just an order-eight example:

> Positivity, normalization, and all coordinate stationarity equations up
> to any fixed rank cannot prove `(VDR)` uniformly in the graph order.

The exact replay instantiates the first new case `m=2`, `s=8`, `r=3/2`.
It builds the complete-kernel rank chain, checks all 36 singleton and
doubleton coordinate equations, and verifies a strict pseudo-law violation.
The pseudo-law is deliberately not stationary at rank three.

## 3. Honest return is a root-marked Green identity

Now return to a genuine dual.  Split its recurrent state space into

\[
 \mathcal L=\{A:1\le |A|\le2\},\qquad
 \mathcal H=\{A:|A|\ge3\},                            \tag{9}
\]

and let

\[
 G^-=(-Q^{--})^{-1},\qquad
 \eta=\pi^+Q^{+-}.                                   \tag{10}
\]

The exact stopped-chain relation is

\[
                         \pi^-=\eta G^-.              \tag{11}
\]

For a named root `i`, put

\[
 K_i(C)=G^-(C,\{i\}),\qquad C\in\binom V2.           \tag{12}
\]

Then (11) gives the rooted singleton atom

\[
 \boxed{v_i=\sum_C\eta(C)K_i(C).}                    \tag{13}
\]

Summing over roots retains only

\[
 q_1:=\sum_iv_i
 =\sum_C\eta(C)\sum_iK_i(C).                         \tag{14}
\]

Equation (14) is the scalar rank-profile shadow of (13).  It discards the
orientation of the doubleton-fed occupation among the singleton roots.

The canonical way to upgrade a scalar average theorem

\[
                         {q_1\over s}\ge T            \tag{15}
\]

to `v_i>=T` for every `i` would be the root-average bridge

\[
                         v_i\ge {q_1\over s}
                         \quad(i\in V).               \tag{16}
\]

But summing (16) over `i` forces equality in every coordinate.  Thus (16)
is equivalent to uniform singleton atoms.  The next section refutes that
property exactly inside the connected regular class.

## 4. Exact regular obstruction to root averaging

Partition six vertices into classes

\[
 X=\{0,1\},\qquad Y=\{2,3,4,5\},                     \tag{17}
\]

and use the symmetric stochastic kernel

\[
 P_{ij}=\begin{cases}
  3/5,&i\ne j,\ i,j\in X,\\
  4/15,&i\ne j,\ i,j\in Y,\\
  1/10,&i\in X,\ j\in Y\ \text{or conversely},\\
  0,&i=j.
 \end{cases}                                         \tag{18}
\]

Every row sums to one, so this is a connected regular weighted graph.  Let
`mu_xy` be the stationary dB-dual mass of states containing `x` vertices
of `X` and `y` vertices of `Y`.  The singleton atoms within each class are

\[
                         v_X={\mu_{10}\over2},\qquad
                         v_Y={\mu_{01}\over4}.         \tag{19}
\]

Solving the exact 13-state orbit chain gives

\[
 v_X-v_Y=
 -{375r(r-1)^2(9r+1)F(r)\over2D(r)},                 \tag{20}
\]

where

\[
\begin{aligned}
F(r)={}&224583960r^{10}+3150513334r^9+17487944995r^8\\
&+53883076579r^7+112461136241r^6+181841150181r^5\\
&+224583406416r^4+192172906510r^3+102331562256r^2\\
&+29868277824r+3503896704,                            \tag{21}
\end{aligned}
\]

and \(D(r)=\sum_{k=0}^{18}d_kr^k\) has the coefficient vector

\[
\begin{aligned}
(d_0,\ldots,d_{18})={}&(
1513683376128,33103970621568,291981783940704,\\
&1439657416451304,4625918408977902,10744093126699298,\\
&19442041987593843,28860066322602760,36258144436319895,\\
&39084932504333196,36258144436319895,28860066322602760,\\
&19442041987593843,10744093126699298,4625918408977902,\\
&1439657416451304,291981783940704,33103970621568,\\
&1513683376128).
\end{aligned}                                                    \tag{22}
\]

All coefficients in (21)--(22) are positive.  Therefore

\[
                         v_X<v_Y\qquad(r>1).          \tag{23}
\]

Since `q_1/6=(2v_X+4v_Y)/6`, equation (23) gives

\[
                         v_X<{q_1\over6}<v_Y.         \tag{24}
\]

Thus the root-average bridge (16) fails for the two roots in `X` at every
fitness `r>1`, in particular at `R_hyb`.  At `r=3/2`, an independent exact
labelled-chain audit gives

\[
 v_X={30887287990994154160\over494390162744319752327},
 \quad
 v_Y={31101376043908505160\over494390162744319752327}. \tag{25}
\]

Permuting an `X` label with a `Y` label leaves the complete scalar rank law
unchanged but changes the singleton atom at that named label.  Hence a
rank-only stopped-chain calculation cannot recover (13).  It must retain a
root-marked Green occupation, or introduce information that is no longer a
scalar rank profile.

## 5. Consequence for the proof program

The two obstructions identify the minimal information that a surviving
stopped-chain or submartingale proof must keep:

1. the entire high excursion, not one more finite rank-return row; and
2. the named root throughout the excursion, not only its terminal rank.

Rank-by-rank induction simply moves the scaling obstruction upward.  The
honest alternative is a full high-block Green identity or an equivalent
root-marked tree functional with a uniform sign.  No such new invariant is
proved here, so this route stops at the exact obstruction rather than
starting a graph or coefficient search.

## 6. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_rank_return_obstruction.py
```

The replay uses exact arithmetic.  It verifies the `m=2` coordinate
closure, the strict pseudo-law failure, the honest low/high Green identity,
and the all-`r>1` factorization (20).  It does not assert that the pseudo-law
is a stationary graph law or that universal `(VDR)` is false.
