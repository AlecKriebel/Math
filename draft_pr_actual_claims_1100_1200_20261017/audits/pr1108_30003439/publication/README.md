# A negative-curvature normal barrier on an algebraic cone that is not a hyperbolicity cone

Alec Kriebel, independent researcher, ORCID https://orcid.org/0009-0001-9320-500X.
Version 1.0.0, 2026-10-17. Research note for problem 30003439 / OWR-15219-008.

The five-page note answers Tunçel's original 2017 existential problem with the one-sided cone K={x,y,z≥0:xy²≥z³} and F=-25log(z(xy²-z³)), parameter 100. It proves the cone-direction third-derivative matrix inequality universally and excludes every homogeneous hyperbolic defining polynomial in the original R³. The cone and prior self-concordant power-cone barriers are explicitly credited to Hildebrand and Roy–Xiao. The parameter is deliberately nonoptimal. The broader every-regular-cone question is outside the theorem.

AI tools were used extensively in development, verification and writing. This work is unrefereed; independent adversarial AI reviews are not external human peer review, journal acceptance, or proof-assistant certification. The accompanying priority screen is bounded and makes no exhaustive literature or first-ever claim.

## Contents and reproduction

- `main.tex` and `output/pdf/negative-curvature-cone.pdf`: complete analytic research note.
- `verification/check_geometry.py`: independently authored standard-library exact polynomial and rational tensor verifier. 791 checks including 8 adverse controls, enforced with explicit exceptions. Both normal and optimized Python run all checks.
- `verification/curvature_reproduction.py`: separately authored sparse-polynomial and logarithm-series verifier, including 45 rational parameter cases and 315 independent contractions. Its assertions are protected by a startup check that rejects optimized Python.
- `verification/expected_results.json`: stable expected results, excluding runtime timestamps/version fields.
- `audits/`: independent mathematical reports, source identities, and bounded priority evidence. No third-party source documents are redistributed.
- `PROVENANCE.json` and `SOURCE_MANIFEST.json`: frozen PR identity and exact file bytes/hashes.

Use Python 3.10 or newer with its standard library; no packages, network access, randomness, or numerical thresholds are required:

```sh
python3 -B verification/check_geometry.py
python3 -B -O verification/check_geometry.py
python3 -B verification/curvature_reproduction.py
```

`python3 -B -O verification/curvature_reproduction.py` must fail at startup, rather than silently disabling checks. The computations supplement the analytic universal proof; rational samples alone are not a proof of the theorem.

Compile `main.tex` with Tectonic or a standard LaTeX installation. The builder `build_package.py` (in the repository) recompiles the verifier expectations and creates explicit deterministic ZIP archives; rendered PDF bytes can differ due to compiler metadata. The two upload files are the final PDF and `negative-curvature-cone-source-and-verification.zip`. The separate upload kit contains exactly these files plus the same Zenodo metadata and a portable deposit manifest. The default repository license/author metadata are preserved.

The accepted source claim was frozen at PR #1108, head 148130ab93ab46a3459d7bc98a11a1ca79052d65; original proof SHA256 9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302. This publication is a new concise exposition with newly reproduced verification. Historical comments in the original proof-only edition do not describe this package's new computations or priority search. Two sequential fresh reviews of the actual publication package are recorded separately in the repository after its byte freeze, avoiding a self-referential archive manifest.

## License

Original note and authored verification materials: Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/. Citations and public-source identities do not relicense third-party works.
