# Function Theory 4.29: Roitman prior-resolution attribution

Problem ID 2304029, catalogue rank 678. Disposition: **already_solved, 1/5, prior-resolution attribution only**.

Roitman's 1983 paper supplies the matching prior counterexample attribution: monic complex polynomials P and Q have equal zero sets and equal first-derivative zero sets, but no equality P^m = Q^n with positive integers m,n. Sets need not have the same multiplicities. The reported integral-coefficient result is within this target. This packet does not independently certify a complete source proof or an explicit counterexample.

Read [final/INDEPENDENT_AUDIT.md](final/INDEPENDENT_AUDIT.md) for the acceptance decision and exact limits, [final/STATUS.md](final/STATUS.md) for the reconstruction, and [final/VERIFIER_PROOF.md](final/VERIFIER_PROOF.md) for the factored-verifier argument. The publisher abstract was available through indexing in the independent audit; the publisher page itself was unavailable in that pass. The author-linked transcription is missing construction formulas. Earlier retrieval descriptions in SOURCE_AUDIT.json and pre_edit/ remain historical; they are not claims of a newly inspected full paper.

## Reproduce

Requires Python 3.10+ and SymPy (tested with Python 3.12 and SymPy 1.14.0). From this directory run:

    python verify_publication.py --replay --selftest

The checker validates exact file inventory, hashes and byte counts, immutable final and pre-edit manifest bindings, the exact correction diff, attribution limits, and original-file preservation. It replays the final verifier self-tests and independent controls in ordinary and optimized Python: 406 expanded-oracle cases, 21 rejected invalid inputs, and one large-exponent control. Temporary copies keep the published packet unchanged. The controls use one SymPy backend and include no positive counterexample fixture.

## History and publication boundary

- final/ is the byte-identical 11-file audited packet, anchored by FILE_MANIFEST.json SHA-256 0a24a3780c51b133f7366a19d3ebba122dc5bfd4a2ade6fddae9857f83083c0a.
- pre_edit/ preserves all six frozen original public files, including the original verifier's reproduced approximate-input coercion defect. These are historical artifacts, not the recommended implementation.
- CORRECTIONS.diff is the exact generated diff between common original and final files; BINDING.json identifies both snapshots. The correction rejects Float coefficients before rational-domain conversion. No change certifies a counterexample.
- This is fresh reconstruction and fresh independent auditing. No lost historical audit is claimed to have been recovered.
- Source PDFs, source screenshots or copied text, dataset contents, and private coordination files are excluded. Only authored analysis, code, test results, and public verification metadata are included.

AI-assisted research and independent internal AI review are not external human peer review or formal proof-assistant certification. No new mathematical solution or priority claim is made.
