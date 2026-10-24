# Exact winding transport for fixed torus blocks

Research partial, 2026-10-24 UTC. No claim to solve Kourovka 21.127. Originality of the elementary observations here has not been established; they are research records, not publication claims.

## Fixed data and exact scope

Let a graph of groups have free abelian vertex groups with specified coordinate bases, and let every edge injection identify a coordinate subgroup with the same named coordinates at its two ends. Choose finitely many oriented polygonal boundary blocks in the vertex tori and pair their turns across edge tori. The arcs of each polygon lying on the prescribed exterior boundary are fixed; a paired turn can be assigned any integer winding vector in its edge subgroup. Changing a turn by a vector adds that vector to one polygon's winding and its negative to the paired polygon. These are the usual paired turns in Chen, *Scl in graphs of groups*, arXiv:1904.08360v2, Section 3.1, especially (3–1).

Every polygon whose total winding is zero can be filled by a disk in its torus. A polygon with nonzero winding is instead the polygonal boundary of a mapped annulus, with one inner loop boundary representing its winding. This gives a simple **relative** surface. Inner boundaries are allowed; they are not silently counted as disks. All claims below concern this fixed collection of polygons and the fixed pairing of turns, unless arbitrary rewiring is explicitly mentioned. They do not assert that these are the only possible polygon types for the exterior boundary word.

For each piece p and coordinate x present in its vertex torus, let b(p,x) be the integer sum of x exponents on its fixed exterior arcs. Let H_x have one vertex for each piece whose vertex torus contains x, and one edge for every paired turn whose edge torus contains x. An isolated vertex is retained. Orient each edge arbitrarily. The winding assignment on x is an integer variable t_e on each edge, contributing +t_e at its initial vertex and -t_e at its final vertex.

## Transport lemma

For a set D of pieces required to be disks, integer turn windings making every piece of D a disk exist **if and only if**

> for each coordinate x and every connected component C of H_x all of whose vertices lie in D, the total charge sum_{p in C} b(p,x) is zero.

**Necessity.** Sum the zero-winding equations over C. Each turn variable appears once with each sign, so all cancel. There is no x-turn crossing from C to its complement, by the definition of a component.

**Sufficiency.** Work independently for each coordinate x. In a component C containing a piece not in D, root a spanning tree at such a free piece. Successively eliminate the non-root vertices from leaves inward, choosing the winding on the parent edge to cancel the current integer charge at that vertex. This places the total residual charge at the free root and satisfies every disk equation in C. In a component entirely in D, root the spanning tree arbitrarily and perform the same elimination. Its residual root charge is exactly the total initial charge, which is zero by hypothesis. Non-tree edge variables can be set to zero. This construction uses integers, so there is no divisibility or rational-to-integral gap. Coordinates are independent because an edge coordinate subgroup has independent integer coordinates. Combining these assignments makes the complete winding vector vanish at every piece of D.

A vertex torus can have coordinates absent from every incident edge. For such a coordinate H_x consists of isolated vertices; the condition correctly requires zero exterior charge at each disk piece. No hidden assumption that all coordinates occur on edges is used.

## Finite hitting-set consequence

Call a component C of any H_x **bad** when its total charge is nonzero. A set N of pieces can contain all non-disks precisely when it intersects every bad component. Thus the smallest possible number of non-disks for these fixed blocks and pairings equals the transversal number tau of the finite family of bad components.

For completeness, a minimum transversal N gives feasible windings with all other pieces disks by the lemma. If any member of N also became a disk, the actual smaller set of non-disks would still meet every bad component by necessity, contradicting minimality. Thus tau is attained exactly.

If there are V polygon blocks and E paired turns, the best Euler characteristic of such a simple relative surface is

    chi = V - tau - E.

Each disk contributes 1, each annulus 0, and gluing along each turn interval subtracts 1. Equivalently, counting two corners per turn on each side gives the same orbifold Euler characteristic. For tight nontrivial exterior loops there are no global disk or sphere components, so the usual negative-Euler-characteristic convention agrees with this calculation. Where such a hypothesis is absent, the statement is about Euler characteristic, not automatically the scl objective.

This is an exact finite optimization **after** the normal block data are fixed. It does not prove that all extremal or asymptotically extremal surfaces for a fixed RAAG word admit a finite list of blocks or a bounded matching complexity. Taking an infimum over an uncontrolled infinite family of such rational optimizations does not prove that the resulting scl is rational.

## Unchanged-block graph covers explain a failure of automatic promotion

Here a graph cover duplicates the original polygon blocks, with every local incidence unchanged. A general cover of an annular surface piece can instead produce a longer polygon boundary and is not such a fixed-block cover. A finite cover of the entire piece incidence graph restricts to a cover of each H_x. If a bad coordinate component C is a tree, every lift is another copy of C. Its nonzero charge survives in each copy, so at least one non-disk is required in every copy. The resulting loss is proportional to the covering degree. It cannot be made negligible by large covers.

Components containing cycles can have connected covers of arbitrarily high degree. In favorable cases their whole charge can be concentrated in one exceptional piece, making a normalized loss tend to zero. That observation alone gives no simultaneous result for all coordinate components or all rewiring choices. The positive-density tree obstruction below shows why that missing step matters even in the path RAAG P4.
