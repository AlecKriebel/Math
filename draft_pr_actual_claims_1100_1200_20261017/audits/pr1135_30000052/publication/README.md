# A three-point counterexample to a random lattice discrepancy comparison

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version1.0.0 · 17October2026.

This four-page research note records the full negative answer to Novak's displayed expected-pth-power comparison in Oberwolfach Report13/2004, printed698, reporting joint work with Hinrichs (problem30000052 / OWR-723-005). For independent continuous uniform generator and shift, three one-dimensional points have normalized anchored fourth discrepancy moment19/1620, exceeding the iid value4/405=16/1620 by1/540. The ratio is19/16. A separate no-wrap empty-tail argument gives2/[105(n−1)], exceeding iid for every integer n≥4. Complete-law equality at n≤2 proves the minimal point count; second moments agree for all n,d.

## Exact overlap, chronology and credit

Alper Ferudun's14October2026 unrefereed preprint, DOI https://doi.org/10.5281/zenodo.23372668, explicitly gives the same exact counterexample and broader results in dimensions and exponents, and uses the same empty-progression mechanism. It is prominently credited in the paper's abstract, related-work discussion, bibliography, metadata and provenance. The source PR1135 has GitHub creation record10October2026; this note is released17October. Historical public visibility of the repository and worldwide first discovery/publication are not certified. No causal inference about either author's awareness, dependence or copying is made. The negative answer is not claimed new relative to all current literature.

The broad priority review has52 actual queries,48 fetch attempts and16 PDF bodies with inspection boundaries; the rotation family51 searches and classification review7; the root17queries. Overlapping searches are not a distinct global total. No pre-PR full answer was identified in that bounded coverage. Several actual journal/full bodies remain unavailable, including Hinrichs/Weyhausen2012, original Sugita/Takanobu2000 and Sugita2002, Janson1988, Cesaratto/Vallée2012/2016 and several final-publication comparisons. Inspected abstracts/slides/preprints are not complete exclusions of inaccessible journal bodies. Source/version/access limits are in the full reports. Absence of a hit and historical open labels do not certify novelty.

The archive also records a NEW audit Fourier proof using classical formulas of Su2000 and Anderson et al.2007: a nonzero anchored discrepancy coefficient, common-phase cancellation and the Dirichlet fourth moment give a bound(2n²+1)/(48π⁴n³), reversing iid for n≥234. These generic older ingredients are credited; the new model-specific application is not mislabeled an earlier recorded solution. A fresh independent classification review addresses that distinction.

## Contents and provenance

- `main.tex` and `output/pdf/random-lattice-counterexample.pdf`: operative paper and frozen four-page reading copy.
- `verification/verify_all.py`, `CONTROL_PLAN.json`, `REPLAY_RECEIPT.json`: portable runner, exact input/checker/result pins and deterministic successful replay.
- `audit/inputs/`: all ten source-PR artifacts, unchanged. They retain their10October scope and historical literature claims; current paper and `audit/ROOT_PRIORITY_DECISION.md` supersede those summaries.
- `audit/reviews/`: three distinct mathematical audits, broad/focused priority audits and a fresh priority-classification review, with authored programs, results, query/retrieval/inspection metadata and fingerprint manifests.
- `audit/root_reproduction/`: independent parent programs and replay receipts; `audit/sources/`: bibliographic/version/chronology receipts only.
- `PROVENANCE.json`, `SOURCE_MANIFEST.json`: reviewed head, source-proof identity, exact scope, contemporary overlap and archive-member fingerprints.
- `zenodo-metadata.json`, `zenodo-deposit.json`: exact metadata and repository-relative upload manifest. The separate upload kit has the PDF, source archive, identical metadata, flat portable manifest and this README.

Historical receipts retain their original paths. Match files by the suffix after the audit folder and the recorded hashes. Third-party article bodies, extracted text, HTML, rendered images, downloaded source archives/raw API bodies and private caches are excluded. Current source and original source-proof editions are distinguished by their exact pins. No historical input is silently rewritten.

## Reproduction

Use Python3.10 or later with only its standard library; no installs or network access are required:

```text
python3 -B verification/verify_all.py
```

The runner executes seven unchanged programs in ordinary and optimized modes. Three independent mathematical families use inclusion-mask polygons, complete affine wrap strips with direct antiderivatives, and empty-tail simplex integrals. Two independent priority checkers verify Fourier/additive-energy and circular-gap transcriptions. Two parent programs separately reconstruct moments and the Fourier proof. Complete JSON results are compared; only the two parent historical execution-receipt wrappers are unwrapped to their `result` field. No mathematical fields are discarded. All ten input files, checker bytes, expected-result bytes and auxiliary input-pin files are verified. Python `assert` statements are rejected. Deliberate failure modes are exercised where the original programs provide them. Temporary mirrors leave the package unchanged.

The direct affine-cell integration additionally yields the supplementary n4 full moment139/17280. Neither analytic counterexample needs that value or software. Finite exact checks supplement universal written arguments; they are not formal proof certificates, a substitute for the primary-source target check, or exhaustive literature clearance.

## Rebuild and review status

Run `python3 -B build_package.py` to verify all pinned authored reviews, rerun the portable checks and deterministically recreate the source archive/upload kit. It uses fixed member lists, so later approval or publication receipts cannot silently enter a rebuild. The operative PDF is a frozen input, not silently recompiled. Under the same Python/zlib runtime an extracted source archive rebuilds byte for byte; compression runtimes may affect ZIP bytes while leaving member contents identical.

To revise the PDF, deliberately compile `main.tex`, inspect every page, replace the frozen reading copy and update its QA receipt before rebuilding. Current PDF/source pins identify the operative release. The repository Zenodo tool handles staging, exact metadata/checksum verification and publication separately; this archive does not publish itself.

AI tools were used extensively in proof development, computation, adversarial verification, literature research and writing. The note and supporting materials are unrefereed. Independent AI audits are not external human peer review, journal acceptance or proof-assistant certification. Original authored materials are CC BY4.0; third-party works retain their rights. No human outreach was prepared or initiated.
