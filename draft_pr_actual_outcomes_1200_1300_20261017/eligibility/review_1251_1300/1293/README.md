# A bounded spectral criterion for almost-everywhere independence

Problem 2100702 / AMR-020-0702. This report is accepted only within the explicit measure-theoretic and quantization hypotheses in the full proof. It makes no novelty claim and does not establish a resolution of the unrestricted source problem.

## Accepted result

Let F be a smooth map from a Hausdorff, second-countable smooth 2n-dimensional manifold to R^n, and let nu be a smooth everywhere-positive volume density. Suppose its pushforward is locally finite. If C is the set where rank(dF) is less than n, the Lebesgue decomposition is exactly

- Absolutely continuous part: the pushforward of nu restricted to the regular set
- Singular part: the pushforward of nu restricted to C

Thus the pushforward is absolutely continuous if and only if F has full rank almost everywhere. For finite total volume, the singular mass equals nu(C). The proof includes Sard's theorem, Borel measurability of the critical-value set, submersion charts, Fubini and the uniqueness of Lebesgue decomposition.

The conditional spectral criterion assumes an independently available, rank-free joint Weyl law for multiplicity-weighted joint eigenvalue measures. In the standard compact Kähler application, a positive prequantum line bundle and exactly commuting self-adjoint scalar Berezin–Toeplitz families with O(1/k) operator-norm perturbations give the required limit. The probability measure converges to the pushforward of normalized Liouville volume, and its singular mass is the critical-volume fraction.

The complete telescope argument, scalar product and trace estimates, normalized trace error bound, compact spectral support and Stone–Weierstrass extension are retained. The imported estimates are limited to the cited scalar quantization setting; no full-rank hypothesis is imported to derive the joint law. Ma–Marinescu's positive-prequantum framework avoids treating an older very-ample convention as an unrestricted theorem.

## Scope limits

The result concerns the exact asymptotic limiting measure and joint multiplicities. It does not settle arbitrary semiclassical operators, infer multiplicities from unweighted spectra, decide independence from finite data, provide a stability guarantee, or detect every rank-deficient point. No claim is made that every classical commuting tuple admits an exactly commuting quantization. The original source does not specify a multiplicity convention. No exhaustive current-literature status or novelty finding is claimed.

## Contents

- [Full authored proof](PROOF.md)
- [Mathematical audit](AUDIT.md)
- [Accepted scope and limitations](ACCEPTANCE.json)
- [Public bibliography and source verification metadata](SOURCE_PINS.json)
- [Aggregate verification results](CHECK_RESULTS.json)
- [Public file manifest](MANIFEST.json)

The full accepted proof, audit, acceptance and public source metadata are reproduced byte-for-byte. The acceptance's no-publication statements record the earlier audit stage. The manifest binds all six other public files; the public directory is the complete seven-file publication payload.

The existing input, source and artifact checks passed again under Python normal, -O and -OO modes. These are integrity checks supporting an analytical audit, not formal proof verification or external human peer review. Direct source-inspection descriptions belong to the preceding audit; this preparation matched the pinned bytes without new source retrievals.

Only authored mathematics and public bibliographic or aggregate verification metadata are included. Copied source documents, source extracts, datasets, screenshots, checking scripts and private coordination material are excluded.

## Primary sources

The originating question is Vũ Ngọc's Problem 7.2, p. 36, in Bolsinov, Matveev, Miranda and Tabachnikov, Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems, [arXiv:1804.03737v2](https://arxiv.org/pdf/1804.03737v2). It is Problem 6.2, p. 46, in v1.

The scalar quantization inputs are attributed precisely in the proof to [Schlichenmaier's review](https://arxiv.org/pdf/1003.2523v1), [Bordemann–Meinrenken–Schlichenmaier](https://arxiv.org/pdf/hep-th/9309134v3), and [Ma–Marinescu](https://arxiv.org/pdf/1009.4405v1). Source metadata gives versioned URLs, hashes, byte counts and the audited locations.
