# Sources and public verification metadata

12 October 2026 UTC. This file contains only public bibliographic, retrieval, inspection, and input-identity metadata. No scholarly source text, PDF, image, graph6 records, or generated collection is included.

## Signed degree-list dependency

Thomas Schweser and Michael Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/abs/1507.04569v1), submitted 16 July 2015. [Primary PDF](https://arxiv.org/pdf/1507.04569v1); [primary HTML](https://arxiv.org/html/1507.04569v1).

The 21-page primary PDF has 202,056 bytes and SHA-256 `727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`.

The external mathematical contract is Theorem 2.1(a),(c),(e), pp. 7–8, and Lemma 2.4, pp. 13–14, using v1 numbering. Graph, degree, sign, and list conventions occur on pp. 2–6; the uncolorable-pair definition is on p. 7. Theorem 2.1’s proof on pp. 8–12 and Lemma 2.4’s proof were read. All 21 pages were read in extracted text; pages 8, 12, and 13 were also rendered and visually inspected. Lemma 2.2(b), p. 12, was inspected as background; its proof is left to the reader by the manuscript and it is not a premise of the accepted result.

The source theorem remains external. Complete-source inspection and application review are not an independent reproof. The journal identity is Discrete Mathematics 340(5), 882–891 (2017), [DOI 10.1016/j.disc.2017.01.007](https://doi.org/10.1016/j.disc.2017.01.007). Journal full text was not inspected, and journal publication metadata do not replace v1 theorem locators.

### Recorded retrieval and inspection history

- 2026-10-12T09:58:17Z: web open, [public source](https://arxiv.org/abs/1507.04569v1). Version-specific title, authors, submission date, and primary-source identity verified.
- 2026-10-12T09:58:17Z: web open, [public source](https://arxiv.org/pdf/1507.04569v1). Cache miss; no new download claimed.
- 2026-10-12T09:58:38Z: web open, [public source](https://arxiv.org/html/1507.04569v1). Primary HTML retrieved; added theorem statements cross-checked.
- 2026-10-12T09:58:38Z: web open, [public source](https://arxiv.org/pdf/1507.04569). Primary 21-page PDF text retrieved.
- 2026-10-12T09:59:24Z: web screenshot, [public source](https://arxiv.org/pdf/1507.04569). Screenshots of pages 8, 12, and 13 failed with cache miss. Switched to local rendering of the pinned source bytes.
- 2026-10-12T09:59:44Z: local PDF render and image inspection, [public source](https://arxiv.org/pdf/1507.04569v1). Pages 8, 12, and 13 visually inspected from the pinned PDF.

The inspected PDF reused previously downloaded version-specific bytes; their hash and size were independently rechecked. No new version-specific PDF download is claimed after the recorded cache miss.

## Clebsch background

Matt DeVos and Robert Šámal, [High-girth cubic graphs are homomorphic to the Clebsch graph, arXiv:math/0602580v2](https://arxiv.org/abs/math/0602580v2). This is background for the cubic-to-Clebsch formulation. It is not a source for a novelty claim, a comprehensive literature review, or a current open-problem-status claim.

## Public catalog identities

Provider: [House of Graphs cubic graphs](https://houseofgraphs.org/Cubic). These are the previously retrieved connected triangle-free cubic graph6 catalogs used by the finite testing. No new retrieval was made in this round. Supplied-record coverage was exhaustively checked; completeness up to isomorphism and nonisomorphism remain provider assertions.

- Order 6: 1 records; 5 bytes; SHA-256 `71f49f06c24df520ed960e6c438423ac3bc1bc06f89ba390f8b5e7ed0d9f36d4`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.06.04.g6).
- Order 8: 2 records; 14 bytes; SHA-256 `6fea93e58c75b760f24e58ea93673a627075c42d7ef31f1125bfb25e8dec5ee4`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.08.04.g6).
- Order 10: 6 records; 60 bytes; SHA-256 `01324766dc1dfd3b64a9ab130f4162684e9df86f7fee664e6c904e0471eff285`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.10.04.g6).
- Order 12: 22 records; 286 bytes; SHA-256 `3b231b32b339de0a94f8c8237d58aeaac5a2844f8e6ff8c6c666d83b2f9e4803`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.12.04.g6).
- Order 14: 110 records; 1,980 bytes; SHA-256 `6eb7b8060b76eed5c4473bbdd8af330baa9dcbe541a59808691d0941fdd8fe99`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.14.04.g6).
- Order 16: 792 records; 17,424 bytes; SHA-256 `23311537ce71087a7b39a6fe02242244a0ff4b687058c435c40ddff7f1388bb6`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.16.04.g6).
- Order 18: 7,805 records; 218,540 bytes; SHA-256 `ff31e77fd019b74d2cab1427fb2408e8d66964e0f5a6d0042db1eaa82f12ad7a`; [exact public download](https://houseofgraphs.org/data/cubics/Generated_graphs.18.04.g6).

## Authored generation and retained provenance

The seven generated batches used fixed-seed bipartite configuration pairing, prescribed internal matchings, and the standard 64-bit Mersenne Twister engine. Labeled duplicates were rejected within each batch; isomorphic duplicates were not removed. Their orders differ, so within-batch distinctness gives distinctness across these batches. These are bounded labeled samples, not uniform samples of isomorphism classes. Exact seeds are retained as reproducibility parameters, not as claims that the undistributed implementation or streams are available here.

- (|X|,|Y|; |M_X|,|M_Y|)=(8,6; 4,1): 10,000 graphs, seed 1752303.
- (|X|,|Y|; |M_X|,|M_Y|)=(9,7; 4,1): 10,000 graphs, seed 1752316.
- (|X|,|Y|; |M_X|,|M_Y|)=(14,10; 7,1): 100,000 graphs, seed 1752324.
- (|X|,|Y|; |M_X|,|M_Y|)=(15,11; 7,1): 100,000 graphs, seed 1752326.
- (|X|,|Y|; |M_X|,|M_Y|)=(20,14; 10,1): 100,000 graphs, seed 1752334.
- (|X|,|Y|; |M_X|,|M_Y|)=(12,10; 4,1): 100,000 graphs, seed 1752322.
- (|X|,|Y|; |M_X|,|M_Y|)=(10,10; 2,2): 100,000 graphs, seed 1752344.

Recorded software versions: GNU C++ compiler 14.2.0 (Debian 14.2.0-19), Python 3.12.14, gzip 1.13. Byte-identical generation depends on the recorded C++ standard-library implementation. Independent positive-certificate validation does not depend on replaying that generation. No executable, build recipe, original collection identity, or raw stream is distributed.

The two obstruction graphs are authored explicit constructions. Their literal neighborhoods, attachments, elementary contradiction, unrestricted label vectors, and two displayed maximum-cut label vectors are included in the proof and audit prose. They are not copied catalog records.
