# Source and prior-work gate

Checked 2026-10-03 UTC.

## Identification

Catalogue locator: https://www.unsolvedmath.com/problems/2306038, code AMR-022-6038. Direct retrieval returned HTTP 403. The pinned record was used only to identify the primary source and exact problem. Generated status/findings were not treated as mathematical evidence.

Hayman–Lingham, [Research Problems in Function Theory, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200), printed p. 131 / PDF leaf 132: Problems 6.37–6.38 and both updates were read and visually checked. Reference [576], printed p. 237, was also read. The problem's notation is restored explicitly in `PROOF.md`.

Update 6.38 already reports convergence for every positive power, despite the imported open-status label. It cites I. M. Milin (1968). The two exponents used in the question and update differ by a factor of two; this does not obstruct the conclusion.

## Resolving publication

V. I. Milin, *O sosednikh koeffitsientakh nechetnykh odnolistnykh funktsii*, Sibirsk. Mat. Zh. 22:2 (1981), 149–157. English translation: *Adjacent coefficients of odd univalent functions*, Siberian Math. J. 22 (1981), 283–290, [DOI 10.1007/BF00968424](https://doi.org/10.1007/BF00968424). [Math-Net](https://www.mathnet.ru/eng/smj6431).

The complete nine-page Russian PDF was obtained. The complete relevant proof, pp. 149–155, was read from both extracted text and page images:

- p. 149: normalization and the exact Lucas exponent;
- pp. 150–151: Theorem 1 and logarithmic-coefficient corollary;
- pp. 151–153: definitions and Lemma 1, including the Lebedev–Milin input;
- pp. 153–154: full proof of Theorem 2, including the radial estimate, coefficient bound, and Abel summation;
- p. 155: Corollaries 1 and 2 and the exponent-zero obstruction.

The separate starlike-function theorem in Section 3, pp. 155–157, is not needed for the all-odd-function summability conclusion and is not represented as an audited dependency. Theorem 2, not the abstract's numbering, is the correct theorem locator in the paper.

## Bibliographic correction

The source collection's reference [576] is I. M. Milin, *Adjacent coefficients of univalent functions*, Dokl. Akad. Nauk SSSR 180:6 (1968), 1294–1297, [Math-Net](https://www.mathnet.ru/eng/dan33933).

All four pages of that paper were obtained and read visually. Its Theorem 1 bounds successive coefficient differences for general normalized univalent functions. Its Theorem 2 gives an n^(-1/2) difference estimate for odd functions with nonzero growth parameter. It does not state the universal positive-weight summability conclusion used here.

The unrestricted resolving theorem is explicitly in the 1981 paper by V. I. Milin. The initials are distinct and must not be silently interchanged. This note cites the verified 1981 theorem and does not claim to determine the earliest possible proof or the origin of the bibliography error.

## Prior repository work

Read-only checks in AlecKriebel/Math preceded drafting:

- All-state PR searches for the exact ID, exact code, “6.38”, and “Milin” returned no matches.
- Default-branch code searches for the exact ID and the joint Lucas/univalent topic returned no matches. Search-index completeness is not assumed.
- Exact-ID branch and commit searches returned no matches.
- The actual root listing and nontruncated 580-entry `problems` subtree were checked and contained no matching ID or topic path.
- The separately retrieved queue row was `queued`, `0/5`; this was not used alone to infer the absence of prior work.

These checks establish only that no matching prior attempt or PR was located in the checked surfaces, not an exhaustive statement about all repository history.

## Decision and limits

The exact target has a published affirmative solution. Proposed disposition: `already_solved`, `1/5`. The independent review remains pending. No new-resolution, current open-status, exhaustive-priority, or external-human-review claim is made.

Only original exposition, source citations, reading-scope statements, and auxiliary verification files are proposed for repository inclusion. Third-party source PDFs, scans, extracted full texts, catalogue imports, and access logs are excluded.
