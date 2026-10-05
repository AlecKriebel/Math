# Gromov Question 64: a credited smooth-category implication

Target: 6700060 / AMR-066-0060, ranked 702. Prepared 2026-10-05.

## Status and credit

This is a proof-application and verification record, not a new theorem or a claim of priority. The all-dimensional implication below uses Yuchen Bi, *Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, arXiv:2608.06320v1, Theorem 1.1. That manuscript is a recent preprint. The author of this packet inspected its complete argument and its principal published index-theory dependency, finding no unresolved step in the application under the precise smooth convention below. A fresh independent mathematical/source audit remains required before assigning a settled repository status.

The older Wang–Xie–Yu route is not the basis for an unconditional disposition here: a July 2026 update by Bär–Hanke–Schick explicitly says WXY version 6 remains under verification. See SOURCE_STATUS.md.

## 1. Exact mathematical target and conventions

Gromov's 2017 *101 Questions, Problems and Conjectures about Scalar Curvature*, §22, printed p.60, defines extremality by comparing a compact, full-dimensional convex polyhedron P in R^n with convex polyhedra of the same combinatorial type: simultaneous nonincrease of the corresponding interior dihedral angles must force equality. Question 64 asks whether this implies the analogous property for smoothly deformed domains with nonnegative face mean curvature. Its prohibited competitor has all corresponding interior dihedral angles at most the reference angles, with strict inequality at even one point. No prescribed face metric, volume, edge length, or distance-decreasing map is required. Source: https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf

Here “diffeomorphic” has its usual smooth polyhedral-domain meaning: there is a face-preserving smooth diffeomorphism F:P→P', with smooth inverse, in charts locally extending to open subsets of R^n. Equivalently for this argument, its differential is nonsingular up to every stratum and its pullback Euclidean metric is smooth and positive definite up to the corners. Faces are smooth hypersurface pieces, and their intersections have the reference face incidences. This is not merely a homeomorphism or an interior diffeomorphism singular at a vertex. Such weaker interpretations are not certified by this packet.

Mean curvature is the trace of the second fundamental form for the outward unit normal, with the boundary of a Euclidean ball positive. Dividing by n−1 would not change any sign or zero conclusion. Dihedral angles are interior wedge angles, not the possibly supplementary angle between unoriented hyperplanes. The comparison ensures that competitor angles are below π.

## 2. Imported theorem, with the needed conclusion only

Bi's Theorem 1.1 concerns n≥3, a compact full-dimensional convex polytope P, and a smooth metric g on a neighborhood of P. If R_g≥0, every facet has H_g≥0, and interior dihedral angles are no larger than their Euclidean values, it concludes equality of the corresponding normal inner products on intersecting facets. Thus, in particular, all corresponding dihedral angles agree. It also proves flatness and totally geodesic facets, but neither strengthening is needed here. There is no simple-polytope, acute-angle, dimension-upper-bound, or additional spin hypothesis in this stated theorem. https://arxiv.org/abs/2608.06320v1

## 3. Pullback and neighborhood extension

Suppose a prohibited smooth competitor P' exists, with F as above. On P set

    g_x(v,w) = <dF_x(v), dF_x(w)>_Euclidean.

The differential is invertible, so g is positive definite. Local smooth extensions of F give local smooth extensions of g. These can be combined into one metric on a neighborhood of P as follows. Cover the compact set P by finitely many extension charts. Shrink each so that the extended metric is positive definite throughout. Choose a smooth partition of unity subordinate to those charts on a neighborhood of P and take the weighted sum of the local tensors. At each point of P all the local tensors equal g, so their sum restricts to g. A convex combination of positive-definite symmetric tensors is positive definite. This supplies precisely the neighborhood metric required by the imported theorem; no claim about its curvature outside P is needed.

The map F:(P,g)→(P',Euclidean) is an isometry by definition. On the interior, scalar curvature is therefore identically zero. Smoothness extends this zero value to the boundary. The isometry sends the outward side of a facet to the outward side of the corresponding facet. It consequently carries the outward unit normal, induced connection, second fundamental form, and its trace to the corresponding Euclidean objects on P'. Hence

    H_g(Q_i)(x) = H_Euclidean(Q'_i)(F(x)) ≥ 0.

The differential also preserves inner products of normals to adjacent faces. If θ is the interior dihedral angle and α the angle between outward unit normals, then θ=π−α. Thus the competitor inequality θ'_ij≤θ_ij(P) is exactly α^g_ij≥α^0_ij, which is Bi's convention. One strict interior inequality is equivalent to one strict reversed exterior inequality. The all-point nature of the hypothesis and of this implication is preserved.

All assumptions of the imported theorem hold. Its angle equality contradicts the stipulated strict inequality. Therefore no prohibited competitor exists for n≥3.

P was arbitrary: its convex-extremal property was not used. Under the smooth convention above, the imported theorem implies the requested affirmative answer and in fact the stronger mean-convex extremality statement for every compact full-dimensional convex P. This does not assert that every combinatorial equivalence between nonsimple polytopes is a smooth corner diffeomorphism.

## 4. Dimension two, proved separately

Let P be a convex m-gon. Write its interior angles θ_i, so that Σ_i(π−θ_i)=2π. Suppose P' is a smoothly face-preserving diffeomorphic planar competitor. It is a disk with a piecewise smooth Jordan boundary. Traverse that boundary counterclockwise. Its signed turning curvature k on smooth arcs equals the outward-normal mean curvature in the convention fixed above: the round circle has k>0. The turning-angle theorem, equivalently Gauss–Bonnet with zero interior curvature, gives

    Σ_i(π−θ'_i) + ∫_(smooth boundary) k ds = 2π.

Every θ'_i≤θ_i, so the sum on the left is at least 2π. Moreover k≥0. Equality therefore forces θ'_i=θ_i for every vertex and ∫k ds=0. The continuity and nonnegativity of k on each smooth arc imply k=0 there. In particular no angle can be strictly smaller. This proves the target in dimension two independently of the higher-dimensional imported theorem. In dimension one there is no codimension-two face at which the required strict inequality could occur, so the stated obstruction is vacuous.

## 5. Scope controls

- Pulling back Euclidean geometry gives R_g=0, not merely an assumed nonnegative scalar curvature.
- No distance, area, or boundary isometry comparison with the *reference Euclidean metric on P* is inserted. The pullback isometry is with P'.
- The reference P supplies a trivial tangent bundle and an orientation. Its contractibility and its diffeomorphic competitor do not introduce a nonspin obstruction. This is why no extra spin condition on the original target is being hidden.
- Convexity is imposed on the reference polytope only. The deformed facets need only have H≥0; their full second fundamental forms need not be nonnegative.
- Corners with more than n incident facets are permitted under the smooth chart convention. No assumption that P is simple is used.
- Equality of every angle, rather than intrinsic flatness alone, is the needed conclusion: the competitor metric is already flat. A theorem asserting only flatness would not finish this argument.
- The result is not extended to C^0 metrics, arbitrary nonsmooth domains, branched or merely continuous face maps, different topology, or weak distributional curvature notions.

## 6. What has and has not been certified

The deduction from the specified source theorem is complete. The dimension-two proof is complete. The attached verification note records the author's proof-level checks of the newer source and the published smooth-boundary Dirac input. These checks are AI-assisted mathematical review, not formal verification or human peer review. The exact finite controls test algebraic conventions and packaging only. They do not establish a PDE index theorem or certify the source manuscript's community acceptance.
