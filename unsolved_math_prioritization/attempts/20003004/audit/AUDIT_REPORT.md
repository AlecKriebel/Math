# Independent audit: higher digital homotopy

**Problem:** 20003004 / AIM-TOPOLOGY-0092, rank 517  
**Frozen author packet:** manifest dated 2026-10-03 18:32:14 UTC  
**Audit date:** 2026-10-03 UTC  
**Disposition:** **PASS, full stated strong-product scope; resolution by prior theory.**  
**Novel discovery:** No.

## Decision

The frozen packet correctly constructs the groups using finite boxes and identifies them, naturally as groups, with

\[
D_n(X,b)\cong \pi_n(|\operatorname{Cl}(X)|,b),\qquad n\geq1.
\]

Here the graph is reflexive and undirected, every grid product and homotopy product is categorical/strong, every spatial boundary is fixed at the basepoint, and the equivalence relation permits basepoint trivial extensions before a finite strong homotopy. Those qualifications are essential. They agree with the successful 2024 digital second-group construction. The six-point octahedral graph therefore has \(D_2\cong\mathbb Z\).

The proof is an application of Grandis's established intrinsic simplicial homotopy theory, with a valid finite-box/finite-support identification. It is not an inference from finite computations. The classification must remain “already-known theory under the explicit strong-product convention,” not a novel discovery, not a resolution for every theory called digital homotopy, and not a proof of additional relative-group or exact-sequence claims.

No mathematical defect requiring HOLD was found. The source-status nuance in Section 8 must be preserved in any summary: the 2026 paper's unknown-comparison remark cannot simply be dismissed as using some different digital second group.

## 1. Original target and source provenance

The pinned original-statement field was inspected independently of the prior generated research report. It asks for higher digital homotopy groups and an integer-valued second group for the six-vertex digital sphere. The associated remark asks about Tucker's lemma. No product convention, relative theory, exact sequence, or algorithmic complexity requirement appears in that original text.

The live [AIM problem-list page](http://aimpl.org/combhomotop/1/) remained unavailable during this audit. Thus this audit does not claim fresh live verification of its exact wording. The primary [AIM workshop report](https://aimath.org/pastworkshops/combhomotoprep.pdf), pp. 1–2, independently confirms boundary-constant rectangular representatives, the vertices \(\pm e_i\), diagonal adjacency, and the computed second group. The [official workshop page](https://aimath.org/pastworkshops/combhomotop.html) links that report and the digital second-group paper. Together these support the substantive target and the adopted convention. The prior generated research report was not used as mathematical authority.

Fresh downloads of the Grandis, digital-second-group, and face-group arXiv PDFs were byte-identical to the supplied local source PDFs. Their SHA-256 values are recorded in `source_verification.json`. The source PDFs and full texts are outside this sanitized audit directory and outside the frozen public packet.

## 2. Exact product and simplicial dictionary

For a reflexive undirected graph \(X\), its clique complex contains every finite pairwise-adjacent vertex set. For the interval graph \(I_m\), a set is a clique exactly when its coordinates lie in a consecutive pair (or a singleton). Consequently a finite subset of

\[
Q=I_{m_1}\times\cdots\times I_{m_n}
\]

is a clique exactly when every coordinate projection is a simplex of its interval complex. This is precisely the categorical product in the category of abstract simplicial complexes used by Grandis. In particular, the vertices of a unit \(n\)-cube span a \((2^n-1)\)-simplex. No planar triangulation or ordinary topological product is silently substituted for that complex.

A vertex map \(Q\to X\) preserves graph adjacency exactly when it is a simplicial map \(\operatorname{Cl}(Q)\to\operatorname{Cl}(X)\). One-step strong homotopy of two such maps is equivalent to contiguity:

* Strong homotopy supplies all cross pairs \(f(u)\sim g(v)\) for \(u\sim v\), as well as the within-slice pairs.
* Therefore the union of the two images of any domain clique is a target clique.
* Conversely apply contiguity to every two-vertex clique, including singleton cases for the reflexive condition.

The flag target assumption is doing real work. Pairwise adjacency does not in general certify a simplex in an arbitrary nonflag target, but every target to which the packet applies this equivalence is \(\operatorname{Cl}(X)\).

Fixed boundary vertices suffice. Whether a source describes the boundary as a union of simplicial faces or as the set of boundary vertices causes no discrepancy for maps required to be constant there: every simplex all of whose vertices have that prescribed value maps constantly.

## 3. Collar and subdivision audit

Write \(\alpha_j(i)=i\) for \(i\leq j\), and \(\alpha_j(i)=i-1\) otherwise, from \(I_{m+1}\) to \(I_m\). Each map is nondecreasing and has consecutive increments zero or one. For successive indices, \(\alpha_j\) and \(\alpha_{j+1}\) differ only at \(j+1\). The neighboring values there are \(j\) and \(j+1\). Thus

\[
|u-v|\leq1\quad\Longrightarrow\quad
|\alpha_j(u)-\alpha_{j+1}(v)|\leq1.
\]

Precomposition in one coordinate therefore gives a strong homotopy in every dimension, leaving the other coordinate adjacency tests unchanged. All intermediate maps preserve the two ends of that coordinate as a map of pairs; hence a boundary-constant representative remains boundary-constant throughout.

At one end of the chain the extra hyperplane is upper padding; at the other it is lower padding. This proves translation through a basepoint collar, with no unsupported assumption that a direct one-step translation is strong. Iterating the same construction also shows that repetition of an arbitrary coordinate hyperplane is equivalent to upper trivial extension. Uniform rectangular subdivisions, being finite strings of such repetitions, do not add a stronger equivalence relation to the packet.

For a local rectangular block, an adjacent vertex outside the block can only meet a vertex on its boundary. If that boundary is fixed at the basepoint, the local homotopy glues to an unchanged continuous outside map. This verifies the local sliding assertion used for group operations. The checker includes actual cross-condition tests along the collar chains, rather than testing only the continuity of their endpoints.

## 4. Finite boxes versus Grandis's loop objects

The relevant source is [Grandis's preprint](https://arxiv.org/abs/math/0009166), §§1.2–1.6, 2.1–2.6, 3.1 and 6.2–6.6; its [published version](https://doi.org/10.1023/A:1014326730784) appeared in 2002. Theorem and section numbering here is pinned to the checked preprint. The journal metadata were separately verified; the journal full text was not needed.

The definitions impose exactly the following conditions:

1. Abstract simplicial complexes have finite simplices, with all vertices present. A graph's tolerance complex is its clique complex, not merely its one-skeleton.
2. The integral line uses consecutive integers; its categorical powers have unit cubes as generating simplices.
3. A path has a finite support interval and is constant on both tails. The based loop object requires both tail values to be the basepoint.
4. Iteration yields a uniformly finite rectangular support and constant faces. The loop complex carries the induced internal-hom simplicial structure.
5. \(\pi_n\) is \(\pi_0\Omega^n\). Here connected component means a finite chain of links, not an arbitrary pointwise-finite homotopy on an infinite domain.
6. The comparison theorem assumes a pointed simplicial complex and its usual weak geometric realization. It does not require local finiteness, connectedness, a metric realization, or a special digital embedding. It is all-dimensional.

The finite-support description can also be checked without relying on terminology. In an iterated based loop, only finitely many outer-coordinate values are nonconstant lower-dimensional loops. Each has a finite inner support; a finite union has a common finite bound. This proves uniform finite support inductively. Conversely a based map supported in a finite rectangle curries to an iterated based loop. The internal-hom exponential law identifies a link between two such loops with the requirement that the union of their images of every elementary cube is a simplex.

The packet's comparison of equivalence relations is valid in both directions:

* **Well-defined:** Extend a finite boundary-constant map by the basepoint to \(\mathbb Z^n\). A unit cube meeting both the box and its complement has every vertex lying inside the box on a boundary face. Its image is constant. The same check works for every time slice and every adjacent-time pair. Upper trivial extensions yield the identical infinite map.
* **Surjective:** Choose a finite box containing a loop's support, add a constant collar, and translate to nonnegative coordinates. Restriction is a finite representative. The collar chains, extended by the basepoint, identify the original loop and its translate in \(\pi_0\Omega^n\).
* **Injective:** A path between two extended representatives is a finite list of finitely supported maps. Choose one rectangle containing all their supports, with a constant boundary collar. After a common integral translation, restricting the list gives one finite strong homotopy relative to the boundary. Its endpoints are padded translates of the original representatives. The collar lemma removes those changes.

The finiteness of the chain in the last step is crucial and explicitly satisfied. There is no uncontrolled passage from infinitely many individual support bounds to one finite bound.

## 5. Group operations, naturality, and realization

After equalizing transverse side lengths by trivial extension, concatenate two representatives in the first coordinate. Adjacent blocks meet only through their constant boundary faces, so continuity holds. The resulting infinite map is an admissible loop concatenation, up to a duplicate constant slice and a translation. Both are removed by the checked collar/delay relation.

Grandis's support-dependent concatenation descends to the connected components of the loop object. Its identity, reversal, associativity, and higher-dimensional interchange therefore give exactly the finite-box group operation: constant representative as identity; reversal in the concatenation coordinate as inverse; commutativity for \(n\geq2\). No set-level bijection is being promoted to a group isomorphism without checking its operation.

For \(n=2\), the 2024 diagonal two-block product can be moved to horizontal concatenation by sliding the second block down inside its own, disjoint vertical slab. Each local slide uses the collar chain and leaves the first block fixed. The common bounding rectangle remains boundary-constant. Thus its operation agrees with the operation in the packet. The independent checker verifies this slide on two nonzero-degree blocks using forty strong elementary steps.

Postcomposition by a based graph map respects every construction, so the identification is natural for based graph maps. The realization map uses multi-affine interpolation in the simplex spanned by each cube's labels. Adjacent cube formulas agree on their faces. Strong homotopies give the same construction one dimension higher, and fixed spatial boundary labels give fixed realization boundaries. Grandis's Theorem 6.6 supplies the converse and the natural isomorphism. This does not assert that the realization of a categorical simplicial cube is literally a topological cube.

## 6. Independent degree-two source route

The checked [face-group preprint, version 2](https://arxiv.org/abs/2503.23651v2), Remark 2.1 and §§3–4, explicitly uses the clique complex of the strong rectangle, boundary-constant maps, relative contiguity chains, upper trivial extensions, and the same diagonal product. Hence its face group for \(\operatorname{Cl}(X)\) is definitionally the 2024 digital second group after the contiguity dictionary above. Theorem 8.1 compares that face group with ordinary \(\pi_2\) of realization. This is a genuinely independent degree-two route.

Its §9 announces the digital comparison and defers a separate proof. Its introduction acknowledges Grandis while describing a direct combinatorial correspondence as non-immediate. Those statements have not been silently upgraded into a published proof of the finite-box bridge; the bridge is verified in Sections 3–5 of this audit. The face-group reference is not needed for the all-dimensional conclusion.

## 7. Octahedral sphere and convention countercheck

For \(S=\{\pm e_1,\pm e_2,\pm e_3\}\), the stated \(c_2\) adjacency is exactly \(u\sim v\iff u\ne-v\); restricted \(c_3\) adjacency is identical. A simplex of its clique complex chooses at most one vertex from each antipodal pair. Its eight maximal triangles are the facets of the three-dimensional cross-polytope. Thus the realization is \(S^2\), giving \(D_2(S,-e_1)\cong\mathbb Z\), and more generally \(D_n(S,-e_1)\cong\pi_n(S^2)\). No claim that all these groups are integers is present.

This degree-two value was independently proved in [Lupton–Musin–Scoville–Staecker–Treviño-Marroquín (2024), Theorem 5.5](https://doi.org/10.1007/s10801-024-01352-9). The published theorem, its definitions, and its future-work discussion were checked. In particular the future-work discussion does not itself establish the all-dimensional comparison.

For the weaker box homotopy, the displayed intermediate map sends \(+1\) to \(+2\) and every other vertex to \(-1\). Its two-value image is adjacent. Both its pointwise adjacency with the identity and its pointwise adjacency with the constant map hold. It fixes \(-1\), so the claimed based box contraction is valid. The indicated cross pair fails strong continuity. Moreover the intersection of the neighborhoods of all vertices adjacent to \(v\) is \(\{v\}\), proving the identity has no other strong neighbor. These are compatible facts because the two homotopy products differ.

The Tucker observation is a correct limited non-extension statement: an odd boundary labeling of the specified triangulated three-ball by three opposite label pairs must have a complementary edge; that edge cannot map into the octahedral adjacency graph. This supplies the requested connection without claiming equivalence with the entire higher-group theory.

## 8. The June 2026 comparison warning

The [Milićević–Scoville paper](https://doi.org/10.1007/s41468-026-00246-y), published June 29, 2026, was inspected at Example 2, §4, and Theorem 24. It uses the continuous topological interval in pseudotopological homotopy and proves a realization comparison for finite digraphs/closure spaces. Example 2 explicitly describes comparison with the cited 2024 digital groups as unknown.

That is genuine contrary **literature-status evidence**; it must remain visible. It does not constitute a mathematical counterexample to the independently checked bridge. Although its ambient definition differs, the digital second group discussed there is the same relevant 2024 convention. Therefore “a different convention” alone is not a sufficient reconciliation. The justified conclusion here is narrower and more precise: the finite-box groups specified in the frozen packet agree with Grandis's intrinsic groups by the explicit argument, and hence with clique realization. This is a consequence of prior theory, not a claim that the 2026 authors stated or proved the bridge, and not a global priority claim.

## 9. Controls, freeze, and sanitization

All seven frozen author files matched their recorded SHA-256 hashes before and after the audit. The author checker was run from a temporary copy, so its output-writing behavior could not modify the frozen packet. Its JSON output exactly matched the frozen result.

`check_independent_controls.py` is an independently written, standard-library-only, read-only control script. It prints deterministic JSON. It checks:

* 1,057 based octahedral endomorphisms, the unique strong identity neighbor, the based box contraction, and the face vector \((6,12,8,0)\).
* 534,600 elementary collar cross-conditions.
* The strong/contiguity equivalence on path, square, two-cell rectangle, and cube domains; the precise bounded counts are in `independent_control_results.json`.
* A degree-one finite strong-grid representative, reversal degree minus one, horizontal and diagonal product degree two, actual relative-boundary collar/sliding chains, and two uniform subdivisions.

These are supplemental falsification controls. They neither enumerate all homotopy classes nor replace the symbolic proof and source theorem.

This audit directory contains only the report, short metadata, original control code, and exact control output. It contains no full paper, source text, corpus excerpt, prior generated-report dump, or private coordination. No remote mutation or frozen author-file modification occurred.

## Publication classification

**PASS for the full exact scope in the frozen RESULT.json.** Retain attribution to Grandis for the established all-dimensional intrinsic theory and to the 2024 authors for the digital octahedral computation. Describe the finite-box bridge as the explicitly checked identification making that prior theory applicable. Preserve the strong-product qualification, the unavailable-live-original-page disclosure, and the 2026 literature-status warning. Do not promote this packet as a new mathematical discovery or a convention-independent digital-topology theorem.
