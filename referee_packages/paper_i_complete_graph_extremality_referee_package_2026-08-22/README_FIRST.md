# Read this first

This is a frozen, self-contained project-source and certificate handoff for
*Local Complete-Graph
Optimality at Fitness Two and Strong-Selection Rigidity under Death--Birth
Updating*. The package is intended for an independent, submission-style audit;
it does not prescribe a favorable verdict.

Start by reading `REFEREE_PROMPT.md`. Inspect the paper and code before running
the convenience command. `CLAIM_CODE_MAP.md` is only a navigation index, and
`REFEREE_REPORT_TEMPLATE.md` is optional.

## Frozen identity

- Scientific source commit: `3652cfda20a3edad1b4e9ca75a4e5536f6f7f5ba`
- Source archive SHA-256: `b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`
- Manuscript PDF SHA-256: `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`
- Source archive: `complete_graph_extremality_db_source_and_certificates.tar.gz`
- Detached archive checksum: `complete_graph_extremality_db_source_and_certificates.tar.gz.sha256`
- Whole-package manifest: `PACKAGE_MANIFEST.sha256`

The package may itself be added by a later wrapping commit. The scientific
source commit above identifies the tracked state from which both the archive
and PDF were generated, avoiding a self-referential package hash.

## Layout

- `complete_graph_extremality_db.pdf`: convenience copy of the compiled paper.
- `complete_graph_extremality_db_source_and_certificates.tar.gz`: exact deterministic source, certificate, test, and replay
  archive supplied with the paper.
- `source_and_certificates/`: byte-identical extraction of that archive for
  immediate inspection.
- `verify_referee_package.py`: standard-library integrity verifier.
- `run_all_referee_checks.sh`: manifest verification, pinned clean replay,
  deterministic PDF rebuild, and PDF comparison in a disposable directory.

Prior review verdicts, research diaries, and saved successful output are
deliberately absent. Proof documents and independent checking programs remain.

## Suggested order

1. Independently inspect the PDF, LaTeX, proof documents, replay entry point,
   every invoked verifier, and imported helpers.
2. Verify package identity with `python3 verify_referee_package.py`.
3. With Python 3.14.6 available, run `./run_all_referee_checks.sh`. If
   `python3` is not that exact interpreter, set for example
   `BOOTSTRAP_PYTHON=/path/to/python3.14.6`.
4. Preserve the transcript and complete an independent mathematical and code
   audit using the neutral prompt.

The replay pins SymPy 1.14.0, python-flint 0.9.0, and mpmath 1.3.0. The PDF
rebuild requires Tectonic 0.16.9 and Poppler 26.08.0 (`pdfinfo` and
`pdftoppm`). The bootstrap may access the configured Python package index to
install the pinned dependencies; it does not contact any person or submit any
artifact. A fresh document build may also populate Tectonic's standard v33
resource-bundle cache. The exact theorem replay is independent of the document
tools, and the final PDF comparison detects any rendering difference.
