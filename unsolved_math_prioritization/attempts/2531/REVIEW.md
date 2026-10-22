# Independent review of problem 2531 (Kourovka 21.22)

## Verdict

**Accept the frozen packet as correct, explicitly scoped partial progress. The original problem remains UNSOLVED after 5/5 substantive author turns. No blocking mathematical correction is required.**

This is an independent mathematical and reproducibility review of the five written arguments, not a claim of formal proof-assistant verification, historical novelty, or confirmation by the Kourovka editors. The computational certificates check finite examples and exact identities; they do not settle the original infinite-group question.

The reviewed repository is AlecKriebel/Math, directory `unsolved_math_prioritization/attempts/2531`, at frozen commit [1a9ff1531147bca3a1279fb7fc21e740acb8ecd4](https://github.com/AlecKriebel/Math/commit/1a9ff1531147bca3a1279fb7fc21e740acb8ecd4), branch `math/2531-hopfian-wreath-wip`. Review performed 2026-10-03 UTC. No author proof was changed, no sixth author research turn was undertaken, and this review itself does not authorize publication.

## 1. Object identity and evidence chain

The supplied local directory contained the four source PDFs, extracted source text, the problem/prior records, and remote receipts, but did not contain the author proof files. I therefore fetched all frozen files through the GitHub connector into a separate review directory.

The verification was stronger than trusting the author's receipt:

- A fresh read of the branch resolved to the stated frozen commit.
- A fresh directory listing at that commit contained exactly 38 files and agreed with the supplied receipt on every filename, size, and Git blob SHA.
- Each of the 38 contents was fetched at the immutable commit. I independently recomputed its Git blob hash from the actual local bytes, including the Git blob header, and matched the remote listing.
- `FINAL_AUTHOR_MANIFEST.json` binds the other 37 files; every recorded SHA-256 and byte length matched. Its own SHA-256 is `7ab53c438285404d5283c822a54a184c45ac66991aa4a5b091ce1fed954744be`, agreeing with the separately supplied receipt.
- All five turn manifests replayed: 27 historical file bindings and four links between successive manifests passed.
- All four primary-source PDF byte counts and SHA-256 hashes matched `SOURCE_MANIFEST.json`.

Earlier state files remain historical checkpoints. `FINAL_STATE.json` and `STATE_T5.json` consistently say five turns consumed, original target unresolved, and author work frozen. Their pre-review field saying independent review is pending is historical author state, not an inconsistency to repair by overwriting frozen bytes. A subsequent disposition should be additive.

## 2. Exact source gate and source qualifications

### 2.1 The original question

The exact target concerns the standard restricted **regular** wreath product of finitely generated Hopfian groups. Its base consists of finitely supported functions from H to G, and H acts by left translation. A positive result for a smaller class of bases or a negative example for a different action does not answer it.

I visually inspected the supplied rendering of printed/PDF page 180 and independently extracted page 180 from the hash-verified October 2026 PDF. Problem 21.22 has the expected wording and attribution to H. Bradford and F. Fournier-Facio. It bears neither the solved marker nor an unverified-solution marker. Independently re-extracted text of the supplied October update file contains no 21.22 entry.

The [editors' current page](https://kourovkanotebookorg.wordpress.com/) also identifies the October 2026 update and its distinction between confirmed solutions and unverified AI proposals. A fresh web-tool open of the main PDF URL returned a retrieval error during this review; that did not prevent inspection of the already supplied, hash-verified PDF. The PDF identity and content verification here should not be described as a successful fresh download by this reviewer.

The local catalogue record agrees with the primary question. Its cached prior-research record is null. The author's historical claims about all-ref searches, queue rank, and absence of earlier attempts were read, but I did not independently repeat the full 494-ref search or reconstruct the whole catalogue provenance. Thus those are historical search assertions, not a new exhaustive no-prior-work certificate. This qualification does not alter the primary-source identification or the mathematical verdict.

### 2.2 Credited 2024 inputs

I checked the supplied published PDF and the [publisher's primary article](https://link.springer.com/article/10.1007/s00209-024-03589-3). The dependencies used by the packet have the necessary hypotheses:

- Proposition 2.6 provides basicity for abelian bases with finitely generated infinite acting group.
- Lemma 2.14 retains Hopficity of the quotient. The packet also proves this reduction directly.
- Lemma 5.7 provides invariance of the central restricted base for nonabelian lamp group and Hopfian acting group.
- Theorem 1.5 and Corollary 1.6 supply the abelian matrix criterion and cited sufficient cases.
- The stated nilpotent and just-non-property results have narrower hypotheses and are not incorrectly promoted.

The local text of Proposition 2.15 is not a safe substitute for the explicitly qualified argument: its displayed statement does not state all the assumptions used by the cited Lemma 2.14, and its final formula abbreviates the relabeling. Turn 4 correctly retains Hopficity of H and performs the relabeling itself.

The matrix dimension used here is the **maximum multiplicity at a fixed prime-power exponent**, not the sum of all multiplicities. That matches the credited theorem. Its use is a transport of a prior result, not a new direct-finiteness proof.

### 2.3 The 2026 paper does not close the question

I checked the introduction, Proposition 2.2, and Corollary 2.3 of the supplied hash-verified PDF, and verified the [arXiv version record](https://arxiv.org/abs/2602.19235v1). Kochloukova's example is on the coset space B/H with a nontrivial infinite stabilizer, whereas the present question uses B acting on itself.

The distinction is algebraic, not terminological. The induced module has h v = v for h in the stabilizer, which is used in the one-sided-inverse calculation. In the regular group ring those distinct group elements remain distinct basis elements; the same calculation does not become the identity. The action in the newer example is faithful, so faithfulness alone would not remove this issue. Turn 2 additionally requires nonabelian simple lamp factors, absent from that example.

I accept the packet's exclusion of this example as a solution of the original question. Neither that exclusion nor the absence of a notebook annotation proves that no unindexed later solution exists. The packet appropriately makes no historical-priority claim.

## 3. Turn 1: centerless basic epimorphisms

**Accepted with its exact basicity hypothesis.**

The base restriction F is onto and the quotient endomorphism alpha is an automorphism because H is Hopfian. This is proved before any normal-image or kernel argument uses it.

The key argument in Sections 3-4 withstands the main possible failure modes:

1. Finite generation of G gives a finite support set S for the image of a single lamp group. It does not require H to be finite or finitely generated.
2. Each local image A_s is normal in G because the corresponding image lamp subgroup is normal in the surjective image base.
3. At output coordinate y, offset s comes from the unique input h = alpha^(-1)(y s^(-1)). This is the correct order for noncommutative H.
4. Distinct input groups commute. Their coordinate images are exactly A_s, even with inner conjugation, because A_s is normal. Hence these local images commute and multiply onto G.
5. If a product of their elements is the identity, each component is central in G. Centerlessness therefore makes the decomposition an internal direct product.

Most importantly, coordinatewise surjectivity alone is **not** used to assert that the collapsed endomorphism Theta is onto. The proof prescribes a single finitely supported output simultaneously, placing the requested A_s component at coordinate s for every s. In a preimage, the single input lamp at 1 supplies precisely those components, because b(1)=1 and no other input contributes to the same factor at that coordinate. This proves simultaneous surjectivity.

Hopficity of G now legitimately makes Theta invertible. Factor uniqueness then kills every local component of a putative kernel element. The explicit inverse has the stated conjugations and finite support bound. No trivialization of the cocycle is assumed. The Hom(G,H)=0 sufficient condition really does force every lamp to have trivial projection to H, so its corollary is valid.

Nothing in this argument proves automatic basicity for arbitrary centerless G. In particular the general nonabelian free-base case remains outside the result.

## 4. Turn 2: simple-factor orbit counting

**Accepted for finite products of nonabelian simple groups and faithful transitive actions.**

The normal-subgroup classification used here is valid for restricted sums, including infinite simple factors. A nontrivial coordinate of an element of a normal subgroup gives, by commutation with that coordinate group and centerlessness of a nonabelian simple group, a nontrivial normal intersection with the simple factor. That intersection is the whole factor. This excludes diagonal normal subgroups and justifies the description of quotients and their intrinsic minimal normal factors.

The two-commutator identity is correct. For a moved coordinate x, the first commutator has x-coordinate g^(-1); the second commutator isolates [g^(-1),u] at x. Perfectness and transitivity then give the entire base inside every nonbasic normal subgroup. Faithfulness is used exactly to obtain such a moved coordinate.

The orbit count does not assume an abstract isomorphism is equivariant. It uses surjectivity of Phi: every target conjugator has a source preimage. Consequently images of surviving source simple factors have at most m ambient W-conjugacy orbits. If the image base N were nonbasic, it would contain B. Normality of B inside the semisimple group N makes B a union of intrinsic factors; its m orbits are preserved by W, and any extra factors give another orbit. This is the required contradiction.

Once basicity is proved, Hopficity of H gives Phi(B)=B and kernel containment. Killing a nontrivial simple factor kills its entire source orbit, leaving at most m-1 target orbits, again a contradiction.

The finite number m, normality, faithfulness, and transitivity are all genuinely used. The one-point nonfaithful factor swap correctly refutes automatic basicity when faithfulness is removed, without claiming non-Hopficity. No conclusion for arbitrary abelian lamps or arbitrary centerless bases is obtained.

## 5. Turn 3: perfect bases and central extensions

**Both theorems accepted.**

For perfect G, the proof that G/Z(G) is centerless is correct: a lift of a central quotient element induces a central-valued commutator homomorphism, which vanishes on a perfect group. Also P Z(G)=G implies P=G, by taking commutators.

The quotient step has no circular appeal to Hopficity of G/Z(G). Surjectivity of F preserves the center of the restricted base and gives an onto map on the quotient base. Only the simultaneous-surjectivity part of Turn 1 is applied there. It gives Theta(G) Z(G)=G; perfectness then yields surjectivity of Theta on G, and only then is Hopficity of G used.

For p_s = psi_s composed with Theta^(-1), the inner-equivariance calculation is valid. On a different perfect factor K_t, p_s has central image and is therefore trivial. On its own factor it is the identity. Thus the local images really are direct factors despite the possibly nontrivial center. This justifies both the kernel argument and reuse of the finite-support inverse.

The proof of the credited invariant-central-base lemma is also valid. In the nonbasic case, the regular action gives a surjective coordinate projection of the normal image intersected with the base. An abelian normal image cannot have such a projection onto nonabelian G. Centrality then follows by commutation with the image of the whole base.

Passing to the semisimple central quotient and using Turn 2 does force basicity upstairs. The preimage of the quotient base is exactly the original base. Perfectness then supplies injectivity without an additional Hopficity assumption on Z(G) wr H.

The SL_2(F_5) central-product example is consistent: order 7,200, center of order 2, and central quotient a product of two simple groups of order 60. The independent-shift construction fails to preserve its diagonal central relation, exactly as claimed. If an empty simple product is admitted as a convention in Theorem B, the extra case is G=1 and reduces immediately to Hopficity of H; it creates no substantive gap.

## 6. Turn 4: derived and abelian reductions

**The conditional theorem, twisted-base criterion, and split equivalence are accepted.**

The proof of finite generation and perfectness of D=G' is important and correct. It follows from G=D Z(G) and the chosen finite generating set, not from a false claim that arbitrary derived subgroups of finitely generated groups are finitely generated. It also correctly identifies Z(D)=D intersect Z(G).

The twisted-base criterion requires only the displayed individual covariance relations. None of its factor, quotient, or kernel arguments uses a cocycle law for the chosen c_h. Thus coordinatewise lifts of b(h) into D^(H) need not form a cocycle, and no splitting of a central extension has been smuggled into the argument.

Surjectivity of F implies F(D^(H))=D^(H). On abelianization, inner conjugations vanish, so discarding the cocycle gives a genuine epimorphism of A wr H. Its assumed Hopficity pushes the remaining kernel into D^(H), where the twisted criterion removes it. The two assumptions, Hopficity of D and of A wr H, are not silently inferred from Hopficity of G.

For G=A times P, G is Hopfian by the derived-subgroup and abelian quotient argument. Conversely a noninjective epimorphism of A wr H can be made H-equivariant on its base after relabeling by alpha^(-1); it then extends by the identity on P^(H) and H. The finite-H case is separately excluded by the standard finitely generated virtually abelian argument. This establishes the exact split equivalence under the stated hypotheses.

The row-vector matrix orientation is correct. From XY=I, right multiplication by Y is onto because applying X then Y is the identity. A nonzero row of I-YX lies in its kernel. Right multiplication commutes with the left H-action even when the group ring is noncommutative. This is a conditional construction; the packet produces no forbidden one-sided inverse over an unresolved group ring.

## 7. Turn 5: finite central residue

**The derived-subgroup theorem and its stated wreath-product consequences are accepted.**

This is the most delicate extension argument, and its distinctions are preserved:

- A surjection psi of D need not initially extend to G.
- It preserves C=Z(D), and the Hopfian quotient D/C implies psi(C)=C, not merely psi(C) contained in C.
- Finiteness of C/mC gives a finite order for the induced automorphism there. A suitable power psi^N is therefore the identity modulo mC on C.
- No finite-index condition on C inside Z(G) is assumed. Z(G)/C is the finitely generated abelian group A and may have a free summand.
- Choosing lifts of a direct-sum presentation of A gives precisely the additional relations n_i z_i=c_i, together with the internal abelian relations of C. Reducing a relation modulo C verifies completeness of this presentation.
- Since n_i divides m, the difference rho(c_i)-c_i is in n_i C. The chosen corrections b_i preserve each relation.
- The resulting theta on Z(G) maps C onto C and induces the identity on A, so it is onto.
- The two maps agree on D intersect Z(G), commute across the factors, and glue to an onto endomorphism of G. Hopficity of G now forces injectivity of psi^N and hence of psi.

These statements remain valid when C has torsion or is not finitely generated. The torsion-free-abelianization case uses m=1, while the wreath consequence separately imposes the semisimple central quotient. The perfect Hopfian quotient in the derived-subgroup theorem must not be confused with that stronger wreath hypothesis.

The infinite shift example accurately identifies a failed lifting mechanism. In the enlarged torsion-free abelian group, any extension kills z, so its image misses the nontrivial quotient. This does not construct a finitely generated Hopfian G with the prescribed center, and it is not a counterexample to the original problem. The author states both limitations.

## 8. Reproducibility and the limits of the certificates

Using Python 3.12.14, I ran:

```text
python REPLAY_ALL.py --sources PATH_TO_SUPPLIED_SOURCE_DIRECTORY
```

The resulting JSON is byte-identical to `FINAL_REPLAY.json`:

- Turn 1: 244,606 reported exact assertions
- Turn 2: 20,374
- Turn 3: 72,670
- Turn 4: 26,333
- Turn 5: 83,023
- Total: 447,006

All manifest and source checks also passed. The final-manifest verification was performed separately, because the supplied aggregate script verifies the historical manifests but does not itself verify the final manifest.

The scripts were read, not merely executed. Their scope is appropriately limited:

- Turn 1 exhausts one finite cyclic case and tests bounded supports over a nonabelian acting group. Its tested cocycle is a coboundary.
- Turn 2 samples double commutators with a fixed seed and exhausts finite orbit masks. Its factor-swap control is only a simple sanity check, not an enumeration of endomorphisms.
- Turn 3 checks the finite central product and finite inverse controls. The theoretical central quotient and perfectness arguments remain necessary.
- Turn 4 exhausts the stated finite rings. In such rings the defect I-YX is zero whenever XY=I, so that test cannot furnish a nonzero kernel defect over an unknown infinite ring.
- Turn 5 checks relation identities, including bounded fragments of infinite examples. It does not establish a group realization or infinite surjectivity by enumeration.

I added a separate reviewer-only supplemental checker, `check_review_supplements.py`, with **55,220** successful exact controls. It tests sparse lamps on the infinite integer line with a step conjugator whose resulting restricted cocycle is not a restricted coboundary; the proof of that last fact is the nontrivial single jump versus telescoping for a finitely supported conjugator. It also tests a central presentation with C=(Z/16)^2, two torsion quotient generators, and a free generator, using rho=5 id, which is nonidentity on C but identity modulo 4C. These are independent boundary controls for the already written arguments, not an additional author theorem or a sixth search turn.

## 9. Required disposition and publication boundaries

No blocking correction is requested. Publication may describe the packet as independently reviewed partial progress with the qualifications above. It must retain:

1. Original target: **unsolved**, author turns: **5/5**.
2. All exact hypotheses of each positive theorem.
3. Credit for prior reductions, matrix criteria, and abelian sufficient cases.
4. The distinction between regular and nonfree coset actions.
5. The distinction between a failed extension mechanism and an actual group counterexample.
6. The distinction between finite identity checks and proofs for arbitrary groups.

The remaining gap is substantial. General nonbasic epimorphisms outside the proved quotient classes are uncontrolled; nonperfect central behavior still includes the credited abelian stable-finiteness obstruction. Even a fixed nonabelian direct factor such as A_5 does not remove that obstruction. Neither the original positive assertion nor a counterexample has been established.

The author's 40 percent estimate is explicitly subjective coverage language. This review does not endorse it as a mathematical completion metric or a probability.

Any final reviewed-state or queue update should be additive and preserve the 38 frozen files. Raw source PDFs, catalogue imports, extracted source text, and local provenance material need not be republished. This review was completed before, and separately from, any publication action.

