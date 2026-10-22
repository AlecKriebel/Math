## Scoped prior-result audit, finite counterexample, and remaining proof gap

This draft adds an AI-assisted, unrefereed authored audit for 2302 / EP-783, coprime sieving under a reciprocal budget. The claims have separate dispositions.

- The sharp fixed-C leading minimum ρ(e^C)+o(1) is accepted as prior work with explicit local repairs and classical analytic dependencies. The general-modulus reduction is credited to Terence Tao; the prime-modulus value/equality theory and correctly budgeted prime-tail construction are retained.
- Fixed-power-cutoff prime stability is accepted after the small-prime hypothesis and factor-2 corrections. Its scale parameter is fixed.
- Composite reciprocal mass o(1) for near-minimizers at C>log 2 is recovered by the corrected two-parameter argument. Tightness does not imply one fixed cutoff with o(1) loss.
- General harmonic rigidity is not accepted from the inspected February 25 proof because the fixed-error/cutoff-uniformity bridge is missing. This is no counterexample to the theorem, no disproof, and no global-openness claim.
- The literal all-N exact greedy rule fails at N=100, C=1/2: the greedy tail leaves 62 integers and the admissible replacement leaves 57. This single exact witness does not refute a fixed-C eventual rule, certify the replacement as globally optimal, or classify optimizers.

AUDIT.md preserves the complete ten-section authored audit, including all mathematical repairs, both Corollary 35 counterexamples, the strictness and fixed-u compactness arguments, the full composite-mass reconstruction, the exact remaining gap and the cardinality limitation. PROOF.md preserves the complete finite proof: both prime sets, every exact fraction and signed comparison, the next-prime obstruction and exact overlap-free counts. ACCEPTANCE.md and ACCEPTANCE.json preserve the separate dispositions and limitations.

Principal sources: Erdős's original printed p. 135, https://users.renyi.hu/~p_erdos/1973-21.pdf ; Tao's February 22 third version, https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf ; Chojecki's January note, https://www.ulam.ai/research/erdos783-final.pdf ; Chojecki's February 25 note, https://www.ulam.ai/research/erdos783-rem.pdf ; Granville–Soundararajan, https://arxiv.org/abs/math/0308009 .

The February note expressly claims general stability and is audited accordingly. The Granville–Soundararajan theorem, prime number theorem, Mertens theorem, Dickman asymptotics and Dickman log-concavity remain classical dependencies. Hildebrand's separate original paper and the full dependency closure were not re-audited; GS numerical inequalities were not interval-certified. The Dickman continuation calculation is a mechanism check, not a standalone full dependency certification. No formal proof project was executed.

Source inspection and retrieval statements are historical. All January, February, Tao and GS text was read, with the specified critical pages visually checked; only the original Erdős target page was audited. Tao's February 23 no-journal-plan statement is attributed historical intent from search-indexed discussion, not current publication status or journal acceptance. The direct forum fetch failed, and the bounded source search is not exhaustive.

## Distribution and verification

Exactly eight authored prose and public-metadata files are added under attempts/2302. No copied source manuscripts/text/images, raw datasets or calculation outputs, executable code, private sources or private coordination material are distributed. The mathematical finite sets and exact fractions are authored proof content. This is not a computational reproduction package.

Historical normal/-O/-OO independent finite checks agreed byte-for-byte on the one N=100 witness. VERIFICATION.json records their scope and identities, without raw output or code. No mathematical programs, scholarly-source retrieval or source-body inspection were repeated during editorial preparation. Byte-integrity and packaging checks do not prove the mathematical claims. Acceptance means internal AI mathematical audit, not external human peer review, journal acceptance, formal certification, novelty, priority or universal consensus.

QUEUE.md and unrelated paths are unchanged. Draft publication only; no merge, release or DOI creation.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,275 bytes; SHA-256 `c4b2d9f80070cb0a8d5e3f1ff34bf547b2d20b7de0f386df6f6df48a7da9e73b`.
- `ACCEPTANCE.md`: 5,608 bytes; SHA-256 `8b34862d4878107df8880b46c6a64d78f5cbfaec56baf6e5b5790c5359254a42`.
- `AUDIT.md`: 29,054 bytes; SHA-256 `8a9c0cc8e780410fec9a1aeac2b1eb1f894e468ab25a537804412c6b7cd20587`.
- `MANIFEST.json`: 1,338 bytes; SHA-256 `c518efc81f1c86a78e06b5d146f6c9b04a57f8bae6caa51c004abdf6af612153`.
- `PROOF.md`: 4,437 bytes; SHA-256 `4be00c28ca3be4fcc3c721bd6961cf4cef510a8054cf10cd9597b41213a4b58d`.
- `README.md`: 6,293 bytes; SHA-256 `564d917f4966f8b85acc81aac6aab6814b200627cf6a35785670a9222b8b5659`.
- `SOURCES.json`: 7,426 bytes; SHA-256 `13377eb5051315c64f2e6d982cae00389e9ab3fbbf04df50c44c5fc24d306566`.
- `VERIFICATION.json`: 3,355 bytes; SHA-256 `7aaca00d1edaf2ee35a72462524cb1a4fef5abd2b7647fbeca075d11f6fa41d5`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.
