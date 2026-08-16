# bioRxiv upload map

Verified against bioRxiv's official **Submission Guide** and **About bioRxiv** pages on 2026-08-14:

- https://www.biorxiv.org/submit-a-manuscript
- https://www.biorxiv.org/about-biorxiv

The official guide says that a single PDF containing text and figures is the simplest main upload, supplemental material should be separate, LaTeX should be converted to PDF before submission, article categories include New Results, and the author must select a distribution/reuse option. The official scope page lists Evolutionary Biology as a subject category.

## Portal sequence

1. **Main manuscript:** upload `Strong_Tree_Childness_Sharp_Level2_JC.pdf` as the article PDF.
2. **Supplementary material:** upload `Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`. The full computational archive should live in the persistent repository rather than relying on a large bioRxiv supplement.
3. **Optional source supplement:** `Strong_Tree_Childness_Sharp_Level2_JC_source.zip` contains LaTeX, BibTeX, TikZ sources, and deterministic build instructions. bioRxiv's guide permits LaTeX source as supplemental material but requires the rendered PDF as the main article.
4. **Title and abstract:** paste the exact fields from `BIORXIV_METADATA.md`; compare the portal preview character-for-character with the PDF.
5. **Subject:** select **Evolutionary Biology**.
6. **Article category/type:** select **New Results**.
7. **Author:** enter Alec Kriebel, Independent Researcher, me@aleckriebel.com, ORCID 0009-0001-9320-500X. Do not add an institution or coauthor.
8. **Funding:** enter “No specific funding supported this work.” Do not invent a grant.
9. **Competing interests:** enter “The author declares no competing interests.”
10. **Data/code link:** use the GitHub URL in the metadata and add the persistent repository URL only after the deposit exists.
11. **License:** the author must select one of the portal's offered choices. This package intentionally makes no selection.
12. **Preview:** verify title, author spelling, ORCID, abstract symbols, subject/category, figure rendering, supplement association, page count, and data/code URL.
13. **Final stop:** do not click the final submission control until the human author has reviewed the generated PDF, metadata, license choice, and portal preview.
