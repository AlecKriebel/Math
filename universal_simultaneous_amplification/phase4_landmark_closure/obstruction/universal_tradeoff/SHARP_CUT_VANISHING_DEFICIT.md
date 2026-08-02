# A balanced sharp cut with only a vanishing fixation-sum deficit

Date: 2026-08-02 (America/Los_Angeles)

## Status and purpose

The theorem below is **PROVED**.  It gives an explicit fitness-independent
family satisfying all inherited local consequences of eventual all-fitness
dB amplification:

* complete support, hence support degree tending to infinity;
* normalized influence concentration `c(G_n)->0`;
* `t_I->1` in uniform `L1`.

At the fixed fitness `r_*=16/9>3/2`, its only mesoscopic cut makes both Bd
and dB one-step biases converge to `r_*^(3/2)` and makes their product
converge to the sharp upper bound `r_*^3`.

Despite this maximally adverse cut, the Bd--dB fixation-sum deficit relative
to the complete graph is only order `1/n` and therefore tends to zero.  This
**precisely falsifies** the route which tries to deduce an unscaled constant
tradeoff deficit solely from support diffuseness, `t->1` in `L1`, and the
statewise product bound.  It does not falsify an argument using the actual
dB-amplification inequalities, and the family constructed here is not
claimed to amplify dB.

## 1. Explicit graph family

For `m>=2`, let `G_m` have two vertex classes `L_m,R_m`, each of size `m`.
Put

\[
 \eta_m=2^{-m^4},\qquad \gamma_m=m\eta_m.
 \tag{1}
\]

Give every edge inside `L_m` weight `3/(m-1)`, every edge inside `R_m`
weight `4/(m-1)`, and every edge across `L_m|R_m` weight `eta_m`.  Thus the
weighted degrees are

\[
 d_L=3+\gamma_m,\qquad d_R=4+\gamma_m.
 \tag{2}
\]

All weights are positive rationals independent of fitness.  The graph is
connected and has complete loopless support.

### Theorem 1

Let `U` be Bd or dB and fix any `r>1`.  Put

\[
 a=1-\frac1r,\qquad q=\frac43,
 \tag{3}
\]

and

\[
 M_m(r,q)=\frac12\left{
 \frac{r^mq}{1+r^mq}+\frac{r^m/q}{1+r^m/q}
 \right\}.
 \tag{4}
\]

Then, for every fixed positive integer `K`,

\[
 \rho_{\rm Bd}(G_m,r)
 =M_m(r,q)\frac{a}{1-r^{-m}}+o(m^{-K}),
 \tag{5}
\]

\[
 \rho_{\rm dB}(G_m,r)
 =M_m(r,q)\frac{a(1-1/m)}{1-r^{1-m}}+o(m^{-K}).
 \tag{6}
\]

Consequently

\[
 \boxed{
 \begin{aligned}
 &\rho_{\rm Bd}(G_m,r)+\rho_{\rm dB}(G_m,r)\\
 &\quad-\rho_{\rm Bd}(K_{2m},r)-\rho_{\rm dB}(K_{2m},r)
 =-\frac{a}{2m}+o(m^{-1})
 =-\frac{a}{|V(G_m)|}+o(|V(G_m)|^{-1}).
 \end{aligned}}
 \tag{7}
\]

In particular, the fixation sum is eventually smaller than the complete
sum, but the deficit has no positive unscaled limit.

At

\[
 r_*=\frac{16}{9}=q^2,
 \tag{8}
\]

and the macrostate `S=L_m`,

\[
 \boxed{
 R_{\rm Bd}(S)\longrightarrow\frac{64}{27}=r_*^{3/2},
 \qquad
 R_{\rm dB}(S)\longrightarrow\frac{64}{27}=r_*^{3/2},}
 \tag{9}
\]

so

\[
 R_{\rm Bd}(S)R_{\rm dB}(S)\longrightarrow r_*^3.
 \tag{10}
\]

At this fitness, (7) reads

\[
 \rho_{\rm Bd}(G_m,r_*)+\rho_{\rm dB}(G_m,r_*)
 -\rho_{\rm Bd}(K_{2m},r_*)-\rho_{\rm dB}(K_{2m},r_*)
 =-\frac{7}{32m}+o(m^{-1}).
 \tag{11}
\]

## 2. Exact local diagnostics

For a vertex of `L_m`, its temperature is

\[
 t_L=\frac3{3+\gamma_m}+\frac{\gamma_m}{4+\gamma_m},
 \tag{12}
\]

whereas for a vertex of `R_m`,

\[
 t_R=\frac4{4+\gamma_m}+\frac{\gamma_m}{3+\gamma_m}.
 \tag{13}
\]

Therefore

\[
 t_L-1=-\frac{\gamma_m}{(3+\gamma_m)(4+\gamma_m)},
 \qquad
 t_R-1=+\frac{\gamma_m}{(3+\gamma_m)(4+\gamma_m)}.
 \tag{14}
\]

In particular, uniform `L1` convergence to one holds superexponentially.
The average Simpson concentration is exactly

\[
 c(G_m)=\frac12\left[
 \frac{9/(m-1)+m\eta_m^2}{(3+\gamma_m)^2}
 +\frac{16/(m-1)+m\eta_m^2}{(4+\gamma_m)^2}
 \right]=O(m^{-1}).
 \tag{15}
\]

Thus the inherited local diagnostics do not see the cut-scale asymmetry.

For `S=L_m`, write

\[
 \delta_L=\frac{\gamma_m}{3+\gamma_m},\qquad
 \delta_R=\frac{\gamma_m}{4+\gamma_m}.
 \tag{16}
\]

The two normalized boundary flows are

\[
 A(S)=m\delta_L,qquad B(S)=m\delta_R,qquad
 \frac{A(S)}{B(S)}=\frac{4+\gamma_m}{3+\gamma_m}\longrightarrow q.
 \tag{17}
\]

The exact cut biases are consequently

\[
 R_{\rm Bd}(S)=r\frac{\delta_L}{\delta_R},
 \tag{18}
\]

and, because `P 1_S` is `1-delta_L` on `L_m` and `delta_R` on `R_m`,

\[
 R_{\rm dB}(S)
 =r\frac{\delta_R}{\delta_L}
 \frac{r-(r-1)\delta_L}{1+(r-1)\delta_R}.
 \tag{19}
\]

Multiplication gives the exact approach to the statewise envelope:

\[
 \boxed{
 R_{\rm Bd}(S)R_{\rm dB}(S)
 =r^2\frac{r-(r-1)\delta_L}{1+(r-1)\delta_R}
 \longrightarrow r^3.}
 \tag{20}
\]

Equations (18)--(20) prove (9)--(10) after setting `r=q^2`.

## 3. Exact rare-event reduction

First hold `m` fixed and let the common cross-edge weight tend to zero.
Before a cross replacement, a polymorphic clique absorbs internally.  After
an introduction, a failed lineage returns to the same homogeneous
macrostate; a successful lineage flips its target clique.  Thus the only
transient homogeneous macrostates are

\[
 (L\text{ mutant},R\text{ resident}),\qquad
 (L\text{ resident},R\text{ mutant}).
\]

The complete-graph singleton fixation probabilities, derived from their
one-dimensional birth--death chains, are

\[
 b_m(r)=\rho_{\rm Bd}(K_m,r)=\frac{a}{1-r^{-m}},
 \tag{21}
\]

\[
 d_m(r)=\rho_{\rm dB}(K_m,r)
 =\frac{a(1-1/m)}{1-r^{1-m}}.
 \tag{22}
\]

Their reciprocal-fitness ratios are exactly

\[
 \frac{b_m(r)}{b_m(1/r)}=r^{m-1},\qquad
 \frac{d_m(r)}{d_m(1/r)}=r^{m-2}.
 \tag{23}
\]

Suppose first that `L` is mutant.  Under Bd, the raw favorable-to-adverse
cross-introduction ratio tends to `r*d_R/d_L`, so the ratio of successful
macro-change rates tends to

\[
 Z_{{\rm Bd},L}=r^m\frac43=r^mq.
 \tag{24}
\]

Under dB, the exact raw introduction ratio before taking the weak-cut limit
is

\[
 r\frac{r d_L+o(1)}{d_R+o(1)},
\]

and (23) gives

\[
 Z_{{\rm dB},L}=r^m\frac34=\frac{r^m}{q}.
 \tag{25}
\]

When `R` is mutant, `q` and `1/q` are interchanged.  Hence the uniform
average of the two macro success probabilities is the same `M_m(r,q)` for
both update rules.  A uniform singleton first fixes in its initial clique
with probability `b_m(r)` or `d_m(r)`.  This proves the weak-cut limits in
(5)--(6).

For completeness, the explicit diagonal `eta_m=2^(-m^4)` has the same
limits with an error smaller than every inverse power of `m`.  One elementary
uniformization argument suffices.  At fixed fitness, every nonzero internal
transition probability is bounded below by a reciprocal polynomial in `m`.
From every polymorphic clique state there is a monotone path of at most `m`
internal changes to absorption.  Consequently the expected internal
absorption time is at most `exp(O(m log m))`.  The probability of a cross
replacement in one update is `O(gamma_m)`.  After a cross introduction, the
probability of a favorable introduction followed by local establishment is
bounded below by a positive constant depending only on fixed `r`; hence the
number of failed introductions before a macro change has bounded geometric
mean.  A union bound therefore gives total time-scale-separation error

\[
 \gamma_m\exp(O(m\log m))=o(m^{-K})
 \quad\text{for every fixed }K.
 \tag{26}
\]

This proves (5)--(6) for the displayed explicit rational graph family, not
merely as an iterated limit.

## 4. Comparison with the complete baseline

Since `M_m(r,q)=1+O(r^{-m})`, equations (5)--(6) give

\[
 \rho_{\rm Bd}(G_m,r)+\rho_{\rm dB}(G_m,r)
 =2a-\frac{a}{m}+O(r^{-m})+o(m^{-K}).
 \tag{27}
\]

The exact complete-graph formulas at order `2m` give

\[
 \rho_{\rm Bd}(K_{2m},r)+\rho_{\rm dB}(K_{2m},r)
 =2a-\frac{a}{2m}+O(r^{-2m}).
 \tag{28}
\]

Subtracting proves (7), and (11) follows from `a=7/16` at `r=16/9`.

## 5. Consequence for the obstruction program

The family proves that the following inference is invalid:

> diffuse support + `c(G_n)->0` + `t_I->1` in `L1` +
> `R_Bd(S)R_dB(S)<=r^3` on every cut
> imply a fixed positive asymptotic deficit in
> `rho_Bd+rho_dB` at some fixed fitness.

All premises available from the inherited local analysis hold here; the
decisive cut asymptotically saturates the product inequality with both biases
strictly larger than `r`; yet the fixation sum approaches the complete sum.

A successful universal obstruction must therefore retain information beyond
those premises.  The remaining possibilities include:

1. resolve the `1/n` correction rather than seek an unscaled deficit;
2. use the strict finite dB-amplification hypothesis itself, not only its
   local consequences;
3. prove a global inter-level or occupation-measure inequality that charges
   every internally equilibrated module for its finite dB loss.

The example actually supports the third possibility: its exact deficit is
`a/n+o(1/n)`, one complete-graph finite-size unit lost at the extra module.
