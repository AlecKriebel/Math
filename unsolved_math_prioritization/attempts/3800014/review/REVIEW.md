# Independent review: shortest intervals of every exact count

**Final verdict: PASS_COMPLETE_CREDITED_REAL_RAM_ALGORITHM.** The known $O(n^2/\log(2+n))$ algorithm resolves the original request for any faster-than-quadratic algorithm in a reasonable model. Recommend **already_solved**, with prior-algorithm attribution. No polynomial exponent improvement, arbitrary-precision bit-time speedup, lower bound or novelty claim is established.

This is a separate adversarial AI review by gpt-6-astra at xhigh, completed 30 September 2026. It is not human peer review.

## 1. Final snapshot and correction

- `KNOWN_ALGORITHM.md`: SHA-256 `c4b1d498978ee9e6db91bb5a5947a491a991b8dfa2a5a686e0d0d1a108c44f34`
- Corrected `algorithm.py`: SHA-256 `cc976625a1e20d78742ff6bbff44ca5c776341369cd3d2cd1ece1bba713293f0`
- Submitted `verify.py`: SHA-256 `b9006df7f0e485faf0f72f893f8c65c6187170b89ef9dac323d56e88b915a0fe`
- Corrected submitted receipt: SHA-256 `a30039f7ab13f45d2d52a7e71382831095e598facd2978a194958e0e8245c4a5`

One implementation correction was requested and completed during review. The earlier algorithm hash `2b4c3a4949c84c9c7dd1b716e4207ee3367a8e449ff7be138c5f98c3f1d37381` used recursive `yield from` forwarding. Propagating each output through recursive generator frames can add a depth factor, so that implementation did not directly justify the asserted $O(P)$ reporting cost. The author replaced it with one shared output list and direct leaf appends. I checked the exact diff: only the reporting implementation changed, and the mathematical artifact is unchanged. Each reported pair now incurs a single append, with amortized constant cost on the stated RAM model. No small-space claim is made.

There are **no outstanding mandatory corrections**. The 10,388 submitted assertions replay byte-identically on the corrected implementation. The separate checker passes 22,962 exact assertions.

## 2. Original source and prior credit

I independently opened [Erickson’s original algorithmic page](https://jeffe.cs.illinois.edu/open/algo.html), read the complete dynamic-programming question, and checked the [index’s stale-status warning](https://jeffe.cs.illinois.edu/open/). The input is a sorted list of real numbers; the output is a smallest interval containing exactly $k$ entries for every $1\le k\le n$. The requested alternatives are a faster algorithm or a superlinear lower bound. Nothing there requires $O(n^{2-\varepsilon})$ time for a fixed positive $\varepsilon$.

I read and visually checked Theorem11 and its full proof in Section4.3 of the [retrieved necklace author manuscript](https://tmc.web.engr.illinois.edu/convol.pdf), and Lemma2.1 with its complete proof in [Chan’s author manuscript](https://tmc.web.engr.illinois.edu/apsp.pdf). The former supplies the real-RAM min-minus convolution bound; negating an input gives min-plus. The latter supplies output-sensitive dominance reporting with explicit exponential dependence on dimension. The package’s reconstructed coordinates and boundary conventions were checked independently, rather than relying on inconsistent printed indices in the older convolution display.

The [author’s institutional publication page](https://jeffe.cs.illinois.edu/pubs/necklace.html) confirms Algorithmica69(2) (2014),294–314 and a 2006 conference predecessor. The proof audited here is the complete retrieved author version, not a line-by-line comparison with the final publisher-layout journal PDF. All algorithmic priority is retained with the credited authors; the stale open-problem label does not confer new discovery credit.

## 3. Exact-count reduction, including repeated values

For strictly increasing values, the consecutive-window formula is immediate. With repetitions, the stronger implementation is correct: an interval either contains an entire equal-value run or none of it. A feasible interval may be tightened to the smallest and largest included values, so run starts and run ends characterize all possible optimal endpoints.

After shifting, $0\le t_j\le R$. The array masks keep only run ends in $A$ and reversed run starts in $B$. At coefficient $h=n+k-2$, a non-sentinel term satisfies

$$i+(n-1-j)=h\iff i-j+1=k.$$

Since $k\ge1$, this also ensures $i\ge j$. Thus the non-sentinel terms at the requested coefficients are exactly the feasible intervals of count $k$. Earlier convolution coefficients may have other interpretations, but they are not used as requested interval answers.

The sentinel separation is strict even when all values are equal. With $M=3R+1$, a term containing an input-mask sentinel is at least $M-R=2R+1>R$, while every valid interval has width in $[0,R]$. Therefore the test $C_h>R$ detects precisely infeasible counts. No infinite or floating-point sentinel is needed.

For a feasible coefficient the minimizing index $i$ determines $j=i-k+1$ and hence an actual attaining interval. For fixed $k$, minimizing the first convolution index $i$ among ties is also minimizing the left endpoint index $j$, so the implementation’s witness convention agrees with the independent endpoint oracle. Singleton input, all-equal runs, negative shifts, infeasible counts, rational coordinates and tied optima were all checked.

## 4. Block winners and dominance

The second sentinel $S=10M$ is distinct from the masking sentinel. Every true prefix-convolution coefficient has an in-range candidate of value at most $2M$. Any term using an out-of-range index costs at least $S-M=9M>2M$. Thus block padding cannot win globally, although padded candidates are safely included in local comparisons.

For each block start $r$ and shift $s$, the exact lexicographic dominance condition in equation(4) is equivalent to

$$(A_{r+\delta}+B_{s-\delta},\delta)
\le_{\mathrm{lex}}(A_{r+t}+B_{s-t},t)\quad\text{for every }t.$$

The real-coordinate equality case is resolved by $\delta-t\le0$. This uses ordinary ordered pairs, not an unspecified infinitesimal or precision-dependent perturbation. Consequently exactly one offset wins for every $(r,s)$, even for fully tied data. The total number of reports across all passes is exactly

$$\lceil N/d\rceil(2N-1).$$

The range $-(N-1)\le s\le N-1$ covers $s=h-r$ for every desired $0\le h<N$ and every block start. Reports outside that coefficient range are discarded only after being included in the count. Retaining the least pair of value and actual first index among block winners returns the global minimum with the promised witness.

## 5. Dominance correctness, including ties

The recursive reporter works over any totally ordered coordinate set, so lexicographic pairs are admissible. Sorting the last coordinate with red before blue at exact equality has an important consequence: a red point in the upper half and a blue point in the lower half cannot form an omitted dominating pair. If their coordinates were equal, the red-before-blue convention would put the red first instead.

Every pair is in exactly one of three disjoint classes: both endpoints in the lower half, both in the upper half, or lower red with upper blue. The first two retain all coordinates; in the third, the last coordinate is already valid and can be dropped. This proves both exhaustive reporting and absence of duplicates by induction. Empty colors terminate, dimension zero emits the Cartesian product, and the bounded-size case checks all remaining coordinates directly.

The corrected implementation follows precisely this recursion. Its shared output list prevents per-output recursive forwarding. Sorting uses only the last coordinate, color and integer label; it does not compare whole $d$-coordinate vectors as sort keys. Projection is implemented by decreasing the active dimension, without copying each full point vector again.

## 6. Uniform complexity audit

The dimension is not treated as a constant. Excluding output, the literal implementation permits the recurrence

$$T_d(m)\le T_d(\lfloor m/2\rfloor)+T_d(\lceil m/2\rceil)+T_{d-1}(m)+O(m\log(2+m)).$$

The two same-dimensional branches have smaller point counts, and the third has smaller dimension, so induction on $(d,m)$ is legitimate. For $m>16$, both halves are at most $17m/32$. Substitution of $C16^d m^{5/4}$ gives the contraction coefficient

$$\rho=2(17/32)^{5/4}+1/16<1,$$

where the exact inequality $17^5<32\cdot15^4$ certifies strictness. The remaining fixed slack absorbs sorting because $\log(2+m)/m^{1/4}$ is uniformly bounded. A single constant $C$, independent of $d$, works. At bounded $m$, the direct $O(dm^2)$ cost is absorbed by $16^d m^{5/4}$, and the dimension-zero scan is also covered. The corrected direct-append reporting contributes an additional $O(P)$ in total, not $O(P)$ per recursion level.

There are $d$ passes, each with $O(N)$ points and $d$ coordinates. Constructing those coordinates therefore costs $O(Nd^2)$, rather than an erroneously dimension-free bound. The choice

$$d=\max\{1,\lfloor\log_2N/16\rfloor\}$$

gives $16^d=O(N^{1/4})$. Thus all dominance work, coordinate construction and reporting cost

$$O(Nd^2+dN^{3/2}+N^2/d).$$

Both lower-order terms fit the claimed bound. For this choice, $d^4\le N$ and $d^3\le N$ (the case $d=1$ is immediate; otherwise $N\ge2^{16d}$), giving $dN^{3/2}\le N^2/d$ and $Nd^2\le N^2/d$. Finally $d=\Theta(\log(2+N))$ asymptotically, with the finitely many small cases absorbed in the constant. Taking $N=2n$ proves the stated $O(n^2/\log(2+n))=o(n^2)$ real-RAM bound.

The dimension can be computed by repeated integer doubling in $O(\log N)$ operations if bit-length is not taken as a primitive; that cost is harmless. No unit-cost operation on arbitrary coordinate bit strings is needed.

## 7. Model and verification limits

The claim counts exact real arithmetic, comparisons and ordinary array/index operations. The corrected Python implementation is an executable reference, not a promise that arbitrary-precision rational arithmetic has constant physical cost. Each derived coordinate uses a bounded number of input values; rational bit sizes and index lengths introduce additional polynomial overhead. This does not justify a subquadratic bit-time claim when input precision grows, and the package correctly does not make one.

The independent tests use direct geometric interval enumeration, direct prefix-convolution minimization and direct dominance pair comparison, with no copied optimization logic. They include 960 interval implementation runs, 204 generic convolution runs, 147 dominance instances, explicit lexicographic winner equivalences, exact report counts, both sentinel gaps and the recurrence arithmetic. Overridden small block sizes exercise nontrivial dimensional paths; timings or small tests are not used to prove the asymptotic bound.

From this report’s directory:

```sh
(cd author_replay && python verify.py > /tmp/interval-submitted.json && cmp verification.json /tmp/interval-submitted.json)
python independent_checks.py > /tmp/interval-independent.json
cmp independent_results.json /tmp/interval-independent.json
```

**Recommendation:** the original faster-algorithm alternative is fully covered in the stated real-RAM model. Classify this as a credited known resolution, with zero new-discovery attempts; the recorded reconstruction/validation family can remain documented separately. Preserve the publication-access qualification, the exact-count duplicate handling and the absence of lower-bound, fixed-exponent or bit-time claims.
