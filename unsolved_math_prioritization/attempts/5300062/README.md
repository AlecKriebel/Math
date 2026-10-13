# Exponential parameter hairs: repaired interior-smoothness partial

Problem **5300062 / AMR-052-0062**, rank **796**. General status: **UNSOLVED, 5/5 approaches**. Current scoped verdict: **ACCEPT_SCOPED_PARTIAL_V2**. This is unrefereed, AI-assisted analysis, not a novelty determination or a complete resolution.

## Accepted scope

The repaired argument establishes a regular C-infinity standard potential parametrization of the **interiors** of parameter rays for every exponentially bounded address, including unbounded addresses. It credits Foerster-Schleicher's dynamic-ray construction, local domains, simple-root transversality and nonvanishing derivative inputs. Those external theorems are not independently reproved here.

General geometric real analyticity remains unresolved. No endpoint regularity, landing of all rays, or analytic boundary extension is proved. A fixed-map dynamic-hair nonanalyticity result does not transfer to parameter hairs. The explicit positive-real parameter arc does not settle the general question or the analyticity of its prescribed potential coordinate.

## Read the four preserved stages

1. `author_v1/REPORT.md`: the original frozen proof, with its historical pending-audit labels.
2. `audit_v1/AUDIT.md` and `audit_v1/CORRECTIONS.md`: the full independent audit and mandatory repair. Its historical verdict remains **REPAIR_REQUIRED_V1**.
3. `author_v2/REPORT.md`: the actual repaired proof. Only three mandatory mathematical replacements were made: strengthen the tail threshold by 2 log(K+3), explicitly verify the cited convergence hypothesis, and retain the same gap after the low-potential shift. The original six other payload files are byte-identical.
4. `v2_acceptance/ACCEPTANCE.md`: bounded-delta acceptance of the exact v2 ZIP, manifest and report. This closes the repair only for that identified v2, without rewriting prior evidence.

`frozen_archives/` stores canonical base64 encodings of all four original safe ZIP byte streams. The portable verifier decodes them, checks the supplied external hashes and sizes, and compares every ZIP member with the corresponding preserved directory. `FREEZE_BINDINGS.json` records all anchors.

## Portable verification

Requires Python 3 and mpmath **1.3.0**. Numerical controls use finite high-precision computations, not interval certification or a formal proof. Exact rational identities are distinguished from numerical controls.

    python3 -B verify_publication.py --expected-manifest PUBLICATION_MANIFEST_SHA256
    python3 -B test_publication_integrity.py

Run either command from any working directory using an absolute script path. The first validates strict recursive inventory, all four immutable archives and manifests, original/v2 author replay, the independent audit controls, and the full bounded-delta acceptance. It reproduces retained output bytes where specified by the frozen verifiers. The independent suite includes 480 exact rational-jet checks, 297 numerical controls and 12 diagnostic branch traps.

To verify the queue patch as well, supply both `--queue-before BASE_QUEUE` and `--queue-after BRANCH_QUEUE`. The complete files are hashed, then the verifier reconstructs the exact permitted patch: only this row's Status and Turns, queued / 0/5 to unsolved / 5/5. Findings and all other bytes, including the stale header, remain unchanged.

Optional source-input revalidation is documented in `audit_v1/README.md`. Its complete corpora, PDFs and raw snapshots are external inputs and are not distributed. Source inspection limits and public links remain in the immutable source metadata; publication does not claim a new literature search or a new visual inspection.

## Publication boundaries

The packet contains authored analysis, code, retained results, audit records and public verification metadata. It excludes source PDFs, extracted source text, page images, raw corpora, selected corpus records and private coordination files. This is one draft PR for one problem; no merge, release, DOI, or external outreach is included.
