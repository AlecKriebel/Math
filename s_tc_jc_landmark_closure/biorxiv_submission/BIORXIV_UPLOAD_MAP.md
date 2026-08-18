# bioRxiv upload map

Verified against bioRxiv's official **Submission Guide** and **About bioRxiv** pages on 2026-08-16:

- https://www.biorxiv.org/submit-a-manuscript
- https://www.biorxiv.org/about-biorxiv

The official guide says that a single PDF containing text and figures is the simplest main upload, supplemental material should be separate, LaTeX should be converted to PDF before submission, article categories include New Results, and the author must select a distribution/reuse option. The official scope page lists Evolutionary Biology as a subject category. Portal fields can change; recheck both official pages immediately before submission.

## Release-assets gate

Before opening the bioRxiv portal, confirm that the public GitHub release
`stc-jc-sharp-boundary-v1.1.4` exposes all eight hash-bound replay assets
listed in `../release/PUBLIC_RELEASE_ASSETS.md`.  Download the outer envelope
and checksum manifest once from the public release and verify them against the
local copies.  Do not rely on the superseded 18-page replay records under
`history/`.

From the monorepository root, require all three commands to pass:

```bash
(cd s_tc_jc_landmark_closure/biorxiv_submission && shasum -a 256 -c SHA256SUMS)
python s_tc_jc_landmark_closure/reproducibility/verify_submission_source_archives.py
python s_tc_jc_landmark_closure/reproducibility/verify_public_release.py
```

The last command downloads the public tag and all eight replay assets; a URL
string alone does not satisfy this gate.

## Portal sequence

1. **Main manuscript:** upload `Strong_Tree_Childness_Sharp_Level2_JC.pdf` as the article PDF.
2. **Supplementary material:** upload `Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`.
3. **Verifier entry points:** upload `Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip` as supplementary code (or supplementary material if the portal has no code-specific type). It contains the executable entry points, Python dependency lock, external-tool requirements, active theorem map, and internal checksums. It deliberately does not duplicate the complete graph/certificate archive, which is hundreds of megabytes and remains at the immutable public release.
4. **Optional source supplement:** `Strong_Tree_Childness_Sharp_Level2_JC_source.zip` contains LaTeX, BibTeX, TikZ sources, and deterministic build instructions. bioRxiv's guide permits LaTeX source as supplemental material but requires the rendered PDF as the main article.
5. **Title and abstract:** paste the exact fields from `BIORXIV_METADATA.md`; compare the portal preview character-for-character with the PDF.
6. **Subject:** select **Evolutionary Biology**.
7. **Article category/type:** select **New Results**.
8. **Author:** enter Alec Kriebel, Independent Researcher, me@aleckriebel.com, ORCID 0009-0001-9320-500X. Do not add an institution or coauthor.
9. **Funding:** enter “No specific funding supported this work.” Do not invent a grant.
10. **Competing interests:** enter “The author declares no competing interests.”
11. **Data/code link:** use the tagged GitHub source and public GitHub Release URLs in the metadata. Add a persistent repository URL only after the deposit exists.
12. **License:** the author must select one of the portal's offered choices. This package intentionally makes no selection.
13. **Preview:** verify title, author spelling, ORCID, abstract symbols, subject/category, figure rendering, both supplementary files, the manuscript page count, and both data/code URLs.
14. **Final stop:** do not click the final submission control until the human author has reviewed the generated PDF, metadata, license choice, and portal preview.
