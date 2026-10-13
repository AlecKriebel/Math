# Source and scope gate

Problem: 30003571 / OWR-15582-005, “Relative Kähler–Ricci Flow on Projective-Space Fibrations.” Checked 2026-10-03; primary files recovered and rechecked 2026-10-04.

## Identification and access

The [catalogue URL](https://www.unsolvedmath.com/problems/30003571) was attempted directly. The web reader could not retrieve it; a direct HTTP request returned 403. The previously pinned catalogue record was used only to locate the primary report, never as evidence for a theorem or current status. Its generated literature assessment is not an input to the proof.

The complete [publisher OWR report](https://ems.press/content/serial-article-files/46702?nt=1), DOI [10.4171/OWR/2017/39](https://doi.org/10.4171/OWR/2017/39), was downloaded and the entire Naumann contribution, printed pp. 2440–2443, was read. The report is for the August–September 2017 workshop; it was published in 2018. A catalogue label describing a 2018 workshop is not used.

The update is Naumann's [published article](https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806601940286992386-1806601940286992386-fb415fcde747f9c588db3e8aababba9d.pdf), *Mathematical Research Letters* 28 (2021), 1505–1523, DOI [10.4310/MRL.2021.v28.n5.a10](https://doi.org/10.4310/MRL.2021.v28.n5.a10). Sections 3.1–3.3, including the full proofs of Theorems 3–5, were read. The earlier [arXiv version](https://arxiv.org/abs/1710.10034) was also read before consulting the publication. The PDF has publisher production marks; mathematical equations and printed pagination are readable.

Berman's [arXiv manuscript](https://arxiv.org/abs/1002.3717), Sections 4.1–4.2, was read for the normalized versus non-normalized distinction and its existence theorem. The proof here uses only the existence result explicitly stated in Naumann's published Theorem 5, not Berman's positivity claims in other settings.

## Exact scope reconciliation

1. The catalogue asks for developing the relative flow on \(\mathcal O_E(r)\). This is already done in report equation (2), and published equation (13), Theorem 5.
2. The report's comparison bundle is \(K_{X/S}^{-1}\), not \(K_{X/S}\); loss of that inverse changes the sign of the geometry.
3. The actual unresolved step is preservation of total-space positivity. It appears at the end of the contribution, printed p. 2443, and remains explicitly open in the published article, Section 3.3, printed p. 1521.
4. The claim in PROOF.md addresses that exact normalized flow and gives strictly positive initial data on a compact projective-space bundle. It does not relabel fiberwise positivity as total-space positivity.
5. The probability-normalized Monge–Ampère numerator is used, matching the published article. Omitting the fixed total-volume normalization adds only a constant function of time to the weight, and does not affect the counterexample.
6. The evolution of the crucial base second derivative is derived directly from the scalar equation. Published equation (14) displays an \(r c\) term, whereas differentiating the defining equation (13) for an \(\mathcal O_E(r)\)-weight gives coefficient one for the undifferentiated base second derivative. The present proof does not rely on equation (14) or silently change the flow to match it: equations (3)–(4) and (8)–(10) in PROOF.md expose every normalization and derivative. Its target is the explicitly defined equation (13). This distinction is a specific review point.

## Later-work and prior-attempt checks

Targeted searches for Naumann, the relative Kähler–Ricci flow, positivity preservation, and counterexamples located the 2021 publication and later discussions of the same obstruction. No primary source resolving this exact preservation question was identified. This is a bounded literature check, not a claim that no such result exists or a historical-priority certification.

Read-only checks of AlecKriebel/Math searched pull requests for the numerical identifier, OWR identifier, Naumann, and title keywords, including all states. No target attempt or PR was returned. The queue row was separately fetched and was `queued`, `0/5`, with no findings or linked chat. These two checks are distinguished: the queue alone was not used to infer absence of a prior attempt. They were repeated after recovery on 2026-10-04.

## Inputs and public-content boundary

The public package contains only the authored proof, source audit, attempt log, and algebraic verification. Downloaded papers, full extracted paper text, cached catalogues, account data, and coordination material are excluded. Source URLs are provided so the mathematics can be checked independently. The exact public-file hashes are recorded in FROZEN_MANIFEST.json.

## Dependencies and remaining gates

The only substantial analytic theorem imported is smooth finite-time existence of the normalized fiberwise flow for initially fiberwise positive data, with the compact smooth base treated as parameters, as stated in Naumann's Theorem 5. Its source proof and preceding existence discussion have been inspected. Global positivity of the initial metric, symmetry, stationarity of the central fiber, the closed second-variation equation, its exact solution, and strict negativity are proved in this package. Symbolic checks confirm the algebra, not the imported existence theorem. Independent mathematical review of the frozen candidate is required before external publication; no external write is part of this source gate.
