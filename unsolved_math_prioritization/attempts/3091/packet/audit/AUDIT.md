# Independent mathematical and executable audit: generalised empty hexagons

**Target:** 3091 / OPG-59923; assigned rank 1058.  
**Audit date:** 2026-10-08 UTC.  
**Decision:** accept the authored elementary partial results and the disposition **exhausted, 5/5, full target unresolved**. This is not acceptance of a complete solution, a novelty claim, or a formal proof certificate.

No mathematical correction to the frozen report was required. The original author freeze was not edited. This audit and its additional checks are separate artifacts.

## 1. Public derivative and accepted mathematical scope

This is a labeled public derivative of an independently completed mathematical
audit. The proof-by-proof analysis below is preserved. The mathematical report,
native geometry checker, authored point fixtures and independent Caratheodory
oracle are unchanged. Original research-history material, original full-packet
manifests and identifying aggregate archive metadata, and historical receipts
that bound excluded files are not distributed or authenticated here.

Fresh public-only manifests enumerate exactly the retained public files.
The new replay checks the native geometry and independent oracle against those
public inputs. It does not replay or certify integrity of the full original
private packet. Fresh complete outputs and controls are supplied separately.

## 2. Mathematical scope and conventions

The target is finite point sets, every fixed integer ell >= 3, six distinct extreme points, and emptiness of the **closed** convex hull relative to the entire ambient set. Strict convexity, ordinary two-dimensional interior, and boundary blockers are kept distinct throughout the report. A weakly convex six-set, a subset-relative hole, and a pentagon do not solve this target.

The report uses H=30 as a literature dependency. For completeness, an exact-30-point general-position theorem extends to all larger finite general-position sets by choosing a linear functional injective on the ambient set and taking its first 30 points. Every other point lies beyond their projection interval and hence outside their hull. This elementary observation justifies applying H=30 to the perturbations in Proposition 1 without assuming that arbitrary subset holes are ambient holes.

The inspected literature supports the general-position case and the separate bounded-collinearity pentagon theorem. The report makes neither an all-ell conclusion nor an ell=4 conclusion.

## 3. Proof-by-proof review

### 3.1 Boundary cleanup lemma B: accepted

The finite minimum-area selection is nonempty because it includes the original strict k-set. Every selected hull remains full-dimensional inside the original hull. Its interior therefore lies inside the original interior and is empty of ambient points.

A boundary blocker distinct from all selected vertices must lie strictly between the endpoints u,v of an edge. Replacing u by p=(1-t)u+tv, with 0<t<1, keeps k distinct points. The report's support-line argument establishes **global** strict convexity, not just positive local turns. In particular, for the preceding vertex w and any vertex z on the remaining v-to-w chain, orient(w,p,z) is the positive combination of the corresponding chord/support determinants. The new segment wp cuts away u, while pv retains the old uv support line. All retained vertices remain extreme, including at k=3. The removed corner has positive area. This contradicts minimality and proves closed emptiness.

There is no assumption that boundary blockers are absent beforehand. The lemma changes the vertices and cannot repair a loss of extreme vertices in a degenerate limit. Both restrictions are stated correctly.

### 3.2 Perturbation and limiting six-set: accepted with the stated gap

Label-preserving perturbations exist by avoidance of finitely many zero determinant conditions. Distinct limiting points remain distinct when labels are kept in disjoint neighborhoods. Passing to one repeated six-label set is a finite pigeonhole step.

The support-function margin argument correctly establishes stability of membership in the ordinary interior of a full-dimensional limiting hull. It excludes unselected ambient points from that interior. If a selected point were interior, its deletion would leave the limiting hull unchanged, and the same stability argument would contradict its extremality in the approximating six-sets. A segment limit has empty plane interior and is explicitly allowed.

For ell <= 6, noncollinearity of the six selected points follows from the line-size bound. Counting boundary points over h edges gives at most h(ell-2), since every corner is counted twice before correction. At ell=3 this forces six corners. At larger ell it does not. The six-point triangular fixture has maximum collinearity three and loses three corners in the limit; all tested positive rational perturbations regain strict convexity. It demonstrates failure of direct transfer, not a large counterexample.

### 3.3 Deletion and disjoint slabs: accepted

A projection injective on all ambient points exists. The consecutive 30-point blocks of Q have genuinely disjoint closed projection intervals: the last projection in one block is strictly below the first in the next. A block hole is therefore empty relative to all Q, including any incomplete leftover block.

Each deleted point can block at most one chosen hexagon, because it can enter at most one slab. Thus at least max(0, floor((n-d)/30)-d) chosen hexagons remain. These are vertex-disjoint and closed-empty in P. The sufficient inequality is exactly n >= 31d+30; the contrapositive n <= 31 tau(P)+29 is correct. The argument also gives (H+1)d+H for any valid H.

The maximal-general-position extraction inequality counts at most ell-3 outside points per pair-line of a maximal subset. Overlap only overcounts and is harmless. It gives no bound on ambient blockers. The inductive disjoint-triple construction correctly forbids old-old-new and old-new-new triples using nonzero polynomial conditions, while allowing each intended new triple. Its deletion number is exactly one per triple, so bounded collinearity does not imply sublinear deletion cost. This is an obstruction to the proposed deletion bound, not a hole-free construction.

### 3.4 Grid parity obstruction and lower bounds: accepted

A line meets an m by m grid in at most m points; rows attain m. Five vertices force two equal parity classes. Their midpoint is a grid point in the closed hull and cannot itself be a strict vertex of the selected polygon. This includes edge midpoints and is exactly why closed emptiness matters. The proof covers every k >= 5, not only the finite enumerations.

Taking m=ell-1 yields the conditional lower bound (ell-1)^2+1. The additional lower bound 30 uses the known 29-point general-position example as a literature dependency. Heule and Scheucher credit this witness to Overmars; no witness coordinates or independent witness verification are claimed here. Affine transformations preserve the relevant geometry and do not produce an unbounded family at fixed ell. No cluster-amplification proof is supplied or implied.

### 3.5 Boundary-only sets and final layer: accepted

The collinear case cannot satisfy n>5(ell-2) for ell>=3. Otherwise the edge-incidence count n<=h(ell-2) forces at least six hull corners. Any selected six corners remain extreme in their own hull. Its interior lies in the full hull interior, which contains no ambient points under the boundary-only hypothesis. Lemma B then removes possible edge blockers.

Removing **all** boundary points is essential in the layer argument. Every retained point is strictly inside the previous two-dimensional hull, so any hull of retained points stays inside that interior. Earlier removed points are consequently outside the final hull. Degenerate final layers cause no problem. Thus a last-layer hole would be ambient-empty, and the reported last-layer bound follows.

This does not bound earlier layers. Arbitrarily long finite nested-triangle configurations can be chosen generically with no collinear triple; their three-point final layer says nothing about total size. The report correctly avoids the false claim that a boundary subset cannot acquire more corners than its parent hull.

### 3.6 Nearest one-edge ear: accepted

The strict inequalities defining E_i ensure that q sees precisely one polygon edge and lies strictly inside all other edge halfplanes. The augmented hull is the old pentagon plus the attached triangle, and all six proposed vertices are extreme. Thus this is a global convex-hull conclusion, not merely an orientation test around a potentially intersecting list.

For a blocker in the attached triangle, the barycentric coefficient gamma of q is zero only on the clear old edge. Otherwise gamma is strictly between zero and one unless the point equals q. Every other edge determinant is then strictly positive, and its distance determinant from the base is gamma times that of q. This places the blocker in the same E_i, closer than the selected minimum. Blockers on the new side edges are included. Ties at the minimum cannot block, since every non-apex point in the triangle has smaller distance.

The explicit two-edge exterior fixture leaves the pentagon empty, has no collinear triple, and has only five extreme points. It validates the claimed obstruction to deducing ear occupancy from the existence of exterior points. The pentagon theorem supplies a pentagon, not the missing occupied ear. The report preserves that gap.

## 4. Public-only native geometry review and replay

The entire native geometry code was reviewed. It uses exact integers/rationals
and explicit exceptions, with no Python assert statements. The monotone-chain
hull removes collinear intermediate points. Closed containment includes polygon
edges and handles singleton/segment cases separately. No solver, network service
or external proof assistant is called.

The fresh public replay runs the unchanged geometry checker and the independent
oracle in normal, -O and -OO, using -I -S -B. All input files are read-only under
actual/effective UID 1000. Native geometry probes attempt an existing-file update
and a new-file creation; both must fail with PermissionError. The original
whole-packet integrity checker is omitted because the public inventory differs.
The fresh publication wrapper authenticates the new public inventory instead.

The original finite counts are 4,494 five-subsets, 8,092 six-subsets, 1,162 parity
blockers, 4,095 boundary subsets with 738 applicable cases, 511 extraction cases,
four cleanup sizes, eight perturbations, six intended triples and five ear regions.
One slab fixture does not prove the universal slab theorem or H=30.

Eight meaningful semantic controls are replayed in every optimization mode:
missing fixture, invalid fixture schema, an interior rather than boundary blocker,
a weak six-set acquiring a corner, a destroyed intended collinear triple, ignored
closed-edge blockers, farthest instead of nearest ear, and slab constant 30 rather
than 31. All 24 must give the exact intended error, structured FAIL, exit 2 and
empty stderr. Unrelated crashes are not accepted. Public-only integrity/schema
controls are documented separately in the publication evidence.

## 5. Independently implemented geometry oracle

`independent_geometry.py` implements closed-hull membership by the planar Caratheodory criterion: singleton, segment, or nondegenerate triangle. Extremality is checked by asking whether each point lies in the hull of the remaining points. This differs materially from the native sorted monotone-chain hull and its polygon-halfplane membership test.

In each optimization mode it independently checked:

- Every 3-, 4-, 5-, and 6-subset of the 4 by 4 grid: 560, 1,820, 4,368, and 8,008 cases
- Native strictness against the oracle on all 14,756 cases
- Native closed-hole rejection against the oracle on all 12,376 five/six cases
- 208 global corner replacements, for k=3 through 10, including rational points very near both endpoints; extremality, containment, and strict area decrease all checked
- 15 minimum-area cleanup outputs with simultaneous blockers on every edge, for k=3 through 7
- 16 exact perturbation scales
- Five ear regions with 156 rational candidates total
- 14 affine fixture checks, including reflection and rational scaling

The independent tests strengthen implementation confidence and test degeneracies. They do not turn finite evidence into a universal proof. The universal conclusions are accepted on the mathematical arguments reviewed in section 3.

## 6. Source scope, credit, and current-status check

The auditor freshly matched nine retained public source files against their recorded byte counts and SHA-256 hashes. `SOURCE_CHECKS.json` records only public metadata. The failed Gerken-variant retrieval has no source bytes and was not counted as a verified document.

- [Open Problem Garden](https://www.openproblemgarden.org/op/generalised_empty_hexagon_conjecture): exact all-ell statement and closed-hull exclusion inspected; the current page still presents it as a conjecture.
- [Abel et al.](https://arxiv.org/abs/0904.0262): strict/weak definitions, the perturbation lemma, and the concluding bounded-collinearity hexagon question inspected in the retained version. The packet's mechanism is properly presented without a novelty claim.
- [Barát et al.](https://arxiv.org/abs/1207.3633), [published article](https://doi.org/10.1137/130950422): definitions, Theorem 1, grid discussion, and open hexagon case inspected. The bound 328 ell^2 is for pentagons. The full pentagon proof was not rederived.
- [Heule and Scheucher](https://arxiv.org/abs/2403.00737): general-position hypothesis, Theorem 1, and lower-bound attribution inspected. H=30 and the Overmars witness remain cited dependencies. No full SAT computation or witness validation was performed.
- [Gerken publisher record](https://doi.org/10.1007/s00454-007-9018-x): correct DOI, article identity, general-position scope, and volume/pages verified. Full Gerken proof not reviewed. The earlier existence theorem also credits Nicolás, as the original problem and sharp-bound paper state.
- [Final formal-verification article](https://doi.org/10.4230/LIPIcs.ITP.2024.35): authoritative DOI .35 verified. [DOI .24](https://doi.org/10.4230/LIPIcs.ITP.2024.24) identifies a different Isabelle/HOL paper. Selected definitions and sections 6.1, 7, and 8 confirm the stated trust boundary: Lean's geometric reduction and an externally checked SAT computation are connected through the assumed CNF unsatisfiability assertion. The audit does not claim a local Lean build or end-to-end replay.

Fresh searches on the audit date used British/American exact-title variants, collinearities, bounded collinearity, solved/proof terms, and 2025–2026 terms. No inspected primary source resolved the all-ell target. This is a bounded current-source finding, not proof that no unindexed or inaccessible resolution exists. Search snippets from aggregators were not used as mathematical authorities.

## 7. Dataset/gate metadata boundary

`DATASET_CHECKS.json` records a fresh read-only hash and byte-count match for both public dataset files. The exact numeric target has one problem record, its code is OPG-59923, and that code is absent from the research-results join. These checks agree with the author metadata. No dataset body or record text was copied into the deliverable.

This establishes the stated dataset match and exact join absence only. The auditor did not repeat the author's entire repository/index/corpus-wide earlier-attempt search. Its broader negative result remains explicitly bounded inherited evidence, and is not needed to prove any elementary lemma.

## 8. Acceptance boundary

Accepted: lemma B; Propositions 1–5 with their stated hypotheses; the displayed counting inequalities and countermechanism examples; conservative source scope; five distinct substantive approaches; and the unresolved/exhausted disposition.

Not established: any finite threshold for every ell>=4; a fixed-ell unbounded counterexample; a new optimal bound; originality of the elementary lemmas; a complete proof reconstruction of the cited prior theorems; or a formal verification of the report.

No source body, private source, dataset contents, private personal data, or private coordination material belongs in this audit. At the time of the original mathematical audit, no publication or queue change had been performed. This public derivative preserves the accepted mathematical reasoning and supplies independently scoped public-only replay evidence. Original private-packet integrity is not certified by this publication.
