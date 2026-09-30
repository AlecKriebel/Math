# Problem 16 is solved by Gasull–Rojas (2025)

**4700016 / AMR-046-0016. Recommended status: already_solved, 0/5 original proof attempts. Independent source audit pending.**

## Exact original target and published answer

Gasull's *Some open problems in low dimensional dynamical systems*, Section 3.5, Problem 16 (printed p.16), asks whether the period of the center at the origin decreases throughout its period annulus for

    dz/dt = i z + (z conjugate(z))^n z^(k+1),   n,k positive integers.

Gasull and Rojas's Theorem A answers this exact question affirmatively, even allowing an arbitrary nonzero complex coefficient on the nonlinear monomial. Taking that coefficient to be 1 gives the requested result for every allowed n and k. The theorem also gives the limiting periods: 2 pi at the center and 2(k+n) pi/(k+2n) at the outer boundary.

The published source is Armengol Gasull and David Rojas, *Monotonous Period Function for Equivariant Differential Equations with Homogeneous Nonlinearities*, Mediterranean Journal of Mathematics **22**, article 112 (2025), DOI [10.1007/s00009-025-02879-2](https://doi.org/10.1007/s00009-025-02879-2). The publisher records publication on 24 June 2025 and explicitly identifies the original Problem 16. The complete author preprint is [arXiv:2411.12408v1](https://arxiv.org/abs/2411.12408v1), Theorem A on p.2 and its reduction on pp.13–14.

This is a credited prior resolution, not a new campaign discovery. The full global period-monotonicity theorem is an imported published result, not independently reproved by the finite controls below.

## Direct checks of the matching conventions

The original formula has z^(k+1), with conjugation only inside z conjugate(z). Its nonlinearity has total degree 2n+k+1. For omega^k=1, substitution gives F(omega z)=omega F(z). Thus the correct equivariance group is Z_k. The imported report's Z_(k+2) assertion is erroneous and is not used. Reversibility holds for R(z)=exp(i pi/k) conjugate(z): direct substitution gives F(Rz)=−R(F(z)), where R acts real-linearly. The linearization at the origin is rotation, consistent with the specified reversible center.

For a check of the cited reduction, put z=r exp(i theta), m=2n+k, R=r^m, Theta=k theta and tau=k t. The transformed equations, computed directly, are

    dR/dtau = b R² cos Theta,    dTheta/dtau = 1+R sin Theta,
    b = (2n+k)/k.

Writing X+iY=R exp(i Theta), then x=−(1+b)Y, y=−(1+b)X and s=−tau gives

    dx/ds = −y+xy,
    dy/ds = x+D x²+(D+1)y²,
    D = −1/(1+b) = −k/[2(k+n)] in (−1/2,0).

The algebra and parameter inclusion are exact. The k-fold angular covering corresponds to k repeated sectors, while tau=k t multiplies elapsed sector time by k; the factors cancel for the full physical period. Reversing time does not change a positive period. The published Theorem A, rather than this algebra alone, supplies the global annulus correspondence and monotonicity. In particular a sign check of the first local period coefficient would not prove the requested global result.

The target concerns the center at the origin with n,k>0. It does not ask about other centers, n=0, k=0, or the general two-parameter family of reversible quadratic centers. The earlier campaign record 4700009 asks about positive periodic solutions of x^p x''=f(t), a distinct nonautonomous equation; its result is not reused here.

## Verification and provenance

The checker verifies rational parameter inclusion, the polynomial coordinate-change identities, the boundary-period coefficient, and the degree/exponent symmetry conditions. These are source-application controls, not a proof certificate for the published analytic theorem. Both original Problem 16 and preprint Theorem A were visually checked from their full PDFs; the publisher's full HTML confirms the theorem and publication details.

The current queue and prior-Alec gates found the target queued and no previous attempt or PR. The pinned imported report was read in full: its partial-progress assessment is superseded by this complete published resolution. No repository queue generator was run. No external outreach, release, original-discovery claim or new human peer-review claim is made. The inherited native runtime was used unchanged; its exact model identifier was not exposed.

### Primary sources

- Original Problem 16: https://arxiv.org/abs/2012.02524
- Published Theorem A: https://link.springer.com/article/10.1007/s00009-025-02879-2
- Full author preprint: https://arxiv.org/abs/2411.12408v1
