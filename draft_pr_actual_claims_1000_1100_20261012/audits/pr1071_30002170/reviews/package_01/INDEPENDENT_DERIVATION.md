# Independent theorem derivation before previous verdict labels

The candidate paper was read completely after a hash-only freeze. No previous acceptance or review verdict was used to derive the following.

## Target and assumptions

Two independent centered standard equal-H fractional Brownian motions, H in (1/4,1), T>0, n>=1, both full uniform observation vectors including T. X is the canonical cross iterated integral, not an antisymmetric difference. The proposed lower bound applies to every square-integrable nonlinear function of this finite observation vector. Canonical existence and convergence must be verified from primary source interfaces separately below.

## Reconstruction

Use the real conjugate-symmetric subspace of complex L2(R), with K_t=D_H^(-1/2)(exp(it xi)-1)|xi|^(-H-1/2). Its increments have squared norm |t-s|^(2H), by substitution, and real polarization gives the standard covariance. D_H is positive finite for 0<H<1: near zero the integrand is O(|xi|^(1-2H)), and at infinity it is O(|xi|^(-1-2H)). A real zero-extended bump h has u_h=sqrt(D_H)/(2pi)|xi|^(H+1/2) conjugate(hat h). Then <K_t,u_h>=h(t)-h(0). Conjugation is necessary with the stated Fourier transform; this covariance identity, not a label on a reproducing kernel space, is the needed mechanism.

Choose phi=x^4(1-x)^4 on [0,1], f=phi-prime, g=phi, and zero extensions. The traces of f,f-prime,f-double-prime and of g,g-prime,g-double-prime vanish at both boundaries, so their third weak derivatives contain no delta masses. Three integrations by parts give |hat r|<=min(L_r,N_r|xi|^-3), sufficient for absolute inversion and weighted L2 integrability at alpha=2H+1 in (3/2,3). The positive deterministic pairing is integral f*g-prime=integral (phi-prime)^2=4/45045.

Cell bumps r_j(t)=Delta^H r(t/Delta-j) produce scale-independent Gram kernels: Fourier transform is Delta^(H+1) exp(-ij Delta xi) hat r(Delta xi), and 2H+2-alpha-1=0. Periodize weighted squared transforms, retaining signed actual Fourier coefficients rather than assuming independent cells. The central term is bounded by pi^alpha L_r^2; the two tails are bounded by 2 N_r^2 pi^(alpha-6) sum_(l>=1)(2l-1)^(alpha-6). Monotone integration gives sum<=1+1/[2(5-alpha)]. Thus each finite Gram matrix is PSD and bounded above by M_r I, M_r=D_H Pbar_r/(2pi).

Every cell bump vanishes at every full-grid point and at zero. Therefore all witness coordinates U_j=W1(u^f_j), V_j=W2(u^g_j) have zero covariance with all observation coordinates. Joint Gaussianity yields independence of the WHOLE witness vector from the WHOLE observation vector, although witness cells need not be independent among themselves. Define Y=sum U_j V_j. Independence of the two Gaussian processes gives E Y=0, E Y^2=sum A_jk C_jk=tr(AC). Since A<=M_f I and C is PSD, tr(AC)<=M_f tr C<=n M_f M_g. No elementwise sign or commutativity assumption is needed.

With fixed n,T,j, pair a finite left Euler sum with U_j V_j. Independent components factor the expectation into f_j(t_k)[g_j(t_(k+1))-g_j(t_k)]. If the left sums converge in L2 to X, this pairing passes to the limit and the deterministic sums tend to integral f_j g_j-prime=a Delta^(2H). A finite sum over j gives E XY=n a Delta^(2H). All nonlinear L2 grid estimators F satisfy E FY=0; Cauchy-Schwarz therefore gives ||X-F||2 >= a/sqrt(M_f M_g) T^(2H)n^(1/2-2H), exactly the stated c_H. E XY>0 also ensures Y is not the zero variable.

## Stochastic convergence requiring source verification

On unit cells, finite variance c0 and Cauchy-Schwarz bound |c1|<=c0 suffice. For separated cells r>=2, derivative kernels have no cross singularity. Component independence multiplies two factors H(2H-1), even when each is negative for H<1/2; triangle volumes give 0<=c_r<=H^2(2H-1)^2(r-1)^(4H-4)/4. The finite lag sum consequently has orders m^(1-4H), m^-2 log m, or m^-2 for H below/equal/above 3/4. Each vanishes when H>1/4. Brownian cross Ito is handled separately. The linear-interpolation correction is exactly half the sum of products of independent component increments, with variance T^(4H)m^(-4H)/4 times [m+2 sum_(r>=1)(m-r)rho_H(r)^2]; the second-difference bound gives the same vanishing regimes. Thus a valid analytic-area construction with Chen relation and the stated separated-cell limit supplies the canonical Euler interface without exact asymptotic coefficients.

## Boundary and law-transfer checks

n=1 needs no asymptotic argument. No constant uniform in H is asserted. At H=1/4 the correction's diagonal term is T/4, so this bridge does not extend; at H=1, linear paths make X endpoint measurable and D_H diverges. Enlarging the Gaussian representation to obtain U,V is allowed: finite observations and Euler sums have the same joint law in both models, their L2 limits preserve that law, and any L2 estimator is a Borel function of the finite observation vector up to null sets. The argument does not require the auxiliary witness to be measurable with respect to the original paths.

Initial mathematical reconstruction: no apparent logical gap in the claimed lower theorem, contingent on checking the primary canonical-area source interface and exact original target. This is not a whole-package clearance or novelty certification.
