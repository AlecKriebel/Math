# Source and scope audit

Checked 2026-10-03. These are source-identification and mathematical hypothesis checks, not an independent peer review.

## Original question

- Catalogue: https://www.unsolvedmath.com/problems/30001148 . The live page was inaccessible through the web reader. Its current contents were not verified live. A supplied pinned catalogue record identified OWR-3388-006; the exact original was then obtained independently.
- Primary report: https://doi.org/10.4171/OWR/2009/05 . Official institutional PDF: https://publications.mfo.de/bitstream/handle/mfo/3106/OWR_2009_05.pdf?isAllowed=y&sequence=1 . Printed pp. 317–318, Colliot-Thélène's contribution.
- Report interpretation: K is the fraction field of a complete rank-one DVR, with arbitrary residue field k. F is a one-variable function field over K. All rank-one discrete valuations of F are included, even if nontrivial on K. The group is connected linear. Y is homogeneous, with no projectivity assumption. Finiteness of k is introduced only later for a special case.
- The catalogue's supplied open-status assessment is contradicted by the primary counterexamples below. Its 2026 triage date is not mathematical evidence of continued openness.

## Decisive older source: CTPS

Jean-Louis Colliot-Thélène, Raman Parimala, Venapally Suresh, *Lois de réciprocité supérieures et points rationnels*, Transactions of the AMS 368 (2016), 4219–4255.

- DOI: https://doi.org/10.1090/tran/6519 .
- Checked full author final version: https://arxiv.org/pdf/1302.2377v3 ; abstract and version history: https://arxiv.org/abs/1302.2377 . First submission 2013; final arXiv revision 2015. Journal publication 2016. Do not present this as a 2026 discovery.
- §1 distinguishes rank-one discrete valuations, henselizations, and the separate projective-homogeneous question.
- §5.2 and Proposition 5.2 give the required divisor choices and norm-product variety.
- Corollary 5.3, author-version pp. 29–30, has local points at every discrete-valuation henselization and no global point.
- Lemma 5.5 and Example 5.6(a), author-version pp. 31–32, supply the elliptic curve over C((t)) with triangular reduction.
- Henselization is stronger local solubility than completion for this use: its F-embedding in F_v transfers points. No reverse inference is used.
- CTPS's F/K lettering differs from this packet. RESULT.md consistently reserves K for the complete base field and F for the one-variable function field.

## Constant-torus corroboration: CHHKPS

Jean-Louis Colliot-Thélène, David Harbater, Julia Hartmann, Daniel Krashen, Raman Parimala, Venapally Suresh, *Local-global principles for tori over arithmetic curves*, Algebraic Geometry 7 (2020), 607–633.

- DOI: https://doi.org/10.14231/AG-2020-022 .
- Publisher text: https://content.algebraicgeometry.nl/2020-5/2020-5-022.pdf .
- Corrected final arXiv text also checked: https://arxiv.org/pdf/1906.10672v3 ; version history: https://arxiv.org/abs/1906.10672 . The v3 notice records a correction to Theorem 6.5 and rewording around Proposition 6.3 and §8.3. RESULT.md does not use Theorem 6.5. Theorem 4.4, Theorem 6.4(c), and Examples 8.1/8.7 in v3 retain exactly the inputs used here.
- §1.2, publisher pp. 609–610, defines Sha using all discrete valuations, not just a chosen regular model's divisors.
- Theorem 4.4, p. 616, compares patching, model-point, all-valuation and model-divisor obstructions for a torus over the normal-crossings model.
- Theorem 6.4(c), p. 623, computes Sha from graph cycle rank and H¹(k,S) when all reduced fiber components are P¹_k and meet at k-points, for an R-torus with a flasque resolution.
- §8.1 / Example 8.1, p. 628, provides the nonzero residual norm-one obstruction. Its flasque-resolution identification credits Colliot-Thélène–Sansuc, *La R-équivalence sur les tores*, Ann. Sci. ENS 10 (1977), Proposition 15, p. 206, DOI https://doi.org/10.24033/asens.1325 . This packet relies on the identification as stated in CHHKPS and does not claim an independent reconstruction of the entire 1977 resolution.
- Example 8.7, pp. 629–630, supplies the triangular cubic model. This packet independently checks the field, smoothness, regularity, and anisotropy hypotheses for k=C((u))((v)).
- The dual graph is a triangle; the bipartite patching graph is its subdivision. Both have one independent cycle. No graph-name shorthand changes the computed obstruction.

## Why the catalogue's Linh citation does not repair the claim

Nguyen Manh Linh, *Arithmetics of homogeneous spaces over p-adic function fields*, Journal of the London Mathematical Society 109(1) (2024), e12842, DOI https://doi.org/10.1112/jlms.12842 . Author version: https://arxiv.org/pdf/2211.08986v2 .

The introduction and Theorem A use a function field of a smooth projective geometrically integral curve over a finite extension of Q_p, and homogeneous spaces of SL_n with geometric stabilizers that are extensions of a multiplicative-type group by a unipotent group. The theorem controls a specified unramified cohomological obstruction; it is not an unconditional implication from bare local points. The standard places are closed points of the generic curve. The introduction explicitly distinguishes these from all rank-one discrete valuations. We do not transfer a positive result across those differences.

## Repository duplicate check

Read-only GitHub queries were made for the exact number, OWR identifier, semi-global wording, homogeneous spaces, local-global, and torus. Exact-ID/identifier and branch-name searches found no prior target attempt; broader results were inspected for mathematical overlap. The existing Laurent-descent packet for 30004320 / OWR-17295-004 (PR 368) concerns descent of a constant homogeneous space from k((t)) to k, rather than all-valuation local-global solubility over a curve function field. It is not mathematically the same target. Other returned tori were geometric/dynamical tori.

No genuine previous repository attempt on this question was found in this bounded search. Search indexes are not an exhaustive proof about every historic Git object. Published mathematical counterexamples are credited as prior work, not mistaken for repository duplicates or new discoveries.

## Source integrity and exclusions

SHA-256 of inspected primary reading copies:

- OWR report: 8ccf63e7cd0a58db51ff73e3f3301d59b610f88ef2ac1da35e001bc28f0a49d5
- CTPS arXiv v3: a158820e9112959e7deba61f380a9fb45946514a62ae3c6c5207d5c17c692d73
- CHHKPS publisher PDF: 20057fb52e51a8ceb75c626625dfdc3862b9b043ac1c477d08642ad77f26aa96
- CHHKPS arXiv v3: af6900a116fff923ee35a2e0694ed03c34cc77604776eb2aca8dbc4b2bcb9f3b
- Linh arXiv v2: 9836803e30361f50c0287980d589f19d9b5660925bf5729956ac839a4b5b74a0

The public packet contains analysis, citations, and limited original controls. Full downloaded papers, extracted full texts, rendered pages, imported catalogue records, corpus data, private coordination and unrelated work are excluded. Sources should be obtained from their publishers or authors.
