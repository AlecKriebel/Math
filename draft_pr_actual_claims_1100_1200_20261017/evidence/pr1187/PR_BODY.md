## Accepted restricted-family result

The full EP-509 question remains unresolved. This edition preserves the complete
authored written proofs and independent audit, with no required mathematical
correction and no claim of novelty, priority, an improved general bound, or a
solution of the unrestricted disk-cover problem. The alias is 2304007 /
AMR-022-4007, Hayman's Problem 4.7.

For every compact planar set with finitely many connected components, the
finite/countable closed-disk covering content equals the minimum sum of
circumradii over partitions of those components. The minimum is attained.
Thus a fixed polynomial's bounds 2+epsilon for every epsilon>0 would imply
an attained bound 2, but no such unrestricted estimate is proved here.

For p(z)=(z-a)^n-c, n>=2 and t=|c|, put b=(t+1)^(1/n). The exact content is b
for 0<=t<=1, and min{b,n[(t+1)^(1/n)-(t-1)^(1/n)]/2} for t>1. Degree one has
content 1. With q_n=(1-2/n)^n, the family maximum is
M_n=[2/(1-q_n)]^(1/n)<2, attained at t=(1+q_n)/(1-q_n).
The proof covers the full closed region, countable covers, and every component
partition, without assuming that an optimal covering has rotational symmetry.

For p(z)=z^4-65537/65536, separate component-cover costs sum to more than 9/4,
although one shared disk costs less than 6/5. This is a closed-form analytic
route obstruction with the complete exact inequalities retained. It is not a
counterexample to EP-509. The loss from forbidding cross-component grouping
is unbounded with degree.

## Independent audit, evidence, and historical credit

All original topological, analytic, and general proofs are preserved verbatim,
including the fractional-power integral, disk-map identity, regular-polygon
bound, partition argument, family maximum, and quartic construction. Editorial
scope appendices change no mathematics. These mathematical conclusions rest
on the written proofs, not the finite supplementary tests.

The historical independent checker passed in Python normal, -O, and -OO modes.
It verified 36 candidate members and four external dependencies, exact quartic
arithmetic, seven crossover degrees, a five-variable algebraic identity, and
16,272 finite block-size arithmetic checks. Each run rejected 15 corrupted
scalar certificates and 13 integrity controls. Code, scalar certificates and
raw computational data are not distributed, so those supplementary runs are
not reproducible from this edition alone. Verification hashes establish byte
identity and recorded match results, not mathematical truth. No mathematical
tests or scholarly-source inspection were newly performed for this edition.

[Pommerenke (1960)](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0141/LOG_0031.pdf)
provides the prior 2.59 result and reports a prior 1959 surrounding-contour
obstruction. That earlier construction was not independently retrieved or
reproved, and the report is credited to Pommerenke. It is not a disk-cover
counterexample or an exclusion of other geometric routes. Historical source
inspection covered the relevant printed pages 143 and 147-149.
[Erdős (1961)](https://users.renyi.hu/~p_erdos/1961-22.pdf), printed page 246,
was historically visually inspected for the full target and known bounds.
The known connected-case result remains prior work.
[Hayman's Problem 4.7](https://arxiv.org/abs/1809.07200) supplies the catalog
alias; no fresh full-book audit or literature-wide priority claim is made.

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI mathematical audit; no external human peer review, journal acceptance, or
proof-assistant certification is claimed.

## Narrow publication boundary

Only eight authored-prose/public-verification-metadata files are added under
unsolved_math_prioritization/attempts/2150. No source documents, scans, OCR,
copied source text, code, scalar certificates, raw datasets, private sources,
personal data, or coordination material are included. Original sealed packages,
QUEUE.md, and unrelated repository paths remain unchanged. The exact residual
is to bound the component-partition minimum by 2 for every monic polynomial,
or exhibit a polynomial for which it is greater than 2.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,159 bytes; SHA-256 `538c159523d3a8ae73c9578f89f131553c7aa0c41718bd4440e3c1f2cfc43a9e`.
- `ACCEPTANCE.md`: 4,039 bytes; SHA-256 `a9e3a77949e35e45bd982c37587bb5499d67bdef2c34f43ae5a9b25f3d5d9de8`.
- `AUDIT.md`: 14,470 bytes; SHA-256 `a62e8f380ad6fabfd99e569214dcdeff5e88b0c5db6e3f3d03400895595e348b`.
- `MANIFEST.json`: 2,142 bytes; SHA-256 `7f982f52f9dc495382b76cc08ddf93ca46153436886218b0892432053dd3198f`.
- `PROOF.md`: 15,541 bytes; SHA-256 `19725a9275ffc0e622a44515336775c9e3f6dd79fb3157025b8cdce838c7089f`.
- `README.md`: 4,086 bytes; SHA-256 `fa02c4ca065241d52e8605d33aa6bd8d3d4da3a5eefde676d30af4b0b06d0c6f`.
- `SOURCES.json`: 2,632 bytes; SHA-256 `51afc4cc63fbf96d4724230d313141a90f9278c1fce9db7c7a5107a06b408d43`.
- `VERIFICATION.json`: 4,393 bytes; SHA-256 `6d4d3120a95c9bc42d1afaba142c194b8f2f31c9d45e2ce79706ed0abdb856a4`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

