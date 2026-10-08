# Publication acceptance: restricted results only

Decision dated 2026-10-08: accept corrected partial progress for problem 30003116 / OWR-14603-015, queue rank 993. Preserve **unsolved, 5/5** for the intended sufficiently-large-denominator target. This publication/validation adds zero substantive proof-search turns.

The mathematical acceptance requires the nonempty-U domain clarification in `MATHEMATICAL_CLARIFICATION.patch`. The average collision identity holds at T=0, but the subsequent quotient T^2/E_r would be 0/0. Every orbit application already has T>=1; neither headline bound changes. The patch is applied exactly in `corrected/04_average_collision.md`.

Separately adopt `OPTIONAL_VALIDATOR_HARDENING.patch` in `corrected/verify_public.py`. It validates redundant schema/target fields and gives controlled errors for malformed top-level manifests and Python syntax. It is optional diagnostic/schema hardening, not a mathematical correction or evidence that the original packet was corrupted. All original files and all audit files remain byte-for-byte unchanged at baseline 0644 modes. Both patch texts are preserved unchanged in the audit.

Manifest SHA-256 anchors:

- Original: f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115
- Independent audit: c31e73a1f91d61795313bd602583881ef06dbbf03491aa5c995b286bfe6929ee
- Corrected with both patches: 5bad065fa3e8cdce7dc68a7772b66075a124f112648176bb9da417a0b21762b4

The central accepted uniform bound is C(A,(log s)^(-4)) >= c sqrt(log log s) at logarithmic time, below the requested polynomial-in-logarithm covering bound. The prime-denominator density-one bound gives C(A,(log p)^(-6)) >= c(log p)^(3/2), with at most (p-1)/sqrt(log p) exceptional nonzero numerators. The worst numerator and arbitrary composite denominators are not controlled. Conditional Baker-based seed and close-pair results, exact empirical-invariance identities and a single-generator entropy-transfer obstruction are retained with their hypotheses. The literal a=4,b=7,s=3 fixed-point counterexample is not an asymptotic resolution or a two-generator large-denominator obstruction.

Full written proof review and the independent audit, rather than finite testing, support these scoped conclusions. Baker–Wüstholz remains an external theorem input; BLMV's effective rational-orbit triple-log density theorem is credited prior work. Neither novelty nor current global openness follows from bounded searches. This is AI-assisted, unrefereed work; an independent AI audit is not conventional human peer review or formal verification.

The publication wrapper requires separately trusted wrapper and outer-manifest identities, exact inventory and modes, strict types, no duplicate JSON keys, no links/special files, and exact patch derivation. Read-only projections preserve frozen bytes; native read-only fixtures explicitly re-pin mode-only manifest changes instead of reusing the baseline anchor. Re-pinning arbitrary false mathematical text can still pass an integrity-only checker if the trust root is deliberately changed; the preserved audit demonstrates that boundary. The publication wrapper rejects drift against its fixed frozen anchors, but is not a theorem prover or security proof.

Only this target's existing QUEUE.md Status, Turns and Findings cells are amended. The literal existing first sha line and every other byte, including Chat/DOI cells and unrelated rows, are preserved. No queue regeneration or private coordination-state upload is part of this packet. No merge, release, external outreach or additional manuscript-status promotion is requested.
