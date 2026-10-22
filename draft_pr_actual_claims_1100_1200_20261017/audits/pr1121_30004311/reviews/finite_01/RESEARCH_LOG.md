# Independent finite audit research log

Scope: PR1121 / problem 30004311, frozen head `f86b108ac1bc024302648eee9f47f74e26c810ec`.
Frozen `PROOF.md` SHA256: `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`.

## 2026-10-17T20:08:23Z — 10% complete

Created the dedicated directory and `.gitignore` containing `tmp/` before reading the proof. Read the frozen proof and verified its supplied digest. No source retrieval, external communication, Git mutation, or dependency installation is part of this audit.

Hypothesis: the direct operations produce the claimed simple 20,000-element brace, with the stated multiplicative invariants and explicit star-product obstructions. Success requires independent finite encodings, factored exhaustive identities, all 19,999 nonzero ideal-seed derivations, adversarial controls, and clearly delimited computational scope. The general no-presentation conclusion additionally needs the abstract obstruction theorem, independently audited by the parent task.

Plan: represent ring elements by base-five integers but calculate ring products by truncated polynomial convolution; represent vectors by five-bit even masks. Compare the direct operation with a separately implemented semidirect-product law. Build ideal certificates from allowed lambda differences, stars, and additive operations. Check generic two-trivial-factor examples and malformed variants to ensure the checker detects absent hypotheses.

## 2026-10-17T20:13:25Z — 80% complete

Initial exact run passed 3,317,275 guarded requirements in about eight seconds. Every one of the 19,999 nonzero seeds reaches the nine additive generators in at most 13 ideal operations. Exact invariants: fixed set order 10, multiplicative center order 5, derived subgroup order 400, socle order 1, and abelianization order 50. All listed explicit witnesses match.

The generalized-cocycle control enumerated 169 normalized symmetric maps across six small cyclic configurations. Among 29 action-preserving symmetric cocycles, precisely 12 satisfy the brace identity; all 17 rejected maps are nonbilinear. Ten valid cases have all multiplicative Sylows abelian, and all relevant triples vanish. A genuine order-eight asymmetric-product brace with a nonabelian Sylow subgroup has an explicit nonzero triple. These are finite controls, not a proof of the universal lemma.

Three structural mutations (raw fourth coefficient instead of eta, removal of Q, removal of beta) each produce explicit associativity failures. Replacing sigma or M by the identity destroys a required simplicity-propagation step. A wrong exponential coefficient is detected as an inverse failure.

Before completion, strengthened certificate validation: each generated transcript will be consumed by a strategy-independent replay using the opposite direct-operation/lambda encoding, with prior-node guards and repeated-addition verification of scalar operations. Also added all 390,625 P5 star-product pairs, and finite checks that the nine terminal generators generate the stated additive groups. Final run will use Python optimization to demonstrate that no validation depends on assertions.

## 2026-10-17T20:14:24+00:00 — 100% complete

Final optimized run passed all 4,327,588 guarded requirements. Strategy-independent replay verified 259,858 derived transcript nodes for all 19,999 seeds. The added P5 star check covered every one of the 390,625 pairs. Exact input fingerprint, computed witnesses, negative controls, and generalized-product finite scope are recorded in REPORT.md and results.json. The earlier accidental future checkpoint timestamp was corrected to the actual observed UTC time before freezing fingerprints. No mathematical defect was found. Universal obstruction theorems remain the analytical audit responsibility. Final report and artifact receipts are now being frozen.
