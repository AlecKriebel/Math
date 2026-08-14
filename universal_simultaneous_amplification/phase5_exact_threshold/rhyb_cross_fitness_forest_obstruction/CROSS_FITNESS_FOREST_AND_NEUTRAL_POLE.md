# Cross-fitness forests and the neutral-pole obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## Status

This note proves three exact statements.

1. For either Bd or dB updating on an arbitrary finite connected weighted
   graph, fixation is a ratio of two directed two-root forest sums.  Its
   fitness derivative is exactly a covariance between the fixation-root
   mark and an additive forest likelihood score.
2. The normalized endpoint support

   \[
   G_{dB}(R)+(R-1)G_{Bd}(R)
   \]

   has one exact denominator-cleared expression involving the two full
   subset-forest determinants and their two root-marked numerators.
3. A derivative-at-neutrality interpolation cannot, by itself, handle the
   quantifiers in the definition of `R_sim`.  The already proved dilute
   pair--leaf diagonal has a scaled Bd response with an exact
   `lambda_*/(r-1)` pole, although every finite member has an analytic gain
   which vanishes at `r=1`.  Consequently no uniform first-order bound from
   `r=1` survives this diagonal.

The last statement is a rigorous nonuniformity obstruction, not a
counterexample to the finite-graph disjunction

\[
 \min\{G'_{Bd}(1+),G'_{dB}(1+),
        G_{dB}(R_{hyb})+(R_{hyb}-1)G_{Bd}(R_{hyb})\}\leq0. \tag{D}
\]

That disjunction remains open.  Even if `(D)` were proved for every finite
graph, an additional scale-uniform theorem would be needed before it could
bound `R_sim`.  A comparison based at one fixed `r_0>1`, rather than at the
singular neutral boundary, remains a viable but open cross-fitness route.

## 1. The two update generators

Let `G=(V,w)` be finite, connected, loopless, and undirected.  Write

\[
 d_j=\sum_iw_{ij},\qquad
 W_j(A)=\sum_{i\in A}w_{ij}.                              \tag{1}
\]

The mutant set is `A`.  Multiplying every rate out of one state by the same
positive number does not change a fixation committor, so convenient
continuous-time row gauges may be used.

For Bd updating, take

\[
 q_B(A,A\cup\{j\};r)
   =r\sum_{i\in A}{w_{ij}\over d_i},\qquad j\notin A,    \tag{2}
\]

\[
 q_B(A,A\setminus\{j\};r)
   =\sum_{i\notin A}{w_{ij}\over d_i},\qquad j\in A.    \tag{3}
\]

For dB updating, take

\[
 q_D(A,A\cup\{j\};r)
 ={rW_j(A)\over d_j+(r-1)W_j(A)},\qquad j\notin A,       \tag{4}
\]

\[
 q_D(A,A\setminus\{j\};r)
 ={d_j-W_j(A)\over d_j+(r-1)W_j(A)},\qquad j\in A.       \tag{5}
\]

The omitted target factor `1/|V|` is common to the whole dB row.  Equations
`(2)`--`(5)` therefore give the standard fixation probabilities.

Let

\[
 \Omega=\{A:\varnothing\ne A\ne V\}.
\]

For either rule, define the transient Dirichlet matrix and fixation-boundary
column by

\[
 L_U(r)=-Q_U(r)|_{\Omega\times\Omega},\qquad
 c_U(r)=Q_U(r)|_{\Omega\times\{V\}}.                    \tag{6}
\]

Connectedness makes `L_U(r)` a nonsingular M-matrix for every `r>0`.
If `s_A=|V|^{-1}` on singleton states and zero otherwise, then

\[
 h_U(r)=L_U(r)^{-1}c_U(r),\qquad
 \rho_U(G,r)=s^Th_U(r).                                  \tag{7}
\]

This is the determinant starting point; it has no approximation and no
population-size restriction.

## 2. Exact two-root forest law

Adjoin the two absorbing roots `0=emptyset` and `1=V`.  Let
`mathcal F_U` be the directed spanning forests in which every transient
state has one outgoing edge, each root has none, and every directed path
ends at one of the two roots.  For a forest `F`, put

\[
                         w_{U,r}(F)=\prod_{e\in F}q_U(e;r). \tag{8}
\]

The directed matrix-forest theorem and its root-marked version give

\[
 \Delta_U(r):=\det L_U(r)=\sum_{F\in\mathcal F_U}w_{U,r}(F)>0, \tag{9}
\]

\[
 N_U(r):=s^T\operatorname{adj}(L_U(r))c_U(r)
 ={1\over |V|}\sum_{i\in V}\sum_{F\in\mathcal F_U}
 w_{U,r}(F)\,\mathbf1\{\{i\}\longrightarrow V\},       \tag{10}
\]

and hence

\[
                         \boxed{\rho_U(G,r)={N_U(r)\over\Delta_U(r)}.} \tag{11}
\]

For dB, the rates in `(4)`--`(5)` are rational in `r`, but this does not
weaken the polynomial interpretation.  Multiply the row at `A` by

\[
 \gamma_A(r)=\prod_{j\in V}\{d_j+(r-1)W_j(A)\}
             =\prod_{j\in V}\{d_j-W_j(A)+rW_j(A)\}.      \tag{12}
\]

Every cleared transition rate is then a polynomial in `r` with nonnegative
coefficients.  Every forest contains exactly one edge out of each transient
state, so this row gauge multiplies both `N_D` and `Delta_D` by the same
positive factor

\[
                         \prod_{A\in\Omega}\gamma_A(r).
\]

Thus `(11)` is also a ratio of positive dB forest polynomials after a
canonical clearing.

## 3. The exact neutral covariance

Choose `F` with probability `w_{U,r}(F)/Delta_U(r)`, choose `i` uniformly
and independently from `V`, and define

\[
 I(F,i)=\mathbf1\{\{i\}\longrightarrow V\},\qquad
 Z_{U,r}(F)=\partial_r\log w_{U,r}(F).                    \tag{13}
\]

Differentiating the finite forest sums in `(9)`--`(11)` gives the exact
score identity

\[
 \boxed{
 \rho'_U(G,r)=\operatorname{Cov}_{U,r}(I,Z_{U,r}).}       \tag{14}
\]

At neutrality the individual edge scores are especially simple.  For Bd,

\[
 \left.\partial_r\log q_B(e;r)\right|_{r=1}
 =\begin{cases}1,&e\text{ increases }|A|,\\0,&e\text{ decreases }|A|.
 \end{cases}                                             \tag{15}
\]

Therefore `Z_{B,1}` is the number of upward edges in the forest.  For dB,
an edge which changes target `j` from state `A` has

\[
 \left.\partial_r\log q_D(e;r)\right|_{r=1}
 =\mathbf1\{e\text{ increases }|A|\}-{W_j(A)\over d_j}. \tag{16}
\]

Equations `(14)`--`(16)` retain the entire signed target information.  A
positive row gauge adds the deterministic number
`sum_A gamma'_A(1)/gamma_A(1)` to every forest score, which does not change
the covariance.  Thus the formula is gauge invariant.

Under uniform initial mutation, neutrality gives `rho_U(G,1)=1/|V|` for
both rules.  For the complete graph of order `n`, write

\[
 \kappa_B^{(n)}(r)={1-r^{-1}\over1-r^{-n}},\qquad
 \kappa_D^{(n)}(r)={n-1\over n}{1-r^{-1}\over1-r^{1-n}}. \tag{17}
\]

Their removable neutral derivatives are

\[
 (\kappa_B^{(n)})'(1)={n-1\over2n},\qquad
 (\kappa_D^{(n)})'(1)={n-2\over2n}.                      \tag{18}
\]

For normalized gains

\[
 G_U(G,r)={\rho_U(G,r)\over\kappa_U^{(n)}(r)}-1,         \tag{19}
\]

the exact weak responses are consequently

\[
 G'_B(G,1)=n\left\{\operatorname{Cov}_{B,1}(I,Z_{B,1})
                         -{n-1\over2n}\right\},          \tag{20}
\]

\[
 G'_D(G,1)=n\left\{\operatorname{Cov}_{D,1}(I,Z_{D,1})
                         -{n-2\over2n}\right\}.          \tag{21}
\]

These are exact forest/determinant forms for the two neutral observables in
`(D)`.

## 4. Exact endpoint clearing

Fix `R>1` and abbreviate

\[
 \Delta_U=\Delta_U(R),\quad N_U=N_U(R),\quad
 \kappa_U=\kappa_U^{(n)}(R),\quad c=R-1.                 \tag{22}
\]

The normalized leaf-annihilating endpoint score is

\[
 \mathcal S_R(G)=G_D(G,R)+cG_B(G,R).                     \tag{23}
\]

Using `(11)` and multiplying by the positive denominator
`kappa_B kappa_D Delta_B Delta_D` gives

\[
\boxed{
 \begin{aligned}
 \mathcal E_R(G)
   &:={\kappa_B\kappa_D\Delta_B\Delta_D}\,\mathcal S_R(G)\\
   &=\kappa_B\Delta_BN_D
     +c\kappa_D\Delta_DN_B
     -(1+c)\kappa_B\kappa_D\Delta_B\Delta_D.
 \end{aligned}}                                         \tag{24}
\]

Thus `S_R` and `E_R` have exactly the same sign.  Formula `(24)` is the
minimal paired-forest endpoint object: it couples one Bd forest and one dB
forest, and its last term is the complete-reference product.

For additive rather than normalized gains, the analogous clearing is

\[
 \Delta_BN_D+c\Delta_DN_B
 -(\kappa_D+c\kappa_B)\Delta_B\Delta_D.                  \tag{25}
\]

At `R=R_hyb`, the sextic

\[
 P(R)=R^6-8R^5+22R^4-30R^3+21R^2-6R+1                  \tag{26}
\]

only specifies the scalar evaluation point in `(24)`.  No factor `P(R)` is
created by the universal forest identity.  The sextic came from the sharp
pair--leaf tangency; a universal cross-fitness proof would have to introduce
its sign through a new comparison between the two marked forest laws.

There is also the taut but useful integral form

\[
 \mathcal S_R(G)=\int_1^R
 \{G'_D(G,t)+(R-1)G'_B(G,t)\}\,dt.                       \tag{27}
\]

A positive-weight integral therefore does not remember separately whether
`G'_B(1)` and `G'_D(1)` are both positive.  Any proof of `(D)` from `(27)`
would need a genuinely two-coordinate evolution theorem, not just a scalar
forest-moment inequality.

## 5. The exact neutral-pole obstruction

The proved dilute pair--leaf family supplies the decisive quantifier test.
Let `G_k` be the fitness-independent diagonal from
`phase4_landmark_closure/threshold/dilute_pair_leaf_hybrid/`, let
`n_k=|G_k|`, and let `delta_k=q_k/n_k` be its pair density.  Define its
scaled normalized responses by

\[
 F_{U,k}(r)={1\over\delta_k}
 \left\{{\rho_U(G_k,r)\over\kappa_U^{(n_k)}(r)}-1\right\}. \tag{28}
\]

The proved diagonal limit is locally uniform on every compact subinterval
of `(1,R_hyb)` and gives

\[
 F_{B,k}(r)\longrightarrow
 B(r;\sigma_*,\lambda_*)
 ={2(\sigma_*-1)\over1+\sigma_*(r^2-1)}
   +{\lambda_*\over r-1},                               \tag{29}
\]

\[
 F_{D,k}(r)\longrightarrow
 D(r;\sigma_*,\lambda_*)
 ={2\{r(2-r)-\sigma_*\}\over\sigma_*+2r(r-1)}
   -\lambda_*.                                          \tag{30}
\]

Here `lambda_*>0`.  Hence

\[
 \boxed{\lim_{r\downarrow1}(r-1)B(r;\sigma_*,\lambda_*)
       =\lambda_*>0.}                                    \tag{31}
\]

On the other hand, every finite `F_{B,k}` is analytic at `r=1` and

\[
                              F_{B,k}(1)=0.               \tag{32}
\]

This proves a sharp failure of uniform neutral control.  For every
`eta>0`, every `0<C<infinity`, and every index `K`, there are `k>=K` and
`r in (1,1+eta)` such that

\[
                         |F_{B,k}(r)|>C(r-1).              \tag{33}
\]

Indeed, choose a fixed sufficiently small `delta in (0,eta)` so that the
right side of `(29)` at `1+delta` exceeds `2Cdelta`; this is possible by
`(31)`.  The pointwise consequence of the compact-uniform diagonal limit
then gives `F_{B,k}(1+delta)>Cdelta` for every sufficiently large `k`, which
contradicts the proposed bound.  By the mean-value theorem, `(32)`--`(33)`
also imply

\[
 \sup_{k\ge K}\sup_{1<r<1+\eta}|F'_{B,k}(r)|=\infty.     \tag{34}
\]

This is not a technical loss in a Taylor estimate.  The pole in `(29)` is
the exact ordinary-leaf response which is essential to the construction
attaining `R_hyb`.

## 6. Consequence for a proof of the exact threshold

The neutral forest covariance `(20)`--`(21)` is exact for each fixed graph,
and the endpoint determinant `(24)` is exact for the same graph.  What
fails is passage from the former to the asymptotic fixed-fitness
quantifiers.  A graph sequence can have a neutral boundary layer whose
width shrinks with its response scale.  Amplification at every fixed
`r>1` is then compatible with behavior arbitrarily close to neutrality
which is invisible after the diagonal limit.

Accordingly, a proof of `(D)` would not alone prove
`R_sim<=R_hyb`.  It would need a separate theorem which prevents the
neutral layer from collapsing.  The natural uniform first-order version of
such a theorem is exactly false by `(33)`.

The smallest cross-fitness target not defeated by this obstruction uses a
fixed fitness `r_0>1`:

\[
 \min\{G_B(G,r_0),G_D(G,r_0),
        G_D(G,R_hyb)+(R_hyb-1)G_B(G,R_hyb)\}\le0.         \tag{35}
\]

For an asymptotically universal family, both first coordinates in `(35)`
are eventually positive.  Thus `(35)`, in a sequence-uniform form, would
give the required endpoint contradiction.  Proving it would require a
nonlinear comparison of forest laws at two fixed fitnesses; neither
`(14)` nor coefficient positivity of the separate forest polynomials
provides that comparison.

The rigorous bound therefore remains

\[
                         R_{hyb}\le R_{sim}\le\infty.
\]

## 7. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_cross_fitness_forest_obstruction/verify_cross_fitness_forest_obstruction.py
```

The replay uses one symbolic weighted three-path only as a determinant
sanity check.  It performs no graph enumeration or parameter search.  It
checks the two Dirichlet systems, adjugate forest ratios, weak derivatives,
dB edge scores, endpoint clearing, the hybrid root isolation, and the exact
leaf pole.
