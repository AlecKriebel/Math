# Sources, attribution, and inspection limits

Inspection date: 5 October 2026 (UTC).

## Original problem

Boris Shapiro, *Problems Around Polynomials: The Good, The Bad and The Ugly…*,
Arnold Mathematical Journal 1 (2015), **91–99**,
[DOI 10.1007/s40598-015-0008-4](https://doi.org/10.1007/s40598-015-0008-4),
[arXiv:1503.05295](https://arxiv.org/abs/1503.05295).
The [journal PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0008-4.pdf)
was downloaded and printed page 93 was visually inspected. Its Problem 3 is
the exact target; Conjecture 4 is a separate proposed formula.

The inspected source confirms the proposer attribution, exact degree (2k),
summand degree at most (k), isolated **real** zeros, and the absence of a
complex-finiteness hypothesis. It credits the planar equality to Choi, Lam and
Reznick, *Real Zeros of Positive Semidefinite Forms I*, Math. Z. 171 (1980),
1–26, [DOI 10.1007/BF01215051](https://doi.org/10.1007/BF01215051).
That original 1980 proof was not directly inspected; the planar equality is
reported with this attribution and is not used as a premise for other results.

The imported research summary's page range 91–104 is incorrect; the actual
journal article is nine pages, 91–99. The original problem endpoint
[UnsolvedMath 2200006](https://www.unsolvedmath.com/problems/2200006) could not
be retrieved by the web tool. The local corpus record was matched directly
to the primary journal problem rather than treating the generic title as enough.
The imported statement's UTF-8 SHA-256 matches the catalogue statement hash.
Full-corpus byte hashes and sizes are in `SOURCE_METADATA.json`; corpus contents
are not redistributed.

## Later prior construction: verified here

DannyExperiments, *A counterexample to the Ottaviani–Shapiro isolated-zero
conjecture*, version 1.0.0, public release 10 August 2026,
[DOI 10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290),
[public repository](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample).
The manuscript title is *Many Isolated Real Zeros of Sums of Squares*.

The [designated manuscript](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/blob/main/paper/manuscript.tex),
README, citation metadata, and Zenodo record were directly inspected.
The archived manuscript bytes match the GitHub manuscript exactly. The archived
PDF also matches the SHA-256 published in the README, and both archival files
match the repository's Zenodo MD5 records. The entire mathematical argument
for the explicit quartic and even-degree family was independently reconstructed
in this packet. No external executable source was run.

Zenodo records creation at 2026-08-10T15:09:20.726761+00:00 and publication date
2026-08-10. The named creator is DannyExperiments. These facts establish a
public source predating this investigation, not absolute historical priority.
The release expressly disclaims an exact extremal formula, human peer review,
and full formal verification. Its own audit labels are not adopted as independent
evidence; the present acceptance rests on the elementary proof reconstruction.
Source files are excluded from this packet, including its all-rights-reserved
TeX manuscript and PDF.

## Recent small-dimensional claims: not verified here

Alper Ferudun, *Isolated Real Zeros of Sums of Squares: Quaternary Forms and
Quinary Quartics*, EulerSolve Research Papers, 30 September 2026,
[author page](https://eulersolve.org/papers/amr-014-0019/),
[DOI 10.5281/zenodo.23066556](https://doi.org/10.5281/zenodo.23066556).
The landing page identifies this as an unrefereed AI-assisted preprint and
advertises the affine cases (l=3) for every (k), and ((k,l)=(2,4)).
The linked PDF and metadata request returned HTTP 403 through the download
route; web PDF retrieval also failed. No attempt was made to bypass that denial.
Only the landing-page claims are recorded, and they are not promoted to proved
theorems in this packet.

The landing page describes the universal companion conjecture as still open.
That blanket wording conflicts with the independently verified earlier
counterexample above. This is a scope/status inconsistency; it does not itself
disprove the page's separate low-dimensional theorem claims.

## Bounded search for existing attempts

The actual `AlecKriebel/Math` default-branch queue was inspected and shows rank
764 as queued, 0/5. GitHub file search for `2200006`, `AMR-021-0006`, and
`Ottaviani` returned no indexed code matches; PR search for those target terms
returned no matching PR. Branch searches for `2200006` and `polynomial` returned
no matches. A broader polynomial PR search found unrelated work, not an attempt
on this exact target. Search results do not exclude unindexed or private work.
A targeted prior-user-work search likewise returned no relevant prior attempt;
unrelated personal material was not used or published.

Public searches used combinations of Ottaviani, Shapiro, isolated real zeros,
sums of squares, maximum, the exact source title, and the later manuscript title.
They located the two later sources described above. This was a bounded research
pass, not a certificate of completeness or worldwide openness. The exact
extremal problem is unresolved **by this investigation**, regardless of other
unlocated work.
