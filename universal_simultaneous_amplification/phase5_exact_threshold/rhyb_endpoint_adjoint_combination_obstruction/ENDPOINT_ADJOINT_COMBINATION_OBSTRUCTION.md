# A temperature-adjoint scalar-combination obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, numerical optimization, literature search, or
external communication was used.

## 1. Status and scope

**PROVED: A NARROW PROOF-ROUTE OBSTRUCTION.**  Fix

\[
                         {3\over2}\leq r\leq {151\over100},
 \qquad c=r-1.
\]

For reversible adjoint endpoint data, put

\[
 h_1={1\over1+rcRq},\qquad d=cq-s,
\]

and let

\[
 G=E_p(h-h_1).
\]

The still-open endpoint-versus-first-orbit target is `G>=0`.  The exact
reciprocal identity

\[
 \boxed{
 G=rE_p\{dP(h_1^2)\}
      +E_p\!\left[{(h-h_1)^2\over h}\right]}             \tag{1}
\]

retains a positive square.  Applying the proved scaled-first theorem after
temperature adjunction gives a second scalar inequality.  Nevertheless:

> After passing to the quadratic tangent and projecting away all endpoint
> data except the two mean residuals, no nonnegative scalar combination of
> the original and temperature-adjoint scaled-first sign rows implies
> `G_2>=0`.

The obstruction is exact and already appears in the quadratic tangent of a
physical reversible two-state family.  Both orientations acquire the same
strictly negative remainder.  Nonnegative averaging therefore cannot cancel
it.

This is only a conic/projection obstruction.  It does **not** refute `G>=0`,
and it does not obstruct a proof that retains additional endpoint structure,
state-dependent information, or a stronger quantitative form of the
scaled-first theorem.  In fact, the physical family used below has a strictly
positive quadratic endpoint-gap coefficient.

## 2. The two exact orientations

Let `P` be a finite row-stochastic kernel self-adjoint in `L^2(pi)`.  Let
`a>0`, normalized by `E_pi a=1`, and define

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a}.
                                                               \tag{2}
\]

Then `P` and `R` are adjoint under `p`:

\[
                         E_p(fRg)=E_p(gPf).                    \tag{3}
\]

Suppose the positive Bd and dB endpoints satisfy

\[
 tb=rqPb,\qquad s=rhRs,\qquad q=1-b,\quad h=1-s.              \tag{4}
\]

Define the original scaled-first slack, endpoint gap, and mean residual by

\[
 \begin{aligned}
 U&=cE_pq-E_p(1-h_1),\\
 G&=E_p(h-h_1),\\
 M&=E_pd=U+G.
 \end{aligned}                                                \tag{5}
\]

The scaled-first theorem proves `U>=0` throughout the stated interval.

Now apply the exact temperature-adjoint involution

\[
 p^\dagger=pt,\qquad P^\dagger=D_t^{-1}R,\qquad
 R^\dagger=D_t^{-1}P,\qquad t^\dagger={1\over t}.             \tag{6}
\]

Here `p^dagger` is normalized, `P^dagger` is row stochastic, and
`R^dagger` is its `p^dagger`-adjoint.  The endpoint roles swap:

\[
 b^\dagger=s,\quad s^\dagger=b,\quad
 q^\dagger=h,\quad h^\dagger=q.                              \tag{7}
\]

Consequently the transformed residual and first-iterate complement are

\[
 d^\dagger=ch-b,
 \qquad
 q_1={1\over1+rcR^\dagger h}
     ={t\over t+rcPh}.                                       \tag{8}
\]

The transformed scalar averages, written entirely in the original measure,
are

\[
 \begin{aligned}
 U^\dagger
   &=cE_{p^\dagger}h-E_{p^\dagger}(1-q_1)
     =cE_p(th)-E_p\{t(1-q_1)\}\geq0,\\
 G^\dagger
   &=E_{p^\dagger}(q-q_1)=E_p\{t(q-q_1)\},\\
 M^\dagger
   &=E_{p^\dagger}d^\dagger=E_p(td^\dagger)
     =U^\dagger+G^\dagger.
 \end{aligned}                                                \tag{9}
\]

The two residuals differ exactly by

\[
 \boxed{
 d-d^\dagger=(r-2)(q-h).}                                  \tag{10}
\]

At `r=2` they coincide.  On the interval considered here, the right side is
the obstruction that survives orientation averaging.

## 3. Reciprocal squares and oriented cross terms

Subtracting the reciprocal endpoint equations gives the pointwise identities

\[
 h-h_1=rhh_1Rd,
 \qquad
 q-q_1={rqq_1\over t}Pd^\dagger.                            \tag{11}
\]

For the original orientation, use adjointness in the first equation and
split `hh_1=h_1^2+h_1(h-h_1)`.  The second summand transforms back into a
square.  This proves (1).  Applying the same calculation to the transformed
system gives

\[
 \boxed{
 G^\dagger=rE_p\{d^\dagger R(q_1^2)\}
       +E_p\!\left[{t(q-q_1)^2\over q}\right].}             \tag{12}
\]

All denominators in (1) and (12) are positive on the active endpoint branch.

Let

\[
                         \mu_{ij}=p_iP_{ij}.
\]

The two cross terms, in one common edge orientation, are

\[
 \begin{aligned}
 A&:=E_p\{dP(h_1^2)\}
    =\sum_{i,j}\mu_{ij}d_i h_{1,j}^2,\\
 A^\dagger&:=E_p\{d^\dagger R(q_1^2)\}
    =\sum_{i,j}\mu_{ij}q_{1,i}^2d_j^\dagger.
 \end{aligned}                                               \tag{13}
\]

Inserting (10) into the second line exposes the residual with its exact sign:

\[
 \boxed{
 A^\dagger
 =\sum_{i,j}\mu_{ij}q_{1,i}^2d_j
  -(r-2)\sum_{i,j}\mu_{ij}q_{1,i}^2(q_j-h_j).}              \tag{14}
\]

Thus the transformed cross term is not the original cross term with its edge
orientation reversed.  A proof at general `r` cannot identify the two
residuals as it can at `r=2`.

## 4. A physical two-state tangent family

Take

\[
 P_\lambda={1\over2}
 \begin{pmatrix}
  1+\lambda&1-\lambda\\
  1-\lambda&1+\lambda
 \end{pmatrix},qquad
 \pi={1\over2}(1,1),\qquad
 f=(1,-1)^T,                                                \tag{15}
\]

where `-1<=lambda<0`, and perturb the positive label by

\[
                         a_\epsilon=1+\epsilon f,
 \qquad |\epsilon|<1.                                      \tag{16}
\]

This is a genuine reversible endpoint family, not a kernel enumeration.
Since `P_lambda f=lambda f`, the nonzero endpoint branches are analytic near
`epsilon=0`: their endpoint Jacobians have eigenvalues `1-r` and
`lambda-r`, both nonzero.

Write `[epsilon^2]Z` for the quadratic Taylor coefficient of a scalar `Z`.
Direct implicit expansion of (4) gives

\[
 \begin{aligned}
 q&={1\over r}+\epsilon Qf+\epsilon^2Q_2+O(\epsilon^3),\\
 h&={1\over r}-\epsilon Qf+\epsilon^2H_2+O(\epsilon^3),
 \end{aligned}                                               \tag{17}
\]

where scalar multiples of the all-one vector are understood and

\[
 \begin{aligned}
 Q&={c(\lambda-1)\over r(r-\lambda)},\\
 Q_2&=-{(\lambda-1)c(r-\lambda^2)
              \over r(r-\lambda)^2},\\
 H_2&={\lambda(\lambda-1)c^2
              \over r(r-\lambda)^2}.
 \end{aligned}                                               \tag{18}
\]

Put

\[
 D=(r-2)Q,
 \qquad
 L=-Q\left(1+{\lambda(r-2)\over r}\right).                 \tag{19}
\]

Then

\[
 \begin{array}{lll}
 d=\epsilon Df+O(\epsilon^2),
 &\quad& d^\dagger=-\epsilon Df+O(\epsilon^2),\\[2mm]
 h_1=r^{-1}+\epsilon Lf+O(\epsilon^2),
 &&q_1=r^{-1}-\epsilon Lf+O(\epsilon^2),\\[2mm]
 h-h_1={\epsilon\lambda D\over r}f+O(\epsilon^2),
 &&q-q_1=-{\epsilon\lambda D\over r}f+O(\epsilon^2).
 \end{array}                                                 \tag{20}
\]

The original and transformed measures are exactly

\[
 p=\pi(1+\epsilon f),
 \qquad
 p^\dagger=pt=\pi(1+\lambda\epsilon f).                    \tag{21}
\]

Consequently, if

\[
 M_2=[\epsilon^2]M,
 \qquad M_2^\dagger=[\epsilon^2]M^\dagger,
\]

then

\[
 \begin{aligned}
 M_2&=H_2+cQ_2+D,\\
 M_2^\dagger&=Q_2+cH_2-\lambda D,
 \end{aligned}
\]

and both simplify to the same strictly positive quantity

\[
 \boxed{
 M_2=M_2^\dagger
 ={(\lambda-1)^2c\{r+\lambda c\}
       \over r(r-\lambda)^2}>0.}                            \tag{22}
\]

## 5. The common negative remainder

The oriented cross terms and reciprocal squares have the exact quadratic
coefficients

\[
 \begin{aligned}
 [\epsilon^2]A
   &={M_2\over r^2}+{2DL\lambda\over r},\\
 [\epsilon^2]A^\dagger
   &={M_2^\dagger\over r^2}+{2DL\lambda\over r},\\
 [\epsilon^2]E_p\!\left[{(h-h_1)^2\over h}\right]
   &=[\epsilon^2]E_p\!\left[{t(q-q_1)^2\over q}\right]
     ={\lambda^2D^2\over r}.
 \end{aligned}                                               \tag{23}
\]

Thus the two orientations have the same remainder

\[
 \begin{aligned}
 C&:=2DL\lambda+{\lambda^2D^2\over r}\\
  &=-\lambda(r-2)Q^2
       \left(2+{\lambda(r-2)\over r}\right)\\
  &=-{\lambda(\lambda-1)^2(r-2)c^2
        \{2r+\lambda(r-2)\}
       \over r^3(r-\lambda)^2}.
 \end{aligned}                                               \tag{24}
\]

For

\[
 {3\over2}\leq r\leq{151\over100},qquad -1\leq\lambda<0,
\]

all denominators in (24) are positive,
`2r+lambda(r-2)>0`, and the factor `r-2` is negative.  Hence

\[
                              \boxed{C<0.}                  \tag{25}
\]

The positive reciprocal square in (23) has not been discarded: it is the
second summand in `C`.  The non-mean, fluctuation part `2DLlambda` of the
reciprocal cross contribution is more negative, so that fluctuation part plus
the square remains negative.  The full cross-plus-square coefficient is
`M_2/r+C=G_2`, which is positive on the physical family by Section 7.  At
`r=2`, by contrast, `D=C=0` exactly.

Equations (1), (5), (12), and (23) now give

\[
 \begin{array}{ll}
 G_2:=[\epsilon^2]G={M_2\over r}+C,
 &U_2:=[\epsilon^2]U={cM_2\over r}-C,\\[2mm]
 G_2^\dagger:=[\epsilon^2]G^\dagger={M_2^\dagger\over r}+C,
 &U_2^\dagger:=[\epsilon^2]U^\dagger
                  ={cM_2^\dagger\over r}-C.
 \end{array}                                                 \tag{26}
\]

For every `0<=theta<=1`, define the orientation averages

\[
 \overline G_2=\theta G_2+(1-\theta)G_2^\dagger,
 \qquad
 \overline U_2=\theta U_2+(1-\theta)U_2^\dagger.
\]

Eliminating the averaged mean residual from (26) yields

\[
 \boxed{
                    \overline G_2={\overline U_2+rC\over c}.} \tag{27}
\]

The negative remainder survives with coefficient one for every nonnegative
orientation average.  The proved sign `overline U_2>=0` is weaker than the
missing quantitative estimate `overline U_2>=-rC`.

## 6. Exact Farkas obstruction

Fix any allowed `(r,lambda)`, and therefore the exact number `C<0`.  Project
the quadratic data onto the two mean residual coordinates `(m,m^dagger)`,
retaining only the two scalar scaled-first inequalities.  The feasible
relaxation is

\[
 {cm\over r}-C\geq0,
 \qquad
 {cm^\dagger\over r}-C\geq0.                               \tag{28}
\]

The exact witness

\[
                            m=m^\dagger=0                   \tag{29}
\]

satisfies both inequalities strictly, because their values are `-C>0`, but
the projected target has value

\[
                            {m\over r}+C=C<0.                \tag{30}
\]

The same witness obeys the additional equality `m=m^dagger`.  Therefore,
in homogeneous coordinates `x=(m,m^dagger,C)`, the two premise rows are

\[
 \left({c\over r},0,-1\right),
 \qquad
 \left(0,{c\over r},-1\right),                              \tag{30a}
\]

while the target row is `(1/r,0,1)` and the optional equality row is
`(1,-1,0)`.  The witness (29)--(30) proves, by the finite-dimensional Farkas
alternative, that the target row is not in the cone generated by the two
scaled-first rows plus the span of the equality row.  Equivalently, no
nonnegative scalar combination of the two sign inequalities can prove the
quadratic endpoint gap after the remaining endpoint data have been projected
away.

The witness (29) is deliberately a witness in the projected scalar
relaxation.  It is not a physical endpoint tangent.  Indeed the physical
value (22) is positive.

## 7. The physical family is not a counterexample

Set `u=-lambda`, so `0<u<=1`.  Substitution in the first line of (26) gives

\[
 G_2={c(\lambda-1)^2\over r^3(r-\lambda)^2}
 \left[
 r\{r+\lambda c\}
 -\lambda(r-2)c\{2r+\lambda(r-2)\}
 \right].                                                   \tag{31}
\]

Call the bracket `N_r(lambda)`.  It is concave in `lambda`, with endpoint
values

\[
 N_r(0)=r^2,
 \qquad
 N_r(-1)=r^3-r^2-3r+4.                                     \tag{32}
\]

On the full fitness interval,

\[
 N_r(-1)-{5\over8}
 ={(2r-3)(4r^2+2r-9)\over8}\geq0.                          \tag{33}
\]

A direct interval check is
`4r^2+2r-9=3+(2r-3)(2r+4)>=3`.
A concave function on `[-1,0]` is bounded below by the smaller endpoint
value.  Hence `N_r(lambda)>=5/8`, and therefore

\[
                              \boxed{G_2>0}                 \tag{34}
\]

for the physical family.  The family detects the failure of the proposed
scalar-combination proof architecture; it does not violate the desired
endpoint inequality.

## 8. What remains

The sign `G>=0` at `R_hyb` remains open.  A successful proof must add
information not present in the two scalar conclusions `U>=0` and
`U^dagger>=0`.  Formula (27) identifies the missing local strength exactly:
one needs endpoint structure that controls the mean residual strongly enough
to dominate `-rC`, or a genuinely coupled orientation argument that does not
project to the two scalar slacks.

## 9. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_endpoint_adjoint_combination_obstruction/verify_adjoint_combination.py
```

The replay uses exact symbolic arithmetic only.
