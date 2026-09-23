# Preprint revision response: version 1.0.1

Scope: the fresh adversarial review cycle requested on 23 September 2026. This is internal AI-assisted review of mathematical soundness, attribution, and preprint materials, not journal refereeing or a formal proof certificate.

## Changes made after round 1

| Finding | Decision and correction |
| --- | --- |
| R1-1: the relation between Abbar's single-offset criterion and the finite-block formulation should be explicit | Accepted. The paragraph after Lemma 2 now chooses an integer `q >= max(F union {1})` and displays `c_(j±n)^(1/p) <= ||S||^(q-j) c_(q±n)^(1/p)` for `j in F`. This is the missing explanatory bridge in the attribution, not a new hypothesis or a repair to the direct proof. |
| Parent precision check: "makes it integrable" could be read as asserting L1 membership | Accepted. The gluing argument now states exactly what its estimate establishes: `phi in L^p(X,mu)`. No L1 conclusion is needed or claimed. |

Round 1 found no blocking mathematical issue and no material package inconsistency. Both changes preserve the theorem, its assumptions, and the stated contribution as an attributed application of earlier results. The paper remains five pages.

## Propagation and reproducibility

- Advanced the manuscript and all active version fields to 1.0.1, including the source README, citation entry, website, Zenodo instructions, and generated metadata.
- Rebuilt the PDF, source archive, upload kit, expanded upload files, website downloads, and repository Pages copies. Historical review reports remain bound to the versions they actually inspected.
- Rendered and visually inspected all five revised PDF pages. No clipped mathematics, broken references, or other material formatting defect was found.
- Extracted the revised source archive into a fresh directory and compiled it. With the recorded fixed build date, the resulting PDF is byte-identical to the distributed PDF.
- Checked archive CRCs and source-member equality, the nested PDF/source copies, metadata agreement, copy-and-paste version fields, and both generated-site manifests. All checks passed.

## Revised artifact identifiers

| Artifact | SHA-256 |
| --- | --- |
| `manuscript/note.tex` | `3b16fbb6a78491f117dd2d50345c1863dad7b6486863a403ecccf74d6b4a9794` |
| `output/pdf/note.pdf` | `671cf6be89c45cbda49c207c2a656064958494fce60f05619d63a3061ee123c7` |
| `output/note-source.zip` | `7ef22e4bdf8a34289384f25d2fb481d76059910b9caf21b6d1d8ff92c4d47385` |
| `output/zenodo-upload-kit.zip` | `838ed43c0f91a402e608a72421b7564288ed9a2b1d1bb15881c61af9b8001e22` |

## Fresh second review and final disposition

A new independent adversarial reviewer examined version 1.0.1 without reading the first review's conclusions. It used a counterexample-driven route, checked the original and prior-theorem assumptions directly, rederived the analytic arguments, inspected all five rendered pages, and verified the distribution files. Its verdict is **no actionable findings at any grade**.

| Round | Reviewed version | Outcome |
| --- | --- | --- |
| [Fresh adversary 1](preprint-adversary-r1.md) | 1.0.0 | No blocking issue; one worthwhile explanation requested and adopted above. |
| [Fresh adversary 2](preprint-adversary-r2.md) | 1.0.1 | No blocking, worthwhile, or cosmetic correction requested. |

No identified manuscript or preprint-package issue remains unresolved, so the requested iterative review cycle closes here. The note is ready for submission as the attributed, unrefereed preprint it describes. This conclusion does not assert a new scalar criterion, a new amplification mechanism, established priority for the explicit application, or journal acceptance. No journal-submission work was undertaken.

The exact version reviewed in round 2 is the version identified above. Repository and live-publication completion is recorded in the research log and `live-deployment.json`; those records do not change the manuscript or upload files.
