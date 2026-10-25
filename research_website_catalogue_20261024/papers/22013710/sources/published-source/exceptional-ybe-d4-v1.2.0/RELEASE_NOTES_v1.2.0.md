# Version 1.2.0 — concurrent-work revision

Status: **DOI-bearing archival release; arXiv and journal submission pending**

Date: 19 August 2026

Version 1.2.0 is a scholarly update prompted by the independent concurrent
preprint of C. Galindo and E. C. Rowell, arXiv:2608.16865v1. It does not alter
the historical version-1.1.0 GitHub release or the dedicated version-1.1.3
Zenodo record.

## Manuscript changes

- Extended the continuous title with the subtitle “a five-word
  Pauli–Clifford normal form.”
- Added a neutral note documenting the earlier public v1.1.0 release, the
  later Galindo–Rowell arXiv timestamp, their reported earlier private work,
  and the independent-concurrent-work framing.
- Added an intrinsic quaternionic Family III factorization of the existing
  `(M,E)` construction, including the essential factor `-i` in
  `U_K + V_K + U_K V_K = -i sqrt(3) H`.
- Added an exact local-unitary comparison between the Pauli–Clifford operator
  and the opposite of the literal Galindo–Rowell Family III operator. The
  theorem displays the four-dimensional unitary `S` and makes the site
  reversal explicit.
- Distinguished the new 16-by-16 ordinary operator `R_GR` from the older
  8-by-8 GHR Equation (5.2) generalized operator `K_GHR^gen`.
- Replaced sole-novelty language with a comparison of the two independent
  proof architectures and retained the existing limitations.
- Proved a scalar Turaev enhancement and identified the enhanced matrix trace
  with `2 P_H(L;i,i)`.
- Proved the exact all-strand unitary equivalence using tensor-site reversal
  and the Garside half twist.
- Added finite-image, conjugated-Clifford-frame, quaternionic-tower, and exact
  deterministic polynomial-time consequences with audited source locators.
- Added the exact Lickorish--Millett triple-cyclic-branched-cover formula after
  a direct primary-source normalization and parity audit.
- Clarified which Section 9 conclusions are direct calculations and which are
  transported from established Family III results. Added an exact
  standard-frame non-Clifford witness and exact figure-eight and Borromean
  trace checks without changing any theorem or formula.

## Verification changes

- Added `verify_concurrent_equivalence.py`, a separately written
  standard-library verifier over `Q(sqrt(2),sqrt(3),i)`.
- Added exact checks of the intrinsic quaternionic relations, unitarity of
  `S`, the generatorwise comparison, and the full site-reversed operator
  identity.
- Added deliberate failures for a sign of `S`, omission of the site swap,
  conjugation of `zeta`, a wrong tensor placement, and omission of the `-i`
  factor.
- Added and froze a standalone successful transcript, and integrated the new
  route into `run_all.sh`.
- Added `verify_braid_link.py`, including exact enhancement, skein, local-order,
  low-link, Clifford, global reversal, and Garside checks at `n=3,4`.
- Added six global-structure mutations for quarter-turn order, writhe phase,
  `kappa`, skein sign, reversal index, and Garside word.
- Added a deliberate sign mutation for the printed standard-frame witness.

## Provenance and handoff changes

- Added `CONCURRENT_WORK_AND_CHRONOLOGY_v1.2.0.md` with source-backed UTC
  chronology, historical hashes, and the ten mathematical contents already
  present in v1.1.0.
- Added a Journal of Algebra cover-letter draft and private, gated email
  drafts for human use; all operational handoff documents remain local and
  are excluded from the public source ZIP.
- Added source tables and a line-by-line Turaev/Lickorish--Millett
  normalization audit.
- Updated Zenodo, arXiv, journal, citation, website, and package metadata for
  version 1.2.0 and completed the DOI-bearing freeze with reserved version DOI
  `10.5281/zenodo.22013710`.
- Rebuilt deterministic PDF, source, and arXiv artifacts and refreshed every
  checksum after all exact and adversarial checks passed.
