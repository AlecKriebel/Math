# Turn 5: the three-color deficit-two slice

Fifth and final substantive author turn. **The general source question remains unsolved5/5.** This turn gives a deductive exclusion for the next small-deficit three-color slice. The proof uses forced adjacency, not an integer-program infeasibility flag or a finite-order graph scan.

## 1. The isolate-free theorem

**Theorem.** If H is an isolate-free3-colorable graph with deficit D=N-w(H)=2, then N<=10. Consequently H satisfies the stronger core property from Turn3.

If H is bipartite, Turn1 gives N<=3D=6, so assume chi(H)=3 and fix a proper coloring with nonempty class sizes a<=b<=c. Turn1 gives

    a<=2, b<=a+2, c<=a+b+2, N<=14.                     (1)

Suppose N>=11. If a=1 then b<=3 and c<=6, giving N<=10; if a=b=2 then c<=6, also giving N<=10. Hence a=2 and b is3 or4. The only size triples with11<=N<=14 are

    (2,3,6), (2,3,7), (2,4,5), (2,4,6), (2,4,7), (2,4,8).  (2)

Since every color class has size at least two, every degree is at most N-2. There are exactly W=N-2 distinct positive degrees. Thus the degree set is **exactly**1,...,N-2. Denote the size-two class by A and the other two classes by B,C.

Turn2's quadratic cut bound excludes(2,3,7), where15>12, and(2,4,8), where24>16. It remains to exclude four actual adjacency patterns.

## 2. All three shapes with |B|=4

Write |C|=c in{5,6,7}, so N=c+6 and W=c+4. Every vertex of B has degree at most c+2, and every vertex of C has degree at most6. Therefore the required degree values W and W-1 can only occur in A. Call their vertices v and u, respectively.

The vertex v is adjacent to every vertex outside A. The vertex u misses exactly one vertex z outside A. The required degree-one vertex must be z, and z has no neighbors apart from v: every other vertex outside A is already adjacent to both v and u.

The value M=c+2 is required. It exceeds6 and is smaller than both A degrees, so it occurs at a vertex b_* in B. This is the maximum possible B degree, so b_* is adjacent to all of A and all of C. The degree-one vertex z cannot lie in C, where it would be adjacent to both v and b_*. Thus z lies in B, and every C vertex has both A neighbors as well as b_*; its degree is at least three.

The required degree-two vertex therefore also lies in B, say b_0. It is distinct from z and b_*. Since z is u's only missing outside neighbor, b_0 is adjacent to both A vertices and to no C vertex.

Of the four B vertices, z and b_0 have no C neighbors. Hence a C vertex has at most two A neighbors and two B neighbors, and has degree at most four. The required values five and six cannot occur in C or A. But B already contains the three distinct degrees1,2,M, with M>=7, leaving only one vertex to represent both five and six. This contradiction excludes(2,4,5), (2,4,6), and(2,4,7).

## 3. The shape (2,3,6)

Now N=11, W=9, B has size3 and C size6. Every C degree is at most5. The degree-nine vertex v must lie in A and is adjacent to every vertex outside A; call the other A vertex u.

### Case A: a B vertex has degree eight

Such a vertex b_* is adjacent to all of A and C. Every C vertex then has at least the two neighbors v,b_*, so the required degree-one vertex lies in A union B. The four required degree values6,7,8,9 also lie in A union B, since C degrees are at most5. There are exactly five vertices in A union B; therefore those five vertices have exactly the distinct degrees1,6,7,8,9. In particular degree five must occur in C.

If the degree-one vertex is u, its only neighbor is b_* (which is adjacent to all of A), so u has no C neighbors. A C vertex can then have at most the one A neighbor v and three B neighbors, hence degree at most four. If the degree-one vertex is in B, its only neighbor is v, so it has no C neighbors. A C vertex then has at most two A and two other B neighbors, again at most four. Either alternative contradicts the required degree five in C.

### Case B: no B vertex has degree eight

The degree-eight vertex is then u in A. It misses exactly one outside vertex z. As before, the required degree-one vertex must be z and has only neighbor v. The required degrees six and seven lie at two distinct B vertices, because A has degrees8,9 and C degrees are at most5. Let b_0 be the remaining B vertex.

If z belongs to B, then z=b_0. It has no C neighbors, so all C degrees are at most four. The required degree five can be neither in A nor B, a contradiction.

Suppose z belongs to C. The degree-seven B vertex is adjacent to both A vertices, since u's sole missing outside neighbor is z. It needs five C neighbors. It cannot be adjacent to z, whose only neighbor is v, so it is adjacent to all five vertices of C\{z}. Each of those five vertices has both A neighbors and this B neighbor, and therefore has degree at least three. The required degree two must consequently be b_0. That vertex has both A neighbors and no C neighbor. All C degrees are again at most four, while degree five must occur in C. This final contradiction excludes(2,3,6).

All possibilities in(2) have been excluded. The theorem N<=10 is proved.

## 4. Restoring isolates and the exact source slice

Let G have chi(G)=3 and d=n-w(G)=2. If it has no isolates, the theorem gives n<=10. If it has r>=1 isolates, its nonempty isolate-free core has deficit D=d-r+1=3-r. Since D>=1, r is1 or2.

- If r=1, the core has D=2, so N<=10 and n<=11
- If r=2, the core has D=1; the classical deficit-one result in Turn4 gives N<=2chi-1=5 because the core has no isolates, so n<=7

Thus n<=11 in all cases. This is precisely n-1<=5d for the three-color, deficit-two slice. Graphs with chromatic number at most two were already proved separately. The result does not address all higher-chromatic graphs of deficit two.

## 5. A small-order corollary with no enumeration at that order

Every simple graph of order at most15 satisfies the exact source inequality. To see this, let n<=15. The cases chi<=2 and d=1 have already been established. If chi=3, then d=2 is covered by this turn, while d>=3 gives (2chi-1)d>=15>=n-1. If chi>=4 and d>=2, then(2chi-1)d>=14>=n-1.

This is a consequence of the written class and deficit theorems. The diagnostic graph enumeration in this packet only runs through order six; it is not an enumeration through order15. The first parameter possibility left by these deductions is n=16, chi=4, d=2. Another surviving family has chi=3, d>=3 and n>=5d+2. These are unresolved parameter configurations, not constructed graphs or counterexamples.

## 6. Final disposition

The five turns establish the exact integer reduction, universal and local degree-capacity bounds, a cross-class moment constraint, structural classes closed under union/join, all triangle-free graphs, the credited deficit-one case, and this three-color deficit-two slice. They do not establish the universal linear coefficient2chi-1.

No full source solution or counterexample is claimed. The original status is **unsolved5/5**, subject to full independent audit of these scoped partials. No additional author proof-search turn is included after this freeze. Known historical results retain their credit, and no novelty certification is asserted.
