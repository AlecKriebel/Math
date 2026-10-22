# Independent algebraic / germ route for Kourovka 21.149

Checkpoint: 2026-10-17 13:23 America/Los_Angeles (20:23 UTC).
Authoring agent: `p21149_algebraic`.
Status: independently checkable reductions and obstructions; **not a claimed original complete resolution**. The root/dynamics two-tail proof uses stronger geometry and supersedes the first order-dependent route below. Estimated completion of this route's assigned definition/germ audit: 90%; estimated completion of the full discovery/publication goal is not assigned by this subagent.

## 1. Authoritative definition input

V. Dlab, *On a family of simple ordered groups*, J. Austral. Math. Soc. **8** (1968), 591–608, DOI [10.1017/S1446788700006261](https://doi.org/10.1017/S1446788700006261). Full authoritative Cambridge PDF downloaded as `dlab_1968.pdf`, with extraction `dlab_1968.txt`.

The defining interval class consists of increasing homeomorphisms whose restriction to some right neighborhood of each point below the terminal endpoint is affine with slope in the prescribed multiplicative subgroup H of positive real numbers. The compact-support version is identity near both endpoints. Dlab's Theorem 4.1 classifies all its bi-invariant linear orders by the orders on H, for **arbitrary H**, using the first nonidentity right slope. Theorem 4.3 gives simplicity. These are not statements restricted to rank one.

A. V. Zenkov and N. Ya. Medvedev, *Dlab groups*, Algebra and Logic **38** (1999), 289–298; Russian original 531–548, DOI [10.1007/BF02671746](https://doi.org/10.1007/BF02671746). Primary Russian PDF endpoint:
<https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt>.

Direct retrieval of that endpoint repeatedly timed out during this subtask. Web search indexing did expose the PDF's p. 542 proof of the full extended-real group's affine-germ decomposition, and p. 537 introduction to Section 2. **The downloaded full primary PDF is still needed for a complete source audit.** The p. 542 argument explicitly represents an element outside the subgroup fixing a left ray by an affine map on a sufficiently far left ray, and factors every full extended-real element into that affine map and an element fixing a left ray. Consequently the standard extended-real definition is not merely finite-point local right affinity: it also requires an eventual affine germ at minus infinity.

This eventual-affine condition is essential. The tempting larger class in Section 4 below does not have it.

## 2. Rank-independent perfect-subgroup reduction at minus infinity

Let A be any group of increasing homeomorphisms of the extended real line whose members are affine sufficiently far left. The slopes may lie in any multiplicative subgroup H of positive reals. There is a homomorphism

    germ_-infinity : A -> Aff_+(R),

where the germ is represented uniquely by x -> a x+b. The composition law is

    (a,b)(c,d) = (ac, a d+b)

when maps act on the left and composition means ordinary functional composition. Thus this germ group is metabelian: its slope homomorphism has abelian kernel (translations), and the slope image is abelian.

**Lemma.** Every perfect subgroup P of A consists of maps fixing some left ray, with the ray allowed to depend on the element.

**Proof.** The image Q of P under the germ homomorphism is perfect. It is also a subgroup of a metabelian group. Hence Q=Q'=Q''=1. Each element therefore has identity germ. By the definition of a germ at minus infinity, this means that each p in P equals the identity on some interval (-infinity,c_p). No countability, uniform bound, linear-order, slope-rank, or topology-of-P hypothesis is used. QED.

In particular this holds for the image of the simple compact-support source D_<2>([0,1]), and for every local source subgroup supported compactly inside an open source interval.

For the reflected real subgroup D_*H whose elements are identity sufficiently far right, the lemma forces any perfect embedded source into the bounded-support subgroup D_H. For the full real group bar(D_H), it forces the source into D_H*. Both conclusions hold for arbitrary H. The conjugating element itself need not belong to these kernels.

A perfect source on a bounded interval also fixes a right neighborhood of the left endpoint individually: the right slope at that fixed endpoint is a homomorphism into the abelian group H, so perfection makes that slope 1; an affine germ of slope 1 through a fixed point is the identity germ.

**Relevance to the two-tail proof.** This provides exactly its finite-left-endpoint condition for each image element. Coupled with well-ordered support components and local affine germs at finite fixed points, it avoids every ambient-order classification issue.

## 3. A useful simplification of the published rank-one argument

The September 2026 Gong–Yang–Zeng proof uses, in Lemma 4.2, a rank-one argument to rule out equality of the first breakpoints of two commuting local subgroup elements. This strict inequality is stronger than needed.

Here is the independent replacement, conditional only on an ambient first-breakpoint sign rule for some ordered H.

Let P,Q be the images of source local groups supported on L<M. Suppose their least action components coincide in K=(a,b), where all nontrivial elements p,q have finite first support endpoints lambda(p),lambda(q)>a, and

    inf_{q != 1} lambda(q) = a.

Order preservation and the source's leftmost-support order imply

    sign(p q^n)=sign(p)  for all integers n.

If lambda(q)<lambda(p), then p is identity just to the right of lambda(q), and the first germ of p q^n is exactly that of q^n. The two choices n=1 and n=-1 have opposite signs for every ordered H. They cannot both have sign(p). Thus

    lambda(q) >= lambda(p)  for all p != 1, q != 1.

Fix p0. Then inf_q lambda(q) >= lambda(p0)>a, contradiction. Equality of breakpoints never needs to be excluded; neither Archimedean behavior nor rank one is needed.

**Scope.** This yields a genuine proof simplification for any ambient family whose given order has a first-breakpoint description for arbitrary H. Dlab 1968 supplies that description for the compact-support interval family. I did not independently establish the corresponding all-H classification for every noncompact family. Treating that unproved classification as automatic would transfer the central problem to an unsupported hypothesis. The geometric centralizer/two-tail route avoids this gap entirely.

## 4. Twisted diagonal embedding: correct in an enlarged class, inadmissible for standard real Dlab groups

The root agent suggested the following counter-embedding test. For n in Z set

    I_n=[-2^(n+1), -2^n],
    ell_n(x)=-2^(n+1)+2^n x  (0<=x<=1),
    t(x)=2x for x<0, and t(x)=x for x>=0.

For an automorphism alpha of the compact-support source G, define e(g) on I_n by the affinely transported alpha^n(g), and identity on [0,infinity). In the class of maps only required to be locally right affine at **finite** points, this is valid: each alpha^n(g) is identity near the block endpoints, and the only accumulation of block endpoints at a finite point is from the left at 0, where the right germ is the identity. The shift t satisfies

    t^-1 e(g) t = e(alpha(g))

with ordinary left functional composition and the displayed indexing. Hence this would realize arbitrary alpha by an inner automorphism of that enlarged homeomorphism class.

**Fatal membership obstruction.** For every nontrivial g, e(g) fixes all block endpoints -2^n and acts nontrivially in every block, including arbitrarily far left. If it agreed with a single affine map on some left ray, that affine map would have infinitely many distinct fixed points and hence would be the identity. But e(g) is nonidentity in infinitely many blocks on that same ray, contradiction. Therefore e(g) is not eventually affine at minus infinity and does not belong to the full standard extended-real Dlab group or its reflected subgroup. This route is **blocked** by a precise failed hypothesis, not evidence of an embedding into a permitted Dlab group.

A second consistency test shows why the enlarged class should not be silently substituted for an ordered Dlab group. Pick a nontrivial compact PL bump c with slopes in <2>. Put c in even blocks and c^-1 in odd blocks. The resulting b is conjugate to b^-1 by t. Thus it has generalized torsion and the enlarged class admits no bi-invariant linear order. The ordinary Dlab ambient with its affine germ at minus infinity avoids that element.

For a completely explicit c, let c be identity outside [1/4,3/4], let c(x)=2x-1/4 on [1/4,5/12], and c(x)=x/2+3/8 on [5/12,3/4]. Both formulas give 7/12 at 5/12, and c is continuous and increasing. This makes the failed enlarged-class example exact, with no numerical assumptions.

## 5. Other algebraic routes examined and rejected

- **Local indicability.** Finitely generated subgroups of the finite-left-endpoint right-affine class have a first active germ and hence a nontrivial homomorphism into an abelian slope group. This does not distinguish G semidirect-alpha Z: any subgroup mapping nontrivially to Z is indicable, and a subgroup contained in G inherits local indicability. It gives no obstruction for the proposed source automorphisms.
- **Pure semidirect-product embeddability.** A conjugating realization always yields a homomorphism from the semidirect product, but injectivity requires care if a nonzero power of alpha is inner. It is therefore wrong to assume without proof that every realization embeds G semidirect-alpha Z. More importantly, no new quasivariety identity separating the relevant semidirect product from all genuine Dlab families was found. Rephrasing 21.149 as that embeddability question is not a solution.
- **Archimedean classes of slopes.** Higher-rank slope orders may have infinitesimal elements, so the assertion that s t^n crosses 1 in both directions is invalid for arbitrary ordered H. The non-strict endpoint argument in Section 3 avoids that exact error. No general collapse of higher-rank slope orders to the usual real order is justified.

## 6. Exact strongest verified outcome of this subtask

The germ reduction in Section 2 is elementary, self-contained, and independent of the rank of H. The twisted-diagonal proposal fails the actual eventual-affine-left hypothesis. The endpoint simplification in Section 3 removes one artificial use of rank one, but is not on its own a proof for every ambient order. The root/dynamics two-tail proof can use the Section 2 reduction directly and does not require the incomplete all-H order classification.

No external outreach, publication, git mutation, or claimed resolution was performed by this subagent. The result is a research checkpoint for adversarial validation and the root's final source/priority audit.
