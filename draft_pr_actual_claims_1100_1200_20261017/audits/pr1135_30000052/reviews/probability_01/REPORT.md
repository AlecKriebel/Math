# Independent adversarial probability review — PR #1135

**Verdict: PASS for the full displayed comparison target, resolved negatively. No mathematical repair required.** This is a fresh AI mathematical audit of the candidate at head `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`, rather than reliance on its prior acceptance. The assigned probability/quantifier family finds no gap in the three-point proof, its normalization, or its scope. This report does not determine historical priority or certify external human peer review.

## 1. Fresh original-source check

I fetched the [official Oberwolfach Report 13/2004 PDF](https://ems.press/content/serial-article-files/45858) afresh and read and visually inspected physical pages 25–27, printed 697–699. `SOURCE_FETCH.json` pins the returned 445532-byte PDF (SHA-256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`). Third-party PDF, extracts, and page images remain exclusively under ignored `sources/private/`.

The original question concerns the expectation of the **p-th power** of normalized anchored Lp discrepancy, with **even p**. Its law integrates both generator and shift over their full product cube, so they are independent continuous uniforms. The point indices are 0 through n−1. No rational-generator, prime-n, no-collision conditioning, or well-spaced-generator restriction is imposed. The candidate's n=3, d=1, p=4 therefore meets the displayed target. The different final existence question about well-chosen lattices is not disproved. I inspected the formulas themselves, including the exponent on the expected discrepancy; ordering fourth moments does not by itself order expectations of norms.

## 2. Independent probability reconstruction

Put u=Delta and v={z+Delta}. For each fixed Delta, circle translation preserves uniform z. Therefore (u,v) has product uniform law on the unit square, and the third point is w={2v−u}. This change of variables discards no generators and has the correct probability normalization.

For any distinct j,k, conditioning on z makes t_j={jz+Delta} uniform. In fact t_j is independent of z, since that conditional law does not depend on z. Then t_k={t_j+(k−j)z}; multiplication by any nonzero integer preserves circle Lebesgue measure. Explicitly, for a positive integer m, partition the circle into m intervals on each of which z↦{mz} rescales length by m; the m preimages have total length equal to that of the target. Reflection handles negative m. Thus each indexed pair is independent uniform. This proves the necessary moment identities but does **not** imply triple independence.

For 0<x≤1/2 and 0≤u,v<x, the raw value 2v−u is in (−x,2x). If negative, its fractional part is at least 1−x≥x, apart from endpoints. If nonnegative, it is below one apart from endpoints. Hence w<x is precisely 0≤2v−u<x up to a null set. At fixed u, this cuts v to [u/2,(u+x)/2], an interval of length x/2 entirely inside [0,x]. Its area is

q(x)=P(u<x,v<x,w<x)=x²/2.

The statement also holds at x=0. At x=1/2 the possible wrap endpoint is a line/corner of area zero. This calculation uses the full u,v probability square, not a selected positive-measure part or a fixed-generator example.

Let P_k=P(N_x=k), where N_x counts all three indices. Total probability, E N_x=3x, E binom(N_x,2)=3x², and P_3=q determine

(P_0,P_1,P_2,P_3)=(1−3x+3x²−q, 3x−6x²+3q, 3x²−3q, q).

For x≤1/2 these become

(1−3x+5x²/2, 3x−9x²/2, 3x²/2, x²/2).

Their entries sum to one and are nonnegative on this interval: P_0 has negative discriminant and positive leading coefficient, and P_1=x(3−9x/2)≥0 there. In particular q(1/4)=1/32 differs from the iid value 1/64.

## 3. Reflection and the fourth moment

The parameter map (z,Delta)↦({−z},{−Delta}) preserves product Lebesgue measure and sends every t_j to {−t_j}. At a fixed x, a point at 0 or at a tested endpoint can spoil an exact pointwise complement statement. Every point is uniform, so the finite union of such events has probability zero. Outside it, reflection exchanges N_x with 3−N_(1−x). Thus the centered normalized discrepancy changes sign and the expected fourth integrand F satisfies F(1−x)=F(x). The proof does not condition away any positive-measure collision or endpoint event.

Independently expanding the count fourth power before substituting q gives

F(x)=x⁴−(2/3)x³+(2/27)x²+x/27+(4/9)(1−2x)q(x).

The raw count moments needed for this expansion are

E N²=3x+6x²,
E N³=3x+18x²+6q,
E N⁴=3x+42x²+36q.

Substitution of q=x²/2 on the lower half gives

F(x)=x⁴−(10/9)x³+(8/27)x²+x/27.

For an iid triple the same general expansion has q_iid=x³. Therefore on the lower half,

F_lattice(x)−F_iid(x)=(2/9)x²(1−2x)².

This is strictly positive on (0,1/2), providing a sign check independent of subtracting the final rational values. The reflected upper half has the same sign. The measurable integrand is bounded by one and nonnegative, so Tonelli/Fubini applies. Exact integration gives

E disc_4(lattice)⁴=2∫_0^(1/2)F(x)dx=19/1620,

and the full gap is

2∫_0^(1/2)(2/9)x²(1−2x)²dx=1/540.

There is no inference about E disc_4 without the fourth power. The strict moment reversal alone settles the stated universal expected-moment question negatively.

For completeness, reflection plus inclusion-exclusion supplies the full triple probability:

q(x)=1/2−2x+(5/2)x²,  1/2≤x≤1.

Indeed P(all points≥x)=1−3x+3x²−q(x)=q(1−x). Extending the lower-half formula to x=1 would give 1/2 rather than 1 and is false. The candidate does not make that extension.

## 4. Iid value, secondary proof, and limiting claims

For independent Bernoulli(x) variables B_i, let Y_i=B_i−x and a=x(1−x). Then E Y_i²=a and E Y_i⁴=a−3a². Only the all-equal and the two-pair terms survive in the fourth expansion. Thus

E((sum Y_i)/n)⁴=[n(a−3a²)+3n(n−1)a²]/n⁴.

Integrating a and a² over x gives 1/6 and 1/30. Therefore the iid moment is (3n−1)/(30n³), equal to 4/405 at n=3. This independently confirms both the gap 1/540 and ratio 19/16. The coefficient 1/n in the discrepancy is retained throughout.

The independent empty-tail proof is also sound. On the increasing no-wrap triangle with 0≤z≤1/(n−1) and 0≤Delta≤1−(n−1)z, the two tails alone contribute [Delta⁵+(1−Delta−(n−1)z)⁵]/5. Their integral is 1/[105(n−1)]. Reflection in the generator yields a decreasing triangle of equal contribution. Their generator intervals have disjoint interiors for n≥3. All other fourth-power contributions are nonnegative. Consequently the lattice moment is at least 2/[105(n−1)]. For n=4 the excess of that lower bound over the iid value is 5/8064>0. For n=3 the tail bound alone is too weak, as the candidate correctly recognizes.

At n=1 the sole point is uniform; at n=2 the complete ordered pair is product uniform in every dimension. Therefore the entire ensemble laws agree for these counts and every measurable discrepancy functional with defined expectation. Three is the smallest possible point count for this kind of counterexample. This is not a claim that p=4 is the only failing even exponent, or that every dimension exhibits the reversal.

For any n,d, the same pairwise argument applies coordinatewise. For a box of volume b, the normalized count variance is b(1−b)/n. Integration over the anchored-box endpoint cube gives (2^(−d)−3^(−d))/n. Thus the candidate's all-n,d second-moment equality is correct. It provides no justification for equating the fourth moments.

Collisions for finitely many indices occur on null generator sets. The proof counts by index and does not delete collisions, deduplicate, or change n. Closed parameter cubes and half-open coordinate intervals differ only on null sets. No unproved regularity assumption, asymptotic approximation, or statistical estimate is used.

## 5. Independent exact supplementary artifact

`check_inclusions.py` imports no candidate code and uses only Python's standard library with exact rational arithmetic. The geometric mechanism is a full event-mask partition, not inference of triple independence and not evaluation of the candidate's returned fractions:

1. It partitions the u,v square into the three bands −1≤2v−u≤0, 0≤2v−u≤1, and 1≤2v−u≤2, with respective areas 1/4,1/2,1/4. On band m, w=2v−u−m.
2. At every threshold it clips each band by each of the eight combinations of u<x, v<x, w<x or their complements. Rational polygon shoelace areas directly produce all eight probabilities. Closed clipping boundaries are legitimate because they are finitely many lines of area zero.
3. It checks all masks and resulting P(N=k) at all 279 distinct rational thresholds with denominator at most 30, including 0,1/2,1. These finite checks corroborate, but do not replace, the universal area proof above. It additionally checks 98 unequal-threshold rectangles for (u,w) and (v,w).
4. A separate exact polynomial ring verifies the universal count-moment expansion, both q polynomials, symbolic reflection, the factored strict gap, and exact integrals. Full binomial expansions independently verify iid second and fourth formulas for n=1 through 12.
5. Nine adverse controls distinguish triple dependence, omitted modular bands, invalid extension of the lower-half q, weak n=3 tail bounds, wrong normalization, inference about expected norms, a fixed zero generator, finite even-grid multiplication, and reflection boundary exceptions.

Both `python3 check_inclusions.py` and `python3 -O check_inclusions.py` pass **3859 explicit checks** with byte-identical JSON output. Both modes reject `--negative-guard` via an explicit exception; no `assert` is used. All ten frozen input files are authenticated by size and SHA-256 on each run. `RUN_RECEIPT.json` records the runs and code hash. The results use no floating-point arithmetic, Monte Carlo sampling, or external mathematical package.

Reproduction should preserve this review directory's relative location to `../../inputs`, or copy both that directory and `INPUT_PINS.json` in the same layout. The code writes only stdout and does not modify inputs or reports.

## 6. Disposition and remaining limits

No repair is needed for the full negative mathematical conclusion or the accompanying claimed consistency checks. The original target's expectation, measure, normalization, finite-index convention, and even-exponent condition match exactly. The analytic gap is positive on a set of positive endpoint measure and the generator law is averaged in full. The candidate's n=4 supplementary argument is independently sufficient as well.

This review supplies no exhaustive priority judgment and no assurance about later literature; that is a separate task. It does not settle the distinct carefully-chosen-lattice existence problem. The proof remains an unrefereed AI-audited derivation, not formal proof-assistant certification. None of those limits weakens the exact counterexample to the displayed comparison.
