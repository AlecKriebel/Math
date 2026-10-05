# A complete negatively curved observation Gramian with two-state ambiguity

Version 1.0, 5 October 2026. Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

The note gives a nonvacuous two-dimensional counterexample to Krener's printed manifold conjecture. Zero dynamics on a connected genus-three double cover, observed through a smooth Nash embedding of its hyperbolic genus-two quotient into R17, has exact Gramian `P_T=T*pi^*g`. For each fixed T>0 the metric is complete and has actual curvature `-1/T`, with fixed-normalization uniform positive bounds. Every attained history has exactly two initial states. It does not settle a strengthened question restricted to one global Euclidean state chart.

This is an application of classical constructions. Nash, covering classification, hyperbolic geometry and older local/global observability ambiguity are credited. The bounded primary audit, including complete Dirr2009 and Kang2013 reads and a fresh independent adversarial priority assessment, found no verified earlier explicit complete construction. Those two formerly named access gaps are closed. Some older realization originals and the wider literature remain uninspected; no worldwide firstness, seventeen-year openness, new mechanism or first refutation of every literal dimensional reading is claimed. `SOURCE_AUDIT.md` gives exact scopes, source pins and limits.

AI tools were used extensively in solving, drafting, reproducing and adversarially reviewing this work. This is an unrefereed preprint without conventional human peer review.

## Files and reproduction

- `negative_gramian_cover.pdf`: research note.
- `negative_gramian_cover.tex`: standalone manuscript source.
- `verify_cover.py`: Python 3.9+ standard-library supplementary verifier.
- `verification_results.json`: deterministic receipt from the recorded normal run.
- `SOURCE_AUDIT.md`: source and bounded priority supplement.
- `README.md` and `LICENSE.txt`: instructions and license.
- `negative_gramian_cover_sources.zip`: six authored source/support files and an internal `SOURCE_SHA256SUMS.txt` for those six members.
- `SHA256SUMS.txt`: SHA-256 digests of all eight other deposit payloads, including the PDF and ZIP; the list excludes itself.
- `zenodo-deposit.json`: intended upload metadata/file list; this JSON is not itself an upload payload.

From this directory, with optimization disabled:

```sh
python3 -E -B verify_cover.py > reproduced_verification.json
python3 -E -B -c 'import json; from pathlib import Path; expected=json.loads(Path("verification_results.json").read_text()); actual=json.loads(Path("reproduced_verification.json").read_text()); equal=expected==actual; print("MATCH" if equal else "MISMATCH"); raise SystemExit(0 if equal else 1)'
```

`python3 -E -B -O verify_cover.py` must fail with exit 2 and the optimization-refusal diagnostic, without printing a PASS receipt. No test depends on `assert`.

The verifier checks 1490 supplementary exact polynomial, Fraction, quadratic-field, monodromy and matrix controls, including 197 rational chart points. The all-point bounds rely on exact polynomial factorizations and the proof's interval argument, rather than finite samples. Its separate 80-digit Decimal radius calculation is a finite-precision diagnostic without a rigorous interval enclosure. It does not construct a Nash embedding or machine-certify global covering existence, quotient smoothness, compactness, completeness or history fibers. Those are analytical proof claims and explicitly imported classical theorem inputs. The original historical SymPy 873-check and independent 138-check audits remain separate evidence; they are not counts of this verifier.

## Compilation and package provenance

The LaTeX source is standalone. For example, compile it with `tectonic negative_gramian_cover.tex`. The deposited PDF and the six authored source/support files are accompanied by a source ZIP for convenient reproduction. ZIP members use relative filenames and contain no third-party papers. Its internal SOURCE_SHA256SUMS.txt verifies the six other archive members; the external SHA256SUMS.txt verifies the eight other deposited payloads. These lists exclude themselves and avoid cyclic archive digests.

The complete deposit contains nine payloads: PDF, LaTeX, verifier, results, source audit, README, license, external digests and source ZIP. zenodo-deposit.json is the repository's exact intended upload manifest, not an additional deposit payload. Real local compilation, verification, layout inspection and independent AI review evidence is retained in the dedicated repository audit folders. This is not a formal proof certificate or conventional human peer review.

The earlier source-only publication_package_v1 and publication_preparation_v1 snapshots are preserved. This assembled internal revision v3 is still publication version 1.0. Submitted original head 7271f51995532791220ac8e6b738a578d5d59143 and budget 1/5 remain unchanged; additional central proof-search turns 0.
