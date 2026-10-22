# Elliptic conformal Hausdorff gauges: corrected partial research

Problem 30001397 / OWR-4137-017, rank 669. **UNSOLVED, 5/5 approaches exhausted.** No full proof, counterexample, prior full resolution, or novelty is claimed. The budget is closed.

## Current result and scope

The retained partials exclude power gauges and gauges bounded by the h-power, reduce regularly varying exact gauges to positive finite total mass, and obstruct globally uniform scalar-gauge ball bounds using the pole/parabolic exponents. The last obstruction is not a counterexample to exact Hausdorff representation. The independent Pareto model does not establish an elliptic recurrence theorem.

All mathematical conclusions retain the basin-attraction interpretation and explicit conformal-measure hypotheses. Arbitrary exact scalar gauges, positive finite total gauge mass, and the required quantitative/all-scale dynamical transfer remain unresolved. Conformal probability is distinct from the possibly infinite invariant measure. This is AI-assisted research and audit, not human peer review.

## Read in this order

1. [Corrected proof](release/safe/PROOF.md), [claims](release/safe/CLAIMS.json), and [limitations](release/safe/LIMITATIONS.md).
2. [Complete original independent audit](release/audit-safe/AUDIT.md) and its [binding](release/audit-safe/AUDIT_BINDING.json).
3. [Final corrected-byte acceptance](final-audit/FINAL_BINDING_ACCEPTANCE.json), which accepts the exact corrected release and all C1/C2/C3 changes.
4. [Exact author diff](release/release-meta/EXACT_AUTHOR_DIFF.patch), [release binding](release/release-meta/RELEASE_BINDING.json), and [historical snapshots](release/history/).

The corrected author verifier executes and reports 7,580 assert statements. The independent audit runs 87,730 exact predicate checks. The original 8,700 report was an overcount; it is preserved solely as historical evidence and is not the current count. C2 distinguishes constant metric scaling for regularly varying gauges from gauge composition for arbitrary gauges. C3 supplies the Koebe-quarter argument showing the transported radii shrink; it supplies no missing recurrence estimate.

## Historical status fields

Every file under release/ and final-audit/ is preserved byte-for-byte. Statements such as audit pending, no remote writes, or final confirmation pending in frozen proofs, status records, logs, and release metadata describe their creation time. The separate final acceptance satisfies the corrected-byte audit gate for precisely the bound corrected author ZIP and complete release ZIP. These historical fields are intentionally not rewritten. The scientific conclusion remains unsolved.

## Portable verification

From any working directory, run:

```sh
python3 /path/to/this/folder/verify_publication.py --replay
python3 -O /path/to/this/folder/verify_publication.py --replay
```

The standard-library wrapper checks the exact file/directory inventory, rejects symlinks, verifies manifests and all frozen ZIP entries, binds the final acceptance, recomputes the exact author diff, and runs all replay subprocesses with assertions enabled even when the wrapper uses -O. It replays the original audit only against its original author ZIP, never against the corrected ZIP. It also instruments the corrected verifier to check the actual 7,580 assertion count. Finite checks and byte integrity do not certify the full mathematics.

[Public source metadata](release/safe/SOURCE_VERIFICATION.json) and [independent source checks](release/audit-safe/AUDIT_SOURCE_CHECKS.json) contain public URLs, fingerprints, retrieval history and inspection scope. Third-party source PDFs/text, dataset contents and private coordination files are excluded. The 2023 book was not inspected in full; no exhaustive openness or priority claim is made.

The queue edit changes only this row's Status from queued to unsolved and Turns from 0/5 to 5/5. All other queue bytes, including Findings, Chat, DOI and the header, are preserved. No queue command, merge, GitHub release, DOI or outreach is part of this draft.
