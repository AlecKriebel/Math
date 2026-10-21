# Fresh independent full-package adversarial review: PR1102 / problem30006658

**Verdict: PASS. No actionable finding or required repair identified.**

Review date: 17 October 2026. Completion estimate: **100% of the assigned bounded mathematical/publication-package review**. This is a review completion estimate, not a probability of correctness or universal novelty. No publication, branch change, commit, remote mutation, outreach, or final-artifact modification was performed.

## Independence and exact reviewed target

The sole target was the existing frozen publication package for PR1102 / problem30006658. The proof in publication/main.tex was reconstructed independently and the reconstruction was recorded in INDEPENDENT_DERIVATION.md at 16:47 UTC before reading package_round1 reasoning. **No package_round1 reasoning has been read at all.** The included older hopf_01 and topology_01 audits were read only after the independent reconstruction and the central checks. The included bounded priority report was examined as a report to be audited, not accepted as a source of mathematical truth.

The theorem is: for every compact Lie group G with non-p-nilpotent component group and every characteristic-p field k, the canonical map from the k-cellularization of C_*(Ω((BG)^∧_p);k) to that algebra is zero on every homotopy group. It is the full map, with completion before looping; it is neither derived nullity nor projection to component-group homology. The literal [OWR Question 2.2, printed p. 594](https://ems.press/content/serial-article-files/53607?nt=1) asks the positive-dimensional part of precisely this claim. Including finite groups is harmless and is explicitly credited prior work.

## Mathematical falsification attempts and evidence

| Mechanism challenged | Independent resolution | Remaining gap |
|---|---|---|
| Finite coefficient envelope J may be infinite or fail the coideal condition | Coproducts of a finite basis of I have finitely many first factors. Counit gives I⊂J; coassociativity gives ΔJ⊂J⊗B. | None |
| Right-ideal closure may use the antipode in the wrong order | The formula expands to Σi₁b₁ f(i₂b₂S(b₃)), contracting to Σi₁b f(i₂). It uses S, never S^{-1}. | None |
| Shortened counit finish may be circular | If ε(J)=0, (ε⊗1)Δ annihilates every j∈J, contradicting nonzero J. Scale ε(j)=1; Δj∈J⊗B and right ideal closure put Σj₁S(j₂)=1 in J. Hence J=B. | None |
| Left ideals may require an invertible antipode | Reversing both multiplication and coproduct yields B^{op,cop} with the original antipode. Its two antipode identities are exactly the two original identities. | None |
| Odd signs and characteristic 2 | Characteristic 2 genuinely erases Koszul signs. Otherwise parity bosonization has the stated product, coproduct and antipode. Both antipode identities were expanded independently, with the signs cancelling as required. Coassociativity gives the same three group exponents on both sides. | None |
| Bosonization may fail to preserve an ideal side | Multiplication by h#g^i on either side preserves I⊗kC₂ on the corresponding side, because I is graded. Finite dimension of homogeneous pieces and connectedness are not used. | None |
| Noncompact k or unbounded modules may invalidate finite approximation | Morita theory uses compact K, not k. A semifree E-module has finite differential dependency closures by finite branching and well-founded descent. Their filtered union is a derived filtered colimit of finite semifree modules. Tensoring with K preserves it. | None |
| Finite class representatives may not have finite TOTAL homology | Every stage lies in thick(K)⊂thick(k). Finite sums, shifts, cones and retracts preserve finite total k-homology. Exact filtered colimits make every individual homology class accessible. No single finite stage for the whole cellular module is claimed. | None |
| Homology image may be only a subspace | A-linearity into the regular module makes the entire homology image a graded left ideal. The finite-stage image therefore vanishes by the Hopf lemma. | None |
| DGI may require orientability or a nilpotent component action | DGI §5.7 states completed-loop proxy-smallness for every compact Lie group over F_p. The finite homogeneous-space construction, goodness, finite p-group π₁ after completion, and §4.22/Proposition 4.17 supply the stated hypotheses. | None |
| Arbitrary characteristic-p fields may require commuting infinite cochain duals with scalars | The paper extends CHAINS and a compact proxy from F_p. Flat scalar extension preserves perfect construction, localizing construction, and infinite total homology dimension. No infinite cochain-dual exchange occurs. | None |
| Disconnected ΩX may fail the Hopf hypothesis | A loop-group model gives the antipode; field Künneth has no finite-type requirement. H₀ may be a nontrivial group algebra, which the lemma allows. | None |
| Ishiguro may be used backwards or with a different completion | Its definition at p. 195 and Proposition 1.3(a), p. 199 give the necessary implication for Ω((BG)^∧_p). Only its contrapositive is used. The false converse is not assumed. | None |

The finite-dimensional boundary A=k has identity cellularization, consistently excluded by the infinite-dimensional hypothesis. Connected compact Lie groups and p-nilpotent finite groups are outside the theorem's antecedent. No claim about arbitrary coefficient rings is made. The proof never identifies the source with an untwisted dual, so orientability is absent for a mathematical reason.

The strongest verified result is the theorem as stated, and the more general algebraic proposition that every A-linear map from a k-cellular source to A vanishes on homology when k is proxy-small and H_*(A) is an infinite-dimensional graded Hopf algebra. No remaining mathematical gap was identified.

## Primary sources and credit

Fresh downloads of the four cached primary PDFs matched their local bytes: OWR, DGI, Ishiguro, and Lomp. Fresh Greenlees v3 and BIS published PDFs were also obtained; retrieval timestamps, lengths and hashes are in primary_sources/RETRIEVALS.json. Redundant reading copies were later removed under disk-space pressure, preserving this receipt; the originally cached first four primary PDFs remain outside this review.

* [DGI, publisher-version mirror](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf): Definition 4.6, Remarks 4.7–4.8, Theorem 4.9 and its use with K in the proof of Theorem 4.10, Proposition 4.17, §4.22 and §5.7 were inspected. The paper accurately states their scope.
* [Ishiguro](https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf): definition and Proposition 1.3(a) were inspected. The 2007 author's restatement suffices; the 2001 original was not independently inspected.
* [Lomp §2.4](https://arxiv.org/pdf/math/0307046): the ordinary one-sided finite-ideal theorem and Sweedler credit are present. The note properly calls the theorem classical. It does not claim to have directly read Sweedler's original body.
* [BIS, published article](https://nyjm.albany.edu/j/2025/31-26p.pdf): Definition 2.1/Ind-completion and Lemma 4.1 proof support filtered-perfect approximation; this is correctly treated as existing machinery.
* [Greenlees v3](https://arxiv.org/html/2504.03050v3) and the actual [published HTML](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.70405) were independently inspected. The browser displayed the published Lemma 6.5 and Remark 6.6 formulas after section navigation. Finite groups are prior work; the compact-Lie results retain nilpotent-action/restricted-image or tensor-collapse conditions. The note's comparison is accurate. The current arXiv abstract still identifies v3, 27 April 2026, as latest.
* The official OWR text establishes the question, coefficient field, and completion convention. The surrounding orientability assumption concerns a duality identification, not an obstacle to the independent proof.

The included priority report distinguishes established ingredients from the connecting consequence and expressly limits its search. The preprint makes no unsupported exhaustive-priority or new-Hopf-theorem claim. No priority defeat was located in this bounded review. Unindexed or unpublished prior work remains possible; that is a literature-search limitation, not an identified defect or required signoff.

## Actual package, verifier efficacy, and PDF consistency

audit_archive.py inspected the ACTUAL upload kit and nested source archive, not merely the surrounding directory. integrity_checks.json records successful checks of every PACKAGE_RECEIPT file entry; every internal SOURCE_MANIFEST member name, byte count and hash; every archive CRC; absence of duplicate or traversal member paths; matching metadata; resolving deposit-relative upload paths; identical source main.tex; identical copies of the PDF in all three places; and PROVENANCE's pinned report hash.

The source archive contains the complete TeX proof, bibliography, license, README, PDF, verifier, expected output, and the advertised mathematical/priority audit evidence and public source locators. Its source manifest deliberately does not hash itself. Third-party source bodies, credentials and unrelated data are absent. The archive is sufficient to rebuild the PDF and rerun every computation on which it advertises reproducibility. The proof itself has no computational dependency.

The actual archived standard-library verifier returned exactly the expected JSON over F₂,F₃,F₅. Per field: 512 associativity triples; 676 coproduct multiplicativity pairs; 80 coassociativity/counit inputs; 80 two-sided antipode inputs; 208 products on each ideal side; and the odd-sign negative control. Inspection confirms that input word length is bounded but operations are not truncated. Optimized Python explicitly exits unsuccessfully. Five independently made formula mutations all failed assertions without printing PASS; see negative_control_results.json and check_negative_controls.py. The ideal-membership tests exercise the advertised free-algebra example, not all ideals; this is consistent with the restrained claims in the paper. The analytic proof, not bounded testing, establishes the universal theorem.

The archived main.tex was rebuilt with Tectonic in the review's extraction directory. The resulting PDF has the same extracted text as the distributed PDF; each of its four 1600-pixel renders is byte-identical to the matching distributed render. All four distributed pages were visually inspected: no missing formula, clipping, overlap, missing citation, or disclosure omission was found. render_comparison.json preserves the evidence. The reviewed distributed PDF is four US-letter pages.

The author, affiliation and ORCID agree across TeX, README and metadata: Alec Kriebel, independent researcher, 0009-0001-9320-500X. Version 1.0.0 and 17 October 2026 agree. CC BY 4.0 is explicit and matches Zenodo's license. The metadata identifies a preprint and includes the exact theorem/scope. Extensive AI use and the AI nature of the reviews are explicit; unrefereed status and absence of external human peer review/formal certification are disclosed. No unsupported human endorsement is implied.

## Exact frozen artifact identities

| Reviewed artifact | SHA-256 |
|---|---|
| Distributed PDF | f11b2f3aa0e1aeec4c5971264e734c0458bd512cbb09e5e5ca11a60f0a037644 |
| Source/verification ZIP | 1aeab807b46af3836bcce647c6bd24be945c2f1b82fb710684d087538db51933 |
| Upload kit ZIP | 24358d7f6d49248e6abca8d3c90dc909b7217b3e7483d7e8c3a75985e457cab6 |
| main.tex | c051fdd5c20882305a04f61aaad4385f1e425c5a893e2c28fd914d8da979c6e0 |
| Internal SOURCE_MANIFEST.json | c5d2e78209778e82d2d2b04a8ff401a3e1fef87cfe876f0046eb09da40e3679a |
| Directory zenodo-deposit.json | e6053e430f5a325216513cf555cd981c290b09dd605985631b1dc444ac0048a5 |
| Kit-relative zenodo-deposit.json | 02514c83fde1dfd0b57fc590e00eb13f749f80611c780904f8ca4660f69b161f |
| zenodo-metadata.json | 98c6e61e5d3c4af5011d789babc02655e169a354295430c8fdf5ff43f590183e |
| PACKAGE_RECEIPT.json | 6eb95db89a7414770d23928805b900ca1a146751821176d72c3ad4e38777a4d7 |

The directory and kit deposit manifests intentionally differ only by their relative file paths; their metadata are equal and both paths resolve in their intended locations.

## Final disposition and exact limits

**PASS; actionable issues: none; required repairs: none; unresolved proof gaps: none identified.** This is an evidence-backed AI adversarial review of the exact identities above. It is not formal certification, external human peer review, or exhaustive novelty certification. No additional confirmation or expert signoff is required by this review. Publication remains the parent's responsibility under the user's authorization. A final-artifact change would require reviewing its changed content and identities.


Final frozen-hash recheck and completion timestamp: 2026-10-17T16:53:54.231196+00:00. All seven surrounding-file identities remained unchanged.
