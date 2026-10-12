# Source and prior-work audit

## Exact target

The first attempted lookup was the assigned [UnsolvedMath record](https://www.unsolvedmath.com/problems/2306022); it was not retrievable. The complete pinned record and its complete imported report are preserved here. The pinned corpus revision is `37e53eabe540fb458758e198be61634bd02ee008`.

The actual primary source is [Hayman–Lingham, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed pp.122–123, PDF pp.123–124. Both pages were inspected from the complete PDF; the formulas and the 2018 editorial update agree with the extraction. The exact class is normalized univalent functions on the open unit disk, starlike of order one half. The request is the sharp uniform convexity radius, not a coefficient bound or a fixed-second-coefficient problem.

The arXiv record as inspected on 30 September 2026 shows v2, revised 21 September 2018. Its editorial no-progress update is preserved as a historical statement, not treated as a reliable current open-status certificate.

## Prior-attempt and duplicate gate

The sparse main checkout is based on `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. Its QUEUE row is rank 172, queued 0/5. The state file is empty, and neither the history nor the related-target-groups file records this ID. Exact-ID branch lookup and all-state PR search for `2306022 OR "6.22"` returned no previous target. No target-named tracked folder or target-named commit was found. The imported OPEN-TRIAGE report says only that it read the statement and searched without finding a resolution; it is not an Alec proof attempt and is retained unchanged.

The corpus's other starlike/convexity search hit, Problem 6.11/2306011, concerns a distinct target. The earlier campaign target 2306064 is Hayman Problem 6.64: coefficient sufficient conditions for alpha-convexity. Its full source statement was read and is not equivalent to this radius problem. No result from that attempt is reused.

## Primary known-result evidence

- MacGregor, Proceedings of the AMS 14 (1963),71–76, [DOI10.1090/S0002-9939-1963-0150282-6](https://doi.org/10.1090/S0002-9939-1963-0150282-6). The [journal issue record](https://www.jstor.org/stable/i335921) confirms title, author, volume, pages and year. Attempts to retrieve the AMS full PDF returned 403; a JSTOR full PDF was also not recovered. The 1963 paper is therefore credited through corroborated bibliographic evidence and explicit attribution in the current primary paper below, not falsely described as fully audited.
- Singh–Goel, Journal of the Mathematical Society of Japan 23 (1971),323–339, [publisher record/DOI](https://doi.org/10.2969/jmsj/02320323), [complete published PDF](https://www.jstage.jst.go.jp/article/jmath1948/23/2/23_2_323/_pdf). The normalized starlike-order definition appears in(1.1); Lemma 2,p. 325 proves the needed derivative disk inequality directly by Schwarz–Pick. Theorem 4.2,p. 330 and the sharpness paragraph on p. 331 cover the exact half-order case. The threshold polynomial in beta is negative at 0 and positive at 1/2, so its smallest positive root is below 1/2 and the theorem's second branch applies. That branch simplifies to the radius claimed here. Equation(4.9) yields `r^4+6r^2−3=0`, and extremal(4.6) specializes to the explicit function in our artifact. These formulas were visually checked against the scan. The proof specialization is independently supplied, avoiding reliance on all of the paper's general-beta optimization.
- Bhowmik–Biswas, [arXiv:2606.20872v1](https://arxiv.org/abs/2606.20872v1), submitted 18 June2026. Its page3 explicitly recalls the same exact radius and cites MacGregor, Theorem 1, reference [11]. Current metadata lists a submitted preprint, one version and no journal reference. Its convolution problem is different, and its new results are not used.

Bounded searches for corrections or an exact Hayman6.22 update did not locate an official erratum. None is claimed. The package corrects our imported classification using a fully available classical primary theorem and a direct proof; it does not purport to edit the source publication or establish historical priority.

## Audit boundaries and reproducibility

The sole validation family is the classical Schwarz–Pick reduction with an explicit sharp extremal. Its derivation began during source triage before the exact historical title was found; no new discovery is credited. All 467 exact diagnostics pass. These finite checks do not establish the all-function theorem on their own; the mathematical artifact provides that argument.

The full PDF files, extracted text, and page renders are retained in the local source cache rather than uploaded into the repository. `source_manifest.json` records public links and SHA256 values. The package uses the actual selected model gpt-6-astra at xhigh reasoning. No claim of ultra reasoning is made. No queue generator, shared status file, external contact or release was used.
