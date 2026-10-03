# Attempt 3 of 5: blow-up constructions and homogeneous cuts

## Aim

Try to obtain a sublinear construction, or an unbounded improvement on the additive deficit, by replacing vertices of a small admissible coloring with homogeneous blocks. The test instead gives explicit obstructions and an exact-strength lower bound for a restricted class.

## Lemma: edge colors with no disjoint equal-colored edges

If the edges of K_s are colored with q colors and no color contains two vertex-disjoint edges, then q>=s-2 for s>=3.

Proof by induction on s. A pairwise-intersecting family of edges is either a star or the three edges of a triangle. Indeed, take incident edges xy,xz. If every edge contains x it is a star; otherwise an edge avoiding x must be yz, and any further edge meeting all three lies in that triangle.

If a nonempty color class is a star, delete its center. That entire color disappears, and the induced K_(s-1) still has the required property. For s>=4, the inductive bound gives q-1>=(s-1)-2. The base s=3 is immediate. If no class is a star, every nonempty class is a triangle, so q=binom(s,2)/3>=s-2: the equivalent inequality is (s-3)(s-4)>=0, valid for s=3 and all s>=4. This proves the lemma. Empty named colors can be ignored.

## Common monochromatic neighborhood obstruction

In an admissible coloring of K_n, let u,v be distinct vertices and let S be a set disjoint from them such that both ux and vx have a fixed color c for all x in S. If xy and zw were disjoint edges of one color b inside S, the triangles uxy and vzw would be disjoint with common type {c,c,b}. Therefore every color class induced on S is an intersecting edge family. The lemma gives

    |S| <= q+2.

This includes b=c; excluding monochromatic triangles here would invalidate the result. Thus each monochromatic graph is K_(2,q+3)-free. A direct extremal-graph bound using only this fact is insufficient for linear growth because the forbidden second part grows with q.

## Exact-strength theorem for a monochromatic cut

Suppose n>=5 and V(K_n)=A disjoint-union B, where |A|,|B|>=2 and every crossing edge has one color c. Then every admissible q-coloring satisfies

    q >= n-4.

If |A|=2, the previous lemma applies to S=B, giving q>=|B|-2=n-4 (the case |B|=2 is symmetric). Otherwise both parts have size at least three. The common-neighborhood argument shows that the internal palettes use at least |A|-2 and |B|-2 colors respectively.

Those palettes are disjoint. For if edges a1a2 in A and b1b2 in B had the same color d, choose a3 in A outside {a1,a2} and b3 in B outside {b1,b2}. The triangles a1a2b3 and b1b2a3 would be vertex-disjoint and both have type {c,c,d}. Contradiction. Adding the palette sizes proves q>=(|A|-2)+(|B|-2)=n-4. The crossing color c may occur internally in at most one part; no unsupported extra +1 is claimed.

## Why the natural product construction fails

In any uniform blow-up of a colored complete graph, edges between each pair of blocks have the color of the corresponding original edge. If three distinct blocks each have at least two vertices, choose two representatives in each block. The three first representatives and the three second representatives form disjoint triangles of the same type. This happens regardless of colors or edges inside blocks, and regardless of whether the original coloring was proper.

Consequently an admissible homogeneous blow-up can have at most two blocks of size at least two. If a putative binary recursive construction uses a monochromatic cut with two nontrivial sides, the preceding theorem already forces the target n-4 lower bound. Multiplicative seed amplification therefore cannot be justified by the usual uniform blow-up or monochromatic binary-join operations.

## Verdict

No unrestricted resolution. The proof establishes q>=n-4 for the explicit subclass with a monochromatic cut whose sides have at least two vertices, and rejects broad families of product constructions. General colorings need not admit such a cut; no structural theorem producing one has been proved. This is substantive attempt 3/5.
