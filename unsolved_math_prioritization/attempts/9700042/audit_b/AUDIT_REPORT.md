# Independent mathematical audit B: sharp oriented-flow asymptotic

Date: 2026-10-07. Problem 9700042 / AMR-096-0042, canonical Aldous flow model.

## Verdict and exact scope

**ACCEPT the mathematical argument in the revised C4 manuscript**, with the explicitly stated external inputs listed below. The conclusion is

\[
\lim_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}=1.
\]

No substantive gap remains in the directed duality, strengthened mark budget, sparse limit, exponential-moment estimate, deterministic skeleton, disjoint-witness argument, parameter order, or lower bound. This is an independent mathematical audit, not formal verification, human peer review, or a novelty claim. The proof uses the existence and normalization of the flow-density limit as stated on Aldous's primary problem page; it does not independently prove that existence theorem.

Acceptance is bound to these exact bytes:

- `TURN_C4_BK_POISSON_REVISED.md`: 20,646 bytes; SHA-256 `8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a`.
- Prerequisite `TURN_C1_MARKED_DEFECT_BOUND.md`: 9,957 bytes; SHA-256 `f38d6ac74d3abad6f7675a13429f09e0bc6fc8151c137284e4655e8fc0c39120`. Only its finite-model duality and marked-list enumeration are needed.
- Preserved original `TURN_C4_BK_POISSON_CANDIDATE.md`: 19,887 bytes; SHA-256 `3ca69bacb1a4458243626ea0adfb360fc991bb2f8e2ed4293fa98b9c85534691`.
- Exact original-to-revised `C4_CLARIFICATION.patch`: SHA-256 `2429a7e365743dddff4785839b667f5b1f83a5e0be2f915d6840813a29dccfb3`.

The original has two literal errors that the revision corrects: the strict inequality `a_j < b_j+h` fails when `b_j` is a multiple of `h`, and the segment-index statement must exclude the last segment. It also too tersely attributes last-segment side positivity to bounds that alone are insufficient when its level increment is short. The revision supplies the actual endpoint-displacement argument and explicitly supplies the mean-convergence uniform-integrability step. These corrections do not change an estimate, theorem, or parameter choice. The acceptance target is the revision, not a claim that every sentence of the original was already correct.

Neither the C2/C3 attempts nor any unavailable historical lower-bound proof is needed for this verdict.

## 1. Primary inputs and their verified scope

1. [David Aldous, A discrete Hammersley process as an extreme case of oriented percolation flows](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html). The live primary page was inspected. Its source vertices, sink vertices, north/east capacities, denominator `2n`, stated `L^1` limit, and conjectured constant match the manuscript. Its subsequent continuum discussion is expressly heuristic and is not used as a theorem here.
2. [J.-D. Deuschel and O. Zeitouni, On increasing subsequences of i.i.d. samples](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf). The local PDF was visually inspected on printed/PDF pages 1 and 9 because its extracted text has a broken character map. Page 1 identifies the uniform planar-chain law with the random-permutation increasing-subsequence law and states its probability limit `L_max(n)/sqrt(n) -> 2`. Theorem 2 on page 9 states, for `c >= 0`,
   \[
   \lim_{n\to\infty}n^{-1/2}\log\Pr\{L_{\max}(n)\ge(2+c)\sqrt n\}=-U_0(c),
   \]
   with `U_0(c)>0` for `c>0`. This is the required upper-tail speed `sqrt(n)`, not a speed-`n` assertion. The displayed rate is `2(2+c) arcosh(1+c/2)-2 sqrt(c^2+4c)`; the proof needs only its positivity.
3. [J. van den Berg and J. Jonasson, A BK inequality for randomly drawn subsets of fixed size](https://arxiv.org/pdf/1105.3862). The definitions and Theorem 1.1 on PDF pages 2–3 restate product-measure disjoint occurrence with coordinate witnesses and its product bound. Although this paper's new subject is fixed-size sampling, the cited Theorem 1.1 is explicitly the product-measure theorem, not the later fixed-size theorem. Its increasing-event specialization suffices here. Mutually disjoint witnesses imply an iterated disjoint-occurrence event, so the finite-many extension follows by induction.

The inspected public-source byte hashes and sizes are in `AUDIT_MANIFEST.json`. A local PDF hash identifies the inspected bytes; it is not by itself evidence that a later download would be unchanged.

## 2. Exact model and directed duality

Write `N=n-2`. The source and sink arcs force precisely the two boundary crossings `e_L,e_B` in C1. Reflecting the vertical coordinate of the bounded face grid makes forward east/north dual crossings outward primal crossings. Their cost is the corresponding primal capacity; reverse dual crossings represent inward primal edges and have zero directed-cut cost.

For any primal cut, a separating interface component joins the two forced boundary crossings; its directed crossing cost is no larger than the whole cut cost. Conversely, a simple dual corner path completed by the two forced boundary crossings separates the prescribed boundary arcs and determines a valid primal cut. Thus

\[
V_n=c_L+c_B+T_N.
\]

All dual costs are nonnegative, so deleting a cycle does not increase cost. If a corner path has `b` backward steps, then it has `2N+b` forward steps. With `k` closed forward edges its cost is `2N+b-k`, yielding `D_N=max(k-b)=2N-T_N`. Every closed walk has equally many forward and backward steps, so its reward is nonpositive. The maximum reward can therefore be attained by a simple path.

A monotone path gives `D_N>=0`; the nonnegative-cost representation gives `D_N<=2N`. The two boundary terms are bounded uniformly in `n`. Aldous's stated `L^1` limit therefore gives C4 equation (22) with exactly the denominator `2N`. The reflection and the two possible forward orientations preserve independent Bernoulli marks. There is no hidden factor of two in this reduction.

## 3. Strengthened budget and rough rectangular moments

The C1 count uses only an ordered list of distinct marked edges on a simple path with `b<=k`. It does not need a lower bound on `k-b` beyond that inequality. Each coordinate's total negative variation after passing to the list of marked starting vertices is bounded by that of the whole path. Appending the two corners preserves this claim. Thus the count applies to `K_N^+`, not only to `D_N`.

For a coordinate list with `k` internal entries, choose its strictly negative increments and their positive magnitudes with total at most `k`, then use stars and bars for the nonnegative increments. This gives C1 (4). The falling-factorial ratio and the diagonal-of-a-product bound give C1 (5). Squaring for coordinates, allowing two forward-edge orientations, and charging `q^k` only to lists of distinct edges gives C4 (23). Extra invalid lists are harmless upper bounds; repeated edges are never assigned probability `q^k`.

The two numerical bases used in (24) are

- `2 e^2 (3/2)^6 / 32^2 = 0.16438665454469126 < 1/4`;
- `32 e^2 10^-6 * 6^2 = 0.008512192625968109 < 1/4`.

The prefactors are at most 4. Summing `4*4^-k` gives at most `(16/3)*4^-r < 6*4^-r`, proving (25). On `K_N^+<=B_N`, every nonnegative-reward simple corner path has both `b` and `k` bounded by `B_N`. An optimum is one such path. This is stronger than a bound on its net reward and is exactly what the skeleton needs.

For `0<theta<log 4`, tail summation gives (27) uniformly in `q<=10^-6` and `N>=1`; ceilings can be absorbed in a constant depending only on theta. To get (28), place the rectangle in a square of side `max(W,H)`, independently extend the marks, and monotonically pad an optimal rectangular path to the square corner. Padding has nonnegative reward. The square reward is at least the rectangle reward, and `max(W,H)<=W+H`. No independence of overlapping rectangles is being asserted in this marginal bound.

## 4. Sparse fixed-box limit and uniform integrability

In a box whose side lengths satisfy `sqrt(q)W_q -> w` and `sqrt(q)H_q -> h`, there are `2W_qH_q+W_q+H_q` candidate marked edges. The Bernoulli Laplace functional converges to that of intensity two on the rescaled rectangle. Both orientations count; the boundary contribution tends to zero.

For a fixed integer `M`, restrict to at most `M` marks and to pairwise starting coordinates separated by more than `M` in both coordinates. A nonnegative-reward simple path has `b<=k<=M`. If its ordered mark list decreased in a coordinate, the decrease would require more than `M` backward steps, a contradiction. Its marked starting vertices therefore form a strict increasing chain. Conversely, the coordinate gaps allow monotone connections between any such chain's oriented marked edges, including the one-lattice-step edge displacements. The first and last connections remain inside the rectangle. Hence the unrestricted reward equals the maximum strict-chain length on this event.

For fixed `M`, the probability of any pair being within `M` in either coordinate is `O_M(sqrt(q))` at bounded rescaled box size. The total mark count has uniformly bounded mean and converges to `Poisson(2wh)`, so its tail can be made small after taking `M` large. With probability one the finite limiting Poisson configuration has no coordinate ties; the chain-length map is locally constant there. These facts prove distributional convergence.

The domination `0<=D<=Z`, where `Z` is the total mark count, is valid because an optimal path is simple. For every fixed `a>0`, the displayed binomial moment bound in Section 2 is uniform in small `q`. Applying it with a larger exponent gives uniform integrability of `exp(theta D)` for any fixed theta. Consequently (29) holds. A positive separate rescaling of the two coordinates turns the intensity-two rectangle into a rate-one square of side `sqrt(2wh)` without changing coordinate order. The intensity and shape constants are correct.

## 5. Sharp fixed-theta Poisson moment bound

Theorem 2 supplies an exponential tail beyond each fixed `(2+a)s` after Poissonization. One precise coupling is to take an infinite iid uniform sequence independent of `Z_s~Poisson(s^2)`. On `Z_s<=ceil((1+delta)s^2)`, its first `Z_s` points are contained in the first `n` points. Choose delta so `(2+a/2)sqrt(1+delta)<2+a`; then the fixed-sample theorem bounds the latter event by `exp(-c_a s)` for all sufficiently large `s`. The Poisson overflow term decays on the faster `s^2` scale and can be absorbed.

For completeness, the first factorial moment of the number of increasing `k`-point subsets is `s^(2k)/(k!)^2`. The first `k!` is the Poisson unordered-subset factor; the probability of consistent order in the second coordinate contributes the other. Markov's inequality and `k! >= (k/e)^k` give (31).

To make the manuscript's moment conversion fully explicit, take `0<a<epsilon/3` and fixed `M>10e`, then choose `0<theta<min(log 4,c_a/(2M))`. Split the tail sum for `E exp(theta Lambda_s)` into thresholds below `(2+a)s`, between that level and `Ms`, and above `Ms`:

- The low part is bounded by `exp(theta(2+a)s)` up to harmless rounding.
- The middle part is at most a polynomial in `s` times `exp(theta Ms-c_a s)`, so it is exponentially negligible.
- The high part is dominated by a geometric series with ratio at most `exp(theta)(e/M)^2<1`.

For large enough `s`, the slack from `2+a` to `2+epsilon` absorbs constants and rounding. This proves (30) with one fixed positive theta before increasing the box scale. It is not an invalid interchange of a volume limit with an exponential moment.

The same factorial bound gives uniform integrability of `Lambda_s/s` for `s>=1`. Poissonized probability convergence, obtained by the usual two fixed-sample sandwiches, thus implies mean convergence. The revision now states this explicitly. The lower bound need not invoke an additional uncited expectation theorem.

## 6. Rectangles, quantization, and exceptional perimeter budget

The first-hitting times exist in increasing order because each path step changes `x+y` by one. There are `J=ceil(2N/L)` segments, with increments `L` except possibly the final one. All level coordinates are deterministic once `N,L` are fixed.

A segment with `b_j` backward steps cannot descend below its starting coordinate by more than `b_j`, nor overshoot its ending coordinate by more than `b_j`. Since `a_j=(floor(b_j/h)+1)h>b_j`, (39) contains every vertex, including both endpoints.

With `x_j=i_jh+delta_j`, `0<=delta_j<h`, the exact widths are

\[
W_j=(x_{j+1}-x_j)+2a_j+h+delta_j-delta_{j+1},
\]
\[
H_j=(y_{j+1}-y_j)+2a_j+h-delta_j+delta_{j+1}.
\]

The quantization remainders are positive, and each true displacement is at least `-b_j`. Thus each side exceeds `2a_j-b_j>=h`. This checks the short last segment without substituting its increment by `L` in a lower bound. Adding the two formulas gives (40).

The endpoint displacement bounds imply the loose but valid integer range `-s_j-2 <= i_{j+1}-i_j <= m+s_j+2`. For a nonlast segment with `s_j=0`, its dimensions are exactly `(z+3)h,(m-z+3)h`, giving the finite good-shape list. Both dimensions are positive.

A nonlast bad segment has `b_j>=h`, and the corrected inequality `a_j<=b_j+h<=2b_j` holds. Its perimeter contribution is bounded by `(m+10)b_j`: its level increment costs at most `m b_j`, the `2h` term costs at most `2b_j`, and `4a_j` costs at most `8b_j`. The last segment contributes at most `L+6h+4b_last`. Since `4<=m+10`, allocating its actual backward budget gives (41) with no double counting. There are at most `K+1` bad segments.

## 7. Skeleton entropy and disjoint occurrence

For a fixed backward-quantization vector, the next coarse x-coordinate has at most `m+2s_j+5 <= (m+5)(s_j+1)` choices. Using `s+1<=exp(s)` and counting all nonnegative vectors of sum at most `K` gives (42). Endpoint restrictions and confinement may remove records, which only improves the upper bound. No microscopic endpoint offset needs to be recorded: the rectangle and its marginal law depend only on the coarse record and deterministic levels.

At fixed `q,m,R`, the integer roundings vanish as `N` grows, giving `K/J -> 16m sqrt(q)`. The entropy formula `log binom(J+K,K)<=J F(K/J)` is valid, including `K=0`. The principal entropy cost is per coarse segment, with no factor `log(1/q)`.

For the BK step, fix a skeleton before applying a probability inequality. For a realized global simple path, keep only a segment's original marked forward edges fixed as closed. Changing all other edge states cannot lower that segment's reward: formerly unmarked forward edges remain nonnegative and backward steps always cost one. Monotone padding from the rectangle corners also has nonnegative reward. The concatenated walk has at least the original segment reward, and deleting nonpositive-reward cycles yields a simple local corner path. Therefore these original marks alone witness `{X_j>=r_j}` when `r_j>0`; when `r_j=0`, the empty witness suffices.

The global path is simple, so the original marked-edge sets for distinct segments are pairwise disjoint. Padding edges are **not** included in those witness sets. This is why rectangle overlap, padding overlap, and dependence of the optimizing path on the whole field do not invalidate BK. For fixed threshold vector and skeleton there is an event inclusion into disjoint occurrence; no conditional independence is used.

The needed mark field can be independently extended to a finite union of rectangles, or to all rectangles from the finite set of allowed skeletons. The event inclusion holds for every extension, so the original event's probability is bounded in the extended product space. The tail-vector union bound (44) and geometric tail-sum identity then give (45). The product on its right consists of marginal moments, not moments asserted to be independent.

## 8. Parameter order and large-volume upper bound

For prescribed `zeta>0`, fix epsilon and integer `m` so `Delta>0`; choose theta from the Poisson moment lemma; then choose a sufficiently large fixed `R`. The finitely many good-shape aspect ratios are now fixed. Their smallest normalized side product grows with `R`, so the Poisson moment bound applies to every shape. Fixed-box convergence yields (36) uniformly over this finite list for all sufficiently small `q`, independently of `N`. The factor two absorbs finite-q approximation and rounding.

Combining the good moments, rough bad moments, exceptional perimeter budget, skeleton count, and BK yields exactly (46). After `N -> infinity` at fixed `q,m,R`, the normalized terms are:

- main slack `-theta sqrt(2) Delta`;
- principal entropy `log[2(m+5)S_theta]/(sqrt(q)L)`;
- backward-budget entropy and bad-moment prefactors `[kappa(1+log C_theta)+F(kappa)]/(sqrt(q)L)`;
- bad-perimeter contribution `512 theta(m+10)sqrt(q)`.

The coefficient 512 is correct: it is `32*32/2` from the moment exponent, backward budget, and normalization. First choose `R` to make the principal entropy smaller than half the fixed main slack. Only then take `q` small, so `sqrt(q)L -> R`, `kappa -> 0`, `F(kappa)->0`, and the bad-perimeter term tends to zero. This makes the large-`N` exponential rate negative. The mark-budget failure probability independently decays exponentially in `sqrt(q)N`.

Thus for each sufficiently small fixed `q` the normalized reward exceeds `(1+zeta)sqrt(2q)` with probability tending to zero. Since `0<=D_N/(2N)<=1`, boundedness passes this statement to the expectation limit (22), establishing (50). The parameter order is valid and addresses, rather than assumes, the interchange-of-limits issue.

## 9. Independent lower bound

Consecutive diagonal squares intersect only at their common corner, not along an edge. Concatenating optimal confined paths produces an admissible large-square path; independence is unnecessary for the expectation inequality. Divide by the large-square side and use (22) along multiples of the small side to get (51).

For fixed `R`, take `ell=floor(R/sqrt(q))`. The sparse limit and its uniform integrability imply `E D_ell -> E Lambda_(sqrt(2)R)`. Dividing (51) by `sqrt(2q)` gives the manuscript's lower bound `E Lambda_(sqrt(2)R)/(2sqrt(2)R)`. Taking `R -> infinity` yields 1. This uses neither the missing historical lower-bound manuscript nor C1's nonsharp asymptotic estimate.

## 10. Supplemental finite checks

A fresh checker, `independent_checks.py`, uses exhaustive primal cut enumeration, a separately implemented reflected dual shortest-path computation, and exhaustive simple dual paths. It passed:

- 4,352 primal/dual capacity configurations, exhaustive for primal side lengths 2 and 3 and randomized for sides 4 and 5;
- 104,520 simple-path/parameter skeleton cases, exhaustive over all corner-to-corner simple paths for dual side lengths 1 through 4 and the stated 12 `(m,h)` choices;
- 285,750 segment containment, positivity, dimension, index-range, and bad-perimeter checks;
- 47,744 marked-list negative-variation cases, over every mark configuration on the side-2 dual square and every simple path;
- 13 separated-mark stability configurations within that small exhaustive family;
- the two numerical constants in the rough mark tail.

These computations are supplemental diagnostics only. They do not establish BK, the Poisson-chain theorem, uniformity in unbounded volume, or the asymptotic conclusion. Acceptance rests on the mathematical checks in Sections 1–9.

## Final disposition

**Accepted:** the sharp asymptotic in the canonical model, as proved by the pinned revised C4 plus the pinned C1 finite duality/count prerequisites and the explicitly cited external inputs.

**Not certified:** novelty, current literature-wide unresolved status, formal-machine verification, human peer review, or unavailable historical artifacts. No publication or repository mutation was performed as part of this audit.
