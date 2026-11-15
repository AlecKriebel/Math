# Independent analytic derivation — record 23331080

This document was completed after the independent manuscript reconstruction
sealed in `INITIAL_SEAL.json`. It concerns the whole original theorem, including
the exact coefficient for every finite time, global initial strict positivity,
the positive root metric, and the prescribed probability normalization.
It does not replace that sealed reconstruction with a post-source account.

## 1. Category, frames, and exact flow

Use the quotient/projectivization convention in the paper:
`f_* O_E(1)=E`, `X=P(E*)`. For `E=O(1) tensor C^2` on `S=P^1`,
`X=P^1_s x P^1_z`, `O_E(1)=O(1,1)` and `L=O_E(2)=O(2,2)`.
The relative anticanonical bundle is `K_(X/S)^(-1)=O(0,2)`:
the determinant twist in `L tensor f^*(det E)^(-1)` is necessary. The example
does not identify these two line bundles on the whole total space.

A fixed nonvanishing holomorphic determinant frame over a base coordinate
neighborhood identifies the restrictions of L with the anticanonical bundle.
In this frame, `e^(-phi) dA_z` is a fibre density. A change of fibre coordinate
has the anticanonical Jacobian, and a determinant frame change multiplies the
whole fibre density by a base factor. The latter cancels from its normalized
probability measure. Thus the ratio of the two measures below is a global
scalar; it is not defined using an arbitrary fixed background area measure:

`phi_t = log(MA(phi)/mu_phi)`,
`MA(phi)=g dA/(2*pi)`, `mu_phi=e^(-phi)dA/I(s)`,
`g=phi_(z zbar)`, `I(s)=integral e^(-phi)dA`.

Here `dA` is ordinary planar area in the finite chart and the curvature
mass of a weight on O(2) is `integral g dA=2*pi`. Hence the exact scalar
equation is

`phi_t=log g+phi+log I-log(2*pi)`.                         (A)

Other fixed positive curvature/area conventions alter only the constant.
The coefficient multiplying this weight phi is **one**, not the rank two.
Adding an arbitrary time-independent smooth base function b leaves both
normalized measures and the right side of (A) unchanged, since I is multiplied
by `e^(-b)`. A time-dependent added b(t,s) would contribute b_t to the left;
it must not be silently treated as the same solution.

In particular the time-dependent L2-normalized anticanonical weight sometimes
introduced to interpret mu need not obey the very same scalar weight equation
as phi. No such change of unknown is used here. The fixed holomorphic frame
in Naumann's proof of Theorem 5, printed1519, is the relevant identification.

Naumann's actual 2021 defining equation (13) and Theorem 5 supply precisely
this flow on O_E(r) and smoothness on `X x [0,infinity)` for fibre-positive
initial metrics. The actual text distinguishes this finite-time smoothness
from base regularity at the infinite-time limit. For this example the fibres
are P^1, so their anticanonical class is Kähler and Kähler–Einstein. Their
continuous automorphisms do not violate the stated finite-time theorem.
Alternatively, classical normalized fibre Kähler–Ricci flow, finite-time
parabolic bounds and smooth dependence on the compact base parameter give
the same finite-time interface. No infinite-time transverse convergence is
imported or required.

Uniqueness is also directly available here, including base constants. For two
solutions put v=phi-phi_tilde. On each fibre,
`|log I(phi)-log I(phi_tilde)| <= ||v||_infinity`. At a fibre maximum of v,
the logarithmic Hessian difference is nonpositive; at a minimum it is
nonnegative. Taking maxima also over the compact base gives the upper Dini
estimate `D^+||v||_infinity <= 2||v||_infinity`. Gronwall forces v=0 for
common initial data. This justifies the lifted circle symmetries used below.

## 2. Global metric and continuum certificate, including the four corners

Put `epsilon=1/96`, `delta=1/4`, `u=|s|^2`, `v=|z|^2`,
`p=u/(1+u)`, `x=v/(1+v)`. The proposed finite-chart weight is

`phi_0=2log(1+u)+2log(1+v)+(2-epsilon)(1-p)+delta*p*x^2`.

Under `w=1/s`, subtract the O(2) frame transition `2log|s|^2`.
The logarithmic part becomes `2log(1+|w|^2)` and
`p=1/(1+|w|^2)`. Under `zeta=1/z` the corresponding fibre transition gives
`2log(1+|zeta|^2)` and `x=1/(1+|zeta|^2)`. Every remainder is smooth in
the corresponding finite coordinate, including the joint infinity chart.
Consequently this is a smooth Hermitian weight on O(2,2), not merely a
potential on a dense affine subset.

For a radial smooth function R(u,v), direct Wirtinger differentiation gives
`R_(s sbar)=R_u+u*R_uu`,
`R_(z zbar)=R_v+v*R_vv`,
`R_(s zbar)=sbar*z*R_uv`.
Thus the Fubini–Study frame diagonal coefficients and mixed squared modulus are

`A=4p+(epsilon+delta*x^2)(1-2p)`,
`B=2+2delta*p*x*(2-3x)`,
`Q=4delta^2*p*(1-p)*x^3*(1-x)`.

The coefficient matrix has positive determinant exactly when `AB-Q>0`.
The following are identities, with every displayed slack nonnegative on the
closed square `0<=p,x<=1`:

`A0=epsilon+(167/48)p`, `B0=3/2`, `Q0=p/4`,
`A-A0=delta*x^2+2delta*p*(1-x^2)`,
`B-B0=2delta*((1-p)+p*(1-x)*(1+3x))`,
`Q0-Q=4delta^2*p*(1-(1-p)*x^3*(1-x))`.

For the last sign, each factor `(1-p),x^3,(1-x)` lies in [0,1], so their
product is at most one. Since A0 and B0 are strictly positive,

`AB-Q >= A0*B0-Q0 = 1/64+(159/32)p > 0`.                  (B)

This includes p=0,1 and x=0,1 without a limiting numerical argument.
Sylvester's criterion proves strict positive definiteness everywhere on the
compact total space. In particular g>0 on every fibre. Dividing phi_0 by two
is a valid metric on O_E(1): the frame transitions halve to those of O(1,1),
and the curvature halves while retaining strict positivity. The bundle is
ample, and it already admits Griffiths-positive metrics; neither a missing
square root nor an unproved ampleness claim is used.

The independent `check_analytic.py` performs the actual radial differentiations
in each of the four coordinate charts in the exact rational function ring
`Q[U,V,(1+U)^(-1),(1+V)^(-1)]`. In every chart it substitutes the appropriate
finite or reciprocal p,x, differentiates the actual remainder, and checks A,
B,Q and all four certificate identities. Its denominator factors are
strictly positive for the nonnegative squared coordinate radii. This is an
identity check throughout the charts; no grid or sampled determinant is used.

## 3. Exact nonlinear two-jet, rather than a perturbative approximation

The initial weight and the defining flow are equivariant under the lifted
base rotations. Uniqueness therefore gives
`phi_s(0,z,t)=phi_sbar(0,z,t)=phi_(s zbar)(0,z,t)=0`
for all finite t. Their fibre derivatives vanish as well. The same rotations
are valid globally on the line bundle; they fix s=0, and the finite local
frame can be taken invariant there.

The restricted initial central fibre is
`phi_F=2log(1+v)+2-epsilon`. Its curvature coefficient is
`g_F=2/(1+v)^2`. Both normalized measures equal
`dA/(pi*(1+v)^2)`. Hence this fibre is exactly stationary under the probability
flow. Fibre uniqueness identifies it with the restriction of the actual
global smooth solution for every finite time.

Let `w(z,t)=phi_(s sbar)(0,z,t)`. Differentiating (A) is legitimate by the
actual finite-time C-infinity solution and compact fibre. Since g_s=g_sbar=0,

`(log g)_(s sbar)=w_(z zbar)/g_F=Delta_F w`.

The density derivative is exact:
`(e^(-phi))_(s sbar)=(phi_s*phi_sbar-phi_(s sbar))*e^(-phi)`.
At s=0 its first derivatives vanish, so
`I_s=0`, `I_(s sbar)=-I*mean_F(w)` and
`(log I)_(s sbar)=-mean_F(w)`. Therefore

`w_t=Delta_F w+w-mean_F(w)`,
`w(z,0)=epsilon+delta*x^2`,
`Delta_F=((1+v)^2/2)*partial_z partial_zbar`.              (C)

This follows by taking the actual second jet of the nonlinear solution.
Terms of higher base order have zero contribution to this derivative;
the cancellation of the first jets eliminates the quadratic logarithmic
term and the density covariance term. No small-parameter truncation or
uncontrolled interchange with the infinite-time limit occurs.

The horizontal geodesic coefficient is
`c=phi_(s sbar)-|phi_(s zbar)|^2/g`. At s=0 its mixed term is zero,
so c=w, and phi_(s sbar) is curvature on the actual vector partial/partial s.
Thus a negative w is genuine total-space negativity rather than a choice of
horizontal lift concealing a positive curvature form.

## 4. Solve the exact jet and identify all time boundaries

Radial integration of mu_F gives `dv/(1+v)^2=dx`; its pushforward is uniform
Lebesgue probability on [0,1]. A radial function F(x) satisfies

`Delta_F F = (1/2)*(x*(1-x)*F''+(1-2x)*F')`.

Set `P1=2x-1`, `P2=6x^2-6x+1`. Both have zero uniform mean, and direct
differentiation gives `Delta_F P1=-P1`, `Delta_F P2=-3P2`.
Since `x^2=1/3+P1/2+P2/6`, the solution candidate is

`w=epsilon+delta/3+(delta/2)*P1+(delta/6)*exp(-2t)*P2`.     (D)

Its initial value and full equation (C), not just its value at the pole, are
verified by the independent exact polynomial check. To identify it with the
actual derivative, the difference of two smooth solutions of (C) has constant
mean because the fibre Laplacian integrates to zero. With zero initial data,
its mean remains zero, and the difference solves `a_t=Delta_F a+a`.
Applying the maximum principle to `exp(-t)*a` gives uniqueness. This uses only
finite compact time intervals and the smooth stationary fibre metric.

At x=0,

`phi_(s sbar)(0,0,t)=1/96-(1-exp(-2t))/24`.                (E)

At t=0 it is 1/96>0. Its initial time derivative is -1/12. The first zero
is `t0=(1/2)log(4/3)>0`; it is strictly negative for every finite t>t0.
At the asserted finite time `t*=(1/2)log2` it is exactly -1/96. Its scalar
limit would be -1/32; no existence or smoothness assertion about an
infinite-time total-space limit is needed to obtain (E) at finite times.
The fibre metric remains positive by the imported finite-time flow theorem.

## 5. Normalization attacks and honest scope

The product weight `phi_prod=2log(1+u)+2log(1+v)` is stationary because its
two probability measures agree fibrewise for every s. At s=0 it has c=2,
zero fibre Laplacian of c, zero Kodaira–Spencer term, and
`(log I)_(s sbar)=-2`. Thus a literal same-weight, same-time equation with
reaction `r*c=2c` would predict c_t=2 rather than zero. The actual 2021
equation (14) indeed prints r*c. This calibration isolates a convention
discrepancy with the defining equation (13); it does not infer the source's
undocumented intention. The proof above uses only (13)/(A) and rederives (C).

Positive rescaling can legitimately produce a rank coefficient: put
`psi=phi/r` and `tau=t/r`. Then
`psi_tau=log(psi_(z zbar))+r*psi+log integral e^(-r*psi)dA+C'`.
Weights, time, the integral exponent and the Laplacian all transform together.
The sign of curvature is unchanged by this positive scaling. Dropping log I
instead changes the weight flow: the mean subtraction in (C) disappears.
Berman's positive preservation theorem for the nonnormalized weight flow is
therefore compatible with the counterexample.

Six exact mutation controls reject dropping the mean term, changing the
reaction to two in the same weight/time, doubling the Laplacian, reversing
the exponential derivative, confusing the initial pole with zero, and using
the rank-two term on the stationary product calibration. These are checks of
load-bearing conventions, not numerical evidence for a PDE existence theorem.

The verified conclusion concerns the universal total-space preservation
question for the specified normalized O_E(r) flow. It neither settles the
Griffiths conjecture nor excludes special initial metrics, nor makes a
statement about all possible normalizations. Berman had earlier noted
normalized anticanonical negativity in effectively parametrized Fano
families; that is an essential historical boundary. The present bundle is
locally isotrivial with P^1 fibres and uses O_E(r), with an explicit globally
strict initial metric and exact finite-time witness. Worldwide firstness,
and the contents of an unrecovered Naumann habilitation mentioned in the
paper, are not established by this bounded review. Those are priority limits,
not missing premises of (A)–(E).
