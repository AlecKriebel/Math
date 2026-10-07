# Independent audit of the four spectral realization routes

Problem 30005990, OWR-14298587-002. Audit date: 2026-10-07 UTC.

Reviewed file: REALIZATION_APPROACHES.md, 18,644 bytes, SHA-256 eb2502b48d0781a2ab70e6ed023696875f889a33ce95ac08cf7fffff75409b0b.

## Decision

Accept the four results at the scopes actually stated in this file. They are useful partial results and obstructions. None proves attainment of boundary frequency 5/2 by an unrestricted bounded-domain global spectral sum minimizer. The unresolved disposition is warranted. The acceptance of PROOF.md was not used as a substitute for checking these additional arguments.

## Cartesian product route

The restricted product formula follows by separating tangential and interval energies for normalized factors. The interval ground-state contribution is pi^2/L^2 per component. The restriction that the tangential components are already segregated is explicit; this is not asserted for arbitrary product-domain competitors.

The long-cylinder obstruction is valid. Globally normalized segregated functions on the base are orthonormal, so the sum of their Rayleigh quotients is at least the sum of the first N base eigenvalues. Connectedness of the bounded Lipschitz base gives a strict spectral gap above the first eigenvalue. Thus Delta=E_N(Omega)-N lambda_1(Omega)>0. The N transverse slabs have sum N lambda_1(Omega)+N^3 pi^2/L^2, and subtracting the restricted value gives

    -Delta + N(N^2-1) pi^2/L^2.

The stated threshold makes this negative. This is an actual family of admissible competitors disproving unconditional tensorization, not just failure of a proposed proof. At a nonzero slice of one slab only one phase survives, so the proposed stronger slice inequality also fails exactly as described.

As an independent concrete control, take the square base (0,pi)^2, N=3 and L=10 pi. The first three base eigenvalues are 2,5,5. Every vertical Cartesian partition has total at least 12.03, whereas the horizontal slabs have total 6.27. These values simply verify the general obstruction; no knowledge of the precise optimal three-partition of the square is used.

## Angular spectral route

The surface Jacobian is correct: in x coordinates the original hemisphere has measure dx/t and its radial lift has measure t dx d omega, hence the ratio is t^2. Division of the angular function by t cancels this ratio in the squared L^2 norm.

The ground-state transform with h=t and -Delta_S h=(d-1)h gives the angular energy shift with the negative sign stated in equation (3.1). Since the resulting identity makes the old H^1 norm equivalent to a fixed positive linear combination of the new L^2 norm and energy, the initial compactly supported transform extends continuously by density.

The onto argument for invariant functions is also valid. Averaging compactly supported smooth approximants over the compact rotation group keeps their supports compact inside the invariant lifted domain. They descend to compactly supported smooth functions of (x,t), and the same norm identity passes to the limit. This avoids needing a regular boundary for the open angular cell. The omitted codimension-three axis has zero H^1 capacity and does not create a positive-energy Dirichlet barrier.

For the full bottom eigenvalue, the proof averages a nonnegative first eigenfunction. The average is nonzero, remains an eigenfunction, and has the same eigenvalue. This is the correct argument; averaging an arbitrary Rayleigh quotient would not justify the conclusion. Thus

    lambda_1(omega_tilde)=lambda_1(omega)-(d-1)

holds at the claimed scope. If a cell is disconnected, a connected component supporting part of a first eigenfunction has the same first eigenvalue, which justifies the reduction used for the min-max comparison.

Corollary 3.6 of the cited Ognibene-Velichkov v5 paper gives the full-sphere three-cell min-max result. Substituting ambient dimension d+2 and adding back d-1 yields exactly (5/2)(d+1/2). The tangential tY cells attain it. No arbitrary-open-cell point-set uniqueness is claimed; that would require attention to removal of capacity-zero sets.

The source distinguishes the sphere's sum conjecture from its proved min-max theorem. The candidate preserves that distinction. Even a hemispherical sum result would not by itself settle nonconical Euclidean competitors. The two remaining steps are genuine and are not supplied by the spectral shift.

## Thin cylinder route

The rescaling w(x,s)=sqrt(epsilon)u(x,epsilon s) preserves each component's L^2 normalization. The transverse energy coefficient is epsilon^(-2), and the subtraction is N pi^2/epsilon^2. On the normalized admissible class every transverse excess is nonnegative.

Projection onto e(s)=sqrt(2)sin(pi s) is correctly used only as an analytic approximation. The projected components are not prematurely asserted to be segregated. The first non-ground transverse mode has eigenvalue 4 pi^2, so the excess bounds the remainder's squared L^2 norm by the factor 3 pi^2. This gives a remainder of order epsilon in L^2 for every bounded-energy sequence.

The projected functions have zero base trace, remain nonnegative, and have bounded tangential H^1 norms. Rellich compactness and the vanishing remainder give strong L^2 convergence to f_i e, preserving the individual norms. Strong convergence of both factors gives convergence of their products in L^1, so segregation of the original tuples passes to f_i f_j=0. This is the essential nonlinear constraint, and the proof handles it correctly.

Weak lower semicontinuity gives the liminf. The exact products f_i e give recovery. The same bounded-energy compactness shows that a finite-energy limit outside this product class cannot occur. Therefore the stated extended-functional Gamma-convergence assertion and convergence of the minimum values are justified, not merely formal dimensional reduction.

There is no established persistence theorem for boundary singularities in this argument. Its compactness and energy convergence do not identify a finite-thickness boundary stratum or prove exact frequency. The product boundary's edges also remain. The file expressly disclaims both missing steps.

## Bessel spectral construction

The separation index is correct:

    nu=gamma+(d-2)/2=(d+3)/2, with gamma=5/2.

For the radial factor r^(-(d-2)/2)J_nu(kr), the Bessel equation supplies angular coefficient nu^2-(d-2)^2/4=gamma(gamma+d-2). Choosing k=j_(nu,1)/R imposes the outer Dirichlet condition. Positivity before the first positive zero and positivity of the angular factor identify a first eigenfunction on each connected cell. Rotational congruence permits one common normalization.

The Bessel series gives a relative radial error O(r^2). Multiplying the degree-5/2 cone produces the asserted O(r^(9/2)) function remainder and O(r^(7/2)) gradient remainder. The gradient estimate is understood in each smooth phase and for the zero extension almost everywhere; classical derivatives across a regular interface need not exist. These estimates suffice for the limiting boundary-frequency computation. The Bessel equation, series, and zero conventions were checked against NIST DLMF Sections 10.2 and 10.21.

The equal angular flux magnitudes remain equal after multiplication by the common radial factor. The localized Hadamard first variations therefore cancel pairwise. The supports are explicitly restricted away from the singular spine and outer boundary, so the calculation does not silently assert a second-variation or singular-junction theorem.

This constructs real eigenfunctions and the desired local boundary asymptotic, but no global minimum certificate. The half-ball rim is not globally C^1, and the proof does not assume its smoothing preserves either exact separation or the singularity. These limitations are essential and accurately stated.

## Final conclusion

No additional corrective patch is required for the scoped statements in the frozen file. The four routes strengthen the partial result without closing global spectral realization. Accept them alongside the independently checked sharp cone theorem, while retaining the original problem as unresolved under the strict spectral-attainment reading.

## Primary sources

- Ognibene-Velichkov, arXiv:2412.00781v5, Section 1.2 and Corollary 3.6: https://arxiv.org/abs/2412.00781v5
- NIST DLMF, Bessel equation and defining series: https://dlmf.nist.gov/10.2
- NIST DLMF, positive zeros: https://dlmf.nist.gov/10.21
