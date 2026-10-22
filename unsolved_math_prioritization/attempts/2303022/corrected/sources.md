# Source provenance and bounded literature review

Checked 4 October 2026. The target remains unresolved in this attempt; absence
of a later resolution from these searches is not an exhaustive literature proof.
No copyrighted source PDF or catalogue corpus is included in the public package.

## Target and original update

1. Catalogue entry: https://www.unsolvedmath.com/problems/2303022
   Attempted first. The web tool could not access it; no claim is made to have
   inspected a live rendered catalogue page.
2. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*,
   arXiv:1809.07200v2 (21 September 2018), Problem and Update 3.22, printed p. 67.
   https://arxiv.org/abs/1809.07200
   https://arxiv.org/pdf/1809.07200
   The complete primary statement and update were inspected, including the
   distinction between the unit disk and the domain from which the obstacle is
   removed. The update discusses the connected continuum special case and
   cites Jenkins and Marshall--Sundberg. It does not certify the unrestricted
   sharp constant.
   PDF SHA-256: 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0.
3. The immutable UnsolvedMath catalogue snapshot at revision
   372682f27c1b0d3d39e75fa63ad7932c7a2e1bde identifies ID 2303022 as
   AMR-022-3022. Its accompanying prior report records only statement reading
   and a literature search, and leaves the sharp supremum open.
   https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde
   The research-results corpus SHA-256 was
   8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b
   (80,334,822 bytes). Only the selected report was retained as working evidence.

## Connected benchmark and two-curve warning

4. D. E. Marshall and C. Sundberg, *Harmonic measure and radial projection*,
   Transactions AMS 316 (1989), 81--95.
   https://doi.org/10.1090/S0002-9947-1989-0948195-5
   This is reference [554] of the primary update. The publisher PDF request
   returned 403. Its complete proof was not inspected in this attempt; do not
   treat this citation as an independently reverified proof certificate.
5. D. E. Marshall and C. Sundberg, *Harmonic Measure of Curves in the Disk*,
   Journal d'Analyse Mathematique 70 (1996), 175--224. The primary author preprint
   abstract explicitly states the connected-set hypothesis and identifies its
   constant using a 3:1 rectangle:
   https://library.slmath.org/preprints/files/1995/1995-098/1995-098abs.html
   Marshall's own retrospective also explicitly limits the Fuchs solution to
   connected sets:
   https://sites.math.washington.edu/~marshall/myreviews/select.pdf
   The full 1996 proof was not retrieved (the linked old PostScript URL failed).
6. D. Betsakos, *Geometric theorems and problems for harmonic measure*,
   Rocky Mountain Journal of Mathematics 31(3) (2001), 773--795,
   https://doi.org/10.1216/rmjm/1020171668.
   The indexed author preprint (dated December 1998) was inspected through
   primary-document search excerpts, particularly Theorem 2.7 and Problem 1:
   https://citeseerx.ist.psu.edu/document?doi=b279c6c7daf32cfcb269c82e93749b6ed9d87d9e&repid=rep1&type=pdf
   Problem 1 concerns the union of two curves meeting every radius. It is an
   explicit warning against treating the one-continuum result as the full answer.
   Full-PDF fetches were unsuccessful: the publisher returned a bot-check HTML
   response, and CiteSeer retrieval failed. The indexed excerpt has a decimal
   0.997 inconsistent with the rectangle value; our package uses the author
   Marshall--Sundberg value and a separate exact rectangle computation.
7. J. A. Jenkins, *Some estimates for harmonic measures*, Lecture Notes in
   Mathematics 1275 (1987), 210--214; and *Some estimates for harmonic measures
   III*, Proceedings AMS 119(1) (1993), 199--201. Bibliographic details were
   verified in the primary collection's references [463] and [464]. Neither
   complete proof was independently rechecked here.

## Later related work checked for scope

8. A. Yu. Solynin, *How to keep a spot cool?*, Annales Fennici Mathematici 46
   (2021), 739--769.
   https://doi.org/10.5186/aasfm.2021.4648
   https://afm.journal.fi/article/download/110574/65029/203266
   Inspected its stated extremal problem and introduction. It concerns wires
   joining prescribed interior controlling points to the boundary, especially
   two symmetric prescribed points. This is a different constraint, and the
   article does not give an unrestricted every-radius theorem.
   PDF SHA-256: 9cb6c30562e2bb51e311c07f3f6c637cac6b965c1af5e16f509cdd6e4c7577af.
9. R. W. Barnard, L. Cole, and A. Yu. Solynin, *Minimal Harmonic Measure on
   Complementary Regions*, Computational Methods and Function Theory 2 (2002).
   https://www.math.ttu.edu/~barnard/minimal_harmonic_measure.pdf
   Inspected its problem and scope: an average at two fixed points in
   complementary regions, not the present radial-covering supremum.

Searches used the exact problem number, Fuchs, radial projection, Hall's lemma,
connected/disconnected obstacles, two curves, and the cited article titles.
Unrelated search matches and generative summaries were not used as proofs.
Neighboring Hayman--Lingham Problem 3.14 has a related subharmonic optimization
formulation; no equivalence in full generality is asserted or separately counted
as a new discovery here.

## Repository readiness evidence

The live queue file was retrieved through the connected GitHub API:
https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md
Its returned blob SHA was c1009ab2e12b93cffb15cb17c0ac893979ce5a44, and the selected
row was queued, 0/5, with blank chat/findings/DOI cells. Exact target-number issue
and branch searches returned no matches; the target attempt path returned 404;
code search and an issue search for Fuchs also returned no matches. Search
indexing limitations mean these are bounded duplicate checks, not proof that no
unindexed historical work exists. The prior report was read before proof work.

No remote mutation was performed while creating this frozen package. A queue
update, if approved after audit, should change this row's Status and Turns only.
