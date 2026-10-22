# Independent global geometry and exact-algebra audit of PR 521

Problem 30003571. Audit completed 2026-10-13 UTC. Completion estimate: **100% of this assigned geometry/algebra audit**.

## Verdict and precise scope

**PASS for the global geometry and exact counterexample calculation for the explicitly displayed probability-normalized equation.** No mathematical repair is needed in the checked chart patching, strict positivity, Laplacian, eigenmodes, or finite-time sign calculation.

The strongest verified result is conditional in exactly this sense: if the flow displayed in `public/PROOF.md` has a unique solution smooth in the base and fiber through the stated positive time, then the proposed smooth strictly positive initial metric on `O(2,2)` has horizontal curvature exactly `-1/96` at `(s,z,t)=(0,0,log(2)/2)`. The proof correctly isolates smooth finite-time existence as an external analytic input. This audit did not independently authenticate the published source equation, the intended scope of the source question, or the applicability of its existence theorem; those remain external source-validation tasks, not algebraic gaps in this construction.

The accompanying `verify_independent.py` imports no author code and runs neither supplied verifier. It passed **57 exact checks** with SymPy 1.14.0. Its mechanisms are real-coordinate Wirtinger differentiation, a positive Bernstein expansion of the exact determinant, and a polynomial coefficient-matrix solution of the evolution. It uses no positivity grid. `verification_results.json` records every identity and the exact certificates.

## Bundle convention, amplitude, and relative anticanonical line

Let `E=A⊗V` with `A=O_P¹(1)` and `V=C²`. For the convention in the claim, `P(E*)` parametrizes lines in `E*`; the dual of its tautological line is `O_E(1)`. Scalar twisting cancels in projectivization, so

\[
P(E^*)=P^1_s\times P(V^*)=P^1_s\times P^1_z.
\]

The tautological subline is `A*⊠O_z(-1)`, hence its dual is `A⊠O_z(1)=O(1,1)`. Moreover `H⁰(P(V*),O(1))=V`, so the pushforward is `A⊗V=E`, exactly as stipulated. This avoids the possible opposite-projectivization convention, which would change the scalar twist.

The line `O(1,1)` is very ample by the Segre embedding; therefore the vector bundle is ample under the stated tautological criterion. Its square is `L=O(2,2)`. The relative tangent Euler sequence, or direct cancellation of the base factor, gives

\[
K^{-1}_{X/S}=O_E(2)\otimes f^*(\det E)^{-1}=O(0,2).
\]

Thus the stated fiber density is a legitimate relative anticanonical density after choosing a local determinant frame. A different holomorphic determinant frame multiplies the unnormalized density by a positive base factor. It cancels in the probability normalization. No global determinant trivialization is assumed.

## All four chart weights are genuine smooth metric weights

Write a local radial base variable `U` and fiber variable `V`. In each chart put

\[
p=\begin{cases}U/(1+U)&s\text{ finite},\\1/(1+U)&s\text{ inverted},\end{cases}
\qquad
x=\begin{cases}V/(1+V)&z\text{ finite},\\1/(1+V)&z\text{ inverted}.\end{cases}
\]

The four local weights are uniformly described by

\[
2\log(1+U)+2\log(1+V)+(2-\epsilon)(1-p)+\delta p x^2.
\]

On changing `s` to `1/s`, the weight changes by `-2 log|s|²`; changing `z` to `1/z` adds `-2 log|z|²`. These are precisely the weights of the `O(2,2)` frame transitions. The new expressions have no singular denominators at `U=0` or `V=0`. The perturbations are globally smooth real functions. The checker verifies all three nontrivial overlap formulas separately.

Dividing each local weight by two changes its transition law to that of `O(1,1)` and divides its curvature by two. The resulting metric is smooth and strictly positive, and its square is exactly the proposed metric on `L`.

## Independent strict-positivity certificate on the whole compact surface

The checker differentiates in `Re(s),Im(s),Re(z),Im(z)` and uses

\[
\phi_{s\bar s}=\tfrac14(\phi_{rr}+\phi_{aa}),\quad
\phi_{z\bar z}=\tfrac14(\phi_{zz}+\phi_{bb}),\quad
\phi_{s\bar z}=\tfrac14(\phi_{rz}+\phi_{ab}+i\phi_{rb}-i\phi_{az}).
\]

Rotational invariance permits evaluation at zero phases; the diagonal entries and mixed modulus are unchanged by those rotations. Direct differentiation in all four charts reproduces

\[
A=4p+(\epsilon+\delta x^2)(1-2p),\quad
B=2+2\delta p x(2-3x),\quad
Q=4\delta^2p(1-p)x^3(1-x).
\]

These are normalized by the local product Fubini–Study metric, so they are meaningful and continuous at all chart boundaries.

For an independent continuum check, define the Bernstein basis `b_i^m(y)=binom(m,i)y^i(1-y)^(m-i)`. It is nonnegative and sums to one on `[0,1]`. The exact determinant has the expansion

\[
AB-Q=\sum_{i=0}^{2}\sum_{j=0}^{4}c_{ij}b_i^2(p)b_j^4(x),
\]

where the coefficient matrix is

\[
(c_{ij})=\begin{pmatrix}
1/48&1/48&5/48&13/48&25/48\\
4&3073/768&3073/768&4&1511/384\\
383/48&1149/128&3415/384&23/3&359/64
\end{pmatrix}.
\]

Every entry is at least `1/48`. The exact reconstruction is verified symbolically, giving the stronger universal bound

\[
AB-Q\ge 1/48>0.
\]

The same independent method gives `A≥1/96` and `B≥3/2`. Thus the full Hermitian Hessian is positive definite in every tangent direction everywhere on the compact total space. In particular the initially delicate point `p=x=0` has `A=1/96,B=2,Q=0`; no zero initial direction is hidden. All four corners and all infinity edges lie in the same closed-square certificate.

The draft's weaker determinant estimate `1/64+(159/32)p` is also correct: its stated nonnegative remainders expand to the claimed `A`, `B`, and `Q` bounds. The supplied finite grid is supplementary evidence and is not needed for either continuum proof.

## Exact central-fiber evolution, derived independently

Take standard planar area for clarity. On `s=0`, the weight is

\[
\phi_F=2\log(1+|z|^2)+2-\epsilon.
\]

Its curvature density is `2/(1+|z|²)²`, of mass `2π`; its anticanonical density is `exp(-(2-epsilon))/(1+|z|²)²`, of mass `π exp(-(2-epsilon))`. Both probability densities are therefore `dA/[π(1+|z|²)²]`. The normalized flow right side is zero on this fiber.

The base rotation symmetry is a genuine lifted bundle symmetry. Uniqueness preserves it, so all first base derivatives vanish at `s=0`. Differentiating those identities in the fiber gives the vanishing mixed coefficient. The central fiber remains stationary by fiberwise uniqueness. Consequently differentiating the displayed scalar equation is exact: the quadratic first-derivative terms in `∂s∂bar_s log g` and `∂s∂bar_s log I` vanish, leaving

\[
w_t=\Delta_Fw+w-\int_0^1w(x,t)dx,
\qquad w(x,0)=\epsilon+\delta x^2.
\]

No linearization parameter, truncated nonlinear expansion, or small-time extrapolation is used. The stationarity and symmetry make this equation close on the actual second derivative.

Radial integration gives `dx=dv/(1+v)²`, and independent real-coordinate differentiation for a generic function verifies

\[
\Delta_FF=\tfrac12\{x(1-x)F''+(1-2x)F'\}.
\]

Rather than use the draft's eigenmode ansatz, the independent calculation applies the full generator to `(1,x,x²)`. Its matrix is

\[
T=\begin{pmatrix}0&0&-1/3\\0&0&2\\0&0&-2\end{pmatrix}.
\]

Solving the coefficient system with the stated initial value gives, for `q=exp(-2t)`,

\[
w(x,t)=\epsilon-\frac\delta6(1-q)+\delta(1-q)x+\delta qx^2.
\]

It agrees identically with the draft's `P₁,P₂` expression. Independently checked eigenvalues are `Δ_FP₁=-P₁` and `Δ_FP₂=-3P₂`. The mean is constant at `epsilon+delta/3`. Uniqueness of this linear closed equation follows from mean conservation and the scalar heat maximum principle.

For all positive times, `w_x=delta[(1-q)+2qx]≥0`; the central-fiber minimum is therefore at `x=0`, not at an unexamined interior point or at the infinity pole. At `q=1/2` its value is

\[
1/96-(1/4)(1/2)/6=-1/96.
\]

The zero crossing is exactly `q=3/4`, or `t=(1/2)log(4/3)`. At the selected negative point the mixed coefficient still vanishes and the fiber coefficient is `2`, so the curvature is negative on the actual horizontal vector `∂/∂s`; it is also the negative Schur complement. Smoothness then gives an open neighborhood of negative horizontal curvature at the selected finite time.

## Normalization attacks and code/proof consistency

Multiplying the Monge–Ampère numerator by its fixed fiber mass changes the weight solution by a function of time and changes no curvature. Positive rescaling of the `dd^c` convention likewise cannot change the sign of the computed curvature.

For a root weight `psi=phi/r` and time `tau=t/r`, direct substitution gives

\[
\psi_\tau=\log\psi_{z\bar z}+r\psi+\log\int e^{-r\psi}dA+C'.
\]

Its central second variation has operator `Δ_psi+r-r mean`, with `Δ_psi=rΔ_phi`. The checker verifies this conversion. For rank two the negative coefficient becomes `-1/192` and the stated time becomes `tau=log(2)/4`. The sign survives coherent root/time conversion. One cannot merely replace the reaction coefficient by two while leaving the metric, Laplacian, density normalization, and time untouched.

As a negative control, removing the anticanonical probability denominator altogether produces a genuinely different equation. Its pole derivative initially is `epsilon>0`, rather than `-delta/3`. Its exact pole coefficient grows for all positive time: writing `growth=exp(t)` and `q=exp(-2t)`, its derivative is `epsilon*growth+delta(growth-q)/3>0`. Thus this counterexample must be attached to the stated normalized flow, as the draft does.

A positive product weight is stationary for the displayed probability equation; its constant horizontal jet has `w-mean(w)=0`. This is a useful convention control, but authenticating any conflicting printed source formula is outside this sub-audit.

After obtaining the independent certificates and evolution, I compared the formulas and checks in `public/verify.py` and `audit/audit_verify.py`. Their chart Hessians, continuum remainder decompositions, radial Laplacian, eigenmodes, exact target value, and root/time conversion agree with the independently derived results. The provided grid is correctly described as supplementary. Neither code claims to prove the smooth-existence input. There is no checked proof/code inconsistency.

## Exact gaps and necessary repairs

**No repair to the checked geometry or algebra is necessary.** Retain the scope qualification that this is a counterexample for the explicitly displayed probability-normalized `O_E(r)`-weight flow and not a claim about other flow choices or the Griffiths conjecture.

Before treating the PR as an answer to the source problem, separately verify the published defining equation, its conventions, the requested class of initial metrics, and the cited finite-time smooth-existence theorem. This audit's algebra cannot establish those external dependencies. If those checks match the draft, no further mathematical gap has been found in the construction.
