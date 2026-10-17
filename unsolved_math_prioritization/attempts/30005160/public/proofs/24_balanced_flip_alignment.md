# Proof 24  Balanced flips against an arbitrary aligned ellipse group

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Arithmetic progressions with radial noise and joins](09_robust_ap_and_joins.md); [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md); [Angular order under a common rotation](15_common_rotation.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## 1. Center-square convexity for independent ellipse sums

Let

`S=sum_j exp(i delta_j)(A_j cos(theta_j)+i B_j sin(theta_j))`,

where the angles are independent and uniform, `A_j,B_j>=0`, and the rotations `delta_j` are arbitrary. Let `Y` be independent bounded rotationally invariant noise. For every `p>=2`,

`g_p(s)=E |sqrt(s)+S+Y|^p`, `s>=0`,

is convex. More generally, for every continuous radial planar bisubharmonic function `Phi`,

`g_Phi(s)=E Phi(sqrt(s)+S+Y)`

is convex. Only bounded regions of definition of `Phi` large enough for the expectations are needed.

### Proof for powers

Fix a projection angle `t`. Each projected ellipse is a centered sinusoid and thus has the same law as `r_j(t) cos(theta_j)` for some nonnegative deterministic radius `r_j(t)`. These scalar variables remain independent. Consequently the projection of `S+Y` has the law of `Re W_t`, where

`W_t=sum_j r_j(t) Z_j+Y`

is a bounded rotationally invariant variable and the `Z_j` are independent uniform unit complex numbers. This assertion concerns only a fixed projection angle; no joint-in-t coupling is asserted or needed.

For `p>2`, put `h_t(x)=E |x+Re W_t|^p`. The accepted scalar arcsine-potential lemma gives that `h_t` is even, `C^2`, and `h_t''` is even and nondecreasing on the nonnegative half-line. In particular, for `x>0`,

`x h_t''(x)-h_t'(x) = integral_0^x [h_t''(x)-h_t''(u)] du >=0`,

since `h_t'(0)=0`. Therefore

`d^2/ds^2 h_t(sqrt(s)) = [sqrt(s) h_t''(sqrt(s))-h_t'(sqrt(s))]/[4 s^(3/2)] >=0`

for `s>0`; continuity extends convexity to zero. The same holds for `h_t(|cos t| sqrt(s))`, by nonnegative linear rescaling of `s`.

The scalar projection identity and Fubini give

`m_p g_p(s)=E_t h_t(sqrt(s) cos t)`, `m_p=E |cos t|^p>0`.

The right side is an average of convex functions of `s`, proving the claim for `p>2`. For `p=2`, independent zero means give `g_2(s)=s+E|S+Y|^2`, so it is affine. Degenerate ellipse radii are allowed throughout.

### Proof for the Green kernel and radial bisubharmonic cone

First set `Y=rho Z`, where `rho>=0`. Fix `s_1,s_2>=0` and `lambda in [0,1]`, and put `s=lambda s_1+(1-lambda)s_2`. The power convexity gap

`lambda g_p(s_1)+(1-lambda)g_p(s_2)-g_p(s)`

is nonnegative for every `p>2` and is zero at `p=2`. All variables in these three expectations are bounded. Differentiation at `p=2` is justified by the continuous extension of `r^p log r` at `r=0` and a uniform compact bound for `p` near two. Taking the right derivative proves the same convexity inequality for

`g_{K,rho}(s)=E K(sqrt(s)+S+rho Z)`, `K(z)=|z|^2 log|z|`, `K(0)=0`.

For a general continuous radial bisubharmonic test, use the accepted local radial Green representation on a disk containing all three supports:

`Phi(z)=a+b|z|^2+(1/(8pi)) integral K(z-w) dmu(w)`,

with finite nonnegative radial `mu`. Decompose `mu` into uniform circle measures. The constant term cancels in the convexity gap, and the quadratic term cancels because `E|sqrt(s)+S|^2=s+E|S|^2`. Each circle kernel has nonnegative gap by the preceding paragraph; boundedness on the relevant compact set justifies Fubini. Thus `g_Phi` is convex.

Finally, convolution by the independent bounded radial `Y` preserves radiality, continuity, and distributional bisubharmonicity. Apply the result to `Psi(z)=E Phi(z+Y)` to include arbitrary `Y`. The same argument also follows directly from the power proof with that `Y` retained.

The result is convexity in the **squared size of one deterministic center**. It does not imply convex order of the squared moduli under mixed sign changes, and it does not imply that the sign gap increases with the center.

## 2. Aligning any balanced flipped group

Let

`S=sum_j(A_j cos(theta_j)+i B_j sin(theta_j))`, `A_j>=B_j>=0`,

be an arbitrary aligned ellipse sum. Let `V` be any bounded symmetric real random variable independent of `S`. For every `c>=0` and every continuous radial planar bisubharmonic test `Phi`,

`E Phi(c+S+V) >= E Phi(c+S+iV)`.                                      (2.1)

Arbitrary independent bounded radial noise can be included on both sides.

### Proof

Absorb the radial noise into the test. Write

`F(w)=E_S Phi(w+S)`, `g(s)=F(sqrt(s))`.

Section 1 makes `g` convex. Also `F(x)=F(-x)` for real `x`, because `S` is centrally symmetric and `Phi` is radial.

The common-rotation theorem in [Proof 15](15_common_rotation.md) gives

`F(w)<=F(|w|)` for every complex `w`.                                  (2.2)

Indeed, writing `w=r exp(i alpha)`, radiality yields

`F(w)=E Phi(r+exp(-i alpha)S)`;

the all-aligned orientation is a global maximum of the common-rotation expectation, using the evenness and pi-periodicity in that theorem. The zero case follows directly.

For each real `v`, center-square convexity gives

`[F(c+v)+F(c-v)]/2`

`= [g((c+v)^2)+g((c-v)^2)]/2`

`>=g(c^2+v^2)=F(sqrt(c^2+v^2))>=F(c+iv)`.

Average in the symmetric variable `V`; its symmetry identifies the left side with `E F(c+V)`. This proves (2.1). No monotonicity of a difference as a function of `c` has been used.

## 3. Consequences for centered-cross signs and coefficient boxes

Use the endpoint representation

`c+sum_j(a_j Z_j+s_j b_j/Z_j)`, `a_j,b_j>=0`, `s_j in {-1,+1}`.

A pair is called balanced if `a_j=b_j`; it is circular if `a_j b_j=0`; it is genuinely unequal if `a_j b_j>0` and `a_j!=b_j`. Circular summands can be absorbed into independent radial noise. After harmless independent phase changes, a balanced pair is a symmetric real cosine if `s_j=+1`, and an imaginary symmetric cosine if `s_j=-1`.

**Sign-pattern theorem.** The all-positive pattern dominates every sign pattern for which all genuinely unequal pairs have the same product sign. The comparison holds for every continuous radial planar bisubharmonic test and after arbitrary independent bounded radial noise.

If all genuinely unequal pairs are unflipped, put all unflipped ellipse variables into `S` and sum all flipped balanced variables into `iV`. Equation (2.1) aligns `V`, proving the result. If there are no genuinely unequal pairs this case alone suffices.

If all genuinely unequal pairs are flipped, let `H` be `c` plus the sum of the unflipped balanced variables, and let `S` be the aligned sum obtained from every flipped pair before its common quarter-turn. Conditional on the real number `H=h`, the earlier common-rotation theorem gives

`E_S Phi(h+S)>=E_S Phi(h+iS)`.

This is valid for `h<0` as well: central symmetry of `S` and radiality reduce `h` to `|h|`. Averaging in `H` proves the result.

**Full prescribed-majorant corollary.** If the prescribed nonnegative endpoint magnitudes contain at most one genuinely unequal pair, the full real coefficient-box majorant inequality holds for every `p>=2`, with arbitrary independent bounded radial noise. Every sign vertex falls under the sign-pattern theorem; power moments are convex in the real coefficient vector, so the sign-vertex comparison extends to its coefficient box. The center coordinate is included in that box. This box step is asserted for powers, not arbitrary nonconvex tests in the radial cone.

This extends the previous balanced-or-circular prescribed-majorant result. It still does not resolve two genuinely unequal pairs with opposite product signs, even with only two total pairs. Therefore it does not establish the missing general classification on `2<p<3`.
