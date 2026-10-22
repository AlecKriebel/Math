# Final-package adversarial review, round 1: PR #1102 / problem 30006658

Timestamp: 2026-10-17T16:45:34+00:00.
Assigned audit completion estimate: **100%**. Best-guess completion of the stated mathematical discovery: **100%**, in the limited sense that the full target has a checkable proof with no unresolved proof obligation identified in this review. This is not a probability of correctness or exhaustive priority certification. Subsequent publication workflow is outside this assignment.

**Verdict: PASS. No concrete actionable mathematical, attribution, metadata, archive-integrity, reproducibility, or PDF defect found. No required repair is identified.**

This is an independent AI adversarial review of the actual final package, not external human peer review or proof-assistant certification. The final package was not edited. No repository branch/index change, commit, push, PR action, upload, or external communication was performed. All review outputs and private reading/build copies are in this folder.

## 1. Frozen inputs and review independence

I began with the actual two ZIP archives, rejected unsafe extraction paths and symbolic-link members, and extracted each into a separate private folder. Neither archive contained an unsafe member. The source archive contains 20 file members; the upload kit contains 5. The independent reconstruction and initial objections were saved in `INDEPENDENT_DERIVATION.md` before any included Hopf, topology, or priority verdict was read. Source-retrieval receipts were later read only to locate originals, which were freshly downloaded and independently inspected.

The reviewed source archive is SHA-256 `1aeab807b46af3836bcce647c6bd24be945c2f1b82fb710684d087538db51933` (109403 bytes); upload kit `24358d7f6d49248e6abca8d3c90dc909b7217b3e7483d7e8c3a75985e457cab6` (179786 bytes); PDF `f11b2f3aa0e1aeec4c5971264e734c0458bd512cbb09e5e5ca11a60f0a037644` (69097 bytes); main source `c051fdd5c20882305a04f61aaad4385f1e425c5a893e2c28fd914d8da979c6e0` (13093 bytes).

## 2. Mathematical claim and independent validation

The exact statement at `main.tex:26–40` is: every compact Lie G whose finite component group is not p-nilpotent, every characteristic-p field k, and every integer n satisfy H_n(Gamma_k R -> R)=0 for R=C_*(Omega((BG)^hat_p);k). Completion precedes looping. The full induced homotopy map is at issue; nullity of the derived morphism is explicitly excluded.

This matches [Greenlees's original OWR 9/2026 contribution](https://ems.press/content/serial-article-files/53607?nt=1), notation on printed p. 593 and Question 2.2 on p. 594. The source question has positive dimension. Including finite G is a consistent strengthening, with that already-known case credited. Orientability belongs to the surrounding duality description, whereas the submitted proof avoids that description.

My independent mechanism and falsification register is:

| Location in main.tex | Mechanism and adversarial check | Result and remaining gap |
|---|---|---|
| 51–71 | The coefficient envelope J of a finite nonzero right ideal is finite, contains I, and is a right coideal. Expanding the displayed contraction identity proves it is also a right ideal. Epsilon(J)=0 would force J=0; otherwise the antipode puts 1 in J. Applying op and cop together gives the left side with the original antipode. | Verified. No implicit cocommutativity, connectedness, or inverse antipode. Gap: none. |
| 73–84 | Characteristic two permits ungrading. For odd characteristic the parity smash product has the stated multiplication, coproduct and antipode. I independently derived both antipode identities, including their signs, and checked preservation of each ideal side. | Verified. A finite graded ideal embeds in a finite ordinary ideal without changing infinite dimension. Gap: none. |
| 89–103 | Compact K, rather than possibly noncompact k, generates Loc(k). Morita theory reduces to DG E-modules. Finite-support differentials and a well-order give finite dependency closures by the finitely branching tree argument. Finite closed semi-free submodules form a filtered system. | Verified for arbitrary/unbounded modules. Filtered homology makes each class come from a perfect stage; tensoring yields P in thick(K) with finite total k-homology. Gap: none. |
| 106–114 | An A-linear P -> A has its entire homology image a graded left ideal, of finite total dimension. This is stronger than merely knowing each homogeneous piece is finite. | Finite-ideal lemma forces that image to be zero, class by class. No unjustified factorization of the entire module/map is needed. Gap: none. |
| 119 | The compact-Lie proxy hypothesis must refer to completed loop chains for every G. | Direct source check confirms exactly this hypothesis. Gap: none. |
| 121–138 | Chains and the proxy extend from Fp to arbitrary k. Loop multiplication, diagonal and inversion provide a Hopf structure even for disconnected loops. Non-p-nilpotence must force infinite total homology. | Verified. No cochain dual/base-change interchange or completion/loop interchange. Gap: none. |

The direct primary input checks were:

- [Dwyer–Greenlees–Iyengar, published text](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf), Definitions 4.6/4.8, Theorem 4.9, Proposition 4.17, section 4.22, and section 5.7, especially printed p. 382. Section 5.7 explicitly takes arbitrary compact Lie groups, k=Fp, and X the Bousfield–Kan completion of BG. It proves cochain proxy-smallness using SU(n)/G, then uses finite p-group pi_1X, EM completeness, and Proposition 4.17 to obtain completed-loop-chain proxy-smallness. There is no orientability or component-action requirement. Theorem 4.9 can be applied with K as generator, as its own use in the proof of 4.10 confirms.
- [Ishiguro (2007)](https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf), printed pp. 195 and 199, Proposition 1.3(a). His definition uses the loop space of completed BG; finite total mod-p homology would give p-compactness and hence p-nilpotent pi_0G. Only this necessary direction is contraposed. The false general converse is never invoked.
- [Lomp, section 2.4](https://arxiv.org/pdf/math/0307046), confirms the classical finite one-sided ideal theorem and its Sweedler credit. The paper supplies its own direct proof and does not depend on an uninspected antipode-invertibility variant.
- [Briggs–Iyengar–Stevenson](https://nyjm.albany.edu/j/2025/31-26p.pdf), printed p. 709, Lemma 4.1 proof, explicitly uses filtered perfect approximation and tensoring. This corroborates the categorical step rather than supplying a hidden extra assumption.

Boundary checks include A=k (infinite-dimensionality fails and cellularization is the identity), finite p-nilpotent G, connected G, S_3 at p=3, and O(2) times S_3 at p=3. In the last case reflection acts by -1 on degree-two cohomology of the identity-component classifying space, so a nilpotent-action/orientability shortcut is unavailable; the present proof still applies. Arbitrary infinite or imperfect characteristic-p extensions retain the proxy and infinite dimension. Negative source degrees cause no problem, and disconnected Omega X need not have H_0=k. Dropping the field, antipode, or infinite-total-dimension hypotheses would invalidate the general criterion; none is dropped here.

## 3. Priority, credits, and disclosures

I read the included `audits/priority_01/PRIORITY_AUDIT.md` and its query, retrieval, and source ledgers after my independent derivation. It identifies a bounded dated search, records access limits, distinguishes current sources from stale bibliography, and does not claim exhaustive absence of earlier work. That is an appropriate level of priority evidence for the claims actually made.

I independently checked [Greenlees v3](https://arxiv.org/pdf/2504.03050v3), section 6, and the [live arXiv version history](https://arxiv.org/abs/2504.03050). V3 remains the latest listed version (27 April 2026). Lemma 6.2 is finite-group work; Lemma 6.5 has a nilpotent-action hypothesis and restricted vanishing; Remark 6.6 gives full vanishing under an extra tensor-collapse hypothesis. These support the precise credit at `main.tex:42`. The included audit reports independent inspection of the published HTML; I did not replicate that browser inspection because my direct Wiley web access failed. Fresh publisher-deposited [Crossref metadata](https://api.crossref.org/works/10.1112/blms.70405) independently confirms volume 58(6), e70405, and first online publication on 1 June 2026. No version/publisher byte-equivalence is claimed.

The paper credits Greenlees for the question and prior finite/restricted cases, Sweedler/Lomp for finite ideals, DGI for proxies/Morita, and BIS for approximation. It asserts the consequence answering the question, with no new general Hopf or Morita theory claim. No evidence of a priority defeat or unsupported stronger novelty claim was found. A universal priority proof or human referee signoff is not imposed as an additional requirement.

The title/date paragraph says unrefereed (`main.tex:17`), and `main.tex:143–147` explicitly discloses extensive AI involvement and that independent reviews are AI reviews. The paper does not claim external human review or formal certification. README and upload descriptions are consistent with this status.

## 4. Verifier efficacy and reproduction

The archived standard-library verifier was inspected and run. Its JSON exactly equals `verification/expected_results.json`. Over each of F2, F3, F5 it passes 512 associativity inputs, 676 bialgebra-multiplicativity inputs, 80 coassociativity/counit inputs, 80 inputs for both antipode identities, 208 left-ideal and 208 right-ideal products, and one ungrading control. All operations use the infinite free tensor superalgebra; word bounds restrict tested inputs and are not quotient/truncation relations. The paper and README accurately limit the computation to convention checks.

`python3 -O` exits with code 1 and the stated refusal, so optimized Python cannot silently skip all assertions and print PASS. In separate private copies I independently removed (one at a time) the bosonized product sign, coproduct group parity, super-coproduct sign, super-antipode crossings, and antipode group parity. **Every mutated verifier exits with AssertionError.** The tests therefore have actual sensitivity to the mathematical errors they purport to detect. These experiments are in `negative_control_results.json`; exact standard output is in `verifier_actual.json`.

## 5. Archive, metadata, and PDF checks

`integrity_checks.json` records zero source-manifest errors, zero unlisted source members, and zero package-receipt mismatches. Every source member hash and byte length matches. The receipt's source-members object equals the archive manifest. The outer and inner source ZIP are byte-identical; all three distributed PDF copies are byte-identical; archive and publication main.tex are byte-identical. The upload metadata matches the publication metadata and its deposit metadata. Both deposit manifests resolve every declared file: the kit deliberately uses root-relative paths, while publication uses output-relative paths. This is correct, not a mismatch.

Author Alec Kriebel, independent-researcher affiliation, ORCID 0009-0001-9320-500X, version 1.0.0, date 17 October 2026 / 2026-10-17, title, open access, and CC BY 4.0 agree across paper, README, license and metadata. The supplied ORCID matches the user's author metadata. Bibliographic DOIs/locators match the checked primary sources. No third-party source-body PDFs, credentials, internal coordination files or unrelated research are in either ZIP. The analytic source and verification script are sufficient to reproduce the claimed artifact without omitted code or data dependencies.

I compiled the extracted main.tex using Tectonic into a private build directory. It succeeds with four pages and no relevant warnings, undefined references, overfull boxes or underfull boxes. The rebuilt PDF has a different creation timestamp and byte hash; exact text extraction matches. More strongly, rendering each compiled and distributed page at 110 dpi produces **identical PNG bytes on all four pages**, recorded in `render_comparison.json`.

I visually inspected all four distributed pages: equations, signs, theorem/proof transitions, references, author/ORCID, date/version, page numbers and disclosures are readable; no clipping, overlap, missing glyphs, placeholder text or broken citation is visible. The four-page description is accurate.

## 6. Final disposition and residual limits

**Concrete actionable issues: none. Required repairs: none. Strongest verified result: the complete theorem stated in the preprint, together with a coherent and reproducible final package. Exact remaining mathematical gap identified: none.**

This verdict is based on independent reconstruction, primary-source hypothesis checks, active falsification of the verifier, full archive checks, source recompilation, exact rendered comparison and visual inspection. It remains an unrefereed AI review; no exhaustive priority or formal-certification conclusion is inferred. The parent can proceed to its separately planned fresh reviewer without a repair cycle required by this round.
