# Source, identity, literature, and prior-attempt audit

Inspection date: 2026-10-05 UTC. This is a bounded inspection record, not a claim that the literature was exhaustively searched or that the retained partials are novel.

## Exact target and primary source

The requested [problem page](https://www.unsolvedmath.com/problems/30006060) was attempted first. The web fetch failed; a direct HTTP request returned 403. Its live text and current status were not verified. The supplied problem record identifies 30006060 / OWR-14298592-014 and the exact four-block words stated in this packet. Its UTF-8 statement hash is 3c062a84a1760d6c102cd840c55082a885e929feff4841eb7a6a4987f3b80043, matching the catalog's statement_hash exactly. Catalog rank 804 is queue metadata, not mathematical evidence.

The authoritative report was obtained from the [EMS publisher PDF](https://ems.press/content/serial-article-files/50050?nt=1), DOI [10.4171/OWR/2024/43](https://doi.org/10.4171/OWR/2024/43). The report has 40 pages, printed pp. 2511–2550. The contribution begins on printed p. 2543. Its definition on pp. 2543–2544 is smooth oriented concordance; its displayed pair is on p. 2545 (PDF page 35, one-based), visually inspected as well as extracted. Both superscript/subscript word transcriptions were checked. No mirrors appear in the inputs. The report explains that concordance of this non-isotopic positive-braid pair would contradict Slice–Ribbon.

The report concerns the September 22–27, 2024 workshop; the PDF was produced and the report published in 2025. These are compatible dates. The supplied status/triage language was not treated as a proof or as independently current.

## Load-bearing mathematical sources

- Julia Collins, [An algorithm for computing the Seifert matrix of a link from a braid representation](https://webhomes.maths.ed.ac.uk/~v1ranick/julia/SeifertMatrix.pdf), November 2007 with July 2013 corrections. Read Sections 3.1–3.3, including the positive diagonal -1, same-column, and interleaving rules. The executable implementation in this packet is newly authored; no external program was installed or executed.
- Sebastian Baader, [Positive braids of maximal signature](https://ems.press/content/serial-article-files/44257?nt=1). Section 2's brick-basis and symmetrized-form description checked. The whole-circle tree-phase proof in this packet is written out explicitly rather than delegated to source wording.
- Paula Truöl, [The upsilon invariant at 1 of 3-braid knots, v2](https://arxiv.org/abs/2108.03674v2), accepted version; published Algebraic & Geometric Topology 23 (2023), 3763–3804. Proposition 3.2(C), Lemma 4.11 and the block-minimality corollary checked. Its formula concerns Upsilon at 1, not the entire function.
- Kenneth L. Baker, [A note on the concordance of fibered knots](https://arxiv.org/abs/1409.7646), revised manuscript; published Journal of Topology 9 (2016), 1–4. Lemma 2 and Theorem 3 read with proof and hypotheses. They obstruct ribbon/homotopy-ribbon behavior, not arbitrary smooth concordance.
- Ozsváth–Stipsicz–Szabó, [Concordance homomorphisms from knot Floer homology, v3](https://arxiv.org/abs/1407.1795v3). The initial slope, quasi-alternating formula, and L-space coefficient restriction were checked. The full complex is not reconstructed from the Alexander polynomial for these inputs.
- Anthony Conway, [The Levine–Tristram signature: a survey](https://arxiv.org/abs/1903.04477), Section 2.4. The distinction between raw singular values and legitimate concordance-invariant values is retained. An author-site download yielded HTML instead of PDF; the arXiv route supplied the actual PDF.
- Jacob Rasmussen, [Khovanov homology and the slice genus](https://arxiv.org/abs/math/0402131), positive-knot formula, used only to obtain s=2g=16 here.

Classical Burau, Fox–Milnor, branched-double-cover presentation/linking-pairing, and Arf formulas are credited standard inputs; the packet claims no original version of those theorems. Computed certificates and their logical limitations are given in full.

## Current literature pass

The [author's research page](https://paulatruoel.github.io/research.html), last updated September 2026, was inspected. Targeted searches used the exact report DOI, positive three-braid concordance terms, the author, and the explicit exponent pattern. No resolution of this particular pair was located. This is a negative search result, not a theorem of historical openness.

Two newer, potentially confusing developments were specifically checked:

- Zhechi Cheng and Matthew Hedden, [Knot Floer homology of positive braids, v2](https://arxiv.org/abs/2504.13005v2), July 14, 2026. This revision adds Hedden and overhauls the 2025 version. The main result gives a next-to-top term, not a full concordance detector for the present pair.
- Maciej Borodzik and Paula Truöl, [Non-complex cobordisms between quasipositive knots, v3](https://arxiv.org/abs/2504.04894v3), accepted version December 24, 2025, published 2026. Its concordant strongly quasipositive examples are explicitly nonfibered. They do not resolve the positive-braid pair, and Question 1.5 still distinguishes the fibered situation.

Other search hits on braid-positive surgery diagrams, T-positive links, and the Conway knot concern different results. None was used to infer a solution to the target. No author/editor contact or unpublished-result claim was made.

## Prior repository attempt check

Repository: [AlecKriebel/Math](https://github.com/AlecKriebel/Math). Main was observed at fb079fe5a515ee449967b93db4925919300f3fb3.

- Exact code search for 30006060: no returned results.
- Code search for concordance: no returned results.
- Exact PR search for 30006060, all states: no returned results.
- Broader PR search for the target number, report label, positive braid, and three-braid returned only unrelated positive-link, surface-braid, semi-brace and mutation work.
- Branch search for 30006060 and concordance: no results. A braid-name search was paginated to exhaustion and returned unrelated surface-braid and braided-Thompson branches.
- Commit search for 30006060, the exact report label, and positive/braid terms: no results.
- The target attempts directory on the observed main commit returned 404.

Two full recursive tree requests encountered transport closure, so this audit does not claim an exhaustive tree-content inspection or review of every unrelated branch. The completed exact artifact and history searches supplied no evidence of an actual earlier attempt; generic triage and queue presence are not counted as earlier mathematical work.

## Publication boundary

provenance.json lists public source URLs, hashes, byte counts, and inspection scope. Imported catalogs and research corpora were inspected locally only; the record includes their hashes and byte counts, not their contents. The frozen packet excludes PDFs, source text extracts, page images, downloaded programs, complete source records, and private coordination. Everything retained is authored mathematics/code, calculated output, or public verification metadata.
