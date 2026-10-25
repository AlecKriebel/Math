# Early independent mechanism audit

This note is fixed before consultation of package history, current sibling reviews, or external literature. The complete actual six-page reader and complete deposited TeX were read. All six rendered reader pages were visually inspected. The paper's own references and historical discussion were necessarily included in that reading, but no other report, historical authoring record or primary body has yet been consulted. This is an early provisional analytic assessment, not publication clearance.

## Exact target and success criterion

For every fixed finite-dimensional smooth Hausdorff second-countable boundaryless positive Riemannian statistical manifold (M,g,∇,∇*), including disconnected and noncompact M, find a proper embedding f into an open U⊂R^N, N=binom(2n+4,3) for n≥1, and one globally defined smooth Ψ on U with positive ordinary Hessian G. The pullback metric must be exactly g, and metric-orthogonal tangential projection of the ordered ambient pair (D,D*) must give exactly (∇,∇*). Both ambient connections must be torsion-free and flat everywhere on U. The open domain may depend on the data, may be nonconvex/incomplete, and the gradient map need only give local dual affine coordinates.

The separate necessity claim says that for an arbitrary positive Riemannian dual pair, both torsions must vanish if such a torsion-free ambient realization exists. Zero-dimensional and empty cases are separate. No claim about indefinite metrics, boundaries, fixed probability models, dimension optimality, historical firstness or worldwide current openness is included.

## Independent reconstruction

1. Let L be Levi-Civita and K=∇−L, K*=∇*−L. Torsion-freeness makes K and K* symmetric in their vector arguments. Duality gives T_ijk:=g(K_i j,k)=−T*_{ikj}. The two symmetries imply T_ijk=T_kji and then total symmetry. Thus K*=−K and C=∇g=−2T; the ordered connections are L−C♯/2 and L+C♯/2. The sign is fixed by differentiating g, not inferred from nomenclature.

2. The ordinary third-jet target is Q_ijk=∂_k g_ij+Γ_ijk=½(∂_i g_jk+∂_j g_ik+∂_k g_ij−C_ijk). It is symmetric but is not a tensor. Under x=x(y), differentiating the metric contributes the x_ac and x_bc terms and transforming Γ contributes x_ab. Therefore Q transforms as the third ordinary derivative of a scalar with first derivative zero and second derivative g. Omitting any one inhomogeneous term would be a defect; all three are present.

3. The germ in L-exponential coordinates, q_p(exp_p v)=½g_p(v,v)−C_p(v,v,v)/12, gives zero value/first jet, second jet g and third jet −C/2 in normal coordinates. For ordinary x coordinates, the inverse exponential germ has quadratic term +½L^a_ij(x−p)^i(x−p)^j. Its contribution to the third derivative is L^a_ij g_ak+L^a_ik g_aj+L^a_jk g_ai, exactly converting −C/2 to Q. Only a local germ near each zero tangent vector is needed. Smooth dependence near the zero section supplies a smooth jet section without completeness or a common injectivity radius.

4. Starting with a proper embedding e:M→R^(2n+1), include every polynomial feature of degree≤3, including the constant and every linear coordinate. The original e is recovered by a linear coordinate projection, so f is an embedding and proper. At each p, n linear combinations of ambient e-coordinates form local coordinates. Their degree≤3 polynomials span all scalar third jets, hence E_p:R^N→J³_p is surjective. This is finite-dimensional jet surjectivity at each point, not a global polynomial interpolation claim over M. The bundle rank is constant; positive bundle metrics give the smooth right inverse E†(EE†)⁻¹. No norm bound or finite atlas is required. Smoothness and invertibility are local properties.

5. With a=RJ and φ=−a, the pointwise identities are a·f=0, a·f_i=0, a·f_ij=g_ij, a·f_ijk=Q_ijk. In the jet evaluation a(p) is frozen. Differentiating along the base subsequently differentiates a. Hence f_i·∂_jφ=g_ij and f_ij·∂_kφ=Q_ijk−∂_k g_ij=Γ_ijk. Also φ·df=0 identically. These three equations explicitly produce the needed pair; no global pair-embedding theorem is being imported. Positivity of g forces dφ to be injective, but never forces global injectivity of φ.

6. Proper f has closed embedded image S. On an actual Euclidean normal tubular neighborhood with variable width, let z=r(z)+ν(z). Define Ψ₀(z)=φ_r(z)(ν(z)). The annihilation φ|TS=0 makes dΨ₀|S=φ as an ambient covector identity. Differentiating its ambient coordinate components gives Hess Ψ₀(f_i,·)=∂_iφ; there is no extra f_ij term in that derivative. Thus its tangent block is g. Along an affine normal fiber r is fixed, so the normal-normal Hessian block is zero. The mixed block B may be nonzero and unbounded.

7. Relative to the Euclidean tangent metric, A is a smooth positive endomorphism and B:NS→TS is smooth. The scalar t=tr(A⁻¹)||B||²_HS is smooth globally and pointwise finite, regardless of growth. With λ=1+t, the correction λ(r)|ν|² has zero first jet on S and Hessian 2λ P_N there. Schur completion gives

   H(v,w)=⟨A(v+A⁻¹Bw),v+A⁻¹Bw⟩+⟨(2λI−BᵀA⁻¹B)w,w⟩,

   BᵀA⁻¹B≤tI, so the second block is at least (2+t)I. It is positive pointwise, including B=0. Taking U to be the open positivity locus of this single already-defined smooth Ψ contains all of S. This avoids a uniform radius or eigenvalue bound and avoids an infinite patched potential. Derivatives of λ contribute nothing to the Hessian on S because the normal displacement vanishes to second order.

8. The correction preserves dΨ|S=φ, hence G f_k=∂_kφ and f*G=g. The standard connection induces the prescribed ∇ by G(f_ij,f_k)=f_ij·∂_kφ=Γ_ijk. Orthogonal projection of ambient duality then forces the other induced connection to be exactly the specified ∇*. This fixes their ordering.

9. In ambient standard coordinates D* has coefficients G^(CE)∂_A G_BE. Symmetry of Ψ's third derivatives gives zero torsion. The gradient functions η_E=∂_EΨ have invertible Jacobian G and satisfy their affine-coordinate PDE; they supply a local chart at each point, proving flatness. Their global injectivity is unnecessary. Properness into U follows because every compact subset of U is compact under inclusion into R^N.

10. Projection of either ambient torsion-free identity along an immersion gives zero torsion of its induced connection. The necessity corollary therefore uses no Hessian positivity argument beyond existence of the orthogonal projection. A second-countable 0-manifold is a countable discrete space and admits a proper enumeration into nonnegative integers with the quadratic potential on R. The empty case is vacuous.

## Boundary and obstruction checks

The problematic noncompact assertions are pointwise/local at the relevant stages: E_p onto, smooth inverse fiberwise, exponential germ near zero, variable tubular domain, smooth unbounded λ, and open Hessian positivity locus. No assertion is upgraded to a uniform statement. Nontrivial normal bundle and disconnected M cause no frame-choice problem because r,ν and the trace/HS expressions are intrinsic bundle objects. Rank changes cannot occur because f is an immersion of fixed dimension.

Compact closed S does not contradict Ψ|S=0 with positive Hessian: the ambient first derivative is a generally nonzero conormal, and second derivatives along S include the curvature term φ·f_ij=−g_ij. It would be wrong to infer that Ψ has vanishing tangent Hessian from its constant restriction. A positive Hessian on a nonconvex U also does not imply global convexity of U or injectivity of its gradient.

The n=1 test target is arbitrary positive g(t) and arbitrary C(t), with e(t)=(log t,0,0) on (0,∞). In y=log t coordinates, a centered cubic with coefficients h=g(t)t² and q=t³(3g′(t)−C(t))/2+3g(t)t² realizes the required pointwise jet. This supplies an independent exact-check family for the base/coefficient derivative distinction and connection sign; it is not used as proof for higher dimension. A nonlinear two-dimensional coordinate change will test the inhomogeneous Q law independently. General positive-block Schur completion is already a deductive proof, with finite samples serving only diagnostic purposes if used.

## Current status and exact remaining work

The literal analytic chain has no central gap identified after this independent reconstruction. This is provisional: the proper Whitney dimension/hypotheses and variable smooth Euclidean tube theorem still require exact primary-interface verification. The historical meaning of dually flat and the antecedent pair/contrast/extension statements require bounded direct primary inspection; an unavailable body must remain unavailable, not become a deductive import or an inferred absence of earlier work. The construction itself does not rely on Lauritzen's separate pair note, Matumoto's contrast theorem, or finite-simplex gluing.

A route that merely assumes an arbitrary global Lauritzen pair or an unrestricted noncompact finite-simplex embedding would transfer the central difficulty into an unsupported external theorem; it is not used to validate this manuscript. The actual finite-feature/jet construction above supplies the required mechanism directly.

Completion estimate: **40% of the bounded independent analytic audit**, with main algebra/geometric mechanism independently reconstructed and primary-interface, adversarial limiting checks, reproducible diagnostics and final custody/report still pending. This percentage measures work, not a probability of truth.
