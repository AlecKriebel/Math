# Historical primary-source access report

Bounded source retrieval for PR #662, problem 2306086, supplied immutable head `e31701151c331a6eed9224fb37a75a374ea1043e`.

## Result

The January 1979 Rodemich original is recovered, and its full relevant page has been visually read. The Jenkins 1960 original remains unavailable through the checked public routes. This report does not adjudicate novelty, priority, or the PR disposition.

## Rodemich: the missing functional is identified

The source is Eugene Rodemich, *An inequality for univalent functions with real coefficients*, Notices of the AMS 26 (January 1979), abstract 763-30-11, printed A-68, received October 20, 1978. The complete relevant page is PDF page 152 in the publisher's 276-page issue. The issue cover independently confirms January 1979, volume 26, number 1, issue 191, pages 1-82 and A-1-A-190.

The publisher URL returned HTTP 403 through the available transport. A CDX catalogue request found a public Wayback capture dated 2022-06-20T05:00:40Z. Downloading that public replay returned an unencrypted PDF with HTTP 200, 39,063,095 bytes, SHA-256 `04df2b98e61313f7afb1da73329dc536237ce6d8c0f7431a9409991f693a64a0`. This is an archived publisher scan, not the separate Internet Archive microfilm item whose scan files are marked private. No private file was requested.

Provenance:

- Publisher: https://www.ams.org/journals/notices/197901/197901FullIssue.pdf
- Public replay: https://web.archive.org/web/20220620050040id_/https://www.ams.org/journals/notices/197901/197901FullIssue.pdf
- Catalogue and transport receipts, complete PDF, full text, complete A-68 rendering, and cover rendering are under this review's ignored `tmp/`; hashes are in `SOURCE_BINDINGS.json`.

The announced hypotheses are exactly a univalent function on the unit disk with expansion
\[
f(z)=z+a_2z^2+\cdots,
\]
with all Taylor coefficients real. Write
\[
q=\frac{|z-\bar z|}{1-|z|^2}.
\]
The visually transcribed displayed inequality is
\[
\left|\arg\big((1-z^2)f'(z)\big)\right|
\le
\begin{cases}
2\arctan q,&q\le1,\\
\pi/2+\log q,&q>1.
\end{cases}
\]
The argument convention is not explicitly specified in this short abstract. The abstract announces a variational-method result and supplies no proof. The title in the scan contains an apparent typographical misspelling of “univalent”; the class definition removes any ambiguity about the subject.

The left-hand side is now verified: it is an argument bound on `(1-z^2)f'(z)`, not a displayed bound on the PR's centered pre-Schwarzian modulus
\[
\left|(1-|z|^2)f''(z)/f'(z)-2\bar z\right|.
\]
These functionals are related, so the difference alone must not be promoted into a mathematical nonimplication or priority clearance. For example, with an analytic logarithm `G=log((1-z^2)f')`, differentiation gives `G'=f''/f' - 2z/(1-z^2)`; translating an argument estimate into the target derivative estimate would require an additional valid argument. This bounded retrieval task does not supply that implication or establish that no implication exists. In particular, differentiating the displayed absolute-value inequality formally would not be justified.

## Jenkins 1960: exact content remains unknown

The bibliographic identity is securely matched by DOI, JSTOR's issue table, Crossref, OpenAlex, Semantic Scholar, OpenAIRE, and Jenkins's own 1962 bibliography: James A. Jenkins, *On Univalent Functions With Real Coefficients*, Annals of Mathematics 71(1) (1960), 1-15, DOI `10.2307/1969877`.

The bounded access checks used materially distinct routes:

1. Publisher/JSTOR article and issue pages; no full article text exposed by the available reader. The attempted Annals site page was unavailable.
2. Internet Archive periodical catalogue and issue metadata. The exact January 1960 issue exists, but `access-restricted-item=true` and its PDF/OCR files are marked `private=true`. Those files were not requested, nor were accounts or borrowing used.
3. OpenAlex and Semantic Scholar bibliographic/OA APIs. OpenAlex has only the DOI location and no repository full text. Semantic Scholar's `openAccessPdf` URL is empty and status is `CLOSED`.
4. OpenAIRE's DOI-specific query. It returned DOI and zbMATH metadata links, with no full-text repository location.
5. Public Wayback CDX checks of the standard JSTOR PDF route (no PDF capture returned) and the historical `pdfplus` route (request timed out). The timeout is not evidence that no capture exists.
6. Exact-title/DOI web searches, which surfaced bibliographic mentions rather than a publicly accessible original.

A relevant primary source already supplied by the parent was independently read and rendered: Jenkins's 1962 *The General Coefficient Theorem and certain applications*, DOI `10.1090/S0002-9904-1962-10670-3`. Its complete printed p7 explicitly credits the 1960 paper with both point-value regions and derivative bounds. Printed p9 identifies reference 4 as the exact Annals article. That survey paragraph does not specify a derivative order or functional, an exact estimate, or the normalization needed for those derivative results.

Consequently, describing Jenkins 1960 as dealing **only** with function-value regions is unsupported. Conversely, claiming that it proves the target centered pre-Schwarzian gap is also unsupported. Its exact theorem statements, hypotheses, equality conditions, and relevance to the target remain an access gap. Metadata, introductory indexing, and the author's survey cannot substitute for reading those statements.

## Limits and completion

One of the two requested historical originals has been recovered and checked visually. The remaining source gap is explicit. Completion estimate for full two-source verification: **50%**. Completion estimate for this bounded access subtask and its requested reports: **100%**. No novelty or disposition conclusion is supplied. No communication with individuals, Git operation, remote mutation, PR action, paper preparation, or publication occurred.
