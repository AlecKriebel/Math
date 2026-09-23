# Independent adversarial review: algebra and metric passage

Reviewed: 2026-09-23T03:35:36Z. Scope completion estimate: 100% of this algebra/analysis audit; this is not a completion or priority estimate for the publication project.

This review was performed from the supplied candidate and the original source, before reading other reviewers' conclusions. No numerical evidence is needed for the verdict. No external communication was initiated.

## Verdict and exact scope

**PASS.** For the unit-round geodesic sphere, with target distance induced by either the **unnormalized Hilbert–Schmidt norm** or the **operator norm**, the candidate proves a strong deformation retraction of both the strict Lipschitz sublevel `Lip < 1/2` and the closed sublevel `Lip <= 1/2` onto the constant maps. The advertised factor

\[
q_t=\frac{1-t^2}{1+t^2}
\]

is valid. The construction remains in the original finite-dimensional `U(N)` and is jointly continuous for the uniform topology. There is **no unresolved mathematical gap in this stated theorem**. This review does not establish publication priority.

The source checked was M. Gromov, *101 Questions, Problems and Conjectures around Scalar Curvature*, October 1, 2017, printed pp. 35–36, [original PDF](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf). Its question [?24](i), on printed p. 36, concerns continuous dependence of contractions of maps with Lipschitz constant below one half. The candidate supplies this and the additional preservation of the Lipschitz sublevel. It does not resolve the distinct later questions on arbitrary sphere fibrations.

**Metric wording caution:** shortest nonconstant closed geodesic length `2 pi` does not by itself characterize every bi-invariant metric on `U(N)`. The paper should define its norm explicitly, as the candidate does. The present audit proves the result for the two norms just stated; it does not license an assertion for all bi-invariant metrics having that one normalization.

## 1. Spectral confinement

Put `A=Phi(p)` and `W(x)=A* Phi(x)`, with `*` denoting adjoint. The diameter bound gives

\[
d_\nu(I,W(x))\leq \pi\operatorname{Lip}(\Phi)\leq\pi/2.
\]

For an eigenpair `Wv=exp(i theta)v`, `||v||=1`, `theta in [-pi,pi]`, a piecewise smooth unitary path `U` from `I` to `W` sends `v` to a path in the real unit sphere from `v` to `exp(i theta)v`. The latter points have spherical distance `|theta|`; their inner product over the reals is `cos(theta)`. Its speed is bounded by `||U'||op`, and therefore by `||U'||nu` for either permitted norm. Taking infima proves `|theta| <= d_nu(I,W)`. Thus every eigenangle belongs to `[-pi/2,pi/2]`, and `Re W >= 0` by the spectral theorem.

There is no hidden choice of eigenvectors in the homotopy. Eigenvectors appear only in this pointwise proof. The boundary eigenvalues `i` and `-i` are permitted.

## 2. Noncommutative identities checked in their actual order

Write `R_W=(I+tW)^(-1)` and `F_t(W)=(W+tI)R_W`. The positive matrix inequality

\[
(I+tW)^*(I+tW)=(1+t^2)I+2t\operatorname{Re}W\geq(1+t^2)I
\]

proves invertibility throughout the closed parameter interval and
`||R_W||op <= (1+t^2)^(-1/2)`. In particular there is no `t=1` singularity at the allowed boundary eigenvalues.

The unitarity argument is sound: with `X=W+tI`, `Y=I+tW`, one has `X*X=Y*Y`, whence `(XY^(-1))*(XY^(-1))=I`. No interchange of `X` and `Y` is necessary for this step.

For the difference identity, multiply on the left by `I+tU` and on the right by `I+tV`. Each matrix commutes with a rational function of itself. The resulting numerator is exactly

\[
(U+tI)(I+tV)-(I+tU)(V+tI)
 =U+tUV+tI+t^2V-V-tI-tUV-t^2U
 =(1-t^2)(U-V).
\]

The two occurrences of `UV` have the same order, so they cancel without assuming `UV=VU`. Therefore

\[
F_t(U)-F_t(V)=(1-t^2)R_U(U-V)R_V.
\]

The norm inequality `||BXC||nu <= ||B||op ||X||nu ||C||op` holds for both permitted norms, and yields the claimed chordal estimate. Differentiation gives the same ordered derivative `DF_t(W)[E]=(1-t^2)R_W E R_W`; this also holds for tangent directions that do not commute with `W`.

## 3. The intrinsic length step has no smoothness gap

Let `gamma:[0,ell] -> S^(n-1)` be an arclength parametrized minimizing geodesic. Then `W o gamma` is `L`-Lipschitz into `(U(N),d_nu)`, hence also `L`-Lipschitz into the matrix norm because chordal distance is bounded above by intrinsic distance. As a finite-dimensional vector-valued Lipschitz function it is absolutely continuous, has a derivative almost everywhere, and its derivative has norm at most `L` almost everywhere.

The rational function `F_t` is smooth on an open neighborhood of the image, since every denominator there is invertible. The chain rule for absolutely continuous curves consequently applies. Integrating the derivative estimate gives

\[
\int_0^\ell\|(F_t(W\circ\gamma))'(s)\|_\nu\,ds
\leq q_t\int_0^\ell\|(W\circ\gamma)'(s)\|_\nu\,ds
\leq q_t L\ell.
\]

These integrals are lengths for the induced intrinsic metric. One elementary justification, which also avoids any reliance on an unmentioned differentiability theorem for a Finsler norm, is as follows. If `U,V` are nearby unitary matrices and `Z=U*V-I`, the logarithm power series and the ideal norm inequality give

\[
\|U-V\|_\nu\leq d_\nu(U,V)
\leq \|\log(I+Z)\|_\nu
\leq \frac{\|Z\|_\nu}{1-\|Z\|_{\rm op}}
=\frac{\|U-V\|_\nu}{1-\|U-V\|_{\rm op}}.
\]

Here the exponential path for the skew-Hermitian principal logarithm gives the middle inequality; the final estimate follows term by term for `||Z||op<1`. Thus the ratio of intrinsic and chordal distances tends uniformly to one at short distances. Refining partitions of any continuous curve proves equality of the corresponding curve lengths. In particular the preceding absolutely continuous curve integral is the intrinsic length.

No shortest target geodesic joining `W(x)` and `W(y)` is assumed to remain inside the unitary semicircle. The proof uses the existing curve `W o gamma`, which does remain there. This distinction is essential, and the candidate makes it correctly.

Left multiplication by `A` is an isometry. The endpoint distance of the image curve is bounded by its length. Since `ell=d_S(x,y)`, this proves the stated Lipschitz estimate, including at antipodal domain points (choose any minimizing geodesic).

## 4. Endpoints and joint dependence

`F_0(W)=W`, `F_1(W)=I`, and `F_t(I)=I` are exact identities. It follows that the terminal map is the constant `Phi(p)` and that every constant map is fixed at every time. Thus the target of the retraction is a copy of `U(N)`; the full map space is not asserted to contract to one preselected point.

For two input maps, writing `delta=sup ||Phi-Psi||nu`, the anchor changes by at most `delta` and the normalized input changes by at most `2 delta`. The difference identity therefore yields the uniform bound

\[
\sup_x\|H_t(\Phi)(x)-H_t(\Psi)(x)\|_\nu
\leq(1+2q_t)\delta\leq 3\delta.
\]

Continuity in `t` is uniform on the compact set of accretive unitaries times `[0,1]`; combining these two facts proves joint continuity. On the compact finite-dimensional target, the norm and intrinsic metrics are uniformly equivalent. The candidate therefore proves continuity for the stated uniform topology, not merely pointwise continuity in the input.

A continuous family with an arbitrary parameter space yields a continuous family of homotopies by composition with this joint map. One may alternatively check the finite matrix formula directly in the evaluation variables. No parameter-dependent logarithm or eigenbasis is selected.

## 5. Boundary checks and falsification targets

| Attempted failure | Outcome |
| --- | --- |
| Noncommuting `U,V` | Ordered expansion cancels `UV` exactly; no error. |
| `Re W=0` on some eigenspaces | Denominator singular value remains at least `sqrt(1+t^2)`; no error. |
| Final time `t=1` | Both numerator and denominator are `W+I`; denominator is invertible; exact endpoint. |
| Constant maps and zero Lipschitz constant | Fixed identically, as required by a strong deformation retraction. |
| Merely Lipschitz maps | Absolutely continuous domain-geodesic restrictions justify the length argument. |
| Domain antipodes | Minimizing geodesics exist, and uniqueness is not used. |
| Strict threshold approaching the boundary | Uniform inverse bound and `3 delta` continuity estimate survive; no strict margin is needed. |
| Different anchors for nearby maps | Their change is explicitly included in the continuity estimate. |
| Ambient target chordal metric confused with intrinsic metric | The proof passes through curve lengths and is valid; the local comparison above supplies an explicit justification. |

The optional two-point sphere statement is also correct when its two points have angular distance `pi`. For the second value, apply the scalar derivative bound to each principal eigenangle from zero to that angle. The path `exp(i s diag(theta_j))` and the usual principal-angle distance formula then give the asserted bound for either target norm. This case is not required for the source's `n>=2` geometric setup and may be omitted from a concise paper.

The formula is also equivariant under constant left and right changes of frame: `H_t(Q Phi R)=Q H_t(Phi) R` for unitary `Q,R`. This is immediate from the normalization and conjugation equivariance of `F_t`, and is compatible with the source's discussion of families arising from frames.

## Publication recommendation

The theorem is ready to state as a proved mathematical result under its explicit metrics. Expand the nonsmooth length step by one or two sentences in the paper. Keep priority claims separate from validity: a complete priority audit must still determine what is already known, and no exhaustive absence claim follows from this algebra audit. No additional numerical verifier can improve the deductive status of these exact identities; any supplied script should be labeled an auxiliary check, not a proof of the quantified theorem.
