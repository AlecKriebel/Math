# Independent universal endpoint proof

Scope: the literal candidate at original head `4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29`. All constants below may depend on the fixed integer r, the fixed smooth cutoff, and the background, but never on n. Each r has its own sequence. This is an independent verification of the endpoint construction, not a priority claim or a finite-test proof of a universal statement.

The source topology is the compact-open ordinary C^r topology on smooth metrics and functions and C^{r+1} on normalized smooth orientation-preserving diffeomorphisms. The original primary question and its cited paper confirm this convention. Failure of convergence of the diffeomorphism component alone disproves inverse continuity.

## 1. Background and the zero endpoint

In the plane chart put b=(1/2)log(1+|z|^2) for the plane and b=log(1+|z|^2)-log 2 for the sphere. Then g*=e^{-2b}|dz|^2 is respectively the complete cigar metric and the unit round metric. Direct differentiation gives curvatures 2/(1+|z|^2) and 1. Plane completeness follows from the divergent radial length integral int dr/sqrt(1+r^2). Sphere completeness follows from compactness. Both backgrounds have positive curvature, with a positive minimum on the fixed perturbation disk.

For r=0, let theta_n(s)=theta_0 eta(log(R/s)/n), R=1/4, with smooth eta equal to 0 for arguments <=0 and 1 for arguments >=1. Choose theta_0 not in 2pi Z. The map phi_n(z)=exp(i theta_n(|z|))z is a rotation on a neighborhood of 0 and the identity outside radius R; the flat transitions make it smooth. It is a diffeomorphism because it preserves radius and shifts angle. It fixes 0,1 and infinity as required. In orthonormal polar frames its differential, after rotation, is [[1,0],[q_n,1]], where q_n=s theta'_n(s)=-theta_0 eta'(log(R/s)/n)/n. Thus phi_n^*g* has relative matrix [[1+q_n^2,q_n],[q_n,1]], converging uniformly to I. The radial background factor is unchanged because the map preserves radius. These metrics are complete and positively curved by isometry. However Dphi_n(0)=Rot(theta_0) for every n. Their unique normalized inverse coordinates therefore fail to converge in C^1 to those of g*. No logarithmic estimate is needed at this endpoint.

## 2. All-r regularized logarithm estimates

For r>=1 fix a smooth radial chi supported in |z|<1/4 and equal to 1 in |z|<=1/8. Set rho=e^{-n}, epsilon=1/n, s=(x^2+y^2+rho^2)^{1/2}, L=log s, and f=id+epsilon chi z^{r+1}L. For n>=1, throughout the support s<1. The following bounds also cover rho->0 uniformly.

For any ordered x/y derivative of order j>=1, write D^jL=P_j/s^{2j}. The numerator P_j is a homogeneous polynomial of degree j in x,y,rho. Initially P_1 is x or y. Differentiation replaces P_j by s^2 D_i P_j - 2j x_i P_j. If C_j is its coefficient l1 norm, then C_{j+1}<=5j C_j: the derivative term contributes at most 3j C_j and the second term 2j C_j. Every coordinate has absolute value <=s, so |D^jL|<=5^{j-1}(j-1)! s^{-j}. This recurrence proves the estimate for every finite derivative order; no inference from checking j=1,...,4 is involved.

Leibniz's rule gives, for 0<=k<=r+1,

    |D^k(z^{r+1}L)| <= C_{r,k} s^{r+1-k}(1+|log s|).

Terms retaining L satisfy this by polynomial homogeneity, and every differentiated-L term has the same remaining power of s. Put t=-log s>=0. Then s(1+|log s|)=e^{-t}(1+t)<=1, and s(1+|log s|)^2<=4/e<2. For any integer p>=1, s^p(1+|log s|)<=1 as well. At the exponent-zero top derivative, s>=rho gives 1+|log s|<=n+1. Hence epsilon times that top bound is <=2. On the cutoff annulus |z|>=1/8, L and all fixed-order derivatives are uniformly bounded, so every differentiated-cutoff contribution is O(epsilon). These observations prove ||Df-I||_infinity<=C_r epsilon and ||f_z||_{C^r}<=C_r.

In the inner disk direct Wirtinger differentiation gives f_bar_z=epsilon z^{r+2}/(2s^2). To obtain all derivative bounds independently, write B=z^{r+2}/(2s^2); after k ordered x/y derivatives it has form Q_k/s^{2(k+1)}, with homogeneous numerator degree r+2+k. Differentiation replaces Q_k by s^2 D_i Q_k - 2(k+1)x_i Q_k. Its coefficient norm has a finite r,k-dependent recurrence. Thus |D^kB|<=C_{r,k}s^{r-k}. For k<=r these exponents are nonnegative, so ||f_bar_z||_{C^r}=O(epsilon), including the cutoff annulus.

For all sufficiently large n, |f_z|>=1/2. Repeated differentiation of 1/f_z expresses each derivative as finite products of derivatives of f_z divided by bounded-away-from-zero powers of f_z. Its C^r norm is therefore uniformly bounded. Consequently mu=f_bar_z/f_z satisfies ||mu||_{C^r}=O(epsilon). It is essential here that f_z is bounded in C^r, not convergent to 1 in C^r; the nonvanishing top jet precludes the stronger claim.

## 3. Global inversion, support, and exact reconstruction

Writing f=id+w, the global bound ||Dw||<1 gives |f(z)-f(z')|>=(1-||Dw||)|z-z'|. Surjectivity follows by iterating z_{k+1}=y-w(z_k): the successive distances decrease geometrically, the complete plane supplies a limit, and the limit solves f(z)=y. The Jacobian stays positive since Df is uniformly close to I, and the local smooth inverse theorem supplies a global smooth orientation-preserving inverse. This proves global inversion without invoking an endpoint continuity theorem for Beltrami solutions. Since f is the identity outside the fixed disk and injective, it maps that disk to itself and its inverse is also the identity outside. It fixes 0,1 and extends by the identity at infinity.

At 0 the cutoff is 1 and L(0)=log rho=-n. The first nonidentity Taylor term is -z^{r+1}; terms from L-log rho have degree at least r+3. Therefore

    partial_x^{r+1}(f-id)(0)=-(r+1)!

for every n, whereas this derivative of id is zero. This is exact, and disproves C^{r+1} convergence.

For a correction a supported in the same disk define

    g_n=e^{-2(b+a)} |dz+mu dbar z|^2,
    h=log|f_z|,   U=(b+a+h) composed with f^{-1}.

The real tensor |dz+mu dbar z|^2 has eigenvalues (1+|mu|)^2 and (1-|mu|)^2. It is positive for large n. The identity df=f_z(dz+mu dbar z) gives the exact equality g_n=f^*(e^{-2U}|dw|^2). In the plane the conformal-coordinate function is u=U; in the sphere it is u=U-b(w). Because f^{-1} is the identity off the disk and h=a=0 there, U=b there. Thus the sphere u is identically zero near infinity and extends smoothly; there is no singular-coordinate-factor leak.

The constructed g_n equals g* outside a compact disk, so it is complete: on that compact disk two smooth positive metrics are uniformly comparable, and outside it they coincide. This applies individually to every retained n. The conformal target metric is isometric to it and hence complete too. The normalized decomposition identifies the constructed f uniquely: two such representations differ by an orientation-preserving conformal automorphism of the underlying conformal plane or sphere. On the plane an affine map fixing 0,1 is the identity; on the sphere a Mobius map fixing 0,1,infinity is the identity. The conformal factors then agree. This argument needs neither an arbitrary quasiconformal solution choice nor an unproved inverse-continuity assertion.

## 4. Curvature for r>=2

Take a=0. The C^r algebra bound on mu yields g_n->g* in C^r, in particular in C^2. On the fixed disk, curvature is a continuous expression in the metric, its inverse, and its first two derivatives, with denominators uniformly bounded away from zero. The positive minimum of background curvature on this disk therefore gives positive curvature for all sufficiently large n. Outside it curvature is exactly that of g*. A global lower bound for the plane cigar curvature is not asserted or needed.

## 5. Critical r=1: exact nonlinear curvature control

The C^2 curvature-continuity argument is unavailable when r=1. On the inner disk let ell=1+|log s|. For f=id+epsilon z^2L the preceding Leibniz bounds imply

    |Df-I|<=C epsilon, |D^2f|<=C epsilon ell, |D^3f|<=C epsilon/s.

The third derivative has no undifferentiated-log term because the polynomial z^2 has degree 2. Since |f_z|>=1/2, the chain rule for h=log|f_z| gives |Dh|<=C epsilon ell and |D^2h|<=C(epsilon/s+epsilon^2 ell^2)<=C'epsilon/s; the last step uses s ell^2<=4/e and epsilon<=1.

For a smooth scalar v let L_n v=[Delta_w(v composed with f^{-1})] composed with f. With J=Df and H=J^{-1}, a second application of the chain rule gives

    L_n v=A^{ij}v_{ij}+B^i v_i,
    A=H H^T,   B=-H (A^{ij} partial_{ij} f).

Here the latter contraction is a vector over the two components of f. The order H H^T is important; generally H^T H is different. Thus A-I=O(epsilon), A>=I/2 for large n, and B=O(epsilon ell). With the fixed smooth b and the preceding h estimates, L_n(b+h)>=Delta b-C_0 epsilon/s, for one n-independent C_0. On the inner disk Delta b>0 for both backgrounds.

The Hessian of s is I/s-(z z^T)/s^3, with eigenvalues 1/s and rho^2/s^3; it is positive semidefinite even in the limiting rho->0 regime. Its trace is (|z|^2+2rho^2)/s^3>=1/s, and |Ds|<=1. Therefore

    L_n s >= (1/2)Delta s-C epsilon ell
          >= 1/(2s)-C epsilon ell >=1/(4s)

uniformly for all sufficiently large n, using s ell<=1. Choose one fixed K>4C_0 and set a=K epsilon chi s. This smooth correction satisfies ||a||_{C^1}=O_K(epsilon), because s and its gradient are uniformly bounded. Its C^2 norm need not be small. On the inner disk,

    L_n(b+h+a) >= Delta b+(K/4-C_0)epsilon/s >0.

On the fixed cutoff annulus, all fixed-order derivatives of f-id,h,a are O_K(epsilon). There the same exact operator is a small perturbation of Delta b>0, so its value is positive for all sufficiently large n, depending on the fixed K. Off the support it is Delta b. The conformal curvature formula is K(g_n)(z)=e^{2U(f(z))}L_n(b+h+a)(z), hence positive everywhere. This is a sign proof for the full nonlinear operator, not merely its linearization.

Finally mu->0 in C^1 and a->0 in C^1 give g_n->g* in C^1. The exact second derivative of f-id at 0 remains -2, so normalized inverse coordinates do not converge in C^2. No growth assumption at plane infinity is imported: the background is unchanged there, and completeness has already been proved.

## 6. Independent falsifying control for omitting the correction

For r=1 and chi=1, Re((f_z-1)/epsilon)=x[log(s^2)+(x^2+y^2)/(2s^2)]. Its exact Laplacian is

    4x[(x^2+y^2)^2+3(x^2+y^2)rho^2+3rho^4]/s^6.

Fix rescaled coordinates (xi,eta), set (x,y)=rho(xi,eta), and keep epsilon=1/n, rho=e^{-n}. Here Df-I=O(rho), D^2f=O(1), D^3f=O(epsilon/rho), Dh=O(1), and B=O(1). The second derivative formula for log f_z shows that the quadratic first-derivative term is O(1), while replacing 1/f_z by 1 changes the singular Hessian term by O(epsilon). Thus multiplying the full operator by rho/epsilon removes the O(1) nonlinear/drift/background errors, since rho/epsilon=n e^{-n}->0. The scaled curvature-sign operator tends exactly to

    4xi[T^4+3T^2+3]/(1+T^2)^3
      +K(T^2+2)/(1+T^2)^{3/2},   T^2=xi^2+eta^2.

At (xi,eta)=(-1,0), the uncorrected coefficient is -7/2. Therefore for sufficiently large n the uncorrected metric genuinely has negative curvature near that point, on either background. This is a falsifying control for deleting the correction, not a defect in the corrected candidate.

The absolute ratio of the error coefficient to the radius trace is bounded by 4. Squaring the worst-angle comparison, and putting Q=T^2>=0, its positive margin is

    (1+Q)^3(Q+2)^2-Q(Q^2+3Q+3)^2
      =Q^4+4Q^3+7Q^2+7Q+4 >0.

For fixed rescaled points the corrected leading coefficient is positive when K>4. This independent scaling check is consistent with the proof's nonlinear domination. It does not supply a simultaneous uniform-in-coordinate threshold or certify the diagnostic K=8 everywhere; Section 5 supplies the required uniform fixed-K estimate, including the cutoff region.

## Conclusion and limits

The construction supplies, for every finite integer r>=0 and on each of the two source surfaces, smooth complete strictly positive-curvature metrics converging to g* in C^r whose uniquely normalized coordinate diffeomorphisms fail to converge in C^{r+1}. Hence the inverse of the source parametrization is discontinuous. The constants are uniform in n for fixed r, including rho->0, the fixed cutoff transition, and the r=1 nonlinear correction. The candidate survives this adversary. This does not prove a C^infinity discontinuity, a simultaneous all-orders sequence, a fixed global lower positive curvature bound on the plane, or a new result's priority.
