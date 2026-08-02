# Exact stationary split for the component-odds problem

Date: 2026-08-02 (America/Los_Angeles)

## Status

The identities and counterexamples in this note are **PROVED / EXACTLY
COMPUTED**.  The two inequalities in the stationary sandwich below remain
**OPEN** for connected undirected weighted graphs.  Consequently the
component-odds inequality itself remains **OPEN**.

This checkpoint uses only the special post-clock stationary mixture.  It
does not reinstate the false arbitrary-start stopped-count lemma.

## 1. Direct stationary/resolvent formulation

Fix a target vertex `i`.  Use the notation from the exact clock-interval
reduction:

* `eta_i` is the outside-set law immediately after an `i`-clock ring;
* `R_0` is the sub-Markov terminal kernel up to the next independent
  rate-one `i` clock, restricted to paths with zero raw samples equal to
  `i`;
* `u=R_0 1` is the zero-count probability;
* `g(Y)` is the expected raw `i`-sample multiplicity before that clock;
* `p_i` and `q_i=1-p_i` are the stationary occupancy and vacancy
  probabilities.

Let `pi_i^0` be the stationary outside law conditional on `i` being absent.
Looking at the terminal state of a zero-count clock interval gives the exact
measure identity

\[
 \boxed{q_i\pi_i^0=\eta_iR_0.}                         \tag{1}
\]

Put

\[
 h_i(Y)=\sum_{v\in Y}\frac{2P_{vi}}{1+P_{vi}},\qquad
 b_i(Y)=2\sum_{v\in Y}P_{vi}.                         \tag{2}
\]

When `i` is absent, `h_i(Y)` is its instantaneous successful fill rate.
When it is occupied, its rate-one clock clears it.  Exact coordinate
stationarity therefore gives

\[
 \boxed{\frac{p_i}{q_i}=E_{\pi_i^0}h_i.}              \tag{3}
\]

The renewal-reward identity for raw samples gives

\[
 \boxed{\lambda_i:=E_{\eta_i}g
 =E_\pi b_i=2\sum_vP_{vi}p_v.}                        \tag{4}
\]

Thus the desired component inequality has the direct stationary form

\[
 \boxed{E_{\pi_i^0}h_i\ \le\ E_{\eta_i}g.}           \tag{5}
\]

This is the formulation that now needs proof or an admissible exact
counterexample.

## 2. Exact two-piece stationary sandwich

Bias the post-clock start by the event that its next interval has zero
count:

\[
 \widehat\eta_i(Y)=\frac{\eta_i(Y)u(Y)}{q_i}.          \tag{6}
\]

Then elementary expansion gives two exact identities:

\[
 A_i:=E_{\eta_i}[u(1+g)]-1
 =q_i\left(E_{\widehat\eta_i}g-E_{\pi_i^0}h_i\right), \tag{7}
\]

\[
 \operatorname{Cov}_{\eta_i}(u,g)
 =q_i\left(E_{\widehat\eta_i}g-E_{\eta_i}g\right).   \tag{8}
\]

Consequently

\[
 \boxed{
 q_i(1+\lambda_i)-1
 =A_i-\operatorname{Cov}_{\eta_i}(u,g)
 =q_i\left(E_{\eta_i}g-E_{\pi_i^0}h_i\right).}       \tag{9}
\]

A sufficient stationary sandwich is therefore

\[
 \boxed{
 E_{\pi_i^0}h_i
 \ \le\ E_{\widehat\eta_i}g
 \ \le\ E_{\eta_i}g.}                              \tag{10}
\]

The left inequality is `A_i>=0`; the right is
`Cov_eta_i(u,g)<=0`.  Broad exact random screens through five vertices and
adversarial floating-point optimization found no failure of either side for
symmetric weights.  That is discovery evidence only, not proof.

## 3. Exact boundary of the left split

The left split is not a theorem for arbitrary directed kernels.  On four
vertices take

\[
 W=\begin{pmatrix}
 0&150&1&600\\
 1&0&6000&300\\
 1&3000&0&6\\
 300&25&1&0
 \end{pmatrix},\qquad i=3.                            \tag{11}
\]

The exact verifier obtains

\[
 A_3<0\quad(A_3\simeq-3.20486001\cdot10^{-5}),        \tag{12}
\]

while

\[
 \operatorname{Cov}_{\eta_3}(u,g)<0,qquad
 q_3(1+\lambda_3)-1\simeq0.0785752592>0.              \tag{13}
\]

Thus stationarity alone does not prove the left side of (10).  Any proof of
that side for the admissible class must use the undirected-weight relation,
or some consequence of it.  This example is not an admissible graph
counterexample and does not refute (5).

## 4. Two exact symmetric resolvent dead ends

It is tempting to interpolate the left inequality in (10) through
`E_eta R_0g` by proving

\[
 E_\eta(ug)\ge E_\eta R_0g\ge p_i.                   \tag{14}
\]

Both comparisons are false on connected symmetrically weighted `K_4`s.
In edge order `(01,02,03,12,13,23)`:

* `(40,1,60,1,1,1000)`, with `i=3`, gives

  \[
  E_\eta(ug-R_0g)\simeq-1.67435352\cdot10^{-4}<0;
  \tag{15}
  \]

* `(2000,1,1,100,1,300)`, with `i=2`, gives

  \[
  E_\eta R_0g-p_i\simeq-8.14745609\cdot10^{-6}<0.
  \tag{16}
  \]

In both graphs the actual two sides of (10) have the conjectured strict
order.  Equations (15)--(16) only close the proposed intermediate route.

Two generic correlation shortcuts also fail exactly:

* `eta_i` need not be pairwise associated.  Edge weights
  `(1,2,1,2,2,10)`, target `i=0`, give covariance approximately
  `-0.118150249` between outside coordinates `2` and `3`.
* `u` is not globally a scalar antitone function of `g`.  With edge weights
  `(1,5,100,2,5,10)` and target `i=0`, outside states `{1,2}` and `{3}`
  have both `u` and `g` ordered in the same strict direction.

These failures do not decide the covariance in (8), which involves the
special functions and the special stationary mixture simultaneously.

## 5. Verification

Run

```text
python3 verify_stationary_odds_split.py
```

The verifier uses only exact rational arithmetic.  It independently builds
the geometric-union generator, solves its stationary equations, constructs
`R_0`, `u`, and `g`, verifies (1)--(9), and checks every strict sign in
(12), (15), and (16).  It also checks the two correlation-route
counterexamples exactly.  The separate numerical optimizer
`search_split_counterexamples.py` is explicitly a discovery tool and is not
used by the proof certificate.
