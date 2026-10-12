# Exact adapters, controls and route status

This document compares logical hypotheses. It is validation of the sealed candidate and establishes no independent novelty claim. The original 1/5 research charge is unchanged.

## Full dependency chain required

Let T(K₁,K₂,K₃) be the affine lines meeting each convex set Kᵢ and contained in a supporting plane for it. The target is

    L³*( ⋃{ ℓ : ℓ ∈ T(K₁,K₂,K₃) } ) = 0.

An alleged equivalent prior theorem must verify all five links below, not merely a dimension count.

| Link | Exact assertion | Prior evidence found | Remaining adapter |
| --- | --- | --- | --- |
| Localization | Every original tritangent occurs among countably many triples of disjoint compact contact caps, preserving its actual three contacts | Elementary closure, rational-ball and support-plane localization used by candidate | Verify reductions if prior theorem assumes compactness, full dimension or closedness; closures of original disjoint sets need not stay disjoint |
| Bitangent covering | All bitangents of each pair of relevant arbitrary compact convex caps belong to countably many Lipschitz two-parameter line charts | Conditional Clarke adapter below; planar pointed-support rectifiability; WDC covers conditional on WDC hypothesis | Supply simultaneous cap geometry or prove a directly applicable WDC/DC/normal-cycle incidence theorem, including corners and flat contacts |
| Contact rank | At almost every density parameter q in each measurable tritangent subset E, and at the three distinct actual contact heights zᵢ, rank(Du(q)+zᵢDv(q)) ≤ 1 | Smooth focal/tangent-surface theory gives a classical analogue | Need density-point quantifiers for arbitrary nonsmooth convex support contacts and lower-dimensional cases, at a common nonexceptional q |
| Polynomial | det(Du+zDv) has degree at most two; three distinct roots force it to vanish for every z | Classical line-congruence mechanism; direct matrix algebra | No novelty assigned to the degree bound or three-root algebra |
| Sweep measure | Locally Lipschitz G(q,z)=(u(q)+zv(q),z) has zero Jacobian a.e. on E×bounded intervals, hence entire sweep is outer null after countable unions | Density, Rademacher and multiplicity area formula, independently inspected in Simon | Verify measurability, differentiability exceptions, products with height intervals, noninjectivity and full-line exhaustion |

A family is marked blocked below when invoking its general theorem merely replaces the bitangent or contact-rank problem by an equally unsupported hypothesis. This does not prove that no materially new adapter exists.

## Conditional adapter to Clarke's 1976 theorem

Assume the candidate's localized chart has coordinates (a,b,r), with r∈R², and locally Lipschitz signed support gaps g_A,g_B satisfying throughout an open neighborhood:

    m_A ≤ ∂ₐg_A,       |∂ᵦg_A| ≤ ε,
    m_B ≤ ∂ᵦg_B,       |∂ₐg_B| ≤ ε,
    m_A > 0, m_B > 0,  ε² < m_A m_B,

at ordinary differentiability points. Define

    H(a,b,r) = (g_A(a,b,r), g_B(a,b,r), r).

Every ordinary Jacobian, every limit of such Jacobians and every convex combination has block form

            [ α   c   *   * ]
    DH  =   [ d   β   *   * ]
            [ 0   0   1   0 ]
            [ 0   0   0   1 ],

where α≥m_A, β≥m_B and |c|,|d|≤ε. Consequently

    det DH = αβ − cd ≥ m_A m_B − ε² > 0.

Thus every element of the Clarke generalized Jacobian is nonsingular. Its [Theorem 1](https://msp.org/pjm/1976/64-1/pjm-v64-n1-p07-p.pdf), printed p.98, gives a local Lipschitz inverse. The map r↦H⁻¹(0,0,r) parameterizes the simultaneous-zero locus, and projection into affine line coordinates gives the desired local two-parameter chart.

This is a checkable replacement of the candidate's analytic inversion after its geometric inequalities. It establishes credit for the inverse theorem, not a historical solution of the conjecture. The unexplained hypotheses cannot be silently assumed at every nonsmooth bitangent; the rational cap construction and coverage/countability remain necessary.

## Independent-normal control for the common-normal / convex-hull route

Take three closed radius-one balls with centers

    c₁=(1,0,0),
    c₂=(−1/2,√3/2,3),
    c₃=(−1/2,−√3/2,6).

Their pairwise squared distances are 12,12,39, so they are pairwise disjoint. The vertical line ℓ={(0,0,z):z∈R} is at distance one from each center. It meets the three balls at (0,0,0),(0,0,3),(0,0,6), and each ball has a vertical supporting plane containing ℓ. Its unique outward contact normals are

    n₁=(−1,0,0),
    n₂=(1/2,−√3/2,0),
    n₃=(1/2,√3/2,0).

No two are parallel, including after a sign change. Thus the actual contacts do not supply the same outward normal required by Fu–Pokorný–Rataj Lemma 3.2. A higher-dimensional or variable transformation might produce a different encoding; the direct same-normal adapter fails on this concrete legal input.

No plane containing ℓ supports all three balls on a common side. A unit horizontal normal n for such a plane would require n·cᵢ,xy≥1 for all i, after choosing the side. Adding these inequalities contradicts c₁,xy+c₂,xy+c₃,xy=0. Accordingly ℓ is not made into a boundary segment of their convex hull simply by combining these balls. This blocks a direct appeal to the boundary-segment direction/normal theorem for that hull. It is a control for a proposed adapter, not a counterexample to target nullness.

## Why line-space nullness and genericity do not close the chain

The family of all vertical lines is parameterized by (x,y)∈R². It is a smooth two-dimensional set in four-dimensional affine line space and has zero four-dimensional invariant line measure. Its spatial union is all R³. Hence even a two-dimensional line-family bound requires a rank condition on the three-dimensional incidence projection; an invariant-measure-zero theorem alone is insufficient.

Rectifiability of two tangent hypersurfaces does not automatically control their intersection: two coincident smooth hypersurfaces retain their full dimension. Disjointness and distinct contact heights may supply additional geometry, but that geometry must appear in the actual theorem or adapter.

An a.e.-motion kinematic theorem allows exceptional fixed configurations. A general-position or positive-curvature theorem excludes precisely the boundary cases that need analysis. Approximating arbitrary convex sets by smooth or polyhedral sets also does not alone preserve nullness of swept unions; null sets can converge to a positive-measure set (finite grids approaching a cube are a basic control).

A line-space H²-null exceptional set can in principle be swept harmlessly: on bounded coordinate/height patches a Lipschitz incidence map and product-cover estimate can make its product with an interval H³-null. The earlier seal's warning asks that this control be supplied; it does not assert such exceptional sets are inherently fatal.

## Route status after actual-primary inspection

| Sealed family | Mechanism and evidence | Status | Exact gap / condition to reopen |
| --- | --- | --- | --- |
| Generalized implicit functions | Uniform positive diagonal and small cross derivatives imply every generalized Jacobian invertible | **Known ingredient; conditional adapter verified** | A historical source must supply the arbitrary-convex cap inequalities and all-bitangent coverage |
| DC touching / tangent hyperplanes | Null touching-plane sets; DC graph tangent-plane size estimates | **Blocked as exact prior adapter** | Encode independent tangent lines and their full spatial incidence into the source's specified DC graph without assuming the desired regularity |
| WDC structure | Finite DC covers when WDC and dimension hypotheses hold | **Blocked as exact prior adapter** | Prove the bitangent locus has the required aura/weak regularity and topological dimension; neither follows from arbitrary DC zero sets |
| Normal cycles / common normals | Rectifiable-current and finite-content geometry; strong common-outward-normal lemma | **Positive nearby theorem, direct adapter fails** | A new valid encoding must preserve independently oriented support contacts; the ball control above falsifies the naive encoding |
| Focal / developable sweep | Classical quadratic focal equation and smooth tangent-surface equivalence | **Known geometric mechanism; incomplete exact adapter** | Supply Lipschitz measurable density-subset rank statement and arbitrary-convex chart existence; avoid division by an identically zero determinant |
| Integral / kinematic geometry | Null flats in invariant parameter measure; intersections for a.e. motion | **Wrong conclusion/quantifier for direct resolution** | Obtain the spatial incidence projection's rank/null conclusion for every prescribed disjoint triple |
| Visibility / Grassmannian algebraic congruences | Smooth algebraic/generic event descriptions and singular-locus results | **Special-case credit** | Remove input restrictions with a proved limiting argument, not informal dimension counting |
| Planar pointed support | Rectifiable support curve including corners | **Known lower-dimensional analogue** | Verify simultaneous dependence on variable spatial slices and countable two-parameter coverage |
| Density / Rademacher / area | Standard measurable-subset, multiplicity-aware Jacobian implication | **Known ingredients directly applicable** | No missing analytic theorem after geometric cover and rank hypotheses; these are not themselves priority-clearing |

The strongest unresolved historical question in this mechanism family is the complete arbitrary-convex **bitangent cover plus density-contact rank** application. The audit neither certifies its novelty nor replaces the independently checked candidate proof.
