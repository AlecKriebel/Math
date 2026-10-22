# Bounded integral homology obstruction for outer automorphism groups

This packet records an accepted bounded consequence for problem 11000286. If `n, m >= 8`, `n != m`, and `m < binomial(n, 2)`, every homomorphism `Out(F_n) -> Out(F_m)` induces the zero map on integral second homology, while both second homology groups are nonzero. In particular, this applies to `m = n + 1` for every `n >= 8`.

## What the proof establishes

Kielak's Theorem 6.8 forces the homomorphism to factor through `C_2`, whose integral second homology vanishes. An explicit integral bar cycle detected by a Clifford-cover cocycle proves nonvanishing for the symmetric groups. The actual comparison maps in Galatius's Theorem 1.1 and Hatcher and Vogtmann's Corollary 1 transfer that nonvanishing to `Out(F_r)` for `r >= 8`.

The proof relies on those published source theorems; this packet does not reprove them. It does not claim novelty, a general-rank obstruction, or a resolution of the full original question. No conclusion is asserted for target ranks `m >= binomial(n, 2)`, equal ranks, ranks below eight, or all homological degrees. Rational stable homology is discussed separately in the proof.

## Review status

The proof, audit, and preparation are AI-assisted. The audit includes separate source checks and an explicit mathematical review, but no external human peer review or formal proof-assistant certification is claimed. The finite exact-arithmetic results are historical audit outcomes, not a replacement for the proof. Preparation verified their recorded fingerprints and the frozen inputs without rerunning the mathematical checker or source-author code.

## Reading this packet

- `PROOF.md` is the full expanded proof, preserved byte for byte from the accepted audit packet.
- `AUDIT.md` is the full mathematical audit. Its only editorial changes disclose review status, redirect an excluded validation-file reference to aggregate outcomes, and clarify this packet's contents.
- `SOURCE_PINS.json` provides scholarly titles, public URLs, inspected page locations, PDF sizes, and SHA-256 fingerprints.
- `SOURCE_RETRIEVAL.json` records the upstream public-source retrieval and byte-match history.
- `AGGREGATE_CHECKS.json` records finite-check totals, historical run outcomes, and preparation checks.
- `ACCEPTANCE.json` binds the acceptance scope to the proof, audit, and supporting metadata.
- `MANIFEST.json` is the closed inventory of the seven other files. The manifest's own fingerprint is recorded outside the public packet to avoid a circular hash.

The public inventory consists of exactly these eight files. Source PDFs, extracted source text, source-page images, dataset contents, raw 48-element group data, raw cocycle tables, scripts, control files, and private coordination material are excluded. Preparation made no repository or queue changes.
