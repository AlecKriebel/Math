# Recovery proof turn 3: the iterated-image route

2026-10-03. Recovery turn 3/5, historical count unknown. Original unresolved. Completion estimate 20%, subjective approach coverage. We try to contradict properness by iterating a missing region. The resulting quantitative criteria are rigorous, but their uniformity assumptions are not supplied by the source conjecture.

## Disjoint layers

Let X be a nonempty compact metric space, f:X→X a continuous injection, and U⊂X\f(X). Then the sets f^n(U), n≥0, are pairwise disjoint. If n<m and f^n(u)=f^m(v), injectivity gives u=f^(m−n)(v)∈f(X), contradicting u∈U. A proper image is compact, so X\f(X) contains a nonempty relatively open ball B(a,s).

## Quantitative distortion-collapse dichotomy

Write D=diam X>0. Suppose f^n is η_n-quasisymmetric, n≥0, with η_0(t)=t. Put d_n=diam f^n(X). For each n choose z_n∈X for which d(f^n(a),f^n(z_n))≥d_n/2; compactness guarantees a maximizer and the triangle inequality gives this bound. For every b∈X\U, d(a,b)≥s, whereas d(a,z_n)≤D. Quasisymmetry therefore implies

  d(f^n(a),f^n(b)) ≥ d_n / [2 η_n(D/s)].

Here z_n≠a whenever d_n>0; in the case b=z_n the same inequality is harmless since η_n(D/s)≥1. For m>n, f^m(a) belongs to f^n(f(X)), and f(X)⊂X\U. Thus the displayed lower bound applies with b=f^(m−n)(a).

Consequently for any index set I with d_n/[2η_n(D/s)]≥ε>0 at every n∈I, the points {f^n(a):n∈I} are ε-separated. Total boundedness of X makes I finite. In particular,

  diam f^n(X) / η_n(D/s) → 0.

This conclusion concerns the actual chosen distortion bounds. Inflating η_n artificially weakens it, never strengthens it.

If every iterate is η-quasisymmetric with the same η, properness forces diam f^n(X)→0. Since the nonempty compact sets f^n(X) are nested, their intersection is a single point p. Continuity gives f(p)=p. Moreover f^n converges uniformly to p, because both f^n(x) and p lie in f^n(X). Hence a uniformly quasisymmetric-iterate self-embedding of a compact space is either onto or has a global point attractor.

There is an explicit packing bound. If X has a measure μ satisfying μ(B(x,r))≥c_- r^Q at the radii in question, μ(X)=M<∞, then any finite set of iterates with d_n/[2η_n(D/s)]≥ε has cardinality at most M/[c_-(ε/3)^Q]: radius ε/3 balls around these points are pairwise disjoint. This estimate is valid even if their centers cluster near a metric boundary, because the assumed lower bound is for relative balls in X.

## An independent measure-decay obstruction

Let μ be Q-dimensional Hausdorff measure restricted to X, with 0<μ(X)=M<∞ and μ(B(a,s))=u>0. Suppose f^n satisfies the global lower Lipschitz bound d(f^n x,f^n y)≥λ_n d(x,y). The inverse on its image is λ_n^(-1)-Lipschitz, so the elementary Hausdorff-measure inequality yields μ(f^n U)≥λ_n^Q μ(U). These sets are Borel when U is open in compact X, since f^n is a homeomorphism onto a closed image. Disjointness gives

  μ(U) Σ_{n≥0} λ_n^Q ≤ M.

Therefore divergence of this series forces surjectivity. In particular, uniformly co-Lipschitz iterates are onto; so are iterates with λ_n≥c(n+1)^(-α) when αQ≤1. These statements use Hausdorff measure rather than silently treating an arbitrary Ahlfors-regular measure as exactly scale-covariant.

## Sharp countermodel to the naive iteration argument

For X=[0,1]^q with Euclidean metric and f(x)=x/2, every iterate is a similarity and is t-quasisymmetric. Nevertheless f is proper and its images collapse to 0. Lebesgue measure, equivalently a constant multiple of H^q, gives shell U=X\f(X) mass 1−2^(−q); λ_n=2^(−n), and the infinite series inequality is an equality. Thus iteration alone, even with perfectly controlled QS distortion, cannot rule out a proper embedding without a noncollapse input.

## Source-specific gap

For a general QS self-embedding of a Loewner group boundary, neither uniform control of all iterates nor a nonsummable lower metric bound is known here. Normalizing each image separately by ambient group elements destroys the relation f^m(X)⊂f^n(X) needed for the disjoint-layer argument; it is not legitimate to combine arbitrary normalizations with this proof. No claim that the cube is a group boundary is made. This route has produced exact necessary behavior for a counterexample, not the conjectured exclusion.
