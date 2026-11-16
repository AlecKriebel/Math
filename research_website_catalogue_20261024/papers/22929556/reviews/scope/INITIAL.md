# Source-only initial freeze: 22929556

Frozen UTC: 2026-11-16 09:36:07. Completion estimate toward this scientific scope review: 55%.

## Exposure and custody

Read all three actual native manuscript pages through own new 135-dpi Poppler rasters and all 160 lines of `sources/published-source/container-001/tree/knudson-gradient-path-v1.0.1/paper/paper.tex`. The manuscript necessarily exposed its proof. No scientific support/code/results, deposited audit judgments, current other-family findings, or foreign mathematical bodies were read. Metadata was read by a field projection excluding its public description. No native scientific program, external contact, or prepared outreach occurred.

Native PDF: 49210 bytes, SHA256 `7e63996fdec314e02adf668eb676e4926a5700097d664bf28ab128d617ca210e`. TeX: 7213 bytes, SHA256 `364d097566295023d0c19e0b3e1a52e6f58d24760bffc6be9a7b84c451683a05`. Rasters `rasters/page-{1,2,3}.png` respectively SHA256 `e32c204be2a93f3834de9b788fc1a3e4a3553b4ec6ab5071d7b73ee202be874d`, `eb52c9e19898a7d6dded5dba92689cc10a216af621150b0f2e9f4ec452cf8c72`, `7c09f53223ff0831331f4b5d41d200619b95dc5387ab5675ca23adb19fd9ede5`. Printed date/version: 23 September 2026 / version 1.0.1. Native version field is ABSENT, which is not inferred from the folder or printed version. Native publication date `2026-09-23`; created `2026-09-24T03:43:53.253905+00:00`; updated `2026-10-10T21:45:29.013278+00:00`. Creator name Kriebel, Alec, ORCID `0009-0001-9320-500X`, native creator affiliation null; printed footnote says Independent researcher. Native license CC BY 4.0. Asset order is SHA256SUMS, source-and-verification.zip, paper.pdf. Complete original metadata/order/rights and transport are preserved in source-owner manifests reused by reference.

## Exact target and boundary

The finite construction is the one-simplex-at-a-time filtration a,b,c,d,cd,bd,ac of the interval a-c-d-b. The claim is that persistence pairing P={(d,cd),(c,bd),(b,ac)}, restricted to incident face/coface pairs, gives the fixed field V={(d,cd)}, in which the critical edge ac has zero gradient paths to critical vertex b although (b,ac) is a persistence pair. This refutes the cited conjecture only if its exact original field, class of filtrations, coefficient and path convention match those stated. The mathematical construction is checkable without any program or foreign theorem. It makes no minimality assertion and no claim against results for iteratively modified matchings. An independent identification of the original conjecture is the remaining source gate.

## Actual independent derivation and controls

Every edge's two endpoints precede it, so the filtration is valid. The stagewise component partitions are:

| stage | components |
|---|---|
| 1 | a |
| 2 | a; b |
| 3 | a; b; c |
| 4 | a; b; c; d |
| 5 | a; b; cd |
| 6 | a; bcd |
| 7 | abcd |

There is no 1-cycle at any stage because every graph is a forest. For s<=t the H0 map sends each s-component to the containing t-component; its rank is the number of t-components meeting the s-stage vertex set, over every field. This rank description independently yields the four interval summands [1,infinity), [2,7), [3,6), [4,5): the youngest singleton d merges at 5, the surviving component whose oldest vertex is c merges with b at 6, and the b-component merges with a at 7. Equivalently the multiplicity of each finite interval can be recovered by the rank invariant's mixed finite difference. Thus the finite birth/death pairs are exactly (d,cd),(c,bd),(b,ac), independently of the column calculations.

For a separate signed algebraic control, orient cd from c to d, bd from b to d, and ac from a to c. Boundary columns in row order a,b,c,d are d-c,d-b,c-a. Left-to-right pivot cancellation gives d-c,(d-b)-(d-c)=c-b,(c-a)-(c-b)=b-a. Their latest nonzero rows are d,c,b, each with coefficient +1 over any field (also +1=-1 in characteristic 2 without causing zero pivots). All lower-dimensional birth columns are zero. Thus no hidden characteristic assumption changes the pairing. The only persistence pair whose lower simplex is an actual facet of its upper simplex is (d,cd).

The directed incidence graph of V has exactly six arrows: ac->a, ac->c, bd->b, bd->d, d->cd, cd->c. The vertex order ac,bd,d,cd,a,b,c is a topological ordering, proving that the matching is acyclic, so it is a discrete gradient in this explicit example. Critical simplices are a,b,c,bd,ac; their alternating count is 3-2=1, matching the interval's Euler characteristic. From ac either descent reaches a or c, and neither vertex has an outgoing matched edge. The reachable set is exactly {ac,a,c}. Therefore b is unreachable even if every directed path were allowed; a gradient path, being more constrained, cannot exist. Both ac and b are critical, and b is not a vertex of ac. This establishes the finite counterexample under the stated conjecture interpretation, with zero versus one paths unambiguous.

The earlier nonincident pair (c,bd) has one path bd->d->cd->c; its other initial endpoint b terminates. Reversing that path indeed removes (d,cd) and adds (d,bd),(c,cd). In this changed matching ac->c->cd->d->bd->b is a valid path. This checks that the claimed contrast between fixed-field and cancellation-based statements is real, rather than concluding that no matching can connect the pair.

## Falsifiers and remaining scope gap

The local finite pairing, admissibility, acyclicity and no-path assertions are proved above. The remaining decisive falsifier would be an original conjecture whose field is updated by ordered cancellations, requires a more restrictive filtration/function class not satisfied here, or uses a different meaning of P/path. The original wording and nearby definitions must be read in its primary body after the source gate opens. ELZ's full theorem is not needed to justify these hand computations; the maps and signed reduction were explicitly checked. The related BLW statement can be scoped separately without assuming that this example refutes it. No historical firstness/current openness claim is inferred from the manuscript's bounded audit assertion. Followup remains null; no replacement theorem or extended repair is proposed.
