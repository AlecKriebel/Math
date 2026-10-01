# Turn 3: the entire circle-odd sector is a weighted Hodge operator

Original target remains unresolved at three substantive turns. This turn closes the coupled exact-form gap left inside the circle-odd sector in Turn 2. It does not claim full regularity, full normal stability, a global fiber classification or a connected-sum law.

## 1. Precise result

Let a member of the known S¹×R³ family be written, in the Bamler–Chen normalization, as

g=a²dθ²+g_B,    g_B=dr²+b²g_S²,    f=f(r),

where Ric_g+Hess_g f+λg=0 with λ=1/2. The smooth quotient B is R³; a(0)>0 and b(r)=r+O(r³). The functions a,b grow linearly at infinity with finite positive slopes, and the metric/potential have the bounded-curvature and proper-potential properties used in Turn 2.

Set K=∂θ and F=f−3log a. For a base one-form α on B, define

Uα=K^flat⊙α=a²dθ⊙α,

where ⊙ is the sum of the two tensor products, without a factor1/2. This identifies base one-forms with the circle-invariant symmetric two-tensors odd under θ↦−θ. Then

||Uα||²_(L²(e^(−f)dvol_g))=2∫ a³|α|²e^(−f) dθ dvol_B,

and the exact quadratic-form identity is

Q(Uα)=2∫ (|dα|²+|δ_Fα|²) a³e^(−f) dθ dvol_B.                 (1)

Here δ_F=δ+ι_(∇F) is the adjoint of d for the measure e^(−F)dvol_B=a³e^(−f)dvol_B. Formula (1) first holds for smooth compactly supported forms and then for the closed form domains. Thus the circle-odd restriction of −L is, after the constant normalization of U, unitarily equivalent to the weighted Hodge Laplacian dδ_F+δ_Fd on one-forms of B.

For this one-ended smooth quotient, that operator has no weighted-L² harmonic one-form. Consequently the **entire circle-invariant, circle-odd sector has neither negative spectrum nor kernel**. This includes the radial/exact-sphere coupled sector that was not eliminated in Turn 2.

## 2. Derivation of the quadratic identity

Write A=a′/a, B₁=b′/b and C=a″/a. To avoid confusing B₁ with the quotient B, use the subscript here. In Turn 2's orthonormal frame, any odd tensor has h_(01)=v, h_(1α)=w_α, with both symmetric entries included. Let η=vdr+w be the corresponding base one-form, so h=(a dθ)⊙η. The connection and curvature calculation there can be collected invariantly as

Q(h)/2=∫ a e^(−f) [ |∇^Bη|²+(4A²−2C)v²+(A²−2AB₁)|w|² ] dθ dvol_B.       (2)

Indeed |∇^Bη|² includes the radial derivatives, the terms |b⁻¹dv−B₁w|² and |b⁻¹∇^S w+B₁v g_S²|². The remaining circle-connection terms and curvature contraction are exactly those displayed in Turn 2. Thus (2) retains all coupling of the exact sphere component and the radial component.

Now put η=aα. Its derivative norm expands as

|∇^B(aα)|²=a²[|∇^Bα|²+2A〈∇_rα,α〉+A²|α|²].

In the measure μ=a³e^(−f)dvol_B, radial integration by parts turns the middle term into

∫ μ A∂_r|α|²=−∫ μ [A′+(3A+2B₁−f′)A]|α|².

For compact support there are no endpoint terms. Combining it with (2), the resulting radial and sphere coefficients are respectively

3A²−3C−2AB₁+Af′,
−C−4AB₁+Af′.                                           (3)

The circle component of the soliton equation is

−C−2AB₁+Af′+λ=0.

Hence (3) becomes

3A²−2C−λ,          −2AB₁−λ.                            (4)

These are precisely the radial and sphere components of Ric_B+Hess_B F. One can verify this without coordinates. The warped-product Ricci equation on the base gives

Ric_B+Hess_B f=a⁻¹Hess_B a−λg_B.

Subtracting3Hess_B(log a) yields

Ric_B+Hess_B F=−2a⁻¹Hess_B a+3 d(log a)⊗d(log a)−λg_B,

whose components are (4). It follows that

Q(Uα)/2=∫ [|∇^Bα|²+(Ric_B+Hess_B F)(α,α)] e^(−F)dθ dvol_B.

The weighted Weitzenböck identity for one-forms identifies this with the right side of (1). To check the sign convention, δ_F=e^F δ e^(−F)=δ+ι_(∇F), and dδ_F+δ_Fd is the ordinary Hodge Laplacian plus Lie differentiation by ∇F. The one-form Weitzenböck curvature term is therefore Ric_B+Hess_B F. This proves (1). The proof uses the actual soliton equations; it is not a statement for an arbitrary warped product and arbitrary weight.

## 3. Closed domains and the reducing subspace

Circle rotations and circle reflection are isometries preserving f. Their averaging/eigenspace projections commute with L, and the circle-invariant odd subspace is reducing. All of its tensors have the form Uα, including the coupled radial component. This does not assume that an arbitrary soliton over a symmetric cone is itself symmetric; it is an operator calculation at the known symmetric metrics.

Writing C_θ=∫dθ (equal to2π for the standard circle), the map U/√(2C_θ) is an isometry from the base weighted L² space onto this tensor subspace. The tensor form Q plus a sufficiently large multiple of the L² norm is equivalent to the weighted H¹ norm, since the curvature is bounded. Bamler–Chen Proposition5.38 and Corollary5.40 use this closed form. Smooth compactly supported tensors form a core; circle averaging and reflection preserve that property.

For the origin one may first cut away r<ε. A smooth tensor is bounded there, the volume is O(r²)dr and a,f are smooth and bounded. The derivative error of a cutoff supported on an ε-annulus is O(ε⁻²·ε³)=O(ε). Radial cutoffs commute with U and with circle symmetry. At infinity the weighted H¹ and L² tail estimates give convergence, as in Turn 2. There is no assumed polynomial decay compensating an exponentially growing weight.

The identity therefore extends by closure. More explicitly, if compactly supported α_j correspond to tensors converging in the closed form norm, (1) applied to α_j−α_k shows that dα_j and δ_Fα_j are Cauchy in their weighted L² spaces. Their limits are the distributional derivatives of α. Conversely the closure of the first-order Hodge form corresponds under U to the tensor closed form. This reasoning avoids silently assuming that the unbounded coefficient ∇F makes δ_F bounded on an ordinary H¹ space.

In particular, a tensor zero eigenvector corresponds to a smooth weighted-L² form α satisfying dα=0 and δ_Fα=0. A negative eigenvector is impossible by (1).

## 4. No weighted-L² harmonic one-form on the quotient

We prove the kernel assertion directly; no weighted cohomology identification is assumed.

Because B is diffeomorphic to R³ and simply connected, dα=0 implies α=dψ for a globally smooth function ψ. The coclosed equation is

Δ_Bψ−〈∇F,∇ψ〉=0.

The weighted-L² assumption is exactly finite Dirichlet energy

∫_0^∞ p(r)∫_S² [ |∂_rψ|²+b⁻²|∇^Sψ|² ] dvol_S² dr <∞,

where p(r)=a(r)³b(r)²e^(−f(r)). The circle factor is constant and omitted. Expand ψ in real spherical harmonics. For a harmonic of degree l with eigenvalue Λ=l(l+1), its radial coefficient u satisfies

(pu′)′−Λ p b⁻²u=0.                                    (5)

Projection and the energy estimates are justified by smoothness on each compact annulus and orthogonality; the energy contributions are nonnegative, so their integrability follows individually.

For l≥1, smoothness at the origin gives u=O(r^l), u′=O(r^(l−1)), while p(r) is asymptotic to a positive constant times r². Thus the origin integration-by-parts term puu′ tends to0. Take a radial cutoff χ_R equal to1 up to R, vanishing after2R, with |χ_R′|≤C/R. Testing (5) against χ_R²u gives

∫ χ_R²p[u′²+Λb⁻²u²]=−2∫ χ_Rχ_R′puu′.

Young's inequality absorbs half of the u′² term and bounds the rest by2∫(χ_R′)²pu². Since b(r)/r tends to a finite positive number, on the annulus [R,2R] this error is bounded by a constant times the tail ∫_R^(2R)pb⁻²u², which tends to0 by the finite angular energy. Letting R→∞ forces u′=0 and u=0. This includes all nonconstant spherical harmonics.

For l=0, (5) says pu′ is constant. Near the origin p=O(r²), whereas u′ is bounded for a smooth radial coefficient. The constant is therefore zero and u is constant. Its derivative contributes nothing to α.

All coefficients of dψ vanish. Therefore α=0. This proves that the weighted Hodge kernel is trivial. The one-ended smooth R³ topology is used essentially; one cannot substitute a two-ended weighted interval, where finite-energy harmonic gradients may exist.

## 5. Consequences and exact remaining gap

Combining the two circle statements gives a sharper parity reduction:

index_full(−L) ≡ index_(circle-invariant, reflection-even)(−L) (mod2).

The reflection-odd invariant sector contributes neither index nor nullity. Nonzero Fourier weights still have even real index multiplicities; possible zero eigenvalues in those weights have not been excluded.

The remaining circle-even subspace contains the base symmetric two-tensors and the circle-circle component, including nonspherical SO(3) modes and their couplings. Its normal negative multiplicity and kernel have not been controlled. A calculation of the cohomogeneity-one degree alone still cannot determine this remaining index or guarantee that all solutions over a symmetric cone are covered by the known family. No unrestricted degree value is concluded.

No boundary-connected-sum gluing or compactness theorem is established. Original status is unresolved at3/5, with two substantive turns remaining if a full resolution is not reached earlier. The partial Hodge factorization is not claimed novel, and must receive independent review before a partial-result PR.

## Verification scope

The existing pinned Bamler–Chen spectral theorem and Rajan warped-product equations suffice as inputs. The checker verifies the rescaling/integration coefficients and their soliton reduction to the weighted Ricci tensor, alongside exact cutoff-exponent and representation arithmetic. The closed-domain and infinite harmonic-mode argument is the written proof, not a finite computational assertion.
