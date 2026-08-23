# bioRxiv upload map

Verified against bioRxiv's official **Submission Guide**, **FAQ**, and
**Submission Help** pages on 2026-08-22:

- https://www.biorxiv.org/submit-a-manuscript
- https://www.biorxiv.org/about/FAQ
- https://submit.biorxiv.org/help/submissionhelp.dtl

The official guide says that a single PDF containing text and figures is the simplest main upload, supplemental material should be separate, LaTeX should be converted to PDF before submission, article categories include New Results, and the author must select a distribution/reuse option. The official scope page lists Evolutionary Biology as a subject category. Portal fields can change; recheck both official pages immediately before submission.

## Short answer: what goes where

**Yes: publish the complete verifier/certificate archive at Zenodo first.**
The manuscript and capsule must cite an issued, publicly resolving DOI and the
exact downloaded archive must pass authentication before the bioRxiv
submission is approved.

bioRxiv should receive the main PDF, reader supplement, and the small verifier
entry-point ZIP.  The official help pages permit supplemental files in a wide
range of formats and post them as submitted, so attaching the ZIP is
appropriate.  The ZIP is deliberately small but functional: it identifies and
checksums the canonical archive and contains the download authenticator and
reviewer entry points.  The complete 94 MB proof archive remains on Zenodo,
whose DOI, versioning, manifest, and checksums make it the authoritative proof
object.  Uploading the same full archive to bioRxiv as a redundant mirror is
possible if the live portal accepts its size, but is not required or
recommended; if done, it must be the identical Zenodo-authenticated bytes and
must be labelled as a mirror, not a second authoritative release.

## Proof-archive gate

Before opening the bioRxiv portal, upload the sealed DOI-bearing assets to the
existing Zenodo draft and publish it.  The reserved DOI is already embedded;
do not rerun DOI finalization or rebuild unless an artifact changes.  From the
project root, require:

```bash
(cd biorxiv_submission && shasum -a 256 -c SHA256SUMS)
python reproducibility/verify_submission_source_archives.py
python reproducibility/verify_certificate_zenodo_release.py /path/to/downloaded/archive.tar.gz
```

The last command must authenticate the bytes downloaded from the public DOI,
not merely find a matching URL string.

## Portal sequence

1. **Main manuscript:** upload `Strong_Tree_Childness_Sharp_Level2_JC.pdf` as the article PDF.
2. **Supplementary material:** upload `Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`.
3. **Verifier entry points:** upload `Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip` as supplementary code (or supplementary material if the portal has no code-specific type). It is a navigation capsule containing the Zenodo archive identity, checksum, runtime requirements, minimal theorem map, and a download verifier. The complete proof object remains at Zenodo.

   This split is intentional: Zenodo supplies the single persistent,
   DOI-citable, versioned and checksummed copy of the load-bearing proof
   archive, while the small bioRxiv attachment makes that object immediately
   discoverable.  Do not upload a second authoritative copy of the complete
   archive to bioRxiv unless the portal specifically requires it.
4. **Optional source supplement:** `Strong_Tree_Childness_Sharp_Level2_JC_source.zip` contains LaTeX, BibTeX, TikZ sources, and deterministic build instructions. bioRxiv's guide permits LaTeX source as supplemental material but requires the rendered PDF as the main article.
5. **Title and abstract:** paste the exact fields from `BIORXIV_METADATA.md`; compare the portal preview character-for-character with the PDF.
6. **Subject:** select **Evolutionary Biology**.
7. **Article category/type:** select **New Results**.
8. **Author:** enter Alec Kriebel, Independent Researcher, me@aleckriebel.com, ORCID 0009-0001-9320-500X. Do not add an institution or coauthor.
9. **Funding:** enter “No specific funding supported this work.” Do not invent a grant.
10. **Competing interests:** enter “The author declares no competing interests.”
11. **Data/code link:** use the public Zenodo DOI and, secondarily, the tagged GitHub source. Do not submit while any placeholder identifier remains.
12. **License:** the author must select one of the portal's offered choices. This package intentionally makes no selection.
13. **Preview:** verify title, author spelling, ORCID, abstract symbols, subject/category, figure rendering, both supplementary files, the manuscript page count, and both data/code URLs.
14. **Final stop:** do not click the final submission control until the human author has reviewed the generated PDF, metadata, license choice, and portal preview.
