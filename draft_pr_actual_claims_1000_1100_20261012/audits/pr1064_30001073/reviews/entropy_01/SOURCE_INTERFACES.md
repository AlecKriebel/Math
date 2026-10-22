# Fresh primary-source interfaces

Scope: version-bound source checks for head `bdefe31b9d226c8f27008d13f57775d5de8df3d7`, made after freezing `INDEPENDENT_DERIVATION.md` except that the exact original problem was read before that freeze. Full third-party documents, copied text and rendered images stay in ignored `sources/raw/`. This file contains authored analysis and bibliographic/custody metadata only.

## Original problem interface

The [official EMS publisher page](https://ems.press/journals/owr/articles/2090) identifies *Discrete Geometry*, Oberwolfach Reports 5(4), pp. 2477-2556, DOI [10.4171/OWR/2008/44](https://doi.org/10.4171/OWR/2008/44). A fresh download of [official EMS file 46191](https://ems.press/content/serial-article-files/46191) contains the full report. Printed pp. 2549-2550, corresponding to PDF pages 73-74, were extracted and visually inspected in full. Problem 9 is attributed to Alexander Barvinok and Alex Samorodnitsky.

The question fixes gamma>=1 and assumes a nonnegative doubly stochastic n by n matrix with the unnormalized sum of entry squares at most gamma. It seeks exp(-n) up to a polynomial factor in n. The preceding page records van der Waerden's already-proved lower bound, so the submission supplies the missing upper direction. The following note distinguishes the stronger entrywise hypothesis a_ij<=gamma/n. The candidate uses the norm hypothesis itself. The asymptotic reading permits n>=2 for the prefactor-free consequence; its all-n bound includes a constant prefactor.

Retrieval: 2026-10-14T03:32:38.901659+00:00; 731001 bytes; SHA-256 `3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35`. Fresh bytes equal the submission's recorded PDF identity. Receipt: `sources/ORIGINAL_FETCH_RECEIPT.json`.

## Direct prior entropy comparison

The full [Anari-Rezaei arXiv:1811.02933v2 PDF](https://arxiv.org/pdf/1811.02933v2) was fetched afresh. Its title page identifies v2 and a December 2019 revision. Section 1.4, pp. 5-6, explains the substitution of Gibbs assignment marginals for input entries. The complete section 4, pp. 10-13, was read; pp. 11-12 and the title page were visually inspected. Equation (6), p. 12, has precisely the credited random-order comparison. The paper also credits Radhakrishnan's entropy proof of Bregman's theorem.

In notation B for Gibbs marginals, its comparison is

    log per(A) <= sum_ij b_ij log(a_ij/b_ij) + sum_i T(B_i),
    T(p) = sum_k p_k E_pi log(sum_{j at or after k in pi} p_j).

The candidate's random row ordering induces the same uniform column ordering after conditioning on X. Its independently checked Jensen/integral calculation gives T(p)<=-1+sum_j g(p_j). This substitution gives the candidate's entropy/KL bound exactly. Thus the core marginal/random-order mechanism is prior work; the source comparison supplies no first-method or first-solution certificate. The candidate's positive-history conditional proof handles zero entries directly without needing a greedy distribution on impossible histories.

Retrieval: 2026-10-14T03:34:47.675471+00:00; 248293 bytes; SHA-256 `c6d22620c7963ead242068941ef05562c8c72c40accea40cd3304705d546b405`. Fresh bytes equal the submission's recorded PDF identity. Receipt: `sources/ANARI_REZAEI_FETCH_RECEIPT.json`.

## Supplementary bounded checks

Fresh version-bound downloads also match the submission's recorded hashes:

- [Anari, arXiv:2608.28031v2](https://arxiv.org/pdf/2608.28031v2): 349123 bytes; SHA-256 `e166fb3d448e33307396df4eb6d00bef8b804c6387d8aba56c959ea7ff942927`; retrieved 2026-10-14T03:35:53.083027+00:00. The title/version page, section 4 Lemma 7 on pp. 9-10, and every extracted-text Frobenius occurrence on pp. 29-31 were read. The sequential relative-entropy identity and the numerical-optimization context of those occurrences agree with the submission's bounded description. This does not rule out unstated consequences elsewhere.
- [Gurvits-Samorodnitsky, arXiv:1408.0976v1](https://arxiv.org/pdf/1408.0976v1): 264183 bytes; SHA-256 `0cd940d197d6dab71ca7e4ef580183a9f7c09100683f7c46add97bc30a899f28`; retrieved 2026-10-14T03:35:53.451475+00:00. The title/version page and full pp. 13-14 were read. The Orlicz row-norm upper bounds there yield a constant-to-the-n entry-product estimate, consistent with the ledger's limited statement.
- The publisher DOI for [Radhakrishnan's 1997 article](https://doi.org/10.1006/jcta.1996.2727) did not open in the web tool during this review. The classical attribution is corroborated by the directly inspected Anari-Rezaei section 1.4 and bibliography, p. 22. No fresh full-text inspection of Radhakrishnan's paper is claimed, and the proof does not depend on it.

These checks establish source interfaces and version identities. They do not reproduce the prior audit's retrieval timestamps, original proof edits, removed diagnostics, or bounded search execution. No global literature absence, novelty, priority, sharp exponent, or present worldwide open status is certified.
