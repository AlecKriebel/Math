# OPG-605 / 3075: a deletion-induction obstruction and exact defect identities

Status: partial, stalled; the requested conjecture is not solved. This is an authored mathematical audit and finite certificate, not a claim of novel published mathematics. Three substantive approaches were used; the remaining two were not spent once the obstruction was isolated.

## 1. Exact target and literature boundary

A simple affine arrangement consists of n >= d+1 real hyperplanes in R^d, with every d normals independent and every d-fold intersection distinct. Its bounded chambers are closed d-polytopes. Write I = binom(n-1,d), S = sum_P diam(G(P)), and D = dI-S. Here G(P) is the vertex-edge graph, not a Euclidean metric space. The target is D >= 0 for every such arrangement.

The primary problem is [Open Problem Garden, node 605](https://www.openproblemgarden.org/op/average_diameter_of_a_bounded_cell_of_a_simple_arrangement), corresponding to [UnsolvedMath 3075](https://www.unsolvedmath.com/problems/3075). Direct retrieval of the latter failed; its exact imported record was matched to the supplied, byte-pinned corpus. That record and its complete report object were hashed without field projection.

[Deza and Xie](https://arxiv.org/abs/0710.0328) prove the planar case and small regimes and establish asymptotic lower constructions. The [2012 computational paper](https://www.cas.mcmaster.ca/~deza/aspm2012.pdf), Sections 1.2 and 5, retains the average-diameter conjecture while refuting the stronger external-facet lower bound E >= d binom(n-2,d-1): its minimum at (d,n)=(3,8) is 44 rather than the predicted 45. That refutation is not a counterexample to the average-diameter conjecture. Its exact small-parameter conclusions use realizability checks, not an identification of all abstract oriented matroids with real arrangements.

The [author's current publication list](https://www.cas.mcmaster.ca/~deza/pub.html) and targeted searches were checked on 2026-10-06. No general resolution was located. The recent [Facial distance and diameter, arXiv:2609.32440v1](https://arxiv.org/abs/2609.32440) uses Euclidean diameter (Section 1), so its newly resolved conjecture is a different question. Search failure is not proof of novelty or of unresolved status.

## 2. An exact defect identity without assuming Hirsch

Let f(P) be the number of actual facets of P, E the number of bounded arrangement facets incident to exactly one bounded chamber, and

    sigma = sum_P (f(P)-d-diam(G(P))).

The summands in sigma are signed. No nonnegativity assumption is made in arbitrary dimension.

**Proposition 1.** For every arrangement in the target class,

    D = E + sigma - 2 binom(n-2,d-1).                         (1)

**Proof.** On each supporting hyperplane, the other n-1 hyperplanes induce a simple (d-1)-arrangement. Consequently the total number F of bounded arrangement facets is n binom(n-2,d-1).

Every bounded arrangement facet has at least one bounded chamber incident to it. For completeness, fix such a facet in H and keep the signs of all other hyperplanes. Let K be the recession cone of those other halfspaces. Boundedness of the facet implies K intersect dir(H) = {0}. If both adjacent chambers were unbounded, there would be u,v in K with the H-normal strictly positive on u and strictly negative on v. A positive combination lies in K intersect dir(H), hence is zero. Thus K contains a line. But the other n-1 normals span R^d, so K is pointed, a contradiction. A bounded facet has either one or two bounded chambers on its sides, while an unbounded facet cannot be a facet of a bounded chamber. Double counting gives sum_P f(P)=2F-E.

Set B=binom(n-2,d-1). Since dI=(n-1)B, the definition of sigma gives

    S = 2nB-E-dI-sigma = dI+2B-E-sigma.

Rearranging proves (1). The elementary chamber-count formula and induced-facet count can also be obtained by the usual hyperplane-insertion recurrence. QED.

This keeps the exact term that would be lost by silently assuming the false general Hirsch conjecture. Equation (1) is an exact reformulation, not a new universal bound. The 2012 paper already uses its underlying incidence count.

## 3. A three-dimensional nonnegative-slack version

For d=3 define, for each bounded chamber,

    r(P) = the residue of 2f(P) modulo 3, in {0,1,2},
    t(P) = floor(2f(P)/3)-1-diam(G(P)),
    R = sum_P r(P),   T = sum_P t(P).

**Proposition 2.** Both R and T are nonnegative, and

    3D = 2E + R + 3T - 2(n-2)(n-3).                       (2)

In particular, E >= (n-2)(n-3) is a sufficient condition for this arrangement to satisfy the conjecture. The exact necessary-and-sufficient condition is 2E+R+3T >= 2(n-2)(n-3).

**Proof.** A simple 3-polytope with f facets has v=2f-4 vertices by Euler's formula and 3-regularity. Its graph is 3-connected. For two nonadjacent vertices at distance ell, Menger's theorem supplies three internally vertex-disjoint paths, each with at least ell edges. Thus v >= 2+3(ell-1), giving ell <= floor((v+1)/3)=floor(2f/3)-1. Adjacent pairs also satisfy this inequality because f>=4. Therefore t(P)>=0.

By definition, 3 diam(G(P))=2f(P)-r(P)-3-3t(P). Summing and using sum f(P)=2F-E, F=n(n-2)(n-3)/2, and I=(n-1)(n-2)(n-3)/6 gives (2). QED.

The local 3-polytope bound also underlies Deza-Xie's Proposition 6. Retaining all residues and diameter slacks gives a useful exact audit criterion; no improved universal lower bound on the right-hand side is proved here. The remaining problem is a global bound coupling external facets and cell structure, rather than merely checking one cell.

## 4. A rigorous obstruction to arbitrary-deletion induction

One tempting induction would prove, for every hyperplane H of every simple arrangement A,

    S(A)-S(A without H) <= d binom(n-2,d-1),               (3)

equivalently D(A) >= D(A without H). Together with the base case, this would imply the target. The following explicit planar example disproves (3).

**Proposition 3.** Let A be the eight lines a*x+b*y=c with rows

    (1,1,5), (1,2,-1), (1,4,2), (1,5,-2),
    (1,7,2), (1,8,-5), (1,9,-1), (1,10,-2).

Let H be x+8y=-5. Then A and A without H are simple and

    I(A)=21,              S(A)=36,        D(A)=6;
    I(A without H)=15,    S(A without H)=23, D(A without H)=7.

Thus S(A)-S(A without H)=13 > 12=2*(21-15), and D decreases on adding H.

**Exact finite proof.** All slopes b are distinct. Solving every pair of equations and evaluating every remaining line verifies, with rational arithmetic, that no three lines concur. The complete bounded-polygon enumeration is:

- A: eight triangles, eleven quadrilaterals, two hexagons.
- A without H: seven triangles, seven quadrilaterals, one pentagon.

A k-gon's graph is a cycle, of diameter floor(k/2). The asserted sums follow: 8+22+6=36 and 7+14+2=23. The independently replayable enumeration and all rational polygon coordinates are in witness.json.

The certificate is checked by two different exact constructions. The first joins consecutive intersection vertices on every arrangement line and identifies unbounded chambers from extreme rays. The second tests every sign vector by rational half-plane clipping against a square strictly containing all line intersections. A positive-area clipped polygon is bounded precisely when it misses the square boundary. It then counts polygon sides. Both constructions inspect all chambers, without numerical tolerances or floating-point LP decisions; their bounded sign-vector sets and side counts agree. The independent clipping algorithm's completeness is proved in VERIFYING.md. QED.

This is not a counterexample to OPG-605: both averages, 12/7 and 23/15, are below 2. It only refutes the universally quantified arbitrary-deletion strengthening. It also does not refute an induction that selects a suitable hyperplane: deleting the eight lines, in the listed order, gives defects [6,5,5,6,6,7,6,6]. No minimality or literature novelty is claimed for the witness.

## 5. Stop condition and remaining obstruction

Approach 1 retained signed Hirsch slack instead of using an invalid cellwise assumption. Approach 2 isolated the exact nonnegative-slack obstruction in dimension 3. Approach 3 tested arbitrary-deletion induction and produced Proposition 3, verified independently. These establish identities and a proof-route obstruction, not a new positive parameter regime or a full solution.

To finish the original problem one still needs a universal estimate E+sigma >= 2 binom(n-2,d-1), an adequate substitute, or a genuine counterexample with S>dI. Neither a general estimate nor such a counterexample was found. The packet stops as partial/stalled after 3/5 approaches. No repository or queue changes were made by this author.
