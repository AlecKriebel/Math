# Fresh candidate v3 priority and metadata subaudit

Audit date: 2026-10-07 UTC (2026-10-06 America/Los_Angeles). Reviewer scope: independent priority, attribution, title/metadata, authorship, disclosures and license audit for complete-package review 4. Best-guess completion of this scoped audit: 100%; this is not an estimate or certification of mathematical resolution or publication readiness.

## Verdict and scope

No substantive priority, attribution, title, authorship, disclosure or license inconsistency was identified in the exact files below. The candidate consistently presents an explanatory immediate corollary of the OpenAI EGH input and the published Harima–Wachi–Watanabe implication. It does not advertise an independently invented EGH proof, a new all-ideal extension of HWW, or first priority. Approval of the central unrefereed mathematical input remains the responsibility of the separate mathematical audits.

I read `/Users/alec/Documents/Math/AGENTS.md` and the project's `PROJECT_BRIEF.txt`. I did not read the project's root `README.md`, `THEOREM_STATUS.md`, `RESEARCH_LOG.md`, existing complete-package reviews, review JSON, responses or prior verdicts. I did not use `list_agents`. The package and both Git repositories were left unchanged; the only authored artifact is this report. No individual was contacted.

Reviewed candidate files, relative to `/Users/alec/Documents/Math/openai_followon_sperner_complete_intersections`:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `manuscript/main.tex` | 15258 | `88bcd2d8c620011eca8732ce30cd77f3322ae993403cf45aff0fb93729f1cf4f` |
| `manuscript/references.bib` | 1094 | `67c7d887a32280a89bbcaa3cfa41e6bba3ddaff74276b736a1ca67384eec30f9` |
| `publication/README.md` | 5057 | `f6875a7152c785cb1ace811ff4be8da726d0c2a60ed6e357b1ecba05177ff20d` |
| `zenodo-deposit.json` | 2229 | `803ec40cf0aa3e25b567c3a6bdd343104344372f6fe6f9f21c5e17aad88185ac` |
| `publication/zenodo_upload_kit/files/paper.pdf` | 73479 | `ae0526dfe7442b63e9c3f4754c324970b0d4e8ccd15d85b6f9585ed3ee45a119` |
| `publication/zenodo_upload_kit/files/source.zip` | 9840 | `6a1ce33589e9811d253e2b2b094d00236cd5dca9925383d8694fbae26c629272` |
| `publication/zenodo_upload_kit/files/verification.zip` | 65205 | `367e1a3e0b3a214cf8dcec3d13c64ae0db8031c00b7183904cde8e3fd3cbd6ae` |

## Current primary priority and correction evidence

All live checks in this report were made on 2026-10-07 UTC. These observations bound what was checked; absence of a search hit is not proof of novelty.

1. HWW's [current arXiv record](https://arxiv.org/abs/1601.06928) lists only v1, submitted **2016-01-26 08:55:23 UTC**. The [versioned full text](https://arxiv.org/html/1601.06928v1) and [PDF](https://arxiv.org/pdf/1601.06928v1) were inspected. Definition 2 includes arbitrary ideals. Proposition 8 explicitly invokes Watanabe's Lemma 2.4 to reduce to graded ideals. Theorem 11 is conditional on EGH for the given complete intersection over a field. This establishes that the implication and all-ideal scope predate this candidate; candidate `main.tex:63–76` and `:139` correctly inherit them.

2. The [Crossref primary registry record for HWW](https://api.crossref.org/works/10.1090/proc/13347), retrieved directly by a read-only HTTP request, confirms three authors, the candidate's title, volume **145**, issue **4**, pages **1497–1503**, and online publication **2016-10-26**. Its DOI is [10.1090/proc/13347](https://doi.org/10.1090/proc/13347). The 2017 issue-year citation in `main.tex:292–297` is consistent with the journal issue; the online date is additional provenance, not a correction to that citation. The registry had an empty `relation` field and no `update-to` field. Its 2026-04-20 deposit timestamp is a metadata-update timestamp and does not establish a mathematical correction. Publisher full-text access returned HTTP 403, including the correct [published PDF URL](https://www.ams.org/journals/proc/2017-145-04/S0002-9939-2016-13347-9/S0002-9939-2016-13347-9.pdf). The final published full text was therefore not independently compared.

3. Targeted current searches on arXiv/AMS for the paper title/identifier with `correction`, `erratum` and `corrigendum` found no relevant correction. No later version is listed on the checked arXiv record. This supports the absence of a *listed* correction in these checked sources, not a universal claim that no correction exists.

4. The [Crossref record for Watanabe](https://api.crossref.org/works/10.2969/aspm/01110303) confirms the title *The Dilworth Number of Artinian Rings and Finite Posets with Rank Function*, author Junzo Watanabe, and pages **303–312**. The candidate's citation at `main.tex:299–302` is consistent. The directly inspected HWW reference chain supplies the volume/year information and identifies Lemma 2.4 as the graded-ideal reduction; this subaudit did not re-prove that lemma from the inaccessible Watanabe publisher text.

5. The exact upstream input is repository commit **adc7f1241b42e322a6451854ab7e4b4c146bf78a** in the read-only clone `/Users/alec/Desktop/math`. Both paper-specific `README.md` files supply OpenAI as author, September 23, 2026 as manuscript date, and the manuscript-specific BibTeX entries used in the candidate. I independently read those pinned citation files:

   - [Betti supplied citation](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/README.md), local path `preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/README.md:10`.
   - [EGH supplied citation](https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/README.md), local path `preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/README.md:10`.

   `manuscript/references.bib` preserves the supplied author/title/year/howpublished fields. The inline bibliography adds the exact audited commit. Its moving `main` PDF links are made reproducible by the recorded commit and pinned tree in the README/manifest; they do not silently imply that an uninspected later version was audited.

6. A fresh history-free internal child separately inspected the pinned family-200 source trees. The companion's `build/sections/01-introduction.tex:92` supplies the EGH Hilbert-function consequence, while its `build/sections/09-consequences.tex` discusses field scope, local cohomology and quadratic Cayley–Bacharach. The Betti paper's Corollary 1.2 supplies stronger EGH/Betti consequences. The child found no explicit Sperner/HWW/Dilworth/maximal-ideal-generator consequence in either manuscript tree after targeted source searches; a broader pinned-source search found only unrelated uses. This is bounded evidence that the note is not copying an explicit upstream Sperner corollary, and is not evidence of exhaustive novelty. Upstream proof soundness was outside this priority subaudit.

7. Both I and the child directly checked the [official public collection announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/), dated **October 6, 2026**. The [pinned initial commit](https://github.com/openai/math/commit/adc7f1241b42e322a6451854ab7e4b4c146bf78a) has timestamp **2026-10-06T14:58:50-07:00** and no parents. The child made live read-only remote-ref checks on October 7 UTC: current advertised `HEAD`/`main` still equal the exact pin, and no other heads or tags were advertised. No later official revision appeared on this checked main. GitHub REST history access was rate-limited, so rewritten/withdrawn history, external corrections and unpublished revisions remain unexcluded. September 23 is correctly presented by the candidate as a manuscript date, not verified public priority.

Current broader arXiv searches for the Sperner property of complete intersections and EGH returned the established conditional paper rather than a competing full new corollary. This cannot prove firstness, and the candidate makes no firstness claim. The justified classification is **an explicit explanatory consequence newly available from the cited upstream input**, not a new base-conjecture proof or a newly invented all-ideal theorem mechanism.

## Metadata, scope and rights checks

- The manuscript title, PDF title metadata, publication README title and deposit title agree exactly apart from the TeX line break. All state **standard graded Artinian complete intersections in characteristic zero**. The abstract/manifest specify arbitrary characteristic-zero fields and all ideals. The manuscript handles degree-one elimination and the empty/all-linear algebra, and expressly excludes Lefschetz, nongraded and unrestricted positive-characteristic conclusions. No scope inflation is visible in the metadata.
- The title is descriptive and unconditional; the abstract's immediate-corollary attribution and explicit input citation make the dependence clear. The mathematical reviewers must still verify that input before publication; a metadata audit cannot turn an asserted upstream theorem into an independently verified result.
- `main.tex:18`, PDF author metadata, README and manifest all identify **Alec Kriebel** only. The ORCID **0009-0001-9320-500X** matches the supplied instructions. There is no invented affiliation or coauthor. OpenAI is credited as the upstream author using its supplied citation, rather than being silently absorbed into Alec Kriebel's contribution.
- `main.tex:281–289`, README and manifest state extensive AI use, explicitly distinguish automated audits from conventional human review, disclose absence of conventional human refereeing, and make no formalization claim. PDF extracted text contains the same disclosure. The deposit is correctly typed `publication` / `preprint`.
- The publication date **2026-10-06** matches the manuscript date and the local audit/publication-candidate day. The PDF creation timestamp is **2026-10-06 23:00:33 PDT**, compatible with that date. This review makes no claim that publication has already occurred.
- The manifest lists exactly the three intended separately downloadable payload files. The related identifiers label HWW's DOI and the pinned upstream repository as `isDerivedFrom`, which is consistent with the stated dependency and attribution.
- Both archive `LICENSE` files are identical: SHA-256 **23c7b7147d919bb30e7d8f6e4769de044465e3bae3289c7428f6348757587b59**. They apply **CC BY 4.0** to the original note, code and project-authored verification material, retain third-party rights, and agree with `cc-by-4.0` in the manifest and README. No third-party manuscript/PDF/source-tree copy occurs in the inventoried archive file set. The scoped research-note bodies were not read, to preserve independence, so this finding is an inventory/declared-scope check rather than a legal audit of every quotation inside them.

## Exact archive inventories and consistency

`source.zip` has four members: `LICENSE`, `README.md`, `manuscript/main.tex`, `manuscript/references.bib`. Its manuscript and supplied bibliography are byte-identical to the reviewed working files. Its README is byte-identical to `publication/README.md`.

`verification.zip` has these 21 members:

```text
APPROACH_TABLE.md
DEPENDENCY_LEDGER.md
LICENSE
README.md
notes/companion_audit.md
notes/companion_checks.py
notes/downstream_proof.md
notes/lpp_audit.md
notes/lpp_box_tests.json
notes/lpp_box_tests.md
notes/lpp_box_tests.py
notes/picard_subaudit.md
notes/priority_audit.md
notes/root_dependency_check.md
receipts/build_scope.json
receipts/clean_reproduction.json
receipts/pdf_visual_check.json
receipts/pinned_sources.json
verification/hilbert_examples.json
verification/hilbert_examples.py
verification/reproduce.py
```

Its README matches `publication/README.md` byte for byte, and its LICENSE matches the source archive. Both archives have no duplicate member names and no absolute or parent-traversing member paths. Inventory and member hashes were computed directly; previous review/priority-note bodies and receipt verdicts were not used.

The deposited PDF was read for metadata and extracted text, not visually judged in this subaudit. It has five pages, the expected title, author and immediate-corollary subject metadata, and contains the same statement/attribution/disclosure as the reviewed TeX.

## Limitations and independence record

No actionable metadata/priority repair is required on the evidence inspected. There is no claim of exhaustive literature novelty, complete historical search, independent verification of upstream proofs, legal review of every supplement quotation, remote Zenodo-state inspection or publication authorization decision here.

The child accidentally caused a GitHub repository landing page to render the upstream root README. It disclosed the incident and excluded that text as evidence. All prohibited local project status/review/verdict files remained unread by both reviewers. This procedural exposure did not supply any prior candidate-review verdict or alter the evidence-based classification above, but is retained transparently.
