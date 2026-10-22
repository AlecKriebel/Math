# A finite disproof of temporal unimodality

For database problem 3100082 / AMR-030-0082, the simple symmetric nearest-neighbour random walk on the integer lattice has a verified finite counterexample to Cooper–Spencer Conjecture 3. In dimension 26, the occupation probability at (17,0,...,0) strictly decreases from time 65 to time 67, then strictly increases to time 69. All three times lie in the reachable odd parity class.

The full proof is in [PROOF.md](PROOF.md). It derives exhaustive finite counting recurrences, displays all three exact walk counts and both strict differences, and uses the probability normalization 52 per step and 2704 across two steps. The [audit](AUDIT.md) supplies independent counting arguments and discriminating checks. The [acceptance report](ACCEPTANCE.md) states the accepted conclusion and its limits. [Source metadata](SOURCE_PINS.json) records public citations, versions, PDF hashes and sizes, and inspection history. [Aggregate checks](CHECK_SUMMARY.json) summarizes the verified diagnostic outcomes. [The manifest](MANIFEST.json) records the exact public file set and SHA256 hashes; it excludes itself from its own entries and is not a digital signature.

## Attribution and scope

The dimension, endpoint, and three-time witness were already given by Anonymous, *Counterexamples to the Cooper–Spencer temporal-unimodality conjecture*, version 1.0.0-candidate, 19 September 2026, available through the [Evidence Press release](https://evidencepress.org/releases/cooper-spencer-temporal-unimodality/). That manuscript describes itself as an unrefereed AI-assisted preprint. This report reconstructs and independently verifies its finite witness; it makes no novelty or external peer-review claim.

The result concerns discrete-time occupation probabilities. It makes no claim about minimal dimension, a complete mode count, endpoint classification, continuous time, an infinite family, historical priority, proof-assistant formalization, the other Cooper–Spencer conjectures, or their deterministic-simulation theorem. Public source metadata describes the material inspected on 11 October 2026; it does not certify later revisions. No source-author code was executed.

The mathematical exposition is self-contained. No copied source documents, extracts, images, scripts, or exhaustive raw count tables are included.
