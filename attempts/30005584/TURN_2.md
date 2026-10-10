# Turn 2: an actual normal-index reduction and a positive mixed sector

Original target remains unresolved at two substantive turns. This turn studies the actual weighted Einstein operator on the known rotational Ricci expanders, rather than inferring a degree from the finite-dimensional countermodel. It establishes a circle-weight parity reduction and excludes an entire nonsymmetric tensor sector from both the negative spectrum and kernel.

## 1. Operator and spectral category

Work on a smooth complete member of Rajan's S¹×R³ family, after the normalization adjustment in Turn 1:

g=dr²+a(r)²dθ²+b(r)²g_S²,  f=f(r),

with a>0, b>0 for r>0, a(0)>0 and b(r)=r+O(r³) at the singular orbit S¹×{0}. These metrics have bounded curvature, quadratic curvature decay and a potential bounded above and proper. Thus the hypotheses of Bamler–Chen Proposition 5.38 apply to

L=Δ−∇_(∇f)+2Rm,

acting on symmetric two-tensors in L²(e^(−f)dvol_g). In particular −L is self-adjoint, has discrete spectrum with finite-dimensional eigenspaces, and finitely many negative eigenvalues. Its index is the sum of their real multiplicities (Definition 5.39). The associated quadratic form is

Q(h)=∫ (|∇h|²−2〈Rm(h),h〉) e^(−f)dvol_g.

The inverse-Gaussian weight grows at infinity; ordinary unweighted integration by parts is not substituted. Proposition 5.38(a) supplies this identity for eigenvectors, which lie in the weighted H¹ space. All subsequent spectral assertions concern this operator and this domain.

## 2. Circle symmetry removes nonzero Fourier weights from index parity

Rotations of the circle preserve g and f, hence act orthogonally on the weighted space and commute with L. Every negative eigenspace is a finite-dimensional real representation of SO(2). Its nontrivial irreducible summands are two-dimensional rotations (equivalently conjugate nonzero complex Fourier weights). Consequently

index_full(−L) ≡ index_SO(2)-fixed(−L)  (mod 2).

The analogous congruence holds for nullity, but it does **not** prove the absence of any nonzero-weight kernel. Full regularity is still needed when invoking the degree's regular-value formula.

Proof: average over the compact circle to project orthogonally onto the invariant vectors. After complexification, diagonalize the commuting circle action. Complex conjugation pairs weights k and −k, k≠0, with equal dimensions; their real contribution is even. Sum over the finitely many negative eigenvalues. The same finite-dimensional argument applies to the zero eigenspace. No assertion about the sign or size of individual nonzero Fourier eigenvalues is required.

This is an exact reduction for the actual normal index. It does not yet identify it with the full SO(3)×SO(2)-fixed index, since nontrivial SO(3) representations can have odd real dimension.

## 3. Circle-odd tensors and the local calculation

Put A=a′/a, B=b′/b and C=a″/a. Choose the radial-parallel orthonormal frame E₀=∂r, E₁=a⁻¹∂θ, E₂,E₃=b⁻¹ times a unit sphere frame. At a point where the unit sphere frame is geodesic, the relevant connection coefficients are

∇₁E₀=A E₁,   ∇₁E₁=−A E₀,
∇_αE₀=B E_α,   ∇_αE_β=−B δ_(αβ) E₀

for α,β∈{2,3}, with the intrinsic sphere connection understood. The mixed sectional curvature is K_(1α)=−AB, and K_(01)=−C. The convention is Rm(g)=Ric, so Rm acts on an off-diagonal tensor in an i,j plane by −K_(ij).

A circle-invariant tensor that is odd under the isometric reflection θ↦−θ has only components

h_(01)=h_(10)=v(r,x),
h_(1α)=h_(α1)=w_α(r,x),

where x∈S² and w is a sphere one-form represented in its unit orthonormal frame. All other components vanish. The symmetric-product convention here includes both off-diagonal entries, so |h|²=2(v²+|w|²).

Write d and ∇^S for the unit sphere derivative. Direct substitution into the connection formula gives the pointwise identity

|∇h|² = 2(v_r²+|w_r|²)+8A²v²+2A²|w|²
          +2|b⁻¹dv−Bw|²+2|b⁻¹∇^S w+Bv g_S²|².

The curvature term is

−2〈Rm(h),h〉 = −4C v²−4AB|w|².

These formulas are checked by the supplied independent-coordinate symbolic certificate. Their derivation retains the covariant connection terms; replacing them with ordinary component derivatives would miss the essential square below.

After integrating over the unit sphere, the only cross term between v and w is

(8B/b)∫ v div_S w,

since integration by parts gives ∫〈dv,w〉=−∫v div_S w. In particular, this cross term vanishes for a coclosed one-form w.

## 4. The coexact circle–sphere sector is a reducing positive sector

Let H_coex be the circle-invariant, circle-reflection-odd sector with v=0 and w(r,·) coclosed on S² for each r. On the two-sphere coclosed one-forms are coexact, since H¹(S²)=0. For a separated vector spherical harmonic this is the sector h_(1α)=u(r)ω_α(x), δ_Sω=0; the statement also holds for arbitrary radial combinations.

For such a tensor the preceding identity reduces exactly to

Q(h)=2∫ a b² e^(−f) [ |w_r|²+(A−B)²|w|²+b⁻²|∇^S w|² ] dr dθ dvol_S².       (1)

Every term is nonnegative. No sign assumption on the sectional or Ricci curvature and no positivity estimate on a″ or b″ is involved.

**Reducing property.** First, circle invariance and circle reflection are commuting isometries preserving f, so L preserves the circle-invariant odd sector. That sector consists exactly of the v,w tensors above. Split w into exact and coexact pieces on S². The form has no cross term between v and a coexact w, by the integrated identity. It also has no cross term between exact and coexact sphere forms in any of the other summands: the L² and radial derivative pairings are orthogonal, and the angular rough Laplacian preserves the Hodge splitting because on the unit S² it differs from the Hodge Laplacian by the scalar Ricci term. Thus the form is block diagonal for H_coex and its complement. This proves that its closed realization is a reducing subspace of the self-adjoint operator. This argument is stronger than positivity merely on a family of trial tensors.

**Origin and infinity.** Formula (1) is first proved for smooth tensors with compact radial support away from the singular orbit. It extends to smooth weighted-H¹ eigenvectors in this sector. At infinity take radial cutoffs with derivative bounded by O(1/R); the weighted H¹ and L² tails control all integration errors. At r=0 a smooth tensor is bounded, while dvol is O(r²)dr times the circle measure. A cutoff changing on r∈[ε,2ε] with derivative O(1/ε) has tensor error energy O(ε), tending to zero. Hence no unproved boundary term at the collapsed two-sphere is discarded. The curvature is bounded, so its quadratic contribution is continuous in this approximation. Radial cutoffs preserve coclosedness and circle parity.

**Spectral conclusion.** There is no negative eigenvalue in H_coex, by (1). There is no zero eigenvector either: equality would require ∇^S w=0 almost everywhere on each sphere. The unit two-sphere has no nonzero parallel one-form, as follows for example from its nonzero constant curvature acting on a parallel form. Therefore w=0 and h=0. By elliptic regularity this excludes any nonzero smooth weighted-L² kernel vector in this sector.

For a coclosed vector harmonic of angular degree l≥1, the unit-sphere rough eigenvalue is l(l+1)−1, so (1) has the scalar potential

(A−B)²+[l(l+1)−1]/b².

This last standard spherical-harmonic formula is not needed for the positivity proof. It shows explicitly that the entire tower, including the three-dimensional l=1 representation, is excluded. Those odd-dimensional representations would otherwise be possible contributors to the normal index parity.

## 5. What remains after this genuine reduction

The result removes all nonzero circle weights from index parity, and removes the coexact circle–sphere mixed sector from both index and kernel on the known symmetric metrics. It does not remove:

- circle-invariant tensors even under circle reflection, including radial, sphere-trace, trace-free sphere and coupled mixed modes;
- the circle-odd sector coupling h_(01) to exact sphere one-forms;
- possible nonzero-circle-weight kernel vectors relevant to full regularity;
- the global problem that all solutions over a chosen cone need to be accounted for, with any required symmetry lifts identified.

The remaining odd-dimensional SO(3) modes cannot be discarded by representation theory alone. Neither (1) nor its reducing property asserts that the entire full Einstein operator is nonnegative, or that its kernel vanishes. It therefore does not yet yield an unrestricted signed count, parity, or an integer value for deg_exp(S¹×D³).

No boundary-connected-sum law is established. The next substantive route must address one of these remaining operator/global gaps or the neck-gluing problem. Original status remains unresolved at 2/5; this is not a final unsolved publication.

## Source and verification scope

The exact spectral setup is Bamler–Chen arXiv:2305.03154v3, Proposition 5.38, Definition 5.39 and Corollary 5.40, pp.50–51. The metric and curvature conventions are the already pinned Rajan published paper, its soliton setup and Appendix A. No new source PDF was added. The certificate verifies finite representation multiplicity arithmetic and the exact tensor contraction identity. It does not prove an infinite-dimensional spectral theorem or the original Ricci degree.
