# Read this first

This is a frozen, complete scientific referee handoff for *A fitness-independent
family of simultaneous amplifiers beyond relative fitness 3/2*.  It is meant
for an independent, submission-style audit of the manuscript and its exact
certificate programs.  It does not prescribe a favorable verdict.

Start by reading `REFEREE_PROMPT.md`.  Inspect the manuscript, replay entry
point, and every invoked program before running the convenience command.
`CLAIM_CODE_MAP.md` is only a navigation index, and
`REFEREE_REPORT_TEMPLATE.md` is optional.

## Frozen identity

- Scientific source commit: `bd66a3bbf1c530ef67a4b7be5ee69a6825678457`
- Annotated tag object: `755969d69cdd7f86ad8eceddb4df52a4fe2b23ee`
- Frozen annotated source tag (unsigned): `simultaneous-amplification-beyond-three-halves-v2.0.3`
- Source archive SHA-256: `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`
- Manuscript PDF SHA-256: `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`
- Source archive: `simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz`
- Detached archive checksum: `simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz.sha256`
- Whole-package manifest: `PACKAGE_MANIFEST.sha256`
- Internal source-archive members: 23

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
- `verify_git_binding.py`: optional exact comparison of every archived
  repository-backed blob and executable mode with an independently obtained
  Git checkout containing the frozen tag.
- `run_all_referee_checks.sh`: package verification, pinned replay,
  deterministic source-archive and PDF rebuilds, and byte comparisons in a
  disposable directory.

The integrity verifier checks exact payload sets, hashes, safe regular archive
members, and the expected `0644`/`0755` modes in both the archive and copied
extraction.

Prior referee verdicts, hostile-audit ledgers, submission correspondence, and
saved successful output are deliberately absent.  The source archive does
include provenance and research logs; treat every statement in those files as
an author claim, not evidence.

## Suggested order

1. Read the PDF and LaTeX source and make an independent theorem ledger.
2. Inspect the wrapper runner and both integrity checkers,
   `bootstrap_replay.sh`, `replay.sh`, `build.sh`, `release_bundle.sh`,
   `bundle_manifest.py`, `requirements.txt`,
   `tests/test_verifier_fail_closed.py`, every verifier invoked, both bundled
   wheels, and all imported code.
3. Verify package identity with
   `PYTHONDONTWRITEBYTECODE=1 python3 verify_referee_package.py`.
4. With Python 3.14.6 available, run `./run_all_referee_checks.sh`.  If
   `python3` is not that interpreter, set
   `BOOTSTRAP_PYTHON=/path/to/python3.14.6`.
5. Optionally, from an independently obtained and updated repository checkout,
   run `./verify_git_binding.py --repo /path/to/checkout`.  This compares the
   annotated tag, all 21 repository-backed source blobs, and their modes.  It
   does not authenticate the unsigned tag, checkout, author, or hosting account.
6. Complete the mathematical and software audit described in the neutral
   prompt and record any limitation that prevents a complete check.

The replay pins SymPy 1.14.0 and mpmath 1.3.0 and includes their pure-Python
wheels with required SHA-256 hashes.  The bootstrap disables package indexes,
so the Python replay is offline once Python 3.14.6 is present.  The PDF rebuild
separately requires externally installed Tectonic 0.16.9 and Poppler 26.08.0
(`pdfinfo` and `pdftoppm`); Tectonic may populate its standard resource cache
or require its resource endpoint.  This package is therefore not an offline
operating-system or document-tool image.  Run untrusted review material in an
unprivileged disposable environment without personal credentials.

The manifests and local Git comparison establish consistency relative to the
bytes or checkout supplied.  They do not prove authorship or cryptographically
authenticate the unsigned tag.  A journal/preprint deposit or a separately
trusted signing key is the appropriate external provenance anchor.
