# Independent review of the fifth and final square-circularity edition

Problem row 1757 / 5500059 / AMR0540059. Review date: 2026-10-13.

## Verdict

Accepted for its stated partial and conditional results. The edition preserves the mathematical content of the complete final construction report, the adjacent-right pentagon proof, and both independently authored mathematical reviews. Its rational certificates, pair data, margin table, angle records, illustrations, and exact predecessor dependencies are mutually consistent.

The accepted construction is a 136-cell partial collar at strict circularity ceiling 64439/50000 = 1.28878. It retains the 56 boundary cells and adds 80 hexagons. It covers approximately 32.24892181598094% of the square and leaves an open neighborhood of the center uncovered. This number is not a whole-square upper bound.

The sharp adjacent-right pentagon minimum is 1.290772978969... . The near-90.30-degree restriction applies to the stated full facets only when their seams are exact equal-unfilled-sector bisectors. The separate three-cell dead-end certificate obstructs retaining those three cells at ceiling 13/10; it does not reject the accepted 136-cell collar.

The whole-square interval remains G <= Gamma_fin < 1.295516, with G = 1.2886844618704579... as the previously audited source context. Neither the exact optimum nor unrestricted finite attainment is established. This is the fifth and final newly documented mathematical pass; the earlier lifetime count is unknown. This review does not start a sixth research pass.

## Complete proof review

I read the complete final construction and pentagon arguments and both complete mathematical audits, rather than accepting the summary statements or replay booleans. I also read the full fixed-patch side-deficit proof used by the final count. The originals and publication-normalized texts were compared in full through reversible whole-text transformations.

For the collar, the indisk conditions use positive oriented support distance and a nonnegative squared support slack. The enclosing condition is strictly positive at every vertex. These are sufficient because the intersection of the supporting half-planes contains the displayed disk, and a disk containing all vertices contains their convex hull. The true inradius can exceed the witness radius and the true circumradius can be smaller than the displayed bound. The argument therefore correctly permits independent, nonextremal centers.

For the pentagon theorem, moving each support inward to the normalized unit disk preserves all five genuine sides: the tangent point on any one support strictly satisfies the other distinct unit-normal inequalities. This justifies the reduction without introducing a concentric-circle assumption. The adjacent-right family has positive heights a,b with ab<1. Its larger height t yields a diagonal lower bound increasing in t, while the apex-triangle bound decreases on 0<t<1. Reflection and averaging of both vertices and enclosing centers justifies the symmetric-apex comparison for asymmetric polygons.

The two bounds cross at the unique root in (0,1) of m^4+2m^3+4m^2-2m-1. The displayed symmetric pentagon is tangential, has exact inradius one by its width, and is cyclic with a diameter attaining the required enclosing radius. Thus the claimed sharpness and attainment apply to this particular pentagon angle class. They do not establish square-partition optimality.

The support-perturbation estimate uses the origin-centered radius M=2gamma-1, justified because an enclosing disk of radius at most gamma contains the unit indisk. It gives boundedness and a scaled inclusion after normal perturbation. The proof includes both genuine-pentagon and merged-support quadrilateral cases. The tilted-angle argument proves a sufficient rational lower bound, with no false claim of sharpness for tilted angles. Its endpoint comparisons certify the bisector angles at precisely vertices 5, 6, and 7. Variable seams, subdivided facets, or cells with six or more sides remain outside that conditional obstruction.

The local dead-end reasoning correctly uses an actual exterior sector, not an unidentified smaller angle. A finite completion must have a new cell containing the obstructed tip: finitely many closed cells avoiding it cannot cover arbitrarily close points. Splitting the narrow sector among several cells cannot evade the necessary individual-angle bound.

Finally, the Euler calculation allows subdivisions and T-junctions. With 60 outer edges and 1,068 genuine sides among 136 fixed cells, the added-side deficit is 310+2X+C. The independent-center polygon inequality R/r >= sec(pi/s) excludes added cells with fewer than five sides below sqrt(2). Hence at least 310 further pentagons and 446 total cells are necessary. At ceiling 13/10 the angle bound gives X=V4 and C=T, producing the stated refined identity. None of these necessary conditions supplies an attaining completion or a finite stopping rule.

## Newly authored exact verification

A separate standard-library Fraction checker was authored for this edition review. It imports none of the producer, mathematical-audit, or preparation validators. It reconstructs the rational placements, verifies the mathematical content directly, and independently checks publication identities and transformation coverage. The accompanying INDEPENDENT_EDITION_CHECK.json records its result.

The geometry checks include:

- Reconstruction of all 136 placed polygons, strict global support inequalities, positive indisk squared radii, valid indisk witnesses, and strict enclosing-disk witnesses.
- Exact recomputation and equality comparison of every field in all 136 published margin rows, including the final row, actual area, genuine side count, support determinant, indisk slack, and enclosing slack.
- Exact replay of every one of the 9,180 producer edge-axis witnesses, with pair uniqueness, valid edge selection, and separation direction checked.
- Independent verification of every published pair-classification axis and the full intersection on its supporting separator. There are precisely 8,972 empty intersections and 208 complete shared edges; no partial-edge or point contact is accepted.
- Exact edge inventory, opposite orientations of shared edges, the 60 outer-square edges, and interval-by-interval coverage of all four square sides.
- A connected degree-two residual graph with 592 edges, supported by the global intersection classification that rules out crossings and accidental contacts.
- Complete recomputation of all nine canonical tip tests, both canonical end tests, and all 144 global two-cell residual-angle records, including exact D and A values and canonical strict margins.
- Exact old and new covered-area fractions and strict support exclusion of the square center from every cell.
- A separate exact check of the three-cell certificate, all three full shared interfaces, strict disk witnesses, the exterior-sector rays, exclusion of its tip from the parent, and the strict cosine obstruction at 13/10.

The pentagon arithmetic is also independently recomputed: both adjacent-right split margins, its stability margin, a strict rational root and rho enclosure, both tilted split margins, its stability margin, and all six endpoint comparison margins at the three selected vertices. Clearing positive denominators recovers the stated sharp equality polynomial. The geometric deductions remain supported by the complete written proof, not by the arithmetic checks alone.

Hostile tests separately alter the unresolved status, the final-pass stopping condition, the whole-square interval, the last pair record, the last global angle record, the last margin row, an incenter, support orientation, the final facet margin, and an illustration's element type. These are semantic checks run outside the manifest gate; invalid mathematical or scope content is rejected even when no digest comparison is used as the reason. Reformatting mathematical JSON without changing its values is a benign control and remains accepted.

## Editorial fidelity and dependency closure

The reviewed edition has 23 public files totaling 1,181,953 bytes, including its 26,192-byte manifest. The manifest identifies all 22 other public files and exactly 107 unchanged base-public dependencies from the first four editions. Each predecessor manifest and its entire declared public payload are present in that closure. Every listed dependency's actual bytes, size, and digest match; every local and cross-edition Markdown link resolves within the retained closure.

All 22 nonmanifest public files have complete reversible maps to retained source bytes. Whole-text forward and reverse splicing reproduces the exact public and original texts. The independently applied editorial replacement list accounts for every transformed byte. The certificate and mathematical result objects remain byte-identical where no reference normalization was needed. Newly authored guides, illustrations, and margin data match their retained edition-authored originals.

The original pentagon proof's section 6.3 named EXACT_CHECK.json. The public proof now points to EXACT_PENTAGON_OBSTRUCTION_CHECK.json, and the pentagon review explicitly discloses that documentary correction. This changes no premise, formula, conclusion, or arithmetic. Both independent review documents bind the actual byte length and SHA-256 of their respective normalized public proofs; they do not mistakenly retain the original proof identity after an editorial change.

The public files contain authored mathematical material, exact rational witness data, mathematical replay metadata, and passive illustrations. No runnable program, copied scholarly document, raw numerical search ledger, private coordination text, local operational path, or withheld operational digest is included. Mathematical rational components that happen to contain 64 decimal digits are treated as numbers, rather than misclassified as hash claims. The source-context references remain in the exact prior editions; this review makes no new literature-priority claim.

## Illustrations

Both SVG files were checked as passive XML with no scripts, event handlers, external resource references, or active document declarations. Their polygon coordinates agree with the rational certificates under the stated affine display transformations, within half a unit of the last displayed decimal. The overview contains 136 polygons; the canonical view contains its parent plus ten hexagons.

The rendered images were also inspected. Their labels fit and explicitly identify the open center and incomplete finite-completion status. The illustrations clarify scale and placement but are not mathematical evidence in place of the exact certificates.

## Replay and preservation acceptance

Actual extraction of the preparation archive and a separate reconstruction from its compressed actual-byte store produced complete matching preparation trees. All 201 retained source files were materialized independently from each recovered tree, with 160 distinct source objects. Scoped restored-source replays cover the producer collar, producer local dead end, producer pentagon arithmetic, independent geometry audit, and independent pentagon audit.

Each of those five source entry points was actually executed in normal, -O, and -OO modes in both recovered source trees. Their 30 outputs match the corresponding accepted original mathematical results byte for byte. The newly authored edition checker and its semantic controls were also run in all three modes on the original preparation and both recovered preparations. All nine results agree. Checks use explicit exceptions; optimization cannot remove them.

Full preparation inventories and the first-four-edition baselines were compared before and after these operations. No retained input changed. A compact separately preserved review package retains this authored review, its exact checker, the replay evidence, and the preparation inputs needed for reproduction. Actual archive extraction, separate byte-store reconstruction, and restored review replays are part of the successful terminal evidence, rather than inferred from a plan or an existing receipt.

No remote repository or queue changes were made by this review. Publication and root acceptance remain separate steps. The final edition is accepted only with the partial, restricted, and unresolved scopes stated above.
