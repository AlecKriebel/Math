# Research log

## 2026-09-23T03:26:16Z — Intake checkpoint (10%)

Goal: determine whether the supplied filtered interval refutes Knudson's
Conjecture 2 (OWR 29/2008, p. 1629); if verified and no concrete priority
collision is found, prepare a concise preprint, exact verifiers, GitHub Pages
page, and manual Zenodo package. Percentages estimate progress through this
verification/publication task, not a probability of mathematical correctness.

Copied the two user-supplied artifacts unchanged into `inputs/`. Treated their
claims as hypotheses. The original report is the authoritative target; the
user associates it with OWR-2040-002. Independent mathematical and literature
agents were assigned distinct audits under the repository research policy.
The repository is on main with pre-existing unrelated modifications, excluded
from this effort. No external communication is permitted or planned.

## 2026-09-23T03:29:13Z — Source and computation checkpoint (60%)

Read Knudson's complete contribution at pp. 1628–1630 in the primary report:
https://ems.press/content/serial-article-files/46173 . It allows arbitrary
simplex-wise filtrations with F2 coefficients; VP is precisely the incident
part of the persistence pairing. Conjecture 2 concerns this fixed field.
The supplied Python program was inspected before execution and ran
successfully. Its reduction and union-find calculations agree.

Independent adversarial reconstruction also finds zero paths from ac to b.
The subsequent-cancellation interpretation is a different statement and is
not an extra hypothesis in the report. The catalogue page itself failed in
the web tool and returned HTTP 429 through direct retrieval; no claim is made
about its current status. A fresh independently structured checker and
priority review remain to be finished. Existing GitHub Pages uses main:/docs.
No release or Zenodo deposit will be made; only a manual deposit kit is requested.

## 2026-09-23T03:35:53Z — Verification/priority checkpoint (80%)

Mathematical verification is complete against the primary source. Both exact
verifiers pass normally and under Python optimization. The independent agent
reports no gap. The priority agent finished 39 logged searches: no earlier
explicit refutation located, with unpublished-work, book/thesis, and citation-
index limitations retained. A further elevated retrieval of the public Bauer
thesis failed with HTTP 403. The original report was downloaded temporarily
and printed p. 1629 visually inspected. No source PDFs are redistributed.

Prepared and visually checked a three-page manuscript. It claims a factual
counterexample to the original Conjecture 2, not first discovery or verified
current catalogue status. A final independent artifact review is underway.
The manual Zenodo kit and GitHub Pages publication remain to be completed.

## 2026-09-23T03:42:37Z — Release-candidate checkpoint (95%)

The independent prepublication review passed all proof and code checks. Its
minor documentation correction (H0 inclusion-map ranks, not all such ranks)
was applied. All three PDF pages were rendered and visually inspected.
The static site was inspected in the local browser, including the diagram and
reduction table; every local link and anchor resolves. Source archives and
metadata were validated after extraction, and rebuilding the kit from its
extracted sources produced identical bytes.

Checkpoint 7ffac2c0d was committed; remote main had an unrelated queue update,
so it was merged without rewriting history. Merge 0a52482b8 was pushed.
The final page and kit now await the publication push and live verification.
The source kit freezes this predeployment research-log snapshot; postdeployment
checks will be recorded separately in audit/deployment.md and the repository
log. No mathematical or manuscript changes are planned.

## 2026-09-23T03:46:26Z — Published checkpoint (100%)

GitHub Pages built publication commit 2e5c47d93 successfully at
2026-09-23T03:44:39Z. All 12 live project files returned HTTP 200 and matched
local bytes, and the live page was opened and verified in the browser.
The final exact source archive and its byte-reproducible Zenodo kit passed a
clean extraction check. See audit/deployment.md for hashes and evidence.
The archived research log remains the intentional predeployment snapshot;
this entry does not change the mathematical or download artifacts.
All requested tasks are complete, with the documented historical-priority
limits and manual DOI assignment left explicit.

## 2026-09-23T13:35:06.659952+00:00 — Fresh preprint review started (10%)

User requested a new adversarial review/fix/review loop for preprint readiness.
Baseline hashes recorded in audit/preprint_baseline.json. A fresh agent is
reviewing the paper and primary sources independently of prior verdicts.
Both verifiers pass normally and optimized; the archived kit rebuilds
byte-identically from its extracted source. No journal-submission work is in scope.

## 2026-09-23T13:38:40.343232+00:00 — Review round 1 and correction checkpoint (60%)

Fresh round 1 independently passed the mathematics, primary-source scope,
all-field extension, cited comparison and both exact verifiers. Its only
actionable item was the parent-identified invalid CFF root type. Corrected it
and validated the resulting CFF against the official 1.2.0 schema. Added PDF
title/author metadata, links to the companion page and cited author bibliography,
and explicit critical-simplex/path definitions. Version 1.0.1 propagates the
changes across current metadata, instructions and public copies; the theorem
and verification calculations are unchanged. A new independent reviewer will
now review the revised material.

## 2026-09-23T13:45:00.572430+00:00 — Fresh round 2 clean pass (95%)

A distinct new adversarial agent independently decomposed the persistence
module, checked all paths and coefficient conventions, primary references,
PDF pages and annotations, citation schema, metadata and clean extracted
archive reproducibility. It found zero actionable defects. The requested
review/fix/fresh-review loop is complete. The revised three-page preprint
(v1.0.1) has no identified mathematical or artifact blocker. Historical-
priority and human-review limitations remain calibrated.

All reviewed scientific files are frozen at the round-2 hashes. Added only
review reports and documentation of the completed cycle; regenerated packages
will include these records. Publication and live-download checks remain.

## 2026-09-23T13:51:19.083134+00:00 — Preprint revision published (100%)

Two fresh adversarial rounds are complete; round 2 found no actionable
mathematical, bibliographic, PDF, metadata or package defects. Version 1.0.1
fixes the citation metadata and improves standalone discoverability and
definitions without changing the theorem. Publication commit 27c8b68d1 is
pushed. A successful descendant Pages deployment serves all 12 project files
with bytes identical to the final checked local materials. The revised Zenodo
kit includes both review reports and passes clean extraction/rebuild checks.
Detailed hashes and deployment evidence are in audit/deployment.md.
This final log entry is outside the intentional predeployment source snapshot.
No journal-submission work was undertaken.
