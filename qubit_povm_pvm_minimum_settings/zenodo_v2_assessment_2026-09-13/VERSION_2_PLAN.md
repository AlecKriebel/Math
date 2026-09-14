# Zenodo version 2: revision and release plan

This is a proposed release specification, not a published revision or live Zenodo draft. The baseline is the material downloaded directly from Zenodo on 14 September 2026 UTC / 13 September Pacific. No website text was used to determine what needs correction.

## Verified baseline

| Record | Actual archived object | Latest-version check |
|---|---|---|
| [21699161](https://zenodo.org/records/21699161) | 34-page publication PDF, filename v1.1.0 | Same July 30 record |
| [21699069](https://zenodo.org/records/21699069) | 34-page line-numbered PDF used in the original correspondence | Same July 30 record |
| [21699181](https://zenodo.org/records/21699181) | Manuscript source archive | Same July 30 record |
| [21699224](https://zenodo.org/records/21699224) | Original exact-verification software package | Same July 30 record |

All four files matched Zenodo's published MD5 values; SHA-256 values are recorded in `archive_manifest.json`. The source main.tex differs from the current working manuscript only in the strict-residual signature clarification. The appendix and bibliography are byte-identical. The public software archive contains the older symbolic verifiers, not the subsequent Lean development.

## Manuscript changes

1. **Correct Definition 5.1, printed page 13.** Keep signature (1,3) as an explicit separate assumption, orient the future cone to contain u, and restrict the common-cone/positive-pairing equivalence to that signature hypothesis. The scalar inequalities alone do not force it. This is already fixed in the working source but not in the downloaded PDF. State the correction in the changelog and that the principal theorem is unchanged; do not hide it as stylistic editing.
2. **Add precise formal-verification coverage, printed page 23 and Appendix I.** The current archived wording describes symbolic checks only. Add the principal Lean endpoints, pinned environment, fixed successful receipt, theorem-to-paper map and reproduction instructions. State that auxiliary arguments may be specialized or replaced. Keep the separate symbolic-verifier limitations, which remain accurate. Do not claim all manuscript statements or the original proof route have been formalized verbatim.
3. **Clarify Section 3's role, printed pages 6–8.** The known three-by-two existence theorem is already attributed in the abstract, introduction and Table 1. Make the section explicitly a supporting rational exact certificate in that known architecture. Lead the article with the new two-input lower bound. Keep the displayed functional, witness and global projective bound readily accessible; move routine bound derivations to the appendix if this improves the reading order. A wholesale withdrawal of Section 3 is not warranted by the comparison.
4. **Narrow or remove Table 1's “Global optimum claimed” row, printed page 3.** Its unqualified “No” for the earlier paper conflates different optimization questions. The earlier work includes an exact fixed-state projective optimum and numerical/NPA global projective results. Specify exactly which optimum is meant, or remove the row. [Earlier paper](https://arxiv.org/html/1007.2578v1).
5. **Compact routine proofs without removing hypotheses.** Lemma 4.1, printed pages 8–9, can be reduced to the minimal-dependence bound and extremality inequalities, while retaining a short justification of support minimality and the same-ray cancellation case. The independent Section 3 audit supplies a candidate proof. Do not compress physical reconstruction, multiplier signs or boundary cases into unexplained slogans.
6. **Update related work.** Include [Zhu et al., arXiv:2608.01317](https://arxiv.org/abs/2608.01317), distinguishing their separation result from this paper's universal two-input equality. Do not add a private numerical observation from correspondence as an established theorem or public citation. A raw-set inequality requires matching conventions and a certified witness before it can support a formal corollary.

An optional improvement is to report the Lean development's stronger universal PVM bound 289/10 in a clearly identified supplement. It is proved by an alternative physical SOS certificate and is not an exact-optimum claim. This is useful but unnecessary for version 2's principal purpose; do not let it expand the revision into a new optimization project.

## Recommended record structure

Use **two linked new versions of existing records**, with the common release label **2.0.0**:

- Publication: create a new version of **21699161**, preserving its concept DOI **10.5281/zenodo.21699160**. Upload `paper-v2.0.0.pdf`, `review-v2.0.0.pdf`, `source-v2.0.0.tar.gz`, `CHANGELOG-v2.0.0.md`, and a final checksum manifest together. The two PDFs must be generated from the same source.
- Software/proof companion: create a new version of **21699224**, preserving its concept DOI **10.5281/zenodo.21699223**. Upload one reproducibility archive containing the exact scripts, Lean sources, pinned manifests, validation contracts, authoritative receipts and required documentation. Link the exact new publication version.

The legacy review-PDF, source-only and checksum records can remain historical. Their descriptions may receive metadata-only cross-links to the consolidated new publication record. Creating further independent paper/source/PDF DOI families is unnecessary.

Zenodo's **New version** action creates a linked draft with its own version DOI; the existing version remains available. Upload revised files and set the metadata before publishing. Metadata-only edits are a separate operation. [Official instructions](https://help.zenodo.org/docs/deposit/manage-versions/). Use exact version DOIs in the reproducibility links and the all-versions DOI where a general latest-paper pointer is useful. [DOI versioning explanation](https://zenodo.org/help/versioning).

There is no new DOI yet. Do not invent one or paste an old version DOI as the new version's identifier. Obtain the identifiers from the actual new-version drafts, then insert them into the files and cross-links before the final build. A separate GitHub release is optional; because this repository automatically archives releases, creating one should be deliberate rather than an incidental consequence of preparing these Zenodo versions.

## Metadata changes grounded in the current records

- Set the Version field to `2.0.0`; all four downloaded records currently omit that field even though filenames contain `v1.1.0`.
- Add the author's ORCID `0009-0001-9320-500X` and affiliation `Independent Researcher`; the current creator metadata has neither.
- Use the actual revised-release date, and put both the initial and revision dates in the manuscript. Preserve July 30 as the historical initial deposit date.
- Clean copied HTML/math markup from the review/software descriptions. Use simple readable text.
- Replace the software description's obsolete blanket statement that the package does not formally verify the general arguments with a precise account of principal Lean coverage and auxiliary limits.
- Correct the software description's “Immutable source tag” link: it currently points to a path on mutable `main`. Link an actual fixed commit or verified tag.
- Keep the paper as a preprint and the companion as software; formal certification is not human peer review. Retain substantive AI-use disclosure.
- Preserve the existing manuscript/data and code licenses and third-party notices. Explicitly state the license for the newly included Lean source; the original package's code-license clause names only its artifact scripts and top-level runner.
- Add explicit reciprocal related-record links and a concise version changelog. Do not present the old software record as though it already contains Lean.

## Proof-package checks before publication

Do not zip the entire live working directory. Stage only the intended package, while retaining all files referenced by its verification scripts and documentation. Exclude local dependency caches and build backups. Retain the historical baselines required by preflight. Omitting those archives would require revising and revalidating the actual verifier scripts, not merely editing instructions; any changed verifier would need new fingerprints and verification evidence. Resolve all sibling-folder documentation links in the staged package.

Four hashes in the live Lean shipment manifest are currently stale: the convenience copies of `axiom_audit.json`, `kernel_report.json`, `latest_run.json`, and `statement_audit.json`. They reflect a later run than the original manifest. This is an archive-integrity problem, not evidence of a false theorem. Select consistent receipt pointers in staging, preserve the immutable historical run evidence, and generate a new shipment manifest after verification.

The same four entries were checked against the committed snapshot `53b1570d6424d5d24cabdbdfa3144e318202ba5a` and all match there. Thus an immediate link to that fixed proof snapshot avoids the live working-directory mismatch; it does not replace the final v2 staging checks.

Keep the old manuscript-correspondence receipt as historical evidence. Add a new v2 correspondence record covering the revised TeX, PDFs and exact proof-source snapshot; do not imply that old PDF hashes certify the new typography or exposition. If proof sources are unchanged, record that fact, but still execute the final advertised reproduction path from the staged archive.

Publication acceptance checks: source and review PDF agree; all newly introduced references resolve; no missing glyphs or overfull tables; clean extracted symbolic checks; full pinned Lean check and expanded statement contracts; current source/dependency fingerprints; all retained shipment hashes pass before execution; no private correspondence in the archive; exact version DOI links point to the staged versions. A source-only Lean archive requires prepared dependencies or bootstrap access and should not be advertised as self-contained offline proof execution.

The revision remains bounded: clarity, explicit correction, formal-proof integration, current literature and dependable packaging. It need not solve raw-set separation, exact global optima, or higher-dimensional generalizations.
