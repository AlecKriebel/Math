# Public-source identity and scope ledger

Research and independent-audit inspections dated 10 October 2026 UTC. This authored ledger contains bibliographic metadata and inspection history; edition preparation does not claim a new source retrieval, PDF rehash, visual inspection, or literature search. Source copies and extracted text are not included in the authored proof package. Public availability is not a redistribution licence.

## Original target

- Andreas Neuenkirch, *A conjecture on the optimal approximation of the fractional Lévy area*, in *Rough Paths and PDEs*, Oberwolfach Report 41/2012, pp. 2524–2525. DOI: https://doi.org/10.4171/owr/2012/41
- Publisher landing page: https://ems.press/journals/owr/articles/12013
- Public PDF: https://ems.press/content/serial-article-files/46412?nt=1
- Previously retrieved 2026-10-10T01:04:15.718196+00:00, HTTP 200. Rehashed before use: 448314 bytes, SHA-256 `302476077b9e76aab36045af07d2d262611914ec1ae2484367ad6d10af29dcb1`.
- PDF pages 32–33 (printed 2524–2525) visually rechecked for this attempt. Exact target: canonical iterated integral of two independent standard fBm components, observations of both components at all positive uniform grid times, and an all-sample-count RMS lower rate. This is the source formulation, not an antisymmetric-area substitution.

## Prior convergence used in the proof

- Andreas Neuenkirch, Samy Tindel and Jérémie Unterberger, *Discretizing the fractional Lévy area*, Stochastic Processes and their Applications 120 (2010), 223–254.
- Correct journal DOI: https://doi.org/10.1016/j.spa.2009.10.007
- Publisher page: https://www.sciencedirect.com/science/article/pii/S0304414909001823
- Author preprint record: https://arxiv.org/abs/0902.0497
- Inspected PDF: https://arxiv.org/pdf/0902.0497
- Retrieved 2026-10-10T01:48:43.188349+00:00, HTTP 200; 424962 bytes; SHA-256 `de4d91bff1cde45c02298d9f7f49f34790b6c4043232eb6ef5da999af3128ebf`.
- PDF page 3 visually inspected. Theorem 1.1 gives (L^2) convergence of the specified left-point cross-component sums for the rough range and each smooth regime. The following calculation supplies Brownian convergence. The proof uses this convergence to pass a finite Gaussian moment identity to the canonical area.
- The downloaded PDF is labeled arXiv:0902.0497v1; its front-page typesetting date reads March 22, 2022. These are recorded as observed; no claim that the retrieved bytes equal journal bytes is made. The preprint and publisher text differ in their trapezoid theorem presentation, so the proof does not interchange theorem numbering between them.
- The imported DOI ending `2010.06.002` is not the DOI of this paper and is not relied on.

## Credited smooth-range prior

- Andreas Neuenkirch and Taras Shalaiko, *The maximum rate of convergence for the approximation of the fractional Lévy area at a single point*, Journal of Complexity 33 (2016), 107–117.
- Journal DOI: https://doi.org/10.1016/j.jco.2015.09.008
- Author-uploaded text: https://www.researchgate.net/publication/280310281_The_maximum_rate_of_convergence_for_the_approximation_of_the_fractional_Levy_area_at_a_single_point
- The author-uploaded full text was read online on 10 October 2026: Theorem 1 assumes (H>1/2) and gives positive lower liminf and finite upper limsup at the claimed rate. Theorem 2 and its following discussion explain why their increment lower bound fails for (H<1/2). Its Brownian remark gives the known exact optimum.
- No local PDF retrieval, PDF byte hash, or visual-PDF inspection is claimed for this source. The new witness proof does not use the failed increment lower bound.

## Bounded current-literature check

Public searches on 10 October 2026 used the exact title, fractional Lévy-area lower-bound and optimal-conditional-expectation phrases, rough-range variants, and Cameron–Martin/localization method terms. The directly relevant primary findings were the original report and the two papers above. Search hits about general fBm SDE numerical schemes, Brownian-only area simulation, or generalized space-time Lévy areas were not treated as solving this exact target. No verified later full rough-range optimal conditional-expectation lower theorem was found in that bounded pass. This is not a global novelty or priority certificate.

## Independent audit and acceptance source checks

The independent audit read the original report in extracted text and visually inspected PDF pages 32–33, printed pages 2524–2525. It independently visually inspected the NTU arXiv PDF pages 3–4, including equations (4)–(5), Theorem 1.1, the Brownian calculation and analytic-approximation convention; pages 1–4 and the convention statement at the beginning of page 5 were also read in extracted text. Its retained public-PDF byte identities agree with those recorded above. A subsequent acceptance review visually checked the original report's printed pages 2524–2525 and NTU page 3. These are recorded inspection histories, not new inspections during edition preparation.

The audit checked the author-uploaded Neuenkirch–Shalaiko text for its H>1/2 scope and its explanation of the failed rough-range increment bound. Its attempted DOI opening failed. The audit retained the earlier publisher-metadata confirmation, without claiming a newly downloaded or visually inspected journal PDF. The arXiv record lists NTU version 1 submitted 3 February 2009; the different printed PDF date above is not treated as a new submission version.

The Gaussian representation, joint Gaussian independence, Fourier inversion, Tonelli, finite-polynomial Parseval, positive-semidefinite trace inequality, Cauchy–Schwarz, and conditional-expectation projection property are standard inputs whose needed forms are supplied in the proof and audit. The established NTU convergence theorem is imported, not re-proved. The companion convention note independently identifies its area limit with the canonical polygonal iterated integral.
