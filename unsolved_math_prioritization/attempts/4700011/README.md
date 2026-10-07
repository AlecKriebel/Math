# Periodic rational difference equations: accepted partial results

Problem 4700011 (Gasull Problem 11), rank 941. **Unsolved; five of five proof-attempt turns used.** The arbitrary-order classification remains unresolved. No novelty, priority, new periodic example, or literature-completeness claim is established.

## Accepted mathematical scope

- Complete classifications at orders 6, 13, and 15, with arbitrary nonnegative real coefficients in the original recurrence class.
- Every-order classification when the reduced numerator has at most two active variable terms.
- A finite cyclotomic-factor reduction and per-order period/identity decision for odd orders.
- An all-L exclusion at order k = 4L + 2 when the midpoint is the only active odd lag and at least one even lag is active, for arbitrary real active coefficients and either constant status.
- Rational-ratio and rationally scaled finite-candidate reductions, together with necessary cubic, parity, algebraic-unit, and lag-gap conditions under their stated hypotheses.

The finite procedures are termination theorems for their specified subclasses, not a completed all-order enumeration or an efficiency guarantee. Necessary spectral and arithmetic tests are not sufficient for nonlinear periodicity. The exact remaining gaps are in the five manuscripts and each audit's acceptance boundaries.

## Frozen proofs and complete audits

The [authored packet](authored/README.md) contains all five unchanged manuscripts, their original exact verifiers, outputs, source credits, and original manifest. Read the manuscripts in turn order.

- [Turns 1 and 2 acceptance report](periodic_recurrence_independent_audit/ACCEPTANCE_REPORT.md): structural reductions and the complete order-six argument; 22 independent named checks.
- [Turns 3 and 4 acceptance report](odd_recurrence_audit/ACCEPTANCE_REPORT.md): odd-order reduction, exact orders 13 and 15, and every-order sparse support; 49 independent named checks.
- [Turn 5 acceptance report](fifth_recurrence_audit/ACCEPTANCE_REPORT.md): uniform mixed-lag exclusion and arithmetic reductions; 10 check groups including 502 support patterns.

No mathematical correction was needed. Each entire acceptance report, audit implementation, recorded result, frozen input, replay artifact, and allowlisted public-source inspection metadata is preserved. The audits are independent AI-authored mathematical reviews, not human peer review or formal proof-assistant certification. AI tools were used extensively in producing this work.

## Source scope

See [the qualified public-source credits](authored/SOURCES.md). Gasull's 2020 problem formulation and the specified method sources were inspected to the extent documented there. The full proof of the 2004 Cima–Gasull–Mañosas article was not inspected; bibliographic and abstract checks do not establish novelty. This packet includes authored mathematics and public verification metadata, not copied papers, screenshots, source dataset contents, or private sources.

## Portable verification

Requires Python 3.10+ and SymPy 1.14.0; recorded runs use Python 3.12.14. From this directory:

```sh
python -m pip install -r requirements.txt
python verify_packet.py
```

Once dependencies are installed, verification is offline and source-free. The verifier checks all byte counts/SHA-256 pins, the four original input manifests, and author/frozen equality. It then copies the allowlisted packet into a temporary directory and runs all five authored verifiers and all three independent audit verifiers, comparing each of their eight generated result files byte-for-byte against the frozen record. It rechecks the untouched packet afterward. The historical replay copies are inventoried but are not run again as duplicate jobs.

`python verify_packet.py --integrity-only` checks integrity without running the algebra. [PACKET_MANIFEST.json](PACKET_MANIFEST.json) inventories every package file except itself; [INPUT_PINS.json](INPUT_PINS.json) binds the four untouched input inventories. [REPLAY_VERIFICATION.json](REPLAY_VERIFICATION.json) records the actual publication replay. The verifier does not formally check manuscript prose, retrieve literature, establish novelty, or implement all unbounded/per-order decision procedures proved in the manuscripts. Finite support samples supplement the general proofs rather than replacing them.

See [RESEARCH_LOG.md](RESEARCH_LOG.md) for the publication checkpoint and unresolved scope.
