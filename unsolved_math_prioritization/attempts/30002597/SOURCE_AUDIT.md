# Source and scope audit

Historical source-only audit, frozen at commit `aeb7bb3b659db44664de13ece41a8b9d639a6cc6`.
Subsequent substantive attempt 1 is [CORANK_CANDIDATE.md](CORANK_CANDIDATE.md);
its full decision criterion was not covered by this source-only review.

Checked 2026-10-01. Numeric record: **30002597**, code **OWR-12984-009**.

## 1. What is actually at issue?

Let `E(S, gamma)` mean that a prescribed generic immersion
`gamma: S^1 -> S` of a circle in a closed oriented surface extends to a map
`f: D^2 -> M`, where `M` is a compact 3-manifold with `boundary M = S`,
`f|boundary D = gamma`, `f^-1(boundary M) = boundary D`, and the map has the
usual stable surface-to-3-manifold singularities.

These are different targets:

1. **Universal existence:** `E(S, gamma)` holds for every such pair. This is
   false by an old counterexample, audited below.
2. **A particular input:** decide `E(S, gamma)` for a specified pair. No particular
   curve is supplied by the imported question.
3. **Unrestricted classification/decision:** characterize all pairs satisfying
   `E`, or supply a complete decision procedure. This package does not do this.

The negation of (1) settles neither every instance in (2) nor (3). The corrected
record should make this distinction rather than promote an old obstruction as a
new complete classification.

## 2. Original OWR context

Manturov's contribution, *New Parities and Cobordisms in Low-Dimensional
Topology*, occupies pp. **1443–1446** of Report 26/2014. The question is at the
bottom of p. **1445**, immediately followed by acknowledgment of existing
homological obstructions. The next page's Theorem 5 is about framed four-graphs
without a prescribed ambient surface or 3-manifold. It is not a theorem giving
a general answer for the preceding surface-curve problem. The original printed
line also contains the typographical expressions “2-curve” and `g` at the end
of its boundary equation. These should not supply extra hypotheses.
[Primary report, PDF p. 43](https://math.rice.edu/~shelly/publications/Oberwolfach_2014.pdf#page=43)

The earlier checkpoint's “printed1445–1446” describes the relevant passage,
not the full contribution's page range. The surface is explicitly oriented;
orientation of `M` is not explicitly stated in that paragraph. Compactness and
the word “closed” are explicit in the imported normalization, not in that
printed sentence. A closed genus-two example nevertheless lies in the imported
scope. The notation identifying `boundary D` with the curve is interpreted as
the boundary **map**, not just an equality of image sets.

## 3. Earlier published obstruction and credit

Carter, *Closed curves that never extend to proper maps of disks*,
Proc. Amer. Math. Soc. **113** (1991), 879–888,
[DOI](https://doi.org/10.1090/S0002-9939-1991-1070511-1):

- Theorem 1.1, p. 880, gives a three-double-point curve on a genus-two surface
  with no proper singular-disk extension in any bounding 3-manifold
- Example 5.1, p. 885, identifies the signed Gauss word
  `a b c b^-1 a^-1 c^-1`
- The introduction works in PL general position. Sections 2–4 include branch
  points, not only immersions; Theorem 4.2 explicitly uses an oriented ambient
  solid

The complete author-uploaded text was read, including Sections 1–6. The AMS
PDF request returned HTTP 403; the author-posted text is available
[here](https://www.researchgate.net/publication/243064762_Closed_Curves_That_Never_Extend_to_Proper_Maps_of_Disks).
The figures were not independently recovered as a Carter facsimile. This
limitation does not supply the mathematical certificate: the independently
encoded example and Turaev's published argument below supply that check.

Turaev, *Virtual strings*, Ann. Inst. Fourier **54** (2004), 2455–2525,
[published PDF](https://www.numdam.org/item/10.5802/aif.2086.pdf), supplies the
obstruction `disk extension => u = 0`: Theorem 5.1.4 and Lemma 5.1.5,
pp. 2475–2478; Section 5.2, p. 2479. The lemma allows a compact genus-zero
oriented source and an oriented 3-manifold, with generic boundary curves.
Remark 5.5(1), p. 2482, explicitly credits Carter and identifies `alpha_(2,1)`.
The complete published PDF was recovered, and its relevant definitions,
proof, and attribution were checked against
[arXiv:math/0311185v5](https://arxiv.org/abs/math/0311185v5).
The shorter arXiv:math/0310218 is not the version used for theorem numbering.

## 4. Singularity and boundary conventions

The ordinary local models are regular sheets, transverse double curves,
isolated transverse triple values, and isolated simple branch points
(Whitney umbrellas/cross-caps). Along the boundary there are regular and
transverse-double half-sheet models. Thus “stable singularities” does not mean
an immersion everywhere and does not mean an embedding.

These models and stability are spelled out in Ben Hadar, *The intersection
graph of an orientable generic surface*, Algebraic & Geometric Topology
**17** (2017), 1675–1700, Definition 1.1 and the following discussion,
pp. 1675–1676.
[Publisher PDF](https://msp.org/agt/2017/17-3/agt-v17-n3-p08-p.pdf#page=1)

For boundary-preserving general position, Funar, *Surface cubications mod
flips*, Manuscripta Math. **125** (2008), 285–307, proof of Lemma 4.1,
pp. 302–303, explicitly uses homotopy relative to the boundary to achieve
simple branch points and normal-crossing double/triple strata. Its subsequent
operation removing branch points may change the source surface, so it must
**not** be used to replace the disk by an arbitrary surface here.
[Author-hosted published paper](https://www-fourier.univ-grenoble-alpes.fr/~funar/2008manuscripta.pdf#page=18)

In fact, the obstruction used here excludes a continuous null-homotopy in an
oriented filling, a broader allowance than stable maps. Therefore it cannot
be evaded by admitting additional disk singularities. The orientation issue
left implicit by OWR is addressed explicitly in APPLICATION_CHECK.md.

## 5. What the literature check does not settle

Chen's 2024 primary preprint, *FlatKnotInfo: the first 1.24 million flat knots*,
distinguishes homotopy classification from sliceness. Section 5 gives examples
that are algebraically slice but not slice, and pp. 19–20 and 37–38 record
unresolved sliceness cases, including 6.540. This prevents treating vanishing
of one obstruction, or a flat-knot classification algorithm, as a complete
sliceness criterion.
[Version 1](https://arxiv.org/html/2410.00216v1#S5)

Searches on 2026-10-01 for unrestricted virtual-string/flat-knot sliceness
criteria and later work on 6.540 did not locate a complete decision theorem.
This is bounded literature triage, not proof that none exists. The live
6.540 table page could not be retrieved. Its 2024 status is not asserted as a
freshly verified 2026 status. The safe conclusion is that unrestricted
classification remains **unresolved by this audit**, while the universal
affirmative interpretation is already false.

## 6. Review questions

The separate reviewer should challenge: the signed-word/arrow conversion;
the genus calculation; application of the disk obstruction rather than only
a fixed-handlebody obstruction; the orientation-double-cover argument;
the distinction between stable maps and immersions; attribution; and the
absence of any general-classification or current-status overclaim.
