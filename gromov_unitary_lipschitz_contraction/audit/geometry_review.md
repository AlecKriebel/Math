# Independent geometric verification

Checkpoint: 2026-09-23T03:36:38Z. Reviewer: independent geometry audit agent. Completion estimate for this bounded verification task: 100%. Publication priority is outside this review's completed scope.

## Verdict and limits

The supplied Möbius formula is a complete proof of the stated strong deformation retraction, for the unnormalized Hilbert–Schmidt Riemannian metric and for the operator-norm length metric on each finite-dimensional U(N). It proves the literal mathematical assertion printed as Gromov's [?24](i), including the stronger requirement that the homotopy never increase the input Lipschitz constant. No stabilization or dimension restriction beyond the natural sphere conventions is needed. No mathematical counterexample or proof gap was found.

There are two important scope qualifications, neither a gap in the theorem:

1. The source names a standard bi-invariant metric and gives its closed-geodesic normalization, but does not explicitly write either matrix norm. State the two metrics explicitly; do not say the normalization alone uniquely specifies every bi-invariant metric on U(N).
2. The preceding K-area discussion uses Lip < 1, whereas [?24](i) literally prints Lip < 1/2. This result answers the printed question; it does not, merely by that fact, establish a contraction preserving the Lip < 1 sublevel or close the surrounding argument at that larger threshold.

## Primary-source verification

Inspected both extracted text and rendered pages of M. Gromov, *101 Questions, Problems and Conjectures around Scalar Curvature (Incomplete and Unedited Version)*, October 1, 2017, printed pp. 35–36:

https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf

Printed p. 35 fixes unit spheres, n >= 2, target U(N), and the metric normalization with shortest nonconstant closed geodesic length 2 pi. Printed p. 36, [?24](i), asks for contraction to constant maps depending continuously on the original map, at Lipschitz bound strictly below 1/2. The nearby discussion involves families indexed by a manifold Y. The question does not spell out the topology of the map space or explicitly demand preservation of the Lipschitz sublevel during the homotopy. The candidate uses the natural compact-open/uniform topology and proves preservation, hence addresses the stronger reading.

The question URL https://www.unsolvedmath.com/problems/AMR-066-0025 did not produce content through this reviewer's web reader. The primary-source question itself was directly verified; matching aggregator metadata is left to the separate source/priority audit.

## Independent route: radial geodesic contraction

This route was developed independently of other reviewers' conclusions. It supplies a second geometric proof for the Hilbert–Schmidt metric. It is a derivation, not a claim that the result has previously appeared in print.

Write d_2 for the intrinsic metric from ||X||_2^2 = tr(X*X). Fix p in the unit sphere, A = Phi(p), W(x) = A*Phi(x), and let L = Lip(Phi). Principal eigenangles theta_j of W satisfy

    sum_j theta_j^2 = d_2(I,W)^2 <= pi^2 L^2.

For completeness, the distance formula follows because a minimizing geodesic in this compact bi-invariant Riemannian group is exp(i s B), and minimizing its Hilbert–Schmidt length among Hermitian logarithms B minimizes the sum of squared eigenangles, achieved by principal arguments. The injectivity radius is pi.

For 0 <= s <= 1, let P_s(W) = W^s = exp(s Log W), with the principal logarithm. When L <= 1/2, all eigenangles lie in [-pi/2,pi/2], so the logarithm is uniquely and smoothly defined. In a unitary eigenbasis, the derivative of holomorphic functional calculus multiplies the (j,k) entry of E by

    (exp(i s theta_j) - exp(i s theta_k)) /
    (exp(i theta_j) - exp(i theta_k)),

with the derivative value s exp(i(s-1)theta_j) on repeated eigenvalues. The off-diagonal multiplier has modulus

    |sin(s (theta_j-theta_k)/2)| /
    |sin((theta_j-theta_k)/2)|.

Since |theta_j-theta_k| <= pi, sine is increasing in absolute value on the relevant half-angle interval, and every multiplier has modulus <= 1. Summing squared matrix entries gives

    ||D P_s(W)[E]||_2 <= ||E||_2.

Apply this local estimate along the image under W of a minimizing domain geodesic. It gives Lip(A P_s(W)) <= L. As s decreases from 1 to 0, this is a strong deformation retraction to the evaluation constant A. The analytic logarithm gives joint continuity. This argument does not need a globally minimizing target geodesic to remain in the spectral region: the image curve of the domain geodesic is the curve to which the derivative estimate is applied.

In fact this argument proves the Hilbert–Schmidt result for L <= 1/sqrt(2). Indeed, |theta_j-theta_k| <= sqrt(2) (sum theta_l^2)^(1/2) <= pi, and |theta_j| <= pi/sqrt(2) < pi still avoids the logarithm cut. This stronger Hilbert–Schmidt threshold is not claimed for the operator-norm metric by this proof. An entrywise bound on Schur multipliers does not by itself give their operator-norm bound.

Geometrically, the same derivative computation is the Jacobi-field computation for radial geodesic contraction. For the standard Hilbert–Schmidt metric the sectional curvature is <= 1/2: the bi-invariant curvature formula is K(X,Y)=||[X,Y]||_2^2/4 for orthonormal X,Y, and diagonalizing X gives ||[X,Y]||_2 <= sqrt(2)||X||_2||Y||_2. The explicit spectral computation above avoids any need to cite or assume a general convexity theorem.

## Direct adversarial checks on the supplied formula

- **Eigenangle control:** Following any unitary path on a fixed eigenvector yields a curve on the real unit sphere. Its length is at least the principal eigenangle magnitude. Because vector speed <= operator-norm matrix speed <= Hilbert–Schmidt speed, d_nu(I,W) <= pi/2 implies Re W >= 0 for either metric. This step is sound.
- **No pole at the endpoint:** (I+tW)*(I+tW) = (1+t^2)I+2t Re W >= (1+t^2)I. Thus the inverse exists even at t=1 and on the closed boundary Re W=0. The strict sublevel is not being silently used at this step.
- **Noncommutativity:** Multiplying the difference identity on the left by I+tU and the right by I+tV gives exactly (1-t^2)(U-V). Only a matrix commutes with its own rational functions; there is no assumption that U and V commute.
- **Unitarity:** The factors X=W+tI and Y=I+tW have X*X=Y*Y, which directly implies (XY^{-1})*(XY^{-1})=I.
- **Intrinsic versus extrinsic metrics:** The matrix-norm difference inequality alone would not establish the intrinsic Lipschitz estimate. The candidate correctly adds the derivative estimate and integrates it along the actual image of a spherical geodesic. Lipschitz image curves are absolutely continuous in this finite-dimensional matrix setting, with metric length computed by integrating the corresponding tangent norm almost everywhere. This completes the bridge.
- **Continuous families:** Evaluation at one fixed p, matrix multiplication, adjoint, and uniformly bounded inversion depend continuously on the input in uniform topology. The displayed 3-delta estimate is valid. The time variable is uniformly continuous on a compact matrix domain. Thus arbitrary continuous parameter families are treated, not merely each individual map.
- **What retracts:** The endpoint is the input-dependent constant Phi(p). The constant-map subspace is U(N); it is not claimed to be contractible. Only the based subspace contracts to the identity map.
- **Strict and closed thresholds:** q_t=(1-t^2)/(1+t^2) lies in [0,1], so both Lip < 1/2 and Lip <= 1/2 are invariant. Boundary eigenangles +/-pi/2 cause no singularity.
- **N=1:** All arguments reduce to an ordinary disk-boundary Möbius transformation. The angular derivative has the asserted bound, including the endpoints.
- **n=2 and all larger n:** The only domain facts needed are compactness, diameter pi, and existence of minimizing geodesics. There is no parity restriction.
- **n=1:** S^0 is not a connected geodesic space. It must be handled separately, as the candidate does, if equipped with angular distance pi. The scalar eigenangle formula and the max/Euclidean norm formula for distance from I give the claimed two-point estimate. The printed geometric setup already assumes n >= 2; the extension is optional.
- **Stabilization:** F_t(diag(W,I_k))=diag(F_t(W),I_k), so the construction is compatible with standard inclusions but never requires an inclusion.
- **Change of target frame:** H_t(B Phi C)=B H_t(Phi) C for fixed B,C in U(N). This follows from conjugation covariance of F_t and confirms that choosing matrix frames does not introduce hidden discontinuous choices.

## Metric-normalization qualification

The shortest-geodesic normalization alone does not uniquely specify a bi-invariant metric on U(N), which has independent central and traceless weights. For example, on U(3) the invariant quadratic norm on Hermitian generators

    ||B||_g^2 = (1/2) tr(B^2) + (5/6)(tr B)^2

has shortest nonzero integral generator norm 1 (attained at diag(1,-1,0)), hence shortest closed one-parameter subgroup length 2 pi. But B=diag(1,-1/2,-1/2) has ||B||_g=sqrt(3)/2 < ||B||_op=1. Thus the eigenangle domination used in the candidate is not a consequence of the closed-geodesic normalization alone for arbitrary invariant metrics. This does not refute the explicitly stated standard Hilbert–Schmidt or operator-norm theorem. It is a reason to define those norms in the paper rather than elevate an informal normalization to a uniqueness assertion.

## Priority implications and remaining gap

There is no remaining mathematical gap in the candidate's precise theorem. The two independent mechanisms here are (a) the proposed rational matrix homotopy, valid in both norms, and (b) radial geodesic contraction, valid with the above direct proof in Hilbert–Schmidt norm and even at a larger threshold.

If sublevel preservation is dropped entirely, the principal-log homotopy already works for L < 1 in either norm, because d_nu(I,W) < pi keeps the image away from eigenvalue -1. Therefore a paper should emphasize its explicitly quantitative, sublevel-preserving theorem, not suggest that every ordinary null-homotopy construction was unavailable.

This review does not certify first publication or novelty. The elementary alternative and familiar Möbius/Cayley mechanism make an explicit and qualified prior-art audit particularly important. No outreach was initiated or prepared.
