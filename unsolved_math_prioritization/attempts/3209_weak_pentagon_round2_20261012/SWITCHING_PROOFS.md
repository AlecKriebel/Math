# Second-round fixed-cut research: exact switching barriers and scoped positive certificates

## Result and limits

No global-maximum-cut obstruction was found. This packet proves elementary, exact restrictions on local and global optimality, gives an authored sharpness example for the four-vertex-switch bound, and supplies directly checked positive extension certificates for 33,400 graph–cut records (33,386 distinct labeled graph–cut pairs) in explicitly bounded constructed samples. It does not prove that all maximum cuts extend, or settle the Weak pentagon conjecture. No novelty is claimed.

The strongest new negative conclusion concerns a proposed construction route: **no triangle-free cubic completion injectively retaining the 19-edge proof core of the first-round obstruction, with its prescribed edge statuses, can make that cut globally maximum.** Two sealed three-vertex switches prevent it. This rules out preserving that core and simply attaching an amplification gadget at its four available ports.

The original target is a homomorphism to the Clebsch graph. Prescribing which edges use the canonical antipodal difference is stronger. All constructed finite records retained here have explicit positive prescribed witnesses; the negative core has an unrestricted positive witness. None is a counterexample to the original target.

## Definitions

Let G be a finite simple triangle-free cubic graph, let B=δ(S) be a cut, and let M=E(G)\B. A fixed-M extension assigns f(v) in F₂⁴ so that the xor difference on M is 15 and on B is one of 1,2,4,8. For X⊆V(G), switching X means replacing S by S△X. Its gain is

    g(X)=|δ_M(X)|−|δ_B(X)|.

A cut is k-stable if g(X)≤0 for every X with 1≤|X|≤k. Zero-gain switches are allowed. A global maximum is exactly a cut satisfying this inequality for every X. A one-stable cubic cut has matching complement M. Write W=V(M), m=|M|, U=V(G)\W and u=|U|.

For a matching complement and any X, put r=|X∩W|, b=e_B(X), and a=e_M(X). Cubic degree counting gives the useful exact identity

    g(X)=2r−3|X|+2b−2a.                         (1)

## Theorem 1: exact three/four-switch characterization and sharp density

For a matching cut complement M in a simple triangle-free cubic graph, the following are equivalent:

1. The cut is three-stable.
2. The cut is four-stable.
3. The graph B[W] has maximum degree at most 1.

Every such cut satisfies m≤3|V(G)|/8. The bound is attained by the 16-vertex example below, so this is sharp for three- and four-stable cuts.

### Proof

If B[W] has a path a–b–c, the three vertices are distinct and all are M-saturated. Their M-edges leave this set: the only possible internal M-edge would join a to c and form a triangle. Its B-boundary has size 2, and its M-boundary has size 3. Switching these three vertices gains 1.

Conversely, assume B[W] has maximum degree 1. For |X|≤2, (1) immediately gives nonpositive gain. For |X|=3, if r≤2 then b≤2 by triangle-freeness, so (1) is negative. If r=3 then b≤1, so again the gain is negative.

For |X|=4, a bipartite graph on four vertices has at most four edges. If r≤2 this suffices in (1). If r=4 then b≤2. If r=3, the one vertex of X outside W can contribute at most three B-edges and B[X∩W] at most one; attaining four would create a triangle. Hence b≤3. Again (1) is nonpositive. This proves all equivalences.

Every vertex of W has B-degree 2 and at most one B-neighbor in W. Consequently at least 2m B-edges join W to U. There are at most 3u such edges. Thus 2m≤3u=3(n−2m), or 8m≤3n. ∎

Since M is a perfect matching of G[W] and B[W] is a matching, G[W] consists of alternating paths and alternating cycles. Any such cycle has a multiple of four edges: its B-edges form an even cut intersection and alternate with M.

## Authored sharpness example, and its exact global maximum

Take V={0,…,15}, S={8,…,15}, and the following 24 edges (unordered pairs):

    (0,1) (2,3) (4,5) (8,9) (10,11) (12,13)
    (1,12) (5,8) (3,10) (4,13) (2,9) (0,11)
    (0,14) (1,15) (2,15) (3,14) (4,14) (5,15)
    (8,7) (9,6) (10,6) (11,7) (12,6) (13,7).

The first six edges are M. Its endpoint set W has 12 vertices. The next six edges are precisely B[W], a perfect matching. Hence Theorem 1 gives four-stability, and m=6=3n/8. The cut has size 18.

The set X={0,3,4,10,14} induces the B-tree with edges 14–0,14–3,14–4,3–10; its four M-edges leave X, while its B-boundary has size 3. It therefore improves the cut by 1. Direct enumeration of all subsets of sizes 1,…,5 independently gives maximum gains −1,0,−1,0,1.

The actual maximum cut is 22. An attaining cut is

    S*={1,2,5,6,8,11,13,14}.

The two vertex-disjoint pentagons

    0–11–10–3–14–0,
    2–9–8–5–15–2

force every cut to omit at least two edges, proving the matching upper bound 24−2=22. An independent recurrence over all 2^15 normalized cuts confirms that S* (mask 26982) is the unique normalized maximum. This exhaustive check is additional to the human certificate.

The original six-edge M does extend. One fixed-M witness, in vertex order 0,…,15, is

    (0,15,9,6,3,12,15,0,4,11,7,8,13,2,2,13).

Thus this example sharply separates small-switch optimality from global optimality, without furnishing an extension obstruction.

## Theorem 2: a five-switch obstruction and a local density consequence

In a five-stable cut, an unsaturated vertex x with three neighbors in W cannot have a neighbor a that itself has a B-neighbor d in W.

Indeed, writing the other two neighbors of x as b,c, the five distinct vertices x,a,b,c,d induce the B-tree xa,xb,xc,ad. Theorem 1 prevents further B-edges from d to b or c. No M-edge is internal: M-edges between a,b,c would create triangles with x, and d lies on the opposite cut side from a,b,c. Equation(1), with r=4,b=4,a=0, gives gain 1.

This necessary restriction implies m≤n/3 for every five-stable cut. To see this, let a₀ be the number of edges of B[W], and let n_i count vertices of U with exactly i neighbors in W. The 2a₀ endpoints of B[W] each have exactly one B-neighbor in U, and that neighbor has at most two W-neighbors by the forbidden-tree result. Therefore

    2a₀≤n₁+2n₂,
    4m−2a₀=n₁+2n₂+3n₃.

Adding yields 4m≤2n₁+4n₂+3n₃≤4u, so m≤u=n−2m.

This is only a necessary five-stability test, not a characterization; additional five-vertex patterns can improve a cut. Sharpness of the n/3 bound is not claimed. Nor is this a global-maxcut numerical improvement: the known 4/5 edge-cut theorem for triangle-free subcubic graphs gives the stronger global bound m≤3n/10. DeVos and Šámal attribute the underlying theorem to Hopkins–Staton and Bondy–Locke; that published theorem's full proof is not independently audited here.

A further elementary global restriction is that B spans a connected graph whenever G is connected: if B had several components, a component with an incident M-edge could be switched with no B loss and a positive M gain.

## The sealed-core amplification barrier

Consider the 14-vertex graph with 19 edges

    (0,1) (0,4) (0,11) (1,2) (1,8) (2,6) (2,12)
    (3,5) (3,12) (4,7) (5,9) (5,13) (6,7) (6,10)
    (7,9) (8,9) (8,10) (11,12) (11,13),

with S={1,3,6,7,8,11,13} and

    M={(0,4),(1,8),(2,12),(5,9),(6,7),(11,13)}.

This is the first-round obstruction with the two proof-unused cut edges (3,10) and(4,13) removed. Its fixed-M obstruction survives: normalize the pentagon 0–1–2–12–11–0 to f(0)=0,f(1)=1,f(2)=3,f(11)=4,f(12)=12. Then f(4)=15,f(8)=14,f(13)=11. Cube-neighbor intersections force

    f(6)∈N(3)∩N(0)={1,2};
    f(6)=2, since 1 and 14 are antipodal but 6–10–8 is a two-edge unit path;
    f(5)∈N(11)∩N(1)={3,9};
    f(5)=3, since 7–9 is a unit edge and f(6) xor f(5) must be a unit.

But 5–3–12 would then be a two-edge unit path from 3 to 12, which are antipodal. This is impossible. The normalization is legitimate because the four unit edges of the pentagon must use all four coordinate directions.

Both triples {1,2,6} and{7,8,9} consist of M-saturated vertices joined by a B-path. Every vertex in either triple already has degree 3 inside this 19-edge core. Each triple has gain 1, and no cubic completion can add an edge at its vertices. Thus **every cubic completion preserving these core edges and cut statuses has an improving three-switch**, irrespective of what gadget is added at vertices 3,4,10,13. In particular it cannot be globally maximum.

This does not rule out a construction that changes the proof core or simulates its constraints through different gadgets. It pinpoints exactly why keeping this core intact cannot work.

The unrestricted Clebsch witness inherited from the authored full graph is

    (0,1,3,9,1,8,2,3,5,7,13,4,11,0).

It works on every retained core edge. Hence the negative claim is only about the prescribed M.

## Bounded computational scope and independently checked certificates

No first-round catalog was rescanned. Four authored seeded construction runs were retained:

- Pentagon packing: 200 graph–cut records for each of 6,8,10,12,16,20,30,40 vertex-disjoint pentagons, hence orders 30,40,50,60,80,100,150,200; 1,600 records total. A cross-cut perfect matching completes all degrees, and no matching edge joins vertices of the same pentagon. The one uncut edge on each pentagon gives m=k. The k disjoint odd cycles prove every specified cut is globally maximum. Every specified cut extends. These are not all maximum cuts of the sampled graphs, or all graphs of those orders.
- Small defects: 1,000 records for each order 14,16,18,20,22,24,28,32,40 and each m∈{4,5}; 18,000 total. M is split 2+2 between cut sides for m=4 and 4+1 for m=5. This follows the cubic side-degree identity 3|S|−2m_S=3|Sᶜ|−2m_{Sᶜ}. Every retained record extends. Global optimality is not asserted.
- Rejection-based three-stable screen: 1,000 records with m=6 at each order 16,18,20,22,24,28,32,40,48; 9,000 total. An inefficient attempted next group was interrupted, then excluded in full; only these nine completed groups are claimed. No interruption was interpreted as unsatisfiability. Every retained record extends.
- Direct three-stable construction: 200 records for each of the 24 parameter pairs listed in [SWITCHING_AUDIT.md](SWITCHING_AUDIT.md); m∈{6,8,10,12,16,20,30,40}, with orders 16–120; 4,800 total. The generator builds B[W] as a matching directly. Every retained record extends. Global optimality is not asserted.

These are deterministic constructed samples, not exhaustive lists, uniform random samples, or nonisomorphic graph catalogs. There are 33,400 records and 33,386 distinct labeled graph–cut pairs across the four families. Only the 1,600 pentagon-family cuts are guaranteed globally maximum by the family certificate; global optimality is not claimed for the other 31,800 records. Exact scope and duplicate counts appear in [SWITCHING_AUDIT.md](SWITCHING_AUDIT.md). No extrapolation to untested cases is justified.

An authored finite-domain solver generated the positive witnesses. Every retained result is positive, so correctness does not depend on trusting solver exhaustion. A separately authored mathematical checker imported no builder code or solver. It checked graph simplicity, connectivity, cubic degrees and triangle-freeness; every prescribed matching and unit/antipodal difference; claimed local invariants; and odd-cycle packing certificates for the 1,600 globally maximum pentagon-family cuts. It also checked small-switch gains and the normalized cuts of the sharpness example. That original checker did not enforce a complete inventory or incoming integrity metadata; the separate independent audit supplied the required fail-closed integrity wrapper and active negative controls.

## Reproduction and sources

This prose edition includes no executable builders, retained raw sample collections, search logs, or operational identities. The written proofs and displayed small graphs can be checked directly. An independent implementation can follow the constructions and tests described here, but the exact original seeded runs cannot be regenerated from this edition alone. [REPRODUCTION_SCOPE.md](REPRODUCTION_SCOPE.md) separates public proof checking from prior full-run replay and records all bounded counts and caveats.

- Matt DeVos and Robert Šámal, High-girth cubic graphs are homomorphic to the Clebsch graph, author manuscript: https://iuuk.mff.cuni.cz/~samal/papers/clebsch/clebsch.pdf. This supplies background formulation and the attribution of the 4/5 edge-cut theorem. Publisher abstract: https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.20580.
- J. Adrian Bondy and Stephen C. Locke, Largest bipartite subgraphs in triangle-free graphs with maximum degree three, Journal of Graph Theory 10(1986),477–504. Bibliographic information checked in the DeVos–Šámal references; the complete original proof was not retrieved or audited in this task.
- First-round authored 14-vertex graph: the retained 19-edge core and complete argument are displayed above. Source-lineage checks were performed during the audit; excluded program and raw-artifact identities are not published here. No third-party catalog records or copied source documents are included.

The second-round outcome is a rigorous obstruction to one natural amplification strategy, a sharp small-switch theorem with a human exact-maxcut example, and bounded positive evidence. The unrestricted conjecture and the all-global-maxcuts strengthening both remain open in this work.
