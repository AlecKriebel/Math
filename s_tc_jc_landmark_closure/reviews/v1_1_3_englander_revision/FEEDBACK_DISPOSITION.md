# Englander-v4 and release-package feedback disposition

Date: 2026-08-17
Status: **ADOPTED WITH ONE BOUNDED SUBSTITUTE**

The supplied Englander et al. v4 PDF was treated as a source, not as an
instruction document. Its SHA-256 is
`3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5`.

| Feedback | Disposition | Reason/action |
|---|---|---|
| Identify Omega as two differently labelled type-(2c) quarnets | **Adopted** | Figure 5 and Lemma 2.14 confirm that type-(2c)-versus-type-(2c) is not covered. The manuscript paragraph and Figure 6 caption now give the exact crosswalk. |
| Use leaf-coordinate permutation for equal Omega dimensions | **Adopted** | This is cleaner and avoids transporting the displayed Euler identity through unspecified edge indices. |
| Print all rank-nine row/column sets | **Adopted** | Supplement section 5 now lists the common orbit rows, both zero-based column sets, all four exact determinants, and the parameter order. |
| Rename the trinet invariant and explain `q123`/`q111` | **Adopted** | The article now uses `I_tri`; it records Englander et al.'s collapsed notation explicitly. |
| Cross-reference the no-omnian criterion | **Adopted** | Definition 2.3 is cited while retaining the self-contained fixed-`sd_0`, binary LSA proof. |
| Add the quartet-distance paper | **Adopted** | The published 2025 article and its distinct combinatorial/galled scope are now cited. |
| Repair supplement notation and path convention | **Adopted** | Polynomial/state-group notation is disentangled and all evidence paths are monorepository-root-relative. |
| Note the explicit Omega dimension deficit | **Adopted** | Added narrowly as one explained instance, without claiming a general solution. |
| Import and replay the entire external Englander computer archive | **Not made a theorem dependency** | The manuscript's claims require only an exact literature/taxonomy crosswalk. Importing a second large computational universe late in the release would add supply-chain and convention risk without proving the present atlas. A fail-closed local regression instead checks every Englander statement actually used and the exact Omega record. |
| State the four-leaf origin of both all-taxon families | **Adopted** | Added once in the theorem overview. |
| Put verifier scripts in each submission-support package | **Adopted with journal-specific routing** | bioRxiv receives the small verifier-entrypoint ZIP.  The Systematic Biology and JMB directories retain identical capsules for the external repository deposit, but their upload maps follow each journal's policy rather than sending those ZIPs to the manuscript portal.  The complete graph/certificate archive and clean transcripts remain in the immutable GitHub Release, avoiding a redundant hundreds-of-megabytes portal upload. |

No DOI was created, requested, or inserted by this revision.

## Adversarial release closure

Two successive reproducibility reviews returned `FAIL` and are preserved as
`ADVERSARIAL_REPRODUCIBILITY_REVIEW_INITIAL_FAIL.md` and
`ADVERSARIAL_REPRODUCIBILITY_REVIEW_SECOND_FAIL.md`.  Their findings forced
repairs to the deterministic source-build environment, exact annotated-tag
byte/mode binding, journal-specific capsule routing, clone-versus-archive
commands, stale-size wording, and current manifest coverage.  A third fresh
read-only review then rejected seventeen targeted mutation classes and ended
`PASS`; see `ADVERSARIAL_REPRODUCIBILITY_REVIEW.md`.  The independent
mathematical review separately ended `PASS`.
