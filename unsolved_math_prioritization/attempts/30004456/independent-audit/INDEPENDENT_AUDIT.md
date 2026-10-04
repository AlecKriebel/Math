# Independent audit of record 30004456

## Recommendation and scope

**PASS_WITH_NOTES. Recommend `already_solved`, `1/5` for the intended nonzero-character conjecture, normalized to the character image.** The frozen application proof correctly deduces the target from existing literature. The decisive result is Jaikin-Zapirain, Kudlinska and Sánchez-Peralta, *Thurston norm, polytopes and splitting complexity*, arXiv:2606.31774v2, Corollary 1.5 and Theorem 3.3(ii). This is an existing preprint resolution, not a new solution produced by this packet. No peer-reviewed publication of the resolving work was verified.

The literal statement with an unrestricted zero character is not covered. If “inducing” means the canonical HNN exponent homomorphism, it must mean an epimorphism, or a nonzero character after identifying its image with Z. That qualification is material and must accompany the disposition. The frozen packet already states it repeatedly.

No blocking mathematical defect was found in the theorem application. A nonblocking packaging note is recorded below. This audit is independent of the producer's theorem ledger and uses freshly retrieved primary PDFs, direct theorem inspection, separate computations, and full release hashing. It is not a formal proof or an independent reproof of every external ring-theoretic foundation of the 38-page resolving preprint.

## Exact release binding

Audited directory: `submission/` in the rank 612 / ID 30004456 package.

External frozen manifest SHA-256:

`d51066d53d8cbe9e114b044fa828b9adaad61f08140b4f0bac7cfa90a7cdb9eb`

All ten listed payloads have the recorded byte lengths and SHA-256 hashes; the actual payload file set equals the manifest file set. The internal manifest checks all nine non-manifest files. No frozen file was edited. The application proof specifically audited has SHA-256:

`d2a8e1af8d2342390cab9b2bcb5de240cb60f45a1c5e0dc57b834414fe4aed12`

The catalogue statement text in the private selected record independently hashes to:

`2ad5545ab4fd0d9150d5bcd5fef8428d772d84a375eab9dcb5da23d4d6a1bdd3`

This matches the frozen statement identifier. The review hash is inherited queue metadata, not a proof certificate. This audit did not redo the producer's entire repository/dataset history investigation, and makes no additional uniqueness claim about every branch or historical attempt. Its mathematical target was checked against the original report itself.

The audit's `AUDIT_MANIFEST.json` binds its own deliverables to this exact frozen release. Any change to a frozen payload falls outside this acceptance.

## Source verification

Four PDFs were downloaded afresh from the primary endpoints during this audit, rather than trusting the producer's local extracts. Every downloaded byte count and hash matched the frozen provenance ledger:

- [JKS v2](https://arxiv.org/pdf/2606.31774v2): 538,557 bytes; SHA-256 `f072c52f2f9878932173c897b44cc4591e7dbdcdc3538d370a8ac99d6096a7f0`.
- [Oberwolfach Report 16/2020](https://ems.press/content/serial-article-files/46853?nt=1): 412,166 bytes; SHA-256 `85003e2defa1e14e5b34c1d6a761ebc0ca4aefd1afedfdde2ec734022bcf122a`.
- [Feighn–Handel](https://arxiv.org/pdf/math/9905209): 211,390 bytes; SHA-256 `86b7be03cefa22726bde055df6b074b8f12f89b3d4b038b9315a6fb79945a9b2`.
- [Gaboriau](https://www.numdam.org/item/PMIHES_2002__95__93_0.pdf): 560,557 bytes; SHA-256 `7a9bc905ccda760eb2e214ed37cea28c1842bfad60369f1e1926767846ce70ae`.

Relevant text was extracted from these independently retrieved PDFs. Original report p. 899, JKS p. 3, Feighn–Handel p. 1063, and Gaboriau p. 146 were also rendered and inspected as images, guarding against subscript or inequality extraction errors.

The [arXiv version record](https://arxiv.org/abs/2606.31774v2) independently confirms the authors, title, v1 submission on 30 June 2026, and v2 on 31 August 2026. The current unversioned record still identifies v2. The [author's papers page](https://sites.google.com/site/monkudlinska/papers) lists the work under preprints. Narrow searches for the exact arXiv identifier with “erratum” and the title with “correction” did not find a contrary mathematical correction; this is not an exhaustive absence result. The catalogue page could not be retrieved through the web tool, so no claim is made to have inspected a fresh live catalogue rendering.

Full PDFs, extracted text and page images remain private. None is included in the audit release manifest or authorized for redistribution by this audit.

## Exact question and conventions

Gardam's *Computing fibrings*, joint work with Kielak, occupies report pp. 898–900. Its conjecture on p. 899 minimizes the negative Euler characteristic of the **base** A in an HNN presentation with finitely generated base and edge. It does not assume that the base is free. The previous page explicitly introduces finite-rank free-by-cyclic groups. The frozen catalogue formula matches that substantive question.

For finite n, let G = F_n semidirect Z and let phi be a nonzero map G to Z. Write phi(G) = dZ with d positive. An admissible splitting has A contained in ker(phi) and a stable letter t with phi(t) = d after orientation is chosen. Its canonical exponent map is phi/d. Because G is generated by A and t, once A lies in the kernel the absolute value of phi(t) necessarily generates the image. Thus the normalized formulation is not an additional restriction on admissible nonzero splittings.

If instead the phrase “inducing phi” is required literally to assign 1 to the stable letter, phi must be onto. For a general nonzero integral character the kernel formula is invariant under normalization, whereas the homogeneous Thurston map includes the image-generator factor. The proof correctly uses the unscaled kernel invariant.

For phi = 0 no canonical HNN exponent map can equal phi: a stable letter survives in the quotient by the base and maps onto Z. The proposed minimum is consequently empty/undefined under that convention. This is already visible for G = Z squared, whose L2 Euler characteristic is zero. This wording problem is inherited from the abbreviated source statement and is not an unresolved nonzero-character case.

## Independent derivation of the application

The following is the audit's reconstruction, with the assumptions needed at each step.

1. **Ambient hypotheses.** For n at least 1, G is torsion-free: a finite-order element would project trivially to Z and then lie in torsion-free F_n. A graph homotopy equivalence representing the automorphism has a finite aspherical mapping torus, so G is finitely presented. Applying Gaboriau 6.6 to the original extension by Z and the finite value b1(F_n) = n minus 1 gives b1(G) = 0. These establish the hypotheses of JKS 3.3 with the associated finitely presented cover chosen to be G itself and its map the identity. G also directly satisfies Corollary 1.5(i); the word “virtually” permits index one.

2. **Higher L2 vanishing for arbitrary subgroups.** Let S be any subgroup of G and D = S intersect F_n. D is free, with no finite-generation assumption. If S has trivial image under the original projection, S is free and its L2-Betti numbers in degrees at least 2 vanish. Otherwise the image is infinite cyclic and S fits into an extension of D by Z. If D is trivial, S is cyclic. If D is nontrivial, it is infinite, and its L2-Betti numbers in every degree j at least 2 are zero and hence finite. Gaboriau 6.6 can therefore be applied separately in each such degree. It gives b_j(S) = 0 for j at least 2. Crucially, that theorem requires finiteness in the chosen degree alone, not finiteness of b1(D). This is exactly what is needed when D has infinite rank.

3. **Degree zero.** G cannot be infinite cyclic when n is at least 1: any nontrivial subgroup of a cyclic group has finite cyclic quotient, whereas the given quotient G/F_n is Z. Thus N = ker(phi) cannot be trivial, since otherwise G would embed into Z. Torsion-freeness makes N infinite. Likewise a splitting with A trivial would have B trivial and G isomorphic to Z, impossible. Therefore both N and any admissible A have vanishing zeroth L2-Betti number.

4. **Finite classifying spaces.** Feighn–Handel Theorem 1.2 is stronger than coherence: the finitely generated subgroups of the relevant mapping-torus groups have finite type, explicitly defined there by a compact Eilenberg–Mac Lane model and realized by finite presentation complexes. It applies to each A and B. Ordinary group Euler characteristics are consequently defined and equal their L2 Euler characteristics. From steps 2–3, negative chi(A) equals b1(A). It would be invalid to use finite presentation alone to infer this finite-model conclusion, but that shortcut is not taken.

5. **Kernel L2 summability.** JKS Corollary 1.5 supplies a finitely generated edge B with b1(N) = b1(B). The latter is finite for any finitely generated group. Together with steps 2–3, this makes the L2 Euler sum of N finite and shows negative chi2(N) = b1(N). Neither finite generation of N nor finite b1(D) was assumed.

6. **Lower bound and actual minimum.** For every admissible splitting, JKS 3.3(ii) gives b1(N) at most b1(A), at most b1(B). Thus the kernel's negative Euler characteristic is a lower bound for every admissible base complexity. In the splitting supplied by Corollary 1.5 the first and last numbers coincide. The intermediate base value must coincide as well. This proves attainment and establishes a minimum, not merely an infimum. It also resolves the source's edge-versus-target-base discrepancy without assuming free edge or base groups.

7. **Rank zero.** When n = 0, G = Z and every nonzero phi has trivial kernel. Any admissible A lies in that trivial kernel, so A = B = 1. The unique type of splitting is the HNN extension of the trivial base along the trivial edge. Both requested negative Euler quantities are minus 1. Its first L2-Betti number is zero, so the general conversion in step 5 cannot be used here. The frozen proof correctly treats this case separately.

8. **Signs and scaling.** Replacing phi by a nonzero integral multiple does not change its kernel. Multiplication by a negative integer reverses the chosen stable letter orientation; positive multiples only change d. The admissible normalized splitting class and the minimum therefore do not change. A homogeneous norm at d times a primitive character would instead scale by d; it is a different quantity.

A separate topological check gives chi(G) = chi(A) minus chi(B) from finite aspherical graph-of-spaces models. The mapping torus has chi(G) = 0, hence chi(A) = chi(B). In the n at least 1 case B cannot be trivial, since that would force chi(A) = 1 despite chi(A) being minus the nonnegative b1(A). This independently checks all three complexity conventions. The main squeeze argument does not depend on this auxiliary calculation.

## Proof-chain audit of the resolving paper

The decisive result was checked beyond the abstract. The following dependency boundaries are important.

- **Theorem 3.3, pp. 12–16:** its full hypothesis is type FP2(l2), with an associated surjection from a finitely presented group. In this application the identity map is valid, giving exactly part (ii). The proof uses the HNN augmentation-ideal sequence, the invertibility of t minus 1 in affiliated operators, and vanishing b1(G) to make the edge-to-base module map surjective. Claims 3.4–3.7 identify conjugate modules and bound the modules for finite intervals in the kernel's infinite line of groups. Direct-limit dimension control supplies the kernel-to-base bound. Nothing in this argument requires a finitely generated kernel. The finite-edge-image case is separately considered on p. 13. Part (iii) obtains equality under independence of both edge embeddings.

- **Theorem 1.3(ii), pp. 16–17:** the Weak Atiyah hypothesis provides discrete complexity values and an attained smallest edge value. If the chosen edge is not independent, the compressed-to-independent assumption supplies a finitely generated overgroup with smaller b1. The proof enlarges the base by its stable-letter conjugate and explicitly constructs inverse homomorphisms between the old group and the new HNN presentation. I checked that the new base lies in the kernel, that finite generation is retained, and that the stable letter still maps to the original one. The contradiction therefore concerns an admissible presentation of the same group, rather than an unjustified quotient or enlargement. Reversing orientation treats the second embedding.

- **Theorem 1.4, p. 31:** the L2-closure from Theorem 7.7 and the finite-generation conclusion of Corollary 7.6 allow compression to apply to the closure. Lemmas 2.7 and 7.4 identify the obstruction dimension with the difference between b1 of the subgroup and b1 of its closure. This number is nonnegative by dimension theory and nonpositive by compression, so it is zero. For the target application the ambient base is finitely generated, as required to use the finite-generation machinery. Bases with free intersection of infinite rank remain covered by the paper's broader free-by-cyclic results; a base contained in the original F_n is free and is covered by the free-group case.

- **Theorem 7.7 and Sections 5–7:** the closure theorem depends on subgroup rigidity over F2, comparison with rational coefficients, and properties of Hughes-free universal division rings. The paper invokes or adapts arguments from earlier papers. In particular Claim 7.10 and the final proof of Theorem 7.7 refer back to Jaikin-Zapirain's arXiv:2403.09515, and Section 6 adapts Sánchez-Peralta's arXiv:2603.26580. Proposition 6.5 supplies coherence and homological-dimension properties; Theorem 6.6 invokes Farrell–Jones input; Theorem 1.6 yields the required universal division-ring property. These are identified imported dependencies, not computations certified by the packet.

- **Corollary 1.5, p. 31:** the proof explicitly assembles Theorems 1.3 and 1.4 after finite presentation, vanishing b1, and the appropriate Atiyah conclusion. It does not posit the desired splitting as an assumption. The original conjecture is explicitly identified on p. 2.

This inspection found no circularity or omitted target hypothesis in the application. It does not convert the paper into peer-reviewed work and does not certify all of its imported arguments from first principles. The recommendation is a literature-resolution determination at that stated level.

## Adversarial examples and computational checks

The supplied script was read before execution, then run both without sources and with the four independently retrieved source PDFs. Both modes pass. Its 5,656 Schreier cases, 16,968 scaling cases and all boundary counters reproduce. Source-free mode truthfully checks zero source files; source mode checks all four. Fresh replay verifies nine internal-manifest entries.

A separately written script imports no producer code. It verifies all ten external payload bindings and checks:

- 7,020 signed-offset cyclic Schreier graphs using union-find, rather than the producer's breadth-first spanning-tree implementation;
- 28,080 positive and negative character scaling cases;
- 1,085 incidence-matrix ranks by exact rational Gaussian elimination;
- 6,936 bounded normal-form kernel checks for rank-one inversion monodromy, covering the Klein bottle alternative to Z squared;
- 24 rank-zero sign controls;
- 1,705 exact reduced-word checks for the nontrivial automorphism x maps to x, y maps to yx.

The last family checks the stable-letter change yielding base generated by x and t, isomorphic to Z squared, with edge generated by t and other edge image generated by xt. The relation y-inverse t y = xt follows from the original mapping-torus relations, and the converse presentation recovers them. This is a useful nonfree-base example. It is not evidence that a finite example list proves the general theorem.

Negative controls distinguish an unnormalized factor from the correct one, distinguish b1(1) from negative chi2(1), and identify the zero-character normalization obstruction. The mathematical direct-product graph formula is correct: when phi(w,z) = a(w) + qz and q is nonzero, projection identifies the kernel with the congruence subgroup of F_n, of index absolute(q)/gcd(a_i,q). Its free rank is `1 + (absolute(q)/gcd(a_i,q)) * (n - 1)`. For q = 0 the frozen packet correctly states that the cell arithmetic does not compute infinite-dimensional L2 homology.

These are deterministic finite consistency controls. They neither establish the all-automorphism theorem nor replace the primary-source proof chain.

## Nonblocking observations

1. Frozen `CHECK_RESULTS.json` says `manifest_payload_files_checked: 0`, whereas fresh replay says 9. All other captured result fields agree in source mode. The producer's snapshot was evidently taken before creating the internal manifest; the snapshot itself does not claim a manifest pass. The independent replay and external frozen-manifest check now supply that missing packaging check. No frozen rewrite is required.
2. The supplied script conditionally skips the internal manifest if that file is absent. Accordingly it is not a stand-alone authenticity checker for an incomplete directory. This does not affect the audited release: the external binding confirms the manifest exists and every payload matches. The audit's independent script requires the external manifest and exact file set.
3. `STATUS.json` retains pending independent-audit/root-acceptance fields because it is frozen producer output. This separate audit supplies its recommendation; root acceptance remains a distinct decision. There is no authority here to silently mutate the frozen record or any remote destination.

## Final disposition

Accept the frozen mathematical application as an accurately attributed existing-preprint resolution of the normalized **nonzero** target. Recommend `already_solved`, with `1/5` reflecting the producer's one substantive literature-verification turn. Do not describe this as a new proof, peer-reviewed resolution, literal solution for zero characters, or computation-certified theorem. Keep the specified preprint dependency, character qualification and rank-zero treatment with the disposition.

No remote writes were performed by this auditor. Original frozen files remain unchanged. Audit results apply only to the external frozen-manifest hash recorded above.
