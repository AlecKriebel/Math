# bioRxiv submission checklist

> **DRAFT — NOT POSTED.** Only the human author may enter private metadata,
> accept terms, choose a license, or press the submission button.

## Scientific and document checks

- [ ] Confirm the final PDF title, author, abstract, theorem statements, and
      limitation statements match `BIORXIV_METADATA.md` exactly.
- [ ] Confirm the submission remains biological research in evolutionary
      dynamics and is presented as a research article with new mathematical
      results and reproducible exact outputs.
- [ ] Select **New Results** as the article type and **Evolutionary Biology**
      as the subject category.
- [ ] Upload the final manuscript PDF and the enclosing reproducibility
      package if accepted by the live portal; the inner source archive alone
      does not contain the certified package-root launcher.
- [ ] Confirm all fonts render, hyperlinks work, and no tracked-change or
      internal-review material appears in the PDF.
- [ ] Confirm the abstract and keywords copied into the portal are identical
      to the frozen manuscript.

## Author-only fields and choices

- [ ] Confirm `me@aleckriebel.com` is the intended corresponding email.
- [ ] Replace `[[POSTAL_ADDRESS]]` everywhere it occurs if the portal asks for
      an address or residence.
- [ ] Confirm the author name, Independent Researcher affiliation, and ORCID.
- [ ] Select and approve the preprint license after reading the live options.
- [ ] Read and accept the current bioRxiv terms and screening declarations.
- [ ] Confirm that no simultaneous journal consideration conflicts with the
      intended journal workflow.

## Integrity and provenance

- [ ] Disclose the public software snapshot at DOI
      `10.5281/zenodo.21753405`, which contains the earlier fixed-graph
      obstruction manuscript and code superseded by this consolidated paper.
- [ ] If requested, disclose DOIs `10.5281/zenodo.21850042` and
      `10.5281/zenodo.21852072` as related **software archives** for the
      separate simultaneous-amplification workstream, not as prior
      publications of this manuscript.
- [ ] Confirm that any public project webpage containing an earlier draft is
      disclosed wherever the portal asks about prior online dissemination.
- [ ] Use the substantive AI-assistance statement in `DECLARATIONS.md` and
      verify it against the live policy.
- [ ] Confirm no third-party copyrighted figure or table requires permission.
- [ ] Confirm no human participants, animals, clinical material, personal
      data, or empirical dataset are involved.

## Reproducibility and freeze

- [ ] Run `../release_bundle.sh` and retain the printed archive SHA-256.
- [ ] Supply the frozen enclosing reproducibility package containing
      `complete_graph_extremality_db_source_and_certificates.tar.gz`, its
      detached checksum, package verifier, and certified launcher.
- [ ] Run `run_all_referee_checks.sh` from the reproducibility-package root;
      do not substitute plain `shasum -c` or direct internal bootstrap status.
- [ ] Rebuild and visually inspect the deterministic manuscript PDF.
- [ ] Create a versioned public release for the present consolidated package
      only after the author approves the frozen files.
- [ ] If a new archival DOI is created later, add it to a subsequent manuscript
      and preprint-record version; do not reuse a prior DOI.
- [ ] Human author performs the final submission and retains the confirmation.
