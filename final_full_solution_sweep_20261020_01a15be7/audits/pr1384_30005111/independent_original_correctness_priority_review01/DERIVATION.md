# Independent derivation: PR1384 /30005111

This is a mathematical audit, not human peer review or a formal proof certificate. The exact target head is bfec87a455b12a99a16a4dcdc944136d1acb42db. No claimant program was run. Source and priority qualifications are in REPORT.md.

## 1. Fixed category and claim

Fix the actual positive-length edge path W:C_n→G. Its n domain vertices are indexed modulo n; the final displayed endpoint is the initial domain point. Every domain edge maps homeomorphically onto a specified target edge, with a specified direction. A stacking is a continuous h:C_n→R such that (W,h) is injective. Compactness and Hausdorffness then make it an embedding. Powers mean repetitions of this actual cyclic itinerary, equivalently factorization through a nontrivial cyclic circle covering, rather than free-basis primitivity. We first assume local immersion, including at the cyclic seam.

Only the finite image is needed, even if the ambient graph is infinite or disconnected. Loops count twice in vertex degree. Multiple edges remain distinct. Edges need not all be traversed in the same direction. Reversal and cyclic rotation of the whole walk preserve all conclusions.

## 2. Zero evaluation does not force a gradient

Let H be the connected current image, with E edges and V vertices, and choose one direction per edge. Put r=E−V+1. The evaluation functional L:Q^E→Q sums c(e) with the signed multiplicity of W. For a gradient δf(e)=f(head(e))−f(tail(e)), the sum telescopes around the closed domain, so L(δf)=0. The gradient space has dimension V−1 because H is connected, including when H has loops. If r≥2,

    dim ker L ≥ E−1 ≥ V > V−1 = dim gradients.

Thus choose a rational c in ker L outside the gradients, and clear denominators. Neither a nonzero homology class of W nor a surjective map to Z is required. In a spanning-tree gauge the chord coordinates represent H^1; one equation in at least two chord variables leaves a nonzero solution. A homologically zero W leaves all chord choices available. A graph bridge creates no difficulty: its signed count in a closed walk is zero.

An integral c need not be primitive. The voltage graph with vertices (v,k), k∈Z, and oriented edges

    (e,k):(u,k)→(v,k+c(e))

can have more than one connected component. The component visited by the lift is all that is used. Calling this a finite cover would be inaccurate: the cover is generally infinite; its visited image is finite. This distinction is correctly preserved by the PR's actual proof.

## 3. Finite image splitting really progresses

Set s_0=0, s_(i+1)=s_i+direction_i c(edge_i). Then s_n=0. Lift W to vertices (v_i,s_i); a backward traversal uses the oriented edge whose initial level is s_(i+1). Take H' to be the image consisting of the lifted traversed edges and endpoints. It is connected and finite. The projection H'→H is locally injective since it is the restriction of a graph covering, so the lifted circle is still immersed.

Every old vertex has at least one visited lift. If it had exactly one, denote its level s(v). Every old edge is traversed somewhere, so its lifted endpoints force c(e)=s(head(e))−s(tail(e)), including an edge only traversed backward. This would make c a gradient, contradiction. Therefore

    V(H') > V(H),       V(H') ≤ n.

This is the progress invariant; rank need not decrease. It applies even to zero-homology walks such as a commutator, nonprimitive voltages, bridges, negative voltages, loops, and parallel edges. The accompanying independently written controls deliberately add gradients and multiply nongradient cochains by 2 or −3.

Every vertex of a current image has degree at least two: the incoming and outgoing germs at any of its domain preimages are distinct by immersion. Hence E≥V and r≥1. Whenever r≥2 another strict vertex increase is available, so the process must reach r=1 after at most n−V(H_initial) steps. At r=1 the degree sum is 2V, and minimum degree two forces all degrees exactly two. A finite connected graph with this property is a circle, including the one-loop and two-parallel-edge cases.

An immersed combinatorial map between circles is a covering: at every vertex the two distinct domain germs exhaust the two target germs, and the local maps on interiors are homeomorphisms. The direction around the circle is consistent. Let d≥1 be the absolute degree. If d>1, the terminal circuit projects to a shorter closed edge itinerary in the initial G and W is exactly its d-fold repetition. Thus a nonperiodic W has d=1. The terminal lifted map is already embedded, with constant height zero.

This proves termination without assuming the maximal tower theorem. It is, however, the graph-specialized version of the classical tower progress mechanism, which must be credited in any claim about method provenance.

## 4. Descending an embedding: the integral separation is uniform

For one split, extend cumulative levels affinely along domain edges to a. Over a fixed old oriented edge e, let t∈[0,1] be its base coordinate. A point in lifted edge (e,k) has

    a = k+t c(e).

For a reverse domain traversal, its local parameter is 1−t, giving exactly the same formula. Distinct lifted edges over the same old interior point therefore differ in a by a nonzero integer. The same integer-separation assertion holds over old vertices. Coincident lifted projections have exactly equal a.

Suppose b is a stacking height for the lifted walk. Its absolute value is bounded by M on the compact domain. Choose ε>0 with 2εM<1 and set h=a+εb. For any distinct domain points with equal old projection there are two cases:

* Different lifted projections: |a(x)−a(y)|≥1 while ε|b(x)−b(y)|≤2εM<1, so h(x)≠h(y).
* Equal lifted projections: a(x)=a(y), while b(x)≠b(y), so again h(x)≠h(y).

Endpoint formulas agree, so h is continuous. The resulting injective map is an embedding. Start from b=0 on the final embedded circle and repeat through the finite sequence. No global embedding of the entire infinite cover product is needed. Piecewise linear heights on the original finite subdivision suffice for immersed paths. With integral levels and rational ε these heights can be rational, though the target problem asks neither a complexity bound nor implementation.

Necessity requires no immersion: if W factors through a covering with deck rotation τ of order d≥2, the continuous function h(τx)−h(x) would be nowhere zero. It has one strict sign on the connected circle; the sum over its finite orbit is zero by telescoping. Contradiction.

Together these prove the full immersed nonpower criterion by finite graph counting, rational linear algebra and elementary continuity/compactness. The proof never transfers stacking existence into an unsupported lemma.

## 5. Arbitrary backtracking: a literal negative

Let G be the simple three-vertex path a—v—b, and take

    W = v a v b v a v b v a v.

The five excursions have labels a,b,a,b,a. The directed edge v→a occurs three times and v→b twice. A repetition exponent would divide both counts, impossible. This also covers every cyclic rotation and inverse itinerary. The walk nevertheless represents 1 in π_1(G): it is not a counterexample about a nonpower free-group element.

For an excursion to a leaf, orient its target edge from v toward that leaf. Its outgoing and incoming height strands are continuous functions of target coordinate. Two different excursions to the same leaf have distinct limiting heights at the leaf. Near the leaf, both strands of one are below both strands of the other. Each of the four cross differences is continuous and nonzero on the connected open edge, hence retains its sign everywhere. Taking limits at v shows the two intervals spanned by their central endpoint heights have disjoint interiors. Equality may occur only at the same domain visit shared by consecutive excursions. There is no affine, monotonic-height, smoothness, or planar-approximation assumption.

Let h_0,…,h_4 be the pairwise distinct heights at the central visits. The a-excursions span I_01,I_23,I_40. Since I_01 and I_40 have disjoint interiors and share h_0, h_0 lies strictly between h_1,h_4. Their union J is the interval spanned by these three heights. Because h_2,h_3 differ from all three, the interval I_23 must lie strictly on one side of J; otherwise it would overlap an a-interval in its interior. The b-intervals I_12 and I_34 both cross the same nonempty open gap between J and I_23, contradicting the leaf-interval condition. Thus no continuous stacking exists.

A missing immersion assumption alone would not prove this. Indeed a single out-and-back on one edge stacks: with projection t for t∈[0,1] and 2−t for t∈[1,2], use height sin(πt), endpoints 0 and 2 identified. Distinct strands over 0<x<1 have heights ±sin(πx). An affine-only test on the original two edges wrongly rejects this positive case.

The original OWR words admit the literal reading just disproved, but do not decide the intended convention. If closed walk implicitly means cyclically reduced walk, Section 5 lies outside that convention and Sections 2–4 provide the requested elementary proof instead. If power is read in the fundamental group, this tree example is outside the nonpower hypothesis. The qualification is essential and must not erase the correct literal negative.

## 6. Independent falsifiable controls

independent_controls.py imports only Python's standard library. It constructs its own spanning-tree cochains, checks cycle defects by a separate potential-integration test, uses a different tree choice, adds integer gradients and changes voltage scales/signs, and independently verifies every resulting rational affine embedding. It checks 1,112 valid immersed walks: 280 selected rose3 walks (explicitly bounded selection), all 268 barbell-with-bridge, 180 parallel-theta, 72 subdivided-theta and 312 K4 closed reduced walks through the stated length bounds. Of these 1,022 are primitive and 90 proper powers. All three cochain choices per walk give the exact expected terminal root degree: 3,336 runs. The sample commutator requires two splits although the first leaves rank unchanged, demonstrating why rank decrease is not the invariant.

The same independent program exhausts all 5!·3!·2!=1,440 vertex-fiber orders for the ten-edge counterexample; none satisfies the necessary weak endpoint order condition. The single-excursion positive control is accepted. All 20 rotation/inverse nonpower tests pass. Four malformed/corrupt controls reject colliding heights, inexact heights, nonimmersion, and a pure gradient masquerading as a nongradient. Normal, -O and -OO outputs are identical. These bounded checks corroborate Sections 2–5; they are not their general proof or a complexity proof.
