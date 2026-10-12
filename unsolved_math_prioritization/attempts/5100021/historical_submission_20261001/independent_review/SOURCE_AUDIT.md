# Independent source audit:5100021 / k403,b

Checked2026-10-01 against the three complete pinned PDFs and both rendered Table5 pages.

- arXiv2004.12497v11, Section3.3 defines the feet on **original orbit chord lines**; Section3.5 defines the antipedal construction from perpendicular lines through the original vertices. Table5, printedp.7, identifies k403,b as the pedal/antipedal signed-area product, N divisible by4, at either original focus. The adjacent k403,a is the origin/odd case and is different.
- The final *Fifty New Invariants*, Arnold Mathematical Journal7(2021), Section3.5 and Table5, printedp.348, agrees on the target, point and parity. Its surrounding definitions use signed shoelace areas and allow self-intersecting antipedals. The introductory billiard model is a strict pair of confocal ellipses. The original-polygon construction is not replaced by the outer tangent or inner contact polygon.
- Stachel, *On the motion of billiards in ellipses*, Theorem4.3 and equation4.9, printedp.1614, gives the normalized canonical coordinates and midpoint contact phase, with modulus equal to the caustic eccentricity and coprime period/turning data. Numerical libraries use its square as parameter.
- DLMF22.4 was checked for the sn/cn/dn periods, their common poles, the dn zero row and both quarter-shift identities used for the focal foot. DLMF22.8 supplies additions; DLMF22.13 gives derivatives. In particular the derivative factors at sn(x)=±1/(k sn(v)) are nonzero for the strict real parameter range, whereas sn(x)=1/k at K+iK' is a second-order contact causing the foot's double pole.

Primary links and PDF hashes are in the author's source_manifest.json and the review's HASH_CHECK.json. No source PDF, full text or rendered page is included in the portable review.

The compact-torus and original-pedal trace methods have earlier campaign uses. The antipedal trace lemma was shared with the parallel k404 author packet; its full proof is present here and was independently audited. I did not contribute to either k403,b or k404. I had previously authored other billiard packets, including k307 and the credited k805 corollary, and had read PR207's related trace method. That common methodological background is disclosed rather than presented as fresh independent discovery. The current original-antipedal vertex algebra, pole cancellation, exact product parity and domain were checked anew.

This audit certifies source match and mathematical scope, not historical novelty or external acceptance. No theorem about hyperbolic/degenerate caustics or parity manufactured by repeating an excluded orbit is imported.
