# Cross-rule orbital midpoint symmetrization is false

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Exact status

For a loopless undirected conductance matrix `W`, a vertex transposition
`sigma`, and

\[
 \bar W={W+\sigma W\sigma^{-1}\over2},
\]

consider the fitness-two cross-rule functional

\[
 \Phi(W)=\log\rho_{Bd}(W,2)+\log\rho_{dB}(W,2).       \tag{1}
\]

The proposed orbital inequality

\[
                         \Phi(\bar W)\geq\Phi(W)      \tag{2}
\]

is **false**, already on three vertices.  Consequently, iterative
permutation averaging cannot prove the fitness-two product inequality.

Take the weighted path

\[
             w_{01}=0,\qquad w_{02}=3,\qquad w_{12}=1,       \tag{3}
\]

and let `sigma=(0 2)`.  Its midpoint has

\[
             \bar w_{01}=\bar w_{12}={1\over2},\qquad
             \bar w_{02}=3.                                \tag{4}
\]

An exact solution of both six-state absorbing systems gives

\[
 \begin{array}{c|cc}
 &W&\bar W\\ \hline
 \rho_{Bd}&817/1479&4397/8226\\[2mm]
 \rho_{dB}&41/105&466/1161.
 \end{array}                                                \tag{5}
\]

Thus dB improves but Bd falls by more, and

\[
 \boxed{
 \rho_{Bd}(\bar W,2)\rho_{dB}(\bar W,2)
 -\rho_{Bd}(W,2)\rho_{dB}(W,2)
 =-{94973014\over82395955215}<0.}                           \tag{6}
\]

The failure is not confined to a zero-edge boundary.  The positive
triangle

\[
             (w_{01},w_{02},w_{12})=(1,10,2)                \tag{7}
\]

under the same transposition has midpoint `(3/2,10,3/2)` and exact product
gap

\[
                         -{531647447363\over14553217942853040}<0. \tag{8}
\]

## 2. Exact even--odd Schur identity

The counterexample can be located precisely in the transposition-odd
sector.  This identity applies to either update rule and to every finite
conductance orbit.

Let `Omega` be the nonabsorbing configuration space and let `J` be the
permutation matrix induced by `sigma` on `Omega`.  Delete self loops from
the update chain and normalize the remaining flip rates in each row.  For
rule `X` in `{Bd,dB}`, write its Dirichlet system as

\[
                         H_X(s)f_X(s)=q_X(s),                 \tag{9}
\]

where `H_X(s)` is the killed matrix, `q_X(s)` is the influx to the full
configuration, and `W_{-s}=sigma W_s sigma^{-1}`.  If `alpha` is the
uniform-singleton start vector, then

\[
                         \rho_X(s)=\alpha^Tf_X(s),\qquad
                         J\alpha=\alpha.                    \tag{10}
\]

Covariance gives

\[
 JH_X(s)J=H_X(-s),\qquad Jq_X(s)=q_X(-s).             \tag{11}
\]

Suppress the rule subscript temporarily and put

\[
 \begin{aligned}
 H^e&={H+JHJ\over2},&H^o&={H-JHJ\over2},\\
 q^e&={q+Jq\over2},&q^o&={q-Jq\over2},\\
 g&={f+Jf\over2},&d&={f-Jf\over2}.
 \end{aligned}                                             \tag{12}
\]

Here `H^e` preserves parity and `H^o` switches it.  Adding and subtracting
the endpoint and conjugate endpoint equations proves

\[
 H^eg+H^od=q^e,\qquad H^ed+H^og=q^o.                 \tag{13}
\]

Restricting the second equation to the odd sector gives the literal Schur
elimination

\[
 d=(H^e_{--})^{-1}(q^o-H^o_{-+}g),                  \tag{14}
\]

and hence

\[
 \{H^e_{++}-H^o_{+-}(H^e_{--})^{-1}H^o_{-+}\}g
 =q^e-H^o_{+-}(H^e_{--})^{-1}q^o.                  \tag{15}
\]

Let `H_0=H_X(0)`, `q_0=q_X(0)`, and

\[
                         \mu_X=H_0^{-T}\alpha.              \tag{16}
\]

The midpoint is transposition invariant, but in general `H_0` is not
`H^e`: update rates are nonlinear functions of the conductances.  Since
`rho_X(s)=alpha^Tg`, equations (13) and (16) give the exact center--endpoint
identity

\[
 \boxed{
 \begin{aligned}
 \delta_X(s)&:=\rho_X(0)-\rho_X(s)\\
 &=\mu_X^T\{(q_0-q^e)+(H^e-H_0)g+H^od\}.
 \end{aligned}}                                            \tag{17}
\]

The three terms are, respectively, the boundary-source change, the
parity-even rate change, and the odd Schur feedback (14).

The cross-rule product has no additional hidden term.  With

\[
 \overline\rho_X={\rho_X(0)+\rho_X(s)\over2},
\]

one has identically

\[
 \boxed{
 \rho_{Bd}(0)\rho_{dB}(0)-\rho_{Bd}(s)\rho_{dB}(s)
 =\overline\rho_{dB}\,\delta_{Bd}
  +\overline\rho_{Bd}\,\delta_{dB}.}                       \tag{18}
\]

Equations (14), (17), and (18) are the exact combined Schur/odd-sector
reduction for (2).

## 3. The sharp obstruction on the path

For the path (3), evaluate (17) at `s=1` using the row-normalized killed
systems.  After the cross-rule weighting in (18), the source, even-rate,
and odd-feedback contributions are exactly

\[
 \begin{aligned}
 \mathcal S&={471596086168619\over43188663885494400}>0,\\
 \mathcal E&={13253289226241\over5398582985686800}>0,\\
 \mathcal O&=-{368843888887\over25390161014400}<0.          \tag{19}
 \end{aligned}
\]

They satisfy

\[
                 \mathcal S+\mathcal E+\mathcal O
                 =-{94973014\over82395955215}.              \tag{20}
\]

Thus neither the local midpoint source bonus nor the parity-even generator
change is responsible for failure: both have the desired sign.  The
nonlocal transposition-odd excursion is larger and has the opposite sign.
This is the minimal structural obstruction to the proposed proof.

## 4. Failure is finite-amplitude, not local curvature

The whole path orbit is

\[
 w_{01}(s)={1-s\over2},\qquad w_{02}(s)=3,\qquad
 w_{12}(s)={1+s\over2},\qquad |s|\leq1.                     \tag{21}
\]

The replay derives exact even rational functions of `s` for both fixation
probabilities.  In particular, if

\[
                         F(s)=\rho_{Bd}(s)\rho_{dB}(s),
\]

then

\[
 {d^2\over ds^2}\log F(s)\bigg|_{s=0}
 =-{273956014655842\over69260545804505391}<0.               \tag{22}
\]

So the midpoint is a strict local maximum along this orbit, exactly in the
conjectured direction.  Nevertheless `F(1)>F(0)` by (6).  Any surviving
orbital argument would therefore need a genuinely global monotonicity
principle capable of controlling the odd Green feedback after it reverses
the local curvature.  The explicit counterexample shows that no such
principle can hold for the product itself.

## 5. Scope

**PROVED:** the exact parity/Schur identities (13)--(18), the connected
weighted-path refutation (3)--(6), the strictly positive triangle
refutation (7)--(8), and the odd-feedback decomposition (19)--(20).

**FALSIFIED:** cross-rule log-product midpoint monotonicity under a single
conductance transposition, even for `n=3` and even in the interior of the
positive conductance cone.

**NOT FALSIFIED:** the original PAPT inequality

\[
 {\rho_{Bd}(G,2)\over\rho_{Bd}(K_n,2)}
 {\rho_{dB}(G,2)\over\rho_{dB}(K_n,2)}\leq1.
\]

Both witnesses still satisfy that inequality strictly.  They refute only
the proposed route from an arbitrary graph to the complete graph by
successive permutation midpoints.

## 6. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_cross_rule_orbital_midpoint.py
```

The verifier independently constructs both absorbing chains from their
update rules, checks covariance and the two parity equations, verifies the
Schur/product identity and all rational values in (5)--(20), and derives
the exact orbit curvature (22).
