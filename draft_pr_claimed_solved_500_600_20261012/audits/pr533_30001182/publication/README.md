# Ambient dependence verification package

Paper: **Ambient Dependence of Extremal-Exchangeable Independence**, Alec Kriebel (ORCID 0009-0001-9320-500X), version 1.0, 12 October 2026. Unrefereed, extensively AI-assisted, no human peer review or formal certification. CC BY 4.0.

The note answers the displayed unrestricted definition in Liebscher OWR 09/2009, printed p. 540, item (1). It proves actual ambient dependence, separately proves algebraic non-lifting, and explains positive C*-lifting. Extremality is among all exchangeable states. Faithful-only, tracial-only, fixed-marginal extremality, trivial-tail and normal W*-variants are outside its claim. Known pure folding is credited. Historical-first priority and continued open status in 2026 are not certified; consult the bounded source audit and its exact remaining leads.

## Verify offline

Use Python 3.10 or later, without optimization:

```sh
python3 run_all.py
```

No third-party Python packages or network access are needed. The runner checks every archived file against MANIFEST.json and cross-checks all preserved inner manifests, rejects missing/extra/changed payloads and optimized execution, and runs original controls plus independently authored operator, extension, source-scope and parameter/boundary checks. Scripts that write reports are run in scratch copies. Repeated runs leave the sealed files unchanged. A virtual environment or Python cache may be present; neither is an archived payload. The manifest protects consistency and is not a cryptographic authenticity signature.

Universal all-witness/all-word proofs are in ambient_independence.tex, original/public/PROOF.md, reviews/operator01/REPORT.md and reviews/extension01/REVIEW.md. Finite checks do not establish those quantifiers. Source/category and prior-work evidence is in reviews/source01/; full downloaded papers/datasets are omitted. Original authored records and their frozen manifests remain in original/ as historical evidence. Current scope clarifications are in CORRECTIONS.md.

## Rebuild the reading copy

The separate deposited PDF SHA256 is 5b271d3fa00e4353314996e77c0d2055c1bf33e95635a9543679c688472a4de5. Rebuild outside this verified directory so generated files do not alter its strict inventory:

```sh
mkdir -p ../pdf-rebuild
SOURCE_DATE_EPOCH=1791806400 tectonic --outdir ../pdf-rebuild ambient_independence.tex
```

The recorded compiler/build and visual QA are BUILD.json and PDF_QA.json. Rebuilds should preserve content; compiler/font differences may affect PDF bytes. metadata.json records the supplied deposit configuration, with paths relative to the deposit directory holding the separate PDF and ZIP.

Fresh complete-package adversarial review reports are kept in the [repository audit](https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_500_600_20261012/audits/pr533_30001182/reviews), with frozen artifact hashes. They are outside this ZIP to avoid cyclic artifact/report hashes. Acceptance and DOI receipts, when obtained, are recorded separately in that audit.
