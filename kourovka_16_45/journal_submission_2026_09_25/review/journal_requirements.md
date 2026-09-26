# Archiv der Mathematik: current journal audit

Checkpoint: 2026-09-26T04:07:09+00:00 (2026-09-25 America/Los_Angeles).
Estimated completion of this requirements audit: **95%**. Official public requirements, template, and initial agreement are verified. Exact later upload labels remain unverified because reaching them requires accepting the author agreement. Submission eligibility is a separate unresolved issue, not a formatting issue.

## Critical decision

**Do not mark this manuscript ready to submit to Archiv until the AI authorship condition has been resolved honestly.** The live public author agreement states: “An article largely written by AI may not be submitted to this journal.” AI assistance with arguments or citations must be disclosed both in the manuscript and later in the form. This is stronger than a disclosure-only rule. The existing manuscript says its revision and verification were prepared with Codex, so the provenance requires substantive human assessment; removing a disclosure or paraphrasing automatically would not resolve eligibility. The agreement also bars simultaneous consideration and previously rejected submissions absent an invitation. No checkbox was accepted. [Current Step 0 agreement](https://ef.msp.org/submit/ems_adm)

## Submission route and scope

The journal's Springer home explicitly redirects **new** submissions to EMS, ahead of publication transfer in January 2027. The legacy Springer Editorial Manager/birkjour instructions must therefore not drive this package. [Springer transition notice](https://link.springer.com/journal/13)

Use [EMS journal page](https://ems.press/journals/adm), then [Submit](https://ems.press/journals/adm/submit), then [EditFlow new submission](https://ef.msp.org/submit/ems_adm), which currently resolves to `https://ef.msp.org/submit_new.php?j=ems_adm`.

The EMS scope calls for short research for a broad mathematical readership, typically no more than ten pages. This precise counterexample fits the subject and length aspiration well; fit is conditional on mathematical review, priority, and policy eligibility, and is not an acceptance prediction. [Current scope](https://ems.press/journals/adm)

## Verified initial submission requirements

Initial submission uses a PDF. Required metadata include all authors' names, emails and complete mailing addresses; corresponding author; MSC2020 classifications; and keywords. The page directs algebra submissions to managing editor **Gabriele Nebe**, who allocates a handling editor; a preferred subject editor may be indicated. Review is single blind. Source files and macros plus PDF are requested after acceptance, using the EMS template. There are no author charges/APCs under the journal's Launch to Open model. [Journal-specific instructions](https://ems.press/journals/adm/submit)

No cover letter, reviewer list, anonymized PDF, separate title page, mandatory abstract word range, or exact supplement upload label was established from the public instructions. A concise optional statement of significance can be prepared only if allowed by the user's independent-research policy; do not claim it is a required upload. The source bundle is for reproducibility and possible later production, not a verified mandatory initial upload.

## Format and template

The actual current [template ZIP](https://ems.press/files/standalone/journals-template/ems-journal-template.zip) is retained in `sources/journal/`; it explicitly supports `journal=AdM`. Use the supplied author, affiliation, MSC and keyword commands. The style's native layout is 170 × 240 mm, 357 pt text width, 10 pt body text and 42 lines. The current nine-page letter-size manuscript therefore needs a fresh page count in this template; final publisher pagination can still vary. See `sources/journal/TEMPLATE_PROVENANCE.md` for hashes and limited license findings.

EMS asks for structured LaTeX without custom page layout or forced spacing/page breaks. The abstract should be self-contained, with inline rather than displayed formulae. Acknowledgments and funding precede the bibliography. References use numerical labels, alphabetic ordering, and every item must be cited. Standard theorem environments are supported; use `definition` rather than `remark` theorem style. [Author formatting guidance](https://ems.press/author-guidelines)

## Disclosure and reproducibility

EMS accepts non-peer-reviewed preprints as original submissions. It expects complete proofs and shared code for computer-assisted proof steps; positive funding and conflicts must be declared. Negative conflict declarations are not required. AI tools enhancing mathematical content require precise disclosure upon submission that will appear in the published work. The journal homepage expressly adopts this code even though the code's older appendix does not yet list the transferring title. None of these general provisions overrides the stronger current form restriction above. [EMS ethics code, §§1.1–1.7](https://ems.press/code-of-conduct)

Open access for 2027 depends on institutional subscriptions meeting the Launch to Open target by 31 January 2027; it is not guaranteed at submission. When achieved, journal articles receive CC BY 4.0. Immediate sharing of the author accepted manuscript remains available under the model. [Launch to Open](https://ems.press/open-access/launch-to-open)

## Recommended classifications and subject handling

Use primary **20B05** (finite permutation groups), secondary **20D30** (subgroup series/lattices) and **20D60** (arithmetic/combinatorial finite-group problems). These are recommendations based on the manuscript; codes were verified against [AMS MSC2020](https://mathscinet.ams.org/msc/msc2020.html?t=20-08).

Suggested keywords: finite permutation group; minimal base; independent set; subgroup lattice; Kourovka Notebook.

If the form permits a subject-editor suggestion and there is no relevant personal conflict, **Colva Roney-Dougal** is a strong subject match: she is on the [current board](https://ems.press/journals/adm/editorial-board) and works on finite groups and permutation bases, with recent publications directly in that area. [Official university profile](https://www.st-andrews.ac.uk/mathematics-statistics/people/cmr1/). This is an optional subject-fit recommendation, not an instruction to contact her and not a referee nomination. Nobody was contacted.

## Presentation advice based on the current manuscript

Keep the named problem, explicit order-100920 group, sharp values, and structural proof as the main narrative. Define inclusion-minimal bases immediately to prevent confusion with ordered irredundant bases. Preserve the distinction between faithful and arbitrary actions and the nonnormal central-in-the-complement obstruction. Shorten the software-validation narrative into a concise reproducibility paragraph, placing run commands, historical optimizer details, counts and audit history in the supplement. The characteristic-11 boundary example is mathematically useful but can move to the supplement if needed to meet ten pages. Remove the forced page break before the author statement. Alphabetize the bibliography and replace the long search-priority disclaimer with a short dated statement of notebook status. Retain specific and truthful AI disclosure; do not treat presentation edits as curing the eligibility condition.

## Exact remaining gaps

1. Human provenance assessment against the current form's AI authorship restriction. If incompatible, recommend a different journal with an applicable policy; do not submit here by omission.
2. Final manuscript page count in the untouched `AdM` style, including references and disclosures.
3. The author must supply/verify a complete postal address, email, funding/conflict status, originality/exclusivity and prior-submission history.
4. Later form labels, file-size limits and supplement slots were not publicly visible without accepting the author agreement. Instructions must label these as conditional, not invent them.

No external person was contacted, no author agreement accepted, and no journal submission initiated. No manuscript was edited by this audit.
