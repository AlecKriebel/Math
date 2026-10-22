# Turn 1: identify the two-stage operator and its consistency gap

**Scoped partial results only. Original adaptive convergence is not proved.**

The recovered source is the coarse-primary/fine-flux Ku–Lee–Sheen method. In OWR p2422 the test-function divergence is missing on the right-hand side; KLS, ESAIM:M2AN51(2017), equation(2.6), gives the correct formula. This turn studies that formula, not an HHO/HDG scheme or the different published dual-first reaction-diffusion method. The arguments below are standard coercive projection and Schur-complement ideas applied to the recovered system; no novelty is claimed.

## 1. Set-up and exact mixed reaction equivalence

For this partial analysis take a bounded Lipschitz domain Omega, homogeneous Dirichlet data, f in L2(Omega), and an essentially bounded symmetric uniformly positive definite matrix A. Let u in H0^1(Omega) solve

    (A grad u,grad v)=(f,v),    v in H0^1(Omega),

and let sigma=-A grad u. Then sigma is in H(div) and div sigma=f.

Let S_H be a conforming primary space and u_H its Galerkin solution. For a finite-dimensional flux space V_h subset H(div), and a **fixed** delta>0, the second step is

    B_delta(sigma_h,tau_h)=(f+delta u_H,div tau_h),              (1.1)
    B_delta(v,w)=(div v,div w)+delta(A^-1 v,w).

This is coercive in H(div) for fixed delta. Put Q_h=div V_h and let P_h be the L2 projection onto Q_h. Define the recovered scalar

    q_h=P_h u_H+delta^-1(P_h f-div sigma_h).                    (1.2)

Then (1.1) is exactly equivalent to

    (A^-1 sigma_h,tau_h)-(q_h,div tau_h)=0,         tau_h in V_h,
    (div sigma_h,v_h)+delta(q_h,v_h)=(f+delta u_H,v_h), v_h in Q_h.  (1.3)

Indeed substituting (1.2) into the first equation gives (1.1), since div tau_h is in Q_h; the second equation is simply (1.2). Conversely (1.3) gives (1.2) and hence (1.1). No identification of q_h with u_H is valid in general.

Thus the fine solve is a mixed discretization of a reaction-diffusion problem with a coarse-solution-dependent right side. Its exact discrete conservation defect relative to the original Poisson problem is

    div sigma_h-P_h f=delta(P_h u_H-q_h).                       (1.4)

The standard mixed Poisson method has zero defect in (1.4). This is one reason why a mixed-method adaptive convergence theorem cannot be imported without controlling the additional term.

## 2. Continuous input map and an exact coarse-data bias

For any q in L2(Omega), let Sigma_delta(q) in H(div) solve

    B_delta(Sigma_delta(q),tau)=(f+delta q,div tau), tau in H(div).

It exists uniquely. Equivalently, let w in H0^1 solve

    (A grad w,grad v)+delta(w,v)=(f+delta q,v), v in H0^1.       (2.1)

Then Sigma_delta(q)=-A grad w. The right side of (2.1) is L2, so div Sigma_delta(q)=f+delta q-delta w is L2. Integration by parts, using w=0 on the boundary, verifies the flux equation, and uniqueness gives the equivalence.

Subtracting the true Poisson equation shows that e=w-u satisfies

    (A grad e,grad v)+delta(e,v)=delta(q-u,v).                   (2.2)

In particular

    Sigma_delta(q)=sigma  if and only if q=u.                  (2.3)

For the nontrivial direction, equality of the fluxes implies grad e=0; e in H0^1 is then0, and (2.2) implies q-u=0 by density of H0^1 in L2. Thus a fixed inaccurate coarse input gives a genuine nonzero fine-limit bias when delta is fixed.

The map is stable. Subtracting two flux equations and testing with their difference yields

    ||Sigma_delta(q)-Sigma_delta(p)||_(B_delta) <= delta ||q-p||_0,
    ||A^-1/2(Sigma_delta(q)-Sigma_delta(p))||_0 <= sqrt(delta)||q-p||_0. (2.4)

The same bounds hold in every fixed discrete flux space. Here the B_delta norm is the square root of B_delta(v,v). These statements are not uniform equivalences to H(div) as delta tends to0.

## 3. Nested two-space sequences are Cauchy, but need not be consistent

Let S_l and V_l be increasing sequences of conforming primary and H(div) flux spaces. Keep delta fixed. Denote the H0^1 energy closure of their primary union by S_infinity and the H(div) closure of their flux union by V_infinity.

The Galerkin projections u_l converge strongly in the energy norm to u_infinity, the energy projection of u onto S_infinity. This follows from nested-space orthogonality:

    ||u_m-u_l||_a²=||u-u_l||_a²-||u-u_m||_a²,     m>=l.

Let z_l be the B_delta projection of Sigma_delta(u_infinity) onto V_l. These projections likewise converge strongly to a limit z_infinity in V_infinity. The actual second-stage solution sigma_l has input u_l, so the discrete version of (2.4) gives

    ||sigma_l-z_l||_(B_delta) <= delta ||u_l-u_infinity||_0 -->0.

Consequently the two-stage sequence is Cauchy and sigma_l converges strongly to z_infinity. Its limiting equation is

    B_delta(z_infinity,tau)=(f+delta u_infinity,div tau), tau in V_infinity. (3.1)

If the relevant exact solutions belong to the two limit spaces, this identifies the correct solution; in particular density of both unions is sufficient. Adaptive meshes, however, need not become globally dense. Establishing that their particular limits are the true solutions requires estimator and marking information. Cauchy convergence alone does not answer the original adaptive question.

## 4. Explicit fine-only refinement obstruction

Take A=I, Omega=(0,1)^2, zero Dirichlet values, and

    u(x,y)=sin(pi x)sin(pi y),       f=2pi² u,       lambda=2pi².

Use the conforming linear space on the mesh of two triangles obtained by one diagonal of the square. Every vertex is on the boundary, so its homogeneous Dirichlet space is {0} and u_H=0. Keep that coarse space fixed, and uniformly refine shape-regular Raviart–Thomas lowest-order flux spaces so their union is dense in H(div).

By (2.1), the limiting scalar and flux are

    w=lambda/(lambda+delta) u,
    sigma_delta=lambda/(lambda+delta) sigma.

Hence

    ||sigma-sigma_h||_0 --> delta/(lambda+delta) ||sigma||_0 >0. (4.1)

This is **not** a counterexample to a specific adaptive rule in the OWR source: no such rule is printed there, and the refinement sequence need not respect any intended two-mesh coupling. It proves only that accurate refinement of the fine solve, without coarse-input or parameter control, is not enough.

## 5. A calibration failure of an unaugmented mixed-flux residual

The same example illustrates why additional terms matter. On the fine triangulation define the explicit residual quantity

    eta_h²=sum_T h_T² ||f-div sigma_h||_(0,T)²
          +sum_T h_T² ||curl sigma_h||_(0,T)²
          +sum_(E interior) h_E ||[sigma_h·t_E]||_(0,E)²
          +sum_(E boundary) h_E ||sigma_h·t_E||_(0,E)².          (5.1)

This is the familiar curl/tangential-jump/residual structure of mixed flux estimators, **without** any coarse-data augmentation. It is defined here explicitly; it is not claimed to be the complete unpublished OWR estimator, which expressly has extra terms.

For the example in section4, eta_h tends to0 while (4.1) is positive. To prove this, the fixed-delta Ritz approximation converges in H(div) to the smooth gradient field sigma_delta, so its divergence residual stays bounded. Multiplication by h makes the first term vanish. A lowest-order RT field has the form a+b x on each triangle, hence has elementwise curl0 when A=I.

For the edge terms, let Pi_h sigma_delta be the standard RT interpolant. Shape regularity, trace/inverse estimates and smoothness give

    edge_residual(sigma_h)
       <= C ||sigma_h-Pi_h sigma_delta||_0 + C h ||sigma_delta||_H1 -->0.

Here edge_residual is the square root of the two edge sums in (5.1). The jump and boundary tangential traces of the smooth exact field sigma_delta vanish: it is globally smooth and is the gradient of a scalar with zero boundary trace. The interpolant error has the standard trace bound, and the discrete difference is bounded by its L2 norm through the inverse trace inequality. Both the Ritz and RT interpolation errors tend to0; the claimed result follows.

Thus the usual residual expression loses its reliability if one silently drops the mixed method's conservation identity. Equation(1.4) identifies the missing consistency information. This calibration does not show that the OWR augmented estimator fails; it explains why its unprinted higher-order terms cannot be ignored.

## 6. First-turn disposition

The exact operator, its reaction-diffusion interpretation, the discrete conservation defect, the fixed-delta Cauchy limit, and the fine-only inconsistency example are now established. None proves convergence of the original adaptive procedure. The remaining tasks are to recover or state and validate the exact additional estimator terms, control the changing coarse input and delta, and identify the estimator-driven limit with the original PDE solution. The published 2024/2026 methods with different solve orders cannot supply those missing steps by name alone.

One substantive turn is complete. The source target remains unresolved, with four turns available and the exact-estimator readiness gap explicit. Estimated completion20%.
