# Sources, attribution, and exact target

Historical source checks: 10 October 2026. These are bounded search findings, not a certificate that no unpublished or unindexed solution exists. The independently required source-description correction is applied below. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns.

## Target

Emmanuel Kowalski, joint work with K. Soundararajan, “Twisted multiplicativity and exponential sums,” in *Analytic Number Theory*, Oberwolfach Report 50/2022, printed pp. 2929–2932. Problem 4 is on printed p. 2932, PDF p. 38.

- Official report: https://ems.press/content/serial-article-files/46986
- DOI: https://doi.org/10.4171/owr/2022/50

The question concerns integral polynomials and normalized complete additive exponential sums at prime modulus. Its two regimes are equality for all nonzero frequencies at one large prime, or at every sufficiently large prime. It asks for algebraic relations; it is not a conjecture that all such pairs are affine-equivalent. A single-prime conclusion over the residue field must not be silently promoted to a characteristic-zero conclusion.

## Prior generic theorem

E. Kowalski and K. Soundararajan, *Exponential sums, twisted multiplicativity and moments*:

- https://arxiv.org/abs/2107.06527
- https://arxiv.org/pdf/2107.06527
- Published 2022 in *Analysis at Large*: https://doi.org/10.1007/978-3-031-05331-3_13

The current arXiv record retrieved in this pass lists v1, 14 July 2021, 26 pages. The theorem and definition numbering in that version must not be confused with the published version. The relevant primary locations read are Definition 1.8, Remark 1.9, Theorem 1.10, Theorem 6.3, Propositions 6.5–6.6, and the OWR statement above. In the retained arXiv v1, Definition 1.6 additionally requires that f have simple roots and that its derivative have degree d-1; the derivative is also required to be squarefree, with distinct critical values. These are the source's stated conventions, not hypotheses of Theorems A and B in [PROOF.md](PROOF.md). The Sidon–Morse definition has an ordinary Sidon option and a symmetric option that additionally requires equivalence to an odd polynomial. Merely having a symmetric-Sidon set of critical values is not substituted for that stronger definition. The prime-size restrictions in Theorem 6.3 include `p > 2d-1` and `p` not dividing `d-1`.

There is a convention tension within that arXiv version: Lemma 6.1(2) asserts invariance under arbitrary output translations, whereas a translation can give f a multiple root by moving a critical value to zero. We do not resolve or use that source-level issue here.

This existing machinery gives rigidity in its restricted class. The present elementary low-degree proof does not rely on it and is not claimed as a new solution to the unrestricted problem.

## Additional primary talk notes found in this pass

E. Kowalski, joint with K. Soundararajan, *Remembrances of polynomial values: Fourier’s Way*, Wisconsin talk notes dated 25 March 2021:

- https://people.math.ethz.ch/~kowalski/wisconsin.pdf

All 12 pages were rendered and visually inspected; the PDF is handwritten and its text extraction contains no substantive text. Page 5 states generic rigidity at a large prime over the algebraic closure of the finite field, followed by a rational-polynomial version. Page 6 asks whether indecomposability can replace genericity. Pages 9–12 describe the Fourier-sheaf and endomorphism-representation route. These are an earlier announced restricted theorem and research question, not an unrestricted classification or a later resolution.

The 2021 paper lists an in-progress work with the related title “Remembrances of polynomial values: du côté de chez Fourier.” Fresh exact-title searches, and checks of the author's current paper and unpublished-note lists, did not locate a full later manuscript resolving the unrestricted question:

- https://people.math.ethz.ch/~kowalski/papers-books.html
- https://people.math.ethz.ch/~kowalski/notes-unpublished.html

This absence is bounded negative evidence only. The author's papers list does include the published 2022 exponential-sums paper.

## Recent but different-modulus result

Francesco Naccarato, *The arithmetic of critical values I: equicritical quartic polynomials*, *International Mathematics Research Notices* 2026, issue 13, rnag141, published 6 July 2026:

- https://doi.org/10.1093/imrn/rnag141
- https://academic.oup.com/imrn/article/2026/13/rnag141/8725239

Its Section 5.3 and Corollary 5.3.1 concern Weyl sums modulo `p^2`. That is not the prime-modulus condition in the target. No application of this source is used in the present proof, and its full proof has not been independently audited here.

## External standard theorem used for the all-primes cubic case

Romyar Sharifi, *Algebraic Number Theory*, Chapter 7, Theorem 7.2.2 (Chebotarev):

- https://www.math.ucla.edu/~sharifi/notes/algnum-ch07.html

The theorem gives positive density to every Frobenius conjugacy class in a finite Galois extension. Applied to a 3-cycle in the splitting field of an irreducible rational cubic, it gives infinitely many good primes where that cubic has no root. This is the only non-elementary input in Theorem B. Theorem A and the explicit obstruction examples are elementary.

## Search and acceptance limits

The pass began with exact target/title searches and author/topic searches, then followed the named in-progress work and the official author bibliography. Irrelevant search-engine collisions were not treated as mathematical evidence. The primary report and 2021 paper were read from retained complete PDFs and text; the Wisconsin PDF was newly retrieved and visually read. A direct homepage retrieval did not complete; it was not retried. A separately available web copy supplied the bibliography links.

No complete arbitrary-degree classification was established or accepted. The outcome is a complete degree-at-most-three theorem with an exact residual. The calculations provide reproducible finite checks, not proof by enumeration. Neither the low-degree theorem nor the obstruction examples are claimed to be novel.
