# Attempt 2 of 5: exploit the structure of intersecting type families

## Aim

Attempt 1 loses a factor q by taking a separate three-vertex transversal for every non-rainbow type. Here the attempted improvement is to show that large type families have a single forced center, then charge these centers efficiently to colors.

## An elementary common-center lemma

Let F be an intersecting family of triples on n vertices. If F has no vertex common to every member, then

    |F| <= 9(n-2).

Proof. Choose T in F. For each x in T, choose T_x in F with x not in T_x; these exist because F has no common vertex. Every U in F intersects T, so choose x in U intersect T. It also intersects T_x, so U contains some y in T_x. Since x not in T_x, x and y are distinct. Thus U contains one of at most nine pairs {x,y}, where x is in T and y is in T_x. Each pair belongs to at most n-2 triples. A union bound proves the assertion. No extremal set-theory theorem is being invoked without proof.

For any triangle type in an admissible coloring, its triangles form an intersecting family. Thus any type realized on more than 9(n-2) triangles has a common vertex. This applies to all types, with or without repeated colors.

## A conditional exponent improvement

Suppose every non-rainbow type family has no common vertex. Let B be the total number of non-rainbow triangles. There are q^2 types, so

    B <= 9q^2(n-2).

Let d_a(v) count edges of color a incident to v and let W be the number of monochromatic two-edge paths, with their common vertex distinguished. Then

    W = sum_{v,a} binom(d_a(v),2)
      >= n(n-1)(n-1-q)/(2q),

by sum_a d_a(v)=n-1 and Cauchy-Schwarz. A two-color triangle contributes one such path, and a monochromatic triangle contributes three; a rainbow triangle contributes none. Therefore W<=3B, giving

    (n-1)(n-1-q) <= 54q^3(n-2)/n < 54q^3

when n>2. In particular, n=O(q^(3/2)), or q=Omega(n^(2/3)), under the no-common-center hypothesis. The inequality is harmless when n-1<=q.

This is an actual partial theorem, but the hypothesis is not automatic. In the n-4 upper construction, the large two-color type families are precisely common-center families.

## Why center deletion still stops short

For each non-rainbow type having a common vertex, select one such vertex and collect them in C. There may be q^2 selected vertices. Deleting C eliminates these types; every remaining non-rainbow triangle belongs to an original non-centered type, whose total original family size is at most 9(n-2). If m=n-|C|, the same cherry calculation in the remaining clique gives

    m(m-1)(m-1-q) <= 54q^3(n-2).

Hence when q=o(n^(2/3)), any such center selection must have |C|=n-o(n). This reveals the necessary structure of a hypothetical low-color example: almost every vertex would have to be assigned as the common center of some non-rainbow type.

The missing step is a linear bound on the number of such forced centers in terms of q. A color occurs in q distinct non-rainbow types, and being common to one complete type does not make that color globally private to the center. Charging one center per color is unjustified. Also, the common center of a type {a,a,b} need not be the vertex incident to both a-edges; it may be an endpoint of the b-edge. Ignoring these possibilities would make an induction invalid.

## Verdict

No full resolution. The elementary family lemma yields a rigorous n^(2/3) lower bound for a restricted center-free class and a necessary concentration condition for low-color examples. The unrestricted linear lower bound remains open in this attempt. This counts as substantive attempt 2/5.
