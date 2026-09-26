# Zenodo publication and tracker workflow

## 2026-09-26T20:44:13.516540+00:00 — 20% complete

The user authorized publication through the repository deposit tool with the exact existing upload-kit metadata and the two named files, followed by a Google Workspace CLI tracker append. Both file hashes and every metadata field match the kit. The deposit tool’s five unit tests passed. The requested worksheet resolves to Math Puzzles (gid 1254632077), with Original Problem, Solution Chat URL, DOI, and Notes columns; no existing Brandes row was found. The installed Sheets append helper lacks its documented range option, so the explicit values.append command will target the correct worksheet. Frozen paper and source-archive bytes will be preserved.

## 2026-09-26T20:46:05.777201+00:00 — 70% complete

The initial request received an HTML HTTP 403 traffic-filter response and created no saved draft. Controlled read-only requests showed that the missing User-Agent header triggered the rejection; a truthful Math-Zenodo-Deposit-Tool/1.0 header returned HTTP 200 with the same credentials. Added this header and a regression assertion to the reusable tool; all five tests pass. Staging then succeeded as production draft 22982894. A separate inspect rechecked every original metadata field and both remote file sizes/MD5 hashes against the unchanged kit files. Ready to publish under the user’s explicit authorization; tracker update follows publication.
