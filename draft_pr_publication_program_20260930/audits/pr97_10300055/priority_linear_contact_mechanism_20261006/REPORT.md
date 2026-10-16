# PR97 priority audit: contact pencils and deformation literature

Audit family: linear deformation of general integrable defining forms, contact/foliation interpolation, and adjacent Reeb/Anosov mechanisms. This is a bounded priority report, not a new proof-search turn or an authorization to merge or publish. The accepted pencil proof and the repaired C1 disk criterion remain the mathematical gate supplied by ROOT.

## Result

**A precise prior general theorem covers the contact-pencil mechanism.** Dathe–Khoule (2012), Theorem 2.2, printed pp.102–103, admits a general nonclosed integrable defining form. Its criterion specializes to the exact pencil in PR97. The primary author-uploaded original source body was read through all eight printed pages. A later primary author preprint, Khoule–Manso–Ndiaye–War, arXiv:2503.00454v1 (2025), Theorem 6.2, printed/PDF pp.32–33, reproduces the criterion, expressly attributes its C1 version to the 2012 paper, and supplies the polynomial calculation. Its original PDF and the pinned page images are preserved here.

Neither of those inspected source bodies explicitly answers Calegari Question 13.2 or states that the endpoint contact structure is tight under the PR's taut-foliation hypothesis. Nevertheless, the pencil is covered by a known theorem, and smooth endpoint tightness follows by the separately established Eliashberg–Thurston neighborhood theorem plus finite Gray transport. That implication is **this audit's covering interpretation**, requiring ROOT's new independent falsifier; it is not a claim that the 2012 authors wrote the conditional answer.

I do not clear novelty, certify exhaustive priority, assign the final QUEUE status, or authorize publication. The full Confoliations book, the published 2011 Dathe–Rukimbira article, and the 2025 affine-pairs article remain unread in full. The additional C1 disk/form correction must be distinguished from the already known pencil.

## Exact target and boundary

The inherited candidate concerns a closed oriented smooth three-manifold with a cooriented taut C2 foliation, no sphere leaves, a global nonsingular C1 form α, and a global C1 form ω satisfying

```
dα = α∧ω,       ω∧dω ≠ 0.
```

The ordinary contact-tightness theorem explicitly assumes ω smooth. The lower-regularity extras are the precise C2 embedded-disk obstruction and tightness of sufficiently C1-close smooth forms; I do not silently replace those by an unspecified C1 definition of tightness.

The original Question 13.2 includes a minimal taut C2 foliation on an atoroidal three-manifold with nonzero Godbillon–Vey class and asks whether a contact representative ω must be tight. The general candidate is stronger in its topology but has the stated global/coorientation and smooth-endpoint assumptions. The contact-pencil proof uses the pointwise contact hypothesis, not merely nonzero integral Godbillon–Vey class. It neither produces a contact ω nor solves Question 13.1. ROOT's gate pins source head fb50facb2a7389bb272bbf0b5cbd80c24c79b992 and candidate digest 393241cc6299a7a8e7b9a2d72c22e48f574702e0f3c822e0310647a16e0ff4c7.

## The closest prior theorem and the exact covering map

Dathe–Khoule, *Sur les déformations d'un feuilletage de codimension 1 en structures de contact*, African Diaspora Journal of Mathematics 13(2) (2012), 100–107, Definition 2.1/Theorem 2.2, pp.102–103, considers α integrable on a compact contact (2n+1)-manifold with contact form β. It allows

```
α_t = C(t)α + B(t)β,
C(t)>0, C(0)=1, C continuous at 0,
B(0)=0, B continuous and strictly increasing.
```

The necessary and sufficient condition is

```
α∧(dβ)^n + nβ∧dα∧(dβ)^(n−1) ≥ 0.
```

The source's overall introduction takes the ambient manifold smooth; the original displayed theorem does not itself print a C1 regularity threshold. The explicit historical C1 attribution is authenticated in the later author preprint's paragraph preceding Theorem 6.2. No closedness condition on α occurs in this theorem. The 2012 Corollary 2.4 and Theorem 2.6 subsequently specialize to closed α; they are distinct statements.

Source access is precisely: [author-uploaded original full source body](https://www.researchgate.net/publication/258228980_Sur_les_deformations_d%27un_feuilletage_de_codimension_1_en_structures_de_contact), pp.100–107, preserved in actual web responses source_pages_22_web.json and source_pages_25_web.json; author upload date shown as 21 August 2026, distinct from printed publication year 2012. Actual read coverage is source_pages_22 lines0–809 plus source_pages_25 lines673–1326: this overlap includes the otherwise missing lines809–1090 and all original body/References through line1208. Later citing snippets are excluded from the original article. Direct PDF links did not yield a locally downloaded original PDF. The criterion is cross-authenticated in the preserved [2025 arXiv primary PDF](https://arxiv.org/pdf/2503.00454v1), pp.32–33, equation (59), with equation (62) providing the expansion. This is source-body verification, not an inference from a title, abstract, or citation count.

**Application derived in this audit.** In dimension three, set n=1 and β=ω. Frobenius gives α∧dα=0. The accepted differentiation step gives α∧dω=0; also ω∧dα=ω∧α∧ω=0. Thus the prior criterion vanishes identically:

```
α∧dω + ω∧dα = 0.
```

C(t)=1 and B(t)=t meet all the coefficient requirements and give α+tω. The known expansion then gives

```
(α+tω)∧d(α+tω) = t²ω∧dω,       t>0.
```

This is the same family of planes as the candidate's β_s=ω+sα, with s=1/t after multiplication by the positive scalar t. The constant-volume s-pencil is an equivalent normalization of this special case. It is not made different by calling the parameter s instead of t.

For arbitrary positive C,B the same mixed-term cancellation gives B(t)²ω∧dω. The statement covers the contact deformation; it does not itself assert endpoint tightness, and it does not generate a contact Godbillon–Vey representative.

A typographical issue in the 2025 proof should not be concealed: after equation (62), a displayed equality drops the nonnegative mixed term for the general criterion. The correct general conclusion there is an inequality. In the PR's identically-zero mixed-term specialization, the displayed equality is exactly true, and the original 2012 expansion plus a direct three-dimensional expansion independently confirm the required case. I have not audited the later preprint's unrelated main dynamical claims or C0 exterior-derivative theory.

### What the original 2012 paper says about Gray/isotopy/tightness

The original paper's eight-page body contains no Gray-stability theorem, isotopy assertion for the affine family, taut-to-tight theorem, Godbillon–Vey contact condition, or reference to Calegari Question 13.2. Its remaining results concern closed forms, K-contact/flat examples, torus foliations, and Euler-characteristic obstructions. ResearchGate's page includes later citing-paper snippets mentioning Gray; these are below the original References and are **not** part of the 2012 article. This distinction is material.

The later 2025 preprint discusses smooth Gray stability in its introduction and poses a separate question about deformation to nearby contact forms; its Theorem 6.2 and Corollary 6.4 cover the general criterion and the vanishing mixed-term/Reeb criterion, respectively. The statement does not assert taut endpoint tightness. Low-regularity Gray failure in that preprint is not a license to use Gray on C1 contact paths.

## The separate classical tightness deduction

Vogel (2011), *Rigidity versus flexibility for tight confoliations*, Geometry & Topology 15, 41–121, printed p.42, explicitly restates Eliashberg–Thurston's theorem that **every sufficiently C0-close contact structure** to a taut foliation is symplectically fillable and tight. The primary shared PDF/text was read directly. Dathe–Rukimbira's 2008 author preprint, Proposition 3.3, p.5, restates the same neighborhood theorem and cites Confoliations p.50. Its Proposition 3.4 combines that theorem with its preceding isotopy statement, but expressly assumes α0 closed. It does not cover the present nonclosed α by itself. [Vogel primary publication](https://msp.org/gt/2011/15-1/p02.xhtml); [Dathe–Rukimbira author preprint](https://arxiv.org/pdf/0812.3389v1).

The following is our application of those established statements, not a historical claim about what any cited author explicitly concluded.

When α and ω are smooth, ker(α+tω) tends uniformly to ker α as t→0+. Select one sufficiently small finite t0>0. That smooth contact plane is tight by the taut-neighborhood theorem. For a direct compact path all the way to the smooth endpoint, use

```
λ_u = uα + ω,      0 ≤ u ≤ 1/t0.
λ_u∧dλ_u = ω∧dω.
```

All parameters are finite and all forms in that compact interval are smooth contact forms. Gray stability transports tightness from ker(α+t0ω)=ker λ_(1/t0) to ker λ_0=ker ω. There is no use of Gray at a degenerate foliation endpoint or at infinity.

For the actual candidate α need only be C1. The repaired finite-interval smoothing argument is therefore essential to the accepted proof. A general C1 affine-deformation criterion does not by itself give a smooth Gray isotopy. ROOT's candidate already addresses that issue, and this priority family does not reopen or claim independent clearance of its simultaneous C1 disk/form correction. I found no inspected prior source explicitly stating that exact extra conclusion. A claim of novelty would have to identify the contribution relative to the known general pencil, the classical smooth deduction, and any genuinely needed regularity refinement, instead of presenting the pencil as a new mechanism.

## Distinct literature families and why tempting substitutions fail

| Source body checked | Actual mechanism/hypotheses | Relevance and boundary |
|---|---|---|
| Dathe–Rukimbira 2004, original author-uploaded source, Theorems 1–2 and remaining pp.75–81 | Closed α0, contact endpoint and α0(Reeb)=0 criterion. The introduction expressly distinguishes its definition of linearity from ET's stricter one. | Genuine earlier precedent; it does not remove the closedness hypothesis. Publisher PDF attempts yielded HTTP202 empty bodies; the author-uploaded original source body is available through the web. |
| Dathe–Rukimbira 2008, full 8-page author preprint, Props.2.1,3.2–3.4 | Closed nonsingular α0; contact family, isotopy, and tightness by the taut neighborhood theorem. | Closest prior tightness proof architecture, but insufficient as a direct nonclosed covering theorem. Published 2011 version DOI 10.1515/advgeom.2010.043 is identified by Crossref; its full body remains unread. |
| Dathe–Khoule 2012, full original source body; Khoule et al.2025 §6 pp.32–35 | General integrable α with the mixed wedge inequality; affine families. | Exact prior pencil criterion. The full tightness answer is our further interpretation, not an explicit statement in the article. |
| Zois 2000v4, §0.5, printed pp.23–27 | ET strict first-derivative positivity; interpolation of two integrable forms in a bi-contact/conformally-Anosov setting; general taut/fillability discussion. | Full source is dated31 July 2000. It does not state the α–ω conditional tightness theorem. Its strict mixed form is positive; the present mixed form is zero. |
| Bowden 2016, §4 printed pp.708–710, especially Prop.4.4 p.710 | Strict linear deformation means positive first derivative of contact volume at the foliation. Convexity plus Gray gives isotopy of two same-sign strict deformations. | The PR's α+tω has volume t²ω∧dω and derivative zero at0. Its coefficients are linear, but it is not strict-linear in this theorem's sense. |
| Ndiaye–Wade 2023v2, entire 15-page preprint, especially Thm5.3 | Pairs of independent **closed** defining forms on even-dimensional M; affine contact-pair compatibility. Later publication AdvGeom24(4)(2024)545–552 identified in 2025 references. | Does not cover a single general nonclosed form in3D. |
| Mori 2002, introductory p.1, §4 Thm3 pp.7–8 | Open-book construction under positive-Dehn-twist hypotheses, fillability and deformation into a foliation with Reeb components. | Not the taut/nonclosed/GV conditional statement. Reversing an arbitrary contact-to-foliation construction cannot establish the needed tautness. |
| Etnyre–Ghrist 2002, author source §2 Thm2.1 pp.3–4 | Anosov flow lies in the intersection of oppositely oriented tight contact planes, credited to Mitsumatsu 1995. | Those contact planes **contain** the flow. ker ω is transverse to its Reeb flow. Their theorem cannot simply be applied to ker ω. |
| Mitsumatsu Hayama 2002 proceedings, full 8 pages, §§2–4 | Foliated-cohomology/GV asymptotic-linking framework; bi-contact constructions; an explicitly open analytic-torsion justification in the final section. | The proposed analytic argument is not a proved conditional tightness result. Do not promote it to one. |
| Asaoka 2010, exact Thm1.5 printed p.1652/PDFp.5, introduction pp.1649–1652 | A C^r codimension-one foliation on closed 3M with a C^r tangentially contracting flow, r≥2, yields Anosov flow and an algebraic weak-stable foliation. Cor.1.4 concerns associated bi-contact structures. | Supplies a separate potentially covering rigidity route after an additional derived hypothesis check, below. It does not explicitly mention GV contact representatives or Q13.2. |
| Dramé–Khoule–Ndiaye 2025, author-uploaded full PDF accessible through web, Thm3 p.4 and Eq.(26) | Contact–symplectic pairs with integrable α0 and compatibility requiring dα0∧η^k=0, dα0∧(dα)^h=0, α0(Reeb)=0. | In the single-contact specialization k=0 the first condition imposes dα0=0, so this displayed result is not a replacement for the general2012 criterion. Direct local PDF retrieval returned403; web PDF body and page evidence were obtained, with OCR limitations noted. |
| Khoule–Ndiaye–Wade 2025, DOI 10.1007/s00022-025-00742-z | Affine deformation of pairs of confoliations. | Original full text unread; publisher/ResearchGate expose preview only. I do not claim exact hypotheses from the abstract or eliminate this source as irrelevant. |
| Dathe 2026, DOI 10.1155/jom/8818157 | Publisher full-HTML body concerns taut/R-covered foliations with transverse measure. | No authenticated exact covering α–ω theorem found there; no full PDF read. |

Primary URLs and retrieval results are in SOURCE_CATALOG.json and actual web/HTTP records. The internal filename asai2011_pa is a bookkeeping misnomer; the actual author is **Masayuki Asaoka**, the paper is **2010**, DOI 10.5802/aif.2569. The title/author/year were read on the original PDF, not inferred from that filename.

## Secondary Reeb/Anosov interpretation: explicitly this audit's inference

This section is for the next falsifier, not a substitute proof or a claim of a previously written answer. Let ω be smooth and R its Reeb field. Since α∧dω=0 in dimension3,

```
α(R)=0,       L_R α=−α,       φ_t^*α=e^(−t)α.
```

Here φ is the smooth Reeb flow; φ_t^*ω=ω and φ_t^*dω=dω. On ξ=ker ω the restriction α|ξ is nonzero: if α were proportional to ω at a point, α∧dω could not vanish there. Define V∈ξ by

```
i_V(dω|ξ)=α|ξ.
```

Then V is a nonzero C1 section of TF∩ξ and invariance gives Dφ_tV_x=e^tV_(φ_t x). Compactness turns this exact scaling into uniform contraction of TF/TR under the reverse Reeb flow. Thus the reverse flow appears to meet Asaoka's tangential-contraction definition for the actual C2 foliation and smooth R; the exact theorem and definition were visually checked on PDFp.5. This suggests an Anosov/rigidity consequence, but it remains **our derived application** until independently falsified, and it was not used to grant any clearance here.

There is also a classical hypertight interpretation: a nowhere-zero Reeb field tangent to a Reebless C2 foliation cannot have a contractible closed orbit if one imports Novikov's leaf π1-injectivity and the leafwise index obstruction. Foulon–Hasselblatt–Vaugon2021, *Orbit growth from contact surgery*, Remark 2.4 printedp.1107/PDFp.5, explicitly records hypertight implies tight and attributes it to Hofer 1993. That page and Definition 2.3 were visually checked. The original Novikov theorem and Hofer 1993 full proofs were **not** read in this family. Hofer's correct DOI is10.1007/BF01232679; the Springer page exposed subscription preview, not the full article. The Novikov→hypertight→tight application is therefore separately labelled an inference with imported classical premises, not an authenticated prior exact answer. It is also distinct from the bi-contact-plane theorem.

## Source-access gaps and limits of this audit

1. **Confoliations**, Eliashberg–Thurston, University Lecture Series 13, AMS1998, including p.50 and any relevant interpolation/GV sections: no complete legitimate full text obtained/read. The attempted official AMS PDF URL returned HTML; publisher/preview/author-collection attempts did not deliver a complete book. Vogel and Dathe–Rukimbira authenticate the exact neighborhood theorem as a cited premise; they do not authenticate the entire book's absence of a closer covering discussion.
2. Dathe–Rukimbira 2011, *Contact deformations of closed 1-forms on T²-bundles over S¹*, AdvGeom11(1)131–137, DOI 10.1515/advgeom.2010.043: full published body unread. Crossref metadata verified; publisher PDF/HTML attempts returned empty202 bodies. The 2008 author version was fully read. Changes in the published body are not assumed away.
3. Khoule–Ndiaye–Wade 2025, *Affine deformations of pairs of confoliations*, DOI 10.1007/s00022-025-00742-z: full body unread; explicit subscription preview. Its generalization means it remains a possible relevant later source, without an authenticated exact covering claim.
4. Mitsumatsu's full Warsaw/book chapter and Japanese *Topology of 3-dimensional contact structures*, cited in the Hayama proceedings: these full texts were not obtained/read by this family. The public eight-page proceedings is not silently treated as a substitute for them.
5. Original Hofer 1993 and Novikov proofs, and original Mitsumatsu 1995 theorem proofs, were not fully read in this family. The exact adjacent theorem statements read in later primary articles are identified above.
6. C0-contact Anosov flows2025 was read in the exact relevant §6 and introductory Gray/deformation discussion; its unrelated main proof was not fully audited. The 2025 contact–symplectic article's relevant body was obtained through web PDF, but not locally downloaded/visually checked as a whole. All such access modes are preserved distinctly.
7. Current bibliographic searches encountered further2025–2026 contact/Anosov/Liouville papers. Titles/abstracts alone were not counted as exact-covering evidence. This bounded audit does not claim to have checked every current citation or every language.

No failed download was represented as a PDF. No outreach, email, author request, publication, PR change, branch change, or commit was performed. Source bodies are private audit material. This family stayed in its dedicated folder and reused the shared source cache for the existing Dathe–Rukimbira/Vogel PDFs.

## Recommendation for ROOT

Obtain a fresh independent falsification of the **covering interpretation**, especially: the original criterion's nonclosed and regularity scope; exact parameter normalization; smooth versus C1 Gray transport; whether the algebraically automatic zero-CB case adds more than a short corollary; and which, if any, C1 extras are distinct from prior statements. Preserve the repaired verified proof as mathematical evidence. Rewrite priority discussion globally to credit Dathe–Khoule 2012 and its 2025 reproduction if the covering reading survives. Do not retain novelty clearance solely because no paper title explicitly mentions Question 13.2.

The bounded family work is complete with material prior art found and explicit access gaps left open. ROOT adjudication/publication authorization remains false. Search absence cannot establish priority, and the PR95 publication qualification waiver does not extend to PR97.
