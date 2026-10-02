# Turn 2: exact finite capacity of extensional planar preprocessing

**Scoped result: extensional preprocessing can encode at most four finite choices into planar path-connected choice with strong decoding, and four can be achieved. The full source target remains unresolved.** General Weihrauch preprocessors are allowed to depend on the input name, so this does not prove the requested nonreducibility. The planar crossing-parity ingredient is classical, not new.

## 1. Extensional negative-information preprocessing is monotone

Call a preprocessor extensional if every negative name of a source closed set A produces a negative name of the same target set B(A), even though the resulting target name itself may vary. Suppose it is computable, or just continuous at the name level. Then

    A subset D implies B(A) subset B(D).           (1)

Here is a direct name proof, without a hidden positive-information representation. Fix a negative name of D. Any finite prefix of that name can be extended to a negative name of A, because every ball already enumerated outside D is also outside A. Any output ball enumerated outside B(D) is determined by some finite input prefix. On an extension of that prefix naming A, the same output ball is enumerated. Extensionality ensures that this output describes B(A), so the ball is outside B(A). Since the output balls exhaust the complement of B(D), the complement of B(D) is contained in the complement of B(A), proving (1).

The extension remains within the nonempty-set domain whenever A is nonempty. No decision whether an input enumeration is complete is used. Extensionality of the *target set*, rather than of its name, is essential.

## 2. A monotone five-choice obstruction

Let a_1,...,a_5 be five distinct source points. Suppose each nonempty subset A of these five points is assigned a nonempty compact path-connected planar set B(A), with monotonicity (1), and suppose one strong postprocessor works for all these inputs.

By Turn 1's name-level shared-output lemma,

    A intersect D empty implies B(A) intersect B(D) empty.     (2)

Choose v_i in B({a_i}). The v_i are pairwise distinct. Monotonicity places v_i and v_j in B({a_i,a_j}); path connectedness supplies a continuous path gamma_ij between them inside that set. For disjoint edges {i,j} and {k,l}, their path images are disjoint by (2). A vertex v_k with k not in {i,j} is likewise disjoint from the gamma_ij image.

We have therefore drawn all ten edges of K5 by continuous paths in the plane, with disjoint independent-edge images and no nonincident vertex on an edge. Such an almost embedding is impossible.

For clarity about wild paths, only finitely many compact path images occur. Every pair required to be disjoint has positive distance. Uniform polygonal approximations and a sufficiently small general-position perturbation preserve those disjointness requirements and keep the fixed endpoints. Polygonal self-loops can be removed without introducing intersections with independent edges. This would give a graph drawing whose independent edges have zero crossings, contradicting the classical parity lemma recalled next.

## 3. The precise classical parity obstruction

**K5 parity lemma.** In a general-position planar drawing of K5, the total number of crossings of pairs of independent edges is odd.

This is a classical consequence of Hanani/Kleitman crossing parity; see [Cairns–Groves–Nikolayevsky, Bad drawings of small complete graphs](https://arxiv.org/abs/1903.06292), the discussion of Kleitman's theorem in Section 6. A short parity explanation is included to make the exact ingredient transparent.

Move the five vertex positions by a plane homeomorphism to a convex pentagon and approximate the resulting finite paths in general position. Replace one edge path at a time by its straight chord, keeping endpoints fixed. The old and new paths together form a closed mod-two cycle. The edges independent of this edge form the triangle on the other three vertices, another closed mod-two cycle. Two closed planar cycles have even total intersection parity, by decomposing polygonal cycles into simple loops and applying the Jordan separation property. Therefore this replacement changes the total independent crossing count by an even number. After all replacements the convex straight-line K5 has one crossing for each four-vertex subset, hence five crossings. The original count is odd as well.

Adjacent-edge crossings do not enter the count. They may occur during replacements and do not invalidate the argument. This distinction is why ordinary nonplanarity alone, without controlling crossings of independent edges, should not be used as a shortcut in Section 2.

Sections 1–3 prove:

**Theorem A.** There is no strong reduction from choice on a five-point discrete space to planar path-connected choice whose negative-information preprocessing is extensional as a map of closed sets. More generally, no monotone assignment of compact path-connected planar sets can satisfy the disjointness condition (2) for all nonempty subsets of five source points.

## 4. Sharpness at four choices

For a four-point source space label the points 1,2,3,4 and fix a rational crossing-free straight-line embedding of K4 in the unit square: use three vertices of a triangle and one strictly interior vertex. For example take

    v_1=(1/8,1/8), v_2=(7/8,1/8),
    v_3=(1/2,7/8), v_4=(1/2,3/8).

For each nonempty label set A, let B(A) be the union of its vertices and all embedded edges with both endpoints in A. This is the geometric realization of the induced complete graph, not its filled convex hull. It is compact, nonempty and path connected. It is monotone in A. Because the embedding has no crossings or nonincident vertex-edge contacts, disjoint label sets have disjoint output sets.

This preprocessing is computable from negative information. Maintain the finite candidate label set S of points not yet excluded. Enumerate the computable open complement of the finite rational graph B(S). As further labels are excluded, S decreases and B(S) decreases. The union of the enumerated complements is exactly the complement of B(A). In a finite source, every excluded label eventually appears, so S eventually equals A, without needing to recognize that stage.

There is also a computable strong decoder. For each label i let F_i be the finite closed union of every embedded vertex other than v_i and every embedded edge not incident to i. Given a Cauchy name of an output point x, search for an i with

    distance(x,F_i)>0.                          (3)

Distances to these finite rational segment unions are computable, so strict positivity is semidecidable. The search terminates for every point of the embedded K4: at a vertex choose its own label, and in an edge interior choose an endpoint. Nonincident edges never meet that point. If x belongs to B(A) but i is not in A, all cells making up B(A) are contained in F_i; hence (3) is impossible for that i. Every returned label is therefore in A.

The decoder sees only the output point name and fixed finite geometry, not A. No preferred name is assumed, and no distance-equality test is performed. Restricting labels gives the same construction for one, two or three choices.

**Theorem B.** Four is the maximum n for which a strong reduction from n-point closed choice to planar path-connected choice can have an extensional computable preprocessor. The negative part already excludes continuous extensional preprocessing at size five and above.

## 5. Implication for the source target and the exact remaining gap

A hypothetical extensional preprocessor for C_[0,1] reducible_sW PWCC_2 would restrict to the five-point situation, contradicting Theorem A. Thus any successful strong reduction for the full source must use the freedom to depend on the negative *name*, not merely the underlying source set. This does not exclude a general strong Weihrauch reduction: its preprocessing is a function on names and is not required to be extensional at the target-set level. The known connected-only planar construction already illustrates why name/order dependence cannot be ignored in this subject.

The theorem also does not exclude ordinary Weihrauch reductions, for which the shared-output lemma fails when the decoder retains the source input. The assigned strong problem and the paper's ordinary Question7.3 remain distinct.

`verify_turn2.py` checks the exact rational K4 geometry, every finite subset pair, the decoder's allowed labels on exact sample points, the K5 independent-edge parity bookkeeping and a finite mod-two rank certificate. These are finite controls on the stated proof, not a search over all name-dependent reductions.

Estimated full-target completion: 15%, low confidence. Two of five substantive turns used; three remain. Independent review and historical novelty assessment are pending.
