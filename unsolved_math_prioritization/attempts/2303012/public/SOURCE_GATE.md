# Source and prior-work gate

Checked 4 October 2026 UTC.

## Catalogue identity and exact question

The requested catalogue URL was attempted first:
https://www.unsolvedmath.com/problems/2303012 . The web reader could not
access it and direct HTTP returned 403. The exact record was recovered
from the public dataset's pinned revision
`372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`, without relying on its
status labels:
https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json .

The actual statement was checked in W. K. Hayman and E. F. Lingham,
*Research Problems in Function Theory*,
https://arxiv.org/abs/1809.07200v2 , Problem and Update 3.12, printed
p. 64 / PDF p. 65. The page was rendered and visually inspected.
It credits B. Kjellberg, asks for a uniformly bounded remainder in the
upper half-space, and also asks for the higher-dimensional analogue.
The fixed radius and fixed positive area were preserved. In higher
dimensions area is replaced by the measure of the separating hyperplane.

## Original resolution

Michael Benedicks, *Positive harmonic functions vanishing on the boundary
of certain domains in R^n*, Arkiv för Matematik 18 (1980), 53–72,
https://doi.org/10.1007/BF02384681 . The original full article was
retrieved at:
https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7328-11512_2006_Article_BF02384681.pdf .

Decisive locator: Corollary 3 on printed p. 67 / PDF p. 15. It is an
exact resolution, not merely the related one-or-two Martin-boundary-point
classification. The standing regularity hypothesis on p. 53 was checked
and is addressed explicitly in `PROOF.md`. Lemma 2 and equation (2.4)
on p. 55, Lemma 3 on pp. 55–56, and Lemma 8 on pp. 63–66 supply its
proof. The introduction, representation, density estimate, and corollary
pages were visually checked; the remaining proof text was also read.

Benedicks reference [13], printed p. 72, identifies the original question
as B. Kjellberg, Problem 3.12, *Symposium on complex analysis Canterbury,
1973*, p. 163, Cambridge University Press (1974). The publisher confirms
the containing chapter, *New problems*, pp. 155–180:
https://doi.org/10.1017/CBO9780511662263.034 .
That 1974 page was not recovered. The publisher provides an access-limited
chapter listing; the available retrieval did not yield the question leaf.
The exact later primary collection and the original resolution were
recovered, so the historical-page limitation does not leave the
mathematical conclusion dependent on an unread solution.

## Prior report correction

The pinned dataset's report joined by AMR-022-3012 described the problem
as open in the 2018 edition and said no result had been located. Its
search did not catch the explicit Benedicks reference in Update 3.12
or Corollary 3 of the cited original paper. It contained no proof
attempt to extend or repair. The report is superseded for this target
by the primary-source evidence above. Its raw text is not published here.

## Repository duplicate search

Repository: https://github.com/AlecKriebel/Math . Observed main commit:
`12c8ecfe519fbf1d6f3cb7b35547c39055307341`.
The queue blob was `59dba610d333684751e889818d21f66aba29cec9`;
row 569 was queued, 0/5.

Additional checks, rather than relying on that row alone:

- Complete contents listing of `unsolved_math_prioritization/attempts`
  returned 54 children and no directory named 2303012.
- All-state PR searches for 2303012, AMR-022-3012, the Function Theory /
  3.12 phrase, and Kjellberg / harmonic returned no matching PR.
- Code, commit, and branch searches for 2303012 returned no result.
- The current state file has no 2303012 entry.
- `review_v2/related_target_groups.json` has no 2303012 mention.

Recursive tree retrievals failed and were not used as evidence of
absence. Search results are bounded by the tools and indexing; they
do not certify that every historical branch has been inspected. No
actual prior repository attempt at this target was found.

## Classification

Use `already_solved`, with one substantive source-verification and
proof-mapping investigation (`1/5`). No remaining mathematical subcase
of the exact target is left open by Corollary 3. Five invented proof
attempts would be inappropriate after locating the complete published
answer. No public novelty claim, release, or external outreach is part
of this work.
