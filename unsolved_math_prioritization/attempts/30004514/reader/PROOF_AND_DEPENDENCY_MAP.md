# Proof and dependency map

## The logically sufficient route

Read [MTY_DIMENSION5_VERIFICATION.md](mty/MTY_DIMENSION5_VERIFICATION.md). Its dimension-five construction alone falsifies the universal n ≥ 3 lower-bound question. [MTY_GEOMETRY_AUDIT.md](geometry/MTY_GEOMETRY_AUDIT.md) independently checks the corresponding geometry, measures, parameter choices, and count. No WXY lemma is used on this route.

| Obligation | Dimension-five reconstruction | Independent geometry audit |
|---|---|---|
| Ordinary volume centroid and induced section measure | §1; exact formulas (21)–(23) | §1 |
| Radon self-adjointness and smooth even inverse | §§2.1–2.2, (2)–(5) | §3; Fourier/Radon normalization |
| Exact seed and companion transforms | §2.3, (6); (11), (15) | §§3–4 |
| Positive radius and global convexity | §3, (7)–(10); uniform perturbation §6 | §§2, 6 |
| Strict opposite endpoint moment signs | §4, (12)–(17) | §4, (B)–(C) |
| Smooth division across the equator | §5, (18)–(19) | §5 |
| Nonzero section moment in every other direction | §7, exact identity (21) | §6 |
| Full zero centroid of the exceptional section | §7: origin-centered four-ball | §6: origin-centered (n−1)-ball |
| Exact body centroid without recentering | §8, (22)–(25) | §7 |
| Exactly one unoriented affine hyperplane | §§1, 7–8 | §8 |
| Author-v2 equation (5) and equatorial repair | §9 | §§3–4 |

The special section is a ball centered at zero, so its full centroid vector vanishes. Merely checking its fifth coordinate would be insufficient. Two opposite unit normals designate one hyperplane. Every noncentral affine hyperplane is excluded because the centroid of a section must lie in its affine hyperplane.

The positive perturbation size and intermediate-value centering parameter are existential. The argument chooses them inside a uniform convexity range and uses exact endpoint signs plus continuity. No numerical root or finite list of directions supplies the conclusion.

## Background for the sufficient route

The reconstruction proves the needed Radon self-adjointness, inverse eigenvalues and polynomial inverse bound, ellipsoid section identity, seed curvature estimate, global gauge convexity, smooth quotient, exact moments, and parameter selection. It uses standard Euclidean polar integration, Fubini/coarea, spherical harmonic decomposition and derivative bounds, smooth calculus, compactness, and the intermediate value theorem. It does not depend on a classification of intersection bodies or a numerical approximation theorem.

The Fourier discussion in reconstruction §9 identifies the correct replacement for the inspected statement and translates normalizations. The dimension-five proof itself is already established through the Radon route. Yaskin's precursor is credited and inspected for the historical seed and constants, while the necessary seed calculation is re-proved in the reconstruction.

## The supplementary route

Read [WXY_RECONSTRUCTION_AUDIT.md](wxy/WXY_RECONSTRUCTION_AUDIT.md) and [WXY_SUPPLEMENTARY_GEOMETRY_AUDIT.md](geometry/WXY_SUPPLEMENTARY_GEOMETRY_AUDIT.md). These concern the July 2026 submitted preprint, not the published basis of the universal disposition.

| Supplementary obligation | WXY reconstruction | Independent geometry audit |
|---|---|---|
| Derivative of hemisphere volume equals full section moment | §1 | §4 |
| Globally smooth phase with exact weighted cancellation | §2 | §1 |
| Twisted height has exactly two extrema and no first harmonic | §3, including n = 3 and n = 4 | §1 |
| Hemisphere eigenvalue normalization and smooth inverse | §4 | §2 |
| Forward transform bound in the same differentiability order | §5 | §2 |
| Exact body centroid and global strict convexity | §6 | §3 |
| No additional critical points after perturbation | §7 | §5 |
| Antipodal pair equals one geometric hyperplane | §§1, 7 | §5 |
| Inspected pages, diagnostic limits, standard prerequisites | §§8–9 | Conclusion and supplementary disposition |

The WXY route uses standard spherical harmonic decomposition, Funk–Hecke, Sobolev characterization/embedding on the compact sphere, and elementary differential calculus. It reconstructs the pivotal hemisphere eigenvalue formula rather than depending on inspection of Rubin's entire original proof. It does not assert a bounded inverse from C² to C²: the inverse is applied to one fixed smooth function; the perturbation uses the forward operator bound. Exact stability of the two critical points is established with local definite Hessians and a compact-complement gradient bound.

## Evidence linkage

[geometry/CROSS_REVIEW_RECEIPT.json](geometry/CROSS_REVIEW_RECEIPT.json) pins the exact accepted bytes of both full reconstruction files. [integrity/ORIGINAL_ARTIFACT_MAP.json](integrity/ORIGINAL_ARTIFACT_MAP.json) verifies those pins against the original public-artifact manifests and maps them to this layout. Source-only status checks and mathematical proof checks are recorded separately so that a metadata match cannot be mistaken for a proof.
