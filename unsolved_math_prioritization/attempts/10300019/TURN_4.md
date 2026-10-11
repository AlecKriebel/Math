# Author turn 4: a compact normal-gluing certificate allowing reconnection

**Conditional construction, not a general existence theorem. Original question unresolved.** 2026-10-01.

Turn3's faithful-union test was too restrictive for Haken exchanges. This turn instead allows the local pieces of the two input laminations to be reconnected. It gives a sufficient certificate for a normal output, and makes explicit the remaining geometric choices. It does not replace those choices by finite disk counts.

## 1. The data to be certified

Work with a fixed finite triangulation of a compact 3-manifold and compatible normal disk types. For each tetrahedron and each occurring type, take the two compact ordered transverse parameter spaces for the input disk families. Assume we are supplied with the following additional data.

(A) A compact ordered parameter space K for each output disk family, embedded as a closed subset of a real interval, together with continuous order embeddings of the two corresponding input parameter spaces as disjoint subsets whose union is K. The output family is a continuous embedded normal product family of disks in the tetrahedron, parametrized by K. All output families in the tetrahedron are pairwise disjoint. This explicitly includes geometric realizability, not merely an abstract order.

(B) Across each identified triangular face, the outgoing normal-arc families have a prescribed homeomorphism respecting their normal-arc types and their transverse order (with the fixed orientation sign). After the supplied normal face-collar identifications, their actual arcs coincide under the original triangulation's face gluing. These identifications are coherent on edge collars. They may switch which input color a disk continues into. Thus original whole leaves and labels need not survive.

(C) Around every interior edge, composing the finitely many corner identifications through the incident tetrahedra returns every transverse parameter to itself, and the entire collar atlas there is a product of a meridional disk with a compact interval subset. At a boundary edge the corresponding half-disk product condition holds. No output meets a triangulation vertex. This is an explicit local product and no-branching check, not an inference from equality of cardinalities. It also rules out a nontrivial parameter return masquerading as a transverse lamination at the edge.

The face/corner maps are maps of compact topological spaces and are continuous. A bijection of underlying sets is insufficient. These conditions are deliberately stronger than the currently unproved assertion that such data exist for every compatible input pair.

## 2. Sufficiency theorem

**If a certificate(A)–(C) is given, the prescribed local pieces glue to a closed normal lamination in the original triangulated manifold.** The construction uses no transverse measure. It may reconnect leaves at faces and need not preserve essentiality.

Proof. The local disk families are compact. There are finitely many tetrahedra and finitely many types, so their images in the compact manifold have compact union, hence closed union. Condition(B) identifies exactly the prescribed boundary arcs along each face, with their product neighborhoods agreeing. Thus each interior disk point has a disk-times-transversal chart by(A), and each interior face point has such a chart by gluing two half-disk charts through the prescribed transversal homeomorphism. The order/normal-face matching prevents intersections of distinct sheets at that face.

At an edge, local normal disks contribute finitely many corner charts. Condition(C) is exactly the check that these cyclic corner charts assemble to one meridional disk-times-transversal chart instead of an extra branch or a nontrivial return. The boundary case is the same with a half-disk. Vertices do not occur. These charts cover the closed union and define compatible two-dimensional leaves. Consequently it is a lamination, and its intersection with each tetrahedron is the supplied family of compact normal disks. It is therefore normal to the fixed triangulation. No convergence of infinitely many separate surgeries or finite-test compactness argument has been used.

Conversely, an already constructed normal lamination with the specified continuous local input-piece embeddings supplies such a certificate by restricting its genuine charts. This converse is only about outputs admitting that piecewise description. It is not a claim that every possible interpretation of an unmeasured Haken sum preserves exactly those local pieces.

## 3. Relation to finite Haken sum and holonomy

For finite normal surfaces the parameter spaces are finite, continuous order maps are just order maps, and the classical regular-exchange construction supplies the compatible local disk/arc families. The resulting output has the sum of the normal coordinate vectors, hence is the classical Haken sum up to normal isotopy. This familiar specialization is credited, not a new classification.

For infinite transverse sets, condition(B) retains the actual gluing homeomorphisms. Following them along leafwise paths defines the output holonomy. Its relations are automatically satisfied once the full atlas is consistent; choosing sector-wise maps independently need not make it so. An edge-return test only handles the local meridians; it is not a declaration that all other holonomy has become trivial. Global leaf holonomy may remain nontrivial, as is permitted for laminations.

The certificate permits color changes at face arcs, so it avoids the faithful-union obstruction exhibited by the intersecting torus pair. It does not require or assert that the unmeasured result is independent of the certificate. With finitely many disks uniqueness comes from normal coordinates; that finite uniqueness theorem has not been extended here to general compact transversals.

## 4. Exact remaining gate

This is a verification/realization theorem for **given compact continuous reconnection data**, not a procedure obtaining those data from every input pair. In particular:

- Compatible quadrilateral types do not by themselves supply the transverse embeddings, all face identifications, or the edge product charts
- Passing every finite shuffle test does not establish(A) or continuity in(B), by the split-interval countercontrol
- Essentiality or incompressibility of the output requires separate hypotheses and is not claimed
- No specified monotone-equivalence relation or topology makes these choices automatically unique or continuous

Thus the main source problem has been reduced to a genuinely geometric compatibility choice only in this restricted piecewise model, and that existence/uniqueness step remains open here. It would be circular to announce a full solution by assuming the certificate. The useful conclusion is the precise scope in which a measure-free, possibly leaf-reconnecting normal construction is already justified.

Substantive author turns:4/5. Estimated completion30%. Original unresolved; no novelty claim.
