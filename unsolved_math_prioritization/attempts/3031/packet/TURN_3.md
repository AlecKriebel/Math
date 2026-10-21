# Author turn 3: gap-specific proper-clique semigroups

2026-10-03 UTC. Status: partial; full-target completion estimate remains15%.

## Construction theorem
Let d=6r≥12. For every integer t with d/2+2≤t≤d, take a properly edge-colored K_t using χ'(K_t)=t−1 colors for even t and t colors for odd t. Such a coloring is explicit: for odd t label vertices modulo t and assign ij color i+j; for even t use vertices modulo t−1 plus∞, assign ij color i+j and i∞ color2i, all modulo t−1.

Its total deficit is w(t)=binom(t,2)−χ'(K_t). Deleting one vertex loses t−1 edges and no color, because every color matching has at least3 edges. Thus its deficit loss is exactly t−1, lying strictly between d/2 and d. Deleting at least two vertices causes loss at least2t−3>d: after deleting exactly two vertices every matching still has an edge, and further vertex deletion cannot increase deficit. Consequently every nonzero loss is>d/2 and loss d is absent. In any disjoint union of these gadgets, total loss d remains absent, since two positive losses already exceed d.

Suppose p is a nonnegative integer combination of these weights, q=p−d, k>d,0≤q≤k−2,0≤p≤n−2, and c=binom(n,2)+2−p>m=binom(k,2)+2−q. Embed the gadgets disjointly in K_n, using separate palettes, and color all remaining edges distinctly. There is room because every gadget's order is at most its deficit, so their total order is≤p<n. Add distinct common spoke and tail colors. Exactly c colors result, and m is absent: subset sizes below k have too few colors, size k would require the excluded deficit loss d, and sizes above k have at least m+(k−d)>m colors.

The gap d=6 has the more efficient gadgets proved in turn 2.

## Coverage for each fixed gap
For each fixed d≥12 the allowed weights have gcd1. Indeed the interval contains four consecutive orders2s,2s+1,2s+2,2s+3. Their weights are(2s−1)(s−1),(2s+1)(s−1),(2s+1)s,(2s+3)s. The gcd of the first two is s−1; a common divisor of all four must divide both 3 and 5 and therefore is1. A finitely generated positive integer semigroup of gcd1 contains every sufficiently large integer (use the generated residues modulo the smallest generator, then add that generator).

This covers all sufficiently large p for each fixed deficit gap d, with the stated k>d condition. It is a construction subfamily, not the full exact-color conjecture. The prior2025 sufficiently-large-m theorem retains its broader asymptotic credit.

`large_gap_gadgets.py` gives exact residue-minimum certificates. For d=12,18,24,30,36,42,48 the computed semigroup conductors are respectively 122,258,458,641,964,1258,1698. Each residue representative is an explicit nonnegative sum; adding the minimum generator proves coverage above the conductor. Only the d=12 local gadgets were exhaustively subset-checked(7936 subsets total); the general loss proof above covers larger orders.

## Failure and remaining obligation
For d=12, the smallest generator is21, so p=16,q=4 is not covered. The existence of a finite semigroup threshold does not prove the finitely many smaller p cases, nor does it bound all gaps d simultaneously. Large p is a sufficient condition, not an equivalent characterization. Further work must preserve exact c while controlling all subset sizes, especially k≤d.
