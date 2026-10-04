# Source, scope and novelty gate

Checked 2026-10-04 UTC.

## Exact identity

- Numeric ID 2305046, code AMR-022-5046, rank 575.
- Requested catalogue: https://www.unsolvedmath.com/problems/2305046 . Web access
  failed; a direct read returned HTTP 403. No catalogue status was inferred
  from that failure.
- Primary statement: W. K. Hayman and E. F. Lingham, *Research Problems in
  Function Theory (New Edition)*, arXiv:1809.07200v2 (21 September 2018), printed
  p. 103, Problem 5.46 and Update 5.46.
  https://arxiv.org/abs/1809.07200v2
- The source page was text-read and visually inspected. Its “non-zero
  derivative” means nowhere zero, as independently confirmed by the specialist
  paper's locally-univalent formulation. The collection credits K. F. Barth;
  the specialist literature attributes the originating question to G. R.
  MacLane (1970). These are compatible attributions, not different problems.

## Specialist sources and precise use

1. K. F. Barth, P. J. Rippon and D. J. Sixsmith, *The MacLane class and the
   Eremenko--Lyubich class*, Ann. Acad. Sci. Fenn. Math. 42 (2017), 859--873.
   https://doi.org/10.5186/aasfm.2017.4252
   Official full PDF: https://www.acadsci.fi/mathematica/Vol42/vol42pp0859-0873.pdf
   Checked Question 1, Theorem B, Theorem 1(a), Theorem 6, equation (4.1),
   and definitions of asymptotic paths and global tracts. This paper explicitly
   leaves the full question open. Imported statements are not newly proved here.

2. K. F. Barth and P. J. Rippon, *On a Problem of MacLane Concerning Arc Tracts*,
   Comput. Methods Funct. Theory 4, 405--418.
   https://doi.org/10.1007/BF03321077
   The PDF masthead dates volume 4 to 2004; the publisher records the issue as
   May 2005 and online publication in 2013. It is identified by DOI and pages
   rather than treating these dates as separate results.
   The public author-uploaded full text was inspected at
   https://www.researchgate.net/publication/42790512_On_a_Problem_of_MacLane_Concerning_Arc_Tracts
   Theorem A on p. 406 supplies the Koebe-arc equivalence and boundary
   consequence D5. A private downloadable PDF was unavailable on the attempted
   routes; no PDF hash is asserted. No author's inbox or account was contacted.

3. R. J. M. Hornblower, *A Growth Condition for the MacLane Class A*, Proc.
   London Math. Soc. (3) 23 (1971), 371--384.
   https://doi.org/10.1112/plms/s3-23.2.371
   Bibliography checked against the publisher. The theorem statement used here
   was checked in source 1, p. 866, and source 4, Theorem 3.2. The original
   article's proof was not independently reconstructed.

4. S. Charpentier, M. Manolaki and K. Maronikolakis, *Abel universal functions:
   boundary behaviour and Taylor polynomials*, Rev. Mat. Iberoam. 41 (2025),
   no. 3, 867--890. https://doi.org/10.4171/RMI/1514
   Official PDF: https://ems.press/content/serial-article-files/50390
   Checked the definition, Theorem 3.2, and p. 873's exclusion from A.
   Proposition 8 gives its own elementary crossing proof of the relevant
   incompatibility. This article concerns a different function class and is
   not a resolution of Problem 5.46.

The exact theorem-level derivative criterion traces to Barth--Rippon,
*Asymptotic Tracts of Locally Univalent Functions*, Bull. London Math. Soc.
34 (2002), 200--204, https://doi.org/10.1112/S0024609301008815 . Its official
abstract was read; the full criterion was checked in source 1. The affine
edge case is handled separately in PROOF.md.

## Prior report, duplicate and live repository check

The immutable UnsolvedMath revision used for statement/prior-report comparison
was 372682f27c1b0d3d39e75fa63ad7932c7a2e1bde. Both complete source-file hashes
match the recorded snapshot. Only the selected records were retained in this
attempt; no corpus is included in the release files.

The prior report says OPEN-TRIAGE, contains no proof, and states that the
statement was read and a web search found nothing. It is not evidence that no
specialist results exist. The modern paper above is a concrete correction to
that impression, while leaving the target unresolved.

Live repository evidence:

- Main observed: bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b.
- QUEUE.md Git blob: c1009ab2e12b93cffb15cb17c0ac893979ce5a44.
- Selected row: queued, 0/5; no state.json record for this numeric ID.
- Complete attempts directory listing contained no path for 2305046 or MacLane.
- PR searches for the numeric ID and MacLane each returned zero results;
  a branch-name search for 2305046 returned zero results.
- The related-target group file contained no selected-ID entry. A dataset
  statement search found only this exact arc-tract existence target. Other
  MacLane mentions concern growth criteria, Hadamard-gap asymptotics,
  differential expressions, or a distinct normal-derivative-family concept.

Repository search is evidence against duplicate local work, not a global
novelty certificate. No source-repair of neighbouring queue rows is proposed.

## Literature-search limits

Queries included the exact problem number, “MacLane arc tract derivative”,
“locally univalent MacLane”, “arc tracts solved”, and date-qualified variants
through 2026. The 2017 result and the 2025 boundary-behaviour paper were checked
at primary sources; no later solution was located. Search snippets' crawl dates
were not mistaken for publication dates. No exhaustive citation-index search
or personal communication was performed. The defensible disposition is
**unsolved in this investigation**, with the published open status precisely
dated, not a claim of omniscience about 2026 literature.

## Scope and integrity

PROOF.md settles only its named propositions. Standard/public literature inputs
remain dependencies. Complete source PDFs, source-page screenshots, extracted
source text, bulk datasets and coordination records are excluded from the
public package. SOURCE_MANIFEST.json identifies source bytes where available.
SHA256SUMS.json identifies every public file other than itself. The verifier
checks exact file-set coverage as well as hashes.
