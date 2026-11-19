# Live research catalogue completion

2026-11-19 05:28:40 UTC

Completion is 100%. The reviewed inventory consists of 203 eligible distinct Zenodo papers. The site publishes all 194 that passed review. Nine are deferred with defect or gap evidence in the spreadsheet. The 36 ineligible rows and six consolidated aliases retain their original dispositions.

Firebase verified the three approved historical rollback deletions. The preceding live release remained available. The prepared source commit `352763640a979bf407868c36ccfdd49a6e632e0a` was released as version `6458634a6753741c` at 2026-11-19T05:20:52.445Z. The release bundle contained 1,029 files verified against the website Git tree.

The public research index contains 194 article URLs, and the research sitemap contains those 194 URLs and the index. All 194 public article pages matched the released HTML and their recorded canonical URLs and version DOIs. Every PDF matched the frozen Zenodo file by byte count and SHA-256, and every article has an explicit same-site PDF download. An additional full pass matched all 641 linked research files to the release bundle. All 61 new article pages and the index passed desktop and mobile layout checks. Five representative PDF embeds and actual downloads passed in Chrome.

The two former GitHub Pages articles changed only once their production replacements passed verification. The published redirect files went live in GitHub Pages commit `cbba17151aaa9f9231174c0f7082352b8c41d653`. Chrome followed both to the exact replacement, including the no-JavaScript fallback. With JavaScript, the redirects preserved query strings and fragments.

The Full List tab now holds 194 verified live URLs. The 61 newly published records have clickable URLs, verified statuses and preserved research notes. Existing cell and link formatting was checked against native data, and sample ranges from the export were visually inspected.

See [catalogue and file verification](CATALOGUE_LIVE_VERIFICATION.json) for article-level checks, [research index](https://aleckriebel.com/research/) for the live catalogue, and [Full List](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1052646184#gid=1052646184) for the inventory and deferrals.
