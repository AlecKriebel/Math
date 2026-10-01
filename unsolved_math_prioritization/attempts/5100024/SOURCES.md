# Exact sources, scope, and prior-work gate

## Primary definitions and table

1. Reznik, Garcia, Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, header **29 October 2020**, https://arxiv.org/pdf/2004.12497v11. Table 5 printed p. 7 labels this target **k406,a**, outer antipedal with M=O, even N, vertex and signed-area centroids both O. Section 2 defines signed shoelace area and signed-area centroid. Section 3.5 defines the antipedal via the perpendicular line through each polygon vertex, allows self-intersections, and uses primes for the outer polygon. Full PDF and rendered Table 5 were read.
2. Same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341–355, https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf. Table 5 printed p. 348 retains **k406,a** and the same target. Both editions were visually checked rather than inferred from the code. The table's question mark does not establish novelty.
3. Hellmuth Stachel, *On the Motion of Billiards in Ellipses*, European Journal of Mathematics 8 (2022), 1602–1622, https://doi.org/10.1007/s40879-021-00524-2. Theorem 4.3 and equation (4.9), printed p. 1614, give the Jacobi parametrization used in Section 2. The complete primary PDF/text were read. The proof uses its nondegenerate confocal elliptical-caustic case and primitive rotation number, with both convex and star orbits.

The classical identities sn(u+2K)=−sn(u), cn(u+2K)=−cn(u), and d(am u)/du=dn u are standard Jacobi real-period identities; DLMF Chapters 22.4 and 22.13 provide primary reference tables: https://dlmf.nist.gov/22.4 and https://dlmf.nist.gov/22.13.

## Restored target and exclusions

The pinned record is ID 5100024 / AMR-050-0024. It specifies the **outer tangent polygon's** antipedal and **both** centroids at **M=O**. It does not ask for a focus or the original orbit's antipedal. The source area is signed even for self-intersections. Its centroid formula has a denominator, so its domain must be stated. `PROOF.md` proves the identity throughout that domain and proves that the excluded zero-area cases are real, not merely hypothetical.

Primitive means least period N. A doubled list of an odd orbit is not an even primitive orbit. Hyperbolic caustics, collapsed caustics, and two-bounce orbits are not included in the restored ellipse-pair scope. Noncircular ellipses are the target; the circle is used only as a limiting comparison in the domain argument.

## Prior work / campaign gate, checked 2026-10-01

- Complete pinned record and prior report read. Their desk-search statement that no general proof had been found is a research lead, not proof of novelty.
- Exact-ID all-state PR search, branch search, k406 PR search, and default-branch attempt-path history found no prior attempt of 5100024.
- The related-target registry groups this with central-inversion identities. That is a shared elementary mechanism, not a duplicate target.
- Existing https://github.com/AlecKriebel/Math/pull/140 (5100023 / k405) concerns the **original orbit** antipedal **vertex** centroid at center or foci. Its proof was read and credited for the common central-symmetry principle. No focal formula from it is used here.
- Current targeted source/literature searches found no specific later proof to import as this target. We make no historical-priority or novelty claim. The affirmative result is explicitly credited as a classical-symmetry consequence.

Full source copies, extracted text, rendered pages, upstream record, and desk report remain local reading aids outside the publishable attempt directory. `source_manifest.json` records hashes and the pinned data provenance without copying their text.
