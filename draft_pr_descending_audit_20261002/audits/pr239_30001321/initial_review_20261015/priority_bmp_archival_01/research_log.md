# PR239 BMP archival primary-source acquisition log

Scope: acquire a complete public primary copy of BMP1999 or the authors' 2007 survey and authenticate the local-limit hypotheses, residual and spatial range. All writes remain in this folder. No outreach, other chats, Git/index/ref mutations, provider mutations, or manuscript edits.

## 2026-10-15 04:42:25 UTC - initial checkpoint

Completion estimate toward complete-source acquisition and theorem authentication: **5%**. Began with supplied metadata and known blocked MathNet/IOP routes. Exact success criterion is a full source, pinned bytes and SHA256, followed by relevant theorem/proof reading. Search snippets and abstracts do not meet that criterion.

## 2026-10-15 04:46:20 UTC - archival coverage checkpoint

Completion estimate toward complete-source acquisition and theorem authentication: **30%**. No target full text acquired. Public mp_arc yearly indexes 1991-2008 have been downloaded and searched for Boldrighini, Pellegrinotti, Minlos and target-title fragments. No target item appears; unrelated Minlos entries are recorded in access_attempts.jsonl. Its public author-search CGI returned HTTP500. OpenAlex and Semantic Scholar return closed/no public PDF locations for the survey. A new Roma Tre metadata record (11590/150170) explicitly has no attachment; Mathdoc Geodesic provides only metadata/bibliography. Crossref gives a standard IOP stacks PDF route, but it redirects to the known bot challenge. No challenge was bypassed. MathNet aliases fail with 20-second network timeouts. Wayback CDX also timed out; this says nothing about its holdings.

A new useful route is Vernadsky National Library of Ukraine's public DSpace API: it responds normally and returns three Boldrighini search objects (two 2008 items and their collection), none a target paper. The journal community and currently returned annual records begin in 2005. This is coverage of the searched service, not a proof that no archival copy exists.

## 2026-10-15 04:48:14 UTC - acquisition pass checkpoint

Completion estimate toward complete-source acquisition and theorem authentication: **35%**. Authenticated the full institutional OAI metadata response and pinned its bytes/SHA256. Newly located Roma Tre BMP1999 record 11590/116583, which explicitly has no attachment. Vernadsky TSP community child listing is complete (4 children:2005-2008). New BiBoS candidate year routes all return404. No target full primary acquired, so theorem/proof authentication remains at zero completed target sources; the increase reflects reproducible archival coverage and precise claim boundary only. See source_report.md for the strongest verified content and exact gap.

## 2026-10-15 04:49:26 UTC - final reproducibility checkpoint

Completion estimate toward complete-source acquisition and theorem authentication: **35%**. The saved-metadata/index verifier passes, checking the primary OAI bytes/hash, 18 mp_arc yearly indexes, all 4 Vernadsky journal annual children, and 31 saved-response hashes. Its first run exposed Latin-1 names in the historical index HTML; the reader now decodes those byte-preserving indexes as Latin-1 and the corrected check passes. Standard system-certificate access to the candidate Roma Tre `/users/pellegri/` directory returned404. Bounded acquisition pass concluded with zero target full sources and no authenticated target theorem. These failures are not novelty evidence. Private responses and source-byte inventory stay outside the authored manifest.

## 2026-10-15 04:56:54 UTC - public-checkpoint sanitation

Completion estimate toward complete-source acquisition and theorem authentication: **35%**, unchanged. Before changing the authored log, privately preserved all six original sealed artifacts plus their original manifest byte for byte. Removed 13 transient bot-challenge query parameters from access_attempts.jsonl line 20, retained the query-free verification-page URL, and recorded the private preservation-receipt hash and redaction reason. Primary evidence remains unchanged; acquisition was not renewed. See sanitation_receipt.json for hashes and verification scope.

Sanitation validation passed at 2026-10-15 04:57:23 UTC: the original six-artifact seal is valid in its private snapshot; all seven original files are byte-exact; only the intended access-log row changed; all other log lines are byte-identical; challenge URLs in the authored log have no query or fragment; all 31 original response hashes and primary OAI evidence remain valid. Completion estimate remains **35%**.
