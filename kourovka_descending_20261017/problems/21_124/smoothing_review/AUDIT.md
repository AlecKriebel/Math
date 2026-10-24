# Fresh adversarial audit of height convolution and rational positivity

UTC: 2026-10-24T22:57:34.023233+00:00. **PASS for the corrected supporting criterion**, with exact hashes in RECEIPT.json. Review completion: **100%**. Discovery completion estimate for full21.124 remains **4%**. This is a nonauthor audit, with a separate independent secondary check. No author files were changed by the reviewers. This is neither an originality audit nor a complete Kourovka solution review.

## Exact accepted scope and corrections

For finitely many integer pairs(pi,qi), the reviewed criterion equates finite nonnegative-integer projected-multiset couplings, with a nonzero required horizontal component, to a finite horizontal support carrying rational functions defined and **strictly positive at every real z>0**, satisfying the exact rational-function kernel identities. It does not establish the existence of this finite rational kernel from CAT(0) metrics or covariance constraints.

Two literal defects were corrected by the author and the final bytes freshly reread:

1. A shift in Z cannot clear negative X,Y exponents. Q=X^-1 is an immediate counterexample to the original phrase “ordinary polynomial.” The corrected output is a polynomial in Z whose coefficients are Laurent polynomials in X,Y with nonnegative integer coefficients. No horizontal shift is asserted. This matches exactly the intended finite integer triples, which can have negative horizontal coordinates.
2. The illustrative family now explicitly has **integer** m≥1. Its sharp exponent4m−3 is not an integer for arbitrary real m≥1.

INITIAL_FINDINGS.json preserves the original proof hash, counterexample and resolutions. The corrections do not change the underlying smoothing lemma or finite-coupling equivalence.

## Uniform coefficient positivity, including endpoints

Let a nonzero Laurent slice be q(Z)=Z^r f(Z), where f is an ordinary degree-d polynomial with nonzero constant and leading coefficients. Because Z^r>0 on the positive axis, f is strictly positive there. Its nonzero constant coefficient must be positive by its limit at0 from the right; its nonzero leading coefficient must be positive by its sign for large positive arguments. These conclusions remain valid when r is negative, or when the un-factored polynomial originally vanished at0.

The degree-d homogenization F(x,y)=sum c_j x^j y^(d−j) is positive on the whole simplex x,y≥0,x+y=1. Interior points reduce to f(x/y)>0; the endpoints use the just-checked leading and constant coefficients. Compactness and continuity give a strictly positive minimum ε. Degree0 is a positive constant, and degree1 already has two positive coefficients; these cause no exception.

For M=N+d≥d and0≤k≤M, elementary factorial cancellation gives

    binom(N,k−j)/binom(M,k) = (k)_j (M−k)_(d−j)/(M)_d,

with zero for out-of-range binomial indices. Thus the author's normalized coefficient formula is correct, including the boundary values k=0,M. Zero falling factorials handle impossible success/failure counts. Choosing M large avoids any vacuous M=0 parametrization in the limiting argument.

An independent proof gives a uniform quantitative bound. Interpret the last ratio as the probability of the ordered pattern of j successes followed by d−j failures under sampling without replacement from M labels, of which k are successes. Sampling with replacement has pattern probability(k/M)^j(1−k/M)^(d−j). Conditional on having no repeated labels, it has precisely the without-replacement law. A union bound puts the probability of any repetition at most binom(d,2)/M. Hence the difference of pattern probabilities is bounded by that quantity, **uniformly in k**, including both endpoints. Therefore the entire normalized coefficient differs from F(k/M,1−k/M) by at most

    binom(d,2) * sum_j |c_j| / M.

This is below ε for all sufficiently large M. Every normalized coefficient is then positive. The result follows by dehomogenizing. This independently verifies the author's finite-product uniform argument without a hidden interior-only asymptotic assumption. No external positivity theorem is needed.

There are finitely many nonzero slices. For each slice choose a valid exponent N; taking the maximum works because further multiplication by1+Z preserves nonnegative coefficients. Restore the factored powers Z^r, choose one common height shift to make all height exponents nonnegative, and clear all finitely many rational denominators by a positive integer. Multiplication by a nonzero common height polynomial cannot annihilate a nonzero slice in the integral domain Q[Z±1], and different horizontal labels never mix. Horizontal support and each required a- or b-nonzero slice are therefore preserved. If Q is identically zero the lemma is vacuous and N=0 suffices; the nonzero-witness criterion separately rules out empty required support.

Strict positivity is essential. A nonzero nonnegative-coefficient Laurent polynomial evaluates positively at every z>0. Consequently q=(Z−1)^2, although nonnegative on the positive axis, can never become coefficientwise nonnegative after multiplying by(1+Z)^N: it stays nonzero and vanishes at1. The endpoint conditions also cannot be silently imposed before factoring out the lowest monomial.

## Rational denominator clearing and both directions

Necessity is immediate but was checked at the right support: collect exactly the nonzero height slices of the finite positive multiset and discard zero slices. Every such slice is strictly positive for all positive real z, including when some height exponents are negative. The projected-multiset equalities are coefficientwise Laurent identities and yield the rational kernel identity. The required nonzero horizontal slice is retained.

For sufficiency write each nonzero rational weight as reduced p_s/q_s. Since the weight is defined on every positive real argument, the reduced denominator has no positive real root. Squaring each denominator and multiplying gives D=product q_s^2, strictly positive on that whole open axis. It clears every denominator: D p_s/q_s is an ordinary rational-coefficient polynomial. Even if q_s has a root at0, D is positive on the open positive axis; an initial power of Z in the cleared slice is harmless because it is factored out before applying the lemma. A negative constant sign of a denominator is also harmless after squaring. Removable singularities must first be removed, exactly as the author states.

All cleared slices are strictly positive because D and every weight are positive. Multiplication by D preserves every kernel identity. Apply the already-proved common smoothing, the common height shift and positive integer denominator clearing. The final expression is coefficientwise nonnegative and preserves every horizontal slice. The projection differences are now Laurent polynomials. Their vanishing as rational functions implies their vanishing as Laurent polynomials, since Q[Z±1] injects into Q(Z). Thus the final projected multisets agree exactly, with multiplicities, and the finite integer coefficients give the stated finite construction.

For the version requiring two nonzero horizontal coordinates, exactly the same support-preservation argument retains both. This does not introduce a new hypothesis that any particular individual triple must have both coordinates nonzero.

## Common height convolution and the sharp example

Substituting X=Z^pi,Y=1 or X=1,Y=Z^qi leaves a multiplier H(Z) unchanged on both sides, so multiplication by any Laurent H(Z) preserves the identity. Coefficientwise nonnegative H is finite common height convolution. Signed H is algebraically allowed only if the final coefficients are nonnegative; the author does not claim arbitrary signed H preserves multiplicities. The small exact identity(1+Z)(1−Z+Z²)=1+Z³ demonstrates the permitted situation. Horizontal monomial shifts generally do not preserve the identities and are correctly absent from the corrected construction.

For integer m≥1, f_m=(Z−1)^2+Z/m is strictly positive. The coefficient numerator stated in the note is correct. Maximizing k(M−k) gives the middle index. At even M the minimum numerator is M(M−4m)/(4m); at odd M it is(M−1)(M−(4m−1))/(4m). Since M=N+2≥2, the first nonnegative case is M=4m−1, so N=4m−3, with two zero middle coefficients. This is an all-integer-m proof; the finite computation is supplementary.

## Independent reproduction and limits

Run `python3 smoothing_review/independent_check.py` from the problem directory, or invoke its absolute path from anywhere. Only Python's standard library is needed. The script hashes the final proof, manifest, author checker and frozen author result before and after; it verifies all manifest file hashes, and runs the author checker only in a temporary copy.

Its independent exact arithmetic covers37,874 falling-factorial/binomial identities and uniform probability bounds,100 sharp-family cases with20,200 coefficients,21 additional smoothing cases of degrees0,1,2,4,6, and101 failures at the positive-root boundary. It also clears two distinct positive denominators, retains negative horizontal labels, applies a common smoothing exponent14, and constructs an81-type finite positive multiset satisfying five projection identities. A separate17-type control verifies a heterogeneous slope pair(pi,qi)=(1,2), with weights proportional to1+Z and1. These are reproduction controls for the mechanism, not evidence that every possible slope system has a positive kernel.

No substantive objection remains to the corrected supporting criterion. The real unresolved assertion is exactly the one the author labels blocked: produce a suitable finite rational-function kernel which stays positive on the **entire** positive axis for the general eligible group. Point samples, local Taylor data or a compatible Gram matrix are not substituted for that assertion. No full21.124 resolution, original-discovery claim or publication approval is made here.
