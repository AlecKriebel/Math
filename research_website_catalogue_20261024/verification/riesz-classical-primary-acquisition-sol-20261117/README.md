# Frozen classical primary-source acquisition

Source-only completion: **100%**. This package contains six inert PDF editions and full layout-preserving extracted text for the four requested paper families. It does not assess mathematical claims, proofs, priority, or novelty. No source program was executed or imported.

The per-edition records and PDF/text paths are in `ACQUISITION_MANIFEST.json` and `sources/*/acquisition.json`. Current local copies have byte counts, SHA-256, and MD5. New HTTP requests retain requested and final URLs, timestamps, status, raw headers, curl metadata, and literal failure evidence.

| Source edition | PDF location | Provenance qualification |
| --- | --- | --- |
| KS1998 author-hosted journal copy | `sources/KS1998_author/historical.pdf` | Reused frozen continuation primary copy, directly matches native historical pin. |
| BHS2012 arXiv 1202.4037v1 | `sources/BHS2012_arxiv_v1/historical.pdf` | Reused frozen continuation primary copy, directly matches native historical pin. |
| BHS2012 author 235.pdf | `sources/BHS2012_author/historical.pdf` | Reused frozen continuation primary copy, directly matches native historical pin; separate from arXiv v1. |
| HSS2014 arXiv 1403.7505v2 | `sources/HSS2014_arxiv_v2/retrieved.pdf` | Fresh HTTP 200, exact historical native byte/SHA-256 match; version banner checked. |
| HLSS2018 arXiv 1702.02894v2 | `sources/HLSS2018_arxiv_v2/retrieved.pdf` | Fresh HTTP 200, exact historical native byte/SHA-256 match; version banner checked. |
| HLSS2018 published author copy | `sources/HLSS2018_published_author_fallback/retrieved.pdf` | Fresh HTTP 200, 42 pages including publisher cover material, separately pinned; journal front matter qualifies the edition. Full notes retained without interpretation. |

The native archive tree contains reference manifests but lacks the referenced PDF payloads. The three KS/BHS copies therefore come from the independently frozen continuation packet and were checked directly against native manifest pins. Historical final URL/status/headers and precise retrieval times absent from the native manifests are explicitly unavailable; they are not inferred. Its manifests are copied under `native-reference-manifests/`.

The author list at <https://my.vanderbilt.edu/edsaff/research-articles/> identifies item 266 and links to the `www.math.vanderbilt.edu` author PDF path. That requested hostname failed TLS hostname verification. The literal failed request remains under `sources/HLSS2018_published_author/`. The same official author path at the native-manifest-documented primary hostname, <https://math.vanderbilt.edu/saffeb/texts/266.pdf>, succeeded with normal certificate validation. The published author copy has no historical native hash and is not relabelled as arXiv v2.

`FREEZE_MANIFEST.json` inventories every payload file and directory, including hidden/empty entries, modes, symlink targets, hardlink groups, byte counts and hashes. It explicitly reserves the manifest and terminal names to avoid self-reference. `TERMINAL.json` pins the inventory and declares the exact finite entry set; the terminal's SHA-256 is reported outside the package. No Git/index/native-source writes, commit, push, release, or external communication were performed by this acquisition task.
