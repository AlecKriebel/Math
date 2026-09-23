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
