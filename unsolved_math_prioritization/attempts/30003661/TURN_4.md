# Turn 4: computable-arc and finite-graph carrier obstruction

**Scoped obstruction, with no full separation claim.** Turn3 handles every fixed finite discrete choice through intervals. This turn tests whether an infinite extension can remain on a computably parametrized arc or finite embedded graph. Such an extension cannot realize WKL, even with ordinary input-aware postprocessing. The argument concerns nonuniform existence of computable points, not a uniform choice algorithm.

## 1. Every nonempty co-c.e. interval has a computable point

Let J be a nonempty closed interval in [0,1] given by a computable negative name. If J contains at least two points, it contains a rational number, which is a computable point. This is an existence statement: it does not uniformly identify that rational from the negative name.

If J={x}, x is computable uniformly under the singleton promise. For precision n, search for a rational open ball of radius less than 2^(-n) containing all of J. Containment is semidecidable: combine that ball with the enumerated complement of J and search for a finite subcover of the computably compact ambient interval. Under the singleton promise such a ball exists, so this search halts, and its rational center approximates x with the prescribed error. Adjusting the precision by a fixed factor gives a standard fast Cauchy name.

The dichotomy proves nonuniform existence for every such J. It does not let an algorithm decide whether J is a singleton or select a point uniformly across both cases. This is the familiar nonuniform-computability boundary of one-dimensional connected choice.

## 2. Pullback along a computable arc

By a computably parametrized arc we mean the image Gamma=gamma([0,1]) of a computable continuous injection gamma:[0,1]->[0,1]^2. Compactness and the Hausdorff property make gamma a homeomorphism onto Gamma. Let B be a nonempty connected co-c.e. closed subset of the square contained in Gamma.

Then J=gamma^(-1)(B) is nonempty and closed, and it has a computable negative name because computable continuous preimages preserve effectively open complements. Its connectedness follows from the inverse homeomorphism Gamma->[0,1], not from a generally false assertion that arbitrary continuous preimages preserve connectedness. Thus J is a closed interval. Section1 gives a computable t in J, and gamma(t) is a computable point of B.

**Proposition. Every nonempty connected co-c.e. closed set contained in a computably parametrized arc contains a computable point.** The carrier arc need not be supplied uniformly; mere existence of one computable parametrization suffices for this nonuniform conclusion. The carrier itself is not confused with an arbitrary co-c.e. arc lacking a given computable parametrization.

## 3. Finite embedded graph carriers

Let Gamma be a finite embedded graph in the square, with computable vertices and edges parametrized by computable continuous injections, meeting only at their prescribed endpoints. Loops may first be subdivided at a computable midpoint, so every edge has distinct endpoints. Suppose a nonempty connected co-c.e. closed B is contained in Gamma.

If B contains a graph vertex, it contains a computable point. If it contains no vertex, it lies in Gamma minus the finite vertex set. This space is the disjoint union of the open edge interiors, each open in that subspace. Connectedness forces B into one edge interior. Pulling back along that edge's computable parametrization gives a nonempty co-c.e. closed interval as in Section2, hence a computable point of B.

**Theorem. Every nonempty connected co-c.e. closed set carried by a computably embedded finite graph contains a computable point.** There is no assumption of positive information about B and no need to decide which vertex or edge it meets. The proof is deliberately nonuniform. In particular it applies to path-connected B.

## 4. Why this prevents a WKL coding in that class

Use a computable infinite binary tree with no computable path, a standard Kleene-tree instance of WKL. Suppose a proposed computable reduction, strong or ordinary, sent every computable source instance to a negatively computable nonempty connected target B contained in some computably embedded finite graph. For this particular source input, the preceding theorem supplies a computable point x of B and hence a computable Cauchy name of x.

The reduction must work for every oracle realizer, including one that returns that computable name on this target instance. The postprocessor is computable. In an ordinary reduction the source input name is also computable, so allowing access to it does not help. The resulting path through the chosen binary tree would be computable, a contradiction.

Thus no reduction of WKL to this restricted target class exists. The conclusion does not require an effective procedure that finds a carrier graph from the target set or uniformly chooses its computable point. Existence of a computable point on one computable hard input is enough to refute such a reduction.

## 5. Scope controls and literature boundary

The known strict distinction between interval choice and WKL already warns that Turn3's finite interval construction cannot simply be extended to infinitely many decisions. The graph-carrier theorem explains a larger geometric failure mode. Existing continuum results are stronger in some directions; for example the source paper attributes a computable-point result for co-c.e. chainable decomposable continua to Iljazovic. No novelty is claimed here.

Crucially, a finite graph approximation at each stage does not imply that the limiting set has a computable finite-graph carrier. Nor does ordinary path connectedness imply computable parametrizability of its connecting arcs. Replacing one by the other would wrongly collapse the original open problem. The result excludes only the explicit carrier class and leaves unrestricted planar path-connected sets untouched.

`verify_turn4.py` checks exact rational edge/interval witnesses and boundary cases, as finite controls. The computable-point and no-reduction arguments are the proofs above; they are not inferred from sampled carrier sets.

Estimated completion toward the full target:15%, low confidence. Four genuine author turns used; one remains. The remaining route asks whether the carrier obstruction extends to countably many computable arcs without local finiteness. Independent review is pending.
