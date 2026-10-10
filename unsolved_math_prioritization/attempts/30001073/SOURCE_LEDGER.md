# Public source ledger

Checked 2026-10-10 UTC. This publication edition records public-source metadata and the completed research and audit inspection history. Source documents and source-derived text or images are not distributed. Edition preparation rechecked retained PDF identities without new retrieval, scholarly inspection or literature search. No priority claim is made.

## Original target

Alexander Barvinok and Alex Samorodnitsky, problem 9, *Discrete Geometry*, Oberwolfach Report 44/2008, printed pp. 2549–2550.

- DOI: https://doi.org/10.4171/owr/2008/44
- Publisher page: https://ems.press/journals/owr/articles/2090
- PDF: https://ems.press/content/serial-article-files/46191?nt=1
- Verified PDF size: 731001 bytes
- SHA-256: 3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35
- The source's pages 2549–2550 define an unnormalized sum of squared entries, with fixed γ. Page 2550 was visually inspected during this attempt; both pages had already been inspected in the target screen. The source distinguishes the stronger entrywise hypothesis and treats the van der Waerden lower bound as known. The requested estimate has asymptotic meaning.

## Direct prior entropy method

Nima Anari and Alireza Rezaei, *A Tight Analysis of Bethe Approximation for Permanent*, arXiv:1811.02933v2 (2019 revision).

- https://arxiv.org/abs/1811.02933v2
- PDF: https://arxiv.org/pdf/1811.02933
- Verified PDF size: 248293 bytes
- SHA-256: c6d22620c7963ead242068941ef05562c8c72c40accea40cd3304705d546b405
- Retrieved 2026-10-10T00:57:24.018765+00:00.
- Sections 1.4 and 4, especially equation (6) on printed/PDF page 12, were read; page 12 was rendered and visually inspected. Their random-order sequential comparison uses Gibbs assignment marginals in place of input entries. Equation (6), followed by the conditional Jensen step proved in PROOF.md, supplies our variational entropy inequality. This method is prior work. The main advertised bounds concern exponential-factor Bethe approximation. The inspected text does not state the bounded-Frobenius consequence here.

Jaikumar Radhakrishnan, *An Entropy Proof of Bregman's Theorem*, Journal of Combinatorial Theory A 77 (1997), 161–164.

- https://doi.org/10.1006/jcta.1996.2727
- Publisher abstract inspected for classical entropy-method provenance. The present argument does not rely on an uninspected claim in this article. An attempted download of the author's later *Entropy and Counting* exposition returned HTTP 502; that failed download is not claimed as a full-text inspection.

## Additional related bounds checked

Leonid Gurvits and Alex Samorodnitsky, *Bounds on the permanent and some applications*, arXiv:1408.0976.

- https://arxiv.org/abs/1408.0976
- PDF: https://arxiv.org/pdf/1408.0976
- Verified PDF size: 264183 bytes
- SHA-256: 0cd940d197d6dab71ca7e4ef580183a9f7c09100683f7c46add97bc30a899f28
- Retrieved 2026-10-10T00:53:51Z.
- Text extraction read, especially the upper-bound statements on pp. 13–14. Their Orlicz-norm approach gives a constant-to-the-n factor involving entry products. No assertion that those stated results directly yield the target Frobenius bound is made.

Nima Anari, *Beyond the Bethe Approximation of the Permanent*, arXiv:2608.28031v2 (2026 preprint).

- https://arxiv.org/abs/2608.28031v2
- PDF: https://arxiv.org/pdf/2608.28031
- Verified PDF size: 349123 bytes
- SHA-256: e166fb3d448e33307396df4eb6d00bef8b804c6387d8aba56c959ea7ff942927
- Retrieved 2026-10-10T00:57:24.048913+00:00.
- Primary abstract and §4, Lemma 7, pp. 9–10 read. This work keeps sequential relative entropy to improve a universal exponential approximation factor. Searches of the extracted text for Frobenius references found numerical-optimization error estimates, not the present target theorem. This observation is a bounded text check, not an exhaustive interpretation of every consequence.

## Search boundary

The search used target phrases, author combinations, Frobenius and sum-of-squares terms, and weighted marginal entropy/permanent terms. The most directly relevant marginal-entropy source and recent related work were checked independently. No source was located that explicitly states the bounded-Frobenius conclusion, but an absence from these bounded searches does not establish novelty.

The result is a self-contained proof derived from established entropy techniques and has passed independent mathematical audit. The scalar KL absorption and its application are written out in full. The classical entropy method, the original source's lower bound, and its stronger entrywise special case are not claimed as new.
