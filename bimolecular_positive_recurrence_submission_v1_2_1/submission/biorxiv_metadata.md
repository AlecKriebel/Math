# bioRxiv submission sheet

This sheet prepares Version 1.2.1 for bioRxiv. It is not evidence of screening,
acceptance, posting, or DOI assignment.

## Submission selections

- **Subject area:** Systems Biology
- **Result type:** New Results
- **Main file:** `manuscript/main_biorxiv.pdf`
- **Supplementary file:** `manuscript/supplementary_note.pdf`
- **License:** select **No reuse/adaptation without permission** to remain
  consistent with `LICENSE.md`. Choose a Creative Commons option only after
  deliberately changing the deposited-version license.
- **Other preprint server:** No. Do not submit this version to arXiv before or
  while pursuing bioRxiv; bioRxiv does not post manuscripts already present on
  another preprint server.

Do not upload the complete preservation ZIP as supplementary material. The
tagged repository supplies code, source, reports, manifests, and provenance.

## Core metadata

**Title:**
Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible
Stochastic Reaction Networks

**Author:**
Alec Kriebel

**Affiliation:**
Independent researcher

**Corresponding author:**
Alec Kriebel, <me@aleckriebel.com>

**ORCID:**
<https://orcid.org/0009-0001-9320-500X>

**DOI:**
None before posting. A repository tag or commit is not a preprint DOI.

**Abstract:**

Weak reversibility is conjectured to imply positive recurrence for stochastic
mass-action systems. We prove the conjecture for finite bimolecular networks with one
linkage class, removing the earlier requirement that every species occur in a
pure unary or pure-double complex. Under weak reversibility, the states
reachable from each initial population form a closed communicating class.
Under the additional one-linkage and bimolecular hypotheses, for every positive
rate vector each nonabsorbing reachable class is positive recurrent, whereas
an absorbing singleton carries its point-mass law; consequently every
reachable class has a unique stationary probability distribution. The closure
statement follows by lifting directed return paths of complexes to population
states. For recurrence, the proof marks the target of the most recently fired
channel and applies a log-factorial potential after subtracting that target.
Its increment is exactly the logarithm of a target/source falling-factorial
ratio, so following the carried target has zero reward. Finite target-following
paths propagate the negative drift of a rare terminal source, while a
normalized-log compactification and a bimolecular top-complex alternative rule
out all other divergent sequences. The same return-cycle construction recovers
nonexplosion directly. Multiple linkage classes and molecularity above two
remain open.

**Keywords:**
stochastic reaction network; systems biology; chemical master equation;
positive recurrence; mass-action kinetics; weak reversibility; continuous-time
Markov chain; Foster--Lyapunov method

**Competing-interest statement:**
The author declares no competing interests.

**Funding statement:**
This research received no specific grant from any funding agency in the public,
commercial, or not-for-profit sectors.

## Scope and research-material declarations

**Life-science relevance:**
The paper studies stochastic mass-action continuous-time Markov chains used for
low-copy-number biochemical reaction networks. It proves a rate-independent
structural criterion for stationary molecule-count laws. Weak reversibility
makes the population set reachable from any initial state a closed
communicating class; under the additional one-linkage and bimolecular
hypotheses, every such class has a unique stationary probability law. No claim
is made that all biochemical models satisfy these restrictions.

**Data:**
No empirical or third-party dataset was used. The mathematical proof is
universal. Deterministic code outputs and exact finite calibration cases
accompany the paper, but finite computation is not a substitute for proof.

**Code and supporting materials:**
The tagged Version 1.2.1 package contains the standalone verifier, tests,
canonical output, release manifest, manuscript source, supplementary note,
and reproducibility record:
<https://github.com/AlecKriebel/Math/tree/bimolecular-positive-recurrence-v1.2.1/bimolecular_positive_recurrence_submission_v1_2_1>.

**Ethics:**
Not applicable. The work involves no human participants, animals, patient
information, identifiable data, or biological specimens.

**Generative-AI use:**
The manuscript includes a three-paragraph reader-facing note. Full system,
model, date, access-route, use, checking, and responsibility details through 16
August 2026 are recorded at
<https://github.com/AlecKriebel/Math/blob/bimolecular-positive-recurrence-v1.2.1/bimolecular_positive_recurrence_submission_v1_2_1/supplement/ai_use_full_statement.md>.
No AI system is an author.

## Prior-online status and permanence

Repository versions 0.3, 1.0, 1.1, 1.2, and 1.2.1 are publicly accessible as
unrefereed author manuscripts. No version has been posted to another formal
preprint server. Disclose the repository copies if the interface asks about
prior online text or overlap.

A posted bioRxiv version is citable and cannot ordinarily be removed. Revisions
before journal acceptance should be submitted as new versions of the same
bioRxiv record. Post only before journal acceptance.

## Screening risk

bioRxiv permits mathematical work only when it has direct life-science
relevance and describes its service as disseminating research articles with
new data. This paper has direct systems-biology model relevance and a new
theorem with exact result outputs, but no empirical dataset. Screening remains
a genuine judgment. If bioRxiv declines it as primarily mathematical, use
arXiv as the alternative rather than posting to both servers.

## Submission-day consistency check

Before completing the form, confirm that the entered title, author,
affiliation, abstract, competing-interest statement, funding statement, and
AI disclosure agree exactly with the uploaded PDF. Preview both the main PDF
and the separately posted supplement.

Recheck arXiv:2409.05340, ConStRAINeD item 16, and whether the announced
two-species manuscript has appeared. If uploading after 16 August 2026,
update the manuscript date and all ``as of'' and access dates, then rebuild.

## Primary policies rechecked 16 August 2026

- bioRxiv submission guide: <https://www.biorxiv.org/submit-a-manuscript>
- bioRxiv scope, categories, permanence, and licensing:
  <https://www.biorxiv.org/about-biorxiv>
- bioRxiv FAQ: <https://www.biorxiv.org/about/FAQ>
- bioRxiv screening procedures:
  <https://connect.biorxiv.org/news/2022/06/13/screening_procedures>
