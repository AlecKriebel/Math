# Author approach 1: finite-image lifting and stable genus

## Target and status

Problem 30004818 asks whether some local classical knot K in an orientable smooth three-manifold M satisfies g_{M×I}(K) < g_4(K). Here g_{M×I} minimizes the genus of a compact connected orientable smooth properly embedded surface whose sole boundary is K in M×{0}.

This is one substantive author attempt, not a literature-review turn. It derives a restricted obstruction and identifies exactly why the covering strategy does not settle the full question. No full solution or counterexample is claimed. The result below is an authored deduction from the standard covering-space and compression facts; novelty is not claimed.

## Proposition: a finite-image bound

Let M be a closed connected oriented smooth three-manifold, let K lie in an embedded three-ball B ⊂ M, and let F ⊂ M×[0,1] be a compact connected oriented smooth proper surface of genus g with ∂F=K⊂M×{0}. Suppose the image H of π_1(F)→π_1(M×I)=π_1(M) is finite, of order d. Then

    g_4(#^d K) ≤ d g.

Consequently the stable smooth four-genus satisfies

    g_st(K) := lim_{n→∞} g_4(#^n K)/n ≤ g.

Thus if g_st(K)=g_4(K), no genus-saving surface for K in an orientable M×I can have finite fundamental-group image. In particular, when π_1(M) is finite and g_st(K)=g_4(K), one has g_{M×I}(K)=g_4(K).

### Proof

1. The projection of F to M is the image of a smooth map from a compact two-manifold to a three-manifold. It has empty interior (for example, by Sard's theorem). Choose a small closed three-ball D disjoint from that projection and from B. Set W=M\int(D). The puncture does not change π_1, and F remains properly embedded in W×I with its only boundary on W×{0}.

2. Let p:W~→W be the universal covering map, and pull back F under p×id. Take a connected component F~ of the preimage. Covering-space monodromy shows that F~→F is the covering corresponding to ker[π_1(F)→π_1(W)]. Its degree is exactly d=|H|. In particular, this is a finite covering and F~ is compact. This step lifts a finite cover of F, not F itself.

3. The boundary K is null-homotopic in W because K is local. Therefore the boundary monodromy is trivial. Each of the d preimages of a point of K belongs to a distinct boundary component, and each boundary component maps with degree one to K. Hence F~ has d boundary components. Euler characteristic gives

    χ(F~)=d χ(F)=d(1−2g),
    2−2g(F~)−d=d(1−2g),
    g(F~)=1+d(g−1).

4. The universal cover of a punctured closed oriented three-manifold smoothly embeds in S³. This is the compression lemma of Boden–Nagel; in the accessed arXiv manuscript it is Lemma 2.10 (the later numbering cited by Klug–Ruppik is Lemma 2.11). Choose the embedding to preserve orientation. Its product with id_I sends F~ into S³×I. The d boundary components lie in distinct lifts of B, whose images are disjoint three-balls in S³. They therefore form a split union of d copies of the same oriented classical knot K. Orientability of M is essential here: the lifts have the same ambient orientation, rather than a mixture of K and its mirrored orientation variants.

5. In an added boundary collar S³×[−ε,0], attach d−1 oriented standard connected-sum bands to this split link, arranged along a tree of disjoint arcs connecting the balls. The resulting boundary is #^d K. These bands are embedded and disjoint from the old surface except at their prescribed attaching intervals. The resulting surface is connected, orientable, and has one boundary component. Each band decreases Euler characteristic by one, so

    χ(new surface)=d(1−2g)−(d−1)=1−2dg.

Its genus is dg. Reparametrize the interval to obtain the required classical bounding surface. This proves g_4(#^d K)≤dg.

6. Subadditivity of g_4 under connected sum implies, by the elementary subadditive-limit lemma,

    g_st(K)=inf_{n≥1} g_4(#^n K)/n.

Taking n=d yields g_st(K)≤g. For a stable-genus-sharp knot, this lower bound and the universal local upper bound g_{M×I}(K)≤g_4(K) prove the corollaries. ∎

## Additive-invariant corollary and the original trefoil example

Let v be any additive knot concordance invariant satisfying |v(J)|≤g_4(J) for every classical knot J. The finite-image proposition yields

    d |v(K)| = |v(#^d K)| ≤ g_4(#^d K) ≤ dg,

hence |v(K)|≤g. In particular, if the signature bound |σ(K)|/2=g_4(K) is sharp, the finite-image route cannot save genus. For the connected sum of two equally handed trefoils, the signature has absolute value 4 and the classical four-genus is 2. It cannot bound a genus-one surface with finite π_1-image in an orientable product M×I. This rules out a direct finite-monodromy orientable imitation of the OWR example.

## Attempted strengthening and exact obstruction

The hoped-for proof was that passing to a cover always preserves the genus of a bounding surface. The computation above refutes that step: a nontrivial image of order d produces a genus 1+d(g−1) surface with d boundaries, and joining the boundaries costs d−1 extra handles. The resulting single-boundary genus is dg, not g.

Even after dividing by d the conclusion concerns stable genus, which need not equal g_4. For example, the figure-eight knot is non-slice and has g_4=1, whereas its concordance class has order two, so its stable genus is zero. The known genus-zero theorem separately handles that particular knot; the example only shows that replacing stable genus by ordinary genus is an invalid general inference.

If H is infinite, the connected pullback F~ has infinitely many sheets and is not compact. Cutting out a compact piece introduces additional boundary that the argument cannot cap for free. Residual finiteness of π_1(M) does not repair this: a finite cover need not kill the infinite subgroup H, and its ambient covering three-manifold need not embed in S³ or S⁴. No conclusion for arbitrary H follows here.

Likewise, an arbitrary small-genus surface for #^d K cannot simply be divided by a cyclic group. An equivariant embedding, a free ambient action, the correct local boundary orbit, and the desired quotient product structure would all need construction. Numerical stable-genus savings alone are not a counterexample.

## Concrete next author routes, not yet counted

- Analyze genus-one surfaces using the fact that π_1(Σ_{1,1}) has generators a,b and local boundary forces [i_*(a),i_*(b)]=1. Any genus-one candidate therefore has abelian image generated by at most two elements. This is only an algebraic restriction; an embedding/compression theorem for the corresponding subgroup cover would still be needed.
- Try a genuinely equivariant surface in a spherical cover and verify that its quotient has local boundary and ambient product M×I.
- Test whether the low-genus Spin(L(3,1)) constructions of McDonald–Miller can be localized to a collar. Their existing filling theorem supplies no such localization.
- Use a surgery description of M×I and track both ends of every handle; a surface in a surgery trace alone is not enough.

## Public references

- H. U. Boden and M. Nagel, Concordance group of virtual knots, https://arxiv.org/abs/1606.06404 and https://doi.org/10.1090/proc/13667.
- M. R. Klug and B. M. Ruppik, Deep and shallow slice knots in 4-manifolds, https://arxiv.org/abs/2009.03053, §2.
- C. Livingston, The stable 4-genus of knots, https://doi.org/10.2140/agt.2010.10.2191 and https://arxiv.org/abs/0904.3054.
