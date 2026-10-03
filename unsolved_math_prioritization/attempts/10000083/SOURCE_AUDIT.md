# Source and literature audit

Checked 2026-10-03 UTC.

## Catalogue identity

- Exact requested URL: https://www.unsolvedmath.com/problems/10000083
- Exact numeric ID/code/title are verified against the pinned UnsolvedMath
  corpus, revision `37e53eabe540fb458758e198be61634bd02ee008`.
- Full problems corpus SHA256:
  `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- Full prior-report corpus SHA256:
  `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.
- The record says `open`; its imported report is `OPEN-TRIAGE` and records
  only a web/arXiv search with no resolution found. That is neither evidence
  of a proof attempt by this campaign nor an authoritative literature verdict.
- The exact live page returned HTTP 403 in the cloud browser. Its live body
  was not verified. The pinned record is the stated identity/wording source.

## Original mathematical source

Itai Benjamini, *Random Planar Metrics*, section 4.1, **unnumbered cover-time
conjecture following Conjecture 4.1**, PDF page 9. The original
[author-hosted URL](https://www.wisdom.weizmann.ac.il/~itai/randomplanar2.pdf)
now returned 404. The same primary text was recovered at the
[Berkeley-hosted copy](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/benjamini_rpm.pdf).
Page 9 was read in extracted text and in a rendered image. It asks for a
graph-uniform exponential bound at linear time, excluding double edges.
Conjecture 4.1 itself concerns the largest vacant component and is distinct.

The corresponding proceedings contribution is *Proceedings of ICM 2010*,
pp.2177–2187, [DOI 10.1142/9789814324359_0140](https://doi.org/10.1142/9789814324359_0140).
The imported report's parenthetical “Saint-Flour” is not the provenance of
the primary source checked here. No claim about that separate lecture text
is needed. Dubroff–Kahn trace the question to Benjamini in 2009.

## Resolution and same-title trap

1. [Benjamini–Gurel-Gurevich–Morris, arXiv:1011.3118](https://arxiv.org/abs/1011.3118)
   proves the bounded-maximum-degree case, allowing degree dependence in the
   exponent, and states the general simple-graph version as a conjecture.
2. [Dubroff–Kahn, arXiv:2109.01237v2](https://arxiv.org/abs/2109.01237v2)
   is a different paper with essentially the same title. Its Theorem 1.1
   gives the general case. The displayed theorem on p.1, graph/walk usage
   on p.3, and the explicit large-n convention on p.4 were checked. Pages
   1 and 4 were also rendered and visually inspected.
3. Publication in *Annals of Probability* 53(1), January 2025, pp.1–22 is
   corroborated by the [publisher's issue listing](https://www.imstat.org/publications/aop/aop_53_1/aop_53_1.pdf)
   and [Rutgers's publication record](https://www.researchwithrutgers.org/en/publications/linear-cover-time-is-exponentially-unlikely/).
   DOI: `10.1214/24-AOP1699`.

The full arXiv v2 proof was retrieved. The final journal proof was not compared
line by line; DOI/publisher direct retrieval was unsuccessful. A bounded
title/author/correction search located no correction contradicting the
resolution. This is not an exhaustive assertion that no later correction
exists, nor a fresh peer review of the imported theorem.

Only original commentary, metadata, references, and verification code belong
in the publication packet. Primary PDFs, screenshots, extracted source text,
full corpus files, and raw repository snapshots are excluded.
