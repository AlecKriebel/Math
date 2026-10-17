# Proof 12  Uniform pair signs on centered crosses

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Arithmetic progressions with radial noise and joins](09_robust_ap_and_joins.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Statement and scope

For independent uniform unit complex variables `Z_j`, arbitrary nonnegative `c,a_j,b_j`, every `p>=2`, and arbitrary independent bounded rotationally invariant complex noise `Y`,

`E |c+sum_j(a_j Z_j+b_j conjugate(Z_j))+Y|^p`

`>= E |c+sum_j(a_j Z_j-b_j conjugate(Z_j))+Y|^p`.                 (1)

The endpoint magnitudes may be arbitrarily unequal. The conclusion covers sign patterns in which every nonzero endpoint-pair product has the same sign; common pair signs and the center sign are removed by independent angular shifts and an overall sign. It does **not** compare an arbitrary mixture of positive and negative endpoint-pair products with the all-positive array. Hence it is not the full centered-cross majorant property.

This is a corollary of the scalar arcsine-potential monotonicity proved in the included robust AP proof [Arithmetic progressions with radial noise and joins](09_robust_ap_and_joins.md), Lemmas 1 and 2. 

## 1. The only scalar monotonicity needed

For every `alpha>0` and every bounded radial complex variable `W`, the scalar function

`x -> E |x+Re W|^alpha`

is even and nondecreasing for `x>=0`. The cited self-contained earlier proof conditions on `|W|` and uses

`E |x+cos(theta)|^alpha = E |cos(theta)|^alpha sum_(k>=0) [(-alpha/2)_k^2/((1/2)_k k!)] x^(2k)`

on `|x|<1`, together with pointwise monotonicity for `x>=1`. Its positive-coefficient identity follows from a distributional ODE, so it remains valid when `alpha<1`.

For `p>2`, define

`h(x)=E |x+Re Y|^p`,

`G(s0,s1,...,sn)=E h(sqrt(s0)+sum_j sqrt(sj) cos(theta_j))`.

For any fixed random-radius index `j`, first average over all other cosine terms. Those terms plus `Re Y` are the real projection of a bounded radial complex variable `W`: take the sum of `Y` and independent uniform circles of radii `sqrt(sk)`, `k!=j`. Therefore

`h_rest''(x)=p(p-1) E |x+Re W|^(p-2)`

is even and nondecreasing for `x>=0`. Since `p>2`, this second derivative is continuous and differentiation under bounded expectations is valid.

For `s0,sj>0`,

`G_(s0,sj) = [4 sqrt(s0 sj)]^(-1) E [cos(theta_j) h_rest''(sqrt(s0)+sqrt(sj)cos(theta_j))] >=0`.      (2)

Pairing opposite cosine values proves the sign using `a+b>=|a-b|` for `a,b>=0`. Boundary coordinates follow by continuity. No random/random mixed derivative is asserted to have a sign.

Consequently, if `u>=v>=0` and the random-radius vectors satisfy `x>=y` coordinatewise, then

`G(u,x)+G(v,y) >= G(u,y)+G(v,x)`.                              (3)

To see this, change the random-radius coordinates from `y` to `x` one at a time and integrate (2) over the resulting center/radius rectangles. This proof only uses center/random mixed derivatives.

## 2. Angular projection of the two patterns

Set

`A_j=a_j+b_j`, `B_j=|a_j-b_j|`,

`alpha_j=(A_j^2+B_j^2)/2`, `beta_j=(A_j^2-B_j^2)/2>=0`,

`alpha_0=beta_0=c^2/2`.

The positive pattern is a sum of aligned ellipses `A_j cos(theta_j)+i B_j sin(theta_j)`, displaced by `c` along their major axes. Flipping exactly one endpoint in **every** pair rotates every ellipse by a right angle, up to changes of independent angles that preserve their joint law.

For any complex number `z`,

`E_t |Re(exp(-it)z)|^p = m_p |z|^p`, `m_p=E|cos(t)|^p>0`.

Rotational invariance of `Y` allows its scalar projection to be included in `h` for every direction. Thus the positive and all-flipped moments, multiplied by `m_p`, are respectively

`E_t G(alpha_0+beta_0 cos(2t), (alpha_j+beta_j cos(2t))_j)`,

`E_t G(alpha_0+beta_0 cos(2t), (alpha_j-beta_j cos(2t))_j)`.

For `z>=0`, write

`s0+=alpha_0+beta_0 z`, `s0-=alpha_0-beta_0 z`,

`s+=(alpha_j+beta_j z)_j`, `s-=(alpha_j-beta_j z)_j`.

The paired difference at `cos(2t)=z` and `cos(2t)=-z` is

`G(s0+,s+)+G(s0-,s-)-G(s0+,s-)-G(s0-,s+) >=0`

by (3). The law of `cos(2t)` is symmetric, so integration proves (1) for `p>2`. At `p=2`, all cross terms vanish by independence and phase symmetry, giving equality.

## 3. Consequence for the unresolved gap

For `2<p<3`, a hypothetical centered-cross sign counterexample must involve at least one nonzero endpoint pair of each product sign after the elementary sign gauges. The all-flipped pattern cannot give a counterexample, in any dimension and with any unequal endpoint magnitudes. Together with the separately proved balanced-or-circular majorant theorem, this narrows the unresolved regime to genuinely mixed-sign, genuinely elliptical configurations.

The scalar random/random obstruction from earlier remains genuine. This proof does not repair it or infer lattice-supermodularity of the full scalar multiradius function.
