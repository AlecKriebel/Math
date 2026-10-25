# Bounded downstream integration note — 22089807

This is a source-bound preparation handoff. The editor did not change or run the shared renderer/checker and did not create rendered or live site output. The current renderer already resolves the two deposited assets, including the tar.gz, through `PublishedAssets`; no asset-helper mutation is required for this work. The config sets the correct tar.gz label. Root owns actual rendered public-copy approval, local/live HTTP, downloads/embed, desktop/mobile/browser and native tracker verification.

## Source shape

Add the exact paper mapping to the downstream content checker:

```python
'22089807': 'published-source/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/main.tex',
```

The existing `sources/record.json` path and `metadata` envelope are standard. The complete raw response remains `sources/record-raw.json`. Original `receipt.json` uses a string `record_id`, `files`, `name`, `bytes`, `sha256` and `zenodo_checksum`; preserve it unchanged. The existing `asset_name` and `normalized_receipt_view` interfaces accept it. Do not create `metadata.json` aliases, rewrite the receipt, or substitute an embedded PDF.

The deposited standalone PDF is the only public primary reader: 21 pages, SHA-256 `1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3`. The complete tar.gz is SHA-256 `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`, with 23 regular members and two nested wheels containing 1662 members. Its embedded 21-page PDF has the same basename but different bytes, SHA-256 `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`. The bound independent comparisons found date/layout differences, without mathematical text differences.

Keep `additional_assets=[]` and `source_binding.embedded_assets=[]`. The second reader is documented under `reviewed_documents` and retained inside the full tar, rather than incorrectly registered as a distinct public PDF under the colliding filename. The helper's ZIP-embedded resolution mechanism need not be extended for this deposit.

## Complete original abstract

The exact raw abstract body is in `ABSTRACT.tex`, and the entire normalized two-paragraph text in `ABSTRACT.txt` and `publication.json.abstract`. It has 214 whitespace-separated words after mathematical typography normalization. The source contains a display equation inside its first paragraph; removing `\[` and `\]` must not accidentally split that paragraph into three. A minimal safe normalizer is:

```python
def normalized_amplifier_abstract(body):
    body = body.replace('\n\\[\n', ' ').replace('\n\\]\n', ' ')
    for old, new in [
        ('R^6-8R^5+22R^4-30R^3+21R^2-6R+1.',
         'R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1.'),
        (r'r\in(1,R)', 'r ∈ (1,R)'),
        (r'1<r<\Rhyb', '1 < r < R_hyb'),
        (r'\Rsim\geq\Rhyb=1.5028569127905696\ldots>3/2',
         'R_sim ≥ R_hyb = 1.5028569127905696… > 3/2'),
        (r'\Rsim', 'R_sim'), (r'\Rhyb', 'R_hyb'),
        (r'(\sigma,\lambda)', '(σ,λ)'),
        ('$', ''), ('--', '–'),
    ]:
        body = body.replace(old, new)
    assert '\\' not in body
    return '\n\n'.join(' '.join(p.split())
                       for p in re.split(r'\n\s*\n', body.strip()))
```

Require whole-text equality, 214 words, two paragraphs, exact source/abstract-body hashes from `source_binding`, and equality to the frozen scope abstract after whitespace folding. Do not rewrite `reviews/scope/content.json` to insert paragraph breaks. The literal original abstract's final sentence reports the manuscript's open-problem statement; retaining that complete abstract is not an independent certificate of current worldwide openness. No additional openness, firstness or exhaustive novelty claim is made in the editorial copy.

## Custom scientific verdicts and later root authority

The exact root clearance is `verification/root-clearance-22089807-20261025.json`, SHA-256 `547296ed820667dfb47b36f796631c23f5eae67be7fb5c2ad898fb5d0bb72125`. `promotion.json` embeds the full original authority, all three original verdict objects, all three report/verdict hashes, the custody receipt, receipt bytes and original review-seal hashes. Do not replace the original custom fields with generic PASS statuses:

- Scope retains `status="COMPLETE"`, `mathematical_gate="not_decided_by_this_scope_verdict"` and `promotion_authorized=false`; its separate root disposition is `SCOPE_COMPLETE`.
- Analytic retains `verdict="PASS_STATED_CLAIMS"`; its separate root disposition is `PASS`.
- Adversarial retains `verdict="supported_as_stated_no_substantive_fault_found"` in the original uppercase `VERDICT.json`; its separate root disposition is `PASS`.

The later root scientific clearance resolves publication scope without rewriting the earlier held-scope chronology. A downstream gate must validate these exact objects and bindings rather than assume every reviewer used a common status schema. Preserve the original scientific reports and seals.

## Dates, canonical metadata and required rendered checks

The selected current record is version 2.0.4, published 25 August 2026. Citation metadata and `ScholarlyArticle.datePublished` therefore use `2026-08-25`. The earlier named same-work release 21852072 is dated 8 August 2026 and receives an explicit separate note. It is not another completed work and must not backdate 2.0.4. The standalone cover says August 2026; the embedded cover says 22 August 2026. Historical no-new-DOI and v2.0.3 prose remains frozen source history.

The proposed slug-derived canonical URL is already populated consistently in the config and proposed SEO payload:

`https://aleckriebel.com/research/simultaneous-amplifiers-beyond-three-halves/`

Root must generate and inspect the actual visible copy and scholarly tags, byte-identical standalone PDF/tar links and iframe, research-index entry and sitemap, date labels and citation/BibTeX. Only the native spreadsheet AA URL remains withheld until the proposed page is actually live and verified. Config canonical metadata is not a live-publication claim.

The public copy must retain the exact quantifier order, fixed interior fitness, connected loopless undirected weighted hypotheses, uniform singleton starts, distinct finite same-size pure Bd/dB benchmarks, lower-bound direction for unrestricted R_sim, restricted fixed-positive-parameter first-order response optimality, rational-edge specialization and vanishing gain. Preserve endpoint/uniform-onset/fitness-varying-with-size/finite-size/time/bounded-weight/empirical/mixed-process limits and prior credit to Svoboda2024, Tkadlec2020 and the separate earlier papers. Keep private audit dates, counts, hashes and replay narratives off the public page. Follow-up remains null.

The owned read-only check can be rerun with a fresh result name:

```text
python3 papers/22089807/reviews/editorial/check_bindings.py --output-stem root-bindings-rerun
```

It refuses an existing result filename and grants no rendered/live/browser approval. Do not rerun existing scientific/scope helpers with fixed outputs. The current live47/readiness51 state remains frozen pending root browser verification.
