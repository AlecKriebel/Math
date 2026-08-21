# Independent referee audit log

## Scope

Adversarial mathematical and reproducibility audit of *Strong Tree-Childness Is the Sharp Identifiability Boundary for Level-2 Jukes-Cantor Networks*, its supplement, source package, and certificate archive v1.1.5.

The target conclusion is treated as a hypothesis. Passing scripts are not accepted as mathematical evidence unless their outputs are traced to primitive inputs and independently regenerated.

## 2026-08-20 20:55 PDT - Checkpoint 1: archive authentication

- Computed SHA-256 of `stc_jc_sharp_boundary_atlas_certificates_v1.1.5.tar.gz`:
  `66f0e324b9cdb1448806eecd9cd9397f9e8c45f4762ff48c5750cd64d2938e6a`.
- The value exactly matches the separate `.sha256` file and `archive_sha256` in `CERTIFICATE_BUNDLE_ENVELOPE.json`.
- Computed byte count is 79,567,059, exactly matching `archive_bytes` in the envelope.
- `gzip -t` succeeded; all tar member names are relative and traversal-free; the archive contains no symbolic-link members.
- Trust boundary: the supplied envelope has no digital signature or independently resolved publication identifier (`zenodo_doi` is `ZENODO_DOI_PENDING`). Authentication therefore proves consistency with the supplied sidecar files, not external provenance or authorship.

Best-guess completion: **4%**.

## 2026-08-20 - Checkpoint 2: complete reading and theorem reconstruction

- Read the complete 31-page manuscript and 7-page supplement, including all stated proofs, appendices, certificate claims, and interpretation limits.
- Rendered and visually inspected every PDF page; no page-layout or formula-rendering failure was found.
- Reconstructed the exact object class, open parameter domain, directed and symmetric observational relations, positive theorem, sharpness theorem, and proof dependency graph in `notes/SCOPE_AND_DEPENDENCIES.md`.
- Directly checked the algebraic identities in the two-active-endpoint argument and the dimension counts in the localized Theta locus. These checks are consistent, but the finite certificate premises remain unaudited at this checkpoint.
- Recorded a reproducibility/provenance limitation: the paper and supplement still cite a pending Zenodo DOI, and the supplied envelope is not independently signed.

Best-guess completion: **22%**.

## 2026-08-20 21:15 PDT - Checkpoint 3: written-proof and certificate semantics

- Traced the cut, bridge, finite-cover, localization, marginalization,
  restoration, probe, triangle, Omega, and Theta arguments through their
  primary and separately implemented certificate programs. No theorem-level
  counterexample has been found.
- Found a normalization/crosswalk defect in the two-active-endpoint account.
  The article defines `Gamma` after removing the physical central arm, but the
  archived endpoint replay checks `G=a-bc` before that removal. The needed
  weak normalized inequality follows by letting the independent central-arm
  multiplier tend to one. Direct evaluation of all nine `Delta=0` records
  gives seven normalized zero cases and two strict cases, so the proof's
  dichotomy survives, while its claim of nine strict normalized `Gamma`
  records does not.
- Found a reproducibility defect in
  `reviews/root_probe/verify_parameter_submersion.py`: it partitions physical
  edges by raw descendant-mask rows, not by the split/complement-normalized
  zero-sum JC indicator signatures stated in Lemma 6.2. An independent
  in-memory census of all 42,908 generated completions found that every raw
  class count changes under the required normalization, by one to four
  classes. The program also defines the claimed rank and target dimension by
  the same expression, making its zero-failure test tautological. The written
  positive-product argument remains valid for the corrected disjoint
  partition, and the load-bearing hard-cover and clean-room relation engines
  do use the corrected normalization.
- Found a second non-load-bearing certificate defect in
  `verify_probe_coherence.py`: the purported prediction key already contains
  the full two-port code that it then predicts. The zero-collision result is
  therefore vacuous. The actual direct-anchor and compact semantic gates
  independently regenerate all one- and two-port extensions and enforce
  parent-restricted transports, so this does not defeat the coherent-probe
  theorem.
- Confirmed exact graph-to-switching-to-Fourier regeneration, direction and
  port binding, complete raw-presentation coverage, strict-sign checking,
  restoration transitions, and mutation sensitivity in the active primary
  and clean-room atlas gates. The clean-room graph and sparse-polynomial
  representations are genuinely separate from the primary implementation.

Best-guess completion: **72%**.

## 2026-08-20 21:24 PDT - Checkpoint 4: full eight-port cut-word census

- Detected that `independent/bridge_cut/verify_cut.py` tests only the five-word
  per-segment palette `(), (0), (1), (0,1), (1,0)` plus a narrow singleton
  duplication, despite the manuscript's claim that every at-most-eight-port
  compressed two-colour completion is checked. The script refers to an
  arbitrary-subdivision proof in a nonexistent `PROOF.md`; no palette-reduction
  argument exists elsewhere in the archive.
- Added the audit-only exhaustive program `work/core_extended_word_census.py`.
  It enumerated all 808,642 balanced binary-word configurations with four to
  eight active ports across the cycle and all four theta cores in root and
  nonroot modes. Of 479,374 valid standard-strong configurations, only 85,974
  are represented by the archived palette and 393,400 are omitted.
- No valid configuration, covered or omitted, had its noncut colour split
  displayed by every switching. Thus the mathematical one-active handoff is
  true on the complete stated finite universe, but the frozen certificate's
  exhaustiveness claim is false and should be repaired by incorporating this
  expanded census (and a separate replay) or a genuine verified reduction
  lemma.
- Completed the detailed core proof report in `notes/core_proof_agent.md`,
  including exact page/source/code locations, theorem scope and dependencies,
  the all-nine endpoint normalization repair, and audits of the bridge fibre,
  finite-cover localization, marginal restoration, triangle gluing, and
  genericity.

Best-guess completion: **82%**.
