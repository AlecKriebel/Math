# PLOS Computational Biology submission checklist

> **DRAFT — NOT SUBMITTED.** No journal portal has been completed, no files
> have been uploaded, and no editor or reviewer has been contacted by this
> work. Only the human author may make declarations, enter personal data,
> choose reviewers/editors, accept publication terms, or submit.

This checklist reflects the PLOS requirements summarized for this project and
the current local manuscript. The human should recheck the live journal and
portal instructions immediately before submission because forms and file
requirements can change.

## 1. Submission identity and article type

- [ ] **Journal:** human confirms PLOS Computational Biology.
- [ ] **Article type:** human confirms Research Article.
- [ ] **Title:** *No universal death–birth amplifier on a finite weighted
      population structure*.
- [ ] Human confirms the title entered in the portal exactly matches the final
      manuscript and code archive.
- [ ] Human selects the appropriate editorial subject area(s).
- [ ] Human enters keywords. Candidate terms for human review:
      `evolutionary graph theory`, `fixation probability`, `death–birth
      updating`, `Moran process`, `amplifiers of selection`, `weighted directed
      networks`.
- [ ] Human confirms whether any prior journal inquiry or related submission
      must be disclosed.

## 2. Author and portal fields — human only

- [ ] Legal author name.
- [ ] Affiliation and country.
- [ ] Corresponding-author email and any required postal details.
- [ ] ORCID entered by the human; this package intentionally leaves it blank.
- [ ] Every author has approved the final manuscript and submission. The
      current manuscript lists one author; human confirms that authorship is
      complete and compliant.
- [ ] CRediT contribution roles entered and approved by the human. Possible
      single-author roles to review—not declarations made by this package—are
      Conceptualization, Formal analysis, Methodology, Software, Validation,
      Visualization, Writing – original draft, and Writing – review & editing.
- [ ] AI systems are not listed as authors.

## 3. Abstract and author summary

- [x] An abstract draft is available in `publication/abstract.md` and matches
      the current manuscript (159 words under the LaTeX extraction and 164
      under this package's Markdown extraction).
- [x] A plain-language author-summary draft is available in
      `publication/author_summary.md`.
- [ ] Human confirms the live abstract limit and approves final wording.
- [ ] Human confirms the current Author Summary length requirement and approves
      a summary that is accessible, citation-free, and avoids unexplained
      specialist shorthand.
- [ ] Portal text is compared character-for-character with the final manuscript
      versions after any edit.

## 4. Manuscript content and formatting

- [ ] Human approves the final title page, author line, affiliation, and date.
- [ ] Mathematical notation and the source-to-target weight convention are
      consistent throughout.
- [ ] The fixed-graph quantifier and the open reversed asymptotic quantifier are
      stated distinctly in the abstract, main text, summary, and cover letter.
- [ ] Prior and new results are clearly separated; the Tkadlec et al.
      noncomplete-support theorem is not presented as new.
- [ ] The unrestricted weighted K4 and broader fixed-fitness/growing-population
      questions remain labeled open.
- [ ] Figure 1 and its legend are understandable without relying on color.
- [ ] Human checks whether the portal requires separately uploaded figure files
      rather than the current TikZ-generated embedded figure, then exports an
      accepted format/resolution if required.
- [ ] Tables, equations, and references render correctly in the uploaded PDF.
- [ ] Human confirms whether line numbering, page numbering, section order, a
      PLOS template, or a specific initial-submission layout is currently
      required.
- [ ] All references contain complete metadata and resolve correctly.
- [ ] The manuscript contains no unsupported priority claim; novelty remains
      qualified by the targeted audit.

## 5. Required declarations — human confirmation required

- [ ] **Competing interests:** human enters the exact portal declaration and
      adds matching manuscript text if required.
- [ ] **Funding/financial disclosure:** human lists every funder and grant, or
      confirms the journal-compliant no-specific-funding wording. This package
      does not infer funding status.
- [ ] **Funder role:** human states the funder's role where the portal requires
      it.
- [ ] **Author contributions:** human approves the CRediT statement.
- [ ] **Ethics:** based on the manuscript, no human participants, animal
      subjects, clinical data, or empirical personal data are involved; human
      selects and confirms the appropriate not-applicable portal answers.
- [ ] **Competing manuscripts/exclusive consideration:** human confirms the
      manuscript is not under consideration elsewhere and supplies any related
      manuscript information requested by the portal.
- [ ] **Preprint/public posting:** human states whether a preprint or public
      manuscript version exists and supplies its link/status.
- [ ] **AI assistance:** retain a transparent disclosure consistent with
      `paper/main.tex`; human checks the current PLOS placement and wording
      requirement.
- [ ] **Copyright/open-access terms and charges:** human reviews and accepts the
      journal's current license and publication-fee arrangements.

## 6. Data and code availability

- [x] No empirical data are used.
- [x] Development repository remote verified as
      <https://github.com/AlecKriebel/Math>.
- [x] Reproduction code, exact certificates, audit materials, manuscript source,
      pinned SymPy requirement, Make target, and MIT License exist locally.
- [x] Clean versioned publication snapshot created and verified at
      <https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>.
- [x] The manuscript's release claim and the public tag agree.
- [x] The release URL is consistent across the current availability drafts.
- [x] Zenodo version DOI <https://doi.org/10.5281/zenodo.21753405> resolves to
      version `universal-db-obstruction-v1.0.0` and links to the exact tag.
- [x] Confirm the scoped GitHub release assets are public and contain no
      unrelated or sensitive material; the separate automatic Zenodo snapshot
      is transparently identified as a public monorepository archive.
- [ ] Use the final wording in `publication/data_code_availability.md` only
      after these checks pass.

## 7. Reproducibility and source freeze

- [x] Start from a clean source archive of the proposed release.
- [ ] Install the pinned Python dependency in a fresh environment.
- [ ] Install/document the required Tectonic or LaTeX compiler.
- [x] Run `make paper1` successfully and retain the complete output.
- [ ] Run `make test`, `make verify`, `make directed`, `make triangle`,
      `make n4`, and `make phase3-check` as needed for diagnostic isolation.
- [x] Confirm no generated `.venv`, cache, temporary, or developer-only files
      are included in the archive.
- [x] Record source hash, PDF hash, code-release identifier,
      Python version, SymPy version, and document-compiler version.
- [x] Rebuild the final PDF and inspect every page visually.
- [x] Scan the final build log for errors, undefined references, overfull text,
      or missing assets.
- [ ] Record the final commit hash in the journal portal or audit record if
      requested.

## 8. Audit status

- [x] Internal exact and adversarial audits exist for the main theorem and
      finite-family certificates.
- [x] A final manuscript PDF currently exists.
- [ ] Human decides whether to obtain an external specialist audit.
- [ ] If obtained, freeze hashes and use
      `publication/external_audit_checklist.md`.
- [ ] Resolve every audit finding against the exact frozen source.
- [ ] If no external audit occurs, retain the manuscript's explicit statement
      that none has occurred.
- [ ] Do not describe AI-assisted hostile audits as external peer review.

## 9. Files to prepare for the portal

- [x] Final manuscript PDF.
- [x] Editable LaTeX source and support files in the release archive.
- [ ] Separate figure file(s), if required by the live portal.
- [ ] Figure legend(s), if entered separately.
- [ ] Supporting-information files and legends, if the code archive is also
      supplied as Supporting Information.
- [ ] Final abstract and Author Summary portal text.
- [ ] Final Data Availability statement.
- [ ] Final Funding, Competing Interests, Author Contributions, AI-use, ethics,
      and preprint declarations.
- [ ] Cover letter approved by the human.
- [x] Versioned public code/archive URL.
- [x] Zenodo version DOI for the journal record.

## 10. Cover letter and editorial selections

- [x] A cover-letter draft exists at `publication/cover_letter.md`.
- [ ] Human removes all bracketed placeholders and verifies every declaration.
- [ ] Human chooses any preferred editor, reviewer suggestions, or exclusions
      directly in the portal if requested. This package deliberately does not
      prepare specialist outreach or contact anyone.
- [ ] Human confirms no confidential information appears in the cover letter.

## 11. Final human sign-off

- [ ] I have read every submitted file and portal field.
- [ ] The title, claims, author list, declarations, and archive links agree.
- [ ] All personal information and ORCID entries are accurate.
- [ ] All coauthor approvals are complete, if the author list changes.
- [ ] The code/archive DOI resolves and reproduces the frozen submission.
- [ ] I understand that the manuscript is currently **not submitted**.
- [ ] I, the human author, authorize the final portal submission.

Until every blocker and declaration above is resolved by the human, this
package is submission support only and must not be represented as a completed
journal submission.
