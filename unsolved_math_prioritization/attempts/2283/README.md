# Accepted prior result: equal prime supports of central binomial coefficients

Campaign ID 2283; Erdős Problem 730.

## Result

The prior proof attributed to Liam Price, Tomodovodoo and Will Blair is accepted as a conventional mathematical solution of the original question: there are infinitely many distinct positive integers n < m for which binomial(2n,n) and binomial(2m,m) have the same prime divisors. In fact, infinitely many consecutive pairs occur.

The proof exhibits T=5289, P(x)=42Tx+11 and Q(x)=72Tx+13, and n(x)=P(x)Q(x)−1. The lower asymptotic density of successful positive parameters x is strictly greater than 107/2500. This is density in x, not in n or in all pairs. The positive strictly increasing quadratic n(x) gives an injective bridge to the original statement.

This is an audit of prior work, with no novelty claim. According to the author's public formalization manifest, Liam Price supplied the informal idea, Tomodovodoo an algebraic follow-up, and Will Blair the analytic reconstruction/formalization. The earlier informal argument is publicly described as unadjudicated and the author review as self-assessed. Priority between contributors and an unavailable antecedent manuscript were not independently authenticated.

## What is here

- AUDIT.md: the complete conventional argument, from exact prime-support transitions and branch arithmetic through the Fourier and tail bounds, top-prime analysis, strict density budget, and positive injective bridge.
- FOCUSED_AUDIT.md: an independent full derivation of the fixed-depth Fourier bound and its first-power application, with the separate uniform depth tail.
- ACCEPTANCE.md and ACCEPTANCE.json: exact acceptance and review limits.
- SOURCES.json: selected public citations, byte/hash identities, inspection history and limitations.
- VERIFICATION.json: historical-check and edition-verification scope.
- MANIFEST.json: exact public membership and hashes of the other seven files.

All general analytic constants and written derivations are retained. Executable code, source bodies, datasets, raw finite certificates, numerical toy cases, private sources and private coordination are excluded.

## Essential limits

Acceptance is unrefereed internal AI mathematical review relative to the stated classical Kummer, reciprocal-prime Mertens and fixed-modulus PNT inputs. It is not external human peer review or journal acceptance.

Formal replay is NOT REPRODUCED. No Lean/Lake build, author script or imported third-party program was executed. The imported module closure contains two admitted experimental declarations; bounded static evidence supports their exclusion from the terminal theorem's dependency cone, but no elaborated axiom footprint was independently verified. Import reachability and proof-term dependency are different questions.

The actual pinned PNT dependency is ajirving/PrimeNumberTheoremAnd at 769d3b81fbff001d9fa7028df0168a8e546cf692, with current terminal moduli 1,7,14. Older repository/revision and exact-modulus documentation is stale. The source's generic fixed-modulus PNT theorem covers the current uses.

Palomar acceptance remains UNVERIFIED: HTTP 403 responses were respected. No registry approval, current community-wide resolution, exhaustive novelty search, or independent formal certificate is claimed.

## Public sources

[Will Blair's complete proof at the audited pin](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/proof.md) and [formalization attribution/status](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/formalization.yaml).

[Erdős, Graham, Ruzsa and Straus, On the prime factors of C(2n,n), Math. Comp. 29 (1975)](https://www.renyi.hu/~p_erdos/1975-27.pdf), original question at printed page 91.
