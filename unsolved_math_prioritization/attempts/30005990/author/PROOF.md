# A radial dimension lift for the sharp boundary homogeneity gap

## 1. Precise statement and imported results

Write H_d = R^(d-1) x (0,infinity), with coordinates (x,t), and let

Sigma_N = {a in R^N : a_i >= 0 and a_i a_j = 0 for i != j}.

For an open set G, write E(u,G) = sum_i integral_G |grad u_i|^2. In this proof S(G,N) consists of maps u in H^1_loc(G;Sigma_N) satisfying, distributionally,

    -Delta u_i <= 0,
    -Delta (u_i - sum_{j != i} u_j) >= 0                  (1.1)

for every i. Inequalities are tested against nonnegative compactly supported smooth functions. A local minimizer minimizes E against every Sigma_N-valued map with the same Sobolev boundary trace on every relatively compact Lipschitz subdomain.

We use these established results, not claims proved in this packet:

**Interior input I.** S(G,N) is the local minimizer class; its maps are locally Lipschitz. At a zero of a nontrivial such map, its Almgren frequency is either 1 or at least 3/2. A nonzero globally 3/2-homogeneous member is a planar three-sector Y profile, extended constantly in the other variables, up to rotation, positive scaling, and relabeling. The applicable references are [OV-triple], Section 2, Theorems 2.1 and 2.4, and Proposition 3.5. The article attributes the gap to prior work including [ST15], and S=M to [WZ10, Theorem 1.6]. The equivalence S=M is only needed below to verify attainment; the exclusion and equality classification use exactly class S.

**Boundary input B.** For a spectral optimizer on a bounded domain satisfying [OV-boundary, Assumption 2.1], a normalized boundary blow-up is a nonzero homogeneous half-space minimizer with zero flat trace, and its degree equals the boundary frequency. See Definition 4.3 and Proposition 6.13 there. C^(1,alpha) domains with alpha>0 are covered; the more general Dini hypotheses remain exactly those of that paper.

Let B_gamma^(d,N) consist of nonzero maps U with the following properties:

1. U is in H^1(B_R^+;Sigma_N) for every R>0, with zero trace on the flat part of the boundary.
2. U(r x,r t)=r^gamma U(x,t) almost everywhere for every r>0.
3. U minimizes E on each B_R^+ among Sigma_N-valued maps with the same full boundary trace.

This is the half-space class of [OV-boundary, Definition 4.3]. It implies U belongs to S(H_d,N), by interior variations and the usual extremality conditions included in input I.

**Theorem.** Let d>=3. If U belongs to B_gamma^(d,N) and gamma>2, then gamma>=5/2. If gamma=5/2, then exactly three components are nonzero and

    U_i(x,t) = c t Y_i(Px),   i=1,2,3,                  (1.2)

after relabeling, where c>0 and P is an orthogonal coordinate projection from R^(d-1) onto a two-plane. Conversely, for every N>=3, every map (1.2), with other components zero, belongs to B_(5/2)^(d,N). Therefore, when N>=3 (or when N is allowed to vary), the minimum admissible homogeneity strictly above 2 is 5/2. Its additive separation from 2 is 1/2. For N=2, equality at 5/2 is impossible; the theorem's exclusion still applies.

The exclusion conclusion also holds if assumption 3 is replaced by U in S(H_d,N), retaining assumption 1 and homogeneity. This stronger distributional formulation is what makes the lift useful.

## 2. Sobolev lifting and the axis

Let n=d+2 and write z=(x,y) in R^(d-1) x R^3. Put A={y=0}. For t>0 set v(x,t)=U(x,t)/t, component by component, and define

    V(x,y)=v(x,|y|),   y!=0.                             (2.1)

We first prove V is in H^1_loc(R^n;Sigma_N). Assign arbitrary values on A for now, a Lebesgue-null set.

Fix R>0. Choose a smooth radial cutoff eta which is one on B_R, vanishes outside B_(2R), and is bounded with bounded derivative. The zero flat trace of U permits eta U to be extended by zero and viewed as an H^1 function on the half-space with zero boundary trace. The one-dimensional Hardy inequality on each vertical line, then Fubini, gives

    integral_Hd |eta U|^2/t^2 <= 4 integral_Hd |partial_t(eta U)|^2 < infinity.       (2.2)

Thus U/t is square-integrable on B_R^+. Off A, ordinary weak differentiation and polar coordinates in R^3 give

    integral_(B_R^n) |V|^2 = 4 pi integral_(B_R^+) |U|^2,

    integral_(B_R^n minus A) |grad V|^2
      = 4 pi integral_(B_R^+) [ |grad_x U|^2 + |partial_t U - U/t|^2 ].             (2.3)

Both quantities are finite by (2.2) and the H^1 hypothesis. The factor 4 pi is the area of S^2; all component norms are summed.

For completeness the weak derivatives extend across A without a hidden jump. Choose a Lipschitz cutoff chi_epsilon(y) which is zero for |y|<=epsilon, one for |y|>=2epsilon, takes values in [0,1], and has gradient bounded by C/epsilon. On any fixed compact cylinder K,

    integral_K |grad chi_epsilon|^2 <= C_K epsilon.       (2.4)

Apply integration by parts off A to chi_epsilon times any test function. The extra term containing V grad chi_epsilon is bounded by

    C ||V||_(L^2(K intersect {|y|<2epsilon}))
       ||grad chi_epsilon||_(L^2(K)),

which tends to zero. The other terms converge by dominated convergence and (2.3). Hence the off-axis weak derivatives are the global weak derivatives, proving the claim. Nonnegativity and segregation survive because the scalar divisor t is positive and A is null.

This argument explains why finite energy at the axis is a necessary step. Merely writing a classical Laplacian away from A would not suffice.

## 3. The lifted map satisfies exactly the interior inequalities

It suffices to treat one scalar function h, either U_i or U_i-sum_(j!=i)U_j, for which a distributional Laplacian inequality is known. Write w=h/t and W(x,y)=w(x,|y|).

Take a smooth test phi compactly supported away from A. Its spherical average

    a(x,t) = (1/(4 pi)) integral_(S^2) phi(x,t omega) d omega

is smooth, supported away from t=0, and nonnegative if phi is nonnegative. Rotational integration gives

    integral_(R^n) grad W dot grad phi
       = 4 pi integral_Hd t^2 grad(h/t) dot grad a.       (3.1)

The integrands satisfy

    grad h dot grad(t a) - t^2 grad(h/t) dot grad a
       = (partial_t h) a + h partial_t a
       = partial_t(h a).                                (3.2)

The total derivative integrates to zero because a is supported away from both t=0 and infinity. Identity (3.2) remains valid for H^1 h by ordinary local approximation. Therefore

    integral_(R^n) grad W dot grad phi
       = 4 pi integral_Hd grad h dot grad(t a).           (3.3)

The right side has the required sign because t a is an admissible nonnegative test for the inequality of h. Thus (1.1) holds for V off A.

Now let phi>=0 be an arbitrary compactly supported smooth test in R^n. Use phi chi_epsilon in the off-axis inequality, approximating the Lipschitz cutoff if desired. By (2.3), the principal term converges to integral grad W dot grad phi. The error is bounded by

    C ||grad W||_(L^2(K intersect {epsilon<|y|<2epsilon}))
       ||grad chi_epsilon||_(L^2(K)),

which tends to zero by (2.4). The same argument applies to every signed combination of components. Both inequalities extend to all of R^n. Consequently

    V belongs to S(R^(d+2),N).                           (3.4)

In particular there is no extra distribution supported on the codimension-three axis. This is membership in the precise class of input I, not just componentwise harmonicity on positivity sets.

The formal differential identity behind this proof is

    Delta_(x,y) V = (1/t) Delta_(x,t) U,   t=|y|>0.

It is a useful check, but the weak proof above is essential.

## 4. Homogeneity and the sharp exclusion

Equation (2.1) and the homogeneity of U show

    V(rz)=r^(gamma-1) V(z).                              (4.1)

The map is nonzero. By (3.4) and input I it has a locally Lipschitz representative. When gamma>2, its positive homogeneity beta=gamma-1 forces V(0)=0. The homogeneity identity, initially almost everywhere, holds for this continuous representative everywhere.

For a homogeneous member of S the Almgren frequency at its origin equals its degree. One can see this directly from the standard energy identity for class S: each component is harmonic on its positive set, its zero-set boundary term vanishes, and radial differentiation is partial_r V=beta V/r. Thus

    r integral_(B_r) |grad V|^2 / integral_(partial B_r) |V|^2 = beta.

The corresponding identity and monotonicity are included in [OV-triple, Section 2.2]; the denominator is positive for a nonzero homogeneous map. No normalization of that denominator is needed here.

Input I now says beta=1 or beta>=3/2. Under gamma>2, beta>1, so gamma>=5/2. This proves the exclusion on (2,5/2).

For spectral optimizers satisfying input B, a boundary free-interface frequency larger than 2 has a nonzero U in this half-space class with that degree. Applying the exclusion proves the asserted spectral frequency bound. This is a deduction from a boundary blow-up theorem, not a replacement for its domain regularity assumptions.

## 5. Rigidity at equality and tangential orientation

Suppose gamma=5/2. Then V is globally 3/2-homogeneous and belongs to S. Input I gives

    V(z)=c Y(P_E z),                                     (5.1)

up to component relabeling, with c>0, where E is a two-dimensional linear subspace of R^n and P_E denotes orthogonal coordinates on it. The remaining components vanish. Let L=E^perp. The singular triple-junction spine of (5.1) is exactly L; the other points of its zero set are ordinary two-phase interfaces.

By its definition the actual map V is invariant under every rotation which fixes x and rotates y in R^3. This invariance preserves the singular spine L, hence also E=L^perp. Let Q be the orthogonal projection onto E. Then Q commutes with every matrix diag(I_(d-1),R), R in SO(3). Write it in blocks:

    Q = [ A  B ; B^T  C ].

Commutation gives B R=B for every R and C R=R C for every R. No nonzero vector is fixed by every SO(3) rotation, so B=0. Since C is symmetric and commutes with all rotations, its quadratic form is constant on the unit sphere; hence C=c_0 I_3. Because Q is a projection, c_0 is either 0 or 1. But rank Q=2, so c_0=1 is impossible. Therefore C=0 and E is contained in the tangential factor R^(d-1) x {0}.

Consequently V is independent of y and equals a tangential planar Y profile. Substitution in U=tV proves (1.2). In particular exactly three components survive and their common multiplicative coefficient is fixed by the interior classification. Independent unequal component multipliers are not allowed.

This orientation argument also shows why the 5/2 profile cannot exist when d=2: the tangential factor then has dimension one. The present theorem is stated for d>=3, as in the target higher-dimensional question.

## 6. Attainment in the admissible half-space class

Here is an unambiguous definition of the nonnegative planar Y profile. In polar coordinates (rho,theta), choose sectors

    I_i=(2 pi(i-1)/3, 2 pi i/3),   i=1,2,3.

For theta in I_i let

    Y_i(rho,theta)=rho^(3/2) sin((3/2)(theta-2 pi(i-1)/3)),

and let Y_i=0 outside its sector. Boundary values are zero, with the periodic endpoint theta=0=2 pi identified. The shifted sine is positive on each open sector. This explicit convention avoids alternating signs from an unshifted trigonometric formula.

Each positive piece is harmonic because its radial degree and angular frequency are both 3/2. Across a sector ray, each adjacent piece has the same inward normal derivative magnitude (3/2)rho^(1/2). Its zero extension has nonnegative Laplacian measure there. Thus Delta Y_i>=0. For hat Y_i=Y_i-sum_(j!=i)Y_j, the measures cancel on rays adjacent to sector i and add with negative sign on the remaining ray, so Delta hat Y_i<=0. There is no atom at the origin: the flux through a small circle is O(rho^(3/2)). Equivalently these inequalities follow from the standard Y model in input I.

Extend Y independently of all other tangential variables and put U(x,t)=tY(x_1,x_2). In H_d the factor t is positive and independent of those two coordinates. Therefore its distributional Laplacians are t times the corresponding Laplacians of Y. This proves U belongs to S(H_d,N), with zero additional components if N>3. It has finite H^1 norm on bounded half-balls, zero flat trace, and degree 5/2.

It remains to check energy minimality for competitors touching the fixed boundary, rather than silently equating interior minimality with that boundary assertion. By S=M from input I, U is locally minimizing in H_d. Fix R>0 and let W be any Sigma_N-valued H^1 map on B_R^+ with the same full trace as U. Set f=W-U in H^1_0(B_R^+;R^N), extend it by zero to H_d, and apply Hardy:

    integral_(B_R^+) |W-U|^2/t^2 < infinity.              (6.1)

View Sigma_N with its intrinsic star-tree metric. Its distance is |a-b| on one ray and |a|+|b| on different rays; it lies between Euclidean distance and sqrt(2) times Euclidean distance. Let G_s(a,b) be the constant-speed point on the unique tree segment from a to b, at parameter s in [0,1]. This interpolation stays in Sigma_N. On individual rays it is linear; on different rays it moves to the vertex then out along the other ray. It is Lipschitz in its arguments, and its speed with respect to s is the tree distance.

Choose eta_epsilon(t)=0 for t<=epsilon, =1 for t>=2epsilon, with |eta_epsilon'|<=C/epsilon, and define

    W_epsilon(x,t)=G_(eta_epsilon(t))(U(x,t),W(x,t)).      (6.2)

This map equals U near the plane, equals W outside the strip t<2epsilon, and has the same spherical trace as U since W=U there in the trace sense. The Sobolev chain rule for the piecewise linear tree interpolation gives on the strip the bound

    |grad W_epsilon| <= C (|grad U|+|grad W|+|W-U|/epsilon).

The strip's gradient-energy contribution tends to zero: the first two terms do so by absolute continuity of the integral; the last is bounded, on epsilon<t<2epsilon, by a constant times the integral of |W-U|^2/t^2, which tends to zero by (6.1). It follows that W_epsilon converges to W in H^1(B_R^+). (The same bounds and the equality off the strip give the L^2 conclusion.)

Apply the interior minimizing property to the Lipschitz truncated half-ball B_R intersect {t>epsilon/2}, whose closure lies in H_d. On its entire boundary W_epsilon and U have the same trace. Below t=epsilon/2 they coincide. Hence

    E(U,B_R^+) <= E(W_epsilon,B_R^+).

Let epsilon tend to zero. Strong H^1 convergence proves E(U,B_R^+)<=E(W,B_R^+). Thus U belongs to the exact boundary class B_(5/2)^(d,N), and sharpness is established within that class.

## 7. Geometry, notation, and what is not proved

The positive sets of tY are three sectors in a tangential two-plane, multiplied by (0,infinity) in the normal direction and by R^(d-3) in the other tangential directions. The pairwise interfaces are flat vertical half-hyperplanes and meet at 120-degree angles. The common interior spine is {x_1=x_2=0,t>0}, with unused coordinates free. It meets the flat fixed boundary orthogonally. In d=3 the spine is a half-line; in higher dimensions it is the cylindrical extension of that picture.

At a spine point with t=t_0>0, a dilation by r has leading term t_0 r^(3/2)Y and an error of order r^(5/2). Its interior frequency is therefore 3/2. At the boundary origin the entire map is 5/2-homogeneous. This verifies the geometric endpoint in the corrected conjecture.

Write beta_d=inf{gamma>2 : B_gamma^(d,N) is nonempty for some N}. The theorem proves beta_d=5/2 for d>=3. If instead g_d is defined by the optimal inclusion gamma in {2} union [2+g_d,infinity), its value is 1/2. The report's printed g_d=5/2 uses the same symbol inconsistently; it cannot be preserved as a literal numerical conclusion.

For example, even without the Y construction, the signed harmonic polynomial P=t(x_1^2-t^2/3) has degree 3 and zero flat trace. Its positive and negative parts give a two-ray minimizing configuration (equivalently scalar harmonic Dirichlet minimization), showing that an additive gap as large as 5/2 is impossible for the boundary cone class. This is a notation diagnostic, not a replacement for the sharp theorem.

The packet does not prove that a bounded smooth-domain optimizer for the unrestricted global spectral sum realizes this cone at a boundary point. Sharpness in B_gamma and the universal spectral lower bound are different logical assertions from that global realization. Nor is regularity near actual 5/2 points proved: that would require decay and uniqueness information beyond the cone classification. No assertion is made that merely C^1 boundaries satisfy all the imported quantitative blow-up hypotheses.

## References

- [OWR] B. Velichkov, joint work with R. Ognibene, *Regularity up to the boundary for optimal partition problems*, in *Calculus of Variations*, Oberwolfach Reports 37/2024, printed pp.2120-2123. https://doi.org/10.4171/OWR/2024/37
- [OV-boundary] R. Ognibene and B. Velichkov, *Boundary regularity of the free interface in spectral optimal partition problems*, arXiv:2404.05698v1. https://arxiv.org/abs/2404.05698v1
- [OV-triple] R. Ognibene and B. Velichkov, *Structure of the free interfaces near triple junction singularities in harmonic maps and optimal partition problems*, arXiv:2412.00781v5; Arch. Rational Mech. Anal. 250, 77 (2026). https://arxiv.org/abs/2412.00781v5 ; https://doi.org/10.1007/s00205-026-02221-4
- [ST15] N. Soave and S. Terracini, *Liouville theorems and 1-dimensional symmetry for solutions of an elliptic system modelling phase separation*, Advances in Mathematics 279 (2015), 29-66. https://doi.org/10.1016/j.aim.2015.03.015
- [WZ10] K. Wang and Z. Zhang, *Some new results in competing systems with many species*, Ann. Inst. H. Poincare Anal. Non Lineaire 27 (2010), 739-761. https://doi.org/10.1016/j.anihpc.2009.11.004
