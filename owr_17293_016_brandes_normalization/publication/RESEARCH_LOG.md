# Zenodo publication and tracker workflow

## 2026-09-26T20:44:13.516540+00:00 — 20% complete

The user authorized publication through the repository deposit tool with the exact existing upload-kit metadata and the two named files, followed by a Google Workspace CLI tracker append. Both file hashes and every metadata field match the kit. The deposit tool’s five unit tests passed. The requested worksheet resolves to Math Puzzles (gid 1254632077), with Original Problem, Solution Chat URL, DOI, and Notes columns; no existing Brandes row was found. The installed Sheets append helper lacks its documented range option, so the explicit values.append command will target the correct worksheet. Frozen paper and source-archive bytes will be preserved.

## 2026-09-26T20:46:05.777201+00:00 — 70% complete

The initial request received an HTML HTTP 403 traffic-filter response and created no saved draft. Controlled read-only requests showed that the missing User-Agent header triggered the rejection; a truthful Math-Zenodo-Deposit-Tool/1.0 header returned HTTP 200 with the same credentials. Added this header and a regression assertion to the reusable tool; all five tests pass. Staging then succeeded as production draft 22982894. A separate inspect rechecked every original metadata field and both remote file sizes/MD5 hashes against the unchanged kit files. Ready to publish under the user’s explicit authorization; tracker update follows publication.

## 2026-09-26T20:50:33.155009+00:00 — 100% of upload/tracker actions complete; resolver activation unconfirmed

Published Zenodo record 22982894, assigned DOI 10.5281/zenodo.22982894, through the repository tool. Post-publication inspect confirms the exact original metadata and file checksums. Both public files were downloaded without authentication and matched the kit bytes; the direct public record returns HTTP 200. Google Workspace CLI appended Math Puzzles row 5 and a separate read-back matched all four cells. The chat URL remains blank because no shared URL was provided. DOI resolver and DataCite initially returned 404; publication is confirmed but activation is not yet verified. A final availability check will be saved separately. Publication receipts and workflow feedback are outside the unchanged upload snapshot. No duplicate deposit or automatic publication retry is warranted.
