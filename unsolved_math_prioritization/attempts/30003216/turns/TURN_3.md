# Turn 3: a terminating reconstructed adaptive algorithm

**Unreviewed scoped theorem for an explicitly specified variant. The original OWR adaptive procedure is still unidentified and unresolved.**

This turn closes the conditional algorithm gaps of Turn2 for a planar RT0 model by choosing an absolute conservation-defect test and a separate data-oscillation step. It treats the actual coarse-primary/fine-flux equations, with potentially changing coarse inputs, but changes the parameter/marking policy explicitly. It does not assert that these choices are the unprinted original higher-order estimator or two-mesh rule. The Schur/Uzawa interpretation and small-parameter idea are credited to KLS and Adhikari–Kim–Lee–Sheen2024. The proof below does not import a mixed adaptive-convergence theorem without its hypotheses.

## 1. Precise variant and theorem

Let Omega be a bounded polygon in R², star-shaped with respect to a ball. Take A=I, homogeneous Dirichlet values, and f in L2(Omega). Write sigma=-grad u for the exact Poisson flux. Let T_l be nested conforming triangulations in a uniformly shape-regular refinement family. Put V_l=RT0(T_l), Q_l=P0(T_l), and let P_l be the cellwise L2 projection. Boundary normal flux is not constrained in V_l, as appropriate to this Dirichlet formulation.

The refinement family is assumed to permit finitely many conforming refinements that bisect every prescribed edge, and arbitrarily fine uniform refinements with a fixed shape-regularity bound. Standard compatible triangular bisection families have these properties. Local refinement counts and optimal complexity are not claimed.

At each level choose any finite conforming primary space S_l subset H0^1, on its own mesh, and compute its exact Galerkin solution u_l. The primary meshes need not be nested or synchronized with T_l. All cross-mesh integrals and both variational solves below are exact; quadrature and algebraic-solver errors are outside this theorem.

Fix 0<theta<1 and tau_l=2^(-l). Use this algorithm:

1. The current fine mesh satisfies osc_l:=||h_l(f-P_l f)||_0<=tau_l. Arrange this initially by finite refinement.
2. Start delta at1, solve the recovered hybrid equation

       (div sigma_l,div v)+delta(sigma_l,v)
           =(f+delta u_l,div v),       v in V_l,

   and halve delta and re-solve until

       ||d_l||_0<=tau_l²,       d_l=div sigma_l-P_l f.        (1.1)

3. Compute the all-edge tangential indicator eta_l from Turn2(3.1). Mark a set M_l with

       eta_l(sigma_l;M_l)²>=theta*eta_l(sigma_l)².

   If the indicator is zero, M_l may be empty.
4. Refine every marked edge at least at its midpoint. Perform any additional conforming data refinements necessary to make osc_(l+1)<=tau_(l+1), preserving uniform shape regularity. The resulting mesh is T_(l+1).

**Theorem.** Every inner parameter loop and data step terminates. The resulting hybrid fluxes satisfy

    ||sigma_l-sigma||_0 + ||div sigma_l-f||_0 ->0.            (1.2)

There is no requirement that the primary Galerkin solutions themselves converge; their moving input is controlled by the measured conservation defect. The theorem makes no rate, mesh-complexity, conditioning or original-source-algorithm claim.

## 2. Uniform divergence lift: the exact stability input

There is a constant C_R independent of the mesh such that every q_l in Q_l has a lift r_l in V_l with

    div r_l=q_l,       ||r_l||_0<=C_R||q_l||_0.              (2.1)

Here is the standard construction and the reason its hypotheses apply. For zero-mean q, the Bogovskii right inverse on a domain star-shaped with respect to a ball gives a vector field in H0^1 with divergence q and H1 norm bounded by C||q||_0. For general q, add a scalar multiple of the affine field x/2, whose divergence is1, to handle its mean. Thus an H1 lift v exists with ||v||_H1<=C||q||_0. No zero-normal boundary condition is imposed on that final lift.

Apply the canonical RT0 interpolant. Its commuting identity gives div(Pi_l v)=P_l div v=q_l, and its local interpolation estimate gives

    ||Pi_l v||_0 <= C(||v||_0+||h_l grad v||_0)
                 <= C_domain,shape ||q_l||_0.

This proves(2.1). The minimum-L2-norm lift R_l q_l can only be smaller. The primary inputs used here are the classical Bogovskii bound and RT interpolation properties, not an adaptive theorem. They were checked in Duran, arXiv:1103.3718, section3, and Guermond's finite-element notes, Chapter16, Lemma16.2/Theorem16.4. The mean correction and mesh-uniform consequence are stated explicitly so no hidden mean-zero or boundary assumption is imported.

## 3. Termination and finite-level comparison

For a fixed mesh and fixed u_l, Turn2 gives

    d_delta=delta*S_l*(S_l+delta I)^(-1)(P_l u_l-p_M,l),

where S_l is the positive Schur operator and p_M,l its conservative mixed scalar. Hence d_delta->0 as delta->0. Halving reaches the strictly positive tolerance tau_l² after finitely many solves, even if eta_l(sigma_M,l)=0. There is no division by an estimator in this stopping rule. The spaces are finite and the fixed-delta solve is positive definite. If Q_l is zero the flux and defect are trivially zero; ordinary RT0 triangulations have nonzero Q_l.

Let sigma_M,l be the exact conservative mixed flux on the same mesh, characterized as the unique minimum-L2-norm element of V_l with divergence P_l f. The hybrid equation makes sigma_l orthogonal to the discrete divergence-free subspace. The exact correction identity and(2.1) yield

    ||sigma_l-sigma_M,l||_0<=C_R||d_l||_0<=C_R*tau_l².        (3.1)

This bound contains no difference of successive primary solutions and is valid for every changing Galerkin input. It avoids trying to sum a moving-data perturbation with no summability proof.

The data step also terminates: after enough uniform refinements, h_max||f||_0 is below the desired tolerance, and osc<=h_max||f||_0. Local data refinement can be used instead; no efficiency assertion is needed. Oscillation never increases under nested refinement, since each new cell has no larger diameter and its mean is the best L2 constant on that cell. Thus extra conformity refinements do not invalidate the test.

## 4. A nested mixed-flux Cauchy lemma with changing projected data

This lemma requires only nested V_l,Q_l, the uniform lift(2.1), and f in L2. It does not assume that the meshes become globally dense.

The orthogonal projections f_l=P_l f converge in L2 to f_infinity, the projection onto Q_infinity=closure(union Q_l). Let V_infinity be the H(div) closure of union V_l. The minimum-norm property and(2.1) bound sigma_M,l in H(div). Any weakly convergent subsequence therefore has a limit sigma_* in V_infinity with divergence f_infinity.

The union of the discrete divergence-free spaces is dense in Z_infinity:=ker(div) intersect V_infinity in H(div). To prove this, approximate any z in Z_infinity by v_l in V_l in H(div), and set

    z_l=v_l-R_l(div v_l).

The correction has L2 norm at most C_R||div v_l||_0->0 and divergence div v_l->0. Thus z_l->z in H(div) and div z_l=0. This argument applies along a sequence of increasing levels, and nestedness fills the intermediate levels.

Every sigma_M,l is L2-orthogonal to the corresponding discrete kernel. Taking limits, every weak cluster point sigma_* is orthogonal to Z_infinity. Therefore there is at most one such point: the difference of two candidates is in Z_infinity and is orthogonal to itself. This proves weak convergence of the entire bounded sequence.

For strong convergence, choose v_l in V_l converging in H(div) to sigma_*. Set

    w_l=v_l+R_l(f_l-div v_l).

The argument of R_l is in Q_l and tends to0 in L2. Hence w_l->sigma_* in L2 and div w_l=f_l. Minimality gives ||sigma_M,l||_0<=||w_l||_0. Combined with weak lower semicontinuity, this proves convergence of the norms and therefore

    sigma_M,l -> sigma_* strongly in L2,
    ||sigma_M,l+1-sigma_M,l||_0 ->0.                         (4.1)

Its divergence already converges in L2, so the sequence is also Cauchy in H(div). The limit is not yet identified with the true solution; that identification is the next, essential step.

## 5. Indicator stability and actual refinement reduction

For the all-edge tangential indicator in Turn2, the inverse trace inequality on a shape-regular RT0 mesh gives

    |eta_l(v;M)-eta_l(w;M)|<=L||v-w||_0                     (5.1)

for every edge subset M and v,w in V_l, with uniform L. It follows by summing h_E||jump((v-w) dot t)||_E² and the corresponding boundary terms, using bounded patch overlap. The indicator is the norm of a linear collection of traces, so the reverse triangle inequality is applicable.

If T' refines T and every edge in M is bisected, evaluate the old RT0 field v on the fine mesh. A new interior edge inside an old triangle has zero jump. An old edge is partitioned into smaller edges; on each marked old edge their lengths are at most h_E/2. Its weighted squared contribution is therefore at most one half of its old value. Unmarked contributions cannot increase. Hence

    eta_T'(v)²<=eta_T(v)²-(1/2)*eta_T(v;M)².                (5.2)

This includes boundary edges. Additional data refinements only improve the inequality. Combining(5.1)-(5.2) with (a+b)²<=(1+zeta)a²+(1+1/zeta)b² gives

    eta_(l+1)(sigma_M,l+1)²
       <=(1+zeta)[eta_l(sigma_M,l)²-(1/2)eta_l(sigma_M,l;M_l)²]
          +C_zeta||sigma_M,l+1-sigma_M,l||_0².              (5.3)

These are the actual reduction properties used below. No unverified assertion that an arbitrary mixed estimator contracts is needed.

## 6. Convergence, including zero-indicator levels

Write a_l=eta_l(sigma_l) and b_l=eta_l(sigma_M,l). From(3.1) and(5.1),

    |a_l-b_l|<=L*C_R*tau_l².                               (6.1)

There are two exhaustive cases.

### Infinitely many small-indicator levels

Suppose a_l<=tau_l along an infinite sequence. Then b_l->0 along that sequence by(6.1). Turn2's reliability theorem applied to the conservative flux (whose defect is zero) gives

    ||sigma-sigma_M,l||_0<=C(b_l+osc_l)->0

there. The full mixed sequence is Cauchy by section4, so its unique limit must be sigma. Equation(3.1) proves convergence of all hybrid outputs. This argument covers exact zero indicators; no parameter-loop exception or a priori lower bound on b_l is needed.

### Eventually all indicators are larger

Otherwise a_l>tau_l for all sufficiently large l. By(3.1), chi_l/a_l<=C_R*tau_l, where chi_l=||sigma_l-sigma_M,l||_0. The exact bulk-transfer inequality from Turn2 then shows that, eventually,

    eta_l(sigma_M,l;M_l)² >= (theta/4)*b_l².                (6.2)

For example, it suffices that L*C_R*tau_l<=min(sqrt(theta)/4,1/2). This is an eventual mathematical bound, not an extra test requiring knowledge of the constants in the algorithm.

Insert(6.2) into(5.3) and choose a fixed zeta>0 so that q=(1+zeta)(1-theta/8)<1. Then

    b_(l+1)²<=q*b_l²+C_zeta||sigma_M,l+1-sigma_M,l||_0².

The last term tends to0 by(4.1). Iterating this scalar inequality, splitting the convolution into a finite initial part and a uniformly small tail, gives b_l->0. Reliability and osc_l<=tau_l->0 again identify the mixed limit with sigma, and(3.1) proves all-level hybrid convergence.

Finally f_l=P_l f converges in L2 to f_infinity, while

    ||f-f_l||_-1<=C||h_l(f-f_l)||_0<=C*tau_l->0.

Thus f_infinity=f as a distribution and hence as an L2 function. Since div sigma_l=f_l+d_l and ||d_l||_0<=tau_l², the divergence converges to f in L2. This completes(1.2).

## 7. Scope, classical credit and remaining original gap

The theorem genuinely proves convergence of the displayed variable-parameter algorithm for arbitrary L2 data and arbitrary changing coarse Galerkin inputs in the stated planar RT0 setting. It uses the source's recovered two-stage equations. The parameter halving, absolute defect tolerance, all-edge indicator and data refinement are explicit additions. They have not been shown to coincide with the original OWR augmented estimator, its intended fixed/variable delta rule, or its two-mesh policy. Higher-order RT/BDM spaces, general coefficients, nonhomogeneous data, other domains, inexact solves, rates and complexity are not proved here.

The proof uses classical divergence lifting, interpolation, projection and residual-estimator arguments, all with their hypotheses stated. Duran's primary paper supplies the star-shaped-domain lifting input; Guermond's primary notes supply the RT commuting/interpolation properties. The already credited 2024 paper supplies prior Schur/Uzawa context. Carstensen–Hoppe is historical motivation; its adaptive theorem is not a black-box assumption in the proof above. The attempted additional final-journal PDF link returned an HTML page, so the already pinned institutional primary copy remains the inspected CH reading source.

Three substantive author turns are complete. The original source target remains unresolved; estimated completion40%. This is a scoped partial awaiting later independent review, not a claimed solution of an unspecified original algorithm.
