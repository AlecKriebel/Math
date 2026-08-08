# Endpoint product: variational and orientation branch

Date opened: 2026-08-07 (America/Los_Angeles)

No literature search or external communication was used.

## Exact target

The universal fixation-product inequality at `r=3/2` remains the target.  This
branch studies the first factor in the exact adjoint split.  Let `L` be the Bd
branching--coalescing dual, `C` the same set process after reversing every
underlying arrow, and

\[
 M=(L+C)/2,\qquad K=(L-C)/2.
\]

The midpoint `M` is reversible for

\[
 \mu(A)\mathrel\propto 2^{-|A|},\qquad A\ne\varnothing,
\]

and its stationary mean is the complete-Bd dual mean.  Thus

\[
 m_L+m_C\le 2m_B^K                                      \tag{O}
\]

is an endpoint-versus-midpoint statement for opposite arrow orientations.
It is sufficient for the orientation factor of the product conjecture, but
does not by itself compare `C` with the geometrically batched dB dual.

## 2026-08-07 checkpoint 1: exact orientation calculus

**PROVED.**  Put `P_ij=w_ij/d_i`, `t_i=sum_j P_ji`, and `q_i=1-t_i`.
Undirectedness gives the graph-sensitive divergence identity

\[
 q_i=\sum_j w_{ij}(d_i^{-1}-d_j^{-1}).                 \tag{1}
\]

For the cardinality function `k(A)=|A|` and `a=r-1`, direct evaluation of
the labelled-arrow generators gives

\[
 Kk(A)=-{a\over2}\sum_{i\in A}q_i.                    \tag{2}
\]

For

\[
 F(t,s)=\delta_V e^{t(M+sK)}k,
\]

Duhamel differentiation gives

\[
 \partial_s^2F(t,s)=2\int_{0<u<v<t}
 \delta_Ve^{uQ_s}K e^{(v-u)Q_s}K e^{(t-v)Q_s}k\,du\,dv,\quad
 Q_s=M+sK.                                             \tag{3}
\]

The desired transient strengthening of (O) is

\[
 F(t,1)+F(t,-1)\le2F(t,0)\quad(t\ge0).                \tag{4}
\]

Its initial curvature from the full set is exactly

\[
 {d^2\over dt^2}\{2F(t,0)-F(t,1)-F(t,-1)\}_{t=0}
 ={1\over4}\sum_iq_i^2                                \tag{5}
\]

at `r=3/2`.  Formula (5) is a genuine conductance square and is zero exactly
when `P` is doubly stochastic.

**EXACTLY FALSIFIED SHORTCUT.**  The integrand behind (3) is not pointwise
nonpositive for arbitrary starting sets.  On the connected weighted graph

```text
w_01=1, w_02=1, w_03=1, w_23=3,
all other weights zero,
```

at the singleton set `{3}` one has

\[
 Kq(\{3\})=-1/36,
 \qquad -2K^2k(\{3\})=-1/72<0.                        \tag{6}
\]

Thus neither pointwise semigroup midpoint concavity nor a statewise
second-order square is valid.  Any proof of (4) must use the occupation law
from the full initial set (or an equivalent stationary weighting).

## 2026-08-07 checkpoint 2: transient route exactly closed

**RIGOROUSLY INTERVAL-CERTIFIED COUNTEREXAMPLE.**  The full-start
strengthening (4) is false, even on the unweighted four-vertex star.  Label
the center `3`, so the only edges are `03,13,23`, all of weight one.  At the
exact rational time `t=7/2`, a 200-bit Arb matrix-exponential evaluation of
the independently constructed rational generators gives

\[
\begin{aligned}
 &2\,\delta_Ve^{(7/2)M}k
 -\delta_Ve^{(7/2)L}k
 -\delta_Ve^{(7/2)C}k\\
 &\qquad\in
 [-0.036404663597045702,-0.036404663597045701].       \tag{7}
\end{aligned}
\]

The interval lies strictly below zero.  The same function starts with the
positive curvature (5), becomes negative at intermediate time, and returns
to the positive stationary gap.  Therefore even full-start finite-time
domination is too strong; the surviving orientation route must use the
stationary occupation integral after all transient cancellations.

## Computational status

Before the star was included, (4) survived time grids on P3 and dense
rational graphs; this demonstrates why dense-only screening was inadequate.
The stationary endpoint inequality has survived independent optimization
through order six.  Pointwise-in-`s` concavity of `F(infinity,s)` is false
near `s=1`; only the symmetric stationary endpoint pair remains viable.

`search_transient_midpoint.py` is a hostile floating-point optimizer.
`verify_endpoint_orientation_identities.py` reconstructs (1)--(2), (5), and
the exact witness (6) over rational arithmetic.

## Exact boundary of this branch

- `m_L+m_C<=2m_B^K`: **OPEN**.
- Full-start transient strengthening (4): **FALSIFIED** by the interval
  certificate (7).
- Pointwise-in-initial-state transient strengthening: **FALSIFIED** even
  earlier, by (6) already at second order.
- Universal product inequality: **OPEN**; even a proof of (O) would still
  require the independent batching factor `m_D/m_C`.

Best-guess completion of this orientation subproblem: **35%**.  The correct
gradient invariant is isolated, but both pointwise and transient
strengthenings are now closed.  Only the fully stationary occupation sign
remains plausible.

## 2026-08-07 checkpoint 3: exact directed-tree formulation

**PROVED.**  On the nonempty subset state space put

\[
 \mu(A)=2^{-|A|},\qquad c_{AB}=\mu(A)L_{AB}\quad(A\ne B).
\]

The weighted-adjoint identity gives

\[
 c_{AB}=\mu(B)C_{BA}.                                  \tag{8}
\]

Let `I_c(A)` be the total weight of directed spanning arborescences of `c`
whose arrows point into root `A`, and let `O_c(A)` be the analogous total
for arrows pointing out of `A`.  The Markov-chain tree theorem, with the
factor `mu` extracted once from every nonroot row, gives exactly

\[
 \pi_L(A)={\mu(A)I_c(A)\over\sum_B\mu(B)I_c(B)},\qquad
 \pi_C(A)={\mu(A)O_c(A)\over\sum_B\mu(B)O_c(B)}.       \tag{9}
\]

Thus the orientation inequality is a comparison of the `mu`-weighted root
ranks of the in- and out-arborescence ensembles of one directed network.
The reversible midpoint replaces each directed pair by
`(c_AB+c_BA)/2` and has root law exactly `mu/sum(mu)`.

**EXACTLY FALSIFIED TREEWISE SHORTCUT.**  It is not valid to prove (O) one
underlying spanning tree at a time.  On the unweighted three-path (leaves
`0,1`, center `2`), use subset masks `1,...,7` and the undirected state-space
tree

```text
(1,4), (1,5), (3,6), (5,7), (3,5), (2,6).
```

Orienting this tree into each possible root with the `c` weights gives a
`mu`-weighted mean root rank `7/5`; reversing every arrow gives mean `13/9`.
The midpoint reference mean is `27/19`, and

\[
 2{27\over19}-{7\over5}-{13\over9}=-{2\over855}<0.    \tag{10}
\]

Hence termwise in/out tree reversal has the wrong sign.  Any matrix-tree
proof must use cancellations or exchanges **between different spanning
trees** (equivalently, a forest determinant identity); edgewise AM--GM on a
single tree cannot prove the stationary inequality.

**OPEN.**  Whether the full arborescence sums in (9) admit a two-tree/forest
square after summing over all roots.  Direct determinant tests of the
rootwise inequality
`tau_M(A)^2 >= tau_L(A) tau_C(A)` passed P3 and the audited rational
order-four examples, but that rootwise statement alone would still not
control the normalization-weighted rank mean.

## 2026-08-07 checkpoint 4: root-marked determinant and its exact boundary

For any irreducible row generator `Q`, let `tau_Q(A)` be its Markov-tree
cofactor rooted at `A` and define the root-marked polynomial

\[
 Z_Q(z)=\sum_A\tau_Q(A)z^{|A|}.
\]

**PROVED.**  The stationary rank mean is the logarithmic derivative

\[
 m_Q=\left.z\partial_z\log Z_Q(z)\right|_{z=1}.       \tag{11}
\]

Equivalently, if `R=-Q`, `u(z)_A=z^|A|`, and `e` is any fixed coordinate
vector, the rank-one determinant lemma and
`adj(R)=constant * 1 * tau_Q^T` give

\[
 \det\{R+u(z)e^T\}=constant\cdot Z_Q(z).              \tag{12}
\]

Thus the orientation target is exactly

\[
 \left.z\partial_z\log {Z_M(z)^2\over Z_L(z)Z_C(z)}
 \right|_{z=1}\ge0.                                  \tag{13}
\]

On the unweighted three-path, positive rescalings give

\[
\begin{aligned}
 Z_L(z)&=z(25z^2+150z+273)/8,\\
 Z_C(z)&=125z(5z^2+39z+96)/128,\\
 Z_M(z)&=346275z(z^2+6z+12)/65536,
\end{aligned}
\]

and the numerator in (13), before evaluation at one, is a positive multiple
of

\[
 9z(25z^4+320z^3+1449z^2+2706z+1548).
\]

The resulting physical-mark gap is exactly `243/5320`.

Writing the coefficient vectors of `Z_M,Z_L,Z_C` as `u_k,l_i,c_j`, the
coefficient of total degree `m` in the numerator is exactly

\[
 N_m=\sum_{i+j+k=m}(3k-m)u_kl_ic_j.                  \tag{14}
\]

This is a conditional three-arborescence rank-exchange statement.  It
survives P3, the audited order-four graphs, the four-star, and even the
unweighted five-star where ordinary rank MLR is known to fail.

**EXACTLY FALSIFIED STRENGTHENING.**  Coefficientwise positivity, and hence
the proposed inequality for every mark `z>0`, is false.  A connected
integer-weight order-five witness has

```text
01=1000, 02=1, 04=10, 13=1000, 14=10000,
23=1, 24=1000, 34=1; 03=12=0.
```

For this graph, exact stationary solution gives `N_4<0` and in fact
`N(1/10000)<0`.  Nevertheless `N(1)>0`, so this does not refute the physical
endpoint inequality.  It proves that a forest exchange must use the
unmarked-root summation at `z=1`; it cannot work coefficient by coefficient
in total root rank.

**EXACTLY FALSIFIED STABILITY ROUTE.**  Ordinary real-rootedness of the
one-variable root polynomial fails already for the reversible P3 midpoint:

\[
 Z_M(z)\mathrel\propto z(z^2+6z+12),
\]

whose quadratic discriminant is `-12`.  Stable/real-rooted arguments based
only on this rank variable therefore cannot prove (13).  A multivariate
forest identity remains logically possible.

`verify_root_marked_tree_transform.py` independently rebuilds both rational
generators and their stationary laws, verifies (11)--(14), checks the P3
and five-star values, and preserves the exact integer all-mark counterexample.

### Status after checkpoint 4

- Physical root-mark inequality (13) at `z=1`: **OPEN**.
- Coefficientwise/all-`z` strengthening: **FALSIFIED** exactly at order five.
- One-variable real-rootedness: **FALSIFIED** exactly at the reversible P3
  baseline.
- The still-viable determinant route must be a summed two-tree/forest
  identity specialized to `z=1` (or an equivalent stationary resolvent
  square), not a treewise, rankwise, or stability argument.

## 2026-08-08 checkpoint 5: stationary orientation interpolation

For `-1<=s<=1`, define

\[
 Q_s=M+sK,
 \qquad m(s)=\mathbb E_{\pi_s}|A|.
\]

The endpoint orientation target is the `s=1` instance of the stronger
stationary chord conjecture

\[
 \boxed{m(s)+m(-s)\le2m(0)\quad(0\le s\le1).}        \tag{15}
\]

This is not ordinary concavity: `m''(s)` has the wrong sign on exact and
numerical examples near an endpoint.  It is only the chord centered at the
reversible midpoint.

### 5.1 Exact resolvent and tree formulations

Let `G=(-M)^#` be the mean-zero group inverse and put `B=KG`.  Directly
solving the stationary equation gives

\[
 \pi_s=\mu(I-sB)^{-1},
\]

and hence

\[
 m(s)+m(-s)-2m(0)
 =2s^2\mu B^2(I-s^2B^2)^{-1}k.                       \tag{16}
\]

Individual even Taylor coefficients in (16) do **not** have one sign; an
extreme rational-nearby order-four graph already has positive fourth and
sixth coefficients.  Thus (15), if true, uses the full resolvent.

There is also an exact positive tree expansion.  Put `x=(1+s)/2` and expand
each arborescence edge of `Q_x=xL+(1-x)C` by choosing its `L` or `C` term.
If a labelled expanded tree has `p` L-choices out of `D=2^n-2` edges, then

\[
 T(x)=\sum_p t_p x^p(1-x)^{D-p},\qquad
 Y(x)=\sum_p y_p x^p(1-x)^{D-p},\qquad t_p,y_p>0,
\]

and `m(s)=Y(x)/T(x)`.  Equivalently, with
`theta=atanh(s)`, `m(s)` is the mean root rank in an exponential tilt by
the orientation score `2p-D`.  Formula (15) asks that the sum of the two
opposite score tilts never exceed the untilted root-rank mean.  Simple
monotonicity or concavity of the conditional regression `y_p/t_p` has not
been established.

The cleared numerator

\[
 2m(0)T(s)T(-s)-Y(s)T(-s)-Y(-s)T(s)                \tag{17}
\]

is an even polynomial.  Exact Bareiss determinants give nonnegative
Bernstein coefficients after writing it in `y=s^2` on all of the following
hostile instances:

- unweighted P3;
- the unweighted four-star and five-star;
- the sparse integer K4 statewise-curvature witness;
- the extreme integer order-five counterexample to the all-root-mark
  strengthening;
- sixty independently generated connected integer-weight order-five
  graphs with weights spanning up to five orders of magnitude.

This is **EXACT COMPUTATIONAL EVIDENCE**, not a universal coefficient
theorem.

For the weighted path with edge weights `1,17`, exact determinant reduction
reproduces

\[
 m(s)=\frac{9(6069s^5+127993s^4-10128106s^3+37489390s^2
                 +226502325s-378102375)}
 {(s-15)(119s^2+804s-12635)(119s^2+6564s-12635)}.
\]

The reduced numerator of (15) is

\[
 -72s^2(257829327s^8-836686233964s^6+294010589876522s^4
 -26138588919354700s^2+512931826072509375),          \tag{18}
\]

over the exact denominator recorded in the verifier.  The bracket in (18)
is positive on `|s|<=1` even after discarding its two positive nonconstant
terms; the denominator has the opposite sign.  Hence this weighted-path
interpolation is **PROVED** for the full interval.

### 5.2 New skew/defect square

The weighted adjoint relation sharpens as follows.  Let

\[
 V(A)=\frac32\sum_{i\in A}q_i,
 \qquad J=K-\frac12V.
\]

Here `V` denotes the diagonal multiplication operator.  Then

\[
 K^{\dagger_\mu}=-K+V,
 \qquad J^{\dagger_\mu}=-J.                          \tag{19}
\]

Normalize the stationary densities by
`f_s=pi_s/mu`, `f_{-s}=pi_{-s}/mu`.  Their exact ground-state equations are

\[
 (M-sJ+sV/2)f_s=0,
 \qquad(M+sJ-sV/2)f_{-s}=0.                          \tag{20}
\]

Taking the `mu` inner product of the first equation with `f_{-s}` and of
the second with `f_s`, then using self-adjointness of `M` and
skew-adjointness of `J`, proves the new exact orthogonality

\[
 \boxed{\langle V f_s f_{-s}\rangle_\mu=0.}          \tag{21}
\]

Taking the two equations against their own densities gives genuine
Dirichlet squares:

\[
 \boxed{
 {s\over2}\langle V f_s^2\rangle_\mu
 =-\langle f_s,Mf_s\rangle_\mu\ge0,
 \qquad
 -{s\over2}\langle V f_{-s}^2\rangle_\mu
 =-\langle f_{-s},Mf_{-s}\rangle_\mu\ge0.}          \tag{22}
\]

Equations (21)--(22) survive every earlier pointwise and transient witness
and expose the defect as a skew-ground-state energy rather than a signed
local correction.  They do not yet imply the rank sign in (15): `V` has
zero uniform average separately on every rank, so a quantitative trace or
two-particle Picone inequality is still required to convert the energy
into `\langle |A|,2-f_s-f_{-s}\rangle_mu>=0`.

**EXACTLY FALSIFIED RANK-TAIL STRENGTHENING.**  Even the centered endpoint
mixture need not be first-order stochastically dominated by `mu` in rank.
Take the connected integer graph

```text
01=2, 02=227000, 12=536000, 13=5, 14=85,
23=941000, 24=650000, 34=1; 03=04=0.
```

At the exact interpolation value `s=1/5`, exact 31-state rational solves
give

\[
 {\pi_s(V)+\pi_{-s}(V)\over2}-\mu(V)
 \in(4\cdot10^{-6},5\cdot10^{-6}),                  \tag{23}
\]

so the top cumulative tail has the wrong sign.  At the same time,

\[
 m(0)-{m(s)+m(-s)\over2}\in(0.003,0.004),            \tag{24}
\]

strictly in the conjectured direction.  Thus neither individual rank
deficits nor cumulative rank-tail flow can prove (15); cancellations among
rank tails are essential.  The verifier checks both intervals over exact
rationals.

`verify_stationary_interpolation.py` constructs (17) directly from exact
Markov-tree determinants, verifies the displayed weighted-P3 rational
function and its interval sign, and independently checks (19)--(22) at a
rational interior interpolation point.

### Status after checkpoint 5

- Stationary centered interpolation (15): **OPEN universally**, proved on
  the exact instances listed above.
- Endpoint orientation arithmetic inequality: **OPEN** (it is `s=1`).
- Geometric-product orthogonality and Dirichlet identities (19)--(22):
  **PROVED** for every finite graph and every `0<s<=1`.
- First-order stochastic domination of the centered rank law: **FALSIFIED**
  exactly at order five by (23), without falsifying the scalar mean.
- Universal product inequality still additionally requires the independent
  batching comparison after orientation closure.

## 2026-08-08 checkpoint 6: electrical two-tree transfer reduction

The tree pair can be compressed further into one exact electrical trace.
Let `X` denote the nonempty subset state space and retain the normalized
midpoint mass `mu`.  For `x!=y`, put

\[
 c_{xy}=\mu_xM_{xy}=c_{yx},\qquad
 j_{xy}=\mu_xK_{xy}=-j_{yx}.
\]

Choose one orientation `x_e,y_e` of every undirected state edge and form the
ordinary and signless incidence columns

\[
 a_e=e_{x_e}-e_{y_e},\qquad b_e=e_{x_e}+e_{y_e}.
\]

Let `A,B` collect these columns and let `J_e=diag(j_e)`.  If
`H=diag(mu)(-M)` is the symmetric conductance Laplacian, direct assembly of
each two-state block proves

\[
 \boxed{\operatorname{diag}(\mu)(-Q_s)
       =H+sBJ_eA^T.}                                  \tag{25}
\]

The appearance of the signless incidence matrix is the exact diagonal
divergence that defeated a purely skew determinant argument.

For a root field `t`, set

\[
 W_t=\operatorname{diag}(\mu_xe^{t|x|}),\qquad
 F_s(\epsilon,t)=\det(H+\epsilon W_t+sBJ_eA^T).
\]

The linear matrix-forest coefficient is

\[
 F_s(\epsilon,t)
 =\epsilon\Big(\prod_x\mu_x\Big)
   \sum_x\tau_s(x)e^{t|x|}+O(\epsilon^2),             \tag{26}
\]

so the stationary rank mean is the `t` logarithmic derivative of this
coefficient.  For positive `epsilon`, put

\[
 G_{\epsilon,t}=(H+\epsilon W_t)^{-1},\qquad
 X_{\epsilon,t}=J_eA^TG_{\epsilon,t}B.
\]

The determinant lemma gives the exact two-tree identity

\[
 \boxed{
 {F_s(\epsilon,t)F_{-s}(\epsilon,t)\over F_0(\epsilon,t)^2}
 =\det(I-s^2X_{\epsilon,t}^2).}                       \tag{27}
\]

This identity is valid before taking either singular limit and contains all
cross-tree exchanges automatically.

The singular limit also has a closed form.  Let `H#` be the symmetric group
inverse, `1_E` the all-one edge vector, and

\[
 B_c=B-2\mu1_E^T,
 \quad X=J_eA^TH^\#B_c,
 \quad H\phi=\mu(|x|-m(0)),
 \quad u=J_eA^T\phi.
\]

Expanding the killed Green function at `epsilon=0` shows that the root-field
derivative of `X` is the rank-one matrix

\[
 \left.\partial_tX_{\epsilon,t}\right|_{t=0,\epsilon\downarrow0}
 =-2u1_E^T.                                           \tag{28}
\]

(`mu` is normalized; otherwise divide the right side by `sum(mu)`.)  Taking
the derivative in (27) now proves the exact equivalence

\[
 \boxed{
 m(s)+m(-s)-2m(0)
 =4s^2 1_E^TX(I-s^2X^2)^{-1}u.}                     \tag{29}
\]

Consequently the universal interpolation theorem is equivalent to the one
electrical sign

\[
 1_E^TX(I-s^2X^2)^{-1}u\le0.                         \tag{30}
\]

This is not yet a proof: `X` is generally nonnormal, the symmetric part of
`(I-s^2X^2)^(-1)` is already indefinite on connected order-four graph
examples, and individual even resolvent coefficients can have both signs.
Thus ordinary PSD, singular-value, and termwise Neumann-series arguments do
not establish (30).  The remaining usable structure is that `J_e` is the
sum of the labelled three-state circulation blocks induced by original
undirected graph edges, with

\[
 K|A|=-V(A)/6
\]

at `r=3/2`.  Any final square must exploit this set-lattice circulation
identity; (25)--(30) are false as sign statements for a generic directed
state network.

`verify_forest_transfer_reduction.py` checks (25)--(29) on the weighted
`1:17` path entirely over exact rationals.  In particular its independently
computed transfer scalar equals the directly solved stationary chord

\[
 -{189475553746489491137376\over
 1108033745563239785565715}<0.
\]

### Frozen Gate-2 boundary

- Universal endpoint product inequality: **OPEN**.
- Universal orientation arithmetic inequality `m_L+m_C<=2m(0)`: **OPEN**.
- Centered stationary interpolation (15): **OPEN**, with extensive exact
  and numerical support and no counterexample.
- Electrical determinant and scalar reductions (25)--(30): **PROVED**.
- Full-start transient interpolation: **FALSIFIED** by an interval-certified
  counterexample on the four-vertex star `K_{1,3}`.
- Statewise curvature, single-tree reversal, all-root-mark,
  real-rootedness, termwise even-resolvent, and rank-tail strengthenings:
  **FALSIFIED** by the exact witnesses recorded above.
- Even if orientation is closed, the independent C-to-dB batching factor is
  still required for the full fixation-product theorem.
