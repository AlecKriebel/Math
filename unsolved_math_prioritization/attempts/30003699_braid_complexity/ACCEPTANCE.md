# Independent scoped acceptance: problem 30003699, row 1911

Verdict: ACCEPT the exact frozen package as a mathematical audit with an explicit scoped complexity corollary and reproducible finite implementation checks. No substantive mathematical, integrity, replay, or public-projection defect was found. This is not acceptance of a novel algorithm, a new resolution of the original informal question, or a new proof of every cited theorem. This report is external to the frozen package and does not change it.

## Exact object accepted

- Archive: braid_complexity_1911_frozen.zip
- Archive bytes: 70035
- Archive SHA-256: 77a2316ee31ec338881c68e72e098a3b181004aa8828e8e5e698de7fef6c01ae
- Frozen MANIFEST.json SHA-256: 0b8b57a25976d408df4e4b87c487829ac9a59184076618b374e61960d6a3c597
- External receipt SHA-256: 52399392dcec90ee38ff95097f3fa0973a7cd91bc542ca59b11e785a25c87a63
- Frozen inventory: 16 single-link regular files, comprising 15 payloads and the manifest; 161651 total uncompressed bytes.
- Mathematical checker, whole-file SHA-256: 666ba85cdbe3fbc4a3055f1c719b00fd49d6811f4626acc75bd4810100ee4a01

Every receipt entry was independently checked against its full payload bytes, size, and SHA-256. Every archive member was compared byte-for-byte with its frozen counterpart. All seven original allowlisted files are byte-identical, with only the original manifest's filename changed to ORIGINAL_MANIFEST.json. The checker comparison covers the complete module, not selected functions or edited mathematical excerpts. All four Python modules contain zero AST assert nodes.

## Independently executed checks

Both normal and optimized Python executions of replay.py succeeded. Their complete outputs reproduce the corresponding frozen JSON byte-for-byte: all three coefficient routes for n=1,...,18; every Z-route coefficient for n=1,...,60; all 60 leading values; and the claimed exact integer schemas. The underlying unchanged checker also verifies full characteristic identities, full Z palindromy, and nonnegativity, rather than only matching a few illustrative values. Arithmetic is integer/Fraction based, including small-case negative exponents.

Both normal and optimized executions of mutation_tests.py succeeded and reproduce the frozen outputs byte-for-byte. Each mode rejects 19 controls: seven mathematical mutations, six filesystem inventory defects, and six schema/integrity defects. Inventory defects include payload and manifest symlinks, payload and manifest hardlinks, a directory, and a FIFO. Those six tests enforce zero content reads before rejection. Exact-int checks reject booleans and floating-point identifiers; duplicate JSON keys are rejected. The six schema/integrity controls include hash/content tampering and unexpected regular files. Inspection confirms that mathematical mutations and malformed inventories are confined to disposable writable fixtures. No actual sockets are created by these scripts.

The validator lstat-checks the root and the complete flat inventory, including MANIFEST.json, before reading manifest or payload content. It rejects nonregular entries and multiple hardlinks before any content read. This is ordinary local integrity validation, not an adversarial signature or a concurrent-filesystem-race defense; the package accurately states that limitation.

## Independent analytic assessment

The Z recurrence follows from flats indexed by set partitions and the known palindromicity theorem. Reflection gives p(n,i)=r(n,n-1-i)-r(n,i) exactly on the allowed low-degree range; initialization and the excluded central degree are correct. Induction against the existing KL polynomials supplies general correctness, rather than treating finite agreement or reflection alone as sufficient.

The weighted strict-partition-chain majorant is valid. D(1)=1 and D(n)=2 sum S(n,k)D(k) majorize absolute coefficients. Every strict chain extends to a maximal chain; counting weighted endpoint-preserving subchains of all maximal chains gives D(n) <= 2*3^(n-2)*n!*(n-1)!/2^(n-1). Multiple counting makes this an upper bound in the correct direction. Thus coefficients, products, absolute partial sums, and Stirling intermediates have O(N log(N+1)) bits. The dense Z computation uses O(N^3) integer operations and O(N^2) stored integers; conservative schoolbook accounting yields O(N^5 log^2(N+1)) bit time and O(N^3 log(N+1)) storage bits. These claims concern this specified prefix algorithm, not the slower verification routines or optimal complexity.

The explicit task is polynomial in numerical N (or unary input), not in binary input length log N. This distinction is stated correctly. The original question does not supply the computational model, target bound, or coefficient regime needed to claim its wholesale resolution.

Locally retained scholarly text was inspected for the original question, both leading-coefficient formulas, the all-coefficient interpretation, generating-function normalization, and the 2025 enumeration formula. Ferroni-Larson's all-coefficient theorem and odd-rank leading result, Gao-Proudfoot-Yang-Zhang's even-rank leading result, and Proudfoot-Xu-Young's enumeration and published sign correction are credited, not claimed as new. Formula indices, signs, factorials, rank parity, singleton and empty-object normalizations match the reviewed material. The 2018 recurrence attribution is appropriately bounded by the package's stated inspection history; this audit does not independently re-prove or freshly retrieve that paper. No exhaustive literature search or novelty certificate is inferred.

## Classification and public scope

Substantively this is an authored mathematical audit with a proved, explicitly specified complexity corollary, reconstruction of established machinery, and acceptance/verification materials. It contains real mathematical proof work, not merely bibliographic metadata. Its content and scope do not support presenting it as a new research manuscript that resolves the original problem. This classification follows the substance and does not relabel material to evade a publication restriction; this acceptance itself grants no new publication authority.

The 16-file frozen projection contains authored exposition, code, finite computed verification outputs, and integrity metadata. It includes public scholarly titles and URLs but no copied third-party source documents or source-text extracts, dataset/corpus contents, private personal data, private source paths, or private coordination records. The original mathematical checker and authored exposition remain intact. The broad disposition remains PARTLY_SUPERSEDED_SCOPED_UPPER_BOUND_NOT_FULL_RESOLUTION.

No publication, actual socket experiment, or QUEUE edit was performed in this audit. No frozen file was modified. Acceptance is confined to the archive hash above and the explicitly stated analytic and finite-check scope.
