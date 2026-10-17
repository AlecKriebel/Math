# Independent adversarial review: Kourovka 21.149 dynamics route

Timestamp: 2026-10-17 13:22 America/Los_Angeles (20:22 UTC; tool clock).
Reviewer: independent adversarial subagent `p21149_adversary`.
Scope: mathematical attack on the proposed abstract target-class obstruction; no complete solution or publication is claimed here.
Checkpoint estimate: 90% of this initial abstract-proof audit; approximately 25% toward a fully sourced resolution of every intended Kourovka quantifier. The latter is not a proof-confidence percentage.
No external individuals were contacted. No Git, PR, queue, publication, or tracker operation was performed.

## Finding

The **two-tail argument survives this independent audit under its three explicit target hypotheses**: well-ordered support components, affine right germs at finite fixed points, and finite left endpoints for components of the relevant embedded local groups. It avoids the delicate full diagonal-action reconstruction, and in particular does not need an Archimedean order on the ambient slope group. No counterexample to that abstract theorem was found.

This is **not yet a verified resolution of the complete Notebook problem**. The exact extended-real Dlab definitions, especially any reflected family, remain a substantive scope issue. The naive group of all locally right-affine maps of the real line with support bounded above admits an explicit Klein-bottle relation and is not bi-orderable; it cannot simply be included or excluded by nomenclature.

## Independently checked centralizer mechanism

Let A act by increasing homeomorphisms on a real interval. Suppose every element has well-ordered support components and has an affine right germ at each finite fixed point. Let q in A, and let P be a perfect subgroup commuting with q. Assume every support component of q has finite left endpoint.

Each p in P permutes the support components of q in their natural order. Every order automorphism of a well-ordered set fixes every point, by transfinite induction. Thus p preserves each component J=(a,b) and fixes its finite endpoint a. The right slopes at a define a homomorphism P to the abelian multiplicative positive reals. Perfection forces all slopes to equal one, so each p has an identity right germ at a.

The restriction of q to J has no fixed point. Suitable positive or negative q-iterates of every x in J converge to a. Choose such an iterate in the identity germ of p; commutation and injectivity give p(x)=x. Thus P fixes supp(q) pointwise.

In particular, commuting images of perfect source local groups have disjoint supports. This argument uses the real-valued slope only as an abelian germ invariant; it makes no comparison between its numerical size and a chosen group order.

**Scope warning:** the hypothesis about finite left endpoints is needed by this proof. For a component beginning at minus infinity there is no finite affine right germ to use. A solvable-germ substitute would need its own proof from the exact target definition.

## Least action components

The standard simplicity theorem for G=D_<2>([0,1]) and for every local subgroup G(L) is an external input that must be cited accurately. Once it is supplied, every nontrivial action-component restriction is faithful: the kernel is a proper normal subgroup of a simple group.

Fixing one nonidentity source element, each action component contains a support component of its image. An ordered subfamily of a well-ordered family is well ordered, so the nontrivial action components of e(G) have a least member J0. The same argument inside J0 gives the least component K(L) of e(G(L)). A normalizer of e(G) fixes J0; a normalizer of e(G(L)) which fixes J0 fixes K(L). These are purely topological statements.

The nesting proof must choose the **least** local component inside K(M), when L is contained in M. An arbitrary local component inside K(M) need not be the least one. This is a repairable wording issue in the September preprint's corresponding argument, and the current dynamics note explicitly repairs it. Nesting is not needed for pairs having a positive source gap, which are sufficient for both tails.

## Uniform orientation without order assumptions

For any two increasing finite tuples in (0,1), there is a compactly supported finite piecewise-affine map with slopes in <2> carrying the first tuple to the second. One direct construction fixes points a and b outside both tuples. On each segment of the resulting subdivision, the required positive average slope r is a convex combination of adjacent powers 2^k and 2^(k+1). Splitting that segment accordingly gives the desired two affine pieces, with the single-piece boundary case allowed. The map fixes everything outside [a,b].

Therefore any ordered pair of relatively compact open source intervals with a positive gap is carried to any other such pair by some g in G. The equation K(gL)=e(g)K(L) follows by conjugating the local subgroups and using increasing preservation of the least component in J0. Since e(g) is increasing, **one uniform orientation applies to all such ordered interval pairs**. Either L<M always implies K(L)<K(M), or it always implies K(M)<K(L).

This proof does not confuse the order on the group with pointwise movement. It also allows the orientation-reversing alternative, so it does not silently assume that every embedding is increasing diagonal.

## Two-tail contradiction checked independently

Choose an increasing h on [0,1], locally finite piecewise affine with slopes in <2> on (0,1), with bump components C_m descending to zero and D_m ascending to one, and identity between the tails. A reflected finite-piece bump is still finite piecewise affine, so constructing the right tail by reflection is legitimate; one is not reflecting arbitrary elements of G. The conjugation alpha(g)=h g h^-1 preserves G and its two standard orders because every g has support compactly inside (0,1), and its first right slope is unchanged under conjugation.

Suppose u implements alpha after an embedding e into an eligible A. It fixes J0. For every tail component L, h(L)=L, so alpha normalizes G(L), and u consequently fixes K(L) setwise.

The restriction of u to K(L) is nonidentity. Otherwise conjugation by u acts trivially on the faithful restriction of e(G(L)), forcing alpha to act trivially on G(L). To contradict that conclusion directly, choose x moved by h in L and a sufficiently small open V compactly inside L with V and h(V) disjoint. A nonidentity bump supported in V is carried to one supported in h(V), and therefore changes under alpha.

Every finite endpoint of K(L) is fixed by u, because u preserves this interval and is increasing. A component of supp(u) containing a moved point of K(L) cannot cross either such endpoint; infinite endpoints cause no crossing issue in the real line. Thus K(L) contains a genuine ambient support component of u.

If orientation is increasing, the intervals K(C_m) descend strictly. If orientation is decreasing, the intervals K(D_m) descend strictly. Select one support component of u in each of the corresponding intervals. These are distinct and form a strictly descending family, contradicting well ordering. No common support component can accidentally serve two intervals, because they are disjoint and their finite boundaries are fixed.

No full action conjugacy, semiconjugacy, absence of Denjoy gaps, or centralizer uniqueness is used in this version. Thus those potential failure modes do not apply to the shortened proof.

## Explicit counterexample to the naive reflected-real definition

Let A_naive consist of all increasing locally right <2>-affine homeomorphisms of R fixing some final ray. Define

    b(x)=x+1             for x<=0,
    b(x)=x/2+1           for 0<=x<=2,
    b(x)=x               for x>=2.

This b belongs to A_naive. The intervals I_n=b^n((0,1)), indexed by every integer n, tile (-infinity,2) apart from their endpoints. They are in increasing order with n, accumulate only at minus infinity on the left and at 2 from the left on the right. Take a nonidentity finite piecewise-affine bump q supported compactly inside (0,1), with slopes in <2>. Define a on I_n by

    a|I_n = b^n q^((-1)^n) b^(-n),

and make a the identity at all cell endpoints and on [2,infinity).

At each finite point below 2 there is an affine right neighborhood: each cell copy has finitely many pieces and is identity near the cell endpoints. At 2 there is an identity right neighborhood, exactly as the one-sided definition requires. Hence a also belongs to A_naive, with slopes in <2> and support bounded above.

On I_n, conjugation b a b^-1 replaces the exponent (-1)^n by (-1)^(n-1), so

    b a b^-1 = a^-1,       a != 1.

This is impossible in a bi-ordered group: conjugation preserves the sign of a, while inversion reverses it. Thus A_naive is not bi-orderable. This also shows why a missing global well-order condition cannot be harmlessly restored after the fact.

This construction is an independently verified obstruction to a proposed ambient *definition*, not a disproof of Kourovka 21.149. Whether Zenkov-Medvedev's D_*H means A_naive, a reflected locally-left class, or a more restricted class has to be settled from the primary text before declaring complete coverage.

## Remaining substantive tasks

1. Read and archive the exact defining sections of Dlab (1968), Zenkov-Medvedev (1999), and the authoritative Notebook reference conventions; enumerate every intended ordered target family.
2. For each family prove or cite, within the exact hypotheses, the three target properties used above. In particular address every potential component starting at minus infinity.
3. Perform a renewed originality search for the rank-independent perfect-centralizer/two-tail route. The one-tail rank-one result and related automorphism were already published as a September 2026 preprint; do not claim that witness or restricted theorem as new.
4. Write a complete manuscript with an explicit ambient-class theorem, then assign a fresh reviewer who did not devise this proof. The present audit is not a substitute for that review or for a proof.

## Sources inspected

The current dynamics notes and independent priority audit in this problem directory; the full HTML of Gong-Yang-Zeng, arXiv:2609.18630v1, particularly the hypotheses and the least-component proof; primary MathNet indexed records for the 1999 and 2001 Dlab papers. This review's mathematical constructions and checks above are independent derivations. Full access to the 1999 primary definition was not obtained during this initial audit.

## Primary-source lead obtained after the initial audit

The search index exposes printed p. 543 of the 1999 Russian paper at the [MathNet full-text endpoint](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt). Its Proposition 2.3 describes D_*H as a semidirect product of D_H by a subgroup isomorphic to T_H, for rank-one H. The page also says D_*H is the bounded-above-support subgroup of the full extended-real Dlab group. The article DOI is [10.1007/BF02671746](https://doi.org/10.1007/BF02671746).

This is evidence that the primary D_*H has an additional global breakpoint restriction absent from A_naive. The likely mechanism is an eventual affine germ at minus infinity. **That mechanism remains conditional until the defining passage is read.** If every full real Dlab element is affine on some initial ray, its affine germ defines a homomorphism to Aff_+(R), a metabelian group. Every perfect embedded source subgroup has trivial image under this homomorphism and hence every one of its elements fixes an initial ray. This would supply precisely the finite-left-endpoint input missing from the abstract proof, without any rank assumption. It would also apply to a reflected/bounded-above subgroup of the full real group.

Independently, any group of eventually-left-affine, locally-right-affine homeomorphisms has well-ordered support components. A nonidentity affine left germ supplies one initial support component extending to minus infinity; all later components are bounded below by a finite point. If the left germ is identity, all support components are bounded below. An infinite descending family with finite infimum would accumulate from the right at a fixed point, contradicting that point's affine right germ. Thus the conditional germ approach exactly repairs the structural issue; it does not justify replacing the primary definition by A_naive.
