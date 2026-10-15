# Frozen version acceptance

Independent mathematical audit completed on 7 October 2026.

Verdict: ACCEPTED. No mathematical correction is required to the frozen v2 proof. Its formulation limits and historical disclaimers should be preserved.

## Accepted version

- Version: v2_epsilon_extension, frozen 2026-10-07T19:42:06Z.
- PROOF.md: 10,165 bytes; SHA-256 a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1.
- MANIFEST.json: SHA-256 0256537fe98d411ca8911c22b341785d029e1f4b51f3a20207e056789bc8e380.
- All eight files listed in that manifest independently matched their recorded byte counts and SHA-256 hashes.
- The 185 exact author checks reran successfully and byte-matched checks.json, SHA-256 1da9fd49d0222a1ae94d75255ab10ab1dee7fe35f28dc2f371d647cfabb71173.
- Independently written exact controls also passed, including degree-0 through degree-3 evaluation ranks 1, 3, 6, 10, a cubic determinant of −128, and all eleven line restrictions.

## Accepted claims

1. The Robinson sextic R is globally nonnegative.
2. For every ε≥0, R+ε is not a finite SOS of real polynomials modulo the ordinary radical, real radical, or real vanishing ideal of either explicitly defined J_R or K_R.
3. Consequently the catalogue's (i) and (ii) hold for R, while its (iii) and (iv) fail. The same classification holds for R under the explicit separate-product reading.
4. For the tangency-minor formulation, (i)⇔(ii) holds generally by the candidate's sphere-minimization proof.
5. The separate Q example is a valid nonattaining-infimum counterexample to product-ideal (ii)⇒(i).

The independent review initially confirmed the exact-only candidate, then derived and checked the constant-perturbation strengthening. The author separately checked and integrated that extension into frozen v2. The original exact-only proof remains preserved. The final acceptance includes the positive-ε argument with its constants retained and its univariate degree lemma explicit.

## Exact target verification

The exact catalogue record for ID 30000717 and number OWR-1465-011 was inspected. Its statement explicitly asks the four-way equivalence using tangency differences and an ordinary radical in (iii), with all positive ε and the original ideal in (iv). Its record's claim of notation normalization does not erase the visible comma/ellipsis difference from the primary report.

The extracted record was compared semantically to the unique matching ID in the full problems corpus, with exact equality. Public verification metadata:

- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- Matched record: 4,590 bytes; SHA-256 c825ef251ba35435bc42b9b181955d49280da9074476d9f7e506012b13dbae1b.
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. Its exact top-level OWR-1465-011 key is absent. This is a bounded provenance check, not a comprehensive historical search.

No dataset contents are included in this acceptance.

## Primary and related source checks

The independently downloaded publisher report matched the recorded 559,967-byte source hash. Printed pp.798, 810, and 811 were freshly rendered and visually inspected. The DOI resolves to the EMS Press record for Reelle Algebraische Geometrie, Oberwolfach Reports 4 (2007), no.1, pp.753–820.

Additional supplied-source inspections confirm the scope distinctions: the gradient-tentacle manuscript's Theorem 25, Open Problem 33, and Theorem 46 use semialgebraic sets and an inequality multiplier; the ISSAC 2010 paper's p.2 includes M−f≥0 and the multiplier t(M−f) in its truncated-tangency certificate. Those statements are not contradicted by the ideal-only obstruction. The complete proofs of those external papers and exhaustive historical priority were not audited.

The source's ellipsis is not assigned an unverified intended meaning. The acceptance is for the explicit catalogue ideal J and explicit separate-product ideal K, each proved independently of that interpretive question.

## Publication boundary

This acceptance and the accompanying authored mathematical review, supplemental proof, code, exact results, and public verification metadata are suitable as the review record. Source PDFs, rendered source pages, catalogue records, and complete datasets are inspection material only and should not be copied into a public packet. The audit itself performed no publication.
