# Source, edition and prior-attempt audit: k904,a

NumericID5100063, codeAMR-050-0063, queue rank227. The full pinned dataset record and exact-key imported prior report are retained. The third-party report is historical triage, not a prior campaign attempt or proof.

## Exact source and objects

[Reznik-Garcia-Koiller arXiv2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table10 printedp12, explicitly lists the product A_1'^dagger A_2'^dagger for oddN as k904,a, with '?' in its proof column. The complete table page was rendered and visually inspected. Section3.9 defines unit-circle inversions about original foci and says primed symbols refer to the outer polygon. Section2 defines all polygon areas by signed cross-product sums.

The outer polygon is obtained by intersecting consecutive tangents at the billiard vertices; its own vertices, not the original orbit or caustic contacts, are then inverted. The centers are the ORIGINAL billiard foci. Section3.10 distinguishes inversion about the outer locus's own foci, using a different symbol; that is the separate k906 row. The outer locus is generally nonconfocal and may have its longer axis in the opposite direction, so one cannot import an original-ellipse focal-inversion theorem without checking the centers.

The shorter [published Fifty New Invariants](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) has no900-series table. The imported report's suggestion of an unchanged published k904,a entry is therefore not retained. No differently numbered formula is substituted for the actual arXiv target.

Scope follows the arXiv introduction's confocal ellipse pair: strictly nested nondegenerate elliptical caustic, odd least period, all coprime primitive star turning numbers. Repeating a smaller polygon does not change its least-period class. Areas use straight segments joining inverted vertices, not inversions of complete sides into circular arcs.

## Primary analytic inputs

Stachel, [On the motion of billiards in ellipses](https://doi.org/10.1007/s40879-021-00524-2), European Journal of Mathematics8(2022),1602-1622, Theorem4.3/equation4.9 printedp1614. The same verified published source used in the preceding tasks is retained locally. Its canonical modulus is the caustic eccentricity; numerical-library parameter is k^2. This theorem is credited, not rediscovered.

Standard periods, poles, zeros and half/quarter shifts: [DLMF22.4](https://dlmf.nist.gov/22.4). Addition/double/triple-angle derivations: [DLMF22.8](https://dlmf.nist.gov/22.8). Derivative and zero-order checks: [DLMF22.13](https://dlmf.nist.gov/22.13). The complex continuation is meromorphic and bilinear; no conjugation in the parameter is introduced. Classical complex methods for billiard invariants: [Akopyan-Schwartz-Tabachnikov](https://arxiv.org/abs/2001.02934).

## Related campaign work, explicitly not a substitute target

- [PR200/k115](https://github.com/AlecKriebel/Math/pull/200) supplies the preceding independently reviewed outer-locus calculation. The present proof derives that formula again and needs a different area argument.
- [PR207/arXiv k804,a](https://github.com/AlecKriebel/Math/pull/207) is original-orbit area times one focal-inverse area for0mod4 periods. Its analytic organization is reused with credit; its conclusion does not imply this outer odd-period product.
- [PR206/k903,a](https://github.com/AlecKriebel/Math/pull/206), frozen proof c4c2c5399d46f8aa30c4580160ea15a1375939eab3a2ba390d74abdce9a30905, was read in full. It concerns original-vertex inversions. Its author warned that its common-isotropic-tangent identification relies on using foci of the vertex ellipse. That premise does not hold for the present outer-locus/original-focus combination; the present proof instead derives an explicit inverse-edge formula. Source/framework advice is not independent review.
- k806,a/5100047 is a separate ratio target at rank278. No k806 PR was found during this check. Its asserted ratio is not assumed to transfer k903,a to k904,a.

## Prior-attempt gate and literature limits

Live all-state searches by5100063 andk904 returned no campaign PR; target branch search and default-branch attempt-path commit history were empty before this work. related_target_groups.json contains no matchingID. The queue row was queued0/5. No campaign attempt was found, and no historical counter reset is intended.

Focused searches for k904 and outer inversive area products recovered the source and related work but did not verify an exact general-target prior proof. This bounded search does not certify novelty. No outside person was contacted. Full PDFs and table renderings remain reading copies outside the public attempt package. All executed check code is locally authored and uses preinstalled standard scientific libraries.
