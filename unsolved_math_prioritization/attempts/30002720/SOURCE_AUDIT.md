# Source and scope audit

Checked 2026-09-30. Numeric ID 30002720; OWR-13352-004. Model: gpt-6-astra, xhigh. Historical priority has not been established.

## Exact original request

The complete primary contribution is Kevin Leckey, *Radix Sort on Markov Sources*, OWR 50/2014, printed pp. 2854–2856. Its final paragraph, p. 2856, asks about marginal convergence for the centered, square-root-scaled radix-selection process. The input strings are independent copies of a binary Markov chain; the first part of the contribution concerns sorting and is not the selection problem. [Full original](https://ems.press/content/serial-article-files/46539), [DOI](https://doi.org/10.4171/owr/2014/50).

The cited 2014 paper, *Analysis of radix selection on Markov sources*, Section 3.1, Theorem 3.1, expressly states its first-order quantile asymptotic **away from the cylinder-boundary set**. It discusses boundary ranks separately. Thus merely repeating a known boundary obstruction could miss the intended quantile question. [Primary preprint](https://arxiv.org/abs/1404.3672).

## Later result and a textual tension

Leckey–Neininger–Sulzbach's later full process paper defines the exact cost by prefix counts with singleton truncation, and Section 2.4 uses deterministic centering by n times the first-order profile. Proposition 2.9 proves fixed-marginal non-tightness at a dense set of boundary ranks. The paragraph immediately after Corollary 2.11 nevertheless calls one- or finite-dimensional marginal convergence open. Both pages were visually inspected in the full PDF; these are not distinct symbols confused by text extraction.

This package does not label the already known boundary result a new discovery, or claim the authors intended a particular unprinted restriction. Its separate construction uses a single nonboundary continuity rank and rules out **every deterministic centering**. Therefore it also addresses a natural interpretation that excludes the known bad boundary points. It does not settle convergence for almost every rank or classify all ranks. The published random-centering process result is not contradicted.

[arXiv:1605.02352v2](https://arxiv.org/abs/1605.02352v2), [author-hosted manuscript](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf), [published article DOI](https://doi.org/10.1016/j.spa.2018.03.009).

## Access, dates, and search limits

The complete arXiv PDF and the author's complete linked manuscript were obtained. The former carries the arXiv v2 date 2 October 2017 and an internal 15 October 2018 date; the latter is dated 2 October 2017. The author's [publication list](https://www.math.uni-frankfurt.de/~neiningr/publist.html) identifies the final article as *Stochastic Processes and their Applications* 129 (2019), 507–538 and links that manuscript. The final publisher-typeset PDF was not recovered. No claim of a full final-typeset comparison is made.

Targeted current searches included the paper title with “marginals”, “continuity”, “fixed rank”, and “non-tightness”, and the author publication list. No later primary result settling the nonboundary construction was located. Search failure is not evidence of novelty, nor a comprehensive classification of the literature. The familiar cylinder-jump mechanism is explicitly credited; the proof uses a sparse fixed rank approaching these jumps on selected sample-size scales.

## Repository and duplicate gate

The immutable imported record was read in full; its research-report entry is null. Its August 2026 literature triage records the later open-marginal sentence but omits the stronger fixed-rank content of Proposition 2.9. The current queue row was queued with 0/5 attempts. No earlier attempt-path history, remote problem branch, related-target index entry, or matching all-state PR was found at the gate. An all-state PR snapshot covered 156 PRs, including their bodies. A pinned-record search found no second radix-selection target. The same-report Waring-polynomial record 30002719 concerns another contribution and is distinct.

Read-only source caches and gate snapshots are retained outside the public attempt folder. SHA-256 hashes and stable URLs are in `source_manifest.json`; third-party PDFs are not included in this research PR. Parent coordination owns queue changes.
