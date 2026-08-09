# The global adjoint factor-two conjecture is false

Date: 2026-08-08 (America/Los_Angeles)

## Status

The proposed endpoint inequality

\[
 {1\over2}-\sigma\ \geq\ 2\left(\beta-{1\over2}\right)       \tag{1}
\]

for every diffuse Bd/dB adjoint branching kernel is **FALSIFIED**.  The
counterexample below is a three-type kernel induced by a positive symmetric
weight matrix, so it is exactly on the undirected-realizable side of the
normal form.  A rational member is certified by exact interval arithmetic.

The same family has the limiting response

\[
 \left(\beta-{r-1\over r},\ \sigma-{r-1\over r}\right)
 =\left({(1-\gamma)(1-\theta)\over r},
        -{(1-\gamma)(r-1)\over r}\right)+o(1),       \tag{2}
\]

uniformly on every compact fitness interval on which the displayed positive
branch exists.  Its dB cost divided by its Bd gain is

\[
                         {r-1\over1-\theta}.          \tag{3}
\]

Thus (1) fails at `r=2` whenever `theta<1/2`.  On the other hand, this family
does **not** supply the required catalyst: its endpoint cost/gain ratio has
infimum one, not zero.  It instead identifies the sharper unresolved
boundary

\[
                         \boxed{\ \beta+\sigma\leq1\ }.          \tag{4}
\]

## 1. Positive symmetric three-type family

Fix

\[
 0<\gamma<1,\qquad 0<\theta<1,
 \qquad 0<\varepsilon<1-\gamma,
\]

and put `A=1-gamma-epsilon`.  The uniform-initialization type law and the
symmetric weight matrix are

\[
 p=(A,\varepsilon,\gamma),\qquad
 W=\begin{pmatrix}
 \varepsilon&(1-\theta)/\varepsilon&\theta/\gamma\\
 (1-\theta)/\varepsilon&1&1\\
 \theta/\gamma&1&1/\varepsilon
 \end{pmatrix}.                                      \tag{5}
\]

Define

\[
 \delta_i=\sum_jp_jW_{ij},\qquad
 P_{ij}={p_jW_{ij}\over\delta_i},\qquad
 R=D_p^{-1}P^TD_p,\qquad t=R\mathbf1.                \tag{6}
\]

All entries are positive.  Moreover
`p_i delta_i P_ij = p_i p_j W_ij` is symmetric in `i,j`, so `P` is precisely
the latent kernel of an undirected weighted clone graph.  As
`epsilon -> 0` with `gamma,theta` fixed,

\[
 P\longrightarrow
 \begin{pmatrix}
 0&1-\theta&\theta\\
 1&0&0\\
 0&0&1
 \end{pmatrix},                                      \tag{7}
\]

while

\[
 t_A\to0,\qquad t_B\to\infty,\qquad
 t_C\to T:=1+{(1-\gamma)\theta\over\gamma}.         \tag{8}
\]

This is not the deterministic involution boundary: a positive fraction
`theta` of the first row leaks into the sticky third type, while the
reversing stationary mass becomes singular.

## 2. Exact limiting survival probabilities

At fitness `r`, the rare-mutant survival vectors solve

\[
 t_i b_i=r(1-b_i)(Pb)_i,
 \qquad
 s_i=r(1-s_i)(Rs)_i.                                \tag{9}
\]

Assume

\[
                         T<r.                        \tag{10}
\]

Taking `epsilon -> 0` in the unique positive solutions gives

\[
 b_A\to1,\qquad b_B\to0,\qquad
 b_C\to1-{T\over r}.                                \tag{11}
\]

For the dB system,

\[
 s_A\to0,\qquad s_C\to{r-1\over r},                \tag{12}
\]

and `s_B` tends to the unique root in `(0,1)` of

\[
 s_B=r^2(1-\theta)(1-s_B)(s_B+H_r),\qquad
 H_r={(1-\gamma)\theta(r-1)\over r\gamma}.          \tag{13}
\]

The `B` type has vanishing initialization mass, so this last coordinate
does not enter the limiting averages.  Equations (11)--(13) yield

\[
 \beta(r)\to1-{\gamma+(1-\gamma)\theta\over r},
 \qquad
 \sigma(r)\to{\gamma(r-1)\over r},                  \tag{14}
\]

which is (2).  The convergence follows from the isolated positive roots and
is uniform when `r` ranges over a compact set separated from both `1` and
`T`.

At `r=2`, write `G=beta-1/2` and `L=1/2-sigma`.  Then

\[
 G\to{(1-\gamma)(1-\theta)\over2},\qquad
 L\to{1-\gamma\over2},\qquad
 L-2G\to(1-\gamma)(\theta-1/2).                     \tag{15}
\]

This gives a robust open set of violations of (1).

## 3. Exact rational finite-kernel certificate

Take

\[
 \gamma={1\over14},\qquad\theta={1\over50},\qquad
 \varepsilon={1\over1000}.                          \tag{16}
\]

Then

\[
 p=\left({6493\over7000},{1\over1000},{1\over14}\right),
 \qquad
 W=\begin{pmatrix}
 1/1000&980&7/25\\
 980&1&1\\
 7/25&1&1000
 \end{pmatrix}.                                      \tag{17}
\]

Let `q=1-b` and `h=1-s`.  At `r=2` their fixed maps are

\[
 \mathcal T_B(q)_i={t_i\over t_i+2(1-(Pq)_i)},
 \qquad
 \mathcal T_D(h)_i={1\over1+2(t_i-(Rh)_i)}.          \tag{18}
\]

Both maps are coordinatewise increasing.  The replay file constructs exact
rational boxes around

```text
q = (0.10007400874271313, 0.99802218643427953,
     0.62476550479407289),
h = (0.99803836212282937, 0.21910476890768346,
     0.50131062575520824)
```

with respective radius vectors

```text
10^-8 (283, 1, 938),     10^-8 (1, 174, 227).
```

Writing the lower and upper corners as `L_B,U_B,L_D,U_D`, exact `Fraction`
arithmetic verifies

\[
 \mathcal T_B(L_B)\ge L_B,\quad
 \mathcal T_B(U_B)\le U_B,\quad
 \mathcal T_D(L_D)\ge L_D,\quad
 \mathcal T_D(U_D)\le U_D.                           \tag{19}
\]

All entries of `P,R` are positive.  Monotone iteration and the standard
uniqueness of the subunit fixed point for a positively regular
supercritical multitype branching process therefore enclose the two
extinction vectors in these boxes.  Finally, since

\[
 L-2G=2E_pq+E_ph-{3\over2},                          \tag{20}
\]

the exact upper corner gives

\[
 2E_pU_B+E_pU_D-{3\over2}
 =-{182920163290948548677\over700000000000000000000}<0. \tag{21}
\]

This is an exact, non-asymptotic refutation of (1) inside the rational
three-type branching normal form.

For any clone multiplier `m` divisible by `7000`, take `mp_i` vertices of
type `i`.  Give a cross-type edge `{i,j}` weight `W_ij/m`, and a within-type
edge weight `p_iW_ii/(mp_i-1)`.  Every vertex then has exact type-level
outgoing masses `p_jW_ij`; hence the loopless connected undirected graph
realizes (6) exactly at singleton level.  Sending `m` to infinity removes
same-vertex collision terms and yields the certified branching kernel.

## 4. Sharp singular ray supplied by the family

Let `c_k -> 0`, choose

\[
 \gamma_k=1-c_k,\qquad \theta_k\to0,
\]

and then choose `epsilon_k` sufficiently small relative to `c_k` that the
error in (14), uniformly on a prescribed compact subset of `(1,2]`, is
`o(c_k)`.  A final clone multiplier can make every type population diverge
and the stopped-chain approximation error `o(c_k)`.  The normalized
branching response is

\[
 {1\over c_k}\left(
  \beta_k(r)-{r-1\over r},
  \sigma_k(r)-{r-1\over r}
 \right)
 \longrightarrow
 \left({1\over r},-{r-1\over r}\right).             \tag{22}
\]

The construction is fitness-independent and compact-uniform after the
usual diagonal exhaustion of `(1,2]`.  But (22) has endpoint cost/gain one.
Nonnegative mixtures of rays from this same family cannot cancel that
cost, because every member has ratio `(r-1)/(1-theta)>=r-1`.

## 5. Scope ledger

**PROVED:** the symmetric-weight realization, the limiting solutions
(11)--(14), the exact rational interval certificate (19)--(21), and the
normalized response ray (22) within the diffuse adjoint branching normal
form.

**FALSIFIED:** the global factor-two conjecture (1), including its proposed
restriction to undirected-realizable kernels.

**OPEN:** the sharper factor-one inequality (4); a classification of its
equality/singular-attainment cases; extension from branching establishment
to a fixation lower bound; and a catalyst with dB cost little-oh of its Bd
gain.

The present counterexample is not a simultaneous amplifier and is not a
counterexample to an endpoint separator for finite fixation probabilities.

## 6. Exact replay

Run `verify_adjoint_factor_two_refutation.py`.  It checks the symbolic
limits and response formula, reconstructs `P,R,t` from (17), verifies all
box inequalities using rational arithmetic, and certifies (21).
