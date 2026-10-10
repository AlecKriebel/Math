# Independent adversarial audit A: compact three-form deformation

Date: 2026-10-07.

## Decision

**ACCEPT the mathematical counterexample in the unchanged frozen R3 manuscript.** No correction is required for the asserted existence of a smooth closed connected almost-complex four-manifold with nonintegrable almost-complex structure and at least three independent closed anti-invariant real two-forms.

Audited object: `R3_counterexample_candidate.md`, 9,997 bytes, SHA-256:

`50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e`

This is an independent verification of this exact proof, not a novelty determination, journal endorsement, or assertion that every related claim in the literature has been checked. The original manuscript was not edited. No mathematical correction patch is attached because none is needed.

## Scope and target match

The target is the integrability implication for the real dimension of closed J-anti-invariant two-forms on a compact real four-manifold. The original OWR report states this as Conjecture 2.5 on printed page 1687, PDF page 31. Its definitions use anti-invariance in the usual sense, alpha(JX,JY)=-alpha(X,Y), and identify the dimension with anti-invariant de Rham cohomology in the compact four-dimensional case. The construction meets both interpretations: it supplies three closed anti-invariant forms whose de Rham classes are independent.

Primary target: [Mini-Workshop: Almost Complex Geometry, OWR 33/2020](https://doi.org/10.4171/owr/2020/33), [publisher PDF](https://ems.press/content/serial-article-files/46869?nt=1).

No statement or proof from the withdrawn arXiv:1507.00282 is used. The generic-vanishing clause is outside this counterexample audit; a special family with three surviving classes is compatible with generic vanishing.

## 1. The compact starting surface and forms

The affine curve y^2=z^6-1 is nonsingular. At an affine point where y=0, z is a nonzero simple root of z^6-1, so the derivative with respect to z is nonzero. Near infinity, put s=1/z and Y=y s^3. The equation becomes Y^2=1-s^6, yielding two smooth points at infinity with Y=+1 and Y=-1. The branched double cover of the sphere has six simple branch points, giving genus two by Riemann-Hurwitz. Its connectedness also follows from the connected branched cover, or the nonsquare polynomial.

At finite branch points, z-r is a nonzero constant times a squared local coordinate to leading order, so dz/y is regular and nonvanishing there. At infinity the exact expressions are

- dz/y = -s ds/Y;
- z dz/y = -ds/Y.

Both differentials extend holomorphically. They are independent because their ratio is the nonconstant meromorphic function z. Taking their wedge products with the nowhere-zero one-form on an elliptic curve produces two independent holomorphic two-forms on the closed connected product surface.

The manuscript's cohomology-independence argument is valid. An independent proof avoiding harmonic theory is available: for real constants a,b,c, put F=(a-ib)Omega_0+c Omega_1 and q=Re F. If q is exact, Stokes gives integral q^2=0. In complex dimension two, q^2=(1/2)F wedge conjugate(F), which is nonnegative for the complex orientation and is positive wherever F is nonzero. Hence F vanishes identically. Complex independence of Omega_0 and Omega_1 then gives a=b=c=0. This proves independence of the three real de Rham classes.

## 2. Simultaneous coordinate normalization

Near z=0, y=i and w=0, take a single-valued holomorphic nonzero branch y(z) and an honest elliptic local coordinate w. The proposed coordinate change zeta=z, xi=w/y(z) has Jacobian determinant 1/y(z), so is locally invertible. Furthermore

 d zeta wedge d xi = dz wedge (dw/y - w y'(z) dz/y^2) = (dz/y) wedge dw.

The extra term vanishes because dz wedge dz=0. Thus both claimed normal forms hold simultaneously, including the factor zeta for Omega_1. There is no requirement to find incompatible Darboux coordinates or to normalize a Kähler form at the same time.

With zeta=u+iv and xi=x+it, the signs of alpha=du wedge dx-dv wedge dt, beta=du wedge dt+dv wedge dx, and gamma=u alpha-v beta are all correct.

## 3. Exact perturbation, third-form identity, and support

The cutoff is smooth with compact support strictly inside the coordinate ball. Consequently both R dv and R v dv extend by zero to smooth global one-forms, with no boundary distribution or derivative jump. Their exterior derivatives are globally exact. Closure and the three de Rham classes are therefore preserved exactly, not merely approximately.

The identity that could have failed in the cutoff region does hold:

 d(R v dv)=v dR wedge dv + R dv wedge dv = v d(R dv).

Thus gamma_epsilon=u alpha-v beta_epsilon throughout the whole chart, including where the cutoff varies in all four variables. No derivative of the cutoff has been dropped. Outside the chart the forms are unchanged. The functions u and v need not extend globally; only the compactly supported one-forms using them are extended.

## 4. Positive plane and actual construction of J

Direct independent expansion, using vol=du wedge dv wedge dx wedge dt, gives

- alpha^2=2 vol;
- alpha wedge beta_epsilon=R_t vol;
- beta_epsilon^2=2(1-R_x) vol.

The R_u term does not contribute to these wedge products; the R_v term vanished already on wedging dR with dv. Thus the determinant condition is exactly D=1-R_x-R_t^2/4>0. The manuscript's bounds |R_x|<=1/4 and |R_t|<=1 imply D>=1/2. Such uniform bounds follow from fixed compact support and sufficiently small |epsilon|.

After subtracting (R_t/2)alpha and dividing by sqrt(D), the normalized imaginary form B_epsilon satisfies alpha wedge B_epsilon=0 and B_epsilon^2=alpha^2. Therefore Psi_epsilon=alpha+i B_epsilon has square zero and Psi_epsilon wedge conjugate(Psi_epsilon)=4 vol.

Here a nonzero square-zero complex alternating two-form on a complex four-dimensional vector space has rank two, hence is decomposable. The nonzero product with its conjugate ensures that its two-dimensional complex kernel and the conjugate kernel are complementary. Declaring the kernel to be T^(0,1) gives a genuine real almost-complex structure, not merely a conformal class or an unoriented plane. Constant rank gives smoothness. This also fixes the sign of J: when R and its derivatives vanish, Psi_epsilon=Omega_0, so this J is exactly J_0 rather than -J_0.

There is an open collar of the ball on which the cutoff, R, and all derivatives vanish. The local structure consequently agrees identically with J_0 on that collar and glues smoothly to J_0 outside. Zeros of Omega_0 elsewhere are irrelevant because the kernel construction is never used there. The claimed C-infinity convergence follows from the fixed smooth cutoff, linear dependence R=epsilon rho x^2/2, and the smooth positive square-root normalization near D=1.

The real and imaginary parts of a (2,0)-form are anti-invariant. The three perturbed forms lie in their real span in the chart, by the normalization and the exact third-form identity, and are original anti-invariant forms outside. This proves global anti-invariance of each form. Together with the already verified class independence, it establishes h^- >=3.

## 5. Independent nonintegrability calculation

On the open core, k=1-epsilon x is positive and the proposed (1,0)-coframe is valid. Its wedge is exactly alpha+i beta_epsilon/sqrt(k), with no omitted scale factor. Direct calculation gives

 d phi_1 wedge phi_1 wedge phi_2 = k_x/(2k) vol.

It is nonzero for epsilon nonzero. Under integrability, the exterior derivative of any smooth (1,0)-form has no (0,2) component, so that wedge would vanish. Only this necessary condition for integrability is used; no unproved converse is invoked.

Independently, the coframe determines

 J partial_u=k^(-1/2)partial_v, J partial_v=-sqrt(k)partial_u,
 J partial_x=sqrt(k)partial_t, J partial_t=-k^(-1/2)partial_x.

For the precise Nijenhuis convention given in the manuscript, the only relevant bracket is

 [k^(-1/2)partial_v,partial_x]=k_x/(2k^(3/2))partial_v.

It follows that N(partial_u,partial_x)=k_x/(2k)partial_u, which equals -epsilon/2 partial_u at the origin. This agrees with the manuscript and is manifestly nonzero. Differences in conventions can multiply N by a nonzero constant or sign, but cannot change the conclusion.

## 6. Adversarial checks against possible obstructions

1. The number three concerns real linear independence of global forms/classes, not pointwise independence. The pointwise bundle of anti-invariant forms has rank two. The exact functional relation among the three forms is therefore expected and does not contradict global independence.
2. Neither the original beta nor the original gamma is asserted to remain anti-invariant after the deformation. Their exact differences from the perturbed forms therefore do not violate the absence of nonzero exact anti-invariant forms on compact four-manifolds.
3. Closedness of two pointwise independent real anti-invariant forms does not force integrability. The normalized complex combination need not be closed. On the core its nonconstant normalization is exactly where the nonzero Nijenhuis tensor appears.
4. Theorem 1.1 of Draghici-Li-Zhang, [On the J-anti-invariant cohomology of almost complex 4-manifolds](https://arxiv.org/abs/1104.2511), concerns structures sharing a compatible metric with the initial integrable structure. This hypothesis fails here. At a core point with x not equal to zero, beta_epsilon-beta=-epsilon x dv wedge dx is nonzero and has square zero. If J_epsilon and J_0 shared a compatible metric, alpha, beta and beta_epsilon would all be self-dual for that metric and span a positive-definite subspace of the wedge pairing. Such a subspace cannot contain a nonzero square-zero form. This gives a direct reason the cited special-case bound does not exclude this construction.
5. No equality h^-=3, fixed-symplectic-form compatibility, or completeness of the almost-complex moduli description is needed or established.

## Computational cross-check

The separately authored `check_algebra.py` verifies the general cutoff Gram identities, decomposability and conjugate-volume identities, the core matrix equation J^2=-Id, anti-invariance of alpha and beta_epsilon, and the coordinate Nijenhuis component. All assertions passed with exact symbolic algebra. These checks corroborate the written derivation; they do not replace the global geometric arguments above.

## Final assessment

The exact frozen proof supplies a compact connected smooth counterexample to the specified integrability implication. The compactness, global form classes, pointwise almost-complex structure, smooth gluing, and nonintegrability are all accounted for. This audit found no unresolved mathematical gap and requires no patch. Any claim of historical novelty remains a separate literature question.
