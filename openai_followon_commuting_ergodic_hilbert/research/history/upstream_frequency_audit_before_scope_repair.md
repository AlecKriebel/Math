# Independent audit of the frequency, rough-kernel and completion arguments

Date: 2026-10-06, America/Los_Angeles. Reviewer: independent AI subagent
`upstream_frequency_audit`. This is an automated adversarial review, not human
peer review. No external individual was contacted; no Git operation or
publication operation was performed by this reviewer.

## Scope and verdict

I read the original request in `research/ORIGINAL_REQUEST.txt`, the pinned
upstream manuscript's `frequency.tex`, `rough.tex`, `completion.tex`,
`introduction.tex`, `preliminaries.tex`, `heat.tex`, and `matrix.tex`, its
`main.tex`, and its manuscript README. The assigned emphasis was the new
frequency-block mechanism, including arbitrary output-dependent coefficients,
rough endpoint families and the full pointwise supremum.

**No substantive gap or counterexample was found in the assigned arguments.**
The frequency proof uses the stated pointwise square integral over scales and
frequency; it does not replace that integral with a sum of frequency suprema.
The completion argument does yield an output-point-dependent supremum over
all finite partitions and all positive scales. This finding does not certify
the separately assigned smooth-switch proof, the new lattice restriction and
ergodic transference proof, the priority audit, or a publication package. The
frequency proof depends on the upstream finite-matrix and heat statements;
those statements must also pass their separately assigned audit.

The pivotal new frequency steps were reconstructed analytically below rather
than accepted merely from the theorem statement. Concrete finite coefficient
probes were also run; they are exploratory floating-point quadrature and not
proof of the estimate.

## Exact dependency and coefficient scope

The proposition fixes any `q>0`, `D>=1`, measurable
`Xi_D subset [-2D,2D]` with measure `d gamma=d xi/D`, and any nonempty finite
set of integer scales `L_k=2^k`. Its coefficient conditions are

\[
 |\mu_{ij,k}(\xi)|\le C_1,\qquad
 \sum_k\int_{\Xi_D}|\mu_{ij,k}(\xi)|^2\,\frac{d\xi}{D}\le C_1^2
\]

at **each output pair** `(i,j)`. Coefficients can be complex and measurable
in frequency, without continuity or a common frequency maximizer. The mesh
is constrained by `h^2<=q min_k L_k^2/(16D^2)`; passage to the continuum uses
arbitrarily fine meshes, so this is not an output restriction. Constants can
depend on `q,C_1`, but cannot depend on `D`, mesh, scale count, array dimensions
or coefficient values. Because `q` is fixed in the rough-kernel application,
large constants depending on `q` do not conceal a dependence on the annulus
count.

The continuum corollary initially requires a common finite rectangular
partition of output space whose cells are independent of frequency. The
**coefficient values** on a cell remain measurable functions of frequency.
The wording "partition, independent of xi" is correctly interpreted as a
property of the partition; the following sentence explicitly allows the
values to depend on xi. Subsequent rough-kernel transformations preserve this
finite partition. Arbitrary measurable finite-menu choices are introduced
later by approximation, after the analytic estimate has been proved.

## Reconstruction of the refined window identity

For `a=qL^2`, `omega=xi/L`, the correctly normalized dilated window is

\[
 \operatorname{Dil}_L\ell_\xi(u)
 =\frac{L}{D}\frac{d}{du}\bigl(g_a(u)e^{i\omega u}\bigr).
\]

There is no missing dilation factor. On `2a<s<3a`, the diagonal insertion
`f_{xi,k}/g_s` is bounded uniformly in `D,L,s`: since `|xi|/D<=2`, an explicit
bound is

\[
 \|f_{\xi,k}/g_s\|_\infty
 \le \sqrt3\left(2+\sqrt{2/(e q)}\right).
\]

The real and imaginary parts are Hermitian diagonal maps; the eight-term
expansion of the mixed trace handles complex windows without treating a
complex direction as a Hermitian one.

Set `theta=1/(16D^2)`, `b=theta s`. Then `b/a<3/16`, in particular
`b<a/2`. Conditional Gaussian integration gives the exact formula

\[
 \int g_b(u-d)e^{i\omega'd}g_{a-b}(d)\,dd
 =g_a(u)e^{i\omega'(a-b)u/a}
    e^{-\omega'^2b(a-b)/(2a)}.
\]

Taking `omega'=a omega/(a-b)` proves the manuscript's modulated-Gaussian
identity. Its prefactor has exponent bounded by `6q/13`, because
`|xi|<=2D`, `s/a<3`, and `b/a<=3/16`. Thus its exponential cost is uniform
in `D`. Also

\[
 g_{a-b}(d)\le Cg_{s-b}(d),\qquad
 L/D\le C(q)\sqrt{\theta s}.
\]

Differentiating the **first** Gaussian gives
`-(u-d)/b`, the negative refined row score. The scalar coefficient is exactly

\[
 c(d)=-\frac LD e^{\omega^2ab/(2(a-b))}
 e^{i\omega'd}\frac{g_{a-b}(d)}{g_{s-b}(d)}.
\]

Its real or imaginary part has magnitude at most
`C(q) sqrt(theta s)`. Gaussian row averaging changes the row density only.
The two column densities, including their square roots in the row matrix,
remain fixed. Consequently the averaged Gram and inserted Gram identities
are valid, and all row Grams have the same kernel: strictly positive row
scaling cannot alter it. The upstream probability-average convexity lemma
therefore applies to `(T_v^d,alpha(d) U_v^d)` and yields

\[
 b_{T_v}(K_v)\le C(q)\theta s
    \int V_v(p_0,\ldots,p_v+d,\ldots,p_2;s)\,d\nu_s(d).
\]

The factor `theta s` is required: integration with `ds/s` then produces
`theta integral V_v ds`, exactly the amount controlled by dissipation.

## Reconstruction of the mixed boundary majorant

After expanding the switching edge's Hilbert--Schmidt norm squared, the
measure

\[
 h^{-2}w_v(i_v)w_w(i_w)\,d\pi_d\,d\nu_s(d)
\]

is indeed a probability measure. Using `p_v,p_w` as free coordinates makes
them independent normals of means `u_{i_v},u_{i_w}` and variances
`theta s,s`; independently `d` has mean zero and variance `(1-theta)s`.
The last center is `p_2=d-p_v-p_w`.

The expectation of `h^{-2}w_v(m)w_2(l)` is the density of the additional
Gaussian convolution. Its mean and covariance are exactly

\[
 (u_{i_v},-u_{i_v}-u_{i_w}),\qquad
 \Sigma=s\begin{pmatrix}2\theta&-\theta\\-\theta&3\end{pmatrix}.
\]

The claimed covariance comparison has a direct certificate:

\[
 4s\operatorname{diag}(\theta,1)-\Sigma
 =s\begin{pmatrix}2\theta&\theta\\\theta&1\end{pmatrix},
\]

whose leading principal minor is `2theta` and determinant is
`theta(2-theta)>0`. Hence inverse order compares the Gaussian exponent to
that of `g_{4theta s} g_{4s}`. The normalization ratio is
`4/sqrt(6-theta)<=16/sqrt(95)` for `theta<=1/16`. This gives an explicit
uniform density majorant, including the regime `D -> infinity`.

The Gaussian maximal bound is available in both coordinates because
`h^2<=theta s`. Applying it to `|E|^2` gives

\[
 \mathcal H_E(i,j)^2
 =C(M^{(1)}_{\mathbb Z}M^{(2)}_{\mathbb Z}|E|^2)
       (i_v,-i_v-i_w).
\]

The index map is an exact unimodular bijection of `Z^2`, for both choices of
the row endpoint `v`. Thus `||H_E||_3<=C||E||_3`, independently of `s,theta`.
Cauchy--Schwarz under the probability measure proves the mixed boundary
bound. In particular, there is no unbounded cost from the narrowing row
variance and no evaluation on a measure-zero diagonal.

## Integrated heat costs and switching audit

For rates `(theta,1,1)`, the plane heat identity has second derivative
coefficient `2+theta`. Differentiating the averaging measure
`g_{(1-theta)s}(d) dd` contributes **plus** `(1-theta)` times the averaged
second derivative; integration by parts twice has positive sign. The total
coefficient is therefore `3`, as stated:

\[
 2\partial_s\widetilde J_v
 =3\widetilde Z_v-\theta\widetilde V_v
       -\sum_{w\ne v}\widetilde Y_{v,w}.
\]

Using `2Z_v<=Y_{v,v+1}+Y_{v,v-1}` yields the precise residual factor `1/2`
in the column costs. Each column vertex has variance rate **one**, so the
single-edge heat identity pays its cost with no division by `theta`.
Order comparison is applied to directions supported on the corresponding
single-edge Gram; it remains legitimate if the full star has larger rank.

The switching edge is zero off the disjoint slabs `(2qL_k^2,3qL_k^2)`.
The slabs are disjoint even when the finite integer scale set has gaps.
For a fixed frequency its single-edge costs can be paid separately on each
slab. Cubic boundary terms and cubic edge energies sum by

\[
 \sum_k\int |A_0(i,j)\mu_{ij,k}(\xi)|^3\,d\gamma
 \le C_1^3|A_0(i,j)|^3.
\]

The mixed jump of a star is bounded by
`C(||C_sw||_HS^3+||C_sw||_HS^2||C_fix||_HS)`, obtained by integrating the
first derivative of the positive energy when a whole edge is added. It is
valid at rank changes by continuity. The majorant just reconstructed is
independent of `k,xi,s`, so the mixed contributions sum instead by

\[
 \sum_{i,j}h^2|A_0(i,j)|^2\mathcal H_v(i,j)
  \sum_k\int|\mu_{ij,k}(\xi)|^2\,d\gamma
 \le C n_0^2(n_1+n_2).
\]

This is the decisive exact use of the square-integral hypothesis. No
frequency supremum or integration over a scale-dependent null set replaces
it. The vertex-2 star has no switch, since it uses only the two fixed edges.
All initial energies and fixed-edge frequency costs acquire at most the
factor `gamma(Xi_D)<=4`. Telescoping discards a nonnegative final energy;
the jump sign is controlled by absolute jumps, so there is no assumption
that switching energies decrease. Young's inequality gives the cubic sum,
and independent trilinear normalization of the three inputs converts that
sum into `C product n_v`.

The needed measurability is finite dimensional; supported costs are limits
of positive definite regularizations. Tonelli applies only to nonnegative
costs, and signed center integrations are separately absolutely convergent.

## Rough-kernel reconstruction and boundary cases

The three vanishing moments give a triple primitive `U` whose first three
listed derivatives can be represented from either tail. This makes each
decay Gaussian. With a sufficiently wide, fixed `g_{3q}`, the quotient
`f=U/g_{3q}` has Gaussian-decaying derivatives through order three.
`f,f',f''` are continuous; its third weak derivative is bounded and is
piecewise differentiable with at most `Am` bounded jumps. Bounded classical
derivatives on each interval give one-sided limits at those jumps. Thus its
distributional fourth derivative is a finite measure of variation `O(m)`.

The frequency supremum bound follows from that fourth derivative. The
blockwise square bound follows from the translated third derivative:

\[
 \|f'''(\cdot+D^{-1})-f'''\|_2^2\le Cm/D.
\]

Plancherel and `|exp(i xi/D)-1|>=2 sin(1/2)` for
`D<=|xi|<2D` give the stated `integral |D^3 fhat|^2 dxi<=Cm/D`. The low
block `|xi|<2` is treated separately using Gaussian decay; a high-frequency
argument is not incorrectly applied at zero.

Cutoff convolution approximates all weak derivatives through order three
in `L^1` at rate `m/P_*`, with uniform supremum bound. Interpolation gives
the `L^5` error used by the Gaussian envelope. The product rule for
`(g_{3q}f)'''` has no extra point masses: the second derivative of `f` is
continuous. For `P_*=(2+n)^8`, `m<=A sqrt(n)` implies
`(m/P_*)^(1/5)<=C/n`; at most `An` scales are active at an output point.
The resulting replacement error is uniformly bounded by the same line
maximal envelope.

The Gaussian convolution identity is exactly

\[
 (g_qe^{i\xi\cdot})*(g_qe^{i\xi\cdot})*
 (g_qe^{i\xi\cdot})=g_{3q}e^{i\xi\cdot}.
\]

No damping factor occurs: all three modulation factors multiply to
`exp(i xi z)` on a convolution slice. After differentiation it gives
`(g_{3q}e^{i xi z})'''=D^3H_xi`. Defining
`mu=D^4 fhat chi/sqrt(n)` gives simultaneously the uniform coefficient bound
from `m<=A sqrt(n)` and the square-integral bound from `sum m<=An`.
There are only `O(log(2+n))` frequency blocks after the finite cutoff.

For odd kernels, zeroth and second moments already vanish. Subtracting
`u_k phi`, `u_k=integral zK_k(z) dz`, removes the first. The identity
`Psi=phi-(1/2)Dil_2 phi` cancels all three moments, and the remaining dilation
series has coefficients `2^-j`; the remainder is bounded by
`C2^-J n product ||G_v||_3` and tends to zero for every fixed `n`.

Endpoint grouping was checked with complex coefficients, shared endpoints
and dyadic-boundary endpoints. The half-open choice `[L_k,2L_k)` assigns each
endpoint exactly once. For paired annuli in that group, disjointness gives
`sum(gamma_j-alpha_j)<=1`, controlling smooth terms and their derivatives.
At any nonendpoint radius at most one hard difference is active. At most
two crossing intervals can leave an unpaired endpoint; intervals spanning
the whole dyadic group leave none. The tail formula
`P(v)-c_0=-2g_3''(v)` proves uniform Gaussian tails. Consequently deleting
the at most `2sqrt(n)` groups whose count exceeds `sqrt(n)` is legitimate
pointwise, independent of choices made at other output points.

## Supremum, measurable selection and complete scale coverage

The source's variation definition is the **pointwise** supremum over all
finite rational positive partitions; its count definition is the pointwise
supremum of sums of at most `n` disjoint rational annular increments.
There is no restriction to dyadic endpoints in either definition.

For a finite menu, all annuli have a common positive lower endpoint and a
common finite upper endpoint. Smooth input integrals are bounded on the
compact support of the dual input. Approximation of finitely many selection
sets by unions of rectangles therefore passes the estimate to arbitrary
measurable finite-menu choices. Tie-breaking and choosing a coefficient
from `{1,-1,i,-i}` are measurable; the latter obtains at least half the
modulus of an increment in the real part. Duality against nonnegative
smooth compactly supported functions controls the finite maximum. Countable
exhaustion then places the supremum **inside** the output `L^(3/2)` norm.

For general complex `L^3` inputs, each fixed annulus is continuous in the
inputs by the elementary finite-annulus bound. The difference of two finite
maxima is bounded by a finite sum of these truncation differences. Thus
finite-menu estimates pass to the limit before countable exhaustion. The
common representative lemma supplies absolute integrability and endpoint
continuity simultaneously for every finite annulus.

The rank grouping uses the largest `2^j` increments of any partition, which
are disjoint annuli even though they need not be adjacent to each other.
It therefore yields

\[
 V_r\le\sum_{j\ge0}2^{j/r-j}\mathcal S_{2^j},\qquad
 \|V_r\|_{3/2}\le C\|F\|_3\|G\|_3
   \sum_{j\ge0}(1+j)2^{j(1/r-1/2)}.
\]

This converges precisely for every `r>2`. It establishes the needed full
annular variation once the upstream smooth estimate is supplied; neither
the number of increments nor a dyadic-only scale restriction survives.
It gives no `r=2` endpoint and no nonsymmetric or one-sided Cesaro theorem.

## Concrete falsification probes and their limits

`frequency_audit_computations.py` and its JSON result use Python 3.14.6 with
only standard-library modules. The script evaluates the closed Gaussian
formula for `H_xi` and constructs coefficient phases separately at every
output pair. For discrete quadrature responses `T_{ij,k,xi}`, it chooses

\[
 \mu=\overline T/
 \max\{(\sum_{k,\xi}|T|^2\,\Delta\gamma)^{1/2},\ \max_{k,\xi}|T|\}.
\]

This deliberately aligns every coefficient phase with the output response
while satisfying the finite-menu analogues of both bounds (up to roundoff).
The magnitudes are a simple admissible normalization, not a claim to solve
the entire constrained optimization problem. The dual array can then be
chosen to attain the discrete `ell^(3/2)` norm of this positive response.
Inputs tested were constant arrays, complex linear chirps arranged to cancel
a triangular phase, and independent random-sign arrays, with one/four scales,
`D=1,2,4` and 17/33 nodes per coordinate. The mesh was
`h=1/(4D)`, satisfying the hypothesis at equality for the smallest scale.

The largest sampled normalized output ratio was approximately `3.194` in
the four-scale `D=1` chirp example. No contradiction emerged; the theorem
allows an unspecified constant larger than that. The `D` comparisons also
change the physical support because the node count is held fixed, so they
are **not** evidence of an asymptotic uniform estimate. Midpoint quadrature
is not a certified continuous-frequency integration and no bound or theorem
is inferred from these probes. Their purpose is to expose obvious phase,
sign, normalization or frequency-growth failures. The analytic covariance
certificate above, unlike those probes, is an exact check.

## Exact remaining dependency and reproducibility record

There is no identified remaining gap **within this assigned reconstruction**.
The complete upstream theorem still depends on the independently reviewed
smooth-switch bound and finite-matrix/heat machinery, and the requested
ergodic conclusion additionally needs the new positive-area restriction and
finite-window transference proof. No claim of formal verification is made.
No numerical experiment establishes a singular-integral theorem.

SHA-256 of reviewed source files, relative to the pinned manuscript folder:

| File | SHA-256 |
| --- | --- |
| `build/sections/frequency.tex` | `d7c8163675bcee6040efcab72c6ad0146aed9eccc00ee42d933382f0e6213ec2` |
| `build/sections/rough.tex` | `f5a80e111befed4781b7a9b0d75f2b8d15646c08580c3ad98fe95d48bc877064` |
| `build/sections/completion.tex` | `0d14e5d2a234b36044627628ad1dd960929dd357f3b5fc4e85feb84fe3a7c7d3` |
| `build/sections/introduction.tex` | `0c1678042ab9a0e3c5c21c1acd280d1a43b8e3c65e019bf78f7509a49f26422e` |
| `build/sections/heat.tex` | `c6a85b01fdecf3a7b03bf3ba25ec03a3da68ab71c3c85c5d82da139ce1ebd3c6` |
| `build/sections/matrix.tex` | `914af3c5e87cd4af52b1c7a9e7f2a4ac03d82b9456b8be50b69ffbbbee59f9ad` |
| `build/sections/preliminaries.tex` | `305281fb7f26046eea88b4087beba843ab6e48a62be6158f3a987bd91a68ddb0` |

The reviewed manuscript source belongs to family 082 and is dated October
5, 2026. Its README attributes the work to OpenAI. This audit does not
establish its public priority date or check for later corrections; those
are separate tasks.
