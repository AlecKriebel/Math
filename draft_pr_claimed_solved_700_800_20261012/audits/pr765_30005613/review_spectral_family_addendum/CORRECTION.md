# Correction to the closed spectral-family source reading

Recorded UTC: 2026-10-16T04:50:55.530062+00:00. PR #765 / problem 30005613 / OWR-14297736-021. Exact frozen candidate head: 021518f6f65a86658f72e0b31bfa0814bf1aa25d.

The previous spectral-family REPORT.md contains a source-reading error. Both displayed point-spectrum equalities in the proof discussion on PDF page 16 of Krejcirik, Spectral geometry: old questions and new answers, arXiv:2609.28602v1, DO have closure bars over the point spectrum. I failed to notice them in the earlier page inspection. The survey is correct on this point. I withdraw the statement that its equality is imprecise.

## Exact correction

The superseded sentence in the preserved report is:

> The survey’s displayed equality of the entire spectral set with point spectrum for the disconnected tower is imprecise under the standard countable-eigenvalue definition; I do not use it.

The correct reading of the first displayed equality is

    sigma(-Delta_D^(Omega-prime))
      = closure(sigma_p(-Delta_D^(Omega-prime)))
      = [0,infinity).

The repeated equality later in the same paragraph also places a closure bar over sigma_p and its argument. Thus the survey states closure of the point spectrum, not equality of the countable point-spectrum set itself with the nonnegative semi-axis.

This addendum supersedes the quoted sentence and my parent-directed message describing the source equality as imprecise. The earlier closed review, its manifest, and every original candidate byte are preserved unchanged.

## Fresh verification and provenance

On 2026-10-16 at approximately 04:49:58 UTC, after the parent reported the overlooked bars, I freshly viewed the entire full-resolution page-16 image supplied by the parent. Both bars are plainly visible: one in the first displayed spectral equality and one in its later repeated equality. This is a fresh read-only visual check of that image, not a claim that I independently downloaded or rendered another PDF during this addendum.

The viewed image is ../private_sources/root_survey_page16.png, SHA256 b41313cb7cd753e88b8465240adf001e8f98aa2964bc99324431bc84c63eb79c. The parent identifies it as rendered from the same v1 PDF independently downloaded by both reviewers: 2,413,179 bytes, SHA256 d9d296eec2dcebc5b5cb7ce97257f4efb0ab3203f1265dc317be05f804899d30. My preserved SOURCE_RECEIPTS.json independently records that PDF identity from the earlier download. The source is [arXiv:2609.28602v1](https://arxiv.org/pdf/2609.28602v1), submitted 23 September 2026, PDF p.16. I did not copy or modify the parent image, download another source body, or create disposable source scratch for this addendum.

The exact earlier source-viewing instant was not captured. The prior log confirms completion of the relevant page checks by 04:44:17.033435 UTC; the erroneous report was subsequently closed at 04:47:51.750157 UTC. The parent’s correction arrived after that closure and before this addendum’s fresh check; I do not invent an exact message-arrival time.

## Impact and disposition

This is one resolved source-description issue in my audit, with zero unresolved issues and zero candidate theorem issues introduced. The candidate itself correctly distinguishes pure point spectral type from every spectral point being an eigenvalue. Its assertion that the closure of the eigenvalues is [0,infinity) agrees with the corrected source formula.

No mathematical proof step, spectral-completeness conclusion, finite-window dependency, or scope statement requires repair. The prior spectral-family theorem verdict remains PASS. No further mathematical testing was necessary for this typographical source-reading correction; the new check directly verifies the disputed bars. Historical priority remains outside the reviewed verdict.

Original review preservation was checked before writing this addendum. Every prior authored file still matches the prior closed manifest. The original MANIFEST.json SHA256 is 4ecbce1a7321c0f6ccb6f9103c9a0af9bbb9a8827cc41b3906f0348585cef0ad. This addendum is an append-only sibling record and does not silently rewrite the mistake.
