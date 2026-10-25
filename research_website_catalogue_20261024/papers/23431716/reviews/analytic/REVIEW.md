# Independent analytic review — Zenodo 23431716

**PASS at the stated scope.** I found no substantive mathematical defect in the seven-page Version 1.0 manuscript, dated 16 October 2026, *A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs*. The complete proof supports ordinary conservative chip-firing on finite loopless simple strongly connected digraphs, including the oriented subclass, with the stated root-deletion restriction. NP membership covers arbitrary nonnegative binary configurations; the hardness construction uses polynomial numerical total chips and therefore also gives unary-configuration hardness. This is an AI review, not human peer review, formal proof-assistant certification or a novelty/priority certificate.

## Bound inputs and independence

The fresh published PDF is 83,409 bytes, SHA-256 `52d4355533f5095be83c8799bd148e9927e5c4bef8c2f6a00d534303f0b7ee5c`. The support ZIP is 798,999 bytes, SHA-256 `a9606c07600ca9ac60f36f5165c8c09ff3e0c0b42e83e50d006df6f1ee2723fe`. The final verdict binds the current receipt, record metadata, both assets and all 124 extracted members. Original bytes remain unchanged.

I read the full actual PDF and complete `paper.tex`, reconstructed the proof, and wrote and ran the independent controls before opening published helper code. The mathematical helpers `checks.py`, `run_checks.py` and `common.py` were subsequently read in full. The current package's `verify_kit.py` was also inspected: its executable checks contain historical administrative adoption/zero-finding strings, so those were incidentally exposed after the independent derivation and controls. They were not evidence for the mathematical verdict. No dedicated historical assessment body, sibling finding or sibling code was read. The mathematical replay does not load the historical review files; the administrative whole-package checker was not run or used as a correctness oracle.

## Exact decision problem and least action

The input explicitly has at least two vertices, no loops, no repeated ordered arc, strong connectivity and nonnegative integral chips. “Oriented” further excludes opposite arcs. Strong connectivity ensures positive outdegree at every vertex. A legal firing subtracts the actual outdegree and sends one chip along each outgoing arc. No vertex is a dissipative sink; conservation is exact. HALTING means that some legal finite word ends in a stable state. Stopping voluntarily while an active vertex remains is not a YES witness.

With the column convention `Δvv=dv`, `Δvu=−1` for `u→v`, the state after firing counts `g` is `x−Δg`. The least-action argument is correct: at the first attempted excess over a nonnegative stabilizing vector `f`, the attempted vertex has already fired exactly `fv`, while every incoming contributor has fired at most its corresponding coordinate of `f`. Its current chips are therefore at most the stable target coordinate, below its threshold. This contradiction bounds every legal prefix by `f`. Consequently repeated legal firing must stop, without a fairness assumption, whenever a stabilizing certificate exists. Conversely, a single infinite legal word rules out every terminating word. The proof does not infer arbitrary-schedule behavior merely from a preferred simulation order.

## Polynomial-bit certificate

For a strongly connected digraph, the positive in-arborescence counts form a kernel vector for the column Laplacian; dividing their gcd gives the positive primitive period `π`. The direction of the trees and of the kernel is correct. One can see the balance identity by adding an outgoing edge to a rooted in-tree: the resulting unique directed cycle can be rerooted at the predecessor of the old root, giving the incoming/outgoing tree-count bijection. Each nonroot vertex has at most `N−1` outgoing choices, so `πv≤(N−1)^(N−1)`.

For an actual terminating word with count vector `f`, at least one vertex `w` has `fw<πw`. Otherwise `f−π≥0` would give the same stable endpoint, and least action applied to the actual word would imply `f≤f−π`, impossible. The crucial edge inequality follows from exact chip balance and the nonnegative initial configuration:

`fu ≤ Σ(a→v) fa = dv fv + zv − xv ≤ dv(fv+1)−1`, hence `fu+1≤dv(fv+1)` for `u→v`.

Following a directed simple path **from `u` to `w`**, not the reverse path, gives `fu+1≤(N−1)^(N−1)πw≤(N−1)^(2N−2)`. Thus each coordinate needs only `O(N log N)` bits. The verifier can check `f≥0` and `0≤x−Δf<d` using polynomial-time integer arithmetic, regardless of the supplied input chip magnitudes. It need not find or simulate the legal word. The two-vertex case is correctly separated: only the directed two-cycle is possible, and conservation makes the zero configuration the only halting input.

The additive slack is essential. For the displayed three-vertex graph, firing vertex 0 once sends `(1,0,0)` to stable `(0,1,0)`, so the slack-free inequality `f0≤d1 f1` fails. I checked the actual Farrell–Levine source line as well as the example. This does not invalidate the prior NP-membership result; the reviewed paper supplies its own corrected bound.

## Modular storage identity

For nonempty `A⊆Z/qZ`, `q≥2`, the multiplicities `ca=1+h(−a−1)−h(−a)` are nonnegative and at most two, and their sum telescopes to `q`. Distinct copies at the same offset are separate physical vertices. On increasing the checkpoint index by one, every counter gains one except the wrapping counters, which lose an extra `q`. Therefore the storage difference is `q(h(k+1)−h(k))`. Averaging over a period gives exactly `SA(k)=q(q−1)/2−|A|+q h(k)` for every integer `k`. Its maximum is attained precisely on `A`; deficits are exactly `q`.

Full allowed sets correctly give constant storage, including the `q=2` case where the auxiliary constant can be negative while every physical counter count is nonnegative. Empty allowed sets are excluded because their purported upper level is unattainable. The reduction itself uses moduli at least three. These distinctions prevent a hidden endpoint failure in the bank-to-predicate step.

The substitution into Holroyd–Levine–Winkler's actual Lemma 4.1 is exact: `F(k)=k+h(0)−h(k)` has nonnegative increments, zero initial output and period-`q` additive increase `q`; its parallel toppler multiplicities at offset `a=q−i` equal the printed `ca`. Each physical degree-`q` counter emits `q` chips on firing, whereas an abstract unary toppler emits one output letter. The manuscript does not confuse these models: it proves the conservative realization separately, consistent with that source's Section 8.3.

## Boolean encoding and polynomial construction

The preprocessing is total on explicitly encoded strings: reject malformed data, remove repeated literals, discard tautologies, handle empty clauses and empty conjunctions, and relabel only variables actually present. It does not expand numerical variable names or declared unused variables. Hence both actual variables and clauses are `O(L)` in the input length.

Distinct primes starting at three are pairwise coprime. The variable predicates force Boolean residues. For a normalized clause using `t=1,2,3` variables, exactly `2^t−1` Boolean assignments satisfy it, giving a nonempty allowed set of at most seven residues modulo the product of its primes. The local CRT map is injective on assignments; global CRT gives a common nonnegative checkpoint for every satisfying assignment. The reverse direction follows from the variable banks, so no non-Boolean residue can masquerade as a satisfying global assignment.

The comparison with Stockmeyer–Meyer and Gramlich is qualified correctly. A clause's allowed-set complement contains non-Boolean residues as well as its unique falsifying Boolean residue. Those extra residues are already rejected by the variable predicates, so the **full** intersection of allowed predicates is the complement of the classical union of invalid-variable and falsifying-clause predicates. It is not an equality of each isolated local complement with just one bad residue.

Dusart's original Eq. (4.2) is `log p*j≤log j+log log j+1`, `j≥2`, which exponentiates to the bound used here. The coarse estimate `p*(n+1)≤3(n+1)^2` follows and includes `n=1`. Thus each prime is polynomial, each local modulus is at most a three-prime product, and enumerating individual offsets remains polynomial. The global product of all primes serves only as a correctness witness. Its numerical value is never expanded into vertices, arcs or a forced simulation by the reduction.

Using the displayed coarse bounds gives, for example, `P=O(L^6)`, `Q=O(L^7)`, vertices `O(L^7)`, arcs and numerical chips `O(L^13)`, and even a full adjacency matrix of `O(L^14)` bits. These loose bounds suffice; no efficient small exponent is claimed. Polynomial numerical mass is stronger than merely polynomial binary description and establishes the unary-configuration hardness assertion.

## Physical graphs and arbitrary-schedule equivalence

In the main construction the root has one arc to each of `Q` separate counters. A modulus-`q` counter has one arc to the root and `q−1` arcs to distinct returns; a return has exactly one arc to the root. Vertex classes are disjoint, so there are no loops or duplicate ordered arcs. Opposite root-counter arcs are permitted only in this first construction. A largest-modulus bank has `P` actual counters and reaches every return. Every vertex reaches the root and the root reaches every vertex, proving strong connectivity. Deleting the specified root leaves only counter-to-return arcs: no cycle and no directed two-arc path. Counts `N=Q+P` and `|E|=Q+Σq²+P−1` are correct.

The initial counters contain their offsets, returns contain zero, and the root holds `Q+B−1−S(0)≥Q−1≥0`; total conserved mass is `C=Q+B−1`. At a checkpoint a legal root firing gives every counter exactly one chip. Because counters have no other incoming arcs and were stable, each can fire at most once. Processing all counters and then all ordinary degree-one returns is a finite legal phase. Delaying the root during that phase is allowed. Every emitted chip returns to the root; the proof does not replace these returns with dissipative sinks.

After `k` such phases the counters hold their residues and the root contains `Q+B−1−S(k)`. Since storage is integral and at most `B`, the root is stable exactly when `S(k)=B`, and nonnegative bank deficits imply that this occurs exactly when all predicates accept. A satisfying formula gives a finite successful checkpoint, unless the process already halted earlier. For an unsatisfiable formula every checkpoint permits another root firing and a finite clearing phase, producing an infinite legal word. Least action then rules out every finite stable-ending schedule. No fairness, polynomial-time dynamics or unique schedule is assumed.

The oriented version replaces the direct counter-to-root output with one additional distinct return and uses `P` returns. Each counter still has degree `q`, still sends exactly `q` chips per firing, and all chips reach the root. All arcs follow root→counter→return→root, so there are no opposite pairs. Counts increase by one vertex and one arc; the checkpoint identity and mass are unchanged. Fixed two-cycle YES/NO instances in the main class and three-cycle instances in the oriented class handle preprocessing cases and retain the root-deletion restriction.

The stable-capacity calculation also checks: `(|E|−N)−C=Σ[q(q−3)/2+|A|]≥0` because reduction moduli are at least three. Thus a trivial excess-mass test does not decide these SAT instances. The construction is not claimed Eulerian, bidirected or coEulerian, where stronger tractability results might apply.

## Independent controls and replay

`independent_controls.py` was authored from the paper before helper inspection and uses only exact standard-library arithmetic. It completed **1,109,572 assertions**:

- All 2,035 nonempty allowed sets for moduli 2–10, including negative checkpoint indices, full sets and cumulative primed-toppler outputs.
- All 255 nonempty subsets of the eight possible normalized clauses on two variables, eight individual three-variable clauses, and the unsatisfiable conjunction of all eight three-variable clauses: 264 formulas, 528 physical main/oriented graphs. A direct residue scan independently checked local CRT sets and the full bad-union complement. Physical firings checked conservation at every move, graph restrictions, exact checkpoint storage and halting/nonhalting outcomes.
- All 19 loopless strongly connected labeled graphs on two or three vertices. Direct enumeration of in-arborescences checked the period orientation and bound. For every total mass through one above stable capacity, a complete finite transition graph was built: 256 configurations and 227 legal transitions. Reverse reachability of stable states was compared with iterative dead-end removal, whose surviving states are exactly those admitting an infinite legal walk. There was no state admitting both termination and an infinite word. Complete legal-prefix count checks corroborated least action and the additive certificate inequality.
- Eight additional complete state spaces for physically constructed modulus-two bank games, including contradictory predicates, rather than only selected schedules.
- Exact semantic negative controls: increasing the root mass by one makes an otherwise accepting full-set bank nonhalting; deleting the direct return without replacing its output changes the actual degree and makes a satisfiable bank game nonhalting. Saved repeated states certify the mutant cycles. Empty allowed sets and the missing additive slack are separately detected.

These finite controls corroborate the general proof; their limits are explicit. They do not establish an unbounded theorem by exhaustive sampling.

The unmodified current mathematical diagnostics were then run in an isolated copy, under ordinary and optimized Python. Outputs agree and both pass: 501 bank sets, 67 CRT formulas, 134 constructed graphs, 73,386 legal firings, 19 generic graphs, 186 configurations, 109 halting certificates, eight noncanonical schedules, eight rejected faults and four semantic outcome faults. The deliberately invalid command is rejected under both modes. The helpers use unconditional guards, so optimized mode does not silently remove their checks. The diagnostic implementation is not advertised as a complete production SAT-to-graph tool; the polynomial constructor is specified by the mathematical proof. The package's historical programs and administrative adoption tests were not replayed or adopted as new mathematical evidence.

## Primary-source audit scope

The exact primary PDFs and reading scopes are bound in `primary-source-bindings.json`. The important interfaces were read in source bodies, not inferred from titles or abstracts:

- Farrell–Levine v3: ordinary conservative nonnegative chip input, strong connectivity, least action, period/tree orientation, the membership argument with its omitted intermediate slack, and Section 3.1/Table 1's historical simple-graph question. The table establishes historical attribution, not present worldwide openness.
- Holroyd–Levine–Winkler v2: full Lemma 4.1 construction and Section 8.3's conservative-gate distinction. The specialization is exact; the physical graph proof is supplied here.
- Stockmeyer–Meyer, Theorem 6.1 and complete relevant reduction on scan pp. 7–8, visually checked as well as extracted; Gramlich's Fact 3 and proof on pp. 5–6. Both support the attributed prime/Boolean/clause scheme and complement distinction.
- Dusart v1, Section 4 Eq. (4.2) and its short proof: exact endpoint and logarithm convention checked.
- Farrell's sole-author thesis Sections 1.1 and 4.1: root-last scheduling and the conserved-mass comparison are antecedents. Eriksson's three-page paper supplies a simple directed family with linear initial mass and exponential convergent play length; it does not turn simulation into a polynomial decision algorithm.
- The actual generalized rotor journal PDF pp. 39–43 specifies arc-state and chip-state endpoints and branching routing faces. Bond–Levine Definition 6.5/Corollary 6.6 concerns halting on **all** inputs. Esparza's selected pp. 31–32 concern Petri-net classes whose restrictions must be checked separately. These are scope comparisons, not imported hardness transfers. I do not certify those entire outside papers or prove that no other transfer exists.

The main proof is self-contained apart from standard background such as 3-SAT NP-completeness, CRT, the tree-period identity and the explicitly bounded prime supply. No inaccessible modern weighted-net result is needed for its mathematical conclusion. Full-result priority, priority of the physical/oriented realization and worldwide openness remain unknown; no novelty conclusion is supplied by this review. There is no remaining central mathematical gap identified at the stated scope, and no source repair, publication action or outreach was performed.
