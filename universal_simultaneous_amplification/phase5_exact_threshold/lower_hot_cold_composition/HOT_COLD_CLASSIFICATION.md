# Exact hot--cold two-stage classification

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Scope and conclusion

This note classifies the minimal two-stage diffuse branching composition in
which a singular cold Bd-gain type feeds a non-cold type, and the non-cold
type communicates with a neutral bulk.  It is the first positive-temperature
escape from the saturated cold-root calculation.

The outcome is a no-go for this exact composition.  The response splits as

\[
 (G,C)=\left({x\over r},x{r-1\over r}\right)+(-E_B,E_D),
 \qquad E_B,E_D\geq0,                                      \tag{1}
\]

where `G` is Bd gain and `C` is dB cost.  Thus whenever `G>0`,

\[
                         {C\over G}\geq r-1.                \tag{2}
\]

The hot stage cannot improve the cold constituent's ratio; it can only
reduce Bd gain and increase dB cost.  Equality requires the hot remainders
to vanish.

This does **not** exclude every two-stage hierarchy.  It identifies the
exact missing feature: a genuine compensating stage must have a *signed*
response, with positive dB response at the same order, and must beat the
fractional-linear condition in Section 5.  The canonical non-cold relay
below has the opposite sign.

### Exact adjoint involution

There is a useful global check on what “complementary” means.  For any
normal form `(p,P)`, set

\[
 R=D_p^{-1}P^TD_p,qquad t=R\mathbf1,qquad
 p'=p\odot t,qquad P'=D_t^{-1}R.                          \tag{2a}
\]

Since `sum_i p_i t_i=1`, `p'` is a probability law.  Direct calculation
gives

\[
 R'=D_{p'}^{-1}P'^TD_{p'}=D_t^{-1}P,qquad t'=1/t.         \tag{2b}
\]

Consequently the two branching endpoint systems swap exactly:

\[
                         b'=s,qquad s'=b.                  \tag{2c}
\]

The transform is realizable whenever `P` comes from symmetric weights.
But its averaging law is `p'=p odot t`, not `p`.  Thus adjoining an
adjoint-complementary layer is not a free cancellation: it reweights starts
toward hot types and away from cold ones.  Equations (11)--(12) are the
triangular instance of that unavoidable averaging correction.

## 2. Canonical reversible triangular trace

Fix `r>1` and write

\[
                         p_0={r-1\over r}.                   \tag{3}
\]

At first order in a dilute mass parameter, use three roles:

- neutral bulk `O`;
- a cold gain type `C` of mass `epsilon x`;
- a hot relay type `H` of mass `epsilon`.

The limiting forward arrows are

\[
 P_C(H)=1,
 \qquad P_H(H)=h,
 \qquad P_H(O)=1-h,                                        \tag{4}
\]

where `0<=h<1`.  Let the first-order bulk-to-hot flow be `epsilon a`.
Reversibility then fixes the hot temperature and its reverse split:

\[
                         t_H=h+a,
 \qquad R_H(H)=h,
 \qquad R_H(O)=a.                                          \tag{5}
\]

The cold type has no same-order incoming flow, so `t_C->0`.  Its outgoing
arrow remains live through `H`; hence

\[
                         (b_C,s_C)=(1,0).                   \tag{6}
\]

The hot endpoint coordinates `b,s in (0,1)` solve exactly

\[
 (h+a+x)b=r(1-b)\{hb+(1-h)p_0\},                           \tag{7}
\]

\[
 s=r(1-s)\{hs+ap_0\}.                                     \tag{8}
\]

These are the two scalar quadratic traces remaining after the cold and bulk
coordinates have been eliminated.  All parameters are nonnegative.

## 3. Uniform-start response and exact squares

Linearizing the bulk coordinate as required by uniform initialization and
summing the three starting roles gives the total first-order response

\[
 G={x\over r}+{ab\over r-1}+b-1+{h\over r},                \tag{9}
\]

\[
 C=x{r-1\over r}+{a+r-1\over r}
       -{r-h\over r-1}s.                                  \tag{10}
\]

The terms outside the displayed cold ray are not optional: they are the
hot singleton and bulk-coordinate corrections imposed by reversibility.

Eliminate `a` from (7).  A direct factorization gives

\[
 \boxed{
 {x\over r}-G
 ={x b r+h(rb-r+1)^2\over r(r-1)}=:E_B\geq0.}              \tag{11}
\]

Eliminate `a` from (8).  Another direct factorization gives

\[
 \boxed{
 C-x{r-1\over r}
 ={(rs-r+1)^2\over r(r-1)(1-s)}=:E_D\geq0.}                \tag{12}
\]

Equations (1)--(2) follow immediately.  More precisely,

\[
 C-(r-1)G=E_D+(r-1)E_B\geq0.                              \tag{13}
\]

So the constituent-minimum theorem holds here in its sharp form: the cold
constituent has ratio `r-1`, while the canonical hot stage contributes the
adverse vector `(-E_B,E_D)`.  This is stronger than merely saying that a
positive linear combination has ratio at least the smallest constituent
ratio.

Equality in (13) requires `E_B=E_D=0`.  With `x>0` this is impossible in
the strict interior because (11) contains `xbr>0`; equality is accessible
only on a further singular boundary.  A finite non-cold relay therefore
strictly worsens the cold ray.

## 4. Positive-matrix and fractional-linear principle

For comparison, let two genuine gain/cost constituents be

\[
                         v_j=(G_j,C_j),\qquad G_j>0, C_j\geq0.
\]

Every positive diagonal rescaling and nonnegative mixture has

\[
 {\sum_j w_jC_j\over\sum_j w_jG_j}
 =\sum_j {w_jG_j\over\sum_lw_lG_l}{C_j\over G_j},          \tag{14}
\]

so its ratio lies between the constituent ratios.  Equivalently, the
projective action of a nonnegative `2 by 2` matrix

\[
 M=\begin{pmatrix}\alpha&\beta\\ \gamma&\delta\end{pmatrix}
\]

on a ray of ratio `q=C/G` is the fractional-linear map

\[
                         T_M(q)={\gamma+\delta q\over
                                      \alpha+\beta q}.      \tag{15}
\]

There is no universal assertion that `T_M(q)` exceeds the minimum of all
four matrix-entry ratios: cross-coordinate transfer can change the ray.
The correct exact comparison with an input ratio `q` is

\[
 T_M(q)<q
 \quad\Longleftrightarrow\quad
 \boxed{\beta q^2+(\alpha-\delta)q-\gamma>0},              \tag{16}
\]

provided `alpha+beta q>0`.  Thus a positive matrix improves a ratio only if
its gain-side transfer is sufficiently stronger than its adverse-side
transfer.  Formula (13) proves that the canonical reversible hot stage does
not meet this condition after all uniform-start corrections are included.

## 5. Exact condition for a genuine signed compensator

Suppose a cold gain ray `(G_c,C_c)` with `G_c>0,C_c>0` is combined with a
hot response `(G_h,C_h)` at nonnegative weight `lambda`.  If `G_h>=0` and
`C_h>=0`, (14) applies.  Ratio improvement below the cold ratio
`q_c=C_c/G_c` is possible only through a signed compensator.  Exactly,

\[
 {C_c+\lambda C_h\over G_c+\lambda G_h}<q_c
 \quad\Longleftrightarrow\quad
 \boxed{C_hG_c<C_cG_h},                                   \tag{17}
\]

as long as `G_c+lambda G_h>0`.  If the desired compensator has
`G_h<0,C_h<0`, this becomes

\[
                         {|C_h|\over|G_h|}>q_c,             \tag{18}
\]

and the admissible weights satisfy

\[
 0<\lambda< {G_c\over|G_h|}.                               \tag{19}
\]

Cancellation of the entire cold cost uses

\[
 \lambda_*={C_c\over|C_h|},
\]

and leaves positive gain exactly when (18) holds.  This is the symbolic
target for a true hot compensator: it must return more dB benefit per unit
of Bd damage than the cold layer's cost/gain ratio.

The canonical relay (11)--(12) instead has signed increment
`(G_h,C_h)=(-E_B,+E_D)`.  Its dB coordinate has the wrong sign, so (17)
cannot hold.

## 6. Endpoint quantifiers and the actual lower target

An endpoint-uniform catalyst with `C_k(r)/G_k(r)->0` up to `r=2` is not the
required target and is expected to conflict with the proposed `r=2` PAPT
upper theorem.  The lower construction may be nonuniform at the endpoint.
It needs

\[
 {C_k(r)\over G_k(r)}\longrightarrow0
 \quad\hbox{for every fixed }1<r<2,                         \tag{20}
\]

while allowing

\[
                         {C_k(2)\over G_k(2)}\geq1.          \tag{21}
\]

The model behavior is `(r-1)^{L_k}` for fixed `r<2`: it tends to zero as
depth grows but remains one at `r=2`.

Equations (11)--(13) show why affine uniform-start mixing cannot generate
this boundary layer.  A viable two-stage construction must exponentiate a
*conditional adverse passage probability* along a locked history.  Each
successful level must transmit the Bd event while charging the dB adverse
event only if it passes every level.  Positive addition of initialization
masses, or a relay whose correction is `(-E_B,+E_D)`, cannot do this.

Accordingly the proof-first construction target is now narrow: find a
reversible, finite-trace stage whose conditional projective map obeys (16)
for `1<r<2`, tends to equality at `r=2`, and composes before uniform-start
averaging.  Only then can iteration produce the necessary nonuniform power.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_hot_cold_classification.py
```

The replay derives (9)--(13) from the two endpoint equations and checks the
adjoint involution, fractional-linear, and signed-compensator criteria
symbolically.
