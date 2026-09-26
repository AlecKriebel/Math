# Zenodo publication and tracking log

## 2026-09-26T22:04:28Z — Deposit preparation — 20%

The user explicitly authorized publication through the repository Zenodo tool with exact kit metadata, a Google Workspace CLI tracker append, a queue status/DOI update, and two unsent notification drafts. The version 1.0.1 kit metadata and all three payloads match canonical files byte-for-byte. The manuscript hash is the one cleared by the two fresh sequential adversarial reviewers. The existing September 23 preprint date is retained; the deposit action occurs September 26. The target spreadsheet tab is Math Puzzles (gid 1254632077), columns Original Problem, Solution Chat URL, DOI, Notes; no existing target row was found. Existing source/kit files remain frozen, and publication receipts are saved separately. No token is printed or committed.

## 2026-09-26T22:10:43Z — Published, tracker verified, queue updated — 90%

The first staging call created draft 22983513 and uploaded all three files but correctly stopped because Zenodo normalized two U+2019 apostrophes to ASCII in the HTML description. Every other metadata field matched. The original metadata and payloads were not edited. The tool now recognizes only that exact transformation in plain paragraph-only HTML and reports it explicitly; changed text, numbers, tags/attributes, other punctuation, partial normalization, and other metadata fields remain rejected. All 27 offline regression tests pass. A read-only inspect verified the saved draft, after which one publication action succeeded. DOI 10.5281/zenodo.22983513 resolves with HTTP 200. Public downloads of all three files match the kit byte-for-byte.

Google Workspace CLI appended exactly one row to Math Puzzles!A10:D10 after duplicate checks; a separate readback matches the request. Solution Chat URL is blank, following the existing tracker convention; no conversation was publicly shared. QUEUE.md target 30001163 / OWR-3389-016 is now preprint_published with the DOI, preserving its earlier findings and adding the publication checkpoint. The unsupported queue regenerator was not run over the manually maintained Chat/Findings/DOI table.

Both user-requested notification drafts are saved. Suggested recipient is Evans M. Harrell II, one of the named proposers; his official Georgia Tech profile confirms his affiliation and public contact address. Drafting is explicitly authorized by the user’s current instruction; nothing is sent to a person or posted to unsolvedmath.com. Final receipt/documentation and repository publication remain.
