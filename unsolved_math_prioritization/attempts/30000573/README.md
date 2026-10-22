# Chaotic operators on nuclear Fréchet spaces: audited partial results

Problem **30000573 / OWR-1323-010**, rank **813**. Status: **unsolved, 5/5 substantive approaches used**.

The original basis-free question is not resolved. No nuclear Fréchet space on which every continuous operator is nonchaotic is constructed. Chaos means hypercyclicity together with dense periodic points. This is an AI-assisted, unrefereed partial-results checkpoint; no new-priority claim is made.

## Accepted scope

1. For nonzero separable real or complex Fréchet E, the full backward shift on E^N is mixing and chaotic; nuclearity is preserved when E is nuclear. The zero factor is excluded.
2. Every continuous linear map intertwining that shift with an operator on a continuous-norm target is zero. This blocks that factor-transfer route.
3. Every continuous weighted backward shift on the specified lacunary nuclear Köthe space is strongly stable. The space and prior no-hypercyclic-shift conclusion are credited to Charpentier–Grosse-Erdmann–Menet, Example 3.8. This concerns weighted shifts, not all operators.
4. A specified complex diagonal-plus-shift has dense periodic vectors but a nonzero continuous eigenfunctional, and hence is not hypercyclic.
5. Scalar-plus-finite-rank operators on infinite-dimensional Hausdorff locally convex spaces are not hypercyclic. The broader compact-perturbation obstruction is credited with its neighborhood-based compactness hypothesis.

The complex unconditional-basis existence theorem is credited literature. The full Fréchet proof sections are in [arXiv:1005.1416v1](https://arxiv.org/abs/1005.1416v1), Theorems 2.4 and 3.1; the shorter [v2](https://arxiv.org/abs/1005.1416v2) announces these extensions and does not contain those proof sections. A general real-space result is not inferred from the complex citation.

## Reading and provenance

- [Authored proofs](author/PROOFS.md) and [result and gaps](author/RESULT.md)
- [Independent mathematical audit](independent_audit/AUDIT_REPORT.md) and [acceptance](independent_audit/ACCEPTANCE.json)
- [Public source metadata](author/SOURCES.json), [verification metadata](independent_audit/PUBLIC_VERIFICATION.json), and [publication status](PUBLICATION_STATUS.json)
- Public-safe author and audit ZIPs in archives/, each bound by its byte count and SHA-256

This publication uses a public-safe author derivative. One nonmathematical provenance clause was removed, and its manifest was updated. All proof, code, arithmetic-result, and source-metadata bytes are unchanged. The accepted audit is rebound to the actual distributed derivative. Historical author statements that independent review was pending describe the author checkpoint; the independent audit and current publication status provide the subsequent verdict. No mathematical correction patch was required.

A fresh bounded GitHub preflight inspected main, the complete nonrecursive attempts tree, the target directory, and ID-based PR, branch, commit and code searches. It found no earlier target-specific attempt. PR #633 concerns the separate chaotic-semigroup question 30000576 and is excluded. Search absence is not a proof of exhaustive absence. Current live problem-page contents remain unverified; no claim of complete worldwide literature coverage is made.

## Reproduction

Python 3.10+ and its standard library are sufficient. Before executing downloaded code, verify every file against the independently trusted publication manifest pin and the inventory, including both ZIPs. The remote publication receipt records this bootstrap check. A self-checking script is not a secure bootstrap for untrusted code.

From this folder, run:

    python3 -I -B verify_publication.py --expected-manifest PUBLICATION_MANIFEST_SHA256
    python3 -I -O -B verify_publication.py --expected-manifest PUBLICATION_MANIFEST_SHA256
    python3 -I -B test_publication_integrity.py --expected-manifest PUBLICATION_MANIFEST_SHA256

Replace the placeholder by the pin in the PR description. The wrapper checks the entire inventory, bytes, ZIP/extracted equality, source anchors, acceptance and 13,722 finite diagnostics, then compares the independent auditor's full output with its frozen result. That auditor includes normal and optimized, original and relocated runs, 36 independent negative controls and two expected-pass prose diagnostics. The separate publication tests check outer-package mutations. No unmanifested bytecode or other package files are allowed.

Finite diagnostics and hashes are not mathematical proofs. Acceptance rests on the written scoped arguments and the independent mathematical review.

## Queue and distribution

Only this target's Status and Turns cells in QUEUE.md change, to unsolved and 5/5; every other byte, including its existing header, is preserved. No queue regeneration is performed.

The distribution includes only authored proofs, code, audits, results, and public verification/source metadata. It includes no third-party PDFs or extracts, dataset contents, private sources, or private coordination files. Draft PR only: no merge, release, DOI creation or outreach.
