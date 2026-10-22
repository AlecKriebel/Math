# A fixed-area exceptional set for positive squared-pole sums

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version 1.0.0 · 17 October 2026.

This four-page research note gives a full affirmative mathematical deduction for Baernstein’s question, Hayman–Lingham Problem 7.37 (2307037 / AMR-022-7037). For every finite positive normalized sum g(z)=sum lambda_j/(z-z_j)^2, with arbitrary complex or repeated poles, one compact set S(g) of exact area pi works simultaneously for every real R>1:

`integral over D_R outside S(g) of |g| <= 2*pi*log(R) + pi*(log(2)+1/e)`.

The integral is ordinary and finite. The leading coefficient 2*pi is sharp; the additive constant is not claimed optimal. The proof identifies the quadrature field on every complement component, including holes, and fixes S before the radius is selected.

## Established inputs and priority limits

The indicator-transform inequality is due to Eremenko–Hamilton (1995), building on Astala. Quadrature existence, regularity and finite smash sums are established Levine–Peres (2009 manuscript/2010 journal) results with Sakai and partial-balayage antecedents. No new singular-integral theorem, quadrature construction or general balayage/operator principle is claimed. Yongxi Lin’s related partial-balayage principles and André Guerra’s 2026 real-input Beurling weak-type work are credited in the paper and metadata. The generic ingredients used here were logically available by 2009; a newly supplied exact-target deduction is not mislabeled an earlier recorded full solution.

The bounded priority search identified no verified pre-PR explicit full-target answer. It does **not** certify historical novelty, worldwide first discovery/publication or current global openness. In particular, Leung preliminary reports titled *On a fixed area problem* are indexed in AMS Abstracts 11 (1990), p.181, and 13 (1992), p.440. Their mathematical text was inaccessible in the inspected restricted scans; relevance to this target remains unresolved. Both records and exact body locations are documented in the dedicated supplement. The 1992 title lead in the sealed earlier classification report was real but incomplete earliest-title coverage; its sibling correction adds 1990 without silently editing the earlier audit.

Other unavailable full/final texts include Macintyre–Fuchs 1940, parts of the Sakai/antecedent quadrature literature, EH 2002 full chapter, several final journal/version comparisons and Eiderman 2007. Actual sources, versions, access failures and inspection boundaries are recorded; preprints, previews, titles and source restatements are not represented as full-body exclusions. The broad audit has 95 actual queries, analytic 58, classification 40, Leung supplement 65 plus structured discovery, and root 45. Searches overlap and are not summed into a global distinct total. Lin’s inspected PDF matches a Git-version body with 5 October metadata, before the source PR’s 10 October creation metadata; those dates do not certify historical public visibility or causal independence. No firstness or causal attribution is made.

An independently scoped follow-up verifies that the 2002 EH correction concerns the combined general-distortion coefficient/sharpness wording. The exact indicator estimate used here follows from the retained conformal-on-E part(i). Full chapter unavailable; the relevant primary publisher preview and actual 1995 derivation were inspected. The report reproduces the first-order expansion and bilinear L2 duality, including the extra-area-term guard against using the wrong general theorem.

## Contents and historical editions

- `main.tex` and `output/pdf/fixed-area-squared-poles.pdf`: operative note and frozen reading copy.
- `verification/verify_all.py`, `CONTROL_PLAN.json`, `AUDIT_MEMBERS.json` and `REPLAY_RECEIPT.json`: portable runner, frozen authored-file inventory and complete diagnostic replay.
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1136_2307037/inputs/`: all twelve unchanged source PR artifacts at head cbbe7826cca914588018c840ba99c6b7a59fa7f5. They retain their historical 10 October scope. Current paper/root decision supersede historical priority and source-inspection summaries.
- Under that same preserved audit prefix, `reviews/`: three distinct mathematical families, three priority approaches, EH correction check and Leung supplement, with complete authored reports, code/results, source/version/query metadata and authenticated manifests.
- `root_reproduction/` and root documents: independent parent controls/replays, mathematical reconstruction, source authentication, final priority decision and PDF QA.
- `PROVENANCE.json`, `SOURCE_MANIFEST.json`: provenance and exact archive-member fingerprints; `zenodo-metadata.json` and `zenodo-deposit.json`: identical publication metadata and upload manifest.

The original audit hierarchy is preserved so historical unmodified path lookups remain usable. Original receipts retain their timestamped historical input/end pins and absolute-path strings; those are not asserted to be current release manifests. Match by the audit-relative suffix and hash; current ARTIFACT_RECEIPT records and SOURCE_MANIFEST identify release members. Third-party full bodies, extracted text, HTML, raw API responses, downloaded archives, rendered images and private caches are excluded. The analytic reviewer disclosed accidental late exposure to an embedded prior-audit introduction/metadata after its own core derivation; strict end-to-end isolation is not claimed for that reviewer. The other two mathematical reviews were isolated. AI audit independence is procedural and limited, not external peer review.

## Reproduction

Python 3.10 or later and its standard library are sufficient. The default requires no installs or network:

```text
python3 -B verification/verify_all.py
```

It authenticates all 118 frozen authored audit members and twelve source artifacts, then runs three mathematical programs in ordinary and optimized modes in a disposable mirror. These are the parent’s exact/rational and scalar controls, the independent Green-boundary/oval/hole quadrature diagnostics, and the independent Beurling/scaling/localization controls. Complete outputs are compared. Two explicit process metadata fields in the quadrature output are adjusted to the executing runtime; no mathematical fields are discarded. Integer/string/Boolean results are exact; floating diagnostic fields allow absolute or relative roundoff of 1e-12, while every original checker independently enforces its own numerical thresholds. Four actual corrupted-oracle executions must fail with the expected diagnostic. Optimizable Python assert statements are rejected. No program modifies the release files.

The fourth independent target reviewer’s checker also authenticates the exact primary Hayman–Lingham PDF, intentionally excluded from this archive. To reproduce that additional source-bound control and its six ordinary/optimized mathematical-mutant failures, explicitly fetch the hash-pinned primary PDF in the temporary mirror:

```text
python3 -B verification/verify_all.py --with-target-source
```

Alternatively supply a previously retrieved matching PDF with `--target-source-file PATH`. The required source URL, byte count and SHA-256 are in CONTROL_PLAN; changed primary bytes or unavailable access cause a clear failure. This optional source check is not silently counted as an offline execution. The target source is removed with the disposable mirror and never incorporated into the published ZIP.

All floating computations are diagnostics, not rigorous error enclosures or formal proof certificates. Finite examples and rejected wrong alternatives supplement, rather than establish, the universal written proof and its imported source interfaces. The original mathematical reports include further supplementary observations, including a modest split-parameter improvement; the operative theorem deliberately retains its displayed simpler constant and does not claim it optimal.

## Rebuild and publication

Run `python3 -B build_package.py` to check all frozen audit pins and replay the offline controls, then deterministically rebuild the source archive and five-member upload kit. The frozen REPLAY_RECEIPT remains an original execution record; rebuilds do not replace it with changing runtime metadata. The PDF is a frozen input, not silently recompiled. Under the same Python/zlib runtime, an extracted source archive rebuilds byte for byte; compression runtimes may alter ZIP bytes without altering member contents. Later approval/deposit/tracker/PR receipts cannot enter the fixed member list.

To revise the paper, deliberately compile the source, inspect every page, replace the frozen PDF, update PDF QA and audit-member pins, and rebuild/review the new release. The separate Zenodo kit contains the identical PDF, source archive, metadata and flat portable deposit manifest. The repository’s production upload tool handles staging, metadata/checksum readback and publication separately. Neither the verifier nor builder publishes anything.

AI tools were used extensively in proof development, computation, adversarial verification, literature research and writing. These materials are unrefereed and have not undergone external human peer review, journal acceptance or formal proof-assistant certification. Original authored material is CC BY 4.0; third-party works retain their rights. No human outreach was prepared or initiated.
