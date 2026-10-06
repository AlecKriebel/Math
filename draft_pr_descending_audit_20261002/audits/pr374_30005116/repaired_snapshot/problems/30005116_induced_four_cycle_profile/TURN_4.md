# Turn 4: the full proposed profile for weighted cographs and their limits

**Original unrestricted problem unresolved; fourth substantive author turn.** The result of this turn is complete for the recursively defined cograph class, including arbitrary positive vertex weights and arbitrary cotree depth. It does not reduce arbitrary hosts to that class.

Continue to write F(x)=3[(1−x)²−L(1−x)] for the proposed profile from turn1. For x≤1/2 this equals the known exact unrestricted value3x²/2. The formulas in this turn use the unlabeled induced-C4 density c(W) and edge density p(W) defined in turn2.

## 1. Three properties of the explicit profile

The following properties hold:

    (i)  0≤F(x)≤3/8 for all x∈[0,1];
    (ii) F is nonincreasing on [1/2,1];
    (iii) F(x)≥(3/2)(1−x)² for x∈[1/2,1].              (1)

**Proof.** Let q=1−x. On an open interval between reciprocal-integer q, the minimizing vector from turn1 has r copies of a and one b, with ra+b=1 and ra²+b²=q. Its fourth moment is L(q)=ra⁴+b⁴. Differentiating the two constraints gives

    r da+db=0,       2r(a−b) da=dq.

Therefore

    dL/dq=2(a²+ab+b²),
    F′(x)=−6[(r−1)a²−ab].                              (2)

For x>1/2 one has r≥2, a≥b≥0, so (2) is nonpositive on every interval. Continuity at knots and at1, already proved in turn1, gives (ii). Combined with F(x)=3x²/2 below1/2 and F(1/2)=3/8, this proves (i).

For (iii), in the minimizing vector every part is at most a and q≥ra²≥2a². Hence

    L(q)=∑a_i⁴ ≤ a²∑a_i² ≤q²/2.

Thus F(x)=3(q²−L(q))≥3q²/2, including the endpoints by continuity. ∎

## 2. Closure under complete joins

Suppose finitely many graphons W_i each satisfy

    c(W_i)≤F(p_i),      p_i=p(W_i).

Place them on blocks of positive masses w_i summing to1 and put all edges between different blocks. The resulting complete join also satisfies c(W)≤F(p(W)).

Indeed turn2's exact count

    c(W)=∑w_i⁴c(W_i)+6∑_{i<j}w_i²w_j²(1−p_i)(1−p_j)   (3)

shows that we may replace each W_i by a complete multipartite graphon of the same density achieving F(p_i), without decreasing the global C4 density or changing global edge density. The resulting join is itself complete multipartite, so turn1 applies.

If a child has p_i=1, it has W_i=1 almost everywhere and c(W_i)=0. Approximate that child by balanced multipartite graphons with an increasing number of parts. Their edge densities tend to1 and C4 densities to0; (3) and continuity of F give the same conclusion. Thus no fictitious positive-mass part vector of edge density exactly1 is assumed. For finite weighted cotrees with empty leaves all child densities are below1, so this limiting endpoint is not needed there.

This closure statement differs from turn2: children may now have internal density above1/2, provided their own profile inequality has already been established.

## 3. Closure under disjoint unions, with a strict high-density gap

Suppose again that c(W_i)≤F(p_i), and form their disjoint union with masses w_i>0 summing to1. Then

    x=p(W)=∑w_i²p_i,        c(W)=∑w_i⁴c(W_i).           (4)

The union satisfies c(W)≤F(x). If 1/2<x<1 and the union is nontrivial, let w=max_i w_i<1. Then the stronger bound holds:

    c(W) ≤ F(x) − (3/8)(1−w)(1−x)²[4−(1−x)].          (5)

**Proof.** If x≤1/2, the universal matching inequality c(W)≤3x²/2 from turn2 is already exactly F(x). Suppose x>1/2. Since

    x≤∑w_i²≤max_i w_i=w,

a largest child has mass w≥x>1/2 and is unique. Let p be its internal edge density. The other children contribute at most (1−w)² to x, so

    p≥[x−(1−w)²]/w² ≥x.                               (6)

For the second inequality, after multiplying by w² it suffices that

    (1−w)[x(1+w)−(1−w)]≥0,

which holds because x,w>1/2; if w=1 it is equality. The monotonicity in(1) therefore gives F(p)≤F(x). Every other child has C4 density at most3/8 by its assumed bound and(1). Consequently

    c(W)≤w⁴F(x)+(3/8)∑_{i≠i_max}w_i⁴
         ≤w⁴F(x)+(3/8)(1−w)⁴.                         (7)

Set q=1−x. Since1−w≤q, the difference between F(x) and the right side of(7) is at least

    (1−w)F(x)−(3/8)(1−w)⁴
      ≥(1−w)[(3/2)q²−(3/8)q³]
      =(3/8)(1−w)q²(4−q).

This proves(5), and the final expression is strictly positive when x<1 and w<1. The x=1 endpoint has C4 density0 directly. ∎

The proof actually needs the full profile bound only for the largest child; a bound3/8 suffices for the others. No assertion that a component's density equals the global density is used.

## 4. Theorem: arbitrary finite weighted cotrees

A finite weighted cograph graphon is constructed from finitely many independent leaf blocks of arbitrary positive masses, recursively combining subblocks by either disjoint union (all cross edges absent) or complete join (all cross edges present). The masses are normalized within each subproblem. The associated rooted expression tree is a cotree. This is the usual recursive cograph class; the classical equivalence with finite induced-P4-free graphs is terminology/background, not a substitute for the proof below.

**Theorem.** Every such weighted cograph graphon W satisfies

    c(W)≤F(p(W)).                                      (8)

The supremum within this class at every edge density is exactly F, since the complete multipartite graphons from turn1 belong to the class, with x=1 obtained as a limit.

**Proof.** Induct on the finite cotree. A single independent leaf has p=c=0 and satisfies the bound. At a join node use Section2, and at a union node use Section3. Both operations allow arbitrary child masses and arbitrary child densities, and their hypotheses are supplied by induction. There is no restriction on the number of nodes or depth. The matching constructions were proved in turn1. ∎

In particular, for every finite cograph G on n≥4 vertices, its adjacency graphon is a weighted cograph with leaf masses1/n. The replacement-sampling estimate from turn2 gives the explicit bound

    ρ(C4,G)≤F((1−1/n)x(G))+6/n.                        (9)

Consequently every sequence of finite cographs, even with unbounded cotree depth and number of leaves, has limsup induced-C4 density at most F(x) when its edge densities tend to x. More generally the same is true for any limit, in edge and induced-C4 densities, of the finite weighted cotree class. Continuity of F is enough; no uniform-depth approximation theorem is assumed.

## 5. What this does and does not settle

The theorem proves the exact proposed profile throughout a genuine non-multipartite recursive class. The paw blow-ups tying F in turn2 are cographs: their inner block is a disjoint union of a complete bipartite graph and an independent set, joined to the other independent parts. Thus the cograph theorem is compatible with those nonunique equality examples.

For any finite positive-mass disjoint-union node whose own edge density lies strictly between1/2 and1, (5) supplies a positive local gap if its children satisfy the profile bound. This is not a uniform global stability theorem when a component mass tends to zero, a density approaches1, or the cotree changes with n.

The source conjecture quantifies over **all** graphs. Graphs outside the cograph class and arbitrary graphons need not admit any union/join decomposition on which this induction can begin. No removal lemma or quantitative conclusion about almost-P4-free graphs is silently invoked. The original remains unresolved after four turns. No historical novelty is claimed for cograph terminology, the underlying multipartite construction, or the scoped deduction.

## Verification and sources

`verify_turn4.py` independently checks the profile derivative identities and bounds, the union-gap arithmetic on an exact parameter grid, all finite cographs through the declared order using both recursive and induced-P4 recognition, and selected weighted cotrees. Direct weighted motif counts are compared with the exact radical inequality from turn1. The all-size conclusion follows from the written closure proof, not from enumeration.

Source profile and credited known low-density bound: https://arxiv.org/abs/2106.16203v2 . A primary contemporary statement of the standard recursive cograph definition and its P4-free equivalence is Coudert–Coulomb–Ducoffe, *Leanness Computation: Small Values and Special Graph Classes*, DMTCS26:2#13(2024), Section6.2, https://dmtcs.episciences.org/13878/pdf , crediting Corneil et al.(1981). That paper's leanness results are not used here.
