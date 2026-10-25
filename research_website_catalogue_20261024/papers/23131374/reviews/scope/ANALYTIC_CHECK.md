# Independent analytic check of Zenodo 23131374

The full actual six-page PDF, all six raw page renders and the complete TeX were read before the initial independent seal at 2026-10-25T06:37:04.564908Z. This note expands that reconstruction after primary-source checks. No historical internal review body or current sibling opinion was used. The later external antecedent changes the priority assessment, not the independently reconstructed proof below.

## Exact statement and category

For each fixed finite integer r >= 0 and each surface C or S², the paper gives its own sequence of smooth complete metrics of strictly positive Gaussian curvature converging to a smooth complete positive-curvature background in ordinary compact-open C^r. Their unique normalized uniformizing diffeomorphisms do not converge in ordinary compact-open C^(r+1). The maps preserve orientation and fix 0,1 on C, and 0,1,infinity on S². There is no derivative normalization at zero. The function space O consists of smooth real u such that e^(-2u)g_kappa is complete with K >= 0. The parameter map is (u,phi) -> phi*(e^(-2u)g_kappa); its domain topologies are C^r on u and C^(r+1) on phi.

These are topologies on smooth objects, not spaces of merely finite regularity. Noninteger Hölder, little Hölder, Zygmund and smooth C-infinity topologies are not interchangeable with ordinary integer C^r. The theorem does not assert failure at every metric, one sequence for all r, a result for RP², failure of every abstract homeomorphism, or a prescribed uniform positive lower curvature bound on C. The abstract's phrase about every finite endpoint concerns the integer values, as the theorem makes explicit.

## Background, completeness and identification of the inverse factor

The planar b = (1/2)log(1+|z|²) gives g* = (1+|z|²)^(-1)|dz|² with K = 2/(1+|z|²) > 0. For an escaping curve, length dominates total variation of arsinh|z|; hence the metric is complete. The spherical b = log(1+|z|²)-log 2 gives the unit round metric. All perturbations equal g* outside the disk of radius R=1/4. A positive smooth metric equal to a complete metric outside a compact set is globally comparable to it, for each fixed metric, and is complete. A common comparison constant over n is not needed.

If f and psi are two orientation-preserving coordinate factors for one metric, psi composed with inverse f is a standard conformal automorphism. A planar automorphism is affine; fixing 0 and 1 forces identity. A spherical automorphism is Möbius; fixing three distinct points forces identity. Thus each constructed coordinate map is the actual normalized inverse factor. This argument does not assume continuous dependence of Beltrami solutions, which would be circular here. The published parametrization context is available in Banakh–Belegradek Sections 8–9; surjectivity of that general parametrization is not needed to build these explicit inverse discontinuity examples.

## Zero endpoint

The radial angle theta_n(t)=theta_0 eta(log(R/t)/n), with eta constant outside its transition interval and theta_0 not a multiple of 2 pi, gives phi_n(z)=exp(i theta_n(|z|))z. It is a fixed rotation near zero and identity outside R, so it is smooth across zero and the support boundary. Subtracting the angle gives its global inverse. Its polar derivative after rotation is a shear with q=t theta_n'(t)=O(1/n). Since the background is radial, the pullback tensor relative to it is the matrix [[1+q²,q],[q,1]], tending uniformly to identity. At zero the tensor is exactly unchanged, yet Dphi_n(0) is the same nontrivial rotation for every n. Completeness and curvature are preserved by isometry. The point normalization is satisfied because 1 and spherical infinity lie outside the support.

## Every positive finite endpoint: analytic bounds

Fix r >= 1, rho=exp(-n), epsilon=1/n, s=sqrt(|z|²+rho²), L=log s and f=z+epsilon chi z^(r+1)L. All constants may depend on this fixed r, the fixed cutoff and background, but not n; finitely many initial n may be discarded.

For any ordered real derivative of order j>=1, D^j L=P_j/s^(2j). Starting with P_1=x or y, differentiating replaces P_j by s² partial_i P_j - 2j x_i P_j. This is homogeneous of degree j+1 in x,y,rho. The coefficient l1 norm grows by at most 5j: multiplication by the three terms of s² costs at most 3j and the second term at most 2j. Since each coordinate is bounded by s, |D^jL| <= 5^(j-1)(j-1)! s^(-j), for every finite j. This is an induction, not an inference from the finite checker.

Leibniz gives |D^k(z^(r+1)L)| <= C s^(r+1-k)(1+|log s|) for k<=r+1. For every positive exponent p, s^p(1+|log s|) is bounded on the fixed disk. When the exponent is zero, epsilon(1+|log s|) is uniformly bounded because s>=rho and epsilon|log rho|=1. Consequently Df-I=O(epsilon), f_z is bounded in C^r, and f_z -> 1 in C^(r-1). Boundedness of f_z in C^r is not convergence in that norm.

On the inner disk f_barz = epsilon z^(r+2)/(2s²). After k real differentiations its numerator has degree r+2+k and denominator s^(2k+2), giving |D^k f_barz| <= C epsilon s^(r-k), hence the C^r norm is O(epsilon). On the cutoff annulus s>=R/2 and all fixed derivatives are O(epsilon). Since |f_z|>=1/2 for n large, derivatives of its reciprocal through order r stay bounded, so mu=f_barz/f_z tends to zero in C^r. The logarithm at zero gives the exact obstruction partial_x^(r+1)(f-id)(0)=-(r+1)! for all n. No possible cancellation from the higher |z|² terms changes this jet.

For f=id+w with ||Dw||<1, the lower Lipschitz bound proves injectivity, and for every target y the map z -> y-w(z) is a contraction of the complete plane, proving onto. Near-identity differentials have positive Jacobian, and the inverse function theorem gives a smooth orientation-preserving global inverse. Identity outside the disk plus injectivity implies the disk maps to itself; f fixes 0,1 and is identity near spherical infinity.

## Exact metric and higher orders

Set h=log|f_z| and g_n=e^(-2(b+a))|dz+mu dbarz|², U=(b+a+h) composed with inverse f. Since df=f_z(dz+mu dbarz), exactly g_n=f*(e^(-2U)|dw|²). The tensor eigenvalues are (1 +/- |mu|)². The required conformal factor is U on the plane, and U-b(w) on the sphere; it is zero near spherical infinity. Both g_n and the conformal target are complete, the latter by the onto isometry f.

For r>=2 choose a=0. The C^r convergence of mu implies g_n -> g* in C^r and in C² on the compact disk. Curvature is continuous in the positive metric two-jet. The positive compact minimum of background curvature therefore gives K(g_n)>0 for all sufficiently large n, with curvature unchanged outside the disk. The bad (r+1)-jet of f proves the asserted endpoint failure.

## Critical r=1: full nonlinear sign and quantifier order

Put ell=1+|log s|. The relevant bounds are |Df-I|<=C epsilon, |D²f|<=C epsilon ell, |D³f|<=C epsilon/s. The last estimate uses that the third derivative of z² vanishes. Chain rule yields |Dh|<=C epsilon ell and |D²h|<=C(epsilon/s+epsilon² ell²)<=C' epsilon/s. The bound s ell²<=4/e on 0<s<=1 and epsilon<=1 justifies the absorption; n can first be made large enough that the whole disk has s<1.

With J_ai=partial_i f_a and H=J^(-1), define L_n v=[Delta_w(v composed with inverse f)] composed with f. Twice differentiating the inverse identity gives

A=H H^T, B^i=-H_ia (partial_jk f_a) A^jk, L_n v=A^ij partial_ij v+B^i partial_i v.

The matrix order H H^T matters; H^T H generally differs. The drift B is present and bounded by C epsilon ell. It need not tend uniformly to zero on the shrinking scale, and the proof does not require that. A-I=O(epsilon), and A>=I/2 for n large. Bounded first and second background derivatives imply L_n(b+h)>=Delta b-C0 epsilon/s: the background error C epsilon(1+ell), Hessian h term C epsilon/s and drift term C epsilon² ell² are all controlled by epsilon/s with n-independent constants.

D²s=I/s-zz^T/s³ is positive semidefinite with eigenvalues rho²/s³ and 1/s; Delta s=(|z|²+2rho²)/s³>=1/s and |Ds|<=1. Therefore L_n s>=1/(2s)-C epsilon ell>=1/(4s), uniformly once epsilon is small, using bounded s ell. Choose one fixed K>4C0, then set a=K epsilon chi s. Its C¹ norm is O_K(epsilon), while its C² norm need not be small. On the inner disk L_n(b+h+a)>=Delta b+(K/4-C0)epsilon/s>0.

On the fixed annulus R/2<=|z|<=R, all derivatives of f-id,h,a needed in L_n are O_K(epsilon). With K already fixed, L_n(b+h+a) tends uniformly to Delta b, whose annular minimum is positive. The expression equals Delta b beyond the support. Thus the cutoff transition, both boundaries and the full inverse-coordinate drift are controlled. The exact curvature identity K(g_n)(z)=exp(2U(f(z))) L_n(b+h+a)(z) proves strict positivity; no first-order curvature approximation or numerical sample is substituted. Mu and a tending to zero in C¹ prove metric convergence, whereas partial_x²(f-id)(0)=-2 prevents C² map convergence.

The order of choices is fixed r and cutoff, derivative/background constants, one fixed K, then an n threshold covering the entire disk and annulus. There is no requirement of one universal n threshold across all r. No central analytic gap was identified within this theorem's exact scope.

## Finite diagnostic role and boundaries

The original standalone checker was fully read, then run with the bundled Python in isolated normal mode. Its complete 22,181-byte stdout equals the published expected JSON byte for byte. Its five rational geometric controls distinguish matrix order, inverse drift, negative uncorrected critical curvature, convex-radius Laplacian and a critical logarithmic conformal jet. Other finite controls cover log derivatives through 7, Beltrami homogeneity for r=1 through 8, and six metric reconstruction cases. Optimized Python refuses execution with the intended nonzero error. These tests check algebra and implementation guards; the all-order induction and uniform global curvature/completeness conclusions remain the written argument above.

The finite pointwise correction threshold in the diagnostic is not the proof's uniform K. Strict positivity on C is pointwise and decays at infinity for the background. Integer r=1 requires the correction, r>=2 uses curvature continuity, and r=0 uses a different isometric construction. A normalization also fixing a derivative would exclude the zero-endpoint example and is not the category being studied.
