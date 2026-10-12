# Root mathematical reconstruction: regular ZAS and boundary Bianchi defect

This is current authored validation, not an edit of the thirteen frozen source files. Target and boundaries are recorded in ROOT_CLAIM_LEDGER.md and independent primary-source receipts. No earlier exact priority claim is inferred here.

## Independent area-radius curvature route

Set a>0, rho>a, phi=1−a/rho, r=rho phi^2, f=1+4a/r and v=sqrt(f)=(rho+a)/(rho−a). Then dr/d rho=phi^2 v>0. The spatial metric is h=dr^2/f+r^2 dOmega^2. The general lapse is N=A+Bv, A,B>=0, A+B>0; the main case A=B=1/2 gives N=phi^-1. In this coordinate form g=−N^2dt^2+dr^2/f+r^2dOmega^2.

The smooth interior spherical Einstein formulas, obtainable directly from this diagonal metric, are

    G^t_t=(f−1)/r^2+f'/r,
    G^r_r=(f−1)/r^2+2fN'/(rN),
    G^theta_theta=G^varphi_varphi=fN''/N+(f/r+f'/2)N'/N+f'/(2r).

Here f'=−4a/r^2 and N'=B f'/(2v). The time component is exactly zero and G^r_r=4aA/(N r^3). Differentiating v^2=f gives

    fN''+(2f/r+f'/2)N'=0.

Hence each angular component is−2aA/(N r^3). The trace vanishes, so R_g=0. The radial eigenvalue agrees under the smooth r↔rho transformation. In rho coordinates the main diagonal is (0,2a/(rho^3 phi^5),−a/(rho^3 phi^5),−a/(rho^3 phi^5)); Ricci squared is6a^2/(rho^6 phi^10)>0 and diverges. This independently obtains the family's curvature without assuming the author's conformal-Ricci formula or a static-vacuum theorem.

At A=0 the Einstein tensor vanishes, while N=Bv is the negative-mass Schwarzschild vacuum lapse up to time rescaling. The same spatial metric with main N is not vacuum. At B=0,A>0 the metric is ultrastatic and still has a nonzero boundary functional; this endpoint is allowed for the family. A=B=0 is not Lorentzian. The a→0 family tends to flat interior geometry, but shrinking a changes the test boundary: a nonzero normalized boundary flux cannot be interpreted as a flat-spacetime defect at a=0.

## Geometric admissibility and causality

The resolution (delta,phi) is smooth through the exterior boundary, with phi zero only at rho=a and inward derivative1/a>0. Euclidean Laplacian phi=0. For any permitted C1 approaching surface family, Euclidean areas are bounded and sup phi^4→0, so physical areas shrink to zero. The regular mass formula yields −1/4(4a^(2/3))^(3/2)=−2a. These facts prove a harmonically regular ZAS on every constant-time slice, not merely a coordinate-sphere area limit. They do not assert resolution on every arbitrary tilted hypersurface, which is not the static-slice construction of the cited framework.

For the main lapse, the radial optical coordinate s satisfies ds/d rho=phi^3 and s~(rho−a)^4/(4a^3). The radial spacetime metric becomes phi^-2(−dt^2+ds^2), so s=0 is a timelike conformal radial boundary; nearby rho tubes have Lorentzian induced metrics. A radial null geodesic with conserved energy E=N^2 dt/d lambda has |d rho/d lambda|=E/phi and finite affine length (rho−a−a log(rho/a))/E, of order (rho−a)^2/(2aE). Invariant blow-up shows a genuine curvature singularity. N,phi→1 at infinity in the main normalized case.

## All-field absolute convergence and boundary functional

In exterior Cartesian coordinates x, rho=|x|>=a, n=x/rho. The volume density is N phi^6 dt d^3x. The weighted mixed Einstein tensor has only spatial entries,

    D^i_j=N phi^6 G^i_j=(Aa/rho^3)(6n_i n_j−2delta_ij).

D is Euclidean symmetric and trace zero. With

    Gamma^j_ik=2phi^-1(delta^j_i phi_k+delta^j_k phi_i−delta_ik phi_j),

D^i_j Gamma^j_ik is zero: its first term is tr(D)phi_k and the other two cancel by symmetry. Static spatial Christoffels with a time lower argument vanish and the entire time row/column of G is zero. Therefore for every smooth boundary-reaching compactly supported vector field psi,

    G^mu_nu nabla_mu psi^nu dV_g = D^i_j partial_i psi^j dt d^3x.

D and all coordinate derivatives of psi are bounded on its compact support, including the boundary, so the full scalar density is absolutely integrable. Individual connection summands may diverge logarithmically; there is no justification for integrating them separately, and none is used. This is no product of distributions.

The radial and angular eigenvalues of D are 4Aa/rho^3 and−2Aa/rho^3. Their spherical divergence D_r'+2(D_r−D_T)/rho vanishes, so partial_i D^i_j=0. The exterior-domain inner outward normal is−n. Ordinary Euclidean integration by parts then gives

    I_N(psi)=−(4A/a^2) integral_{R x S_a} <psi_spatial,n>_delta dt dA_delta.

For psi=eta(t)chi(rho)partial_rho, chi=1 near a, integral eta dt=1, this is−16pi A, hence−8pi at A=1/2. The radial field is smooth in the blown-up exterior Cartesian chart because rho>=a>0. It has angular-independent spherical components. The complete radial density directly equals4Aa eta(chi'/rho−chi/rho^2), another absolute convergence/sign check.

The area-radius transformed radial test has psi^r=(dr/d rho)eta chi. Weighted flux N r^2 G^r_r psi^r/v=4Aa chi/rho, giving the same inner trace. This explicitly tracks the field component; substituting an unrelated smooth field at a collapsed r=0 point would change the test space.

## Interpretation and source boundaries

For a vector test field, raising the first index in G_mu_nu nabla^mu psi^nu gives G^mu_nu nabla_mu psi^nu pointwise on the smooth interior. Lowering a vector by this singular metric need not preserve boundary smoothness; no vector-versus-covector convention is silently exchanged. The BKTZ source explicitly allows inner-boundary support and retains the radial normal component in its boundary formula. The original OWR conjecture is geometric, with no printed independent energy or specified electromagnetic matter restriction. Its broader physical research program is not resolved here.

The main case has exactly nonzero order(rho−a)^−5 mixed curvature and lacks the strict kappa>0 improvement in BKTZ Theorem1.1. The scalar density nevertheless exists absolutely by cancellation. Orthonormal energy density is zero and angular pressures are negative, so the angular NEC fails. The result must retain this limitation. Tests confined to the open interior give the automatic classical identity; smooth collapsed-point fields impose another convention. Neither is substituted for the directly verified source boundary convention.

## Verification and remaining gaps

Analytic reconstruction and direct source pages pass so far. Independently reproducible symbolic evidence and adversarial family reports are still pending. Historical manifests contain eleven extant file references (six FROZEN_INPUTS author payloads, five AUDIT_MANIFEST payloads); a standalone author-manifest SHA has no supplied path or bytes in this snapshot and cannot be claimed verified. That provenance limit does not change the immutable13-file SOURCE_RECEIPT binding. No new original proof-search turn was used. Earlier construction of the affine-lapse metric and any earlier exact conjecture resolution must still be investigated separately; no new-metric or first-resolution claim is made.
