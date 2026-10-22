# Priority audit of PR 1150: mixed-extension mechanism

Reviewer: independent mixed-extension priority family. Completed 2026-10-17 UTC.

**Disposition: no earlier recorded full resolution of the original three-kernel target was established in this review. The mixed generator used by the candidate is already present in ALO's 2019 manuscript, published in 2020, and must be credited at the exact definition/lemma level.** The checked candidate supplies a direct universal obstruction after the separate Pfister kernel is added. This bounded result does not certify firstness or that the question remained open worldwide until this PR.

The reviewed candidate is `REVIEWED_PROOF.md`, 12,322 bytes, SHA256 `7f63c1f6e4f79a78b979903db59e8030a8222266a65d296a4a6fc1a29a6e2e1b`. An immutable review copy is retained privately. No older audit, acceptance verdict, root report or sibling report was read. The task brief disclosed the candidate data and the likely ALO relationship. `INDEPENDENT_CORE.md` was sealed before opening the candidate; its external SHA256 is `2a12c154df2be3f459a4ecd0baad00148b7d92b56330a7e7e665ebb1640f5e05`.

## Exact target and scope comparison

The [original report](https://ems.press/content/serial-article-files/46609), printed p. 251, asks whether the kernel for `L K(B)/F` equals the sum of the kernels for `L/F`, `K/F`, and `F(B)/F`, assuming finite purely inseparable `L/F`, separable quadratic `K/F`, and a bilinear Pfister form remaining anisotropic over `L`. Its convention uses the projective quasilinear quadric. The whole contributing talk, printed pp. 248–251, was read; the target page was also visually inspected.

The candidate takes cohomological degree two, `L/F` of degree four and exponent two, and a genuine binary bilinear Pfister form. Thus one example disproves the universal assertion. It does not claim failure at every cohomological degree or for every extension.

| Primary result inspected | Relevant scope | What it establishes for this comparison |
|---|---|---|
| ALO, J. Algebra 449 (2016), author manuscript Theorems 1.1–1.2; complete proofs and subsequent Sections 6–8 | Exponent-one purely inseparable multiquadratic extensions, with separable quadratic and bilinear Pfister factors | The earlier positive regime. Replacing exponent one by a fourth root is outside its hypotheses. |
| ALO, [2019 author manuscript](https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf), Definition 1.3, Lemma 3.1, Theorem 1.4; complete Sections 1–6 | Higher-exponent simple purely inseparable extension composed with a separable quadratic extension | Supplies the mixed generator and its vanishing. The full-target exclusion modulo a third independent Pfister kernel is not recorded in these statements or proofs. |
| Same manuscript, Theorem 1.2 and Theorem 1.5 | Separable biquadratic factors; exponent-one splitting and higher-exponent mixed-kernel description | Different separable-degree generalizations; no recorded three-summand counterexample was found. |
| Same manuscript, Proposition 6.1 and Example 6.2; whole example proof | Composita of purely inseparable extensions | The example involves two purely inseparable factors. It cannot silently replace the target's separable quadratic factor. |
| ALO, [pure-extension author manuscript](https://laghribi.perso.math.cnrs.fr/kernels-modular-ext.pdf), dated 4 May 2016, Theorems 3.1 and 4.1 | Kernels of purely inseparable extensions of higher exponent | Supplies individual-kernel descriptions and cross terms, without the target's separable factor. Read scope is selective, not a claim to have reverified its entire proof. |
| Sobiech, arXiv:1512.02079v5, Theorem 3.13 and Corollary 3.15 | Purely inseparable kernels in arbitrary positive characteristic | Independently antecedent individual-kernel tools; no direct full-target result identified in the inspected scope. |
| Aravire–Jacob–O'Ryan, [PJM 306 (2020)](https://msp.org/pjm/2020/306-2/pjm-v306-n2-p01-s.pdf), Theorems 4.1–4.2, Corollary 4.3 | Purely inseparable kernels with Witt-vector coefficients | Different coefficient-length and separability scope. The modular splitting corollary requires the coefficient length to meet the extension exponent. It is not a positive theorem contradicting the degree-two candidate. |
| Bingöl–Chapman–Laghribi, arXiv:2406.14339v2, complete mathematical body, especially Proposition 2.6 and Example 3.3 | Symbol-length bounds and nonexcellence for mixed multiquadratic splitting fields | Nearby field constructions, but neither the original three-kernel equality nor its negative instance is recorded in this inspected body. |
| Laghribi–Maiti, arXiv:2503.16859 and 2504.15957, introductions and Theorem 1.1 in each; full-text keyword screening | Rational-function cohomology via residue and transfer sequences | General tools. This review did not identify an application recording the original target consequence; the whole proofs were not read. |

## Exact antecedent of the submitted class

Here is my own specialization calculation, rather than an inference of novelty from terminology. Use ALO's Definition 1.3 with its extension parameter `n=1`, differential degree `m=1`, and `f=1+beta^2 z`. Its two coefficient entries can be chosen as `1,z`. The first entry contributes no logarithmic differential. The second contributes

`((beta^2 z)/(1+beta^2 z))^2 dlog z = (b z^2)/(1+b z^2) dlog z`.

This is exactly the differential multiplied by `s^(-4)` in the candidate. The Artin–Schreier representatives `s^(-4)` and `s^(-1)` define the same quadratic extension: their sum is the Artin–Schreier image of `s^(-2)+s^(-1)`. Theorem 1.4's displayed power hypothesis holds with its `l=2>1`; Lemma 3.1 already gives the needed containment. The current author's direct computation of vanishing agrees with this antecedent.

**Required publication credit:** identify this as a specialization of ALO Definition 1.3 and Lemma 3.1, also appearing in their Theorem 1.4 kernel formula. The weaker phrase “consistent with” in the present introductory paragraph should be strengthened in the eventual publication package. Do not present the mixed class, the mixed-kernel phenomenon, or its membership as newly discovered mathematics. This is a credit/presentation requirement; it does not invalidate the direct proof.

## Why two-field nonsplitting does not by itself dispose of this target

Write `A=ker(H(F)→H(L))`, `C=ker(H(F)→H(K))`, and `P=ker(H(F)→H(F(B)))`. Even if an earlier class lies in `ker(H(F)→H(LK))` outside `A+C`, it might belong to `A+C+P`. Adjoining the Pfister function field enlarges the right-hand side as well as the left-hand side. A symbol killed by that field supplies the simplest warning. In the submitted setting, taking the Pfister slot to be `z` would kill the differential outright.

Moreover, the appearance of a separately named group in a sum formula does not prove that group is not contained in the other summands. I did not turn the notation `a G_L^1(1)` into an unproved strictness assertion. The earlier mixed paper's discussion announces the failure of splitting in its setting; that antecedent remains material even when a particular universal nonmembership proof is supplied separately.

To obtain this PR's exact conclusion one needs an admissible nontrivial `B`, its anisotropy over `L`, and survival modulo the new kernel. I checked the candidate's proposed bridge directly. Restriction to `M=L F(B)` annihilates the first and third summands. A putative membership then makes `[s^(-1),f/c)` split over `M` for some `c` in the original base. Completion at `s` turns this into a norm condition for a totally ramified quadratic extension. Its unit norms have square residues. Consequently the residue of `f/c` would give

`1+beta^2 z = q(u+vz)`,

with `q` in `F_2(beta^2,z^2,gamma^2)` and `u,v` in `F_2(beta^4,z^2,gamma^2)`. Linear independence of `1,z` over the former field forces `beta^2=v/u` in the latter field, contradicted by the `beta^2` valuation. This excludes all base-field scalars, not a bounded test set. The independent slot `t=gamma^2` is fully present throughout.

That explicit argument establishes the missing third-kernel survival. A new generic-extension or specialization bridge from older results would also require a proof and attribution; its availability alone would not demonstrate that an earlier source recorded the original question's full answer. I found no such recorded bridge in the complete core bodies reviewed here.

The binary projective function field is exactly `F(sqrt(t))`. The 2016 predecessor instead uses affine quadrics. In the binary case the affine field is one rational variable over that projective field, so their kernels agree by rational-extension injectivity (the predecessor's Proposition 7.6). This convention difference creates no escape from the target and no unsupported substitution of a zero-fold form.

## Later correction and access limits

A search for corrections found a relevant but separate precision in Sobiech, [J. Algebra 604 (2022), DOI 10.1016/j.jalgebra.2022.04.011](https://doi.org/10.1016/j.jalgebra.2022.04.011), arXiv:2105.01319v2. The paragraph following Theorem 4.4 flags a base-field coefficient issue in ALO's published pure-extension Theorem 5.5. I read that theorem's whole proof and surrounding remarks, and visually checked printed p. 14. This concerns a description of the **differential-form kernel** for nonmodular purely inseparable extensions, not a correction to the candidate's cyclic-algebra norm argument. The candidate does not invoke that disputed description. The old author copy inspected here has no Theorem 5.5, so I do not pretend to have compared that published statement with its proof.

The author-site mixed manuscript is dated 15 August 2019. Its association with J. Algebra 542 (2020), 249–276, DOI `10.1016/j.jalgebra.2019.09.012`, is confirmed by the author publication list, Crossref's publisher-deposited metadata, and HAL's metadata API. HAL records 15 January 2020; Crossref's creation date is 30 September 2019 and its publication field has January 2020 precision. Creation is not being called publication, and the current URL's presence does not prove it was online on the manuscript date.

The mixed paper's publisher endpoint returned 403 and its public text endpoint 429; the HAL document link returned an HTML bot challenge, not a PDF. Accordingly, **the final journal body was not obtained or compared line by line**. The authenticated, completely read author manuscript is the mathematical evidence used here.

The non-normal-extension paper, DOI `10.1080/00927872.2019.1686510`, is directly adjacent literature. Its publisher abstract and bibliographic record were available through web search, but its full body returned 403. It treats quadratic or quartic purely inseparable extensions over a separable quadratic subfield and therefore has mechanism overlap worth disclosing; its unseen proofs were not cleared by this review. Likewise the 2022 transfer article, DOI `10.1016/j.jpaa.2021.106930`, was screened through its primary abstract, not a read of its full body. These are access limits, not evidence that either paper resolves or fails to resolve the exact target.

The 2025 rational-cohomology papers were screened at their statements, introductions, and text searches. The complete mathematical body of the short mixed-splitting paper was read, but its final published typesetting was not fetched. No relevant correction to the mixed-paper DOI itself was located in 47 executed queries; this is a bounded negative finding, not an absence theorem. Secondary aggregators were used as leads only, never for a theorem-level conclusion. No person was contacted, and no outreach was prepared.

## Conclusion for the parent audit

Continue the publication review if the other independent families and root review agree, with exact ALO mechanism credit and the stated access/priority limitations retained. This family does **not** support reclassifying the PR as an earlier recorded full-target resolution. It also does **not** support a first-solution, still-open-worldwide, or independently rediscovered-origin claim.

This was a priority family review, not either of the required final whole-package adversarial reviews. It authorizes no publication or PR action. All external bodies, extracts, renderings, snapshots, and raw web material remain in ignored directories. The receipt has no self-hash dependency; its external seal is supplied in the final handoff.
