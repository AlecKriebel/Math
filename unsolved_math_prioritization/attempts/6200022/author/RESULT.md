# Delzant's diagonal convex-core question: attributed negative resolution

## Disposition and conventions

**6200022 / AMR-061-0022, rank 809.** The universal existence assertion is false under the standard compact-convex-core interpretation. This is an **already resolved literature target**, not a new solution. The investigation stopped after one substantive route, rather than spending the remaining four routes on a settled assertion.

Here a geometric action is an isometric, properly discontinuous, cocompact action on a proper CAT(0) space. A compact convex core requires a nonempty closed invariant convex subset C of the metric product X1 × X2 with compact quotient C/G. The product metric throughout is the CAT(0) Euclidean product metric, d² = d1² + d2². Merely having an invariant convex subset, such as the entire product, is insufficient. No assertion about the existence of a smallest such subset is needed for the counterexample.

The question has two logically distinct parts:

1. Do two geometric G-actions always have a compact convex core for the diagonal action?
2. When such a core does exist, can its visual boundary supply cell-like maps to the two factor boundaries?

The first answer is no. Section 3 gives an elementary counterexample valid for every member of an unbounded integer family. Section 4 proves a positive answer to the second question in the stated proper CAT(0) setting, indeed with homeomorphisms. The first negative answer does not logically settle the second question by itself.

## 1. Source normalization

The author-hosted Kapovich survey, *Problems on Boundaries of Groups and Kleinian Groups*, printed page 7, Problem 22, attributes the question to Thomas Delzant. The file inspected is dated October 24, 2007 on page 1 and says its problems were mostly collected at the 2005 AIM workshop. Thus 2005 is the catalog's problem-origin year, not the PDF's version date.

The statement asks about a diagonal action, mentions differently marked hyperbolic surface structures as a special case, and connects the boundary to the preceding cell-like-equivalence question. Its last parenthesis prints X1 and X2 where the context requires their boundaries. We make this correction explicitly; a visual boundary is not being required to map cell-like onto the noncompact spaces Xi. The compact-quotient interpretation of “convex core” is essential and is independently confirmed by Dey–Liu's formulation.

Source: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

The individual catalog page could not be retrieved during this review (web lookup failed; direct public request returned 403). Identity was recovered from the supplied complete catalog records and the independently inspected primary PDF. The public catalog listing also displays this ID/title. No live-page verification is claimed.

## 2. Prior result and attribution

Dey and Liu's *Rigidity of convex co-compact diagonal actions* directly identifies this as Delzant's Problem 22 and answers existence negatively. Their Theorem 1.2 says that a common rank-one element, proper factor actions, and a convex-cocompact diagonal action force proportional marked translation lengths. Corollary 1.5 gives an equivariant homothety criterion in the negatively curved surface case and certain symmetric cases. We inspected the arXiv v1 proof, and visually checked pages 1–2. EMS Press confirms publication online on July 4, 2025 in *Groups, Geometry, and Dynamics*, DOI 10.4171/GGD/908. The publisher's subscription PDF was not inspected; its publication metadata and the public preprint were checked separately.

- Public theorem text: https://arxiv.org/abs/2408.03462v1
- Publisher: https://ems.press/journals/ggd/articles/14298926
- DOI: https://doi.org/10.4171/GGD/908

The weighted-tree construction below already appears as background in Guilbault–Mooney's *Cell-Like Equivalences and Boundaries of CAT(0) Groups*, Examples 2.2 and 2.4: https://arxiv.org/abs/1011.1298v1 . We give our own direct midpoint proof of its obstruction. No priority for the example, negative answer, elementary argument, or conditional boundary lemma is claimed; exact novelty of the presentation has not been established.

## 3. An elementary obstruction requiring no rigidity theorem

### 3.1 Spaces and actions

Let G = F(a,b). Let T1 be its Cayley tree in the basis {a,b}, with all edges of length 1. Let T2 have the same vertices, edges, and labels, but a-edges have length 1 and b-edges length 2. Inversely labelled edges have the same length as their positive labels. The group acts on each tree by left multiplication.

Both are proper complete real trees and hence CAT(0). The actions are free, isometric, and properly discontinuous. Each quotient is a rose with two edges of finite length, so each action is cocompact. Let o=(1,1) and O=G·o in T1×T2. Under the common combinatorial identification of the two trees, d2≥d1.

### 3.2 Midpoints escape the diagonal orbit

For each integer n≥1 set w_n=a^(4n)b^(4n). The distances from 1 to w_n are 8n in T1 and 12n in T2. A geodesic in the Euclidean product progresses through both factor segments using the same fractional parameter. Therefore the midpoint p_n of [o,w_n·o] has coordinates

    p_n = (a^(4n), a^(4n)b^n).

Write x=a^(4n), y=a^(4n)b^n as vertices of the common unit-edge tree. For every g∈G, putting A=d1(x,g) and B=d1(y,g),

    d(p_n,(g,g))² = d1(x,g)² + d2(y,g)²
                  ≥ A²+B²
                  ≥ (A+B)²/2
                  ≥ d1(x,y)²/2 = n²/2.

Thus d(p_n,O)≥n/√2. This is a proof for all integers n, not an extrapolation from tested cases.

There is also an exact orbit-distance formula. The gate of any vertex g onto the combinatorial segment [x,y] is a vertex z=a^(4n)b^k for 0≤k≤n. The unique tree paths from x and y to g both pass through z; travelling off the segment cannot decrease either weighted distance. Hence the minimum occurs at a segment vertex and

    d(p_n,O)² = min_{0≤k≤n, k integer} [k²+4(n−k)²]
              = 4n²/5 + 5·dist(4n/5,Z)².

The nearest integer to 4n/5 lies in [0,n]. This refinement is checked by exact rational arithmetic in the accompanying script but is not needed for the contradiction.

### 3.3 No different invariant convex set can repair it

Suppose C were a nonempty invariant convex subset on which G acts cocompactly. Choose q∈C and let D=d(o,q). Cocompactness provides R<∞ with C⊂N_R(Gq): the orbit-distance function is continuous, invariant, and bounded on the compact quotient.

Let c_n be the midpoint of [q,w_nq]. Invariance and convexity give c_n∈C. The CAT(0) convexity inequality for corresponding points of two segments gives

    d(p_n,c_n) ≤ [d(o,q)+d(w_no,w_nq)]/2 = D.

Pick g_n with d(c_n,g_nq)≤R (or replace R by R+1). Since d(g_nq,g_no)=D,

    d(p_n,O) ≤ d(p_n,c_n)+d(c_n,g_nq)+d(g_nq,g_no) ≤ R+2D.

This contradicts n/√2→∞. It excludes every invariant cocompact convex C, not merely the convex hull of a chosen orbit. In particular, imposing closedness or minimality cannot restore a compact convex core.

The literature theorem provides a separate consistency check: the marked lengths of a are 1 and 1, while those of b are 1 and 2, so no common proportionality constant exists. Tree translations are rank one. The direct proof above does not depend on that theorem.

### 3.4 A control where a core does exist

If instead all lengths in T2 equal c>0 times their counterparts in T1, the canonical equivariant homothety f:T1→T2 has convex graph. The geodesic joining (x,f(x)) and (y,f(y)) stays in that graph, because homotheties preserve fractional geodesic parameters. The graph is closed and invariant, and its quotient is compact. Thus the failure is not automatic for every diagonal action.

## 4. The conditional boundary question

**Proposition.** Let G act geometrically on proper CAT(0) spaces X1 and X2. Suppose C⊂X1×X2 is nonempty, closed, convex, invariant, and C/G is compact. Then each factor projection induces a G-equivariant homeomorphism

    ∂∞C → ∂∞Xi.

Consequently Z=∂∞C has cell-like maps to both factor boundaries, since every fiber is a singleton.

**Proof.** C is proper CAT(0), and the restricted action is geometric. Fix o∈C. By the geometric-action orbit quasi-isometry theorem (Švarc–Milnor), the orbit maps G→C and G→Xi are quasi-isometries. The equivariant projection f=π_i|C identifies their orbit maps. Since the G-orbits are coarsely dense and f is 1-Lipschitz, f itself is a quasi-isometry. In particular, there are A≥1 and B≥0 such that

    d_C(u,v) ≤ A·d_Xi(f(u),f(v)) + B,  u,v∈C,

and f(C) is coarsely dense in Xi.

Each unit-speed ray r from o projects to a constant-speed geodesic, because C is convex in the metric product. Write s(r)=d_Xi(f(o),f(r(1))). Its projected speed is s(r). Substituting u=o,v=r(t) in the preceding inequality and sending t→∞ gives s(r)≥1/A. Also s(r)≤1. Thus the projection never collapses an infinite ray. Send r to the endpoint of the unit-speed ray t↦f(r(t/s(r))).

This boundary map is well-defined independently of basepoint: boundedly asymptotic rays project boundedly close; their projected speeds must agree, and their normalized projections define the same endpoint. It is equivariant by the equivariance of f.

For continuity, use the compact-open topology on rays from o. The speed s(r) is a continuous function of r, as it is read at time 1, and is bounded away from zero. Reparametrizing by 1/s(r) and applying the continuous 1-Lipschitz map f therefore preserves compact-open convergence.

For injectivity, let rays r,r' from o have the same projected endpoint, with speeds s,s'. Unique geodesic rays from f(o) imply

    f(r(t/s)) = f(r'(t/s'))   for every t≥0.

The quasi-isometry inequality gives d_C(r(t/s),r'(t/s'))≤B, so |t/s−t/s'|≤B. Letting t grow shows s=s'. It follows that r and r' are boundedly asymptotic, hence represent the same point of ∂∞C.

For surjectivity, let α be a unit ray in Xi from f(o). Choose c_n∈C with d_Xi(f(c_n),α(n))≤R for a fixed R. Set L_n=d_C(o,c_n). The 1-Lipschitz and quasi-isometry bounds give

    n−R ≤ L_n ≤ A(n+R)+B.

Therefore L_n→∞. Properness gives a subsequence of the unit-speed segments [o,c_n] converging on compact intervals to a ray r in C. Pass to a further subsequence such that their projected speeds s_n converge to s∈[1/A,1]. The factor endpoints are R-close to α(n), and their distances from f(o) differ from n by at most R. For fixed u, CAT(0) convexity bounds the distance between the point at distance u on [f(o),f(c_n)] and α(u) by at most 2Ru/n for sufficiently large n. Hence these normalized factor segments converge to α. Their other description as projected segments converges to t↦f(r(t/s)), proving that r maps to α(∞).

Finally ∂∞C is compact and ∂∞Xi is Hausdorff for proper CAT(0) spaces. A continuous bijection is a homeomorphism. If the spaces are bounded, all visual boundaries are empty and the same conclusion holds with empty spaces; otherwise the proof applies to every ray. ∎

This proof uses the affine-on-geodesics property of a factor projection. It does not assert that arbitrary quasi-isometries of CAT(0) spaces extend to their boundaries. The existence of C is the strong missing hypothesis in the counterexample.

## 5. Limits, status, and audit requirements

- The original universal compact-core assertion is answered negatively and explicitly in prior published work. No new open-problem solution is claimed.
- The conditional boundary proposition has a complete conventional proof here under explicit proper CAT(0) hypotheses. It is an explanatory lemma with unestablished novelty, not attributed to Dey–Liu as a stated result.
- This does not resolve whether arbitrary CAT(0) boundaries of the same group are cell-like equivalent when no diagonal compact convex core exists. That is the distinct neighboring Problem 21.
- Exact finite checks support the midpoint and distance calculations. They do not certify the CAT(0) argument, prove a theorem by enumeration, check the general rigidity theorem formally, or replace expert review.
- Full supplied records were read and bound by the specified complete-review digest. Previously recorded work was only triage. Targeted current repository searches located no substantive earlier artifact for this ID; that bounded search is not a guarantee about every historical branch or unindexed file.
- An uninvolved mathematical audit should scrutinize the arbitrary-core transfer in §3.3 and the boundary-surjectivity argument in §4. No independent audit or formal proof certification is represented as completed in this author freeze.
