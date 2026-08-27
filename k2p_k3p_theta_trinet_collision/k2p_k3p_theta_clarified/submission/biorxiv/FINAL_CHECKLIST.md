# Final bioRxiv approval checklist

Do not approve the bioRxiv submission until every box is resolved. A posted
preprint is permanent and citable even if a later version corrects it.

## Manuscript freeze

- [ ] The canonical source is `combined-paper-clarified.tex`; no legacy parent
      paper or ZIP is in the upload set.
- [ ] Title, abstract, and main theorem have received final author approval.
- [ ] The rendered PDF contains no provisional/confidential language, stale
      submission-status claims, unresolved placeholders, or ambiguous figures.
- [ ] Author name, affiliation, correspondence information, ORCID, keywords,
      funding, competing interests, and code/data availability are complete.
- [ ] Biological relevance to evolutionary inference is explicit enough to
      satisfy bioRxiv's life-science scope.
- [ ] The bibliography and every internal/external link resolve.
- [ ] Version 2 is cited only for the removed K2P Lemma 5.6 and Corollary
      5.8; Version 3 is cited for the correction, ordering diagnosis, and open
      K2P/K3P questions.
- [ ] Every continuous-time claim is explicitly edgewise and does not imply a
      common generator, common rate ratio, molecular clock, or global timing.
- [ ] The non-tree-child scope and separation from strongly tree-child level-2
      JC results are explicit.
- [ ] The exact quartic theta **parameter** is distinguished from its globally
      character-relabeled
      K2P shared **distribution**; only the nearby submersion result is called
      observably genuine K3P.
- [ ] Zariski density is stated only in the effective Fourier ambient spaces
      and does not erase stochastic/continuous-time inequalities or tree
      invariants.
- [ ] The all-leaf theorem inserts one theta blob at one chosen internal vertex
      and is not presented as multi-blob composition or a genuine four-terminal
      blob result.

## Reproducibility freeze

- [ ] All exact verifiers pass from a clean checkout using the documented
      supported Python versions.
- [ ] Stored verification transcripts were regenerated from the release commit.
- [ ] All manuscript claims delegated to computation are explicitly bound to
      named certificate fields, row/column orderings, and verifier checks.
- [ ] The canonical manifest passes and covers every intended release file.
- [ ] `bash submission/build_release.sh --output-dir /absolute/empty/output-directory --commit k2p-k3p-theta-v1.2.2 --version 1.2.2`
      produces byte-stable archives and valid SHA-256 checksums.
- [ ] Both archives contain `RELEASE_PROVENANCE.txt` with the full release
      commit/version and `FILE_SHA256SUMS` with a passing hash for every
      committed file actually included in the archive.
- [ ] Neither archive contains `submission/biorxiv/`, unresolved metadata
      templates, author-only checklists, email warnings, or upload placeholders.
- [ ] A clean extraction of the archive builds the PDFs and passes the complete
      verifier suite.
- [ ] The exact 40-character release commit is recorded in the replay archive
      and the tag `k2p-k3p-theta-v1.2.2` resolves to that commit.

## Portal metadata

- [ ] Portal title and abstract exactly match the frozen PDF.
- [ ] Author spelling/order, affiliation, corresponding email, and ORCID are
      correct in the preview.
- [ ] Subject area selected: `<AUTHOR RECORD FINAL CHOICE>`.
- [ ] Result category selected: `<AUTHOR RECORD FINAL CHOICE>`.
- [ ] Funding/ROR and award data entered, or no-funding status confirmed.
- [ ] Competing-interest response confirmed.
- [ ] Versioned GitHub and/or permanent data/code URL entered.
- [ ] Any supplementary files open correctly and contain no local paths,
      credentials, caches, or legacy drafts.
- [ ] The portal preview preserves mathematical symbols and line breaks.

## Consequential author choices

- [ ] Intended journals/funders permit preprint posting.
- [ ] The manuscript has not already been accepted by a journal.
- [ ] bioRxiv distribution/reuse option selected deliberately and recorded here:
      `<CC BY / CC BY-NC / CC BY-ND / CC BY-NC-ND / CC0 / NO REUSE>`.
- [ ] If a Zenodo package will be deposited, its scope, license, release tag,
      metadata, and DOI are final; the deposit is the curated canonical subtree,
      not the whole `Math` monorepo.
- [ ] The author understands that approval creates a DOI and relinquishes
      control over the exact posting time; no embargo or scheduled release is
      expected.

## Post-posting checkpoint

- [ ] Record the bioRxiv DOI and version-specific URL in `CITATION.cff`, README,
      provenance, and Zenodo related identifiers.
- [ ] Confirm the displayed PDF, author metadata, license, supplementary links,
      and Data/Code links on the public bioRxiv page.
- [ ] Commit and push the DOI/status update without replacing or rewriting the
      release commit used for reproducibility.
