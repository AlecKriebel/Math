# All-load stability of a deterministic-first-chunk file-sharing chain

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0,
20 October 2026. Unrefereed preprint draft.

The accompanying paper proves positive recurrence for every fixed real
arrival rate lambda > 0 for the exact six-rate continuous-time chain in
its equation (1). The seed is permanent, empty first-choice waiting rooms
are invisible to the sampling denominator, and completed peers depart
immediately. This is the model of the historical 2010 Oberwolfach stability
conjecture and the checked January 5, 2011 author proof. Catalogue identifiers:
30001608, OWR-4530-006; originating PR https://github.com/AlecKriebel/Math/pull/292,
head 1198534928f4c2bf8bf758c9ceb16edaa3a496e8.

The all-state, all-real-load conclusion follows from the analytic proof in
`main.tex`. Finite controls do not prove a universal quantifier. No uniform
bound in lambda, finite stationary population moment, performance bound,
geometric ergodicity, or result for another protocol is asserted.

## Reproduction

Extract the ZIP into its own directory. Use standard Python 3.11 or newer,
without `-O` or `PYTHONOPTIMIZE`; no third-party Python packages or network
access are required. From the extracted `dfc_stability_verification` directory:

```
python3 reproduce.py --integrity-only
python3 reproduce.py
```

The full run verifies every distributed payload and reproduces the original
four rounds of controls, the original portable independent controls, the
fresh independently solved tridiagonal Poisson corrector and boundary controls,
the fresh source/model controls, and the exact protocol distinction controls.
It also requires an intentionally false protocol identity to fail. Child
scripts execute in a temporary copy, so frozen expected outputs remain intact.
The script checks the original directory again after reproduction. Temporary
space is removed automatically. Depending on hardware the complete run can
take several minutes.

The source/model script includes a fixed-seed finite-horizon Monte Carlo
diagnostic. Only that diagnostic's floating-point values admit relative or
absolute roundoff tolerance 1e-10 in the wrapper; its integers and all exact
rational control outputs are compared exactly. Volatile timestamps and elapsed
seconds are excluded from comparison. The theorem-transfer numerical control
illustrates an analytically derived limit; its floating-point output is not
the proof of that limit. See `reviews/priority_recheck_02/DERIVATIONS.md`.

Build `main.tex` with a standard LaTeX distribution supporting amsmath, amssymb,
amsthm, geometry, fontenc and hyperref, for example `latexmk -pdf main.tex` or
`tectonic main.tex`. The distributed PDF was built with Tectonic 0.17.0;
PDF byte identity is not a mathematical requirement. The separately supplied
PDF has the same source hash recorded in `BUILD_RECEIPT.json`.

## Contents and provenance

- `main.tex`, `BUILD_RECEIPT.json`, `PDF_VISUAL_QA.json`: paper source and build/layout provenance.
- `PUBLICATION_METADATA.json`: intended Zenodo bibliographic metadata.
- `MANIFEST.json`: SHA-256 and byte length of every payload except the manifest itself.
- `SOURCE_SNAPSHOT.json`, `original/`: all 40 original files, byte-for-byte from
  the pinned PR head, including proof iterations, controls and historical status
  records. Their old review/publication statuses are historical evidence, not
  the status of this new paper. The original nonportable reviewer is retained;
  its exact one-path adaptation is the runnable portable script.
- `reviews/foster_recheck_02/`: fresh all-state derivation, exact tridiagonal
  control program, 315600 new exact assertions on 11330 states, 20 negative
  controls, frozen outputs and evidence-chain checks.
- `reviews/source_recheck_02/`: independent model/source derivation and controls
  on 1635 exact states with four negative controls, plus the explicitly labelled
  finite-horizon diagnostic and limitations of an alternative approach.
- `reviews/priority_recheck_02/`: owned review text, derivations, reading ledger,
  query scope and reproducible protocol/transfer comparisons. Third-party papers,
  downloaded website bodies and images are not redistributed.
- `ROOT_ANALYTIC_ASSESSMENT.md`: the root auditor's rederivation and scope assessment.

The manifests are integrity receipts, not proof-assistant certificates. Test
counts overlap between historical and replayed controls and should not be
summed as independent evidence.

## Literature scope and disclosure

The elementary workload drift already proves the small-load range
0 < lambda < 1/2. The contribution is the all-load certificate, not the first
stable example or a new general Foster criterion. The 2009 preprint made the
opposite high-load conjecture; the 2010 report and checked 2011 author proof
state stability. The complete 2012 Allerton Common Chunk paper was inspected;
its generator and operative Foster function do not transfer directly to this
chain. Its final unresolved conjecture concerns a different algorithm.

An extensive bounded review found no earlier exact all-load theorem in the
inspected sources. The final 2011 publisher body, the final 2015 journal extension
of the Allerton work and some later bodies were not inspected. This absence
from the checked evidence is not evidence that those texts contain no relevant
result. No worldwide-firstness or continuing-openness certification is made.
The reading ledger distinguishes full-text reading, checked author proofs,
abstract-only evidence and access failures.

AI tools were extensively involved in research, proof development, computational
verification, manuscript preparation and adversarial auditing. This is an
unrefereed preprint and has not undergone formal independent human peer review.
Internal AI reviews do not constitute human peer review.

Copyright (c) 2026 Alec Kriebel. The original authored materials in this package
are licensed under Creative Commons Attribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/. Bibliographic citations and hashes
identify third-party sources; those sources are not redistributed here.
