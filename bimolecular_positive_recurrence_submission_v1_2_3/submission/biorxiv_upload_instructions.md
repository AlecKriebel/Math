# bioRxiv upload instructions — Version 1.2.3

This is an operational checklist for the human author. The release process
does not create a bioRxiv account, upload files, approve a submission, register
a DOI, or communicate externally.

## 1. Final eligibility check

Before opening the submission:

- confirm that the manuscript is unpublished and has not been formally
  accepted by a journal;
- confirm author consent to deposit (one author: Alec Kriebel);
- confirm that no version is on another preprint server;
- disclose the public repository versions if the form asks about prior online
  material; and
- recheck the current bioRxiv submission guide and any live form instructions.

Do not submit this version to arXiv while the bioRxiv submission is pending or
after it posts. If bioRxiv declines the paper as outside scope, arXiv remains
the fallback.

## 2. Upload exactly these files

Upload the two files separately:

1. **Main manuscript:** `manuscript/main_biorxiv.pdf`
2. **Supplementary material:** `manuscript/supplementary_note.pdf`

Expected SHA-256 values for the sealed Version 1.2.3 files:

- `main_biorxiv.pdf`:
  `99274c779312a5a0ce87211a3e5ecef505578373ffecdc06034785b25f384315`
- `supplementary_note.pdf`:
  `8f5dca8146df45b96fb6ab61ef5790559aeb847f49243b1d0a03d97368864fb1`

Use one main-manuscript file and one supplement. There are no separate figure
files. Do not upload the release ZIP, manifest, verifier report, LaTeX source,
audit files, or preservation records as supplementary material; the tagged
repository provides those materials.

## 3. Submission selections

- **Number of authors:** 1
- **Result/article category:** New Results
- **Subject area:** Systems Biology
- **Other preprint server:** No
- **License:** No reuse/adaptation without permission

The license selection matches `LICENSE.md`. Choose a Creative Commons license
only after deliberately changing the deposited-version license. A later
license update can move from a more restrictive option to a less restrictive
one, but not back to a more restrictive option.

## 4. Copy-ready metadata

Use `submission/biorxiv_metadata.md` as the canonical copy-ready source. Enter
the following core fields exactly.

**Title**

Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible
Stochastic Reaction Networks

**Author**

Alec Kriebel

**Affiliation**

Independent researcher

Complete any required country, address, or profile fields truthfully; do not
invent an institutional affiliation.

**Corresponding-author email**

`me@aleckriebel.com`

**ORCID**

`0009-0001-9320-500X`

**Abstract**

Paste the abstract from `submission/biorxiv_metadata.md` verbatim. It is
synchronized with the bioRxiv PDF.

**Keywords, if requested**

stochastic reaction network; systems biology; chemical master equation;
positive recurrence; mass-action kinetics; weak reversibility; continuous-time
Markov chain; Foster--Lyapunov method

The public instructions do not state a numeric keyword limit. Obey any counter
shown by the live form.

**Competing interests**

The author declares no competing interests.

**Funding fields**

Select no funder and enter no grant number. Do not invent a Research
Organization Registry entry. The manuscript statement is: “This research
received no specific grant from any funding agency in the public, commercial,
or not-for-profit sectors.”

**Data statement**

No empirical or third-party dataset was used. The mathematical proof is
universal. Deterministic code outputs and exact finite calibration cases
accompany the paper, but finite computation is not a substitute for proof.

**Code/supporting-materials URL**

<https://github.com/AlecKriebel/Math/tree/bimolecular-positive-recurrence-v1.2.3/bimolecular_positive_recurrence_submission_v1_2_3>

**Ethics**

Not applicable. The work involves no human participants, animals, patient
information, identifiable data, or biological specimens.

**Generative AI**

The required disclosure is already in the manuscript. If the live form also
shows an AI field, enter: “Generative-AI systems materially supported
mathematical exploration, counterexample search, verification, drafting, and
adversarial review. The manuscript identifies the systems, dates, uses,
checking, and author responsibility; no AI system is an author.”

**DOI before final approval**

Do not invent or enter a repository tag as a DOI. bioRxiv generates the
preprint DOI automatically when the author gives final approval. New records
use prefix `10.64898`; the approval date forms part of the suffix.

## 5. Optional scope note

If the form provides a cover-note or screening-note field, use the concise
text in `submission/biorxiv_screening_note.md`. Do not paste it into an
unrelated field. The manuscript is mathematical but directly concerns
chemical-master-equation models for low-copy-number biochemical networks;
scope screening remains discretionary.

## 6. Portal sequence and proof approval

The documented submission sequence is:

1. manuscript metadata;
2. author information;
3. file-upload metadata;
4. supplemental-file upload;
5. manuscript-file upload;
6. submission approval and proofing; and
7. confirmation.

Uploading files alone does not submit the manuscript. On the proof page:

- compare the title, abstract, author spelling/order, affiliation,
  corresponding email, category, and subject area against the main PDF;
- open and visually inspect the generated main PDF and separately posted
  supplement;
- confirm the license, competing-interest response, funding fields, and
  code/materials URL;
- approve every section and the manuscript conversion; and
- perform the final approval action only after every item is correct.

Save the acknowledgment and manuscript identifier, record the DOI if shown,
and save a copy or screenshot of the final entered metadata. Confirm that the
submission appears in the Author Area queue. Screening typically
takes 24--48 hours, but may take longer; bioRxiv does not provide a requested
posting time or embargo.

## 7. Submission-day literature and date check

Immediately before final approval, recheck:

- arXiv:2409.05340;
- the ConStRAINeD overview and item 16; and
- whether the announced five-author two-species manuscript has become public.

If approval occurs after 17 August 2026 or the public status changes, stop and
prepare a successor release with matching manuscript, bibliography, metadata,
access dates, PDFs, and hashes. Do not mutate the Version 1.2.3 tag.

## 8. After posting

Verify the posted record's:

- DOI and canonical URL;
- title, author, affiliation, and ORCID;
- abstract, Systems Biology classification, and New Results label;
- competing-interest and funding display;
- license and code/materials link; and
- main PDF, supplementary note, posting date, and version number.

Allow up to 24 hours for DOI resolution and recheck the generated HTML/XML and
extracted metadata after 24--48 hours. Then record the DOI and posting date in
a new successor release, the future journal cover letter, repository page, and
journal metadata. Do not rewrite the immutable Version 1.2.3 release.

Revisions use the same DOI and earlier versions remain accessible. If
supplemental files are revised, the article must accompany them. A posted
record cannot ordinarily be removed; withdrawal leaves a public record.

## Official guidance rechecked 16 August 2026

- Submission guide: <https://www.biorxiv.org/submit-a-manuscript>
- Submission-system help: <https://submit.biorxiv.org/help/submissionhelp.dtl>
- Scope and categories: <https://www.biorxiv.org/about-biorxiv>
- FAQ: <https://www.biorxiv.org/about/FAQ>
- Screening: <https://connect.biorxiv.org/news/2022/06/13/screening_procedures>
- Funder fields: <https://connect.biorxiv.org/news/2025/09/04/funder_information>
- DOI assignment: <https://connect.biorxiv.org/news/2025/11/18/preprint_dois>
- License updates: <https://connect.biorxiv.org/news/2026/01/07/license_update_howto>
