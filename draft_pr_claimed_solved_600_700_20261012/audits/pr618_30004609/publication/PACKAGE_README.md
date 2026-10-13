# Low-exponent supersolvability: submission package

Current result: every finite central free arrangement over a characteristic-zero field whose nonzero exponents are 1 or 2, with at most one 3, is supersolvable. This includes products, nonessential arrangements and the trivial rank-zero lattice. The proof is the manuscript `low_exponent_supersolvability.pdf`; finite exact diagnostics do not replace its all-rank argument.

The paper and original authored supplementary work are distributed under CC BY 4.0. Third-party scholarly fulltexts, credentials, local environments, and private search corpora are excluded. Bibliographic links and inspected-source hashes are included for checking.

## Reproduce

Use Python 3.12 (the audited run used 3.12.14). From a clean extracted package:

```sh
python3 -m venv ../low-exponent-venv
../low-exponent-venv/bin/python -m pip install -r requirements.txt
```

This creates the environment outside the extracted packet for the strict inventory check. Then run its Python against the packet:

```sh
../low-exponent-venv/bin/python verify_package.py
```

The standard-library integrity-only check is `python3 verify_package.py --integrity-only`. Do not write logs, environments or cache files inside the packet: it intentionally has an exact inventory. All computational replays occur in a temporary copy, and the original packet is checked again afterward. The algebra script writes its result in that temporary copy. The author check and older independent audit are replayed; the fresh incidence enumeration, non-Fano certificate and fresh algebra/lattice checks are then compared with their frozen exact results.

`PACKAGE_MANIFEST.json` hashes every member except itself. The archive uses safe relative paths and includes no links. The PDF source is standalone LaTeX. Create an external build directory with `mkdir -p ../low-exponent-pdf-build`, then run `tectonic --outdir ../low-exponent-pdf-build low_exponent_supersolvability.tex`. This leaves the frozen packet untouched. Compiler output can contain timestamps; a fresh compilation need not have the identical PDF hash, but the deposited PDF is frozen and hashed.

## Current priority and historical snapshots

`CURRENT_PRIORITY_AND_STATUS.md` is the current publication assessment. `candidate/` preserves the October 4 packet byte-for-byte, including its then-current pending-review and novelty wording. Those dated statements are historical records, superseded by the current assessment and manuscript; they must not be read as current assertions that no matching paper exists. The fresh reports under `reviews/` identify earlier antecedents and Ferudun's matching October 12 preprint. The GitHub and Zenodo chronology supports the specific dates recorded, with the stated limits; exhaustive first priority and independent development are not certified.

AI tools were used extensively for development, writing, reproduction and adversarial review. The internal reviews are AI-generated and do not constitute independent human peer review. This is an unrefereed preprint. No external researchers were contacted.
