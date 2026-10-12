# Independent primary-source baseline

Prepared 2026-10-03, before reading the candidate proof, result, checks, state, or historical review. Only the two routing files SOURCE_MANIFEST.json and SOURCE_NORMALIZATION.md were read from the candidate. The retrievals below were independent, and their whole PDF hashes match the routing metadata.

The original question is Hayman–Lingham, Research Problems in Function Theory, arXiv:1809.07200v2, printed page 65 / PDF page 66, Problem 3.16, attributed to P. J. Rippon. For compact E in R^n, n >= 3, define

    A(E) = {x in E : integral_0^1 cap(E intersect closed B(x,r)) r^(1-n) dr < infinity}.

The target is a direct proof that A(E) is polar, perhaps with a precise sharpness statement. The source already knows the conclusion from Kellogg's theorem. Its Update 3.16 reports no progress to the editors. Thus a fresh proof of the conclusion alone is not a new theorem, and an invocation of Kellogg or the Wiener equivalence alone does not answer the method request.

Original PDF: https://arxiv.org/pdf/1809.07200 ; 1,706,228 bytes; SHA256 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0. Locally extracted page text was read in full. Web extraction independently agrees on the displayed formula, domain, restriction x in E, method request, and update.

Hedberg–Wolff, Thin sets in nonlinear potential theory, Annales de l'Institut Fourier 33(4) (1983), 161–187, DOI 10.5802/aif.944, is independently retrieved from https://www.numdam.org/item/10.5802/aif.944.pdf ; 1,782,353 bytes; SHA256 f351a967ae723f590d85da9a886ca4f6d8a1a21f7de8315f83180d9dcf3b5006. Introduction pages 161–165 and the direct Borel-set argument pages 173–174 were read; both pages 173–174 were additionally rendered and visually inspected to disambiguate OCR formulas.

Theorem 2, page 165, asserts the Kellogg property for Bessel (alpha,q) capacity, and its page 173 Lemma 2 localizes a Borel counterexample to a compact positive-capacity set with uniformly small Wiener integral. Page 174 pairs this set with its capacitary measure and Theorem 1's energy estimate to obtain a contradiction. The source's page 163 ordinary Choquet capacitability statement concerns Borel/Suslin sets. This is distinct from its page 162 fine-topological Choquet property, which already implies the Kellogg property and would be a circular foundation if silently invoked to prove the target.

The Bessel normalization is not literally the Newtonian kernel. With alpha=1, q=2, d=n>=3, its small-scale singularity matches Newtonian capacity up to constants, but a submitted direct Newtonian proof should be checked on its own and should not silently identify the capacities. The source already contains the localization-plus-capacitary-measure mechanism; any reconstruction must credit that mechanism and avoid claiming a new general theorem or first priority.

The source's earlier ball notation is open, while the compact subset assertion in its localization argument requires attention. The independent proof below uses genuinely compact intersections with closed balls and does not transfer that notational issue into the audit.

Raw copyrighted PDFs, extracted text, and rendered pages are private and ignored. No individual was contacted.
