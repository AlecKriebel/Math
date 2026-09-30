# Independent adversarial review: torsion in fundamental groups of subsets of R³

**Verdict: PASS_SCOPED_REDUCTION.** The compact-witness and neighborhood-kernel reductions are correct. No correction is required. The unrestricted problem remains unsolved; retain two substantive approaches and no novelty claim.

Reviewed on 2026-09-30 by a separate AI reviewer, gpt-6-astra with xhigh reasoning. This is not human peer review.

## Frozen scope and evidence

- Problem: 3415 / OPG-37151, existence of a **nonidentity** finite-order element in the ordinary fundamental group of an arbitrary subset of R³
- Reviewed artifact: PARTIAL_RESULT.md, SHA256 **a02ad483c97dadba56cd434c25365bc403030093cd6135f6e41ffb5d2e2682f4**
- Submitted checklist: verification.json, SHA256 **5fe1b1d67c54bb577d996c22f754f9d913d779ab4800ae1718c8ce18fff54877**
- The checklist is a logical/source inventory. There is no submitted executable geometric computation to reproduce, and this review claims no numerical tests of wild embeddings or fundamental groups

The reviewer read the complete artifact and checklist, the original problem and discussion, the cited expert example, and the exact open-domain theorem in the downloaded primary preprint. No author mathematics was edited.

## 1. Compact disk witness and exact order

Let a based loop γ represent an element of exact order n > 1 in π₁(X,x₀). The degree-n circle map can be chosen to fix the basepoint. Its composite with γ represents the nth power, and its nullhomotopy supplies the disk map h used in the artifact.

Surjectivity of the degree map is essential: it ensures γ(S¹) lies in Y = h(D²), including x₀. The same disk kills the nth power in Y. If a smaller positive power vanished in Y, inclusion into X would kill it there, contradicting the original exact order. Thus the argument preserves the order itself, not merely a divisor.

Compactness and metrizability follow because Y is a compact subspace of Euclidean space. Composing a Peano curve onto D² with h gives a continuous surjection from the interval onto Y. The Hahn–Mazurkiewicz theorem therefore yields a compact connected locally connected metric space, which is locally path-connected. Path-connectedness also follows directly from the disk image. This does not supply local simple connectivity, an ANR property, or a neighborhood retraction.

No arbitrary continuous-image preservation theorem for local simple connectivity is being used. The Peano step is valid specifically through the interval-image characterization.

## 2. Neighborhood groups and the precise kernel

For U_k = {z : dist(z,Y) < 1/k}, every point can be joined by a straight segment inside U_k to a point of Y; two such points can then be joined through a path in Y. Thus U_k is an open connected domain in R³. All maps preserve the fixed basepoint.

Kauranen–Luisto–Tengvall, *On proper branched coverings and a question of Vuorinen*, arXiv:1904.12645v1, Proposition 3.4 on printed page 11, states exactly that domains in R³ have torsion-free fundamental group. The downloaded PDF has SHA256 **4cee54e98506340ebaee10a318bc39a1d9534166eb113dc20682b356dfb9ca78**. Its reference to Papakyriakopoulos, Corollary 31.8, is explicit. The reviewer checked the primary preprint's statement and surrounding scope; this review does not independently reconstruct the deep three-manifold theorem.

The image of γ in π₁(U_k) has order dividing n, so it is trivial by that theorem. This reasoning holds for any finite-order element of π₁(Y), not only the chosen witness.

The nested neighborhood system has the required inclusion bonding maps, with no surjectivity or injectivity assumption. An inverse limit of torsion-free groups is torsion-free because a finite-order compatible tuple has every coordinate equal to the identity. The natural map J consequently kills all torsion in π₁(Y), and an injective J would rule out torsion.

The artifact's phrase “every ambient neighborhood” is justified, not merely the displayed sequence: compactness of Y makes these U_k cofinal in its open neighborhoods. Alternatively, the component of any open neighborhood containing the path-connected Y is itself an open connected subset of R³.

The proof does not interchange ordinary π₁ with an inverse limit. It does not need a formal identification of this limit with a particular definition of the shape fundamental group.

## 3. Adversarial controls on invalid conclusions

The two critical invalid implications remain excluded:

1. A homomorphism to a torsion-free group need not have a torsion-free source or kernel. The abstract map Z/2 → {1} is an elementary control.
2. A nontrivial kernel need not contain torsion. The abstract map Z → {1} is an elementary control.

These are logical group examples only; neither is asserted to be realized by a compact subset of R³.

A nullhomotopy in each U_k does not itself furnish a nullhomotopy in Y. There is no equicontinuity, coherent parameterization, bounded complexity, or compact family of disk maps assumed. Compactness of their ranges does not create such compactness in a function space.

The neighborhood-retract case is sound: the retraction induces a left inverse to the inclusion on based π₁, yielding injectivity. Connectedness can be enforced by taking the ambient component containing Y. No retraction or local regularity is imported into the unrestricted target.

## 4. Source and example boundaries

The [original Open Problem Garden question](https://www.openproblemgarden.org/op/torsion_for_subsets_of_mathbb_r_3) matches the artifact. Its homology sentence is not a safe unrestricted theorem about singular homology. The [original expert discussion](https://mathoverflow.net/questions/4478/torsion-in-homology-or-fundamental-group-of-subsets-of-euclidean-3-space) explicitly distinguishes singular, Čech and Steenrod theories and contains the original author's acknowledgment of overstatement. The artifact correctly refuses to deduce that hypothetical torsion must belong to a commutator subgroup from that sentence.

Moishe Kohan's 2021 argument in the same discussion assumes semilocal simple connectivity. Its small-loop fillings are in the original space and use that assumption. Neither the post nor this review supplies those fillings for an arbitrary compact Peano witness. The package properly credits the related disk-image/neighborhood ideas.

[Jeremy Brazas's Griffiths twin-cone exposition](https://wildtopology.com/bestiary/griffiths-twin-cone/) explicitly records an embedded compact locally path-connected space, nontrivial ordinary fundamental group, trivial shape, and a torsion-free fundamental group. This supports the warning that neighborhood/shape invisibility need not imply triviality of a loop. It provides no finite-order counterexample. The artifact clearly treats this as a credited expert example; this review does not reprove its infinite-word group calculation.

The domain preprint is [arXiv:1904.12645](https://arxiv.org/abs/1904.12645), published in *Bulletin of the London Mathematical Society* 54 (2022), 145–160, [DOI 10.1112/blms.12565](https://doi.org/10.1112/blms.12565). The artifact accurately warns that the journal numbering differs.

## 5. Final assessment and remaining theorem

The package establishes a valid reduction of the unrestricted question to finite-order elements in neighborhood-invisible kernels of compact Peano continua embedded in R³. It does not prove these kernels torsion-free or construct a torsion element in one.

The source repair and logical limitations are material, not cosmetic. Preserve them in any summary. Recommended publication status: **unsolved, 2/5 substantive approaches, scoped partial reduction**. No unrestricted solution, new construction, or priority claim is supported.

The accompanying review_summary.json records the logical checks and their limits. It is not an executable test receipt. The author snapshot and submitted checklist are preserved byte-for-byte for auditability.
