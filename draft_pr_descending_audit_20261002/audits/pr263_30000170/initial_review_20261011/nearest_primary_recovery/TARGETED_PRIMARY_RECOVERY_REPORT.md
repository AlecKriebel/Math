# PR263 targeted nearest-polynomial primary recovery

Audit checkpoint: 2026-10-11 22:21:06 UTC. Completion estimate: 100% of this bounded recovery attempt; 50% of the four requested full bodies recovered. This is not a 100% priority clearance or a certificate of historical firstness.

## Exact comparison target

The accepted target is the following local assertion: for complex monic quadratics in the full real coefficient space C², the closed left-half-plane stable set fails prox-regularity at z²; for every fixed real symmetric positive-definite coefficient metric, arbitrarily close inputs have attained, nonunique global nearest stable polynomials. A full degree-two extension and a whole-epigraph statement are separate parts of the proposed note. Standard function prox-regularity relative to finite subgradients is not refuted by that target.

## Recovered primary bodies

**Moses and Liu (1991), DOI 10.1109/78.80912.** The [public Moses author listing](https://osu.academia.edu/RandolphMoses) links the [actual article OCR](https://www.academia.edu/329556/Determining_the_Closest_Stable_Polynomial_to_An_Unstable_One). I read the complete article text, printed pp. 901–906, including Sections II–IV. Section II explicitly uses real monic coefficient vectors, the closed unit disk, and a positive-definite weighted Euclidean coefficient metric. Section III, p. 902, recognizes possible nonunique solutions because the stability set is nonconvex. Section IV discusses local minima of its alternating Schur-parameter algorithm and also permits a variable leading coefficient. The degree-two relation is a₁=r₁(1+r₂), a₂=r₂, |r₁|,|r₂|≤1. The body does not give the target local complex half-plane theorem, a tie construction accumulating at a repeated root, or a prox-regularity/epigraph assertion. The numerical examples do not fill those gaps. The original PDF and Figure 1 were not visually recovered: this finding rests on public full-body OCR, with that limitation expressly retained. A direct ordinary page fetch returned HTTP 403 and was not bypassed.

**Orban de Xivry (2013), _Nearest Stable System_.** The [primary UCL repository record](https://research.dial.uclouvain.be/entities/publication/650a4c86-3c4c-439e-9a8f-54c4d42eab7f) explicitly marks [the complete thesis PDF](https://research.dial.uclouvain.be/bitstreams/930fe0d3-f488-439c-bce1-37a8dc368917/download) Open Access. I read printed pp. 2, 9, 24–26, 33–38, 55–67, the entire polynomial Chapter 4 pp. 135–181, the conclusion pp. 183–185, and selected bibliography pp. 192–193. The coefficient field includes C, the objective is an ordinary coefficient/Frobenius distance, and marginal stability is admitted through closure. Page 144 explicitly formulates complex monic polynomial stabilization; pp. 175–180 discuss weighted objectives. The singularity survey pp. 55–57 credits earlier real-parameter classifications; the benchmark pp. 63–66 concerns matrix local optima and numerical evidence. Chapter 4 develops algorithms and real polynomial experiments, including repeated boundary roots. None of these read assertions states the comparison target. No whole-epigraph or standard function-prox-regularity result was located. This is a bounded read-extent conclusion, not an exhaustive negative search across all 214 pages. Key pages and figures were independently rendered and inspected; the upstream PDF has a recoverable cross-reference warning.

## Remaining full-body gaps

| Requested work | What was actually obtained | Remaining gap |
| --- | --- | --- |
| Combettes–Trussell (1992), DOI 10.1109/78.175751 | Current and archived primary Combettes publication lists confirm the citation; neither entry supplies a manuscript link. Publisher access was unavailable in this attempt. | Full body, coefficient field, boundary convention, and any uniqueness claim remain unknown. Secondary abstracts are not treated as theorem evidence. |
| Orban–Nesterov–Van Dooren (2013), DOI 10.1016/j.automatica.2013.01.053 | Primary repository record/abstract and author bibliography routes; repository PDF explicitly restricted. Publisher page unavailable. | Journal body remains unread. The recovered thesis is independently useful evidence, but is not asserted byte-identical or theorem-identical to the article. |

The public repository API search recovered the migrated thesis record, superseding the earlier thesis-body gap. No restricted PDF, text companion, login, paid delivery, copy request, or external communication was attempted.

## Adversarial comparison and publication boundary

The following are deductions about scope, not attributed theorems from an unavailable body:

1. Nonconvexity permits global projection ambiguity but does not establish ambiguity in every neighborhood of a particular point. A local prox-normal support inequality is a materially stronger check than that generic observation. Credit Moses–Liu for recognizing the former possibility; do not claim that generic nonuniqueness was discovered here.
2. The real degree-two disk region from the recovered Schur relation is the convex triangle a₂∈[−1,1], |a₁|≤1+a₂. Every positive-definite quadratic metric has a unique nearest point on it. This independently prevents identifying their real degree-two domain with the complex target.
3. Root Möbius transformations alter coefficient coordinates and generally alter the metric after monic normalization. One cannot transfer a nearest-point theorem merely by noting disk/half-plane equivalence of roots. No metric-preserving transfer is established in this audit.
4. Unrestricted matrix nearest points need not be companion matrices. The map to characteristic coefficients can identify distinct matrices, so matrix ties or competing local numerical minima do not supply polynomial ties in the asserted metric.
5. A convergence theorem for an algorithm, stationary points, or distinct local minima does not prove multiple attained global nearest points. Likewise, first-order regularity and finite-subgradient function statements do not imply whole-epigraph prox-regularity.

**Verdict:** These two recovered bodies provide important prior credit and remove two specific body gaps. They contain no located exact match in the stated read extents. A self-contained, carefully credited proof note may accurately present its proved complex counterexample and identify the historical question being answered. This audit alone does **not** authorize claims of firstness, complete priority clearance, or an independently verified assertion that the problem remained open in 2026. The two unrecovered bodies remain explicit limitations for the root's overall priority adjudication.

Private reading copies and renderings are excluded by this folder's `.gitignore`; only original notes and compact provenance should be selected for a research checkpoint. This agent made no provider, Git, manuscript, DOI, or Sheet mutations.
