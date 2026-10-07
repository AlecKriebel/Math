# Bilinear ergodic Hilbert variation for commuting transformations

Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

For arbitrary commuting invertible measurable measure-preserving transformations S,T of a probability space, complex f,g in L3, and every r>2, the symmetric sums H_N=Σ_(0<|n|≤N) f(S^n x)g(T^n x)/n (H_0=0) have bounded pointwise r-variation in L^(3/2), bounded maximum, and converge almost everywhere and in L^(3/2). The maximal tail relative to the limit tends to zero in L^(3/2).

This is a restriction/transference consequence of OpenAI's full continuous annular variation theorem, manuscript dated October 5, 2026, at pinned repository version adc7f1241b42e322a6451854ab7e4b4c146bf78a. The continuous analytic breakthrough is inherited and credited. The note supplies complete fixed-positive-area cell restriction, the uniform signed kernel error, and finite-menu finite-window transference. Calderón transference and its relevant modern uses are credited; no first-priority or independent triangular-Hilbert breakthrough claim is made.

Read `main.tex` or the separately downloadable `paper.pdf`. The self-contained TeX includes its bibliography; `references.bib` preserves the supplied upstream BibTeX and verified comparator citations. `SOURCE_HASHES.json` identifies the exact upstream files inspected; upstream manuscripts are not repackaged in the deposit. The actual local upstream clone was kept read-only. A build copy needed only PDF-engine compatibility changes (omitting pdfTeX-specific glyph-map directives under Tectonic), with no mathematical changes, and compiled successfully.

The independent mathematical audits in the supplement reconstruct the central upstream matrix/heat/smooth and frequency/rough/completion estimates, and independently reconstruct the new restriction/transference. These are automated research audits, not conventional human peer review, formal certification, or external endorsement. The family 082 Lean description and actual main declaration concern the older maximal theorem; neither the annular variation nor this note is claimed formally verified. AI tools were used extensively in research, drafting and verification. The preprint has not undergone conventional human peer review or refereeing at publication.

Scope stays at L3 inputs, symmetric odd Hilbert sums, commuting transformations and r>2. There is no noncommuting, r=2, or one-sided Cesàro conclusion.

## Reproduction

The source archive is standalone. With Tectonic 0.16.9 installed, run:

```sh
SOURCE_DATE_EPOCH=1791349200 tectonic main.tex
python3 restriction_geometry_check.py
python3 frequency_audit_computations.py
```

The checks use only the Python standard library (tested with Python 3.14.6). The geometry program checks 14,850 assertions covering signed kernels, supports, half-integer endpoints, and all anchored partitions through M=7 on reproducible random complex sequences. Decimal coefficients use 70-digit precision. Frequency probes are finite quadrature exploration and are explicitly not certified continuum counterexample searches. None of these computations proves the continuous theorem; the proofs and scoped audits carry that responsibility. A clean-directory build and rerun are recorded in the research repository. Exact PDF bytes can depend on the TeX engine; the fixed build epoch is supplied for reproducibility.

The `verification-supplement.zip` contains dependency/theorem ledgers, independent proof/audits, primary-source priority evidence, numerical result files, source hashes and reproduction information. Complete-package reviews and publication/tracker receipts are retained separately in the project's public repository so the reviewed payload itself does not change to include its own future review.

## Licensing and payload

Original note, code and accompanying original verification materials: Creative Commons Attribution 4.0 International (https://creativecommons.org/licenses/by/4.0/), following the repository's established Zenodo preprint convention. Upstream source copies are excluded; OpenAI's supplied manuscript citation is retained. No affiliation or coauthor is asserted.

Intended deposit files are exactly `paper.pdf`, `source.zip`, `verification-supplement.zip` and `README.md`; these are the payload files inside the local upload kit, not an outer kit archive. All claims in the metadata have the same scope as the note.
