# Independent determinization-input audit

Audit date: 2026-10-06 (America/Los_Angeles). Reviewer: independent subagent `upstream_determinization`. This audit concerns the original family-129 determinization dependency, not the proposed binary reduction or its novelty. The upstream checkout was treated as read-only. Its observed HEAD is `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, matching the required pin.

## Result and present validation status

The exact input is: for every integer `h >= 2`, relation liveness `OWL_h = {R_1...R_l : R_1 ... R_l != empty}` over **all** binary relations on `[h]` has a no-left-move nondeterministic automaton with `h+3` states. Every equivalent ordinary two-way deterministic automaton with `s` states satisfies

`2^floor((h-2)/31) <= 4(s+2)^2`.

Under acceptance that includes the initial configuration, the sharper right side is `4(s+1)^2`. The source accepts the empty word; the empty product is the identity on `[h]`. Alphabet cardinality is `2^(h^2)`.

I found no substantive mathematical or semantic gap in the portions read and checked below. This is a favorable dependency audit, **not** a claim that the follow-on theorem has been formalized. Actual Lean build reproduction and axiom printing are assigned to the separate `formal_reproduction` agent; their eventual evidence must be added before any claim of reproduced formal verification. A source scan found no `sorry`, `admit`, `axiom`, or `unsafe` declaration in `lean/OAI/Combinatorics/Automata`; the apparent `admit` text hit is the English comment “admits a unit lift.”

## Primary sources and exact citations

Let `P` denote `/Users/alec/Desktop/math/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026`, and `L` denote `/Users/alec/Desktop/math/lean/OAI/Combinatorics/Automata`.

* Exact mathematical theorem: `P/build/sections/introduction.tex:99–110`; language and empty input: lines 84–97; finite alphabet size and source-state parameter: lines 119–128.
* Machine conventions: `P/build/sections/machines.tex:4–19`, and `L/Model.lean:36–99`.
* Explicit no-left-move source: `P/build/sections/separation.tex:10–35`; actual Lean construction `L/PathNFA.lean:66–88`, correctness `accepts_iff` at line 192, and state-count theorem `small_nfa` at line 243. In Lean its unused rejecting state has no rules, while the prose construction loops in rejection; both have identical accepted language and count `h+3` states.
* Actual final formal statement: `L/Main.lean:10–16`, declaration `OAI.OneWayLiveness.main_theorem`; its inputs are `small_nfa` and `deterministic_lower_bound`, not a ComparatorChallenges template.
* Actual quantitative lower bound: `L/Recognition.lean:80–95`, declaration `OAI.OneWayLiveness.deterministic_lower_bound`.
* Formalization catalogue names `OAI.OneWayLiveness.main_theorem` in `lean/formalization.yaml:1354–1356`. `lean/docs/129.md` is a scope description, not proof evidence.
* Citation supplied by upstream README: author `OpenAI`, title `An exponential two-way deterministic state lower bound for one-way liveness`, year 2026, manuscript-specific key `OAI:An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026`, URL `https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/main.pdf`.

## Convention agreement and boundary scrutiny

The model has one read-only head; distinct left and right endmarkers; initial head at the left marker; partial deterministic transitions; left, stay and right moves; no move beyond an endmarker; all initial and accepting states counted. Acceptance is reachability of an accepting configuration by a finite run. A missing transition produces no next configuration; an infinite nonaccepting run never yields such a finite witness. Acceptance may be tested either with a zero-length run allowed or with a strictly positive run required.

Lean `FiniteRun` is precisely reflexive-transitive closure for the first convention and transitive closure for the second (`Model.lean:80–90`). Its finite head index type has `length+2` positions, so the empty word still has two distinct adjacent marker cells (`Model.lean:50–56`). The transition boundary fields independently prohibit outward marker moves (`Model.lean:58–70`). The quantifier in `Recognizes` ranges over every finite body word (`Model.lean:95–99`), with no length bound or promise.

The manuscript normalizes accepting configurations to an additional sink state that sweeps right and stops at the right marker (`machines.tex:86–117`). Thus initially accepting, interior-accepting, marker-accepting and formerly undefined accepting rows all reach the designated terminal. Other loops are irrelevant because only the basin of the terminal is used. For strictly positive acceptance it first introduces a nonaccepting initial copy with the old initial transition row; destinations remain old states. An undefined initial row consequently stays rejecting, while a first transition that re-enters the old accepting initial state correctly accepts. This explains the one-state quantitative difference, rather than imposing a hidden halting condition.

## Pivotal dependency ledger and falsification checks

| Dependency | Exact statement and source | Independent scrutiny | Status |
|---|---|---|---|
| Sink-component tree | A finite partial-functional graph's component containing a vertex with no successor consists exactly of vertices reaching that terminal and is a tree. `machines.tex:56–84`; functional-source injectivity in `L/Tours.lean:73–99`. | The “remove the first successor step” implication only uses a terminal distinct from any source. Edge count is `v-1`; loops and parallel edges cannot occur in this component. Nonaccepting cycle components need not be trees. | No gap found. |
| Local symbol matching | Every `s`-state target gives symbol diagrams of degree `4(s+1)^2`, or `4(s+2)^2` under positive acceptance. `machines.tex:21–39`, construction lines 161 onward. | Candidate crossing slots are indexed by direction and ordered state pair; an unused source endpoint becomes its own leaf while the destination endpoint always attaches locally. Hence the target cell never consults its neighbor. Actual stay loops have distinct incidences. Both travel lanes and cyclic-order joins give degree two internally, allowing contraction to a perfect matching. Fixed external test leaves are distinct even for empty input. | No gap found. |
| Full syntactic quotient | Equal body diagrams imply equal relation products, so the generated diagram submonoid maps unitally and onto the entire relation monoid. `separation.tex:37–77`; `L/Syntactic.lean:13–25,31–64`. | Singleton-identity left/right context letters distinguish **every** differing ordered pair. Empty body diagram maps to identity even if another word shares it. Every relation is available as one input letter, so full surjectivity is justified. This argument would fail for a restricted alphabet without separate work. | No gap found. |
| Corner reduction and common support | An idempotent rank-`r` corner embeds unitally into degree `r`, preserving rank; `|supp(e)| <= 2(m-r)`; supported sandwiches remain supported in one set of size at most the original set. `matching.tex:103–124`, proof lines 126–217; `L/Diagram.lean` declarations `reduce`, `reduceHom_common_support` via `Corners.lean`. | Connector paths between retained endpoints are disjoint. A marked identity edge can mark at most one retained transversal. Unmarked paths survive every perturbation supported in `J`, because every internal port on such a path remains occupied. Absolute ranks, rather than newly chosen coordinate sizes, are compared across reductions. | No gap found; independent exhaustive tiny checks pass. |
| Unit lifts | A minimum-rank idempotent preimage of a local identity forces preimages of target units in that corner to reduce to full-rank permutation diagrams. `matching.tex:235–275`; `L/Corners.lean:153–183`; `L/Relations.lean:304–315`. | A finite target unit has a positive identity power; an idempotent power of its lift lies above the local identity. Minimality and rank monotonicity force equality of all intervening ranks. A finite-order permutation's inverse stays inside the reduced submonoid. No unjustified unit lifting from a general surjection is used. | No gap found. |
| Smaller full relation corner | If `EPE=E`, `Q=PEP`, then `Q R(H) Q` is unitally isomorphic to all relations on the retained points. `matching.tex:286–334`; `L/Relations.lean:64–102`. | Direct multiplication uses `P^2=P` and `EPE=E`; inverse is `A -> PAP`. This is full relation surjectivity, not only the sparse addition semilattice. | No gap found. |
| Exponential rank loss | A single extra ordered pair above identity forces rank loss `2^floor((h-2)/31)` after minimum-rank unit-lift normalization. `rank.tex:25–39,202–278,306–351`; `L/RankLoss.lean:20–86,180–266,276–354,365–388`. | There are 32 conjugates, total support at most `64c`, and 256 distinct additions. Retained set at each step has `h-31` points; the current new pair is absent from the old relation there. A **second** minimum-rank reduction supplies actual smaller unit lifts. Each step loses at least `L(h-31)/2`; summation requires at least `128L(h-31)`, giving `c >= 2L(h-31)`. Induction decreases `h`; base range `2..32`; recurrence is exact including `h=33`. | No gap found. |

## Independent finite algebra check

`determinization_algebra_check.py` is an independently written perfect-matching enumerator and direct gluing implementation. It does not import the upstream code. It checks all Brauer diagrams of degrees 0, 1, 2, 3 and 4 and every idempotent in those degrees for:

1. The idempotent support bound.
2. Injectivity, identity preservation and rank preservation of the explicit deleted-cap corner reduction.
3. Multiplication preservation for **every pair** in each corner.
4. Existence of one common reduced support set of size at most `|J|` for every subset `J` and every diagram supported in it, by taking the union of actual reduced sandwich supports.

`determinization_algebra_check_results.json` reports PASS, generated using Python 3.14.6. Degree 4 includes 105 diagrams, 40 idempotents, 11,304 corner products, and 7,520 supported sandwiches. The checks include the zero-degree corner. These are counterexample searches for several pivotal finite facts, **not** substitutes for the uniform induction or formal build. Exact SHA-256 hashes of the 16 Lean modules and five manuscript section sources inspected are in `upstream_determinization_sha256.txt`.

## Exact remaining limitations

* This dependency audit does not establish the proposed binary source state count, target pullback count, malformed-word behavior, complementation-universe convention, literature priority or final package correctness.
* No conclusion here has been drawn about `L != NL`, exponential-in-binary-source-state `2^Omega(n)` growth, uniform transition-table complexity, or uniform logarithmic-space separation.
* Source-only Lean inspection is complete; a successful recreated build, transitive axiom listing and pinned source hash record remain separate evidence from the reproduction agent.
* Upstream manuscript dates and repository existence establish attribution instructions, not earliest public priority. The priority agent must verify public disclosures and later corrections.

Mathematical-input audit completion estimate: 95% pending build/axiom evidence. Publication-package completion attributable to this audit: 0%; no package has been reviewed or published by this subagent.
