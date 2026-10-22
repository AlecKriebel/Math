# Primary-source reading ledger

This ledger records this audit family's own reads. Earlier acceptance reports, sealed PASS reports, PR210 results, and other agents' conclusions were not proof authority. The source originals, extracted text, and selected page renders are private in `private_primary/`; only authored descriptions and hashes are selected for the audit packet. The private manifest inventories retained bytes.

## Reznik--Garcia--Koiller v11

- URL: https://arxiv.org/pdf/2004.12497v11
- Retained private file: `private_primary/reznik_v11.pdf`.
- PDF bytes: 3,389,610; SHA-256: `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`.
- Version printed on p1: arXiv:2004.12497v11, 29 October 2020. PDF heading: *Eighty New Invariants in the Elliptic Billiard*.
- Full extracted text of all 17 PDF pages read. This is not a claim that every diagram or linked reference/video was inspected.
- Full relevant pages visually read: printed p3 (signed-area definition), p9 (beginning of Section 3.9), p10 (continued definitions and distinction of the outer locus's own foci), p12 (complete Table 10 and Figure 8).
- Relevant conclusion: Table 10's `k904,a` is the odd product of the two primed dagger areas. Section 3.9 defines inversions of vertices about unit circles centered on the original foci, and applies primed symbols to outer vertices. The separate double-dagger outer-locus-foci construction is distinguished. The Section 2 area is the ordered signed cross-product sum.
- Limit: no novelty, present worldwide status, or interpretation of an unread linked reference is inferred from the table's proof column.

## Reznik--Garcia--Koiller v10

- URL: https://arxiv.org/pdf/2004.12497v10
- Retained private file: `private_primary/reznik_v10.pdf`.
- PDF bytes: 3,360,046; SHA-256: `f1658e31b96fbbaa6c528b0611de54a5e2df9f27c1e505fb2e927f3833bdd48b`.
- Version printed on p1: arXiv:2004.12497v10, 25 October 2020. PDF heading: *Seventy New Invariants in the Elliptic Billiard*.
- Full extracted text of all 16 PDF pages read. Complete p11 Table 9 visually inspected. Page 12 was also viewed when locating the table, but it contains figures rather than the table; its redundant render was removed from this audit's own folder during disk-pressure mitigation.
- Relevant conclusion: `k808,a` is the same odd primed dagger-area product; the original-vertex odd product is `k807,a` in this version. The version-to-label identification is directly verified and not assumed from current metadata.
- Limit: no absolute priority claim follows from identifying an earlier label.

## Published Stachel parametrization

- Official publisher PDF: https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf
- Institutional primary repository PDF: https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf
- Both independently downloaded bodies had 726,042 bytes and SHA-256 `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`; they compared byte for byte equal. The institutional filename's journal wording is not relied upon: the PDF itself identifies *European Journal of Mathematics* 8 (2022), 1602--1622.
- Retained private file: `private_primary/stachel_published.pdf`. The byte-identical redundant official download was removed only from this family's own folder to conserve space. Its hash, size, URL, and equality evidence are preserved here.
- Full extracted text of all 21 PDF pages, printed pp1602--1622, read. Full relevant p1613 and p1614 visually read; p1614 contains all of Theorem 4.3, equation (4.9), its proof, and Figure 6. The preceding canonical/Lie-group derivation and the following coordinate context were read in full text.
- Relevant conclusion: caustic eccentricity is the Jacobi modulus; canonical vertices differ by twice the shift, with shift `2*tau*K/N` and coprime period/turn; equation (4.9) gives the required axes.
- Printed nearby p1613 typo independently noticed/confirmed: the displayed alternating sign for `dn(u+2jK)` is false for odd `j`. Correct `dn(u+2K)=dn(u)` is used throughout this audit. The theorem and its axes formulas do not use that false sign.
- Limit: the input theorem is credited. This audit is not an independent priority investigation of canonical parametrizations and does not claim to verify every historical statement or cited theorem in Stachel's paper.

## NIST DLMF analytic facts

- https://dlmf.nist.gov/22.4 : Tables 22.4.1, 22.4.2, 22.4.3 read directly, including the principal periods, pole/zero grids, imaginary anti-period signs, quarter shifts, and table erratum. DLMF version shown: 1.2.8, released 2026-09-15.
- https://dlmf.nist.gov/22.8 : equations 22.8.1--22.8.3 read directly and used for the exact algebra derivation. Some alternative and poristic identities were also returned/read but are not inputs to this proof.
- https://dlmf.nist.gov/22.13 : Table 22.13.1 and equations 22.13.1--22.13.3 directly read for the sn/cn/dn derivatives and critical orders.
- Direct Python HTML fetches returned HTTP 403; browser-tool primary-page reads succeeded. `private_primary/DLMF_WEB_EXTRACTION.txt` preserves the first combined returned extraction, with its exact file hash in the private manifest. That extraction is a tool representation, not raw HTML, and does not include all later derivative-page text. The later derivative-table reading is evidenced by this task's tool transcript; no raw-byte equivalence is claimed.
- Limit: these are standard analytic inputs, not an independent rederivation of the entire Jacobi function theory. Compact-torus holomorphic constancy and equality of zero/pole order are standard complex analysis; the application and all exceptional fibers are supplied explicitly in `DERIVATION.md`.

No outside individual was contacted. No linked video, correspondence, other campaign proof, or related manuscript served as proof authority. Primary reading does not accept any publication package or historical priority assertion.
