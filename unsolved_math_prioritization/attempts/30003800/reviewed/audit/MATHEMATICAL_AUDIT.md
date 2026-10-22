# Independent audit of the mixed type unramified cohomology report

Problem 30003800, OWR-16162-015, rank 872. Audit date: 6 October 2026.

## Decision

**Accept the frozen author's report as a correct bounded partial result. No mathematical correction is required.** The disposition remains **unsolved, 5/5 approaches**. Acceptance applies to the characteristic-zero reductions, the stated vanishing family, and the lifting diagnostic. It does not accept a solution of the general mixed-type problem, a counterexample, a positive-characteristic result, a novelty assertion, or a certification of worldwide openness.

This is a separate AI-assisted adversarial mathematical review, not human peer review or formal verification. The published theorems remain external inputs. Their hypotheses and relevant statements were checked in primary manuscripts; the audit does not independently reprove their entire published proofs. No additional substantive approach to the unsolved problem was introduced.

## Frozen object and independent checks

The accepted object is the exact six-file archive `MIXED_UNRAMIFIED_30003800_AUTHOR_SAFE_FREEZE.zip`, SHA-256 `a997d734cdb3d8bde955db0547b5a7619dc37aa0452a2d179b4d913fb7613130`, 15,049 bytes. Its external manifest has SHA-256 `1a3e46334f8fe2ffa54d66f3781faa484a58b96e5e626a490fbc0a1c2262244d`.

The archive inventory, every member's byte count and digest, and identity with the supplied author files were verified before substantive review. There are six Markdown or JSON files and no executable member. No author-supplied code was run. The `author/` directory in this audit archive preserves those six members byte for byte, including the historical pre-review status.

All three complete supplied corpus files were read and parsed. Their full-file pins, the exact statement hash, and the complete problem-and-report-pair digest were independently reproduced. The pair digest is `7622d4021966d37c3c6d851d3943247753b892fb53844329bb44dfb50aa07470`. The complete inherited report is empty. The dated background literature assessment is not a mathematical proof. The data and source extracts are excluded from this deliverable. The author's historical GitHub eligibility query counts were retained as provenance, not independently rerun or treated as mathematical evidence.

Seven supplied primary-source PDFs match the author's public hashes and byte counts. Fresh text extraction reproduced the six pre-existing extracts exactly; the seventh was also freshly extracted. Relevant primary pages were examined, including source page images. Primary web versions and publication metadata were checked during this review. Local PDF hash verification is distinguished from web retrieval: the latter was not represented as a fresh byte-identical PDF download. Integrity checks are provenance evidence, not mathematical proof.

## Original question and permitted scope

Baek's contribution in Oberwolfach Report 21/2018, printed pages 1266-1268, concerns degree-three invariants with Q/Z(2) coefficients. Question 2 allows arbitrary Dynkin components of a semisimple group over an algebraically closed field. It therefore includes central identifications between unlike components. The immediately preceding theorem says characteristic zero; the question does not repeat that qualification. The frozen report makes its own characteristic-zero restriction explicit and leaves positive characteristic unresolved. This accurately preserves the distinction between the extracted question and the partial result. [Official report](https://ems.press/content/serial-article-files/46742)

The report year is 2018 and the EMS publication date is 12 April 2019. That bibliographic discrepancy does not alter the target. The live problem-page retrieval failed during this audit, so its present contents were not verified. The pinned complete record and official source control the statement reviewed. [EMS metadata](https://ems.press/journals/owr/articles/16162)

## External inputs and exact theorem boundaries

The following source checks are sufficient for the deductions below.

- Merkurjev's reductive-group manuscript, Proposition 4.1, connects unramified invariants with unramified cohomology of the generic classifying field. Corollary 6.3 gives the required product additivity. Proposition 7.1 covers a finite central diagonalizable kernel prime to the coefficient prime. Theorems 8.4 and 11.3 respectively give simple-group vanishing and odd-primary vanishing over an algebraically closed field, away from its characteristic. [Primary manuscript](https://www.math.ucla.edu/~merkurev/papers/unramnew2.pdf)
- Merkurjev's type-A Theorem 1.2 applies to all reductive groups whose Dynkin components are of type A over an algebraically closed field of characteristic zero. It is not limited to a single rank. [Primary manuscript](https://www.math.ucla.edu/~merkurev/papers/typeA3.pdf)
- Baek's B/C/D Theorem 1.2 has three separate displayed forms, one each for a product of B, C, or D factors, with arbitrary central subgroup. It does not assert vanishing for arbitrary simultaneous B+C+D couplings. The v4 manuscript's characteristic-zero hypothesis is satisfied. [Primary manuscript](https://arxiv.org/pdf/1801.08845)
- Baek's exceptional manuscript, Corollary 4.3, permits an arbitrary central subgroup of (Spin_12 x SL_2)^n, n at least one, over an algebraically closed field of characteristic different from two, and gives vanishing of the 2-primary unramified subgroup. Lemma 5.2 supplies the E7-only precedent for the central diagram. Theorem 5.4 allows mixtures among exceptional types. Numbering is that of the inspected 2019 manuscript, not a claimed identification with the final publisher PDF. [Primary manuscript](https://arxiv.org/pdf/1906.02087)
- Petrov's Theorem 1 concerns the image of the D6+A1 subgroup in adjoint E7. Its surjectivity at two explicitly means a finite odd-degree separable extension and a torsor preimage. This is not a statement only about strongly inner torsors or a 56-dimensional representation. The preceding construction identifies the subgroup in simply connected E7 as a central quotient of Spin_12 x SL_2. Its characteristic hypothesis is harmless here. Theorem 1 in the inspected v2 and Baek's reference to Proposition 1 are a numbering discrepancy, not different required assertions. [Primary manuscript](https://arxiv.org/pdf/1309.7325)

## Functoriality and the classifying field

The author's U(G) is the unramified subgroup of H^3(F(BG), Q/Z(2)), defined using all discrete valuations trivial on F. It is not the entire field cohomology group, a topological cohomology group, or merely the subgroup with no residues on one chosen affine model.

The generic-torsor identification legitimately lets the proof work with natural transformations H^1(-,G) -> H^3(-,Q/Z(2)). For a homomorphism f:S->G, pullback is the operation alpha -> [y -> alpha(f_*(y))]. An invariant whose every value is unramified remains so after this operation. This explanation is important: arbitrary subgroup maps need not be justified by an unexamined inclusion of classifying function fields. The report uses the invariant functor, which provides the required map.

All coefficient groups are torsion. Their primary decomposition therefore applies element by element. Since F is algebraically closed, its positive-degree Galois cohomology vanishes, so no constant summand has been discarded improperly. Extension fields K/F used to test torsors need not themselves be algebraically closed; the arguments quantify over those fields rather than just F-rational torsors.

**Finding:** the comparison and pullback steps are valid under the stated hypotheses.

## Direct products and central partitions

Lemma 3.1 correctly obtains U(G1 x G2) as the direct sum of the two U groups. The product formula for invariants supplies the algebraic decomposition. Restriction to each factor preserves unramifiedness; conversely each pulled-back unramified summand has zero residues, hence so does their sum. Constants cause no issue over F.

Lemma 3.2 is a quotient statement with an exact kernel computation. If N is the product of its intersections with the block centers, the product of the block quotient maps has kernel N, so it induces the asserted isomorphism. No argument from a disconnected Dynkin diagram alone is used.

The parity subgroup in (Z/2)^3 has four elements, surjects to every two-coordinate projection, and has trivial intersection with each individual coordinate subgroup. Thus pairwise projections do not recover the subgroup as a product. This is an exact structural calculation, not experimental evidence for a cohomology theorem.

**Finding:** both lemmas and the limitation of pairwise tests are correct.

## The central two primary reduction

Let Z be the full center of G_sc and mu a subgroup of Z. In characteristic zero, mu has its canonical primary decomposition as a finite diagonalizable group. The natural map G_sc/mu_2 -> G_sc/mu has kernel mu/mu_2, whose order is odd. The cited prime-to-two isogeny result therefore identifies their 2-primary unramified invariant groups. Odd-primary vanishing applies to both semisimple groups, giving the claimed isomorphism of the full U groups.

For any simple factor with odd-order center, the projection of mu_2 to that center is trivial. Consequently these factors split off from G_sc/mu_2 as an actual direct product. They can then be removed using the product lemma and simple-group vanishing. This argument does not assert that the original mu was coordinatewise, or that the original quotient already split.

The listed remaining types match the center orders. A_n has center of order n+1, so precisely odd n can remain; B and C have order two; D has order four, possibly cyclic; E7 has order two. E6, G2, F4, E8 and even-index A types have odd-order or trivial centers. Small-rank identifications do not create extra cases. In particular, the proof does not replace a cyclic order-four center by an elementary abelian group.

**Finding:** Proposition 4.1 is valid, including arbitrary coupled mu. It proves a reduction, not vanishing of the residual group. Calling the obstruction 2-primary does not require assuming that it has exponent two.

## Common central kernel lifting

The main adversarial concern in Lemma 5.1 is whether a torsor lift on the quotient can be made to equal the given G-torsor, rather than merely have the same adjoint image. The report handles both stages.

First take x in H^1(K,G), pass to an odd-degree separable L/K, and choose ybar in H^1(L,Sbar) with image xbar_L. The two central extensions have the same kernel A and the identity map on that kernel. Naturality of the obstruction maps therefore makes delta_S(ybar) equal to delta_G(xbar_L). The latter is zero because x_L exists. Exactness provides an S-torsor y lifting ybar.

Second, f_*(y) and x_L lie in the same fiber of H^1(L,G)->H^1(L,Gbar). For a central extension, H^1(L,A) acts transitively on that fiber. The compatible action on H^1(L,S) maps to this action by the identity on A. Acting on y by the required A-torsor therefore changes its image to x_L itself. This step would fail if the two kernels were silently replaced by different coordinatewise kernels. They are not.

All central groups in the application are finite and etale in characteristic zero. Galois or fppf cohomology gives the same needed extension statements here. No vanishing of H^2(L,A) is assumed; only the specific obstruction vanishes. No claim of surjectivity before the odd-degree extension is needed.

**Finding:** Lemma 5.1 is correct and retains the obstruction relations that couple the factors.

## Odd degree detection and Proposition 5.3

For detection, if alpha pulls back to zero and x_L=f_*(y), naturality gives res_(L/K)(alpha(x))=0. Applying corestriction gives [L:K]alpha(x)=0. Each value has finite order a power of two. An odd integer is invertible modulo that order, so alpha(x)=0. This works for every K and x and needs neither a common extension L for all torsors nor a uniform exponent bound. Pullback preserves the unramified subgroup by the functorial argument above.

For Proposition 5.3 put Z0=Z(R) x Z(E)^a and A=Z0/mu. A subgroup P of maximal rank contains a maximal torus of E and hence Z(E); this also follows from the cited explicit subgroup description. Thus mu lies in R x P^a, and S=(R x P^a)/mu is a subgroup of G=(R x E^a)/mu.

Taking the quotient by this very A gives exactly

    S/A = R_ad x (P/Z(E))^a,
    G/A = R_ad x E_ad^a.

The R_ad coordinate is the identity map. For each E_ad coordinate Petrov provides a preimage after an odd-degree extension. Applying this successively produces a finite tower with odd total degree; torsor lifts already constructed are simply restricted along later extensions. This proves the quotient-level surjectivity needed by the common-kernel lemma. It imposes no independent-factor condition on mu.

Finally let C=R x Spin_12^a x SL_2^a and let C->R x P^a be the central covering. Its inverse image nu of mu is finite. For any geometric point u of nu, its commutator with a point of the connected group C lies in the finite etale kernel. The commutator morphism from C to that kernel is constant, and its value at the identity is one. Thus every such u is central; in characteristic zero this proves centrality of nu as a subgroup scheme. The resulting quotient is S=C/nu, as claimed.

**Finding:** the injection U(G){2}->U(S){2} and the classical central-quotient description both pass. The argument keeps arbitrary mixed central identifications. Corollary 5.4 is therefore the stated equivalence of universal vanishing questions in characteristic zero. Its classical direction remains an assumption, not a theorem proved here.

## Unequal multiplicities and Proposition 6.1

Write H=(Spin_12^b x SL_2^c)/mu and take n=max(b,c). When n=0 the group is trivial. Otherwise add the simply connected missing factors

    D=Spin_12^(n-b) x SL_2^(n-c).

Embed mu into the enlarged product by assigning the identity in every added coordinate. After permuting factors, the enlarged quotient is (Spin_12 x SL_2)^n/mu', where mu' is still an arbitrary permitted central subgroup, and is also canonically H x D.

Baek's corollary kills U(H x D){2}. For the projection p:H x D->H and identity section i:H->H x D, one has p composed with i equal to the identity. On invariant groups this gives i^*p^*=id. Both maps preserve unramifiedness, so p^* is injective on U(H){2}; its target is zero. This checks the direction of both maps and does not require knowing U(D)=0 separately. It covers b=0, c=0, and all unequal positive multiplicities.

For E7 factors, Proposition 5.3 maps the group into a central quotient of Spin_12^(a+b) x SL_2^(a+c), to which the previous argument applies. Odd-primary vanishing completes the passage from the 2-primary statement to full U. Proposition 4.1 permits any number of odd-center simple factors and arbitrary central identifications with them, since it first removes the odd part of the kernel and then splits those factors off.

**Finding:** Proposition 6.1 and the odd-center extension are valid for every a,b,c at least zero, under the report's characteristic-zero convention. This is a deduction from credited inputs; novelty is neither needed nor asserted.

## The B3 plus C3 diagnostic

For H=(Spin_7 x Sp_6)/diag(mu_2), the map to SO_7 x PSp_6 has kernel (mu_2 x mu_2)/diag(mu_2). Multiplication identifies that quotient with mu_2. Pushing forward the pair of central two-cocycles therefore sends the two Brauer obstructions to their sum. Because H^2(K,mu_2) identifies with Br(K)[2] over a field of characteristic different from two, a pair lifts exactly when the displayed sum is zero.

In K=F(x,y), Q=(x,y) is nonzero: its residue at the x-adic valuation is the nonsquare class of y in F(y), and the y-adic valuation proves that nonsquareness. The degree-six central simple algebra M_3(Q) equipped with transpose tensor quaternion conjugation has a symplectic involution, so it defines the proposed PSp_6 torsor. The natural map from the symplectic central extension to the general linear/projective linear extension identifies its boundary with the Brauer class of its underlying algebra, namely [Q]. The trivial SO_7 torsor has zero boundary. Their pair consequently does not lift to H.

Splitting Q by a quadratic extension can remove that degree-two obstruction, but corestriction then gives multiplication by two, which is not injective on 2-primary torsion. The report correctly uses this only to explain why that detection method no longer follows. It does not assert that every even-degree restriction has nontrivial kernel.

**Finding:** the diagnostic is sound and is not a counterexample to the original question. It constructs neither an H-torsor with a nonzero degree-three unramified value nor an element of U(H). No value of U(H) is determined.

## Status and remaining gap

The five listed approaches match the report's actual work. General coupled classical central 2-primary quotients remain outside the proved families, and no argument constructs compatible ramification witnesses for all their possible degree-three invariants. Nor is there a proposed nonzero class proved unramified at all valuations. The positive-characteristic question, particularly the characteristic-primary part, is not resolved.

Current primary pages for the cited manuscripts and author publication lists did not yield a full resolution in this bounded review. The 2022 Colliot-Thelene list asks an additional base-extension question in Problem 7.8; it cannot certify that this target is open. The September 2026 Scavia-Suzuki abstract concerns finite-field varieties and related cycle maps, not an asserted general mixed-classifying-space theorem. Only its abstract and submission metadata were used. These checks support the report's cautious search statement, not worldwide current openness. [Problem list](https://www.imo.universite-paris-saclay.fr/~jean-louis.colliot-thelene/JLCTlistePb10dec22.pdf) [Recent preprint](https://arxiv.org/abs/2609.36188v1)

No numerical test, finite enumeration, or executable mathematical checker is offered as evidence for any universal assertion. No mathematical blocker or required correction was found. The unchanged frozen author object is accepted only with its existing bounded, unsolved disposition. Publication was not performed.
