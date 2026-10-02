# Turn 4: a non-isometric conformal metric-refinement scheme

Problem 30002820. Fourth substantive author turn. **A complete positive construction is given for the printed output-metric definition, with an essential non-isometry qualification. The intended isometric/geometric question is not claimed solved.** Source-formulation uncertainty remains; this packet's final disposition requires source-specific independent review.

The construction is neither the identity nor a metric-independent constant output. It properly subdivides every old edge, preserves each old edge's total length, produces valid Euclidean triangles, and extends the original conformal vertex factors exactly. It necessarily changes lengths inside old faces.

## 1. One elementary edge split

Let ij be an edge of a triangulated surface with a positive nondegenerate Euclidean metric l. Choose one incident triangle ijk by a fixed rule depending only on the current combinatorics, not on l. For a boundary edge there is only one choice; for an interior edge either choice is allowed. Set

    r=l_ik/l_jk,        t=r/(1+r)∈(0,1).                     (1)

The orientation i→j is arbitrary; reversing it replaces r by 1/r and t by 1−t and gives the same lengths below. Insert a new vertex m on edge ij and replace every incident triangle ijq by imq and mjq. Retain all unaffected edge lengths and assign

    l′_im=t l_ij,       l′_mj=(1−t)l_ij,
    l′_mq=(1−t)l_iq+t l_jq                                 (2)

for each opposite vertex q of an incident triangle. If there are two incident triangles, they use the same t and the same im,mj lengths. Thus the metric assignments glue.

This is a stellar subdivision of the underlying complex. One may choose a fixed interior barycentric point of ij for the underlying subdivision and then equip the new complex with (2). Alternatively, on each input realization one may place m at old edge distance t l_ij; these realizations have the same labelled combinatorics. Only the latter convention preserves the old edge's metric pointwise; both preserve its total length and satisfy the source's combinatorial subdivision condition. No interior-face isometry is asserted.

A symmetric optional version of(1) uses the geometric mean of l_iq/l_jq over both incident triangles. Its covariance proof is identical. The designated-triangle version is sufficient for existence and keeps rational input computations rational; symmetry under every relabelling is not claimed for an arbitrary choice rule.

## 2. Every new triangle is nondegenerate

In an incident triangle put a=l_jq, b=l_iq, c=l_ij and h=(1−t)b+t a. For the triangle imq, whose sides are b,tc,h, the three strict inequality margins are

    b+tc−h = t(b+c−a),
    h+tc−b = t(a+c−b),
    b+h−tc = 2(1−t)b+t(a+b−c).

All are positive because 0<t<1 and the old triangle is nondegenerate. The three analogous margins for mjq are

    a+(1−t)c−h = (1−t)(a+c−b),
    h+(1−t)c−a = (1−t)(b+c−a),
    a+h−(1−t)c = 2t a+(1−t)(a+b−c),

also positive. Thus (2) is a globally valid Euclidean triangle metric, not just a positive edge assignment. The old edge's total length is unchanged, and every new edge is at most the largest side of its incident old triangle.

## 3. Exact conformal covariance, preserving all old factors

Suppose another valid metric has mu_uv=a_u a_v l_uv with a_u>0, so a_u=exp(u_u/2) in the source notation. The same combinatorial choice of incident triangle gives

    r_mu=(a_i/a_j)r,
    t_mu = a_i t / D,       1−t_mu = a_j(1−t)/D,
    D = a_i t+a_j(1−t)>0.                                 (3)

Leave all old multipliers a_u unchanged and assign to the inserted vertex

    a_m=a_i a_j/D.                                         (4)

For the first child edge, mu′_im=t_mu mu_ij=a_i a_m l′_im; the second gives mu′_mj=a_m a_j l′_mj. For **every** incident opposite vertex q, even if it was not used to define t,

    mu′_mq=(1−t_mu)mu_iq+t_mu mu_jq
           =a_q a_i a_j[(1−t)l_iq+t l_jq]/D
           =a_m a_q l′_mq.                                (5)

All unaffected edges retain their old scaling equation. Equations (3)–(5) prove that the elementary operation preserves discrete conformal equivalence and extends the original factors rather than replacing them by unrelated ones.

## 4. One proper whole-surface pass

To obtain a finite-round scheme subdividing **every** old edge, form the conflict graph whose vertices are the old edges, joining two when they belong to a common old triangle. Each old edge has at most four conflict neighbors, so a fixed greedy combinatorial ordering gives a proper coloring with at most five colors. Fix this coloring independently of the metric.

Process the five colors in order. In each round split all original edges of that color by (1)–(2), using the current metric and current incident triangles, with combinatorial tie-breaking fixed in advance. Edges of one color never lie in the same old face, hence cannot lie in one current face: every current face stays inside its old face. Their affected face interiors are disjoint, so the operations can be performed in parallel and commute within the round. Sharing an old endpoint causes no conflict, since the old vertex and all its other edge lengths remain unchanged by that split.

Every original edge persists until its own round and is split exactly once; newly inserted edges are not processed during this pass. Every original triangle is split successively along its three boundary edges and has four child triangles at the end. The resulting pattern is generally **not** the medial pattern with a central triangle used in turn 3. The pass is proper, with one new vertex per old edge and old edge totals exactly preserved. Since each elementary step produces valid metrics and extends conformal factors, their composition has both properties. Both outputs have identical labelled combinatorics because the coloring and choices are independent of the metric.

This gives a five-round composition of local elementary operations. Its choices may depend on a combinatorial ordering/coloring; canonical relabelling invariance is not asserted. On a locally finite countable triangulation, the same bounded-degree conflict coloring and five simultaneous rounds are well-defined, since only finitely many operations affect each old face. For the finite meshes used in the exact checker this is an explicit terminating algorithm. No claim about convergence or smoothness of iterated passes is needed for this one-pass result.

The construction satisfies the printed definition of a map from a metrized simplicial complex to a subdivision equipped with a metric, and it has the additional edge-total and old-factor interpolation properties. It does not satisfy an additional requirement that the new metric induce the original metric on each old face.

## 5. Exact amount of non-isometry

Place m at old metric fraction t on ij in the original Euclidean triangle. Its actual squared distance to q would be

    h_E²=(1−t)b²+t a²−t(1−t)c².

The assigned h in (2) instead satisfies the exact identity

    h²−h_E²=t(1−t)[c²−(a−b)²] > 0.                         (6)

The strict inequality is exactly the old triangle inequality c>|a−b|. Thus the new diagonal is always strictly longer than its induced Euclidean value in a nondegenerate old face. This is not a tiny-roundoff or limiting exception. On a unit equilateral triangle with t=1/2, the assigned diagonal is 1 while the induced diagonal is sqrt(3)/2.

Accordingly, this is not an isometric subdivision of the original piecewise-flat surface. Preserving edge totals and old vertex factors is weaker than preserving its intrinsic face metric. A source interpretation that requires the latter is not answered by this construction.

## 6. Source context and disposition qualification

Bauer's exact printed definition, OWR 13/2015 pp.721–722, https://ems.press/content/serial-article-files/46561 , does not explicitly specify metric compatibility, and Rote's primary reproduction adds none. The surrounding context and the reference to barycentric subdivision make an induced/isometric interpretation plausible; that intended extra requirement has not been verified or dismissed. The construction above must therefore be described as a positive theorem for the stated output-metric interpretation, with changed face interiors, rather than a resolution of an unspecified stronger geometric problem.

The conformal vertex-scaling framework is credited to Luo and Bobenko–Pinkall–Springborn, https://arxiv.org/abs/1005.2698 . The edge-split formulas and full covariance/triangle proofs are supplied here without a historical novelty claim. No statement about iterative contraction, convergence to a smooth conformal metric, angle preservation, or optimal mesh quality is made.

The exact checker independently runs the rule on each input metric, verifies all output triangle inequalities, original edge totals and final edgewise conformal equations, and checks (6). It uses rational arithmetic for the designated-triangle rule. The general proofs above, not the finite test count, establish existence on all nondegenerate inputs in the stated class.

Author turns completed: 4/5. Source's intended metric-compatible interpretation remains unresolved. Subjective completion estimate toward that intended question: 20%. The final turn will examine an additional genuinely isometric metric-dependent class, keeping it separate from this construction.
