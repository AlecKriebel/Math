# Independent adversarial derivations: record 23320818

UTC: 2026-11-15T00:06:25.225805+00:00. Completion estimate: 92% of assigned review; scientific checks complete, packet sealing pending.

## 1. Claim under examination and source interface
The quantified claim is the published Theorem1 and Proposition1, on the retained-cylinder smooth structure R times {rho>=a}, a>0, with compactly supported smooth VECTOR sections allowed a nonzero normal boundary trace. It is not an identity for independent covectors, tests on a collapsed-origin smooth structure, or arbitrary tilted-slice regularity. No matter model or energy condition is assumed. These are the actual stated hypotheses, not a repair proposed by this review.

The source interfaces were checked in raw primary text only after the independent initial seal. BKTZ Section1.3 explicitly uses a conformally flat coordinate blow-up to a sphere boundary. Definition2.1 uses G^mu_nu nabla_mu psi^nu, and Theorem1.1's footnote3 expressly permits support on the inner boundary. Equation2.5 retains the normal radial value at that boundary; footnote7 says its convenient angular-independence restriction is unnecessary. Therefore the published radial test is admissible in that identified static boundary convention. The sufficient BKTZ theorem's improved exponent kappa>0 is absent here; the target correctly does not invoke that theorem to prove this borderline case.

The entire scientific body of Burtscher's report describes admissibility by regular negative-mass ZAS on spacelike slices and proposes the homogeneous identity for admissible timelike singularities. It does not formally quantify over every possible tilted hypersurface or impose a specified matter model/NEC. BJ expressly works with time-symmetric slices and discusses arbitrary-spacelike-slice theory as a separate extension. The target states its static-foliation interpretation, and proves a result in this meaningful framework. Neither this review nor the manuscript establishes a conclusion for every possible stronger formalization of the short report.

## 2. Independent curvature route
The new read-only verifier starts from the unrestricted three-function spherical metric
  g=diag(-U(rho)^2,V(rho)^2,W(rho)^2,W(rho)^2 sin(theta)^2).
It forms every Christoffel symbol, all16 Ricci entries with the exact published sign convention, the scalar, and mixed Einstein matrix BEFORE inserting U=N=A+B(rho+a)/(rho-a), V=phi², W=rho phi². The resulting all-parameter identities are
  R=0,
  G^t_t=0,
  (G^rho_rho,G^theta_theta,G^varphi_varphi)
   = A/N * (4a,-2a,-2a)/(rho³ phi^6),
with every off-diagonal entry zero. This independently checks the areal/static-lapse deduction rather than importing it. A=0 gives every Einstein component zero; B=0 leaves the claimed nonvacuum constant-lapse tensor. The main N=phi^{-1} at A=B=1/2 gives the published tensor and
  Ric_{mu nu}Ric^{mu nu}=6a²/(rho^6 phi^10).
As x=rho-a decreases to zero, x^5G^rho_rho ->2a³ and x^10 Ric² ->6a^6>0. Thus a coordinate singularity or R=0 cannot explain away the end: an invariant diverges. The generic derived expressions and all check counts are in INDEPENDENT_RESULTS.json.

The spatial curvature can also be checked independently from the conformal metric h=phi^4delta, with harmonic phi. Its mixed eigenvalues are (4a,-2a,-2a)/(rho³phi^6), scalar zero. q=(rho+a)/(rho-a) solves Hess_h q=q Ric(h), Delta_h q=0. Linearity in N=A+Bq then yields the same tensor by the static decomposition. This second reasoning agrees with direct four-dimensional curvature, without treating a spatial metric alone as a vacuum spacetime.

## 3. Harmonic-Hessian density and the full test quantifier
Let H(x)=1/rho on rho>a. In exterior Cartesian coordinates,
  D=N phi^6 G_spatial =2Aa Hess_delta H
    =Aa(6x_i x_j/rho^5-2delta_ij/rho³).
This harmonic-potential mechanism provides an independent conceptual derivation of the cancellation. Since Delta H=0, D is symmetric, trace-free, divergence-free, and smooth on a neighborhood of the retained sphere a>0. None of these properties requires a limit of the singular physical metric on the boundary.

For h=phi^4delta,
  Gamma^j_ik=2/phi (delta^j_i phi_k+delta^j_k phi_i-delta_ik phi_j).
For EACH vector component k, the entire connection contraction is
  D^i_j Gamma^j_ik
   =2/phi [tr(D)phi_k+(D^T grad phi)_k-(D grad phi)_k]=0.
The time row and column of G vanish, Gamma^j_it=0 in the static zero-shift chart, and consequently no time-component or time-derivative test term survives. For every smooth four-vector psi,
  (G^mu_nu nabla_mu psi^nu)dV_g
   =D^i_j partial_i psi^j dt d³x.
The new verifier additionally makes the four vector values and all16 first derivatives independent symbols and checks the full spherical contraction before using the global Cartesian expression. Thus the cancellation is not a radial-test sample or an assumption of angular independence.

For any compact support K in the manifold-with-boundary topology, all Cartesian first derivatives of psi are bounded on K. D is bounded there, and the Euclidean volume of K is finite because a>0 and the support is compact in time and space. Hence
  integral |G^mu_nu nabla_mu psi^nu|dV_g
   <=C_K integral_K sum_{i,j}|partial_i psi^j| dt d³x<infinity.
This proves absolute integrability of the FULL ordinary scalar for every test. The relation is pointwise on M before any integration; no principal value, product of distributions, or subtraction of separately divergent integrals occurs. Individual connection summands really may diverge like1/x, but this does not invalidate an integrable finite scalar sum. The definition asks for this full contraction, not separate integrability of each coordinate summand. In the specified mixed-index convention G itself has bounded density near the boundary as well; independently smooth raised-index/covector test spaces cannot be substituted.

## 4. Boundary distribution, orientation, and angular attacks
Divergence-free D gives
  integral D^i_j partial_i psi^j dt d³x
   =lim_epsilon integral_{rho=a+epsilon}(-n_i)D^i_j psi^j dt dA_delta.
The support eliminates all outer and time faces. The exact inner traction is
  -n_iD^i_j=-4Aa n_j/rho³.
Boundary smoothness and finite sphere/time support justify passage to the limit, yielding
  I_gN(psi)=-(4A/a²) integral_{R times S_a}psi_spatial dot n dt dA_delta.
The minus sign is forced by the inner outward normal of an exterior domain, and has also been checked by the radial antiderivative. This functional is an order-zero distribution supported on the retained cylinder. If the smooth density D is extended by zero into rho<a, its Euclidean distributional divergence is +4A/a² n_j delta_{S_a}; the minus of that pairing is I. This is a description of the tensor density and test convention, not a boundary metric extension.

A normalized radial test eta(t)chi(rho)n has integral eta=1 and chi=1 near a. Its trace integral is4pi a², so I=-16pi A, and I=-8pi for A=B=1/2. Directly its full density per dOmega is4Aa eta partial_rho(chi/rho), whose compact-support integral is-4A eta; multiplication by4pi gives the same sign and scale. The dependence on B cancels exactly.

Adversarial traces agree with the universal functional: pure time or tangential boundary vectors give zero; a constant Cartesian vector has zero normal mean; nonconstant angular normal modes with mean zero give zero. For a cutoff vector with boundary value psi=(x1³,0,0), psi dot n=a³ n1^4, and integral n1^4 dOmega=4pi/5, giving I=-16pi A a³/5. This nonradial control is checked exactly in the new verifier. Nonradial/time-dependent compact fields require no extra hypothesis beyond the proven global cancellation.

A=0 implies G=0 and I=0 for every test. For every A>0 the radial test gives a nonzero result, proving the published IF AND ONLY IF statement throughout A,B>=0, A+B>0. The excluded A=B=0 has zero lapse and is not a Lorentzian metric. No uniformity as parameters approach that excluded point is claimed.

## 5. ZAS, mass, causal end, and energy condition
For every a>0, phi vanishes simply precisely on S_a, is positive in the exterior, is harmonic for delta, and its exterior normal derivative is1/a. Thus the smooth resolution (delta,phi) satisfies BJ Definitions6/7. For an arbitrary sequence of C^1-approaching boundary graphs, their Euclidean area densities remain uniformly bounded and sup_surface phi^4 ->0. Therefore area_h<=sup phi^4 area_delta ->0, which proves the FULL BJ Definition4 condition, not just the coordinate-sphere case. The regular mass from Definition10 is
  -1/4 [(1/pi)4pi a²(1/a)^(4/3)]^(3/2)=-2a.
Natural static slices have K=(2N)^{-1}partial_t h=0. At infinity h-delta and the lapse's deviation from1 areO(1/rho), with differentiated decay; R_h=0 meets the spatial AF scalar condition. Matter falloff or a specified physical matter equation is not a hidden hypothesis in this geometric claim.

With areal r=(rho-a)²/rho, dr/d rho=1-a²/rho²>0 inside but vanishes at the boundary. The areal transformation is therefore not a boundary diffeomorphism. It must not be used to identify boundary-smooth normal vector components without their Jacobian. Under a smooth boundary-preserving coordinate change the scalar integral and transported test class are invariant. A singular collapse or r-change can define a different test class, which the paper expressly excludes. Time rescaling transforms A and dt oppositely in the boundary functional; no physical mismatch is introduced by coordinate normalization of the selected test.

For the main metric, radial null motion with E=phi^{-2}dt/dlambda>0 obeys |d rho/dlambda|=E/phi. The remaining affine length is E^{-1}(rho-a-a log(rho/a)), of order x²/(2aE), finite. Setting s=int_a^rho phi³ du makes the two-dimensional radial metric phi^{-2}(-dt²+ds²), with finite endpoint s~x^4/(4a³). Thus s=0 is a timelike limiting radial conformal boundary, exactly the qualified assertion. It does not assert a regular four-dimensional conformal extension with nondegenerate angular metric.

An orthonormal angular null vector (1,0,1,0) has G(k,k)=-a/(rho³phi^5)<0 and T(k,k)=G(k,k)/(8pi)<0. The radial null direction has positive contraction; a radial-only energy check would miss the NEC violation. The published violation is correct and already excludes energy-constrained/matter-specific conclusions.

For constant tilt coefficient b with |b|<1, t=t0+b*s gives induced metric phi^4[(1-b²)d rho²+rho²dOmega²]. The resolution normal derivative is1/[a sqrt(1-b²)], while boundary resolution area is4pi a²; the mass is-2a/(1-b²). These local tilted metrics need not furnish globally AF slices, and the paper describes them locally. The nearly null tilt u'=phi³ sqrt(1-phi²) instead has radial induced coefficient phi^6. Any simple smooth defining factor is c*x+O(x²) with c!=0, so dividing by its fourth power leaves a radial coefficient of order x² and a degenerate resolution. This confirms the explicit limitation against arbitrary tilted slices, rather than silently extending the theorem to them.

## 6. Reproducibility, provenance, and conclusion
The read-only independent verifier passed103 exact symbolic checks, identically under normal and -O modes after excluding only the completion timestamp. It imports no supplied or review helper and writes stdout only. Its universal geometric/analytic conclusions are justified above, not merely inferred from the check count.

The complete supplied runner passed its FULL profile with SymPy1.14.0/mpmath1.3.0. In each normal and optimized mode it reproduced396 geometry controls,1557 curvature controls,2916 direct-connection controls,67 symbolic controls,17 original author Boolean controls, and35 historical independent Boolean controls. Sixteen targeted false claims were specifically rejected in32 normal/optimized executions. The runner has explicit fail-closed external result guards even when an archived final assert is disabled by-O. The13 available frozen files and11 extant references are bound; the unavailable standalone manifest digest remains explicitly UNATTESTED. No verification inference is drawn from that unattested digest.

All181 native ZIP payloads were checked byte-for-byte against frozen extracted objects after execution. Programs that write run receipts were invoked by the supplied runner in temporary private copies under this lane. No source/native object, other review packet, site, Sheet, Git reference, release, or external communication was changed. Historical metric/tensor priority is correctly assigned to DKMV's formulas; its later parameter classification explicitly assumes m>0, so the negative-mass application is not falsely attributed to that classification. The target does not claim global first priority. Wider primary provenance/priority coverage remains the source-owner lane's separate task; no sibling findings were used here.

No counterexample or substantive proof gap was found in the published quantified theorem/proposition. The result must retain its actual static-foliation, retained-sphere, boundary-reaching-vector convention. It is not a result for a stronger all-tilted-slice interpretation, point-collapsed tests, NEC matter, or a specified field theory. These are stated boundaries of the original manuscript, not a newly narrowed replacement result.
