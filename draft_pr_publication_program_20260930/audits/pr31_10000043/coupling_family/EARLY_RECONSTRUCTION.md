# Independent early reconstruction — adaptive coupling family

Sealed before reading original checker, results, review, readiness, other agents, or parent conclusions.

UTC: 2026-10-02T00:59:06.052677+00:00
Frozen head stated by assignment: dbe32750f32cd31c9add3aa3311af86f193fc48e.
Claim source read: source_snapshot/PARTIAL.md only.
Literal target/model source retrieved: archived Benjamini notes PDF, pp. 5, 32–33, 75–76. Web retrieval failed; direct HTTPS retrieval succeeded and preserves literal PDF bytes.

## Model and exact hypothesis

The literal Open Problem 9.49 on p. 76 asks: “Let G be an infinite graph with pc(G) = 1 and look on Bernoulli percolation on G × Z. Does any infinite cluster intersects the fibers {v} × Z infinitely often a.s.?” The defaults on p. 5 are simple, countable, locally finite graphs; p. 33 makes graphs infinite and connected unless stated otherwise, defines root-based bond pc and the Cartesian product. Page 32 is independent identically distributed Bernoulli bond percolation. No bounded degree default exists.

Partial §2 precise claim: for a fixed p ∈ [0,1), and infinite connected countable locally finite simple G with homogeneous bond pc(G)=1, almost surely no infinite product cluster has a finite uniform fiber bound. This is weaker than the target; the unsolved case is finite fiber sizes with unbounded supremum. Success for this audit is verifying or falsifying the partial claim and construction, not establishing that target.

## Universal reconstruction

Choose deterministic orders of countable vertices and each finite incident-edge list. Maintain a FIFO queue of accepted vertices; accept x at time 0. Process finite incident-edge lists in those orders. Physical product edges are globally marked on first query and never queried twice. An open proposed new vertex is accepted only while its fiber count is below M; a full-fiber rejection is final for that proposal, but the state remains recorded. Previously accepted endpoints do not consume extra capacity.

For a fixed unordered base edge e={u,v}, every queried horizontal physical edge is (e,n) with an accepted endpoint at height n. Thus all queried heights lie in H_u ∪ H_v, where each H has at most M elements. This deterministic argument includes rejected additions, queries made from both endpoints, revisits, vertical discoveries, and interactions with other reservoirs. At most 2M DISTINCT queries are possible. No assumption bounds the total degree or total number of queries globally.

Reservoirs X_(e,j), 1≤j≤2M, are mutually independent Bernoulli(p); fresh vertical variables and a separate auxiliary Bernoulli(p) U_a for every physical product edge are independent of all reservoirs. On the jth new horizontal query for e use X_(e,j). Adaptivity chooses the next query and slot using only the revealed transcript. The new slot has not appeared in that transcript, hence has Bernoulli(p) law independent of that transcript. Distinct queries receive distinct primitive variables, including across unordered base edges and vertical edges. Independence of a fresh slot need not hold after conditioning on the global uniform-fiber event; no such conditioning is used.

A checkable proof of the *entire* completed edge field: stop after k physical queries (or termination), and fill every unqueried physical edge a with its independent U_a. For any possible finite transcript, the queried outcomes have the same adaptive transition probabilities as ordinary independent bond percolation, and the conditional remaining field is independent Bernoulli(p). Hence the completed finite-stop field has original product law. As k→∞ each fixed physical edge stabilizes: a queried edge uses its assigned variable thereafter, and a never-queried edge always uses U_a. Every finite cylinder therefore converges pointwise to the corresponding cylinder of the final field, preserving its product-law probability. Countability supplies a measurable whole field. This avoids an unsupported statement that a random assignment permutation is automatically harmless.

Y_e=max_j X_(e,j) are independent across e, with common q_M=1−(1−p)^(2M)<1. If a new base vertex is accepted across (e,n), X_(e,j)=1, hence Y_e=1. Induction along the exploration's accepted predecessor tree puts every projection in the Y-component of v0. pc(G)=1 implies that component is finite almost surely for each fixed q_M<1; an infinite cluster with positive probability at q_M would contradict the definition of pc. Accepted size is ≤M times its finite base-component size.

To transfer back to the actual cluster, on the event that C(x) has at most M vertices in every fiber, every accepted vertex lies in C(x), and no *new* C(x) vertex can be rejected due to cap: M already accepted vertices in that fiber plus that new vertex would contradict the event. Every finite open path from x is eventually scanned. Local finiteness ensures each FIFO vertex has finite processing time and finite queue prefix; a common degree bound is unnecessary. Thus accepted=C(x) on that event. Exact-law coupling gives probability zero for infinite uniformly capped C(x). Countable union over x and integers M handles every cluster and every finite uniform bound for the fixed p. It does not assert a simultaneous null-set statement over all real p.

## Boundaries and adversarial predictions

- p=0: empty open edge set, finite singleton clusters, q_M=0. p=1: q_M=1 and pc=1 supplies no finiteness; nevertheless connected product has one cluster with infinite fibers.
- M=0 is outside the algorithm (initial x consumes capacity); every nonempty uniformly bounded cluster is covered by M≥1.
- Unbounded finite degrees preserve the FIFO argument. Infinite local degree invalidates the stated finite incident-list processing argument; this is outside the source hypotheses.
- Disconnected/noncountable/non-Cartesian/site/random-environment/conditioned models are outside the specified claim.
- Reserving 2M is safe. It is not universally sharp at M=1: no vertical new vertex can be accepted, so all accepted heights equal n0 and there is at most one queried edge per base edge. For M≥2, a base cycle with a sufficiently long alternate route permits both endpoint fibers to fill at disjoint height sets, with all crossing edges above e closed; 2M queries can then occur. On a bridge reached through e, endpoint height sets overlap, but this does not justify a general 2M−1 bound.
- A mutation reusing a reservoir slot or forgetting the physical-edge query cache should fail independence or finite-cap accounting. A mutation using a capacity-dependent variable after conditioning on rejection should alter the law. A query-only completion which leaves unqueried edges fixed closed should fail full product law.
- The uniform-bound proposition seems valid under its actual hypotheses. Predicted residual gap remains unbounded finite fibers; no full-target mechanism will be pursued.

## Other partial claims independently noticed

§1 removal of an entire neighboring fiber and finite-set splitting uses local finiteness correctly; infinitely many independent unopened horizontal edges force infinite hits, countably simultaneously. §3 uniqueness argument must condition on the deterministic a.s. existence regime (vertical translation ergodicity gives 0/1 existence); no claim is made at p with no infinite clusters. §4 stretched-tree estimate and inhomogeneous-ray positive product appear valid; neither proves the target. Published-source claims require literal verification later.

Audit completion estimate: 25% (source model and independent reconstruction fixed; code/diff/replays/controls remain). Target-discovery completion estimate: unchanged and uncertified; this audit adds no target theorem.
