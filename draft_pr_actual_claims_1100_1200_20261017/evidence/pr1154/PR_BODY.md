## Accepted partial result; exact target unresolved

Problem 30001551 / OWR-4425-006 asks whether exactly three independent constant-free equations on three variables, with nonempty variable words on both sides, admit one common nonperiodic solution in a finite-alphabet free monoid. Empty variable images are allowed; independence concerns the complete solution set.

This unrefereed AI-assisted exposition and independent internal AI mathematical/source/computational audit accept three partial statements:

- At most one equation of a hypothetical independent triple with a common nonperiodic solution admits an erasing deletion witness.
- If the triple has a common erasing nonperiodic solution, no equation admits an erasing deletion witness.
- A balanced three-variable system with a common nonperiodic solution and a member equivalent to pairwise commutation is equivalent to at most two original members.

The complete proof and substantive audit are preserved. The exact supplied clarification patch is applied: the two-word criterion uses injectivity of an indexed morphism on distinct formal letters, correctly covering equal and empty images; the three-profile heading explicitly concerns nonperiodic erasing morphisms. No theorem, hypothesis, or inference changes.

The erasure mechanism is credited to Holub–Žemlička, [Algebraic properties of word equations](https://doi.org/10.1016/j.jalgebra.2015.03.021), Lemmas 15–16. The balanced reduction uses Saarela, [On the Solution Sets of Three-Variable Word Equations](https://doi.org/10.1007/s00224-024-10193-9), Lemma 4.4. Nowotka–Saarela's [2022 bound](https://doi.org/10.1137/20M1310448) is 17 with a common nonperiodic solution; 18 concerns systems without that requirement. No novelty or improved general bound is claimed.

Both bounded searches were reconstructed independently with exact arithmetic and every signature bit compared: 157,800 equations / 216 binary morphisms / 5 signatures / 10 triples, and 28,216 equations / 2,744 binary morphisms / 15 signatures / 455 triples. No triple passes on either finite pool. This does not rule out longer or nonbinary witnesses at the searched equation lengths, longer equations, or systems whose common nonperiodic solutions are all nonerasing. It does not exclude erasing common nonperiodic solutions. The exact target remains unresolved by this work.

“Accepted” means the internal audit's stated partial scope. No external human peer review, journal acceptance of these authored documents, formal proof-assistant certification, or exhaustive literature absence is claimed. The public metadata retains recorded inspection scopes, public URLs, PDF hashes and byte counts. Independent URL opens establish source availability and work identity, not a separate byte-identical live download. Edition preparation adds no source retrieval, inspection, mathematical search or literature search.

This addition-only draft contains ten authored prose, correction-patch, audit, acceptance, and public verification/source metadata files. It contains no copied source documents, executable code, raw signature data or certificates, dataset contents, private sources, private personal data, or private coordination material. The documented computational checks are not distributed as an executable reproduction package. Original sealed inputs, QUEUE.md, and all unrelated paths remain unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 4,476 bytes; SHA-256 `b37db41ca3aeb60a0e24f5add78f87b6dbc18a1f8e6f73e55e4b5810a8f16403`.
- `AUDIT.md`: 12,224 bytes; SHA-256 `8a1072d7bccf88723cc957468926ea7c23a9f1f5c6e4a048ceed7973d3200d0f`.
- `MANIFEST.json`: 1,930 bytes; SHA-256 `d1dcd4f00c79c5597d30cffdcb199dbb0f9b334f5100f1a76532d309a3dd33a8`.
- `PROOF.md`: 8,762 bytes; SHA-256 `789e66432d69e98b18230efdf629a7cf55238fd54a040fa2e9195a34692af50f`.
- `PROOF_CLARIFICATION.patch`: 1,638 bytes; SHA-256 `00dd4680003bb5e4a30168f031b192de33366d3cb44e27812b3b81ef690fd5b6`.
- `README.md`: 4,913 bytes; SHA-256 `6037a5af7338e3126c9df7da1b028c6c610833a126b98b66a2307111fac3da14`.
- `REPORT.md`: 5,287 bytes; SHA-256 `5e8d145223c70037e398fb0713202c958519062a0c634e8e6b296fa348a7c102`.
- `SCOPE_AND_SOURCES.json`: 3,052 bytes; SHA-256 `b6da1d8c8cc93719827748aed2f1c49c4f407efc2648bdaa74af605f6655eba0`.
- `SOURCE_VERIFICATION.json`: 3,132 bytes; SHA-256 `ad5286210322730988af458cc3bcf8f533e425c87ac11ed2f397c05ca1233d7a`.
- `VERIFICATION_SUMMARY.md`: 5,515 bytes; SHA-256 `6a57df6a132df354afe2386cc96b8bd995b3d0de538bd166b7b8f0a63d248b55`.

MANIFEST.json lists all ten members and hashes the other nine. Its separately listed digest avoids self-reference.

