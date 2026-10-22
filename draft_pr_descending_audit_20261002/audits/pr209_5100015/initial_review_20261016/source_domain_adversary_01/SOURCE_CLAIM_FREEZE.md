# Independent source and claim freeze

Created UTC: 2026-10-16T04:36:17.743121+00:00

This freeze was authored after reading only the pinned problem/report and the two fixed primary-source PDFs/texts, before opening the inherited PROOF.md or any inherited review conclusion. Scope: mathematical/source-domain audit of original PR209 head fd09a95b479f376234835a4494693bb1316c85ec, problem 5100015, source k303,b.

## Exact target

For a fixed noncircular ellipse E with center O and axes a>b>0 and a fixed confocal interior **elliptic** caustic C, consider an ordered N-periodic billiard/Poncelet family. At each orbit vertex take the tangent to E; intersect successive tangents to form the ordered outer polygon P'. Its sides are those tangent lines (up to cyclic index shift). Project O perpendicularly to these lines and connect feet in the induced orbit order. The claim is that signed shoelace area(P') times signed shoelace area(the feet) is constant over the family when N is odd or N=2 mod4.

The source's Table4 k303,b is the exact row, distinct from k303,a (N=2 mod4, arbitrary M) and k304 (N=0 mod4, ratio). No centroid assertion is part of this target. All areas in both versions are signed by section2 equation(1).

## Source evidence and domain reconstruction

- v11 PDF SHA256 c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da; published PDF SHA256 c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42. Hashes independently checked.
- v11 introduction p1 explicitly identifies this EB with a pair of confocal ellipses. Figure1 defines outer tangential polygon and inner contact polygon. Section2 p2 assumes a>b>0 and uses real major/minor caustic semiaxes; section4 p13 constructs the confocal ellipse. Published introduction p341, section2 p343, and section4 pp351-352 agree.
- v11 section2 p3 and published section2 p343 define all polygon areas by the ordered signed cross-product sum. Thus even a self-intersecting traversal uses signed area, not enclosed union or absolute triangle area.
- v11 section3.4 p6 and published section3.4 p346 define outer pedal from perpendicular feet, with Table4 caption specifying sides. Table4 gives k303,b, product, N not0mod4, M=O, proof '?'. Table verified visually in both PDFs.
- No hyperbolic caustic appears in the definitions, table qualification, or the experimental method. The source uses a narrower ellipse-pair scope than a generic meaning of elliptic-billiard caustic. Hyperbolic billiards are a separate extension/control, especially relevant to even periods, but their failure would not refute the strict source target.
- No explicit requirement of convexity, primitivity, winding1, or coprime rotation number occurs in the relevant source definitions/table. The displayed example and numerical initialization are convex; this is not a textual exclusion of star traversals. Treat all ordered periodic traversals with the stated caustic as required or explain reduction.
- N=1 and N=2 do not produce nondegenerate elliptic-caustic polygons; the conventional meaningful range is N>=3. The source does not state a minimum in the table. The circle a=b, caustic point/segment, grazing/boundary caustic, and zero-length paths are excluded by the nondegenerate strict ellipse-pair setup; a proof should state this.
- Consecutive antipodal vertices give parallel tangents and no finite P'. In the strict elliptic-caustic setup their chord would pass through O and cannot be tangent to a nondegenerate inner ellipse, so this pathology should be proved impossible rather than silently ignored. A generic hyperbolic extension may have different exceptional configurations.
- Repetition: if a primitive d-gon is repeated r times then N=rd, each ordered signed area multiplies by r and the product by r^2. If N not0mod4 then d not0mod4. Thus a primitive theorem for all such d should extend to repetition without a new invariant claim, provided the parametrization respects induced order.

## Success/falsification criteria, frozen before inherited proof

Accept mathematical scope only if an independently checkable derivation applies to every nondegenerate strict elliptic-caustic ordered periodic family, including both parity classes and star winding, handles finite outer vertices, proves the actual side-line pedal formula, and either covers repetitions or gives the reduction. Necessary denominators, caustic/step relations, and global constancy must be justified without assuming the target.

Falsify by an exact in-domain counterexample, a nonzero independently derived variable term in the claimed product, a mismatched constructed polygon, an uncovered in-domain parity/winding family, circular assumptions, or a central lemma that merely transfers the desired invariant to an equivalent unsupported claim. Floating-point samples only corroborate; they cannot prove all-N constancy. Out-of-source examples (hyperbolic, circle, degeneracy) will be labeled separately.

Independent planned controls: derive tangent intersection and center pedal feet directly from the ellipse equation; compute polygon areas geometrically rather than through the submitted formula; exact symbolic local identities; sample convex/star odd and2mod4 periodic families; reversed ordering, cyclic shifts, repetition scaling, and mutants (wrong pedal lines/order/product/parity) where informative. No full priority investigation yet.
