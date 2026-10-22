# Source and history verification

Checked on 2026-10-05. This is a bounded provenance report, not an exhaustive historical search or a certification of global open/closed status.

## Identity and original question

The available public-descriptor catalogue identifies rank 723, numeric ID 30002533, label OWR-12870-003, title *New Rational Lyapunov Exponents on Hilbert Modular Surfaces*, and DOI `10.4171/owr/2014/10`. The original report was retrieved from the publisher. Printed pp. 563–564 were text-inspected and visually inspected. They contain the Kobayashi graph definition, foliation ratio, known set of five values, twist invariance, and request for other rational values. The unrelated twisting-volume hypothesis `D = 5 mod 8` belongs to Theorem 1; it is not imposed on the new-exponent question.

The exact requested URL, https://www.unsolvedmath.com/problems/30002533, produced web-tool retrieval errors and HTTP 403 / Forbidden in direct HTTP retrieval. Its current text was not inspected. No alternate guessed problem page was substituted. The catalogue's statement and review hashes are inherited descriptor metadata, not recomputed source-record hashes. The original raw statement corpus and raw AI-report corpus were unavailable and remain uninspected.

## Primary literature inspected

Six scholarly PDFs were downloaded and parsed successfully. Their SHA-256 hashes, byte sizes, URLs, version descriptions, and inspected portions appear in `SOURCE_VERIFICATION.json`. The original statement's two pages and the Gothic paper's printed p. 1206 were additionally visually inspected, confirming signs, the `3/13` value, and the explicit disconnected-component caveat. These PDFs and extracts are not in this packet.

The Gothic article's publisher PDF says published 30 September 2020; its arXiv record reports initial submission on 26 July 2018 and final revision on 19 July 2019. Publication status was checked against https://arxiv.org/abs/1807.10260 and the publisher. Bonatti–Eskin–Wilkinson was inspected in its July 2017 author version; its 2020 Astérisque publication status and bibliographic data were separately checked at the SMF publisher page. Avila–Eskin–Möller was inspected as arXiv v2 dated 4 December 2014; publication in Crelle 732 (2017) was separately verified. This record does not claim byte identity between those author PDFs and their published typesettings.

The decisive mathematical scope check is in `PROOF.md`: average values alone fail, while dimension, equidistribution and continuity pass to actual components. No floating-point exponent is used as a rational certificate.

## Repository prior-attempt checks

Read-only GitHub connector searches were performed in `AlecKriebel/Math`.

- PR searches for `30002533`, `OWR-12870-003`, and `New Rational` returned no matches.
- Broader `Lyapunov` PR results concerned other numeric problem IDs, not this Hilbert-modular question. A broad `Hilbert` query returned unrelated work and supplied no matching attempt.
- Branch searches for `30002533`, `lyapunov`, `hilbert`, and `gothic` returned empty results with no continuation cursor.
- Commit searches for `30002533`, `Gothic`, and `Hilbert Modular` returned no matches.
- Code search for `30002533` returned no indexed results.
- Direct main-branch reads of `unsolved_math_prioritization/attempts/30002533/README.md` and its parent attempt path returned HTTP 404.
- The main queue was read successfully. Its blob SHA was `c87c275c638939b8008fd58db80657491d14971e`; this problem still read queued, 0/5 at that snapshot. The queue value was not used as proof of no prior work.

Limits: the local `.git` directory is a nonfunctional mount placeholder; `git` reported that the workspace was not a repository. A GitHub recursive-tree retrieval failed with transport errors. Thus no complete local git-history or all-ref tree traversal was possible. Search indexes can omit material; the evidence is consistent with no prior target attempt but does not prove historical absence. No source corpus, private coordination data, search-result bodies, or unrelated PR content is redistributed here.

## Delivery boundary

Only authored proof/log/status/checker files and public verification metadata are retained in the safe freeze. No PDF, source extract, screenshot, dataset content, or raw connector record is included. No remote branch, commit, PR, comment, queue edit, merge, or release was made during this task.
