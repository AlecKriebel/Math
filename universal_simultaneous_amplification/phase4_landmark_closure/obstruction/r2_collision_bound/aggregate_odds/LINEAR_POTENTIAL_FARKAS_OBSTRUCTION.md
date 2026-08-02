# Exact Farkas obstruction to the nonnegative linear-potential route

Date: 2026-08-02 (America/Los_Angeles)

## Status

The obstruction in this note is **PROVED / EXACTLY COMPUTED**.  It closes
one sufficient additive-certificate architecture.  It does **not** disprove
either the component inequality

\[
 {p_i\over1-p_i}\le 2\sum_vP_{vi}p_v                         \tag{1}
\]

or its aggregate consequence

\[
 \sum_i{p_i\over1-p_i}\le2\sum_i p_i.                       \tag{2}
\]

Both (1) and (2) remain **OPEN**.  In fact, every component of (1) is
strictly positive on the graph below.

## 1. The sufficient architecture

Let `Pi` be the stationary law of the exact geometric-union dual at
fitness two, put

\[
 p_i=\Pr_\Pi(i\in A),\qquad q_i=1-p_i,
 \qquad H_{vu}={2P_{vu}\over1+P_{vu}},
\]

and define

\[
 b(A)=\sum_{v\in A}\sum_{u\notin A}{H_{vu}\over q_u}-2|A|.
                                                                    \tag{3}
\]

Coordinate stationarity gives

\[
 E_\Pi b=\sum_i{p_i\over q_i}-2\sum_i p_i.                         \tag{4}
\]

For an additive potential `g(A)=sum_i a_i 1_{i in A}`, set
`c_i=a_i+1/q_i`.  A direct generator calculation gives

\[
 b(A)+\mathcal Dg(A)
 =\sum_{v\in A}\left[-2-c_v+{1\over q_v}
       +\sum_{u\notin A}H_{vu}c_u\right].                          \tag{5}
\]

Consequently, if

\[
 c\ge0,
 \qquad (I-H)c\ge r,
 \qquad r_i={1\over q_i}-2,                                       \tag{6}
\]

then each bracket in (5) is nonpositive: the singleton state gives the
largest hole sum because `c>=0`.  Thus (6) is a clean sufficient
statewise certificate for (2).

The next section proves that (6) need not be feasible, even for a
positive-support undirected weighted graph.

## 2. A positive-support five-vertex obstruction

On vertices `0,1,2,3,4`, use the symmetric edge weights, in lexicographic
order

\[
 (w_{01},w_{02},w_{03},w_{04},w_{12},w_{13},w_{14},w_{23},w_{24},w_{34})
 =(1,2,5,2,200,1,5,1,1,1).                                       \tag{7}
\]

All ten weights are positive, so the graph is connected and has complete
support.  Its weighted degrees are `(10,207,204,8,9)`.

Exact rational solution of the 31-state stationary system gives the two
strict bounds

\[
 p_1>{517\over1017},\qquad p_2>{1001\over2001}.                    \tag{8}
\]

For auditability, the exact positive remainders are

\[
 p_1-{517\over1017}
 ={16128077320739671736850641870246004538310454992515309384997972056317661977333799724588244200601591135935
 \over
 233936825123327277670759725412074607808350232528471794164977487448818818468857110188612155597679923526395608},
                                                                    \tag{9}
\]

\[
 p_2-{1001\over2001}
 ={37986585813440403644776992080130395722906335040929493543357669794334290388581039743580130567855175068333
 \over
 690424169722386257550428039158644970832608872108365870389557451895407751852777400423912866299347384920822436}.
                                                                    \tag{10}
\]

Take the nonnegative row vector

\[
 y=\left(0,1,{1977\over2000},0,{3\over100}\right).                \tag{11}
\]

Direct substitution in the rational matrix `H` gives

\[
 H^Ty-y=\left(
 {73127\over1841125},
 {1\over7070},
 {49\over162800},
 {16829\over666250},
 {291331\over10865000}
 \right)>0.                                                        \tag{12}
\]

Equations (8) imply

\[
 r_1>{17\over500},\qquad r_2>{1\over1000}.
\]

Also `r_4>-1`, since `p_4>0`.  Hence

\[
 y^Tr>
 {17\over500}+{1977\over2000}{1\over1000}-{3\over100}
 ={9977\over2000000}>0.                                           \tag{13}
\]

If a vector `c` satisfied (6), multiplication by `y^T` would give

\[
 0<y^Tr\le y^T(I-H)c.
\]

But (12) says `y^T(I-H)<=0` componentwise, and `c>=0`, so the right side
is at most zero.  This contradiction is an exact Farkas certificate of
infeasibility.

## 3. What the obstruction does not say

The graph (7) is not a counterexample to the odds conjecture.  The exact
component slacks

\[
 2\sum_vP_{vi}p_v-{p_i\over q_i}
\]

are respectively larger than

\[
 {1\over25},\quad {1\over20},\quad {1\over25},\quad
 {3\over100},\quad {1\over100}.                                  \tag{14}
\]

Thus the aggregate slack is also strictly positive.  The conclusion is
only that nonnegative `c` plus the singleton inequalities (6) cannot be a
universal proof.  A signed additive potential checked on all subsets, a
higher-order potential, or a genuinely stationary path argument is not
excluded.

## 4. Verification

Run

```text
python3 verify_linear_potential_farkas.py
```

The verifier uses only `fractions.Fraction`.  It constructs every geometric
burst by Boolean-lattice inversion, builds and solves the full 31-state
stationary generator, checks (8)--(14), and checks stationarity and the
aggregate identity (4) exactly.
