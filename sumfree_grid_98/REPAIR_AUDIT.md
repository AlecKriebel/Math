# Adversarial audit of the local proof repairs

Date: 2026-10-20 UTC.

## Disposition and scope

**PASS for the requested local repairs and numerical certificate obligations, subject to the explicitly identified analytic and imported-theorem dependencies.** No new mathematical obstruction was found in these repairs. This is not a machine-formalized proof, a peer-review determination, a novelty claim, or a solution of the exact finite maximum problem.

Reviewed inputs: the authored `REVIEW.md` and `verify_slice_exact.py`, saved rational brackets, the locally retrieved text of Keevash–Lim v2 (especially §§2–4 and Appendix A), and the copied supplied script. No remote action was taken. This pass used the source text; it does not independently repeat the earlier rendered-PDF visual inspection or source-authenticity checks.

Deliverables:

- `check_repairs_independent.py`: standalone, Python-standard-library-only checker. It imports neither the previous checker nor SciPy. It consumes only saved rational brackets, ignores saved PASS flags, decimal ratio values, and endpoint-sign annotations, and freshly verifies the mathematical inequalities.
- `REPAIR_CHECK_RESULTS.json`: independently generated result.

## 1. Universal hub

The actual positive-edge condition is `0 <= r-i-u <= (d-2)n`. The denominator is positive for all states in `J=[max(0,r-(d-1)n), min(n,r)]`, and every integer in `[0,(d-2)n]` is an attainable bounded-composition sum. Thus this edge condition is both necessary and sufficient.

For `r<=n`, `h=0` works. In the middle range `n<=r<=(d-1)n`, the proposed `h=max(0,r-(d-2)n)` belongs to `[0,n]=J`. Its two endpoint inequalities are `r-n-h>=0` and `r-h<=(d-2)n`. The first follows from `h<=r-n`, using `d>=3`; the second is immediate from the definition of `h`. Since the expression is affine in `i`, these endpoint inequalities cover every state. In the final range, `h=n` works because `r-2n>=0` and the upper bound is attained at `i=r-(d-1)n`.

The overlapping endpoint choices agree. The hub itself is a state, so its self-loop is present. Irreducibility yields uniqueness of the finite-chain stationary distribution; the self-loop additionally yields aperiodicity, though aperiodicity is not necessary for uniqueness. The theorem's case `n=0` is trivial and can be handled separately. The checker exhaustively confirms the endpoint inequalities for 35,175 triples with `3<=d<=12`, `1<=n<=30`, and every `0<=r<=dn`; the general proof above, not finite enumeration, establishes the claim.

## 2. Root existence, uniqueness, and identification with the optimizer

The exact bracketing argument needs continuity plus uniqueness on the specified interval, not the implication `0 in g([a,b]) => a root exists`.

For `d>=2`, the Irwin–Hall density is positive on `(0,d)`, symmetric about `d/2`, and strictly increasing on `(0,d/2)`, strictly decreasing on `(d/2,d)`. Strictness can be obtained without assuming strict log-concavity: start from the triangular `f_2`, then use `f'_d(x)=f_(d-1)(x)-f_(d-1)(x-1)` and symmetry. For `0<x<d/2`, the first argument is strictly closer to the mode of `f_(d-1)` whenever both are in the support; the support boundary cases also give strict positivity. For `d>=3` this proves the required monotonicity inductively.

Consequently `g(u)=f_d(u)-2f_d(2u)` is strictly increasing on `[d/4,d/2]`; it is negative at the left endpoint and positive at the right. It has exactly one root there. For `0<u<=d/4`, `f_d(2u)>f_d(u)`, so `g(u)<0`. For `d/2<=u<d`, `f_d(2u)=0` and `g(u)>0`. Since the slice-volume derivative is `-g(u)`, the interior root is the unique maximizing slice parameter. The trivial zero of the density equation at `u=0` must not be counted as an optimizer. Statements of unique zero should explicitly say the prescribed interior interval, not all of `[0,d/2]`.

The independent checker additionally enforces that each bracket lies in `[d/4,d/2]`, contains two distinct ordered endpoints, and has strict exact opposite endpoint signs. It rejects missing, duplicate, out-of-order, or extra dimension records. Those structural guards were not explicit in the earlier script, although its actual saved brackets satisfy them.

## 3. Exact densities and interval bounds

The density formula follows by differentiating the inclusion–exclusion volume formula for the cube cut by a halfspace. For `d>=2`, the density is continuous at integer knots, and the zero-power ambiguity does not arise because the exponent is `d-1>=1`. Density is zero at and outside the support endpoints.

The new implementation reflects `x` to `min(x,d-x)` before evaluating the exact integer numerator, an implementation difference from the earlier checker. It also cross-checks the result against the corrected B-spline recurrence

`(d-1)f_d(x)=x f_(d-1)(x)+(d-x)f_(d-1)(x-1)`

at all third-integer grid points from just below to just above the support, for `3<=d<=12`. These tests include support boundaries and integer knots. The recurrence coefficient is `d-x`, not `d+1-x`.

Unimodality gives the interval minimum from the two endpoint values and the interval maximum from those values plus the mode if contained. This remains valid if an argument interval crosses a support endpoint. The independent checker verifies the two required inequalities directly by cross multiplication of rational quantities; no rounded reciprocal or decimal threshold is used.

All 197 brackets for `d=4,...,200` pass. Separately, 40 steps of exact rational bisection, without any floating-point root proposer, certify dimensions 3, 200, and 201:

- d=3: A lower display 6.872983346169064; B lower display 3.936491673084532.
- d=200: A lower display 4.311939254933009; B lower display 2.1560064808634753.
- d=201: A lower display 4.311822731633256; B lower display 2.1559478504849166.

These decimals are descriptive only. Acceptance uses `100*A_numerator >= 201*A_denominator` and the corresponding exact `99/100` second inequality. The saved 4–200 bracket set has its smallest displayed A and B lower bounds at d=200.

## 4. Analytic tail and the d=200/201 boundary

For a negative tilt `-lambda`, the mean is `1/lambda-1/(exp(lambda)-1)` and the variance is `1/lambda^2-exp(lambda)/(exp(lambda)-1)^2`. The mean is increasing in the exponential argument; the subtracted function `E/(E-1)^2` is decreasing for `E>1`. The earlier interval directions for both mean and variance are therefore correct.

The independent implementation uses 80-term rational Taylor sums, rather than the earlier 100 terms, and a geometric upper bound on the positive tail. Every remaining successive-term ratio is at most `x/(n+2)`, so this is a genuine enclosure. At D=200 it certifies both required positive window gaps and `(200*delta-1)^2 > 600*variance_upper`. The function `(D*delta-1)/sqrt(D)=delta*sqrt(D)-1/sqrt(D)` has positive derivative for positive D and delta, extending each inequality to every D>=200.

It also explicitly checks the bootstrap `exp(12/5)>2`, proving alpha<1/2 before the local ratio estimate is applied. Symmetry and g(d/3)<0 give alpha>0. The exact exponential tests then yield `77/1000<alpha<145/1000`. All four reflected density arguments relative to `(d-1)/3` are checked to lie in [-1,1]: offsets `1/3+alpha`, `alpha-2/3`, `1/3-2alpha`, and `-2/3-2alpha`. The last offset is the closest to the edge and is still at least `-287/300 > -1`.

For the first ratio, `1-3alpha>1/2` and `exp(4/5)>201/100`. For the second ratio, the certified rational upper bound has display `0.9618436364516034 < 0.99`. These are the needed inequalities, independent of the printed inconsistent decimal calculation.

The analytic argument needs the window for both f_d and f_(d-1), so it starts at d=201. The finite check includes d=200. Fresh exact checks of d=200 and d=201 confirm the overlap/transition has no missed dimension. The new checker does not turn the analytic argument into a theorem prover: log-concavity under convolution, the mean–mode bound, and the monotonicity extension are justified mathematically, not by enumerating infinitely many dimensions.

## 5. Final LP error

Let `Delta(x)=|S(x)|-|S*(x)|` and `H=A union B union D union E`. Both fiber cardinalities lie in `[0,n+1]`, so `|Delta(x)|<=n+1`. Lemma 4.3 supplies `sum_H |W-1|=O(n^(d-2))`. Therefore

`|sum_H (W-1)Delta| <= (n+1) sum_H |W-1| = O(n^(d-1))`.

The assembled weighted inequality bounds `sum Delta + E` from above, with `|E|=O(n^(d-1))`; hence it bounds `sum Delta` from above with the same order error. This is precisely the missing direction. A merely one-sided upper comparison of the weighted sum by the unweighted sum would not suffice. The authored absolute-value repair is valid without knowing the sign of Delta on H.

## 6. Fail-closed behavior and remaining qualifications

Commands run successfully:

- `python computation/check_repairs_independent.py`
- the same command under `python -O` and `python -OO`.

All three produced byte-identical result JSON. A corrupted d=4 bracket `[1,1001/1000]` failed with `ValueError: d=4: right sign` in all three modes. The verifier uses explicit conditional exceptions, no assertions. The earlier script remains assertion-sensitive and should not be presented as safe under optimization; this new checker closes that operational limitation without modifying it.

The imported interval-mixability theorem, external d=1,2 base results, and fiber inequalities remain dependencies. This pass audited the requested repairs, not every detail of every imported result, the manuscript's separate convex-body discussion, or arbitrary finite-instance certificate files. Nothing here establishes peer-reviewed status or an exact finite-cardinality formula. The qualified asymptotic-only disposition is preserved.
