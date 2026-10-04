# Audited candidate: Knill item 10

Problem 4200010 / AMR-041-0010. Manuscript status: `claimed_solved`, 2/5 substantive approaches. AI-assisted and unrefereed; independently audited by an AI reviewer, without human peer review or a historical novelty claim.

## Result and exact scope

The candidate constructs a connected compact smooth symplectic four-manifold and a global autonomous real Hamiltonian with an invariant open band of normalized Liouville volume 1/4. All four Lyapunov exponents vanish on that band, and no positive-measure invariant part has an almost-periodic Koopman representation. Each individual energy component in the band also fails almost periodicity.

The ambient symplectic form is nonexact: it has positive integral on a torus fiber. This is a result in the unrestricted smooth symplectic category. It makes no claim for standard Euclidean phase space, an exact cotangent form, analyticity, a natural kinetic-plus-potential Hamiltonian, contact-type energies, robustness, genericity, or weak mixing. The suspension actually has a clock eigenfunction, so it is not weakly mixing.

Here almost periodicity means precompact Koopman orbits for every L2 observable. The 2000 source does not provide a formal definition. The audit documents corroborating terminology in Knill's 2016 primary source and an additional pointwise Bohr almost-periodicity check; neither is represented as a formal definition supplied by the 2000 problem itself. These qualifications are part of the claim, not optional editorial detail.

## Preserved files and review

The original 12-file candidate is preserved byte-for-byte under `submission/`. Its original status files correctly describe the state at author freeze; subsequent independent review is documented separately under `audit/`, whose 11 files are also unchanged.

- Candidate manifest SHA-256: `0e82b3cd57b31613728a1c61cc2eef4c911651b805dbea6ad56dab40736869ad`
- Candidate proof SHA-256: `541bc3c95d8f04b1d89cac3d2af21815ab331c7eeff9d79ff3591ba8f53eabd1`
- Audit manifest SHA-256: `5dd45dcd47faf43074f7aad2eeb8569d573c7c60c5b3704bf94b3ce38a435239`

The independent audit accepted the complete construction within the stated scope, with no mandatory proof corrections. It did not certify historical priority. The elementary skew-shift and mapping-torus ingredients are classical.

## Reproduce in this final layout

From this directory run:

```
python3 submission/verify_manifest.py
python3 audit/verify_audit_manifest.py
python3 audit/run_audit.py submission
```

The author replay passes 3,248 exact checks and six controls. Independent replay passes 2,460 further exact checks and eight additional controls. Four strict-manifest mutation controls reject an edited proof, an extra file, a missing file, and a same-content symlink. All original bytes remain unchanged after replay. The analytical proof and audit establish the infinite-dimensional, measurable, and asymptotic steps; the finite check counts are supporting coverage metadata, not formal proof certification.

## Sources and publication limits

Primary problem list: https://people.math.harvard.edu/~knill/seminars/intr/ , item 10, talk dated 19 October 2000. The source inspection history and exact retrieval limits are in `submission/SOURCE_MANIFEST.json` and `audit/SOURCE_CHECKS.json`.

This release contains only authored proof, authored analysis, code, and verification metadata. Source PDFs, scholarly full text, dataset contents, and private coordination material are excluded. This is a draft research PR, not a merged result, a release, a DOI deposit, or an outreach action.
