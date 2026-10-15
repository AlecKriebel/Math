# Publication package

Preparation snapshot: 7 October 2026. Status statements below describe this
snapshot. Final complete-package reviews and any later publication/tracker
receipts are recorded separately in the project repository; archive
construction is not a claim that those later actions have occurred.

This package accompanies **Ordinary Banach–Mazur rigidity of von Neumann
algebras**, by Alec Kriebel, ORCID
[0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X), dated
7 October 2026. No affiliation is asserted.

For each fixed complex von Neumann algebra M, the paper establishes an
algebra-dependent positive ordinary complex Banach–Mazur threshold for
comparison with every complex von Neumann algebra N. The same threshold
works for their canonical preduals, and the conclusion is Jordan
*-isomorphism. The proof relies on OpenAI's family-295 ordinary bounded
self-coefficient Hochschild vanishing theorem at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` and on Roydor's geometric
estimates. The separable-predual conclusion follows immediately from
Roydor's published Theorem 1.2 and the new vanishing input. The paper gives
an explicit fixed-source proof extension for arbitrary preduals. Roydor's
2020 slides already announce the general conditional implication.

The cohomology breakthrough belongs to the attributed upstream work.
Multiplication stability, the geometry and the predual reduction are
established mechanisms. The potential distinct contribution is the complete
fixed-source assembly and its scope and constant bookkeeping; the note
does not claim firstness, a new cohomology proof, a universal numerical
threshold, or reproduced formal verification. The fresh priority audit is
`research/priority_audit_20261007.md`; its final-candidate addendum controls
the current proof comparison, while its earlier checkpoint remains
historical evidence.

## Exact intended Zenodo files

The project-local `zenodo-deposit.json` lists exactly two upload files:

| Local file | Independently downloadable name |
|---|---|
| `output/pdf/paper.pdf` | `paper.pdf` |
| `publication/upload-kit/source-and-verification.zip` | `source-and-verification.zip` |

The PDF is downloaded separately from the source archive. The archive has
a standalone `manuscript/main.tex` with its bibliography embedded, a clean
build helper, current mathematical ledgers, complete source/proof audits,
the fresh priority audit, exact finite mechanism checks, and unchanged
Apache-2.0 family-295 source/PDF/README/license material. Its generated
`SOURCE_MANIFEST.json` binds every other archive member by byte size and
SHA256; `SOURCE_VERSIONS.json` records the pivotal primary versions and
`VALIDATION_SCOPE.md` distinguishes the preparation evidence from final
publication checks.

`build_upload_kit.py` declares the exact curated relative paths rather than
copying the entire project. It uses fixed ZIP member timestamps, names,
permissions, order and compression settings. It verifies the original
pinned upstream hashes before writing an archive. Rebuild after any change
to an included input, then freeze and review the actual resulting bytes.

```sh
python3 publication/build_upload_kit.py --license cc-by-4.0 --license-confirmed
```

The generated build receipt records the archive hash, input hashes, and the
separately downloaded PDF hash. The PDF build and visual inspection evidence
is maintained by the root researcher; archive generation does not assert
visual inspection, mathematical validity, or complete-package review.

## Confirmed license

The human user selected the less restrictive of the two proposed licenses
on 7 October 2026: **Creative Commons Attribution 4.0 International
(CC BY 4.0)**, https://creativecommons.org/licenses/by/4.0/.
Original project material is licensed under CC BY 4.0. The metadata field
`cc-by-4.0` records that confirmed choice. The unchanged included OpenAI
material retains its Apache 2.0 license and original attribution.
Rebuild the archive with the confirmed decision recorded:

```sh
python3 publication/build_upload_kit.py --license cc-by-4.0 --license-confirmed
```

The flag records the received human decision. The archive's `LICENSES.md`
separates the selected license for original material from the unchanged
Apache-2.0 upstream exception. No third-party Roydor or arXiv PDF, extracted
text, or rendered page is included.

## Validation and publication status

AI tools were used extensively in research, proof development, drafting and
verification. Internal adversarial AI audits are not conventional human
peer review. The preprint has not undergone conventional human
refereeing. No fresh Lean kernel build of the upstream declarations was
reproduced, and this follow-on theorem is not represented as formalized.
The finite exact computations test specific mechanisms; they do not prove
the infinite-dimensional theorem by sampling.

This README describes an intended package. It is not a Zenodo publication
receipt. The root research log and exact versioned review records govern
those gates. A reserved DOI is not evidence
of publication. Production publication must use the repository tool's
separate check, stage, inspect, verified-ID publish and DOI-inspect steps.
The authorized tracker append follows only a confirmed public record.
No GitHub release or separate publication pathway is intended.
