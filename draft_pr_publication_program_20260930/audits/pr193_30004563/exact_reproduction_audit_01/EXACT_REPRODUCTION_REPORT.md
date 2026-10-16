# Independent exact reproduction of PR193 / problem 30004563

Original submission reference: b9a399eeac816dbb8f0e50e81b498c26e5acef81. Audit completed 2026-10-15 UTC in a new owned folder. No original files, Git index, or Git refs were modified. No external communication, package installation, or network execution occurred.

## Result and precise scope

**PASS for the exact arithmetic and algebraic construction.** Independently implemented rational interval arithmetic establishes five pairwise disjoint open outgoing zero brackets and one incoming zero bracket for the candidate's fixed algebraic boundary data. All coarse numerical inequalities in CANDIDATE.md are verified as strict rational inequalities. All six boundary points are distinct, all 20 boundary triples are noncollinear, and the five outgoing centers and the incoming center avoid every line through a boundary pair. Each center is also separated from every boundary point by disjoint coordinate intervals.

The strongest result is existence of **at least five** outgoing centers for the stated boundary data, together with an incoming center for those data, under the stated crossing-allowed alpha-quad interpretation. This does not prove uniqueness in any zero bracket, exactly five total centers, a finite upper bound, an embedded-tiling counterexample, or historical novelty. Matching the construction to the primary source's definitions and claim, and historical priority, belong to the separate source-scope audit. No arithmetic obligation remains unresolved in this audit.

## Independence and reproducibility

INDEPENDENT_PLAN.md was frozen before CANDIDATE.md was read. The independent implementation and its initial successful exact certificate were hashed and logged before the submitted source or submitted certificate was read. No previous REVIEW.md, previous verdict, or previous review certificate was consulted.

The independent implementation uses a new immutable interval class with Fraction endpoints, a direct integer eighth-power binary search, 224-bit dyadic root cells, 192 boundary bisections, and 112 outgoing bisections. The submission uses its own interval class, three nested integer square roots, 200-bit cells, 160 boundary bisections, and 100 outgoing bisections. After the author source was read, only two small independent-check changes were made: explicit nonzero boundary/height preconditions, and strengthening a negative root-cell control to put the exact root strictly outside its forged cell. These do not import the submitted mechanism.

Commands actually run successfully from this owned audit folder, before making artifacts read-only:

```
python3 independent_check.py
python3 submitted_replay/certify_five_centers.py
python3 replay_count_audit.py
python3 compare_certificates.py
```

The scripts use only Python's standard library. The independent checker writes its certificate beside itself. The submitted verifier writes only its sibling certificate in submitted_replay/. The count wrapper verifies the inspected source hash and refuses optimized Python, because the submission uses assert. For a future rerun after finalization, copy this folder to a fresh writable sibling folder; the comparison script resolves original data as a sibling original_submission/ directory. Existing outputs must be writable in that copy.

## Independently checked proof mechanism

For every rational radicand q, the independent root routine finds k and proves by integer multiplication and eighth powers

```
k^8 * denominator(q) <= numerator(q) * 2^(8*224)
numerator(q) * 2^(8*224) < (k+1)^8 * denominator(q).
```

Thus the root lies in the rational cell [k/2^224,(k+1)/2^224]. The zero radicand is handled exactly. For interval radicands, monotonicity uses a separately checked root cell at each endpoint. Intervals never replace the algebraic boundary values with arbitrary rational samples: the same three unique real roots are enclosed throughout. Losing their dependence by ordinary interval propagation enlarges the enclosures safely; every final decision still has a strict margin.

The exact outgoing data are

| s | strict containing interval for G(s) |
|---|---|
| 9/10000 | (38/100,39/100) |
| 11/10000 | (-28/100,-27/100) |
| 13/10000 | (51/100,52/100) |
| 1/2 | (-91/100,-90/100) |
| 1 | (9,10) |
| 10^17 | (-39,-38) |

Every radical is the nonnegative eighth root; all six cutpoints are positive. Therefore G is continuous on the entire chain. The five open intervals between successive cutpoints are disjoint, have opposite strict endpoint signs, and each contains a zero. At a zero, x^2+y^2=u and the two linear equations imply squared distances v,w. Taking eighth powers is valid because all three squared distances and eighth roots are nonnegative. Conversely every common-focus solution determines s=|X-A|^16. Different zero parameters therefore give different centers. Bisection preserves existence without presuming monotonicity or uniqueness of G.

The large-parameter endpoint is computed with exact arithmetic even though u,v,w nearly cancel in their differences. Its final G enclosure has width strictly less than 10^-58, checked by a Fraction comparison, while it lies strictly between -39 and -38. There is no floating-point cancellation in this decision.

Each boundary polynomial is evaluated with exact rational coefficients at both retained endpoints, giving strict positive/negative residuals. Its parameters have nonzero direction vector and nonzero h. For g(t)=(t^2+h^2)^8,

```
g''(t)=16(t^2+h^2)^6(15t^2+h^2)>0.
```

Hence g(t-1)-g(t) is strictly decreasing. Its odd degree 15 has negative leading coefficient, so its limits are +infinity and -infinity. The three retained brackets each specify exactly one real algebraic boundary parameter, and the boundary norm-difference identities hold for those exact roots.

Incoming levels L,M are enclosed by strictly positive rational intervals. The determinant used to solve for Y excludes zero. The checker propagates the full boundary-root boxes through every occurrence of the levels, differences, determinant, and roots. It establishes

```
H(1/100) in (37/100000,38/100000)
H(11/1000) in (-81/100000,-80/100000).
```

For the fixed exact boundary values, H is continuous throughout this interval. Consequently there is an incoming center Z in the retained coordinate box, which is contained in (0.1677,0.1717) x (-0.0036,-0.0026); these terminating decimals are exact rationals. All 15 incoming line determinants exclude zero using the whole retained parameter interval, not a rounded root.

For clarity, writing d_ij=|Ai-Aj|^16, the boundary identities are

```
d16-d12=mu; d34-d23=lambda; d56-d45=mu-lambda.
L=d45-d34; M=d12-d23.
M-L=d12-d45+lambda=d16-d56.
```

This last identity supplies the third incoming quad condition after the first two follow from the incoming focus equations. It is a direct algebraic consequence of the exact boundary root definitions, rather than an interval equality test or an assumed flip theorem.

## False controls and count meanings

Nine controls reject: forged root cells above and below the exact root 1, a negative radicand interval, a denominator interval containing zero, a residual interval straddling zero presented for a strict sign, a reversed outgoing positive sign, a false large-s residual enclosure, a reversed boundary-root endpoint sign, and a reversed incoming negative sign. Basic arithmetic checks also cover mixed-sign multiplication, squares crossing zero, division of negative intervals, zero/exact roots, and direct integer-root boundary values. Forged controls fail through explicit exceptions; the independent checker does not rely on assert or Python optimization settings.

The independent final run performs 7,007 require calls, including comparisons deliberately failed inside caught negative controls. Its count is bookkeeping, not a count of independent propositions. The original reported **6,987** reproduces exactly and means successful calls to the author's verify function. A callsite trace finds 3,144 root nonnegativity checks plus 3,144 root-bound checks (6,288 total), leaving 699 other calls, including 500 outgoing bisection sign decisions. Interval-constructor and interval-division asserts are not included in that number.

## Submitted source inspection and comparison

The entire 8,852-byte submitted verifier was read before execution. It imports Fraction, isqrt, pathlib.Path, and json; it has no subprocesses, package installation, network, environment/credential reads, or imported project modules. Its single file write uses __file__.with_name('turn2_exact_certificate.json'), so the byte-identical owned copy writes within submitted_replay/. Float conversions occur only when producing decimal_bounds and printed explanatory approximations; all validity decisions use integer/Fraction arithmetic. Its assertions must be active, as confirmed by the recorded optimization flag 0.

The owned verifier SHA-256 is 09b5db2b625b00e2c20f9c41ea1922733b1b6ab04f404c2e37ba8f0e6ef1e585. The replay certificate is byte-identical to the original certificate, SHA-256 393f41d9cafb49f8b60f6950b54150b5ed3d395076d99fb8c6507a0bbc7ced5e. This original certificate was first read as JSON data after the independent result and reviewed replay existed.

Every compared independent enclosure is contained in the corresponding author enclosure: six G residuals, three algebraic root brackets, twelve boundary coordinates, five retained outgoing root brackets, ten outgoing coordinates, the two incoming residuals, two incoming coordinates, two incoming levels, both alternating determinants, and the A3 exclusion residual. The comparison corroborates the independent result; it was not used to construct it. Full exact rational enclosures and all determinant intervals are in independent_certificate.json. SHA256_MANIFEST.json records all final audit file hashes and the three original input hashes.
