# Later root checker integration — 23306332

Only this paper's publication/promotion files and owned publication-review artifacts were prepared. No shared checker, renderer or site was edited or executed by this editor. Root still owns actual public-copy inspection, rendering, local/live HTTP, desktop/mobile/browser and native tracker gates.

## Preserved source shape

Add this exact `TEX_PATHS` mapping, including both package directories:

```python
'23306332': 'published-source/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics.tex',
```

The raw acquisition uses **`sources/metadata.json`**, not `sources/record.json`. Its SHA-256 is `82e624db015b8f612e7d1eb56463b6c035130e88d4579887c3b5306ef3dd9bdd`. Both `source_binding.metadata_path` and `source_binding.record_path` explicitly point to that preserved file. The raw receipt uses `metadata_sha256`, an integer `record_id`, and `filename` in its original `files` list. The existing renderer's `PublishedAssets`, `asset_name` and `normalized_receipt_view` interfaces accept that list without mutation; the owned check confirmed asset resolution. The shared content checker's hard-coded `record.json` read needs a narrow metadata-path accommodation for this record. Do not create a source alias or rewrite the raw receipt.

The raw receipt SHA-256 is `1267dcd347b53c295116bac15151fa92dff359469da3c0c7e16c1e6a8de3d53a`. The PDF and standard verification ZIP are the only original assets. There are six searchable reader pages and 12 regular ZIP members, with no embedded PDF, nested archive or additional reader. `additional_assets=[]` and `source_binding.embedded_assets=[]`.

## Complete original abstract

Use this conservative normalization before generic abstract tokenization:

```python
def normalized_quadratic_abstract(body):
    return ' '.join(body.replace('$z^2$', 'z²').split())
```

Require full normalized text equality, 124 whitespace-separated words, seven complete sentences and one paragraph. Also require equality with the frozen `reviews/scope/public-candidate.json` field **`full_original_abstract`**, rather than an assumed `abstract` key. The exact raw body is in owned `ABSTRACT.tex` and the normalized whole paragraph in `ABSTRACT.txt`. There are no omitted sentences.

- TeX SHA-256: `caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677`.
- Stripped abstract-body SHA-256: `e923d5b23fa4b00127bb3c3b1a9ec5382d45ebb2d366aadab0ce6f3e959c8aff`.
- Frozen scope candidate SHA-256 is explicitly bound in `source_binding.frozen_scope_content_sha256`.

## Metadata and chronology

The printed manuscript date is exactly:

```python
r'\date{11 October 2026\quad\textnormal{(research note; unrefereed preprint)}}'
```

The manuscript prints **no version number**. Zenodo metadata gives version `1.0`; therefore the prepared labels are `Manuscript dated`, `Zenodo version 1.0`, and `manuscript_version=null`. Keep the creation timestamp `2026-10-11T23:14:10.664861+00:00` separate from the manuscript date and declared publication date `2026-10-11`. No priority or first-public-availability inference is authorized.

The exact root authority is `verification/root-clearance-23306332-20261025.json`, SHA-256 `9faabde229535455e707dfae14639727c129953be08b08b2984299a83da0b436`. `promotion.json` retains the entire authority object and all exact original review objects/hashes. The original schemas are custom:

- Analytic: `verdict="PASS_WITH_BOUNDED_BIBLIOGRAPHIC_LIMITS"`, with `publication_clearance=false`.
- Adversarial: `result="no_substantive_mathematical_defect_found"`, with `promotion_clearance=false`.
- Scope: `scope_status="COMPLETE — conditional scope candidate ready"`, `mathematical_pass=false`, `mathematical_verdict=null`, `promotion_authorized=false`.

Do not fabricate generic original `status="PASS"` values. Root dispositions for analytic/adversarial are separately `PASS`; scope is separately `SCOPE_COMPLETE`. The later root clearance resolves all four mathematical claims while preserving this original chronology. The root-sealed scientific reports and seals remain unchanged.

## Required actual rendered-content checks

Check the actual visible sections, full abstract, title/author/ORCID/DOI, scholarly/canonical/citation metadata, date/edition labels, exact PDF/ZIP links/downloads/embed, index/sitemap, unrefereed/extensive-AI disclosure, passive contribution-based collaboration and absent follow-up. Content requirements are:

1. Complex monic `z²+az+b`, closed-half-plane stability `α≤0`, all complex stable competitors, repeated and imaginary-axis roots, coordinates `(Re a, Im a, Re b, Im b)`. For **each fixed** real SPD coefficient metric, **every neighborhood** of zero contains **some unstable** input with at least two distinct **attained global** nearest stable polynomials. No claim covers every nearby target.
2. Full exact degree `ℓ≠0`, base `(1,0,0)`, all six real coefficient directions, both leading-coefficient directions, and fixed SPD coefficient metrics. The original set is not globally closed. Compact clipping within `ℓ≠0` and the `R/3` versus `2R/3` comparison supply global attainment in the original set.
3. The **entire epigraph**, monic and full, fails set prox-regularity at height zero under each fixed SPD coefficient/height metric, including mixed metrics. The limiting horizontal object is a **covector**; its representing vector can tilt.
4. The positive **function** statement is separate: monic abscissa, real Euclidean coefficient metric, **each fixed finite limiting subgradient** selected before the local constants. Constants may depend on that subgradient. No uniform-all-subgradient, full-degree-function or all-mixed-metric extension. The `(v₀,−1)` epigraph normal differs from the horizontal set obstruction.
5. Both nonnegativity conditions in the exact stability chart; actual proximal-normal sequence, cubic support versus quartic squared displacement, classical PRT global projection characterization and its closed/finite-dimensional hypotheses. Credit the classical root/normal calculus, related Whitney-umbrella geometry and earlier nearest-stable approximation work.
6. Exact Lewis2003 complex convention and qualified OWR2005 Question1: the short OWR wording omits field, normalization and metric. The real monic slice is a convex orthant with unique fixed-SPD projection. No real-only or all-degree classification, arbitrary norm/singular/varying metric theorem, nonlinear parameter-metric transfer, explicit input/minimizer pair, firstness or current-open claim.
7. PR2010 Theorem3.1 is a conditional composition result and does not itself supply unconditional exact subdifferential equality. The direct two-sided diffeomorphism/lower-support proof supplies the equality. Do not assert unchecked precise Cross/Moses–Liu/Bottema original-body comparisons. Preserve bounded source credit and access limitations.
8. Finite exact/Decimal diagnostics supplement analytic proof; decimals are not interval certification. Keep private audit/replay counts, custody hashes and dated internal review narratives off the public page. Null follow-up remains appropriate to the stated high bar.

The owned helper is **pre-render editorial validation only**. It refuses an existing output filename. For a later read-only rerun choose a fresh stem, for example:

```text
python3 papers/23306332/reviews/publication/check-bindings.py --output-stem root-bindings-rerun
```

Do not rerun existing fixed-output scientific or scope helpers. No public-page approval or publication action follows solely from the prepared artifacts.
