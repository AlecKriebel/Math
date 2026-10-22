# Turn 2: conservation correction, a reliable augmentation, and a conditional marking transfer

**Unreviewed scoped partial results. The original adaptive convergence question remains unresolved.** The exact OWR higher-order estimator terms and two-mesh refinement rule are still unavailable. This turn derives conditions for an explicitly reconstructed variant; it does not identify that variant with the original procedure.

The Schur-complement and Uzawa interpretation is classical. In particular, Adhikari–Kim–Lee–Sheen, DOI10.1002/num.23120 (2024), section3.2, already identifies the hybrid solve with a single augmented-Lagrangian Uzawa step, recovers the scalar, and bounds its pressure error using the least Schur eigenvalue. Its section4 analyzes the small-parameter flux error. Those inputs and the original KLS method are credited, rather than claimed as discoveries. The additional primary lead DOI10.1016/j.cam.2026.117609 describes a related iterative reduced-mixed adaptive algorithm; only its public abstract and introduction were accessed, so no theorem from its unavailable full text is used below.

## 1. Exact distance to the conservative mixed flux

Use the homogeneous Dirichlet setup and signs of TURN_1. On a fixed finite flux space V, equip V with the inner product

    m(v,w)=(A^-1 v,w),

and Q=div V with its L2 inner product. Let D:V->Q be divergence, let G:Q->V be its adjoint for these two inner products, and put S=DG. Since D is onto Q by definition, G is injective and S is positive definite. The zero-dimensional Q case is trivial and can be omitted. These definitions avoid treating nonorthonormal finite-element coefficients as Euclidean L2 coordinates.

Write F=P_Q f, c=P_Q u_H. The hybrid solution and recovered scalar satisfy

    sigma_delta=G q_delta,  (S+delta I)q_delta=F+delta c.

The conservative mixed solution is

    p_M=S^-1 F,    sigma_M=G p_M.

Thus, with the computed defect d=D sigma_delta-F,

    q_delta-p_M=delta(S+delta I)^-1(c-p_M),
    d=delta(c-q_delta),
    sigma_delta-sigma_M=R d,       R=G S^-1.                 (1.1)

R d is the unique minimum-m-norm flux with divergence d. Indeed D R d=d, R d belongs to range G=(ker D)^perp_m, and every other lift differs by a member of ker D. Consequently

    chi² := ||sigma_delta-sigma_M||_m² = (S^-1 d,d),          (1.2)
    chi = sup_(v in Q, v!=0) |(d,v)| / ||Gv||_m.             (1.3)

The supremum identity follows by writing (d,v)=m(Rd,Gv), and taking v=S^-1d. Formula(1.2) is an exact certificate but requires a global Schur solve; it is not advertised as a free local estimator.

If ||Gv||_m >= beta ||v||_0, then

    chi <= beta^-1 ||d||_0.                                 (1.4)

For arbitrary V this beta can depend badly on the space. Uniformity is an extra hypothesis, available for the usual stable RT/BDM families with the appropriate boundary conditions; it is not a consequence of coercivity of the fixed-delta hybrid solve.

## 2. Uniform parameter control and its limits

Diagonalizing the positive self-adjoint S gives

    chi <= min{delta/beta, sqrt(delta)/2} ||c-p_M||_0,
    ||d||_0 <= delta ||c-p_M||_0,
    ||p_M||_0 <= beta^-2 ||F||_0.                            (2.1)

For the first inequality, each scalar multiplier is delta*sqrt(lambda)/(lambda+delta), at most delta/beta when lambda>=beta², and at most sqrt(delta)/2 because (lambda-delta)²>=0. For the second, the multiplier for d is delta*lambda/(lambda+delta)<=delta. These estimates include the small-delta singular limit without using a degenerating H(div) coercivity constant.

For a mesh sequence with uniform beta>0 and bounded coarse inputs ||u_H||_0, delta_l->0 therefore implies

    ||sigma_delta_l-sigma_M_l||_m + ||div(sigma_delta_l-sigma_M_l)||_0 ->0.  (2.2)

If the conservative mixed sequence converges to the true flux, so does this hybrid sequence. This is a conditional transfer, not a proof that the source's adaptive sequence has that property. It is also consistent with the known reduced-mixed strategy: small delta can remove coarse-input bias, at the cost of a more ill-conditioned algebraic system. No computational-complexity conclusion follows.

## 3. An explicit reliable flux estimator in a restricted planar model

Here restrict to A=I, a bounded simply connected polygon Omega, homogeneous Dirichlet data, a conforming shape-regular triangular mesh, and V=RT0. Let P be the cellwise constant L2 projection. Let sigma=-grad u be the true flux, sigma_h the hybrid flux, and

    d=div sigma_h-P f,
    osc=||h(f-P f)||_0.

For every interior edge E fix a unit tangent and let j_E be the tangential jump of sigma_h in that orientation; on a boundary edge let j_E=sigma_h dot t_E. Define

    eta²=sum_(all edges E) h_E ||j_E||_(0,E)².               (3.1)

Boundary edges are included. Define ||r||_-1 as the dual norm against H0^1(Omega) with gradient norm. Then constants depending only on the domain and shape regularity satisfy

    ||sigma-sigma_h||_0 <= C(eta+osc+||d||_-1),              (3.2)
    eta+||d||_-1 <= C(||sigma-sigma_h||_0+osc).              (3.3)

In particular eta+osc+C_P||d||_0 is a computable reliable upper estimator. The L2 substitution can overestimate the error; no uniform efficiency claim is made for that substitution.

Proof of reliability. Put e=sigma-sigma_h and r=f-div sigma_h=(f-P f)-d. Solve -Delta z=r in H0^1, and decompose

    e=-grad z+w,      div w=0,
    ||e||_0²=||grad z||_0²+||w||_0².

The orthogonality follows by integration against H0^1. Subtracting element means of a test function and applying the element Poincare inequality gives

    ||grad z||_0=||r||_-1 <= C osc+||d||_-1.                 (3.4)

On the simply connected polygon the divergence-free L2 field w has a stream function psi in H1 with w=curl psi and ||grad psi||_0=||w||_0. The true Dirichlet gradient is orthogonal to every such curl. The hybrid equation gives (sigma_h,tau_h)=0 whenever div tau_h=0. For a continuous piecewise linear quasi-interpolant I_h psi, curl I_h psi is in RT0 and has divergence0. Hence

    ||w||_0²=(e,w)=-(sigma_h,curl(psi-I_h psi)).

Elementwise curl sigma_h is zero for RT0. Integration by parts leaves the interior jumps and the boundary terms in(3.1). The standard local H1 quasi-interpolation trace estimate is

    sum_E h_E^-1 ||psi-I_h psi||_(0,E)² <= C ||grad psi||_0².

Cauchy-Schwarz therefore gives ||w||_0<=C eta, proving(3.2). The stream-function representation, local quasi-interpolant and trace inequality are standard planar Helmholtz/finite-element inputs. Multiply connected domains or general coefficients require extra work and are not covered by this particular proof.

Proof of the converse estimate. For each edge use a scalar polynomial edge-bubble extension of j_E, supported on its one- or two-element patch. Its trace pairing with j_E is comparable to ||j_E||_E² and its gradient norm is at most C h_E^-1/2 ||j_E||_E. Since curl sigma_h=0 elementwise and the exact Dirichlet gradient is orthogonal to curls (including boundary-supported tests), integration by parts yields

    h_E^1/2 ||j_E||_E <= C ||e||_(patch E).

Finite patch overlap gives eta<=C||e||_0. Also d=(f-Pf)-div e, so

    ||d||_-1 <= C osc+||e||_0.

This proves(3.3). Thus the nonlocal negative norm of the conservation defect is the precise additional consistency quantity in this restricted setting. It is not legitimate to replace it by h||d|| merely because a mesh is fine: the turn1 example rules out that substitution in general. The computable L2 upper bound has no mesh factor for the same reason.

## 4. Quantitative Dörfler marking transfer

This section is an abstract, conditional algorithm theorem. It is intentionally separate from the unrecovered original marking rule.

Suppose a chosen residual indicator has a vector of local components eta(v), with nonnegative entries and Euclidean subset norms. Suppose on each common mesh

    |eta(v;M)-eta(w;M)| <= L ||v-w||_m                      (4.1)

for every index subset M, with one mesh-independent L. Such bounds follow from inverse/trace estimates for fixed-order curl/jump residuals with aligned piecewise constant coefficients. In the restricted RT0 model of section3 they apply to(3.1). Let epsilon be a certified upper bound for chi, for example beta^-1||d||_0. Choose 0<theta<1 and kappa>0 with L*kappa<sqrt(theta). Assume that the parameter is selected so that

    epsilon <= kappa eta(sigma_delta),                     (4.2)

and mark a set M satisfying eta(sigma_delta;M)>=sqrt(theta)eta(sigma_delta). Then the same set satisfies conservative mixed Dörfler marking with

    eta(sigma_M;M) >= sqrt(theta_*) eta(sigma_M),
    theta_* = [(sqrt(theta)-L*kappa)/(1+L*kappa)]² >0.       (4.3)

Indeed the left side is at least (sqrt(theta)-L*kappa)eta(sigma_delta), whereas eta(sigma_M)<= (1+L*kappa)eta(sigma_delta). No equality of the two fluxes or residual vectors is assumed.

For a fixed mesh, fixed finite input c, and eta(sigma_M)>0, repeatedly halving delta eventually enforces(4.2), because(2.1) makes epsilon->0 and(4.1) makes eta(sigma_delta)->eta(sigma_M). If eta(sigma_M)=0, this argument does not prove termination. A zero-estimator/data-oscillation branch must be specified and analyzed; silently assuming termination would be a gap.

Now assume all of the following for a reconstructed algorithm:

1. The parameter test terminates on every visited mesh and(4.2) holds.
2. The mesh/refinement and data-reduction rules, together with the conservative bulk condition(4.3), satisfy a valid mixed-method convergence theorem, yielding sigma_M,l->sigma and eta(sigma_M,l)->0.
3. Constants in(4.1) and the certified bound epsilon>=chi are uniform.

Then its hybrid outputs converge to sigma. Indeed

    eta(sigma_delta) <= eta(sigma_M)+L*chi
                     <= eta(sigma_M)+L*kappa*eta(sigma_delta),

so eta(sigma_delta)<=eta(sigma_M)/(1-L*kappa)->0, and chi<=kappa eta(sigma_delta)->0. The triangle inequality completes the proof. Carstensen–Hoppe's 2006 error-reduction framework motivates assumption2, with its own RT0/model, refinement and data-oscillation requirements. A bare citation does not establish those requirements for the OWR two-mesh scheme.

This theorem supplies exact tolerance and bulk-loss constants, but not a complete original algorithm. It leaves both the source-estimator identification and the zero-indicator/data branch open. It makes no optimality or work estimate.

## 5. Turn2 disposition

The recovered hybrid flux is an exact nonconservative mixed flux whose distance to the conservative solution is a minimum-norm divergence lift. In the stated planar RT0 model, a negative-norm conservation augmentation gives a rigorous reliable and efficient flux bound up to data oscillation, with a cheaper reliable L2 replacement. A computable small-defect test transfers bulk marking quantitatively; conditional mixed convergence then transfers to the hybrid outputs. These are scoped partials and classical-method consequences, not a certification of the missing original adaptive procedure.

Two substantive turns are complete. The original question remains unresolved. Estimated completion30%.
