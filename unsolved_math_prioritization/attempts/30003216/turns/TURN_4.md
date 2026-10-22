# Turn 4: fixed-parameter two-mesh convergence with explicit coupling

**Unreviewed scoped theorem. The original unprinted augmented estimator and marking rule remain unresolved.**

This turn removes the vanishing-parameter control used in Turn3. It proves convergence for a different, fully specified variant with fixed delta>0, independent residual marking on the primary mesh, tangential-jump marking on the flux mesh, and a refinement-overlay condition. The original recovered two-stage variational equations are unchanged. The additional estimator/coupling choices are explicit and are not asserted to equal the unpublished OWR procedure.

The proof uses classical conforming residual reliability, nested Galerkin projections, local trace estimates and planar Helmholtz decomposition. The Schur/Uzawa and coarse/fine construction remain credited prior methods. No novelty, rate or optimal complexity is asserted.

## 1. Algorithm and theorem

Let Omega be any bounded simply connected polygon in R², take A=I, zero Dirichlet data and f in L2(Omega). Let u in H0^1 solve -Delta u=f, and sigma=-grad u. Fix delta>0 once for all levels.

Let H_l be a nested conforming primary triangulation and T_l a nested conforming flux triangulation, with T_l refining H_l at each level. Assume uniformly shape-regular refinement rules with finite overlays. They must permit marked primary cells to have all edges bisected and all child diameters at most half the old diameter, and marked flux edges to be bisected at their midpoint. Compatible repeated bisection and additional closure refinements can enforce these requirements. No bound on the amount of refinement is part of this theorem.

Use S_l=P1(H_l) intersect H0^1 and V_l=RT0(T_l), with Q_l=P0(T_l) and L2 projection P_l. Solve exactly

    (grad u_l,grad v)=(f,v),                         v in S_l,
    B_delta(sigma_l,tau)=(f+delta*u_l,div tau),       tau in V_l,
    B_delta(v,w)=(div v,div w)+delta(v,w).           (1.1)

All cross-mesh integrals are exact. Algebraic and quadrature errors are excluded.

The primary residual estimator is

    rho_l²=sum_(K in H_l) H_K²||f||_K²
           +sum_(E interior in H_l) H_E||[grad u_l dot n_E]||_E². (1.2)

Assign half of each interior-edge contribution to each adjacent primary cell. Choose a primary cell set N_l carrying at least theta_p*rho_l² of these cell contributions, where 0<theta_p<1. Refine these cells as specified above, obtaining H_(l+1).

On T_l use the all-edge tangential indicator

    eta_l²=sum_(E interior) h_E||[sigma_l dot t_E]||_E²
           +sum_(E boundary) h_E||sigma_l dot t_E||_E².      (1.3)

Mark flux edges M_l carrying at least theta_f*eta_l², 0<theta_f<1. Form T_(l+1) as a conforming refinement of T_l and H_(l+1), bisecting each marked flux edge. Additional refinements are allowed. Empty marked sets are allowed when the relevant estimator is zero.

**Theorem.** This algorithm is well defined at every finite level and

    ||u_l-u||_H1 ->0,
    ||sigma_l-sigma||_0+||div sigma_l-f||_0 ->0.             (1.4)

There is one fixed-positive-parameter hybrid solve per level. No conservation-defect stopping loop or summability assumption on successive primary errors is needed. The theorem does not prove that the fine mesh has any optimal relation to the coarse work, or that(1.2)-(1.3) are the original OWR higher-order flux estimator.

## 2. Primary residual reliability and convergence

For P1 functions and A=I, the element Laplacian of u_l is zero. Let I_l be a boundary-preserving locally H1-stable quasi-interpolant into S_l. Galerkin orthogonality and elementwise integration by parts give, for any v in H0^1,

    (grad(u-u_l),grad v)
       =sum_K(f,v-I_l v)_K
          -sum_(E interior)([grad u_l dot n_E],v-I_l v)_E,

with an immaterial sign choice for edge normals. The local volume and trace approximation estimates, summed with finite patch overlap, give

    ||grad(u-u_l)||_0<=C*rho_l.                             (2.1)

This is the standard residual-reliability proof; no additional solution regularity is required.

For the old P1 function on a refined mesh, new interior edges inside an old cell have zero gradient jump. Existing marked-cell edges are bisected, so their weighted jump contribution is at most half its old value. The marked-cell volume contribution is at most one quarter of its old value. Since every edge contribution was allocated in halves, the total reduction is at least one half of the marked cell-indicator sum. Closure and other extra refinements cannot increase this old-function estimator. Hence

    rho_(l+1)(u_l)² <= (1-theta_p/2)*rho_l(u_l)².            (2.2)

On a fixed primary mesh, the volume part is the same for two trial functions, while inverse trace inequalities bound the difference of their jump vectors by C||grad(v-w)||_0. Thus Young's inequality and(2.2) give

    rho_(l+1)²<=q_p*rho_l²+C||grad(u_(l+1)-u_l)||_0²        (2.3)

for a fixed q_p<1, choosing the Young parameter small enough.

The nested primary Galerkin projections satisfy

    ||grad(u_(l+1)-u_l)||_0²
      =||grad(u-u_l)||_0²-||grad(u-u_(l+1))||_0².

Their increments therefore tend to zero, without any prior density claim for the adaptive spaces. The elementary recursion a_(l+1)<=q*a_l+o(1), q<1, applied to(2.3), gives rho_l->0. Reliability(2.1) then identifies the Galerkin limit with u. This is an explicit verification of the coarse adaptive hypotheses, not a generic appeal to Dörfler marking.

## 3. Cauchy convergence of the moving-input flux solves

The exact flux sigma satisfies

    B_delta(sigma,tau)=(f+delta*u,div tau),    tau in H(div),

because u has zero boundary trace. Let z_l be its B_delta-orthogonal projection onto V_l. For fixed delta, B_delta is equivalent to the H(div) norm. Since V_l is nested, z_l converges strongly in H(div) to its projection onto V_infinity, the H(div) closure of union V_l.

Subtract the equations for sigma_l and z_l and test with their difference. The same stability estimate as Turn1 gives

    ||sigma_l-z_l||_(B_delta)<=delta*||u_l-u||_0 ->0.        (3.1)

Therefore sigma_l has a strong H(div) limit sigma_infinity, and its L2 increments tend to zero. This uses convergence of the moving primary input, not a claim that the sum of its successive differences is finite. It also does not yet identify sigma_infinity with sigma; that is the central consistency step below.

## 4. Fine indicator vanishing and its precise meaning

The fixed-mesh inverse-trace bound and old-field edge subdivision argument in Turn3 apply directly to the actual hybrid fluxes. Marking(1.3), the fine-mesh nesting and bisection of marked edges give

    eta_(l+1)²<=q_f*eta_l²+C||sigma_(l+1)-sigma_l||_0²       (4.1)

with a fixed q_f<1. The additional primary overlay only refines T_l and so preserves the old-field reduction. The last term tends to zero by section3; consequently eta_l->0.

What this controls is the nongradient part of sigma_l, not its conservation defect by itself. Decompose in L2

    sigma_l=-grad w_l+z_l^s,
    w_l in H0^1,       div z_l^s=0,

with orthogonal summands. The gradient range is closed by Poincare's inequality. On a simply connected polygon z_l^s=curl psi_l for some psi_l in H1, with ||grad psi_l||_0=||z_l^s||_0. The hybrid equation makes sigma_l orthogonal to every discrete divergence-free field. In particular it is orthogonal to curl I_l^f psi_l, where I_l^f is a continuous P1 quasi-interpolant on T_l with no boundary restriction.

Since curl sigma_l=0 inside every RT0 cell, integration by parts and the local trace approximation give

    ||z_l^s||_0²=(sigma_l,curl(psi_l-I_l^f psi_l))
                 <=C*eta_l*||z_l^s||_0.

Boundary tangential terms in(1.3) are essential here. Thus the distance of sigma_l from -grad H0^1 is at most C eta_l. Passing to its L2 limit shows

    sigma_infinity=-grad w for some w in H0^1.              (4.2)

This does not yet assert w=u.

## 5. Overlay coupling identifies the projected forcing

Let f_l=P_l f. Nested orthogonal projections imply f_l->f_infinity in L2 for some f_infinity in Q_infinity:=closure(union Q_l). Since T_l refines H_l, each fine-cell diameter is at most the diameter of its enclosing primary cell. The best-constant property on fine cells therefore yields

    ||h_l(f-P_l f)||_0 <= ||h_l f||_0
                         <=||H_l f||_0<=rho_l ->0.         (5.1)

For every v in H0^1, subtract its fine-cell means and use cell Poincare to obtain

    |(f-f_l,v)|<=C||h_l(f-f_l)||_0||grad v||_0.

Hence f_l converges to f in H^-1. Its L2 limit is therefore f, and

    P_l f -> f strongly in L2.                            (5.2)

This is where the fine-over-coarse overlay is used. It supplies data consistency without a separate fine data loop or a global-mesh-density assumption.

## 6. The positive-projection identity closes the conservation gap

Define the recovered scalar, exactly as in Turn1,

    q_l=P_l u_l+delta^-1(P_l f-div sigma_l).

The exact mixed first equation is

    (sigma_l,tau)=(q_l,div tau),       tau in V_l.            (6.1)

Let P_infinity be the L2 projection onto Q_infinity. Since u_l->u in L2, P_l u_l->P_infinity u. Strong H(div) convergence of sigma_l and(5.2) imply

    q_l -> q_infinity
       =P_infinity u+delta^-1(f-div sigma_infinity)         (6.2)

in L2. All q_l are in Q_l, so q_infinity is in Q_infinity. Also div sigma_infinity is in Q_infinity by the strong divergence limit.

Take tau in any fixed V_j and pass to the limit in(6.1) for l>=j. With(4.2) and w's zero boundary trace, integration by parts gives

    (w-q_infinity,div tau)=0.

The union of div V_j=Q_j is dense in Q_infinity. Therefore

    q_infinity=P_infinity w.                              (6.3)

Combining(6.2)-(6.3) gives

    div sigma_infinity=f-delta*P_infinity(w-u).

Since sigma_infinity=-grad w and f=-Delta u, the difference e=w-u in H0^1 satisfies

    -Delta e+delta*P_infinity e=0

weakly. Testing with e is legitimate because P_infinity e is L2. Orthogonality and positivity of the L2 projection yield

    ||grad e||_0²+delta*||P_infinity e||_0²=0.

Thus e=0, proving w=u and sigma_infinity=sigma. The already established strong H(div) convergence gives the full flux conclusion in(1.4). In particular the conservation defect tends to zero as a consequence, not as a separate stopping assumption.

This argument remains valid when Q_infinity is a proper subspace of L2. It does not secretly replace the adaptive mesh family by globally dense spaces. Only f's membership in the limiting scalar space is forced by the overlay/data argument.

## 7. What has and has not been resolved

The fixed-delta two-mesh variant is now proved convergent with a specified primary residual, a specified fine tangential indicator, explicit refinement requirements and exact treatment of the changing coarse input. The strongest new consistency step is the positive projected-reaction equation in section6. It avoids both a conservation-defect smallness assumption and an unsupported transfer from a conservative mixed theorem.

The source's unprinted higher-order flux estimator, any intended rule using that estimator alone, a prescribed h-versus-H work relation, higher-order RT/BDM, three dimensions, variable coefficients, nonhomogeneous boundary data and inexact solvers are not settled by this theorem. In particular the two independent marking rules are an explicit reconstruction. This is not a counterexample to, or proof of, a different unspecified algorithm.

Four substantive author turns are complete. The original target remains unresolved. Estimated completion50%, reflecting the proved reconstructed fixed-parameter variant and the still-open source-identification and generality gaps. All partial mathematical claims await separate independent review after the final turn.
