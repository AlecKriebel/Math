# Independent whole-proof reconstruction and falsification record

This reconstruction was made without reading the earlier whole reviewers' derivations. Earlier PASS labels are not premises. The result being assessed is the finite, explicit counterexample at a specified supercritical parameter in the repaired package, not an inference of the historical questioner's unique intended quantifier.

## Exact question, model, and success criteria

The full-byte authenticated 30 October 2013 Benjamini lecture file defines countable locally finite simple graphs (p.5), rough isometry (Definition 1.25, p.9), common-parameter independent bond percolation and root critical probability (pp.32–33). The actual Problem 9.6 on p.64 omits the percolation-parameter quantifier. Its local context on pp.63–65 discusses supercritical uniqueness and also separate transitive questions; this does not impose transitivity on every graph in Problem 9.6. The manuscript explicitly declares the all-fixed-supercritical reading: every bounded-degree graph roughly isometric to the square lattice has almost surely exactly one infinite cluster at every fixed p with pc(G)<p≤1. A deterministic graph G with pc(G)≤0.9 and P_0.95(N∞≥2)>1/3 refutes that reading. It does not refute uniqueness sufficiently near one, prove what the questioner uniquely intended, or establish simultaneous claims over all parameters. These qualifications survive unchanged in the PDF, source, and all corrected metadata.

## Construction, local structure, and metric boundary cases

Keep all edges internal to A={(x,y):x,y≥1} and B={(x,y):x,y≤−1}; replace every other square-lattice edge by its own path of exactly 100 bonds, with private internal vertices. This is deterministic, countable, simple, connected and of maximum degree 4; internal chain vertices have degree 2. Boundary lattice vertices still have precisely the original four incident directions, realized by edges or distinct first chain bonds. No chain intersections introduce identifications or parallel bonds.

Map original lattice vertices identically, and each chain vertex to a nearest endpoint, choosing a consistent tie at position 50. Each vertex is at graph distance at most 50 from its image. Each actual bond has image displacement at most one, including the midpoint switch, so d_Z2(fu,fv)≤d_G(u,v). Lift a lattice geodesic between the endpoint images using paths of length at most 100 per lattice edge and at most 50 at each end. Hence d_G(u,v)≤100 d_Z2(fu,fv)+100. Surjectivity on the original vertices gives a strict 100-net. The other required inequality in the book's convention follows immediately from d_Z2≤d_G. This proves the literal C=100 convention, not only a vaguely equivalent metric convention. Finite boundary truncations in my independent BFS are checks, not the proof of this uniform statement.

## Series reduction, finite/infinite component correspondence, and root survival

For an internal A or B edge the effective probability is p. For a weak edge it is q=p^100, because all 100 independent actual bonds must be open. Distinct chains and retained edges use disjoint sets of actual bonds, so all effective edge states are independent even when their original endpoints coincide. An original-vertex connection through a chain must complete it: the chain has no exit at an internal vertex. Erasing excursions shows that two original vertices are connected exactly when they are connected in the effective lattice. An actual component with only finitely many original vertices can touch only finitely many private finite chains and is finite; a component with no original vertex lies inside one chain. Thus infinite components correspond bijectively to infinite effective components. Dangling partly open chains do not merge different original-vertex components or create a new infinite component.

For any chosen actual root o, choose a fixed finite path F to a quadrant corner v. Setting every bond of F open can only increase the increasing event {v connects to infinity}. Conditioning on these finitely many bonds, or coupling the remaining independent bonds and then forcing F, gives P_p(o↔∞)≥p^|F| P_p(v↔∞). Positive quadrant survival at p=0.9 therefore gives root-independent pc(G)≤0.9. No 0–1 law, transitivity or monotonicity of uniqueness is used.

## Quadrant finite-cut parity, including holes and dual degree four

Translate a strong quadrant to N_0². If the corner's open cluster D is finite, all cut edges between D and its complement inside the quadrant are closed. In the associated finite dual cut graph, a bounded square face has degree 0,2 or 4: its cyclic membership sequence changes an even number of times. A boundary half-edge ends at degree one. On the bottom primal ray, membership starts inside D at the corner and eventually becomes outside; the number of bottom boundary endpoints is odd. Therefore some connected dual component has odd bottom-endpoint count. The handshake lemma in that finite component forces odd left-endpoint count too. It contains a simple dual path from bottom to left. This argument permits disconnected finite D, holes, diagonal contacts and degree-four dual vertices; no unjustified unique-contour or degree-two assumption is present.

A path of length m joining the corresponding bottom and left positions has m≥2 and has at most m possible bottom starting positions. For each start, the full lattice nonbacktracking bound is 4·3^(m−1); restricting to eligible simple quadrant dual paths only reduces that number. Each eligible path crosses m distinct primal edges, so its all-closed probability is (1−t)^m. Ineligible paths may enlarge the count, but no probability is assigned to nonexistent primal bonds. Thus with z=3(1−t)<1,

P_t(corner finite) ≤ (4/3) Σ_(m≥2) m z^m = (4/3) z²(2−z)/(1−z)².

At t=9/10 this is 102/245, leaving survival at least 143/245. At p=19/20 the same lower bound follows by the usual monotone coupling of the increasing survival event. The proof's limiting operation is a countable union bound over finite dual paths; it does not substitute finite-box numerical survival for an infinite event.

## Every weak-path start and every path length

If any finite effective path joins A to B, stop at its first B vertex and take the last earlier A vertex. All edges in that segment are weak. Loop erasure gives a weak self-avoiding path with no larger length, beginning on (1,n) or (n,1), n≥1. Its endpoint lies in B, so its length is at least n+3. The corner may be counted twice, which is harmless. Count all lengths and all starting positions; with r=3q<1,

P(W) ≤ 2 Σ_(n≥1) Σ_(m≥n+3) 4·3^(m−1) q^m = (8/3) r^4/(1−r)^2.

No finite cutoff or exchange of a conditionally convergent series occurs: the sums have nonnegative terms and converge for r<1. The 100-chain choice is sufficient because (20/19)^20≥1+20/19>2 and hence q=(19/20)^100<1/32. Therefore P(W)<27/107648. My complete short-path DFS, exact positive tail identity, far-start path n=1024 and deliberately false finite-cutoff controls test distinct failure modes of this step; none replaces this analytic all-start/all-length proof.

## Infinite-event independence and strict final margin

Let S_A,S_B be corner survival using only the retained bonds internal to A,B. Let W be weak-path connection, using only weak chains. These are measurable in three disjoint countable product coordinate sets: survival is a countable intersection of finite-radius connection events, and W is a countable union of finite path events. Independence of the three sigma-fields follows from the independent product law (finite cylinders extended by the monotone class theorem). If one uses paths to arbitrary distances to characterize an infinite component, local finiteness gives the usual compactness/König argument. No independence of events that merely share a boundary vertex is assumed; the coordinate sets are actual bonds and are disjoint.

On S_A∩S_B∩W^c, the two infinite strong components cannot be connected in the effective graph, since any such finite connecting path would force W. The series correspondence then gives distinct infinite components in G. Consequently

P_0.95(N∞≥2) > (143/245)^2 (1−27/107648)
=2200741829/6461571200 > 1/3,

with exact margin 140654287/19384713600. This is a positive-probability multiplicity conclusion; it does not assert almost sure multiplicity or an exact number of infinite clusters. At p=1, connectivity of G implies uniqueness, consistent with the expressly unrefuted near-one question.

## Independent reproducible attacks

`independent_paths_series_metric.py` imports no claimant, preparer or prior reviewer code. It enumerates every corner-containing subset of a 5×3 box (16384), including disconnected sets and 9753 dual degree-four incidences; computes variable-length series component laws on a two-triangle graph by all 8192 micro-configurations at two rational probabilities; checks 122880 original-vertex pair connections and all 128 effective state masses; checks 34225 ordered distance pairs in a 3193-vertex expanded box; and completely enumerates first-B weak self-avoiding paths through length 11 from all 16 starts that can contribute at those lengths. Counts by lengths 4 through 11 are 12,24,60,146,378,920,2334,5790. It proves the exact positive analytic tail after that finite prefix and constructs a valid path from start index 1024 of length 1027. Ten active false controls are rejected. Normal, -O and -OO outputs are byte-identical. The executable work corroborates local combinatorics, exact arithmetic and bookkeeping. The universal graph, probability and compactness claims above are proved separately.

No substantive mathematical defect was found after these deliberate attempts. Originality is separately bounded by actual primary comparisons in PRIORITY_REVIEW.md; it is not inferred from the proof's elementary character or from a prior PASS label.
