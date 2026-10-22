# FunctionTheory 6.46: credited prior-literature resolution

Target: rank 684; UnsolvedMath 2306046; AMR-022-6046. Checked 2026-10-05 UTC.

**Disposition: already solved in the literature; no new full solution or novelty claim.**

For every analytic, univalent function on the open unit disk that is normalized by f(0)=0, f'(0)=1 and whose image is starlike about zero, its Taylor coefficients satisfy

\[
\bigl||a_{n+1}|-|a_n|\bigr|\leq1\qquad(n=1,2,\ldots),\quad a_1=1.
\]

Hayman–Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2#page=136), Problem/Update 6.46, printed p. 135, explicitly credit the solution to Yuk Leung, *Successive Coefficients of Starlike Functions*, Bulletin of the London Mathematical Society 10(2) (1978), 193–196, [DOI 10.1112/blms/10.2.193](https://doi.org/10.1112/blms/10.2.193). The publisher's [issue contents](https://academic.oup.com/blms/issue/10/2?browseBy=volume) confirm those bibliographic details.

The exact target, normalization, update, and bibliography were visually checked. The outer absolute-value bars are essential: ordinary text extraction dropped them. [Arora–Ponnusamy–Sahoo, arXiv:1903.10232v1, p. 2, Theorem A](https://arxiv.org/pdf/1903.10232v1#page=2) independently restates the same credited theorem. Leung's original four-page proof was not obtained or independently verified. This is a verified attribution and exact-target match, not a reconstruction of his proof.

`PROOFS.md` gives complete elementary controls, including normalization/scaling, starlikeness of a two-pole family, that family's coefficient inequality, and exact sharpness examples. These controls do not prove the theorem for arbitrary starlike functions.

The live queue still said `queued`, `0/5`. Bounded repository duplicate checks found no earlier attempt on this target. The full imported corpus and prior AI report were not inspected. See `SOURCE_VERIFICATION.json` for exact inspection limits.

Source verification ended fresh proof search before the five-approach budget. No artificial five-attempt log is claimed. Publication requires a fresh independent audit; no remote changes were made.

## Reproduction and publication boundary

Run `python verify.py` for standard-library exact rational controls, and `python verify_integrity.py` for the frozen allowlist and hashes. A passing finite test is not a proof of the historical theorem, and file hashes certify bytes only.

Only this `author/` directory is a publication candidate. It contains authored mathematics, code and public verification metadata. No source PDF, source extraction, rendered source page, dataset contents, or private coordination is included.
