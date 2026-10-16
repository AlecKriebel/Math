# Author approach 4: surgery traces, dual spheres, and the product obstruction

## Proposed full construction

Start with a classical knot K of certified large g_4. Its local immersed slice disk in an orientable product M×I has finitely many double points. Choose M with enough topology, then try to remove those intersections without paying a handle for each: tube the disk into closed spheres or tori that are dual to the relevant sheets, as in standard four-manifold constructions. If the resulting surface had genus below g_4(K), it would answer the question positively.

A related version attempts to import the intersecting-tori construction in punctured T⁴ into a product neighborhood of an orientable three-manifold. This attempt investigates the actual intersection data needed to make these constructions work; it does not substitute a general filling for a product.

## Algebraic calculation in a product

Let M be closed, connected, and oriented, W=M×I, and let F⊂W be a compact connected oriented proper surface with sole boundary the local knot K⊂M×{0}. Then

    [F]=0 in H₂(W,∂W;Z).

Proof. The inclusion M×{0}→W is a homotopy equivalence. Consequently the map H₂(∂W;Z)→H₂(W;Z) is surjective. The long exact sequence of (W,∂W) therefore gives an injective boundary map

    ∂:H₂(W,∂W;Z)→H₁(∂W;Z).

It sends [F] to [K]. Because K lies in a ball, its class in H₁(M×{0};Z), and therefore in H₁(∂W;Z), is zero. Injectivity proves [F]=0. This argument is integral and does not assume that H₁(M) is torsion-free. ∎

The absolute intersection form of W also vanishes identically. Every absolute two-class is represented by a cycle in M×{1/3}; another class can be represented in M×{2/3}. These representatives are disjoint, so every pairwise intersection number is zero. Equivalently, the intersection form factors through the map H₂(W)→H₂(W,∂W), which is zero by the preceding exact sequence.

### Consequence for dual surfaces

For every closed oriented surface S⊂W,

    F·S=0.

The same is true for an oriented proper immersed surface with local boundary, since its relative fundamental class obeys the identical calculation. Thus no such S can meet F in exactly one transverse point: a unique transverse intersection would have algebraic number +1 or −1.

This rules out the precise input needed for the direct dual-sphere version of the Norman trick. In a stabilized punctured four-manifold, one uses a sphere with the required single intersection to trade self-intersections for tubes without the same genus cost. No algebraically dual closed surface exists for a local-boundary surface inside an orientable product collar.

Pairs of intersections of opposite signs are not ruled out. But the algebraic calculation supplies neither embedded Whitney disks pairing them nor the required framings and complement control. Their existence would be a new geometric argument, not a consequence of vanishing algebraic intersection.

## Absolute versus relative homology: an important failed shortcut

The result [F]=0 in H₂(W,∂W) does not say that capping F with a classical Seifert surface gives zero in H₂(W). The latter absolute class can be nonzero.

For example, let M=T³, take a local embedded disk D with unknot boundary near M×{0}, and take an embedded coordinate two-torus T in an interior time slice. Join D to T by a thin interior tube along an arc disjoint from both surfaces except at its ends. The resulting embedded punctured torus F still has local unknot boundary. Capping with the original local disk gives the nonzero coordinate-torus class in H₂(T³×I). Yet its relative class is zero, as required above.

Thus relative null-homology cannot be used to erase all ambient topology or justify a classical branched-cover genus calculation without additional work. It also cannot justify lifting F to the universal cover.

## Test against the punctured-T⁴ construction

The low-genus construction in punctured T⁴ begins with the closed tori

    A=T²×{point},       B={point}×T²,

which satisfy A·B=1. Parallel copies and a puncture around their intersection produce the boundary link used in that construction.

A neighborhood preserving this pair of closed tori and their oriented intersection cannot smoothly embed in any orientable product M×I, because all absolute intersections in that product vanish. This is a concrete obstruction to directly transplanting that local four-dimensional configuration into the required collar.

This does not prove that an individual punctured-T⁴ surface can never have another realization in a product. It proves only that this intersecting-tori mechanism cannot be carried over while preserving its geometric input. A different product realization would have to be constructed independently.

## Test using surgery traces

A surgery presentation of M gives a four-dimensional trace from S³ to M. One can concatenate that trace with the product containing F, but the result is a surface in a different four-manifold. Reversing the trace on the other side does not automatically cancel the two-handles relative to F and recover S³×I. The cancellation data are part of the problem.

This distinction can already be seen for the lens spaces L(p,1). The oriented disk bundle over S² with Euler number p has boundary L(p,1) (up to orientation convention). Doubling the disk bundle produces an S²-bundle over S². A section and a fiber have intersection matrix

    [ p  1 ]
    [ 1  0 ].

The determinant is −1. The double has nonzero intersection pairing, whereas any collar of its boundary lens space has identically zero absolute intersection pairing. The closed double has geometric resources that the collar lacks. A surface produced by using those resources need not lie in the collar.

The same warning applies if one kills ambient loops by surgery away from F. Although one-dimensional surgery curves can be chosen disjoint from the two-dimensional surface by general position, the operation changes the ambient four-manifold. It does not establish that the resulting surface can be returned to a product without additional intersections or genus.

## Result of this author attempt

The hoped-for counterexample construction fails at its first required dual-surface input. For local K in an orientable product, the integral relative class vanishes and forbids an algebraic dual intersecting once. The direct T⁴ import fails because its two closed tori have nonzero intersection.

These are useful obstructions to two broad construction shortcuts, not a proof that all genus-saving product surfaces are impossible. Techniques based on canceling pairs of intersections, nontrivial surface-group image, or a more elaborate link concordance are still outside this calculation.

This is substantive author approach 4. No full solution, counterexample, or final disposition is claimed. The source/review stages do not count as additional approaches.

## Sources and independent derivation

The homology exact-sequence argument, product intersection calculation, relative/absolute example, and resulting obstruction above are authored here from standard homology and intersection theory. No novelty is claimed.

The construction being tested appears in C. McDonald and A. N. Miller, Constructing knots with low rational genera, Proposition 2.14: https://arxiv.org/abs/2511.15900 . For the role of dual spheres and the distinction between null-homologous and non-null-homologous slicing, see M. R. Klug and B. M. Ruppik, Deep and shallow slice knots in 4-manifolds, §4: https://arxiv.org/abs/2009.03053 .
