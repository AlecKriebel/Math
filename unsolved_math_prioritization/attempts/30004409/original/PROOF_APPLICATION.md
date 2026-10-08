# A single-edge obstruction to a literal Hopf-tree automorphism identification

## Result and status

Let H be the standard Hopf link in R^3, and let E(H) be the path component containing H in

    Emb(S^1 disjoint-union S^1, R^3) / Diff(S^1 disjoint-union S^1).

Thus a point remembers the embedded submanifold, not parametrisations, orientations, or component labels. Let K_2 be the tree with two vertices and one edge. Its right-angled Artin group is

    A(K_2) = <a,b | ab=ba> = Z^2.

The following is an application of established Hopf-link computations, not a claim of a newly discovered motion group:

**Proposition.** The group pi_1(E(H),H) is not isomorphic to any subgroup of Aut(A(K_2)). In particular the literal identification with a symmetric automorphism subgroup of the forest RAAG cannot hold for all the links described in the 2020 source.

This conclusion does not require selecting one of the conventions for “symmetric automorphism.” It only requires that an automorphism group in that phrase really be a subgroup of Aut(A(K_2)). An intended extension, a quotient of the motion group, or an altered definition of motion is a different statement.

## 1. Source and quantifier match

Rachael Boyd's contribution, joint with Corey Bregman, in Oberwolfach Report 8/2020 defines the smooth H-trivial link space on p.501. The quotient is by the full diffeomorphism group of the disjoint union of circles. On p.502 the contribution considers links associated to disjoint unions of trees and proposes an isomorphism between their motion groups and symmetric automorphisms of their RAAGs. That paragraph does not define the quoted terminology further or remove one-edge trees. The same page records the quaternion group for a single Hopf link.

The standard Hopf link is the example for K_2. Neither disconnected-forest conventions nor ambiguities in constructing more complicated links from pairwise linking numbers can remove this example. This application concerns R^3 throughout.

Primary source: https://ems.press/content/serial-article-files/46844, pp.501–502; DOI https://doi.org/10.4171/owr/2020/8.

## 2. Credited topological input

Boyd–Bregman, *The embedding space of a Hopf link*, arXiv:2504.21806v2, Definition 2.2, uses precisely E(H) above. Theorem A states

    E(H) ≃ S^3 / Q8,

so pi_1(E(H)) = Q8. Theorem B supplies the passage from round circles to all smooth embeddings. Section 4 describes the connected fourfold cover obtained by labelling and orienting the components with positive linking number; its model is SO(3). Simultaneous orientation reversal and component exchange generate its Klein-four deck group. Lifting the three half-turns through SU(2) → SO(3) gives {±1,±i,±j,±k}.

The smooth theorem is used as a credited theorem input here. Its full parametrised smoothing proof is not claimed to have been independently re-proved by the finite checks below. The group and cover calculations needed for this application were inspected in Sections 3–4. The source is a preprint, version 2 dated 18 August 2025; this packet does not assert journal acceptance.

Independent historical corroboration is Damiani–Kamada, *On the group of ring motions of an H-trivial link*, Topology and its Applications 264 (2019), 51–65, Theorem 6.6: the unordered round motion group has presentation

    <t,s | t^4=1, s^2=t^2, sts^(-1)=t^(-1)>.

That is Q8. This round result alone would not identify the smooth motion group; the explicit smooth input above is essential. The 2020 report also credits Goldsmith's earlier topological computation. The Goldsmith paper's bibliographic record was checked, but its full PDF was not successfully retrieved in this audit, so no fresh proof inspection of that paper is claimed.

Sources: https://arxiv.org/abs/2504.21806v2; https://arxiv.org/pdf/2504.21806v2; https://doi.org/10.1016/j.topol.2019.06.004; https://eprints.whiterose.ac.uk/id/eprint/148587/8/H_trivial_reviewed.pdf.

## 3. Why no automorphism-subgroup convention can fix the literal claim

Aut(Z^2) is GL_2(Z), which is a subgroup of GL_2(R). Suppose that Q8 embedded in GL_2(R). Average the Euclidean inner product over its eight matrices. The resulting positive-definite inner product is invariant, so a change of real basis conjugates the image into O(2).

If every image matrix has determinant +1, the image lies in SO(2), an abelian group. This contradicts the noncommutativity of Q8. Otherwise the determinant map onto {±1} has four elements with determinant −1. Every determinant −1 matrix in O(2) is a reflection, hence has order two. Faithfulness would then give four distinct involutions in Q8. But Q8 has exactly one nonidentity involution, −1; its other six nonidentity elements have order four. This is again a contradiction.

Thus Q8 has no faithful two-dimensional real representation and cannot be isomorphic to any subgroup of GL_2(Z). Applying the credited computation from Section 2 proves the proposition.

For comparison only, the usual signed symmetric convention sends each distinguished generator to a conjugate of a generator or its inverse. Since Z^2 is abelian, conjugation does nothing, and this group consists of the eight signed permutation matrices. It is the order-eight dihedral group, with five involutions, rather than Q8. The unsigned convention gives only the two permutation matrices; the pure conjugating convention is trivial. None of these choices is needed for the stronger preceding argument.

## 4. The Dahm map and its missing kernel

Choose orientations of H_1 and H_2 with linking number +1, and use positively oriented meridians a,b to identify the complement group with Z^2. A motion in E(H) extends to an ambient isotopy; it can be supported in a sufficiently large ball. A fixed point outside that ball gives the usual Dahm homomorphism

    D: pi_1(E(H)) → Aut(pi_1(R^3 minus H)) = GL_2(Z).

The image sends the two meridians to signed permutations of themselves. If the endpoint signs are epsilon_1 and epsilon_2, invariance of the oriented linking number under an ambient isotopy gives epsilon_1 epsilon_2=1, including when the components are exchanged. Therefore, writing P=[[0,1],[1,0]],

    image(D) is contained in V={I,-I,P,-P} ≅ C2 × C2.

All four matrices occur. Use the translated standard link with radius-one circles centred at (-1/2,0,0) in the xy-plane and (1/2,0,0) in the xz-plane. Rotation by pi about the x-axis preserves the two components and reverses both orientations, giving -I. Rotation by pi about the axis in the direction (0,1,1) through the origin exchanges the components and preserves their chosen normal orientations, giving P. Their composite gives -P. A common reversal of one reference orientation merely conjugates the description and changes none of these conclusions.

Consequently |image(D)|=4. Since the domain is Q8, its kernel has order two, hence is its centre {±1}. We obtain the exact sequence

    1 → C2 → Q8 → C2 × C2 → 1.

It is nonsplit: a splitting would embed a Klein-four group in Q8, which has only one involution. Geometrically the central element is the full-turn loop in the SO(3) model; it is invisible to the meridian action.

There is no hidden Aut-versus-Out repair in this example: Inn(Z^2)=1, so Out(Z^2)=Aut(Z^2). Changing complement basepoints changes an induced automorphism only by an inner automorphism and therefore changes nothing here. Changing the base configuration conjugates the motion-group identification, preserving the abstract obstruction and kernel.

The oriented-and-labelled component gives the double-cover kernel C2 rather than Q8; the labelled-but-unoriented component gives C4. These are different spaces, not the source quotient. The obstruction above uses the full source quotient throughout.

## 5. What the split-link theorem does and does not supply

Boyd–Bregman, *Embedding spaces of split links*, Advances in Mathematics 470 (2025), article 110235, Theorem A and Example 4.12, give for the split union of n unknots and m Hopf links the R^3 formula

    pi_1(E(H_{n,m})) =
    (FR(Z^{*n} * (Z^2)^{*m}) ⋊ ((C2)^n × (Q8)^m)) ⋊ (S_n × S_m).

Here FR is the subgroup generated by partial conjugations between distinct free factors; the exponents on free products denote repeated factors. Their order of indices is n unknots, then m Hopf links, opposite to the 2020 SH_{m,n} notation. At n=0,m=1 the free-product and permutation terms are trivial, leaving Q8. This agrees with the single-edge obstruction and retains the internal motion-group factor instead of replacing it by its Dahm image.

This formula covers H-trivial split links. It is not asserted here to solve the motion group of a connected Hopf tree with three or more vertices. It supplies no warrant to erase internal Dahm kernels for general pieces.

Sources: https://doi.org/10.1016/j.aim.2025.110235; https://eprints.gla.ac.uk/350452/2/350452.pdf, pp.2–3, Section 4.3, and Example 4.12, pp.27–28.

## 6. Scope and verification

The result is a source-compatibility correction based on a known example. It settles the literal universal isomorphism in the negative, subject to the explicit meaning that an automorphism group is a genuine subgroup of the automorphism group of the stated RAAG. It does not identify the authors' intended revised conjecture, establish a general forest motion-group formula, or claim originality for the quaternion computation.

`check_groups.py` is an auxiliary exact finite verification. It checks all products and associativity for Q8, all signed 2×2 permutation matrices, their involution counts, the four-element Dahm image and its two-element kernel, non-splitting, and the exact 3×3 endpoint rotations. It contains no floating-point arithmetic and no optimisation-sensitive `assert` statements. The mathematical no-embedding proof in Section 3 is a proof over all real matrices, not an inference from a bounded matrix search.

No S^3 embedding-space claim or R^3-to-S^3 comparison is needed in this argument. A source discrepancy involving that separate comparison is recorded in the source audit and is not used to justify the R^3 conclusion.
