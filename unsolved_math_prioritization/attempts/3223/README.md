# Cycle continuous antichains

## Result and scope

Problem 3223 / OPG-323 has a known positive resolution due to Robert Šámal. The published result gives an infinite antichain of finite simple cubic connected bridgeless graphs under cycle-continuous edge functions. This report makes no claim of a new theorem or priority.

A cycle-continuous function from the edges of G to the edges of H must pull every element of the binary cycle space of H back into the binary cycle space of G. These cycle spaces consist of all even-degree edge sets, including the empty set and disconnected unions of circuits. They are not restricted to single connected circuits. The exact definition and literature match are in [ACCEPTANCE.md](ACCEPTANCE.md).

The source is Robert Šámal, *Cycle-Continuous Mappings—Order Structure*, Journal of Graph Theory 85(1), 56–73 (May 2017), [DOI 10.1002/jgt.22047](https://doi.org/10.1002/jgt.22047), first published online 12 June 2016. Full-text inspection used [arXiv:1212.6909v1](https://arxiv.org/abs/1212.6909v1), submitted 31 December 2012. Theorem 1.3 (PDF page 2) and Corollary 3.5 (PDF page 9) are locators in that 12-page version. The final journal PDF was unavailable; only its publisher metadata and abstract were verified.

## Contents

- [PATH_PROOF.md](PATH_PROOF.md) gives the complete path-specific flow-gluing, localization, no-collapse, and no-folding argument. Its proof text is preserved byte-for-byte from the accepted explanatory audit.
- [ACCEPTANCE.md](ACCEPTANCE.md) records the definition match, mathematical dependency audit, conclusion, and limits.
- [FINITE_CHECK_SUMMARY.json](FINITE_CHECK_SUMMARY.json) reports aggregate results for the two manually transcribed Blanuša graphs, including all 54 single-edge-deletion flow checks and separate cut and perfect-matching checks.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) records source titles, public URLs, version-specific locators, PDF hash and size, and the observed retrieval and inspection history.
- [ARTIFACT_MANIFEST.json](ARTIFACT_MANIFEST.json) inventories the other five files by exact byte counts and SHA-256 hashes. The manifest excludes itself to avoid a self-referential hash.

## Verification and review limits

This is an AI-assisted explanatory proof and mathematical audit. It has received no external human review and no formal certification or proof-assistant verification. References to independent checking mean an explanatory derivation or distinct finite-check algorithms, not external human review. File-integrity checks establish byte identity and inventory coverage only; they do not certify mathematical truth.

The finite computations concern exactly the two manually transcribed 18-vertex, 27-edge Blanuša graphs. They do not replay a general small-snark classification, certify the paper's general tree-localization lemma, or audit the complete countable-poset theorem. No source-author code was executed. The source figures, raw graph adjacency lists, flow witnesses, scripts, copied source documents, source images, dataset contents, and private coordination material are excluded from this report. As a result, this public packet is not a self-contained computational reproducibility bundle.

The large antichain graphs have nontrivial 3-edge cuts. No result for an antichain restricted to cyclically 4- or 5-edge-connected graphs is claimed. The paper's broader countable-poset result is cited as literature context only, and its full proof is outside the independently expanded path argument.
