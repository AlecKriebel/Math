## Accepted prior original-statement result

The prior EP730 proof is accepted as a conventional mathematical solution:
infinitely many distinct positive n<m have equal prime supports of
binomial(2n,n) and binomial(2m,m). Infinitely many consecutive pairs occur.
This is an audit of prior work, with no new-solution or novelty claim.

As credited by the author's public formalization manifest, Liam Price
provided the informal idea, Tomodovodoo an algebraic follow-up, and Will Blair
the analytic reconstruction/formalization. The author describes review as
self-assessed and the earlier informal argument as unadjudicated. Priority
and unavailable antecedent material were not independently authenticated.

With T=5289, P=42Tx+11, Q=72Tx+13, R=28Tx+5 and S=72Tx+19, the family is

    n(x)=P(x)Q(x)−1=84591927504x²+7076682x+142.

The lower asymptotic density of successful positive parameters x is strictly
greater than 107/2500. This is density in x, not in n or in all pairs. The
positive strictly increasing quadratic makes x -> (n(x),n(x)+1) injective
and completes the original-statement bridge. Equality of prime supports is
not equality of valuations or of central binomial coefficients.

Sources: [Will Blair, complete positive-density proof at the audited pin](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/proof.md),
[public attribution and manuscript status](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/formalization.yaml),
and [Erdős, Graham, Ruzsa and Straus, On the prime factors of C(2n,n),
Math. Comp. 29 (1975), printed p.91](https://www.renyi.hu/~p_erdos/1975-27.pdf).

## Complete proof and independent focused review

AUDIT.md retains the complete general argument: exact Kummer transition,
branch identities and resultant exclusions, valuation and permutation maps,
exact digit deletion, higher-power and transition estimates, fixed-depth
Fourier normalization/completion, fixed-depth prime bands, separate uniform
depth tail, top-prime classification with its ratio hypothesis, both paper
and current implementation analytic routes, strict density margin and the
positive injective bridge.

The final bound is

    S=sum_{r>=1}4^(−r)log((r+2)/(r+1)),
    S<11117760449158646497/89848527388139520000,
    log 2<1123/1620,
    4S+(2/3)log 2<21498408212212214497/22462131847034880000
                  <2393/2500.

FOCUSED_AUDIT.md supplies an independent full derivation of the exact
Fourier constant (2r+3)3^(2r), including the shifted-grid estimate, complete
Gauss magnitude and support, normalization, digitwise L1 induction, and the
first-power application. It fixes r before taking p to infinity; ordinary
non-wrapping digit intervals and exactly p^r inputs are explicit. Growing
depths and exceptional p=7 are covered separately by the permutation tail.
No correction or larger constant was needed. This focused acceptance is
not a second audit of every section of the density theorem.

All general mathematical steps and exact analytic constants remain.
Historical finite-check details and working-package coordination are
omitted; review/edition notices are added. Historical independently authored
checks passed normal/-O/-OO with identical substantive outcomes. Finite tests
do not prove the infinite result, and no new mathematical tests were run
for this edition.

## Formal and registry limits

Formal replay is NOT REPRODUCED. The terminal source declares the correct
unconditional theorem, but no Lean/Lake build, author script, imported
third-party program, kernel replay or elaborated axiom-footprint computation
was performed.

The actual PNT dependency is ajirving/PrimeNumberTheoremAnd at
769d3b81fbff001d9fa7028df0168a8e546cf692, Lean v4.33.0, Mathlib
db584cd6d46c92f209a44c0f1c829460d327499d. Older documentation names a different
PNT repository/revision and a 4.29.x environment. Current terminal AP moduli
are 1,7,14 rather than the stale exact list 1,222138,148092. The generic
fixed-modulus PNT theorem covers the current uses. The implementation's
relaxed full lower-half box is a valid enlargement with the same limiting
mass; it is not a missing exact-valuation hypothesis.

The imported project-specific module closure contains two admitted
experimental declarations. Imported declarations are not automatically
terminal-theorem proof dependencies. Bounded static evidence supports
exclusion of these admissions from that dependency cone, without certifying
it. The full Lean/Mathlib/Batteries boundary, elaboration and generated proof
terms were not kernel-checked. The author's source commands and claimed
outputs are not an independently reproduced axiom report.

Palomar acceptance remains UNVERIFIED. Record/version HTTP 403 responses
were respected without bypass. The author's registry identifier is not
independent registry acceptance.

## Review and publication boundaries

Acceptance means unrefereed internal AI mathematical review relative to
classical Kummer, reciprocal-prime Mertens and fixed-modulus PNT inputs. No
external human peer review, journal acceptance, exhaustive novelty search,
current tracker resolution or community-wide adjudication is claimed.

SOURCES.json records selected public citations, source hashes/byte counts,
inspection history and limits. The earlier original-question inspection is
relied upon; no new PDF retrieval or complete-paper audit is claimed. The
focused reviewer directly read principal proof Sections 3,6,7. Preparation
rehashes accepted artifacts and verifies exact editorial scope and native
addition-only structure without executing third-party programs.

Exactly eight authored-prose/public-verification-metadata files are added
under unsolved_math_prioritization/attempts/2283/. Third-party source bodies,
programs, datasets, raw finite certificates, numerical toy cases, private
sources and private coordination are excluded. This is not an executable
reproduction package. Original accepted artifacts, QUEUE.md and all
unrelated repository content remain unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,842 bytes; SHA-256 `32951eba5cdd0bbe9d27ae323f291c58da0ac4a31afcbb7789169c1b45c3c990`.
- `ACCEPTANCE.md`: 5,114 bytes; SHA-256 `54dbb2cbeda0363de7ead8ad038e772ebc31cf4cc22cd8bca77c9ee2f69aaaa4`.
- `AUDIT.md`: 23,303 bytes; SHA-256 `597f9fe046dea2912c9e068522b193fa3df23ce780af37faef99adf4ed7b2bff`.
- `FOCUSED_AUDIT.md`: 16,465 bytes; SHA-256 `ff704e5f1ca041c5f211d22f688d22ebb8212df20296466dc8f500a75053b0e2`.
- `MANIFEST.json`: 1,667 bytes; SHA-256 `b37cbc3a157ba002eb19431b1a908a20020e929465d7897df6856bab71eda9f0`.
- `README.md`: 3,868 bytes; SHA-256 `c3d6b327948e1f91c517b9451120d0c936c3ba6c4ab8a0e7d2f49e612cd89c3a`.
- `SOURCES.json`: 12,104 bytes; SHA-256 `faa61177e51ab7a03f27ac277f00f346256009717212f4ad3653089d6bcaad21`.
- `VERIFICATION.json`: 3,244 bytes; SHA-256 `ca1ade386b196e6510858e22cc0a6cfb5f06f19e6690d737da7d42a421e7f2e9`.

MANIFEST.json lists all eight public members and hashes the other seven; this body independently pins its digest.

