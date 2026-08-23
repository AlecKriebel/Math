# Read this first

This is a frozen, self-contained project-source and certificate handoff for
*Local Complete-Graph
Optimality at Fitness Two and Strong-Selection Rigidity under Death--Birth
Updating*. The package is intended for an independent, submission-style audit;
it does not prescribe a favorable verdict.

Start by reading `REFEREE_PROMPT.md`. Inspect the paper and code before running
the sole certified package replay. `CLAIM_CODE_MAP.md` is only a navigation
index, and `REFEREE_REPORT_TEMPLATE.md` is optional.

## Frozen identity

- Scientific source commit: `b9a415f763e82d9cc45c83de96c895b109e158a4`
- Source archive SHA-256: `12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0`
- Manuscript PDF SHA-256: `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`
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
- `run_all_referee_checks.sh`: the sole certified end-to-end entry point. It
  verifies the exact package tree, safely extracts the verified source archive
  to a disposable directory, provisions the pinned runtime, runs all internal
  stages, rebuilds the PDF, and compares it byte-for-byte.

Prior review verdicts, research diaries, and saved successful output are
deliberately absent. Proof documents and independent checking programs remain.
The three imported exploratory helper modules have inert guarded mains: only
the function-level reach described in `CLAIM_CODE_MAP.md` is advertised.

## Suggested order

1. Independently inspect the PDF, LaTeX, proof documents, certified launcher,
   internal bootstrap/replay stages, every invoked verifier, and imported
   helpers.
2. Verify package identity with `python3 -I verify_referee_package.py`.
3. With Python 3.14.6 available, run `./run_all_referee_checks.sh`. If
   `python3` is not that exact interpreter, set for example
   `BOOTSTRAP_PYTHON=/path/to/python3.14.6`.
4. Preserve the transcript and complete an independent mathematical and code
   audit using the neutral prompt.

The bootstrap's explicit `--development` mode is a convenience rather than a
certificate; `replay.sh` is internal-only and rejects standalone invocation.
Neither lower-stage status certifies package identity or execution of the
delivered source. The certified launcher rejects links, special nodes, extra
files/directories, and bytecode/cache entries before any project import, then
uses a fresh private cache prefix for every Python process that can import
project code. The preceding exact-tree scanner is standard-library-only and
imports no project module.

The certified replay binds the accepted wheels for SymPy 1.14.0,
python-flint 0.9.0, and mpmath 1.3.0 by SHA-256. The PDF rebuild requires
Tectonic 0.16.9, the pinned standard v33 bundle content, and Poppler 26.08.0
(`pdfinfo` and `pdftoppm`). The bootstrap may access the configured Python
package index to retrieve only hash-matching wheels; it does not contact any
person or submit any artifact. The exact theorem replay is independent of the
document tools, and the final PDF comparison detects any rendering difference.
