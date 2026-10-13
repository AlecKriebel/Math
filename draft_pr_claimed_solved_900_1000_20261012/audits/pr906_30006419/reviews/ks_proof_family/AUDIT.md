# Adversarial proof review: Korevaar–Schoen sphere theorem

**Verdict: PASS for the full metric-Sobolev framework of the cited source.** The frozen companion proof establishes that a locally KS-minimizing map `u ∈ W¹,²(S²,X)` into any complete metric space is infinitesimally `(4+√17)`-quasiconformal. The preliminary differential/chain-rule framework is the ordinary source framework, not an extra restriction to smooth targets, proper targets, nondegenerate differentials, or maps already known to be quasiconformal. No fatal gap or concrete counterexample was found. Priority and optimality are not assessed here.

Audited head: `32eaecaa8907dbf674e65b138b000cdcc49004ae`, PR 906, problem `30006419 / OWR-14299521-012`. Audited candidate: `author/KOREVAAR_SCHOEN.md`, 6,702 bytes, SHA-256 `4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe`. The original candidate was not modified. This family reconstructed the proof in `INDEPENDENT_DERIVATION.md` before reading `audit_b/KS_APPENDIX_AUDIT.md`; no author or previous-audit verification code was imported.

## Exact claim and success criteria

Fix the KS seminorm density `I(s)=π⁻¹∫S¹ s(v)²dv` and the standard sphere metric. Local minimization has the source's neighborhoodwise quantifier: every point has one neighborhood on whose relatively compact Lipschitz subdomains all same-trace Sobolev competitors have at least the original energy. The required conclusion is the almost-everywhere inequality `M(s)≤Qm(s)`, with `Q=4+√17`, where `s` is the approximate metric differential in an orthonormal domain frame. The zero seminorm must satisfy it, and nonzero rank-one seminorms must be excluded. A proof only for quadratic differentials, only for globally minimizing maps, or with a hidden smoothness assumption on `s` would fail this review.

## Source framework and standard inputs

The [cited paper, Sections 2.4, 3, and 6](https://arxiv.org/html/2503.08553v1) uses complete targets and essentially separably valued Sobolev maps. It supplies almost-everywhere seminorm differentials and the integral representation of Reshetnyak energy. Its definitions of infinitesimal quasiconformality, KS energy, and neighborhoodwise harmonicity agree with the audited claim. The source family independently retrieved the versioned official PDF and verified its SHA-256 `23c2b27bf9a39649cea4dc820815c73cb983224488f66de2ccdfe0fc9254dc28`, matching the original source ledger, and directly checked Definitions 3.1 and 6.1. The displayed HTML date is not used as a mathematical version certificate. No final publisher text is claimed to have been examined.

Standard inputs not proved from first principles in the candidate are: existence and measurability of the approximate metric differential; its quadratic energy representation and integrability; ordinary scalar Sobolev composition; distributional Weyl regularity for `∂bar`; and Liouville's theorem. These do not assert the desired quasiconformality and are not equivalent replacements for the central difficulty. Smooth-domain differential composition also follows directly from the approximate-differential definition, as detailed below. The candidate supplies the substantive stress computation and quantitative nondegeneracy argument.

## 1. Arbitrary nonsmooth and degenerate seminorms

For a finite planar seminorm `s`, homogeneity and the angular Jacobian of `v↦Av/|Av|` give

`F_s(A):=I(s∘A)/det A = [π(det A)²]⁻¹∫S¹ s(w)²|A⁻¹w|⁻⁴dw`.

Both exponents are correct. The change of angular variables is a smooth orientation-preserving circle diffeomorphism for every `A∈GL⁺(2)`. It never differentiates `s`. On a compact matrix neighborhood of the identity, the inverse-length kernel and all of its finite-order derivatives are uniformly bounded because the least singular value stays positive. The resulting derivative bounds are `C_k M(s)²`, including rank one and zero.

Differentiating the determinant and inverse-length factors at the identity gives respectively `−2 tr B` and `4 w·Bw`, so

`DF_s(I)[B]=T(s):B`, `T(s)=π⁻¹∫s(w)²(4w⊗w−2I)dw`.

The tensor is symmetric and tracefree pointwise. Its operator norm is bounded by `4M²`. Differentiation of a nonsmooth support function, nonexistent pointwise derivatives in the angular variable, or a differentiable target norm is not being assumed. The seminorm field can vary arbitrarily in space.

## 2. Admissible domain variation and dominated differentiation

Choose a conformal coordinate disc compactly contained in a minimizing neighborhood. A test vector field has compact support in that disc. Extend it by zero to the plane. For sufficiently small positive and negative `t`, `phi_t(x)=x+tV(x)` is a smooth global diffeomorphism: `|t| Lip(V)<1` gives injectivity and a co-Lipschitz estimate, and the map is proper and locally onto. It preserves a smaller disc containing the support and is identical on a boundary collar. This smaller disc is a permitted Lipschitz subdomain.

Distance functions composed with `u∘phi_t` are scalar Sobolev by ordinary smooth composition, with common upper bound `h(phi_t(x))||Dphi_t(x)||`. Change of variables makes this upper bound square integrable. L² and essential separability are preserved as well. The collar equality implies exactly equal traces. Thus the original locality quantifier genuinely supplies this competitor for both signs of `t`; no global minimization hypothesis is introduced.

For each fixed `t`, approximate differentiability gives `s_{u∘phi_t,x}=s_{u,phi_t(x)}∘Dphi_t(x)`. A smooth biLipschitz change preserves density-zero exceptional sets. Its first-order linearization changes the seminorm evaluation by `o(|h|)`; this proves the asserted composition without any target regularity. The representation in coordinate vectors is consistent with the source's exponential-coordinate definition.

Now change variables to `y=phi_t(x)`. The exact energy is

`∫ F_{s_y}(A_t(y))dy`, where `A_t(y)=Dphi_t(phi_t⁻¹(y))`.

The seminorm field is now held fixed at `y`. Its spatial derivative is neither needed nor silently set to zero. The smooth matrix family has `A_0=I` and derivative `DV(y)` at zero, and stays uniformly in a compact matrix neighborhood. Measurability of `s_y` makes the integrand measurable. Dominated difference quotients are bounded by `C M(s_y)²`, integrable by the Sobolev energy representation. This justifies two-sided differentiation of the integral. Exceptional sets for the chain rule may depend on `t`: each exact integral identity is valid separately, and differentiation thereafter uses one fixed measurable field, so an uncountable common exceptional set is unnecessary.

A conformal metric `g=e^{2f(x)}(dx²+dy²)` contributes `e^{-2f}` to the quadratic density in the coordinate differential and `e^{2f}` to the area measure. These cancel exactly. Curvature and a variable conformal factor therefore produce no extra coefficient or connection term. Local minimality yields `∫T(s):DV=0` for every local test field.

## 3. Holomorphic stress, coordinate covariance, and poles

Write `T=[[a,b],[b,−a]]`. The local weak divergence equations are `a_x+b_y=0`, `b_x−a_y=0`. They are precisely `∂bar(a−ib)=0`, with `a,b∈L¹_loc`. Weyl regularity provides a holomorphic representative. One can also convolve locally: the smoothed coefficients satisfy the classical Cauchy–Riemann equations, and local analytic mean-value estimates turn L¹ convergence into a holomorphic limiting representative.

For a conformal coordinate transition `z=z(w)` with derivative `λR_theta`, the new seminorm is `λs∘R_theta`. Angular substitution yields `T_new=λ²R_theta^T T_old R_theta`, so `q_new=(dz/dw)²q_old`, where `q=a−ib`. This is the correct complex square, including its sign and conjugation convention. The a.e. transformation law extends to holomorphic representatives by uniqueness. It constructs one global holomorphic quadratic differential on the sphere.

The north and south poles each have an actual minimizing coordinate neighborhood. The weak equation is valid there just as elsewhere, so no unjustified puncture removal or merely global L¹ argument is substituted. In `w=1/z`, the plane coefficient is `q_z=z⁻⁴ q_w(1/z)`. It is entire and decays as `O(|z|⁻⁴)`, hence zero by Liouville. Consequently the original measurable stress vanishes almost everywhere on a finite coordinate cover.

This tensor conclusion addresses arbitrary anisotropy directions simultaneously. It does not choose a direction field, insert measurable direction-dependent deformations, or assume any spatial derivative of an eigenvector field. Once `T(s_z)=0` is known, the next argument is pointwise and may choose a minimizing direction independently for each seminorm. No measurable choice is required.

## 4. Exact constant and all boundary cases

For a nonzero balanced seminorm, normalize `M=1`. Continuity gives a unit minimum direction; use it as `e₂`, with `s(e₂)=m`, and write `L=s(e₁)`. For every unit vector, the triangle inequality gives `s(v)≤L|v₁|+m|v₂|≤√(L²+m²)`. Hence `L²≥1−m²`. It is not assumed that `e₁` itself maximizes `s`.

Compare with the rank-one seminorm `r(v)=L|v₁|`. The reverse triangle inequality yields `|s(v)−r(v)|≤m|v₂|≤m`. Both seminorms are at most one on the unit circle, so their squared values differ by at most `2m`. The kernel `4v⊗v−2I` has operator norm exactly 2, and the angular measure is `2π`. Therefore `||T(s)−T(r)||op≤8m` with precisely the stated normalization.

Fourth angular moments give `T(r)=L² diag(1,−1)`. The balance condition implies `1−m²≤L²≤8m`. Since `m≥0`, it follows that `m≥√17−4`; the reciprocal is exactly `4+√17`. Undoing the normalization gives the claimed ratio. For the zero seminorm, the inequality is trivial. If a planar seminorm has a nonzero kernel and is nonzero, it is rank one; equivalently here it has `m=0`, which contradicts the estimate. Thus no unstated full-rank hypothesis is needed.

The normalization `I(|·|)=2` is correct for the source's angular formula. For a quadratic seminorm `s²(v)=v^TGv`, the stress is `2G−tr(G)I`. Changing the overall energy by a positive constant scales the entire stress and its comparison estimate together; it does not change this final distortion bound. Non-Euclidean fourfold-invariant norms have zero stress, so the argument properly yields bounded distortion rather than the stronger conclusion that every tangent norm is round.

## 5. Reproducible controls and falsification attempts

Run `python3 independent_checks.py` from this review folder. The script uses only the Python standard library and 131,072 midpoint circle samples. Its stress is computed as the second Fourier mode, independently of the candidate's matrix-kernel implementation. It compares the direct angular density with the inverse-matrix formula for three substantially nonidentity matrices; checks centered first variation, rotation covariance, and scaling; and includes zero, Euclidean, anisotropic quadratic, weighted l¹, weighted l∞, rotated rank-one, polygonal max-linear, and two fourfold norms.

All controls passed. Maximum angular-formula discrepancy was `1.931e−9`; maximum first-variation discrepancy was `4.005e−7` at step `10⁻³`; maximum rotation discrepancy was `4.543e−11`. The exact quadratic and rank-one stresses and the zero stresses of balanced non-Euclidean norms passed. These are numerical consistency controls, not certified bounds for all seminorms; the universal estimates were derived above.

An additional exact rational control uses `u(x,y)=(x²,y²)` and a boundary-fixed polynomial domain variation on `[-1,1]²`. Direct differentiation includes the changing spatial differential field; fixed-field stress differentiation does not. Both integrate to `−128/45`. This catches an incorrect treatment of the spatial composition term. Deliberately replacing the inverse-length exponent 4 by 2, or the determinant exponent 2 by 1, gives errors larger than 1.02 and 0.65 respectively. The controls therefore detect central normalization mutations instead of merely reproducing the desired output.

After independent reconstruction, the prior KS appendix audit was read. It reaches the same verdict. Its evidence is corroboration, not a premise of this review. The companion Reshetnyak counterexample is not reviewed or used here.

## Disposition and exact remaining gap

The strongest verified claim is the candidate's theorem, with its explicit nonsharp constant, for every complete target and the exact source locality/Sobolev framework. Indeed the proof only needs stationarity under the exhibited local smooth domain variations. There is no outstanding proof obstruction and no unsupported equivalent-hardness reduction to mark blocked. The route is verified, not merely conditionally promising.

Limits: this is an adversarial mathematical review, not a formal proof-assistant certification; standard metric-Sobolev existence/measurability facts and elementary complex-analytic regularity are accepted inputs whose usage was checked. Optimal distortion, historical priority, final-publisher wording, and the broad-energy negative result are outside this family's verdict. No candidate correction, source redistribution, external contact, Git mutation, deposit, or publication was performed.
