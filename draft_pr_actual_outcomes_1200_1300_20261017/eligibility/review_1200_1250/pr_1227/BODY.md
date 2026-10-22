## Accepted prior asymptotic bounds and exact constant certificate

This draft adds the complete AI-assisted, unrefereed authored audit for 2355 / EP-872, the primitive-set saturation game on {2,...,n}.

- Jonas Silva and GPT 5.5 Pro's Prolonger-first lower constant 1/2 is accepted with an explicit activation-legality clarification separating earlier Prolonger and Shortener moves. Buddhdev's earlier 1/8 proof is retained and accepted as well.
- Om Buddhdev's integral upper theorem limsup L_P(n)/n<=W4/2 is accepted with the explicit queued-prime matching clarification, where W4=1-J1+J2-J3+J4 and the density and simplex integrals are fully defined in the audit.
- An independently authored exact rational certificate proves W4/2<0.189741239716434<0.19, so L_P(n)<0.19n for all sufficiently large n. The upper strategy also extends to Shortener first by the checked turn count. No effective finite threshold or transfer of the 1/2 lower bound to Shortener first is claimed.
- The manuscript's tighter decimal 0.1897123371 and narrow numerical intervals were not independently replayed or certified. Overlap with the wider audit intervals does not certify them.
- The n(log log n)^2/log n lower scale remains conditional on both strategy-generated safe-edge hypotheses, retaining all allowed replies including unscored edge deletions. The unrestricted safe-edge version is false. The weighted obstruction and arithmetic K4 example are retained.
- Whether the game length is linear or sublinear remains unresolved by this work. No equality of starting-player values, exact order or optimality claim is made.

AUDIT.md retains the complete seven-section written reconstruction, all mathematical corrections and limitations, both lower-bound strategies, the full envelope/moment/prime-rounding/sieve upper argument, the conditional potentials and formalization boundary. PROOF.md retains the complete independently authored rational certificate proof: exact cells and reciprocal breakpoints, logarithm series and remainder, integer rounding, simplex containments, the no-carry convolution proof, and the exact rational upper endpoint. No large raw coefficient arrays are included.

Primary written sources: Paul Erdős, Some of my forgotten problems in number theory, Hardy-Ramanujan Journal 15 (1992), printed page 47, https://hrj.episciences.org/125 ; Om Buddhdev, Improved Bounds for the Primitive-Set Saturation Game (Erdos Problem 872), manuscript dated April 21, 2026, https://www.sensho.xyz/papers/erdos-872.pdf ; Jonas Silva and GPT 5.5 Pro, A Dyadic Semiprime Lower Bound for the Primitive-Set Saturation Game, https://github.com/jonaslsaa/maths/blob/main/872.pdf .

The PNT, Mertens reciprocal-prime estimate, Chebyshev bound and fixed-r almost-prime estimates remain explicit classical dependencies. No full dependency-closure certification is claimed. Complete Buddhdev and Silva/GPT source texts were read in the original audit, with the specified critical pages visually inspected; only the original Erdős target passage was audited. Historical PDF dates, reported submission and website hosting do not establish peer review. No author code, numerical certificate or Lean project was executed, and no end-to-end formal replay is claimed.

## Distribution and verification

Exactly eight authored prose and public-metadata files are added under attempts/2355. No copied source PDFs/text/images, raw datasets, coefficient arrays, executable code, raw calculation outputs, private sources, private personal data or private coordination material are distributed. Necessary mathematical formulas, exact fractions and finite examples are authored proof content. This is not a computational reproduction package.

Historical normal/-O/-OO exact-arithmetic runs agreed byte-for-byte and certify one analytic constant, not a finite-n game theorem or the tighter author decimal. Code and receipt references are explicitly historical private verification. VERIFICATION.json records the bounded scope and public byte identities. No mathematical program, source retrieval or source-body inspection was repeated during editorial preparation. Hashes authenticate bytes and packaging; they do not prove the mathematics.

Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, formal certification, novelty, priority or universal consensus. QUEUE.md and unrelated paths remain unchanged. Draft publication only; no merge, release or DOI creation.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,501 bytes; SHA-256 `be315b769b06b6b17b9c65b58f47b5f12609713cd5649c07db768c0c438a7e8a`.
- `ACCEPTANCE.md`: 6,475 bytes; SHA-256 `da0f428022c22ab377e93f5b1a17b374d4d39b3de1a00482dc1f92202ae03e4e`.
- `AUDIT.md`: 33,832 bytes; SHA-256 `d85496e8205d62cfaabe2b60c6f4db7155f026b51da344882d97f4375dd10f71`.
- `MANIFEST.json`: 1,339 bytes; SHA-256 `61a9b91b137e522fd10d0c6666f7639772a13503fd0e37fdb408079e3c121df2`.
- `PROOF.md`: 5,326 bytes; SHA-256 `fd1a99a72562a5d446c21be3a8faa6e6fde73beb5e7739fae92008e0147be9b5`.
- `README.md`: 6,148 bytes; SHA-256 `0dc13dab8c64d6c6921a33524a6be5ba862761bc07870538ffa18e2c94e29ddf`.
- `SOURCES.json`: 7,895 bytes; SHA-256 `782a2077da043f2cde5cb512726561a7594cde4d4aef2832baa5a0c27e508861`.
- `VERIFICATION.json`: 3,535 bytes; SHA-256 `b0924659240eb213c6455ddb8c4ce920fe2f56011b49290774d670f5376ebfd0`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.
