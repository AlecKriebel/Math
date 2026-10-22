# Source and prior-work gate

Checked 4 October 2026 UTC. This is a bounded source and repository
investigation, not an assertion of exhaustive coverage of all literature
or every repository branch.

## Exact target and interpretation

- Catalogue: https://www.unsolvedmath.com/problems/2302004
- Identity: 2302004 / AMR-022-2004; queue rank 565
- Source: W. K. Hayman and E. F. Lingham, *Research Problems in Function
  Theory (New Edition)*, https://arxiv.org/abs/1809.07200v2
- Locator: Problem 2.4, printed page 23 / PDF page 24; Update 2.4,
  printed page 24 / PDF page 25
- Proposer credited by the source: C. Rényi

The source first defines a Julia ray for a meromorphic function by
infinite occurrence of all values except at most two in every positive
aperture neighborhood of its direction. For an entire function, infinity
is always omitted, leaving at most one finite exception. The concrete
question is whether two different Julia rays of one entire function can
have different finite exceptional values. There is no imposed order,
normalization, prescribed pair of directions, or formula requirement.
The broader introductory request to describe exceptional values is not
a precise classification conjecture.

The question and update were read in the PDF, with both pages rendered
and visually checked. The update credits Toppila with an example having
different exceptional values at n Julia rays and also references
Gol'dberg. We preserve that historical credit; our narrower two-ray
proof does not establish the update's full n-ray statement.

## Recovery and evidence discipline

The exact catalogue URL was tried with both the web reader and direct
HTTP. The latter returned 403. Identity and provenance were recovered
from the existing local copy of the public UnsolvedMath dataset at
revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`:
https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The whole dataset has 69,291,427 bytes and SHA-256
`37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`.
Only the matching record was used to locate the primary question. Its
open-status label and generated research summary were not mathematical
or current-status evidence. The question and explicit resolution update
were independently checked in the 2018 source itself.

## Historical sources and retrieval limits

1. S. Toppila, *Some remarks on exceptional values at Julia lines*,
   Annales Academiae Scientiarum Fennicae, Series A I, no.456 (1970),
   20 pages. This is reference [753] in the 2018 source. The original
   full text was **not recovered**. The publisher's older-number index
   https://www.acadsci.fi/mathematica/oldnumbers.html currently omits
   1970, and the anticipated 1970 PDF location returned 404. We do not
   claim to have checked its original construction or theorem wording.
2. K. F. Barth and W. J. Schneider, *On a problem of C. Rényi concerning
   Julia lines*, Journal of Approximation Theory 6 (1972), 312–315,
   https://doi.org/10.1016/0021-9045(72)90064-0 . The publisher/Crossref
   identity was verified, but the full article was not recovered. It is
   not an invoked proof dependency.
3. J. S. Hwang, *Note on a problem of Catherine Rényi about Julia lines*,
   Acta Mathematica Academiae Scientiarum Hungaricae 29 (1977), 67–68,
   https://doi.org/10.1007/BF01896468 . Original full text retrieved from
   the Hungarian Academy's archive:
   https://real-j.mtak.hu/7427/1/MTA_ActaMathHung_29.pdf , archive record
   https://real-j.mtak.hu/7427/ . Both original pages (PDF 73–74) were
   read and visually checked. Its opening explicitly identifies Hayman's
   Problem 2.4 and credits the affirmative answer first to Toppila and
   subsequently to Barth–Schneider by a different method. Its own
   theorem concerns prescribed asymptotic values along Julia rays;
   asymptotic values are not automatically exceptional values. We do
   not use that theorem to supply the omission part of our proof.
4. A. A. Gol'dberg, original Russian article on angular distribution of
   entire-function values, Acta Mathematica Academiae Scientiarum
   Hungaricae 19 (1968), 191–199. The complete article was recovered in
   https://real-j.mtak.hu/7416/1/MTA_ActaMathHung_19.pdf and its content
   checked. Its main theorem is about values attained in every angle,
   the question recorded as Problem 2.5. The fact that Update 2.4 also
   cites it does not turn the 2.5 theorem into a direct solution of 2.4.
   The article is not needed by our explicit proof.

The exact original 1967 question leaf and Toppila/Barth–Schneider proofs
were not retrieved. Instead of concealing this limit or citing a theorem
whose proof was not read, `PROOF.md` supplies a complete direct verification
of the concrete two-value existence statement with a classical witness.
Historical attribution is independently corroborated by Hwang's original
follow-up and by the source update. No first-discovery claim is made for
the witness, the proof presentation, or the existence conclusion.

## Standard analytic facts used

The error function is defined in NIST DLMF §7.2:
https://dlmf.nist.gov/7.2.E1 . Its standard complementary-function
asymptotic expansion is in https://dlmf.nist.gov/7.12.E1 . These were
checked as a cross-check, but the precise uniform error bound used in
`PROOF.md` is derived by integration by parts and does not require the
asymptotic-expansion theorem. Montel's omitted-values normality theorem,
Cauchy's formula, the identity theorem, and the Gaussian integral are
standard foundational dependencies. They are explicitly identified,
not claimed as new results or formally machine-checked.

## Actual prior-work check

Repository: https://github.com/AlecKriebel/Math

At main commit `4c241e455db6e3f9707cd5ce2b46f2ac5281888f`, the exact row was
queued, 0/5. The queue alone was not treated as a prior-attempt search.
Additional checks found:

- All-state PR searches for `2302004`, `AMR-022-2004`, a Function Theory
  / 2.4 phrase, and a Julia/lines phrase: no target PR found
- Repository code, commit, and branch searches for `2302004`: no target
  result returned
- A complete nonrecursive listing of the main attempts directory: no
  child directory `2302004`
- Both an older local recursive main-tree snapshot and a fresh recursive
  main-tree request were truncated. Neither was used to establish
  absence; the complete directory checks above are the relevant
  evidence.

PR 491 was read directly:
https://github.com/AlecKriebel/Math/pull/491 . Its head was
`b75348bddd2f74b7a80c561844d36832a40b4dac`, and it concerns 2302005,
Problem 2.5, whose condition is that a value occur in **every** angle.
Our condition is about exceptional values in neighborhoods of particular
rays. PR 491's own source gate explicitly distinguishes these targets.
It is neither an earlier attempt at 2302004 nor a reason to skip the
present proof.

## Status conclusion and scope

The terminal existence question is already affirmatively resolved in
the literature. The supplied explicit proof independently verifies it
without relying on unretrieved constructions. This warrants the scoped
status `already_solved`, with one substantive investigation (`1/5`),
subject to independent audit. No full classification is claimed.

The preparation is AI-assisted. Original papers, page images, OCR text,
corpus records, and operational context are excluded from this public
packet. Bibliographic links and hashes identify locally checked inputs
without redistributing them.
