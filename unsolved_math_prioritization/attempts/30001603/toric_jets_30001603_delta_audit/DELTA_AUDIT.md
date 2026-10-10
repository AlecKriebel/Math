# Corrected-release delta audit: problem 30001603

Audit date: 2026-10-05 UTC. Target: rank 698, ID 30001603 / OWR-4527-007, Jet Spanning by Nef Toric Vector Bundles.

## Final verdict

**PASS. Accept the exact corrected packet as an attributed prior negative resolution, disposition `already_solved`, 1/5 substantive author turns.**

The original audit's mathematical conclusions stand. The corrected source descriptions now accurately state that the DJS journal and arXiv v3 both print (-1,-2) for the e1-e2 polygon vertex. The deliberately false (-1,2) coordinate is consistently identified as a synthetic negative control. The sole blocking source-description issue has been resolved. No mathematical inputs or results changed, and there are no outstanding mathematical or source-description corrections for these exact bytes.

This acceptance is specific to the corrected packet and release hashes below. It is not an acceptance of the original erroneous packet, an assertion of novelty, human peer review, or a claim that unavailable full-corpus contents have been inspected.

## Exact acceptance binding

- Corrected packet MANIFEST.json: 670f3a5365201fdcda372dbd6037aefb062cda2a7dd3537522a19c4a5204fe55
- Corrected PROOF.md: 1ae5a43cbf52ba23c3b39a99a4d5c4c376305edb375a0b343da935e8328210ed
- Corrected RELEASE_MANIFEST.json: 506886489cb3eba4235fa555b4d3fb6c5b46dcb8d2b6b577576f8419e2b17a9e
- CORRECTION_BINDING.json: 57555649b4d5b980e55ac55cb02cf6f48b1a276eddb4c54212d84b15156cef1d
- Complete original audit MANIFEST.json: efd9065e283904c34c9f3c863e85b159945186e504c6c3657d5a2547078935d1
- Complete original AUDIT.md: a72e3af8b95a7a0e1c3996777606169ea3539780c475d6301ae1562e90d2730e
- Original CORRECTIONS.md: 309fe21ea139fea48ecc847223ca5fbb9a58499b3943db223bc892ae8dea4d55

EXACT_ACCEPTANCE.json lists every corrected-release file, byte count, and SHA-256. All 17 release files, all ten original packet files, and all nine original audit files were verified and preserved. Hashes bind content; they are not digital signatures.

## Complete diff and source-description review

The entire supplied 14,934-byte unified diff was read and independently regenerated from the old and new bytes. The regenerated diff agrees exactly. Nine packet files changed; CHECK_PACKET.py is byte-identical. The changes follow the original correction map:

1. PROOF.md changes only lines 3, 117, 119, and 121: source agreement in the introduction; synthetic-control wording; the agreement heading; and the correct source-coordinate paragraph. All construction, positivity, global-section, and jet arguments remain unchanged.
2. SOURCE_GATE.md changes only its heading and coordinate paragraph. It explicitly attributes the earlier false allegation to the original verification packet and states that the scholarly source is not being corrected.
3. README.md replaces only its incorrect typo paragraph with source agreement and a synthetic-control description.
4. APPROACH_LOG.md replaces only the sentence alleging a published error. The single mathematical approach and prior-result stopping rationale are unchanged.
5. SOURCES.json changes only the journal inspection description. Source URLs, PDF hashes, byte counts, dates, and other inspection records are identical.
6. STATUS.json changes only the relevant limits entry. The result, counterexample data, substantive turn count, novelty boundary, and unavailable-source limits are unchanged.
7. VERIFY.py changes one comment and four descriptive string literals: two assertion labels, one output key, and its value. After substituting only those four strings, the old and new abstract syntax trees are identical. No condition, integer, vector, loop, routine, or expected mathematical quantity changed.
8. RESULTS.json was regenerated exactly from the corrected verifier. Removing the old metadata key from the original output and the new metadata key from the corrected output yields identical JSON. There are still 79 author checks with the same numerical results.
9. MANIFEST.json correctly updates member hashes and byte counts. Its schema and scope are unchanged.

Search and direct reading found no surviving affirmative allegation that the journal prints the wrong sign. Historical mentions in the correction history and removed lines of the diff are explicitly historical, not renewed claims against DJS. The source-consistent (-1,-2) and deliberately invalid (-1,2) coordinates remain correctly distinguished everywhere in the current packet.

The descriptions agree with the already authenticated scholarly source inspection: journal PDF SHA-256 29d020ccdfffbb91149ed6d72bd3c32306865dc7d4f503bbf581d241b32d0a2b, 365,988 bytes, printed p.7728 / PDF page14; arXiv v3 SHA-256 adb8e9d5c9fbf2d8bb9d5f9f811e126be277f92b69de8b49af6861b16695f991, 390,326 bytes, p.13. The full audit records the rendered-pixel and text checks. No source payload is redistributed here.

## Computational revalidation

VERIFY_DELTA.py performs 115 checks of exact input bindings, full manifest membership, correction-map dependencies, changed-line scope, source metadata, verifier AST equivalence, generated outputs, and preservation of all three input trees. The corrected author's CHECK_PACKET.py passes and reproduces its recorded output exactly, including the three temporary-copy integrity controls. The author's separate correction validator also reproduces its recorded output byte for byte.

The independent mathematical verifier from the earlier audit is itself bound by SHA-256 65a036d7000e89423557d5039c858087467a5115102629b1c5ba73aeba472719. It was rerun in memory against the corrected packet, rebinding only the manifest/proof anchors and two result-description strings. Its mathematical code was unchanged; the earlier audit files were not edited.

All 60 independent checks and eight anchored corruption controls pass on the corrected packet. The full independent calculation still gives:

- Regular invertible equivariant chart transitions and all cocycles
- Invariant-curve splitting degrees (4,3,1), (5,2,1), (6,1,1)
- tau = 1
- An exhaustive 52-variable polynomial-extension system with 88 equations, rank40, nullity12
- Exactly twelve global sections
- Value ranks (3,3,2)
- First-jet ranks (9,9,7)
- The missing middle value and middle y-derivative directions at the bad fixed point

The independent controls still reject incompatible local weights, a broken transition cocycle, a false constant section, and the synthetic vertex sign flip. The O^3, O(1)^3, and O(-1)^3 controls retain their expected behavior. All eight temporary-copy corruption cases are rejected. Original files and corrected files are unchanged after replay.

## Mathematical conclusion and scope

The original full audit supplies the geometric proof, not merely finite tests: the chart modules glue to a genuine locally free toric bundle on P2 over C; the invariant-curve restrictions prove tau = 1; the credited torus-degeneration argument establishes nefness; and the explicit section computation proves failure of value generation, hence failure of first-jet spanning. The complete original OWR contribution has no additional global-generation assumption. Its field, smoothness, completeness, projectivity, and k >= 1 conditions all permit this example at k = 1. Therefore the original universal implication is false by the published DJS example. Ampleness is also supported by the credited HMP theorem but is not needed for the refutation.

This source-description repair is not another mathematical approach, so the recorded 1/5 substantive author turns remains appropriate. The proof and controls continue to disclaim novelty and proof-assistant certification. The live problem page was inaccessible with HTTP403, and the old selected full corpus/AI record remains uninspected; no new full-text hash-match claim is introduced. The descriptor identity and authoritative primary statement remain the basis of identification.

The corrected packet and release controls still contain the pre-review word “pending” in their historical preparation status. That was truthful when frozen. This separate exact-bound acceptance completes the pending review for these hashes; those immutable preparation records need not be edited merely to overwrite their history. Any later content change requires a new binding and review of the changed scope.

## Release boundary

The source-description gate is closed for this exact release. The original freeze and original critical audit remain preserved as provenance. Public delivery should identify the corrected packet and this acceptance, rather than presenting the erroneous original packet as the accepted proof. Source PDFs, extracted text, rendered images, full catalogue data, raw selected records, and private coordination files are excluded. This audit performed no remote writes and does not itself attest to any later upload, commit, PR, merge, or publication.
