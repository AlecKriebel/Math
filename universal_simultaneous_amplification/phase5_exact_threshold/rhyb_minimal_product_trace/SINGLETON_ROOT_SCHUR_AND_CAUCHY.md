# Singleton-root Schur trace and the sharp Cauchy split

Date: 2026-08-13 (America/Los_Angeles)

No external communication or new graph search was used.  Two previously
stored hostile graphs are replayed as exact audits in Section 7.

## Status

This note gives a second exact reduction of the minimal stationary product

\[
 q_Bq_D\ge r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+,
 \qquad p=1-\frac1r.                                  \tag{1}
\]

The rank-one/rank-two trace can be Schur-compressed once more, all the way
to the singleton roots.  After this compression, the total singleton masses
cancel from (1).  The remaining statement compares

1. the two stationary laws of the singleton-root trace chains; and
2. the signed excess-rank reward of one excursion away from a singleton.

There is then an exact Cauchy decomposition into a nonnegative orientation
square and one scalar root-overlap remainder.  This is the sharpest direct
one-step Cauchy factorization: its entire loss is displayed as a sum of
squares.  A sufficient all-portal version of the scalar remainder reduces
to portal vectors supported on at most two vertices.

The sign of the universal remainder remains open.  Moreover, the tempting
stronger hope that the two singleton traces are adjoints of one common
undirected conductance is exactly false already on the unweighted
three-path.  Thus a Picone proof cannot pair their trace edges one by one.

## 1. Direct trace to singleton roots

Fix one of the two dual rules `U` on a connected loopless weighted module
of order `s`.  Work on the recurrent state space of its exact stationary OR
dual.  Partition that space into the singleton states `S` and their
complement `R`, and write

\[
 Q_U=\begin{pmatrix}Q_{SS}^U&Q_{SR}^U\\
                     Q_{RS}^U&Q_{RR}^U\end{pmatrix},
 \qquad \pi_U=(u_U,w_U).                              \tag{2}
\]

Here `u_U(i)=pi_U({i})` is the row of singleton atoms.  The killed
complement is transient, so

\[
 G_U=(-Q_{RR}^U)^{-1}\ge0.                            \tag{3}
\]

Define the singleton-root trace generator

\[
 \boxed{T_U=Q_{SS}^U+Q_{SR}^UG_UQ_{RS}^U.}            \tag{4}
\]

For the density excess reward

\[
 g(A)=\frac{|A|}{s}-p,                                \tag{5}
\]

put

\[
 \tau_U=\mathbf1+Q_{SR}^UG_U\mathbf1,
 \qquad
 \phi_U=g_S+Q_{SR}^UG_Ug_R.                          \tag{6}
\]

Stationarity in the `R` block and then in the `S` block gives

\[
 w_U=u_UQ_{SR}^UG_U,\qquad u_UT_U=0.                 \tag{7}
\]

Normalization and (5)--(6) consequently give the exact identities

\[
 \boxed{
 u_U\tau_U=1,\qquad
 u_U\phi_U=\rho_U-p.}                                \tag{8}
\]

If `omega` is a portal probability vector, its reward is supported on the
singleton roots, and hence

\[
 \boxed{q_U^\omega=u_U\omega.}                        \tag{9}
\]

Thus every rank at least two has been retained, but only through the killed
Green excursion in (4) and (6).

This compression is associative with the rank-three construction.  Namely,
first eliminate all ranks at least three from `S union D`, where `D` is the
doubleton sector, and then eliminate `D`.  The resulting generator, time
reward, and excess reward are exactly (4) and (6).  This is the ordinary
associativity of block Gaussian elimination; the exact replay checks it on
a nonregular weighted four-path for both rules.

## 2. Cancellation of the total singleton masses

Let

\[
 c_U=u_U\mathbf1>0,\qquad
 \lambda_U=\frac{u_U}{c_U},\qquad
 \overline\phi_U=\lambda_U\phi_U.                    \tag{10}
\]

Thus `lambda_U` is the stationary probability law of the singleton-root
trace, while `bar(phi)_U` is the mean signed excess-rank reward per
singleton excursion.  Equations (8)--(10) say

\[
 \rho_U-p=c_U\overline\phi_U,qquad
 q_U^\omega=c_U(\omega\mathbin\cdot\lambda_U).        \tag{11}
\]

Use `gamma` for Bd and `alpha` for dB.  On the active branch of (1), the
raw product gap therefore factors as

\[
\boxed{
 q_Bq_D-r^3(\rho_{Bd}-p)(\rho_{dB}-p)
 =c_Bc_D\left[
  (\gamma\mathbin\cdot\lambda_B)
  (\alpha\mathbin\cdot\lambda_D)
  -r^3\overline\phi_B\overline\phi_D\right].}        \tag{12}
\]

The factors `c_B,c_D` are positive and disappear from the sign problem.
Consequently the minimal stationary product is exactly the following
**singleton-root repayment inequality**:

\[
 \boxed{
 (\gamma\mathbin\cdot\lambda_B)
 (\alpha\mathbin\cdot\lambda_D)
 \ge r^3[\overline\phi_B]_+[\overline\phi_D]_+.}     \tag{SRR}
\]

Compared with the rank-three MPER, `(SRR)` removes the two cycle-time
normalizations and the two total singleton masses.  It does not discard
higher ranks: they determine both trace laws `lambda_U` and both Green
rewards `phi_U`.

## 3. Exact Cauchy decomposition

Put

\[
 A_i=\gamma_i\lambda_{B,i},\qquad
 B_i=\alpha_i\lambda_{D,i},\qquad
 \mathcal H=\sum_i\sqrt{A_iB_i}.                      \tag{13}
\]

The elementary Lagrange identity gives

\[
\boxed{
 (\sum_iA_i)(\sum_iB_i)
 =\mathcal H^2+
 {1\over2}\sum_{i,j}
 \left(\sqrt{A_iB_j}-\sqrt{A_jB_i}\right)^2.}        \tag{14}
\]

Combining (12)--(14) yields the sharp Cauchy split

\[
\begin{split}
 {q_Bq_D-r^3(\rho_{Bd}-p)(\rho_{dB}-p)\over c_Bc_D}
 ={}&{1\over2}\sum_{i,j}
 \left(\sqrt{A_iB_j}-\sqrt{A_jB_i}\right)^2\\
 &+\mathcal H^2-r^3\overline\phi_B\overline\phi_D.
                                                               \tag{15}
\end{split}
\]

No covariance term is hidden.  The first line is exactly the determinant
discarded by a direct Cauchy--Schwarz argument.  Therefore the natural
scalar sufficient condition is

\[
 \boxed{
 \mathcal H^2\ge
 r^3[\overline\phi_B]_+[\overline\phi_D]_+.}          \tag{RHR}
\]

Call `(RHR)` the **root-Hellinger repayment inequality**.  It can be
strictly stronger than `(SRR)`, because the orientation square in (15) may
repay a negative scalar remainder.  Hence `(RHR)` is a proof route, not a
new conjectural reformulation of the target.

## 4. The all-portal root-Hellinger test is pairwise

For a portal load `x>=0`, let `e_i=1/d_i`.  The physical portal laws are

\[
 \gamma_i={x_i\over x\cdot\mathbf1},\qquad
 \alpha_i={e_ix_i\over x\cdot e}.                    \tag{16}
\]

Set

\[
 a_i=\sqrt{e_i\lambda_{B,i}\lambda_{D,i}},\qquad
 Q_0=r^3[\overline\phi_B]_+[\overline\phi_D]_+.      \tag{17}
\]

Then `(RHR)` is exactly

\[
 \boxed{(x\cdot a)^2\ge Q_0(x\cdot\mathbf1)(x\cdot e).}       \tag{18}
\]

There is no continuum of portal dimensions hidden in (18): it holds for
every `x>=0` if and only if it holds for every `x` supported on at most two
vertices.

To prove this, normalize `x` to a probability vector `theta`.  The gap is

\[
 F(\theta)=(\theta\cdot a)^2-Q_0(\theta\cdot e).       \tag{19}
\]

At a minimizer, the active coordinates satisfy the first-order equation

\[
 2(\theta\cdot a)a_i-Q_0e_i=\text{constant}.          \tag{20}
\]

Thus all points `(a_i,e_i)` in the support lie on one affine line.  Their
two moments in (19) can be reproduced by a convex combination of the two
extreme support points.  Hence a minimizer exists with support at most two.
Equivalently, it is enough to check, for every pair `i,j`,

\[
 \left{ta_i+(1-t)a_j\right}^2
 \ge Q_0\{te_i+(1-t)e_j\},\qquad0\le t\le1.           \tag{21}
\]

Each test in (21) is only a convex quadratic in one scalar.  This is a
universal reduction of the sufficient Cauchy certificate, not a search over
portal vectors.

## 5. Exact obstruction to a common-conductance Picone proof

One might hope that undirectedness of the original module makes the two
singleton-root traces adjoints, perhaps after positive diagonal weights and
positive row time changes.  That would put (15) into a common edge
Dirichlet form.  The hope is false on the smallest nontrivial example.

Take the unweighted path `L--C--R` at `r=3/2`.  In the root order
`(L,C,R)`, direct Schur elimination gives

\[
 T_{Bd}=\begin{pmatrix}
 -5/8&7/12&1/24\\
 4/3&-8/3&4/3\\
 1/24&7/12&-5/8
 \end{pmatrix},
 \qquad
 T_{dB}=\begin{pmatrix}
 -1&1&0\\
 3/7&-6/7&3/7\\
 0&1&-1
 \end{pmatrix}.                                      \tag{22}
\]

In particular,

\[
 T_{Bd}(L,R)=\frac1{24}>0,qquad T_{dB}(R,L)=0.        \tag{23}
\]

Positive diagonal similarities and positive row clocks preserve directed
support.  Therefore no such transformation can make the two matrices
adjoints of a common conductance.  The mechanism is physical: a Bd
excursion can branch and return from one leaf singleton to the other without
hitting the centre singleton, whereas a dB singleton trace cannot make that
skip.

The same calculation gives

\[
 \lambda_B={1\over39}(16,7,16),\qquad
 \lambda_D={1\over13}(3,7,3),                         \tag{24}
\]

and

\[
 \phi_B={1\over63}(10,40,10)^T,\qquad
 \phi_D={1\over21}(0,2,0)^T.                         \tag{25}
\]

Thus

\[
 \overline\phi_B={200\over819},\qquad
 \overline\phi_D={2\over39},\qquad
 r^3\overline\phi_B\overline\phi_D={50\over1183}.  \tag{26}
\]

Despite the adjoint obstruction, `(RHR)` holds for every portal on this
path.  Here

\[
 a_L=a_R={4\over13},\qquad a_C={7\over13\sqrt6},
 \qquad e_L=e_R=1,\ e_C=1/2.                          \tag{27}
\]

The only nontrivial pair test is a leaf--centre mixture.  After multiplying
by `13^2`, its gap is

\[
 \left(4(1-t)+{7t\over\sqrt6}\right)^2
 -{50\over7}\left(1-{t\over2}\right).               \tag{28}
\]

It is decreasing on `[0,1]` and has minimum `193/42>0` at `t=1`.
This illustrates the intended role of the reduction: retain root-law
overlap and excursion repayment, but do not impose a false edgewise
identification of the two trace chains.

## 6. Exact replay and remaining gap

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_singleton_root_schur.py
```

The replay checks direct-versus-two-stage Schur elimination on a hostile
rational weighted four-path for both rules, verifies (8), (11), and (12),
checks the generic Lagrange square (14), and reproduces every rational datum
in (22)--(27) together with the exact sign proof for (28).

The universal sign of `(SRR)` is still open.  The new proof-first choices
are now precise:

1. prove `(RHR)` by comparing root-law Hellinger overlap with the two Green
   excursion rewards; or
2. retain the explicit orientation square in (15) and prove the weaker,
   exact `(SRR)` directly.

Any successful route must compare the two rules beyond a common trace-edge
Picone identity, which (22)--(23) refute exactly.

## 7. The entrywise portal target and why same-cut odds do not prove it

Returning from normalized root laws to the raw singleton atoms, the natural
portal-general strengthening of `(MP)` is

\[
 \boxed{
 u_i e_jv_j+u_j e_iv_i
 \ge Q(e_i+e_j)\quad(i,j\in V),
 \qquad
 Q=r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+.}                \tag{29}
\]

Indeed, (29) makes every coefficient of

\[
 (x\cdot u)(x\cdot(ev))-Q(x\cdot\mathbf1)(x\cdot e) \tag{30}
\]

nonnegative.  It is exactly the strengthening used by the proved weighted
triangle theorem.  As finite evidence only, the replay below also verifies
it at the rational diagnostic fitness `r=3/2`, in exact arithmetic, on two
stored hostile order-four witnesses: the nonregular complete-support graph
with edges `(1,2,4,3,5,7)` and the previously stored statewise-committor
witness with matrix

```text
[[0, 7, 3, 17],
 [7, 0, 15, 6],
 [3, 15, 0, 5],
 [17, 6, 5, 0]].
```

These two finite checks are audits only, not a theorem at `R_hyb` and not a
proof of (29) in arbitrary order.

There is a precise obstruction to the most direct optional-stopping proof.
At every *common* mutant set `A`, the exact up/down odds obey

\[
 R_{Bd}(A)R_{dB}(A)\le r^3.                            \tag{31}
\]

But (29) is a two-copy statement: `u_i` and `v_j` are absorption
probabilities under different chains and their occupation histories need
not visit the same set.  The bound (31) is false after independent
cross-state pairing.  On the unweighted three-path at `r=3/2`,

\[
 R_{Bd}(\{L\})=3,
 \qquad R_{dB}(\{L,C\})={5\over2},
 \qquad {15\over2}>r^3={27\over8}.                    \tag{32}
\]

Therefore multiplying path likelihood ratios after independent stopping
does not preserve the factor `r^3`.  A valid path-reversal proof of (29)
would need a synchronized marked-history coupling or a compensating
Radon--Nikodym current; the statewise cut envelope alone cannot supply it.
