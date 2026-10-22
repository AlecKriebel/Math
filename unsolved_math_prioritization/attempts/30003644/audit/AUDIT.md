# Independent adversarial audit: rank 632 / 30003644

## Verdict

**PASS AS AN UNSOLVED, FIVE-APPROACH PARTIAL-RESULT PACKET.** No substantive mathematical or computational correction is required. The exact all-height statement remains unproved in this packet. No new proof-search approach, sixth attempt, global resolution, novelty certification, or counterexample on the specified line is claimed by this audit.

Frozen source code: OWR-15956-010.

- Frozen packet SHA256SUMS: `d218aaade8691a6de5ca584355d83e7e9d02f5ec1452bdb6f993b30eff8c1fa8`
- Frozen authored ZIP: `24ffa30c1d2519a086c6a7f4b901824d3b422902e8e773f99c3792d26dc08ef1`
- All seven manifested original payload files pass their SHA-256 checks.
- Original control replay is byte-for-byte identical to `control_results.json`.
- Originals were not edited. No remote writes, source uploads, or helper-agent delegation occurred.

## Exact target and primary-source check

The question is whether `1 + 2^(-1-it) + 3^(-1-it) + 5^(-1-it)` is nonzero for every real `t`. It is not a right-half-plane assertion, a uniform positive lower bound, or the arbitrary infinite-series problem.

Visual inspection confirms the polynomial and quantifier in [OWR 51/2017, printed p.3065](https://ems.press/content/serial-article-files/46710), and the repeated question in [OWR 51/2025, printed p.2757](https://ems.press/content/serial-article-files/52435). The neighboring 3-full-number questions in the latter are separate.

[Yip, arXiv:2512.16528v1](https://arxiv.org/html/2512.16528v1), read in full and visually checked at p.3, distinguishes the infinite-sequence disproof from the finite-set conjecture and explicitly retains the `{2,3,5}` question. A bounded current primary-source search did not verify any later unconditional resolution; it does not establish exhaustive present-day openness.

The original [Erdős–Ingham scan](https://matwbn.icm.edu.pl/ksiazki/aa/aa9/aa9134.pdf), printed pp.347–355, was visually inspected. Theorem 4 is at p.347, the necessary oscillatory construction at pp.349–350, the relevant discussion at pp.353–354, and the finite example at p.355. [Waldschmidt](https://webusers.imj-prg.fr/~michel.waldschmidt/articles/pdf/DION2005proceedings.pdf), pp.4–5, was visually checked for the precise six-exponentials theorem and Schanuel statement. Source hashes, sizes, and inspection metadata are in `source_inspection.json`; source bytes and text are excluded.

## Analytic and arithmetic proof audit

1. **Rightmost boundary.** Strict decrease of `H(sigma)` gives a unique `sigma_*` with `H=1`. Triangle equality at the boundary forces all three phases to be `-1`, contradicting rational independence of `log 2` and `log 3`. Independence of the three real logarithms follows from unique factorization. It is exactly the condition for density of the continuous torus flow; independence with `2*pi` is not required for this continuous-time statement. Finite sums make convergence of the vertical translates uniform on compact sets. The limiting zero is simple, so Rouché supplies zeros approaching the boundary and strictly right of one. It gives no zero on the requested line.
2. **Torus geometry.** Exact rational arithmetic verifies both unit norms and cancellation for the displayed algebraic triple. The real two-angle Jacobian determinant is `sqrt(6479)/1800`, hence nonzero. The local zero set is one-dimensional. Dense orbit closure and continuity imply infimum zero, but not actual intersection. This is compatible with pointwise nonvanishing.
3. **Phase restrictions and simplicity.** The deficit is exactly `31/30 - 1 = 1/30`. Nonnegative summands yield the three stated real-part bounds. Weighting the deficit by at most `log 5` proves the real derivative bound. Independent rational interval arithmetic gives a lower bound approximately `0.9810173385750259`, exceeding `0.98`. Multiplication by `i` gives the asserted imaginary velocity; no noncrossing conclusion follows.
4. **Tauberian construction.** For nonzero hypothetical `t`, the chosen epsilon guarantees strict positivity and strict monotonicity on all positive `x`. The oscillatory weighted sum cancels with exactly the stated sign convention and coefficient `61/30`. The ratio fails to converge. Truncation below one is monotone and preserves the exact sum for `x >= 5`. Off-line zeros with real part greater than one destroy the desired positivity/monotonicity in this construction. The source attribution and difference of domain conventions are accurate.
5. **Elimination and transcendence.** Substitution gives `B + b/v - c^2/(A+bv)=0`. Multiplication by `v(A+bv)` gives exactly `bB v^2 + (AB+b^2-c^2)v + bA=0`. Neither `v` nor `A+bv=-cw` is zero. The leading coefficient is nonzero because the relevant base weight is less than one. Thus both other phases are algebraic over any selected base phase. All six permutations also pass an exact witness control.
6. **Six exponentials.** The pair `1,-it` is Q-linearly independent for nonzero real `t`, and the three real logarithms are Q-linearly independent. If one phase were algebraic, elimination would make all three algebraic, contradicting the six-exponentials theorem for the six values `2,3,5,u,v,w`. Thus each phase is transcendental and their joint field has transcendence degree exactly one. The theorem does not imply algebraic independence, so this is only an obstruction.
7. **Schanuel.** The six arguments comprising the three real logarithms and their `-it` multiples are Q-linearly independent by separating real and imaginary parts. Schanuel would give transcendence degree at least six; elimination places their field and exponentials inside an extension algebraic over a five-generator field. The contradiction is valid and expressly conditional on the full conjecture.

## Interval implementation and endpoint-export audit

The frozen implementation uses mpmath 1.3.0 at 35 decimal digits (120 bits). Inspection covered scalar/list conversion, directed decimal parsing, arithmetic operations, endpoint comparison, log/exp endpoint evaluation, trigonometric quadrant/extremum handling, and string formatting. Runtime module hashes are recorded in `mpmath_inspection.json`.

The predicates operate on internal interval endpoints, not on strings. Strict interval comparisons require endpoint separation; an inconclusive comparison cannot become success through the explicit boolean tests. Decimal centers/radii are outward enclosures of the stated exact decimal rationals. Binary float leaf endpoints are exact dyadic rationals, and subdivision introduces no floating-point error within this finite depth bound. Independently, every exported endpoint was parsed as an exact rational and every leaf checked for its expected width and aligned dyadic position.

`str(iv)` does round displayed endpoints to nearest. A hypothetical serialization of the 9,564 target component intervals would round 4,418 lower endpoints and 4,932 upper endpoints inward. **This is not a defect in the frozen packet:** none of those strings is exported or used as certificate data. The original JSON contains round-trip decimal renderings of binary float endpoints for the negative control, plus exact decimal-rational thresholds for the disk. Those JSON numbers reproduce the original dyadics when parsed as Python floats, but are not literally identical rationals if interpreted as exact decimals. This does not affect any decision in the verifier, and even the displayed decimal interval strictly contains the known negative-control root. The audit exports leaf endpoints as exact hexadecimal dyadics and all mpmath endpoints as exact `(sign, mantissa, exponent, bitcount)` tuples, avoiding both formatting ambiguities.

## Independent rigorous computation

`verify_independent.py` uses only Python's standard library and integer/rational arithmetic. It does not import mpmath, call a floating-point elementary function, or trust the original component bounds as proof. The original adaptive partition is merely a proposed cover; the independent implementation checks its complete exact coverage and computes rigorous component bounds afresh.

- Scale: integer endpoints divided by `2^160`.
- Arithmetic: integer floor/ceiling rounding for multiplication, division, and rational scaling.
- `log p`: the positive atanh series with `z=(p-1)/(p+1)`, 180 terms, and tail bounded by `2*z^(361)/(361*(1-z^2))`.
- `pi`: Machin's formula `16*atan(1/5)-4*atan(1/239)`, each using 120 terms and the next-term alternating bound.
- Sine/cosine: rigorous period reduction, explicit check of reduced absolute value at most four, degree-99 Taylor polynomials (the cosine polynomial has degree 98), remainder at most `4^100/100!`. Full interval ranges take both endpoints and include every possible critical point `k*pi/2`.
- Exponential: degree-180 Taylor polynomial with remainder at most `81*4^181/181!` for absolute argument at most four; `e^4<3^4=81` suffices.
- Serialization: exact rational numerators/denominators, never nearest-rounded displayed endpoints.

All 4,782 target leaves independently exclude zero. They cover `[0,10000]` exactly without gaps or overlap except common closed endpoints. Their widths and grid alignment match their recorded depths. Their accepted-endpoint digest is the original `642d2bed994405c2f3fbe99b182d4158f493c4b1346acbe62124992cf96b2618`. Every original target rectangle contains its independently rigorous recomputation, providing an additional per-leaf check on the original mpmath bounds. The smallest chosen component exclusion margin is approximately `0.00012168856669178095` (exact bound in the JSON).

The 23 negative-control leaves cover `[0,8]` exactly. Twenty-two exclude zero; the remaining interval is exactly `[1188131/262144, 2376263/524288]`, and an independent rational enclosure of `pi/log 2` lies strictly inside it. The independent implementation does not certify this interval or the entire zero-bearing interval `[0,8]`. One accepted negative-control rectangle is a little wider in the independent implementation because its generic Taylor error includes an exact-zero endpoint; this is harmless and all 22 exclusion predicates independently pass.

Conjugation extends the target cover to `|t|<=10000`. It supplies no information at unrestricted height.

The independent disk check establishes residual less than `1e-27` (computed upper bound approximately `2.4993674059e-31`), real derivative greater than `0.9`, and second derivative modulus less than `2` (computed upper bound approximately `1.1509729892`). The radius is exactly `1e-20`. Taylor's theorem gives boundary error less than `1e-27+r^2<0.9r`; Rouché therefore gives exactly one zero in the stated disk, counted with multiplicity. The whole disk is strictly right of one. Both boundary signs at `1.032` and `1.033` are independently certified.

This is a transparent computer-assisted arithmetic certificate, not a proof-assistant formalization. It relies on correct Python integer/rational execution and the elementary Taylor/series bounds just specified, rather than mpmath transcendental routines for the independently rechecked conclusions.

## Adversarial controls and corrections

`test_adversarial.py` independently verifies unit norms, cancellation, six permuted elimination identities, the nonzero Jacobian determinant, three sign mutants, three denominator mutants, 200 rational-interval arithmetic cases, and inclusion of trigonometric extrema. Missing initial leaves, duplicated initial leaves, and marking the known-zero interval as certified are all rejected.

No substantive correction is required. One optional editorial cleanup: the original comment says “sign/denominator mutants,” while its loop only flips signs. The README accurately describes three sign mutants; the audit additionally exercises actual denominator mutants. The original files are left unchanged.

During construction of the independent checker, direct fixed-point Horner evaluation of tiny Taylor coefficients produced excessively wide bounds and correctly failed an exclusion assertion. Replacing it with forward term recurrences retained the same rigorous Taylor remainder while avoiding this dependency inflation. No failed experimental output is treated as a certificate.

## Replay

Python 3.12 was used. The independent verifier and adversarial tests require only the standard library. Re-exporting the frozen tree and replaying the original verifier additionally require mpmath 1.3.0.

From the audit directory:

```sh
python verify_independent.py > independent-replay.json
cmp independent-replay.json independent_results.json
python test_adversarial.py > adversarial-replay.json
cmp adversarial-replay.json adversarial_results.json
```

Optional original re-export from the extracted portable bundle:

```sh
python export_leaves.py ../frozen /tmp/rank632-leaf-replay
cmp /tmp/rank632-leaf-replay/target_leaves.jsonl target_leaves.jsonl
cmp /tmp/rank632-leaf-replay/negative_leaves.jsonl negative_leaves.jsonl
python ../frozen/verify_controls.py > original-replay.json
cmp original-replay.json replay.json
```

`AUDIT_MANIFEST.json` binds the immutable target and every audit payload, with hashes and byte counts. The portable archive contains only the eight frozen authored files and the authored audit artifacts. No PDFs, rendered source pages, OCR, dataset contents, private coordination files, or runtime-library source files are included.
