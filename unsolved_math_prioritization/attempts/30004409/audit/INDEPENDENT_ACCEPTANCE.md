# Independent acceptance: the single-edge Hopf-tree obstruction

Audit date: 8 October 2026. Target: rank 1073, problem 30004409.

Submitted packet manifest SHA-256:

    a9574bdd908b71ac3bb3fda27e68d3818679706e12847e5482b24b6e8540ae3a

## Decision

**ACCEPT the literal-target counterexample, with prior-known credit and zero new mathematical search turns.** No mathematical correction is required for the proposition or the Dahm exact sequence. The conclusion is that the universal identification, as literally formulated for the source's motion space and an actual automorphism subgroup of its stated RAAG, is false. It is not a general computation of forest motion groups, a resolution of a revised conjecture, or a novelty claim for the Hopf-link calculation.

The submitted originals were preserved byte-for-byte. The audit supplies independent algebra and cover checks, fresh source-pin matches, and full replay outputs. It takes the cited smooth topological theorem as an explicit imported theorem; it does not certify that theorem's entire parametrised-isotopy proof.

## 1. Exact target and source match

The two-page Boyd contribution, joint with Bregman, in [Oberwolfach Report 8/2020](https://ems.press/content/serial-article-files/46844), printed pp.501–502, was inspected in text and visually. Definition 1 quotients smooth embeddings by all diffeomorphisms of the source circles: orientations, labels, and parametrisations are forgotten. Page 502 identifies the fundamental group with the motion group, records the single-Hopf-link quaternion computation, and proposes the automorphism identification for links described by disjoint unions of trees. No condition there excludes the one-edge tree.

For that tree, K2, the admissible link is a Hopf link and the graph presentation gives A(K2) = Z². Issues with larger graph-link constructions, definitions of disconnected forests, or choices among signed/pure/unsigned symmetric subgroups do not remove this example. The relevant literal phrase must denote a subgroup of Aut(Z²) for the objection to apply; replacing it by a group extension changes the statement.

The smooth theorem is source-matched in [Boyd–Bregman, The embedding space of a Hopf link, arXiv:2504.21806v2](https://arxiv.org/pdf/2504.21806v2), Definition 2.2 and Theorems A–B. Its quotient is the same unoriented, unordered, unparametrised R³ space. It gives the homotopy model S³/Q8 and the round-to-smooth equivalence. Sections 4's definitions and endpoints were checked, including visual inspection of pp.3 and 16. Version 2 is dated 18 August 2025; no journal acceptance is asserted.

[Damiani–Kamada, On the group of ring motions of an H-trivial link](https://eprints.whiterose.ac.uk/id/eprint/148587/8/H_trivial_reviewed.pdf), Section 2 and Theorems 6.4/6.6, independently corroborates the round convention, labelled C4 group, and unordered Q8 presentation. The paper is published in Topology and its Applications 264 (2019), 51–65, [DOI](https://doi.org/10.1016/j.topol.2019.06.004). Its round result is not silently substituted for a smooth result.

The explicit motion-space definition rules out interpreting the target as merely the Dahm image. The source's π1 is the domain of that representation. Goldsmith's earlier credit is retained through the inspected sources; this audit does not claim fresh full-text verification of Goldsmith's paper.

## 2. Independent nonembedding proof

The submitted averaging argument is valid: a faithful finite real representation can be conjugated into O(2); an orientation-preserving image is abelian, whereas an image containing reflections would force four distinct nonidentity involutions in Q8, which has only one.

Here is a separate linear-algebra proof. Suppose ρ:Q8→GL2(R) were injective and put C = ρ(−1). Since C² = I and C ≠ I, C is diagonalisable. If its eigenvalues are +1 and −1, every image matrix commutes with C and hence is diagonal in that eigenbasis. The image would be abelian. Consequently C = −I.

Let A = ρ(i) and B = ρ(j). Then A² = B² = −I and AB = −BA. Choosing the basis v, Av puts A into the matrix J = [[0,−1],[1,0]]. The equation BJ = −JB forces B = [[x,y],[y,−x]]. Therefore B² = (x²+y²)I, contradicting B² = −I over R. Thus Q8 cannot embed in GL2(R), hence cannot be any subgroup of GL2(Z) = Aut(Z²).

Combining this proof with the explicitly imported smooth Q8 theorem proves the literal-target counterexample. No finite search over integer matrices is used to establish the universal nonembedding claim.

## 3. Dahm representation and covers

Use positively oriented meridians for orientations with linking number +1. Compactly supported ambient isotopies induce the Dahm action. A component's meridian can only be sent to a conjugate of the signed meridian of its endpoint component. The complement group is abelian, so the conjugations disappear. Linking-number preservation requires the product of the two signs to be +1. Thus the image is contained in {I,−I,P,−P}, where P exchanges the two basis vectors.

For unit circles centred at (−1/2,0,0) in the xy-plane and (1/2,0,0) in the xz-plane, choose normals (0,0,1) and (0,1,0). The half-turn A3 = diag(1,−1,−1) fixes centres and reverses both normals. The half-turn B3 = [[−1,0,0],[0,0,1],[0,1,0]] exchanges centres and preserves the corresponding normals. They realise −I and P. Their motions can be extended with compact support by a cutoff away from a ball containing the entire rigid motion. All four image elements therefore occur.

The domain has order eight, the image has order four, and the only order-two subgroup of Q8 is its centre. Hence the exact sequence is

    1 → C2 → Q8 → C2 × C2 → 1.

It does not split: a Klein-four subgroup would require three distinct nonidentity involutions in Q8. Since Inn(Z²) is trivial, passing to outer automorphisms or changing complement basepoints cannot repair faithfulness.

The complete orientation-and-label decoration cover has eight sheets and two components distinguished by linking sign. Its positive-linking component is a connected fourfold cover with fundamental group C2. The labelled but unoriented cover has two sheets and fundamental group C4. The former's inclusion maps π1 onto the central kernel; the latter's image is the cyclic subgroup generated by an orientation-reversing half-turn lift. These are distinct spaces from the source quotient.

The independent checker uses normal forms a^r b^t and additionally reconstructs the actual quaternion lifts a = i and b = (j+k)/√2 using exact Q(√2) arithmetic. The eight generated endpoints map two-to-one onto the four specified rotations. This checks the actual mixed-axis exchange rotation, rather than identifying it with a coordinate-axis rotation without a change of basis.

Clarity-only suggestion: in the submitted last paragraph of Section 4, “has fundamental group C2, the kernel associated with the connected fourfold cover” is more precise than “gives the double-cover kernel C2.” The latter can refer to SU(2)→SO(3), but should not be read as saying that the oriented-and-labelled cover of the full link space has degree two. This wording does not affect the proposition or the exact sequence.

## 4. Ambient-space and extension boundaries

R³ is the ambient manifold throughout this application. S³ in S³/Q8 is the universal-cover model, not an unnoticed switch of ambient link space. No R³-to-S³ comparison, S³ embedding-space theorem, or point-pushing claim is used.

[Boyd–Bregman, Embedding spaces of split links](https://eprints.gla.ac.uk/350452/2/350452.pdf), Theorem A, Section 4.3, and Example 4.12, was checked. The example retains internal Q8 motion factors and specialises to Q8 for one Hopf link; its n-unknot/m-Hopf convention matches the submitted note. Its formula is not a formula for larger connected Hopf trees. Publication: Advances in Mathematics 470 (2025), article 110235, [DOI](https://doi.org/10.1016/j.aim.2025.110235).

The submitted separate S³ warning was not needed for, and is not a premise of, this acceptance.

## 5. Reproducibility evidence

- The externally supplied submitted-manifest pin and every listed file's hash and byte count match.
- Four fresh downloads from the listed scholarly URLs have PDF headers and exactly match all four supplied source hashes and sizes. `INDEPENDENT_SOURCE_RETRIEVAL.json` records each retrieval.
- Both the submitted and independent checkers passed under normal, -O, and -OO Python: six positive runs, all UID 1000.
- Inputs were copied to a directory with mode 0555 and files with mode 0444. Actual append, new-file, new-directory, and unlink attempts all failed with EACCES as UID 1000. This is an observed permission test, not merely a mode assertion.
- External pre-execution pins are in `AUDIT_INPUT_PINS.json`. Both original and protected-copy hashes were checked unchanged after all runs.
- Neither checker contains an AST Assert node. Explicit runtime guards remain active under both optimised modes.
- Seven independent semantic mutants, each in three modes, were rejected: split extension, commuting generators, single-component orientation reversal, detecting the central element, wrong exchange lift, changed exchange endpoint orientation, and a connected eightfold decoration cover.
- Three submitted-checker mutations, each in three modes, were rejected: a wrong quaternion scalar product, a false trivial-kernel guard, and changed exchange endpoint orientation. Together there are 30 expected failures.
- `INDEPENDENT_VALIDATION.json` includes complete stdout, stderr, and exit status for every positive and negative run. No output was truncated.

The finite validation checks group multiplication, exact endpoints, homomorphisms, the eight candidate sections, and covering subgroup data. It does not turn a cited theorem into a machine-verified topological proof. Within that explicitly credited scope, the submission is accepted.
