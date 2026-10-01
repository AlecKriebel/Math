# Research log: 30005473

All timestamps are UTC on 30 September 2026. This log records research outcomes and validation, not private deliberation. Model: gpt-6-astra; reasoning effort: xhigh. Maximum five substantive attempts and two hours, starting 03:28; no model-ultra claim is made.

## 03:29 — source and duplicate triage

Requested problem URL tried before other sources. Direct web access failed and the cloud browser showed a 403 request-blocked page. The official Oberwolfach report and the repository's pinned dataset provide the statement. Read repository AGENTS.md, queue AGENTS.md, README.md, QUEUE.md, and policy.json. Queue row 27 has no historical attempt note and shows 0/5. Exact-ID and discotope all-state PR searches, branch search, and repository code searches found no previous research attempt. Main state.json is empty and is not relied on to erase historical queue notes. The related-target grouping does not contain this ID.

Completion estimate toward independently verified resolution: 10% (source triage only).

## 03:31 — source distinction established

Pinned source revision 37e53eabe540fb458758e198be61634bd02ee008 confirms the exact target is E, the Zariski closure of exposed points. There is no upstream prior report under the problem code. The 2023 OWR Conjecture 1 concerns E; 2022 Conjecture 8.2 concerns the larger purely nonlinear part S. Treat these as separate statements unless equality is proved. The source papers' degree and critical-locus questions are not part of the exact target.

Completion estimate: 20% (scope and elementary proof mechanism established; not independently verified).

## 03:34 — substantive attempt 1 completed: candidate proof

Saved candidate.md with a complete proof of E irreducibility without genericity. The mechanism is the real-analytic support-point parametrization over the complement of finitely many codimension-at-least-two kernel subspaces. An elementary two-segment construction proves the domain connected; analytic uniqueness proves the vanishing ideal prime. The manuscript explicitly identifies every exposed point as an image point.

A separate theorem proves S=E for generic subspace arrangements by simultaneously prescribing perturbations on summands annihilated by a supporting normal. A nongeneric full-dimensional example shows S can differ from E. Segment summands provide a reducibility boundary check.

Completion estimate: 85% (candidate proof complete; independent validation and priority assessment pending). Turn count: 1/5. This estimate is not a probability of correctness.

## 03:36 — exact checks and independent-review handoff

checks.py passed with SymPy 1.14.0. It checks the nongeneric separating polynomial identity exactly, all seven subset-rank conditions in a small general-position example, the associated face-perturbation limit, repeated-disc support formulas, and rank certificates for a normal-domain detour. These computations are sanity checks, not substitutes for the analytic proof. The initial unverified polynomial written for the nongeneric example was corrected during drafting before the exact-check run and before reviewer handoff; the verified polynomial is the one in candidate.md and checks.py.

The complete artifact was submitted for independent adversarial review. Source checks found no later resolution in the original arXiv record, current author bibliography, or focused public literature searches. This negative search is not a proof of novelty; no historical-priority claim is made.

Remote publication is paused at the coordinator's instruction because GitHub writes in the project returned an integration-access error. No remote branch or PR is claimed. Files are preserved in an isolated local folder. No shared queue, state, catalog, or review file was changed. No external researcher was contacted.

Completion estimate: 90% (candidate and checks ready; review and authorized repository write remain pending).

## 03:41 — independent audit passed

The independent mathematical audit accepted both the exact E theorem and the separate generic S=E theorem. No mathematical revisions were required. The reviewer independently derived and verified the nongeneric separating polynomial. The complete report, verdict, checks and reviewed candidate snapshot are preserved. The proof remains unrefereed and historical priority remains unestablished. The only subsequent candidate changes update these status statements; the mathematical content is unchanged.

Completion estimate: 95% toward an independently checkable research deliverable. Mathematical work and AI audit are complete; final artifact validation and authorized repository delivery remain. This does not claim human verification or novelty certification.

## 03:47 — delivery checks and repository checkpoint

Prepared a five-page typeset proof and inspected every final rendered page. The independently reviewed mathematical Sections2–6 are byte-identical to the final Markdown proof. Changes after review are confined to status wording and reference hyperlink formatting. Exact checks were rerun. GitHub write access is restored, and the dedicated branch has been confirmed at the inspected base commit. An all-state exact-ID PR search returned no prior PR before this checkpoint. Only this problem folder is included in the proposed commit.

Completion estimate: 95% toward the full research goal; mathematical proof and independent AI audit are complete, while human review and historical priority remain unestablished.
