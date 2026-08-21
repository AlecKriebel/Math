# Clean-bundle reproduction test

## 2026-08-20 checkpoint

The deterministic bundler was run twice over the same inputs. The two gzip
archives were byte-for-byte identical. Each included `BUNDLE_METADATA.txt`
and an internal `MANIFEST.sha256`; the bundler printed the archive-level
SHA-256 separately.

One archive was extracted into a new temporary directory. Every entry passed
`shasum -a 256 -c MANIFEST.sha256`. The bundled
`submission/bootstrap_replay.sh` then:

1. created a new isolated environment with Python 3.14.6;
2. installed and checked SymPy 1.14.0 and python-flint 0.9.0; and
3. ran the complete Paper I exact replay to exit status zero.

The replay passed the six unit tests; strong-selection, directed-support,
triangle, symmetric-four-vertex, and lumpability suites; the dual and
complete-refresh identities; all three physical Hessian sectors; the marked
lift and regular-sector cross-checks; and the paper-level integration audit.
Lines labelled `OPEN` in exploratory certificate output refer to stronger
global statements that the manuscript explicitly does not claim; they are not
failed assertions or dependencies of the stated theorems.

The legacy manuscript build was absent from the archive and is no longer
called by Paper I's replay. The development environment had python-flint 0.8.0,
so this clean test deliberately used the pinned 0.9.0 environment rather than
reusing it.

The host document tools separately reported Tectonic 0.16.9 and Poppler
26.08.0 (`pdfinfo` and `pdftoppm`), matching `ENVIRONMENT.md`. The manuscript
was also built inside a fresh extraction. The resulting 26-page PDF matched
the current repository PDF byte for byte.

This records a tested development checkpoint, not an immutable public
release. Regenerate the archive and repeat the clean-extraction checks after
any manuscript, certificate, or submission-material edit; record the final
release digest in public availability text only after the files are frozen.

## 2026-08-20 adversarial-review revision

After the twelve-point external review was adjudicated and the accepted
repairs were integrated, the full development replay again exited zero.  The
paper-level audit additionally checked the sample--retarget collision phase,
the standard-sector Frobenius normalization, and the exact finite symmetric
certificate ranges now displayed in the manuscript.

The revised deterministic archive was generated twice from identical inputs;
the two archives were byte-for-byte identical and contained 83 regular
members, including metadata and the internal manifest.  A new extraction in a
fresh temporary directory passed every manifest hash.  Its bootstrap created
a fresh Python 3.14.6 environment, installed SymPy 1.14.0, python-flint
0.9.0, and mpmath 1.3.0, and replayed the entire exact suite to exit status
zero.

The 29-page manuscript was then built inside that extraction.  The extracted
PDF was byte-for-byte identical to the repository PDF and had SHA-256
`3af20b4648c6a69e1946e6cdd32f5df9557ca55a2ec1a1c16b29a8dbb6e92d98`.
As before, the archive-level digest is intentionally not embedded inside the
archive that it hashes; it is printed by `release_bundle.sh` after the final
source bytes are frozen.
