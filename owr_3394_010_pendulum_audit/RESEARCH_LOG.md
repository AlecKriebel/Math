# Research log: OWR-3394-010 pendulum audit

Completion percentages estimate progress through this verification and priority
audit, not the probability that the mathematical statement is true.

## 2026-09-23T04:05:27Z — Initial checkpoint (35%)

- Claim under test: for the normalized forced damped pendulum on the cylinder,
  one class-K gain works for every measurable essentially bounded open-loop
  input, outside an input-dependent set of zero area.
- Success criteria: verify the original statement, check the candidate's
  calculations and every imported hypothesis, and establish whether the claim
  is new before preparing resolution-publication materials.
- Independent approaches commissioned under the repository research policy:
  adversarial mathematical falsification and primary-source/priority review.
- Primary evidence located: Angeli–Praly, IEEE TAC 56(7), 1582–1592 (2011),
  DOI 10.1109/TAC.2010.2091170. Its introduction identifies the Oberwolfach
  question and its Section III.A treats this pendulum. A CDC 2010 version also
  exists, DOI 10.1109/CDC.2010.5717582.
- Provisional result: affirmative mathematical answer; no new-resolution
  priority. Publication as a novel resolution is blocked by direct prior work,
  not by an unresolved mathematical conjecture.
- Work confined to this dedicated top-level folder on main. No outreach.
  Existing unrelated working-tree changes are excluded from this effort.

## Approach ledger

| Family | Mechanism | Evidence/status | Exact remaining gap |
|---|---|---|---|
| Direct hypothesis verification | Energy, strict Lyapunov function, eigenvalues, flow | Algebra checked by lead; exact verifier in preparation | Checkable recorded calculations and final source mapping |
| Adversarial dynamics | Attempt counterexamples and quantifier changes | Independent reviewer working | Written review pending |
| Primary-source/priority | Original report versus later theorem and application | Explicit overlapping prior publication found | Final page-level record and review pending |
| New-resolution publication | Claim novelty for this same theorem | BLOCKED | Direct prior result; reopen only for a materially distinct new theorem |

## 2026-09-23T04:11:01Z — Verification checkpoint (90%)

- Both independent reviewers accept the conclusion as a corollary of the
  published theorem and reject a new-priority claim. Their reports are saved.
- Visually verified OWR printed pp. 670–671 and IEEE pp. 1583, 1587–1588.
  The original report's equations and quantifier order match exactly.
- Repaired the sole application-level presentation gap: explicitly pass from
  the energy bound to eventual confinement with positive slack.
- Exact standard-library verifier passes 11 checks, including rejection of a
  deliberately false energy identity. Saved output: verification/result.json.
- AUDIT.md includes direct certificates, all theorem hypotheses, half-line
  input extension, uniform entry from compact sets, and continuous gain
  stitching. An adversarial final artifact review is pending.
- The current UnsolvedMath catalogue page and alias could not be inspected;
  that limitation is recorded and is immaterial to the primary-source match.
- Publication decision: the user's clean-priority condition fails. No new
  resolution paper, GitHub Pages site, Zenodo upload kit, or GitHub release.
  Preserve and publish the audit record only. New-discovery completion is not
  claimed; the exact target theorem is already resolved in the literature.
- Remaining work: final artifact review, scoped repository commit/push, and
  verification that the committed files reach origin/main.

## 2026-09-23T04:11:48Z — Final audit checkpoint (100%)

- Independent adversarial review of the assembled AUDIT.md and verifier is
  clean; its addendum is included. The reviewer independently reran all 11
  checks and accepted the explicit globalization and gain stitching.
- Final conclusion: full affirmative answer as an application of documented
  prior work, with the eventual-confinement clarification supplied. No central
  gap remains in this application; the general robustness theorem remains an
  explicitly cited dependency, not a formally reconstructed proof.
- Final approach status: direct checks PASS; adversarial dynamics PASS;
  primary-source match PASS; new-resolution priority FAIL; new-resolution
  publication route CLOSED by prior work. No further mathematical work is
  necessary to answer this exact problem.
- This checkpoint is ready for a scoped commit and push on main. Only the
  nine audit files are included; third-party reading copies remain ignored.
  Git history records the publication commit. Remote delivery is checked
  separately after the push; no GitHub release or DOI is created.
