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
the then-current repository PDF byte for byte.

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
archive that it hashes; `release_bundle.sh` writes it to the adjacent detached
`.sha256` file after the final source bytes are frozen.

## 2026-08-21 second-review revision

The second external review was adjudicated against the exact chains and
certificates.  The final symmetric-sector verifier now asserts the exact
minimum margin printed in Appendix A, and the paper-level audit checks its
displayed SHA-256 binding.

The complete development replay exited zero.  A deterministic 84-member
archive was extracted into a new temporary directory, every internal manifest
entry passed, and `submission/bootstrap_replay.sh` created a fresh Python
3.14.6 environment with SymPy 1.14.0, python-flint 0.9.0, and mpmath 1.3.0.
The entire exact replay again exited zero.  The manuscript rebuilt in that
extraction to 30 pages and matched the repository PDF byte for byte, with
SHA-256
`229747f2a62906dea8976bbad747d0b8a109fb606a4a7695548613a245a93e66`.
Two independent archive generations from the same pre-log inputs were also
byte-for-byte identical.  The final archive digest is recorded outside the
archive after these reproduction notes are frozen, avoiding a self-hash.

## 2026-08-22 R2 re-review correction and R3 certified package

The two R2 re-review attacks were first reproduced independently.  A command
that printed the old public success token made the former direct replay return
zero without running Python, and a timestamp-valid adjacent cache executed
hostile code while its companion source retained the manifest hash.  The R3
workflow removes token authentication, makes the enclosing package launcher
the sole certified route, exact-checks both file and directory sets before
project import, rejects links/special nodes/bytecode caches, and runs every
project import with a fresh private command-line cache prefix.

Scientific source commit
`b9a415f763e82d9cc45c83de96c895b109e158a4` produced a deterministic
73-member source archive with SHA-256
`12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0`.
All 71 nonsynthetic archive members byte-match that commit.  The R3 referee
folder contains 83 manifest payloads and 84 total regular files; its transport
archive has SHA-256
`7e218882df2cf1bba3c5a914a706552bcfe22820dcbc98461df01511286c6717`.

The sole package-root command, `./run_all_referee_checks.sh`, was run under
hostile inherited Python-path, bytecode-cache, and Make settings.  Before the
positive replay it correctly rejected the old token-printing interpreter,
timestamp-valid hostile bytecode, an extra file, an extra empty directory, a
symlink, and a FIFO.  It then created the hash-locked Python 3.14.6 environment,
kept the controlled cache empty, passed all six unit tests and all seventeen
verifier/cross-check programs, rebuilt all 30 pages, and obtained PDF SHA-256
`5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`
byte-for-byte.  The 173-line transcript has SHA-256
`8312c9a552c0be05459cdb7e6efa6ba61c41acdebef4d94473785a1caa0aa347`.

An independent hostile audit repeated the package, archive, source-commit,
attack-fixture, replay, and PDF checks and found no blocker or minor defect.
Its 110-node package fingerprint was unchanged before and after execution at
`dcea48df9a6a1b6f337ff33d45a94a15e2353e9677670f745bc9063c4eb36899`.
The R3 correction changes no theorem, proof, endpoint, equality case, or one
of the 406 scientific predicates.
