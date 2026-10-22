# Proof 15  Angular order under a common rotation

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Arithmetic progressions with radial noise and joins](09_robust_ap_and_joins.md); [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md); [Uniform pair signs on centered crosses](12_uniform_pair_signs.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## Theorem

Let `c,a_j,b_j>=0`, let `Z_j` be independent uniform unit complex variables, and put

`S=sum_j(a_j Z_j+b_j conjugate(Z_j))`.

For every `p>=2` and every independent bounded radial complex variable `Y`, the function

`M_p(delta)=E |c+exp(i delta) S+Y|^p`

is nonincreasing for `0<=delta<=pi/2`. In particular its maximum over all rotation angles is attained at zero. The same angular monotonicity holds with the power test replaced by **every continuous radial planar bisubharmonic test**. It remains valid after independent bounded radial noise.

The theorem rotates the entire aligned sum by one common angle. It does not compare independent rotations of different endpoint pairs, and therefore does not settle the remaining mixed-sign centered-cross inequality.

## 1. Scalar projection and the required two-variable supermodularity

Write `A_j=a_j+b_j`, `B_j=|a_j-b_j|`,

`alpha_j=(A_j^2+B_j^2)/2`, `beta_j=(A_j^2-B_j^2)/2>=0`.

The law of each summand is that of `A_j cos(theta_j)+i B_j sin(theta_j)`. Let

`h(x)=E |x+Re Y|^p`,

`G(s0,s1,...,sn)=E h(sqrt(s0)+sum_j sqrt(sj) cos(theta_j))`.

For `p>2`, the scalar arcsine-potential lemma in [Proof 09](09_robust_ap_and_joins.md) gives

`G_(s0,sj)>=0` for `s0,sj>0`.                                  (1)

For clarity, average first over every cosine variable except `theta_j`. The resulting scalar function has second derivative

`p(p-1) E |x+Re W|^(p-2)`,

where `W` is a bounded radial random variable (the sum of the other independent circles and `Y`). This is even and nondecreasing on the nonnegative half-line. Therefore

`G_(s0,sj)=[4 sqrt(s0 sj)]^(-1) E[cos(theta_j) h_rest''(sqrt(s0)+sqrt(sj)cos(theta_j))]>=0`

by pairing opposite cosine values. No random/random mixed derivative is used.

For `epsilon>0`, define

`H_epsilon(s,z)=G(s+epsilon,alpha_1+epsilon+beta_1 z,...,alpha_n+epsilon+beta_n z)`.

On the compact rectangle `0<=s<=c^2`, `-1<=z<=1`,

`(H_epsilon)_(s,z)=sum_j beta_j G_(s0,sj)>=0`.                   (2)

All its arguments stay strictly positive, so the mixed derivative is continuous. As epsilon decreases to zero, `H_epsilon` converges uniformly on this rectangle to the same expression without epsilon, by continuity of the bounded expectations.

For every complex number `w`,

`E_t |Re(exp(-it)w)|^p=m_p |w|^p`, where `m_p=E|cos(t)|^p>0`.

The sign of `c cos t` is immaterial because the scalar random summands have a jointly symmetric law. Projection of the rotated ellipse has squared amplitude

`alpha_j+beta_j cos(2t-2delta)`.

Consequently

`m_p M_p(delta)=E_t H_0(c^2 cos^2 t,cos(2t-2delta))`.           (3)

## 2. Exact circular-arc overlap lemma

Let `U` be uniform modulo `2pi`. For any thresholds `u,v` in `[-1,1]`, the probability

`P(cos U>u, cos(U-d)>v)`

is nonincreasing for `0<=d<=pi`.

Indeed the two events are circular arcs with respective half-lengths

`a=arccos u`, `b=arccos v`, both in `[0,pi]`,

whose centers have separation `d`. Their intersection length is

`L(d)=(a+b-d)_+-(|a-b|-d)_+ +(a+b+d-2pi)_+`.                 (4)

The first two terms give the ordinary interval overlap, and the last term is the possible wrap-around overlap. Endpoint cases follow by continuity.

The positive-part breakpoints satisfy

`|a-b|<=2pi-a-b`,

because `a,b<=pi`. If `a+b<=pi`, the last term vanishes throughout `0<=d<=pi`; the first two terms are constant and then decrease to zero. If `a+b>=pi`, the first term remains active throughout that interval; after the initial constant part the expression decreases with slope `-1` until the last term activates, after which it is constant. Thus it never increases. This verifies the large-arc case rather than assuming an overlap formula valid only for short arcs.

## 3. Layer-cake supermodular rearrangement

For any continuously mixed-differentiable `H` on the rectangle,

`H(s,z)=H(s,-1)+H(0,z)-H(0,-1)`

`          + integral_0^(c^2) integral_(-1)^1 H_(s,z)(u,v) 1_{s>u}1_{z>v} dv du`.  (5)

The identity is the two-variable fundamental theorem of calculus. The marginal terms have expectations independent of delta when

`s=c^2 cos^2 t`, `z=cos(2t-2delta)`.

For `c>0`, the joint threshold event in the last term is

`cos(2t)>2u/c^2-1`, `cos(2t-2delta)>v`.

By the arc-overlap lemma, its probability is nonincreasing for `0<=delta<=pi/2`. Apply (5) to `H_epsilon`, use its nonnegative mixed derivative from (2), and pass to the uniform limit epsilon down to zero. Equation (3) proves the theorem for `p>2`. If `c=0`, the whole moment is constant in delta by radiality of the test and noise. At `p=2`, Fourier orthogonality gives the constant value `c^2+sum_j(a_j^2+b_j^2)+E|Y|^2`.

Reflection and half-turn symmetry of `S`, together with radiality of `Y`, show that `M_p` is even and pi-periodic, so the monotonicity on `[0,pi/2]` also identifies its global maxima and minima.

## 4. Green kernels and the whole radial bisubharmonic cone

Fix `0<=delta_1<=delta_2<=pi/2`. The power gap is nonnegative for every `p>2`, equals zero at `p=2`, and can be differentiated at `2` under the bounded expectation. The convention `r^2 log r=0` at zero makes the derivative continuous there. Hence

`E K(c+exp(i delta_1)S+Y)>=E K(c+exp(i delta_2)S+Y)`,

where `K(z)=|z|^2 log|z|`.

In particular this holds for every circular noise `Y=rho Z`. The two compared laws have the same second moment. The accepted radial Green representation therefore extends the inequality to every continuous radial planar bisubharmonic test. That cone is closed under convolution with an independent bounded radial probability law, so the stated radial-noise robustness also follows for the entire cone.

No interpolation from endpoint exponents is used: the only passage from powers to Green kernels is differentiation at `p=2`, with a nonnegative gap for every exponent immediately above two.
