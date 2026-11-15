# Source, literature, and attribution record

Checked 2026-10-04 UTC. This file records evidence and its limits, rather than certifying historical priority.

## Target reconstruction

- Catalogue URL: https://www.unsolvedmath.com/problems/30006605 . The first web-tool open failed; a direct read returned HTTP 403. No bypass of the site's restriction was attempted.
- The exact pinned upstream record was inspected from the previously materialized `problems.json` corpus. Numeric ID 30006605; code OWR-14299911-007; title “Weighted Centers on Bounded-Dimensional Median Graphs”; source DOI https://doi.org/10.4171/OWR/2026/8 . The supplied `research_results.json` corpus has no entry matching this code or numeric ID and contains no OWR keys. No earlier AI proof report was available there.
- The official MFO copy of *Median Geometry and Applications*, Report 8/2026, was downloaded for private scholarly verification: https://publications.mfo.de/handle/mfo/4442 . Its PDF is https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1 . The relevant contribution is Guillaume Ducoffe, “Radius functions in median graphs,” pp. 504–507. Page 504 defines multiplicative vertex profiles, p. 505 states Open problem 1, and p. 506 discusses the cube-free result and a distinct locality question.
- The definition allows possibly infinite graphs with finite-support profiles; the finite-input algorithmic question and surrounding complexity discussion use n-vertex graphs. Our theorem explicitly uses that finite algorithmic interpretation. It does not address an unspecified infinite-graph encoding.
- No title correction is needed. The catalogue's background citation “Chepoi et al.” for arXiv:2105.12150 is inaccurate: that work is by Pierre Bergé and Michel Habib. This is not the additive oracle used in the proof.

## Decisive algorithmic sources

1. **[BDH], SODA 2025.** Bergé, Ducoffe, Habib, *Quasilinear-time eccentricities computation, and more, on median graphs*, DOI https://doi.org/10.1137/1.9781611978322.52, pp. 1679–1704. The official SIAM metadata verifies the title, authors, proceedings, date (7 January 2025), and DOI. The direct publisher PDF request returned an HTML response, so the mathematical input/output and proof were inspected in the public full version https://arxiv.org/abs/2410.10235v1 (the only version listed when checked). Its p. 2 defines nonnegative integer additive vertex weights, p. 3 states Theorem 1, and §§3–4 give the algorithm and proof, with final runtime on pp. 22–24. The theorem covers all finite median graphs. Its p. 4 distinguishes multiplicative weighted centers as a future direction, so it is not being mislabeled as an explicitly stated solution to the target.
2. **[D26], ESA 2026.** Ducoffe, *Beyond Trees: The Weighted Center Problem on Gromov Hyperbolic Graphs*, DOI https://doi.org/10.4230/LIPIcs.ESA.2026.133, published 25 August 2026. Its Lemma 2 on pp. 133:6–133:7 supplies the logarithmic decision-to-optimization reduction for arbitrary nonnegative profiles. The full version https://arxiv.org/abs/2607.04287v1 has the corresponding Lemma 2.2. Both versions were inspected. This post-workshop source materially strengthens the available toolkit. The generic weighted-median search is credited to it, even though the packet includes a self-contained, slightly slower, division-free variant.
3. **Cube-free prior work.** Chalopin, Chepoi, Dragan, Ducoffe, Vaxès, *On G^p-unimodality of radius functions in graphs: structure and algorithms*, https://arxiv.org/abs/2503.15011 . Its Theorem E / Theorem 7.8 gives an O(n log² n) algorithm on cube-free median graphs. This is credited background and not the scope of the new conclusion here.

## Literature search limits

Queries included combinations of “Weighted Center,” “median graphs,” “additive,” “multiplicative,” “decision,” “binary search,” “2026,” “ball intersection,” and “log5.” The exact OWR statement, BDH full text, and later ESA full text were checked. No source explicitly stating this all-median O(n log^5 n) consequence was located. That absence does not establish novelty. The substantive addition in this packet is a simple reduction of a multiplicative threshold to small-integer additive eccentricities, followed by the known optimization mechanism.

A search also surfaced an unrefereed September 2026 candidate about long strict-improvement distances in median graphs, https://www.evidencepress.org/releases/median-radius-obstructions/ . Its subject is OWR Open problem 2, not the present algorithmic question; no theorem from it is used or certified here. Slow local improvement cannot by itself be a lower bound for this global algorithm.

## Repository and related-target checks

The live queue was read and the target was queued at 0/5, with blank Findings. The live state file had no target entry. The main attempts directory had no `30006605` directory. Target-ID, exact-code, title, and “median” pull-request searches found no relevant existing attempt; a branch search for the target ID was empty. Main was observed at commit `25aaa7146e257ef5276e80aae60429cf3f4765f9`. Search indexes are not exhaustive evidence of absence. The related-target file contained no target match.

The pinned corpus has a distinct related record 30006606, concerning radius-function locality/unimodality. This packet does not settle or change that record. No remote mutation has been made by the author task. Any future repository update must be separately gated and limited to the target's artifacts and authorized queue cells.

## Source-file fingerprints

These fingerprints identify privately inspected source PDFs; the PDFs and full text are deliberately excluded from the public packet.

- OWR report: SHA-256 `92d33ad86e2ba37d8df828c147e73b40e32206e7090cc6d74c34e5eba47f7c51`
- BDH arXiv v1: SHA-256 `af1a4ea9e338c466892289c99bda9048458e41a490b1bbc915da273b31f60c38`
- Ducoffe arXiv v1: SHA-256 `749d53f69587692b007c0ddb3191633d32a35ce31ae937f6408aa7a8582d4727`
- Ducoffe ESA published PDF: SHA-256 `d51056c90b9d5bfb41b2554ee5e33f994fb33149d6b56b2d56f694a6528c5816`
