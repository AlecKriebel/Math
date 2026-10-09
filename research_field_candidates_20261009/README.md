# Candidate research programs with elementary entry points

Prepared for Alec Kriebel, 2026-10-09. ORCID: https://orcid.org/0009-0001-9320-500X

## Status and scope

This is a scouting dossier, not a claim to have invented a field or proved a novel theorem. The goal is a research program understandable from finite examples, capable of sustained growth, and suitable for largely autonomous proof and exact computation. The names below are working descriptions, not assertions of established terminology or originality.

The literature check is preliminary. A missing search result does not establish novelty. Elementary baseline deductions appear in `BASELINE_CHECKS.md`; their originality is explicitly unclaimed. No exhaustive classification or new general theorem is claimed here.

## Selection principles

Prefer a short definition, inexpensive exact examples, checkable positive and negative certificates, an infinite family beyond the first toy case, natural ways to combine objects, and several independent theorem directions. Accessibility concerns the first rung of the ladder, not a promise that advanced work will stay elementary.

An AI can help enumerate finite systems, propose invariants, search for counterexamples, construct proofs, maintain reproducibility, and independently recheck results. Neither sustained progress nor novelty is guaranteed. The human's main role can be choosing which questions matter and learning the resulting mathematics, rather than performing all technical implementation.

## 1. Temporary help in constrained transformations

**Question.** How many otherwise-correct parts must temporarily change to accomplish a small permanent change?

**Model.** Let configurations be valid assignments to a finite set V. A legal move changes one coordinate while preserving validity. For endpoints x,y, let D be the coordinates where they differ. Define h(x,y) as the minimum number of coordinates outside D that are ever changed along a legal path from x to y; set it to infinity if there is no such path. Track the whole family of sufficient helper sets as well as the minimum cardinality.

**Starting example.** Properly color a path by repeating 0,1,2. Exchange two adjacent interior colors. The endpoints of this transformation differ at two vertices, yet the number of required temporary helpers grows with the distance to the nearer end of the path. The exact elementary formula is in the baseline notes. A fourth color removes the helper requirement for this example.

**First project.** Classify helper sets for small paths and trees. Produce legal recoloring sequences for upper bounds and independently verifiable frozen-region arguments for lower bounds. Then compare number ever disturbed, number simultaneously disturbed, distance of disturbance, and total moves.

**Branches.** Spare colors; weighted helpers; common helpers for many tasks; local constraint systems; composition across boundaries; borrowed new coordinates versus temporarily modifying existing ones; helper cooperation and forbidden helper sets.

**Nearby literature.** [Bounded-length recoloring](https://arxiv.org/abs/1404.0337), [Local Mending](https://arxiv.org/abs/2102.08703), and [Minimum Label Path and related problems](https://pages.cs.wisc.edu/~jyc/papers/label-cut.pdf). In the reconfiguration graph, label each edge by the coordinate it changes. Minimum total support is exactly minimum label path; helper count subtracts the mandatory |D|.

**Exact remaining gap.** The abstract optimization principle is established. The possible contribution is a structural theory of helper sets and spare-resource tradeoffs in natural configuration classes. Check whether existing recoloring results already imply the proposed classifications. The helper count itself is not a metric: distinct adjacent configurations have zero helper count.

**Assessment.** Best practical first project: exceptionally elementary examples and exact certificates. Moderate confidence in finding useful research questions; no certified novelty claim.

## 2. Experiments with a guaranteed undo budget

**Question.** How much can an experiment reveal while remaining quickly recoverable at every stage?

**Model.** A deterministic finite machine has hidden states, available buttons, and an output attached to each state/button transition. Its transition/output table is known; its initial state is unknown. An adaptive experiment must identify the initial state. After every transcript prefix, there must exist an adaptive continuation that restores the actual initial state in at most r further actions, for every initial state compatible with that transcript. Recovery uses ordinary available actions, not an extra save/load operation. Full controller memory is allowed in the starting model.

The computational state is a set B of pairs (possible initial state, current state). Recovery succeeds on the diagonal, where every pair has equal coordinates. A one-step recovery recursion chooses an action and requires all possible observation branches to be recoverable with one less step. Identification is then solved while staying inside the recoverable sets.

**First project.** Enumerate three-state machines with two buttons and two transition-output values (6^6 labeled tables before symmetries). Find minimal examples separating eventual restoration, bounded restoration at every prefix, blind recovery, and adaptive recovery. Output complete decision trees and impossibility certificates, not just simulation outcomes.

**Branches.** Limited controller memory; partial identification; multiple devices with shared controls; noisy observations; blind versus adaptive undo; preserving selected properties rather than every state coordinate; tradeoffs between information, experiment duration, and recovery time.

**Nearby literature.** [State identification](https://arxiv.org/abs/1907.11034), [distinguishing and homing sequences in reversible finite-state machines](https://doiserbia.nb.rs/Article.aspx?id=0353-36701903417L), and [testing restorable systems](https://antares.sip.ucm.es/prabanal/research/ictac09extendedversion.pdf). Belief-state planning and bounded-recovery games are additional collision checks.

**Exact remaining gap.** Ordinary identification followed by restoration is weak: in a strongly connected n-state machine, a distinguishing experiment of depth D can be followed by a return path of at most n-1 steps. Unbounded prefix recovery similarly collapses. The bounded frontier and its structural/compositional behavior must carry any contribution. A reset to one known state is not restoration of an unknown initial state.

**Assessment.** Most distinctive conceptual direction among the finalists. Excellent finite laboratory; substantial prior-art risk remains.

## 3. Finite reservoirs for irreversible behavior

**Question.** How much hidden state does a reversible machine need to imitate an irreversible rule for a specified time?

**Model.** Given a finite set X, a map f:X→X, and an integer horizon T≥0, minimize |E| over a finite environment E, a fixed initial environment state e0, and one permutation U of X×E such that

    first_coordinate(U^t(x,e0)) = f^t(x)

for every x and every integer 0≤t≤T. Call the optimum M_f(T). The same U is used at every step. External clocks, resetting, and initially state-dependent environments are not free resources.

**Starting foothold.** If f sends all n states to the same state, then M_f(T)=(n−1)T+1. The independent proof checks account for shifted overlaps of trajectories. This is a baseline deduction with no novelty claim. |E| counts states, not bits; storage in bits is its logarithm rounded up.

**First project.** Solve small functional graphs exactly, then derive formulas or bounds for trees feeding cycles. Determine how transient branching and cycle lengths control growth with T. Ask first whether known dilation constructions already settle the unrestricted version.

**Branches.** Local reversible operations; multiple possible visible rules; speed versus storage; restricted resets; approximate visible trajectories; stochastic systems; composition of reservoirs. Quantum versions are optional advanced branches, not prerequisites.

**Nearby literature.** [Set-theoretic dilation theory](https://arxiv.org/abs/2004.09255), [universal dilation of discrete Markov evolutions](https://arxiv.org/abs/math/0512393), and [time/space bounds for reversible simulation](https://arxiv.org/abs/quant-ph/0101133). Reversible system–environment realizations are established. Finite-horizon and N-dilation literature needs a focused comparison.

**Exact remaining gap.** Establish whether optimal finite environment cardinality, with fixed coordinate observation, has already been characterized. If the general model is an immediate optimization of known constructions, retain only materially different locality or composition constraints. The model alone establishes no physical heat, energy, or thermodynamic law.

**Assessment.** Best bridge toward physics and information while retaining elementary foundations.

## 4. Stable compact descriptions

**Question.** When an object changes slightly, must its shortest description change dramatically?

**Model.** A picture is a finite set of black pixels on a rectangular grid. A description partitions the black pixels into disjoint, axis-aligned all-black rectangles. Let opt(P) be the smallest rectangle count. Measure representation change by the number of rectangles removed or added, |A symmetric_difference B|. Compare exact optimum with an additive allowance of k extra rectangles.

Separate three questions: existence of nearby representations for each neighboring pair of pictures; a single canonical choice of representation for every picture; and history-dependent maintenance over long edit sequences. These have different quantifiers and must not be conflated.

**First project.** Determine whether one pixel flip can force arbitrarily large change between every pair of optimal partitions. Enumerate small pictures and all optimal partitions; certify either witnesses or finite absence. Seek an infinite obstruction family or a uniform stability theorem. Do not assume an instability family exists.

**Baselines.** In one dimension, optimal maximal black intervals change by at most three intervals after one bit flip. In two dimensions, the optimal rectangle count changes by at most three. From an old optimal partition, one update has a simple representation with at most five rectangle additions/removals and at most four rectangles beyond the new optimum. Therefore the interesting work concerns exact or smaller slack, coherent canonical choices, and persistent online guarantees, rather than arbitrary positive slack.

**Branches.** Hierarchical descriptions; polygon partitions; tile systems; short grammars for strings; graph decompositions; randomized representations; memory versus canonicality; local construction rules.

**Nearby literature.** [Average Sensitivity of Graph Algorithms](https://arxiv.org/abs/1904.03248) and [Average Sensitivity of Geometric Algorithms](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.53/LIPIcs.ITCS.2026.53.html). Low-recourse maintenance, stable geometric algorithms, and selection problems are established neighbors.

**Exact remaining gap.** Check the rectangle-partition stability literature specifically. A compelling first unknown is whether all optimal descriptions of neighboring pictures can be far apart; another is a separation between pairwise and globally coherent selection. Preliminary search did not establish either as new or unresolved.

**Adversarial refinement.** Thin zigzag pictures reduce to matchings. They already separate the existence of a nearby pair of optimal descriptions from stability after an algorithm has committed to one description. Elementary online instability is therefore insufficient as a novel contribution. Prioritize small-slack guarantees over long sequences, canonical selection, or the stronger all-optima separation. Static rectangle minimization is itself classical; it is not the proposed invention.

**Assessment.** Most visual starting point. Attractive candidate for discovering an unexpected obstruction, but the central instability conjecture remains unverified.

## 5. Accuracy versus algebra in finite arithmetic

**Question.** How accurately can a tiny calculator behave while preserving algebraic laws?

**Model.** Fix m≥1 and S_m={−m,...,m}. Choose a commutative addition table ⊕ that agrees with ordinary addition whenever the true sum stays in S_m. Let C_m be clipping to [−m,m]. Define

    E = max_{x,y} |x⊕y − C_m(x+y)| / (2m)
    D = fraction of ordered triples (x,y,z) with
        (x⊕y)⊕z != x⊕(y⊕z).

Study the minimum achievable D subject to E≤ε. This retains fixed numerical meanings for the symbols, rather than considering arbitrary finite operation tables up to relabeling.

**Starting foothold.** E=0 forces clipping/saturation. D=0 forces cyclic addition modulo 2m+1, with E=1. Both endpoints have elementary proofs checked independently. Exact monotonicity also forces clipping, so imposing it together with associativity would destroy the design space. These facts are entry baselines, not novel results.

**First project.** Enumerate small tables, certify exact attainable error/associativity pairs, and search for sharp inequalities and infinite constructions. Check whether an existing approximate-algebra result already yields the frontier.

**Branches.** Other representable number sets; average rather than worst error; distribution-dependent laws; multiplication and distributivity; long expressions; a bounded hidden state; the geometry and classification of nearly optimal tables.

**Nearby literature.** [Saturation arithmetic](https://open-std.org/JTC1/SC22/WG21/docs/papers/2023/p0543r3.html), [Partial associativity and rough approximate groups](https://arxiv.org/abs/1904.08732), and [finite-arithmetic failures in privacy libraries](https://arxiv.org/abs/2207.10635). The approximate-group paper assumes injectivity in each variable, which need not hold here; that difference is not by itself proof of novelty.

**Exact remaining gap.** Establish whether the prescribed-order, prescribed-interior numerical frontier is known. Its mathematical importance must come from sharp laws and reusable constructions, not a catalog of arbitrary custom calculators.

**Assessment.** Strong arithmetic alternative, unusually amenable to exact finite verification. More speculative as a field seed than as a focused extremal problem.

## Independent approach ledger and rejected routes

| Family | Mechanism/evidence | Status | Exact gap |
|---|---|---|---|
| Discrete transformations | Frozen coloring regions; checked path formula | Finalist | Structural helper theory versus known minimum-label paths/recoloring |
| Observation/control | Beliefs retaining original/current pairs; finite recovery recursion | Finalist | Bounded prefix recovery versus existing planning/diagnosis |
| Reversible dynamics | Checked exact constant-map reservoir formula | Finalist | Optimal finite cardinality versus known dilations |
| Geometric descriptions | Interval and rectangle surgery bounds | Finalist | Infinite instability or selection separation |
| Finite arithmetic | Checked saturation/modular endpoints | Finalist | Sharp intermediate frontier versus approximate algebra |
| Carry locality | Redundant digits limiting carries | Rejected in this form | Direct predecessor: [hybrid signed-digit systems](https://www.ecs.umass.edu/ece/koren/research/PhKo-IEEETC-1994.pdf) |
| Generic local repair | Distance to patch a hole | Rejected as invention | Direct predecessor: Local Mending |
| Generic catalytic computation | Borrow memory and restore it | Rejected as invention | [Established catalytic space](https://ir.cwi.nl/pub/22659) |
| Sparse schedule perturbations | Distance in schedule space to changed periodic states | Reserve only | Need nontrivial examples beyond radius one; [order independence already studied](https://arxiv.org/abs/0707.2360) |
| Spatial catalytic rearrangement | Append helper tokens and restore them | Reserve only | Need natural rules with nontrivial catalyst budgets; rewriting and catalysis collision |

Do not reopen rejected broad routes merely under different names. Reopen only with a new mechanism or concrete evidence.

## Recommendation and decision gate

Prioritize temporary helpers for the most approachable first proof program, bounded-undo experiments for conceptual distinctiveness, and finite reservoirs for a route toward physics. Keep stable descriptions and finite arithmetic as genuinely different alternatives.

Before committing to a long program, require (1) a focused equivalence/literature audit, (2) an exact small-instance laboratory with independent certificates, (3) at least one structural phenomenon that survives adversarial checks, and (4) several natural questions that remain after the first theorem. A first result may be known and still useful for learning, but it cannot count as novelty.

The selection of a field and any subsequent research remain future work. This scouting task does not schedule autonomous continuation, contact researchers, publish a release, or create a DOI.
