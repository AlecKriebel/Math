# Final release-byte audit: order-12 frontier manuscript

## Verdict

**`ACCEPT_RELEASE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH`**

No manuscript-byte, scope, metadata, reproducibility, log, or layout defect
was found. The sole prepublication condition is atomic creation and push of
`gamma-theta-order12-frontier-v1.0.0` for these exact bytes.

## Provenance

The findings in this record were produced by the campaign's independent
final-release auditor.  The retained `audit.py` is a deterministic,
root-packaged machine binding of that completed review; it is not represented
as auditor-authored source.  Before publication it emits the conditional
verdict above.  After publication it instead verifies that the annotated tag
contains the accepted manuscript and public-PDF bytes and emits
`ACCEPT_RELEASE_BYTES_TAG_BOUND`.

## Bound artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 48,891 | `44e49d6dbf90174ca27f5b65e99e55a9852fb6deafb0ba3dd78770c53e0faa9e` |
| `references.bib` | 4,534 | `8471090ae03babda7794aea6bbcbc6fbcb36ffa8a859a86005bbb0b7ae2f9ec6` |
| `main.bbl` | 2,484 | `f9789755c4ec0c83b1e2493f5301e7d4d4dfaa4398810aa9e28d22148da4849a` |
| `main.blg` | 191 | `36a26a35030c17e6a29ed5fa683a298f907726cf9a3af844f8f4d3b56dd6020e` |
| `main.log` | 12,311 | `645879feb11804aaffd0e18c617c4616d4fdd6d39014197f795c753aa2110ac0` |
| `main.pdf` | 130,163 | `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2` |
| `README.md` | 2,351 | `5dd9578ca712c5449a6146544b4002f5aefb73b055cba405f9388b9065394cc0` |
| public `paper.pdf` | 130,163 | `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2` |

Against baseline
`b9b74a38415dac6ef11bb7cbc55badf224affadd`, the mathematical body is
unchanged. The complete diff is confined to Alec Kriebel author/PDF metadata
and the tagged-release/project-page data-availability links.

Two clean Tectonic 0.16.9 builds with
`SOURCE_DATE_EPOCH=1785074656` produced identical PDF and BBL bytes, equal to
the retained artifacts. The retained TeX/BibTeX logs are warning-free and
contain no overfull or underfull boxes.

The PDF has the requested title, author, and subject; it is an unencrypted,
form-free, 17-page letter-size document. Text extraction found no replacement
character or publication placeholder. All 17 pages were rendered at 144 DPI
and inspected; no clipping, overlap, broken glyph, margin, table, or page
number defect was found. The public PDF is byte-identical.

The theorem remains explicitly conditional on
MacGillivray--Mynhardt--Virgile's published through-order-11 computation and
repeatedly states that the universal conjecture remains open.
`order12_frontier` is the campaign's sole current paper; `c035_order12_k3`
is explicitly archival, superseded, and not a separate current publication.
No decisive package symlink or unexpected file was found. The tracked
`qa.json` is a machine-readable QA summary and is outside the bound
release-byte set above.
