# Turn 5: an explicit higher-order augmentation and the final source gap

**Unreviewed scoped partial. Five substantive author turns are complete; the original unspecified adaptive procedure remains unresolved.**

The final route constructs a computable flux upper estimator with the classical mixed tangential terms and an explicit higher-order coarse contribution. It proves convergence of that estimator for the fixed-delta reconstructed algorithm from Turn4. The resulting expression resembles the source's verbal description, but that resemblance is not evidence that it is the unprinted original estimator or that its intended marking policy is equivalent.

## 1. Model and estimator

Restrict here to a bounded convex polygon Omega in R², A=I, homogeneous Dirichlet data and f in L2. The fine space is RT0 on a shape-regular triangulation T_h, with Q_h=P0(T_h) and L2 projection P_h. The primary solution u_H is the conforming P1 Galerkin solution on a possibly different shape-regular triangulation H_H. No relation between these meshes is required for the bound in this turn. Delta is any positive number; the estimates explicitly retain its dependence.

Let sigma=-grad u and sigma_h solve the source-supported hybrid equation. Let eta_h be the all-edge tangential indicator from Turn2 and osc_h=||h(f-P_h f)||_0. Define the higher-order primary residual

    rho_H,2²=sum_(K in H_H) H_K^4 ||f||_K²
              +sum_(E interior in H_H) H_E^3
                         ||[grad u_H dot n_E]||_E².        (1.1)

It is computable from the existing primary solve and f. If rho_H denotes the usual primary energy residual from Turn4, then

    rho_H,2<=H_max*rho_H.                                 (1.2)

This exact extra mesh factor is the sense of higher order used here. A universal approximation rate is not assumed.

There are constants C_eta,C_osc,C_dual,C_R depending on the domain and shape regularity, independent of h,H and delta, such that

    ||sigma-sigma_h||_0
      <= C_eta*(1+sqrt(delta)*C_R)*eta_h
          +C_osc*osc_h+sqrt(delta)*C_dual*rho_H,2.          (1.3)

Also eta_h<=C_eff||sigma-sigma_h||_0. No uniform efficiency of the entire coarse-augmented quantity relative to flux error alone is claimed: the separately computed primary residual may overestimate its actual effect on the flux.

## 2. Compare the recovered scalar with the Helmholtz potential

Take the orthogonal L2 decomposition

    sigma_h=-grad w+xi,       w in H0^1,       div xi=0.

The planar tangential argument already proved in Turn2 gives

    ||xi||_0<=C_eta*eta_h.                                 (2.1)

Define the exact recovered scalar

    q_h=P_h u_H+delta^-1(P_h f-div sigma_h).

It satisfies (sigma_h,tau_h)=(q_h,div tau_h) for every tau_h in RT0. Integration by parts for w gives

    (q_h-P_h w,div tau_h)=(xi,tau_h).                      (2.2)

Let epsilon_h=q_h-P_h w, which belongs to Q_h. The uniform minimum-norm divergence lift from Turn3, available on the convex domain, supplies R_h epsilon_h with divergence epsilon_h and norm at most C_R||epsilon_h||_0. Testing(2.2) with that lift gives

    ||epsilon_h||_0<=C_R||xi||_0.                          (2.3)

This controls q_h relative to the continuous gradient potential w associated with the computed flux. It does not assume that either q_h or w already approximates the exact primary solution.

## 3. Positive projected-reaction estimate, without a small-delta assumption

Since div xi=0, the second mixed equation gives

    -Delta w+delta*P_h w
       =P_h f+delta*P_h u_H-delta*epsilon_h.

Subtract the exact Poisson equation, after adding delta*P_h u on both sides. For e=w-u in H0^1,

    -Delta e+delta*P_h e
       =(P_h f-f)+delta*P_h(u_H-u)-delta*epsilon_h.         (3.1)

Test with e. The left side is

    E²=||grad e||_0²+delta*||P_h e||_0².

Element-mean subtraction bounds the first right-hand term by C_osc*osc_h*||grad e||_0. The other two pair with P_h e, since their factors belong to Q_h. Cauchy-Schwarz consequently gives

    E<=C_osc*osc_h+sqrt(delta)*(||u_H-u||_0+||epsilon_h||_0).

The flux error has orthogonal gradient and divergence-free parts:

    ||sigma-sigma_h||_0²=||grad e||_0²+||xi||_0².

Combining this identity with(2.1)-(2.3) yields

    ||sigma-sigma_h||_0
      <=C_eta*(1+sqrt(delta)*C_R)*eta_h
          +C_osc*osc_h+sqrt(delta)*||u_H-u||_0.             (3.2)

No coefficient is absorbed by requiring delta to be small. Positivity of the orthogonal projection is the crucial step. In particular, no term proportional to the unknown flux error remains on the right.

## 4. Computable bound on the coarse L2 error

Convex-polygon Dirichlet regularity gives the dual bound: if -Delta z=g with z in H0^1 and g in L2, then z is in H2 and ||z||_H2<=C_dual||g||_0. This is a classical input, checked in Guermond's scalar elliptic notes, Chapter27, Theorem27.26, citing Grisvard. It is not being asserted on arbitrary nonconvex polygons.

Take g=u-u_H. In two dimensions z in H2 is continuous, so its nodal P1 interpolant I_H z is well defined and has the correct zero boundary values. Galerkin orthogonality and integration by parts yield

    ||u-u_H||_0²
       =sum_K(f,z-I_H z)_K
          -sum_(E interior)([grad u_H dot n_E],z-I_H z)_E.

The local interpolation/trace estimates have orders H_K² in cell L2 and H_E^(3/2) in edge L2. Summing by Cauchy-Schwarz and patch overlap gives

    ||u-u_H||_0²<=C*rho_H,2*||z||_H2
                  <=C_dual*rho_H,2*||u-u_H||_0.

Cancellation proves ||u-u_H||_0<=C_dual*rho_H,2. Substitution into(3.2) proves(1.3). The edge-bubble argument from Turn2 proves the stated efficiency of eta_h alone. It does not prove efficiency of every summand in(1.3) relative to flux error.

## 5. Estimator convergence for the specified fixed-delta algorithm

On a convex polygon, the algorithm in Turn4 has rho_H,l->0 and eta_h,l->0. Its overlay gives osc_h,l<=rho_H,l. Since H_max is bounded by the domain diameter, (1.2) implies rho_H,l,2->0. With fixed delta the entire right side of(1.3) tends to zero.

Thus that reconstructed algorithm has both flux convergence and convergence of this explicit augmented flux upper estimator. The proof does not assume that independently small observed indicators identify the right PDE: the positivity argument proves reliability, and the algorithm proves that its terms vanish. No data-oscillation or hidden conservation term has been dropped.

This also calibrates Turn1's failure example. There the coarse space remains zero and delta is fixed; refining only the fine mesh makes the tangential indicator and the h-weighted ordinary divergence residual small, but does not make the coarse residual(1.1) vanish. The extra term correctly prevents the reconstructed upper estimator from falsely certifying convergence. That example still says nothing negative about the source's explicitly augmented, but unprinted, estimator.

## 6. Final source comparison and outcome

The official OWR paragraph specifies the two-stage method, announces an efficient/reliable flux estimator with mixed-method terms and extra higher-order terms, and asks about convergence of an adaptive procedure. It prints neither that estimator nor a marking/coupling/parameter algorithm. The full cited KLS journal paper supplies the correct fine variational equation and a primary-gradient recovery estimator; it does not provide the missing local flux estimator or adaptive procedure. The additional primary2024 paper credits the Uzawa interpretation, and the accessible2026 reduced-mixed preview describes another adaptive iteration without furnishing an inspected exact-equivalence theorem.

The five-turn work has now supplied two explicit convergent variants and, here, an explicit estimator of the indicated general structure. It has not established that the historical source estimator equals this expression, that its intended markings enforce our separate primary/fine requirements, or that the full source generality is covered. Three dimensions, higher-order spaces, general coefficients, nonhomogeneous data, arbitrary adaptive couplings, parameter policies, and inexact solves remain outside these proofs as detailed in the earlier turns.

The proper final disposition is therefore **original target unsolved, 5/5 substantive author turns**, with these scoped results retained for independent review. This is not a claim that every possible interpretation of the open-ended source is false or still historically open, and it is not a novelty assertion. No sixth proof-search turn will be used to silently fill the remaining original-equivalence gap.
