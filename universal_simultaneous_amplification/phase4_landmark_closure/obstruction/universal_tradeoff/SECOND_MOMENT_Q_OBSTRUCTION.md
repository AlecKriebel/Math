# Exact four-vertex obstruction to the singleton-plus-`Q` route

Date: 2026-08-02 (America/Los_Angeles)

## Status

The generator formula below and the four-vertex separating law are
**PROVED / EXACTLY COMPUTED**.  They show that the stationary singleton
equations together with stationarity of the natural weighted-pair
observable `Q` do not imply the proposed second-moment inequality.

This is **not** a counterexample to the second-moment inequality itself.
Indeed, the actual invariant law of the same graph satisfies that inequality
strictly.  The universal stationary inequality therefore remains **OPEN**.

## 1. The proposed strengthening

Let `P` be the loopless row-stochastic transition matrix of a connected
undirected weighted graph.  At `r=2`, put

\[
 h(p)=\frac{2p}{1+p},\qquad H_{vi}=h(P_{vi}).
 \tag{1}
\]

For a nonempty dual state `A`, write `k=|A|` and define

\[
 C(A)=\sum_{i,j\in A}P_{ij},\qquad
 R_2(A)=\sum_{v\in A,\ i\notin A}
          \frac{P_{vi}^2}{1+P_{vi}}.
 \tag{2}
\]

The exact size drift of the geometric-union dual is

\[
 \mathcal Dk(A)=
 \sum_{v\in A,\ i\notin A}H_{vi}-k.
 \tag{3}
\]

Since `p=p/(1+p)+p^2/(1+p)`, row stochasticity gives the pointwise
identity

\[
 \boxed{C(A)+R_2(A)=\frac{k-\mathcal Dk(A)}2.}
 \tag{4}
\]

Thus every invariant law `Pi` obeys

\[
 E_\Pi\{C(A)+R_2(A)\}=\frac12E_\Pi k.
 \tag{5}
\]

The candidate inequality

\[
 E_\Pi\{C(A)+R_2(A)\}\ge E_\Pi\frac{k^2}{n}
 \tag{6}
\]

is consequently equivalent to

\[
 \boxed{E_\Pi k^2\le\frac n2E_\Pi k.}
 \tag{7}
\]

After size-biasing `Pi`, (7) is exactly the assertion that the occupied-event
chain has stationary mean at most `n/2`.

## 2. Exact drift of the natural pair observable

Put

\[
 s_{ij}=P_{ij}+P_{ji},\qquad
 Q(A)=C(A)=\sum_{i<j}s_{ij}1_{\{i,j\subseteq A\}}.
 \tag{8}
\]

If the occupied target `v` bursts, it is removed and a random nonempty set
of neighbors is inserted.  A named neighbor `i` appears with probability
`H_vi`; two named neighbors `i,j` both appear with probability

\[
 J_{v;ij}=H_{vi}+H_{vj}-h(P_{vi}+P_{vj}).
 \tag{9}
\]

The latter identity is inclusion-exclusion applied to the geometric sample.
Writing `A^c` for the holes, direct accounting of lost, cross, and jointly
created pairs gives

\[
 \boxed{
 \begin{aligned}
 \mathcal DQ(A)=\sum_{v\in A}\Bigg[&
 -\sum_{j\in A\setminus\{v\}}s_{vj}\\
 &+\sum_{i\notin A}H_{vi}
       \sum_{j\in A\setminus\{v\}}s_{ij}\\
 &+\sum_{\{i,j\}\subseteq A^c}J_{v;ij}s_{ij}
 \Bigg].
 \end{aligned}}
 \tag{10}
\]

The companion verifier constructs the full geometric-union law by exact
Boolean-lattice inversion and checks (10) against direct transition
enumeration on every state of the graph below.

## 3. Exact Farkas obstruction on four vertices

Take the symmetrically weighted complete-support graph

\[
 W=
 \begin{pmatrix}
 0&1&1&1\\
 1&0&1&1\\
 1&1&0&2\\
 1&1&2&0
 \end{pmatrix}.
 \tag{11}
\]

Thus the only nonunit edge is `{2,3}`, of weight two.  Its row-stochastic
matrix and one-coordinate appearance matrix are

\[
 P=
 \begin{pmatrix}
 0&1/3&1/3&1/3\\
 1/3&0&1/3&1/3\\
 1/4&1/4&0&1/2\\
 1/4&1/4&1/2&0
 \end{pmatrix},\qquad
 H=
 \begin{pmatrix}
 0&1/2&1/2&1/2\\
 1/2&0&1/2&1/2\\
 2/5&2/5&0&2/3\\
 2/5&2/5&2/3&0
 \end{pmatrix}.
 \tag{12}
\]

Define a probability law `Lambda` on proper nonempty subsets by the following
table.  Bit strings are ordered `x_3 x_2 x_1 x_0`.

| state | `Lambda(A)` | `D x_0` | `D x_1` | `D x_2` | `D x_3` | `D Q` | `k^2/4-k/2` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `0010` | `149/7043` | `1/2` | `-1` | `1/2` | `1/2` | `13/30` | `-1/4` |
| `0100` | `40917/70430` | `2/5` | `2/5` | `-1` | `2/3` | `1/3` | `-1/4` |
| `1000` | `384/35215` | `2/5` | `2/5` | `2/3` | `-1` | `1/3` | `-1/4` |
| `1001` | `12071/133817` | `-1` | `9/10` | `7/6` | `-1` | `187/360` | `0` |
| `1010` | `9836/133817` | `9/10` | `-1` | `7/6` | `-1` | `187/360` | `0` |
| `1011` | `3145/14086` | `-1` | `-1` | `5/3` | `-1` | `-47/36` | `3/4` |

All masses are positive and sum to one.  Exact substitution gives

\[
 E_\Lambda\mathcal Dx_i=0\quad(0\le i<4),
 \qquad E_\Lambda\mathcal DQ=0,
 \tag{13}
\]

but

\[
 \boxed{E_\Lambda\left(\frac{k^2}{4}-\frac k2\right)
 =\frac{100}{7043}>0.}
 \tag{14}
\]

It follows immediately that there are no real coefficients
`a_0,...,a_3,beta` for which the pointwise Poisson/Farkas certificate

\[
 \sum_i a_i\mathcal Dx_i(A)+\beta\mathcal DQ(A)
 \ge \frac{k^2}{4}-\frac k2
 \tag{15}
\]

holds on every proper nonempty state.  Averaging (15) under `Lambda` would
give `0>=100/7043`.  The conclusion allows `beta` of either sign; the
failure is not an artifact of a nonnegativity restriction on the `Q`
coefficient.

More generally, (13)--(14) show that normalization, all singleton balance
equations, positivity of the putative law, and the exact `Q` balance are
logically insufficient to prove (6).  Some additional full-stationarity
information is necessary.

## 4. The graph is not a counterexample

Solving the entire 15-state invariant system of the same geometric-union
chain over the rationals gives

\[
 E_\Pi k=\frac{28299}{16711},\qquad
 E_\Pi k^2=\frac{55968}{16711}.
 \tag{16}
\]

Consequently

\[
 \boxed{
 \frac12E_\Pi k-\frac14E_\Pi k^2
 =\frac{315}{33422}>0.}
 \tag{17}
\]

So the proposed universal second-moment inequality survives this graph.
Only the singleton-plus-`Q` closure route is ruled out.

## 5. Exact verification

Run

```text
python3 verify_second_moment_q_obstruction.py
```

The verifier uses only the Python standard library.  In particular, the
invariant linear system is solved by an explicit rational Gaussian
elimination routine, and the answer is independently substituted into every
stationarity equation.
