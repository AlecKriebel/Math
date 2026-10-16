# A coloured-cycle comparison in degree three

Status: corrected partial theorem accepted by the independent mathematical audit. This does not settle equality of the two seminorms. No priority or novelty claim is made.

Write p_X(alpha)=||alpha||_1. Write G_X(alpha) for the infimum of sum_j |a_j| ||M_j|| over exact finite expressions alpha=sum_j a_j(f_j)_*[M_j]_R by oriented closed connected 3-manifolds and continuous maps. Let v_3 and v_8 be the volumes of the regular ideal hyperbolic tetrahedron and octahedron, respectively.

## Claim

For every topological space X and every alpha in H_3(X;R),

    p_X(alpha) <= G_X(alpha) <= (v_8/v_3) p_X(alpha).

In particular the two seminorms have exactly the same zero classes. The claimed upper factor is approximately 3.60992. The ratio is exact; decimal values are illustrative only.

## Explicit source interfaces

1. Crowley–Löh, *Functorial semi-norms on singular homology and (in)flexible manifolds*, Theorem 4.2 and Corollary 3.2: G is a finite functorial seminorm. On a path-connected target, rational classes are scalar images of connected-manifold fundamental classes. For an arbitrary target, split a class over its finitely many relevant path components and use a finite sum of such images. Every real class is a finite real linear combination of rational classes. Author manuscript, pp. 7–9: https://loeh.app.uni-regensburg.de/preprints/funcseminorms.pdf .
2. Löh–Moraschini, *Simplicial volume via normalised cycles*, arXiv:2003.02584v2, Lemmas 3.2–3.3 state the result over real coefficients for the chain operator

       S_n(sigma) = 1/(n+1)! sum_{pi in S_(n+1)} sign(pi) sigma o pi

   is chain homotopic to the identity over R, has operator norm at most 1, and satisfies partial_j(S_n c)=0 for every j when c is a cycle. Its displayed formula also preserves rational chains. Rational output and preservation of the real homology class are exactly what this proof needs; no separate rational chain-homotopy claim is required. Their Connes–Consani equality is not asserted to equal the present generated seminorm. https://arxiv.org/abs/2003.02584v2 .
3. Gaifullin's coloured realization, in the explicit form stated by Lafont–Pittet, *Comparing seminorms on homology*, pp. 376–377: if P is an oriented closed regularly (n+1)-coloured n-dimensional pseudomanifold with K top simplices, there are a finite cover pi:N→T_n of the Tomei manifold and a map h:N→P, with h_*[N]=q[P], q>0, and

       degree(pi)/q = K/2^n.

   The covers may be disconnected. The published text on p. 377 explicitly states that the construction also applies to regularly coloured Delta-complexes; a simplicial complex is not required. For disconnected P apply this statement separately to its finitely many components. The formula follows from degree(pi)=K B/2 and q=2^(n-1)B, with B a positive integer. Gaifullin's original 2-page construction also gives these counts; its2012 paper gives the equivalent tile count qK=2^n degree(pi). https://people.math.osu.edu/lafont.1/pjm-259.pdf ; https://arxiv.org/abs/0806.3580 ; https://arxiv.org/abs/1204.0208 .
4. Lafont–Pittet, Lemma A.2: ||T_3||=8v_8/v_3. Simplicial volume is multiplicative under finite covers and additive on disjoint unions.

## Proof

### 1. Lower bound and finite-dimensional continuity

For any allowed finite expression, functoriality and the triangle inequality for p give

    p_X(alpha) <= sum_j |a_j| p_X((f_j)_*[M_j])
               <= sum_j |a_j| ||M_j||.

Taking the infimum proves p_X<=G_X. Both are finite seminorms. If beta_1,...,beta_s are fixed rational classes and t_i^(r)→t_i, then, for either seminorm F=p_X or G_X,

    F(sum_i (t_i^(r)-t_i) beta_i)
       <= sum_i |t_i^(r)-t_i| F(beta_i) → 0.

Consequently proving an inequality G_X<=C p_X on rational classes proves it on all real classes, because every real class belongs to a finite real span of rational classes. This argument uses explicit finite-dimensional seminorm convergence, rather than a topology on the full possibly infinite-dimensional homology group.

### 2. Rational near-minimal cycles

Let beta be a rational class, represented by a fixed rational cycle z. For every epsilon>0 there is a rational cycle c representing beta over R with

    ||c||_1 < p_X(beta)+epsilon.

Here is an exact justification for rational coefficients. Start with a real near-minimal c_0 and a finite real 4-chain b_0 with c_0-z=partial b_0. Use the finite 3-simplex support containing c_0, z, and every face in partial b_0, together with the finite 4-simplex support of b_0. On these supports, the equation c-z=partial b is an affine linear system with rational coefficients and rational right-hand side. A nonempty real solution set of such a system has a rational point and a rational basis for its direction space, by Gaussian elimination over Q. Thus rational solutions are dense in it. Choose a rational solution close enough to (c_0,b_0) to retain the strict norm bound. The equation itself, and therefore the represented class, remain exact.

### 3. Coloured realization without subdivision

Apply S_3 to c. Put c'=S_3 c. Then c' is rational, homologous to c, ||c'||_1<=||c||_1, and partial_i c'=0 separately for i=0,1,2,3. Choose a positive denominator m such that

    m c' = sum_sigma n_sigma sigma,

with integral n_sigma, in reduced form. Take |n_sigma| copies of the standard tetrahedron, oriented by sign(n_sigma), each mapped by sigma to X. Give its vertex in position i the colour i.

Fix i and a singular 2-simplex tau. The equation partial_i(mc')=0 says that the number of positive copies whose ith face is tau equals the number of negative such copies. Pair these occurrences. Identify each matched pair of faces by the identity in their standard face coordinates. Do this separately for every i and tau.

Each face is paired exactly once. Paired faces induce opposite orientations because they have the same omitted index and opposite tetrahedron signs. All gluings preserve vertex colours. Hence the quotient P is an oriented closed, regularly 4-coloured, finite face-paired 3-dimensional Delta-pseudomanifold. No tetrahedron is subdivided. Here a Delta-pseudomanifold means a finite pure Delta-complex with every codimension-one open face incident to exactly two top-simplex faces, coherent orientations, and connected top-simplex adjacency graph on each component; normality of lower links is not required. Colour-preserving gluings cannot identify two vertices of one tetrahedron or two different faces of that tetrahedron having distinct colour sets. They thus introduce no self-folding of a simplex. Form the quotient separately on each dual-graph component and retain the disjoint union. Each component is strongly connected, and its signed top-simplex chain is its integral fundamental cycle. The map to X descends continuously because paired singular face maps are literally equal. With the specified orientations, its top cycle pushes forward exactly to mc'. Thus, writing P as the disjoint union of its components P_l,

    sum_l g_*[P_l]_R = m beta,
    K := sum_l K_l = sum_sigma |n_sigma| = m||c'||_1.

The colours are attached to the tetrahedron positions, not to vertices of X. Different vertices of X may be equal, and identical singular face maps may occur at different omitted indices; neither affects the construction because only equal omitted indices are paired.

### 4. Quantified manifold cost

Apply the source interface to each P_l. Obtain pi_l:N_l→T_3 and h_l:N_l→P_l with

    (h_l)_*[N_l]=q_l[P_l],
    d_l/q_l=K_l/8,     d_l=degree(pi_l), q_l>0.

All N_l are oriented closed manifolds; if disconnected, split them into their connected components when forming an admissible expression for G. The exact real homology expression is

    beta = sum_l 1/(m q_l) (g_l h_l)_*[N_l]_R.

Its total cost is

    sum_l ||N_l||/(m q_l)
      = sum_l d_l||T_3||/(m q_l)
      = K||T_3||/(8m)
      = (v_8/v_3)||c'||_1
      <= (v_8/v_3)(p_X(beta)+epsilon).

Let epsilon decrease to zero. This proves the upper bound for rational classes. Step 1 gives it for all real classes. If beta=0, use G_X(0)=0 rather than a nonempty pseudomanifold construction. No integral-class identity after clearing denominators is needed here: the exact real identity is precisely the requested one. This avoids a possible torsion ambiguity.

## Why this is only partial

The factor v_8/v_3 is greater than 1. The colouring argument removes the factorial subdivision cost; it does not remove the cost per permutahedral tile in Gaifullin's realization. Normalized cycles still can have nonspherical vertex links, so they need not be manifold cycles. The equality problem requires a further asymptotically unit-cost realization, or a different argument. A fixed positive comparison factor does not imply equality.
