# Provenance and editorial scope

Edition date: 9 October 2026 (UTC). Target: 2307034 / AMR-022-7034, Hall Problem 7.34.

## Original documents and edition identities

The independent audit reviewed the original proof below. Those original bytes have not been changed. The publication edition is a separate object, and the original proof hash does not bind the edited edition.

| Document | Original bytes | Original SHA-256 | Edition bytes | Edition SHA-256 |
|---|---:|---|---:|---|
| Proof | 13273 | fa99237c49ed63a529c8b5f30ebdb6e62cf516b648e2a5a3aa8b9983cdbed71e | 12994 | 7911a494baefcaf561d26ef8cf8c4cb5ba853834bbc461e10988fc95e80924d7 |
| Independent audit | 18888 | d81979ab8ec29bed9b51315ef1b86317d598a4c9907cc3296392325586b2d7d7 | 17050 | 4c753588c70b81f6355612531d716db499d24c0f1fea07dbb37797dded8bd478 |
| Authored source ledger | 2629 | b7aa7547f0375cabe6798cf6c52f0ec12ff203ee377619503915289f44eaf9b3 | 2611 | b74e22c1a2348b2ea9dfa3a2da21d0894bf2e8a73e81dd0625250fd4c29d994f |

ACCEPTANCE.json records acceptance of the original mathematical results plus the stated explanatory clarification, and identifies the actual edited proof and audit. It does not claim that the original audit hash or original proof hash is the edited file's identity.

## Exact mathematical wording clarification

Original Section 8 sentence:

> This introduces a distant positive real singularity, so the nearby denominator need not have any polynomial multiple with nonnegative coefficients.

Edition replacement:

> This introduces a distant positive real zero of the denominator, hence a pole of the logarithmic derivative; it is a branch singularity of f when the corresponding merged exponent is nonintegral. Therefore the nearby denominator need not have any polynomial multiple with nonnegative coefficients.

The first new sentence is the explicit clarification requested by the independent audit. The second preserves the original denominator-multiple conclusion and connects it to the corrected terminology. The correction changes no accepted theorem, example, coefficient, or limitation. Positive integral merged exponents give ordinary zeros of f and still give poles of its logarithmic derivative.

## Complete editorial scope

1. PROOF.md preserves Sections 1–8, all mathematical derivations, both examples, every exact coefficient, and the full unfinished compactness discussion. Its only mathematical wording change is the quoted clarification. A paragraph about an omitted computational implementation was removed from Section 6. Section 9 retains one-of-five approach accounting while replacing obsolete audit/publication workflow statements with links to the present audit and acceptance.
2. AUDIT.md preserves its complete mathematical review: coefficient lemma, positive-real cancellation, merged-pole reality argument, half-plane and n<=2 cases, both exact calculations and the complete 14-entry rational table, integral/rational bounds, compactness/degree-drop limits, and the original wording recommendation. Introductory language now distinguishes original and edited identities; historical input-integrity and reproduction sections are omitted; derived-image identities and implementation/output references are removed. The mathematical explanation of the independent finite calculation is retained. The correction section describes the clarification as applied in this edition.
3. SOURCE_LEDGER.md retains the primary citation, source pinpoints, raw public PDF identity, inspection history, authored mathematical scope, and bounded-search caveat. Derived-image identities and implementation instructions are omitted, and the completed audit replaces the obsolete unaudited status.
4. README.md, ACCEPTANCE.json, STATUS.json, and this provenance notice are edition-specific summaries. MANIFEST.json identifies every delivered file except itself; its own identity is supplied with the reviewed publication description to avoid a self-hash cycle.

No excluded computational artifact or source document has been converted into new prose. The coefficient tables and mathematical verification discussion reproduced here were already part of the authored proof and audit. The packet contains no scripts, fixtures, checker output files, copied source text, source PDFs or images, dataset contents, or private coordination material. It includes only the authored mathematical texts and scoped public verification metadata.

## Source identity and limits

The public source is Hayman and Lingham, [Research Problems in Function Theory (New Edition), arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), revised 21 September 2018. The preserved [public PDF](https://arxiv.org/pdf/1809.07200v2) is 1,706,228 bytes with SHA-256 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0. Problem 7.34 is printed page 170 / PDF page 171. The source was inspected textually and visually on 9 October 2026; its record and stored PDF identity were checked again during edition preparation.

The 2018 manuscript reports no progress at that time. This does not certify present-day open status. The report claims neither historical novelty nor an exhaustive literature search. The distinct pure-power-sum target 2307004 / Problem 7.4 is not resolved or recounted here. The full target remains unresolved by this work, at one substantive approach consumed out of five; editorial preparation and independent verification add no proof-search approach.
