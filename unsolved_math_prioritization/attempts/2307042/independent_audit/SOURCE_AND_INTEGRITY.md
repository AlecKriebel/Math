# Source reconciliation and integrity scope

Inspection date: 2026-10-06 UTC.

## Primary mathematical question

The independent reviewer opened the primary arXiv record and complete 256-page PDF of W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, version 1809.07200v2. The reviewer also read the complete Problem 7.42 and its update in the available text extraction and visually inspected both rendered original pages: PDF pages 174--175, printed pages 173--174.

- https://arxiv.org/abs/1809.07200v2
- https://arxiv.org/pdf/1809.07200v2

The source's positive-harmonic upper-envelope definition, base normalization, fixed-pole disc example, and explicit multiply connected extension agree with the author's theorem and its equality-along-a-line interpretation. The notation defects in the source are acknowledged; they are not used to manufacture a counterexample. The later update reports the editors' knowledge in that edition and does not establish present openness.

The inspected local primary PDF has 1,706,228 bytes and SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`. Its bytes are not included in this audit packet. The public primary record was independently reopened; the local PDF hash is a measurement of the inspected available file, not a claim of a second independent binary download.

## Bounded literature check

The reviewer inspected the opening sections, definitions, and main-result statements of the available author-hosted manuscript by H. S. Bear and Wayne Smith, *An Extension of the Schwarz--Pick Lemma*, and the introductory definitions and gradient result of D. A. Herron's *The Harnack and other conformally invariant metrics*. These statements concern Harnack distances and their infinitesimal or mapping properties. They are not substituted for the one-sided envelope or the fixed-kernel line-contact assertion.

- https://math.hawaii.edu/~wayne/mathpapers/Harnack2.pdf
- https://www.jstage.jst.go.jp/article/kodaimath1978/10/1/10_1_9/_pdf/-char/en

The provisional journal fields in the Bear--Smith file were visually present in its extracted opening page; this audit identifies it as an author-hosted manuscript. It does not certify correspondence of all its contents with a later published article. The reviewer did not independently inspect the full 2019 Springer chapter or the full Kargar paper. The unchanged author's source report records its own broader inspections and must not be mistaken for the independent reviewer's inspection history.

Six focused web searches combined the question number, attributed problem authors, Harnack-function terminology, Martin kernels, annuli, contact, and Green lines. No direct prior resolution was independently verified from their results. This limited search establishes neither novelty nor absence of a result from the literature. Nothing in the mathematical acceptance depends on that negative search outcome.

## Input identity and inherited review gate

The author's complete six-file freeze was measured before mathematical review:

- Archive: 11,445 bytes; SHA-256 `a23e5104041c2bd7aaf64e9da505a2d07dbd89b4ac599c23a8f008402cd49e3a`.
- External manifest: 1,476 bytes; SHA-256 `5c61737da81e41aae246c33ee3360a10ea71dfc75a48014cca3c2c519585f65d`.
- Author proof: 9,195 bytes; SHA-256 `88ceb90850cd364d3ef53a17d1c60beebff3a19b650c1af14b06c07c208e41fc`.

The complete paired statement/review record was privately inspected for task selection, rather than relying on a summary field. The statement digest matched `437f00b6ee043726bc9778807c9a7be7303a50d7fcef70c7904a210ae5bddac2`. The complete-pair digest using default Python JSON serialization with sorted keys matched `4c32a01e80e86322bdbb4b996ab6353f454d08436c1c96388850ca9d1717e7d4`. The inherited report contained only source reading and web searching, not a prior mathematical derivation. This audit therefore does not count it as an earlier substantive proof attempt. The authored candidate uses one substantive analytic approach; the kernel, minimality, and separation arguments are components of it.

Only hashes, byte counts, identity/match outcomes, and an authored classification are reported here. No raw corpus records, source text, private filenames, private directory paths, or private coordination contents are included.

## Integrity validation is separate from mathematical review

Every author ZIP entry was checked against the external manifest, the inner manifest, its measured byte count and SHA-256, and the corresponding inspected file. All six entries were regular, non-executable UTF-8 files. The reproduced files under `author/` preserve those exact bytes.

The audit archive uses a closed inventory and an inner manifest excluding itself, with an externally pinned manifest and ZIP. Replay checks enforce exact inventories, unique safe paths, regular non-executable files, byte counts, SHA-256 hashes, strict UTF-8, and duplicate-key-free JSON. They do not import or execute anything from an archive. External input pins are checked before trusting an inventory. Plain execution and optimized Python are both used because integrity checks must not depend on `assert` statements. A relocated extraction verifies that no absolute workspace path is required.

Adversarial replay tests exercise altered content, missing/extra files, duplicate ZIP members, unsafe member paths, symbolic-link entries, changed manifests, and filesystem substitutions. The external validation receipt records actual outcomes after the immutable archive is built; this document describes the scope rather than claiming that a future replay has already run.

These are data-integrity checks only. The analytic proof rests on the independent derivations in `INDEPENDENT_AUDIT.md`; a successful hash check is never described as machine verification of the mathematics.
