# Early independent mechanism audit of 23131374

This reconstruction is fixed after complete reading of the actual six-page PDF and sole deposited TeX, including all six rendered reader pages, and before external primary-body reading, package history, sibling review reports or source-lane conclusions. The manuscript's own disclosure, historical narrative and references were naturally part of its reading. They are not independent evidence for historical claims. No deposited program was executed. This is a provisional analytic review, not publication or priority clearance.

## Exact claim and falsifiable target

For each fixed finite integer r≥0 and each of the plane and sphere, construct smooth complete strictly positive Gaussian-curvature metrics g_n→g_* in ordinary compact-open C^r, while their unique orientation-preserving point-normalized conformal coordinate factors fail to converge to the factor of g_* in C^(r+1). The plane factors fix 0,1; the sphere factors fix 0,1,∞. All objects are smooth; the displayed finite regularities describe topologies on those objects. The goal is failure of inverse continuity for this particular normalized parametrization, not a statement about abstract homeomorphisms or about continuity at every metric. Each r may use its own sequence. Noninteger Hölder and C∞ topologies, RP², priority and globally uniform positive plane curvature are not targets.

The proof can establish its counterexample without depending on continuous dependence of general Beltrami solutions. It constructs each coordinate factor and target conformal metric exactly, proves the target complete and nonnegatively curved (indeed positive), and uses uniqueness of normalized conformal automorphisms to identify the actual inverse factor. External sources still need checking for the exact historical parametrization/topology question.

## Background, completeness and normalization

Set b=c log(1+|z|²)+constant, with c=1/2 for the plane and c=1 for the unit sphere (constant −log2). Then Δb=4c/(1+|z|²)²>0. The plane metric is |dz|²/(1+|z|²), with K=2/(1+|z|²)>0. Its escaping-curve length dominates total variation of arsinh|z|, giving completeness. The spherical expression is exactly the smooth unit round metric.

All changes have support in |z|≤R=1/4 and are flat at the support boundary. Every fixed smooth positive changed metric is uniformly comparable to the background on this compact disk and identical outside. Thus it is complete; no uniform comparison constant across n is necessary. On the sphere the changed chart tensor is unchanged near infinity and extends smoothly. If a global onto coordinate map f pulls back a conformal target to that metric, the target is complete by isometry.

If f and ψ are two normalized orientation-preserving coordinate factors, ψ∘f⁻¹ is a conformal automorphism of the standard plane or sphere: conformal rescalings do not change its complex structure. An affine plane automorphism fixing 0,1 is the identity; a spherical Möbius map fixing 0,1,∞ is the identity. Therefore f=ψ and the conformal factors coincide. No derivative normalization at 0 is present. For g_* the normalized coordinate factor is id.

## r=0: slow twist

Take θ_n(t)=θ₀ η(log(R/t)/n), with smooth η constant zero for arguments≤0 and one for arguments≥1, and θ₀ not a multiple of 2π. The map φ_n(z)=exp(iθ_n(|z|))z is a constant rotation on t≤Re^(−n), the identity on t≥R and smooth everywhere. Radius is preserved, and subtracting the same angle gives a global smooth inverse. Its polar-coordinate Jacobian has positive determinant; it fixes all required points.

In orthonormal radial/angular frames, removing the target rotation leaves the shear J=[[1,0],[q_n,1]], q_n=tθ′_n(t). Hence JᵀJ=[[1+q_n²,q_n],[q_n,1]], while ||q_n||∞≤|θ₀| ||η′||∞/n. Radial invariance of b makes this the background-relative tensor of φ_n*g_*. Rotation changes its basis but not its operator-norm distance from I. Therefore metric coefficients converge uniformly to g_*; continuity at 0 is included because the map is exactly a rotation there. Curvature and completeness are inherited by isometry. The normalized factors are exactly φ_n, but Dφ_n(0)=Rot(θ₀) for every n. Thus C¹ convergence to id fails even on a fixed compact neighborhood of 0.

## All r≥1: the anti-holomorphic derivative removes the logarithm

For fixed r set m=r+1, ρ=e^(−n), ε=1/n, S=|z|²+ρ², s=√S, L=(log S)/2 and f=z+εχ z^m L. The smooth radial χ equals one on |z|≤R/2 and zero for |z|≥R. For each n every formula is smooth at 0; smoothness is not being asserted for a singular limiting logarithm.

For any ordered j-th real derivative of L, D^jL=P_j/S^j, with P_j homogeneous of degree j in (x,y,ρ). The recurrence P_(j+1)=S∂iP_j−2j x_iP_j follows exactly. Its coefficient ℓ¹ norm is at most 5j times that of P_j: differentiating a degree-j polynomial contributes at most j, multiplication by the three monomials of S contributes at most 3j, and the remaining term at most 2j. Consequently |D^jL|≤5^(j−1)(j−1)! s^(−j). This is an induction for every finite derivative order, not an assertion inferred from finite examples.

Leibniz gives |D^k(z^mL)|≤C_(r,k) s^(m−k)(1+|log s|) for k≤m. For k=1 the exponent r≥1 absorbs the logarithm uniformly, yielding ||Df−I||∞=O(ε). Up to k=m the only exponent-zero logarithm is multiplied by ε, and ε|log s|≤εn=1 since s≥ρ and s<1 on the perturbation disk. Thus f_z is bounded in C^r; it is not required to approach 1 in that norm. The stronger lower-order convergence f_z→1 in C^(r−1) also follows.

On the inner disk ∂bar L=z/(2S) and the polynomial z^m is holomorphic, so

    f_bar = ε z^(r+2)/(2S).

Its k-th real derivative has a homogeneous numerator of degree r+2+k over S^(k+1), hence size C_(r,k)s^(r−k). This is uniformly bounded for every k≤r. All cutoff derivative terms are on the fixed annulus, where s≥R/2; there their derivatives of every fixed order are O(ε). Therefore ||f_bar||C^r=O(ε). The uniform closeness of Df to I gives |f_z|≥1/2. Repeated reciprocal differentiation, using the uniform C^r bound of f_z, gives ||1/f_z||C^r≤C_r. Thus μ=f_bar/f_z→0 in C^r. This cancellation is the central endpoint mechanism: the tensor distortion is small at the requested order although the conformal part of Df has a persistent top-order derivative.

For each n, near 0, L=logρ+O(|z|²). Since εlogρ=−1, the degree-m term of f−id is −z^m, exactly. In particular ∂x^m(f−id)(0)=−m! for every n. This blocks C^(r+1) convergence to id.

The small global ||D(f−id)||∞<1 gives injectivity and the lower Lipschitz bound. For every target y, z↦y−(f(z)−z) is a strict contraction on the complete plane, giving surjectivity. The Jacobian is everywhere nonsingular and has the positive sign of I, so the inverse is smooth and orientation-preserving. As f is identity outside the disk, injectivity forces the disk to map onto itself. It fixes 0,1 and extends as the identity near spherical infinity.

## Exact metric reconstruction and r≥2

Let h=log|f_z|, take a real supported correction a, and set

    g_n=e^(−2(b+a)) |dz+μ dbar z|²,
    U=(b+a+h)∘f⁻¹.

Since df=f_z(dz+μdbar z), direct cancellation gives g_n=f*(e^(−2U)|dw|²). The distortion tensor has eigenvalues (1±|μ|)², so g_n is positive for large n. The plane factor is u=U, while the sphere factor is u=U−b(w), which vanishes outside the support and hence extends smoothly over infinity. Completeness follows as above. Once K(g_n)>0 is proved, the conformal target also has positive curvature, giving the required admissible factor.

For r≥2 choose a=0. Since μ→0 in C^r, metric coefficients converge in C^r on the fixed disk and are identical outside it. In particular they converge in C². The ordinary coordinate curvature formula is continuous on positive tensors in C²; the background has a positive curvature minimum on that fixed disk. Hence all sufficiently large n have positive curvature there, and outside the curvature is unchanged. The bad degree-r+1 jet already proves failure for the normalized factor. This argument cannot be used for r=1.

## r=1: independent full nonlinear curvature reconstruction

Write ℓ=1+|log s|. For m=2, the previous bounds give |Df−I|≤Cε and |D²f|≤Cεℓ. In D³(z²L), the possible undifferentiated-log term is absent because D³(z²)=0; every remaining Leibniz term has total scale s^(−1). Thus |D³f|≤Cε/s. From h=log|f_z| and |f_z|≥1/2,

    |Dh|≤Cεℓ,    |D²h|≤C(ε/s+ε²ℓ²)≤C′ε/s.

Indeed sℓ≤1 and sℓ²≤4/e for 0<s≤1. These are continuous elementary suprema, not sampled bounds. The Hessian of a logarithm is controlled without choosing a global complex logarithm, because log|f_z| is a smooth real function.

Derive the exact pullback-Laplacian independently: put J_ai=∂i f_a, H=J⁻¹. For x=f⁻¹(w), ∂w_a x_i=H_ia. A second derivative of f(x(w))=w gives ∂²_(w_aw_b)x_i=−H_ic f_c,jk H_ja H_kb. Taking the trace yields

    L_n v := (Δ_w(v∘f⁻¹))∘f
           = A_ij v_ij + B_i v_i,
    A=HHᵀ,       B_i=−H_ia f_a,jk A_jk.

The order HHᵀ is required by the indices; HᵀH is generally different. The drift term is part of the exact operator and cannot be discarded. We have A−I=O(ε), A≥I/2 eventually, and |B|≤Cεℓ. Although εℓ can be order one near the shrinking core, the argument below does not require B to converge uniformly to zero.

Since the fixed b has bounded first and second derivatives, L_nb−Δb is bounded by Cε(1+ℓ). The Hessian term in L_nh is bounded by Cε/s and its drift by Cε²ℓ². The elementary sℓ and sℓ² bounds therefore give

    L_n(b+h) ≥ Δb−C₀ε/s

with C₀ independent of n (and a maximum may be chosen for the two backgrounds).

The regularized radius has Ds=x/s and D²s=I/s−xxᵀ/s³, with radial eigenvalue ρ²/s³ and tangential eigenvalue 1/s. It is positive semidefinite and Δs=(|x|²+2ρ²)/s³≥1/s. Therefore

    L_ns ≥ (1/2)Δs−Cεℓ ≥ 1/(2s)−Cεℓ ≥ 1/(4s)

for all sufficiently large n, uniformly on the inner disk; the last step uses Cεsℓ≤1/4. Set the single n-independent K>4C₀ and a=Kεχs. Then a is smooth for every n and ||a||C¹=O_K(ε); its Hessian is deliberately allowed to grow. Where χ=1,

    L_n(b+h+a) ≥ Δb+(K/4−C₀)ε/s>0.

On the fixed closed cutoff annulus, s is bounded below independently of n. All needed fixed-order perturbation derivatives are O_K(ε), including f through order three, h through order two, and a through order two. Thus the full exact operator tends uniformly to Δb there. The positive minimum of Δb on this compact annulus gives positivity for large n after K has already been fixed. Smooth support transitions are included. Outside the support the operator equals Δb. These three regions cover the chart; the spherical infinity region is unchanged round geometry.

Finally the conformal curvature sign is correct: for target e^(−2U)|dw|², K=e^(2U)Δ_wU. By the exact isometry,

    K(g_n)=e^(2U∘f) L_n(b+h+a)>0.

Meanwhile μ→0 and a→0 in C¹, so g_n→g_* in C¹. The exact second jet of f−id is −2. This handles the critical endpoint with full inverse-coordinate drift, anisotropy, cutoff and curvature; neither C¹ curvature continuity nor a numerical K is needed.

## Early verdict and remaining work

No central analytic defect has been found after this reconstruction. The three endpoint regimes are materially different and each is supplied. Global diffeomorphism, point normalization, exact reconstruction, spherical extension, completeness and positive curvature have explicit mechanisms. The bad map derivative is at a fixed point and therefore witnesses failure in the stated compact-open topology.

Still required before a final review: independent diagnostic controls for the derivative recurrence/inverse operator/curvature sign, direct primary verification of the published topology/derivative-shift/normalization and workshop statement, bounded classical endpoint-source reading (including the newly available raw primary body only after this seal), honest unavailable-body/priority limits, final source custody, report and final seal. Finite tests will only corroborate the universal derivations. No current sibling report has been read and no scientific conclusion from the source lane has been requested.

Completion estimate: **45% of the bounded independent analytic assignment**, measuring completed review work rather than a probability of correctness. No publication or historical-priority clearance.
