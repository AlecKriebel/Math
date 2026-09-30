# Source and prior-attempt audit

Checked 30 September 2026. Limited current searches are not a certificate of
novelty or of present-day openness.

## Exact primary source

The full original report was retrieved from
[EMS Press](https://ems.press/journals/owr/articles/4135), DOI
10.4171/OWR/2009/52. The complete relevant contribution by **Benjamin Rossman**,
*The k-Clique Problem on Random Graphs & New Conjectures on AC⁰*, is on printed
pp.2825–2826. Both pages' text was read; printed p.2825 was rendered and inspected.
The source is in Oberwolfach Reports 6 (2009), pp.2787–2850; the publisher records
publication on 1 September 2010, explaining the dataset's 2009/2010 labels.

The source defines average maximal sensitivity by averaging the pointwise maximum
under the uniform cube measure. Its induction question has n input functions and
n conjunction outputs on n variables. The inputs are not required to have
bounded-depth circuits in the exact implication being asked. It also mentions a
weaker subpolynomial variant. The following balanced-graph-property conjecture is
separate. The known AC⁰ estimate preceding the question is motivation, not its
proof. The frozen artifact retains these distinctions.

The full pinned record, 30001377 / OWR-4135-008, appears in source_record.json.
It is from dataset revision 37e53eabe540fb458758e198be61634bd02ee008.
No exact-code research report is present in the pinned research_results.json.
The upstream desk assessment was treated as provisional context only.

## Current and foundational literature checks

- **Benjamin Rossman, The Average Sensitivity of Bounded-Depth Formulas**,
  [arXiv:1508.07677v1](https://arxiv.org/abs/1508.07677v1). Full PDF retrieved;
  introductory theorem statements, definitions, random-restriction mechanism
  and the displayed induction parameter were checked. It proves a sharper
  formula-size/depth sensitivity bound using the Switching Lemma. It does not
  state the arbitrary-family ams closure principle as a corollary. No claim of
  having independently verified every estimate in that paper is made.
- **Hao Huang, Induced subgraphs of hypercubes and a proof of the Sensitivity
  Conjecture**, [arXiv:1907.00847v2](https://arxiv.org/abs/1907.00847v2), August
  2019. Full PDF retrieved; its main theorem, definitions and sensitivity
  consequence were checked. The maximum over cube inputs in that result is
  different from the current average of a family maximum. Its solved classical
  conjecture is not evidence that the present question is solved.
- **R. W. Hamming, Error Detecting and Error Correcting Codes**, Bell System
  Technical Journal 29 (1950), 147–160,
  [publisher record](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1950.tb00463.x).
  Bibliographic record checked for attribution. The classic syndrome construction
  is credited, and every property used in the obstruction is proved directly;
  no unexamined coding-theoretic theorem is invoked. No full original-paper
  retrieval is claimed.

Searches for the exact phrase “average maximal sensitivity”, its maximum variant,
Rossman with “ams”, “conjunction”, “AND” and “inductive”, and recent sensitivity
literature produced no verified solution of this precise implication. Most broad
sensitivity results concern different measures or circuit classes. This bounded
search does not establish that no relevant unpublished or differently named
result exists. All restricted deductions and standard constructions are presented
without novelty claims.

## Prior Alec/campaign and duplicate gates

The live queue showed rank 100, queued, 0/5. All-state PR searches for the numeric
ID and for “sensitivity” returned no previous attempt. The proposed branch was
absent. The attempt path had no all-branch history; the related-target index had
no matching entry. Repository-wide matches were desk-review/ranking metadata,
not proof attempts. Repetition as a suggested desk route was independently
checked: because the statistic uses a maximum, repetitions alone do not change
it. The skip rule therefore did not apply.

The branch contains no queue, catalog or shared-state edits and did not run the
queue generator. Source PDF hashes and retrieval scopes are recorded in
source_manifest.json; source PDFs are not distributed in this package.
