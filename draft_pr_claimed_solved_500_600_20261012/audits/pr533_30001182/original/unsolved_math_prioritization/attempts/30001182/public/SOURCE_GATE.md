# Source, scope, and prior-work gate

Problem **30001182 / OWR-3392-009**, rank 559. Checked 2026-10-04.

## Catalogue identity

The [requested catalogue URL](https://www.unsolvedmath.com/problems/30001182) was attempted using the web reader and direct HTTP. The web reader could not open it; direct HTTP returned 403. The matching record was recovered from the public [UnsolvedMath distribution](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json), immutable revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`.

The existing local public-distribution copy was checked against the Hugging Face tree metadata at that exact revision: its 69,291,427 bytes and SHA-256 `37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252` agree with the advertised LFS object. Only the matching target record was extracted for this investigation. No dataset copy belongs to the public packet.

The ID, secondary ID, title, date, and source DOI match the assignment. The record asks whether Liebscher's proposed extremal-exchangeable definition depends on the ambient algebra. Its generated open label, literature assessment, and corrected-statement verification label are discovery aids only, not evidence of truth, open status, or historical novelty.

## Primary source and mathematical conventions

The complete [official Oberwolfach report PDF](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1) was downloaded and its relevant complete contribution read: Volkmar Liebscher, “On Quantum Independence,” printed pp. 540–541, in *Mini-Workshop: Product Systems and Independence in Quantum Dynamics*, OWR 09/2009, pp. 493–548, [DOI 10.4171/OWR/2009/09](https://doi.org/10.4171/OWR/2009/09). The complete printed p. 540 was visually inspected, including both diagrams, the definition, and item (1). The publisher's [article page](https://ems.press/journals/owr/articles/3392) identifies the report and publication date.

The source definition demands equality of two states on B*C: the ordinary joint law under φ and the law obtained by putting B into copy 1 and C into copy 2 under an extremal exchangeable state. The ambient free product is unital. The source does not impose faithful states, tracial states, distinct subalgebras, a fixed-marginal convex slice, or trivial tail algebra. Those omissions matter. The proof preserves the entire joint law and gives distinct proper B,C with scalar intersection; its upstairs witness even has the prescribed full ambient marginal.

Item (1) gives a possible failure of extreme-state lifting as a reason for caution. This must be separated from loss of extremality on restriction. PROOF.md proves genuine ambient dependence by a finite-dimensional state-preserving inclusion and additionally gives a separate algebraic polynomial/Laurent-polynomial example with no positive extension. It does not misidentify the first example as non-lifting. The contextual C*-compactness observation is carefully separated from the unrestricted algebraic example.

The other numbered questions on p. 541 are not bundled into catalogue ID 30001182 and are not claimed solved. In particular the note makes no assertion for a reformulated normal W*-free-product definition, faithful-only definition, or fixed-marginal extremality.

## Later primary literature and credit

The complete author preprint [Dykema–Köstler–Williams, arXiv:1305.7293v3](https://arxiv.org/abs/1305.7293v3) was downloaded. The unversioned PDF was compared byte-for-byte with the explicitly versioned [v3 PDF](https://arxiv.org/pdf/1305.7293v3); they agree. The arXiv record lists v3 (22 September 2014) as latest. The supplied PDF has a later typesetting timestamp (9 August 2021) in its running header; the source hash pins the actual inspected bytes rather than interpreting that timestamp as a new mathematical revision.

The entirety of Proposition 8.7 and its proof, spanning preprint pp. 32–33, was read and visually inspected. Theorem 8.1 and its proof, Proposition 5.4.3 and its proof, the distinction between ordinary and quantum symmetric states, and the following fixed-marginal statement (Theorem 8.9) were read. Proposition 8.7 provides the established folding/maximal-amalgamation mechanism; Theorem 8.1 makes the relevant relation with ordinary symmetric-state extremality explicit. The proof packet gives a direct elementary purity proof, so it does not depend on the classification theorem, its tail-algebra setup, or any uninspected long proof.

The journal article is *Transactions of the American Mathematical Society* 369 (2017), 645–679, [DOI 10.1090/tran6661](https://doi.org/10.1090/tran6661). The year and pages also appear in the author's [publication CV](https://artsci.tamu.edu/mathematics/_files/_docs/faculty-docs/k-dykema-cv.pdf). The DOI endpoint could not be opened by the web reader during this check; the full proof was obtained from the author's arXiv version.

Targeted searches included the exact catalogue title, “Liebscher quantum independence extremal,” “extremal exchangeable free product states,” “independence maximal amalgamation,” and “symmetric states restriction extreme free product.” They located the above established mechanism but did not identify a prior paper expressly presenting this exact ambient-dependence counterexample or resolving item (1). This bounded negative search is not proof of novelty. The packet explicitly makes no historical novelty claim and gives credit to the known mechanism.

## Actual repository and prior-attempt checks

The following read-only checks of [AlecKriebel/Math](https://github.com/AlecKriebel/Math) were performed before writing the candidate:

- The actual `unsolved_math_prioritization/QUEUE.md` was fetched. Its blob SHA was `c87c275c638939b8008fd58db80657491d14971e`. The matching rank-559 row read `queued`, `0/5`, with blank findings.
- Direct fetch of `unsolved_math_prioritization/attempts/30001182/README.md` returned GitHub 404.
- Code searches for `30001182` and `Liebscher` returned no matches.
- Pull-request searches for `30001182` and `3392-009`, with state `all`, returned no matches. A broader `exchangeable` PR search returned unrelated SIRSN investigations, not this target.
- Commit search for `30001182` returned no matches.
- Branch search for `30001182` returned no matches and no continuation cursor.

Thus no actual prior attempt or target PR was found in these checks. The queue's `queued` label alone was not used as evidence that the target had never been attempted. Code search can be incomplete; this is a bounded, documented prior-attempt check.

## Frozen result and publication scope

Candidate disposition: **claimed_solved, 1/5 substantive author turns**, pending independent adversarial review. The theorem proves that ambient invariance fails, including in the C*-subcategory. A second example verifies the more specific non-lifting concern for unrestricted algebraic *-algebras. The full question as printed is settled by explicit counterexamples within its allowed category; no five-turn exhaustion is needed after a complete result.

All load-bearing counterexample arguments are proved in PROOF.md from positivity, elementary matrix algebra, and the free-product universal property. No deep de Finetti theorem is invoked. Auxiliary exact controls reproduce checks.json. The author manifest freezes only original authored proof, attribution, attempt description, reproducible checker and results. Source PDFs, renders, extracted text, full datasets, raw repository responses, and private context are excluded.

This packet is AI-assisted research. An independent AI-assisted review is still required before repository publication; it is not a substitute for formal certification or human peer review. No remote changes have been made by this author work.
