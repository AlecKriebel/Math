# bioRxiv submission checklist

> **DRAFT — NOT POSTED.** Only the human author may enter private metadata,
> accept terms, choose a license, or press the submission button.

## Scientific and document checks

- [ ] Confirm the final PDF title, author, abstract, theorem statements, and
      limitations agree with `BIORXIV_METADATA.md`.
- [ ] Select **New Results** as the article type and **Evolutionary Biology**
      as the subject category.
- [ ] Confirm that the submission is presented as evolutionary-dynamics
      research with new mathematical results and reproducible exact outputs.
- [ ] Upload the final manuscript PDF and any supporting archive accepted by
      the live portal.
- [ ] Confirm fonts, mathematics, hyperlinks, and the diagram render correctly
      and no internal-review or tracked-change material appears.
- [ ] Confirm the abstract and six keywords copied into the portal are
      identical to the frozen manuscript.

## Author-only fields and choices

- [ ] Confirm `me@aleckriebel.com`, the author name, Independent Researcher
      affiliation, and ORCID.
- [ ] Replace `[[POSTAL_ADDRESS]]` in any private cover-letter copy or portal
      field that requests it.
- [ ] Read and choose among the live preprint-license options.
- [ ] Read and accept the current bioRxiv terms and screening declarations.
- [ ] Confirm the journal workflow and any concurrent-preprint disclosure
      comply with the live policies.

## Integrity and provenance

- [ ] Disclose DOI `10.5281/zenodo.21852072` as the public v1
      **source/software archive** containing an earlier manuscript version;
      do not call it the DOI of the present revision.
- [ ] Disclose DOI `10.5281/zenodo.21850042` as the superseded
      **source/software archive** for the earlier `R_sim>=3/2` construction.
- [ ] If asked about related work, disclose Paper I separately as described in
      `PROVENANCE_AND_RELATED_RELEASES.md`.
- [ ] Confirm the public project webpage and any earlier manuscript draft are
      disclosed wherever the live portal requests prior online versions.
- [ ] Approve the substantive AI-assistance statement against the live policy.
- [ ] Confirm that no empirical data, participants, animals, clinical
      material, personal data, or third-party copyrighted figures are used.

## Reproducibility and freeze

- [ ] Run `../release_bundle.sh` and retain the printed archive SHA-256.
- [ ] Verify the internal `MANIFEST.sha256` after fresh extraction.
- [ ] Run `bootstrap_replay.sh` from the extracted copy.
- [ ] Rebuild and visually inspect every page of the deterministic PDF.
- [ ] Create a new versioned public deposit only after the author approves the
      frozen package.
- [ ] Add a new persistent identifier to the manuscript and portal metadata
      only after it exists; never reuse a predecessor DOI.
- [ ] Human author performs the final submission and retains confirmation.
