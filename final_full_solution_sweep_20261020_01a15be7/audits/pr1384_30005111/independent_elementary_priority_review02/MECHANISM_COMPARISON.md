# Independent comparison of the actual proof mechanisms

This concerns the graph-specialized steps actually used, not an automatic inference that any proof of the same theorem answers a later request for a new elementary proof.

| PR finite formulation | Older mechanism actually found | Assessment |
|---|---|---|
| Nongradient integer cochain c with evaluation0 on W | Nontrivial homomorphism π1(H)→Z killing the circle class; its associated cyclic cover admits a lift | Coordinate description of the standard graph covering construction. In a spanning-tree gauge, the edge periods are integer coordinates in H1(H). Rank≥2 gives a nonzero annihilator of one vector. |
| Finite graph of the visited lifted edges/vertices | Image subcomplex K1=Im f1 in Howie's original Lemma3.1 | Same operation. The entire voltage graph need not be finite or connected. |
| Strict increase in image vertices, bounded by the number n of domain vertices | Original Howie induction on d(X)−d(K0), d=number of0-cells | Same invariant and termination bound. |
| No rank≥2 remains, minimum degree2 implies circle, nonpower makes degree1 | Terminal circle and homeomorphic lifted map in LW3.4 | Explicit routine graph deductions in place of compressed covering language. |
| h=a+epsilon b, with integer sheet separation and bounded perturbation | LW3.3 embeds cover×R over H by disjoint narrow translates; LW3.4 descends the stacking | Compact affine version of that same descent, with useful explicit constants. |
| Proper repetition forces a nowhere-zero continuous height difference whose orbit sum is0 | Necessary direction of the known nonpower criterion | Correct short argument; no separately new mechanism was established. |

For the first row, choose a spanning tree T. Subtract a vertex gradient to put all T-values at0. The remaining r=E−V+1 edge values are the periods defining Hom(π1(H),Z). Killing W imposes one integer linear equation. If r≥2, its rational nullspace contains a nonzero vector, which can be cleared of denominators. Nonzero periods make the homomorphism nontrivial. If its image is gZ, divide periods by g to obtain the connected infinite cyclic cover; the original visited voltage component is an equivalent realization with a different level scale/gauge. This shows explicitly why disconnected/nonprimitive voltage labels do not produce a distinct covering mechanism.

The image-count argument is also directly equivalent: if a proper cover's visited image had only one lift of each old vertex and surjected onto all old edges, its restriction would be a degree-one graph isomorphism onto H, making the lift a section and contradicting properness. In voltage coordinates the same conclusion is c(e)=s(head e)−s(tail e), the PR's gradient contradiction. Both prove progress without any rank decrease hypothesis. The new control deliberately has rank increasing on its first step.

For descent, an integral edge cochain gives an affine height a on the lifted graph with a(Tx)=a(x)+g for a deck generator after normalization. Adding a fiber variable confined to an interval of length smaller than g yields the old disjoint-strip embedding. On the compact lifted circle, scaling its existing height b by a rational epsilon gives exactly the PR formula. This makes a hidden coordinate choice explicit but does not change the separation principle.

The PR genuinely removes the need to quote the general tower theorem and global bundle discussion. Its complete argument is elementary in the stated finite-graph/linear-algebra/continuity sense. Whether that self-contained exposition, rather than a new mechanism, is the desired mathematical contribution must be stated honestly. The2022 paragraph does not define elementary so as to decide this automatically. No authenticated earlier single source in precisely that restricted presentation was found; no categorical firstness or novelty follows.

## Literal C10 dictionary and its limits

Let the ten domain vertices carry levels `(2,1,2,3,2,1,2,3,2,1)` cyclically. Each edge joins neighboring levels, and the domain is a simple cycle. A stacking of the fixed walk yields a drawing in `[1,3]×R`, with each edge strictly monotone in its level coordinate. For two edges inside one strip, their height difference on a common level is continuous and cannot change sign without a crossing. Their endpoint orders therefore agree. Connecting the same endpoints by straight segments preserves those orders and creates no crossings. Edges sharing one domain endpoint can meet there; the simple C10 has no pair sharing both endpoints. Hence the required drawing would satisfy the classical proper level-planarity model.

The extreme visits occur in the cyclic order a,b,a,b,a. The paths a1→b1, b1→a2, a2→b2 and b2→a3 are four pillars; the remaining a3→a1 path stays on the a-side. This falls under C0. Only the non-planarity implication is used, not any global minimal-forbidden-pattern classification or minimality assertion. The literal nonperiodicity follows from the counts3 and2 of the two directed outward edges. It is an itinerary fact; the group element is1.

The same straightening argument must not be applied unchanged to a two-edge circle with parallel edges sharing both endpoints. That is the familiar curved out-and-back positive control. Nor is the rose word ababa the same map as the excursion walk; its target edges are loops and the old immersed theorem supplies a stacking.
