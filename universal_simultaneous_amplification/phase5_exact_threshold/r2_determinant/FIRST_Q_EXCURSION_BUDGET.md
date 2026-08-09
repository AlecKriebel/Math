# The first marked-cache excursion: an exact budget and a renewal obstruction

Date: 2026-08-08 (America/Los_Angeles)

## Status

This note isolates what can and cannot be obtained by pairing the first
two-label excursion in the standard sector.  It is deliberately narrower
than `STANDARD_MARKED_CACHE_HAUSDORFF.md`.

The following statements are **PROVED**.

1. The antisymmetric two-label quotient has the exact three-channel block
   form displayed below.
2. From the stationary binomial source, the total mass of one visit to the
   bad channel has an explicit supersolution.  It pays both a completed bad
   excursion and an excursion that is stopped in the bad channel, for every
   Hausdorff rank atom.
3. The completed first-excursion row is not a nonnegative mixture of the
   pure good-prefix rows.  This already fails for `N=3`, and an exact
   separating vector excludes a mixture using prefixes of *any* length.
4. Replacing every completed excursion by the collapsed signed kernel
   `S-E` is also insufficient: at `N=3`, the eleventh power has a negative
   coordinate.

Thus the one-excursion budget is rigorous, but an all-reentry reflection
still needs an additional debt/marking state.  Nothing here claims that the
full all-order marked-cache inequality has been proved.

## 1. The signed two-label quotient

Put `n=N+1`, and distinguish labels `x` and `y`.  The positive orientation
has three kinds of active state:

\[
\begin{array}{c|l|c}
P_k&v=x,\quad x,y\notin B&1\le k<N,\\
Q_k&v=x,\quad y\in B&1\le k\le N,\\
R_k&v\notin\{x,y\},\quad x\in B,\ y\notin B&1\le k<N.
\end{array}                                                     \tag{1}
\]

The negative orientation is obtained by exchanging `x` and `y`.  Quotient
entries below are positive-orientation transition mass minus the mass into
the exchanged state.  Terms whose rank is outside its physical range are
deleted.

For `1<=k<N`,

\[
 P_k\longrightarrow
 {k\over2N}P_k+{N-k-1\over2N}P_{k+1}+{1\over2N}Q_{k+1}.       \tag{2}
\]

For `1<=k<=N`,

\[
\begin{aligned}
 Q_k\longrightarrow{}&{k^2-1\over2kN}Q_k+{N-k\over2N}Q_{k+1}\\
 &-{k-1\over2kN}P_{k-1}-{N-k\over2kN}P_k\\
 &-{(k-1)^2\over2kN}R_{k-1}
   -{(k-1)(N-k)\over2kN}R_k .                    \tag{3}
\end{aligned}
\]

For `1<=k<N`,

\[
\begin{aligned}
 R_k\longrightarrow{}&
 \left\{{k\over2N}+{(k-1)(N-k)\over2kN}\right\}R_k
 +{N-k-1\over2N}R_{k+1}+{(k-1)^2\over2kN}R_{k-1}\\
 &+{1\over2kN}Q_k+{k-1\over2kN}P_{k-1}
   +{N-k\over2kN}P_k .                           \tag{4}
\end{aligned}
\]

Order the good states as `S=(P_1,...,P_(N-1),R_1,...,R_(N-1))` and the bad
states as `Q=(Q_1,...,Q_N)`.  Equations `(2)--(4)` have block form

\[
 H=\begin{pmatrix}S&C\\-D&Q\end{pmatrix},          \tag{5}
\]

where every entry of `S,C,D,Q` is nonnegative.  The stationary
antisymmetric source is supported on the `R` states:

\[
 s(R_k)=c_k:={\binom{N-2}{k-1}\over2^{N-2}},\qquad s(P_k)=0.  \tag{6}
\]

The bad block `Q` is upper bidiagonal.  A completed bad excursion has the
nonnegative kernel

\[
 E=C(I-Q)^{-1}D.                                   \tag{7}
\]

Its minus sign in the signed chain comes from the single `Q -> S` crossing.

## 2. Exact one-excursion supersolution

Let

\[
 e=sC,\qquad v=e(I-Q)^{-1}.                       \tag{8}
\]

Thus `v_k` is the total occupation mass in `Q_k` during the first bad
excursion, after summing over every possible number of `Q`-holds.  Directly
from `(4)`,

\[
 e_k={c_k\over2kN}\quad(k<N),\qquad e_N=0.         \tag{9}
\]

Define, for `k<N`,

\[
 w_k={c_k\over2k(N-k)}.                            \tag{10}
\]

Since `Q` is nonnegative, upper bidiagonal, and has diagonal strictly below
one, `(I-Q)^{-1}` is nonnegative.  Exact binomial cancellation gives

\[
 [w(I-Q)-e]_1={c_1\over2N(N-1)},                  \tag{11a}
\]

and, for `2<=k<N`,

\[
 [w(I-Q)-e]_k={c_k\over4Nk^2(N-k)}.               \tag{11b}
\]

Applying the positive inverse of the leading `(N-1)`-by-`(N-1)` block
therefore proves

\[
 \boxed{0\le v_k\le w_k\le c_k\qquad(1\le k<N).} \tag{12}
\]

At the physical top boundary the last coordinate equation is

\[
 \boxed{v_N={N\over N^2+1}v_{N-1}.}               \tag{13}
\]

This boundary term cannot be set to zero.

## 3. What the budget pays

First consider a completed excursion.  The coefficients in `(3)` show that
for `k<N-1` the contributions of `v_k,v_(k+1)` to `(vD)(P_k)` and
`(vD)(R_k)` are termwise bounded by the corresponding contributions of
`c_k,c_(k+1)` to `(sS)(P_k)` and `(sS)(R_k)`.  At `k=N-1`, equations
`(12)--(13)` give, with `c=c_(N-1)` and `v=v_(N-1)`,

\[
\begin{aligned}
 (vD)(P_{N-1})
 &= {v\over2N(N-1)}
    \left\{1+{(N-1)^2\over N^2+1}\right\}
 \le {c\over2N(N-1)}=(sS)(P_{N-1}),\\
 (vD)(R_{N-1})
 &\le {c(N-2)\over2N(N-1)}
      +{c(N-1)\over4N(N^2+1)}
 \le (sS)(R_{N-1}).                              \tag{14}
\end{aligned}
\]

Consequently

\[
 \boxed{sE=vD\le sS\quad\hbox{entrywise}.}         \tag{15}
\]

There is also an exact terminal budget.  Up to a common positive scale, the
standard Hausdorff atom at cut rank `j` has good-channel reward

\[
 g^S_j(P_j)=j,\qquad g^S_j(R_j)=N,\qquad
 g^S_j(R_{j+1})={j(N+1)\over j+1},                 \tag{16}
\]

and absolute bad-channel reward

\[
 g^Q_j(Q_j)=N-j,\qquad
 g^Q_j(Q_{j+1})={j(N+1)\over j+1}.                 \tag{17}
\]

For `j<N-1`, `(12)` bounds these two terms separately.  For `j=N-1`, the
two bad terms combine, by `(13)`, to

\[
 v_{N-1}+{N^2-1\over N}v_N
 ={2N^2\over N^2+1}v_{N-1}
 \le {N^2\over(N-1)(N^2+1)}c_{N-1}
 \le Nc_{N-1}.                                    \tag{18}
\]

Hence every atom satisfies

\[
 \boxed{v g^Q_j\le s g^S_j.}                     \tag{19}
\]

Equations `(15)` and `(19)` are the rigorous first-excursion certificate.
They extend by nonnegative mixing to the corresponding Hausdorff rewards.
They do **not** allocate the same positive mass consistently after repeated
re-entry.

## 4. Exact obstruction to pure-prefix renewal

It is tempting to hope that `sE` is a nonnegative mixture of the pure
good-prefix rows `sS^h`.  This is false even if prefixes of every length are
allowed.

For `N=3`, in the coordinate order `(P_1,P_2,R_1,R_2)`,

\[
 S=\begin{pmatrix}
 1/6&1/6&0&0\\
 0&1/3&0&0\\
 1/3&0&1/6&1/6\\
 1/12&1/12&1/12&5/12
 \end{pmatrix},\qquad
 s=(0,0,1/2,1/2),                                 \tag{20}
\]

and exact block elimination gives

\[
 sE={1\over648}(23,7,5,9).                        \tag{21}
\]

Take

\[
 y=(-1,1,1,1)^T.                                  \tag{22}
\]

Then

\[
 sy=1,\qquad Sy=(0,1/3,0,1/2)^T\ge0,             \tag{23}
\]

so `(sS^h)y>=0` for `h=0`, and also for every `h>=1` because `S` and
`sS^(h-1)` are nonnegative.  On the other hand,

\[
 (sE)y={-23+7+5+9\over648}=-{1\over324}<0.         \tag{24}
\]

The separating functional `(22)` proves

\[
 \boxed{sE\notin\operatorname{cone}\{sS^h:h\ge0\}.}          \tag{25}
\]

Thus a first-excursion reflection cannot be iterated merely by replacing
the excursion law with a mixture of fresh pure prefixes.

A second natural collapse also fails.  Put `M=S-E`.  Exact arithmetic at
`N=3` gives nonnegative rows `sM^m` for `0<=m<=10`, but

\[
 (sM^{11})(R_2)=
 -{2711557269637646196135713
 \over1094189891315123592090000000000}<0.          \tag{26}
\]

So repeated use of the time-collapsed kernel is not the missing renewal
argument either.

## 5. Remaining all-reentry problem

The first-excursion inequalities `(15)` and `(19)` survive exact finite
screens after arbitrary pure `S` prefixes, but that stronger prefix claim
has not been proved for all `N` and all prefix lengths.  More importantly,
even such a rowwise inequality would not by itself prevent two different
bad-excursion histories from spending the same positive prefix mass.

The unresolved step is therefore an all-reentry accounting theorem: either
a ballot/reflection rule with a unique positive partner, or an augmented
positive lift carrying an explicit excursion-debt state.  Equations
`(24)--(26)` show why the debt state cannot be discarded.

The independent verifier reconstructs the labelled active chain, checks
the quotient `(2)--(5)`, verifies `(11)--(19)` over exact rational
instances, and reproduces both exact obstructions `(24)` and `(26)`.
