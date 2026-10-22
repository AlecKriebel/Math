# Source and scope gate

Checked 3 October 2026. Outcome: unresolved mathematical analysis, not a solution claim.

## Identity and prior-work checks

The target's live catalogue URL, https://www.unsolvedmath.com/problems/5300049, returned HTTP 403. A pinned catalogue was used solely to locate the source and identify the record. Its generated status and research prose were not accepted as mathematical evidence. The primary question was then independently recovered from the original paper.

The live public AlecKriebel/Math repository was checked separately from its queue:

- The exact queue row for rank 545 / 5300049 / AMR-052-0049 read `queued`, `0/5`.
- All-state PR searches for `5300049`, `AMR-052-0049`, and the combination `Accessibility` + `exponent` returned no match.
- Default-branch content searches for `5300049` and `positive-exponent` returned no matching attempt.
- The branch-name search for `5300049` returned no result and no continuation cursor.

These bounded checks found no earlier target attempt or PR to supersede. They do not establish the absence of every differently titled historical item. The queued row alone was not used as evidence of no prior work.

## Original question

Feliks Przytycki, “On Invariant Measures for Iterations of Holomorphic Maps,” in *Problems in Holomorphic Dynamics*, IMS preprint 1992/7, printed pp.29–34. The complete 46-page collection was obtained. The setting on printed p.29 and Problems 1.1–1.2 on p.30 were read; p.30 was also visually inspected. The exact limit is a liminf. The original question is not restricted to a completely invariant basin or to a generic point for an invariant measure.

Source: https://www.math.stonybrook.edu/preprints/ims92-7.pdf

## Published accessibility proof

Feliks Przytycki, *Fundamenta Mathematicae* 144 (1994), 259–278, DOI 10.4064/fm-144-3-259-278. Obtained the complete published PDF. Read the definitions, statements, all of §§1–2 (including the full telescope argument and the proof of Corollary 0.1), Remark 0.4, and §3. The Pesin inverse-branch lemma used by that proof is stated as an established input there; it is not reproved or computer-certified here. The local basin-preservation condition is retained throughout. Only the theorem's stated scope is used.

Sources: https://matwbn.icm.edu.pl/ksiazki/fm/fm144/fm14435.pdf and the author's copy https://www.impan.pl/~feliksp/access.pdf

## Later formulations inspected

1. Przytycki's 2018 ICM survey, author's 23-page version dated 16 June 2018: read all of §10, including its complete measure-lifting proof. That section explains the local backward-invariance requirement in terms of telescope domains lying in U. Its measure-lifting refinement is not promoted to a theorem about all starting points.

   https://www.impan.pl/~feliksp/FP_ICM_Survey_home.pdf

2. Przytycki, *Thermodynamic Formalism Methods in the Theory of Iteration of Mappings in Dimension One, Real and Complex*, *Annales Mathematicae Silesianae* 35 (2021), 1–20, DOI 10.2478/amsil-2020-0023. Obtained the complete 20-page author PDF, read §8, and visually inspected Theorem 8.1 on its eighteenth PDF page. It states a pointwise result for **positive lower exponent**, under local backward invariance and uniform tree shrinking. The underlining is lost in extracted text. This concise survey cites the earlier proof rather than providing a new complete proof; that dependence is explicit, not an independent reconstruction claimed here. The proof packet correctly retains this stronger positive subcase.

   https://www.impan.pl/~feliksp/Siles.pdf

A bounded current search used the original item number, title, and combinations of Przytycki, accessibility, lower/positive Lyapunov exponent, boundary and basin. No full resolution of the original general-basin question was verified. This is a statement about the work performed, not proof that no later resolution exists.

## Public-content and verification scope

The public packet consists of newly written mathematical analysis, source links and hashes, and standard-library verification code. It includes no source PDFs, extracted source text, catalogue corpus, scraped pages, private messages or credentials. The six auxiliary propositions have written proofs. The computer checks cover finite exact arithmetic and abstract models only; they neither prove the original question nor verify all cited literature from foundations.

The exact source-byte identities are recorded in SOURCE_HASHES.json. The whole public packet is frozen by SHA256SUMS.
