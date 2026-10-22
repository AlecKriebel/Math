# Primary-source check

Date: 2026-10-03.

Source: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, dated 21 September 2018.

- Record: https://arxiv.org/abs/1809.07200v2
- PDF: https://arxiv.org/pdf/1809.07200v2
- Location: Problem 7.54 and Update 7.54, printed page 177, PDF page 178.
- Retrieved PDF SHA-256: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
- Inspection: both searchable text and a rendered image of the complete page.

The source defines the map phi_t(z) = exp(t z) - 1, iterates it by composition, and evaluates every positive iterate at z = -1. It asks for a uniform modulus bound of 1 on all coefficients of these formal power series. This is precisely the submitted recurrence F_0 = -1, F_(n+1) = exp(t F_n) - 1.

The first displayed expansion really prints the second term as t/2!, rather than t^2/2!. This was checked visually, not inferred solely from extracted text. The next display and the defining map make the missing exponent an unambiguous typographical error. The package corrects it transparently and does not alter the problem.

Update 7.54 says, “No progress on this problem has been reported to us.” This supports the package's account of the 2018 update, not a claim about all subsequent literature.

This audit does not independently certify the package author's repository-search history, the catalogue identifier mapping, the number of prior attempts, or an exhaustive modern literature search. These are not mathematical premises of the partial theorem. No copied source PDF or source-page image is included in the audit deliverables.
