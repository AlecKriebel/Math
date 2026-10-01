# Sources and bounded literature search

Checked 2026-09-30, principally 03:28–03:42 UTC. Search results are leads, not
proof or a certificate of exhaustiveness. No outside individual was contacted.

## Original statement and parameter conventions

1. Stephen Bigelow, *Braid groups and Iwahori-Hecke algebras*,
   [arXiv:math/0505064](https://arxiv.org/abs/math/0505064), May 2005.
   Sections 2–3 specify the braid generators and coefficient-domain convention;
   Section 8, pp. 13–14, gives the relation scheme and Question 6.
   The downloaded PDF was visually checked at p. 14.
   SHA-256: `5666062b7bcf6121f6411bfd4bff4ac338eae7901a44a39bcd64260c0025b31e`
2. [Author-hosted published scan](https://web.math.ucsb.edu/~bigelow/publications/10.pdf),
   pp. 297–298, in Proc. Sympos. Pure Math. 74 (2006), 285–299.
   DOI: [10.1090/pspum/074/2264547](https://doi.org/10.1090/pspum/074/2264547).
   Page 298 visually confirms the same whole-word inverse notation and the
   terminal sigma_n/RB_n conflict. PDF SHA-256:
   `31caf2929cfd10c44bee9b41fc85c27791d58c6769951fee7564f7abab55e909`
3. [Edited-volume draft](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf),
   Chapter 19, pp. 315–316. This is the imported record's source URL.
4. [Author's publications/errata](https://web.math.ucsb.edu/~bigelow/publications.html).
   No correction for this paper appears in the checked list; the page itself
   says publications as of 2020, so it is not a complete current-status source.
5. [2004 BIRS workshop report](https://www.birs.ca/workshops/2004/04w5526/report04w5526.pdf),
   p. 4. Indexed text supplies the historical term "Zipper algebras" and
   discusses a diagrammatic family. Direct web-tool download returned 403.
   We did not equate its two-parameter diagrammatic definition with the printed
   2005 relation scheme or rely on it for any proof.

## Exact pre-existing result

6. Argus AI Team, [Result 11000263](https://github.com/Argus-AiTeam/argus-mathematics/tree/5abed447441b42dbe9f735e8b2960ee0a0705235/results/11000263).
   [Review package](https://github.com/Argus-AiTeam/argus-mathematics/blob/5abed447441b42dbe9f735e8b2960ee0a0705235/results/11000263/review-package.md),
   prepared date 2026-08-28, read in full through the GitHub connector.
   This provides the existing Burau witness for both repaired presentations.
   Blob SHA: `274c04c5f59fd5f56be95373191ae36d278b3618`.
7. The exact same review-package blob was fetched successfully at the
   [initial archive commit](https://github.com/Argus-AiTeam/argus-mathematics/commit/b8f60542f758750e263016cad1d45cc0650ed64d),
   whose GitHub author and committer timestamps are 2026-08-30T12:01:44Z.
   This is direct evidence that our present attempt cannot claim to have
   originated the displayed construction.
8. [September 3 extension](https://github.com/Argus-AiTeam/argus-mathematics/commit/5abed447441b42dbe9f735e8b2960ee0a0705235).
   Its README and completion boundary were read. It distinguishes a finite
   image with twists from finite-dimensionality of a universal quotient.
   The present audit checks the matrix twists and specialization only.

The third-party archive reserves its rights. No report, verifier, zip archive,
or manuscript from it is copied into this attempt. We cite its mathematical
construction and supply our own verification implementation and calculations.
Its historical or unpublished-work assertions are not independently verified.

## Repository and dataset checks

- Repository base: `01358d66fc67d1c462bddf31c0d4ee5b120e6737`.
- Exact numeric-ID, code, and Bigelow searches returned catalog/review metadata,
  not a prior attempt. The checked queue row is queued, 0/5, with empty result
  cells; shared state is empty. No matching PR/issue or branch was found.
- Recursive tree listing has no 11000263 attempt folder at that base.
- Related-target groups contain no entry for this record.
- Pinned dataset revision: `37e53eabe540fb458758e198be61634bd02ee008`.
  Both source files match the manifest checksums. The problem code has
  exactly one matching record, avoiding an ambiguous report join.
- The prior report says that only the statement was read; its remaining task is
  to fetch the full statement. It supplies no proof or solution claim.
- The exact [UnsolvedMath page](https://www.unsolvedmath.com/problems/11000263)
  could not be read live: web fetch failed and the cloud browser showed 403.
  The pinned record was used instead; its snapshot does not establish the
  current website's classification.

## Search families and stopping rationale

Queries included the exact title/question, numeric ID, Bigelow + X3/Z_n,
Bigelow + BMW/zipper algebra, the paper title plus Question 6, and
Bigelow + Moos + algebra. The specific archive was located via a zipper-algebra
query. Author pages, original papers and the actual result archive were then
inspected. Unrelated tensor-network "zipper condition" results were excluded.

No comprehensive novelty theorem or global current-open classification follows
from these searches. The exact public construction is sufficient to stop this
attempt as a new-discovery project. The remaining source-convention uncertainty
is stated rather than resolved by guessing or relying on outside correspondence.
