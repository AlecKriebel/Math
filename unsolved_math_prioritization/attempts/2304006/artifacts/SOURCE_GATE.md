# Source and prior-work gate

Checked 2026-10-03. Target: **2304006 / AMR-022-4006**, queue rank 521.

## Exact target and status

The exact catalogue URL is https://www.unsolvedmath.com/problems/2304006.
The web retrieval was inaccessible; the local HTTP response body said “Forbidden”
and contained no statement (despite a 200 response header).
The pinned catalogue record and imported triage were inspected locally only.
Neither the generated triage's open label nor its conclusion is proof evidence.

The statement was checked directly in W. K. Hayman and E. F. Lingham,
*Research Problems in Function Theory (New Edition)*,
[arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), 21 September 2018,
printed pp.73–74, Problem and Update 4.6.
It uses physicists' Hermite polynomials, complex coefficients, arbitrary integer
indices 2<=n<m, and an absolute constant independent of all four parameters.
A zero on the boundary of the strip is permitted. Zero coefficients and degree
drops are permitted. This is an existence question for a constant, not a demand
for its optimal value.

Update4.6 reports no progress to the editors and explicitly warns that an earlier
report had confused this problem with Problem4.5, the Sendov conjecture.
A Sendov result is therefore not a solution source for this record.

## The actual one-high-term theorem

E. Makai and P. Turán, *Hermite expansion and distribution of zeros of polynomials*,
*Magyar Tud. Akad. Mat. Kutató Int. Közl.* **8** (1963), 157–163.
[Institutional original scan](https://real.mtak.hu/201433/1/cut_MATKUTINT_8_1_-_2_1963_pp157_-_163.pdf).
The entire seven-page article was read, including rendered formula pages.

Its TheoremI is for 1+H1+ζHn with one arbitrary complex high coefficient.
TheoremII gives half-width e^3 for n>=36. The proof on pp.158–161 combines an
extreme-real-zero circle, estimates for Hn there, a small circle about -1/2,
and overlapping Rouché thresholds. Section6 on pp.161–162 handles the remaining
finite degree range using small/large coefficient regions and compactness.
The external Hermite estimates credited in that article to Szegő, Van Veen,
and Makai are classical inputs, not separately reproved in this packet.

The article does not prove the two-high-term claim. We use it as verified source
scope and route guidance, not as a newly proved general solution.

The sharp cubic partial result uses a half-plane polarization lemma. A
self-contained polar-derivative proof of the needed lemma is supplied in
`CUBIC_SUBCASE.md`; no unproved coincidence theorem is needed.

## Bounded current-literature search

Queries combined the exact article title; Hermite with Makai/Turán; the
Hermite-trinomial and tetranomial terms; Landau–Fejér–Montel; and the exact
problem number with Hermite. No primary source resolving the unrestricted
question was located. Results on Hermite–Padé recurrences, Wronskians,
exceptional Hermite polynomials, and Sendov's conjecture address other questions.
This bounded search is not a proof that no later solution exists.

## Repository gate

The live main-branch QUEUE row was queued, 0/5, at blob
`a34c276a8fd0251396fa3a3d2ad2400fe381733f`.
There was no main-branch attempt directory for this numeric ID.
All-state pull-request searches for `2304006` and `AMR-022-4006` returned no hit.
Broader Hermite and Function-Theory4.6 searches returned unrelated work only.
The related-target-group file had no match for this ID, at blob
`b5cfa231ed6079c0f5021e1368c3b30a43100a10`.
Thus no actual prior substantive attempt was found; this determination was not
made from the queued main-branch status alone.

## Claims and publication scope

Overall unresolved after five substantive approach families. The real-coefficient
case and sharp cubic case are explicitly narrower results. No claim of novelty,
priority, full resolution, or human peer review is made. Only original notes,
proofs and small verification artifacts belong in the public packet. Downloaded
source PDFs, extracted source texts, screenshots, imported records, and local
coordination data are excluded.
