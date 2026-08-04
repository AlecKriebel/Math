# Frozen source snapshot

**Version 0.2 — prepared for author audit — August 2026**

This file identifies the exact external versions used for the formula and history audit. The mathematical proof of global injectivity is derived independently from the process definition; the source snapshot is needed only for reproducible comparison claims.

## arXiv version

- Identifier: `arXiv:2607.14653v1`
- Title: *Revisiting a random model of lateral gene transfer in phylogenetics*
- Authors: Laura Kubatko, Simone Linz, Kristina Wicke
- Submission timestamp: `2026-07-16 07:21:05 UTC`
- Retrieval date: `2026-08-03` in `America/Los_Angeles`
- Audited PDF filename: `arxiv_2607.14653v1.pdf`
- Audited PDF SHA-256: `939b62a0dc5e71e01d4e747ea7e216539e11a55478ced7ba008d1ca6686ac809`
- Extracted-text filename used for line navigation: `arxiv_2607.14653v1.txt`
- Extracted-text SHA-256: `11d0e1e25298f21a88b2bb0735f9ae191c10c429c441e7ae954bc742cde438e8`

### Source-archive limitation

The arXiv page exposes the version-1 TeX-source endpoint. Retrieval was attempted on `2026-08-03` in `America/Los_Angeles`, but the available retrieval tool reported `400 Unsupported content-type: application/gzip` before exposing the bytes. Consequently, no local arXiv source-archive file or SHA-256 hash is claimed. The audited PDF, immutable arXiv version identifier, repository commit, and locally hashed repository files below freeze every source used for the exact discrepancies.

## Repository version

- Repository: `https://github.com/lkubatko/LGT-Model`
- Audited commit: `1954b2ab92525dfdaf43b50f97dcf46658cab6c9`
- Commit message: `Add files via upload`
- Commit timestamp: `2026-07-14 12:16:12 UTC`
- Retrieval date: `2026-08-03` in `America/Los_Angeles`

### Audited files

| File | Immutable identifier | Local SHA-256 | Relevant locations |
|---|---|---|---|
| `LGT-SimulationStudy.Rmd` | Git blob `792addf37bed8fc609f5d3c3d9a3a0f60335c22c` | `bd89a43f4663e4d89404f4e358cabfafb5477c3672d30084185e543ff7e28cdc` | `GetSitePatternProbs`, lines 32–64; `GetLikFull`, lines 83–96 |
| `KubatkoLinzWicke-LGT-2026.nb` | Git blob `67c4ba03f56dc1b5d9c6944d417760ab067b163b` | `02d51a3edf85598aa07284c5af6aee3e9de3e4f30cb112216d9f95b23024fab4` | history definitions, text lines 430–749, including Mathematica inputs `In[28]` onward; site-pattern integrations beginning at subsection/cell `Pxxx`, lines 1308–1489, with analogous later pattern cells |
| `KubatkoLinzWicke-LGT-2026.pdf` | Git blob `38f0e4db716a9b1b16b04e879daee67651ea61b9` | not separately downloaded; not used as the locally hashed audit PDF | repository manuscript copy only |

The audited R and notebook files are not redistributed in the author-ready package. Their hashes and immutable locations are sufficient to reproduce the comparison from the repository commit.

## PDF locations relevant to the audit

Page references below use the printed PDF pages in `arxiv:2607.14653v1`; extracted-text line ranges are provided only as a navigation aid.

- Theorem 4.5 and the strict source-paper pattern statement `p_xxy > p_xyx = p_yxx`: PDF page 10; extracted-text lines approximately 520–548.
- Conjecture 4.1: PDF page 11; extracted-text lines approximately 603–606.
- Five-class multinomial convention: PDF page 11; extracted-text lines approximately 618–624.
- Proposition A.2 history densities and ranges: PDF pages 21–23; extracted-text lines approximately 1288–1456.
- Conditional pattern classes and marginalization convention: PDF page 24; extracted-text lines approximately 1458–1502.

## Source-notation translation

The source symbols are aggregate equality classes, not probabilities of one fixed nucleotide triple. Under the source convention,

```text
p0  = p_xxx,
p12 = p_xxy,
p13 = p_xyx,
p23 = p_yxx,
pD  = p_xyz.
```

Their nucleotide-pattern multiplicities are `4, 12, 12, 12, 24`, respectively. In `LGT-SimulationStudy.Rmd`, `GetSitePatternProbs` returns `(pxxx, pxxy, pxyy, pxyz)`, and `GetLikFull` uses `pxyy` twice for the two symmetric discordant-pair classes.

## Version-to-discrepancy map

1. **Exact formula reversal.** The proposition about `F_src` is the exact evaluation of `LGT-SimulationStudy.Rmd`, commit `1954b2…`, function `GetSitePatternProbs`, lines 32–64. At the stated interior cube point it yields positive normalized probabilities but `p_xxy-p_xyx < 0`.
2. **One-transfer density distinction.** The comparison of the two discordant one-transfer density types is tied to arXiv v1, Proposition A.2 and its subsequent topology integrals, together with the notebook history definitions at the frozen commit.
3. **Increment-versus-absolute-time diagnostic.** The `h2` ranges and gene-tree assignments are tied to the notebook history text at lines 480–550 and analogous later classes, and to the `Pxxx` integration cell beginning at line 1308. The exact process theorem does not use these expressions as assumptions.
4. **Exhaustiveness issue.** Under the backward-lineage convention defined in the revised manuscript, repeated noncoalescing lineage movements are absent from the frozen fourteen-class list. This is a probabilistic statement proved from the process definition, not an inference from source-code formatting.
