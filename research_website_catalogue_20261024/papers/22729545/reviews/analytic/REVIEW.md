# Independent analytic review — Zenodo 22729545

**Manuscript:** *Raw Strongly Tree-Child Level-2 Species Networks from Metric Genealogy Laws under the NMSC: Signed pair co-occupancy, rooted graph reconstruction, and demographic fibers*, Alec Kriebel, v1.0.0, 5 September 2026.

**Verdict:** No mathematical defect identified in the core metric-genealogy classification on the manuscript's stated domain. I independently reconstructed the structural and numerical inverse, including the longer incoming-arm argument and its dependence on level two. The fresh exact checks support the argument at their declared finite scopes. The direct-sequence and finite-locus consequences depend on the separate companion theorem; this review checked that import's assumptions and statements, not its entire proof.

This is an AI mathematical review, not human peer review, a formal proof certificate, a novelty certificate, or an empirical validation of the biological model. No archived or parallel reviewer verdict was read before reaching this verdict. No source repair, publication, website, spreadsheet, Git, Zenodo, or outreach action was performed.

## 1. Precisely bound materials

Fresh primary record: [Zenodo 22729545](https://zenodo.org/records/22729545), DOI [10.5281/zenodo.22729545](https://doi.org/10.5281/zenodo.22729545). Acquisition receipt is `../../sources/receipt.json`; the receipt timestamps acquisition at 2026-10-25T00:13:15.165078+00:00. This review freshly recomputed the hashes below and read all 21 main-paper pages and all 11 supplement pages. Relevant TeX and mathematical implementation files were inspected directly.

| Published object | SHA256 |
|---|---|
| Main PDF, 21 pages, 173018 bytes | `2b5ddc6da8cf02d084ae034a2d23328f6633b1cb91e6dd809df6cd6863e4e33e` |
| Supplement PDF, 11 pages, 101991 bytes | `9bfb1431b2cd84a000ba820ef30e18e3e10b4d83475380066a0b042c80062560` |
| Source ZIP | `61a605db1ad090498fb26e26a63768c0aad4a1ea5ce2849c62b865a45feb2da8` |
| Reproducibility ZIP | `90ea0c85320a110d0766956e35739cd165adadda7a5b67dab491f9aad6aa89be` |

The complete source receipts, archive hashes and manuscript hashes remain separate from generated review evidence. The full published replay independently checked its 64-file inventory and manifest SHA256 `82e22e094ba8b13a1ec030167bfaba42a9818b7fcbc4ac306d883f16e55060fe` before executing code in a temporary copy.

## 2. Exact claim and essential assumptions

The principal observation is the complete normalized **rooted, labelled metric-genealogy probability law**. Population locations, reticulation routes and historical routing tags are not observed. The conclusion is equality of a specified raw-presentation quotient, not unique recovery of every biological graph and parameter.

The domain fixes finite taxon and sampled-label sets `(X,S)` and a known surjective sampling map `s:S→X`. It consists of finite rooted binary temporal species networks, with distinct raw reticulation parents, positive edge durations, positive finite piecewise-constant Kingman pair rates, and strictly interior inheritance probabilities. Each extant lineage routes independently. Every taxon is sampled. The root is followed by a single ancestral population with a finite rate word and a final positive constant-rate epoch extending indefinitely, so complete coalescence occurs almost surely.

Two graph restrictions are material: the paper's explicitly defined **strongly tree-child** class, and at most two reticulations in each undirected blob. The strong condition is on the standard semi-directed reduction, equivalently its stated ordinary-incidence tail predicate; it is stronger than merely accepting any supplied rooted tree-child orientation. The graph proof uses the resulting rooted tree-child witnesses. The five-core/twelve-repair enumeration uses the strong predicate explicitly.

Every distinct internal biological event, including the root join, has a distinct absolute age. This does not prohibit coincident demographic changes. It prohibits cancellation of opposite signed biological jumps at one age. Equal positive rates, repeated exponential exponents and inheritance one-half remain inside the domain.

Theorem 1.1 asserts equality of genealogy laws iff equivalence under Q1–Q8: presentation subdivisions/factorizations, equal-rate epoch merger, sample-unary corridors, parent exchange, bi-unary sister reversal with the **entire** donor rate word transferred, label-preserving isomorphism, and hidden-clock unary-fan replacement preserving two typed outlet weights. Theorem 7.3 states that the **indexed collection of all** marginal laws on at most three sampled labels already determines this quotient. It neither claims one triple suffices nor proves three is minimal.

## 3. Reconstruction of the analytic mechanism

### 3.1 Current co-occupancy is observable without historical routes

At a cut inside a common boundary-free chamber, unnormalized pair survival has the form

`S(t+u) = p_sep(t) + Σ_e p_e(t) exp(-λ_e u)`.

Two supplied finite presentations with equal laws have the same germ outside the union of their finitely many boundaries. Finite exponential functions are entire and analytically unique. Freezing the current population arrangement is only a device to extend this local germ; it does not assert the real process never encounters later boundaries. Positivity of every λ separates the constant term from all co-occupied terms. Consequently `q_ab(t)=S(t)−lim_{u→∞}G_t(u)` is determined. One-sided limits determine its jumps even though the original boundary list is latent.

Repeated positive rates combine coefficients but cannot hide the zero exponent. A zero-rate population would defeat this argument, which is why positivity is essential. Conditioning incorrectly on pair survival would change the jump amplitudes; the manuscript consistently uses unnormalized masses in the inverse.

For three labels, the density of first merger `ab` at offset `v` and no second merger during `w` is a sum of an `ab|z` term `p λ exp(-λv)` and an all-together term `r λ exp(-3λv)exp(-λw)`. Extending the germ, sending `w` to infinity and integrating over `v` selects exactly the current `ab|z` mass. This establishes the particular current grouping used later. It does not manufacture a projector onto an arbitrary past routing history. The supplement explicitly gives a counterexample to such a historical projector.

### 3.2 Signed jumps recover the chronological descendant-cluster poset

A tree join can only add co-occupied surviving pair mass. Its strictly positive support is the set of distinct pairs crossing its two child clusters, including the case of overlapping clusters. Independent routing and finite no-merger survival make every compatible crossing strictly positive. At a reticulation, the negative jump equals `−2γ(1−γ)` times the surviving pair mass in its child population. Incoming arms start at that boundary and contain no exterior lineage already waiting there, so there is no compensating gain. Its negative support is the full clique on the descendant sampled-label cluster whenever that cluster has at least two members.

Demographic changes do not relocate blocks and hence do not jump this scalar. Distinct biological ages isolate the event type and support. This is a pointwise positivity argument, not a generic non-cancellation argument.

Every vertex has a tree-only descendant witness. An incomparable vertex cannot reach that witness, because any path entering its indegree-one suffix must pass through its start. Thus non-nested clusters signal incomparability, while containment forces comparability. Equal clusters can occur along an ancestor chain and are ordered by the observed distinct ages. A tree vertex has at least two descendant taxa, so its positive support is never empty. An unexposed reticulation must lie immediately above a singly sampled terminal taxon; its two incoming incidences remain when its hidden clock is contracted into that leaf. The known taxon sampling map prevents multiply sampled leaves from being confused with these hidden singleton heads.

The imported cluster-comparability fact is exactly the statement in Hellmuth–Schaller–Stadler, Lemma 33 and Corollary 13, checked on the [primary publisher article](https://link.springer.com/article/10.1007/s12064-023-00398-w). Its tree-child hypothesis matches the use here. The manuscript also supplies the witness proof rather than relying exclusively on the citation.

### 3.3 Shortcut completion, including the sole ambiguity

Reticulation clusters are distinct. For comparable reticulations, the upper reticulation has a tree-only witness missed by the lower one. If incomparable reticulations had a common descendant, disjoint root prefixes and descendant suffixes would form an undirected cycle through those two reticulations and their first reconvergence. That reconvergence is a third reticulation in the same blob. This contradicts level two. Hence incomparable reticulations have disjoint clusters.

Take the transitive reduction of the recovered reachability poset. Every edge into an ordinary indegree-one vertex is a cover. Every reticulation has its one outgoing cover. A deficient tree tail can therefore have lost only one shortcut, to a reticulation or a contracted singleton head. If its cluster is C and the shortcut head has cluster D, its positive jump graph is the complete graph on C with the clique on `C\D` deleted. When the complement has at least two labels, the universal vertices recover D. If the support is complete, D omits one label. For `|C|≥3`, two possible reticulation heads would have overlapping equal-sized clusters and violate the preceding level-two lemma.

For `|C|=2`, the labels must be distinct singly sampled taxa. Same-cluster tree vertices form a chain. Two deficient tails either overfill one head's indegree or give the bottom tree vertex two reticulation children. Thus the residual ambiguity is exactly one pendant two-terminal sister triangle, with either terminal as recipient. The proof correctly distinguishes this from a singleton terminal with an outside parent that is already a cover edge; no pendant-module assumption is silently imposed on that case.

Because this argument uses the global labelled vertex poset, arbitrary side-port words and nested pendant decorations are covered by the proof itself. The finite catalogue is not used as an unjustified induction over all decorated graphs.

### 3.4 Numerical recovery is attached to the already recovered graph

An ordinary exposed population has a tree-only descendant witness a whose surviving lineage is deterministically there. Selecting b that can reach it gives `λ=f_ab/q_ab`. This identifies all unequal rate changes on that incidence, including the ancestral word. An ordinary singleton terminal population has no coalescence information.

For a reticulation with parent ages `a1<a2`, choose a tree-only descendant witness a below it and a tree-only ordinary-side witness z of the earlier parent. Their paths cannot meet before a1, and the later arm remains isolated until a2. Hence `q_az(a1+)=γ` recovers the oriented earlier-parent weight. This works for unexposed reticulations as well; their weight is not lost with their hidden clock.

For an exposed reticulation at h, choose a second descendant b. The observed triple current-grouping mass `q3=q_ab|z(h−)>0` is the relevant all-three-unmerged child-pair mass. For `h<t<a1`, the density of first merger ab at t and second merger `(ab)z` at `a1+u` is

`D(t,u)=q3 γ² λ1(t) exp(−∫_h^t λ1) λ_o exp(−λ_o u)`.

Only the earlier arm can contribute before a2. The two first arms have no interior side entry. Integrating this recovered first-event density gives its survival A1 and hence `λ1=g1/A1`. The pair density then determines the second arm's first-event density and rate in the same manner. The denominators remain strictly positive at every finite time. No rate-difference or `(2γ−1)` denominator appears.

The longer second arm is the subtle part. For a reticulation without an ancestral reticulation in its blob, the earlier-route witness follows a known ordinary chain until a2. Its initial co-occupied mass is the **entire** observed mass at a1 minus the known isolated-arm mass, including bypass entrants. At later tree joins, the complete observed positive jump is added. No off-chain reticulation can enter an already existing ordinary population. This computes the earlier-route contribution q1; `q2=q_ab−q1>0` then gives `λ2=−q2′/q2`.

If a reticulation has an ancestral reticulation in the same level-two blob, it is the lower sink. Its outgoing child edge is a bridge: otherwise a path leaving its descendant set would create a third reticulation in the blob. Thus its descendant lineages cannot bypass it. Its known both-earlier-route mass is propagated through already recovered ancestral reticulation parameters, processing ancestors before descendants. Original split assignments cannot rejoin while one block remains on the isolated later arm. Subtracting the computed q1 again isolates q2. This resolves physical arm linkage without treating unknown route-conditioned quantities as observations or using a circular parameter solve.

### 3.5 Quotient soundness and fibers

A singleton fan has no Kingman event before first exposure and therefore retains just its two typed exit weights. Tree-only witnesses at its two parent vertices identify those weights; its internal reticulation time and unary demographic words remain invisible. Distinct maximal interiors cannot overlap for different labels without enabling pair co-occupancy. The hidden-clock example is strictly inside the model class, so Q8 is necessary.

For a bi-unary sister triangle, the local density is `γ λ_D(a+u)exp(−Λ_D(u))`. Its marked kernel is preserved by reversal with the same joining weight and the entire exposed donor word, including every unequal breakpoint. Transferring only an integrated hazard or one constant rate would not preserve the metric law. If a sister side is pair exposed, independent splitting creates a strictly positive separated atom in its local frozen survival, which a single positive-rate Kingman population cannot reproduce. The global signed-support proof supplies observability without assuming a hidden conditioning event.

The canonical normalization is a representation of the declared equivalence class; a compound response macro need not itself select a unique biological realization. The proof does not equate a minimal linear realization with a species graph. The demographic conclusions are correspondingly precise: every pair-exposed population word is retained on its recovered incidence modulo Q6 transfer; singleton words and hidden unary reticulation clocks are not. Two samples from a terminal taxon are necessary and sufficient for its terminal rate word to be observable.

The three-label conclusion is consistent across witnesses: all pair laws first recover one global chronological graph on the fixed label set, then graph-selected pairs/triples recover its parameters. It is not an unsupported gluing of separately inferred triple graphs.

## 4. Primary imports and claimed scope

The primary companion [Zenodo 22729537](https://doi.org/10.5281/zenodo.22729537) was checked at the model, principal-class, direct-sequence classification and finite-locus hierarchy statements. Its freshly acquired main PDF SHA256 is `734dd6701b62bb913ae1b7c0d48361dc8fdb94128173c4882a7d2bfc59319304`. Its principal class requires at least two sampled labels; contemporaneous labelled sampling; known, nonrecombining locus boundaries; independent loci; and one shared irreducible stationary reversible finite-state substitution generator. Repeated eigenvalues and some zero individual conductances are permitted while irreducibility is retained.

The B-paper's sequence corollary is explicitly under those assumptions. Its claim is equality of all **indexed** locus-length laws iff equality of stationary distribution, trace-normalized generator, and this normalized NMSC quotient. The physical time/rate conversion remains a scale ambiguity. The finite-locus consequence is restricted to each fixed finite union of compact semianalytic finite-presentation charts; it is non-effective and gives no practical sequence-length bound. No additional universal locus bound with unbounded epoch count is claimed here.

This review does not independently re-prove the entire companion paper. Accordingly the metric-genealogy theorem is the strongest self-contained result supported by this review; the two sequence consequences remain explicitly dependent on that imported result. The other cited topology and introgression papers supply context, not a hidden classification theorem used to establish the present inverse. In particular, simultaneous bidirectional-introgression switching and direct-substitution varieties are not imported as quotient moves. A novelty comparison with all those works was not completed or certified.

## 5. Fresh computational evidence and adverse controls

The supplied public verifier ran against the fresh extracted archive and recomputed all requested outputs in a temporary copy. Python 3.12.14 with SymPy 1.14.0, mpmath 1.3.0 and NetworkX 3.2.1 was used. Results are in `published_replay.json` and `published_replay.log`:

- 96 exact raw-model numerical identities passed.
- Minimum-core signed supports: 628 rows, no cross-core collisions, and the two declared Q6 comparisons passed.
- Additional-port supports: 504 rows, no nonisomorphic collisions in the declared finite domain passed.
- Independent published numerical formulas, including bypass/ancestral propagation and rejected wrong formulas, passed.
- Worked inverse: 12 symbolic identities and four rejected wrong formulas passed.
- The finite-marginal literal-cylinder semantic certificate passed.
- Canonical suite: 90 exact tests, including 13 exposure-loss tests, passed.
- Executable mutations: 57 rejected records in 56 conceptual groups passed.

A separate replay of the published primitive theta-orientation enumerator derived five core orbits, twelve segment-indexed minimal repairs and eight role-preserving repair orbits. The complete source of that enumerator was inspected, including degree predicates, ordinary subdivision suppression, exact multigraph isomorphism and the path-length-three bound. That standalone replay used NetworkX 3.2.1, not the optional Tier-0 environment's 3.5 pin; it is not represented as a complete pinned Tier-0 replay. Its fresh result and command log are retained as `published_core_enumeration.jsonl` and `.log`.

I also wrote two independent checks that import no manuscript code, catalogue, saved certificate or reviewer verdict:

1. `independent_graph_checks.py` constructs labelled binary trees on two through four taxa and introduces up to two reticulations by ordered edge subdivisions. It retains a sufficient strong-tree-child subdomain with ordinary root children. Across **3,193 generated presentations** and **19,135 sampling cases**, cluster comparability, distinct/disjoint reticulation clusters, visibility, contracted singleton handling and shortcut recovery passed. There were **23,532 shortcut checks** and **1,152 lower-sink bridge checks**. Sampling includes one per taxon, two per taxon, and each single doubled taxon. Counts are generated presentations, not isomorphism classes; the generation domain is not an exhaustion of arbitrary networks. A deliberately constructed level-three tree-child network has incomparable reticulations with overlapping descendants and puts three reticulations in one blob. That control demonstrates the need for the level restriction.
2. `independent_scalar_checks.py` freshly derives seven symbolic identities for frozen pair/triple grouping, both incoming-arm inverses, ancestral-reticulation propagation, bypass inclusion and the two-epoch donor word. Four wrong formulas are rejected: replacing balanced splitting by one exponential, losing one inheritance factor, omitting bypass mass, and discarding a donor breakpoint.

One initial reviewer-test failure was caused by permitting a multiply sampled terminal leaf to act as a hidden singleton reticulation head. Correcting that test predicate to match the model removed the failure. It was not a manuscript defect. The final code and exact outputs are preserved, with source hashes in their JSON records.

No finite test is treated as proof of the universal classification or analytic continuation. The universal argument is the analytic reconstruction discussed above. The complete optional twelve-job Tier-0 bundle and a byte-identical TeX rebuild were not run; neither is claimed. The published input inventory and source/PDF hashes were verified separately. There was no numerical tolerance used as evidence of exact equality in these checks.

## 6. Strongest supported result and exact remaining gap

**Strongest supported result:** On the fixed, sampled-complete, strict positive, temporally separated binary strongly tree-child level-at-most-two NMSC domain, the indexed collection of all labelled metric-genealogy marginals on at most three sampled lineages determines exactly the Q1–Q8 raw-presentation quotient. It recovers the retained rooted incidences, exposed biological times, inheritance outlet weights and every exposed finite demographic rate word, while preserving the stated bi-unary donor-transfer and unary-clock/demographic ambiguities. Equal positive rates and inheritance one-half do not create an extra fiber.

**Exact gap:** No unresolved mathematical gap was identified in that core proof. This review does not independently discharge the entire external sequence–genealogy/finite-locus companion theorem; those corollaries remain conditional on it. It supplies neither a formal universal proof check nor human specialist peer review or a literature-complete novelty assessment. Its finite computations do not extend the theorem to level three, simultaneous biological events, zero/infinite rates, endpoint inheritance weights, unsampled terminal taxa, unknown sampling maps, correlated routing, recombination, unknown nonreversible substitution or stable inference from finite noisy data.

For a public summary, the central distinction should remain explicit: this is an identifiability theorem from exact probability laws within a specified model class. It does not recover a unique unrestricted species history from ordinary finite sequence data, and it deliberately retains real observational ambiguities.
