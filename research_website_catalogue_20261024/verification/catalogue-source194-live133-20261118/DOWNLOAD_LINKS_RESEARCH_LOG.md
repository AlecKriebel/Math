# Catalogue verification checkpoint

2026-11-18 08:19:31 UTC

Scientific review is 100% complete (203 of 203 eligible manuscripts). The website source is 100% prepared (194 of 194 passing manuscripts). An estimated 70.0% of eligible manuscripts have reached their final disposition for this project (133 live, nine deferred, 61 awaiting deployment).

The public research index and all 194 intended canonical URLs were checked. The 133 live pages appeared in the index and exposed the expected canonical URL and DOI. Every corresponding public PDF returned HTTP 200 as application/pdf, and its SHA-256 and byte count matched the exact Zenodo manuscript recorded in the inventory. The other 61 routes returned HTTP 404 and were absent from the index. The spreadsheet has 133 canonical URLs and 61 empty canonical cells for the pending papers. The nine deferrals, 36 exclusions and six consolidations still agree with the reconciliation.

Fifty article pages received a direct download link for their existing same-site PDF. Chrome downloaded all 50 from the preview successfully and each matched the byte count and SHA-256 in the inventory. Three affected pages also passed the narrow-screen check. The complete source then passed the same-site download target and file identity check for all 194 prepared articles.

Website source commit [352763640a97](https://github.com/AlecKriebel/aleckriebel.com/commit/352763640a979bf407868c36ccfdd49a6e632e0a) changes the 50 article HTML files. All 995 deployable files and both Firebase configuration files in the local deployment directory matched the website commit. The source change is awaiting the next production release.

The live Firebase version is `245aaf213f501c8a`. It predates the completed catalogue. The six versions already marked deleted date to December 2022, so those deletions are outside Firebase's published 24-hour cleanup window. The 61 remaining website pages and the two corresponding GitHub Pages redirects await a successful production deployment.
