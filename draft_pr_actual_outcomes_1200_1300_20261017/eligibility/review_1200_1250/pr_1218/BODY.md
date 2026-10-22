## Corrected rigorous partial results

This draft adds an AI-assisted, unrefereed corrected partial-report edition for 30000732 / OWR-1536-002, fast Maker constructions of regular graphs. The full original subexponential-in-d question is unresolved by this work. No novelty, priority, external human peer review or formal certification is claimed.

The independent audit required no-isolated-vertices hypotheses in Proposition 2 and Lemma 6. Its exact patch has been applied to a separate report copy; the pre-editorial corrected identity is 19,703 bytes, SHA-256 a646db384b6598f66d6cdb4f26fbdc93c7b0e288e9ea1e9cc6c25c8f529f081f. The complete original report, apart from those two insertions, appears in PROOF.md. The full original audit and its conditional acceptance are retained in AUDIT.md with explicit framing that the required patch is now applied. The K_2-plus-100-isolates counterexamples are retained. All intended regular applications have d>=1.

The accepted mathematics consists of the exact seed reduction, elementary and conservative counting bounds, and precisely restricted fixed-pool/full-activation and fresh-common-neighbour obstructions. Every written mathematical argument, formula and example is retained. Faster component batching and general adaptive constructions remain possible. The original factor-1/4 versus factor-1/2 observation is a caution about the inspected derivation, not a refutation of the stronger source theorem.

The prior Gebauer clique theorem was inspected and cited, not independently fully proved. Conditional on that theorem, corrected amplification yields only 2^((2/3+o(1))d), still exponential. The other cited prior upper proofs are not independently fully certified either. The bounded literature screen establishes neither present openness nor novelty.

Original problem: https://ems.press/content/serial-article-files/46106, Problem 3.1, printed page 1081. Prior sparse-graph manuscript: https://www.math.tau.ac.il/~krivelev/fastwin.pdf. Clique bound: https://arxiv.org/abs/0909.4362. Size-Ramsey article: https://doi.org/10.1017/S0963548313000151.

## Distribution and evidence

Exactly eight authored prose/metadata files are added. Executable code, raw computational datasets, copied source documents or extracted text, source images, raw search responses and private coordination material are excluded. This is not a computational reproduction package. Historical finite checks are supporting illustrations, not asymptotic proofs. No scholarly-source inspection or mathematical tests were rerun during editorial preparation.

SOURCES.json retains the historical report and audit source metadata, including three fresh PDF identity matches and the unsuccessful HTTP 429 ETH refresh. VERIFICATION.json pins the historical receipts and bounded aggregate scope. ACCEPTANCE.md reproduces the exact applied correction. Neither hashes nor finite check counts establish mathematical truth.

## Exact publication identities

- `ACCEPTANCE.json`: 3,966 bytes; SHA-256 `63206169f398fd99c15499456518cf6871fa2e45553c25ed264d7693554aabf5`.
- `ACCEPTANCE.md`: 6,951 bytes; SHA-256 `7088155ea895fb5f3eaf54ba76337bff07f93774bc62be0d69953c50a2293dde`.
- `AUDIT.md`: 24,337 bytes; SHA-256 `5d9a69e65ff91e6cbef08b0da827c6f88eb09300813b1294f66a1fa6d66a6e95`.
- `MANIFEST.json`: 1,349 bytes; SHA-256 `b753727d65ccf0c7f963a469cd11c3508ec8fe9b4ec37fcde2c8cb6b93671eea`.
- `PROOF.md`: 21,936 bytes; SHA-256 `598f3ef7ff9f0a631c93b11fe47466ac5644377ee39c0525f3a7902d7810bf8b`.
- `README.md`: 4,052 bytes; SHA-256 `68180146ad0ce306e9587da9a7bebe4cea2c53876a2bd24562b1dfed679c1c0f`.
- `SOURCES.json`: 12,694 bytes; SHA-256 `d6cd7c80e0b29a7d731b0c8065b0b77964ed747d76ecb0fa3aa96c1a5b0c02f3`.
- `VERIFICATION.json`: 3,944 bytes; SHA-256 `1301fe4403dfc6e101bd71efcc0826ef5df8b31dd4a5f924d5443eba0676172e`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.
