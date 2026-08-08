# The standard sector as a common-pin variation problem

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note gives an exact probabilistic and one-dimensional reduction of the
standard irreducible sector of the fixed-count two-replica coefficient.
It does **not** yet prove the all-order sector sign.

The following statements are **PROVED**.

1. The canonical standard perturbation is a positive scalar multiple of the
   difference between one distinguished pin kernel and the uniform pin
   mixture.
2. The complete active chain is the annealed mixture of the pin active
   chains.
3. The standard two-replica coefficient is a covariance between terminal
   inverse cache rank and the collision count of an iid pin history.
4. After distinguishing one pin, the entire calculation lumps exactly to
   `3N-1` states, where `N=n-1`.
5. The standard coefficient is the binomially weighted curvature at the
   uniform pin frequency of one explicit Bernstein polynomial.
6. Full coefficientwise convexity is false: an exact negative curvature
   control first occurs at `(n,t,c)=(5,21,19)`, while its required binomial
   average is strictly positive.
7. Two weaker sign-regularity statements, and an even weaker positive
   Bernstein-quotient statement, each suffice for the desired standard
   sign.

The sign-regularity and quotient statements are **EXACT FINITE
COMPUTATIONS** on the ranges stated below.  Their all-order forms remain
**OPEN**.

## 1. Pin replacement kernels

Let `V` have order `n=N+1`.  For each `x in V`, define the loopless pin
replacement kernel `Q_x` by

\[
 Q_x(x,j)={1\over N}\quad(j\ne x),\qquad
 Q_x(i,x)=1\quad(i\ne x),                         \tag{1}
\]

with every other entry zero.  Thus the pin itself samples a uniform
ordinary vertex and every ordinary source points deterministically back to
the pin.  Direct row averaging gives

\[
 P_0={1\over n}\sum_{x\in V}Q_x,                  \tag{2}
\]

where `P_0(i,j)=1/N` for `i\ne j` is the complete replacement kernel.
Since the active kernel is linear in the replacement kernel,

\[
 K_0={1\over n}\sum_x L_x,\qquad L_x:=K(Q_x).      \tag{3}
\]

Fix `x`.  Put `s_x=N` and `s_i=-1` for `i\ne x`, and use the standard
sector embedding

\[
 E(s)_{ij}={s_i+Ns_j\over n(N-1)}\quad(i\ne j).   \tag{4}
\]

Entrywise calculation gives the exact scale

\[
 \boxed{Q_x-P_0={N-1\over N}E(s).}                \tag{5}
\]

This scale is important: identifying `Q_x-P_0` literally with `E(s)` would
be wrong.

Let

\[
 A=L_x,\qquad B={1\over N}\sum_{y\ne x}L_y,\qquad
 p_0={1\over n}.                                  \tag{6}
\]

Then

\[
 K(p)=pA+(1-p)B,\qquad K(p_0)=K_0,                \tag{7}
\]

and

\[
 A-K_0=(1-p_0)(A-B).                              \tag{8}
\]

All identities `(2)`--`(8)` are checked independently on the labelled
active chain in `verify_standard_pin_bernstein.py`.

## 2. Pin histories and the collision statistic

Let `X_1,...,X_t` be iid uniform pins and, conditional on this history,
apply the active operators `L_(X_1),...,L_(X_t)`.  The complete-chain reward
is

\[
 a_0=\nu_0K_0^tH
 =E\{\nu_0L_{X_1}\cdots L_{X_t}H\},               \tag{9}
\]

where

\[
 H(B,v)={1\over |B|},\qquad
 \nu_0(B,v)={|B|\over nN2^{N-1}}.                \tag{10}
\]

Choose an unordered pair of times uniformly.  Replacing their two
independent pins by one common uniform pin has Radon--Nikodym increment

\[
 n\mathbf1\{X_a=X_b\}-1.                          \tag{11}
\]

Averaging over the pair gives

\[
 Z_t=\sum_{a<b}\{n\mathbf1(X_a=X_b)-1\}
 ={n\over2}\sum_x\left(C_x-{t\over n}\right)^2
   -{t(n-1)\over2},                               \tag{12}
\]

where `C_x` is the pin count.  Consequently, up to the explicit positive
sector scale in `(5)`, the standard fixed-count coefficient is

\[
 \boxed{
 {1\over\binom t2}E\left[H(Y_t)Z_t\right].}       \tag{13}
\]

Thus the missing sign is a collision/dispersion covariance in an iid pin
environment.  A prescribed pair of times need not contribute positively;
the uniform pair average in `(13)` is essential.

## 3. Exact `3N-1` quotient

Under the stabilizer of `x`, an active state `(B,v)` has one of three
types:

\[
 \begin{array}{c|c|c}
 \text{type}&\text{condition}&\text{ranks}\\ \hline
 X_k&v=x&1\le k\le N,\\
 I_k&v\ne x,\ x\in B&1\le k\le N,\\
 O_k&v\ne x,\ x\notin B&1\le k<N.
 \end{array}                                      \tag{14}
\]

This gives `3N-1` orbits.  More generally let an ordinary source hit `x`
with probability `alpha` and each other ordinary target with probability

\[
 \beta={1-\alpha\over N-1};                       \tag{15}
\]

the row at `x` is uniform on the ordinary vertices.  The distinguished pin
has `(alpha,beta)=(1,0)`, while the other-pin average has

\[
 (\alpha,\beta)=\left({1\over N^2},{N+1\over N^2}\right).       \tag{16}
\]

The nonzero quotient transitions are as follows; absent boundary terms are
deleted.  Every displayed mass already includes the fair active-chain
factor `1/2`.

\[
\begin{aligned}
 X_k\to{}&X_k:{k\over2N},\quad
 X_{k+1}:{N-k\over2N},\quad I_k:{\alpha\over2},\\
 &O_{k-1}:{(k-1)\beta\over2},\quad
 O_k:{(N-k)\beta\over2};                          \tag{17}
\end{aligned}
\]

\[
\begin{aligned}
 I_k\to{}&I_k:{\alpha+(k-1)\beta\over2},\quad
 I_{k+1}:{(N-k)\beta\over2},\\
 &X_{k-1}:{k-1\over2kN},\quad
 X_k:{N-k+1\over2kN},\\
 &I_{k-1}:{k-1\over2k}\{\alpha+(k-2)\beta\},\\
 &I_k:{(k-1)(N-k+1)\beta\over2k};                \tag{18}
\end{aligned}
\]

\[
\begin{aligned}
 O_k\to{}&I_{k+1}:{\alpha\over2},\quad
 I_k:{\alpha\over2},\quad
 O_{k+1}:{(N-k-1)\beta\over2},\\
 &O_{k-1}:{(k-1)\beta\over2},\quad
 O_k:{N\beta\over2}.                             \tag{19}
\end{aligned}
\]

Put

\[
 \pi_k={\binom{N-1}{k-1}\over2^{N-1}}.           \tag{20}
\]

The complete initial masses and reward on these orbits are

\[
 \nu_0(X_k)={\pi_k\over N+1},\quad
 \nu_0(I_k)={k\pi_k\over N+1},\quad
 \nu_0(O_k)={(N-k)\pi_k\over N+1},\qquad H={1\over k}.          \tag{21}
\]

Equations `(17)`--`(21)` prove exact lumpability: the aggregate transition
mass depends only on the displayed type and rank.  The independent verifier
also compares every quotient row with every labelled row for `3<=n<=5`.

## 4. Conditional pin-count controls

Define

\[
 \Phi_t(p)=\nu_0K(p)^tH.                           \tag{22}
\]

Let `psi_(t,c)` be the reward conditional on exactly `c` distinguished
pins among `t` uniformly ordered pin times.  Then

\[
 \Phi_t(p)=\sum_{c=0}^t\binom tc
 p^c(1-p)^{t-c}\psi_{t,c}.                        \tag{23}
\]

The vector controls obey the exact noncommutative recursion

\[
 V_{t,c}={t-c\over t}BV_{t-1,c}
          +{c\over t}AV_{t-1,c-1},\qquad
 \psi_{t,c}=\nu_0V_{t,c}.                         \tag{24}
\]

Writing

\[
 d_c=\psi_{t,c+1}-\psi_{t,c},\qquad
 u_c=d_{c+1}-d_c,                                 \tag{25}
\]

Bernstein differentiation gives

\[
 {\Phi_t'(p)\over t}
 =E\{d_C\},\quad C\sim\operatorname{Bin}(t-1,p),               \tag{26}
\]

and

\[
 {\Phi_t''(p)\over t(t-1)}
 =E\{u_C\},\quad C\sim\operatorname{Bin}(t-2,p).              \tag{27}
\]

Full label symmetry makes the uniform pin law stationary under every
zero-sum pin perturbation, hence

\[
 \boxed{\Phi_t'(p_0)=0.}                          \tag{28}
\]

By `(8)`, the direct standard fixed-count coefficient in direction
`Q_x-P_0` is exactly

\[
 \boxed{
 b^{\rm std}_{t,2}=(1-p_0)^2
 E_{C\sim\operatorname{Bin}(t-2,p_0)}u_C.}        \tag{29}
\]

The verifier checks `(29)` against a separate fixed-two-colour active-chain
recursion, not against another evaluation of `(27)`.

There is also a degree-two Krawtchouk form.  If
`C~Bin(t,p_0)` and

\[
 K_2(C)=(C-tp_0)^2-(1-2p_0)(C-tp_0)-tp_0(1-p_0),                \tag{30}
\]

then

\[
 E\{\psi_{t,C}K_2(C)\}
 =t(t-1)p_0^2(1-p_0)^2E\{u_{C'}\},               \tag{31}
\]

where `C'~Bin(t-2,p_0)`.

## 5. Exact failure of full convexity

Pointwise `u_c>=0` is false.  The first failure in the exact quotient audit
is

\[
 (n,t,c)=(5,21,19),
\]

where

\[
 \boxed{
 u_{19}=-{6721646494761620342351\over
 10038636664090908488047263744}<0.}               \tag{32}
\]

Nevertheless the required binomial mean at `p_0=1/5` is

\[
 \boxed{
 {9895299125872105432076506664291860618105\over
 2970256355669619957016117970498126685929472}>0.} \tag{33}
\]

Thus global coefficientwise convexity is **EXACTLY REFUTED**, while the
standard coefficient itself remains positive on the witness.

## 6. Three surviving sufficient signs

The following are progressively weaker routes to `(29)`.

### 6.1 First-difference one crossing

If the nonzero signs of `d_0,...,d_(t-1)` occur in the order

\[
 -\ \cdots\ -\ +\ \cdots\ +,                     \tag{34}
\]

then `(28)` and the binomial score identity give

\[
 \Phi_t''(p_0)
 ={t\over p_0(1-p_0)}
 E\{(C-(t-1)p_0)d_C\}>0.                          \tag{35}
\]

Indeed choose a threshold `a` between the two sign blocks.  Since
`E d_C=0`, the expectation in `(35)` equals
`E[(C-a)d_C]`, whose summands are nonnegative and not all zero.

### 6.2 Curvature one crossing

Suppose the nonzero signs of `u_0,...,u_(t-2)` occur in the order

\[
 +\ \cdots\ +\ -\ \cdots\ -,                     \tag{36}
\]

and the terminal slope `d_(t-1)` is positive.  Bernstein
variation-diminishing implies that `Phi_t''` has at most one sign change,
from positive to negative.  If `Phi_t''(p_0)<=0`, then `Phi_t'` is
nonincreasing on `[p_0,1]`, contradicting `(28)` and
`Phi_t'(1)=td_(t-1)>0`.  Hence `(29)` is strictly positive.

### 6.3 Positive Bernstein quotient

Put `m=t-1`.  Equation `(28)` gives the exact factorization

\[
 {\Phi_t'(p)\over t}=(p-p_0)Q_t(p).                \tag{37}
\]

Write the degree-`m-1` Bernstein expansion

\[
 Q_t(p)=\sum_{c=0}^{m-1}\binom{m-1}{c}
 q_c p^c(1-p)^{m-1-c}.                            \tag{38}
\]

Coefficient comparison in `(37)` gives

\[
 \boxed{
 d_c=(1-p_0){c\over m}q_{c-1}
       -p_0{m-c\over m}q_c,}                     \tag{39}
\]

with `q_(-1)=q_m=0`.  In particular, `q_c>=0` for every `c` proves
`Q_t(p)>=0` on `[0,1]`, so the uniform pin frequency is a global minimum
along this ray and `(29)` follows.

The quotient criterion is weaker than `(34)`.  If

\[
 w_c=\binom mc p_0^c(1-p_0)^{m-c},\qquad
 \widetilde w_c=\binom{m-1}c p_0^c(1-p_0)^{m-1-c},              \tag{40}
\]

then `(39)` telescopes to

\[
 \boxed{
 q_k=-{\sum_{c=0}^k w_cd_c\over
 p_0(1-p_0)\widetilde w_k}.}                     \tag{41}
\]

Thus quotient positivity asks only that every lower partial binomial mean
of the first differences be nonpositive; it does not ask their signs to be
ordered pointwise.

## 7. A structured operator-pencil clue

The quotient operators have an unexpectedly simple generalized spectrum.
Exact symbolic calculations for `2<=N<=7` give

\[
 \det(A-zB)=C_N z^{N-1}(z-1)^{N+1}
 \prod_{j=1}^{N-1}\left(
 [N^2-(N+1)j]z-N^2\right),                        \tag{42}
\]

with `C_N\ne 0`.  The roots and right generalized eigenvectors admit the
following all-`N` formulas, directly checkable from `(17)`--`(19)`:

* eigenvalue `0`: the `N-1` coordinate functions supported on `O_k`;
* eigenvalue `1`: the `N` coordinate functions supported on `X_k`, together
  with the function equal to one on every `I/O` state and zero on `X`;
* for `1<=j<N`,

  \[
  \lambda_j={N^2\over N^2-(N+1)j},                \tag{43}
  \]

  with

  \[
  f_j(X_k)=0,\qquad
  f_j(I_k)=\binom{N-k}{j},\qquad
  f_j(O_k)=\binom{N-k-1}{j}.                      \tag{44}
  \]

More precisely, if `K_alpha` denotes `(17)`--`(19)`, then elementary
binomial identities give

\[
 K_\alpha f_j={N-j-1+j\alpha\over2(N-1)}h_j,      \tag{45}
\]

for a vector `h_j` independent of `alpha`.  Taking `alpha=1` and
`alpha=1/N^2` yields `Af_j=lambda_jBf_j`.

The vectors in `(44)`, the `O` coordinates, and the eigenvalue-one vectors
are linearly independent: modulo the `O` coordinates, their `I` components
are the triangular binomial basis of degrees `0,...,N-1`.  What is not yet
proved in this note is the all-`N` nonvanishing leading factor in `(42)` or
a variation-diminishing theorem connecting this generalized spectrum to
`(34)`--`(41)`.  The ordered positive values `(43)` strongly suggest a
Krawtchouk/oscillatory-pencil proof, but spectrum alone is insufficient
because `A` and `B` do not commute.

## 8. Exact finite scope and open lemma

The two independent verifiers establish the following without floating
point:

* the scales `(5)` and `(8)` and the pin mixture `(3)`;
* the binomial identity `(29)` against a separate fixed-two-colour
  recursion;
* the exact counterexample `(32)` and positive mean `(33)`;
* exact quotient lumpability against every labelled row for `3<=n<=5`;
* for every `3<=n<=8` and `2<=t<=50`, all 294 order/time pairs satisfy
  `(34)`, `(36)`, positive terminal slope, and positive weighted curvature;
* the quotient coefficients in `(38)` are strictly positive on the same
  exact corpus.

These finite statements are evidence, not a universal proof.  The cleanest
remaining standard-sector lemma is

\[
 \boxed{q_c\ge0\quad(0\le c\le t-2, n\ge3, t\ge2).}           \tag{46}
\]

Any proof of `(46)`, or either stronger sign-regularity statement, proves
the standard fixed-count two-replica sector for every population order and
every time.  It does not by itself prove the symmetric sector or the full
higher-colour transient floor.
