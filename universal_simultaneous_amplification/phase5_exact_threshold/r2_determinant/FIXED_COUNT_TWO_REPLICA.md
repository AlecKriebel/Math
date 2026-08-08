# The fixed-count two-replica coefficient

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note isolates and partially proves the first open complete-ray
Bernstein coefficient in the transient fitness-two route.

The following statements are **PROVED**.

1. The coefficient with exactly two actual-coloured updates is a triangular
   sum of two-perturbation packets.
2. Every packet in the antisymmetric balanced sector is strictly positive,
   for every population order and every pair of time lags.
3. On three vertices, the standard-sector triangular sum is strictly
   positive at every time.  Together with item 2, this proves the complete
   two-colour coefficient for every directed three-vertex kernel.
4. On four vertices, every standard-sector fixed-total-lag diagonal is
   strictly positive at every time.  The symmetric sector remains open.

The exact two-channel reductions for the remaining standard and symmetric
balanced sectors are also derived below.  Their diagonal signs were checked
exactly for `4<=n<=31` and total lag at most 100.  This is **EXACT FINITE
COMPUTATION**, not a universal proof.  The all-order signs in those two
sectors remain **OPEN**.

## 1. From fixed-colour words to a triangular packet

Retain the active state space, complete kernel `K_0`, stationary row
`nu_0`, and reward `H` from `TRANSIENT_BASELINE_FLOOR.md`.  For a loopless
row-stochastic kernel `P`, put

\[
 \Delta=K_P-K_0,
 \qquad K_\alpha=K_0+\alpha\Delta .                 \tag{1}
\]

Let `b_(t,j)` be the degree-`t` Bernstein control of
`nu_0 K_alpha^t H-a_0`.  The rank projection identity
`S Delta S=0` gives `b_(t,0)=b_(t,1)=0`.  Expanding the two actual-coloured
factors as `K_P=K_0+Delta` therefore gives

\[
 \boxed{
 b_{t,2}={1\over\binom t2}
 \sum_{\ell,m\ge0\atop \ell+m\le t-2}Q_{\ell,m},
 \qquad
 Q_{\ell,m}=\nu_0\Delta K_0^\ell\Delta R^mH .}       \tag{2}
\]

Here the omitted prefix has length `t-2-ell-m` and disappears because
`nu_0 K_0=nu_0`; the suffix is radial, so `K_0^mH=R^mH`.  Equation `(2)` is
independently checked against the full active chain in the verifier.

For fixed total lag `L`, define

\[
 q_L=\sum_{\ell+m=L}Q_{\ell,m},\qquad
 S_L=\sum_{j=0}^Lq_j.                               \tag{3}
\]

Then `binom(t,2)b_(t,2)=S_(t-2)`.  Individual `Q_(ell,m)` and even an
individual diagonal `q_L` can be negative; only the cumulative packet in
`(2)` is required.

## 2. Irreducible quadratic sectors

Write `delta=P-P_0`.  It is a row-zero off-diagonal matrix.  Because `(2)`
is invariant under simultaneous relabelling, its quadratic form splits
orthogonally into the following `S_n` sectors:

- the standard sector `delta=E(s)`, where `sum_i s_i=0` and

  \[
  E(s)_{ij}={s_i+(n-1)s_j\over n(n-2)}\quad(i\ne j);               \tag{4}
  \]

- the symmetric row-zero sector;
- the antisymmetric row-zero sector.

For `n=3`, only the standard and antisymmetric sectors occur.  Thus it is
enough to certify one scalar sign in each sector.  All formulas below come
directly from the two active moves, not from a fixation approximation.

Put `N=n-1` and

\[
 \pi_k={\binom{N-1}{k-1}\over2^{N-1}},\qquad1\le k\le N.          \tag{5}
\]

The complete rank chain is

\[
 R_{k,k+1}={N-k\over2N},\quad
 R_{k,k-1}={k-1\over2N}.                           \tag{6}
\]

If `h` is radial, write `d_k=h_k-h_(k+1)` and set `d_N=0`.

## 3. All-time antisymmetric theorem

### Theorem 1

For every `n>=3`, every nonzero antisymmetric row-zero `delta`, and every
`ell,m>=0`,

\[
 \boxed{Q_{\ell,m}(\delta)>0.}                     \tag{7}
\]

Consequently the antisymmetric contribution to `b_(t,2)` is strictly
positive for every `t>=2`.

### Proof

For an antisymmetric direction put

\[
 x(B,v)=\sum_{i\in B}\delta_{vi}.                  \tag{8}
\]

Direct expansion gives, for radial `h`,

\[
 \Delta h(B,v)={d_k\over2}x(B,v).                  \tag{9}
\]

If `D^(m)_k=(R^mH)_k-(R^mH)_(k+1)`, then

\[
 D^{(m+1)}_k={1\over2}D^{(m)}_k
 +{N-k-1\over2N}D^{(m)}_{k+1}
 +{k-1\over2N}D^{(m)}_{k-1}.                       \tag{10}
\]

Initially `D^(0)_k=1/[k(k+1)]`.  Positivity is immediate from `(10)`.  If
`e_k=D_k-D_(k+1)`, subtraction of adjacent equations gives

\[
 e'_k={k-1\over2N}e_{k-1}
      +{N-1\over2N}e_k
      +{N-k-2\over2N}e_{k+1},                     \tag{11}
\]

with the absent boundary terms deleted.  Hence every `D^(m)` is positive
and decreasing.

The complete active kernel preserves the one-feature form:

\[
 K_0\{r_kx(B,v)\}=(Ar)_kx(B,v),\qquad
 (Ar)_k={kr_k+(N-k-1)r_{k+1}\over2N}.              \tag{12}
\]

If `r` is positive and decreasing, so is `Ar`, because

\[
 2N\{(Ar)_k-(Ar)_{k+1}\}
 =k(r_k-r_{k+1})+(N-k-2)(r_{k+1}-r_{k+2})          \tag{13}
\]

away from the immediate upper boundary, which is positive directly.  Thus
`r=(1/2)A^ell D^(m)` is positive and decreasing.

Let `T=sum_(i,j)delta_ij^2`.  Sampling without replacement and expanding
the second perturbation gives

\[
\begin{aligned}
 E_k[\Delta(r_kx)]={T\over2nN}\Big[&
 {k(N-k)\over N-1}(r_k-r_{k+1})+(N-k)r_{k+1}\\
 &+{(k-1)(N-k+1)\over N-1}(r_{k-1}-r_k)
 +(N-k+1)r_k\Big].                                \tag{14}
\end{aligned}
\]

Every term is nonnegative and the last is positive for some rank whenever
`T>0`.  Averaging `(14)` with `(5)` proves `(7)`.  QED.

## 4. The three-vertex standard sector

For `n=3`, choose the canonical standard vector `s=(2,-1,-1)` in `(4)` and
divide by `||s||^2`.  An exact nine-state resolvent calculation gives the
diagonal generating function

\[
 \boxed{
 F(z)=\sum_{L\ge0}q_Lz^L
 ={2(z+8)\over9(z^3+8z^2-40z+64)}.}                \tag{15}
\]

Let `S_L=sum_(j<=L)q_j`.  Since `F(1)=2/33`, write

\[
 S_L={2\over33}+r_L.                               \tag{16}
\]

The residual obeys

\[
 r_L={5\over8}r_{L-1}-{1\over8}r_{L-2}
                         -{1\over64}r_{L-3}.       \tag{17}
\]

On triples `(r_L,r_(L-1),r_(L-2))`, use the weighted maximum norm

\[
 \|(x_0,x_1,x_2)\|
 =\max\{|x_0|,{13\over16}|x_1|,
                    ({13\over16})^2|x_2|\}.        \tag{18}
\]

The companion map contracts this norm by at most `13/16`, because

\[
 {5\over8}+{2\over13}+{4\over169}
 ={1085\over1352}<{13\over16}.                    \tag{19}
\]

At `L=2`, direct calculation gives

\[
 \|(r_2,r_1,r_0)\|={2197\over101376}<{2\over33}.  \tag{20}
\]

The cases `L=0,1` are positive directly, and `(18)`--`(20)` imply
`|r_L|<2/33` thereafter.  Hence `S_L>0` for every `L`.  Combining this with
Theorem 1 and the two-sector decomposition proves:

### Corollary 2

For every directed loopless three-vertex kernel `P` distinct from the
complete kernel and every `t>=2`,

\[
 \boxed{b_{t,2}(P)>0.}                             \tag{21}
\]

## 5. The four-vertex standard boundary case

The simplest pointwise cone suggested by the two-channel recurrence fails
at `n=4`, but the exact diagonal generating function is still tractable:

\[
 F_4(z)=
 {9(4z^5-13z^4-128z^3+807z^2-1809z+1458)\over
 256(z-3)(2z-3)(z^5+z^4-54z^3+297z^2-621z+486)}.                \tag{22a}
\]

Write

\[
 q_m={55\over4032}\left({2\over3}\right)^m+r_m.                 \tag{22b}
\]

The residual satisfies

\[
\begin{aligned}
 r_m={29\over18}r_{m-1}-{28\over27}r_{m-2}
 &+{17\over54}r_{m-3}-{19\over486}r_{m-4}\\
 &-{1\over729}r_{m-5}+{1\over1458}r_{m-6}.        \tag{22c}
\end{aligned}
\]

Let `C` be the companion matrix.  Exact multiplication gives

\[
 \|C^{21}\|_\infty
 ={960357059082763123\over4918301009412067196928}
 <\left({2\over3}\right)^{21}.                    \tag{22d}
\]

Direct exact calculation gives `q_0,...,q_29>0`.  Put
`X_30=(r_30,...,r_25)`.  For every `0<=s<=20`,

\[
 {\|e_1^TC^s\|_1\|X_{30}\|_\infty\over
  (55/4032)(2/3)^{30+s}}<1.                       \tag{22e}
\]

The largest left side occurs at `s=3` and equals

\[
 {13143953338764611150595571035307\over
  128945158113455203437948306456576}<1.            \tag{22f}
\]

Applying `(22d)` block by block proves `q_m>0` for every `m`.  Therefore the
standard contribution to every four-vertex cumulative packet is positive.
The verifier reconstructs both `(22a)` and the contraction certificate.

## 6. Exact two-channel reductions still open

These formulas remove all labelled subsets from the two unresolved sectors.
They are recorded both to make the remaining sign precise and to prevent a
boundary mode from being silently discarded.

### 6.1 Standard sector

Put `u=s_v`, `p=sum_(i in B)s_i`, and write a sector function as
`a_k u+b_k p`.  The complete kernel sends it to `a'_k u+b'_k p`, where

\[
 a'_k={ka_k+(N-k)a_{k+1}-b_{k+1}\over2N},          \tag{22}
\]

and

\[
\begin{aligned}
 b'_k={kb_k+(N-k-1)b_{k+1}\over2N}
 &+{(k-1)a_{k-1}+(N-k+1)a_k\over2kN}\\
 &+{(k-1)^2b_{k-1}+{k(N-k)-(N-k+1)\}b_k\over2kN}.
                                                               \tag{23}
\end{aligned}
\]

The first perturbation of a radial `h` has

\[
 a_k={kd_k\over2n(N-1)},\qquad
 b_k={Nd_k\over2n(N-1)}+{(k-1)d_{k-1}\over2k(N-1)}.             \tag{24}
\]

At rank `N`, the two features are dependent: `p=-u`.  Thus `a_N-b_N`, not
`a_N` or `b_N` separately, is the physical upper-boundary variable.  Any
cone proof that sets this mode to zero is invalid.

The averaged second perturbation collapses to

\[
 {\nu_0\Delta(au+bp)\over||s||^2}
 =\sum_{k=1}^N\pi_k{N-k\over n(N-1)}b_k.           \tag{25}
\]

### 6.2 Symmetric balanced sector

Let `delta=delta^T` have zero row sums and put

\[
 x(B,v)=\sum_{i\in B}\delta_{vi},\qquad
 z(B)=\sum_{w\ne i\in B}\delta_{wi}.              \tag{26}
\]

Write the sector function as `a_kx+b_kz`.  Then

\[
 a'_k={ka_k+(N-k-1)a_{k+1}\over2N}-{b_{k+1}\over N},            \tag{27}
\]

\[
\begin{aligned}
 b'_k={ (k-1)a_{k-1}+(N-k)a_k\over2kN}
 &+{kb_k+(N-k-2)b_{k+1}\over2N}\\
 &+{(k-1)(k-2)b_{k-1}
   +\{k(N-k-1)-2(N-k)\}b_k\over2kN}.              \tag{28}
\end{aligned}
\]

The radial source is

\[
 a_k={d_k\over2},\qquad b_k={d_{k-1}\over2k}.      \tag{29}
\]

Here `a_N=b_1=b_N=0` may be imposed because the corresponding features
vanish identically.  If `T=sum delta_ij^2` and

\[
 r_k=a_k-{2(k-1)\over N-2}b_k,                    \tag{30}
\]

the corrected second-perturbation average is

\[
 {\nu_0\Delta(ax+bz)\over T}
 =\sum_{k=1}^{N-1}\pi_k{N-k\over(N-1)(N+1)}r_k.   \tag{31}
\]

The sign of individual summands in `(31)` changes.  A weighted cumulative
or reflection argument is therefore required.

For either sector, if `W_L` is the pair of feature sequences on the total
lag diagonal, then

\[
 W_L=K_0W_{L-1}+\Delta R^LH,\qquad q_L=\nu_0\Delta W_L.          \tag{32}
\]

Equations `(22)`--`(32)` are the current finite-dimensional theorem target.

## 7. Hostile checks and exact scope

Stronger packetwise positivity is false.  For the symmetric four-vertex
direction with nonzero undirected entries

\[
 \delta_{01}=1,\quad\delta_{02}=-1,\quad
 \delta_{13}=-1,\quad\delta_{23}=1,                \tag{33}
\]

and their transposes, the full active chain gives

\[
 Q_{1,0}=-{1\over36}.                              \tag{34}
\]

The exact verifier also checks the following without floating point:

- `(2)` against a directed rational four-vertex active chain;
- `(15)` from the full nine-state resolvent;
- the antisymmetric cone recurrences through `n=40` and both lags 40;
- every standard and symmetric diagonal `q_L` for `4<=n<=31` and
  `0<=L<=100`.

The last item is finite evidence only.  The surviving bounded lemma is:

\[
 \boxed{S_L^{\rm std}\ge0,\qquad S_L^{\rm sym}\ge0
        \quad\hbox{for every }n,L.}                \tag{35}
\]

A proof of `(35)`, together with Theorem 1, would prove the complete-ray
coefficient `b_(t,2)>=0` for every directed kernel and every time.  It would
be a genuine global two-replica certificate, but it would still not by
itself prove all higher colour counts or the universal transient floor.
