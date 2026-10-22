# Ohtsuki Conjecture 7.30: a literal rank-interpolation obstruction

Problem 10400145 / AMR-103-0145, catalog rank 1010. Disposition: **claimed_solved, 1/5 substantive approaches**, by a complete negative argument for the printed coefficient ring and normalization. This is AI-assisted mathematics with two independent AI-assisted full mathematical/source audits. It is not conventional human peer review or proof-assistant certification, and no novelty or priority is claimed.

## Read the proof and both reviews

- [Accepted final-v3 proof](author_v3/packet/PROOF_AND_STATUS.md)
- [Independent mathematical audit](audit_algebra/INDEPENDENT_AUDIT.md) and [acceptance](audit_algebra/ACCEPTANCE.json)
- [Independent full source-bridge audit](audit_source_bridge/FULL_AUDIT.md) and [acceptance](audit_source_bridge/ACCEPTANCE.json)
- [Primary-source identities and inspection history](author_v3/packet/SOURCE_METADATA.json)

The ordinary Habiro coefficient ring inverts q, but not q−1. The third finite quotient and the dual-number specialization force the first coefficients to be affine in rank. The specified rank-one normalization gives v3=2v2. The published Lê and Habiro–Lê normalization bridge instead gives n(n²−1) times the Casson invariant; the specified Poincare orientation yields 0, −6, −24, rather than the forced rank-three value −12. The proof needs no differentiation of an infinite expansion or Taylor injectivity.

The result concerns literal Conjecture 7.30. It does not refute fixed-Lie-algebra Conjecture 7.29, establish a claim for modified completions or rank-dependent renormalizations, certify novelty, or prove the cited quantum-topological theorems from first principles.

## Exact preservation and publication boundary

All 11 final-v3 author files, all four final algebra-audit files, and all six final source-bridge-audit files are preserved exactly. Their external manifests and pins are included. Earlier author freezes and the superseded audit draft are omitted. The two metadata-only historical correction patches are included for provenance; no mathematical correction was required. Original timestamps, historical receipts, and scope declarations are preserved, rather than silently relabeled as new execution.

Only authored mathematics, audits, acceptance reports, source-free verification code, and public bibliographic/verification metadata are distributed. No PDFs, source extracts, screenshots, dataset contents, private sources, personal data, or private coordination material are included.

## Replay

Obtain the SHA-256 and byte count of BOOTSTRAP.py from the independent PR publication record and authenticate it before execution. Colocated mutable pins do not authenticate themselves. Then run from the packet directory:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

Python 3.10+, an unprivileged Unix account, and working bubblewrap (`bwrap`) are required for full replay. The runner authenticates the exact publication inventory before any payload execution; then it replays the author checker and both final audit harnesses. The source-bridge harness enforces a whole-filesystem read-only mount and verifies errno 30 on a write attempt. Disposable mutation copies are created outside the published packet. If bubblewrap is unavailable, full replay fails; it does not label read-only enforcement as passed. `--integrity-only` performs only integrity and acceptance-scope validation.

    python -I -S -B TEST_MUTATIONS.py .

This checks publication-integrity attacks, malformed manifests reached through deliberate disposable pin refresh, and hostile working directories/import paths. It tests finite algebra and reproducibility, not a formal proof of the mathematics. The threat model requires an independently trusted initial bootstrap pin and files not being concurrently replaced after checks.

Optional retained-input rehashes:

    python -I -S -B BOOTSTRAP.py . --source-dir /path/to/retained/pdfs
    python -I -S -B BOOTSTRAP.py . --problems /path/to/problems.json --research-results /path/to/research_results.json

The source directory uses filenames mapped in audit_algebra/audit_controls.py. All nine PDF identities must match. Both complete corpora must be supplied together. Missing inputs are reported as NOT_RUN; wrong or incomplete supplied inputs fail. These stages establish current byte identity only, not fresh source inspection, fresh downloading, or a fresh record join. Historical source inspections and corpus matching remain separately identified in the immutable reports. GitHub CI status is separate; local replay never claims CI passed.
