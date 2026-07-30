# Minimum input complexity for qubit POVMs versus projective measurements

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

- `paper/`: complete LaTeX manuscript, bibliography, figures, and rendered PDF.
- `artifacts/`: exact symbolic certificates and machine-readable data.
- `reports/`: proof audit, dependency graph, literature/priority audit,
  verifier report, known risks, and final readiness assessment.
- `review_packet/`: theorem summary, proof roadmap, load-bearing lemma index,
  and focused reviewer questions.
- `submission/`: arXiv and journal metadata, availability/disclosure
  statements, and private referee-objection responses.
- `run_all.sh`: one-command exact verification.

## Exact verification

From this directory:

```sh
./run_all.sh
```

The exact verification path uses SymPy rational/algebraic arithmetic and does
not require network access. Numerical discovery scripts are not part of this
release path.

## Status

The package is designed to make expert scrutiny easy. Passing the supplied
checks verifies encoded algebraic identities and explicit constructions; it
is not peer review and does not replace the human proofs in the manuscript.
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
