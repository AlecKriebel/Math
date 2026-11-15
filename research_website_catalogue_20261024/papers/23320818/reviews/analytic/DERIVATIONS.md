# Final analytic derivations and source-interface closure

The complete independent reconstruction is preserved in INITIAL_RECONSTRUCTION.md, sealed before foreign bodies, supplied code/data/inventory or scientific opinions. This final document completes its explicit source/category gaps and gives a checkable standalone proof chain. Record23320818, version1.0, declared12October2026, actual6-page PDF and controlling20223-byte TeX are unchanged.

## 1. Exact geometric and test universe

Fix a>0. The completed smooth manifold is R_t×{x∈R³:ρ=|x|≥a}; its boundary is R×S_a, retained as a sphere, and φ=1−a/ρ. Test vectors are every compactly supported smooth section of its tangent bundle, including nonzero normal traces. This is not the space of boundary-tangent vectors, nor independently smooth lowered covectors, nor vectors smooth after collapsing the sphere to a point. The initial coordinate attack r=(ρ−a)²/ρ, dr/dρ→0, was valid as a warning against silently changing test completions, but it does not refute the paper's actual primary interface: BKTZ explicitly first changes from area-radius coordinates to the spatially conformally flatρ boundary structure before defining its tests.

BKTZ arXiv1901.00813v3, printed pp.4–6, §1.3 equations1.8–1.11 and §1.4 equations1.19–1.21, explicitly uses this exterior-ball blow-up. Printed p.9 Definition2.1 uses ψ∈X_c(overline M) in spatially conformally flat(t,ρ,θ,ϕ) coordinates, with boundary approximants R×∂B_(ρ0+ε). The boundary-support footnote to Theorem1.1 on p.6 explicitly permits support at the inner boundary. Its p.9 equation2.5 explicitly permits a nonzero angular-independent radial trace. Thus η(t)χ(ρ)∂ρ used below is within the stated primary test convention. The angular-independent restriction in its theorem is described there as unnecessary; even restricting to that convenient subclass would not remove the counterexample test. The target's all-vector convergence is proved directly, not imported from the sufficient theorem.

## 2. Curvature without the supplied areal-Christoffel computation

For h=φ⁴δ, dimension3 conformal curvature gives

    Ric(h)_ij=−2φ⁻¹φ_ij+6φ⁻²φ_iφ_j
              −2(φ⁻¹Δφ+φ⁻²|dφ|²)δij.

Here φ_i=a n_i/ρ², φ_ij=a(δij−3n_i n_j)/ρ³ and Δφ=0. Raising with h, its radial/tangential eigenvalues simplify to

    Rr=φ⁻⁴(−2φ″/φ+4(φ′/φ)²)=4a/(ρ³φ⁶),
    RT=φ⁻⁴(−2φ′/(ρφ)−2(φ′/φ)²)=−2a/(ρ³φ⁶).

Hence Rh=Rr+2RT=0. For a radial scalaru the mixed Hessian eigenvalues, derived from the conformal spatial connection, are

    Hr(u)=φ⁻⁴(u″−2φ′u′/φ),
    HT(u)=φ⁻⁴(u′/ρ+2φ′u′/φ).

With q=(ρ+a)/(ρ−a), direct differentiation yields Hess_hq=q Ric(h) and Δ_hq=0. For N=A+Bq, A,B≥0,A+B>0, N>0 on the interior and Hess_hN=Bq Ric(h), Δ_hN=0. The static metric gN=−N²dt²+h has

    Ric_tt=NΔ_hN=0, Ric_ti=0,
    Ric_ij=Ric(h)_ij−N⁻¹Hess_hN_ij,

and scalar curvature0. Its mixed Einstein tensor has zero time row/column and spatial eigenvalues (A/N)(4a,−2a,−2a)/(ρ³φ⁶). All denominator manipulations are onρ>a and N>0, so no boundary value of the degenerate metric is assigned. At A=B=1/2, N=(1+q)/2=φ⁻¹ and

    G^μ_ν=diag(0,2a,−a,−a)/(ρ³φ⁵).

Because Rg=0, Ric_μνRic^μν=6a²/(ρ⁶φ¹⁰), which diverges to positive infinity. For x=ρ−a, x⁵G^ρ_ρ→2a³ and x¹⁰Ric²→6a⁶. In a static orthonormal frame energy density is0, while angular pressure is−a/(8πρ³φ⁵). The frame vector(1,0,1,0) is null and has negative T(k,k), proving NEC violation. This is a geometric effective tensor, not a solution supplied for a specified matter theory.

DKMV gr-qc/0109069v1, printed pp.3–4, equations9–15, supplies the old Einstein/stress tensor and affine-lapse metric. Its isotropic equation15 under (m,rbar,κ,λ)=(−2a,ρ,A,B) is exactly gN. Its equations10–11 give radial/angular stresses in the ratio−2:1, becoming the displayed mixed G after m=−2a and multiplying by8π. Its subsequent paragraph explicitly takes m>0 for the wormhole classification. The target properly claims the negative-mass application of the existing formula, not coverage by that positive-mass classification or a new metric/tensor.

## 3. Full contraction, all-test absolute convergence and exact distributional functional

Since dV=Nφ⁶dt d³x, define the spatial tensor density

    D^i_j=Nφ⁶G^i_j=Aaρ⁻³(6n_i n_j−2δij).

It is symmetric, traceless and smooth up toρ=a. Its radial/tangential eigenvalues are Dr=4Aa/ρ³ and DT=−2Aa/ρ³. The spatial connection is

    Γ^j_ik=2φ⁻¹(δ_i^jφ_k+δ_k^jφ_i−δikφ_j).

Consequently D^i_jΓ^j_ik=2φ⁻¹((trD)φ_k+D^i_kφ_i−D^k_jφ_j)=0 exactly. Γ^j_it=0, and the time row/column of G vanish. Thus the pointwise scalar-density on the smooth interior is

    G^μ_ν∇_μψ^ν dV = D^i_j∂_iψ^j dt d³x.                 (D1)

This combines finitely many ordinary smooth terms BEFORE integrating. It neither integrates divergent summands separately nor uses a principal value, curvature-distribution multiplication or singular metric lowering of an unrelated covector test.

For A≥0, |D|_F=√24 Aa/ρ³≤√24 A/a². If K is the compact support ofψ, its Euclidean spacetime measure is finite and its Cartesian first derivatives are bounded. Hence

    ∫|G^μ_ν∇_μψ^ν|dV
      ≤(√24 A/a²) Vol_E(K) sup_K|∂ψ|_F <∞.                 (D2)

This proves the universal absolute-integrability quantifier for arbitrary time/angular dependence, avoiding spherical pole coordinates. At A=0 it is identically0. The volume is positive on the interior, so the absolute scalar integral is exactly the absolute value of the density in(D1), not an informal signed cancellation of two infinite integrals.

The Euclidean divergence is

    ∂_iD^i_j=[Dr′+2(Dr−DT)/ρ]n_j=0.

On a+ε<ρ<R, with time endpoints/R outside support, integrate(D1) by parts. The inner outward normal of that exterior domain is−n, giving

    I_ε=−4Aa/(a+ε)³ ∫R×S_(a+ε)ψ_spatial·n dt dA_E.

Absolute convergence(D2) and smooth trace convergence give

    I_gN(ψ)=−4A/a² ∫R×S_a ψ_spatial·n dt dA_E.             (D3)

Equivalently the densitized functional is a boundary-supported normal trace, of order0 in the test trace. All interior-supported and boundary-tangent tests give0. The distributional expression depends on this declared completed-manifold test class; it is not changed by a merely interior coordinate transformation to a different smooth boundary structure.

Take a smooth compactly supportedη with∫ηdt=1 and a smooth one-sided cutoffχ equal1 near a and zero beyond a finite radius. Such standard smooth cutoffs exist. The vectorηχ∂ρ is smooth at the retained sphere because∂ρ=x^i∂_xi/ρ and a>0. Formula(D3) gives−16πA; at A=B=1/2 this is−8π. Independently its full radial/angular density is4Aaη∂ρ(χ/ρ)dt dρdΩ; integration of the compactly supported derivative gives the same negative sign. Thus the homogeneous identity for ALL declared tests holds in this family iff A=0. The B=0,A>0 endpoint is included, even though its individual curvature components diverge faster; the densitized cancellation still applies. A=0,B>0 is the negative-mass Schwarzschild vacuum control after time rescaling.

BKTZ p.9 Definition2.1 and pp.10–11 flux calculation have precisely the same interior/boundary functional architecture and inner-boundary sign. The target does not invoke their Theorem1.1 to prove this borderline case: its hypothesis(iii) is strictly O((ρ−ρ0)^(−5+κ)), κ>0, whereas here x⁵G^ρ_ρ→2a³≠0. This exact primary comparison closes the initial borderline-order concern.

## 4. ZAS, mass, causality and slice boundaries

The conformal resolution(δ,φ) is globally smooth at the retained sphere, has a simple zero with derivative1/a into the exterior, and is harmonic. BJ0909.0522v2 printed p.5 Definition4 requires areas of every sequence of boundary graphs converging in C¹ to tend0; pp.6–7 Definitions6–7 require exactly the smooth positive resolution/simple zero/harmonicity stated here. Such graph families have bounded Euclidean area; supφ⁴→0 on them, so their h-area vanishes. This proves the actual approaching-surface condition, not just a spherical example. Printed p.8 Definition10 has inward-to-manifold normal and regular mass

    −1/4((1/π)∫S_a(νφ)^(4/3)dA_δ)^(3/2)=−2a.

The scalar curvature is0 and the exterior asymptotic expansion has the required differentiated O(1/ρ) decay; the lapse is1+O(1/ρ). The spatial metric is independent of t, shift is0, so every natural static slice has K=0. BJ printed p.3 explicitly restricts to time-symmetric/totally-geodesic spacelike slices and §6.6,p.32 describes arbitrary-spacelike extensions as a separate desired development.

For the main lapse define s=∫a^ρφ³du. Then g_rad=φ⁻²(−dt²+ds²), s∼(ρ−a)⁴/(4a³), and the limiting conformal cylinder s=0 is timelike. Nearby constantρ tubes also have Lorentzian induced metric/spacelike normal. With conserved E=φ⁻²dt/dλ>0, nullness gives |dρ/dλ|=E/φ. Remaining affine length is(ρ−a−a log(ρ/a))/E∼(ρ−a)²/(2aE), finite at the invariant curvature blow-up. No smooth nondegenerate extension of the physical four-metric is claimed.

For the uniform tilt t=t0+q_tilt s, |q_tilt|<1, the smooth resolved radial coefficient is1−q_tilt², and the regular mass is−2a/(1−q_tilt²). For the nearly-null tilt u′=φ³√(1−φ²), induced radial coefficient isφ⁶ while tangential coefficients scaleφ⁴; division by any simple defining factor to the fourth power leaves radial degeneracy. An all-arbitrary-tilted-slice regularity assertion would therefore be false, and is explicitly not the target's claim.

## 5. Exact conjecture application and source limits

The actual Burtscher contribution in the published OWR40/2021, printed pp.2231–2233, was read completely. It separates geometric admissibility(i), the static/spherical weak-identity result(ii), and matter-field investigation(iii). Its geometric criterion is regular negative-mass ZAS slice data in the Bray–Jauregui framework; its stated conjecture at p.2233 concerns all admissible timelike singularities. No NEC or specified electromagnetic model is imposed as a hypothesis of that geometric conjecture. The report does not formally settle every nonsymmetric/all-tilted-slices interpretation. The target accurately announces and uses its natural static-foliation/BKTZ test interpretation and explicitly excludes those stronger readings and the wider matter/evolution programme. The counterexample application is supported at exactly that stated interpretation; it must not be promoted as refuting every stronger or differently completed conjecture formulation.

The metric/tensor, negative-mass spatial example, flux method and regular-mass definitions are all credited. This audit authenticates those actual mathematical interfaces; it does not certify historical first priority or current worldwide openness and recommends no follow-up question. None of the initial eight routes is now blocked by an unsupported equivalent central assertion. The exact remaining qualifications are the written source-scope/energy/test/slice/priority boundaries, not a replacement theorem or attempted repair.
