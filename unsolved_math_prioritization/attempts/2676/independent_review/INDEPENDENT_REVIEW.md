# Independent adversarial review: 2676 / KP-1.17

**Verdict: PASS_SCOPED_PARTIALS. Original question remains unsolved, 5/5 substantive author turns. No mandatory mathematical correction.**

This review is independent of the author route and binds the unchanged final packet:

- FROZEN_MANIFEST.json SHA256: `b34533329e970e1e341f28488db8a45b5fcf60831b7a5b4e465233b6530943b6`
- RESULT.md SHA256: `7ad5fc7f8dab26afaeb5a5de7688b3164648965e050c48f4a4aaf6fd49273c1a`
- TURN_5.md SHA256: `8577ed977929648deef973347e428f21d2d433f78a14a3a189b0240572f50ba2`

All 40 manifest-bound author files and all 22 source PDFs match their hashes. The five per-turn manifests also match. All five checkers were read and replayed in a separate directory, giving byte-identical receipts totaling 361,240 assertions. Independent checks and their limitations are recorded separately. Neither finite computation nor this review supplies a solution of the unrestricted problem.

## 1. Source target and budget

The exact K3 preliminary2026 Problem1.17 asks whether an alternating link and a nonalternating link can share a branched double cover. Its all-links scope is not replaced by knots, by hyperbolic closed covers, or by a chosen family of graph manifolds. The distinction from older Kirby numbering and Greene's arXiv/published conjecture numbers is correct. Alternation is a link-type property. Reflecting one branch accommodates an orientation-reversing cover identification without changing alternation.

The source gate and five substantive turns are distinct and preserved. The historical zero-count TARGET.json is explicitly identified as such; the final ledger records all five attempts and the unresolved gap. The metadata correction has a record and does not reset history. The proposed disposition `unsolved 5/5` is appropriate. Established classification inputs and the small toroidal L-space context receive credit; no priority or novelty assertion is certified.

## 2. Hyperbolic actions and determinant-one exclusion

The finite-group reduction is valid. Each branching involution can separately be conjugated into the orientation-preserving isometry group of a fixed closed hyperbolic manifold. Mostow rigidity reconciles the metrics. There is no need to assume that the two original diffeomorphisms already generate a finite group or to geometrize them simultaneously. Once selected representatives lie in that fixed finite isometry group, their generated group is finite.

Conjugacy descends to a homeomorphism of the quotient pairs. The centralizer lemma is sound: a central involution in a Sylow2-subgroup containing t must equal t under the unique-centralizer-involution hypothesis; then the whole Sylow subgroup centralizes t and has no other involution. Sylow conjugacy gives a single global involution class. The contrapositive yields a distinct commuting partner for **each** branch involution, but does not give that partner an S3 quotient.

Conjugating the second involution into the chosen Sylow subgroup gives the stated dihedral2-group reduction. The independent permutation realization of D8 confirms the intended obstruction: its two reflection classes have no commuting representatives although every reflection has a different commuting involution. This is not a topological mixed-pair construction.

The determinant-one exclusion also holds for links. Split union contributes S1×S2 cover homology. In a connected reduced alternating diagram, loops and bridges in either Tait graph would be nugatory crossings. A nonempty bridgeless graph has more than one spanning tree, so an integral homology-sphere alternating cover forces the unknot. The numerator-one surgery exclusion therefore follows without making a statement about general surgery slopes or finite homology of other orders.

## 3. Integral deck homology and definite fillings

The orbifold/Schreier argument gives the **integral** deck action −I on all of H1. With t a meridian involution and a_i=m_i t, conjugation by t sends each a_i to its inverse. Abelianization, rather than nonabelian inversion of arbitrary words, is the step that gives −I. This works for torsion and free summands and for arbitrary nonempty links; no division by2 occurs.

For the push-in of a connected spanning surface, the disk-and-bands description gives a branched-cover handlebody with one zero-handle and b1(F) two-handles. Thus it is simply connected, and its intersection pairing is the Gordon–Litherland form. The Lefschetz trace argument for its natural deck action is valid. The algebraic isometry −I exists for every symmetric form and induces the required discriminant action, so this coarse algebra cannot supply a new equivariant filling.

The opposite-definite criterion keeps every necessary geometric requirement: extensions of the **specified** involution, standard B4 quotients, and branch surfaces isotopic relative boundary to actual push-ins of S3 spanning surfaces. Greene's theorem applies under exactly these hypotheses. Ordinary fillings and lattice actions do not satisfy them automatically.

The Poincaré-double control is genuine but correctly weak. For P a punctured homology sphere, P×I is a homology ball bounded by H#−H with nontrivial fundamental group. Interior connected sums with signed CP2 give the displayed definite forms and correction-term equalities. The boundary is a nontrivial integral homology sphere, so it has no alternating branch. The argument does not refute any stronger criterion requiring simply connected fillings, irreducible boundary, or equivariant push-in data. Its additional amphichiral-surface obstruction follows from Greene's exact corollary. Interior tubing raises the form rank by2 while leaving its boundary correction and signature fixed, and hence adds one positive and one negative direction when determinant is nonzero.

## 4. Prime reduction, small determinants, and BGH scope

The prime-factor reduction is valid for all links. Alternating splitting and connected-sum factors can be chosen alternating; a nonalternating link has some nonalternating nonsplit prime factor. Its irreducible nontrivial cover cannot be absorbed into an S1×S2 factor. Uniqueness of three-manifold prime decomposition, without invoking link-factor uniqueness, then matches it with an alternating prime factor's cover. Unknot detection excludes a hidden S3 factor. The matched cover is a rational homology sphere and an L-space.

The edge bound τ(G)≥|E(G)| has a complete proof: an open ear of length l gives l extensions of each old tree and another tree containing the whole ear, and block tree counts multiply. Blocks have at least two edges. The small graph lists are correct, including multiedges and cut vertices. The determinant≤4 possibilities yield S3, lens spaces, or RP3#RP3; none has a noncyclic finite fundamental group. Determinant5 gives the parallel-five pair, five-cycle, or theta(1,1,2), yielding two-bridge covers. The independent deletion-contraction enumeration checks beyond the needed edge bound and agrees with the Laplacian calculations.

The source applications preserve the exact editions and hypotheses. BGH's Seifert theorem needs prime Seifert link and non-ADE status, not a separate quasipositivity assumption. The D/E double covers have noncyclic finite groups and orders4,3,2,1 as appropriate; the odd-D v1 numerical entry is bypassed by correct independent algebra. BGH v5 Theorem2.13 is a proved **degree-two** exclusion for prime toroidal branch exteriors in the stated homology-sphere setting. The all-degree conjecture is not used. Lens-space branching rules out the alternating torus-link exception. Hence the prime reduced **branch exteriors** are hyperbolic; their common closed cover need not be.

The separate common-Seifert-cover exclusion is already classical and recorded in the exact K3 remark. In the nonspherical case, fiber-orientation-preserving branches have Seifert exteriors, whereas the hyperbolic-exterior branches must be Montesinos and hence mutually related by mutation. The spherical case has the cited uniqueness. These inputs justify reducing the remaining cover geometry to hyperbolic or toroidal non-Seifert, without claiming a general graph-manifold action theorem.

## 5. The actual two-trefoil family

The displayed matrix uses columns in the meridian–longitude basis, has determinant−1, and gives the stated Mayer–Vietoris presentation x1=(r+1)x2, p_r x2=0. The unit relation proves H1 is cyclic, rather than merely bounding its order. Both marked inclusion generators survive as generators because gcd(r+1,p_r)=1.

Irreducibility and incompressibility of the gluing torus follow from those properties of the trefoil exteriors. The regular fiber is 6μ+λ, and its mismatch is −r²+11r−29. The equation that this vanish would force (2r−11)²=5, impossible for integer r. The trefoil pieces are not exceptional nonunique-fibration pieces. They therefore give exactly the single JSJ torus; the union is non-Seifert. A horizontal-torus Seifert alternative cannot have these trefoil pieces.

The L-space slope calculation is correct on the projective circle. The complement of the **interior** right-trefoil interval includes the meridian as an endpoint, even though meridional filling is an L-space. Its image is [r+1−1/(r−1),r+1], strictly inside the other interval for every r≥2. This satisfies HRW's exact gluing criterion. Negative surgery numerators in the quoted rank formula have also been checked against the primary proposition.

There is an actual involution, not just compatible homology. Complex conjugation on the standard complex-coordinate trefoil is orientation preserving, reverses its parameter, and has the stated unknotted fixed circle. An invariant trefoil neighborhood has ball quotient; its complement does too. In marked torus coordinates, the standard boundary action is −I and the **linear** gluing commutes with it exactly. Equivariant collars give a smooth branched quotient built from two balls, hence S3.

Odd cyclic cover homology forces one branch component by the integral Fox-coloring presentation reduced modulo2. Irreducibility forces the branch knot prime. BGH's exact Seifert and toroidal exclusions then make every branch exterior hyperbolic. For r=2, determinant5 and the essential torus exclude every alternating branch. This example cannot be used as a mixed pair.

## 6. Arbitrary involutions and the global gluing attack

The final family theorem survives the principal adversarial challenge. Gordon–Luecke's recalled equivariant-JSJ statement applies to each prime branch knot here. It supplies an invariant representative of the unique JSJ torus. This step does not assume the branch has unknotting number1.

Piece exchange is excluded by the marked inclusions and the integral deck action: exchange would send x2 to ±(r+1)x2, whereas the deck action is −x2; neither congruence holds modulo p_r. The alternate boundary-matrix calculation is consistent. Thus each piece is invariant.

For an orientation-preserving marked trefoil-exterior homeomorphism, the longitude kernel first forces a triangular matrix with diagonal signs. Preserving orientation makes those signs equal. Preservation of the characteristic central generator represented by 6μ+λ then forces the remaining shear to vanish. Boundary matrices are therefore ±I. Surjective inclusions into odd-order cover homology force the involution's piece action to have negative sign.

The boundary −I action can be linearized by a homology-trivial conjugacy. Such a conjugacy extends over the meridional solid torus, so the piece action extends to an actual strong inversion of the trefoil core in S3. This is a three-dimensional meridional extension, not the unsupported four-dimensional filling extension from Turn2. Sakuma's orientation-preserving pair-conjugacy theorem applies, and invariant neighborhoods can be matched equivariantly before restricting conjugacies to the exteriors.

Crucially, these two local conjugacies need not agree along the boundary. The packet retains their discrepancy u=g h_r^{-1}. It commutes with the reference elliptic involution and acts by ±I on torus homology. Its quotient lies in the kernel of Mod(S0,4)→PSL(2,Z), which the precise cited proposition identifies with the four half-translation classes. The three nonidentity classes are Conway mutations. Isotopies of the four-marked gluing sphere extend through a boundary collar, so this is enough for link equivalence of the glued quotient pairs. The at-most-four conclusion, up to the stated mirror convention, follows; no assertion that all four are distinct is needed.

Thus all branch knots of a fixed Y_r have the same alternation status. This closes the displayed family only. General JSJ graphs, piece exchanges, multiple boundary tori, and nonunique local strong inversions are not controlled; closed hyperbolic common covers have no such splitting. The manuscript correctly retains those as unresolved original gaps.

## 7. Final disposition and validation limits

The exact scope is a collection of rigorous, credited partial reductions, a valid weak-criterion countercontrol, and a family-scoped involution-rigidity theorem. No mixed pair has been constructed, and the unrestricted alternation-transport problem remains open in this work. The independent checks are reproducible finite controls and symbolic identities, not replacements for geometrization, equivariant JSJ, strong-inversion classification, Floer theory, or the source-specific theorem hypotheses.

The accompanying SOURCE_NOTES explicitly records unrecovered original papers and the accessible primary statements actually used. A temporary structural-equality assertion in the reviewer's own symbolic checker was normalized before sealing; it was an algebraic-expression comparison issue, not an author error. All frozen author mathematics remained unchanged throughout review.

**Publication recommendation:** a single draft partial-results PR, with original status `unsolved 5/5`, the precise family scope and outstanding gap visible. No mandatory correction, no full-solution or novelty certification. The parent retains the publication gate.
