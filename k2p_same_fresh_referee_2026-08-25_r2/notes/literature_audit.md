# Dated primary-source literature audit

Audit date: 2026-08-26 (America/Los_Angeles). This is targeted source and
novelty-search evidence, not an exhaustive priority guarantee. No person was
contacted.

## Huber et al. (2025)

- Katharina T. Huber, Leo van Iersel, Mark Jones, Vincent Moulton, and Leonie
  Veenema-Nipius, *When Are Quarnets Sufficient to Reconstruct Semi-Directed
  Phylogenetic Networks?*, Bulletin of Mathematical Biology 87:136.
- Primary identifier: DOI
  `10.1007/s11538-025-01510-5`,
  <https://doi.org/10.1007/s11538-025-01510-5>.
- Publisher PDF retrieved 2026-08-26; SHA-256
  `ad2cde93997e87b5ad270836524ea73de193dabf0b1e8c81e8179782af0292af`.
- Exact load-bearing check: Lemma 4.2 and Figure 8 give the two
  semi-directed level-2 generators used by the submission. The same paper's
  global encoding results support quarnet reconstruction and the blob-tree
  attribution. They do not prove the submission's K2P analytic containment
  theorem.

## Englander et al. (2025/2026 v4)

- Aviva K. Englander, Martin Frohn, Elizabeth Gross, Niels Holtgrefe, Leo van
  Iersel, Mark Jones, and Seth Sullivant, *Identifiability of Phylogenetic
  Level-2 Networks under the Jukes--Cantor Model*.
- Primary identifier: bioRxiv DOI
  `10.1101/2025.04.18.649493`,
  <https://doi.org/10.1101/2025.04.18.649493>; first posted 2025-04-24,
  version 4 revised 2026-07-04.
- The locally archived v4 source XML was rechecked on 2026-08-26 at
  `/Users/alec/Documents/Math/s_tc_jc_landmark_closure/reviews/final_standard_convention/sources/englander_649493v4.source.xml`;
  SHA-256
  `1323dec9322099afb9f49e11554c92d1fe78e4b29c5ee03ba8942690ae2e8c38`.
  A fresh bioRxiv PDF request was rate-limited (HTTP 429), so the archived v4
  XML, not that failed response, is the content authority for this audit.
- Exact load-bearing checks: Propositions 2.9--2.10 give the relevant strict
  quartet Fourier sign separators for JC/K2P; Theorem 2.11 makes different
  displayed-quartet sets disjoint under JC/K2P with positive mixing weights;
  Corollary 2.12 gives tree-of-blobs separation. The paper's full level-2
  topology theorem is JC-only, and the submission does not misuse it as K2P.

## Brits et al. (2026)

- Jari Brits, Niels Holtgrefe, Leo van Iersel, and Samuel Martin, *On
  Tree--Network Distinguishability and Full Identifiability of Phylogenetic
  Networks*.
- Primary identifier: arXiv `2607.12919`,
  <https://arxiv.org/abs/2607.12919>. The package pins v2 (2026-07-29); the
  current primary record was v3, updated 2026-08-25T11:37:51Z, when checked on
  2026-08-26.
- Retrieved v3 PDF SHA-256
  `0b088a4ac9c8e04af8e281f5faddcf842b1a902a53053c0e17a2de3b539af59a`;
  retrieved arXiv API response SHA-256
  `a3f567f18b1ac4cb6ca63505b72057e9c1268ffd8bdcd77087bf1117a0e44049`.
- Exact load-bearing check: Theorem 4.9 still states full separation of
  distinct level-1 semi-directed networks, modulo reticulation placement in
  triangles, for JC, K2P, and K3P on its physical parameter region. The v3
  abstract narrows its separate arbitrary-level tree/network result to JC.
  The present submission relies on Theorem 4.9, not on the narrowed result.

## Conclusion

All three cited primary sources support the precise roles assigned to them.
The only literature defect is freshness: the package bibliography and
supplement identify Brits et al. v2 while v3 became current during release.
That is a nonblocking presentation issue, not a mathematical counterexample.
