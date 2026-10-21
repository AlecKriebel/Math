# Author turn 2: closing the deficit-difference-six subfamily

2026-10-03 UTC. Status: partial; original target not solved. Best-guess full-target completion: 15% (subjective).

## Result
Write c=binom(n,2)+2−p and m=binom(k,2)+2−q with 0≤p≤n−2 and 0≤q≤k−2. For every p≥10, q=p−6 and k≥7, with c>m, the following finite construction gives an m-avoiding exact c-coloring. Combined with already credited small-q boundary cases, this handles the whole p−q=6 subfamily. This does not handle all positive multiples of 6. Novelty against the full literature has not been established.

## Four explicit gadgets
For a finite edge-colored clique H let its deficit be δ(H)=|E(H)|−number_of_colors(H). All gadgets are properly edge-colored. Their whole deficits, vertex counts, and possible deficit losses δ(H)−δ(H[S]) are:
- deficit 3, order 4: losses{0,3}
- deficit 5, order 5: losses{0,4,5}
- deficit 9, order 6: losses{0,4,5,8,9}
- deficit 11, order 7: losses{0,4,5,8,9,10,11}

Exact edge lists and every subset's size-stratified deficit are supplied in `gap_six_checks.json`. Here is a proof independent of trusting a large computation.

Order4 is a proper three-color one-factorization; every proper subset is rainbow. Order5 uses color (i+j) mod5, whose proper induced deficits are0 or1.

Order6: take a one-factorization with five colors, each used on three edges, and give one edge a fresh sixth color. Whole deficit=15−6=9. A five-vertex subset has deficit 4 or5: deletion removes five edges and either zero or one color. Any subset of at most four vertices has deficit≤1: after deleting two vertices every original three-edge matching retains an edge, so all five original color classes remain represented before the split; splitting cannot reduce color count. Further vertex deletion cannot increase deficit.

Order7: use colors(i+j) mod7. Color0 occupies(1,6),(2,5),(3,4) and misses vertex0. Split this whole matching into three singleton colors by recoloring(1,6) to 7 and(2,5) to 8. Recolor(0,1), originally color 1, to 9. Whole deficit=21−10=11. Every vertex is incident with at least one unique-color edge, and only vertex1 meets two, so deleting one vertex removes6 edges and 1 or2 colors, leaving deficit 6 or7. Deleting two vertices leaves every original three-edge matching represented, hence at least7 colors and deficit≤10−7=3. Smaller subsets cannot have larger deficit. These observations imply exactly the stated loss sets, or supersets sufficient to exclude loss 6; the full tables were exhaustively checked on 16,32,64,128 subsets respectively.

## Assembly for every p≥10
Use base decompositions:
10=5+5,11=11,12=3+9,13=3+5+5,14=5+9,
and add copies of 5 to cover every p≥10. At most one deficit 3 gadget occurs. The total number of gadget vertices is≤p+1≤n−1. Place these disjointly inside K_n, make gadget color palettes disjoint, and give all other core edges unique fresh colors. Add fresh common spoke and tail colors. Total deficit is p, so the coloring uses exactly c colors.

For every core subset, deficit is additive over gadgets. Its loss from p cannot equal6: a single nonzero loss is3,4,5 or≥8; there is at most one 3; two other positive losses sum to≥8;3 plus any other positive loss is≥7. Therefore no subset has deficit q=p−6.

For |S|<k, the palette is at most2+binom(k−1,2)<m since q≤k−2. For |S|=k, equality would require deficit q and is excluded. For |S|>k, the palette is at least2+binom(k+1,2)−p, exceeding m by k−6>0. Empty S gives one color. Finally c>m and p−q=6 force n>k. This proves the claimed subfamily.

The remaining p<10 cases have q<4 and are among Stacey–Weidl's already credited q=0,1,2,3 coverage. For p=10,k=6 (the only possible k<7 with q≥4), q=k−2 is another credited case. No new proof of those literature cases is claimed here.

## Checks and unsuccessful scope extension
`gap_six_gadgets.py` exhaustively verified each gadget and checked every assembled deficit representation for 10≤p≤10000. This finite replay supports the code; the residue-class argument above proves the infinite p family.

Simply repeating these same gadgets does not handle p−q=12: three K5 gadgets can each lose4, totaling12. Thus the fixed loss-gap family cannot be promoted to the full modular-diagonal conjecture. The next attempt studies larger gap-specific factorizations and their limitations.
