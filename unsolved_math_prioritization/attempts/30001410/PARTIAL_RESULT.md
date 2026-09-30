# Crofton length: planar source correction and a simplex obstruction

Status: source-dimension hold; the intended higher-dimensional ellipsoid-only conjecture remains unresolved, 2/5. Under the natural domain-local Crofton-measure convention defined below, the dimension-unqualified assertion is already false in dimension two. A conflicting global-local-finiteness phrase in a cited paper requires the explicit source qualification in Section 1. This package supplies an explicit planar certificate and a five-point obstruction for every simplex of dimension at least three. Independent review pending. No novelty claim.

## 1. Exact scope of the original source

Rolf Schneider, “Crofton formulae and zonoids,” Oberwolfach Report 04/2010, printed pp.150–153, defines a Crofton measure for k-area by integrating intersection counts against a measure on affine (n-k)-flats. For curve length, those flats are affine hyperplanes; they are lines only when n=2. Signed measures are allowed in the general definition, but the concluding conjecture expressly requires a positive measure. It asks for existence, not uniqueness. The volume convention is Holmes–Thompson, denoted vol_k. Source: https://ems.press/content/serial-article-files/46262?nt=1 .

The final unqualified sentence says positivity for vol_1 in a Hilbert geometry forces an ellipsoid. Yet immediately above, a theorem gives a positive measure for vol_(n-1) in every projective Finsler space; at n=2 this is exactly vol_1. The motivating preceding sentence discusses k<n-1, which suggests the intended dimension n>=3, but the concluding sentence and dataset omit that restriction. We preserve both facts rather than silently rewriting the source.

The known planar exception is explicit in Schneider, *Crofton Measures in Polytopal Hilbert Geometries*, Beiträge Algebra Geom.47 (2006),479–488, https://home.mathematik.uni-freiburg.de/rschnei/Polytopal.Hilbert.pdf . It constructs positive line measures for hypersurface area and credits earlier planar work. Its higher-dimensional line measure concerns vol_(n-1), not curve length, so it is not a counterexample in n>=3. The metric convention in its equation (2) is the full logarithm of the cross ratio, without a factor one-half. We use that convention; scaling lengths by one-half just rescales every measure and inequality below.

There is a second source-convention issue. The 2006 polytopal paper, printed manuscript p.3, defines its line measure as locally finite on the entire affine Grassmannian A(n,1). Our planar measure does not meet that global condition. In fact, for positive hyperplane measures representing Hilbert curve length in a bounded domain, global local finiteness would be impossible even for ellipsoids: the set of all hyperplanes meeting the closure of a bounded convex body is compact (unoriented unit normal and bounded offset parameterization). A globally Radon measure has finite mass on this set. Except for hyperplanes containing a fixed segment, whose mass must be zero if its intersection-count integral is finite, each hyperplane meets that segment at most once. All segment lengths would therefore be uniformly bounded by this finite mass. Hilbert distances instead tend to infinity along a chord approaching its boundary endpoint. In dimension two these are exactly the line and curve-length conventions in question. Thus the printed global condition and claimed complete-domain existence cannot both be read literally without qualification. We use the natural domain-local space H(D) of hyperplanes meeting the open domain D. We do not assert a correction of the author’s intent or a counterexample under the incompatible global convention.

We work inside a bounded convex body with nonempty interior, not on its boundary. Holmes–Thompson one-dimensional volume agrees with the Finsler curve length. No smoothness of the boundary is assumed in the report's generalized Finsler setting.

## 2. Simplex cross-ratio formula

Use the affine hyperplane sum_{i=0}^n p_i=1 and the open simplex p_i>0. Its dimension is n. For p,q in this simplex,

d(p,q)=max_i log(p_i/q_i)-min_i log(p_i/q_i).

Here is a direct cross-ratio verification. Write r_i=q_i/p_i, m=min r_i, M=max r_i. For distinct points, m<1<M because sum p_i r_i=1. Along z(t)=p+t(q-p), the two boundary parameters are A=-1/(M-1)<0 and B=1/(1-m)>1. The cross ratio in the stated convention is B(1-A)/((B-1)(-A))=M/m. Taking logs gives the formula. Thus no external simplex-isometry theorem is needed for the distances used below.

The corresponding tangent norm is F(p,v)=max_i(v_i/p_i)-min_i(v_i/p_i), with sum v_i=0, by differentiation of the displayed distance formula.

## 3. Explicit positive planar line measure

For n=2, define h_ij(p)=log(p_i/p_j), 0<=i<j<=2. For three real numbers u_0,u_1,u_2,

max u_i-min u_i = (|u_0-u_1|+|u_0-u_2|+|u_1-u_2|)/2.

Consequently

d(p,q) = (1/2) sum_{i<j} |h_ij(p)-h_ij(q)|.

For each real t, the level h_ij=t is the intersection with the affine line p_i=e^t p_j. Let H(D) be the open subset of the affine line space consisting of lines meeting the open triangle D. Let mu be one-half the sum, over these three pairs, of the pushforwards of Lebesgue measure dt to H(D). It is positive and Radon on H(D). Indeed, each parameterized line family is continuous and its t-to-plus/minus-infinity limits are boundary-side lines outside H(D), so the inverse image of a compact subset of H(D) is bounded and closed. Equivalently, it has finite mass on lines meeting each fixed compact subset of D, since each h_ij has bounded range there. It is not locally finite on the entire affine Grassmannian: an infinite Lebesgue tail accumulates at a boundary-side line.

For a segment [p,q], its intersection count with that level line is one exactly for t between its endpoint h_ij values, except endpoint levels and a possible constant level, which form a Lebesgue-null set. Thus integrating the count gives the displayed distance formula. This is the interior segment-count identity; it does not satisfy the cited paper’s printed global-local-finiteness condition.

The same measure gives the full curve-length formula on one-dimensional rectifiable subsets M of the open simplex. Indeed the tangent identity is F(p,v)=(1/2)sum_{i<j}|d h_ij(p)v|. Applying the one-dimensional coarea formula to each locally Lipschitz h_ij on a countable compact exhaustion yields length_F(M)=(1/2)sum_{i<j} integral card(M intersect {h_ij=t})dt. Noncompact or infinite-length cases follow by monotone convergence. For parametrized curves, both length and intersections must instead be counted with the same traversal multiplicity. We do not mix these conventions.

The triangle is not an ellipsoid, so under the domain-local measure convention this is an explicit certificate of the already-known planar exception. It is not a resolution of the inferred n>=3 conjecture. The standard coarea theorem used to extend the segment identity to arbitrary rectifiable sets is imported, not re-proved here.

## 4. Positive hyperplane Crofton length forces integer hypermetric inequalities

Suppose a positive measure mu on affine hyperplanes represents the lengths of all segments in an open convex domain by intersection counts. Hyperplanes through a fixed interior point x have measure zero. To see this without assuming singleton sets are included, take nested nondegenerate closed segments centered at x with lengths tending to zero. Every such hyperplane meets each segment, with count at least one (possibly infinity), so its measure is bounded above by each segment length and is zero.

Fix points x_1,...,x_m and integers b_i with sum b_i=1. Almost every hyperplane avoids all these finitely many points. It cuts them into two sides I and I^c, and its segment intersection count is one exactly for pairs on opposite sides. Write s=sum_{i in I}b_i, an integer. Then

sum_{i<j} b_i b_j 1{hyperplane separates x_i,x_j} = s(1-s) <= 0.

Each of the finitely many individual segment counts has finite integral, so the signed finite sum is integrable. Integrating gives

sum_{i<j} b_i b_j d(x_i,x_j) <= 0.

Positivity of mu is indispensable. This argument gives no obstruction to signed Crofton measures.

## 5. An exact five-point obstruction for every n-simplex, n>=3

In R^(n+1), let the following exponent vectors have all unspecified coordinates zero:

u_0=(0,0,0,0,...), u_1=(0,0,1,0,...), u_2=(0,1,0,0,...),
u_3=(1,0,0,0,...), u_4=(1,1,1,0,...).

Define interior simplex points p(u)_i=2^(u_i)/(sum_j 2^(u_j)). All their coordinates are rational. The normalizing factors add a constant to all log coordinate ratios and hence cancel in the maximum-minus-minimum formula. Distances divided by log 2 are the exact integer matrix

[ [0,1,1,1,1],
  [1,0,2,2,1],
  [1,2,0,2,1],
  [1,2,2,0,1],
  [1,1,1,1,0] ].

For b=(-1,1,1,1,-1), whose sum is one, the weighted distance sum is (3 times 2 + 1 - 6) log 2 = log 2 >0. This contradicts Section 4. Therefore no positive hyperplane Crofton measure for curve length exists in an n-simplex for any n>=3. The proof is a finite certificate valid in every dimension, not an extrapolation from a numerical sample.

The certificate is quantitatively stable at the metric level: if all ten pairwise distances are changed by less than epsilon, the weighted sum changes by less than 10 epsilon. It stays positive when epsilon<(log 2)/10. This conditional statement requires actual pairwise-distance control; it is not an unproved blanket assertion about all domain perturbations.

## 6. Remaining question and verification boundary

Under the domain-local measure convention, the n=2 omission has the planar exception above, consistent with the report’s preceding existence theorem. The cited polytopal paper’s global-local-finiteness phrase remains a source inconsistency; no globally Radon planar counterexample is claimed. The intended n>=3 ellipsoid-only assertion remains unresolved for general convex bodies. Excluding all simplices does not exclude every nonellipsoid. We make no claim that every nonellipsoid contains an isometric simplex or this five-point metric, and no conclusion about uniqueness of Crofton measures. The source's higher-dimensional positive hypersurface formula remains compatible with our negative curve-length result.

The exact checker verifies all 32 cuts in the five-point inequality, rational simplex coordinates, cross-ratio ratios, the all-dimensional exponent embedding over a finite range, the three-number variation identity, and exact finite segment-level incidence controls. Infinite coarea and the all-size proofs are logical arguments in this note, not executable geometry. No priority or human peer-review claim.
