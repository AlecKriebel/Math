# Independent mathematical audit of half plane percolation partial results

Problem 10000034 / AMR-099-0034, catalog rank 874. Review date: 2026-10-06 UTC.

## Decision

**ACCEPT the frozen packet as a correctly scoped collection of partial results. Retain UNSOLVED 5/5.** No proof of the target implication, admissible target counterexample, verified prior resolution, or novelty claim is accepted. No mathematical correction to the author packet is required. The independent derivations below expand boundary, counting, domination, and probability-one details; they do not add a sixth research approach.

The reviewed author archive has 16,900 bytes and SHA-256 `3e828d578c7fa15dd5614270e0dddc9635fb922f51da06af5351d47349717605`. Its external manifest has 1,435 bytes and SHA-256 `a6ea64bbfef8a800cbf4855f3dd7edbf1fde6c648ccb8ac946f7e8f90cda8b39`. All seven members match the external inventory and the corresponding author files. These are data-only inventory checks, not a mathematical verifier. The unchanged original remains the accepted author deliverable.

## Target and source controls

The complete catalog and problem record ask about translation-invariant percolation on the nearest-neighbor square lattice, finite energy, positive association, and almost-sure whole-plane percolation. The catalog wording does not select site or bond percolation. The historical source's Open Problem 8.5 uses the word invariant; its later Definition 8.9 specifies bond laws invariant under every graph automorphism. The packet accurately flags this difference and does not establish equivalence of the two formulations. Its bond and site statements are individually labeled.

For this audit, ordinary finite energy means that the full one-coordinate conditional probability lies strictly between 0 and 1 almost surely. A deterministic bound away from both endpoints is uniform finite energy. A lower opening bound near 1 is substantially stronger still. None may be substituted for another. Only lower insertion probabilities are needed for the retained finite-path argument and high-density theorem; upper bounds are not covertly used.

Positive association means the inequality for all increasing events, or equivalently increasing bounded functions. It is not the finite-volume lattice condition, conditional association after an exploration, a domain Markov property, or association of arbitrary ergodic components. Full translation ergodicity, one-direction ergodicity, rotation invariance, reflection invariance, and mixing are also separate assumptions. The retained arguments do not smuggle any of these into the target.

The source passages and modern primary theorem statements were inspected in full-text sources, not only abstracts. The source review records exactly what was inspected. External uniqueness and non-coexistence theorems are cited as external theorems; this audit does not purport to re-certify their entire papers.

## Fixed half plane existence and its quantifiers

Fix a nonzero real normal vector a and a threshold c, and let H be either {v in Z²: a·v >= c} or the analogous strict half-plane. For each z in Z², H and H+z differ only in threshold and are therefore nested. Monotonicity of existence of an infinite open component under domain inclusion makes E_H and E_(H+z) nested. Translation invariance gives equal probabilities, so their symmetric difference has probability zero.

The event E* = intersection over z in Z² of E_(H+z) is measurable. It contains the same configurations after any lattice translation, because translation permutes the indexing set. Since there are countably many z and z=0 is included, P(E* symmetric-difference E_H)=0. Thus the author's invariant representative is correct for every prescribed real normal, including irrational slope. Full-group ergodicity makes its probability 0 or 1; no horizontal ergodicity is required. This argument alone provides no positivity.

The equal mixture of independent laws with parameters 1/10 and 9/10 is a valid control. Take a fair selector and independent uniform variables; the opening indicators can all be made increasing functions of these independent inputs. Product association therefore proves association of the mixture. Conditional opening probabilities are conditional averages of the two selected parameters, and hence lie between 1/10 and 9/10. For the lower parameter, a fixed root has at most 4·3^(n-1) self-avoiding paths of n edges. Their total open probability is at most 4·3^(n-1)·10^(-n), which tends to zero. Countability of roots rules out whole-plane percolation. For the upper parameter, the accepted high-density theorem below gives half-plane percolation. Hence P(E_H)=1/2 for the mixture. Its whole-plane percolation probability is also 1/2, so it does not satisfy the almost-sure premise of the target.

The fixed-H null set in this lemma may depend on the direction. The lemma does not authorize intersecting uncountably many probability-one events. The strong-density theorem addresses that issue separately by a countable family of translated coordinate quadrants.

## Root survival and the confinement gap

For a root o in H, reaching the boundary of o+[-n,n]² using an open path inside that box and H is a decreasing sequence of events in n. A path to the next boundary can be stopped at its first encounter with the preceding boundary. If all these events occur, the finitely branching tree of self-avoiding finite open paths from o has arbitrarily deep levels and therefore an infinite ray. Continuity from above proves the author's survival identity.

E_H is the countable union of root-survival events. Consequently it has positive probability exactly when at least one root has positive survival probability. This is a positivity statement, not a claim that every root belongs to an infinite cluster almost surely.

For H_m={y>=-m}, the array a_(m,n) increases in m and decreases in n. Once m>=n, the box used for a_(m,n) lies inside H_m. Therefore first taking m to infinity and then n gives whole-plane root survival. First taking n to infinity and then m gives the probability that the root survives inside at least one fixed H_m. Both equalities are valid, but an equality between the two iterated limits has not been established. The array 1_{m>=n} has the stated opposite iterated limits, so monotonicity alone is inadequate. This deterministic control is not a spatial percolation counterexample.

Under almost-sure uniqueness of the infinite whole-plane cluster, the event that 0 and x both belong to an infinite cluster entails 0 connected to x. Association and translation invariance then give P(0 connected to x)>=theta², where theta=P(0 connected to infinity). Almost-sure whole-plane percolation and countability imply theta>0. Without uniqueness the first implication need not hold, and the packet explicitly supplies that hypothesis or invokes the classical Burton–Keane theorem under its usual invariant finite-energy setting.

Finite boxes exhaust the event 0 connected to x for each fixed x. The selected box may depend on x. Neither this exhaustion nor the two-point bound yields uniform confinement or summable crossing errors as x recedes. The packet accurately leaves that implication unproved.

## Finite path transfer and its precise limitation

Let F={e_1,...,e_m} denote distinct coordinates on a fixed connector. If B specifies that e_1,...,e_(j-1) are open and P(B)>0, then B is measurable with respect to all coordinates other than e_j. Writing p_j for the full conditional opening probability gives

P(B and e_j open)=E[1_B p_j]>0.

The strict inequality follows because p_j>0 almost surely. Induction proves P(F open)>0 without a uniform bound. If p_j>=q deterministically almost surely, the same calculation proves P(F open)>=q^m.

If a root v survives in H with positive probability, the intersection of this increasing event with the increasing all-open connector event has probability at least their product by association. Connectivity of H provides the fixed connector from any prescribed o to v. On that intersection o survives in H. This proves the author's Lemma 2 exactly as stated.

There is no uniform estimate for a sequence of longer connectors under qualitative finite energy. Even the bound q^m can vanish as m grows. More fundamentally, connecting into a whole-plane infinite cluster does not confine the rest of a ray to H. Thus the lemma transfers already-established half-plane positivity between roots; it does not establish that positivity.

## Association does not imply conditional association

Let A,B be independent fair bits and Y=(A,B,A or B). Conditional on Y, independently output X_i=1 with probability 1/10+(4/5)Y_i. One realization is X_i=1_{V_i>=9/10-(4/5)Y_i} with independent uniform V_i. Every X_i is increasing in the independent inputs A,B,V_1,V_2,V_3. Composition with increasing functions preserves monotonicity, so product association proves association of X.

Every output string has positive probability. Because the ith channel noise is independent of all other outputs and the hidden input, conditional opening given the other outputs equals

1/10+(4/5)P(Y_i=1 | the other outputs),

which lies in [1/10,9/10]. Thus a uniform energy bound does not repair the conditional-association failure.

Direct expansion of the four equally likely hidden strings gives the following authored probability calculation, in order 000,001,010,011,100,101,110,111:

(187,63,43,207,43,207,27,223)/1000.

The entries sum to 1. For u=101 and v=011, their meet and join are 001 and 111. The lattice-condition products are 63·223/10^6=14049/10^6 and 207²/10^6=42849/10^6, in the wrong order. Moreover P(X_3=1)=7/10, P(X_1=X_2=1 | X_3=1)=223/700, and each conditional marginal is 43/70. The conditional covariance is therefore -72/1225. This verifies the exact numbers and the conditional counterexample.

An auxiliary exact-rational enumeration independently checked all 20 upper sets of the three-bit cube and all 400 ordered pairs: every unconditional covariance was nonnegative. This is an arithmetic cross-check only; the increasing-image proof establishes association. No finite calculation is offered as a proof of an infinite-lattice theorem. The example is not an admissible target counterexample.

## Rectangle ladder and summability

Put a=2^k. Then R_k=[0,a]×[a,4a], S_k=[0,2a]×[2a,4a], and R_(k+1)=[0,2a]×[2a,8a]. Stop the R_k vertical crossing between its last suitable visit to height 2a and its first subsequent visit to height 4a; this yields a vertical subcrossing of [0,a]×[2a,4a]. A horizontal S_k crossing has a subcrossing from x=0 to x=a inside the same overlap. Two such nearest-neighbor crossings of a lattice rectangle intersect at a vertex by planar separation. The R_(k+1) path likewise contains a vertical crossing of S_k and so intersects its horizontal path.

This intersection is an open connection for bonds as well as sites. Nearest-neighbor horizontal and vertical grid segments can cross only at lattice vertices; there is no diagonal crossing without a shared vertex. Consequently each S_k connector joins the selected R_k and R_(k+1) paths. If all these crossings occur for k>=K, their union is a connected open set reaching unbounded heights, hence infinite.

Summability of all crossing-failure probabilities implies that only finitely many failures occur almost surely by the first Borel–Cantelli lemma. Independence, association, stationarity, and energy are unnecessary. The random last failure determines K. The lemma still works when the lower finitely many rectangles fail.

For the product formulation, finite intersections of increasing events remain increasing, so repeated association gives the finite product inequality. Continuity from above passes to the infinite intersection. Positive individual probabilities plus summable defects make the product strictly positive: eventually each probability is at least 1/2 and -log p<=2(1-p). A constant bound p>=c<1 alone does not produce a positive infinite-product lower bound. No estimate of this required strength has been deduced from the target assumptions.

## Conditional bounds and independent domination

This section checks the quantitative step in the existing high-density approach, rather than proposing a new target-solving route.

Suppose a law on a countable set of binary coordinates satisfies P(X_e=1 | all other coordinates)>=q almost surely for each e. For a finite set F and e in F, the event that F without e is closed is measurable with respect to the other coordinates. Conditioning and integrating yield

P(F closed)<= (1-q) P(F without e closed).

Iteration gives P(F closed)<=(1-q)^|F|. No conditional FKG assertion is involved. The same argument with open coordinates gives the lower all-open bound. Distinctness matters: counting a coordinate twice would not justify squaring its factor.

For completeness, the bound also gives stochastic domination of independent Bernoulli(q) variables. Enumerate the coordinates as e_1,e_2,... . The tower property gives P(X_(e_i)=1 | X_(e_1),...,X_(e_(i-1)))>=q on every positive-probability past string. Set this conditional probability equal to q on zero-probability past strings. Using independent uniforms U_i, recursively set X_(e_i)=1_{U_i<=p_i(past)} and Z_(e_i)=1_{U_i<=q}. Induction verifies the exact finite-dimensional laws of X, hence its full countable-coordinate law, while X>=Z coordinatewise and Z is independent Bernoulli(q). This establishes the domination rather than inferring it from large one-coordinate marginals. The author's direct blocker proof needs only the finite closed-coordinate bound, not this extra coupling construction.

Neither ordinary finite energy nor a lower bound merely greater than zero supplies the large numerical q used next. Association and high marginal density alone do not supply these conditional bounds.

## Planar blockers and explicit counting constants

Take the vertex rectangle R={0,...,w}×{0,...,h}, with w,h>=2 and all nearest-neighbor edges between its vertices. In the bond case, use a split-boundary dual: ordinary square faces are dual vertices, and each exposed edge on a specified lateral boundary gets its own exterior dual endpoint. These exterior endpoints can be placed at half-integer coordinates immediately outside the rectangle. A missing bottom-to-top primal crossing has a left-to-right dual path whose every edge crosses a closed primal edge. Horizontal failure has the transposed alternative. One can obtain this by taking the edge boundary of vertices reachable from the entire entering side, with that side wired for the exploration. Its separating interface joins the lateral sides. Loop erasure preserves those endpoints and leaves distinct dual edges, hence distinct closed primal coordinates.

For a left-to-right blocker, the exterior x coordinates are -1/2 and w+1/2; its edge count is at least w+1. The vertical version has at least h+1 edges. At most h starting locations are needed on one left side and at most w on one bottom side. Even allowing either side and either orientation, the number of possible starting locations is at most 2(w+h+2), the deliberately loose author bound. The split-boundary graph has maximum degree four; no unbounded-degree exterior face is used in this count. Starting at any chosen vertex, the number of self-avoiding paths of l>=1 edges is at most 4·3^(l-1). This follows from at most four first choices and at most three thereafter, because immediate reversal is forbidden. Further self-avoidance only reduces the count.

In the site case, failure of an open nearest-neighbor bottom-to-top crossing yields a closed left-to-right star path. To see why the blocking sites are closed, attach a virtual open row below the rectangle and explore the open sites connected to it. The upper interface of the explored region runs from the left side to the right side if the top cannot be reached. Each in-rectangle site immediately outside this interface is closed: any open nearest-neighbor site touching the explored set would have been explored. Successive outside sites share a side or a corner, producing a closed star walk; closed bottom sites are handled by the virtual row even when no real entering site is open. Loop erasure gives a self-avoiding closed star path. The transpose gives the other orientation.

A star path crossing from x=0 to x=w has at least w+1 vertices, since one step changes x by at most one; likewise the vertical lower bound is h+1 vertices. Starting at a specified boundary vertex, the number of simple star paths with l vertices is 1 when l=1, and at most 8·7^(l-2) for l>=2. The first step has eight choices; immediate reversal excludes one thereafter. There are at most 2(w+h+2) possible starts when all four rectangle sides are allowed. This count includes corners redundantly, which is harmless.

The preceding sharper bounds imply the common loose estimate used in the packet. Writing d=3 for bonds and d=7 for sites, the number of possible blockers with l closed coordinates is at most 32(w+h+2)d^l. Their coordinate length is at least min(w,h)-1. Both weakenings favor an upper bound. For r=d(1-q)<1, union bounding the finite closed-coordinate estimate over blockers and then extending the sum to all l>=min(w,h)-1 gives

P(a specified crossing fails) <= 32(w+h+2) r^(min(w,h)-1)/(1-r).

Counting the two orientations separately is unnecessary because the stated coefficient already bounds either one, even with all boundary starts included. For sites, l counts vertices, not edges. For bonds it counts dual edges, each in bijection with a distinct closed primal edge. No independence or conditional exploration law has entered the calculation.

The numerical conditions r<1 are exactly q>2/3 for bonds and q>6/7 for sites. These are elementary sufficient bounds, with no sharpness or novelty claim. Nothing in this proof establishes the endpoint cases. For q=1, countability makes every coordinate open almost surely and the conclusion is immediate.

## From exponential blockers to all half planes at once

For R_k, w=2^k and h=3·2^k, so w+h+2<=5·2^k for k>=1. For S_k, w=h=2^(k+1), and the same inequality holds. Both minimum side lengths are at least 2^k. When 0<r<1, each failure probability is therefore at most

160·2^k r^(2^k-1)/(1-r).

The successive-term ratio of 2^k r^(2^k-1) is 2r^(2^k), which tends to zero. Their sum is finite. The rectangle ladder and Borel–Cantelli yield almost-sure percolation in the first quadrant.

Reflecting and translating the *geometric construction* produces the same bounds for every Q_(z,s)=z+{(s_1 m,s_2 n): m,n>=0 integers}, where z in Z² and each s_i is either sign. The probability law need not be invariant under those operations: its same deterministic conditional bound is available on every coordinate of every image. There are countably many such quadrants. Thus their simultaneous percolation event Omega_0 is measurable and has probability one.

For any nonzero real pair (a,b) and c, there exists a lattice point z with az_1+bz_2>c: move far enough along a coordinate with nonzero coefficient. Choose each sign s_i so that its coefficient times s_i is nonnegative, choosing either sign for a zero coefficient. Every vertex of Q_(z,s) then satisfies ax+by>=az_1+bz_2>c. Convexity of the half-plane also places the nearest-neighbor segments between such vertices inside it. Consequently this quadrant lies in both the appropriate open and closed affine half-planes.

On the *single* event Omega_0, this deterministic argument works for every real (a,b,c), without another probabilistic intersection. All Euclidean half-planes therefore percolate simultaneously. No measurability assumption about an uncountable intersection is needed to state the conclusion: it holds outside the measurable null complement of Omega_0. This verifies the strongest quantifier in Theorem 5.

## Modern literature does not close the target gap

Klausen–Kravitz's stated half-plane trichotomy includes absence of infinite clusters in both primal and dual half-planes. The finite-number formulation is for translation-invariant ergodic bond laws; the separate energy formulation uses uniform finite energy. The inspected uniqueness and shift results do not create an infinite half-plane cluster. Timár's square-lattice statement is also non-coexistence. Even if some other applicable theorem eliminates whole-plane dual percolation, these statements do not remove the neither-survives alternative. This is a direct logical limitation, not an objection to those theorems.

The uniform spanning tree lacks finite energy. Häggström–Mester's finite-energy coexistence examples do not establish the missing association hypothesis. The Glazman–Harel–Zelesko theorem assumes tail triviality and stochastic domination of open sites by closed sites, in addition to association. None supplies the target implication under only the stated assumptions. Detailed citations and inspection limits appear in SOURCE_REVIEW.md.

## Final acceptance boundary

Accepted: the invariant representative, fixed-root formulation and limit-order obstruction, unique-cluster two-point bound with its explicit hypothesis, fixed-path positivity transfer, the finite associated but conditionally non-associated example, deterministic rectangle gluing, summable-failure and FKG-product criteria, and the high-density simultaneous all-half-plane theorem.

Not established: positivity of half-plane survival from the target's four qualitative premises; reduction to associated ergodic components; arbitrary-slope use of a theorem stated only for axis-aligned or rational-slope half-planes; target-level summability or domination; a target counterexample; global current openness; a complete solution; novelty or priority.

The five recorded approaches remain exhausted. This audit changes neither that count nor the UNSOLVED disposition. No correction patch or corrected derivative is necessary. The original files and freeze are preserved byte-for-byte. No publication was performed.
