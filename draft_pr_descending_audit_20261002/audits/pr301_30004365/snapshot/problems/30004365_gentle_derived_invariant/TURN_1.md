# Turn 1: an effective surface-certificate algorithm

2026-10-02. AI-assisted proof candidate; independent source and mathematical review pending. This is a terminating algorithm, with no efficiency or implementation-completeness claim. The classification and geometric construction are credited existing inputs. No historical novelty claim is made.

## Claim and exact input

For a finite-dimensional gentle bound quiver (Q,I), with I given by its quadratic monomial generators, there is an algorithm computing its complete numerical derived-equivalence invariant. The algorithm also outputs explicitly encoded geometric symplectic curves and their winding numbers. It works over the fixed base field of the source; no coefficient arithmetic or algebraically closed field assumption is introduced.

The source is Plamondon's Problem3.4, OWR3/2020 pp161–164. The final Amiot–Plamondon–Schroll (APS) paper, Selecta Mathematica29:30 (2023), Theorem7.4 and Remark7.6, identifies the outstanding computational ingredient as extracting a geometric symplectic basis from the bound quiver. Neither source imposes a polynomial-time bound or forbids geometric intermediates. The method below deliberately uses an exhaustive but terminating search for that ingredient.

References:
- Original: https://ems.press/content/serial-article-files/46842
- APS final: https://doi.org/10.1007/s00029-022-00822-x
- Palu–Pilaud–Plamondon (PPP), Non-kissing and non-crossing complexes for locally gentle algebras, J.Comb.Algebra3(2019),401–438; construction and inverse theorem in §4.2: https://arxiv.org/abs/1807.04730

## 1. Recover a finite combinatorial surface

Use the explicit lozenge-gluing construction in PPP Definitions2.2,4.6,4.8 and Theorem4.10. This is a finite combinatorial procedure, not an oracle asking for a drawing:

1. At each original vertex add distinct leaf arrows until there are two incoming and two outgoing arrows. Complete the relation table so that each incoming arrow has one related and one unrelated outgoing continuation. This completion is finite: enumerate the two-by-two matching choices extending the original table and choose the lexicographically first permissible one. Gentleness guarantees one exists; the unused slots are exactly the blossom choices.
2. Make one oriented quadrilateral for each resulting arrow, with its source/target vertices and the two additional, differently colored corners prescribed in PPP Definition4.6. Glue the relation-side pair for a related continuation, and the nonrelation-side pair for an unrelated continuation. Record every edge identification and corner equivalence by finite union-find tables. Use the orientation and side labels of that definition; there is no numerical surface embedding to guess.
3. Retain the two colored dissections and marked corners. The interior colored corners are punctures; boundary colored corners are marked boundary points. Theorems4.9–4.10 guarantee the resulting oriented surface and dual dissections recover (Q,I). For finite-dimensional input the white puncture set is empty. The red/green labels are converted to APS's white/black convention by requiring the white dissection's bound quiver to be the input; this can also be checked from the finite incidence/relations tables. Blossom leaf points are auxiliary boundary points, not additional colored marks.

The construction supplies polygonal charts and finite affine edge identifications, as well as the embedded dual dissection Delta*. Subdivide polygons into triangles and subdivide the resulting finite polygonal manifold if necessary to obtain a genuine finite triangulation T. All vertices, subdivision points and edge identifications can be rational. This is the elementary constructive triangulation of a finite polygonal surface: triangulate each polygon using a new central vertex and matched subdivisions on identified edges, then subdivide the induced cell structure to separate repeated incidences. The side-pairing data retain which sectors meet at each corner; no geometric recognition problem is left undecided.

We use the compact surface with its marked puncture points retained while constructing T. Punctures are then removed by disjoint small polygonal neighborhoods; retain their labels separately from original boundary circles. Call the resulting compact surface S0. Curve calculations are in its interior and represent curves of S minus P. Cutting off sufficiently small puncture collars does not change any of the required topological or winding data.

For a disconnected input, perform these steps componentwise. Alternatively enumerate the components' finite outputs and return their multiset; the source's connected-surface classification applies to each factor. Empty input may be rejected as outside the nonzero source class; isolated vertices, representing the field, are handled by the same blossom construction or by the disk with two white and two black boundary marks and one dissection arc.

## 2. Elementary computable surface operations

A finite triangulated oriented surface has decidable finite incidence tests: every interior edge has two incident triangles, boundary edges one, and vertex links are circles or intervals. Connected components and boundary cycles are found by graph traversal. Euler characteristic is V-E+F. For a connected component with h boundary cycles its genus is (2-h-chi)/2.

Given finitely many rational polygonal arcs in the triangle charts, all intersections are exactly computable by rational linear algebra. Collinear overlaps and multiple intersections are detected and may be rejected. Subdivide at all intersection points and triangulate the planar polygonal regions. Cutting along an embedded polygonal graph is also finite: split each graph edge into its incident-side copies and split vertices according to the cyclic order of adjacent triangle sectors. The same graph traversal/Euler calculations compute every complementary component and its genus and boundary count. These procedures work with sector copies, so they do not identify distinct boundary occurrences of a puncture or repeated polygon corner.

A small regular neighborhood of an embedded graph is built by taking one disk per graph vertex and one thin rectangle per edge, attached in the recorded cyclic orders. This is itself a finite surface-with-boundary complex, and its complementary surface is obtained by the preceding cutting operations. All widths may be chosen rational after inspecting the finite positive separations from disjoint segments.

## 3. A terminating search for a geometric symplectic basis

First compute the genus g of S0. If g=0, return the empty handle basis.

For g>0 enumerate, in increasing height H, every ordered list of 2g closed polygonal curves in the triangle charts of T whose vertices have rational barycentric coordinates with numerators and denominators bounded by H and whose total number of segments is at most H. Segments must lie in a single triangle; edge-crossing points on paired charts have identical rational edge parameters. This is a finite list for each H, and every rational PL loop system eventually appears. Repeated encodings do no harm.

Label the curves a1,b1,...,ag,bg and accept only a list satisfying all these finite tests:

- Every curve is embedded, lies in the interior of S0, and avoids marked/puncture collars and triangulation vertices. Consecutive segments join without a reversal.
- ai and bi intersect transversely in exactly one point; all other distinct curve pairs are disjoint. No triple intersections occur. Choose orientations with local intersection sign ai.bi=+1.
- The closed regular neighborhoods Ni of ai union bi are disjoint, contain no puncture collar or original boundary, and are once-holed tori. The complement S0 minus the interiors of all Ni is connected and has genus zero.
- Curves meet Delta* transversely away from dissection endpoints, with no segment overlap or simultaneous triple intersection. Each curve has finitely many crossings. Every segment of a curve inside a cut-open Delta* polygon is simple and separates that disk into two sides.

The last condition is readily checked by cutting the polygonal arrangement. Because there are no white punctures, APS Proposition3.11 says each Delta* polygon is a disk with one white boundary mark. The loop systems may be moved away from sufficiently small black puncture collars. At a dissection crossing they can be smoothed to be orthogonal to the dissection, without changing their combinatorial sides or intersections.

**Acceptance is sound.** A regular neighborhood of an embedded pair with one transverse crossing is a once-holed torus. Disjoint such neighborhoods with connected planar complement form precisely a geometric handle system. Collars of all original boundaries and punctures are in the complement. Thus these are the geometric symplectic curves required by the classification, not just an arbitrary integral homology basis. Their homology intersection matrix is the standard symplectic matrix, and the complement certificate fixes the necessary embedding information.

**The search terminates.** By the classification of compact connected orientable surfaces, S0 admits g disjoint embedded handles with connected planar complement, and each handle has two simple core curves crossing once. Choose such curves away from boundary collars and all finitely many marked points. A small smooth perturbation puts them transverse to the fixed finite dual dissection and triangulation, with only the prescribed pairwise crossings. A sufficiently close polygonal approximation in the triangle charts preserves embeddedness, the transverse intersections, their cyclic orders and the connected planar complement. Rational points are dense in each chart and on its edges, so the approximation can be chosen rational and has finitely many segments. Its finite encoding appears at some H. It satisfies all the tests. Therefore the algorithm halts for every promised input; there is no appeal to waiting for a negative answer from an undecidable test.

No quantitative bound for the first successful H is asserted. The proof of eventual appearance is the termination argument, as in an ordinary exhaustive search with a guaranteed finite witness.

## 4. Winding numbers are finite signed sums

Construct one small polygonal parallel curve around each original boundary and each removed puncture. Orient each as the corresponding boundary of the remaining surface, consistently with APS Proposition3.20(5): the main surface lies to its right. Perturb to be transverse to Delta*, avoiding the finite exceptional points. This is an explicit finite collar operation. Let B denote these b+p curves.

For every curve in G union B, cut at Delta* crossings. For each resulting simple oriented arc in a disk polygon, determine by the recorded orientation whether the polygon's unique white mark is on its left or right. Add +1 for left and -1 for right. This is APS Lemma3.18, applied after local orthogonal smoothing. The side of a mark is determined by the finite polygon cut and a triangle-sector traversal, not floating-point angles. Therefore the winding integer is computed exactly.

A boundary-parallel curve or a handle curve cannot remain entirely in one disk polygon: it would be contractible there, except for irrelevant contractible boundary cases. In the disk-component case a boundary collar still crosses the dual arcs when the algebra is nonzero (the isolated-field model is explicitly included). If a chosen PL encoding has an avoidable excursion, the polygon rule still applies to its simple pieces; alternatively simplify the excursion by a disk isotopy and re-evaluate. No straight-line angle summation is substituted for the line-field winding convention.

## 5. Output and correctness

Return the topological data, all individual boundary/puncture winding integers paired with their marked-point counts, and the following handle invariant:

- Genus0: no additional handle datum
- Genus1: nonnegative gcd of w(a1),w(b1) and all w(c)+2 for c in B; gcd of all zeros is0
- Genus at least2: the odd-winding flag on G union B; if all are even, the flag that some boundary/puncture winding is0 modulo4; if that flag is false, the bit sum_i (w(ai)/2+1)(w(bi)/2+1) modulo2

Use n(c)=0 for punctures and the number of white marked points for original boundary components; retain b,p and total marks explicitly. Sort the boundary records as a multiset. Raw basis winding numbers and the curve encodings are also returned as a certificate, but are NOT part of the canonical comparison key, since they depend on the chosen basis. The numerical key retains the APS classification data and, explicitly, all puncture winding numbers. The final printed Theorem7.4(2) quantifies winding equality only through j=b, although its permutation and n-values run through b+p; we do not silently change that printed range. Keeping all b+p records is safe: their equality implies the displayed sufficient conditions, and their necessity follows separately from APS Theorem6.1/Remark7.2, since an orientation-preserving marked-surface homeomorphism carrying the line field preserves winding around every puncture as well as every boundary. Thus the additional records cannot distinguish derived-equivalent inputs. The workshop's shorter summary is not used to drop paired boundary winding information. A componentwise multiset handles products: indecomposable blocks are preserved by a derived equivalence, equivalently by its action on the primitive central idempotents of the category.

Every operation is finite, every search stage is finite, and §3 proves the only unbounded search terminates. PPP identifies the constructed dissection with the input algebra, the accepted certificate supplies the required geometric basis, and APS's winding rule and Theorem7.4 identify the output key as a complete derived invariant. These existing theorems supply the classification; this candidate supplies an explicit, although impractical, effective basis-extraction step and its termination certificate.

## Limits and review requirements

No polynomial/exponential complexity bound is proved, and no full production implementation or practical QPA integration is supplied. A literal algorithm can be effective while being extremely inefficient. Independent review must assess whether the source requires anything beyond that literal effectiveness, and must verify the conversion of PPP's colored/dissection conventions, the rational PL enumeration and complement test, boundary orientations, disconnected/isolated cases and the exact final comparison key. The cited final paper's statement that its methods do not provide this algorithm is not claimed false: the exhaustive certificate search is an additional step, not attributed to those authors.

One substantive author turn completed. Candidate completion estimate100% for literal effective computation, pending independent review; this is a planning estimate, not peer-review certification. If a mathematical or source-scope gap is found, retain the proved scoped algorithmic parts and continue substantive research under the remaining turn budget.
