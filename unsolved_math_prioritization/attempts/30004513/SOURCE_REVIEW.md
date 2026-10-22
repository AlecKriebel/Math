# Source review and attribution

Problem 30004513 / OWR-1703876-006 has three distinct questions. The accepted
scope is the sharp constrained-star theorem and its complete-graph upper-bound
consequence. The full original bundle remains partial.

## Original questions and known mechanisms

Pavel Paták, “Helly numbers of disconnected sets,” in Oberwolfach Report
30/2020, printed pages 1500–1501 (PDF pages 32–33), asks whether bk+1 points
suffice for constrained stars, asks for better complete-graph bounds, and
separately asks about extending the method to nontrivial higher homology or
homotopy. [Original contribution](https://ems.press/content/serial-article-files/46867).

Paták’s A sharper Ramsey theorem for constrained drawings,
arXiv:1909.08489v4, November 2024, supplies the definitions and original
b-iatlon and join framework. Definitions 1, 3 and 4, Proposition 1(5)–(6),
Lemmas 1–2 and Conjecture 1 were checked historically against a full text
extraction. The arXiv landing page still listed v4 when checked on October 10,
2026. The typeset 2025 journal version was not inspected.
[Version 4](https://arxiv.org/abs/1909.08489v4).

Credit remains with Paták for the known sharp b=1,2 cases, the b-iatlon lower
example and the join mechanism. The cases k=0,1 are elementary.

## Later exact proof claim and audit

Alper Ferudun, A Proof of Paták’s kb+1 Conjecture for Constrained Stars, with
Improved Bounds for Complete Graphs, version 1.0, was dated and published
online September 30, 2026. It labels itself an unrefereed, AI-assisted preprint.
The general star theorem and monotone-system coloring proof are credited to
that source. [Public landing page](https://eulersolve.org/papers/owr-1703876-006/).

The historical audit extracted the full PDF text, read Sections 2–3 line by
line and checked Lemma 4.1, Corollary 4.2 and Proposition 4.3. PDF pages 3–7
were rendered and visually inspected. Remaining material was read for scope,
not accepted wholesale. The source archive scripts were not read or executed,
and the author’s verification report was not read before the independent
checker was written. Neither is used as correctness evidence.

[AUDIT.md](AUDIT.md) provides the full authored proof reconstruction, including
the link-system induction, exact label exclusions, closure realization,
finite compact-slab sharpness and all cross-edge label conditions in the
join argument. The general clique upper bound is credited to Ferudun using
Paták’s mechanism. There is no proof novelty or priority claim.

The PDF was retrieved directly from the public landing-page link. Its identity
is 159,570 bytes, SHA-256
b2db3bc623aec9e6efdc4986489270ca0343bec3288c658745a5d06267c68001.
[Retrieved PDF URL](https://eulersolve.org/papers/owr-1703876-006/paper.pdf?v=b2db3bc623ae).

The source lists DOI 10.5281/zenodo.23062843. DOI and Zenodo API retrieval
returned HTTP 403, so DOI registration and content were not independently
verified. [Source-listed DOI](https://doi.org/10.5281/zenodo.23062843).

## Scope and review limits

No answer is established here for nontrivial higher homology or homotopy,
which the later manuscript itself excludes. Exact complete-graph thresholds
for general n,b remain undetermined. Its SAT-derived values, Radon/Helly
corollaries and other unaudited topological dependencies are excluded from
acceptance. The arbitrary-b-iatlon Ramsey lower bound is not silently promoted
to a planar-closure lower bound.

The reconstruction and audit are AI-assisted and unrefereed. Acceptance is a
mathematical audit verdict, not external human peer review, journal acceptance
or proof-assistant certification. Bounded literature discovery does not
establish exhaustive status or novelty. No author was contacted.

[SOURCE_METADATA.json](SOURCE_METADATA.json) records historical public source
titles and URLs, PDF hashes and sizes, unsuccessful retrievals and precise
inspection coverage. Edition preparation verified frozen input bytes and
publication integrity only. It performed no new source retrieval, source-text
inspection, literature search or rerun of historical mathematical computations.
The complete proof does not require omitted code or data. Programs, raw
outputs, generated certificates, datasets, copied source documents/text/images
and private coordination material are excluded.
