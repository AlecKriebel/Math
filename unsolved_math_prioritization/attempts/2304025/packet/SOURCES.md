# Source gate, attribution, and limits

Checked 3 October 2026. This is a partial mathematical investigation, not a certification of the current literature status for every parameter.

## Exact problem source

Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018, printed p.79, Problem 4.25 and Update 4.25.

- Record: https://arxiv.org/abs/1809.07200v2
- Full text: https://arxiv.org/pdf/1809.07200v2

The statement asks for the weighted squared circle-integral infimum over monic integer polynomials, with arbitrary positive real parameter and no degree restriction. It attributes the question to W. H. J. Fuchs. The update says, “No progress on this problem has been reported to us.” The complete problem and update were read in the rendered primary PDF, including the leading-coefficient condition. The normalized formulation in `PROOF.md` differs from the printed integral by the explicit factor `2π` only.

The catalogue entry is https://www.unsolvedmath.com/problems/2304025 . Direct access returned HTTP403 during this investigation. Its identity was recovered from a previously pinned catalogue record and then checked against the primary PDF. Generated catalogue research conclusions were not used as evidence of a proof, priority, or present open status.

The earlier listing was identified as J. M. Anderson, K. F. Barth and D. A. Brannan, *Research problems in complex analysis*, Bulletin of the London Mathematical Society 9 (1977), 129–162, Problem 4.25, pp.132–133. The indexed excerpt is consistent with the 2018 statement, but the original full PDF was not retrieved successfully. This is an explicitly incomplete historical-source check; the directly read 2018 primary compilation supplies the exact target and update.

## Classical arithmetic dependency and credit

Peter Borwein and Colin Ingalls, *The Prouhet–Tarry–Escott problem revisited*, L'Enseignement Mathématique 40 (1994), 3–27.

- Author-hosted preprint, dated 13 December 1993: https://www.cecm.sfu.ca/~pborwein/PAPERS/P98.pdf
- Publication DOI: https://doi.org/10.5169/seals-61102

The complete relevant proof text in Section2 was read from rendered author-PDF pages4–5 (printed preprint pp.3–4): Proposition1 establishes the power-sum/product-polynomial/zero-multiplicity equivalence using Newton identities and the operator `x d/dx`; Proposition2 gives the minimum-size bound; the adjacent lemmas explain translation and multiplication by a binomial. These are classical arguments, not claimed as new here. The text extraction for this old PDF was garbled, so the page images, rather than extracted text, were used.

`PROOF.md` supplies the complete needed argument independently and distinguishes ordinary multiset solutions from the distinct-term condition required for equality in the squared-coefficient norm. The six small product constructions are explicitly checked identities; they are not asserted to be novel.

## Search and claim boundaries

Bounded searches used the exact problem number, the Fuchs attribution with the printed leading-coefficient wording, weighted integer-polynomial integrals, and the Prouhet–Tarry–Escott connection. No retrieved source gave a complete all-parameter determination of the exact printed infimum. This limited negative search is not evidence that no such source exists.

No priority is claimed for the initial-parameter formulas or the higher-parameter bounds. No assertion is made that any larger specific integer case is new or open. The mathematical claim is exactly what is proved in the packet: a partial determination, not a full solution.

## Gate result

- Identity and quantifiers: checked against the primary problem and update.
- Relevant classical proof: read in full for the dependency actually used.
- Mathematical proof of the packet's stated results: provided in `PROOF.md`.
- Full all-parameter resolution: not obtained.
- Novelty / first resolution: not asserted or established.
- Computational scope: finite exact controls only.
- Redistribution: this packet includes original exposition and code; it does not include third-party PDFs, scans, or source corpora.
