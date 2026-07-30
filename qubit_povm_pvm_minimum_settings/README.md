# Minimum Bell-setting complexity for qubit POVM--PVM separation

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

- `paper/`: complete LaTeX manuscript, bibliography, figures, publication PDF,
  and line-numbered review PDF.
- `artifacts/`: exact symbolic certificates and machine-readable data.
- `reports/`: proof audit, dependency graph, literature/priority audit,
  verifier report, known risks, and final readiness assessment.
- `review_packet/`: theorem summary, proof roadmap, load-bearing lemma index,
  theorem-to-artifact map, and focused reviewer questions.
- `submission/`: arXiv and journal metadata, availability/disclosure
  statements, and private referee-objection responses.
- `run_all.sh`: one-command exact verification.
- repository workflow `.github/workflows/qubit-povm-pvm.yml`: continuous
  exact verification and warning-free builds of both PDFs.

## Exact verification

From this directory:

```sh
./run_all.sh
```

The reference environment is Python 3.14.6 (pinned in `.python-version`) with
SymPy 1.14.0 (pinned in `requirements.txt`). The exact verification path uses
rational/algebraic arithmetic and does not require network access. Numerical
discovery scripts are not part of this release path.

To rebuild the publication and line-numbered review PDFs with Tectonic 0.16.9:

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

## Author

**Alec Kriebel**  
Independent Researcher  
<https://aleckriebel.com/>

## License

Paper, reports, figures, and machine-readable mathematical data are released
under CC BY 4.0. Verification source code is released under the MIT License.
See `LICENSE`.
