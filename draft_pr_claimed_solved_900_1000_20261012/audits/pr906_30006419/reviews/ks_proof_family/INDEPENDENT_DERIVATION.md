# Independent reconstruction before consulting the prior KS audit

Frozen candidate: `author/KOREVAAR_SCHOEN.md` at head `32eaecaa8907dbf674e65b138b000cdcc49004ae`.

## Angular formula and first variation

Let `s` be any finite seminorm on R²; continuity follows from the triangle inequality and a finite basis. For oriented invertible `A`, set `e(theta)=(cos theta,sin theta)`, `rho(theta)=|A e(theta)|`, and `w=A e/rho`. The angular derivative is `d arg(w)/d theta = det(A)/rho²`. Homogeneity gives `s(Ae)²=rho² s(w)²`. Thus

`F_s(A)=I_avg(s∘A)/det A = [π(det A)²]⁻¹ ∫ s(w)² |A⁻¹w|⁻⁴ dw`.

For `A=I+tB`, `det(A)⁻²=1-2t tr B+O(t²)` and `|A⁻¹w|⁻⁴=1+4t(w·Bw)+O(t²)`. This proves exactly

`DF_s(I)[B] = π⁻¹ ∫s(w)² [4w·Bw-2 tr B]dw`.

The stress is symmetric, tracefree, and has operator norm at most `4 M(s)²`. The kernel and all finite-order matrix derivatives are bounded on a compact matrix neighborhood of `I`, so the same derivative bounds with `C M²` hold for arbitrary norms, rank-one seminorms, and zero seminorms. No derivative of `s` is used.

## Full domain variation and analytic quantifiers

In a coordinate disc compactly inside a fixed minimizing neighborhood, any compactly supported smooth vector field `V` extends by zero to R². For `|t| Lip(V)<1`, `phi_t=I+tV` is a smooth global diffeomorphism (injective co-Lipschitz; proper; locally onto; image both open and closed). Choosing a smaller disc enclosing the support makes `phi_t` a self-diffeomorphism of the disc, identical on a boundary collar. The competitor `u∘phi_t` is Sobolev by applying the scalar smooth-composition chain rule to every distance function, with transported common upper bound multiplied by `||Dphi_t||`. Its trace agrees because the two maps agree on a collar. Essential separability and L² are preserved by the biLipschitz change of variables.

Approximate metric differentiation composes with `Dphi_t`: density-zero exceptional sets remain density-zero under a local biLipschitz map; the C¹ linearization error contributes `o(|h|)` through the seminorm; the coordinate/exponential discrepancy is also `o(|h|)`. This argument proves the chain rule directly from the definition for each fixed `t`.

The exact energy identity after changing to `y=phi_t(x)` is `E(u∘phi_t)=∫F_{s_y}(A_t(y))dy`, where `A_t(y)=Dphi_t(phi_t⁻¹(y))`. In a conformal Riemannian chart the metric scale in the quadratic density cancels its reciprocal area scale, so there is no omitted variable coefficient. There is likewise no spatial derivative of `s_y`: the substitution fixed it. `A_0=I`, `dA_t/dt|_0=DV(y)`, and `A_t,dA_t/dt` are uniformly bounded near zero. Since `M(s_y)²` is locally integrable, dominated differentiation is valid. A common null set across uncountably many `t` is not needed: the exact integral identity is valid separately at every `t`, then the fixed `s_y` kernel is differentiated. Two-sided minimality gives `∫T(s_y):DV(y)dy=0`.

Measurability: standard metric-Sobolev differentiation provides a measurable seminorm field; equivalently it suffices that evaluations on a countable dense unit-circle set are measurable. Continuous evaluation, angular integration, and suprema over that set make `M,T,a,b` measurable. Integrability follows from the source identity `E_+²=∫M²`.

## Holomorphic gluing and all anisotropy directions

Writing `T=[[a,b],[b,-a]]`, integration against arbitrary two-component test fields yields `a_x+b_y=0` and `b_x-a_y=0`. Hence `q=a-ib` satisfies `∂bar q=0` distributionally. With `a,b∈L¹_loc`, convolution and Weyl's lemma give a holomorphic representative. For a conformal transition with Jacobian `λR_theta`, the new seminorm is `λ s∘R_theta`. Angular substitution gives `T_new=λ²R_theta^T T_old R_theta`, whence `q_new=λ²e^{2i theta}q_old=(dz/dw)²q_old`. The a.e. transition equation extends to the holomorphic representatives by uniqueness. The result is a global holomorphic quadratic differential.

Both sphere poles have ordinary coordinate discs inside minimizing neighborhoods, so the weak equation holds there too; no unproved removal of a puncture is invoked. In `w=1/z`, `q_z=z⁻⁴q_w(1/z)`; boundedness of `q_w` near zero gives the decay `O(|z|⁻⁴)`. An entire function with this decay is zero. Thus the entire tensor vanishes almost everywhere, covering every anisotropy direction at once. No measurable eigenvector/minimizer selection, pointwise variation, or localization of variable rotation coefficients is necessary.

## Pointwise quantitative step, including degeneracy

Fix any nonzero seminorm with zero stress. Normalize `M=1`. A minimum direction exists by continuity and compactness. Rotate so `s(e₂)=m=min_{|v|=1}s(v)` and define `L=s(e₁)≤1`. The triangle inequality gives `1=M≤sqrt(L²+m²)`. The reverse triangle inequality applied to `v₁e₁+v₂e₂` gives `|s(v)-L|v₁||≤m|v₂|≤m`. Since `s(v)` and `L|v₁|` are both ≤1, `|s(v)²-L²v₁²|≤2m`. The operator norm of `4v⊗v-2I` is exactly 2; the circle has measure 2π. Therefore the stress difference has operator norm ≤8m.

The elementary circle moments give `T(L|v₁|)=diag(L²,-L²)`. Zero stress therefore implies `1-m²≤L²≤8m`, hence `m≥sqrt(17)-4`. Undoing the normalization proves `M≤(4+sqrt(17))m`. A nonzero degenerate seminorm has `m=0` and contradicts this inequality; in dimension two it is rank one. The zero seminorm satisfies the quasiconformal inequality for every finite `Q`.

Status at independent reconstruction: no fatal logical gap found. The theorem uses the ordinary complete-target, essentially-separably-valued Reshetnyak Sobolev framework and its seminorm representation of KS energy. It has not used the prior audit, target isoperimetry, target topology, lower semicontinuity, or a stronger domain-minimization quantifier.
