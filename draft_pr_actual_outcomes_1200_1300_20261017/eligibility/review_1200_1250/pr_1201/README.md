# Prior vertex critical edge resilience results and repaired proof

For EP944 / problem 2398, this authored edition preserves and audits prior results. Ema Skottová and Raphael Steiner's 2025 theorem supplies a (k,r)-graph for every k>=5 and every r>=1, with the stated square-root progression and cube-root all-large-orders lower bounds. Its complete repaired self-contained conventional lower proof is included, with both appendices, the k=6,8 two-block bridge, vertex-deletion wraparound, gluing, and quantitative order allocation. Every correctness-relevant printed repair remains explicit and the theorem statements and thresholds are unchanged.

A separate historical independent computation accepts Alex Chan's fixed-commit graph on 60 vertices and 180 edges as a (4,1)-graph. Two independent complete searches checked its edge-deletion noncolorability. Its exact three-color defect is 2, so that graph does not extend to r=2. The family k=4,r>=2 is unresolved by these audited results. The computation is not a premise of the conventional k>=5 proof.

The upper-bound argument separately imports Conlon–Fox Lemma 8.1. Its source omits the lemma's proof; only the downstream implication is checked here. No first-principles proof of that external theorem is claimed.

## Contents

- PROOF.md: complete repaired conventional lower proof, quantitative orders, and separate upper-bound dependency
- AUDIT.md: full printed repairs, independent focused review, finite audit methods, and formal-source boundary
- ACCEPTANCE.md and ACCEPTANCE.json: decisions, scope, exact bindings, and limitations
- SOURCES.json: public source URLs, byte identities, and historical retrieval and inspection scope
- VERIFICATION.json: aggregate historical checks, receipt hashes, and proof-dependency map
- MANIFEST.json: exact eight-file membership, with identities of the other seven files

The conventional lower-bound proof is self-contained. The finite result is accepted at a historical exact-computation boundary. This prose edition is not a computational reproduction package: executable programs, graph/generator/coordinate data, raw colorings and certificates, copied sources and images are omitted. Reproducing the finite verification requires the omitted public-source inputs and an implementation of the disclosed exact methods. No author code or Lean project was executed by the audits; static Lean-semantic inspection is not formal replay.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit; no external human peer review, journal acceptance, formal proof-assistant certification, novelty, priority, exhaustive global literature status, or full-problem resolution is claimed. Edition preparation made no new mathematical test run, scholarly-source retrieval, visual source inspection, or literature search.
