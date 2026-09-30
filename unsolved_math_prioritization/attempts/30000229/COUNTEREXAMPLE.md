# The endpoint data-approximation implication fails

**30000229 / OWR-829-001. Complete negative-answer candidate at s=1/2; separate review pending. Two approaches.** The multiscale construction is credited to Cohen–DeVore–Nochetto. The mean-zero bubble argument below connects it to the original piecewise-constant dual-norm question. No novelty or human peer-review claim is made.

## 1. Exact target and the distinction that must be preserved

Stevenson's OWR24/2005 contribution, printed pp.1306–1307, treats the two-dimensional Poisson equation, continuous linear finite elements, and newest-vertex-bisection partitions. It conjectures the data-approximation implication for0<s<=1/2, explicitly including the endpoint, in the H^−1 setting beyond L². The dual norm is that of H^1_0 with gradient norm. The source separately requires a construction procedure for algorithmic optimality; the conjecture at issue asks only for existence of approximants.

We give u in A^(1/2) on Omega=(0,1)², with f=−Delta u in H^−1(Omega), such that

    inf_{T admissible, #T<=N} inf_{g in P_0(T)}
       ||f−g||_{H^−1} is not O(N^−1/2).                    (1)

In fact, along N=4^n it is bounded below by (c n−C)2^−n, for fixed positive constants c,C. Here P_0(T) contains all real piecewise-constant functions, with no bound on their coefficients. The meshes are conforming newest-vertex-bisection refinements of the initial mesh described below, with the standard uniform shape regularity and linear overlay/completion bounds. Allowing nonconforming bisection partitions with uniformly linear conforming completion does not evade the result: refine such a partition to its completion, on which its piecewise constants remain piecewise constant, and absorb the fixed cardinality factor into the bounds below.

Cohen, DeVore and Nochetto, *Convergence Rates of AFEM with H^−1 Data*, Foundations of Computational Mathematics12 (2012),671–718, DOI10.1007/s10208-012-9120-1, already construct the u used here. Section6.4 of their complete author preprint proves an endpoint obstruction for their localized data estimator D(f,T). That estimator is not the best piecewise-constant H^−1 error. A large value of D alone does not prove (1), since even a perfectly representable constant function may have nonzero D. We therefore prove a separate lower bound annihilating every g in P_0(T). Their construction and endpoint insight are prior work, not a new discovery here.

## 2. A mean-zero edge-bubble lower bound

Let T be any conforming shape-regular triangulation in the allowed family. Let

    S=sum_{e interior edge} J_e delta_e,

where J_e is constant on each edge and delta_e acts by integration along e. Fix any subset E_* of interior edges. There is a mesh-independent constant c_*>0 such that, for every g in P_0(T),

    ||S−g||_{H^−1} >= c_* [sum_{e in E_*} J_e² |e|²]^(1/2). (2)

Only shape regularity enters c_*.

To prove this, for an interior edge e with endpoints A,B, take the standard quadratic edge bubble b_e=4 lambda_A lambda_B on its two neighboring triangles, extended by zero elsewhere. On either neighboring triangle K, whose third barycentric coordinate is lambda_C, replace it by

    psi_e|K = 4 lambda_A lambda_B−20 lambda_A lambda_B lambda_C.

It has the same trace on e, zero trace on every other edge of its support, and zero element mean. Indeed

    integral_K 4 lambda_A lambda_B = |K|/3,
    integral_K 20 lambda_A lambda_B lambda_C = |K|/3.

Thus psi_e is continuous, belongs to H^1_0(Omega), and is orthogonal to every piecewise constant on T. Its trace integral on e is (2/3)|e|. Reference-element scaling in two dimensions and uniform shape regularity give ||grad psi_e||²<=C_b, uniformly over the mesh. Define

    v=sum_{e in E_*} J_e |e| psi_e.

At most three such edge bubbles meet in a triangle. Therefore

    ||grad v||² <=3 C_b sum_{e in E_*} J_e² |e|²,
    <S−g,v>=(2/3) sum_{e in E_*} J_e² |e|².

Other edges contribute zero because psi_e has zero trace on all edges except e, and the g term vanishes element by element. The dual norm gives (2). This proof permits arbitrary signs of the jumps and arbitrary coefficients of g; cancellation cannot invalidate the lower bound.

## 3. The credited multiscale solution

Start with the four-triangle mesh T_0 obtained by drawing both diagonals of the unit square. Use the compatible newest-vertex labels of the cited construction: the square's boundary edges have level label0 and the four center-to-corner edges label1. Its piecewise-linear center hat is denoted phi. It is1 at(1/2,1/2),0 on the boundary, and ||grad phi||²=4.

For a dyadic square Q, let phi_Q be the scaled copy of this center hat on Q, zero outside Q. The energy norm is scale invariant in two dimensions, so ||grad phi_Q||=2. Choose disjoint-interior dyadic squares

    Q_j=[2^−j,2^(1−j)] times [0,2^−j],    j=1,2,... .

Subdivide Q_j into4^j equal dyadic squares Q_(i,j), i=1,...,4^j, of side h_j=4^−j. Put

    u=sum_(j>=1) 4^−j sum_(i=1)^(4^j) phi_(Q_(i,j)),
    V_n=sum_(j=1)^n 4^−j sum_(i=1)^(4^j) phi_(Q_(i,j)).     (3)

Supports have disjoint interiors, including across different j. Hence the series converges in H^1_0(Omega) and

    ||grad u||²=4 sum_(j>=1) 4^−j=4/3,
    ||grad(u−V_n)||²=(4/3)4^−n.                            (4)

In particular f=−Delta u belongs to H^−1. With this norm, the weak Dirichlet Laplacian is an isometry, so

    ||f−S_n||_{H^−1}=||grad(u−V_n)||=(2/sqrt(3))2^−n,
    S_n=−Delta V_n.                                        (5)

The mesh facts in the cited Section6.4 apply to every such dyadic square: reaching its four-triangle base pattern requires O(j) path refinements, and filling Q_j with the4^j smaller patterns requires O(4^j) further refinements. Linear-complexity conforming completion and the overlay bound give a conforming admissible mesh T_n with

    V_n in P_1(T_n) intersect H^1_0,
    #T_n<=C_0 4^n.                                         (6)

These are adaptive bisection meshes, not a replacement by globally uniform meshes. Equations(4) and(6), with monotonicity of best errors between consecutive values of4^n, prove u in A^(1/2). The same statement holds for Galerkin best energy error because the Poisson energy projection minimizes that error.

## 4. A lower bound against every piecewise-constant approximant

Fix n and an arbitrary admissible T with #T<=4^n. Let T*=T overlay T_n. Standard bisection overlay gives

    #T*<=#T+#T_n−#T_0<=C_1 4^n.                            (7)

Every g in P_0(T) lies in P_0(T*). Also V_n is piecewise linear on T*, so S_n is a sum of constant edge jumps on that mesh.

For each square Q_(i,j), j<=n, select its segment sigma_(i,j) joining its center to its lower-left corner. The segment has length h_j/sqrt(2). Across this segment the two gradients of its unscaled center hat differ by a normal jump of magnitude2sqrt(2)/h_j. The coefficient4^−j=h_j in (3) therefore makes the jump of V_n have magnitude2sqrt(2), independent of i,j. No other term of (3) changes that jump, because the supports have disjoint interiors. Thus

    |J_sigma| |sigma|=2 h_j=2*4^−j.                        (8)

These selected segments have disjoint interiors and form unions of edges of T*. They may have been subdivided during conforming completion, but the jump remains constant along each. Let m_sigma be the number of fine edges into which a selected segment is divided. Cauchy–Schwarz gives

    sum_{e subset sigma} J_e² |e|²
       >= J_sigma² |sigma|²/m_sigma.                      (9)

Fine edges belonging to different selected segments are distinct, so

    sum_sigma m_sigma <=#edges(T*)<=3#T*<=3 C_1 4^n.        (10)

A second Cauchy–Schwarz inequality, now over all selected segments, gives

    sum_sigma J_sigma² |sigma|²/m_sigma
      >= (sum_sigma |J_sigma| |sigma|)² / sum_sigma m_sigma.

At each level j there are4^j segments, each contributing2*4^−j in (8). Thus the numerator is(2n)², and (9)–(10) yield

    sum_{selected fine edges} J_e² |e|² >= c_1 n² 4^−n.    (11)

Apply (2) on T* with those selected fine edges. Uniform shape regularity makes its constant independent of n and the chosen T. For every g in P_0(T),

    ||S_n−g||_{H^−1} >= c_2 n 2^−n.

Finally use (5) and the reverse triangle inequality:

    ||f−g||_{H^−1} >= [c_2 n−2/sqrt(3)]2^−n.              (12)

The lower bound is uniform over all admissible T with at most4^n triangles and all their piecewise constants. Taking infima proves (1). Since sqrt(4^n)=2^n, the normalized best error is unbounded. This refutes the source's universal implication including s=1/2.

## 5. Scope, validation and attribution

The result is an endpoint counterexample for homogeneous Dirichlet Poisson on a square and the source's shape-regular newest-vertex-bisection family. It is enough to refute the assertion quantified over0<s<=1/2. It does not claim failure for every0<s<1/2, does not identify the source's P_0 approximation class with the different estimator class in the cited paper, and makes no claim about unrestricted anisotropic triangulations or an algorithm's optimality.

The construction, refinement-cost mechanism and endpoint motivation are explicitly credited to Cohen–DeVore–Nochetto. The finite checker verifies exact reference-element bubble means, traces and energy integrals, the selected-edge jump/scaling and geometric tail sums, plus the allocation inequality used in (9)–(11). These are controls, not a finite-mesh search standing in for the uniform proof above.

The inherited native runtime was used unchanged; its exact model identifier was not exposed. No priority or human peer-review claim is made. Independent adversarial review must validate the original dual norm, all-mesh lower bound and endpoint scope before a result PR.

### Primary references

- Stevenson, original contribution, OWR24/2005, pp.1306–1307: https://ems.press/content/serial-article-files/45998?nt=1
- Cohen–DeVore–Nochetto, complete author preprint, Section6.4 and mesh/overlay facts: https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf
- Published article metadata: https://doi.org/10.1007/s10208-012-9120-1
