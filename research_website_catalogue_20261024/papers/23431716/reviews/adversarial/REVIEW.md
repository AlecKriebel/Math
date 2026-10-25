# Independent adversarial review — Zenodo 23431716

**Verdict: PASS within the exact stated theorem scope.** No substantive mathematical defect was found. The conservative realization, both directions of the SAT reduction, arbitrary-schedule implication, simple/oriented graph restrictions, polynomial construction size, and NP certificate bound are supported by the proof reconstruction and controls below. This is an AI mathematical review, not human peer review, a priority certificate, or publication authorization.

## Reviewed object and independence

The reviewed work is *A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs*, v1.0, 16 October 2026, Zenodo 23431716. The complete seven-page public PDF has SHA256 `52d4355533f5095be83c8799bd148e9927e5c4bef8c2f6a00d534303f0b7ee5c`. The public support ZIP has SHA256 `a9606c07600ca9ac60f36f5165c8c09ff3e0c0b42e83e50d006df6f1ee2723fe` and contains 124 files, no additional reader PDF or nested archive. The full PDF and its `paper.tex` were read. Current mathematical support code (`checks.py`, `common.py`, `run_checks.py`) was read after fresh controls were completed.

No sibling mathematical report, historical assessment body, or archived verdict body was read. The source inventory exposed their filenames. The required manuscript contains earlier-checking/priority disclaimers; the current administrative `verify_kit.py`, inspected for replay boundaries, also embeds expected historical review-status labels. Those incidental labels are disclosed and were not mathematical evidence. The administrative/history verifier was not replayed; only the present mathematical diagnostic entry point was run. No omitted historical computation is claimed to have been reproduced.

Before reading submitted helper implementations I wrote separate, standard-library-only controls from the displayed equations. These include complete reachable-state exploration for small banks and graph examples, not merely the preferred firing order. Additional controls explicitly enumerate directed rooted trees to check the NP-certificate reasoning. Frozen inputs, scripts, exact outputs, primary-source read scopes and final hashes are retained. No sources, website, spreadsheet or publication state were changed.

## Exact theorem and model

The input graph is finite, loopless, strongly connected, has at least two vertices and at most one arc per ordered pair. Initial chips are nonnegative integers encoded in binary. A vertex of outdegree \(d_v\) may fire exactly when it has at least \(d_v\) chips; one chip goes along each outgoing arc. Every vertex, including the designated root and return vertices, obeys this ordinary conservative rule. There is no dissipative sink or external supply.

HALTING means that some finite legal firing word reaches a configuration with fewer than \(d_v\) chips at every vertex. The theorem proves NP-completeness, including instances with a supplied root whose removal leaves a DAG with no directed path of two arcs, and with numerical total initial chips polynomial in the SAT input length. A separate construction gives the same restrictions with no antiparallel pair. The main graph may have antiparallel root/counter arcs; “simple” here permits them. The oriented graph does not.

The proof asserts neither a polynomial-length play nor a polynomial-time simulation algorithm. A player voluntarily stopping while a vertex remains legal has not produced a stable endpoint. Schedule independence concerns complete/maximal legal play, and the NO proof uses an infinite legal word without a fairness premise.

## Least action and NP membership

With the manuscript's column-firing Laplacian convention, a count vector \(g\) changes the state to \(x-\Delta g\). Suppose a nonnegative vector \(f\) gives a stable \(z=x-\Delta f\). At the first firing that would exceed one coordinate of \(f\), all other counts are still bounded by \(f\). The current chips at that vertex are at most its chips in \(z\), below threshold. This contradiction bounds every legal word by \(f\). Repeatedly selecting a legal vertex therefore terminates at a stable state. No assumption that \(f\) itself was supplied as a legal word is needed for soundness.

For completeness, let \(f\) be an actual terminating count vector. The directed tree theorem gives a strictly positive primitive integer period \(\pi\in\ker\Delta\), with \(\pi_v\le(N-1)^{N-1}\), since each rooted directed tree selects one outgoing arc at every nonroot vertex. If every \(f_v\ge\pi_v\), then \(f-\pi\) would be a nonnegative stabilizing vector bounding that very legal word, an impossibility. Hence some \(w\) has \(f_w<\pi_w\).

For an arc \(u\to v\), nonnegative input and a final stable state give

\[
f_u\le d_v f_v+z_v-x_v\le d_v(f_v+1)-1,
\qquad f_u+1\le d_v(f_v+1).
\]

Following a simple directed path **from \(u\) to \(w\)** bounds \(f_u+1\) by \((N-1)^{N-1}\pi_w\le(N-1)^{2N-2}\). The orientation of this path matters and is correct. Each coordinate has polynomial bit length; checking nonnegativity and \(0\le x-\Delta f<d\) takes polynomial binary arithmetic. Arbitrarily large binary initial chip values do not invalidate the argument. For \(N=2\), strong connectivity and simplicity force the directed two-cycle, whose only halting nonnegative input is zero.

The additive-one correction is necessary. The displayed three-vertex example truly has firing vector \((1,0,0)\), so the unshifted edge inequality would fail. The inspected Farrell–Levine passage omits this slack; this paper supplies a direct corrected derivation and does not depend on that incorrect intermediate inequality. It preserves the prior membership attribution.

## Bank identity and Boolean encoding

For a nonempty set \(A\subseteq\mathbb Z/q\mathbb Z\), the multiplicity \(c_a=1+h(-a-1)-h(-a)\) lies in \(\{0,1,2\}\) and sums to \(q\). Increasing \(k\) shifts every counter by one but subtracts \(q\) for each wrapping counter, giving

\[
S_A(k+1)-S_A(k)=q-qc_{-k-1}=q(h(k+1)-h(k)).
\]

The difference \(S_A-qh\) is constant. Averaging a full period gives that constant as \(q(q-1)/2-|A|\), proving the exact identity and maximum. There is no probabilistic independence assumption. Full sets give constant storage; the negative constant at the \(q=2\), full-set boundary causes no negative physical counter. Empty sets are explicitly excluded, as they would make the claimed maximum unattainable.

After polynomial preprocessing, every surviving clause has one to three distinct variables, no tautological pair, and exactly one falsifying Boolean assignment. Its allowed CRT set therefore has \(2^t-1\) elements. A separate variable bank forces every residue into \(\{0,1\}\); without those variable banks, local clause complements would contain additional non-Boolean residues. The manuscript explicitly retains them. A common accepted integer gives a satisfying assignment; every satisfying assignment has a nonnegative CRT representative. The constructor needs neither such an assignment nor that representative.

Distinct primes begin at three. The exact primary prime bound yields \(p_{n+1}\le3(n+1)^2\). Only a single prime or a product of at most three primes is enumerated for a bank. The potentially exponential global product is used in the existence proof only, not expanded into graph size or construction time. Relabeling only occurring identifiers avoids exponential expansion of binary variable names or unused declarations.

## Conservative graph realization and both SAT directions

Let \(Q=\sum_b q_b\), \(P=\max_b q_b\), and let \(B\) be the sum of the individual storage maxima. Distinct copies of equal-offset counters are essential: each bank has \(q_b\) actual vertices, not merely one vertex per different offset.

In the main graph the root sends one chip to each of the \(Q\) counters. A modulus-\(q\) counter sends one directly to the root and one to each of \(q-1\) distinct return vertices. Every return has the sole outgoing arc to the root. Hence the counter's firing threshold and total output are both exactly \(q\); every firing conserves mass. Arc types connect different vertex classes, produce no repeated ordered pair or loop, and the largest bank reaches every return. Strong connectivity follows. Deleting the root leaves only counter-to-return arcs. The asserted counts \(N=Q+P\), \(|E|=Q+\sum q_b^2+P-1\) are correct.

The total mass is \(C=Q+B-1\), with counters initially at their offsets, empty returns, and root mass \(C-S(0)\ge Q-1\). At a checkpoint, one legal root firing adds exactly one chip to each stable counter. Each counter fires at most once, its resulting residue is correct, and it cannot be reactivated by any return. Emptying returns is a finite legal sequence; withholding a legal root during this sequence is permitted by the ordinary rules. The phases return every emitted chip, with no sink substitution or hidden dissipative step.

Consequently, at checkpoint \(k\) the root holds \(Q+B-1-S(k)\). It is stable exactly when \(S(k)=B\). Each failed bank loses the positive amount \(q_b\) from its own maximum, so deficits cannot cancel: the equality holds exactly when all bank predicates accept.

For SAT YES, a finite successful CRT checkpoint exists. The prescribed legal process either reaches it or stops earlier at another accepting checkpoint. For SAT NO, every checkpoint allows another root firing and finite legal nonroot phase, so concatenating phases produces an actual infinite legal word. Least action then excludes **every** terminating legal word. Thus examining a preferred schedule is enough here because the proof also supplies this independent arbitrary-schedule exclusion; it does not assume that all schedules visit the same checkpoints.

The oriented graph replaces the direct counter-to-root output by one additional return, using \(P\) returns in total. A degree-\(q\) counter has \(q\) distinct return targets. This preserves thresholds and total output. The three-part root–counter–return–root directions exclude antiparallel arcs. Strong connectivity and root-deleted depth are preserved, and \(N'=N+1\), \(|E'|=|E|+1\). Both halting implications therefore apply to this separate physical construction as well.

## Encoding, boundaries and size

With explicitly encoded SAT length \(L\), the numbers of occurring variables and clauses are \(O(L)\), \(U=O(L^2)\), \(P\le U^3=O(L^6)\), and \(Q\le HP=O(L^7)\). Thus vertices, edges and even an explicit adjacency matrix have polynomial size; the coarse edge bound is \(O(L^{13})\). Counter offset scans and CRT calculations are on polynomial-sized local moduli. The numerical mass bound \(C\le Q+\sum q_b(q_b+1)/2\) is also polynomial, so the unary-chip hardness statement follows.

The stable-capacity calculation has the correct signs and does not decide SAT by total mass alone. For nontrivial inputs \(q_b\ge3\), its difference is \(\sum_b(q_b(q_b-3)/2+|A_b|)\ge0\). The polynomial chip count does not imply a polynomial state space or play length.

Malformed strings, an empty clause and an empty conjunction are dealt with by fixed explicit NO/YES instances. The directed two-cycle is valid for the main class; the directed three-cycle is used for the oriented class. Their zero-chip states are stable, their one-chip states circulate forever, and deleting the designated root has the required depth. Duplicate literals, tautologies, one-variable clauses and large binary identifiers do not create missing reduction cases.

## Independent controls and submitted reproduction

The fresh scripts ran before submitted helper reading:

- `fresh_controls.py` checks all 501 nonempty subsets for moduli 2–8, including negative time residues and full sets; 38 complete reachable-state graphs for small main/oriented constructions (267 reachable states); and 146 two-variable SAT/canonical cases. Reachable directed cycles were computed separately from stable reachability, so the small arbitrary-schedule check is stronger than comparing two scheduling heuristics. The largest such state graph has 68 states.
- Deliberately unprimed banks fail to represent the intended maximum set in 494 cases. An extra root chip changes a tested YES into NO: its complete 33-state graph has a reachable cycle and no stable endpoint. These controls demonstrate sensitivity to the storage phase and strict threshold, rather than merely rerunning valid examples.
- `fresh_np_controls.py` enumerates actual directed trees on all 19 labelled strongly connected loopless simple graphs of sizes two and three. It checks 256 configurations through stable capacity plus one, with 113 halting inputs, verifies the period orientation, period subtraction and shifted bound, and detects 66 instances where the unshifted edge inequality fails.

The current packaged diagnostics passed normally and with Python optimization enabled; their deliberate invalid invocation exited nonzero as expected. Their reported coverage includes 501 banks, 67 CRT formulas, 134 main/oriented constructions, 73,386 legal firings, 186 generic configurations, 109 halting certificates, and damaged semantic variants. The packaged tests include three-literal examples beyond the fresh two-variable controls. All stdout, stderr and command receipts are retained. There was no need to run an administrative verifier that adopts archived review statuses, nor to rebuild or publish the package.

These finite checks supplement the general proofs above. They do not certify an unbounded theorem by exhaustion, nor constitute a new NP-hardness proof solely from sample behavior.

## Primary source interfaces and limits

Primary bytes and exact reading extents are bound in `primary-interfaces.json` and `evidence-bindings.json`. Relevant checks were:

- [Farrell–Levine, arXiv v3](https://arxiv.org/pdf/1502.04690v3): directed-tree period conventions, least-action context, membership passage, historical simple-graph question and Table 1. The source question is historical, not proof of present worldwide openness.
- [Holroyd–Levine–Winkler, arXiv v2](https://arxiv.org/pdf/1511.00422v2): Lemma 4.1 gives the priming increments used here. Its Section 8.3 explicitly distinguishes nonconservative abstract splitters/topplers from conservative sandpile nodes. The manuscript supplies the missing physical graph realization rather than silently identifying the models.
- [Stockmeyer–Meyer](https://esp.mit.edu/download/827dcf47cbc9cf4a3b04dbf773ea54fb/M3175_meyer-stockmeyer-word-probs.pdf), Theorem 6.1 and proof, and [Gramlich](https://ggramlich.github.io/Publications/unaryMFCS03.pdf), Fact 3: Boolean prime residues and local prime-product clauses are existing ingredients. I visually checked the scanned original encoding page as well as extracted text. The manuscript's complement qualification is accurate.
- [Dusart, Eq. (4.2)](https://arxiv.org/pdf/1002.0442v1): the logarithmic inequality and stated \(p_j<ej\log j\) consequence apply from \(j=2\), covering the selected primes.
- Farrell's thesis Sections 1.1/4.1 supplies root-last/conserved-mass antecedents. Eriksson's complete three-page paper gives an earlier exponential-length simple-graph example with linear initial chips; long running time alone is not a new hardness argument.
- The exact statements of Bond–Levine's sandpilization Corollary 6.6 and the journal GRM reachability Theorem 21 have respectively an all-input quantifier and a specified-target/arc-state model. Selected Esparza survey class interfaces likewise do not by themselves establish this restricted ordinary fixed-output halting theorem. I did not reprove those whole papers, inspect the unavailable weighted-net constructions, or exclude all possible earlier reductions.

## Strongest supported conclusion and exact remaining gap

Theorem 1 is supported in full as stated: ordinary conservative chip-firing HALTING is NP-complete on the specified simple strongly connected digraphs, including the root-deleted depth-one and polynomial numerical chip restrictions, and also on the separate oriented subclass. The proof has a polynomial-bit halting certificate and an explicit polynomial-size deterministic SAT reduction; it does not promise efficient physical simulation.

No substantive proof gap or counterexample was found within that scope. Remaining uncertainty concerns exact historical priority and independent human review, not a demonstrated missing step in the reduction. The paper explicitly leaves full-result, realization and oriented-realization priority unknown. This review does not convert those limits into a firstness claim or certify every cited paper's complete proof. Completion is 100% for this adversarial assignment.
