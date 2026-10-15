# Independent topology review — PR 468 / problem 30000689

Reviewed frozen head: `8527ccdba064bca52035fc6c8d96caa750ac9c00`.

Review inputs: `source_snapshot/unsolved_math_prioritization/attempts/30000689/release/PROOF.md` and the adjacent `EXPLANATORY_ADDENDUM.md`. The primary-source locators are in `SOURCE_LOCATORS.md`.

Decision: **PASS for the assigned topological argument, with the frozen proof and explanatory addendum read together.** I found no missing hypothesis or unsupported topological implication in Sections 3–4. The argument gives the dimension-four mod-2 obstruction, including a source carrying a potentially exotic PL structure, and correctly converts a topological embedding to existence of a PL embedding for every `d≥3`, including `d=3`.

This is a bounded verification of those topology dependencies. It does not independently certify the algebraic results and ambient-extension theorem used in Sections 1–2, the numerical artifacts, novelty, or priority. Thus the full conclusion for `d≥3` is conditional in this review on the separately claimed non-PL-embeddability result of Section 2. The dimension-four obstruction argument is itself verified here. The first decision was recorded before reading any earlier audit or parent assessment; none was needed or consulted subsequently.

## 1. Exact target and falsification criteria

The target is that, for a finite simplicial triangulation `S` of the topological sphere `S^{2d}` and a missing `d`-face `M` on its actual vertices, the augmented complex `S^{(d)}∪{M}` has no arbitrary topological embedding in `S^{2d}`. A missing face is a nonface all of whose proper subsets are faces. For `d=2`, the proof establishes the stronger checkable statement `o^4_{Z2}(S^{(2)}∪{M})≠0`.

The main attempted falsifications were: a noncombinatorial four-dimensional source; a nonstandard complementary ball silently used as standard; missing induced-support or removed-star hypotheses; a disk forced to be embedded; relative approximation forced to fix a wild target map; a cone-complement calculation in the wrong complex; the new triangle appearing inside its own replacement chains; an absent move case; a local linking computation using a global PL parametrization; a Pachner sequence crossing PL classes; or an existence bound excluding `d=3`. None survives the checks below.

## 2. Every triangulated topological 4-manifold supplies the required PL manifold

Local homology gives sphere homology for each face link. This alone would be inadequate in higher dimensions, so the dimension restriction matters. In dimension four, the positive-dimensional face links have dimensions at most two. Starting with zero-dimensional links, the link conditions force closed one- and two-dimensional manifolds; their integral sphere homology identifies them respectively with a circle and a 2-sphere. The vertex link is consequently a closed triangulated 3-manifold with the integral homology of `S^3`.

Here is an explicit check of the extra fundamental-group input at a vertex `a`. A sufficiently small conical neighborhood of `a` is contained in a coordinate 4-ball `U`, and `U` can itself be chosen inside the open star of `a`. Radial placement puts any loop from the link in that small conical neighborhood. The punctured coordinate ball `U\{a}` is simply connected. A nullhomotopy there lies in the punctured open star; its radial retraction is a nullhomotopy in the link. Thus the link is simply connected. Three-dimensional Poincaré identifies it as a topological `S^3`, and the three-dimensional PL uniqueness theorem identifies its triangulation as a PL sphere. This is also the precise low-dimensional fact recorded by Davis–Fowler–Lafont on printed p. 797.

This yields a combinatorial 4-manifold. It does not identify its global PL structure with that of the standard PL 4-sphere. No four-dimensional Poincaré or Schoenflies assertion has entered.

## 3. The complement lemma needs exactly contractibility

Let `B=α*∂β` be the closed ball of a legal bistellar move in a combinatorial 4-manifold `Q` whose underlying space is `S^4`. Its common replacement boundary is `∂α*∂β`.

The boundary is locally flat in `Q`. At a boundary vertex its link is a PL 2-sphere sitting in a PL 3-sphere. Three-dimensional PL Schoenflies supplies the standard local pair; the link checks at higher-dimensional strata reduce to lower-dimensional sphere pairs. This is a local, three-dimensional use of Schoenflies, not the unresolved assertion that an arbitrary PL 3-sphere bounds standard PL 4-balls on both sides. Hence the closure `C=Q\int(B)` is a compact PL 4-manifold with boundary `S^3`, with collars.

Collars make `Q=B∪C` a legitimate van Kampen decomposition. The intersection is connected and simply connected; `B` and `Q` are simply connected. Connectedness of `C` follows also from the reduced `H_0` Mayer–Vietoris segment. It follows that `π_1(C)=0`.

For homology, the relative fundamental-class map

`H_4(Q;Z) → H_4(Q,C;Z) ≅ H_4(B,∂B;Z)`

has degree `±1`. The long exact sequence of the pair then gives zero reduced homology of `C` (including `H_3(C)`, where omitting the degree check would leave a gap). Since `C` is a finite CW complex, the least-degree nonzero homotopy group, if one existed, would contradict Hurewicz and acyclicity. All its homotopy groups vanish, and Whitehead gives contractibility.

Nothing later needs `C` PL homeomorphic to a standard 4-ball. In fact, this lemma can be used without deciding that stronger assertion.

## 4. Transfer for a common missing triangle: all hypotheses checked

Set `K=Q^{(2)}∪{M}`, `L=(Q')^{(2)}∪{M}`, `T=(α*∂β)^{(2)}`, and `T'=(∂α*β)^{(2)}`, where `M` is missing in both `Q` and `Q'`. The structural setup at the start of Nevo–Wagner Section 5, before its numbered hypotheses, must be checked as well as Theorem 5.3's `(I.a)`–`(II.b)`.

**Induced support.** The old full ball is induced on its old move vertices: `β` is absent, and every vertex subset not containing all of `β` is already a face of `α*∂β`. The same assertion holds after restricting to the 2-skeleton. If a common missing triangle were inside those vertices, minimal nonface status would force it to equal `β`; that simplex becomes a face in the replacement. This is impossible. For a move introducing a new vertex, a common triangle cannot involve that vertex at all. Thus adjoining `M` does not add a face inside the old induced support.

**Removed star.** All old faces containing `α` are in the move support by legality of the bistellar move. The added triangle cannot contain `α`: if `α` were a proper subset of `M`, its disappearance would contradict that every proper subset of `M` is a face of `Q'`; equality would contradict that `M` was missing in `Q`. Thus the augmentation does not introduce an extra simplex in the removed star. The skeleton really changes by the move stipulated in Theorem 5.3.

**The map and support intersection conditions.** Every proper face of `M` survives the move, so `|∂M|` lies in `C`. By contractibility of `C`, its prescribed boundary map extends to a continuous disk. A collar pushes the disk interior into `int(C)` while fixing its boundary. Relative PL general position in this PL 4-manifold makes its interior avoid the old 1-skeleton, since `2+1<4`. Self-intersections of this disk are permissible: they are not intersections of disjoint domain simplices, and the obstruction representative does not require an embedded added triangle.

Choose a point `x` in `int(B)` off the 2-skeleton and identify `Q\{x}` topologically with `R^4`. Map the old skeleton by this inclusion and the added triangle by the disk. Any vertex-disjoint pair of triangles with one triangle in `T` has disjoint images: the disk interior is outside the ball and its boundary intersections with the skeleton occur only along actual common boundary faces. The old skeleton itself is embedded. This establishes `(I.a)`.

The two standard move balls admit a homeomorphism `B'→B` fixed on their common boundary. Use it on the new support and keep the old map elsewhere. The new map agrees on `K∩L`, and exactly the same separation argument gives `(I.b)`.

There is no approximation problem caused by a potentially non-PL identification `Q\{x}→R^4`. The two continuous maps agree on their common complex, hence define one continuous map on the finite abstract union `K∪L`. Make a sufficiently close PL general-position approximation on that union. Restrictions still agree. The finitely many forbidden vertex-disjoint face pairs were compact and disjoint, and their positive separation is preserved by a sufficiently close approximation. One need not keep the potentially wild target map fixed. This validates the addendum's simultaneous-approximation assertion.

**Outside vertex.** An induced ball cannot comprise a closed sphere on all its vertices: if there were no outside vertex, inducedness would make the whole complex equal that ball. Consequently an outside vertex exists before and after the move. The `p=0` and `q=0` moves remove or introduce a support vertex, respectively, but their outside vertex sets still coincide. This is `(II.a)`.

**Exact homology condition.** For a common support face `ρ`, delete `W=T_0\ρ`. The old induced complex on `W` has the form

`Q[W]=(α\ρ) * (∂β\ρ)`.

The factor `α\ρ` is a nonempty simplex because `ρ` is on the common boundary. This makes `Q[W]` a nonempty cone. Alexander duality in the actual topological `S^4` makes its complement acyclic. The standard induced-complement deformation retraction can be checked directly: retain only barycentric coordinates on vertices outside `W` and normalize their positive sum to one. The homotopy stays in the complement of `Q[W]`. Thus `Q-W` is acyclic.

The 2-skeleton of `Q-W` has the same `H_0,H_1` as `Q-W`; cells of dimension at least three cannot change these groups. In `K-W`, the possible additional triangle already has all its edges present, and attaching it can only quotient `H_1`, while preserving `H_0`. Therefore `H̃_0(K-W;Z2)=H̃_1(K-W;Z2)=0`, exactly `(II.b)` when `d=2`. For an edge used in the cone construction outside the support, intersect it with the support first; the deleted vertex set is the same one. Thus the condition really supplies every required cone, not just cones on edges entirely in the ball.

All structural and numbered hypotheses have now been established using only the combinatorial manifold structure and the topological sphere. Nevo–Wagner Theorem 5.3 transfers the nonzero obstruction. Its cycle manipulation does not demand a global PL parametrization of `Q` by the standard sphere.

## 5. Newly missing triangles and the old-skeleton witness

The elementary face-change classification is exhaustive. If a triangle was an old face and becomes missing, it must be exactly the removed `α`, since all its proper faces survive; hence `p=q=2`. If it was not an old missing triangle, one of its edges must be new. New faces contain `β`. Minimality forces `q=1,p=3`, with the triangle `M=v*β` and `v` outside all move vertices. A triangle on the support vertices is already a new face. The vertex-insertion `q=0` move cannot create a missing triangle: an outside vertex cannot be joined to the new vertex. The edge-removal `p=1` move cannot create one because the removed edge would be a missing proper face. The vertex-removal case likewise causes no omitted triangle case.

For `p=q=2`, the old missing triangle is `β`. The old skeleton plus `β` and new skeleton plus `α` are literally the same abstract augmented complex. The induction hypothesis applies directly.

For `p=3,q=1`, it is essential to construct cones in the **old unaugmented** `Q^{(2)}`. The same cone-complement argument just proved gives vanishing `H̃_0,H̃_1` there. The old skeleton is a subcomplex of the new skeleton, so the cone chains survive. No old missing triangle has been assumed.

Here is a direct chain check of the witness, independently of a mere appeal to its existence. Put `U=α_0∪β_0` (six vertices) and `V={v}∪U` (seven). Every triangle on `U` is in the new support. Every edge on `U` other than `β` is in the old skeleton. Send each formal support triangle to itself, send `v*β` to `M`, and send another formal triangle `v*e` to its old-skeleton homological cone. Also send a formal edge `v*a` to the cone on the vertex `a`. The cone boundary formula makes this a chain map through degree two. For the exceptional triangle `M`, its boundary formula still holds: both edges from `v` to the endpoints of `β` exist, are old edges, and are precisely the prescribed vertex cones.

Apply this replacement to the ordinary mod-2 deleted-product 4-cycle consisting of all disjoint triangle pairs on `V`. At most one triangle in a pair contains `v`. Its cone chain introduces no support vertex outside the original edge, while the other triangle lies entirely in `U`. Thus all replacement pairs remain vertex-disjoint, and the chain map also respects the boundary pairs. The resulting chain is a cycle.

No cone chain contains `M`, because each cone lies in the old unaugmented skeleton and `M` was absent there. The only occurrence of `M` is its expressly assigned formal triangle. Its partner triangles are the four triples on `V\M=α_0`, with no replacements. Therefore the partner chain is exactly `∂α`.

Choose an outside point off the new ball and the new 2-skeleton, and identify the punctured topological sphere with `R^4`. The unaugmented skeleton is embedded. The loop `∂M` consists of the support edge `β` and two exterior edges to `v`. In the explicit geometric ball `∂α*β`, place the tetrahedron `α` and interval `β` in complementary 3- and 1-dimensional subspaces, with one transverse interior intersection. The spanning tetrahedron lies inside this ball. Pull it back to the actual ball. The exterior portion of `∂M` is disjoint from the ball, so the spanning 3-disk meets the loop exactly once modulo two. This proves linking number one for `∂M` and `∂α`.

The intersection/linking boundary relation then gives intersection number one for any general-position filling of `M` against `∂α`. Every other pair in the witness lies in the embedded unaugmented skeleton and contributes zero. Thus the obstruction pairs to one with this cycle. This computation uses a standard local bistellar ball and a topological ambient homeomorphism; it uses neither a globally standard PL sphere nor a standard complementary PL ball. The corresponding obstruction is a necessary obstruction to arbitrary topological embedding, as its deleted-product definition confirms.

## 6. Flag base and Pachner sequence stay in the correct PL class

The order-complex description of `sd(S)` makes it flag: pairwise adjacency of its vertices means pairwise comparability of faces of `S`, and hence they form a chain. In particular, it has no missing triangles. The desired property is therefore vacuous at this base.

The identity subdivision map is a PL homeomorphism between `sd(S)` and `S` for the PL structure supplied by this very triangulation. Both are closed combinatorial 4-manifolds. Lickorish Theorem 5.9 gives a finite bistellar sequence, allowing simplicial isomorphisms, within their PL homeomorphism class. Relabeling preserves the property; each move preserves the underlying topological `S^4`. The transfer result applies at every step. No comparison to the standard PL sphere is required.

This establishes `o^4_{Z2}(S^{(2)}∪{M})≠0` for every missing triangle of every finite triangulation of the topological 4-sphere.

## 7. Weber's original theorem: the equality case is included

Weber Section 1 defines a semilinear map to be simplicial after subdivision, which is the PL category. His Theorem 1 on printed p. 2 is an **existence** result for a finite `n`-polyhedron: an equivariant continuous map from its deleted product to `S^{m-1}` gives a semilinear embedding in `R^m` provided `2m≥3(n+1)`.

A topological embedding of the finite `d`-complex into `S^{2d}` cannot fill the sphere, by invariance of topological dimension. Removing an omitted point supplies an embedding into `R^{2d}`. Its normalized difference map on the full ordered deleted product is continuous and equivariant, so it meets the actual input of Weber's theorem.

Substitution `n=d,m=2d` gives `4d≥3d+3`, equivalent to `d≥3`. At `d=3`, both sides are 12; the original non-strict inequality includes this case. No classification or isotopy statement, and no claim that the supplied topological embedding is itself tame or PL, is required. A PL embedding in `R^{2d}` also yields one in a standard PL sphere: rescale its compact image into a PL coordinate chart. This is precisely the contradiction to the separately proved Section 2 conclusion.

## 8. Audit disposition

Strongest result independently verified here: the dimension-four obstruction proof is valid with the stated addendum; the topology-to-PL existence reduction is valid for all `d≥3`, including the first boundary case. No topological blocker remains in this assigned scope.

A useful editorial improvement, not a proof repair, would be to incorporate the addendum's induced-support, removed-star, simultaneous-map, and old-unaugmented-cone sentences into Section 4.3. They are essential audit landmarks, although the present frozen proof plus addendum already supplies them.

No additional proof search, alternative target, priority search, outreach, publication, release, commit, push, or PR action was performed by this verifier.
