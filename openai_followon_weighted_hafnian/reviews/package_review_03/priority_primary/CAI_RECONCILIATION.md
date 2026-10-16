# Cai–Liu version reconciliation and correction

Follow-up direct checks: 2026-10-07 UTC. This corrects the auxiliary review's initial assertion that the 2019 arXiv account omitted the McQuillan equivalence credit. That assertion was false. I had repeated it in my final report's evidence-limits paragraph; that paragraph is now corrected. No manuscript, archived package, or primary source was changed.

## Positive direct evidence

The [exact v1 HTML](https://arxiv.org/html/1904.10493v1) identifies arXiv:1904.10493v1, 23 April 2019. The paragraph immediately after Theorem 1.2 explicitly credits McQuillan's Proposition 5. The exact sentence, also present in the [actual v1 PDF](https://arxiv.org/pdf/1904.10493v1), printed page 4, is:

> We note that allowing nonnegative edge-weights does not add more computational power [McQ13, Proposition 5].

Fresh PDF text extraction gives this at lines 145–146 of the reading copy. The source obtained directly from [arXiv's versioned source endpoint](https://arxiv.org/src/1904.10493v1) confirms this independently: `intro.tex` line 191 is an active, uncommented sentence with a Proposition 5 citation to key `DBLP:journals/corr/abs-1301-2880`. `paper.bbl` resolves that key to Colin McQuillan, *Approximating Holant problems by winding*, CoRR abs/1301.2880 (2013). Thus this is not merely a modern HTML conversion inserting an absent citation.

The [unversioned/current PDF](https://arxiv.org/pdf/1904.10493) downloaded in the same batch is byte-identical to v1. The primary abstract record lists only v1, publicly submitted 23 April 2019 18:52:15 UTC. The [ICALP 2020 proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol168-icalp2020/LIPIcs.ICALP.2020.23/LIPIcs.ICALP.2020.23.pdf), printed page 23:4, paragraph following Theorem 4, carries the equivalent statement with reference [18, Proposition 5], explicitly mentioning unweighted #PM. Its theorem numbering and expanded wording differ, but the relevant McQuillan credit is present in both versions.

## Fresh byte hashes

| Direct primary retrieval | Bytes | SHA-256 |
| --- | ---: | --- |
| `https://arxiv.org/pdf/1904.10493v1` | 1,175,645 | `b21cb2a28cf4b6f1a075988e5ce4e01cec457b1eac8a10f025e36711a21a564b` |
| `https://arxiv.org/pdf/1904.10493` | 1,175,645 | `b21cb2a28cf4b6f1a075988e5ce4e01cec457b1eac8a10f025e36711a21a564b` |
| `https://arxiv.org/html/1904.10493v1` | 628,745 | `a2005bd5a92893081e3ada1e349276915f0b92f883e6841a0236e29adec916a3` |
| `https://arxiv.org/src/1904.10493v1` | 4,235,003 | `bc5d3714e9270d3c04ae2a5b93cb409f1224a4d54d0d93622eda072ed9e027d5` |
| ICALP proceedings PDF endpoint above | 1,177,193 | `b8cabdc527f1402a0217c5018275f4d91ba68d5a4148420af44f95baddb47af6` |

The active source member `intro.tex` has SHA-256 `80ba9e3e6516a2b9e282e880fb03ae4887337fae26c6f438eac9617552491f47`. Complete retrieval URLs, final URLs, timestamps and member metadata are preserved in the authored `CAI_RECONCILIATION_DOWNLOAD_MANIFEST.json` and `CAI_SOURCE_MEMBER_MANIFEST.json`.

## Package implication

There is no source-version defect in citing arXiv:1904.10493v1's explanation of Theorem 1.2 for this attribution. The parent supplied the archived package's corresponding row wording; that wording is supported by the actual primary source. No supplemental citation/version repair is warranted on the alleged-absence ground. The current manuscript does not cite Cai–Liu, and its McQuillan/Dell/JVV attribution verdict is unaffected. The needed repair is to the authored review evidence, not the candidate package.

Raw third-party downloads and extracted texts are reading copies under `primary_reading/cai_reconciliation/` and are excluded from owned Git commits/public payloads. This authored correction and metadata manifests may remain public review evidence. No claim is made about why the auxiliary reviewer initially missed the sentence; the directly falsified assertion is withdrawn.
