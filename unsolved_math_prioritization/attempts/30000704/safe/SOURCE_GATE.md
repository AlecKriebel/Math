# Source and claim gate

Checked 2026-10-04 UTC.

## Identity and actual prior work

Live repository queue row 660 still had status queued and 0/5 at initial
inspection. The repository state file had no entry for numeric ID 30000704.
Targeted repository file and PR searches found no actual prior attempt;
the expected attempt README was absent. The source-checked related-target
group file did not include this problem. No remote write was performed.
A catalogue “open” label is not a proof of present-day novelty or openness.

The web page https://www.unsolvedmath.com/problems/30000704 was attempted
first. The web reader could not access it; a direct request received HTTP 403.
The supplied public-dataset cache was used instead. Both files matched the
repository's pinned immutable dataset manifest by exact byte count and SHA-256.
The record is ID 30000704, code OWR-1460-010. The accompanying research-results
file contains no OWR-code entries and no report for this target; a missing
report is not treated as a completed attempt. No dataset text is bundled.

## Primary statement

Oliver Roth's problem-session contribution, in *Normal Families and Complex
Dynamics*, Oberwolfach Report 9/2007, pp.528–530, especially printed p.529
(PDF page 43), is the authoritative statement. Source:
https://ems.press/content/serial-article-files/46093
DOI: https://doi.org/10.4171/owr/2007/09

The report was inspected as text and as a rendered image. The metric is
positive and C² for the equivalence; curvature is bounded BELOW by -4;
the known case is an OPEN FREE C² SUBARC; the limits are unrestricted.
The immediate question asks how far the boundary hypothesis can be weakened.
It must not be confused with adjacent Problem 1 concerning holomorphic maps.

## Detailed 2007 paper: access limitation

Daniela Kraus, Oliver Roth, Stephan Ruscheweyh,
*A boundary version of Ahlfors' Lemma, locally complete conformal metrics and
conformally invariant reflection principles for analytic maps*,
Journal d'Analyse Mathématique 101 (2007), 219–256.
https://doi.org/10.1007/s11854-007-0009-x

Publisher page and metadata were inspected. The PDF URL returned 283,429
bytes of HTML subscription-preview content. It was correctly rejected as a
PDF. The full paper's proofs were NOT inspected. The one disk theorem used
by this note is explicitly stated on p.529 of the primary report. A 2013
thesis reproducing parts of the paper was used only to inspect the chart
mechanism, not to upgrade the fulltext access claim.

## Other primary mathematics checked

1. Kraus and Roth, *Conformal Metrics*, arXiv:0805.2235.
   https://arxiv.org/abs/0805.2235
   Sections 2, 3, 4 inspected for metric/curvature conventions, radial formulas,
   Schwarz comparison, and completeness. The survey uses curvature -1 for its
   basic metric; formulas must be divided by two for the -4 convention here.
   No new-result or novelty inference is drawn from this survey.
2. Kraus and Roth, *The behaviour of solutions of the Gaussian curvature
   equation near an isolated boundary point*, arXiv:0801.2866; Math. Proc.
   Cambridge Philos. Soc. 145 (2008), 643–667.
   https://arxiv.org/abs/0801.2866
   Theorems 1.1, 1.2, 1.4; extended comparison discussion; and proof §3.5
   inspected. The theorem uses curvature extending Hölder continuously with
   a negative limiting value, a stronger hypothesis than κ≥-4. It classifies
   conical orders versus the complete cusp; it does not make mere blow-up
   imply completeness at a puncture.
3. Bracci, Kraus, Roth, *The strong form of the Ahlfors-Schwarz lemma at the
   boundary and a rigidity result for Liouville's equation*,
   arXiv:2310.05521v2, 6 March 2024.
   https://arxiv.org/abs/2310.05521
   Theorems 2.1–2.4 and proof §§4.1, 4.4 inspected. Its strong Schwarz theorem
   has curvature bounded ABOVE by -4 and a prescribed sharp ratio rate.
   It therefore does not settle the lower-curvature equivalence question.
   The author's institutional publication page lists the article in 2026,
   DOI https://doi.org/10.1007/s11856-026-2918-3 .

Cross-check, not a substitute for the primary source:
Andrii Arman, *Generalizations of Ahlfors Lemma and Boundary Behavior of
Analytic Functions*, master's thesis, University of Manitoba, 2013, Chapter 3,
especially definitions 3.12–3.13, theorem 3.14, and corollary 3.15.
https://mspace.lib.umanitoba.ca/bitstream/handle/1993/22095/arman_andrii.pdf?sequence=1
Its chart proof explicitly uses nonvanishing continuously extended |φ'|;
some labels in its displayed formulas contain errors. No unsupported sharp
regularity conclusion is taken from those displays.

## Literature conclusion

The bounded source search did not produce a verified full resolution of the
arbitrary-boundary-set minimum-regularity question. This is a search result,
not a claim that none exists. The full 2007 KRR text is an important remaining
priority-check limitation. The author's own Theorem C is presented as a
partial sufficient theorem only, without a first-result claim.

The safe package contains authored text/code and public verification metadata;
source PDFs, source excerpts, raw datasets, and private history are excluded.
