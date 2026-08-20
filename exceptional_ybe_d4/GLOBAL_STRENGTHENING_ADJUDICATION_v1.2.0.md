# Global strengthening adjudication — version 1.2.0

This record adjudicates the final global-braid-and-link strengthening program.
All work occurred in private staging. No repository push, release, DOI
reservation, submission, or external communication was performed.

## Accepted and implemented

- Removed chronology from the abstract and kept one neutral Introduction note.
- Preserved the complete direct localization and minimality proofs.
- Added the missing cyclic trace equality and the complemented Markov
  calculation.
- Distinguished `K_GHR^gen` from the 2026 ordinary operator `R_GR`.
- Added skew-Hermitian unitarity of `U_K,V_K` and softened the site-reversal
  discussion so it does not claim necessity.
- Proved the scalar Turaev enhancement and exact matrix-trace invariant.
- Derived the matrix skein identity, the specialization
  `J_R=2 P_H(i,i)`, mirror invariance, and unlink values.
- Proved `R^3=-I`, `R^6=I`, and local three-/six-twist periodicity.
- Proved the reflected generator identity and same-word all-strand unitary
  equivalence using the Garside half twist.
- Transferred finite-image, Clifford-frame, quaternionic-tower, and exact
  deterministic polynomial-time consequences with exact source locators.
- Included the triple-cyclic-branched-cover formula only after the original
  Lickorish–Millett convention and parity proof passed audit.
- Added an independently written exact braid-and-link verifier and hostile
  mutations.
- Revised metadata, release materials, cover letter, website draft, and the
  gated post-publication email draft.

## Suggestions rejected or narrowed

- No direct local-unitary inequivalence to `R_GR` is claimed; the proof only
  exhibits equivalence to the opposite and then an all-strand conjugacy.
- No all-`n` finite image group is named.
- No claim that `S` belongs to the standard computational Clifford group is
  made.
- Polynomial-time evaluation is sourced from the exact Family III algorithm,
  not inferred from the `4^{n-1}`-dimensional tower.
- The classical HOMFLYPT and branched-cover evaluations are credited and are
  not presented as new.
- Detailed chronology is not repeated in the abstract, conclusion, or related
  work.
- The Introduction does not add the phrase “earlier documented public
  disclosure”; the dated public record is allowed to speak for itself, as the
  strengthening program requested.
- Galindo--Rowell are credited with dimension four being smallest in
  Lechner's exceptional family, not with the separate global dimension-three
  exclusion proved directly here.
- No private correspondence is quoted or included in the public source
  archive.

## Claims omitted for lack of scope or proof

- Uniqueness of the local operator.
- Necessity of site reversal.
- Emptiness of exceptional dimensions 6, 10, 14, and higher.
- Direct-sum or external-product closure/obstruction theorems.
- Universality claims involving measurements, ancillas, or nonbraiding
  resources.

## Historical preservation

The version 1.1.0 tag still resolves to
`e2669c5b2f99338c79381dc42bdbc61ee8b963c3`; its historical PDF SHA-256 remains
`af4ff57c4b8c5cd37f47f8a6da880b4f93b9c22d6e2908a3ef1f6ebf5fb1d049`.
The dedicated version 1.1.3 Zenodo record remains
`10.5281/zenodo.21971507`. Neither record was modified.

## Exact modified-file list for the global strengthening

The following tracked-path candidates differ from the preceding private
v1.2.0 draft. Generated files are included because they are part of the
frozen deliverable.

```text
README.md
docs/index.html
docs/papers/exceptional-ybe-d4/index.html
docs/papers/exceptional-ybe-d4/paper.pdf
exceptional_ybe_d4/ARXIV_METADATA.md
exceptional_ybe_d4/CHANGELOG_v1.2.0.md
exceptional_ybe_d4/CITATION.cff
exceptional_ybe_d4/CONCURRENT_WORK_AND_CHRONOLOGY_v1.2.0.md
exceptional_ybe_d4/GLOBAL_BRAID_SOURCE_AUDIT_v1.2.0.md
exceptional_ybe_d4/GLOBAL_STRENGTHENING_ADJUDICATION_v1.2.0.md
exceptional_ybe_d4/HIGHLIGHTS.txt
exceptional_ybe_d4/JOURNAL_OF_ALGEBRA_COVER_LETTER.md
exceptional_ybe_d4/MANIFEST.md
exceptional_ybe_d4/README.md
exceptional_ybe_d4/RELEASE_NOTES_v1.2.0.md
exceptional_ybe_d4/RESEARCH_LOG.md
exceptional_ybe_d4/SHA256SUMS
exceptional_ybe_d4/SOURCE_SNAPSHOT.md
exceptional_ybe_d4/SUBMISSION_CHECKLIST.md
exceptional_ybe_d4/TOPOLOGICAL_NORMALIZATION_AUDIT_v1.2.0.md
exceptional_ybe_d4/VERIFICATION_ENVIRONMENT.md
exceptional_ybe_d4/ZENODO_DEPOSIT.md
exceptional_ybe_d4/braid_link_output.txt
exceptional_ybe_d4/main.tex
exceptional_ybe_d4/output/pdf/exceptional_ybe_d4.pdf
exceptional_ybe_d4/run_all.sh
exceptional_ybe_d4/submission/ARXIV_SHA256SUMS
exceptional_ybe_d4/submission/SHA256SUMS
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0-arxiv.zip
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0-source.zip
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0.pdf
exceptional_ybe_d4/test_failure_modes.py
exceptional_ybe_d4/verification_output.txt
exceptional_ybe_d4/verify_braid_link.py
```

The human-only communication draft modified in the separate, excluded private
directory is `private_communications/REPLY_TO_GALINDO_AFTER_PUBLICATION.md`.
No private communication file is a source-archive member.

## Remaining human-only gate

The human author supplied reserved v1.2.0 version DOI
`10.5281/zenodo.22013710`. The remaining gate is to upload the matching
DOI-bearing files, verify the downloaded bytes and metadata, publish the
record, and only then perform any GitHub, arXiv, journal, or email action.
