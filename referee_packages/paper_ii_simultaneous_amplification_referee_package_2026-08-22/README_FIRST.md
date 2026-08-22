# Read this first

This is a frozen, self-contained referee handoff for *A fitness-independent
family of simultaneous amplifiers beyond relative fitness 3/2*.  It is meant
for an independent, submission-style audit of the manuscript and its exact
certificate programs.  It does not prescribe a favorable verdict.

Start by reading `REFEREE_PROMPT.md`.  Inspect the manuscript, replay entry
point, and every invoked program before running the convenience command.
`CLAIM_CODE_MAP.md` is only a navigation index, and
`REFEREE_REPORT_TEMPLATE.md` is optional.

## Frozen identity

- Scientific source commit: `2302d7c6ae17fc061a985da322df6d0600b66672`
- Immutable source tag: `simultaneous-amplification-beyond-three-halves-v2.0.1`
- Source archive SHA-256: `ce62bfbdb22681ba48b2a04653155b2e06f52659f140c13f5e0220db365b9250`
- Manuscript PDF SHA-256: `f68142b3d99b95f83ca6ba4688539cb9e0fdb88ed96809aef5316ed22a59888f`
- Source archive: `simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz`
- Detached archive checksum: `simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz.sha256`
- Whole-package manifest: `PACKAGE_MANIFEST.sha256`
- Internal source-archive members: 19

The wrapper package may be added by a later commit.  The scientific source
commit and tag above identify the state from which the source archive and PDF
were generated, avoiding a self-referential package hash.

## Layout

- `simultaneous_amplification_beyond_three_halves.pdf`: convenience copy of
  the compiled manuscript.
- `simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz`:
  deterministic source, certificate, and replay archive supplied with the
  manuscript.
- `source_and_certificates/`: byte-identical extraction of that archive for
  immediate inspection.
- `verify_referee_package.py`: standard-library integrity verifier.
- `run_all_referee_checks.sh`: package verification, pinned replay,
  deterministic source-archive and PDF rebuilds, and byte comparisons in a
  disposable directory.

Prior referee verdicts, hostile-audit ledgers, submission correspondence, and
saved successful output are deliberately absent.  The source archive does
include provenance and research logs; treat every statement in those files as
an author claim, not evidence.

## Suggested order

1. Read the PDF and LaTeX source and make an independent theorem ledger.
2. Inspect the wrapper runner and integrity checker, `bootstrap_replay.sh`,
   `replay.sh`, `build.sh`, `requirements.txt`, every verifier invoked, and
   all imported code.
3. Verify package identity with
   `PYTHONDONTWRITEBYTECODE=1 python3 verify_referee_package.py`.
4. With Python 3.14.6 available, run `./run_all_referee_checks.sh`.  If
   `python3` is not that interpreter, set
   `BOOTSTRAP_PYTHON=/path/to/python3.14.6`.
5. Complete the mathematical and software audit described in the neutral
   prompt and record any limitation that prevents a complete check.

The replay pins SymPy 1.14.0 and mpmath 1.3.0.  The PDF rebuild requires
Tectonic 0.16.9 and Poppler 26.08.0 (`pdfinfo` and `pdftoppm`).  The bootstrap
may access the configured Python package index to install pinned dependencies;
those dependencies are version-pinned but their distribution files are not
vendored or hash-pinned.  A document rebuild may also populate Tectonic's
standard resource-bundle cache.  Run untrusted review material in an
unprivileged disposable environment without personal credentials.
