# The geometric branching-tree rerooting obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, or external communication was used.

## 1. Status

**EXACT TREE EXPANSION AND DECISIVE OBSTRUCTION TO PURE REROOTING.**
Throughout, `1<r<2`, as in the interval containing `R_hyb`.  Let

\[
 c=r-1,
 \qquad A_i=1+rt_i,
 \qquad B_i=t_i+r.
\]

The two endpoint branching processes have exact finite typed plane-tree
weights.  They put the diffuse support target in the form

\[
 E_p h+cE_pq-1
   =\sum_T\{W_D(T)+cW_B(T)-W_0(T)\},                 \tag{1}
\]

where `h=1-s`, `W_D` is the supercritical dB finite-tree weight, `W_B`
is the supercritical Bd finite-tree weight, and `W_0` is the critical
`r=1` dB tree probability.  The total `W_0` mass is exactly one.

The tempting proof would preserve an unrooted typed plane tree and move its
root, using reversibility to transport mass between the three terms in (1).
This note proves that this cannot work.  On a symbolic two-type family, the
total target mass available under *every rerooting* of a `d`-leaf star is
exponentially smaller than its critical source mass.  The supplied identity

\[
 (1+rt)(t+r)-r(1+t)^2=c^2t                         \tag{2}
\]

does not repair the comparison: it is exactly the identity that exposes the
strict per-leaf contraction.

This result rules out coefficientwise extinction-tree injections and mass
transports that only reroot a fixed unrooted typed plane tree.  It does **not**
disprove the diffuse support inequality, and it does not rule out a genuinely
nonlocal tree transform that moves mass between different shapes or a proof
that couples infinite survival trees.

## 2. Endpoint Galton--Watson processes

Let `P` be a finite irreducible row-stochastic kernel reversible for `pi`.
Let `a>0`, normalized by `E_pi a=1`, and set

\[
 p_i=\pi_i a_i,
 \qquad R=D_a^{-1}PD_a,
 \qquad t_i={(Pa)_i\over a_i}.                         \tag{3}
\]

Thus `R1=t`, and

\[
 p_iR_{ij}=p_jP_{ji}.                                  \tag{4}
\]

The dB process started at type `i` has

\[
 N_i^D\sim\operatorname{Geom}_0(rt_i),
 \qquad K^D_{ij}={R_{ij}\over t_i}.                    \tag{5}
\]

Here `Geom_0(m)` has probability

\[
 \Pr(N=k)={m^k\over(1+m)^{k+1}},\qquad k\geq0.
\]

Its extinction probability `h=1-s` obeys

\[
 h_i={1\over1+r(t_i-(Rh)_i)},
 \qquad s=r(1-s)Rs.                                    \tag{6}
\]

The Bd process has

\[
 N_i^B\sim\operatorname{Geom}_0(r/t_i),
 \qquad K^B_{ij}=P_{ij},                               \tag{7}
\]

and its extinction probability is

\[
 q_i={t_i\over t_i+r(1-(Pq)_i)}.                       \tag{8}
\]

Both mean matrices have Perron root `r`: they are `rR` and
`rD_t^{-1}P`, respectively.

## 3. Exact finite rooted plane-tree weights

Let `T` be a finite rooted plane tree.  Give every vertex `v` a type
`\tau_v`; write `d_v` for its number of children.  A direct multiplication
of the geometric offspring probabilities and child-type probabilities gives

\[
 \Pr_i^D(T,\tau)
 =r^{|E(T)|}
   \prod_v A_{\tau_v}^{-(d_v+1)}
   \prod_{v\to w}R_{\tau_v\tau_w},                    \tag{9}
\]

and

\[
 \Pr_i^B(T,\tau)
 =r^{|E(T)|}
   \prod_v {t_{\tau_v}\over B_{\tau_v}^{d_v+1}}
   \prod_{v\to w}P_{\tau_v\tau_w}.                   \tag{10}
\]

The root type in (9)--(10) is `i`.  Include the diffuse root law by defining

\[
 W_D(T,\tau)=p_i\Pr_i^D(T,\tau),
 \qquad W_B(T,\tau)=p_i\Pr_i^B(T,\tau).                \tag{11}
\]

Summing over all finite typed plane trees proves

\[
 E_ph=\sum_TW_D(T),\qquad E_pq=\sum_TW_B(T).            \tag{12}
\]

At `r=1`, let `W_0` denote (9), (11) with `A_i=1+t_i`.
The corresponding mean matrix is `R`, whose Perron root is one.  Its
extinction is certain.  This can be seen without invoking a branching-process
classification theorem: if a nonzero survival vector `z>=0` existed, then

\[
 z=(1-z)Rz.
\]

Since `p` is invariant on the left for `R`, summing against `p` would give

\[
 E_pz=E_pRz-E_p(zRz)=E_pz-E_p(zRz),
\]

which is impossible by irreducibility.  Consequently

\[
                         \sum_TW_0(T)=1.                \tag{13}
\]

Because `E_p s=1-E_ph`, the diffuse support inequality

\[
 E_ps\leq cE_pq
\]

is exactly (1).

## 4. What adjacent rerooting actually does

Take two adjacent vertices of types `i,j` and move the plant/root across
their edge, transporting the plane order in the standard way.  Only that
edge reverses orientation; the old root loses one denominator factor and the
new root gains one.  Equations (4), (9), and (10) give the exact ratios

\[
 {W_D(T^j)\over W_D(T^i)}
 ={a_iA_i\over a_jA_j},                                \tag{14}
\]

\[
 {W_B(T^j)\over W_B(T^i)}
 ={a_jB_i\over a_iB_j}.                                \tag{15}
\]

Thus rerooting changes only one root factor.  It cannot change the unrooted
degree core.  More explicitly, for a fixed rooted typed tree,

\[
 {W_D(T)\over W_B(T)}
 ={1\over a_{\rm root}}
  \prod_v
  \left\{ {a_vB_v\over t_vA_v}
           \left({B_v\over a_vA_v}\right)^{d_v}
  \right\}.                                           \tag{16}
\]

The powers `d_v` in (16) are the obstruction.  Moving the root transfers one
such factor between the two endpoints of the rerooting path, as
(14)--(15) record, but it preserves the unrooted degree profile.  Identity
(2) controls `A_vB_v`; it supplies no one-sided control of the degree base
`B_v/(a_vA_v)`.

## 5. A symbolic star obstruction

The failure is already exact on a two-type reversible system.  Fix `k>0` and
take

\[
 P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \pi=(1/2,1/2),\qquad
 a=\left({2\over1+k},{2k\over1+k}\right).              \tag{17}
\]

Then

\[
 t=(k,k^{-1}),\qquad
 R=\begin{pmatrix}0&k\\k^{-1}&0\end{pmatrix}.          \tag{18}
\]

Let `S_d` be the plane star rooted at its type-1 center, with `d` type-2
leaves.  Put

\[
 A_1=1+rk,\qquad B_1=k+r.
\]

The other two denominators are `A_2=B_1/k` and `B_2=A_1/k`.
Equations (9)--(10) give

\[
 W_D(S_d)={p_1r^dk^d\over A_1^{d+1}A_2^d},             \tag{19}
\]

\[
 W_B(S_d)={p_1kr^d\over B_1^{d+1}A_1^d},               \tag{20}
\]

while the critical dB weight is

\[
 W_0(S_d)={p_1k^{2d}\over(1+k)^{2d+1}}.                \tag{21}
\]

Define

\[
 \lambda={r(1+k)^2\over(1+rk)(k+r)}.                   \tag{22}
\]

Then the exact ratios are

\[
 {W_D(S_d)\over W_0(S_d)}
 ={1+k\over1+rk}\lambda^d,                             \tag{23}
\]

\[
 {W_B(S_d)\over W_0(S_d)}
 ={k(1+k)\over k+r}\left({\lambda\over k^2}\right)^d, \tag{24}
\]

and

\[
 {W_D(S_d)\over W_B(S_d)}
 =k^{2d-1}{k+r\over1+rk}.                              \tag{25}
\]

Now (2), evaluated at `t=k`, says exactly

\[
 (1+rk)(k+r)=r(1+k)^2+c^2k.
\]

Therefore

\[
 0<\lambda=1-{c^2k\over(1+rk)(k+r)}<1.                \tag{26}
\]

If `k>1`, then also `\lambda/k^2<1`.  It follows from
(23)--(24) that

\[
 {W_D(S_d)+cW_B(S_d)\over W_0(S_d)}\longrightarrow0
 \qquad(d\to\infty).                                  \tag{27}
\]

Allowing every possible rerooting does not help.  By (14)--(15), a leaf
reroot multiplies the dB ratio by `A_1/B_1` and the Bd ratio by
`k^2B_1/A_1`; these factors do not depend on `d`.  There are only `O(d)`
root corners.  Hence the ratio of the *total* `W_D+cW_B` capacity of the
whole rerooting class to its `W_0` mass still tends to zero.

This proves the promised obstruction: no mass injection from the critical
tree probability (13) into the two extinction-tree terms in (1) can preserve
the underlying unrooted typed plane tree and use rerooting alone.  Such an
injection would require the target capacity of every rerooting class to be at
least its source mass, contradicted by (27).

Equation (25) separately shows why there is no universal dB-versus-Bd tree
ordering.  The degree factor can be exponentially large or exponentially
small (replace `k` by `1/k`), while rerooting changes it only by a bounded
root factor.

## 6. Why the stronger endpoint is not a finite-extinction-tree comparison

The stronger desired inequality is

\[
 E_ps\leq E_p\mathcal F_r(cq),
 \qquad \mathcal F_r(cq)={rcRq\over1+rcRq}.             \tag{28}
\]

Put

\[
 h_{1,i}={1\over1+rc(Rq)_i}.
\]

Then (28) is `E_ph>=E_ph_1`.  Under the dB offspring law, `h_{1,i}` is the
probability that no child is both independently `c`-marked and the root of a
finite Bd tree.  Its exact positive star expansion is

\[
 h_{1,i}
 =\sum_{d\geq0}\ \sum_{j_1,\ldots,j_d}
   {r^d\over A_i^{d+1}}
   \prod_{\ell=1}^d R_{ij_\ell}(1-cq_{j_\ell}).        \tag{29}
\]

For the fitness interval in question, `0<c<1`, and

\[
 1-cq=(1-c)+c(1-q)=(2-r)+c(1-q).                       \tag{30}
\]

Thus the positive probabilistic expansion (29) contains an unmarked atom
and a marked **Bd-survival** event.  If instead one substitutes the finite
Bd tree expansion of `q` directly into `1-cq`, the result is signed.  The
strong endpoint therefore does not place both sides on a common positive
space of finite extinction trees.  A proof of (28) by branching objects must
retain infinite survival configurations or introduce a different nonlocal
positive representation.

## 7. Consequence for the proof program

The exact branching interpretation is useful, but the straightforward
extinction-tree rerooting route is closed:

1. the support target has a critical-tree source representation, but pure
   rerooting has exponentially insufficient capacity on one unrooted class;
2. the stronger endpoint target is not a positive finite-extinction-tree
   comparison at all; and
3. the normalization identity (2) quantifies the star contraction rather
   than canceling the degree factors.

A viable tree proof would have to change unrooted shapes, or couple a dB
infinite spine directly to the marked finite-Bd event in (28).  Merely adding
more root choices or exhausting finite tree shapes cannot address the
obstruction.

## 8. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_branching_tree_reroot_obstruction/verify_tree_reroot.py
```
