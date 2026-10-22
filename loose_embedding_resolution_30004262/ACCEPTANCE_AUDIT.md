# Adversarial mathematical audit: fixed-dimensional loose embeddings

Audit date: 2026-10-21. This is an independent mathematical assessment of the locally retrieved October 20, 2026 unrefereed manuscript by Alper Ferudun, *Loose Embeddings in a Fixed Euclidean Space: Countable Counterexamples and Flat Tori*. It is not a certification of priority or peer review.

Public manuscript: https://eulersolve.org/papers/owr-17288-004/paper.pdf

Inspected PDF SHA-256: `2d0142767650454c884d6543983836c4a6dde53f559b6a41b47c65cf0fb4ab5f`; length: 177653 bytes. The URL's displayed version identifier agrees with the prefix of this hash. This audit covers the local PDF's extracted full text, including the substantive proofs in Sections 2–7 and the scope/status statements in Sections 1, 8, and 9. It does not adopt the manuscript's reported verification runs as independent evidence.

## Verdict

No substantive mathematical error was found in Theorems A, B, C, Corollary D, or Proposition 5.1. The proofs support the following carefully separated conclusions:

1. For every fixed positive integer N, there exists a compact countable metric space with every finite subspace loosely embeddable in R^N, but with no continuous loose embedding of the entire space into that same R^N.
2. Every flat torus of intrinsic dimension at least two fails the finite-subspace hypothesis in every finite target dimension. Thus not every compact connected Riemannian manifold has the hypothesis.
3. The paper does not resolve whether the finite-subspace hypothesis in one fixed dimension guarantees a global loose embedding in some possibly larger finite dimension.
4. The countable examples do not refute ordinary uniform/topological embeddability in the same Euclidean dimension. Each is topologically a convergent sequence with its limit, and therefore admits a uniform embedding into R, hence into every R^N for N >= 1.

The mathematical arguments can be used as an audited candidate resolution of the corrected catalogue reading, with attribution to this unrefereed manuscript. They must not be presented as resolving the literal undefined wording of the Oberwolfach first question, or the distinct later finite-dimensional question, or as an established peer-reviewed/priority result.

## Exact hypotheses and variant table

Here LE means a **continuous** map phi for which, for every four points, equality of the two image distances holds if and only if equality of the two source distances holds. This includes preservation of unequal distances, and implies injectivity by comparing a pair with a zero-distance diagonal pair. It imposes no ordering or monotonicity requirement on distance classes.

H(N) means a single fixed N works for every finite subset. The finite embeddings may be chosen independently, with no common normalization, compatibility, distortion bounds, or continuity modulus.

| Question / reading | Audited outcome | Scope limitation |
| --- | --- | --- |
| H(N) implies continuous LE into the same R^N | Negative, for every N >= 1, by A/B | This is the corrected problem-record reading |
| H(N) implies ordinary uniform embedding into the same R^N | Not resolved by these examples | All X_N actually uniformly embed in R |
| H(N) implies LE into some finite-dimensional R^M | Not resolved | X_1 is positively LE into R^2; no conclusion for X_N when N >= 2 |
| Every compact connected Riemannian manifold satisfies H(N) for some N | Negative by every flat torus of intrinsic dimension >= 2 | Not a statement about every manifold failing H(N) |
| Every flat torus of intrinsic dimension >= 2 is LE into some finite-dimensional space | Negative | Applies to its geodesic flat metric, not a chord metric imported from an ambient embedding |
| Every compact metric space is LE into infinite-dimensional Hilbert space | Not addressed | Finite-dimensional compactness and representation arguments are essential |

The original OWR report, printed p. 2860, explicitly defines LE, but its first bullet uses the different and undefined phrase “uniformly embeddable” in its conclusion. This is a real textual ambiguity, not proof that the author meant the corrected reading. ArXiv:2101.01242 Definition 0.1 explicitly defines unqualified LE using *some* finite-dimensional Hilbert space, and Question 2.1 uses that unqualified conclusion. The journal renumbers it Question 3.1. Its second question asks whether compact Riemannian metric spaces satisfy the finite-subspace hypothesis and does match the torus result.

Primary context: https://doi.org/10.4171/owr/2019/45 and https://arxiv.org/abs/2101.01242 .

## Theorem A: all-pair audit and role of continuity

The space consists of p and points x_k, with d(p,x_k)=2^(-k), d(x_j,x_(j+1))=2^(-j), and d(x_j,x_k)=2^(-j)+2^(-k-1) when k >= j+2.

Metric verification: in a triangle involving p, the two radii sum exceeds the other side, and each radius is at most the maximum side. For i<j<k, the possibly longest side d(x_i,x_k) is at most 2^(-i)+2^(-j), which is at most d(x_i,x_j)+d(x_j,x_k). The other two inequalities follow from the scale ordering, including when j=i+1 or k=j+1. Positivity is immediate. The points x_k converge to p, and every other point is isolated, giving compactness.

The complete positive-distance partition is important: powers of two occur only on {p,x_k} and {x_k,x_(k+1)}. Every non-adjacent pair gives a binary number with exactly two nonzero digits, at positions j and k+1, uniquely determining the pair and never equaling a power of two. Thus there are no hidden equalities.

For the finite truncation Y_K, map p to 0 and x_k to 2^(k-1). The image of a pair x_j,x_k, j<k, has length 2^(j-1)(2^(k-j)-1). Its 2-adic valuation determines j and its odd factor then determines k. It equals the p-to-x_l length only when k=j+1 and l=j. This proves both directions of the LE biconditional on **all** pairs, not merely the designed adjacent pairs. Every finite subset is contained in a truncation, even if it omits p or has gaps.

For a global LE normalized by phi(p)=0, equality of the two specified lengths forces phi(x_(k+1)) to be either 0 or 2 phi(x_k). Injectivity excludes 0. Hence absolute values grow geometrically, contradicting continuity at p (or compactness of the image).

Continuity is indispensable: the very same doubling map is an equality/inequality-preserving injection on the entire countable set when continuity is dropped. Likewise the finite maps are not ordinal embeddings: the source p-to-x_k distances decrease while their image distances increase.

An independent exact rational check on Y_35 verified all 7,140 triangles and the entire partition of 630 unordered positive-distance pairs. Script: `check_n1_independent.py`. The all-index proof above, not this finite test, establishes the theorem.

## Theorem B: higher-dimensional gadget audit

Let c=sqrt(N/(2N+2)), so 0<c<1. A regular N-simplex of edge S in R^N spans the target, and the unique point equidistant from all its N+1 vertices is its centroid, with radius cS. Subtracting squared-distance equations establishes uniqueness; the standard simplex Gram matrix gives the stated c. In particular there is no extra orthogonal direction available in the same target dimension. This restriction is exactly why increasing the target dimension is not covered by the obstruction.

The source gadget G_k has vertex edges 2^(-k) and centre-to-vertex distances 2^(-k+1). Those are metric distances although they are not the edge/radius ratio of a Euclidean regular simplex; an LE need not preserve ratios or order. Edges in G_k share their source distance with radii in G_(k+1). Any target LE therefore satisfies R_k=c S_k and S_k=R_(k+1), forcing S_k=c^(-(k-1)) S_1, inconsistent with a bounded continuous image.

The source's cross-block distances use heights e(a) in [2^(-k),1.5*2^(-k)) and block positions h(a)=2^(-k). The inequalities |e(a)-e(b)|<2^(-k-1)<d_k(a,b)<=e(a)+e(b) establish all mixed triangle cases. For three distinct blocks the remaining contribution is a line metric plus nonnegative endpoint heights. The block {p} has only one point, so no omitted same-block triangle involving two distinct p-points exists. All gadget points approach p as k tends to infinity; fixed gadget points are isolated.

Rational independence of 1 and the e(a)'s makes every cross-pair length unique and distinct from all internal dyadic lengths. Comparing coefficients determines the unordered pair, including when one endpoint is p. The inductive choice outside countable rational spans is valid and sufficient; the optional square-root construction is unnecessary to the proof.

For finite embeddability, each gadget is represented as a rotated regular simplex and centroid, at scale c^(-k), with an independent translation. The intended internal distance classes are c^(-j), including j=0 for the first gadget's radii. They are pairwise distinct. All remaining failures are finitely many squared-distance equalities or zero-length equations on SO(N)^K times a Euclidean translation space.

The nonidentity check covers every case:
- A single cross-pair length versus a fixed internal length or zero is varied by translating one endpoint's block.
- For cross pairs involving different unordered block sets, translate a block appearing only in one set; the associated squared length has a quadratic term absent from the other.
- For cross pairs involving the same two blocks, their squared-length difference is affine in the relative translation. Its coefficient is the difference between the two internal displacement vectors. If only one endpoint changes this coefficient is nonzero. If both change, independent rotations ensure it is nonzero: when the displacement vectors initially coincide, rotate one by pi in a plane containing it.

The last step requires N>=2; SO(N) is connected for these dimensions, and the parameter space is connected and real analytic. A nonzero analytic function cannot vanish on an open set; finitely many such closed zero sets cannot cover the parameter space. Therefore a parameter avoiding *all* unintended coincidences exists. This is a valid existence argument, not a claimed explicit uniform algorithm or a consistent infinite family. The special N=1 construction must remain separate.

## Proposition 5.1: the N=1 example has a planar LE

The induction chooses the next image z on the circle centered at g_k with radius |g_k|, thereby preserving its one required equality. Restricting to 1/8<|z|/|g_k|<1/4 leaves infinitely many candidates and ensures convergence to 0. Every forbidden new coincidence is either an intersection with another circle of a different centre, an intersection with a line, or a forbidden previously chosen point. Each excludes finitely many candidates. Centres really are different because the previous finite map is injective. Thus one can avoid all undesired equalities at every step. Any comparison of two pairs is settled in some finite stage; the geometric decay proves continuity at p. This establishes a genuine global LE into R^2 and directly blocks use of X_1 against the later some-finite-M question.

## Lemma 6.1: finite maps to a continuous nonconstant map

This is the delicate compactness step. The proof does **not** assume equicontinuity or consistent finite embeddings, and does **not** assert that inequalities survive the limit.

Normalize finite embeddings using the same source pair of length t_0, ensuring that its image distance remains exactly one. For any fixed x,y, add a finite subdivided geodesic and an isosceles-triangle witness with sides t_0,t_0 and base d(x,y)/k, where k=ceil(d(x,y)/t_0). Distance equalities then bound the image separation by 2k. All needed points can be added to a single finite subset; the finite hypothesis is still precisely H(N). Compactness of the source bounds k uniformly, and finite-dimensional target balls are compact.

A cofinal ultrafilter on finite supersets gives limits for every point. Formally one may define each finite map arbitrarily at points outside its domain and truncate arbitrary values outside the bounded cofinal set; those choices are ignored by the ultrafilter. This harmless domain convention is implicit in the manuscript. Equalities survive limits and normalization prevents the constant map. Injectivity and distinctness of other distance classes are neither claimed nor needed.

Continuity is obtained after taking the limit. Isosceles witnesses give Phi(s)<=2 Phi(l) for 0<s<=2l and 0<l<=l_0. If a sequence s tends to zero while Phi(s)>=epsilon, this forces Phi(l)>=epsilon/2 for every small positive l. An infinite source ball of radius l_0/2 would then give infinitely many epsilon/2-separated image points inside a bounded subset of R^N, impossible by total boundedness. The no-isolated-points condition supplies the infinite ball. Consequently Phi(s) tends to zero and the map is uniformly continuous.

On a flat torus the three geometric hypotheses hold: shortest paths subdivide into equal metric lengths; sufficiently small Euclidean isosceles triangles remain distance-preserving under quotient; and there are no isolated points. The choice l_0=lambda_1/8, where lambda_1 is the shortest nonzero lattice-vector length, stays safely inside the injectivity scale. The isosceles construction, and hence this application, requires intrinsic dimension at least two.

## Lemma 6.2 and Theorem C: torus obstruction

For a continuous map whose chord lengths depend only on the flat geodesic distance, translations preserve all chord lengths. Their induced action on the image is well defined even if the map is not injective: equal images have distance zero, and translated images then do as well. On the affine span of the image this extends uniquely to affine isometries. Choosing an affine basis proves continuity of the action and its homomorphism law. Haar averaging gives a common fixed point, after which the action is orthogonal.

The finite-dimensional representation of the compact abelian torus decomposes into finitely many characters. Thus the squared displacement K(z) is a finite sum of terms 2 a_xi(1-cos(2 pi xi dot z)), with nonnegative coefficients. It is real analytic and lattice periodic. Locally, torus distance from the origin equals |z|, so K is radial near zero. For each rotation Q, analytic continuation of K(Qz)-K(z) makes K radial everywhere.

A radial periodic function on R^n for n>=2 must be constant here: if v is a shortest lattice vector of length lambda_1, radiality and periodicity force the radial value at r to equal its values on the full interval [|r-lambda_1|,r+lambda_1]. This is the set of |z+v| as z varies over the sphere of radius r. Starting with K(0)=K(v)=0 gives zero on [0,2lambda_1], and successive intervals cover all radii. Therefore the original map is constant.

Combining Lemmas 6.1 and 6.2 gives a contradiction to H(N) for **each** finite target N. Logically this means that for each N there exists a finite subset failing LE into R^N; it does not identify one subset failing every target dimension. Such a uniform finite witness is impossible because every finite metric space has an LE into some sufficiently high finite dimension. No bound on witness size is obtained.

The same constant-map obstruction directly proves absence of a global LE into any finite-dimensional target; that result alone would not have implied failure of H(N) without Lemma 6.1.

## Dimensions, explicit witnesses, and positive cases

Intrinsic dimension and target dimension must not be conflated. Every rank-n flat torus with n>=2 fails H(N) for every N>=1, independently of lattice shape. The intrinsic one-dimensional case is a circle, whose ordinary planar realization has chord length 2r sin(d/(2r)), strictly increasing for geodesic distances 0<=d<=pi r. Hence circles satisfy H(2), and cannot be included in the negative torus statement. Three equally spaced points show a circle fails H(1).

For the hexagonal torus with lattice basis (1,0),(1/2,sqrt(3)/2), its four half-lattice classes have all six mutual distances 1/2. The three nonzero parity classes contain unit lattice vectors, while every nonzero lattice vector has length at least one. Thus four points obstruct R^2 and any three obstruct R. The proof gives no higher-target explicit witness. On any n>=2 flat torus, a sufficiently small equilateral triangle also already obstructs target R; the manuscript's special four-point example is not needed for that simpler N=1 fact.

The stated positive examples have the correct distance transforms: standard round-sphere inclusion gives 2r sin(d/(2r)); real and complex projective rank-one projector maps give squared chord length 2 sin^2(d) in the stated normalization. Their target dimension bounds are valid, though not asserted optimal. These examples prevent overgeneralizing the negative answer to all compact Riemannian manifolds or all homogeneous manifolds.

## Status, priority, and publication guardrails

The manuscript explicitly labels itself unrefereed and AI-assisted. Its description of searches and earlier internal checks does not establish correctness, completeness of the literature, or novelty. This audit independently checks the central proofs but has not independently rerun its entire source archive, verified every bibliographic claim, or established priority against the helical-immersion literature.

Credit the external author for these constructions and proofs; do not rebrand them as newly discovered in this recovery. The character-expansion argument is expressly related to Heitzig's method, and the manuscript acknowledges possible folklore status. Absence of a known printed answer is not evidence that none exists.

Recommended status wording is variant-specific: “Audited unrefereed negative solution to the same-N LE reading and to the Riemannian finite-subspace question; original uniform-embedding wording ambiguous; later some-finite-dimensional LE question not resolved.” A bare “solved” without these qualifications would erase a material difference between the source and corrected record. No queue, repository, branch, or PR changes were made by this audit.
