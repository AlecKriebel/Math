# Independent audit: Kourovka 21.95 / ID 2604

Audit date: 5 October 2026. Disposition: **PASS, within the explicitly limited partial-results scope. The original problem remains unresolved (5/5 research approaches).** No mathematical correction to the frozen author proofs or finite certificates is required by this audit. This is neither a solution certificate nor a novelty/priority judgment.

The reviewed author ZIP has SHA-256 `6d51c5e2467b119245a6b8ef2e1444f6ffb07decc0822522ea240106a6a02f91`, 25,435 bytes. Its manifest hash is `b14e3900ec0feee118e05a3884c5f2380735950e4e0e252804dd0e26f193c5c9`. Frozen files were preserved. The author manifest and arithmetic verifier both replayed successfully; more importantly, the mathematical arguments were inspected and computational tests were independently rebuilt without importing the author program.

## 1. Governing question and comparison class

The complete editor-maintained October 2026 PDF was independently rehashed, its page 191 freshly extracted and rendered, and the full page visually inspected. Problem 21.94 defines recognisability using the abstract graph after removal of all vertex labels and permits every finite comparison group. Problem 21.95 asks for a nonsimple almost-simple example under that convention. Its author is N. V. Maslova. The entry has neither a solved marker nor an unconfirmed-AI marker.

The [editor's update announcement](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/) and [arXiv v47 metadata](https://arxiv.org/abs/1401.0300v47) were checked live. The latter is dated 30 September 2026. The local PDF's hash agrees with the frozen source metadata. It was reused rather than freshly downloaded. Search failure does not prove that no later solution exists; the defensible status is that this investigation does not solve the question and no verified later solution was located.

The author consistently distinguishes labelled equality from abstract graph isomorphism. In particular, affine competitors need not be almost simple. Their nontrivial elementary abelian normal subgroups are allowed under the actual quantifier in the problem.

## 2. Elementary obstructions and affine-extension lemma

**Propositions 1 and 2: pass.** In a direct product with an r-group, any newly created two-prime element order must involve r. A universal r-vertex already has all those edges. Group orders strictly increase with the extra factor, proving nonisomorphism and infinitely many competitors. A proper subgroup with the same labelled graph also has different order, so supplies a valid competitor.

**Lemma 3: pass.** The hypothesis p divides |G| is important: it ensures that adjoining V introduces no vertex. For distinct r,s different from p, a cyclic subgroup of order rs has trivial intersection with the p-group kernel, so its projection retains that order. Conversely every old edge survives through the complement G.

For an absent p-r edge, if an affine element x has order pr, the projection of its cyclic subgroup has order divisible by r. It cannot have order pr because that edge is absent downstairs, so it has order r. The vector x^r is nonidentity, has order p, and is centralized by x. Conjugation of V by x is exactly the action of its projection, proving the needed nonzero fixed vector. In the other direction, a nonzero fixed vector commutes with an order-r complement element. Their product has order pr because the two factors have coprime orders. No diagonalizability, faithfulness, or irreducibility of the module is needed.

**Corollary 4: pass.** A fixed vector in a direct sum has a nonzero fixed coordinate. The lemma thus applies to every diagonal power, and the positive dimension of V makes the orders |V|^k|G| strictly increase. This is an infinite-family argument, not an extrapolation from enumeration.

An additional characteristic-three test uses the augmentation module of S3 over F3. Exhaustive cycle-order enumeration of its 54-element affine extension finds the newly added 2-3 edge and the six nonzero order-two fixed-vector pairs predicted by the lemma. This checks a genuinely edge-adding case outside the characteristic-two exclusions.

## 3. Symmetric groups and the even-degree quotient

**Theorem 5: pass for every n at least 5.** The prime adjacency criterion r+s <= n is correct. If one cycle accounts for both primes it requires at least rs points, which is at least r+s for distinct primes; otherwise the cycles account for at least r+s points separately.

The only absent edges involving 2 occur when an odd prime r is n or n-1. These are boundary cases, not an assertion that one occurs for every degree. Such a permutation has exactly one r-cycle and zero or one fixed point.

For odd n=r, the constant vector has odd coordinate sum, so no nonzero constant vector lies in the augmentation module. For even n=r+1, the invariant vectors in the augmentation module are exactly the constant-vector line T. Taking the quotient by T is essential.

The quotient step was checked explicitly: if w+T is invariant under g, averaging w over the cyclic group of odd order gives an invariant lift with the same image in W/T. Division by r is legitimate in characteristic two (r acts as the scalar 1). Thus the invariant-space sequence is exact and (W/T)^g is W^g/T, which vanishes in this case. There is no illicit assumption that invariant vectors always lift for groups whose order is divisible by the characteristic.

The more general fixed-dimension formula is also correct. An order-r permutation with k nontrivial cycles has n-k(r-1) orbits. Each orbit length is odd, so the augmentation functional on the orbit-constant vectors is nonzero and reduces dimension by one. When n is even, quotienting the invariant line reduces dimension once more, by the same averaging argument.

Independent finite evidence:

- All affine permutations for n=5,6,7 were enumerated on the actual module points. Their orders were measured by cycle decomposition, rather than the author's norm-sum order calculation.
- The base action was checked faithful by counting distinct action permutations. The groups have orders 1,920; 11,520; 322,560, and every element-order multiplicity matches the author results.
- For each odd-prime conjugacy type in degrees 5 through 100, a concrete action matrix was built and its fixed dimension calculated by binary elimination. All 5,526 ranks agree with the formula. This is stronger than merely substituting into that formula.
- The full permutation module for S5 and the unquotiented augmentation module for S6 both add the forbidden 2-5 edge, as the negative controls claim.

## 4. Characteristic-two semilinear symplectic groups

**Theorem 6: pass in exactly the stated natural-module field-semilinear scope.** The transvection t_v(w)=w+B(w,v)v is a nonidentity involution. Its square is the identity because B(v,v)=0; nondegeneracy supplies a w for which B(w,v) is nonzero. Expanding the form gives two equal cross terms in characteristic two, so t_v preserves B.

For a semilinear element x with field automorphism sigma and xv=v,

x(t_v(w)) = xw + sigma(B(w,v))v = xw + B(xw,v)v = t_v(xw).

The coefficient 1 used in this transvection is fixed by every field automorphism, so there is no unaccounted scalar twist. Since t_v belongs to the included symplectic group, it belongs to G. Commutation of t_v with an element of odd prime order r produces order 2r inside G itself. The affine lemma therefore forbids any new edge.

Every intermediate G is covered because the argument uses only its individual semilinear elements and its inclusion of the symplectic subgroup. No identification of all higher-rank outer automorphisms with natural-module semilinear maps is used. The packet correctly excludes exceptional graph automorphisms from its scope. In dimension two over an even field, the scalar centre is trivial, giving the stated PSL2 field-extension application.

Independent finite evidence uses polynomial-basis field arithmetic and generator closure as permutations of the vector space, rather than enumeration and powering of determinant-one semilinear matrices. For q=4 and 8, it recovers base orders 120 and 1,512 and affine orders 1,920 and 96,768. Every base and affine order multiplicity matches the author output. The q=4 fixed-vector transvection check is vacuous (zero pairs); the q=8 test has 504 pairs and verifies involution membership, commutation, and product order for every pair. An extra exhaustive Sp4(2) test checks a higher-dimensional case (base order 720; affine order 11,520).

## 5. PGL2 formula, all 183 maps, and nonisomorphism

**Lemma 7: pass.** For a nonscalar repeated-eigenvalue matrix, the repeated eigenvalue lies in the odd field and scalar removal yields a nontrivial unipotent Jordan block of projective order p. The split semisimple orders divide q-1, and a cyclic split torus realizes all divisors. For the nonsplit case, the eigenvalues lie in the quadratic extension, and the quotient of its multiplicative group by the base-field multiplicative group is cyclic of order q+1. Its elements realize all those projective orders. This exhausts the cases and excludes mixed orders involving p.

Consequently the p-vertex is isolated and the two torus prime cliques overlap precisely in 2. The branch-size construction is a sufficient graph-isomorphism criterion, including an empty odd branch. The proof does not require a claim that the vertex labels or branch orientation are intrinsically distinguished by the unlabelled graph.

All 183 author certificates were checked individually. Independently generated prime powers verify the complete target set, the prime-power nature and bounds of each witness, and the fact that q differs from its witness. For each map, the domain, codomain, bijectivity, every edge, and every nonedge were checked. All maps pass. Their group orders differ because t^3-t is strictly increasing for positive t at least 1. This remains valid despite small-group exceptional isomorphisms: different orders suffice.

The author's largest witness is actually 461, so every displayed certificate lies inside a stronger bound than the stated search cap of 10,000. This is an optional strengthening; it does not require a correction. A second set of 183 certificates was generated independently by choosing the largest matching witness within 10,000, rather than the author's smallest. Both cross-branch map corruption and loss of bijectivity are rejected.

All author histograms for q=5,7,11,13 were independently reproduced by generating the projective action on the q+1 points of a projective line and reading permutation cycle orders. Additional extension-field enumerations for q=9,25,27 confirm the spectrum formula beyond prime fields. These tests validate the implementation; the infinite formula rests on the Jordan-form proof.

The three named maps, including the q=169 and q=289 collisions, pass separately. They do not contradict a labelled-recognition theorem because the prime labels change. The finite census establishes failure of uniqueness for its 183 targets. It does not establish infinitely many partners for any one PGL2 target, nor an all-q result.

## 6. Imported statements and literature limits

The following is a statement-and-use audit, not independent verification of the complete imported classification proofs. Six scholarly PDFs were independently rehashed; their relevant statements were freshly extracted. Hashes match the frozen source metadata. SOURCE_AUDIT.json records locators and limits.

- [Cameron–Maslova](https://research-repository.st-andrews.ac.uk/bitstream/10023/26585/1/Cameron_2021_Criterion_of_unrecognizability_JAlgebra_AAM.pdf), Theorems 1.2 and 1.3: the claimed radical criterion and necessary labelled-recognition conditions match. Crucially, the hypothesis of finite recognisability cannot be replaced by merely assuming the proposed candidate is almost simple. The packet respects this.
- [Gorshkov–Maslova](https://arxiv.org/abs/1606.01402), Theorems 1 and 2: the no-three-coclique criterion and solvable graph partners match. The explicit list includes S6, PGL2(9), M10 and Aut(A6), validating the limited A6-extension statement.
- [Chen–Maslova–Zinov'eva](https://arxiv.org/html/2504.14703v1), Main Theorem and Problem 2: the theorem concerns specified simple groups; the nonsimple existence question is restated. The live abstract lists v1 only. There is no solution to 21.95 in that theorem.
- [Lee–Popiel](https://arxiv.org/abs/2310.10113), Theorem 1.1 and Remark 1.2: the eight-group classification is for sporadic simple groups, and the Ru correction is genuine. This does not classify their nonsimple automorphism groups. The publisher page could not be reopened during this audit; its journal locator was corroborated by the indexed publisher result, while the mathematical statement was checked in v3.
- [Sajjadi](https://dml.cz/handle/10338.dmlcz/151645), Theorem 3.5: the q=169,289 conclusion assumes labelled graph equality. The author packet's collisions address the weaker input of an unlabelled graph and are compatible with this theorem.
- [Khosravi](https://am-brno.math.muni.cz/09-2/am1714.pdf), Section 3 opening and page 88: the four unchanged-socle equalities are stated for M12, He, Fi22 and HN. The displayed Aut(McL) direct-product equality gives the fifth exclusion by taking k=1. Distinct subgroup/product orders supply nonisomorphic competitors. The later necessary quotient descriptions are correctly not promoted to existence constructions.

## 7. Corrections, residual risks, and certification boundary

Required mathematical corrections: **none found**. Optional presentation improvements: explicitly state that the q=4 fixed-vector check has zero instances; mention the actual maximum author witness 461; distinguish independent rank calculations from the author's formula-substitution checks. None affects the validity of a retained theorem.

Keep the original problem status unresolved and the five approaches classified as partial research. Keep the sporadic exclusions marked literature-dependent. Do not convert an imported conditional classification into a constructed competitor, broaden the semilinear theorem to unrepresented outer actions, generalize the finite census to all q, or claim novelty.

This audit certifies the frozen mathematical claims at the stated scope. It does not re-certify raw public-dataset identity metadata, repository-wide absence claims, unseen prior attempts, every page of every cited proof, or software execution in a formal proof assistant. It performs no remote write. The safe audit contains authored analysis, independent code/results, and public verification metadata only. Source PDFs, source-page images, extracted source text, raw datasets, selected dataset records and private coordination material are excluded.
