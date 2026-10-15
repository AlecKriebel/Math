# Reviewed two-turn answers to the MTP2 factorization questions

**Numeric target:** 30005303 / OWR-11695865-001.  
**Disposition:** claimed_solved, 2/5 substantive author turns.  
**Review:** independent AI-assisted adversarial review passed the complete stated mathematical scope. This is not human peer review or formal proof-assistant certification. Historical priority remains unverified.

## Results

- **Conjecture 1: yes.** For every finite binary graph, the MTP2 edge-factorizing distributions form a pointwise closed set. The proof covers zero probabilities, disconnected support, arbitrary graph structure, isolated vertices, and the source's literal edge-only convention.
- **Conjecture 2: no.** On C4, the distribution p(a,a,b,c)=2^(abc)/9 is MTP2 and globally Markov, but violates a known clique-factorization quartic. It is outside even the closure of the factorizing model.
- The same example also disproves the related **Conjecture 3**, which assumes only lattice support and the global Markov property.

The imported target asks the first two questions. The source contribution's separate Gaussian coordinate-descent problem is outside this target.

## Proof and credit

TURN_1.md contains the eight-atom counterexample and a direct invariant proof. The quartic is explicitly credited to Geiger–Meek–Sturmfels (2006), equation (4.10).

TURN_2.md proves closure by reducing boundary support to pins, equality components and order implications; MTP2 forces the remaining aggregate interactions to be nonnegative. Positive ferromagnetic approximation and the classical max-flow residual reparameterization then provide bounded local factors with nonvanishing normalization. The classical graph-cut tools are credited. The new complete deduction is presented without a priority claim.

## Verification and preservation

The author packet has 19 frozen files, with FINAL_PACKET_MANIFEST.json binding the other 18. All are preserved byte-for-byte. The `review/` directory preserves all eight frozen review files, including its seven-entry manifest. Earlier author turns, source reports, ledgers and manifests remain unchanged.

Three author checkers replayed exactly, passing 564,189 assertions. Separately written review code passed 89,324 assertions, including all 731 nonempty Boolean four-cube sublattices tested against all four-vertex graphs and 1,000 additional residual-flow instances. These finite controls supplement the unrestricted proofs.

Read FINAL_REVIEW_BRIEF.md, then TURN_1.md and TURN_2.md, followed by review/ADVERSARIAL_REVIEW.md. SOURCE_GATE.md and SOURCE_RECHECK_2.md record the exact primary scope and the limits of the current-literature and prior-attempt searches. No third-party PDF or raw full dataset is republished.
