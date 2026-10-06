# Elementary partial results and the remaining gap

**Main target remains unsolved.** All assertions below are scoped lemmas or stronger-hypothesis results. The arguments are mathematical proofs, not finite experiments. Standard product-measure association, planar rectangle separation and the Burton–Keane uniqueness theorem are credited where invoked. No novelty claim is made.

Write H for a vertex-induced lattice half-plane and E_H for the event that its open subgraph has an infinite component. Unless stated otherwise, a lemma works for both bond and site percolation.

## 1. Translation invariance of the half-plane existence event

**Lemma 1.** For a translation-invariant law and a fixed affine half-plane H, E_H has a translation-invariant representative modulo a null set. In particular, under ergodicity for the full translation group its probability is zero or one. No finite energy or association is required.

**Proof.** For any lattice translation z, H and H+z are parallel half-planes, hence one contains the other. Therefore E_H and E_{H+z} are nested. Translation invariance gives them equal probabilities, so their symmetric difference is null. Let

E*= intersection over z in Z^2 of E_{H+z}.

This is a countable intersection, is exactly translation-invariant, and differs from E_H only by a null set. Apply ergodicity to E*. This works for any fixed real normal vector, with no rational-slope assumption. ∎

The lemma does not prove that the probability is positive. Without ergodicity, a translation-invariant event can have intermediate probability. An illustrative law is the equal mixture of independent bond percolation with parameters 1/10 and 9/10. It is positively associated: realize its coordinates as increasing functions of the common Bernoulli parameter selector and independent uniforms. Its one-edge conditional probabilities lie in [1/10,9/10]. At parameter 1/10 the self-avoiding-path bound 4·3^(n−1)(1/10)^n rules out any infinite cluster. At parameter 9/10, Theorem 5 below proves half-plane percolation. Thus the mixture gives P(E_H)=1/2. It does not satisfy the target's almost-sure whole-plane percolation premise and is not a counterexample.

## 2. Fixed-root formulation and the order-of-limits obstruction

For a fixed root o in H, let A_n(H,o) be the event of an open path from o to the vertex boundary of o+[-n,n]^2, wholly in H and in that box. Then A_n decreases in n and

P(o is in an infinite H-cluster) = lim as n→∞ P(A_n(H,o)).       (1)

Indeed, an infinite cluster reaches every boundary. Conversely, the tree of finite self-avoiding open paths from o is locally finite; paths of arbitrarily large length give an infinite ray by the elementary finitely-branching tree lemma. Continuity from above proves (1). Also E_H is the countable union, over v in H, of the events that v is in an infinite H-cluster. Hence P(E_H)>0 if and only if this probability is positive for some v.

For H_m={y≥−m}, m≥0, define a_(m,n)=P(A_n(H_m,0)). These numbers increase with m and decrease with n. For m≥n the half-plane constraint inside the box vanishes. Consequently

lim_n lim_m a_(m,n) = P(0 is in an infinite whole-plane cluster),

whereas

lim_m lim_n a_(m,n) = P(0 is in an infinite cluster inside some H_m).

The second equality uses the increasing union over m. The two limits cannot be interchanged merely from the displayed monotonicities. The deterministic array b_(m,n)=1 if m≥n and 0 otherwise has the same monotonicities, with iterated limits 1 and 0. It is only a logical limit-order control, not a percolation counterexample.

There is a useful whole-plane bound. Assume at most one infinite cluster almost surely, translation invariance, and positive association. Put θ=P(0↔∞). For every lattice vertex x,

P(0↔x) ≥ P(0↔∞, x↔∞) ≥ θ².                    (2)

The first inequality uses uniqueness; the second uses association and translation invariance. Almost-sure whole-plane percolation implies θ>0 by countability. The usual translation-invariant finite-energy setting is covered by the classical Burton–Keane uniqueness theorem; see [HM], introduction, and [KK], Section 1.2. Formula (2) can instead simply be read with uniqueness as an explicit hypothesis.

For each fixed x, increasing finite boxes recover P(0↔x), so connections in some sufficiently large box have probability at least θ²/2. The required box depends on x. Neither (2) nor continuity supplies one fixed lower margin, bounded aspect ratio, or a summable failure estimate as x tends to infinity. That missing confinement step is the obstruction in this route.

## 3. What finite-energy surgery and FKG actually provide

**Lemma 2.** Assume finite energy and positive association. If the induced nearest-neighbor graph H is connected and P(E_H)>0, then every fixed o in H has positive probability of belonging to an infinite H-cluster.

**Proof.** Choose v in H with θ_H(v)>0 by countability. Choose a finite nearest-neighbor path from o to v in H. Let F be its edges in the bond case or its vertices in the site case. Finite energy implies P(all coordinates of F are open)>0. To see this without a uniform bound, add one coordinate at a time: conditional on an event specifying finitely many other coordinates, its strictly positive full conditional opening probability has strictly positive conditional expectation. Induction proves the finite-cylinder claim.

The all-open-path event and {v↔∞ in H} are increasing, so their intersection has probability at least P(F open)θ_H(v)>0. On this intersection o belongs to that infinite cluster. ∎

Under a uniform lower opening bound q>0, the same reasoning gives P(F open)≥q^|F|. This factor is useful for a fixed path. If the repair length tends to infinity, q^|F| can tend to zero. Moreover, opening a finite connector to a whole-plane infinite cluster does not imply its ray thereafter stays in H. Thus the lemma cannot create half-plane survival from whole-plane survival.

### A full-support associated law that fails the lattice condition

This finite example prevents substituting conditional FKG for the stated inequality. Take independent fair bits A,B and set Y=(A,B,A∨B). Independently pass each Y_i through a binary symmetric channel with flip probability 1/10, obtaining X_i. Equivalently, with independent uniform V_i, use X_i=1 when V_i≥9/10−(4/5)Y_i. Each output is increasing in all underlying independent coordinates A,B,V_1,V_2,V_3. By the Harris inequality for product laws, X is positively associated. Every configuration has positive probability, and each one-coordinate conditional opening probability given the other outputs is in [1/10,9/10].

The four possibilities for Y, each of probability 1/4, are 000,101,011,111. Directly summing their independent-channel probabilities gives

P(X=001)=63/1000,  P(X=111)=223/1000,
P(X=101)=P(X=011)=207/1000.

For u=101 and v=011, the lattice condition would require

P(001)P(111) ≥ P(101)P(011),

but 63·223=14049 < 42849=207². Indeed, conditional on X_3=1, the covariance of X_1,X_2 is

223/700 − (43/70)² = −72/1225 < 0.

This is a finite-law hypothesis control, not an infinite lattice law or a counterexample to the target.

## 4. A deterministic gluing criterion

For k≥1, let R_k be the lattice rectangle

[0,2^k] × [2^k,2^(k+2)],

and let S_k be

[0,2^(k+1)] × [2^(k+1),2^(k+2)].

Let V_k denote an open bottom-to-top crossing of R_k and W_k an open left-to-right crossing of S_k, always using nearest-neighbor paths contained in the indicated rectangle.

**Lemma 3.** If V_k and W_k occur for every k≥K, the first coordinate quadrant contains an infinite open connected component.

**Proof.** A crossing of R_k contains a bottom-to-top subcrossing of the overlap [0,2^k]×[2^(k+1),2^(k+2)]. A crossing of S_k contains a left-to-right subcrossing of that overlap. In the square lattice a nearest-neighbor horizontal and vertical crossing of a rectangle share a vertex: otherwise their planar polygonal curves would violate rectangle separation. Hence the chosen R_k path meets the chosen S_k path. The R_(k+1) vertical crossing likewise contains a vertical crossing of S_k and meets its horizontal crossing. Thus S_k joins the R_k and R_(k+1) paths. The union over k≥K is connected and reaches unbounded heights; it therefore belongs to an infinite open component. ∎

**Corollary 4.** For any percolation law, if

sum_k [P(V_k fails)+P(W_k fails)] < ∞,             (3)

the first quadrant percolates almost surely. No independence, association, stationarity or energy condition is needed.

**Proof.** The first Borel–Cantelli lemma gives a finite random K beyond which all the crossings succeed. Apply Lemma 3. ∎

With association, a weaker-looking positive-probability formulation can also be useful: for increasing events C_k whose simultaneous occurrence produces the same chain, if P(C_k)>0 for all k and sum_k[1−P(C_k)]<∞, then

P(intersection_k C_k) ≥ product_k P(C_k)>0.

The finite inequalities follow by iterating association; continuity from above gives the infinite inequality. For all large k, P(C_k)≥1/2 and −log P(C_k)≤2(1−P(C_k)), proving positivity of the product. A fixed lower bound P(C_k)≥c with 0<c<1 does not suffice, since the resulting lower bound c^N tends to zero. No summable estimate (3) is derived from the target assumptions.

## 5. A proved stronger-hypothesis subclass

**Theorem 5 (elementary high-density sufficient condition).** Consider any bond law on Z² satisfying, for every edge e,

P(e open | all other edges) ≥ q almost surely,

for one deterministic q>2/3. Then almost surely every affine Euclidean half-plane simultaneously contains an infinite open cluster.

For site percolation the same conclusion holds with the analogous one-site bound and q>6/7. Translation invariance, ergodicity, association and a uniform upper opening bound are not needed for either statement.

**Proof.** Put ε=1−q. For any finite collection F of distinct coordinates,

P(all coordinates in F are closed) ≤ ε^|F|.       (4)

For a chosen e in F, condition on all other coordinates: multiply the conditional bound P(e closed|rest)≤ε by the indicator that F\{e} is closed and integrate. Iterate. The same argument works for vertices.

We recall the elementary planar rectangle alternative. Failure of an open bottom-to-top bond crossing of [0,w]×[0,h] produces a closed dual left-to-right crossing; failure of a horizontal crossing produces a closed dual vertical crossing. For sites, the blocker is instead a closed star-connected path, where star adjacency permits diagonal lattice steps. One way to obtain the blocker is to explore all open vertices accessible from the chosen entering boundary and trace their interface with the inaccessible vertices. If no crossing reaches the opposite boundary, an interface runs between the two lateral boundaries. In the bond case its successive crossed primal edges are closed. In the site case the adjacent inaccessible sites are closed and star-adjacent. Removing loops gives a self-avoiding blocker. This is a deterministic planar alternative and imposes no probabilistic symmetry or independence.

For w,h≥2, a blocker has at least min(w,h)−1 distinct closed coordinates, a deliberately conservative bound allowing either boundary convention. There are at most 2(w+h+2) possible boundary starting locations. A self-avoiding dual path has at most four first-edge choices and at most three subsequent choices; a star path has at most eight first-step choices and at most seven subsequent choices. Accordingly, for d=3 in the bond case and d=7 in the site case, the number of possible length-ℓ blockers is bounded by 32(w+h+2)d^ℓ. Here length counts edges for bonds and vertices for sites; the constant covers the first step and both boundary orientations. Together with (4), a union bound gives, for either requested crossing,

P(crossing fails) ≤ 32(w+h+2) r^(min(w,h)−1)/(1−r),   (5)

where r=dε<1. The estimate may exceed one for small rectangles, which causes no problem.

For R_k, w=2^k and h=3·2^k; for S_k, w=h=2^(k+1). Thus (5) is bounded by a constant, depending only on q and the model, times 2^k r^(2^k−1). The series converges, for example by its successive-term ratio tending to zero. Corollary 4 proves almost-sure percolation in the first quadrant.

Exactly the same counting and geometric argument works in every reflected coordinate quadrant and every lattice translate. It does not use reflection or translation invariance of the probability law, only the uniform conditional bound on every coordinate. There are countably many such translated quadrants, so all percolate on one event of probability one.

Finally let H={ (x,y): ax+by≥c }, where (a,b)≠(0,0), be any affine half-plane. Choose a lattice point z strictly inside H. Choose signs s_x,s_y with a s_x≥0 and b s_y≥0. The quadrant

z + { (s_x m,s_y n): m,n are nonnegative integers }

is contained in H. On the common probability-one event it has an infinite open cluster. This proves the simultaneous conclusion, including open half-planes by using a strictly interior z. ∎

Theorem 5 is an elementary Peierls bound, not an optimal threshold assertion. The target only gives strictly positive conditional opening probabilities, possibly with no uniform lower bound at all. Even uniform finite energy permits a lower bound far below these thresholds. Almost-sure whole-plane percolation does not itself supply the required conditional bound. Hence this theorem does not settle the target.

## 6. Why the modern non-coexistence theorem does not finish the proof

For translation-invariant ergodic bond laws with finitely many infinite whole-plane clusters, [KK, Theorem 1.2] gives three possible half-plane outcomes: a unique primal infinite cluster alone, a unique dual infinite cluster alone, or no infinite cluster of either kind. Its finite-energy theorem uses uniform finite energy as defined by that paper; the finite-number theorem is stated without energy. Its Lemma 2.3 gives half-plane uniqueness and boundary touching, conditional on existence. Timár [T] also addresses non-coexistence, not the creation of a primal half-plane cluster from a primal whole-plane one.

Even granting, in an applicable model, that the whole-plane dual does not percolate, these statements still leave the third outcome. They cannot establish the missing positivity in (1). The uniform spanning tree, discussed in [KK], illustrates the logical distinction between whole-plane connectivity and half-plane connectivity, but it lacks finite energy and is not an admissible target counterexample. No conversion of a site coexistence construction into an associated bond counterexample is asserted.

**Exact unresolved implication.** From only the target's invariance, finite energy, positive association and almost-sure whole-plane percolation, prove P(E_H)=1 for each specified H, or construct a law satisfying every hypothesis that violates this conclusion. The confinement, surgery, duality, strong-density and summable-crossing routes above do neither.
