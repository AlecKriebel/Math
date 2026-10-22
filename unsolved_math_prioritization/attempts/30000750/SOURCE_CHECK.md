# Source and status verification

Checked 2026-10-04 (UTC). Numeric identity: **30000750**. Upstream code: **OWR-1537-002**. Queue rank at intake: **608**.

## Exact source

The requested [catalogue page](https://www.unsolvedmath.com/problems/30000750) did not load in web retrieval. A direct request returned HTTP 403. Consequently the current catalogue contents were not verified live. The pinned dataset record was read in full and then checked against the original scholarly source, rather than treating its open-status label as authoritative.

The primary statement appears on printed p. 1136 (PDF page 22) of A. Schinzel, “The reduced length of a polynomial, revisited,” in *Diophantische Approximationen*, Oberwolfach Report 21/2007, pp. 1115–1190. The problem asks exactly the inequality proved in `PROOF.md`, for all real polynomials P and t in the closed interval [-2,2], with real monic multipliers in the definition of reduced length. [Report](https://ems.press/content/serial-article-files/46108); [DOI](https://doi.org/10.4171/owr/2007/21).

The report identifies the workshop dates as April 15–21, 2007. The catalogue citation's parenthetical “(2008)” conflicts with the report's own year; this does not alter the mathematical target. The cubic reduced-length computation discussed just before the problem is context, not an additional part of this catalogue question.

## Complete later resolution

The publisher-hosted full text of Edward Dobrowolski's paper was retrieved and inspected. Its Theorem 2.1, printed p. 454, is a universal length bound for complex polynomials with a unit-circle zero. It has no degree, integrality, irreducibility, simplicity, or monicity restriction. The result needed here is the theorem itself, rather than the multivariate corollary or a conjecture quoted in its introduction.

Bibliography: E. Dobrowolski, “On a question of Schinzel about the length and Mahler's measure of polynomials that have a zero on the unit circle,” *Acta Arithmetica* **155** (2012), no. 4, 453–463. [DOI 10.4064/aa155-4-8](https://doi.org/10.4064/aa155-4-8); [publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/82795).

`PROOF.md` checks all hypotheses for A_t P Q and supplies the full deduction to the real reduced-length infimum. This is verification of a published resolution, with no claim of novelty.

## Later-literature cross-check and limits

F. Brunault, A. Guilloux, M. Mehrabdollahei and R. Pengo, “Limits of Mahler measures in multiple variables,” *Annales de l'Institut Fourier* **74** (2024), no. 4, 1407–1451, §1.1 (p. 1411), records Dobrowolski's answer to Schinzel's question; reference [21] identifies the 2012 paper. [Published article](https://aif.centre-mersenne.org/item/10.5802/aif.3611.pdf). This is corroboration of later use, not an independent proof certificate.

Searches for the exact 2012 paper title, its DOI with “erratum correction,” and Dobrowolski/Schinzel/length/Mahler combinations did not locate a correction or retraction. This was a targeted public-source search, not an exhaustive citation-database audit. The known-result classification rests on the positively identified theorem and the exact deduction, not on absence of search results.

## Prior work and duplication check

At intake the live queue row was `queued`, `0/5`. The live `state.json` did not contain this ID. The live attempts directory listing had 54 entries and did not contain `30000750`. No result was returned from repository PR searches for this numeric ID, the phrase “reduced length,” or the combination Mahler/length; no branch matched the numeric ID. The related-target groups file had no occurrence of the numeric ID.

Default-branch code searches also returned no hits, even for the known queue ID, so these searches are not treated as conclusive evidence about repository content or full history. The positive queue read and explicit attempts-directory listing are the stronger scoped checks.

The pinned research-results corpus contains no exact report key `OWR-1537-002`, no key containing `1537`, and no report referencing this numeric ID. Thus there was no matching prior proof report to audit. A broad “reduced length”/Mahler search found an unrelated free-by-cyclic group report, which was excluded. The pinned problems corpus has one record containing “reduced length,” namely this target. No proof in another problem was assumed to transfer without checking scope.
