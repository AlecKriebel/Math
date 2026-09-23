# Fresh adversarial preprint review, round 2 — version 1.0.1

Review completed: 2026-09-23T13:43:43Z. Reviewer: new independent OpenAI Codex audit agent.
Scope: mathematical validity and readiness of the local revised preprint and its reproducibility/publication package; not journal submission or human peer review.
Completion estimate for this scoped review: **100%**. This is task completion, not a probability of historical novelty.

## Verdict and actionable findings

**PASS for preprint readiness. No actionable mathematical, bibliographic, PDF, metadata, or package defect was found in the reviewed snapshot.** No manuscript or executable change is requested by this review. The explicit counterexample proves failure of existence, hence also failure of uniqueness, in the fixed matching stated in the original conjecture.

Severity count: critical 0; major 0; minor actionable 0. Optional stylistic preferences do not change this verdict. Historical-priority uncertainty is explicitly disclosed and does not invalidate the proved claim. The public deployment of this revised snapshot remains an administrative action for the parent task; its currently pending status is not a manuscript defect.

I began with `paper/paper.tex` and the original Knudson contribution, then derived the component quotient below independently. Earlier audit conclusions were not used as premises. The supplied scripts were examined and executed only as corroboration. No person was contacted and no source, PDF, package, or repository commit was changed by this reviewer. This report is my only workspace write; clean-extraction/build/render files were confined to temporary storage.

## Exact reviewed snapshot

SHA-256 values were taken before adding this report. Adding this report or later deployment logs to the archive is expected to change archive hashes without changing the reviewed mathematical core.

| File | SHA-256 |
| --- | --- |
| `paper/paper.tex` | `364d097566295023d0c19e0b3e1a52e6f58d24760bffc6be9a7b84c451683a05` |
| `paper/paper.pdf` | `7e63996fdec314e02adf668eb676e4926a5700097d664bf28ab128d617ca210e` |
| `verification/verify.py` | `aed912e2ba41f1ce6ed400a65d9c0cc6dc7cdd6361b7e87eb924d303607f1df6` |
| `verification/independent_check.py` | `d3b5d2fc62636a7ed3d0e8ffa1b759348c715a9bf97016666454e712ce087359` |
| `CITATION.cff` | `0c57775a3f255761ba081cde99b6235478df880352eae60c4c63429e4d403df7` |
| `.zenodo.json` | `e87a4964dcae781f7fad4ba3bcfe3a4fe0de9d86b26b085e342b340dfdb5b1b9` |
| `zenodo/deposition.json` | `d2bde52c5e2572363e9b872f9ece3ebf62652d383ddcdb1e6a060642be73dae2` |
| `build_package.py` | `ddb6a50bd0457fa6e9fedbbe81ee8b8cfeebb05c23c4a43c1b9b4be6098a852e` |
| `README.md` | `34947dfb7925a59cdd71f124e86a2f680da7cb55cef6851c9613069500c360d9` |
| `site/index.html` | `dfd99fb66a6af4ccbaa1e7d68be154b5b6584ebb848f8656916471ece0a0b3fb` |
| `zenodo/upload/source-and-verification.zip` | `52e545a3ad300d896e3cfffd03ce6900a40f8726a2059aa34f2b71077461f85d` |
| `zenodo/zenodo-upload-kit.zip` | `04fe989380797dfe5fa9e90e8824623f1bb53108547384efe4362cb41b357821` |

## Independent route: the degree-zero module

Let `K_i` contain the first `i` nonempty simplices of `a,b,c,d,cd,bd,ac`, and put `K_0` empty. Over an arbitrary field `k`, ordinary `H_0(K_i;k)` is the free vector space on the vertices present at stage `i`, modulo the endpoint differences of the edges present then. The component partitions are:

| Stage | Components |
| --- | --- |
| 0 | none |
| 1 | `{a}` |
| 2 | `{a}`, `{b}` |
| 3 | `{a}`, `{b}`, `{c}` |
| 4 | `{a}`, `{b}`, `{c}`, `{d}` |
| 5 | `{a}`, `{b}`, `{c,d}` |
| 6 | `{a}`, `{b,c,d}` |
| 7 | `{a,b,c,d}` |

Use the filtered triangular vertex basis `g1=a`, `g2=b-a`, `g3=c-b`, `g4=d-c`, born at stages 1, 2, 3, 4 respectively. It is a basis at every stage where its entries are defined: the change-of-basis matrix is triangular with diagonal 1. At stage 5 the relation from `cd` is `g4=0`; at stage 6 the new relation is `d-b=g4+g3=0`, which kills `g3`; at stage 7 the new relation is `c-a=g3+g2=0`, which kills `g2`. Each remaining generator maps to the corresponding surviving class under inclusion.

Thus, extending the final stage constantly, the module is exactly

`I[1,infinity) + I[2,7) + I[3,6) + I[4,5)`.

This is a filtered-basis decomposition, not merely an agreement of Betti numbers. The finite intervals identify the birth/death simplex pairs `(b,ac)`, `(c,bd)`, `(d,cd)` with no choice or tie. All filtration stages are forests, so no positive-dimensional class complicates this calculation. This independently verifies both the pivot result and the any-field extension.

## Exhaustive incidence and convention challenge

The underlying graph has precisely the six edge/vertex incidences `ac/a`, `ac/c`, `bd/b`, `bd/d`, `cd/c`, `cd/d`. Of the three finite persistence pairs, only `(d,cd)` is an incidence. Hence the complete directed graph has exactly

`ac -> a`, `ac -> c`, `bd -> b`, `bd -> d`, `d -> cd`, `cd -> c`.

It is acyclic. Both possible first descents from the critical edge `ac` end at unmatched vertices, and there are no upward continuations there. Its reachable set is exactly `{ac,a,c}`, including the starting edge. Therefore no alternating gradient path, even allowing a direct endpoint path as length zero after the initial descent, can reach `b`. The other nonincident pair has exactly the path `bd -> d -> cd -> c`. Reversing this path yields precisely `{(d,bd),(c,cd)}` and creates the displayed unique path from `ac` to `b`; it does not create a path in the original field.

The original [Knudson report, printed pp. 1628–1630](https://ems.press/content/serial-article-files/46173) permits an arbitrary finite simplex-wise filtration, uses mod-two coefficients, and defines its matching by retaining incident persistence pairs. Conjecture 2 on p. 1629 names that fixed matching. It does not require positive-dimensional births, a surface, a lower-star filtration, or prior cancellations. The paper therefore addresses the stated conjecture. Its one-based indices simply shift the source's zero-based indices; the source's lifetime convention `j-i-1` does not delete the immediate pair `(d,cd)` from the defined persistence pairing. The manuscript clearly separates filtration order from the gradient matching. Using ordinary rather than reduced `H_0` affects the surviving oldest class, not these finite pairs.

For the signed calculation, the ordered boundaries are `d-c`, `d-b`, `c-a`. Reducing gives `d-c`, `c-b`, `b-a`; their latest nonzero coefficients are all 1. This is valid in every characteristic, including characteristic two, and requires no unsupported inference from finitely many tested fields.

## References and scope

All three manuscript references were checked against primary sources or publisher/author records:

- The [MFO record](https://publications.mfo.de/handle/mfo/3074) confirms report 29/2008, volume 5, and DOI `10.4171/OWR/2008/29`; Knudson's contribution occupies printed pp. 1628–1630 in the primary PDF. The citation is to the whole report DOI while correctly identifying the contribution and conjecture page.
- The [ELZ publisher record](https://link.springer.com/article/10.1007/s00454-002-2885-2) and [author-hosted text](https://pub.ista.ac.at/~edels/Papers/2002-J-04-TopologicalPersistence.pdf) support the cited publication and elimination procedure. Its young-positive-simplex search agrees with the reductions here.
- The [BLW publisher record](https://link.springer.com/article/10.1007/s00454-011-9350-z) confirms authors, title, volume 47, pp. 347–377, year 2012, and DOI. [Author preprint, Lemma 9](https://arxiv.org/pdf/1001.1269) requires cancellation of descendant pairs in a sequence before asserting its unique path. The manuscript's limited compatibility statement is accurate; it does not apply that surface theorem to this interval as a premise.

The [linked Knudson bibliography](https://kpknudson.com/math) still lists the related Bauer collaboration as in preparation. This supports the manuscript's caveat, not any conclusion about unpublished contents or completion. I did not repeat the prior 39-query priority search or certify inaccessible books/theses. Those limitations are disclosed in the package and paper. The note asserts no smallest-example theorem, no counterexample to ordered cancellation results, no verified current catalogue status, and no proof-assistant certification.

## Standalone PDF and executable package

- Inspected all three rendered PDF pages, not only extracted text. Equations, theorem/proof, author/ORCID footnote, all references, and page numbers are legible with no clipping, overlap, missing symbols, or placeholder text. The proof is sufficient without the package. Extracted PDF title, author, subject, and keywords are accurate.
- Inspected all six external PDF annotations: author ORCID, companion page, author bibliography, and the three intended DOI links. Internal citation targets render correctly. The companion link gives a usable route from a standalone PDF to the checks/audits.
- Read both standard-library Python verifiers. The second computes component partitions and inclusion-map ranks rather than merely replaying the first's union-find calculation. The mixed-difference formula recovers the finite bars above; signed reductions and path reversal are correctly implemented. The finite-prime checks and relabeling checks are represented as corroboration, not an all-fields proof or broader search.
- Executed both programs normally and with `-O`, in the workspace and from clean archive extraction; all eight runs succeeded, and clean-extraction outputs matched the distributed expected files exactly. Explicit exception checks remain active with optimization.
- Compared the preserved original script and output with their working verification copies: byte-identical.
- Independently validated `CITATION.cff` against the supplied official CFF 1.2.0 JSON schema using Draft7 validation and format checking. It passes. Its software-package type and preferred article citation are coherent. The ORCID check digit is valid and the supplied author identifier is consistent throughout.
- Parsed the Zenodo metadata and wrapper, inspected title/date/version/resource type/license/provenance, and verified consistency with the manual upload instructions. There is no invented DOI or claim that this kit has already deposited a record. The preprint and code license distinction is explicit.
- Clean-extracted both ZIP files. All 26 source-archive manifest entries and both upload manifest entries matched their SHA-256 values; the reviewed core files in the source archive matched the workspace. The upload PDF and nested source archive are the expected artifacts.
- Ran `build_package.py` from the extracted project: both regenerated ZIP archives were byte-identical to the reviewed distributed archives. Then rebuilt the extracted LaTeX manuscript with Tectonic: compilation succeeded and the complete extracted PDF text matched the reviewed PDF. PDF creation timestamps need not reproduce, and no bitwise PDF reproducibility is claimed.
- Compared the reviewed manuscript, scripts, metadata, upload instructions, and archives with staged `docs/papers/knudson-gradient-path` copies: identical. Validated the public download checksum manifest and all local relative download/navigation targets. The staged site identifies version 1.0.1 and makes the same scoped mathematical and provenance claims.

## Exact remaining gap

There is no remaining mathematical or artifact gap identified for this preprint snapshot. Historical priority beyond the documented bounded search and external human peer review remain unestablished, as explicitly disclosed. Public deployment and any eventual DOI assignment are separate administrative actions, not missing proof steps. If the parent adds only this report and deployment records and regenerates packages, a final checksum/deployment check is sufficient; those administrative additions do not reopen the mathematical review.
