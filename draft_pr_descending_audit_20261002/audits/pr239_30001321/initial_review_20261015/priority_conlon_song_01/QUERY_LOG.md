# Bounded Conlon–Song retrieval query log

Started 2026-10-15 04:42:34 UTC. This records query families and material routes; a negative result is limited to the route searched. Search result abstracts, snippets, denial pages, and metadata labels were not counted as a read full article.

## Title and DOI discovery

- Exact full title with Conlon/Song, PDF, preprint, theorem, ps, and `ps.gz` variants.
- Exact DOI `10.1016/S0304-4149(98)00095-7` with common bibliography/aggregator domains excluded.
- Primary-domain focused queries for Michigan, Illinois, Deep Blue, arXiv, HAL, CORE, CiteSeerX, and Mathematical Physics Preprint Archive.
- Search indexes repeatedly returned the same publisher, author-list, RePEc, or citing-paper records. No exact whole original was authenticated from these results.

## Author and institutional route

- Current Song author list: https://www.renmingsong.web.illinois.edu/pages/publ.html.
- Older Song author list: https://rsong.web.illinois.edu/pages/publ.html.
- Both downloaded in full, with HTML checked around the target citation. No target PDF link.
- Michigan MCAIM faculty directory: https://sites.lsa.umich.edu/mcaim/people/faculty/; actual Conlon homepage link points to `https://www.math.lsa.umich.edu/~conlon/`.
- Historical host failed DNS in direct retrieval; `https://dept.math.lsa.umich.edu/~conlon/` returned404. No target filename was guessed. Existing indexed individual Conlon PDFs were unrelated later works.

## Location metadata route

- OpenAlex DOI work API: DOI/publisher and RePEc only; repository fulltext false.
- Semantic Scholar DOI work API: nominal OA URL is DOI only.
- OpenAIRE DOI search API: useful new public `originalId` pointer to Elsevier fulltext archive; one retrieval returned403, 162-byte HTML, and stopped.
- Exact metadata requests, returned content types, byte lengths, UTC times and hashes are in `source_manifest.json`.

## Public web archival route

- Wayback CDX for historical Conlon homepage: timeout.
- archive.org public availability API for exact historical Conlon homepage and queried Song publications URL: no snapshot in those responses.
- No broad conclusion about all archive captures is made.

## MP_ARC primary archive route

- https://web.ma.utexas.edu/mp_arc/ retrieved; search form inspected.
- Author abstract-search CGI for Conlon, 1991–2000: HTTP500; not repeatedly retried.
- Static official indexes `index-95.html` through `index-99.html` all downloaded successfully.
- Case-insensitive `Conlon|Gaussian limit|Renming` search of all complete HTML responses returned zero matches.
- Static-index search is a distinct route from failed CGI search; no exact full text found.

## Exact ResearchGate record route

- Actual article link followed from public Song profile, not guessed: publication2320351.
- Indexed page explicitly says no full text is available. Direct retrieval403.
- Restored abstract equations and citing-paper snippets are indexed pointers only.
- No request-to-author button, account creation, message, email, or other contact used.

## Primary citation checks

- Full BMP2004 published PDF inherited read-only, copied privately, and hash matched; printed pp134–135/PDFpp2–3 rendered and visually inspected.
- Full BS2002 published PDF inherited read-only, copied privately, and hash matched; printedp371/PDFp27 Remark4.3 rendered and visually inspected.
- BP2001 MathNet landing page timed out; AMS official issue403. No unseen original passage was treated as a verified primary result.

## Stop condition

No authenticated full Conlon–Song copy emerged. No paywall, captcha, credentials, token, or URL encoding workaround was attempted. Metadata-only discovery and primary later citations cannot settle the exact original moment, derivative-norm, or tail bounds. Audit closed with that bounded source gap; reopen only on materially new lawful whole-source evidence.
