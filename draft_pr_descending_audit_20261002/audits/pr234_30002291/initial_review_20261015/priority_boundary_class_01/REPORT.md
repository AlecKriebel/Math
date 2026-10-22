# PR234 / 30002291 — independent boundary-class priority audit

Audit lane: priority_boundary_class_01. Completed 2026-10-15 UTC. Frozen inputs: PROOF.md, SOURCE_SCOPE.md, KNOWN_RESULTS.md only. No sibling findings were read. No Git, index, branch, remote-provider, release, or external-person communication actions were taken.

**Disposition: PRIORITY UNRESOLVED; a significant additional prior overlap is confirmed.** The explicit full candidate class has not been matched to an earlier controlling theorem in this lane. This is not a certification of novelty. The nonsymmetric Lévy subcase with index below two is already covered by a primary preprint associated with a 2019 EJP article. The finite-quadratic-rate index-two endpoint and arbitrary predictable compensator shape remain outside the explicit hypotheses of the closest originals examined here. Two inaccessible primary leads prevent treating this search as closed.

## Exact question and criteria

The candidate concerns the singular convolution with deterministic kernel g=x_+^α f, 0<α<1/2 and exponential C¹ tails. Its driver has bounded drift and uniformly bounded quadratic jump-compensator rate, with arbitrary predictable ν_s(dz)ds. The conclusion is the Δ^(−2α) increment-square statistic converging jointly at finitely many fixed times, stably relative to the entire original sigma field, to squared driver jumps marked by W_α of fresh independent uniforms.

An anticipation finding requires an earlier theorem, or a checkable specialization of one, covering those assumptions and that conclusion. Broader model definitions, abstracts, citation counts, informal claims that symmetry can be removed, and non-dilation examples do not suffice. A narrower earlier theorem is recorded as overlap. A failed retrieval is an unresolved source gap.

## Main determinations

| Proposed extra scope | Finding in this lane | Consequence |
| --- | --- | --- |
| Nonsymmetric Lévy drivers, index β<2 | Exact prior overlap: S03, specializing the general-function theorem to x² using an auxiliary exponent below 2 | Do not promote removal of symmetry alone as new |
| State/path-dependent scalar volatility | Already substantial prior overlap S02 | Mere non-Lévy or dependent volatility wording is insufficient |
| Finite quadratic rate with β=2 | Explicit endpoint is excluded by S01–S06; S03's quadratic specialization cannot cross it | A real hypothesis difference, with priority still unresolved |
| Arbitrary predictable compensator whose mark distribution changes shape | Not supplied by the scalar-volatility model S02 or independent-noise field model S04 | Noncontainment in those stated classes is established, not novelty |
| General martingale convolution / shot noise / ambit terminology | S09, S10, S12 and model leads do not supply the remaining theorem under their examined controlling scopes | Naming a broader process class does not establish limit-theorem coverage |
| Functional M1 / full-original-sigma-field phases | Prior literature already supplies these in major overlap classes | The candidate's finite-dimensional topology is weaker; this is not a stronger-topology contribution |

Source facts, original locations, dates and access qualifications are kept in EVIDENCE_LEDGER.json to avoid repeating source-derived prose. All mathematical specialization and separation arguments are in DEDUCTIONS.md.

### The additional prior that should be added to the candidate bibliography

S03 is Basse-O’Connor, Heinrich and Podolskij, *On limit theory for functionals of stationary increments Lévy driven moving averages*, [arXiv:1806.10352](https://arxiv.org/abs/1806.10352), associated with [DOI 10.1214/19-EJP336](https://doi.org/10.1214/19-EJP336). Its original preprint, not a search summary, controls the nonsymmetric overlap finding. DEDUCTIONS.md §1 gives the complete quadratic specialization. The final publisher PDF was not successfully retrieved; the result is therefore attributed precisely to the independently retrieved 2018 primary preprint rather than asserted as a version-checked statement about the final typeset text.

The earlier AOP preprint also explicitly discusses symmetry as a simplification (S01). That discussion is weaker evidence than an exact theorem; S03 supplies the exact theorem-level overlap.

### Why the index-two separator survives this comparison

DEDUCTIONS §3 proves that the submitted logarithmic Lévy density has total quadratic rate 2 and index exactly 2. Its small-jump quadratic mass tends to zero logarithmically, with no smaller power moment. Thus it satisfies the candidate's L² truncation input while violating a strict exponent-below-two condition. Allowing the tail-integrability parameter θ=2 in an existing theorem does not change its separate small-jump restriction β<2. Neither the critical-kernel cases in S05 nor the higher-dimensional fields in S04 close this endpoint in their examined original statements.

This is a statement about nonimplication from checked theorem hypotheses. An earlier theorem based directly on L² truncation could still anticipate the endpoint. Searches did not produce such a controlling original; that absence is not a proof that none exists.

### Why general predictable compensators remain a separate comparison

DEDUCTIONS §4 supplies an explicit admissible deterministic compensator switching from δ₁ to δ₁+δ₂. Its mass and support change rule out a scalar pushforward of one fixed Lévy measure. This cleanly establishes a class difference from S02. It does not establish mathematical depth or priority: the example is finite activity, admits a simple two-noise construction, and follows the same finite-impulse mechanism. A general marked-Poisson integrand representation must also be checked before claiming that a theorem phrased using a random measure is outside the candidate's class.

The strongest unanticipated-scope hypothesis supported by this lane is therefore the **combination** of general predictable compensator shape, no required exponent below two, and the exact singular-convolution limit. It is not a claim that time dependence, asymmetry, nonstationarity, or dependent volatility are individually novel.

## Search coverage and unresolved primary access

The search covered exact titles/DOIs and forward/backward leads from the main papers, author/institutional bibliographies, critical cases, later general-function and infinitely divisible-field papers, two theses, martingale-Volterra covariation/variation, fractional-integral processes with jumps, generalized shot noise, ambit references, and current primary work through 2026. A 2024 preprint associated with a 2026 survey was used as a bibliography guide; a 2026 shot-noise original was examined as an adjacent scaling regime. Search pages and secondary aggregators were navigation aids only, never controlling theorem evidence.

The following remain material access limitations:

1. **S13, 2018 Ambit Stochastics chapter, pp99–114.** Publisher abstract/table of contents and its general-LSS subsection were located; full text was unavailable. No claim that the chapter lacks a general compensator theorem follows from its abstract.
2. **S14, Liu–Zhang–Fang generalized-difference fractional-integral paper.** Primary publisher dates and abstract were retrieved; PDF and full text returned 403. The actual model and theorem must be inspected before classifying its relation to the candidate. It is not counted as either anticipation or exclusion.
3. Final typeset versions of S01–S04 were not all independently acquired. Primary preprints were acquired and hashed. In particular the new S03 overlap is explicitly a preprint-level finding, sufficient to show prior public theorem evidence but not a version comparison.

S15's primary abstract explicitly identifies an additive Gaussian-integral-plus-Lévy model, helping distinguish that neighboring literature. It does not license assuming S14 has exactly the same model. No outside individual was contacted, and no copy-request mechanism was used.

## Recommended use in the overall review

The candidate bibliography should include S03 and distinguish prior asymmetric Lévy overlap from the remaining general-kernel and endpoint claims. Preserve the statement that the proof follows the known finite-jump truncation method. An accurate possible description is: an explicit bounded-characteristic sufficient-conditions extension, including an index-two L² endpoint and general predictable compensator kernels, with priority of that combined class still under review.

Do not convert the current source audit into either a full-class anticipation verdict or a new-discovery certification. The exact outstanding gap is a version-checked controlling original that includes the combined driver class, or a documented resolution of the primary access leads plus a broader systematic priority investigation. The mathematical correctness review is a separate question and was not reopened by this lane.

## Reproducibility and artifact handling

- EVIDENCE_LEDGER.json: searchable safe source facts and exact controlling locations.
- SEARCH_LEDGER.tsv: query families, query strings, outcomes and preserved raw-search identifiers where available.
- source_provenance*.json and metadata_provenance.json: acquisition times, URLs, response identities and SHA-256 hashes.
- read_provenance.json: exact frozen-input hashes and honest reading-level records.
- DEDUCTIONS.md, check_scope_separators.py, SCOPE_CHECKS.json: checkable overlap and scope-separation certificates; 16 exact-rational auxiliary-exponent checks passed.
- SAFE_ARTIFACT_MANIFEST.json: safe authored artifact hashes and private-cache inventory hashes.

Full PDFs, full extracted texts, raw bibliographic payloads and raw preserved searches remain under ignored private/. Their contents are not publication artifacts. All public source summaries are authored, short and without long quotations. No absence-of-hits inference is used as a novelty proof.
