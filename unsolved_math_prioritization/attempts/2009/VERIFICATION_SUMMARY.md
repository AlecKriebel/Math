# EP252 verification boundary

## Recorded audit, 10 October 2026

- Complete main manuscript: 20 pages read as text; pages 11, 12, 15, 16, 18 and 20 visually inspected in the recorded audit.
- Complete main Lean source: 60,831 bytes, 1,074 lines, 89 theorem declarations and 38 definitions/abbreviations.
- Main-source SHA-256: 784303a58ba3361669a236f5f7c5d38c68c352df8ccd3df9e46cc66149d42569.
- Main source and statement-audit bytes exactly matched the then-fresh pinned retrievals. The PDF was freshly retrieved and its 149,568 bytes matched SHA-256 ebb8a0f32a7b3dad418c7a0486f99f12d8de3705ae9e710f5cc608e66919a0ca.
- Ten directly imported Mathlib files were fetched at the exact official revision; definitions and key interfaces were inspected. This is not a transitive dependency audit.
- Historical public papers were read for the original problem, theorem statements and hypotheses. Complete independent historical-proof audits and exhaustive current-literature review are not claimed.
- Static screening found no lexical sorry/admit/native_decide occurrences and no custom axiom, opaque, unsafe, elaborator, macro, syntax or run_cmd declarations in the main module. This is not an axiom-closure or elaboration certificate.

## Historical finite controls

The independently authored standard-library-only finite checks passed under
normal Python, -O and -OO, with byte-identical result records. Their reported
counts were 630 divisor/phase cases, 972 Stirling-error cases, 819 polynomial-tail
cases, 7,200 affine-count cases, 16,200 prime-refinement cases, 7,873 coprimality
pairs and 326 grouped cancellations. Complete grids at k = 1, 2, 3 have 3, 16,
125 vertices. Four adverse examples detect dropping factorial spacing, squared
CRT moduli, signed finite-difference weights, or the prime requirement in the
mean-refinement identity.

These historical finite checks are bounded corroboration of identities and
indexing. They do not prove the universal theorem or establish any Lean build.
The general mathematical argument is preserved in full in MATHEMATICAL_AUDIT.md.
Executable programs, detailed test outputs and raw test datasets are omitted.

## Edition-preparation boundary

The preparation inspected and authenticated the existing authored reports and
public metadata, preserved their substantive mathematics, and checked byte
identities and the exact proposed file additions. These are packaging-integrity
checks. No new scholarly-source retrieval/inspection or mathematical test
execution was performed during this preparation. No external proof code, Lean
compiler, dependency build, installer or generated proof artifact was executed.

## Not independently established

FORMAL REPRODUCIBILITY HOLD remains in force: independent Lean compilation,
complete transitive compiler/dependency/kernel closure, final-theorem axiom
report and fresh kernel replay have not been obtained. There is no second
kernel implementation check, external human peer review, journal acceptance,
new-proof or novelty claim. The author-reported verification statements retain
their attribution. This AI-assisted authored audit is unrefereed.

The advertised SHA256SUMS file was absent at the audited commit (recorded
404); that metadata defect is not a mathematical counterexample. No
mathematical defect was found within the audited scope, and no correction to
the mathematics is proposed.
