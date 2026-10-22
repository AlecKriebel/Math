# Polynomial compatibility on the Boolean cube from disjoint-support separators

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X · Version 1.0.0 · 17 October 2026.

This four-page research note gives a complete affirmative deduction for Austrin's exact two-polynomial question, OWR 9/2025 printed p. 445 (30006210 / OWR-14299088-012). For all positive integers n,d, two nonzero REAL multilinear polynomials f,g of degree at most d on the UNIFORM sign cube have a common nonzero vertex if every coordinate relative influence of both is at most 1/(4096d^8). Relative influence is Fourier coefficient mass on sets containing the coordinate divided by the FULL squared L2 norm, including the constant coefficient. Disjoint supports force the stronger necessary maximum-influence bound 1/(1024d^8). The supports need not cover the cube. No optimality of constants/exponent, general distribution formulation, other-group, other-measure, or approximate-support theorem is asserted.

## Prior inputs and historical limits

The support separator is Li–Li–Li–Liu, arXiv:2608.03824v1 Lemma3.5 (4 August2026). Its proof totalizes common zeros; the note extracts the explicit depth 16d^4. The exact arbitrary-real covariance inequality is PRIOR O'Donnell–Saks–Schramm–Servedio 2005 section3.3 Eq(6), applied to 2h−1. The Bernoulli/Markov presentation is credited to Kothari–Kovacs-Deak–Wang–Yang arXiv:2601.08727v3; univariate Markov is classical. No new separator, covariance theorem, or generic Markov method is claimed. The target-specific application uses normalized square densities and adds their two separator covariances. Their absolute values sum 1 even on a cube with common zeros.

Three bounded primary priority approaches and root checks found no earlier recorded complete target-specific deduction in the bodies inspected. They do not certify novelty, first discovery/publication, or current global openness. Root logged 60 actual search executions, the separator approach 34, target approach 47, classification 39; these overlap extensively and are NOT summed into a unique global total. Some root queries had an extra opening quote and corrected reruns are separately logged; the counts are execution inventories, not novelty metrics. The full ePrint 2022/218 with its appendix and the full 2023/570 followup were inaccessible; the official thirty-page CRYPTO 2022 conference body was retrieved and is separately pinned. Other body/version/read limitations, unindexed or unpublished knowledge, talks and later citations remain explicit. A tracker calling a conjecture open is not substantive historical evidence. No firstness or causal independence certificate is inferred from Git/arXiv/PR dates.

The total rational/nondeterministic-degree theorem alone leaves a common-zero gap: the ratio p/(p+q) can be undefined. The prior Li separator supplies the missing completion mechanism. Removing polynomial compatibility from a cryptographic application is not equated with proving this target. The original report's old non-strict exponential endpoint fails at d=1 for 1±x; the strict CRYPTO 2022 statement and new safe threshold are distinguished.

## Contents and provenance

- `main.tex` and `output/pdf/polynomial-compatibility.pdf`: operative complete note and frozen reading copy.
- `verification/verify_all.py`, `CONTROL_PLAN.json`, `AUDIT_MEMBERS.json`, `REPLAY_RECEIPT.json`: portable offline runner, exact execution plan, immutable authored audit allowlist, and original replay receipt.
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210/inputs/`: all ten unchanged source PR artifacts at head b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2. These are historical editions: the new operative note/root priority decision adds direct OSSS credit and supersedes their older citation/verification inventories. The historical edition distributed no code; this new package distributes newly authored checkers.
- Under the same preserved audit prefix, `reviews/`: three distinct mathematical families and three bounded priority approaches, with their reports, code/results, source/query/version metadata, procedural-independence disclosures and authenticated receipts.
- `root_reproduction/` and root documents: parent exact controls, complete replays/actual mutation failures, original source authentication, mathematical reconstruction, priority decision and PDF QA.
- `PROVENANCE.json`, `SOURCE_MANIFEST.json`, `zenodo-metadata.json`, `zenodo-deposit.json`: provenance, exact member fingerprints, and identical publication metadata/upload manifest.

Original audit paths are preserved for unmodified historical utilities. Historical absolute paths and end pins are timestamped custody evidence, not current release manifests; identify portable members by relative suffix and digest. SOURCE_MANIFEST and the immutable allowlist identify this release. Third-party source bodies, copied source text/heading scans, extracted pages, HTML/raw API outputs, renders and caches are excluded. The priority-classification reviewer accidentally saw the old AUDIT patch after its independently recorded core; this is disclosed corroboration, not full blindness through completion. The target mathematical reviewer saw an unopened unrelated campaign snippet after its core; its limited exposure is also disclosed. No external human review is inferred from procedural AI audit independence.

## Reproduce the supplementary exact controls

Python 3.10+ and its standard library suffice; no installs or network are required:

```text
python3 -B verification/verify_all.py
```

The runner authenticates every frozen authored audit member and all ten original inputs, copies them to a disposable mirror, then runs FOUR mathematical programs in ordinary and optimized modes. These are the independent separator/monomial/Markov controls, exhaustive small-tree covariance/hybrid and square/Fourier controls, exact coefficient-box/support geometry controls, and new parent rational covariance/square/Chebyshev/endpoint controls. All mathematical output fields, code hashes and proof hashes are compared EXACTLY, including strict Boolean/integer type distinction. Only specified runtime timestamps, elapsed time, interpreter strings and optimization fields are excluded; actual interpreter/mode values are first validated where provided. No mathematical field or numeric tolerance is discarded. Forty actual wrong-mathematics subprocesses must fail with their expected diagnostics across both modes. Optimizable assert statements in mathematical checkers are rejected. No execution changes release members.

These finite checks supplement the universal proof and its source interfaces. They do not prove the result in arbitrary dimension by enumeration and are not formal proof-assistant or cryptographic-paper certifications. The code uses integer/Fraction arithmetic; no floating-point empirical estimate is promoted as proof. Original reviewer reports state their exact finite scopes.

## Rebuild and publication

Run `python3 -B build_package.py` to verify fixed inputs, replay the offline controls, and deterministically rebuild the source ZIP and five-member upload kit. The original frozen REPLAY_RECEIPT remains an archive input; a rebuild does not overwrite it with changing timestamps. The PDF is frozen and is not silently recompiled. Rebuilding an extracted archive under the same compression runtime reproduces exact ZIP bytes; different zlib versions may change compression without changing members. Future review, deposit, tracker and merge receipts cannot enter the fixed member list.

A deliberate paper revision requires compilation, all-page visual inspection, updated PDF QA/allowlist, rebuilt packages, and renewed independent review. The portable upload kit contains the identical PDF, source ZIP, metadata and a flat-path deposit manifest. The repository's production Zenodo tool handles staging/readback and publication separately. Neither builder nor verifier uploads or publishes anything. No GitHub release is needed.

AI tools were used extensively in development, writing, literature research, computation, reproduction and adversarial verification. This note and package are unrefereed; internal AI-assisted reviews are not external human peer review, journal acceptance or formal proof-assistant certification. Original authored material is CC BY 4.0; third-party works retain their rights. No human outreach was prepared or initiated.
