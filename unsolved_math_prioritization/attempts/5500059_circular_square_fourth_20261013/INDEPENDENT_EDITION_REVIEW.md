# Independent review of the fourth square-circularity edition

Problem row 1757 / 5500059 / AMR-054-0059. Review date: 13 October 2026.

## Verdict

Accepted within its stated partial-result scope. The complete 30-file edition has public manifest SHA-256 `ae501ca8e845bd39c0c8e424ae8a46fe5ad425c5c01a59daba6bdfc69becd16b`, 21,142 bytes. No mathematical correction was required.

The complete-square theorem gives a finite partition into 121 positive-area strictly convex polygons, each with true circumradius/inradius strictly below 1.295516. The original fixed 56-cell boundary patch forces at least 6,826 additional pentagons in any completion below sqrt(2). The redesigned 56-cell patch has 588 genuine sides, circularity strictly below 1.28878, and requires at least 310 additional pentagons under that same completion ceiling. Both boundary patches leave an open neighborhood of the center uncovered. Neither count is claimed sufficient or attainable.

This is the fourth newly documented pass in this continuation. Earlier lifetime count is unknown. Exact unrestricted optimum, finite attainment, and general interior completion remain unresolved. No literature-priority claim is accepted.

## Complete proof review

The three complete mathematical proofs, both fresh independent mathematical reviews, earlier boundary-closure proof and its complete review, checking guide, README, and integration text were read. Every edited proof/review passage was compared with the complete retained original. Changes only normalize publication references, remove references to withheld operational material, and rebind identities to displayed public bytes. No argument, inequality, limitation, or mathematical premise was dropped.

The free-center polygon inequality R/r >= sec(pi/m) follows by comparing the valid tangential lower perimeter bound with the valid inscribed upper perimeter bound. The finite-polygon reduction and connected planar graph are sound. Counting genuine sides while explicitly retaining collinear subdivision incidences gives sum(6-s_i)=B-2+2X+C. With B=60 this yields the two pentagon budgets. At ceiling at most 13/10 every angle exceeds 72 degrees, hence X=V4 and C=T. The two refined identities correctly include T-junctions and four-cell vertices. These arguments do not assume a face-to-face tiling or concentric disks.

## Additional independently implemented exact checks

A further implementation was written without importing producer or prior-audit checking code. Arbitrary-precision integer and rational computations reproduce:

- All 2,884 strict supporting-half-plane tests for the complete-square witness, with minimum determinant 160383401566530772.
- All 696 strict indisk inequalities, minimum slack 11903868602776199771750141753138239, and all 696 strict enclosing inequalities, minimum slack 823068242597106816174189584.
- Positive radii, smallest numerator 29350614583, 240 vertices, and all 121 per-face margin rows.
- Exact doubled area 8000000000000000000000000, containment in the square, 336 paired interior edges, and six exact boundary intervals per square side. Disjoint interiors and a finite closed union of equal area prove coverage at every point, including the square boundary.
- Every one of 7,260 unordered pairs, independently searching polygon support edges; the complete published intersection table has 6,916 empty pairs, eight point contacts, and 336 segment contacts. Every published separator and intersection endpoint is checked.
- Every one of the eight explicit edge flips, including old-edge orientation, third incident faces, unique insertions, and every final face cycle.
- Both entire boundary witnesses: 128,166 and 722 canonical support tests; separate valid disk centers; all 1,540 pair separations per patch; 1,484 empty pairs and 56 full-edge contacts per patch; exact complete published pair tables; and 15 intervals on each square side.
- The original inner cycle has 6,932 edges, with 6,876 one-cell and 56 two-cell vertices. The coarsened inner cycle has 416 edges, with 360 one-cell and 56 two-cell vertices. Exact angle-sector checks establish the claimed local incidence restrictions.
- All 80 coarsened canonical supports are retained original inward support lines. All 10,146 original-vertex/new-support comparisons hold. Placements, scales, disk centers and prescribed endpoints are unchanged.
- Both centers are strictly uncovered and both covered areas are strictly less than square area. This independently prevents a boundary-only witness from being accepted as a complete square partition.

## Publication and dependency checks

All 29 payload transformations are reversible in both directions to complete retained original bytes. Every public file is covered by the public manifest. Public audit proof hashes and sizes bind the actual displayed proofs. All 77 first-, second- and third-edition sibling files are exact unchanged dependencies, with complete transitive manifest and relative-link closure. The full predecessor baseline trees are unchanged.

No program, raw solver stream, copied third-party source document, dataset content, private coordination material, or withheld operational hash appears in the public payload. Public source titles and URLs are context only; this review claims no new source retrieval or exhaustive priority search.

Both SVG files are passive. Every complete-square polygon matches the exact rational certificate; boundary illustration coordinates agree with the stated 12-place rounding. Actual rendered images were visually inspected. The boundary image clearly marks its uncovered interior and boundary-only scope.

## Controls and preservation scope

The additional independent checks and hostile/benign controls run in normal Python, -O and -OO, with identical outputs. Hostile cases include geometric corruption, smaller false radius ceilings, missing cells and pair rows, false pair endpoints, topology corruption, active SVG content, broken reversible mappings, and semantic overclaims. Benign cyclic reindexing and exact scaling remain accepted.

The prepared edition reached its actual sealed terminal state before acceptance, after real archive extraction and independent per-file byte-store restoration. Complete retained sources and scoped source-checker outputs are checked rather than inferring unavailable historical runs. The review's separately retained preservation record binds its own final archive and independent byte-store restores, full file comparison, normal/-O/-OO replays, restored-source checks and no-drift verification. No remote repository or queue mutation was made by this review.
