# Ordinary thick closure of representation spheres

Problem 20000157 · AIM Problem 2.5 · 11 October 2026

**Disposition: accepted partial result.** For a finite group in the compact, complete-universe genuine equivariant category, the ordinary thick closure of representation spheres is the whole compact category exactly for elementary abelian 2-groups. The packet also gives the complete rational closure, exact integral membership of orbit spectra, and explicit rationally invisible integral obstructions.

The equality criterion and rational closure are inherited results. This is an AI-assisted reconstruction and mathematical audit, with no discovery or priority claim, independent human referee review, or proof-assistant formal certification. The unrestricted original AIM question is not declared solved.

## Read the complete result

- [PROOF.md](PROOF.md): full derivation, including the coordinate-cell argument, rational Weyl orientation-line classification, Moore-spectrum obstruction, internal smash lemma and exact orbit criterion in Section 6.
- [AUDIT.md](AUDIT.md): complete proof-obligation audit, corrections, source dependencies and exact remaining gap.
- [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): accepted statements and limits in concise form.
- [ACCEPTANCE_SCOPE.json](ACCEPTANCE_SCOPE.json): machine-readable acceptance boundary and binding to the accepted and public proof bytes.
- [PUBLIC_SOURCE_METADATA.json](PUBLIC_SOURCE_METADATA.json): five public primary-source records with URLs, inspected versions, exact sizes and SHA-256 hashes, and retrieval/inspection history.
- [VERIFICATION_METADATA.json](VERIFICATION_METADATA.json): aggregate finite-check results, input-integrity checks and individual upstream allowlist decisions.
- [EDITORIAL_PROVENANCE.json](EDITORIAL_PROVENANCE.json): exact public replacements, original-text hashes and byte-identical mathematical-region pins.
- [MANIFEST.json](MANIFEST.json): closed inventory and hashes of all other public files.

## Precise boundaries

“Thick” means finite sums, cofibers, integer suspension/desuspension and retracts. A separate lemma proves internal smash closure for two members; it does not assert tensor-ideal closure under arbitrary compact spectra.

In each rational subgroup factor H, the allowed Weyl-group lines are exactly the determinant characters of H-fixed spaces of global virtual representations. The result does not assume that every Weyl sign character extends globally. Actual and virtual generators give the same rational closure; their integral closures are not compared for every other finite group.

Orbit membership is settled: G/H-plus belongs exactly when H is normal and G/H is elementary abelian of exponent two. Membership of arbitrary compact integral spectra outside the elementary abelian case remains unclassified. Rational membership alone is insufficient, even for rationally zero compact objects.

The argument imports the explicitly cited Barnes, Greenlees–Quigley and Mathew–Naumann–Noel results; their entire proofs are not re-proved here. No compact Lie, profinite or naive-equivariant classification is claimed.

## Verification and content boundary

The accepted audit and supporting frozen inputs were rechecked without alteration. All five captured source sizes and hashes match. The finite-check program was rerun in normal, -O and -OO modes with identical outcomes. These tests supplement the general prose proofs and do not certify them formally.

This public directory contains authored mathematical reports and public verification metadata only. It excludes the source documents and extracted text, source-page images, dataset contents, raw group/subgroup/face records, executable scripts and private coordination files. Publication preparation is not evidence of publication, peer review or acceptance by an external venue.
