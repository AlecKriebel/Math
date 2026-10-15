# Reproduction and verification scope

The main note states the geometric undecidability and height consequences using the pinned arithmetic input with the corrections explained in the manuscript and source audits. The height supplement isolates the published-modularity substitution under its explicitly stated geometric inputs. The source audits and derivations carry the mathematical argument. The finite computations below check selected interfaces; they do not alone prove Hilbert's tenth problem over the rationals, the pointwise 2-converse, or the full geometric theorem. Neither a successful build nor an automated review is formal verification or conventional human peer review.

## Clean build and finite checks

Use Python 3.10 or later and an existing Tectonic installation. Both TeX documents are standalone, with their bibliographies included; no upstream checkout is needed to compile them. Tectonic needs its standard LaTeX packages available from its cache or package service. The driver does not install software or change any upstream source.

From the project directory, run:

```sh
python3 reproducibility/build_package.py
```

If Tectonic is outside `PATH`, give its installed path. The audited local invocation was:

```sh
python3 reproducibility/build_package.py --tectonic /Users/alec/.local/bin/tectonic
```

The driver first runs all three finite checks with Python's isolated mode so environment settings cannot disable their assertions. It then copies each standalone source into a unique clean temporary directory under this project's `tmp/`, compiles both documents, verifies that no source or check input changed during the run, and exports `manuscript/paper.pdf` and `manuscript/height-repair.pdf`. Only after all checks and both builds succeed are the PDFs exported. Temporary build files are removed. The main PDF is compiled from `manuscript/main.tex`; the historical `manuscript/main.pdf`, if present, is not the publication export.

`receipts/candidate_build.json` records the software versions, source and verification-input SHA-256 hashes, exported PDF hashes and byte counts, exact check outputs, and UTC build timestamps. The local candidate build used Tectonic 0.16.9 and CPython 3.14.6; CPython 3.12.14 is also available in the bundled workspace runtime. A software version or build timestamp is distinct from a manuscript date or earliest public disclosure. The driver records the displayed dates from the actual TeX sources rather than treating its execution time as their date.

The receipt identifies the actual exported PDF bytes. Byte-for-byte PDF reproducibility is not claimed across builds or toolchains. Inspect the rebuilt PDFs' text, equations, references, metadata, fonts and page layout; a compiler success and `%PDF` signature do not perform this visual inspection. The complete-package review records which exact exported versions were rendered and inspected.

The checks can also be run separately from the project directory:

```sh
python3 -I -B reproducibility/arithmetic_checks.py
python3 -I -B agent_notes/parity_matrix_check.py
python3 -I -B verification/check_two_converse_programs.py
```

- The arithmetic output must equal `reproducibility/arithmetic_checks.expected.json` as a JSON object. It verifies exact quadratic-field identities and all 26 primes below 5000 satisfying the specified congruences.
- The parity check must report 1960 generated reciprocity-consistent matrix instances with seed 4003. It exhausts the distinguished-prime toggles for each generated instance; it does not exhaust all possible matrix sizes or arithmetic realizations.
- The graph-program check must report 62 active-group restrictions in dimensions 1 through 5, with three programs per restriction. It verifies the grounding, constant and degree-one pair identities over the two-element field. It does not verify the arithmetic theta correspondence.

## Source provenance and supporting artifacts

`sources/PINNED_INPUT.json` and `sources/PINNED_COMPANIONS.json` identify the exact upstream files and their SHA-256 hashes at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. They cover family 004 and the needed pointwise 2-converse companion. Use the pinned public source links in the manuscripts to obtain the upstream files, then compare their byte hashes with these records. The upstream clone remains read-only. The package excludes downloaded primary-source caches and upstream manuscript copies; source references and hashes provide provenance without redistributing those files.

The current dependency ledger, verified corrections, scoped source audits, integration report and package reviews document which statements and interfaces were checked and their limits. They should be read together with the pinned sources. Historical research notes retain the status at their recorded time; later completed audits and the current ledger determine the candidate's present status.

`receipts/source_build.json` records a separate compatibility build of the pinned family 004 source. That derived build omitted only three unsupported pdfTeX metadata primitives (`pdfinfoomitdate`, `pdftrailerid`, and `pdfsuppressptexinfo`); it did not change the mathematical text. Its success is a build check, not validation of the upstream proof, and it is not the clean build of this project's publication PDFs.

`reproducibility/checkpoint.py` is an operational aid for publishing explicitly named owned files safely on shared `main`. It uses an isolated index and a fast-forward push without changing the shared checkout, real index, branch or HEAD. It is unnecessary to reproduce the mathematical artifacts. No repository publication or Zenodo operation is performed by `build_package.py`.
