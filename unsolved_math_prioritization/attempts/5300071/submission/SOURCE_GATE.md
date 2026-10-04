# Source and literature gate

Checked 2026-10-04 UTC. Imported status descriptions and reports were treated
as leads, never as proof certificates.

## Identity and recovery

- Numeric upstream ID 5300071; source code AMR-052-0071; source-ranked 650.
- The catalogue URL https://www.unsolvedmath.com/problems/5300071 did not yield
  its statement: the web tool could not access it and a direct GET returned
  HTTP 403. No login, protection bypass or external contact was attempted.
- The pinned dataset record identifies Scott Sutherland, Conjecture 2 in the
  1992 list. Its prior report explicitly had not verified the quantitative
  result. Both were inspected locally, without redistribution.
- Followed the official index
  https://www.math.stonybrook.edu/open-problems-dynamical-systems to IMS 92/7
  at https://www.math.stonybrook.edu/preprints/ims92-7.pdf . Visually inspected
  printed p.43 (PDF page 45) and its preceding definitions on printed p.42.
  The simultaneous parameter interval and length denominator agree with the
  imported target. Source PDF bytes and hashes are in SOURCE_MANIFEST.json.
- RESULT.md formalizes centered circles. The omitted center in the old
  phrasing is flagged, not exploited to manufacture a solution.

## Primary literature inspected

1. Scott Sutherland, *Finding Roots of Complex Polynomials with Newton's
   Method*, doctoral thesis (May 1989), revised September 1989:
   https://www.math.stonybrook.edu/~scott/Papers/thesis-alt.pdf . Inspected
   addendum Theorems 1--2 and Sections 3.8/4.2. Classical Newton circle-width
   estimates are relevant fixed-map background; they do not establish common
   arcs for all relaxation parameters.
2. J. Hubbard, D. Schleicher, S. Sutherland, *How to Find All Roots of Complex
   Polynomials by Newton's Method*, Inventiones mathematicae 146 (2001), 1--33:
   https://pi.math.cornell.edu/~hubbard/NewtonInventiones.pdf . Inspected the
   introduction's relaxed-method remark, Proposition 7 and its channel-area
   discussion, and the single-circle section. Fixed-parameter channel geometry
   is not the desired simultaneous intersection. No exact resolution found.
3. Soumen Pal, *Relaxed Newton's Method as a Family of Root-finding Methods:
   Dynamics and Convergence*, arXiv:2603.11591v1, 12 March 2026:
   https://arxiv.org/abs/2603.11591v1 and
   https://arxiv.org/pdf/2603.11591v1 . Inspected Theorems A--D, the parameter
   convention, and Lemma/Proposition 5.1. This preprint discusses convergence
   and qualitative unboundedness, not the requested common-arc lower bound.
   Its global linearization step in Lemma 5.1 is not used here: Koenigs
   linearization is local in general, and a globally univalent linear model
   cannot represent a map with a critical point in the basin. No validation
   of that broader preprint is claimed.

## Earlier leads and limits

The 1992 source points to H. Benzinger, *Julia Sets and Differential Equations*
(Proc. Amer. Math. Soc. 117 (1993), 939--946) for small-step context. An AMS
PDF request returned 403, and its theorem was not independently checked.
H. Kriete, *On the efficiency of relaxed Newton's method*, Pitman Research
Notes in Mathematics 305 (1994), 200--212, is cited in the inspected 2001
paper. Its original full text was not recovered. A 1995 Hokkaido seminar
collection at https://eprints.lib.hokudai.ac.jp/repo/huscap/all/5469/35.pdf
reproduces the conjecture and mentions related partial results; it was used
only as a historical search lead, not as verification of Kriete's theorem.

Searches used the exact source title, Sutherland Conjecture 2, relaxed Newton
intersection/immediate-basin phrases, Benzinger's title, and Kriete's title.
No verified complete resolution was found in this bounded inspection. The
missing older primary papers and nonexhaustive citation coverage prevent an
exhaustive literature-status claim.

## Repository and duplicate gate

Live AGENTS.md and the research-queue AGENTS.md/README.md were read. The live
row for this numeric ID was queued, 0/5; the state file had no matching ID,
and an own-attempt README lookup returned 404. Repository-wide PR searches
for the ID and relaxed-Newton title phrase returned no match. Branch search
for the numeric ID returned none. The related-target-groups file had no group
for this ID. These checks are not a substitute for the final pre-publication
recheck by the publisher.

The corpus has related ID 5300070, the neighboring Sutherland conjecture about
families of bad polynomials and degenerate-flow limits. It is a different
claim; no shared lemma here resolves it. Other retrieved immediate-basin
records concern different dynamics. No queue.py command was run, and no
remote state was changed by this packet.
