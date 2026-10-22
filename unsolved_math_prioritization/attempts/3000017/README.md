# Binary weighted cactus chip firing halting

Problem 3000017 / AMR-029-0017 concerns halting on general Eulerian multigraphs. This edition proves a restricted theorem: O(n²) exact integer arithmetic operations, with polynomial intermediate bit length, suffice on directed-cycle block cacti with independent positive binary-encoded weights on their blocks. Every bidirected weighted tree is included. A bidirected triangle is excluded.

The proof supplies the full compressed elimination algorithm and certifying potentials. Its halting certificate is allowed to have a negative root and is a stable upper bound, not a claimed reachable endpoint. The nonhalting branch gives a nonnegative equivalent configuration with a legal once-per-vertex recurrent sequence. Integral block-potential telescoping, recognition, operation counts, bit bounds, the literal degree-zero singleton convention, and both explanatory families are proved in full.

No required mathematical correction was found. The sole mathematical-wording clarification distinguishes unfinalized aggregates in [−C,N] from finalized coordinates in [0,d_v−1], giving the uniform stored-coordinate interval [−C,max(N,C)].

## Contents

- PROOF.md: complete analytical theorem, algorithm, proof, examples, and source context
- AUDIT.md: complete independent logical review and historical supporting checks
- ACCEPTANCE.md and ACCEPTANCE.json: acceptance scope and exact document bindings
- SOURCES.json: public scholarly and problem-source identities and historical inspection limits
- VERIFICATION.json: aggregate historical verification, outcome digests, and receipt identities
- MANIFEST.json: exact eight-file inventory, hashing the other seven files

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The general Eulerian-multigraph target remains unresolved by this work; no novelty, priority, or exhaustive current-literature claim is made.

This edition contains the complete self-contained mathematical proof and full analytical algorithm. It is not a computational reproduction package: executable programs, raw certificate contents, and copied source documents are not distributed. Historical finite checks are supporting validation only; no omitted computational premise is needed for the theorem. Edition preparation made no new mathematical test runs, scholarly-source retrieval, visual source inspection, or literature search.
