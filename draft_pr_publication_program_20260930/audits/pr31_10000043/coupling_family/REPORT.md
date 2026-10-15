# Independent original-stage adversarial audit: adaptive coupling family

**Verdict: PASS_PARTIAL_ONLY. No mandatory mathematical correction found. The full target is unresolved.**

Target: 10000043 / AMR-099-0043, Benjamini Open Problem 9.49. Frozen original head: `dbe32750f32cd31c9add3aa3311af86f193fc48e`. Actual original comparison base: `60292bed09f59236aa192cb17aa138f7b4750e1a`. The exact 70,010-byte comparison has SHA256 `230a722fbfc87eca480197e69d643046fd762435e35e75778a50887af2d9998b` and consists of the 15-file attempt plus the queue-row change. The GitHub metadata base tip is a different commit; this audit uses the actual merge base and verifies the supplied diff byte for byte.

This is an independent AI mathematical audit, not a proof assistant certificate or human review. It establishes validity of the stated partial deduction under its source hypotheses; it does not certify novelty, a complete present-day literature search, or a solution of the original question. It requests no external input and performs no external communication, repository mutation, publication, merge, release, or DOI action.

## 1. Independence, source recovery, and exact scope

The independent reconstruction was fixed at `2026-10-02T00:59:06.052677+00:00`, before reading any original checker, receipt, prior review, readiness file, or parent/sibling conclusions. `EARLY_RECONSTRUCTION.md` has SHA256 `af89b2e954e2999312e5bb24b607681b83dd1974a638ddba6417fd61330008a2`; `EARLY_SEAL.json` preserves the timestamp and source hashes. Only the literal notes and original `PARTIAL.md` informed that reconstruction.

The [archived author notes](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf) were actually retrieved. The web tool could not access the URL; direct HTTPS retrieval succeeded. The recovered PDF is 1,101,523 bytes, SHA256 `aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe`, agreeing with the original source checksum. Pages 5, 32–33, and 75–76 were read. The defaults are simple, countable, locally finite graphs, later infinite and connected, independent identically distributed Bernoulli **bond** percolation, and the **Cartesian** product. They impose no uniform degree bound. Open Problem 9.49 is the infinite-fiber-intersection question with homogeneous base bond critical probability 1.

The exact partial claim is: for each fixed `p∈[0,1)`, on an infinite connected countable locally finite simple base `G` with `pc(G)=1`, almost surely no infinite cluster in `G×Z` has a finite **uniform** upper bound on its fiber intersection sizes. This is not the assertion that all finite fiber intersections are excluded. The target remains unresolved precisely for an infinite cluster whose intersections with every fiber are finite but whose sizes have unbounded supremum over the base.

After sealing, all 15 original files, their actual programs, the old review, and all metadata were read. The reviewed partial is byte-identical to `PARTIAL.md`, SHA256 `2a716868a8d7e2462adf14045212a8e3d8d502312743b7c1d8aa80575b1b479f`. Every postimage in the 16-file diff was checked against the snapshot. `ACTUAL_COMPARISON_RECEIPT.json` independently verifies the complete diff against the actual base and frozen head. No source bytes were edited.

## 2. Universal proof of the adaptive construction

### 2.1 Deterministic physical query bound

Fix an integer `M≥1` and root `x=(v0,n0)`. Choose deterministic incident-edge orders and use a FIFO queue. On acceptance, put a vertex in the queue exactly once. Processing a vertex means scanning its finite incident list; globally cache every queried physical edge. A found-open proposal to a new vertex is rejected only when that fiber already has `M` accepted vertices.

For an unordered base edge `e={u,v}`, every queried horizontal physical edge has some height already accepted in `Fu` or `Fv`. Let `Hu,Hv` be the sets of all accepted heights in the two fibers. Both have cardinality at most `M`, even after the entire exploration. Each horizontal edge above `e` is uniquely determined by its height. Therefore the set of queried physical edges above `e` has cardinality at most `|Hu∪Hv|≤2M`.

This is a deterministic count, independent of probability and of the order in which other reservoirs are used. It includes two-sided discoveries, revisits to an edge from its other endpoint, queries that return to already accepted vertices, open edges whose proposed endpoint is rejected, and interleaved vertical growth. Global physical-edge caching prevents a revisit from assigning a second state to the same edge. No common bound on vertex degree is required.

### 2.2 Fresh variable assignment and the entire product law

Generate independent Bernoulli(`p`) variables `Xe,j`, `1≤j≤2M`, for every unordered base edge, together with fresh independent vertical-query variables. Independently generate an auxiliary Bernoulli(`p`) variable `Ua` for every physical product edge `a`.

At the `j`-th new horizontal query above `e`, assign `Xe,j`. The queried physical edge and the index `j` are functions of the finite revealed transcript. Each primitive label is unused when selected. This gives an injective assignment of queried physical edges to primitive variables: distinct base reservoirs are disjoint, slots inside a reservoir are consumed once, and vertical-query variables are separate. Conditioning on any possible finite transcript, the next unused variable is Bernoulli(`p`) independent of that transcript. Thus every finite transcript has exactly the transition probabilities of ordinary independent product-edge exploration. Selecting an output location adaptively is harmless here because the input variable remains unread; an arbitrary adaptive reuse would not be harmless.

To justify **all** physical edge states, including edges never queried during an infinite exploration, define `Ωk` by stopping after `k` new physical queries (or earlier termination), retaining their assigned states, and assigning `Ua` to every other physical edge. In the ordinary independent model, conditioning on a finite nonanticipating transcript leaves the unqueried field independent Bernoulli(`p`). Its transcript probabilities agree with the reservoir algorithm. Consequently each `Ωk` has the complete original product measure, not merely the same reached-set law.

For each fixed physical edge `a`, `Ωk(a)` stabilizes: if `a` is ever queried it is assigned at a finite index and never reassigned; if it is never queried it always has value `Ua`. Let `Ω∞` be the coordinatewise limit. For a finite cylinder, its indicator stabilizes almost surely because it involves only finitely many coordinates. Bounded convergence preserves the cylinder probability from `Ωk` to `Ω∞`. All finite cylinders therefore have exactly their independent Bernoulli product probabilities. Countability makes the resulting whole-field construction measurable and identifies its law with the original infinite product measure.

This proof handles infinite explorations without assuming that they terminate and without an unsupported assertion about conditioning on an infinite transcript. In particular it does not condition on the event that the actual cluster fits the cap. The auxiliary completion need not be independent of the dominating base field; only the completed physical field's marginal product law and the base field's independent marginal law are required.

### 2.3 Independent domination on the base

Define `Ye=maxj Xe,j`. Different `Ye` are functions of disjoint independent finite reservoirs; hence their joint law is homogeneous independent Bernoulli with parameter

`qM=1−(1−p)^(2M)`.

Unused slots are included in this maximum. For each finite `M` and `p<1`, `qM<1` exactly. Every accepted vertex has an ancestry path from `x`. A horizontal step in that path used an open reservoir slot and hence a `Y`-open base edge. Vertical steps preserve the base vertex. Its projection is therefore contained in the `Y`-component of `v0`.

By the definition of `pc(G)=1`, the probability that the fixed base root is in an infinite `Y`-component at any `qM<1` is zero. The accepted set then has size at most `M` times the size of that finite component. Thus the capped exploration is finite almost surely. This is a deduction from the independent base law, not a finite numerical extrapolation.

### 2.4 Recovering the actual cluster when the cap fits

In the completed physical field, every accepted vertex lies in the actual cluster `C(x)`. On the event that `C(x)` has at most `M` vertices in every fiber, an open proposed **new** vertex of `C(x)` cannot be rejected because a fiber is full: the `M` accepted distinct vertices there and that new vertex would give `M+1` cluster vertices in the same fiber. Proposals to previously accepted vertices add nothing and need no extra capacity.

Every queued vertex is eventually processed. At each finite step the queue prefix is finite, and each of its vertices has a finite incident-edge list by local finiteness. Equivalently, finite-distance balls are finite even without bounded degree. Induction along any finite open path proves that the entire `C(x)` is accepted on the cap-fitting event. It is then finite almost surely by base domination.

The null events are indexed by the countable set of roots and positive integer caps. Their union excludes every infinite uniformly bounded-fiber cluster, even if the uniform bound is chosen after seeing the configuration. A fixed `p` is essential to this formulation: no simultaneous null-set assertion over uncountably many real parameters is claimed.

## 3. Boundaries, sharpness, and exact remaining gap

- At `p=0`, clusters are singletons and `qM=0`. At `p=1`, `qM=1` and the domination argument does not imply finiteness; the connected full product nevertheless has infinite intersection with every fiber. The original endpoints are covered correctly.
- `M=0` is outside the algorithm because the starting vertex is accepted. Every relevant nonempty cluster with a finite uniform bound is covered by an integer `M≥1`.
- Local finiteness supports both finite incident-edge processing and the finite splitting step in the propagation lemma. Arbitrarily large but finite degrees are allowed. Infinite local degrees, noncountable graphs, disconnected graphs, site percolation, non-Cartesian products, dependent or inhomogeneous physical percolation, and conditioning on the global cap event are outside the stated model.
- The `2M` bound is safe. For `M=1`, it is not sharp: no vertical move can accept a new vertex, so every accepted height equals the initial height and a base edge has at most one queried physical edge. This observation does not invalidate the proof or its stated parameter. For every `M≥2`, the general `2M` bound is sharp: a four-cycle with an alternate route allows the two endpoint fibers of one edge to fill at disjoint height intervals of size `M`, and then all `2M` crossing edges are queried closed. The finite positive-probability event embeds in a four-cycle with an infinite ray attached, a base with `pc=1`. Controls execute this construction for `M=2,…,8`, including closed vertical boundary queries.
- A bridge-specific overlap between height sets cannot justify a general reduction to `2M−1`. The executed sharp cases exhaust a reservoir of that smaller length.
- Fixed finite capacities give a common `qM<1`. Allowing unbounded capacities gives edge bounds approaching 1 and may introduce further dependence when capacities are selected from the configuration. The homogeneous statement `pc=1` supplies no contradiction for such an inhomogeneous base field. The original ray example explicitly shows why the direct extension is blocked. This route transfers the central difficulty to an unsupported uniformity statement and remains blocked.

## 4. Other partial claims and source boundaries

The propagation lemma is valid. Reveal the graph with the whole neighboring fiber deleted. Its clusters can be measurably indexed by their least vertex in a fixed countable enumeration. Each revealed cluster that has infinitely many points in the first fiber has infinitely many distinct still-independent Bernoulli(`p`) horizontal edges into the deleted fiber. For `p>0`, infinitely many are open almost surely, simultaneously over all those countably many clusters. If an original cluster hit the first fiber infinitely but the deleted fiber only finitely, deleting that finite intersection leaves finitely many components because only finitely many edges meet it. One remaining component retains infinitely many first-fiber points and is a full cluster of the revealed graph, giving the contradiction. Countably many oriented base edges and finite base paths prove the simultaneous all-cluster dichotomy.

The uniqueness argument is valid when a unique infinite cluster exists almost surely. Vertical translation is mixing: finite cylinder supports become disjoint under sufficiently large vertical shifts, and approximation extends mixing to the product sigma-field. Existence is therefore a zero-one event. Countability yields a vertex with positive infinite-cluster probability; FKG with a fixed finite connecting path propagates positivity to every vertex. The vertical ergodic theorem gives positive density of infinite-cluster vertices in each fiber. Uniqueness identifies them with the one infinite cluster. Countability yields the all-fiber conclusion. No conclusion is needed in the regime with no infinite cluster.

The [published Benjamini–Kozma paper](https://alea.math.cnrs.fr/articles/v10/10-02.pdf) was independently retrieved, with SHA256 `a898970ec7c92cd4cf5e1a766880ee28341cee27cf854e8ccf05dee53bf1295d`. Its journal pp. 15–16 and 22–23 verify the `0,1,∞` classification, Theorem 2's **uniform** finite edge-cut condition, and Lemma 7's direct fiber-intersection conclusion within that proof. The lattice copies in its Theorem 1 construction give base critical probability below 1; that example cannot refute the present target. These are prior results. The old package's arXiv-version lemma numbering and later-literature search are provenance claims, not inputs to this coupling proof; this family does not certify their exhaustive current-literature status.

The stretched binary tree deduction is correct. At original level `n`, there are `2^n` root paths of length `2^(n+1)−2`. Their union bound tends to zero for each `p<1`. The portion before each level is finite, so an infinite root cluster would reach every level. FKG/finite-energy opening of a finite path transfers any other vertex's positive percolation probability to the root. At `p=1` the infinite connected tree percolates, giving `pc=1`. Its `2^(n+1)` edge-disjoint outgoing infinite rays from the finite truncated tree require that many cut edges to make every truncated-tree vertex lie in a finite component. This refutes the uniform-cutset implication, not the original product question.

The inhomogeneous ray deduction is also correct: the displayed failure probabilities sum to `1/2`, so the finite union bound and continuity give probability at least `1/2` that the whole ray is open. Individual edge parameters below 1 do not substitute for a fixed common parameter below 1.

## 5. Actual replay, independent controls, and falsification

The original programs were inspected, copied unchanged into `isolated_original_replay/`, and executed. The author program's 4,996 assertions and the earlier reviewer's 90,170 assertions reproduce byte-identical saved JSON results. `ORIGINAL_REPLAY_RECEIPT.json` contains every copied-file hash, program hashes, return codes, result hashes, complete result payloads, and exact postimage comparisons. Standard output and standard error are retained separately. These finite programs cannot independently prove infinite-volume claims.

`independent_adaptive_controls.py` imports no original or reviewer code. It uses exhaustive adaptive transcript branching, assigning only the primitive variables actually read. It analytically integrates untouched reservoir slots to compute the **joint** dominating-base law, and independently completes unqueried physical edges over all possible tails. Direct full physical-state enumeration gives a separate comparison. All probabilities are exact rational values, with no floating-point tolerance or symbolic library dependency.

The final controls cover ten cases on four-cycle products with a two-height interval and triangle products with a three-height interval. They vary the cap, root, neighbor order, and use `p=2/7` and `p=3/5`. They enumerate 98,304 direct physical configurations in total. Every accepted-set law and every entire completed physical-edge law agrees exactly, every joint `Y` atom has the independent product probability, every cap-consistent actual cluster is recovered, and actual cap rejection occurs in the capped cases. These are different geometries and parameters from the original author toy and earlier path controls.

All seven deliberately broken variants are detected with durable witnesses:

1. Reusing the first slot of a base reservoir produces primitive aliases and a wrong completed physical product law.
2. Sharing one reservoir across different base edges gives physical-law failures and a joint all-open `Y` probability different from the independent product value.
3. Completing unqueried physical edges by setting them closed gives the wrong full product law even where exploration outputs alone can look plausible.
4. Removing the physical-edge query cache assigns conflicting states on repeated physical-edge queries. The numerical `2M` attempt count can still survive, so a count-only check would miss the defect.
5. Using direction-indexed pools while defining `Y` from only the forward pool permits a reverse open crossing across a `Y`-closed edge. The actual executed trace is retained.
6. Conditioning the original product model on the event that the actual root cluster fits cap 1 changes the root vertical edge's open probability from `2/7` to exactly 0. The conditioning event has strictly positive exact probability. This falsifies the prohibited conditioning interpretation, not the submitted nonconditioning proof.
7. Reducing the reservoir length to `2M−1` yields executed exhaustion failures in the sharp controls for every `M=2,…,8`.

The code also executes deterministic exploration prefixes on an infinite locally finite graph with unbounded degrees: spine vertex `n` has `n` pendant leaves. Prefixes process 100, 1,000, and 5,000 queued vertices with no reprocessing, preserving the per-edge bound while observed degrees grow. This checks the intended finite-list mechanism and is explicitly not probabilistic evidence about an all-open event at `p<1`.

The final receipt records **452,621 elementary checks**. This count is a diagnostic execution record, not a level of proof confidence. The finite diagnostics supplement the universal proof in §2. The successful first control version was preserved in `control_runs/v1/` before enhancing the executed mutant witnesses; no failed control attempt was erased. The initial failed web retrieval is recorded in `SOURCE_RETRIEVAL_RECEIPT.json`.

## 6. Required scope and separate repair suggestions

No mathematical source correction is mandatory for §2. The strongest verified result is the uniform finite-fiber exclusion together with the propagation dichotomy. The finite-but-unbounded case remains neither ruled out nor constructed. The attempt ledger stays **2/5**; this verification adds **0** substantive original-target proof attempts. The original `OPEN-TRIAGE` record is a prior literature/status note, not mathematical evidence or a proof attempt.

Optional clarity improvements, separate from the verdict:

- Add the finite-stop/coordinate-limit cylinder argument to the proof's short completion sentence, making the whole infinite edge-field law explicitly checkable.
- If discussing sharpness, qualify it for `M≥2`; `M=1` has the stronger one-query bound. No parameter change is required for validity.
- Replace the frozen note's stale “separate adversarial review is pending” status when assembling an updated publication package, while retaining the original reviewed snapshot unchanged.
- Correct the PR body's statement that all changed files are under the attempt directory: the exact comparison also changes `unsolved_math_prioritization/QUEUE.md`. This is a description-scope mismatch, not a mathematical defect.

Raw source PDFs and whole text extractions are retained locally for reproducibility and ignored from publication; URL/hash receipts preserve their identities. All proof, control, replay, report, and failure-witness artifacts remain inside this family's dedicated folder. `MANIFEST.json` is self-excluding.

Audit completion estimate: **100%** for this family. Original-target discovery remains unresolved; this audit supplies no full-resolution, novelty, formal-certificate, human-review, paper, DOI, or merge inference.
