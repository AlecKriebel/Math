# Satoh: remaining shared checker integration

This editor did not modify or run the shared renderer/checker. The observed `verification/final-content-check.py` does not yet register record `23387442`. It must be extended before this paper can receive a rendered-content result. The existing renderer accepts the finalized configuration; the single ZIP now uses `supplement_filename`, with no additional-assets branch.

Register this source path in `TEX_PATHS`:

```python
'23387442': 'published-source/satoh_filtration_verification/satoh_filtration_counterexamples.tex',
```

Use the exact normalization below, also implemented in the owned `check-bindings.py`. The final abstract remains exactly equal to both normalized frozen candidates; no sentence was dropped.

```python
def normalized_satoh_abstract(body):
    body = body.replace('$', '').replace(r'\SL', 'SL').replace(r'\C', 'ℂ')
    body = body.replace(r'\setminus', ' ' + chr(92) + ' ').replace(r'\geq', '≥')
    return ' '.join(body.replace("Satoh's", 'Satoh’s').split())
```

Wire this into abstract-token comparison and require full normalized text equality, one paragraph, five sentences, and 104 words. Require the current TeX SHA-256 `6860fe1479f4fb0737489311e0b6c6ec4fda616e98e245feede72b4bde593af8` and the `source_binding.abstract_source` path. The raw abstract body, extracted with `.strip()` and without a trailing newline, has its independent hash in `final-abstract-check.json`.

The paper-specific checks should cover:

- Exact metadata title, author, ORCID, DOI, 15 October 2026 manuscript/Zenodo date, and record creation `2026-10-15T07:50:10.998117+00:00`. Display “Zenodo version 1.0”; the manuscript has no printed version number.
- Four PDF pages, two public assets, one distinct reader. The embedded PDF is an identical duplicate. Both original assets must be linked, served unchanged and CRC/hash checked; only the verification ZIP is the primary supplement.
- Both literal automorphisms and every rank/degree quantifier: `w=[[[x₁,x₂],[x₁,x₃]],x₁]`, `x₄↦x₄w`, `D_n(5) but not A_n(5)`, `n≥4`; and `v=[[[x₁,x₂],[x₁,[x₁,x₂]]],x₁]`, `x₃↦x₃v`, `D_n(6) but not A_n(6)`, `n≥3`. Other generators are fixed.
- The integral lower central series; rational SL(2,ℂ) matrix-entry algebra; action on the entire `J/J^{k+1}`; actual ideal powers. Avoid accepting a single associated-graded-piece or trace/character statement as equivalent.
- Explicit exclusions of degree five at rank three, every-degree failure, larger matrices, trace/character/Grothendieck algebras and the separate IA lower-central-series comparison.
- Classical identity credit, Razmyslov attribution through Burde, the exact 2018 Satoh question, and distinction of the inspected 2017 Satoh author preprint from its related 2021 final journal publication.
- Root-clearance hash `1a100a1722debd437303b74a81585a97cce3defca16923179af9fc5b912ede1f`, exact source receipts, all three unchanged report/verdict objects, and the original scope-pending status. The later root decision resolves that status; it does not rewrite the scope verdict.
- Unrefereed/AI status, no firstness or current worldwide-open-status claim, null follow-up, professional passive collaboration, and absence of private check counts or replay narrative from the public HTML.

The owned `editorial-checks.json` establishes pre-render bindings only. Root still needs to inspect the actual generated public copy, verify canonical/citation/structured metadata and index/sitemap integration, and finish live desktop/mobile/PDF/download and native tracker gates. No public-content or deployment approval is inferred from this document.
