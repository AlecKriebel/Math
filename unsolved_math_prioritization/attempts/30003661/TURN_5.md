# Turn 5: a Baire-category obstruction to countable computable-arc carriers

**Final author disposition: original strong Weihrauch question unresolved, 5/5 substantive turns complete.** The finite-graph restriction from Turn4 can be strengthened substantially: even countably many computable arcs cannot cover a hard computable path-connected choice instance. The conclusion remains an obstruction to a class of geometric routes, not a proof against arbitrary name-dependent planar encodings.

## 1. A local subarc lemma

Let B be a nondegenerate compact path-connected subset of the plane, and let Gamma=gamma([0,1]) be an arc with gamma a computable continuous injection. Suppose B intersect Gamma has nonempty interior relative to B. We show that B contains a computable point.

Choose x in a nonempty relatively open U subset B with U subset Gamma. Pick y in B different from x. Because U is a neighborhood of x in B, choose r>0 such that

    B intersect closed_ball(x,r) subset U,
    r < distance(x,y).

For example first choose an ambient ball of radius 2r inside an ambient open set inducing U, then decrease r if needed. No effective choice of x,y,r is asserted. Path connectedness supplies a continuous path sigma:[0,1]->B from x to y. Let t be its first time at distance r from x. Such a t exists by continuity, is strictly positive, and has sigma([0,t]) contained in B intersect closed_ball(x,r), hence in Gamma. This path image is compact, connected and nondegenerate, because its endpoints are distinct.

The inverse of gamma is continuous on Gamma, so J=gamma^(-1)(sigma([0,t])) is a nondegenerate compact interval. It contains a rational q. The point gamma(q) is computable and belongs to B. The interval J or its endpoints need not be effectively known; existence of one rational parameter establishes nonuniform existence of a computable point.

This proof covers paths that wait at x for an initial time, paths with backtracking and paths that later leave Gamma. Only the initial segment up to the first exit of the chosen ball is used. It does not replace an arc by its straight chord, and it crucially uses injectivity of the computable parametrization.

## 2. Countably many arcs

**Theorem.** Suppose B is a nonempty compact path-connected co-c.e. closed subset of the unit square. If

    B subset union_(n in N) Gamma_n,

where each Gamma_n is the image of a computable continuous injection [0,1]->R^2, then B contains a computable point. The sequence of parametrizations need not be uniformly computable, and no local-finiteness assumption is required.

If B is a singleton, it has a computable point by the compact negative-information singleton argument in Turn4. Otherwise B is nondegenerate. Each B intersect Gamma_n is closed in B, since Gamma_n is compact. The compact metric space B is complete and hence a Baire space. A countable closed cover cannot consist entirely of sets with empty relative interior. Some B intersect Gamma_n therefore has nonempty relative interior, and Section1 supplies a computable point.

The Baire step is classical, not effective. It does not compute a successful n, a path, a parameter interval or the rational witness. No uniform choice principle is inferred from this existence argument. Co-c.e. information is used only to handle the singleton case; the nondegenerate part is a purely topological argument followed by evaluation of a computable arc at a rational parameter.

## 3. A sharper necessary condition for a hard instance

Let B be a nonempty compact path-connected co-c.e. set with no computable point. It is not a singleton. For every computable arc Gamma, Section1 implies that B intersect Gamma has empty interior in B. This intersection is closed and therefore nowhere dense in B.

There are only countably many computable arc parametrizations, since they are specified by finite programs. Consequently

    B minus union{Gamma: Gamma is a computably parametrized arc}

is a dense G_delta subset of B. In particular it is nonempty. There is no assumption that the set of valid injective programs can be computably enumerated, and no computable point in this residual set is produced. Topological residuality is not an algorithm for selecting a point from a negatively represented space.

The same argument relativizes to any fixed oracle: a relatively co-c.e. hard instance without oracle-computable points has a residual subset outside all oracle-computable arcs. The set-theoretic countability and classical Baire theorem are unchanged.

## 4. Consequence for a hypothetical full reduction

Feed a computable binary tree with no computable branch into any proposed computable reduction of WKL to planar path-connected choice. Its target B has a computable negative name. Every point of B must avoid being computable, because a computable output name, combined with the computable source name and postprocessor, would produce a computable branch. This applies to ordinary reductions as well as strong ones.

Therefore that B cannot be covered by countably many computable arcs, and indeed must have the residual escape property of Section3. A construction assembled entirely from a countable inventory of computable paths cannot suffice if every limiting target point remains on one of those arcs. The restriction is on the final set, not on the finite approximations: limits may create points outside the union of all approximation arcs. Such newly appearing points are a possible escape and are not ruled out.

This leaves a concrete joint difficulty for a positive proof: maintain topological path connectedness through a genuinely non-extensional, infinite planar construction while ensuring that every allowed output name, including names of these additional limit points, decodes a valid source branch. No such construction is obtained here.

## 5. Existing nonuniform examples are not a uniform solution

The additional primary-source check was [Kihara, Incomputability of Simply Connected Planar Continua](https://arxiv.org/abs/1110.6140). Its definition of dendroid includes arcwise connectedness, and Theorem13 gives a co-c.e. planar example without computable points; the constructed example is also contractible. Thus the unrestricted class in the original problem genuinely escapes a blanket computable-point argument.

The paper also distinguishes degree-spectrum/Muchnik conclusions from a uniform Medvedev requirement, and explicitly raises the latter in Question21. Those theorem statements do not by themselves supply a uniform point-name decoder, much less the full uniform transformation of arbitrary WKL inputs demanded here. This is a reading of the cited paper's scope, not a claim that its historical questions have all been checked for present-day status.

## 6. Final boundary and review request

- No arbitrary strong reduction has been excluded: Turn2 only excludes extensional preprocessing, and this turn only restricts possible final carrier geometry
- The finite name-dependent interval construction in Turn3 shows why finite-choice barriers alone cannot settle the question
- Computable parametrizations, merely co-c.e. arcs, arbitrary continuous images and supplied effective paths are distinct forms of information; none is substituted for the source's path-connectedness promise
- The point-existence and Baire arguments are nonuniform. The finite rational checks in `verify_turn5.py` only audit model subarc and first-exit calculations, not the Baire theorem or a universal computation

The exact original strong-equivalence question remains unresolved after all five substantive turns. A full answer still requires an unrestricted uniform strong reduction, or a separation covering all computable name-dependent preprocessors. The ordinary version in the expanded source remains separate. Final completion estimate20%, low confidence, with no historical novelty certification. Freeze the packet for independent review; no sixth author turn is included.
