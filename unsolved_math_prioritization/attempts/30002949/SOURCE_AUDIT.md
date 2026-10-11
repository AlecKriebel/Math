# AI-assisted source and coverage audit for problem 30002949

## Finding

The original question is the Bruhat–Tits comparison conjecture in Miaofen Chen's Oberwolfach report, joint with Eva Viehmann, subsequently formulated as Chen–Viehmann Conjecture 4.2. Görtz's Theorems 0.1 and 3.4 explicitly claim this conjecture. The credited prior result is therefore a direct match, subject to the precise representative, level, and classified Coxeter-type hypotheses detailed in PROOF_RECONSTRUCTION.md.

The mathematical audit does not give unconditional approval to the inspected source proof. Its literal Lemma 3.10 fails in its own positive-rank unitary Ã3 example. A finite projected-vertex separation argument repairs the needed implication. The draft also handles the zero-dimensional superbasic case separately and broadens the final combinatorial fork check to the four actual fork rows. These are proof-audit corrections to a credited prior theorem, not a theorem counterexample or a new-solution claim.

## Original problem and exact category

The original report is “A stratification of affine Deligne-Lusztig varieties,” by Miaofen Chen, joint work with Eva Viehmann, in Oberwolfach Report 39/2015, printed pp. 2297–2299, PDF pp. 33–35. The conjectural comparison is item 1 on printed p. 2298. The setup is a connected reductive group over O_F, hyperspecial K=G(O_L), and minuscule dominant μ. It assigns g the function j↦inv(j,g) for every j in the σ-centralizer. The comparison target is a refinement of the EO stratification into classical DL pieces with building-controlled closures. The OWR item is not asking for equality with an entire raw EO union, and its later a-number conjecture is a different question.

Chen–Viehmann, arXiv:1507.02806v2, §4.2, Conjecture 4.2, printed p. 17, makes the basic Coxeter-type statement explicit. The paragraph immediately below records a more general parahoric expectation. Remark 2.1, pp. 5–6, warns that changing b arbitrarily within its σ-conjugacy class can change the partition. Lemma 2.4 and Remark 2.5, pp. 6–7, show why a naive adjoint reduction is insufficient: its converse requires rational surjectivity J_b(F)→J_{b_ad}(F), which need not hold. The reconstruction uses actual rational elements of J and full κ_G instead.

Görtz, arXiv:1802.02225v1, Theorem 0.1, p. 2, explicitly names CV Conjecture 4.2; Theorem 3.4, p. 15, is the precise basic assertion. Its standing group convention is connected semisimple adjoint (§1.2, p. 4); §3 assumes connected affine diagram and K=S\{v} σ-fixed (§3.1, pp. 11–12). The basic representative is the unique length-zero τ in the relevant affine-Weyl coset (§3.1, pp. 13–14). The BT pieces and exact coset index are given in §3.2, pp. 14–15. The source itself says extension to reductive groups is easy; the reconstruction supplies the needed componentwise details, rather than importing an unproved rational adjoint surjectivity.

The original hyperspecial/minuscule setting identifies X(μ,τ)_K with X_μ(τ) by Görtz §1.5. The rational maximal extension means a parahoric obtained by removing one σ-fixed vertex. GH §5.1 expressly distinguishes this from a merely maximal σ-stable subset obtained by removing a multi-node orbit. Arbitrary parahorics, arbitrary disconnected/factor-permuting groups, nonbasic representative choices, non-Coxeter EO strata, and the separate a-number conjecture are not covered by the assertion audited here.

## Source identity and version ledger

The eight mathematical PDFs were retrieved on 2026-10-11 at about 19:00 UTC. Their byte counts and SHA-256 hashes matched the earlier retained source pins. [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) records their public URLs, exact hashes, retrieval history, and separate inspection scopes. Source-author code and TeX were not executed. The public-edition preparation rehashed the identified source representations without claiming a new full source inspection.

| Source | Exact version inspected | PDF bytes | SHA256 |
|---|---|---:|---|
| OWR report | EMS-hosted OWR 39/2015, full report | 619005 | 684765e8e322d574b9adef05b9cac856693fe7dc8f07b299eb74e268158cb8d0 |
| Chen–Viehmann | arXiv:1507.02806v2, 14 September 2016 | 351610 | bfc236add240bbc87e538eb484773036ba9e8d3fd0370fa0822a615477a3f2cb |
| Görtz stratifications | arXiv:1802.02225v1, 6 February 2018, 21 pages | 307312 | 0686087d6bb6d61ad2ec5e4ed9a96b2903e5cb0573c8620d6f1d071d9fbd10d6 |
| Görtz–He old preprint | arXiv:1311.6263v1, 25 November 2013, 27 pages | 322639 | 2b66e5e6076b2a07d5a30c98e0dbd0339828ca37738927be591ac1ab2ae9657a |
| Görtz–He author copy | 28-page main-paper author version hosted by YMSC, final-style numbering; not an erratum | 449150 | 6ac58dd2d7c98f111b3559726a2d2ca8987eda12d1e174a9625cceb521646fa6 |
| Haines–Ngô | American Journal of Mathematics 124 (2002), 1125–1152, journal PDF | 427999 | ae58443a0ee9316734511cfe7bbd02a4f4e520a67aec035bd55adf29d42f0206 |
| Richarz | Bulletin de la SMF 144 (2016), 117–124, journal PDF plus two cover pages | 752924 | 76052f3d1bdccacb957c804fdde2b12e33d5635c5d73a8b9ccf7c2d32fa8da72 |
| Lusztig | Inventiones mathematicae 38 (1976), 101–159, scanned journal article, 61 PDF pages | 5724702 | 82a4489feae5490425e81d9e1df1d91e678c2437851f86b81aad0ac76fad3021 |

Public retrieval URLs:

- OWR: https://ems.press/content/serial-article-files/46591 ; report DOI https://doi.org/10.4171/OWR/2015/39
- Chen–Viehmann: https://arxiv.org/pdf/1507.02806 ; version record https://arxiv.org/abs/1507.02806
- Görtz: https://arxiv.org/pdf/1802.02225 ; version record https://arxiv.org/abs/1802.02225
- GH old: https://arxiv.org/pdf/1311.6263
- GH author copy: https://archive.ymsc.tsinghua.edu.cn/pacm_download/465/10790-Xuhua_He_62.pdf
- Haines–Ngô: https://www.math.uchicago.edu/~ngo/alcoves.pdf ; DOI https://doi.org/10.1353/ajm.2002.0037
- Richarz: https://www.numdam.org/item/10.24033/bsmf.2708.pdf ; DOI https://doi.org/10.24033/bsmf.2708
- Lusztig: https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0038/LOG_0012.pdf

## Read scope and dependency audit

The following is a read ledger, not a claim to have checked every statement in every bibliography. Full relevant proofs were read in the stated sources. Foundational group/building facts and the prior classification are identified explicitly as dependencies, rather than disguised as freshly proved results.

### Original report and Chen–Viehmann

The OWR contribution, PDF pp. 33–35, was read in full. PDF p. 34 was visually checked again after recovery. The conjecture identity, invariant domain/codomain, hyperspecial level, minuscule assumption, and refined-EO wording agree.

For CV the relevant setup and invariant sections, pp. 1–7, and comparison discussion through §4.2, pp. 12–23, were read. This includes the conjecture, GL9 example outside the desired Coxeter range, GSp4 comparison, the unitary comparison Theorem 4.6, its odd/even dimension arguments, and Lemma 4.7/Corollary 4.8. The unitary theorem is independent confirmation that the false escape lemma is not a theorem counterexample. The separate §5 a-number conjecture is not used as coverage for this problem.

### Görtz stratifications

All 21 pages of the retained v1 PDF were read, including the complete §§3.3–3.6 proof and its internal prerequisites. Proof-critical pp. 5 and 17 were visually inspected again after recovery. The audit findings are:

- Proposition 1.1 supplies the classical twisted-Coxeter open-cell result; this was traced to Lusztig rather than accepted solely from the citation.
- §1.4 gate facts and their rationality consequence supply the residue comparison.
- Lemma 3.3 handles lift independence by torus-parahoric Lang.
- §3.3 proves constancy by rational gates and Lusztig, with a valid reduction from arbitrary rational j to its rational alcove representative.
- Lemmas 3.10–3.11 demand an impossible all-wall escape in the explicit Ã3 fixed apartment. Lemma 3.13 is a legitimate sufficiently-far conditional statement, but the hypotheses needed to invoke it cannot be achieved by the preceding lemma in general.
- Lemma 3.14 is valid; its full short proof is reconstructed as Lemma E.
- §3.6 needs only finitely many right-coset distinctions after passing to K-double cosets. Lemmas A–D replace the false escape implication exactly at that point.
- Its positive-rank assertion misses the zero-dimensional superbasic row, which is handled directly.
- Its final “only B” fork sentence misses three other affine quadruples with the same singleton-complement structure. The thirteen-row table and Lemma F verify all of them.
- Remark 3.5 concerns a nonbasic correction to old GH transitivity language. It is not needed for the basic theorem audited here.

### Görtz–He

In the old 27-page version, the definitions, decomposition, fine-to-coarse construction, classification, explicit EO computations, and §7 BT description were read through the relevant pp. 1–24. In the 28-page author copy, §§1–7.2 were checked for the relevant proofs, including Proposition 2.2.1; Theorem 4.1.2 and its construction in §§4.2–4.6; Lemma 4.6.1 and Corollary 4.6.2; §5.1 and its footnote; Theorem 5.1.2; all thirteen affine quadruples in §6.2 and the explicit support computations in §§6.3–6.6; Remark 6.1.1; Proposition 7.1.1 and formula (7.2.1).

The key logical chain is concrete. A θ-stable spherical parahoric permits Lang reduction to J-translates of a finite DL set. The canonical iterated parahoric refinement gives a J-equivariant fine-to-coarse isomorphism at Q=I(K,w,σ). The Coxeter calculation makes Q commute with P=supp_σ(w), and the explicit support list gives P∪Q=S\Σ_w. The coarse sets sit in disjoint residues indexed by J/(J∩P_{P∪Q}); this proves the exact BT stabilizer and survives the reductive extension with κ labels retained. The finite classification itself is credited to GH; the audit rechecks the particular support consequences it uses and does not claim a fresh exhaustive classification of all non-Coxeter data.

The old displayed list already has nineteen entries despite its “21” count. The author copy changes the number to nineteen and changes theorem numbering. A YMSC listing associated this download with the erratum, but the downloaded content is plainly the 28-page main article. It must not be cited as a read copy of the four-page erratum.

### Haines–Ngô

The relevant part of §5, printed pp. 1132–1134, Definitions 5.1–5.4, Lemma 5.3, Proposition 5.5, and Corollary 5.6, including proofs, was read. The proofs require no ambient regular direction. A directed gallery cannot cross the same wall twice, hence is minimal; the signs of walls separating its endpoints determine the direction of every minimal gallery. Point displacement inside a translated Weyl chamber gives the same signs, hence produces an acute gallery. The finite Weyl chambers cover the apartment, giving a direction for every pair. Applying this inside the rational apartment, not the full ambient one, is the exact ingredient in Lemma D.

### Richarz

The full printed pp. 117–124 article was read, including all proofs. Relevant exact numbering in this journal version is:

- §1.1, affine BN-pair (1.2), Lemma 1.3: parahoric-generated subgroup and Kottwitz kernel.
- Theorem 1.4: connected-parahoric double cosets are the corresponding Weyl double cosets.
- Remark 1.5: the simply connected derived cover identifies the affine Weyl subgroup, without asserting rational surjectivity to the adjoint group.
- §1.2, Lemma 1.6: rational and Frobenius-fixed Iwahori-Weyl groups, with the proof explicitly doing the same for affine subgroups. The torus-parahoric H¹ vanishing supplies rational normalizer representatives.
- Corollary 1.7: compatible facet stabilizers.
- Proposition 1.11 and Sublemma 1.12, pp. 122–123: a rational reduced multiplication remains ambient length-additive. The sublemma follows by restricting inversion roots to the fixed apartment and comparing signs; induction gives the gallery assertion used here.

Görtz cites earlier-version numbering for some Richarz facts. The audit uses the numbering actually verified in the pinned journal article. Lemma C additionally spells out an explicit torus-Lang lift n_0t to prove ambient κ_G=0 directly.

### Lusztig

“Coxeter orbits and eigenspaces of Frobenius,” Inventiones mathematicae 38 (1976), was read visually because the PDF is scanned. The checked range is printed pp. 101–103 and 107–113, especially §§1.4, 1.18–1.19 and the full proof chain §§2.2–2.5. The two pages containing the conclusion of Lemma 2.4 and Corollary 2.5, printed pp. 112–113, were rendered and read again after recovery; they are PDF pp. 13–14.

The proof chain reduces centers/products and cyclic permutations of simple factors in §1.18. The root-subgroup/Bruhat calculation in §2.2 and the distinct-Frobenius-orbit word condition in §2.3 force the relevant Bruhat index to be Frobenius-fixed and to send each chosen orbit representative to a negative root. Lemma 2.4 verifies the fixed-index assertion, including its twisted-diagram cases. In Corollary 2.5, Frobenius invariance propagates the negativity to every simple root, so the Bruhat index is the longest element and every DL flag is opposite the chosen rational Borel. Rational-group equivariance gives the assertion for every rational Borel. This is exactly what the gate argument needs, including disconnected finite residue diagrams. Later representation-theoretic parts of Lusztig's article were not audited or used.

### Foundational boundary

The gate/projection theorem for spherical residues, strong transitivity of the affine BN-pair, the Coxeter braid theorem and subword criterion, and Lang surjectivity on connected parahorics remain standard foundational dependencies. Their precise uses are stated and, where short, their consequences are proved in the reconstruction. The full Abramenko–Brown and Björner–Brenti books were not retrieved. The audit does not claim to reprove the theory of buildings or Lang's theorem from first principles. Nor does it claim to have audited every cited proof underlying GH's classification. None of these dependencies supplies the false all-wall claim; that claim is removed from the reconstructed proof.

## Final publication version and erratum limitations

The publication metadata are Görtz, Transactions of the AMS 372 (2019), 4675–4699, DOI https://doi.org/10.1090/tran/7715 . The arXiv record currently exposes only v1, submitted 6 February 2018. The author bibliography at https://www.esaga.uni-duisburg-essen.de/ulrich.goertz/publications/ lists the journal publication but links the arXiv full text. The official university staff bibliography likewise offered only the arXiv route. Attempts to read the AMS final PDF and DOI landing page have not established access to the final journal text. The recorded retrieval attempts and limits are listed in SOURCE_VERIFICATION.json. Consequently every mathematical page/lemma finding above is attributed to the pinned arXiv v1, not to an unseen final PDF.

The GH erratum is a separate publication in Cambridge Journal of Mathematics 6 (2018), 89–92, DOI https://doi.org/10.4310/CJM.2018.v6.n1.e4 . Historical public first-page information indicates correction of building/component indexing and nonbasic orbit language, but the complete erratum was not retrieved. Its full proof is not relied on. The audited formula keeps J/(J∩P_{S\Σ}) and κ_G labels, avoiding the affected unlabelled-building simplification. An adjacent erratum paragraph on an author bibliography belongs to a different paper and is not evidence of a correction to Görtz Lemma 3.10. The later Görtz–He–Nie paper with DOI 10.4153/S0008414X22000608 is context only and is not used to certify a correction.

## Public edition and mathematical acceptance

The complete mathematical reconstruction is accepted together with INVARIANT_SUBSET_CORRECTION.md, whose general formula supplies the invariant-subset calculation used in the reductive stabilizer argument. INDEPENDENT_AUDIT.md records the separate mathematical check. ACCEPTANCE.json binds the verdict to the exact public proof, correction, and audits. EDITORIAL_MAP.json records every editorial replacement and the unchanged mathematical regions.

Source documents, text extractions, source images, datasets, diagnostic programs, and raw computational checks are not reproduced. This edition contains authored mathematical exposition, corrections, audits, and public verification metadata. No fresh canonical-dataset verification, novelty finding, formal certification, or external human peer review is claimed.
