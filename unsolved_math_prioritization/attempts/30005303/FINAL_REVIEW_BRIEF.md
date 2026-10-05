# Full two-turn candidate: 30005303

## Outcome proposed for review

The exact target bundles two binary graphical-model questions from Lauritzen's OWR55/2022 contribution, printed pp.3125–3126:

1. **Yes:** the MTP2 edge-factorizing class is closed under pointwise limits for every finite graph (TURN_2).
2. **No:** an MTP2 globally Markov distribution need not factor over graph cliques, already on the four-cycle (TURN_1).

The counterexample also answers the related stronger lattice-support Conjecture 3 negatively. It is not in the closure of the factorizing model, so it is consistent with the affirmative answer to question 1. The source's separate Gaussian coordinate-descent question is not in this numeric target.

**Substantive count: 2/5. Author search frozen with a complete candidate.** Independent verification may find a gap; this document does not pre-judge that review. There is no claim of historical novelty. No strict-positivity, special-graph, or support-connectivity assumption is silently added.

## Reading order

1. SOURCE_GATE.md and source_record.json for exact source, provenance, prior attempts, and search limits.
2. TURN_1.md for the C4 counterexample; its quartic is explicitly credited to Geiger–Meek–Sturmfels (2006).
3. TURN_2.md for the general closure argument. It gives a self-contained support reduction and residual-cut proof; classical graph-cut reparameterization is credited.
4. SOURCE_RECHECK_2.md, TURN_LEDGER_2.json and exact checker receipts.
5. FINAL_PACKET_MANIFEST.json binds every public artifact, including the unchanged first-turn manifest and earlier ledger.

## Main adversarial questions

- Does global Markov separation in C4 give precisely the two deterministic conditional independences used in TURN_1, despite boundary zeros?
- Is the quartic invariant balanced for every allowed clique potential, including zeros and real signs, and does it rule out the closure as claimed?
- In TURN_2, does edge factorization give the *exact* support intersection (4)? Are all active-edge projections in list (5), and does collapsing implications give every upper set with no missing constraints?
- For incomparable equality components, are all four square atoms in the support? Does the mixed log contrast isolate the **aggregated** coefficient, even if individual edge couplings are negative?
- Does placing an aggregate on one original connecting edge preserve log p on the support without adding graph edges? Are all implication penalties ferromagnetic and all fixed-coordinate penalties unary?
- In the residual network, is cut capacity minus maximum flow exactly the nonnegative residual cut sum for every state? Does it use only original nonterminal edges? Is there a common zero preventing partition sums from tending to zero?
- Does compactness preserve a genuine normalized factorization, and are null conditioning assignments, isolated vertices, empty graphs and the literal edge-only source convention handled?
- Do the source/current-literature checks justify a complete answer to the stated target without converting it into a novelty claim or a claim that the 2006 quartic/max-flow tools are new?

## Reproduction

From this directory:

- `python3 checks/verify_turn1.py`: 332 exact assertions on C4.
- `python3 checks/verify_c6.py`: 13,520 exact assertions on C6.
- `python3 checks/verify_turn2.py`: 550,337 exact assertions. It tests 6,443 admissible factorized MTP2 examples (3,282 with proper nontrivial support), 1,865 incomparable-component interactions, and 2,006 positive-model flow gauges, including multiscale degenerations. One hand-designed case has a negative original edge coupling canceled by another edge after equality-component aggregation.

Total: **564,189 exact assertions**. Randomly generated cases use a fixed seed. These controls do not replace the unrestricted mathematical proof. No floating-point approximation is used in the asserted equalities or inequalities.

Primary PDFs, rendered source pages and extracted text are retained locally for review; only compact links, hashes, authored mathematics and checks are published. All first-turn bytes are preserved.
