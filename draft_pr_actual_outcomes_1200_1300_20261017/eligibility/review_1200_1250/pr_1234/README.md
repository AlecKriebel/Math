# Positive three-term radical blocks: accepted partial results

Problem 2339 / EP-850. For positive integers a<b, the unresolved target asks whether rad(a+i)=rad(b+i) can hold simultaneously for i=0,1,2, with rad(1)=1. Equality is positionwise.

## Exact accepted scope

1. Elementary, fully written proof: the positive starts n whose product n(n+1)(n+2) has at most three distinct prime factors are exactly 1, 2, 3, 4, 6, 7, 8, 16. A target counterexample therefore needs at least four common union primes.
2. BHV-dependent computational result: for primes at most 41, the exhaustive all-magnitude enumeration has 869 consecutive-pair starts and 141 three-term starts, largest triple start 212380. Every triple has union radical at least 3n, with equality only n=2. The target therefore has no counterexample whose common support consists only of primes at most 41.

The full unrestricted problem is unresolved by this work. The remaining obstacle is uniformity over unbounded prime supports. No general inequality rad(n(n+1)(n+2))>=n is proved.

## Read the complete written argument

- [PROOF.md](PROOF.md): complete authored elementary classification, exact reformulations, valuation identities, Pell normalization, continued-fraction argument, explicit BHV hypotheses, finite-field index bound, exhaustive algorithm and unresolved gap.
- [AUDIT.md](AUDIT.md): complete independent mathematical audit, stronger detailed continued-fraction derivation, exact independent-computation counts, source boundaries, controls and acceptance limits.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): exact accepted partial scope and exclusions.
- [SOURCES.json](SOURCES.json): public citations, inspected-source identities and precise retrieval/inspection history.
- [VERIFICATION.json](VERIFICATION.json): public aggregate verification metadata, source/artifact hashes, and reproduction limits.
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory and hashes for the other seven files.

This AI-assisted, unrefereed edition records an independent internal AI audit. Acceptance is an internal mathematical assessment, not external human peer review or formal proof-assistant certification. The complete authored elementary proof and Pell/BHV completeness derivation are retained. BHV is an explicitly imported established theorem; its proof and original computations are not reproduced or independently audited here. The exact 41-smooth enumeration is a computation-dependent result supported by historical independent verification. This edition omits the 141-start inventory, raw certificates, programs and raw datasets, so it is not a self-contained computational reproduction package. Hashes authenticate bytes, not mathematical truth. Source retrieval and inspection described here occurred in the preceding candidate and audit on 11 October 2026; this editorial preparation performed no new scholarly-source retrieval, inspection or mathematical computation.

The 141-start list, 869-pair inventory, arithmetic certificates, programs, copied source PDFs/text/images, raw datasets and private material are omitted. Consequently the numerical classification cannot be independently replayed from this edition alone. Independent reproduction requires executing the complete exact algorithm described in the proof or obtaining the separately authenticated numerical artifacts. The elementary proof is self-contained and independent of those computations.

Bilu, Hanrot and Voutier's published primitive-divisor theorem is imported, with every index at most 30 retained explicitly. Shorey and Tijdeman's theorem for the original target assumes their stated explicit abc conjecture. Neither hypothesis is silently discarded. Classical Størmer/Pell methods are credited; no novelty or worldwide literature-status claim is made.

A historical inventory-tool issue was fixed before the candidate was sealed. The final authenticated candidate and both mathematical results require no correction patch.
