# Online Resource 1: exact verification code

**A five-word Pauli–Clifford normal form for an exceptional unitary Hecke Yang–Baxter operator**

Alec Kriebel · Independent researcher, San Francisco, USA  
Corresponding author: me@aleckriebel.com  
ORCID: https://orcid.org/0009-0001-9320-500X  
Journal submission: *Algebras and Representation Theory*  
Supplement date: 25 September 2026 · upload filename: `ESM_1.zip`

This standalone supplement verifies finite identities used in the accompanying manuscript. It contains five supported verification routes, a focused 26-test failure-mode suite, hash-locked dependencies and a package-integrity checker. The code is licensed under the included MIT license. See `COVERAGE_AND_TRUST.md` for what each computation establishes and what remains a mathematical or cited-source argument.

## Reproduce

Use CPython 3.14.6 with optimization disabled. Create an environment and install the two pinned universal wheels:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements.txt
YBE_PYTHON="$PWD/.venv/bin/python" bash run_all.sh
.venv/bin/python test_failure_modes.py
.venv/bin/python verify_checksums.py
```

The locked versions are SymPy 1.14.0 and mpmath 1.3.0. The standard-library routes do not need those libraries individually; the complete runner checks their versions for the SymPy route. All supported scientific verifiers and the checksum checker reject optimized execution. The test suite checks that no scientific verifier contains disableable Python assertion statements and requires each deliberate mathematical mutation to fail with an explicit scientific `AssertionError`.

`verification_output.txt` contains a fresh successful run of this curated supplement, and `SHA256SUMS` binds the distributed files. The checksum manifest checks consistency with these bytes; it is not a digital signature. A local `.venv` and incidental caches are not included in the distributed archive.

## Source-comparison correction

The archival v1.2.0 standard-library script described an auxiliary two-block matrix as a literal transcription of Galindo–Hong–Rowell Eq. (5.2). Inspection of the accessible preprint shows different displayed scalars on its two blocks. This supplement makes the distinction explicit: it independently defines the common-prefactor block matrix and separately computes residuals for the accessible preprint's mixed-prefactor display. It makes no claim that the common-prefactor choice was the authors' intended correction. The revised manuscript omits the numerical GHR comparison; the construction and its own active generalized operator are unaffected.

The source display at issue is Eq. (5.2) of the accessible version of *Generalized and quasi-localizations of braid group representations* by Galindo, Hong and Rowell, [arXiv:1105.5048v1](https://arxiv.org/pdf/1105.5048v1), p. 26. `COVERAGE_AND_TRUST.md` states both definitions and their distinct exact residuals. These diagnostics are auxiliary source-transcription checks.

## Relationship to the archival release

Before curation, the unchanged v1.2.0 package was rerun in a fresh CPython 3.14.6 environment with these dependencies: all five routes, all 32 original tests and all 43 original manifest entries passed. Its complete stdout reproduced the frozen output byte for byte. This supplement retains 26 scientific tests and omits six tests that apply only to the original archival attachment, release metadata, document wording or historical packaging. It also strengthens mutation diagnostics and adds the source-display distinction described above. The archival release is preserved unchanged.

`PROVENANCE.md` records the earlier public release timestamp and artifact identifiers, and distinguishes this journal revision from the unchanged DOI-bearing archival edition.

The original discovery search code and random seeds were not retained. The manuscript does not claim reproducibility or exhaustiveness of that search. Every included check starts from explicitly specified exact matrices or tensor words.
