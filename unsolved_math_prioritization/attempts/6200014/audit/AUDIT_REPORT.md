# Independent adversarial audit: Kapovich Problem 14

## Verdict

**ACCEPT: full positive consequence of credited published results, in the exact flag/no-square source scope.** No mathematical correction is needed. A separate bibliographic addendum distinguishes the 2005 workshop from the source manuscript dated October 24, 2007.

Target: 6200014 / AMR-061-0014, catalog rank 808. Audited object: author archive of 14,171 bytes, SHA-256 `a7085468b08f93b8422c2764799a0712b806e2772292cbafe5514b38851fb5b9`; internal manifest SHA-256 `a06410f384f30791a067a97d639b0ec73eaf7df75334fcc4dd0cb896987b9b61`. The original archive remains unchanged.

This is an independent AI mathematical audit of an AI-assisted, unrefereed literature-resolution note. It is not human peer review, a new theorem, or a formal proof certificate. Acceptance means that the stated deduction is sound when the cited published results are imported with their actual hypotheses.

## Exact target and scope

Kapovich's Problem 14 refers to the construction immediately preceding it: a closed manifold equipped with a flag simplicial triangulation containing no induced four-cycle, and the associated right-angled Coxeter/Davis complex. Both restrictions belong to the question. The claim is independence up to homeomorphism of the boundary when the underlying closed manifold is unchanged up to homeomorphism. No equivariant homeomorphism or quasi-isometry classification is claimed. The original common-subdivision observation does not alone answer the topological question. [K]

The complete target record and associated report were independently recovered from the full corpus files, rather than accepted from a shortened excerpt. The prescribed default JSON serialization gives review SHA-256 `1ec3eb8a33545c474dae36d4b1ed4c07552f04d21401776d3e67d4c14c057dd6` and 3,282 bytes. Corpus hashes, byte counts, record counts, uniqueness and catalog identity all match. The earlier report's negative suggestion supplies no counterexample and is superseded by the verified deduction. Only identity metadata is included here.

## Load-bearing dependency audit

1. **High-dimensional exclusion.** PS Corollary 5.7(2), p. 466, concerns every triangulation of a manifold of dimension at least five, including non-PL triangulations. The preceding explanation explicitly uses generalized homology-sphere links. Lemma 5.1 transfers flag/no-square to links; Theorem 5.6 excludes generalized homology spheres of dimension at least four. Thus a vertex link obstructs any candidate in dimension at least five. This is not an obstruction for all pseudomanifolds, nor for every four-manifold. Corollary 5.3 gives the needed right-angled Coxeter hyperbolicity criterion. [PS]

2. **Automatic PL property.** DFL p. 797 explicitly states that a simplicial triangulation of a topological four-manifold is PL, and provides its link argument using the three-dimensional Poincaré theorem. Links of positive-dimensional simplices are low-dimensional homology spheres; vertex links are simply connected homology three-spheres. Lower-dimensional cases follow by the corresponding standard link facts. This proves that each permitted triangulation is PL. It does not assert uniqueness of the induced PL structure. [DFL]

3. **Boundary recognition and the TOP/PL distinction.** Świątkowski Theorem 2, p. 594, applies to a PL triangulation of a closed connected manifold and does not require the manifold to bound. The orientable output uses both opposite orientations; the nonorientable output uses the manifold itself. Definition 1.1 and Theorem 1.2 work with topological manifold families, and Definition 1.3 makes their trees independent of the chosen inverse sequence. Consequently, two different PL structures on the same topological four-manifold give the same required tree. A homeomorphism transports the pair of opposite orientations, possibly interchanging its members. The paper's separate cobordism hypothesis in Theorem 1 is not a hypothesis of Theorem 2. [S]

4. **Free products.** MS Theorem 4.1, checked in both the 2013 preprint and the accepted manuscript, requires infinite hyperbolic factors and corresponding homeomorphic boundaries. Those are exactly the requirements used for disconnected positive-dimensional manifolds. No equality of factor groups, chosen metrics, or quasi-isometry types is assumed. Iteration handles finitely many components. [MS]

## Adversarial edge-case review

- **Finite nerve and correct Coxeter nerve:** a finite flag complex is the nerve of the right-angled presentation because its simplices are exactly the cliques. Spherical special subgroups are those cliques. This identifies the input to the recognition theorem.
- **Dimensions at least five:** there are no instances under the required hypotheses. A vacuous case is not a claimed new triangulation obstruction.
- **Dimension four:** automatic PL is sufficient. The argument never invokes the false inference that all triangulations of a fixed topological four-manifold must induce equivalent PL structures. An assumed common subdivision would be an unnecessary strengthening.
- **Sphere nerves:** the author invokes the stated Theorem 2, whose formulation includes sphere nerves, rather than applying the paper's auxiliary singular-pseudomanifold theorem outside its setup. The theorem's orientable formula specializes appropriately. No extra nonsphere restriction is introduced.
- **Connected dimension one:** a simplicial circle is a cycle. Three vertices violate flagness; four violate no-square. For at least five vertices, the right-angled compact hyperbolic polygon reflection realization gives circle boundary. The elementary polygon construction is valid for every such length.
- **Disconnected positive dimension:** compactness and local connectedness give finitely many components. Each component nerve is a full subcomplex, so it retains both combinatorial restrictions. It is not a simplex. Flagness then forces a pair of nonadjacent vertices, whose special subgroup is infinite dihedral; hence its Coxeter group is infinite. Disjoint nerve components give free-product factors. The homeomorphism pairs components, and the checked free-product theorem applies inductively.
- **Dimension zero and the empty case:** a finite discrete space has no alternative simplicial triangulation. Its Coxeter presentation is determined by its number of points. This avoids applying an infinite-factor or positive-dimensional tree theorem to a finite group. The empty nerve is also uniquely determined.
- **Boundary conventions:** the no-square condition ensures hyperbolicity. The visual and Gromov boundaries are identified in S Remark 5.4, so passage to the free-product boundary theorem is legitimate.
- **No-square is global:** replacing it by local flagness, allowing arbitrary subdivisions, or extending the conclusion to unrelated CAT(0) boundaries would change the question. The author makes none of those extensions.

These checks leave no unsupported step equivalent to the target question. The remaining dependencies are the identified published theorems and standard elementary Coxeter/topological facts.

## Replay and adversarial computation

The author archive and manifest match their separately supplied digest anchors. Extraction checks exact names, duplicate entries and symlink encodings before execution. The author verifier passes normally, under `-O`, and from a relocated directory with unrelated working directory.

For each interpreter mode, fourteen mutations are rejected: missing proof; same-length changed proof; extra file; symlink; duplicate manifest key; wrong byte count; traversal entry; removal of no-square; removal of flagness; illicit extra PL assumption; changed problem identity; false recorded control output; broken mathematical control; and a false all-pass field. For semantic mutations, the affected manifest entry is recomputed, so rejection goes beyond a stale checksum. There are 28 recorded rejections plus two clean passes, reproduced by normal and optimized runs of the independent runner.

An independent cyclic-order oracle checks the author's square detector and dimension-one flag test on all **1,100 labeled graphs with zero through five vertices**. A separately constructed icosahedral graph has 12 vertices, 30 edges, 20 clique triangles, no four-clique, no induced square, and twelve pentagonal vertex links. This supplies a nontrivial admissible two-dimensional control. A square with a diagonal is correctly distinguished from an induced square.

Finite controls test combinatorial bookkeeping and verifier behavior. They do not prove the imported infinite-dimensional inverse-limit or manifold-recognition theorems. The author's own explicit limitation is appropriate.

## Repository state and publication boundary

Read-only live checks on October 5, 2026 found the target still queued at 0/5 in the main queue, blob `09860d79fef533fcf0eef0256f3f61b47926554c`. Identifier/code searches, exact target PR searches, a Kleinian PR search, commit search and inspection of 827 branch refs produced no substantive prior target artifact. These are bounded, nonexhaustive searches; search absence is not proof of complete historical absence. No repository mutation, publication, or outside communication occurred in this audit.

The archive contains only authored audit text, a bibliographic addendum, code, results and public verification metadata. It excludes source PDFs, source-text extracts, screenshots, corpus contents and private coordination material.

## Sources

[K] Misha Kapovich, *Problems on boundaries of groups and Kleinian groups*, manuscript dated October 24, 2007, based on the 2005 AIM workshop; Problem 14 and preceding paragraph, p. 5. https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

[PS] Piotr Przytycki and Jacek Świątkowski, *Flag-no-square triangulations and Gromov boundaries in dimension 3*, Groups, Geometry, and Dynamics 3 (2009), 453–468; Lemma 5.1, Corollary 5.3, Theorem 5.6, Corollary 5.7. https://doi.org/10.4171/GGD/66

[DFL] Michael W. Davis, Jim Fowler and Jean-François Lafont, *Aspherical manifolds that cannot be triangulated*, Algebraic & Geometric Topology 14 (2014), 795–803; p. 797. https://doi.org/10.2140/agt.2014.14.795

[S] Jacek Świątkowski, *Trees of manifolds as boundaries of spaces and groups*, Geometry & Topology 24 (2020), 593–622; Theorem 2, Definitions 1.1 and 1.3, Theorem 1.2, Remark 5.4. https://doi.org/10.2140/gt.2020.24.593

[MS] Alexandre Martin and Jacek Świątkowski, *Infinitely-ended hyperbolic groups with homeomorphic Gromov boundaries*, Journal of Group Theory 18 (2015), 273–289; Theorem 4.1. https://doi.org/10.1515/jgth-2014-0043. Accepted manuscript: https://pure.hw.ac.uk/ws/portalfiles/portal/15846713/HomeoBoundaries.pdf. The publisher gives 273–289; the repository cover's 273–290 is a metadata discrepancy, not a theorem difference.
