# PR91 bounded author-follow-up priority comparison

Recorded 2026-10-05 UTC. This audit concerns the incoming PR91 mathematical claim at head `2ea84c5de45cb92783b5b55057af1f52590be6bf`; it does not change that head or its budget. Author/citation-family audit completion: 100%. This percentage measures the assigned bounded comparison, not worldwide priority probability. No outside individual was contacted. All outputs are confined to this directory.

## Verdict and priority framing

No explicit solution of the general mixed-spectrum reverse inclusion was located in the examined Küster follow-up sources or the discovered citing papers. The positive source anchor is precise: Küster's 2015 Theorem 3.1.14(i), printed p43 / PDF52, supplies the inclusion and expressly leaves its converse open. The 2016 *Pure Koopmanism* Theorem 5(ii), printed p321 / PDF25, still supplies only that inclusion.

The full closed-disk row when a nonzero strict-interior matrix eigenvalue exists is already an immediate consequence of the 2015 results. The open disk is already contained in point spectrum by Theorem 3.1.13 / 3.1.14. The Koopman operator has norm one, so its spectrum is contained in the closed unit disk; because spectrum is closed, the known open-disk inclusion forces equality. PR91 must not claim this full-spectrum row as novel.

A later citing primary paper separately restates a classical general compact-map criterion: lack of eventual stabilization of the images implies the full closed disk. Its attribution is to **Egon Scheffold**, *Das Spektrum von Verbandsoperatoren in Banachverbänden*, Math. Z. 123 (1971), 177–190, Theorem 2.7, and Küster 2015 Theorem 3.0.2. See Ikeda–Ishikawa–Schlosser, arXiv v3 dated 26 January 2024, Example III.4(1), PDF5. [Primary v3](https://arxiv.org/pdf/2203.12231v3), [Scheffold journal metadata](https://link.springer.com/article/10.1007/BF01110116).

The defensible specialized target for further priority adjudication is the general mixed-case exclusion of extra unimodular eigenvalues, through the uniform factorization \(f=f\circ P\) of every unimodular \(C(U)\) eigenfunction. The complete table packages older interior, peripheral, nilpotent and spectral-closure facts with that completion. This author-family audit does not decide whether its factorization argument is an immediate consequence of another known general theorem; the independent general-priority family is examining that question. It supplies neither an exhaustive absence claim nor publication authority.

## Exact comparison target and falsifiable criteria

Let \(A\) act on finite-dimensional \(\mathbb C^k\) with any complex norm and induced norm at most one. Let \(U\) be its closed unit ball and \(Kf=f\circ A\) on all \(C(U)\). Write \(S=\sigma(A)\cap\mathbb T\), \(J=\{\alpha\in\sigma(A):0<|\alpha|<1\}\), \(\Gamma=\langle S\rangle\), with empty-generated group \(\{1\}\), and \(Z=\{0\}\) if \(A\) is singular, otherwise empty. The rows compared are:

| Condition | Point spectrum | Full spectrum |
|---|---|---|
| \(J\ne\varnothing\) | \(\mathbb D^\circ\cup\Gamma\) | \(\overline{\mathbb D}\) |
| \(J=\varnothing\) | \(\Gamma\cup Z\) | \(\overline\Gamma\cup Z\) |

An earlier theorem falsifies a priority claim for the missing part if it states the general mixed equality on this space and domain, or if a cited general theorem directly yields the missing exclusion with a routine checked application. A theorem on holomorphic, \(L^2\), \(C^r\) principal, or a proper kernel observable space does not by itself meet that criterion. Nor does a full-spectrum theorem determine point spectrum on the unit circle.

## Exact 2015 and 2016 primary comparison

The supplied PDFs were hashed before extraction; values match the parent-supplied custody records:

- 2015: SHA256 `4422566d4944d0530e610071c3809566829bf18bf7846265e0f981a31c79f9fb`.
- 2016: SHA256 `28a2dc55933344c73a994f7eb50436469c7ddc4bc9ec73166d5cb8b97855aa1d`.

All of 2015 Section 3.1, printed pp35–43 / PDF44–52, was read. Its setup is the arbitrary-norm closed ball and a contractive matrix. Theorem 3.1.5 covers matrices with entirely peripheral spectrum; Theorem 3.1.7 covers nilpotent matrices; Theorem 3.1.9 establishes zero when there is a strict-interior eigenvalue; Theorems 3.1.10–3.1.13 establish the open disk when such an eigenvalue is nonzero. Theorem 3.1.14(i) is the mixed inclusion. Its final sentence is:

> It remains open, whether the converse inclusion in 3.1.14 (i) holds true.

Theorem 3.1.14(ii) proves equality when there are strict-interior nonzero eigenvalues and no peripheral eigenvalues. Additional complete pages printed pp32–34 / PDF41–43 were read for Theorem 3.0.2's full-spectrum alternatives and its citation to Scheffold Theorem 2.7.

Printed pp58–59 / PDF67–68 do not solve the general mixed problem: Example 4.1.7 asks about the relation of the two Jacobs–de Leeuw–Glicksberg decompositions; Remark 4.1.8 handles convergent powers and a special periodic/zero situation; Example 4.1.9 assumes the strict operator-norm inequality \(\|A\|<1\). These are useful antecedents to be credited, not an explicit general converse.

The complete 2016 talk was read on printed pp320–322 / PDF24–26. Theorem 5(ii) repeats the mixed inclusion, while 5(i) and 5(iii) give the peripheral and purely contracting equalities. The general fixed/reversible decomposition results later in the talk do not state the missing equality or a general contractive matrix recurrence projection. An initial extraction offset was caught and corrected: **printed 320–322 correspond to PDF24–26, not PDF25–27**. The actual correction is preserved in `owr_page_mapping_correction_actual.json`.

## Later author sources

| Primary source and date | Actual read scope and relevant results | Comparison |
|---|---|---|
| Küster, *Decompositions of dynamical systems induced by the Koopman operator*. arXiv v1 18 June 2019; v3 9 July 2019. Journal version published 16 January 2021, *Analysis Mathematica* 47, 149–173. | v1 and v3 PDFs downloaded; whole text searched; introduction and theorem-bearing fixed-factor/Lyapunov sections read. v3 Main Theorem 4.6 PDF20 identifies the fixed factor by transfinite superorbits; Main Theorem 4.9 PDF21 treats one-dimensional fixed space/topological ergodicity; Theorem 5.6 PDF24 treats the finest absolutely Lyapunov-stable decomposition induced by the fixed algebra. | The stated theorems concern the eigenvalue-one algebra and dynamical quotients. No mixed linear closed-ball point-spectrum theorem or factorization of every unimodular eigenfunction was found. [Version history and paper](https://arxiv.org/abs/1906.07495), [latest examined preprint](https://arxiv.org/pdf/1906.07495v3), [journal metadata](https://link.springer.com/article/10.1007/s10476-021-0068-8). |
| Küster, *Topological Dynamics via Structured Koopman Subsystems*, Tübingen dissertation, 2021; oral examination 24 September 2021. | All 168 pages extracted; contents and introduction read; all theorem/proposition/corollary/lemma headings inventoried; all spectral keyword/symbol hits checked, then complete relevant pages read. Example 1.2.6(b) printed55/PDF61 defines the Kronecker algebra and discusses compact-group rotations. Example 3.2.17 printed105–106/PDF111–112 contrasts Kronecker and Lyapunov algebras. Lemma 3.2.10 printed98/PDF104 concerns limits of Lyapunov functions. Proposition 3.4.18 and Corollaries 3.4.19–20 printed117/PDF123 give weak stability and attraction on a specified Lyapunov ideal. | The dissertation contains unimodular eigenfunction material, so a simple English “eigen” keyword exclusion would be inadequate. The actual statements inspected concern Kronecker factors or restricted ideals; they do not state the matrix-ball mixed equality or uniform factorization of every unimodular eigenfunction through a contractive recurrence limit. [Repository primary PDF](https://ub01.uni-tuebingen.de/xmlui/bitstream/handle/10900/121768/Dissertation_Kuester_Veroeffentlichung.pdf?isAllowed=y&sequence=1). |
| Kari Küster, *Topologische Dynamik via Koopman-Teilsystemen*, seminar 16 November 2021. | Official seminar abstract inspected. Fixed algebra and Lyapunov algebra examples; no exact classification asserted in the abstract. | Corroborates dissertation topic, not absence of unpublished results. [Official seminar page](https://www.ergodic.de/seminar.php). |

The 2021 dissertation PDF SHA256 is `57d45da4058f06422c95ec80bb26fe3c95f18a40ddf280f65c2911a03af7d073`. The latest examined 2019 v3 SHA256 is `5059c5ed277dd18aa9e7d75d669665db2e5a78d16fc760e8e2a75730812878de`. Source dates come from cover/declaration or arXiv/publisher version history, not search-engine labels or regenerated PDF creation times.

## Discovered citing sources

| Source, date and exact pages | Mechanism / observable scope | Priority comparison |
|---|---|---|
| Schlosser–Korda, arXiv *Sparsity structures for Koopman operators*, v1 20 December 2021; SIADS paper *Sparsity Structures for Koopman and Perron–Frobenius Operators*, published online 22 August 2022. Read PDF7–12 and bibliography; thesis citation is reference 16 in arXiv v1. | Proposition 1 lifts continuous subsystem eigenfunctions. Theorem 2 PDF11 / Corollary 1 PDF12 concern principal eigenfunctions near a globally exponentially stable equilibrium, with smoothness, diagonalizability, simplicity and nonresonance assumptions. | A theorem about unique smooth principal eigenfunctions does not classify all \(C(U)\) eigenfunctions of a general matrix contraction with peripheral directions. No exact completion found. [Primary arXiv](https://arxiv.org/pdf/2112.10887v1), [publisher metadata](https://epubs.siam.org/doi/10.1137/21M1466608). |
| Ikeda–Ishikawa–Schlosser, *Koopman and Perron–Frobenius operators on reproducing kernel Banach spaces*. arXiv v1 23 March 2022; v3 26 January 2024. Read v3 PDF1,3–5,18–25,36,43–45; v1 PDF5 checked. | v3 Example III.4(1), PDF5, explicitly includes **all \(C(X)\)** with supremum norm and gives the no-eventual-image-stabilization closed-disk criterion. Example IV.13 PDF20 realizes \(C(X)\) as an RKBS. Example IV.12's linear-form space is a separate finite-dimensional observable space. | This paper must not be dismissed wholesale as an unrelated RKBS result. It confirms the full-spectrum row's classical provenance, but no mixed peripheral point-spectrum classification was located. The explicit image criterion appears in the examined v3; v1 only says the spectrum is “typically” a disk. v2 / final journal PDF were not compared, so no unsupported March-2022 date is assigned to this precise restatement. [Primary version history](https://arxiv.org/abs/2203.12231), [explicit v3](https://arxiv.org/pdf/2203.12231v3), [v1](https://arxiv.org/pdf/2203.12231v1). |
| Bevanda et al., *Koopman Kernel Regression*, NeurIPS 2023 supplementary material. Primary supplement PDF1–3,5–8 and references inspected. NeurIPS 2023 date is printed on PDF1; repository deposit is October 2024, not publication date. | Appendix A defines a finite-time non-recurrent domain. Lemma 2 / Proof 1 invoke a “rich” spectrum and cite Küster 2015 Theorem 3.0.2. The method uses eigenfunction extensions and kernel approximation along a finite flow tube. | Its domain and claim do not supply the target's invariant closed-ball point-spectrum classification. Küster 3.0.2 is a full-spectrum theorem, so this citation alone cannot certify every value is an eigenvalue in the target problem. No target completion found. [Primary repository](https://epub.ub.uni-muenchen.de/121751/), [supplement](https://epub.ub.uni-muenchen.de/121751/7/KKR_supplementary_.pdf). |
| Uwe Küster–Ruopp–Schneider, *Spectral structures for nonlinear operators, towards applications*, 24th Workshop of Sustained Simulation Performance, Stuttgart, **5–6 December 2016**. | Complete extracted slide text inspected; cover and bibliography visually checked. Numerical spectral mode approximation, Hankel/polynomial construction, fluid-flow examples. Bibliography slide24 cites Kari Küster's 2015 thesis. | No closed-ball \(C(U)\) classification or mixed reverse-inclusion theorem found. Search labels suggesting 2025 are wrong for this source. [Primary slides](https://fs.hlrs.de/projects/teraflop/24thWorkshop_talks/Uwe_Kuester_Koopman_WSSP24.pdf). |

For the compact-map image criterion, its application to \(J\ne\varnothing\) is routine and checked: choose a nonzero left eigenfunctional \(\ell\) with \(\ell(Ax)=\alpha\ell(x)\), \(0<|\alpha|<1\). Because \(U\) is a ball for a complex norm, \(\ell(U)\) is a closed disk of positive radius \(r\). Thus \(\ell(A^nU)\) has radius \(r|\alpha|^n\). These radii strictly decrease, so \(A^nU\ne A^{n+1}U\) for every \(n\). This is an application of the cited prior criterion, not a fresh claimed contribution or a new central proof search.

## Search coverage, receipts and remaining gaps

The actual web queries and returned results are preserved as `search_01_actual.json` through `search_11_actual.json`, `open_01_actual.json` through `open_05_actual.json`, `find_01_actual.json`, and the Scheffold repository click receipt. Queries used the exact 2015/2016 titles, author spellings Küster/Kuster/Kuester/Kari Valentina, spectral/mixed/3.1.14 terms, dissertation title, and year follow-ups through 2026. This is discovery by bounded query families, not a complete forward-citation index. The arXiv mathematics author search returned one record for the queried author; that is not proof of a complete bibliography.

The actual PDF downloads, errors, hashes, extractions, theorem inventory and rendered pages have separate receipts. Whole-text extraction or keyword scanning is not represented as line-by-line proof reading. The read-scope manifest lists the complete pages actually examined and the inspected statement families.

No matching unread theorem was surfaced that materially blocks this bounded verdict. Ordinary coverage gaps remain:

- The 2021 *Analysis Mathematica* version of record is subscription-gated; its metadata/abstract and the latest preprint were read. The later full dissertation supplies relevant author continuation, but the journal body was not read.
- Scheffold 1971 full text was not obtained: Springer exposes metadata and Geodesic exposes bibliographic notice; the EuDML link returned 403. The 2024 primary restatement and the 2015 open-disk results independently establish the attribution/application needed here, so this does not block the full-disk conclusion.
- The precise first appearance of the explicit RKBS image criterion between v1, v2 and the 2022 journal version was not adjudicated. It is definitely explicit in the examined January-2024 v3, already prior to PR91; its older theorem attribution is recorded without pretending to have read that original.
- Search discovery can miss later papers, uncatalogued theses, translated formulations, or unindexed citations. The independent general-priority family must be integrated before any broader novelty statement.

These are scope limitations, not evidence of an unseen earlier solution. No outsider input was solicited or prepared. A narrow defensible report is: “the examined author and citation family did not supply an explicit later solution of Küster 2015 Theorem 3.1.14(i)'s converse; the open disk and full closed-disk row are prior results or immediate consequences.”

