# PR12 document-claims and history audit

Checked independently on 2026-10-01 UTC. Candidate: `reviewed_candidate/` at
`draft_pr_publication_program_20260930/audits/pr12_30005897/`.
Scope: current-document consistency, known-method credit, and preservation of
historical labels. Mathematical correctness and external source validity were
not audited. No external research, outreach, Git operation, or candidate edit
was performed.

Exact inspected `PROOF.md` SHA-256:
`2d2e394d83ab96a6aee9b022d375fb1520499ed4aa360de51f7d1ed04f5b75ea`.
All inspected document hashes are recorded in `preservation_checks.json`.
This final pass applies to those bytes. The first pass on proof
`782a92710ba0e1932bdf02e89f741df2fdf74651d09af260d1e0b1a391da8fa4`
is preserved in five files with suffix `_initial_20261001T134938Z`.

**Verdict: PASS in this scope. Mandatory issues: none. Completion: 100% of this
document audit.** This does not settle the parent acceptance audit.

## Current claims

| Finding | Exact candidate locations |
| --- | --- |
| The main documents credit a full-scope corollary of older equivalent machinery and expressly disclaim new theorem/first-resolution priority. | `PROOF.md:3–7,384–416`; `PRIORITY_AUDIT.md:3–4,16–20,54–59`; `README.md:1–8`; `attempt_status.json:5,18,34,37–39`; `pr_draft.md:3–15` |
| The precise earlier composition-operator wording is not asserted to have been found or advertised. Lack of an exact-question search hit is not treated as novelty clearance. | `PROOF.md:412–416`; `SOURCE_AUDIT.md:149–163`; `PRIORITY_AUDIT.md:54–59`; `pr_draft.md:14–15` |
| Final acceptance remains pending; the proposed disposition is `already_solved`. No new paper, DOI/deposit, or tracker/spreadsheet row is proposed or claimed. | `PROOF.md:3–7,410–412`; `PRIORITY_AUDIT.md:3–4`; `README.md:6–8`; `attempt_status.json:34,39–42`; `pr_draft.md:6–8` |
| Imported-method provenance is bounded: the inspected 2020 statement attributes the result to the uninspected 2011 proof. The avoided equation (33) issue is disclosed. | `PROOF.md:384–408,456–463`; `PRIORITY_AUDIT.md:16–20,44–50`; `pr_draft.md:12–15` |
| The appended precision correction explicitly distinguishes the original printed norm equality from the historical plain-shift operator countercheck, records a broader norm counterexample and repairable growth estimate, and says the old spectral theorem is not refuted. | `PROOF.md:465`; `PRIORITY_AUDIT.md:70`; `SOURCE_AUDIT.md:165`; `attempt_status.json:43`; root `ROOT_EQ33_PRECISION.md:3–8,10,22–26,28–38` |
| The aggregate-mass question, prior representation, and separable complex p=2 slice receive prior-art credit; the current documents do not claim to resolve a general Banach or structural-stability conjecture. | `PROOF.md:9–13,156–159,369–380,418–425`; `SOURCE_AUDIT.md:30–43,69–73,79–94`; `PRIORITY_AUDIT.md:61–64`; `attempt_status.json:14–15`; `pr_draft.md:19–21` |
| AI audit is distinguished from human peer review and formal certification. Original model/effort fields are described as historical, rather than attributed to later audits. | `PROOF.md:3–7`; `PRIORITY_AUDIT.md:66–68`; `README.md:17–19,23–26`; `attempt_status.json:23`; `pr_draft.md:17–18` |

## History is preserved and superseded explicitly

The old source-search conclusion remains at `SOURCE_AUDIT.md:140–147` and is
expressly superseded by the timestamped current reconciliation at lines
149–163. Its original September 30 audit date remains at lines 3–4. This
preserves the old unresolved-priority judgment without presenting it as the
current disposition.

`README.md:11–15` labels `review/` as historical artifacts and the pinned
source fields as upstream historical assessment superseded by the audit.
`PRIORITY_AUDIT.md:9–10` makes the same distinction for the original open
classification. The original record itself retains its dated triage and
open status (`source_record.json:6,8,15,26,31`). `source_provenance.json:2–19`
remains pinned provenance, not an independent current-priority verdict.

The original review is dated (`review/REVIEW.md:4–6`;
`review/verdict.json:3–4`), including its unresolved-priority assessment
(`review/REVIEW.md:12,101–107`; `review/verdict.json:12`). The historical
review request is expressly labeled superseded at `review_request.md:1`.
The prior log remains at `RESEARCH_LOG.md:3–101`, with a separately
timestamped reconciliation at lines 103–114.

The reproducible `preservation_check.py` produced
`preservation_checks.json`: all 12 checks passed. The pinned source record,
provenance, and seven `review/` files are byte-identical to `source_snapshot/`.
The old `SOURCE_AUDIT.md` and `RESEARCH_LOG.md` remain byte-for-byte prefixes
of their current versions; the original review request remains a byte-for-byte
suffix after its historical header. No reviewed historical material was erased.

## Final precision-update recheck

The final three appended notes use identical qualification and correction-link
text (`PROOF.md:465`; `PRIORITY_AUDIT.md:70`; `SOURCE_AUDIT.md:165`). Their
GitHub links all identify the exact locally existing audit-root
`ROOT_EQ33_PRECISION.md`; `preservation_checks.json` records each URL, its
resolved local counterpart, and the root correction's hash. Remote publication
of the links was not tested in this local-only audit.

The root correction labels the completed equivalent-family report immutable
at `ROOT_EQ33_PRECISION.md:3`. Its lines 4–8 qualify the historical countercheck:
the printed display concerns norms, while the plain-shift example alone
distinguishes operators. Lines 10 and 22–26 describe the broader-module norm
counterexample, and lines 28–38 describe a repair and explicitly distinguish
the identity issue from a disproved theorem. These are consistently summarized
in the current appended notes and the status note; this audit checks their
textual consistency, not the mathematics of those constructions.

The old report's narrower equation (33) characterization is thus preserved as
history and explicitly qualified by the correction. The current documents
continue to credit the old scalar theorem, exclude equation (33) from the
sufficient route, disclaim novelty, and leave full acceptance pending. There
is no unintended current claim that the old spectral theorem is invalid.

## Context outside the candidate

Audit-root `README.md:3` still describes equivalent-method falsification as
ongoing. Audit-root `RESEARCH_LOG.md:9–13` dates the last recorded root
checkpoint to 13:33 UTC, before the candidate's 13:42 reconciliation. This is
an earlier workflow checkpoint, not a conflicting new-solution claim. Updating
that root summary when the acceptance audit finishes would improve currency;
it is not a mandatory defect in the scoped candidate.

Optional wording clarity only: `PRIORITY_AUDIT.md:49–50` says hypothesis
matches were “falsified independently” while reporting no obstruction. The
surrounding text plainly means subjected to attempted falsification; using
“adversarially checked” would avoid the literal ambiguity. No mathematical
assessment of those matches was made here.
