# Independent audit of the planar convex integer IKEA prior solution

Target: 1900002 / AMR-018-0002, ranked entry 1016. Date: 2026-10-08 UTC.

## 1. Question, scope, and credit

Karpenkov's 2017 §1.3 Problem 2 asks for a characterization of collections of ordered integer-angle LLS data realizable at the vertices of a lattice polygon. The adjacent Problem 1 concerns an integer cosine rule and is a different problem. The 2017 wording does not explicitly state convexity; the later authors explicitly formulate and solve its convex planar interpretation. The correct disposition is therefore limited to bounded, full-dimensional, convex lattice polygons with no redundant collinear vertices, and n >= 3. Each ordinary interior angle is strictly between zero and pi.

The cited resolution is James Dolan and Oleg Karpenkov, *Lattice angles of lattice polygons*, Journal de théorie des nombres de Bordeaux 37(3) (2025), 873–896, DOI [10.5802/jtnb.1345](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/), Theorem 3.3 and §5.1. The publisher records online publication on 2025-11-27. This is prior work, with zero campaign proof turns. The higher-dimensional question in the article's §6 remains separate. No general nonconvex, cosine-rule, novelty, or polygon-uniqueness claim follows.

## 2. Exact criterion and quantifiers

Fix an ordered list A_1,...,A_n of nonempty positive integer words of odd length. These are the finite regular continued-fraction LLS blocks, not negative Hirzebruch–Jung words. For integers c_1,...,c_n, let

- U_j = (A_1,c_1,A_2,...,c_(j-1),A_j).
- V = (A_2,c_2,A_3,...,c_(n-1),A_n).
- K(empty) = 1, K(a) = a, and K(w_1,...,w_m) = w_m K(w_1,...,w_(m-1)) + K(w_1,...,w_(m-2)).

The theorem requires all three conditions:

1. K(U_n) = 0.
2. c_n = -floor(K(V,1)/K(V)).
3. Delete every zero from K(U_1),...,K(U_n); the resulting list has exactly n-3 sign changes.

The quantifier for angles alone is existence of integer c_1,...,c_(n-1), with c_n then determined by the second equation. The equations classify realizability by witnesses. They do not supply a finite search bound, a rejection algorithm from a failed bounded search, or a unique lattice polygon. For a supplied witness, evaluation is finite exact arithmetic. Enumeration of all integer witnesses semidecides positive instances; its failure to finish has no negative meaning.

The frozen implementation transcribes the published formula accurately, including the unary minus outside floor, signed continuants, zeros removed only for sign counting, and the final cyclic curvature. Its input caps are software resource limits, not theorem hypotheses.

## 3. Independent algebra: the closing quotient and scalar monodromy

For each integer x, write T(x) = [[x,1],[1,0]] and M(W) for their ordered product. Direct matrix multiplication proves that its upper-left entry is K(W), its lower-left entry is K(W with first entry removed), and its determinant is (-1)^length(W). For words of length at least two, the remaining entries are the corresponding end-deleted continuants. This also proves primitiveness of each matrix column.

U = U_n has odd length. If K(U)=0, determinant -1 forces

M(U) = [[0,epsilon],[epsilon,d]], with epsilon in {+1,-1} and d an integer.

Write M(A_1) = [[a,b],[r,s]]. Positivity gives a > 0 and 0 < r <= a. Since M(U) = M(A_1) T(c_1) M(V), inversion of the determinant-one first factor gives

K(V) = -a epsilon,
K(V,1)/K(V) = epsilon d + 1 - r/a.

The second term belongs to [0,1). Thus the denominator never vanishes, and

c_n = -epsilon d.

Equivalently, M(U) T(c_n) = epsilon I. This verifies the final-curvature quotient by a second exact algebraic formulation, including negative denominators and integral endpoints. It also explains why closure alone is insufficient: it closes the endpoint ray but can leave the lattice frame with the wrong final join. No division by an intermediate continued-fraction value is needed.

The finite witness search in the accompanying controls computes c_n from this matrix identity and compares it with the published floor formula. It includes closed data with incorrect winding, which have scalar monodromy but must still be rejected as convex polygons.

## 4. Orientation, equivalence, ordering, and degeneracies

The group is affine GL(2,Z), including determinant -1 reflections and integer translations. Unsigned lattice sine and lattice length are invariants under the whole group; a signed determinant changes by det(M). The source's unqualified signed-area invariance sentence is not literally correct for reflections. This does not change Theorem 3.3: choose an orientation consistently and use absolute determinants where the definition calls for a lattice sine.

For the executable convention, list polygon vertices clockwise and order each angle's rays as previous-minus-current, next-minus-current. Their determinant is positive. Reflecting the entire configuration and then restoring clockwise order reverses the vertex sequence, reverses every LLS block, and reindexes curvatures by the corresponding edge. This is not an independent reversal of arbitrary blocks. A cyclic start change carries c_i with its edge. Arbitrary permutations are not an allowed invariance of the ordered realization problem.

All c_i are allowed to be integers: no assumption c_i < 0 is permissible. Zero curvature does not mean a zero interior angle. Zero intermediate continuants do not mean malformed input. A square already supplies internal zero prefix continuants. At the chord-definition level the closest unit-distance lattice points can coincide, so their signed displacement is zero; locally convex open broken lines also permit a reversed displacement. These cases are retained by the signed formula. Distinct straight-angle degeneracies are excluded by the positive odd angle-block hypothesis and strict convexity of the final polygon.

The independent geometry checks recover sail blocks without the producer's Bezout/continued-fraction normalization: they enumerate lattice points in the primitive ray triangle, compute the origin-facing convex-hull chain, and measure its lattice edge lengths and lattice sines. Chord points are found by an exact monotone integer search on the line one lattice unit inside an edge, rather than the producer's quotient formula.

## 5. Necessity, winding, and constructive sufficiency

### What is imported from the primary proof

In the unit-distance sail-diagram setting required here, the published proof uses its sail-coordinate formula (Theorem 4.7), the identification of angle-curvature data with the sail diagram (Corollary 4.18), and its closing-curvature calculation (Corollary 4.19). These geometric correspondences are inspected and accepted as the primary proof's lemmas; they have not been independently formalized here. The primary proof's occasional missing K notation and its final citation to Proposition 4.14 where the LLS identification is needed are read using the explicitly stated Corollary 4.18. The main theorem's printed three-condition statement is unambiguous.

### Necessity

Translate successive angle sails to the origin, applying central symmetry on alternating angles. Primitive edge-ray representatives then form a positive rotating sail path starting at (1,0) and ending at ((-1)^n,0). The matrix formula identifies the second coordinates of its block endpoints with K(U_j), proving condition 1. The local unit-distance chord join gives the closing floor formula; the independent algebra above checks its equivalent scalar-frame closure. A convex n-gon has total interior angle (n-2)pi, which gives condition 3 by the crossing count below.

### Winding check, including zero endpoints

Here is the crossing count without assuming that the diagram already comes from a convex polygon. Each positive block has a positively oriented ordinary angle alpha_i strictly between zero and pi. Lift the successive directions to real arguments theta_0=0 and theta_j=sum_(i=1)^j alpha_i. They increase strictly, with every increment less than pi. Closure gives theta_n=m pi for some positive integer m; primitiveness gives the endpoint ((-1)^m,0).

For 1 <= j <= n, the sign of K(U_j) is the sign of sin(theta_j). The only horizontal-ray crossings in the open lifted interval (0,m pi) occur at pi,2pi,...,(m-1)pi, so there are m-1 of them. Each open block interval (theta_(j-1),theta_j) has length less than pi and contains at most one crossing. A crossing strictly inside such an interval reverses the two nonzero endpoint signs. If a crossing equals theta_j, then neither adjacent endpoint is zero: two consecutive zero endpoints would differ by a positive integer multiple of pi, contradicting alpha_i < pi. The previous and next nonzero signs around theta_j are opposite, since both adjacent increments are less than pi. Deleting the zero therefore retains exactly that one reversal. Conversely, any two consecutive nonzero signs that differ arise either from a unique interior crossing or from this single deleted-zero case; there cannot be two deleted consecutive zeros or a second hidden crossing. The first nonzero sign is positive because 0 < theta_1 < pi. The zero at theta_n contributes no reversal, and theta_0 is not part of the listed prefixes. Thus, after deleting every zero, there are exactly m-1 sign changes.

Condition 3 consequently forces m-1=n-3, hence m=n-2, winding (n-2)/2, and epsilon=(-1)^(n-2)=(-1)^n. This reasoning covers arbitrarily many total turns, not just a simple sail path, and correctly rejects a multiply wound locally convex cycle.

This supplies the elementary crossing argument also needed in the converse; one must not infer the converse merely by applying a proposition whose statement already assumes a convex polygon.

### Constructive geometric completion

From a witness, the sail-coordinate lemma supplies block endpoints B_0,...,B_n. Set B_0=(1,0) and use outgoing edge directions e_i=(-1)^(i-1) B_i for i=1,...,n. Consecutive exterior turns are pi-alpha_i, all strictly between zero and pi. Their sum is 2pi. Thus these directions make one clockwise turn and give a complete strictly ordered planar normal fan.

For each edge take its outward normal. The half-plane tangent to the Euclidean unit circle with that normal has support equal to the normal's Euclidean length. Consecutive normal gaps are less than pi, so every tangent line is active, the intersection is bounded, and consecutive line intersections are distinct vertices strictly inside the other half-planes. Approximate the finitely many supports closely enough by rationals. The strict inequalities persist. Since all normals have integer coordinates, all consecutive line intersections are rational. Scaling by a common denominator gives a lattice polygon with exactly the prescribed directions, hence the prescribed ordered angle types. The joining sail frames give c_1,...,c_(n-1); scalar monodromy fixes the final c_n.

This explains the classical real-polygon and rational-perturbation step that §5.1 cites without proof. The independently written test constructor uses dyadic support approximations, exact rational line intersections, strict support-side checks, and denominator clearing. This is an executable construction for an accepted witness, not a bounded decision algorithm for angle data with no supplied witness.

Scaling preserves all angles and chord curvatures while changing area, so an accepted sequence typically has infinitely many noncongruent integer realizations. Theorem 3.8 is not used to claim uniqueness.

## 6. Finite controls and limits

The accompanying controls do not copy the producer's implementation. They use path-matching polynomials for short continuants, matrix-frame closure for cyclic witnesses, direct lattice-point sails and chord-point searches for geometric necessity, and rational tangent-half-plane constructions for sufficiency examples.

Per normal, -O, and -OO run:

- 97,656 signed continuant words independently match path-matching evaluations.
- All 2,719 distinct full-dimensional convex hulls of subsets of the 4×4 integer grid pass independently extracted LLS/chord data and the three-condition criterion.
- 11,868 cyclic checks and 10,876 GL(2,Z) transformation checks pass; the latter include reflections with the required reversal/reindexing.
- 934 grid polygons exercise internal zero prefix continuants.
- 47,296 curvature candidates yield 168 accepted witnesses, including 101 with a zero or positive curvature. Another 146 have algebraic closure with wrong winding and are rejected.
- 157 representative witnesses are explicitly realized as integer polygons and their data recovered. The largest needed dyadic support refinement in these tests is 2^7.
- Twenty-six malformed angle inputs, nine malformed JSON inputs, four malformed polygons, a doubled-triangle winding sentinel, and positive/zero/negative local chord displacements are checked.

These counts are finite evidence of transcription, convention, and code behavior. They do not establish the universal theorem by enumeration or amount to a formal proof. Mathematical credit remains with Dolan and Karpenkov. The complete official preprint-correction file was subsequently inspected and compared with the journal; its scope is recorded in SOURCE_STATUS.json. The independent acceptance decision is in ACCEPTANCE.md.

## 7. Exact correction-history comparison

The author university homepage links a [correction file for the 2023 preprint](https://pcwww.liv.ac.uk/~jgd511/papers/lat-corrections.txt). Its 141 bytes have SHA-256 28a2619377376f85a5c245d86a43985adbe785ba19a2d5b99c5e80e1e6022a7d. The entire file was inspected, and the relevant locations compared directly in the arXiv v1 PDF and published journal PDF.

- Preprint Definition 2.7 names the terminal point inconsistently. Journal Definition 3.7 uses the corrected B label. That auxiliary definition still has an indexing shorthand mismatch between n and 2n, and is not the definition used to evaluate Theorem 3.3 here.
- The correction's entry labeled Proposition 3.9 corresponds to preprint Remark 3.9. It directs a terminology change from general winding to vortex broken lines. Journal Remark 4.8 retains the older terminology. This audit uses the explicit positive determinant condition of the vortex definition and only the unit-distance sail setting.
- Preprint Proposition 3.15 needs the continuant K applied to its LLS prefixes. Journal Proposition 4.14 and related proof prose retain the missing-K notation. The principal theorem, preprint Theorem 2.3 and journal Theorem 3.3, already states the sign-change condition with K correctly. A list of words itself has no scalar sign, so the intended reading is fixed both by the correct main statement and by the coordinate formula. The complete crossing proof above supplies the needed argument independently of that shorthand.

No entry in the inspected correction file changes the principal theorem's three conditions or supplies a counterexample to its sufficiency. The finite tests likewise found no contradiction. This is a qualified review of the inspected sources, not a claim that no other correction could exist. The producer's earlier no-correction-found search remains explicitly historical rather than the current source assessment.

## References

1. O. Karpenkov, [Open problems in geometry of continued fractions](https://arxiv.org/abs/1712.01450), 2017, §1.3 Problem 2.
2. J. Dolan and O. Karpenkov, [Lattice angles of lattice polygons](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/), 2025, especially Definitions 2.3, 2.7, 2.13, 3.2; Theorem 3.3; §4 and §5.1; Remark 5.1; §6.
