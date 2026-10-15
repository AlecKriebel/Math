# Priority search and version evidence

Audit date: 2026-10-06, America/Los_Angeles (remote API responses use UTC).

This is a query ledger, not an assertion of exhaustive searching or novelty. Search engine responses mixed primary and irrelevant secondary results; only the primary sources identified in the audit support mathematical or priority conclusions. None of the lack-of-match observations establish that a result has never appeared.

## Web queries

1. `"Kaplansky" "idempotent" "2026" "OpenAI"`
2. `"A Torsion-Free Group Algebra That Is Not Directly Finite"`
3. `"torsion-free" "idempotent" "OpenAI" "2026"` (github.com, arxiv.org, zenodo.org)
4. `"Kaplansky" "idempotent" "characteristic two" counterexample` (github.com, arxiv.org, zenodo.org)
5. `"A Torsion-Free Group Algebra That Is Not Directly Finite" idempotent`
6. `"Kaplansky" "projective" "OpenAI"`
7. `"torsion-free" "idempotent" "October" "2026"` (arxiv.org, zenodo.org, github.com)
8. `"Kaplansky" "cancellation" "2026"` (arxiv.org, zenodo.org, github.com)
9. `"Kaplansky" "idempotents" "Kriebel"`
10. `"OpenAI" "e=1-ba"`
11. `"Kaplansky" "idempotent" "Kriebel"` (zenodo.org, github.com, arxiv.org)
12. `"openai_followon_kaplansky_idempotents"`
13. `"R ≅ R ⊕ P" "Kaplansky"`
14. `"torsion-free" "characteristic-two" "idempotent"`

Useful primary search result: Giles Gardam's lecture source at `https://github.com/gilesgardam/lectures/blob/main/kaplansky.tex` explicitly contains the classical hierarchy through direct finiteness and the defect-idempotent calculation. OpenAI's overview and formalization catalogue were also returned. The other search results did not supply a verified additional prior torsion-free characteristic-two idempotent theorem.

## Primary URLs opened or fetched

- `https://arxiv.org/abs/1904.04847`: version 3, July 20, 2023; first submitted April 9, 2019. Current title: *Units, zero-divisors and idempotents in rings graded by torsion-free groups*, Johan Öinert. Independent full-text/citation audit is recorded in `../CLASSICAL_PROVENANCE_AUDIT.md`.
- `https://github.com/openai/math`: current publicly accessible repository.
- `https://api.github.com/repos/openai/math`: response saved as `remote_repo.json`; `private=false`; creation timestamp 2026-10-06T21:47:02Z. This metadata alone does not prove that the repository was public from creation.
- `https://api.github.com/repos/openai/math/commits?per_page=100`: `remote_commits.json`; only listed commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
- `https://api.github.com/repos/openai/math/commits?path=preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026&per_page=100`: `remote_oct4_history.json`; same initial commit, no later correction shown at this check.
- `https://api.github.com/repos/openai/math/events`: `remote_public_events.json`; no Create/Push/Public/Release event returned. Thus the event endpoint did not establish the first public-access timestamp.
- `https://api.github.com/repos/openai/math/releases`: `remote_releases.json`; empty.
- `https://api.github.com/repos/openai/math/tags`: `remote_tags.json`; empty.
- `https://api.github.com/repos/AlecKriebel/Math/contents/openai_followon_batch2_20261006/REPORT.md`: `triage_remote_report_status.json`; exact decoded bytes in `REMOTE_TRIAGE_REPORT.md`.
- `https://api.github.com/repos/AlecKriebel/Math/contents/openai_followon_batch2_20261006/agent_notes/algebra_groups.md`: `triage_remote_algebra_status.json`; exact decoded bytes in `REMOTE_TRIAGE_ALGEBRA.md`.
- `https://api.github.com/repos/AlecKriebel/Math/commits?path=openai_followon_batch2_20261006/REPORT.md&per_page=100`: `triage_report_commits.json`; first listed path commit `f27318d83bd7000ef817957a9a4b3087de28d198`.
- `https://api.github.com/repos/AlecKriebel/Math/commits?path=openai_followon_batch2_20261006/agent_notes/algebra_groups.md&per_page=100`: `triage_algebra_commits.json`; same path commit.

The web browser tool could not fetch the GitHub commits API or commits HTML page. An ordinary unauthenticated HTTPS API read then succeeded; the exact responses above preserve the evidence. No upstream clone or git refs were changed, and no external individuals were contacted.

## Source searches

- Inspected the family 197 catalogue entries and all four family manuscripts' TeX/README disclosures.
- Searched `.tex`, `.md`, and `.bib` in the relevant companion source copies for idempotent, projective, cancellation, K_0, torsion, coefficient, corollary, and reverse-defect formulations.
- Inspected exact main theorems and relevant introductions/conclusion sections in the torsion-free zero-divisor paper, characteristic-zero Bass/idempotent paper, ℓ¹ Bass paper, and Kadison–Kaplansky projection paper.
- Inspected `lean/docs/197.md` to distinguish its actual stated formalization scope from the catalogue heading.
- Checked the local triage paths' git history and state. They appear untracked in this shared local checkout, but the remote API proves they are publicly present on remote main. Local untracked status therefore does not establish unpublished status.

These searches found an affirmative duplication witness in the user's already-public triage, independent of any unsuccessful keyword queries.
