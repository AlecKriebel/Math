# Source audit and reproducibility receipt

## Primary documents

- Original target: OWR 25/2021, David Witt Nyström's contribution, pp. 1321–1325. https://ems.press/content/serial-article-files/46904 . Read the full contribution; the ambient equation, smooth boundary data, permitted semipositivity, and the interior-failure goal agree with the candidate.
- Ross–Witt Nyström, *Applications of the duality between the Homogeneous Complex Monge–Ampère Equation and the Hele-Shaw flow*, AIF 69 (2019), 1–30. https://www.numdam.org/item/10.5802/aif.3237.pdf . The downloaded file has 31 PDF pages including its cover. SHA-256: `724e742d033b3401b6938011cf07ee4faf79a7d13b14d22bb9ca1a90969cc0e2`; 3,158,845 bytes.
- Full author version: https://arxiv.org/pdf/1509.02665 . SHA-256: `7436b1ef2f43c4bc3b9ca047543a9a85e6a58d06936ff75b4826b4692fd47c3a`. Read alongside the published version. The published numbering and pagination are authoritative for the review.

## Exact checks

The published Definition 1.2 permits finite-time arc tangency. Proposition 2.5 supplies the full current formula and regularity. Theorem 2.15 permits a smooth modification of the area form on the interior side of a smooth boundary. Proposition 3.4 applies it on a covering surface and produces a globally smooth strictly positive form. The covering punctures lie in components of the complement of the *closure* of Ω_T; the overbar is visible in the PDF and can disappear in text extraction. This is consistent with resolving an arc that joins complement components.

Theorem 6.2's proof supplies nonzero pre-contact velocity; it does not itself claim interior nonsmoothness. The candidate's additional Green-function/Legendre argument is separately reviewed. Proposition 4.2 and Theorem 4.4 provide the smooth twisting correction and the Legendre formula. Appendix A (Theorem A.1 and Corollary A.2) proves smooth Green dependence. I checked these proofs and hypotheses rather than relying only on their titles or abstract.

The full published PDF was initially incomplete after a 45-second transfer. Resuming the same primary download completed it; pdfinfo, text extraction, file size, and checksum succeeded. The benign PDF annotation warning did not affect text or the rendered mathematical pages. Published printed pp. 15–16, 24, and 28 were rendered and inspected.

Reading PDFs and the independently authored scalar checker were the only executable-work components of the review. No external source code was executed. No remote mutation, outreach, or publication occurred. This source audit is not a comprehensive novelty search.
