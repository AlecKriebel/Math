# Minimum Bell-setting complexity for qubit POVM--PVM separation

**Current prepared revision:** 1.2.0 (August 2026; awaiting author release)

**Public version of record:** 1.1.0, deposited 30 July 2026,
[doi:10.5281/zenodo.21699161](https://doi.org/10.5281/zenodo.21699161)

**Prepared 1.2.0 paper DOI:**
`[ZENODO V1.2.0 VERSION-SPECIFIC DOI — INSERT AFTER UPLOAD]`

**Prepared 1.2.0 software DOI:**
`[ZENODO V1.2.0 SOFTWARE DOI — INSERT AFTER UPLOAD]`

This folder is the dependency-complete publication and verification package
for the following fixed-dimension Bell-correlation classification:

1. with two inputs per party and arbitrary finite declared outputs, every
   qubit-POVM behavior belongs to the shared-randomness convex hull of
   fixed-qubit PVM behaviors;
2. an explicit rational Bell functional with input architecture `3 x 2`
   has a certified strict qubit-POVM advantage over every fixed-qubit PVM
   strategy;
3. consequently, `3 x 2` is the minimum input architecture, up to exchanging
   the parties.

The equality is about convexified behavior sets. It does **not** assert that
an individual POVM is a PVM, that every POVM can be decomposed into PVMs on
the same state, or that Naimark dilation preserves the qubit dimension.

## Package map

- `paper/`: one canonical mathematical source, bibliography, figures,
  publication PDF, line-numbered review PDF, and a separate one-column
  REVTeX 4.2f PRA presentation.
- `artifacts/`: exact symbolic certificates and machine-readable data.
- `reports/`: proof audit, dependency graph, literature/priority audit,
  verifier report, known risks, and final readiness assessment.
- `review_packet/`: theorem summary, proof roadmap, load-bearing lemma index,
  theorem-to-artifact map, and focused reviewer questions.
- `submission/`: arXiv and journal metadata, availability/disclosure
  statements, the non-destructive Zenodo 1.2.0 upload set, and a complete
  Physical Review A review package. The frozen `zenodo-v1.1.0/` directory is
  preserved byte-for-byte.
- `run_all.sh`: one-command exact verification.
- repository workflow `.github/workflows/qubit-povm-pvm.yml`: continuous
  exact verification and warning-free archival, review, and PRA builds.

## Exact verification

From this directory:

```sh
./run_all.sh
```

The reference environment is Python 3.14.6 (pinned in `.python-version`) with
SymPy 1.14.0 (pinned in `requirements.txt`). The exact verification path uses
rational/algebraic arithmetic and does not require network access. Numerical
discovery scripts are not part of this release path.

To rebuild the publication, line-numbered review, and PRA PDFs with Tectonic
0.16.9:

```sh
./paper/build.sh
```

## Status

The package is designed to make expert scrutiny easy. Passing the supplied
checks verifies encoded algebraic identities and explicit constructions; it
is not peer review and does not replace the mathematical arguments in the
manuscript.
The public-preprint status is **READY, NEEDS EXPERT SCRUTINY**; see
`reports/readiness_report.md`.

Version 1.2.0 adds a primary-source comparison with the related
contemporaneous work of Zhu, Chen, and Wang
([arXiv:2608.01317](https://arxiv.org/abs/2608.01317)), foregrounds the
universal two-input closure theorem, and adds PRA submission and release
materials. The final hardening pass also clarifies notation and exposition,
adds foundational citations, and produces a genuine APS-compatible build.
No theorem hypothesis, Bell coefficient, witness, certified bound, proof
mechanism, or mathematical conclusion changed. See `CHANGELOG.md` and
`reports/version_history.md`.

## Author

**Alec Kriebel**  
Independent Researcher  
<https://aleckriebel.com/>

## License

Paper, reports, figures, and machine-readable mathematical data are released
under CC BY 4.0. Verification source code is released under the MIT License.
See `LICENSE`.
