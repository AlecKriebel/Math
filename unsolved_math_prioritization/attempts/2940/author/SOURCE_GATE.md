# Source and claim gate

Checked: 2026-10-03 UTC. **Gate disposition: primary scope recovered; full target unresolved.** A separate adversarial mathematical review is still pending at author freeze.

## Exact question

The 2026 K3 preliminary author book places Problem 4.64 on printed p. 242 (PDF page 242). The question has all four conditions: irreducible, closed, smooth, and an ordinary Bauer–Furuta/Seiberg–Witten separation. The accompanying remark says the familiar examples use connected sums and identifies the irreducible case as unknown. The book credits M. Stoffregen and I. Dai as proposer and scribe.

The live catalogue URL, https://www.unsolvedmath.com/problems/2940, returned HTTP 403. A pinned catalogue identified the correct primary question; its generated literature annotations were not evidence for any mathematical assertion. The primary PDF was fetched independently with HTTP 200. No statement from inaccessible live catalogue content was treated as newly verified.

The book's notice prohibits reposting the preliminary PDF without permission. The distributable packet contains only original mathematical exposition, bibliographic links, hashes and a short paraphrase of the target. It contains no source PDF or copied full-text extract.

## Core references and proof reading

### K3: modern problem statement

URL: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf

Fetched complete PDF, 6,578,041 bytes. SHA-256: `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`.

Read the exact problem and complete accompanying remark on p. 242. This is a 2026 preliminary author version, not a claim of access to a later final book revision. Its unknown-status remark is dated evidence, not an impossibility theorem or exhaustive search certificate.

### Bauer–Furuta I: target and comparison map

Author preprint: https://arxiv.org/pdf/math/0204340 (v1, 29 April 2002).
Published article: https://doi.org/10.1007/s00222-003-0288-5

Fetched complete 18-page author preprint, 206,323 bytes. SHA-256: `c47e295d561588110c621b577bcd7e3b1ef95b68c43868ec6bbb751b3530d1cb`.

Read the theorem and b⁺=1 boundary discussion in §1, the finite-dimensional setup used for its stable invariant, and the complete proofs of Propositions 3.3 and 3.4 and Lemma 3.5 (preprint pp. 13–15). The latter invokes the Atiyah–Hirzebruch spectral sequence and standard stable-stem/attaching-map facts. This note uses that published computation as an external theorem; the arithmetic checker does not independently compute stable cohomotopy. The source's b⁺>b₁+1 restriction is satisfied in every application here because b₁=0 and b⁺>1. The low-dimensional table is explicitly limited to r≥2.

No final typeset publisher PDF was independently inspected. The corresponding computations are also checked against Bauer's later survey Proposition 6.1; the two source formulas agree in the overlapping range.

### Bauer II: connected-sum multiplication

Author preprint: https://arxiv.org/pdf/math/0204267 (v1, 22 April 2002).
Published article: https://doi.org/10.1007/s00222-003-0289-4

Fetched complete 19-page author preprint, 211,273 bytes. SHA-256: `ec6c4b2e329eb9484c677c1d6f25250c605adf83209462b020bc9921ced46663`.

Read Theorem 1.1; its setup in §2; the complete three-homotopy gluing proof in §3 including the neck-length estimates, Lemmas 3.2–3.5 and the final composition; and the applications in §4, including the complete proofs of Propositions 4.4–4.5 and the K3-support argument in the proof of Corollary 1.4. The distinction between η³≠0, η⁴=0 nonequivariantly and the four-fold **equivariant** nonvanishing condition is retained. The theorem produces reducible examples, not an irreducibility assertion.

The preprint's closing Problem 4.8 is a historical related question; it is not substituted for the exact modern Problem 4.64. No final typeset publisher PDF was independently inspected.

### Bauer: refined invariants and −2 gluing

URL: https://arxiv.org/pdf/math/0312523 (v1, 31 December 2003).

Fetched complete 33-page author manuscript, 361,668 bytes. SHA-256: `3c0fad53a25074252ca50569e5f13a82c66ff9b5ef284d0622372c8fd1752492`.

Read §5's comparison result, §6's complete low-dimensional group discussion, and §8's gluing hypotheses and complete proofs/explanations of Theorems 8.1–8.6 and 8.8. For the RP³ gluing, Theorem 8.4 forces the inducing Chern evaluations to be 0 and 2. The proof of Theorem 8.6 uses sphere reflections and a positive-semidefinite span, precisely the scope used here. The nonvanishing-support condition is required on **both** summands. The note proves its zero-evaluation corollary directly rather than dropping that compatibility condition.

The HTML rendering reports a recent rendering date; that is not a new 2026 mathematical revision. The fixed arXiv v1 manuscript is the version used. Some arguments in the manuscript explicitly build on Bauer II and standard gauge-theory foundations; those dependencies have not been represented as new proofs in this packet.

### Furuta–Kametani–Minami: ordinary invariant survives Pin(2) restriction

Journal-hosted full article: https://www.ms.u-tokyo.ac.jp/journal/pdf/jms080109.pdf
Journal record: https://www.ms.u-tokyo.ac.jp/journal/abstract/jms080109.html

Fetched complete 20-page final journal PDF, 166,632 bytes. SHA-256: `6b8c55df876b0d06cffe037d3ed901200b8e2473a26d3f9695d855b9d2318b9a`.

Read the complete relevant proof chain: §2.1's construction and invariance of δ; stabilization in Lemma 7; its zero class and bijectivity in Definitions 8–9 and Lemmas 10–12; the explicit framed-circle calculation in Lemma 13; the n≥3 zero model in Lemma 14; the full free-involution/Stiefel–Whitney argument of Proposition 16; and Theorems 19–20 in §3. The conclusion δ=1 is about the **S¹ stable-homotopy** invariant, after restriction from Pin(2), so it answers the ordinary-invariant nonvanishing subproblem.

Normalization caution: the displayed general m formula on printed p. 172 visibly has denominator 2; the same page also describes E's fiber with W₀ where the prior definition uses W₁. These are apparent typographical slips, not formulas adopted here. The packet uses the independently checked complex Dirac index r=(c²−σ)/8 from Bauer–Furuta, consistent with FKM's quaternionic-index setup and with H²→R⁶ for the spin rational K3#K3 case. The journal page was visually inspected to distinguish printed notation from extraction errors. Theorems 19–20 and their proof chain are applied with their explicitly stated spin/Betti/rational-ring hypotheses.

## Update search and non-equivalent claims

Identifier searches and subject searches for irreducible ordinary-BF/SW separation found the modern K3 question and the primary results above, but no later full solution. Search coverage is not exhaustive. Two recent primary abstracts were checked to avoid promoting a different invariant:

- Konno–Lin–Mukherjee–Muñoz-Echániz, *Constraints on Lefschetz fibrations with four-dimensional fibers from Seiberg–Witten theory*, https://arxiv.org/abs/2511.00601, concerns family invariants and exotic diffeomorphisms, including ones on irreducible manifolds. That advertised conclusion alone is not an ordinary-BF-nonzero/all-SW-zero example.
- H. Wu, *Pin⁻(2) Bauer–Furuta invariants*, https://arxiv.org/abs/2603.27842, defines a different refinement and connected-sum formula. It is not substituted for ordinary S¹ BF.

These were screened at abstract level, not claimed to have been fully proof-audited. They are not dependencies of the mathematical propositions.

## Prior-work and scope boundary

Repository reads checked the actual root, `problems`, and existing attempt-directory listings, along with PR searches for 2940, 4.64 and Bauer and branch searches for 2940 and 4-64. No existing target-specific attempt or PR was located. Search-index absence alone was not relied on. The target queue row was queued, 0/5; that status by itself was not a no-prior-work certificate.

The author's five mathematical attempts are distinct from this source recovery. Only the proof packet is frozen. The intended eventual status is unsolved, 5/5, subject to separate adversarial review. No solved classification, invariant descent theorem, irreducible realization, universal impossibility, or novelty certification passes this gate.
