# Audited partial: generic integral subgroups and an SL3 Haar calculation

Problem 30002904 / OWR-13687-003; rank 864. **Canonical status: unsolved / 5/5.**

The unchanged [author proof](author/proof.md), [first mathematical audit](audit/audit.md), [independent finite-radius derivations](audit/independent_derivations.md), [second audit](second_review/audit.md), and [second derivations](second_review/derivations.md) are accepted only within their stated scope. Both [first acceptance](audit/acceptance.json) and [second acceptance](second_review/acceptance.json) require no mathematical correction.

## Accepted scope

- The known SL2(Z) ordinary operator-ball subcase is proved using the cited counting input, with finite-index probability at most X^(-1+o(1)).
- For fixed s >= 0, normalized Haar measure in the ordinary operator-norm radius-X ball in SL3(R) has limiting top-gap tail 2 exp(-2s) - exp(-4s), where the gap is log(sigma1/sigma2) and the sigma values are ordinary positive singular values.
- At the threshold sigma1/sigma2 >= eta^2, the limit is 2 eta^(-4) - eta^(-8). This exceeds the eta^(-4) numerical upper bound in Fuchs–Rivin Theorem 3.4 for eta > 4, under the intended limit-of-normalized-volumes interpretation. The literal separate infinite limits do not define a quotient. The explicit KAK decomposition resolves nearby inconsistent squared-eigenvalue terminology.
- The continuous inverse-bounded-to-ordinary Haar-volume ratio is asymptotic to 6 X^(-2). Exact finite-radius formulas appear in the audits.

These conclusions do not transfer to SL3(Z) here and do not solve the original probability-one question for fixed n >= 3. No general-n repair, novelty certification, exhaustive literature-status assertion, or verdict on the separate inverse-bounded thinness theorem is made.

## Preservation and verification

All three immutable data-only ZIP archives, their 19 extracted members, external manifests, and stage receipts are preserved byte-for-byte. Historical fields such as “audit pending” or “publication not performed” describe the original frozen stage and remain unchanged. The present acceptance is stated above and in PUBLICATION_METADATA.json.

PUBLICATION_SOURCE_BINDINGS.json records fresh checks of the three complete retained corpora, complete target-record bindings, and five retained scholarly files. Only hashes, byte counts, match results, titles, public URLs, and inspection history are included. No source documents, source-page images, extracted source text, raw dataset records, private coordination files, or executable code are published.

PUBLICATION_VALIDATION.json records isolated normal/optimized, relocated, and hostile-input checks of the immutable archives. PUBLICATION_MANIFEST.json binds every other package file. The exact-commit receipt on the draft PR records remote byte readback and the manifest's external hash. Data checks and symbolic diagnostics are not proof certificates; the authored mathematical audits carry the acceptance.

Five approach families are disclosed in the frozen status file; publication adds no proof attempt and does not independently certify their historical chronology.
