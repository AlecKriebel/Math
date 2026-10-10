# Independent audit: ordinal colored dense order preorders

## Verdict

**ACCEPT_PARTIAL.** The frozen manuscript proves its stated partial theorem. No mathematical correction is required. The original classification problem, 30000374 / OWR-1116-002, remains **unresolved by this work**: the exact Borel preorder degrees for the nontrivial ordinals and analytic preorder universality are not established.

The reviewed proof is 20,953 bytes, SHA-256 `c283b7c7b0d45374d80280f95bf61a4e2ffd560038846f66d6df72ab88940407`. It was read in full and was not modified during this audit. The verdict covers the mathematical assertions of Theorem 1, Lemmas 2–4, Proposition 5, and the elementary constant-color and finite-support comparisons. This is an independent AI mathematical review, not a formal proof-assistant certificate, external peer review, or a novelty assessment.

The source inspections and finite-control reports below describe the independent audit of 10 October 2026. This publication edition retains every substantive audit argument. Edition preparation rechecked frozen identities and replayed the independent finite controls; it did not perform a new literature search or source-page inspection.

## 1. Exact source interface

Camerlo's report defines reducibility of relations using one Borel map on their underlying spaces. Problem 5 asks for a classification with the usual comparison on every countable ordinal. The original printed page 3128 was checked directly, together with the preceding definition of reducibility and surrounding statements on printed pages 3127–3129. The family in the frozen proof is the correct one. In particular:

- All functions from the rationals into the countable ordinal are allowed.
- The rational witness is strictly increasing, with image dense in its convex hull.
- The witness need not be onto the rationals or have image dense in the whole real line.
- The color comparison is the usual ordinal comparison, not equality or its reverse.
- The boundary ordinals zero and one are part of the quantifier range.

Marcone–Rosendal, Definition 4.1 and Proposition 4.2, agree with this interpretation: the extension is a continuous increasing embedding of the entire real line whose rational arguments have rational images. Their page 6 was independently rendered and inspected. The range of such a real embedding is a nonempty open interval, possibly proper, with finite or infinite endpoints. Strict monotonicity prevents either endpoint from being attained; continuity fills every intermediate value.

These checks establish the mathematical interface. They do not turn the source's historical question, or a dated literature assessment, into a certification that no later classification exists.

## 2. Dense witnesses and the extension lemma

For an increasing rational map, the displayed four-rational density condition tests every nonempty rational interval lying between two image points. These intervals form a basis for the interior of its convex hull, so the condition is exactly the required density. Suprema of image initial segments then extend the map to the real line. Density rules out a jump at a rational or irrational cut; strict increase follows by placing rational arguments between any two distinct real arguments. Conversely, continuity of a real increasing embedding sends a dense set of source points densely into its real interval image.

The distinction from continuity on the rational subspace is essential. In the manuscript's irrational-cut example, take source arguments 1 and 2 and target test endpoints 3/2 and 2. Their images lie between 1 and 3, but the target interval (3/2,2) is missed. On each rational neighborhood avoiding the irrational cut the map is a translation, so rational-subspace continuity alone would fail to exclude it.

Lemma 2 is correct with **one-way** rational preservation. An increasing bijection between the compact sets preserves the pairs of consecutive endpoints. It therefore matches every bounded complementary interval and the two exterior rays. In each matched pair, both sets of rational interior points have countable dense order type without endpoints, regardless of whether either finite endpoint is rational. A back-and-forth isomorphism of those rational orders extends to an increasing homeomorphism of the corresponding real intervals with the required endpoint limits. Gluing the interval maps to the prescribed compact-set map is strictly increasing and surjective on the real line, hence continuous. Every rational point is either in the compact set or in exactly one complementary interval, so the rational-preservation check is exhaustive.

There is no missing condition requiring rational target points of the compact set to have rational preimages. The full real homeomorphism can send an irrational compact-set point to a rational target point. Such a point is simply absent from the image of the rational restriction. The elementary homeomorphism x ↦ x³ already illustrates the possibility of a rational-preserving real homeomorphism with an irrational preimage of a rational value.

A particularly sharp check comes from the manuscript's actual target construction. Along the all-zero natural branch, the leftmost and rightmost binary branch limits are 2/7 and 5/7. Indeed the normalized left and right interval maps are x ↦ 1/4+x/8 and x ↦ 5/8+x/8. All finite target markers are dyadic, so these rational limits are not markers. Thus equality between the two compact sets' rational parts really would be an unjustified extra assumption. The frozen proof correctly avoids it.

## 3. The fixed compact source

At a node of depth n, each of the two open sides of its rational marker contains a rational-endpoint closed subinterval avoiding the finite set of forbidden rationals. The diameter bound can be imposed simultaneously. The recursive construction therefore exists at every node.

For each infinite binary path, nested closed intervals have a unique intersection because their diameters tend to zero. Distinct paths separate at their first different bit. The branch-point map from Cantor space is continuous and injective, so its image is compact and uncountable. Every fixed rational q_i is excluded from the intervals at all sufficiently large levels on every path. Consequently no branch point is rational.

Every finite marker is rational and is separated from its children and from all incomparable subtrees. It is isolated in the resulting compact set. A sequence of markers of bounded depth has only finitely many possible values; one of unbounded depth has a subsequence following successive binary prefixes, hence converging to the corresponding branch point. Conversely the markers on each path converge to its branch point. These observations justify both compactness and K = closure(A), with K ∩ Q = A.

Nowhere density also follows exactly as stated: a nonempty interval contained in K would contain a marker by density of A in K, while the marker's isolation forbids an interval around it from lying in K. Since K is closed, empty interior is equivalent to nowhere density. No measure estimate, effective coding, or Borel regularity of an uncountable coloring domain is needed.

## 4. The tree code and its topology

Write the parent interval length as L. For natural label k, each child has length L/2^(2k+3), at most L/8. The two children are strictly inside the parent and lie on opposite sides of its midpoint. On each side, adjacent labels have a strictly positive gap. Children with labels at least k are all within distance L/2^(2k+2) of the parent marker. Thus the only possible accumulation point coming from child labels tending to infinity is that marker.

Every marker lies outside all its descendants' intervals. Incomparable nodes lie in disjoint intervals. Hence the markers are globally distinct, not merely distinct within a level. This is enough for continuity of T ↦ ψ_T in the product topology: every rational output coordinate is either constantly zero or tests membership of exactly one finite natural node in T. These are clopen tests. Continuity here is coordinatewise continuity; neither computable recognition of the marker set nor uniform control in the Euclidean coordinate is required.

For a well-founded tree, let x lie in the real closure of B_T. If x is not the current parent marker, the child-family geometry forces x into one child interval and into the closure of the selected markers in that subtree. A fixed child interval is positively separated from the other children and the parent marker. If its subtree contributes a marker, prefix closure places the child node itself in T. Repeating gives either a finite marker or nested natural nodes of every length. The latter would be an actual branch of T, so it is impossible. Thus closure(B_T) = B_T, which is bounded and countable, hence compact.

This argument covers arbitrary well-founded trees, including trees of unbounded finite height and of transfinite rank. It does not assume finite branching or a finite bound on the height. The empty tree is a separate harmless case. Prefix closure is essential: omitting the root while retaining arbitrarily large one-step child labels leaves a missing midpoint accumulation point. The frozen domain includes prefix closure and therefore excludes this failure.

For an ill-founded tree, select a natural branch a. The paired intervals indexed by that branch and all binary strings form a full binary construction. All its finite markers occur in B_T. Its compact closure consists of those isolated markers and its Cantor family of path limits. Both this compact set and the fixed source have the order pattern “zero descendants, node marker, one descendants.” Matching finite and infinite binary addresses is therefore an increasing bijection. The shrinking-cylinder argument gives continuity at all branch points, while the finite markers are isolated. Compactness yields the inverse continuity. No assertion that every rational target point is a selected marker is used.

## 5. The reduction and the analytic upper bound

If T has a branch, the compact order homeomorphism maps every rational point of K, precisely a source marker, to a rational selected target marker. Lemma 2 supplies the required real homeomorphism. Restricting it to Q gives an admissible dense witness. Color 1 is preserved on A; color 0 imposes no additional restriction. This proves the positive direction.

For the converse, any admissible witness extends to a continuous increasing real embedding h. The color inequality sends A into B_T. Since K is compact and A is dense in K, h(K) equals closure(h(A)), and is contained in closure(B_T). The first equality is justified in the ambient real topology because h(K) is compact and hence closed. The set h(K) is uncountable by injectivity, contradicting the preceding countable-closure conclusion for a well-founded tree. It is not necessary for h to be surjective on the real line in this direction.

Thus one continuous map reduces ill-foundedness to the fixed upward section. The argument uses only 0 and 1. Their comparison is unchanged inside every ordinal α ≥ 2, so the same reduction works separately for every such countable ordinal.

For the upper bound, the witness space Q^Q with discrete coordinates is Polish. Strict increase is a countable intersection of clopen conditions. Each instance of the density implication is open, because its consequent is a countable union of finite-coordinate conditions. For a fixed source coordinate q, evaluation ψ(g(q)) is continuous: g(q) is a discrete index, and fixing it reduces evaluation to one ordinary coordinate. Comparison of two colors is clopen in the discrete color product, even for an infinite countable ordinal. The set of witnessing triples is Borel; projection gives analyticity of the relation and each section.

Foreman–Rudolph–Weiss, Theorem 4, supplies the standard non-Borelness of ill-founded trees. The manuscript additionally spells out the continuous tree-section reduction for analytic subsets of Baire space. Accordingly “complete under continuous reductions” has its usual descriptive-set-theoretic meaning, tested on Baire space, or equivalently zero-dimensional Polish source spaces. It is not a claim that every analytic subset of an arbitrary connected Polish space continuously reduces to this zero-dimensional product. With the conventional meaning made explicit, the completeness claim is correct.

## 6. Boundary ordinals and comparison maps

There are no functions from Q into the empty ordinal, while the ordinal 1 gives one constant function. The empty map reduces the empty relation to any relation; there is no map from a nonempty space to the empty one. Hence their Borel degrees differ in the stated direction.

For α ≤ β the coordinatewise inclusion preserves and reflects color inequalities. The allowable rational witnesses do not depend on the color set. Thus it preserves and reflects the complete binary relation, not just a selected section. For α ≥ 2 the non-Borelness proved above rules out reduction to the singleton relation. This establishes precisely R₀ <_B R₁ <_B R₂ ≤_B R_α. It establishes no strictness or reversal among the nontrivial parameters.

Reflexivity uses the identity. For transitivity, compose real extensions of two witnesses. Their composition is continuous, strictly increasing, and rational-preserving, and the color comparisons compose by transitivity of ordinal comparison. Thus the relations being discussed are indeed preorders.

## 7. Least and greatest classes

Constant zero is below every coloring. If a coloring is below constant zero, every one of its coordinates must be zero. This proves that the least equivalence class is a singleton.

For the greatest class, one common target interval for all color tails is crucial. At a source stage of the proposed construction, the finite partial map leaves a nonempty open target gap inside that interval. The target tail at the source point's color is dense there, giving a permissible new value. At an interval stage, an unhit target basic interval contains a smaller open interval in one gap of the finite image. The corresponding source gap contains a fresh rational; its particular color then determines a dense target tail, which meets the chosen target subinterval. Both kinds of stages preserve strict order and the color inequality. Enumerating all source rationals makes the union total, and enumerating all target basic intervals makes its image dense in the common interval. The interior and exterior gaps are both covered, including the initial empty partial map.

A successor ordinal has a maximum, whose constant coloring is locally cofinal everywhere. A nonzero countable limit ordinal has a countable increasing cofinal sequence; assigning its values to a partition of Q into countably many dense pieces makes every color tail dense. Countability is used both here and in the descriptive complexity calculation. This constructs a greatest coloring for every nonzero parameter, including α = 1.

Conversely, a greatest ψ admits a witness from this globally cofinal coloring. Each dense source tail is sent densely into the same real image interval of the witness, and its image lies in the corresponding ψ-tail. Therefore all ψ-tails are dense on that one interval. The condition is both necessary and sufficient.

Restricting a nonempty real interval to rational endpoints loses nothing. For fixed rational endpoints and fixed color, density is a countable intersection of open coordinate-existence conditions. Quantifying over the countably many colors remains a countable intersection. The outer choice of rational endpoints gives a countable union of G_delta sets, hence Σ⁰₃. This is an upper bound only. For a successor, the maximum-color tail implies all the other tails; for α = 1 the condition holds for the unique coloring.

The constant-color comparisons follow by applying the same dense-subset construction at one fixed color, or by observing that every source coordinate must lie below the constant target. Finite nonzero support is handled by assigning its finitely many ordered marked rationals and extending that finite map by Lemma 2. Off the support the color is zero. The zero-support case is vacuous and consistent with the least-class assertion.

## 8. Excluded transfers and the remaining problem

Theorems 5.13–5.14 of Camerlo–Marcone–Motto Ros were checked against their actual statements and proofs in Section 5.3. Their equality and reverse-natural-color relations, and the hypothesis of two incomparable colors, do not specialize to a nontrivial usual ordinal. Already constant 0 embeds below constant 1 under ordinal comparison, while equality and reverse comparison forbid that pair. Reversing the underlying order of Q does not reverse the color comparison.

The continuity results for rational subspaces in Carroy–Pequignot–Vidnyánszky allow the irrational-cut behavior excluded by the source's dense witnesses. The countable closed domains of the Continuous Fraïssé Conjecture paper do not cover the deliberately uncountable source compactum used here. No such theorem is imported to prove the partial result.

Finally, complete analytic sections do not imply universality as a preorder. As an explicit logical control, let A be an analytic-complete subset of a standard Borel space Y, add one point r, and put x S y exactly when x = y or x = r and y belongs to A. This is an analytic preorder with a complete analytic upward section, but it has no strict chain of three equivalence classes. The three-point linear order therefore cannot reduce to it. This illustrates why the manuscript's set reduction cannot replace the missing relation reduction. It makes no additional claim about the universality or nonuniversality of R_α itself.

The remaining source problem is the Borel preorder classification for all α ≥ 2, including possible collapses or strict increases, and analytic preorder universality. The packet must not be described as a full solution or a global openness certificate.

## 9. Independent checks and limits

Independent exact-rational controls passed in normal, optimized, and doubly optimized Python modes. They checked 768 child intervals across three parent intervals, 4,681 distinct paired-tree markers, a separately constructed 511-node rational-avoiding source, and a 511-node selected-branch order match using both small and large natural labels. Other controls checked the rational nonmarker limits, a finite prefix of an unbounded-height well-founded model, a 148-point back-and-forth satisfying 30 interval obligations, the irrational-cut gap, proper interval images, and the color-order and set-versus-relation boundaries. Four deliberately invalid local interval constructions were rejected.

These finite controls neither decide well-foundedness of arbitrary infinite trees nor prove compactness, analytic completeness, or the transfinite cofinality assertions. Those obligations are addressed by the preceding mathematical reconstruction. The full frozen proof hash, source PDF identities, exact source definition, and hypothesis interfaces were also independently checked. No source text, copied paper, raw dataset, program, or private coordination material is part of this public audit.

## Primary references

1. Riccardo Camerlo, *Universal analytic preorders*, Oberwolfach Report 55/2005, printed pp. 3127–3129, Problem 5 on p. 3128. https://ems.press/content/serial-article-files/46028
2. Alberto Marcone and Christian Rosendal, *The complexity of continuous embeddability between dendrites*, Journal of Symbolic Logic 69 (2004), 663–673, Definition 4.1 and Proposition 4.2. https://users.dimi.uniud.it/~alberto.marcone/CED.pdf
3. Riccardo Camerlo, Alberto Marcone and Luca Motto Ros, *Invariantly universal analytic quasi-orders*, Section 5.3, Theorems 5.13–5.14. https://arxiv.org/abs/1003.4932
4. Matthew Foreman, Daniel J. Rudolph and Benjamin Weiss, *The conjugacy problem in ergodic theory*, Annals of Mathematics 173 (2011), 1529–1586, Theorem 4, printed p. 1538. https://annals.math.princeton.edu/wp-content/uploads/annals-v173-n3-p07-p.pdf
5. Raphaël Carroy, Yann Pequignot and Zoltán Vidnyánszky, *Embeddability on functions: order and chaos*, Transactions of the American Mathematical Society 371 (2019), 6711–6738, Section 5.1. https://arxiv.org/abs/1802.08341
6. Arnold Beckmann, Martin Goldstern and Norbert Preining, *Continuous Fraïssé Conjecture*, Definitions 11–12. https://arxiv.org/abs/math/0411117
