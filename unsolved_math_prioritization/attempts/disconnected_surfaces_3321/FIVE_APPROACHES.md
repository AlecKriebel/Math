# Five approaches to the universal disconnected-drawing question

21 October 2026. ID 3321, queue rank 1876. Authored mathematical analysis, not a solution claim. No publication or queue mutation.

## Scope and conventions

The target quantifies over **every** optimal drawing, not merely existence of one separated optimum. Work here is with finite undirected loopless graphs (simple input graphs allowed; parallel edges explicitly allowed in intermediate constructions), on connected compact closed surfaces. A drawing places vertices at distinct points and edges as arcs, with finitely many transverse double crossings, no vertex in an edge interior and no triple crossing. Edge homotopy classes and rotations are not fixed. Count crossing points, not crossing edge-pairs. Good-drawing conventions additionally forbid adjacent crossings and repeated crossings of a pair. The reductions below permit intermediate nongood drawings; standard uncrossing removes self-crossings, adjacent crossings, or two crossings of one pair without increasing total count when homotopy classes are unrestricted. No conclusion here concerns fixed-homotopy, fixed-rotation, geodesic, or rectilinear crossing numbers.

Sphere/projective plane/Klein bottle are known territory. Torus existence was announced by Mohar–Šámal in September 2026; no full new proof was located in the supplied source gate. That announcement is not treated as proof of the every-optimum version. The five routes below are deductions and obstructions, with no novelty assertion.

## Approach 1: crossing-budget / surface-saving bound

Put a=cr_S(H), b=cr_S(K), delta_H=cr_0(H)-a and delta_K=cr_0(K)-b. In any optimal drawing D let x,y be its internal crossing counts and m its mixed crossing count. Putting a plane-optimal drawing of one graph into a small disk in the complement of a surface-optimal drawing of the other gives

    x+y+m = cr_S(H disjoint-union K) <= a+b+min(delta_H,delta_K).

Since x>=a and y>=b, this gives the sharper accounting identity/inequality

    m+(x-a)+(y-b) <= min(delta_H,delta_K).

Thus if either component gains no crossings by using S instead of the plane, every optimum is separated. This includes a planar component. An intersecting optimum must have positive saving for both components. This does not prove general separation: the right side can be arbitrarily large, and bounds on individual component crossing numbers alone do not allocate the available topology.

This is a proof, not a computational conjecture. It applies to orientable and nonorientable S.

## Approach 2: one mixed crossing and orientable block additivity

**Lemma.** On a closed orientable surface, a drawing with exactly one mixed crossing between two connected components cannot be crossing-minimal.

**Proof.** Let x,y be the internal crossing counts. Planarize all internal crossings to obtain connected abstract graphs P_H,P_K embedded individually. Subdivide each edge at the one mixed crossing and identify the resulting subdivision vertices to a vertex w. The resulting embedded graph Q is a vertex amalgamation of subdivisions of P_H and P_K. Orientable genus additivity over blocks implies

    genus(P_H)+genus(P_K)=genus(Q)<=genus(S).

Embed P_H and P_K on their minimum-genus orientable surfaces and take a connected sum away from both graphs; add unused handles if necessary. They are now disjointly embedded on S. At each planarization vertex restore the original pairing of its four half-edges inside a small disk. Any pairing of four boundary points needs at most one crossing. Restoring all such vertices therefore costs at most x+y crossings, independently of the new rotations. Finally normalize any nongood edges without increasing crossings. The original drawing cost x+y+1, so it was not optimal. QED.

The same argument works for several connected components if their mixed-crossing multigraph (one vertex per component, one edge per mixed crossing) is a forest: successive vertex amalgamations preserve additive orientable genus, and every mixed crossing can be removed without increasing internal crossings. This is not an argument for two or more mixed crossings between the same two components, since that multigraph contains a cycle.

Combined with Approach 1, a counterexample on an orientable surface with two connected components would have m>=2 and delta_H,delta_K>=2. In particular, if either saving is <=1 the universal assertion holds. This is only a necessary-condition exclusion, not a general solution. No nonorientable block-additivity substitution is made: ordinary nonorientable genus has different additivity behavior.

Classical dependency: Battle–Harary–Kodama–Youngs, *Additivity of the genus of a graph* (1962), DOI 10.1090/S0002-9904-1962-10847-7. The theorem is explicitly restated in Fulek–Kynčl, https://arxiv.org/abs/1903.08637 (abstract and introduction). The original DOI endpoint failed in this inspection; the theorem restatement was successfully checked.

## Approach 3: a strict torus lattice inequality is false

Use the 2015 Cabello–Mohar–Šámal notation

    L(X,Y)=sum_(u in X,v in Y) |det(u,v)|,
    M(X)=min_(A in GL(2,Z)) (sum_(v in X)|(Av)_1|)(sum_(v in X)|(Av)_2|).

One might try to strengthen their sufficient nonstrict inequality into L>min(M(X),M(Y)) whenever L>0. That strengthening is false even for X=Y.

Take u=(1,2), v=(2,-1), X=Y={u,u,v}. Then L(X,X)=4|det(u,v)|=20. To prove M(X)=20, for a nonzero integer row (a,b) set p=a+2b and q=2a-b. Its contribution to a coordinate sum is F=2|p|+|q|, with q congruent to 2p modulo 5. F>=4, and F=4 occurs only for (a,b)=+(1,0) or -(1,0). Indeed p=0 forces nonzero |q|>=5; |p|=1 forces |q|>=2, with equality giving those rows; |p|>=2 gives F>=4, and equality would require |p|=2,q=0, which violates the congruence. Two independent unimodular rows cannot both have F=4. Their product is at least 4*5=20. The identity matrix attains (2+2)*(4+1)=20.

This is an exact positive equality witness, not a graph counterexample. It blocks the blanket strict lattice inequality. Realizing vector multisets by embedded Eulerian graphs, preserving good-drawing conventions, and certifying an abstract graph's planar crossing number are further requirements. The 2015 proof only uses the nonstrict comparison. Any proof of the every-optimum statement along this route needs a separate structural equality analysis or a strictly better redraw than the elementary rectangular cut bound.

Source: https://eurocomb2015.w.uib.no/files/2015/08/endm1983.pdf, Problems 1.1/2.1 and Theorem 2.2. The work was inspected privately; this note reproduces no source text.

## Approach 4: homology cannot replace geometric intersection on higher genus

On a genus-two orientable surface choose a separating essential simple curve c cutting the surface into two once-punctured tori. In each side choose an essential properly embedded arc joining two points of c, and glue the two arcs at their endpoints to form a simple closed curve d. Choose the arcs non-boundary-parallel. The curves c,d cross twice, and there is no bigon: a bigon would make one of the two arcs boundary-parallel. Hence their geometric intersection number is two by the bigon criterion. But [c]=0 in H_1, so the algebraic intersection of [c] with [d] is zero.

This defeats the direct higher-genus substitution "replace torus determinants by the symplectic homology pairing and retain exact geometric information." Homology only supplies a possibly strict lower bound. It does not defeat more sophisticated free-homotopy or multicurve methods. Two cycles drawn along c,d are not a counterexample to the original question: both cycles are planar and their union has crossing number zero. Thus this construction is explicitly an obstruction to an approach, not an optimality certificate.

## Approach 5: amplification and random extraction do not automatically create strictness

Replace each original edge e by r parallel copies, drawn close together. Every crossing between distinct original edges becomes r^2 crossings. From any drawing of the amplified graph, choose one copy independently and uniformly for each original edge. If T is the number of crossings between copies of distinct original edges, the expected retained crossing count is T/r^2. Crossings between copies of the same original edge are never retained. Consequently the amplified optimum is at least r^2 times the original optimum, and the close-parallel construction attains equality (under the usual unrestricted crossing convention).

If an existential separation theorem only gives an amplified separated drawing with at most r^2 C crossings, random extraction yields a separated original drawing with at most C crossings. This proves existence, not that the starting original drawing was separated. At the expectation level there is no automatic strict saving. Strictness would follow if the redraw has a demonstrably discarded crossing between copies of the same original edge, or a strict total bound, or a separate equality-case obstruction. None has been established generally here. Parallel-edge graphs can be converted into simple graphs by giving each parallel edge its own internal subdivision vertex, but this does not manufacture the missing slack.

The exact equality witness in Approach 3 reinforces why a strictness audit is needed; it is not itself proof that every possible amplification/redraw has no slack.

## Outcome and stopping point

Five routes completed: two limited positive exclusions and three concrete method obstructions. No counterexample with certified optimality, and no strict separation theorem on the remaining arbitrary surfaces, has been established. The residual still requires either a universally strict redraw or an explicit intersecting drawing plus a matching global lower bound. Do not publish as a solution or as an independently verified proof of the September 2026 announcement.
