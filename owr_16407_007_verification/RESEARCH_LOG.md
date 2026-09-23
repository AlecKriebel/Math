# Research log: OWR-16407-007

## 2026-09-23T03:40:19.953760+00:00 — initial source checkpoint

- Goal: verify the supplied candidate as a complete, novel resolution; prepare a resolution publication only if both correctness and priority pass.
- Verification/audit completion estimate: 45%. Verified novel-resolution completion: 0%; no novelty established.
- Exact mathematical target: the stated derivative expansion for the one-variable function obtained from the noncommutative Phi^4 boundary-value construction, as a formal series at lambda=0.
- Success requires both the formal resummation and an independent identification with the function defined by the model. Finite coefficient checks alone do not suffice.
- Main branch confirmed. Existing unrelated changes left untouched.
- Independent approach families: (1) formal algebra and adversarial logical dependency audit, (2) historical source and priority audit, (3) parent reading of the model equation and reproducible coefficient checks.
- Primary-source finding: v1 presents the main result as a conjecture; v2 presents it as a theorem and adds a proof of the solution.
- Candidate's route is blocked as a standalone proof: asserting I=K-lambda L transfers the missing model identification into an unsupported equality.
- Original problem URL returned HTTP 429 in direct retrieval and was inaccessible through the web tool; alternative read-only access is being attempted.
- No individuals contacted. No release or DOI created.

## 2026-09-23T03:45:15.116428+00:00 — mathematical and priority checkpoint

- Verification/audit completion estimate: 90%; final artifact review and repository publication remain. Novel-resolution completion: 0%; priority fails.
- Both independent reviewers found the same fatal candidate gap: resummation is not identification with the independently defined integral.
- Parent independently read v2 Lemma 10 and Proposition 11, including the monotone substitution and cutoff correction. These supply the missing identification in prior work.
- The original listing was retrieved successfully through a read-only browser visit; it matches the target exactly but its open-status assessment overlooks the revised proof.
- Common finite-cutoff identity (v2 17c) connects the v1 exponential-Hilbert definition with v2 equation (21). Formal triangularity supplies uniqueness in the admissible coefficient class.
- Reproducible checks passed: 20 symbolic K/L coefficient comparisons through order 10, endpoint jets, and 12 model-integral coefficient checks at 50 decimal digits with discrepancies below 1e-35. These are finite supporting checks, not the all-orders proof.
- Requested new-resolution publication workflow is not activated: the candidate is incomplete and the result already belongs to Panzer–Wulkenhaar (2018 proof; 2019 online journal publication). No new-resolution paper, website, or Zenodo package will be represented as warranted.
- All deliverables remain under the dedicated top-level folder; unrelated concurrent repository edits are untouched.

## 2026-09-23T03:46:26.121912+00:00 — repository checkpoint

- Verification/audit completion estimate: 95%; final independent artifact review pending. Novel-resolution completion: 0%; theorem already established.
- Audit, independent reviews, verifier, numerical results, and source record committed as d6fd08aea and pushed successfully to origin/main.
- No GitHub release was created, avoiding the repository's automatic DOI/deposit integration.

| Approach family | Mechanism and evidence | Status | Exact remaining gap |
|---|---|---|---|
| Formal algebra | Coefficient recursion, Lagrange inversion, removable endpoint | Verified resummation | Cannot identify the model function by itself |
| Model equation | Common-cutoff identity, v2 Lemma 10 and Proposition 11, triangular formal uniqueness | Identity established in prior work | No unresolved target-identity gap found; unrestricted nonanalytic uniqueness not claimed |
| Priority and original source | Original OWR eq. (9), arXiv version history, publisher dates | Priority fails decisively | No basis for a new-resolution priority claim |
| Reproducible computation | Symbolic coefficients and finite numerical integral checks | Passed | Finite checks do not prove all orders; quadrature is not interval-certified |
| Adversarial artifact review | Independent review of scripts, results, and claims | Pending | Final reproducibility and wording check |

## 2026-09-23T03:47:23.903653+00:00 — final audit checkpoint

- Verification/audit completion estimate: 100% for the requested candidate-validity and novelty decision. Novel-resolution completion remains 0%: this audit produces no new theorem.
- Final adversarial review found no actionable defects in the scripts, recorded output, scope statements, or attribution. Reviewer independently reran the verifier and regenerated the recorded exact and numerical results without changing the parent evidence.
- The artifact-review family is complete; its former pending gap is closed.
- Final determination: the formal target identity is established by the 2018 prior proof; the submitted candidate alone omits the essential model identification. A new-resolution priority claim fails.
- Deliverables are a concise audit and verifier, not the conditional new-resolution publication bundle. No paper claiming a new resolution, GitHub Pages site, Zenodo metadata/upload, release, or DOI was created.
- Final reviewer report and this completion log are ready for the final scoped main-branch commit and push.
