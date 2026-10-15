# Rank-one bimatrix equilibrium uniqueness

## Accepted result

For explicitly listed rational payoff matrices A and B of variable dimensions with rank(A+B)=1, deciding whether there is exactly one mixed-strategy Nash equilibrium pair is coNP-complete. Arbitrary degeneracy is allowed. The hardness construction supplies a known strict pure equilibrium and has another equilibrium if and only if the input PARTITION instance is yes.

This edition addresses problem 30003934, /OWR-16413-005, priority rank 1171. The first substantive approach reached the stated theorem. It does not establish hardness under a promise that the entire game is nondegenerate.

## Reading order

1. [The proof](PROOF.md) gives the complete reduction, including the perturbation that controls every optimal flow, injective simplex embedding, uniform exact penalty, exact rank-one construction, strict default equilibrium and polynomial encoding bounds.
2. [The certificate report](certificates/LEMMA_REPORT.md) proves polynomial-size rational witnesses for two distinct equilibria, including degenerate and positive-dimensional equilibrium sets, and therefore the coNP membership needed to complete the theorem.
3. [The full independent audit](independent_audit/AUDIT.md) records the initial conditional decision and every mathematical qualification and requested correction.
4. [The final independent acceptance](independent_audit/FINAL_ACCEPTANCE.md) accepts the exact frozen proof after those corrections. [The edition acceptance](ACCEPTANCE.md) explains the chronology and binds all four preserved documents to their hashes.
5. [Attribution](ATTRIBUTION.md), [source metadata](SOURCE_PROVENANCE.json), and [edition provenance](PROVENANCE.md) separate the established source methods from the present argument and describe the bounded literature check.
6. [Status](STATUS.json) records the scoped disposition. [The manifest](MANIFEST.json) records the exact edition members and their byte identities.

## How to read the historical headers

The proof's candidate/pending header is preserved to keep the accepted manuscript byte-for-byte identical. It is historical: the subsequent final acceptance expressly accepts its exact SHA-256. Likewise the audit's initial conditional verdict concerns the earlier draft, and the certificate report supplies membership rather than claiming to contain the later reduction. The edition does not silently rewrite any of these chronological records.

The proof and audits mention historical finite checks and auxiliary filenames. Those discussions remain part of the written record, but the checking scripts, fixtures, separate results and logs are not distributed. The theorem rests on the complete written proof and certificate argument, not on executing any software.

The mathematical and source reviews are AI-assisted research audits, not external human peer review, journal acceptance or proof-assistant verification. The bounded source search makes no novelty, historical-priority or present-open-status claim. This addition contains no queue edit and no unrelated repository change.
