# Turn 1: exact rational counterexamples and finite piercing certificates

First substantive turn. Original unresolved. This turn proves a complete reduction of a hypothetical counterexample to rational polygon data with strict cross-color intersections, then gives a finite exact test and independent Helly-hypergraph certificate for each such instance. It is a counterexample semidecision procedure, not a terminating decision procedure for the universal conjecture. Compactness, polygon approximation, arrangements and planar Helly are classical tools; no novelty is claimed.

## 1. Stability of failure under small outer thickening

Fix a finite family {K+t_i} that cannot be pierced by three points, with K nonempty compact. There is ε>0 such that {K+εB+t_i} still cannot be pierced by three points, where B is the closed Euclidean unit disk.

Otherwise choose three piercing points for each thickening with ε=1/m. Every used point lies in one of finitely many translates of K+B, a common compact set. Move unused points to one fixed point in that compact set. A subsequence of the triples converges. Since there are finitely many assignments of the sets to one of three piercing points, pass to a further subsequence with the assignments constant. Taking limits gives three points piercing the original family, a contradiction. This proof applies even to lower-dimensional K and tangent configurations.

For a three-color counterexample choose one ε that works for all three families. Each family is necessarily nonempty. Empty K cannot produce such a counterexample: if all colors are nonempty, the cross-intersection hypothesis fails; if a color is empty, the conclusion holds.

## 2. Rational, full-dimensional, strictly intersecting reduction

Choose a rational full-dimensional convex polygon P such that

    K+(ε/4)B ⊂ P ⊂ K+(ε/2)B.                            (1)

Such polygons exist by elementary outer polygon approximation and density of rational vertices, using the positive gap between the two compact convex neighborhoods. One explicit justification is to approximate K+(3ε/8)B by a finite convex hull of nearby rational points within Hausdorff distance ε/16, so all its support functions remain between those of the two neighborhoods. The support-function error is bounded by the Hausdorff error uniformly over unit directions.

Perturb every translation vector t_i to a rational vector t_i' within ε/8. Then

    K+(ε/8)B+t_i ⊂ P+t_i' ⊂ K+(5ε/8)B+t_i
                                     ⊂ K+εB+t_i.        (2)

Every original cross-color intersection point is now the center of a radius ε/8 disk in both perturbed translates. Thus all required cross intersections have nonempty interior, with uniform positive slack. Conversely, any three points piercing a perturbed color family would pierce the larger ε-thickened original family, contradicting §1. Hence a counterexample, if one exists, can always be chosen with rational full-dimensional P, rational translations, and strict cross-color intersections.

The reverse implication is immediate because these are instances of the original conjecture. No upper bound on the number of vertices, family sizes or coordinate denominators is asserted. Restricting to any one finite grid is therefore insufficient to prove the original question.

## 3. A finite candidate set for rational polygon translates

Let P be a nonempty full-dimensional rational convex polygon with m edges, and let a family have N translates. Form the finite candidate set V consisting of:

- every vertex of every translate;
- every nonparallel intersection of two translated edges that lies on both closed segments.

Coincident or overlapping collinear edges need no additional points: their overlap endpoints are original vertices. Thus |V|≤Nm+binom(Nm,2).

A family has piercing number at most three if and only if three (or fewer) points of V pierce it. For the nontrivial direction, assign each translate to a piercing point it contains. Each nonempty assigned class has a nonempty compact convex polygonal intersection, possibly a segment or singleton. Such an intersection has an extreme point. Its active supporting constraints either give an original vertex or two nonparallel translated edges crossing there; in the collinear segment case its endpoint is an original vertex or an edge crossing. Hence that extreme point belongs to V and can replace the original piercing point. Empty assigned classes need no point.

All candidate coordinates, membership tests and edge intersections are rational. Compute each candidate's N-bit coverage mask, then test all unions of at most three masks against the all-covered mask. This is a genuine finite algorithm. A crude bound is O((Nm)^6) mask-union trials after O((Nm)^2) candidates are generated; bit complexity depends on rational input size and mask representation and is not claimed constant. The algorithm is not advertised as efficient for large inputs.

Cross-color intersections can be tested by the same vertex/edge criterion for each pair, or by exact half-plane feasibility. Strict cross intersection can be tested by positive polygon intersection area. The checker uses exact rational arithmetic.

## 4. A second combinatorial certificate via Helly

Build the bad-subfamily hypergraph on the N translates: an edge is any pair or triple having empty common intersection (singletons are nonempty). The family is three-pierceable exactly when these vertices admit a coloring with three auxiliary colors with no monochromatic hyperedge. These auxiliary colors label piercing points and are unrelated to the original three input-family colors.

Indeed a piercing triple partitions the family into three intersecting classes, which avoids all bad edges. Conversely, such a coloring puts every pair and triple within each class in nonempty intersection. Planar Helly's theorem gives a common point for the entire class. Taking up to three such points yields a transversal. The condition on triples cannot be replaced by pairwise intersection: three translates may intersect pairwise without a common point.

Thus a negative finite-instance certificate can list the exact bad pairs/triples and exhaustively refute the finite three-coloring problem; a positive certificate can list at most three rational candidate points and their coverage. The geometric realization of the hypergraph must be verified. An arbitrary non-three-colorable hypergraph alone is not a counterexample to Dol’nikov.

## 5. Consequence and remaining gap

Enumerate rational full-dimensional convex polygons and finite rational translation lists in three colors by increasing finite descriptions. Check strict cross intersections and the exact three-piercing test. By §2 this procedure eventually finds a counterexample if one exists. If the conjecture is true, it need not terminate. This is the exact stopping condition, not a disguised claimed solution.

The accompanying finite controls compare the arrangement-mask minimum with an independent Helly-hypergraph coloring search on small rational instances. Any finite absence of a counterexample remains explicitly finite. Original unresolved1/5.
