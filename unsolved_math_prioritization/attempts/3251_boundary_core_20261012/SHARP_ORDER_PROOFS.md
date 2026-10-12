Editorial note: Complete authored proof or audit prose is preserved below. Only operational artifact identities, byte counts, locations and obsolete replay directions have been replaced; all mathematical arguments, finite scopes and limitations remain. The public manifest identifies the actual distributed edition.

# Third-pass structural frontier: a sharper order barrier for clique cutsets

## Scope and outcome

The unrestricted odd-hole-free 2-divisibility conjecture remains unresolved. This note proves a sharper numerical obstruction, a complete equality classification for the elementary chromatic order bound, and additional necessary maximum-clique locations on the two sides of an edge cutset. It does not rule out the incompatible boundary types. No novelty is claimed.

All graphs are finite and simple. A division of a graph with clique number k >= 2 is a red/blue vertex coloring without a monochromatic k-clique. “Maximum clique” always means maximum cardinality. A minimal indivisible graph has no division, but every proper nonedgeless induced subgraph has one. An odd-hole-free graph has no induced odd cycle of length at least five.

The previously accepted structural continuation and its full acceptance were read. Their intended companion editions are [the earlier structural proof](../3251_divisibility_partials_20261012/STRUCTURAL_PROOFS.md) and [the earlier audit](../3251_divisibility_partials_20261012/STRUCTURAL_AUDIT.md). These relative paths identify the proposed repository layout and do not assert remote publication. Necessary ingredients are reproved below, so the new elementary statements do not depend on an uninspected theorem. The published K4-free four-color theorem is used only when translating the results to the original conjecture's unresolved range k >= 4.

## 1. An equality classification for chromatic order

Write n = |V(H)|, q = chi(H), and r = omega(H).

**Theorem 1.** If q > r, then

    n >= 2q - r + 1.

Equality holds if and only if H is the complete join of a clique of order r-2 and a five-cycle. In particular, equality forces q = r+1. Consequently:

- If q >= r+2, then n >= 2q-r+2.
- If H is induced-C5-free and q > r, then n >= 2q-r+2.

The empty clique is allowed in the join, giving C5 itself when r=2.

**Proof.** Fix an optimal proper coloring with q nonempty color classes. The s vertices in singleton classes form a clique: otherwise two singleton classes could be merged. Thus s <= r. Let

    e = sum (|T|-2),

where the sum is over nonsingleton color classes T. Then e >= 0 and

    n = 2q-s+e >= 2q-r.

We first record a color exchange. If {a,b} is a two-vertex color class and S is the clique of singleton vertices, a and b cannot both have a nonneighbor in S. Indeed, choose nonneighbors x of a and y of b in S. If x=y, merge {a,b,x} into one stable class. If x and y differ, replace the three classes {a,b}, {x}, {y} by the two stable classes {a,x}, {b,y}. Either operation decreases the number of colors, a contradiction.

If n=2q-r, then s=r and e=0. Since q>r, a two-vertex class exists. Neither vertex of that class can be complete to S, since S is already a maximum clique. This contradicts the exchange observation. The first bound follows.

Now suppose n=2q-r+1. The identity gives s-e=r-1, leaving exactly two possibilities.

**Case 1: s=r and e=1.** There is exactly one three-vertex class and every other nonsingleton class has size two. No two-vertex class is possible, by the preceding argument with the maximum clique S. Hence all vertices outside S form a single stable triple T. Every vertex of T has a nonneighbor in S. Assign each vertex of T the color of one such nonneighbor; T is stable, so these assignments produce a proper r-coloring. This contradicts q>r.

**Case 2: s=r-1 and e=0.** Let the remaining classes be {a_i,b_i}, 1 <= i <= t, where t=q-r+1 >= 2. By the exchange observation, choose a_i complete to S in every pair. The set A={a_1,...,a_t} is stable, because an edge between two of its vertices together with S would be an (r+1)-clique.

If all b_i were complete to S as well, every vertex outside S would be complete to S. An edge outside S would again create an (r+1)-clique. Thus the whole outside set would be stable and H would be r-colorable. We may therefore choose b_i and x in S with b_i nonadjacent to x.

Replace the classes {a_i,b_i}, {x} by {b_i,x}, {a_i}. This is another optimal q-coloring, with singleton clique

    S_i = (S minus {x}) union {a_i}.

For every j != i, a_j is nonadjacent to a_i. Applying the exchange observation to {a_j,b_j} and S_i forces b_j to be complete to S_i. Thus b_j is adjacent to a_i and every vertex of S minus {x}. It cannot also be adjacent to x: then it would be complete to S, and S union {a_i,b_j} would be an (r+1)-clique. Therefore b_j misses exactly x among S.

There is a j != i because t>=2. Applying the same exchange with pair j now shows that b_i is adjacent to all S minus {x} and to a_j. Repeating the argument for all pairs gives:

- every b_i is anticomplete to {x} and complete to S minus {x};
- a_i is adjacent to b_j whenever i != j;
- a_i is nonadjacent to b_i, as originally prescribed by the color class.

If t>=3 and b_i were adjacent to b_j, choose an index l distinct from both. The set

    (S minus {x}) union {b_i,b_j,a_l}

would be an (r+1)-clique. Hence B={b_1,...,b_t} is stable when t>=3. But then A and B union {x} are stable, and together with individual colors on S minus {x} they give an r-coloring. This is impossible. Consequently t=2, q=r+1, and b_1b_2 must be an edge to avoid the same r-coloring. The five vertices x,a_1,b_2,b_1,a_2 induce a five-cycle in that order. Every vertex of S minus {x} is complete to the five-cycle and to the other vertices of S. This is exactly K_{r-2} joined to C5.

Conversely, this join has n=r+3, clique number r and chromatic number r+1, so n=2q-r+1. This also proves both stated consequences. Square.

**Sharpness and limits.** The strict improvement by one is attained by C5 joined to a clique. The next improvement by two cannot be increased for all induced-C5-free graphs with chi>omega: the seven-antihole has n=7, q=4, r=3 and no induced C5. Its clique number is the independence number three of C7; its chromatic number is four because every stable set has at most two vertices, and three nonedges plus a singleton give four colors. An induced C5 would require the corresponding five vertices in C7 to form a cycle, which is impossible. This example does not attain the large chromatic gap required of a forcing side; no sharpness claim is made for that more restricted class.

## 2. Sharper obstruction and separator bounds

**Lemma 2 (color grouping with clique precolors).** Let C be a clique in H, let k>=2, and suppose chi(H)<=2k-2. Every red/blue coloring of C with at most k-1 vertices of each color extends without a monochromatic k-clique.

**Proof.** In a proper coloring with at most 2k-2 classes, C occupies distinct classes. Preassign each occupied class its boundary color. If a and b classes are assigned red and blue, respectively, the remaining capacities are k-1-a and k-1-b. Their sum is at least the number of unassigned classes. Assign all remaining classes within these capacities. Each color is a union of at most k-1 stable classes and therefore contains no k-clique. Square.

In particular, every indivisible graph of clique number k satisfies chi>=2k-1. If k>=3, this is at least k+2. Theorem 1 therefore gives the following improvement, with no minimality or odd-hole hypothesis:

**Corollary 3.** Every indivisible graph of clique number k>=3 has at least 3k vertices.

Let now G be minimal indivisible with k>=3. Let C be a nonempty clique cutset of size s and let D_1,...,D_t, t>=2, be the components of G-C. Put H_i=G[C union D_i]. At threshold k, let T be the admissible colorings of C, and let S_i be the restrictions that extend to H_i.

A k-clique cannot meet two distinct D_i. Consequently G has a division exactly when the intersection of all S_i is nonempty. Every S_i is nonempty by proper-induced-subgraph minimality, coloring arbitrarily if omega(H_i)<k. For each i, minimality also colors G-D_i, giving a restriction c_i in all S_j for j!=i. This c_i cannot be in S_i. Thus every side excludes an admissible boundary coloring, and Lemma 2 implies chi(H_i)>=2k-1. A side with omega(H_i)<k would exclude no coloring, so omega(H_i)=k.

Applying Theorem 1 to each side proves:

**Theorem 4 (sharpened separator barrier).** For every such clique cutset,

    |V(H_i)| >= 3k for every i,
    |V(G)| >= s + t(3k-s).

The previously proved orbit bound is unchanged: t<=2^(s-1) for s<k, and t<=2^(k-1)-1 for s=k. For completeness, each S_i is invariant under color swap. The witness c_i above lies in S_j but not S_i for j!=i, so witnesses from different components occupy distinct swap orbits. There are 2^(s-1) orbits, with the constant orbit forbidden exactly when s=k.

For s=2<k there are just two orbits, equal and different colors. Hence there are exactly two components and their feasible restrictions are opposite single orbits. The new order bound is

    |V(G)| >= 6k-2.

At k=4 this is 22 vertices, improving the accepted bound 18. For an arbitrary clique cutset, t>=2 and s<=k give |V(G)|>=5k; at k=4 this is 20, improving 16. Every side at k=4 has at least 12 vertices, improving 10. These are necessary bounds, not existence or sharpness claims.

## 3. Maximum-clique locations and local witnesses

Write M_H(v)=V(H) minus (N_H(v) union {v}) for the open antineighborhood.

**Proposition 5.** If G is indivisible with clique number k>=2, then omega(G[M_G(v)])=k for every vertex v.

**Proof.** N_G(v) has clique number at most k-1, since adjoining v to a larger clique would exceed k. The other part, {v} union M_G(v), has clique number max(1,omega(G[M_G(v)])). If the latter clique number were less than k, these two parts would divide G. Square.

For a minimal indivisible G, delete v and take a division of G-v at threshold k. This threshold is preserved: if deleting v lowered omega, {v} and G-v would divide G. Both colors are blocked on reinserting v, so each color contains a (k-1)-clique in N(v). Thus

    2k-2 <= degree(v) <= n-k-1.

The anticomplete k-clique, these two disjoint neighborhood cliques, and v are pairwise disjoint vertex sets, giving n>=3k-1 directly. Corollary 3 improves this to 3k for k>=3. The antineighborhood statement adds clique location information not present in an order bound alone.

Next consider any graph H of clique number k>=3 with a specified edge xy and at least one division. Say it is equal-only if all divisions color x,y equally, and different-only if all divisions color them differently.

**Proposition 6 (edge-forcing locations).**

1. In an equal-only graph, M_H(x) and M_H(y) each contain a k-clique. In every division with x,y red, N_H(x) and N_H(y) each contain a blue (k-1)-clique lying outside {x,y}.
2. In a different-only graph, H-{x,y} contains a k-clique. In every division with x red and y blue, N_H(x) contains a blue (k-1)-clique and N_H(y) contains a red (k-1)-clique. These cliques may include y and x, respectively.

**Proof.** If M_H(x) contained no k-clique, the two sets {x} union M_H(x) and N_H(x) would give a division with different colors on the adjacent x,y, contradicting equal-only. The same applies to y. Recoloring x alone in an equal-boundary division must create a blue k-clique containing x, and therefore a blue (k-1)-clique in its neighborhood. This clique does not contain the red y. Repeat for y.

If H-{x,y} contained no k-clique, coloring x,y red and all other vertices blue would divide H, because two is less than k. This contradicts different-only. The remaining assertions follow by recoloring one endpoint and identifying the resulting monochromatic k-clique. Square.

Consequently both components D_1,D_2 of the two-vertex cutset in Theorem 4 contain a maximum clique entirely inside the component. On the equal-only side, stronger anticompleteness to each individual boundary endpoint holds. This strengthens the earlier statement that each component merely meets a maximum clique.

## 4. Why these results still stop short

Odd holes cannot straddle a clique cutset: a cycle meeting two components must pass through at least two cutset vertices, whose adjacency produces a chord unless the cycle is confined to one side. More explicitly, on an induced cycle of length at least four a clique contributes at most two vertices, and when there are two they are consecutive; the remaining path therefore lies in one component. Thus odd-hole-freeness of a clique sum is equivalent to odd-hole-freeness of all its sides. There is no additional cross-side odd-hole contradiction to extract merely from incompatible colorings.

The remaining edge-cutset problem is to exclude, within the required hereditary minimal setting, two odd-hole-free sides of opposite forcing types satisfying all the above conditions. Neither the numerical bounds nor the endpoint blocking cliques accomplish that. We do not assert a general clique-cutset extension theorem.

The [clique-boundary extension](BOUNDARY_EXTENSION_PROOFS.md) is a separate result with its own [complete audit](BOUNDARY_CORE_AUDIT.md). The structural audit accepts the structural argument independently of that separate result.

## 5. Sources, prior art, and verification scope

- The target and prior frozen proof are as specified in the accepted second-pass package. The K4-free range uses Chudnovsky–Robertson–Seymour–Thomas, “K4-free graphs with no odd holes,” https://thomas.math.gatech.edu/PAP/k4free.pdf, Theorems 1.3 and 3.2. Its whole decomposition proof is not re-audited here.
- Hu–Xu–Zhuang, “Some properties of minimally nonperfectly divisible graphs,” arXiv:2603.01967v2, 5 March 2026, https://arxiv.org/html/2603.01967v2#S4. Section 4 records minimal non-2-divisible reductions and a choice of side divisions for which every disagreement vertex is blocked on both sides. It does not prove general clique-cutset exclusion. These statements are prior art, not new theorems claimed by this note. The inspected section and its omitted elementary adaptations received a separate source audit.
- Hoàng, “On the structure of perfectly divisible graphs,” https://arxiv.org/abs/2506.12660v2, poses unrestricted minimal non-2-divisible clique-cutset exclusion as Conjecture 4.7.

All new assertions in Sections 1–4 are proved in full above. The archived accompanying checker requires the exact earlier public snapshot, its external pin, and the full acceptance file, checks their bytes before doing mathematics, and rejects missing or mismatched inputs. It exhausts labeled graphs through six vertices and checks additional explicitly named benchmark graphs. These checks are finite regression, not a proof of the unrestricted conjecture. No critical clique-cutset example exists in this small universe, so the larger-order separator bounds rely on the written proof and arithmetic, not nonvacuous computational witnesses.
