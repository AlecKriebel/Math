# Independent corpus completeness audit

Audit date: 2026-10-24. Read-only discovery; no external individual contacted. Initial inventory audit completion estimate: 60%. Fresh primary-deposit cross-check completed 2026-10-24 10:30 PDT; overall corpus audit estimate: 80% (embedded archive manuscripts remain to classify).

## Strongest available local sources

- `/Users/alec/Documents/Math/.zenodo-state/`: 169 JSON publication receipts with 169 distinct published record IDs. Every referenced original manifest currently exists. Receipts record title, DOI, record URL, scientific payload hashes, verification time and manifest path. These receipts are **not a complete author bibliography**: they omit manually deposited early papers and at least ten recent publications from the final sweep whose actor used different state locations.
- `/Users/alec/Documents/Math/zenodo_discoverability_20261010/SOURCE_CATALOG.json`: complete historical account classification as of 2026-10-10: 97 owned record versions, of which 73 were manuscript records and 24 were supporting material, codebase releases or a draft. The 73 records link 82 checksum-matched or checksum-verified public PDF text files under `papers/<record_id>/`. Good reusable provenance, stale for present completeness.
- `/Users/alec/Documents/Math/zenodo_discoverability_20261010/ACCOUNT_FINAL_CHECK.json`: authenticated read-only account check with `all_versions=true`, 97 owned IDs, 73 manuscript records, 24 exclusions, no unaccounted owned record IDs in its contemporary scope.
- `/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/FINAL_RECONCILIATION_REPORT.json` and `.txt`: final 2026-10-23 audit of PRs #9–1446, including 14 new papers. Includes exact new DOI, ledger row, per-PR payload/identity evidence and proof-scope dispositions. Its final spreadsheet had 287 rows including a header, but those are mixed publication/source rows and **not 286 distinct authored papers**. 100 reconciled source/publication rows cover 102 PRs; 257 PRs have publication-recorded dispositions. PR counts, ledger rows, Zenodo record versions, latest concept records and scientific works are separate units.
- `/Users/alec/Documents/Math/PUBLICATION.md` and `README.md`: useful claim/priority histories and early paper descriptions, last updated 2026-09-26. They do not form a complete current catalogue.

## Independent count reconciliation and known traps

The 169 receipt IDs and 73 Oct-10 manuscript IDs intersect in 54 IDs and have union 188 record IDs. The historical 73 manuscript records resolve to 72 Zenodo concepts; after the explicit cross-concept qubit review-copy pair, they represent 71 scientific works at that historical checkpoint. Nineteen manuscript IDs in the old catalogue are absent from `.zenodo-state`. Thus receipt-only discovery demonstrably misses genuine papers.

At least ten of the final 14 sweep publications are absent from this checkout's central receipt directory; their DOI identities are in the final-sweep report. A fresh authenticated all-versions account capture is required for the final denominator.

1. **Legacy open-draft hiding a published manuscript.** The Oct-10 legacy representation of published record 21699069 had `submitted=true`, `state=inprogress`, `files=[]`. A published edit draft hid its public PDF. Native public metadata established one public manuscript file: `kriebel-2026-minimum-bell-setting-complexity-review-v1.1.0.pdf`, MD5 `a5a7a0d08c99e864159de09a7866f6ab`. Do not classify every inprogress/empty-file legacy response as an unpublished draft. Inspect native public record for all submitted publication omissions.
2. **Separate presentation copies.** Records 21699069 and 21699161 have identical mathematical title and descriptions but distinct concept IDs 21699068 and 21699160. One is the line-numbered review presentation. Preserve both for complete record inventory, identify them as presentations of one scientific work, and avoid counting their scientific impact twice.
3. **Older mathematical editions.** Records 21971507 and 22013710 share concept 21971506; native versions report older index 1 and latest index 2. Older title: “An exceptional four-dimensional unitary Hecke Yang–Baxter operator”; latest title adds “a five-word Pauli–Clifford normal form.” Both records belong in version history; score the newest scientific edition for the principal inventory, and retain the old edition explicitly.
4. **Publication metadata misclassification.** Record 22929556 (Knudson four-vertex counterexample) was explicitly rescued by historical classification even if an early upload-type field was not publication. Metadata resource type alone does not decide whether a scientific paper is present.
5. **Software releases often embed papers.** The historical excluded software series included many versions of Exact Diffusion Design and STC/JC packages. Their scientific papers already had separate manuscript deposits. Keep software/support records auditable as excluded or linked supporting deposits; do not score the same scientific content again merely because a release archive contains a PDF.
6. **A single deposit can contain multiple PDF presentations.** Historical 73 manuscript records had 82 PDF source files. Classify primary paper, appendix, review copy and other files before treating PDF count as paper count.

Historical exclusions include unpublished draft 21753316; source 21699181; integrity manifest 21699205; verification package 21699224; computational data 22064121; and nineteen mostly older codebase releases. The complete historical exclusion rationale is in SOURCE_CATALOG.json and RESULTS.json; current state must be rechecked.

## Assessment boundaries and quality/status warnings

All relevant published claims are hypotheses for evaluation. The repository explicitly labels them unrefereed and AI-assisted; internal independent-agent audits and passing exact verifiers are not conventional independent expert peer review. A bounded literature search does not establish global firstness.

The final sweep records 24 historical solved-status withdrawals/reclassifications (23 already_solved, one partial), 18 priority/scope/identity/accounting holds and three original-scope partial results. These are not a count of false proofs. Many holds contain correct deductions whose novelty or original scope was not cleared. Do not silently promote all solved PR labels to novel authored results. The corpus must use the actual published paper's qualified claim and credited source.

Local PUBLICATION.md also distinguishes superseded/consolidated Keller-map explorations and credits pre-existing mechanisms. This is a general warning that titles and raw author records do not independently establish novelty.

## Final acceptance criteria

- Fresh authenticated account listing includes all versions and terminates pagination without duplicate IDs.
- Every account record classified; all omitted publication-like records receive native public metadata scrutiny.
- Manuscripts separate from drafts, software, source, integrity, and verification deposits.
- Every manuscript/version has an accessible deposited PDF and extracted text with checksum provenance.
- Latest concept versions and cross-concept presentation copies identified; record, version, and scientific-work counts stated separately.
- Every assessed principal work maps to exactly one spreadsheet row and every excluded/archive record remains auditable.

## Pending final cross-check

Fresh `sources/corpus_records.json` cross-checked independently:

| Unit | Independently checked count |
|---|---:|
| Fresh owned all-version records | 226 |
| Distinct account IDs | 226 |
| Primary manuscript record versions | 202 |
| Primary manuscript concepts | 201 |
| Principal scientific works after explicit qubit presentation duplicate | 200 provisional |
| Primary manuscript PDFs, including supplements | 211 |
| Independently recomputed PDF MD5/byte-size and nonempty extracted-text checks | 211 passed, zero failures |
| Excluded top-level records | 24 |
| Historical manuscript IDs absent from fresh primary corpus | 0 |
| Local 169 published-receipt IDs absent from fresh primary corpus | 0 |

The fresh account capture used three pages of 100,100,26 records and provides response hashes. No duplicate record ID was observed. All 202 primary manuscript records carry the author ORCID. Normalized-title collision search found only the explicit cross-concept qubit presentation pair. No two primary manuscript PDFs have identical MD5 checksums. The historical Yang–Baxter pair remains the sole multi-version primary manuscript concept.

**Do not promote the 200-work provisional count to “ALL papers” yet.** The top-level exclusion policy misses scientific manuscripts embedded inside software snapshots. Confirmed examples:

- Record 21753405, software snapshot `universal-db-obstruction-v1.0.0`, is explicitly the archival DOI for the distinct 13-page “No universal death–birth amplifier on a finite weighted population structure.” Publication record and frozen manuscript SHA-256 are recorded in `universal_simultaneous_amplification/publication/RELEASE_RECORD_v1.0.0.md`. There is no separate primary manuscript deposit for this theorem in the fresh 202.
- Record 21753527 → 21753997 archives version 1 → version 2 of the reversible mass-action continuum paper. Frozen v2 source at git tag `wr-continuum-v2.0.0`, path `weakly_reversible_continuum_no_common_factor/releases/v2.0/source/MANUSCRIPT_V2.md`, explicitly states that v2 retains v1 and extends it to a four-parameter family, generic coprimality, a smaller fixed-support optimal integer specialization, and transverse stability. This is one additional scientific work, with two meaningful editions. It is absent from the fresh 202 primary PDFs.
- Full repository archives can also embed early paper-page manuscripts such as Keller-map notes, cyclic Bell papers, eternal-domination papers and neural-code notes. Their scientific status must be semantically classified; a monorepo release ID does not make each embedded manuscript a new independent Zenodo concept.

Acquisition agent is enumerating/extracting all excluded archives. Final acceptance requires a separate embedded-manuscript inventory, with author papers, older editions, draft/audit/support files and repeated snapshots distinguished. No impact scores were assigned in this independent inventory audit.

## Existing spreadsheet and public notebook cross-check

The target Full List tab was empty in the retained starting snapshot. The existing Papers tab has62 rows including header and a mix of research programs, manuscripts, and blank/administrative rows. It includes many author manuscripts without a dedicated primary Zenodo-paper DOI. Its Yang–Baxter DOI21971506 is a concept DOI; latest manuscript record22013710 is correctly represented in fresh primary corpus.

The existing Math Puzzles tab has287 rows including header and explicitly includes other authors' prior publications. It is a research/outcome ledger, not an authored bibliography; do not attribute all its rows to Alec Kriebel.

Current `docs/papers/` contains40 paper-page folders,40 canonical paper.pdf files, and27 canonical PDF checksums unmatched among the211 primary deposited PDFs. Unmatched files include actual extra papers, older editions and archival precursors. This is an independent signal requiring the software-archive expansion. Some public-notebook papers developed after the latest2026-09-07 software snapshot may have no verified Zenodo representation (e.g. equal-sum-product and knights/rooks notes); preserve them as repository-only if inclusion is needed to satisfy all authored papers, with DOI blank and publication-status qualification.
