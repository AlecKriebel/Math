# Independent word equations: accepted partial reduction (30001551)

**Status: PARTIAL. The exact independent-triple question remains unresolved by this work.**

This edition preserves an attributed erasing-witness restriction, its complete written proof and substantive audit, the bounded-search report, and public source/verification metadata. It makes no novelty claim, no universal nonexistence claim, and no improvement of the known general upper bound 17.

## Exact target and accepted result

The question is whether exactly three independent constant-free equations on `X,Y,Z`, with nonempty variable words on both sides, can have one common nonperiodic solution in a finite-alphabet free monoid. Empty variable images are allowed. Removing each equation must enlarge the complete solution set.

The accepted partial results are:

1. A hypothetical independent triple with a common nonperiodic solution has at most one equation admitting an erasing deletion witness.
2. If it has a common erasing nonperiodic solution, no equation admits an erasing deletion witness.
3. A balanced three-variable system with a common nonperiodic solution and a member equivalent to pairwise commutation has an equivalent subsystem of at most two original members.

These statements leave the difficult nonerasing-witness cases open. They do not exclude common erasing nonperiodic solutions. The two-erasure mechanism is attributed to Holub–Žemlička (2015), Lemmas 15–16. The balanced reduction uses Saarela (2024), Lemma 4.4. `PROOF.md` contains the complete argument and public citations.

## Terminology correction

The supplied `PROOF_CLARIFICATION.patch` has been applied exactly to `PROOF.md`. The two-word criterion now refers to an indexed morphism on two distinct formal letters: injectivity holds exactly for noncommuting images. This includes equal and empty images correctly. The three-profile heading explicitly concerns **nonperiodic erasing** morphisms. No theorem, hypothesis, or proof inference was changed. The original and clarified proof identities are recorded in `ACCEPTANCE.json`; the patch records the original wording as authored correction history.

## Finite evidence and limits

The two finite searches found no independent triple on their stated pools: side length at most 8 with 216 binary nonerasing morphisms of image lengths 1–2, and side length at most 7 with 2,744 binary nonerasing morphisms of image lengths 1–3. Their 157,800 and 28,216 equations induce 5 and 15 signatures; all 10 and 455 distinct-signature triples fail the pool-specific independence condition.

This does not rule out longer or nonbinary deletion witnesses even for the searched equation lengths. It does not address all longer equations or systems whose common nonperiodic solutions are all nonerasing. Computational restrictions are not universal bounds. The written proof, not finite testing, supports the partial theorem.

## Review and source boundary

This is AI-assisted authored mathematical exposition with an independent internal AI mathematical, source, and computational audit. It is unrefereed. “Accepted” refers to the scope of that internal audit; it does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification.

The original source-check and audit records are dated 10 October 2026. `SCOPE_AND_SOURCES.json` and `SOURCE_VERIFICATION.json` retain public source titles, URLs, PDF hashes and sizes, and recorded inspection scopes. Independent URL opens establish public availability and work identity; they do not assert a separate byte-identical live download. Preparing this edition adds no source retrieval, inspection, or literature search. No exhaustive claim about later literature is made.

## Contents and integrity

- `PROOF.md`: complete proof with the accepted terminology correction
- `PROOF_CLARIFICATION.patch`: exact authored correction patch
- `AUDIT.md`: complete substantive mathematical and computational audit
- `ACCEPTANCE.json`: accepted claims, exact finite scopes, exclusions, and review boundary
- `REPORT.md`: original bounded research report
- `SCOPE_AND_SOURCES.json` and `SOURCE_VERIFICATION.json`: public source/scope and audit metadata
- `VERIFICATION_SUMMARY.md`: computational, source, and integrity verification boundaries
- `MANIFEST.json`: exact public membership and hashes of the other nine files

The original sealed candidate and audit packages remain unchanged. This edition includes authored prose, an authored proof correction patch, and public metadata only. It does not include copied scholarly source documents, executable reconstruction code, raw signature data or certificates. Reported computational verification is documented here; this edition alone is not an executable reproduction package. The manifest's own digest is supplied separately to avoid self-reference.
