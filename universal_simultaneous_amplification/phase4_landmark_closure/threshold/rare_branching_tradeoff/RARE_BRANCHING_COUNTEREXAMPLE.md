# Exact counterexample to the rare-branching Bd--dB sum tradeoff

Date: 2026-08-08 (America/Los_Angeles)

Status: **EXACTLY REFUTED**, by a connected unweighted reversible family.

No literature search or external contact was used.  The exact replay is
`verify_rare_branching_counterexample.py`.

## 1. The proposed inequality

At `r=3/2`, put `p=(r-1)/r=1/3`.  For a row-stochastic replacement matrix
`P`, let

\[
 t_i=\sum_jP_{ji},\qquad h(z)={3z\over2+z}.
\]

The rare-mutant Bd and dB branching survival vectors are the maximal
solutions in `[0,1]^n` of

\[
 {t_i x_i\over1-x_i}=r(Px)_i,                         \tag{1}
\]

and

\[
 {y_i\over1-y_i}=\sum_v h(P_{vi})y_v.                 \tag{2}
\]

The separate Jensen bounds are valid:

\[
 {1\over n}\sum_i t_i x_i\le p,
 \qquad
 {1\over n}\sum_i y_i\le p{n-2\over n-1}.            \tag{3}
\]

The conjectured strengthening was

\[
 \overline x+\overline y
 \le p+p{n-2\over n-1}.                               \tag{4}
\]

Equation (4) is false, and its failure persists as the population grows.

## 2. Explicit unweighted graph family

For every integer `m>=1`, construct `G_m` as follows.

1. Start with a clique on `3m+1` vertices.
2. Distinguish one clique vertex `H`.
3. Attach `m` new pendant leaves to `H`.

All edges have unit weight.  Thus

\[
 |V(G_m)|=4m+1.
\]

The graph is finite, connected, loopless, undirected, unweighted, and its
random-walk matrix is reversible with degree measure.  There are three
automorphism classes:

\[
 H,\qquad L\ (m\text{ leaves}),\qquad
 C\ (3m\text{ ordinary clique vertices}).
\]

The degrees are `4m`, `1`, and `3m`, respectively.  Consequently the three
temperatures are

\[
 t_H=m+1,qquad t_L={1\over4m},qquad
 t_C={1\over4m}+{3m-1\over3m}.                        \tag{5}
\]

The Bd row masses between the three classes are

\[
 P_{\rm class}=
 \begin{pmatrix}
 0&1/4&3/4\\
 1&0&0\\
 1/(3m)&0&(3m-1)/(3m)
 \end{pmatrix}.                                       \tag{6}
\]

Automorphisms preserve the full offspring law, not merely its mean, so the
survival probabilities are constant on these classes.  Equations (1)--(2)
therefore lump exactly.

Writing `f(z)=z/(1-z)`, the Bd equations are

\[
\begin{aligned}
 (m+1)f(x_H)&={3\over2}\left({x_L\over4}+{3x_C\over4}\right),\\
 {1\over4m}f(x_L)&={3\over2}x_H,\\
 \left({1\over4m}+{3m-1\over3m}\right)f(x_C)
 &= {3\over2}\left({x_H\over3m}+{3m-1\over3m}x_C\right).
\end{aligned}                                         \tag{7}
\]

Put

\[
 a_m=h(1/(4m)),\qquad c_m=h(1/(3m)).
\]

The dB equations are

\[
\begin{aligned}
 f(y_H)&=m y_L+3m c_m y_C,\\
 f(y_L)&=a_m y_H,\\
 f(y_C)&=a_m y_H+(3m-1)c_m y_C.
\end{aligned}                                         \tag{8}
\]

These equations are derived directly from the rare branching rules.  For
example, a hub mutant produces into each pendant target at rate `h(1)=1`,
and into each ordinary clique target at rate `h(1/(3m))`.

## 3. Exact finite counterexample without algebraic root solving

For a nonnegative birth matrix `B` and positive death vector `d`, define

\[
 \Phi_i(z)={(Bz)_i\over d_i+(Bz)_i}.                  \tag{9}
\]

This map is coordinatewise increasing.  Branching survival is its maximal
fixed point: iteration from the all-one vector decreases to it.  Hence any
positive rational vector `l` satisfying

\[
 l\le\Phi(l)                                           \tag{10}
\]

is a rigorous lower bound on survival.  Indeed, iteration from `l` is
increasing and converges to a fixed point below the maximal one.

Take `m=25`, so `n=101`, and set, in `(H,L,C)` order,

\[
 \ell_B=\left({3\over125},{39\over50},{8\over25}\right),
 \qquad
 \ell_D=\left({3\over8},{1\over200},{13\over40}\right). \tag{11}
\]

Direct exact substitution in (7)--(9) gives

\[
 \Phi_B(\ell_B)-\ell_B=
 \left(
 {642\over1332625},
 {3\over1150},
 {3226\over1378825}
 \right)>0,                                            \tag{12}
\]

and

\[
 \Phi_D(\ell_D)-\ell_D=
 \left(
 {7\over1944},
 {61\over107800},
 {21089\over24012280}
 \right)>0.                                            \tag{13}
\]

Therefore the true uniform survival sum is at least

\[
 {\ell_{B,H}+25\ell_{B,L}+75\ell_{B,C}
  +\ell_{D,H}+25\ell_{D,L}+75\ell_{D,C}\over101}
 ={68399\over101000}.                                  \tag{14}
\]

The proposed right side is

\[
 {1\over3}+{1\over3}{99\over100}={199\over300}.
\]

Their exact difference is

\[
 {68399\over101000}-{199\over300}
 ={4207\over303000}>0.                                 \tag{15}
\]

Thus `G_25` is an exact finite counterexample.  The certificate uses only
rational arithmetic and monotonicity; numerical fixation or algebraic-root
reconstruction plays no role.

## 4. Persistent asymptotic violation

Equations (7)--(8) also give the limit transparently.  The hub has vanishing
proportion.  From (7), `x_H=O(1/m)`, while the ordinary clique survival
converges to

\[
 x_C\longrightarrow p={1\over3}.                      \tag{16}
\]

The latter follows either directly from the limiting equation
`f(x_C)=r x_C` or by first restricting the branching process to births
inside the `3m`-vertex core, which supplies a positive lower solution
converging to `p`.

If `ell=lim x_L`, then the first two equations of (7) give

\[
 {\ell\over1-\ell}={9\over4}(\ell+1).                 \tag{17}
\]

The unique solution in `(0,1)` is

\[
 \ell={\sqrt{85}-2\over9},
 \qquad 9\ell^2+4\ell-9=0.                            \tag{18}
\]

For dB, (8) gives `y_L->0` and

\[
 y_C\longrightarrow p={1\over3}.                      \tag{19}
\]

The hub survival has a finite nonzero limit but contributes `o(1)` to the
uniform mean.  Hence

\[
 \overline x\longrightarrow {\ell+3p\over4},
 \qquad
 \overline y\longrightarrow {3p\over4}.               \tag{20}
\]

It follows that

\[
 \overline x+\overline y
 \longrightarrow {\sqrt{85}+16\over36}
 ={2\over3}+{\sqrt{85}-8\over36}.                     \tag{21}
\]

The limiting excess is strictly positive because `85>8^2`.  Numerically it
is about `0.03388`, but the sign certificate in (21) is exact.

The mechanism is spatial separation.  The pendant class, of asymptotic
proportion `1/4`, has very small Bd death temperature and Bd survival above
`2/3`.  The dense clique class, of asymptotic proportion `3/4`, retains dB
survival `1/3`.  The losses occur on different vertex classes, so the two
separate Jensen bounds in (3) cannot be added after replacing the
temperature-weighted Bd mean by the uniform mean.

More generally, if the pendant proportion tends to `alpha` and the ordinary
clique proportion to `1-alpha`, the same calculation gives

\[
 \ell(\alpha)=
 {8\alpha-3+\sqrt{9+60\alpha-44\alpha^2}\over18\alpha},
\]

and limiting excess

\[
 \alpha\{\ell(\alpha)-2/3\}
 ={\sqrt{9+60\alpha-44\alpha^2}-3-4\alpha\over18},     \tag{22}
\]

which is positive for every `0<alpha<3/5`.  The rational choice
`alpha=1/4` was used above for the clean algebraic certificate.

## 5. Consequence for the finite-fixation route

The branching inequality itself fails by a constant along an explicit
fitness-independent family.  Therefore it cannot be upgraded to the
endpoint balanced fixation separator by an `o(1)` collision or two-lineage
correction.  Such a correction would start from an upper bound already on
the wrong side of the complete-graph target by

\[
 {\sqrt{85}-8\over36}>0.
\]

No universal finite-fixation correction was proved in this branch.  This
does **not** say that the graph family simultaneously amplifies finite
fixation at `r=3/2`: survival of the rare branching approximation is not
finite-population fixation.  It says precisely that this proposed
branching-sum route cannot establish the endpoint obstruction.

## 6. Classification

- Separate weighted Bd Jensen bound: **PROVED (inherited)**.
- Separate dB row-concavity bound: **PROVED (inherited)**.
- Uniform Bd+dB branching-sum inequality: **EXACTLY FALSIFIED**.
- Finite unweighted counterexample: **EXACTLY CERTIFIED** by rational
  subsolutions on `101` vertices.
- Persistent growing-family counterexample: **PROVED** with exact limiting
  excess `(sqrt(85)-8)/36`.
- Upgrade to finite fixation: **BLOCKED BY THE FALSE PREMISE; NOT PROVED**.

