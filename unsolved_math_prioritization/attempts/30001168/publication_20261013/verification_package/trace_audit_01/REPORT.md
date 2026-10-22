# PR 822 / 30001168: independent spectral and rational-arithmetic audit

**Decision: ACCEPT this mathematical family.** No correction to the frozen author proof is needed within this scope. The round heat trace is uniformly below 129/200, and the finite-cylinder variational estimate with L=10000 is above 13/20 after the stated normalization. A separately implemented certificate actually proves the stronger round bound 321/500. This is an independently checkable spectral/arithmetic review; final project promotion also requires the separate geometry family and later priority review.

Completion: 100% of the assigned trace-family audit. Exact UTC completion and input/output digests are in DECISION.json, INPUT_VERIFICATION.json, and RESEARCH_LOG.jsonl. No source edits, Git/PR/Zenodo/sheet mutations, central problem search, or external communication occurred.

## 1. Frozen claim, exact target, and independence

Frozen head: `c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c`. The original queue status was exactly `claimed_solved`, effort 1/5. All 42 files in `source/` were verified after replay against the sibling SOURCE_MANIFEST.json, and every byte count and SHA-256 matches. The author proof SHA-256 is `f95c74037c1d3bc3437c03ea8211fad796e374a93b462697f81a6c3e91a647cc`.

I read the original author proof, reconstructed the spectral reasoning, checked the dataset payload through an immutable read-only SQLite connection, and saved INDEPENDENT_RECONSTRUCTION.md before opening certificate code or prior AUDIT.md / SECOND_REVIEW.md verdicts. After that checkpoint I read and inspected all three supplied arithmetic implementations, their wrappers, and the prior mathematical reviews. The new witness imports none of them.

The exact official source is section 9, item (16), Conjecture 1, printed pp. 421-422 of [Low Eigenvalues of Laplace and Schrödinger Operators, OWR 6 (2009)](https://ems.press/content/serial-article-files/46205). I inspected both complete target pages in the PDF text and rendered images. The retrieved PDF has 638962 bytes and SHA-256 `a3ab668409f786c7c1783150d9f937b2d6e06471a48b76c5721b58a49bf3a683`. The relevant claim compares the positive-time maxima of the volume-normalized weighted Yamabe and round scaled heat traces for every n>=3, with smooth strictly positive weights in the original round L2 space. The adjacent monotonicity claim has n>=4 scope. The dataset canonical review hash is `0f73b6392b73ca2e1294a961a56b4729d60540884ab899fd488c8e11885a718c`; its prior research report is empty. Its background reference to an adjacent Hardy inequality does not change this target.

A counterexample in n=3 gives a full negative answer to the universal comparison. It does not resolve the comparison restricted to n>=4, and it does not settle the separate monotonicity record 30001169. No additional scalar-curvature, minimizing-metric, or weight-amplitude assumption appears in the primary question. Historical novelty and priority have not been searched in this family.

## 2. Exact round spectrum and heat trace

On the unit S3 the degree ell harmonic eigenvalue is ell(ell+2). Its multiplicity is

    binomial(ell+3,3)-binomial(ell+1,3) = (ell+1)^2,

with the second term zero when ell<2. This follows by decomposing homogeneous polynomials in four variables into harmonic polynomials plus squared radius times lower-degree polynomials. The round scalar curvature is 6, so Y0=Delta+R/8=Delta+3/4. Setting j=ell+1 yields eigenvalue j^2-1/4 and multiplicity j^2, including ground eigenvalue 3/4 with multiplicity one. Therefore

    F(t) = t^(3/2) sum_{j>=1} j^2 exp(-(j^2-1/4)t)

is exactly the desired round expression. Neither a zero mode nor the 3/4 potential may be dropped.

Let Theta(t)=sum_{j in Z} exp(-t j^2). Poisson summation gives

    Theta(t)=sqrt(pi/t) sum_{m in Z} exp(-pi^2 m^2/t).

Both sides and their derivatives converge uniformly on every compact positive-time interval. Differentiating and multiplying by -t^(3/2)/2 gives

    t^(3/2) sum_{j>=1} j^2 exp(-t j^2)
      = sqrt(pi)/4 [1+2 sum_{m>=1}(1-2pi^2 m^2/t) exp(-pi^2 m^2/t)].

The positive potential factor is exp(t/4). For t<=1 each correction is strictly negative, so

    F(t) < sqrt(pi) exp(1/4)/4 < 1773/3000 < 129/200.

The second strict step uses sqrt(pi)<1.773 and exp(1/4)<sum_{k>=0}(1/4)^k=4/3. This works arbitrarily close to zero; it is not finite-time sampling.

## 3. Author's interval envelopes, rounding, and large times

For a=k/100 and b=(k+1)/100, 100<=k<=199, the author uses

    F(t) <= b sqrt(b) [sum_{j=1}^3 j^2 exp(-a(j^2-1/4))
                      +32 exp(-63a/4)]    for a<=t<=b.

Every replacement has the correct direction: t^(3/2)<=b^(3/2), and exp(-lambda t)<=exp(-lambda a). For j>=4 and a>=1, the consecutive tail ratio is at most

    (25/16) exp(-9) < (25/16)/(1+9) = 5/32 < 1/2.

Thus twice the j=4 summand bounds the entire omitted spectral tail. The 100 closed cells cover the complete [1,2] with both endpoints.

The integer-square-root routine is valid even though it first floors the rational radicand multiplied by the squared scale: for any real z>=0, floor(sqrt(floor z))=floor(sqrt z). Its result r=(floor(10^9 sqrt(b))+1)/10^9 satisfies r^2>b, including perfect-square b, and the code explicitly checks the bracket. There is no possible downward rounding in the prefactor.

For x>0, P64(x)=sum_{m=0}^{64}x^m/m! is strictly below exp(x), so 1/P64(x) is a strict upper bound for exp(-x). Large tail arguments cause no convergence or cancellation problem: all terms are positive rational numbers, and this direction does not require bounding the omitted exponential remainder. The 100 exact comparisons replay successfully; the largest displayed outward upper bound is 0.643380136594 on [189/100,190/100].

For each lambda>=3/4, t^(3/2)exp(-lambda t) is nonincreasing for t>=2, because its logarithmic derivative is 3/(2t)-lambda<=0. Comparing positive summands at two times and summing proves F(t)<=F(2) for all t>=2. The last closed cell includes 2. This avoids any infinite derivative interchange and completes the original all-time bound.

## 4. Independent stronger finite witness

The new check_trace_bounds.py uses an independent coarser modal envelope, different exponential degrees, different root precision, and the angle identity

    pi = 8 atan(1/3)+4 atan(1/7).

Indeed tan(2 atan(1/3))=3/4, and adding atan(1/7) gives tangent one. The sum lies in the first quadrant: both component cosines are positive and the addition cosine has positive factor 1-(3/4)(1/7). Thus the sum is pi/4. Twenty-four alternating arctangent terms give a lower bracket and the next positive term gives an upper bracket. The computed brackets prove 3.14<pi<22/7 and 1.772<sqrt(pi)<1.773. This identity was not used by any supplied certificate.

For x>=0 and x<N+2, the independent code evaluates a positive Taylor polynomial by direct powers and factorials, and uses

    P_N(x) <= exp(x)
      <= P_N(x) + [x^(N+1)/(N+1)!]/[1-x/(N+2)].

Every ratio after the first omitted term is bounded above by x/(N+2), so the upper tail is justified. The code uses degree 14 for exp(1) and exp(7/20), and reciprocal degree 50 lower polynomials for the negative exponentials. Integer lattice bisection at scale 10^8 supplies independently checked strict root upper bounds. Every acceptance calculation is a Fraction or integer comparison. Displayed upper decimals are rounded upwards by one lattice unit; they are not acceptance inputs.

For small time 0<t<=7/5 the Poisson corrections are negative, giving

    F(t) < (1.773/4) exp(7/20) < 0.629001690913962.

Write A(t)=t^(3/2)exp(-3t/4), and let B contain all j>=2 modes. A increases to t=2. Every summand in B decreases already for t>=2/5. For a>=7/5 the j>=3 consecutive ratio is at most (16/9)exp(-7a)<1/2, as certified by (16/9)/(1+7a)<1/2. Hence

    B(a) <= a^(3/2)[4 exp(-15a/4)+18 exp(-35a/4)] = T(a).

On each [a,b] below, separate monotonicity proves F(t)<=A(b)+T(a):

| Closed interval | Certified outward upper envelope |
| --- | --- |
| [7/5,3/2] | 0.631337454925643 |
| [3/2,8/5] | 0.636142909076604 |
| [8/5,17/10] | 0.639463656855985 |
| [17/10,9/5] | 0.641171473944811 |
| [9/5,19/10] | 0.641201034994492 |
| [19/10,2] | 0.639540524418950 |

As before, the t>=2 comparison reduces to the endpoint already covered. Exact rational values for every envelope are recorded in EXACT_RESULTS.json. Thus

    F(t) < 321/500 < 129/200       for every t>0.

This is an upper bound on the true maximum, not its exact numerical value. The small-time region, the six closed middle cells, and the monotone large-time extension supply seven analytic bounded-region checks and cover all positive time.

## 5. Finite-cylinder variational sum and normalization

This family independently checked the spectral implications of the geometry; smooth compactification and conformal covariance also receive a distinct geometry audit. For the fixed smooth metric g_L containing an exact product cylinder of length L=10000 and unit S2 radius, R=2 on the cylinder and its Yamabe potential is +1/4. The S2-constant Dirichlet sine modes have Rayleigh eigenvalues

    mu_k=1/4+(pi k/L)^2.

The zero-extended functions have zero boundary traces and belong to the global H1 quadratic-form domain. Their normal-derivative jumps cause no jump in the functions or distributional first derivatives. Their first k span is k-dimensional, orthogonal for both form and norm, and has largest Rayleigh quotient mu_k. Min-max therefore bounds the kth eigenvalue of the full closed operator, with its true multiplicity, by mu_k. It follows termwise that

    Tr(exp(-4Y_gL)) >= exp(-1) sum_{k>=1} exp(-4pi^2 k^2/L^2).

Passing from finite sums to the infinite sum preserves the inequality by monotone summation. No cap decoupling, convergence of spectra, omission of necessary angular multiplicities, or truncation of the actual closed spectrum is needed. Additional modes strengthen the lower bound.

For the positive decreasing Gaussian, the integer sum is at least its integral over [1,infinity), and the latter is at least its integral over [0,infinity) minus one. The result is L/(4sqrt(pi))-1. The standard Gaussian integral gives the factor 4sqrt(pi), not 2sqrt(pi). This lower bound is positive for the specified L.

The transition estimate gives V_L<=4pi(L+4): each of two caps has radial integral below 1+8/(3e^3)<2. The normalized metric is h=a g_L with a=(2pi^2/V_L)^(2/3), and its weight W=aW_L. Thus a^(3/2)V_L=2pi^2 is precisely the required round-measure integral of W^(3/2). Constant metric rescaling gives Y_h=a^(-1)Y_gL. At t_*=4a, including the prefactor as well as the heat exponent gives

    t_*^(3/2) Tr(exp(-t_*Y_W))
      = (16pi^2/V_L) Tr(exp(-4Y_gL))
      >= (sqrt(pi)/e) (L-4sqrt(pi))/(L+4).

The unitary conformal identification supplies the original weighted operator in round L2. All exterior weight powers and the volume measure agree with the primary source. The normalization does not allow keeping time equal to 4.

Bounding each positive factor independently in the right direction yields

    lower > (1772/2719)(10000000-7092)/10004000
          = 1106714561/1700054750.

The exact margin above 13/20 is

    1106714561/1700054750 - 13/20 = 3357947/3400109500 > 0.

In particular the claimed 1/200 separation between thresholds is valid. Our stronger round bound would also give a threshold separation 13/20-321/500=1/125, but no strengthening of the frozen claim is necessary.

## 6. Positivity, limiting times, and literal maxima

For fixed smooth positive W on compact S3, multiplication by W^(-1/2) is bounded and invertible. The weighted form is at least (3/(4 max W)) times the round L2 squared norm. Smooth ellipticity gives compact resolvent and finite heat traces for t>0. This uses no nonnegative-scalar-curvature assumption on the transition caps.

The common normalized small-time leading coefficient is (4pi)^(-3/2)2pi^2=sqrt(pi)/4. At large time, if lambda_1>0 and the heat trace at 1 is finite,

    Tr(exp(-tY)) <= exp(-(t-1)lambda_1) Tr(exp(-Y))    (t>=1).

Therefore the scaled trace tends to zero. Both scaled traces are continuous for positive times. The finite-cylinder value exceeds the Weyl limit. The round first mode at t=2 alone exceeds the same limit; the independent certificate proves this with lower root and upper positive-exponential brackets. A continuous function exceeding both boundary limits attains its supremum in a compact subinterval of positive times. Thus interpreting the source's max literally causes no defect.

## 7. Software audit and falsifiable controls

I inspected the code before replay, including all inequality directions, interval coverage, positive Taylor tails, range-reduced alternating Taylor brackets and outward squaring, square-root enclosures, pi/e proofs, normalized lower bound, and threshold comparisons. The original author, first audit, and second-review certificates all reproduce their archived RESULTS bytes under isolated normal and -O Python. Semantic checks independently require the problem ID, dimension and finite L where supplied, exact thresholds and lower rational, correct interval counts, author's 613 checks, and worst interval. All three associated wrappers pass both modes.

The supplied audit control runner reproduces its complete archived 34-case output under both top-level optimization modes: four relocated baselines are accepted and thirty variants are rejected. Each run itself checks child normal and -O modes. Temporary directories were forced under ignored private_sources. The original second-review wrapper also reaches its two mathematical negatives under each mode.

The new replay_and_controls.py contains sixteen additional direct semantic negatives, eight in each optimization mode. All four certificates reject a too-short cylinder and a falsely tightened round bound with the exact expected mathematical diagnostic, avoiding stale-hash-only failures. The new independent certificate gives identical ordinary and optimized output. The replay harness itself also passed under normal and -O execution; it uses explicit exceptions, not assert.

A deliberate boundary control replaces the analytic Y0 potential in a copied PROOF.md by the false half-sized potential and recomputes the author manifest, leaving certificate arithmetic unchanged. The author wrapper accepts both modes, as expected. This is a useful falsifiable demonstration that hash integrity plus a rational certificate cannot certify analytic prose. It does not invalidate the independently reconstructed analytic lemmas. None of the wrapper successes is used as a substitute for the Poisson identity, smooth compactification, conformal covariance, form-domain argument, min-max, ellipticity, or heat asymptotics.

All source files remained frozen. REPLAY_CONTROLS.json records 34 harness cases (including the two full 34-case supplied-control runs), every expected rejection, both analytical-scope demonstrations, and exact stdout digests where relevant. Checkable new arithmetic is in check_trace_bounds.py and EXACT_RESULTS.json; the derivations making it an all-time claim are in this report.

## 8. Strongest verified result and exact remaining gap

Within this family, no mathematical gap remains: the full round spectrum, infinite tails, arbitrarily small and large times, exact middle envelopes, finite Gaussian min-max lower sum, normalization, strict rational margins, and attainment of the comparison maxima have all been checked. The proof is finite-L and gives a legitimate n=3 negation once the separately audited smooth conformal construction is supplied.

The exact project-level dependencies remaining outside this family are the separate geometry family's final judgment, a distinct dated priority/literature review, and any later promotion or preprint review requested by the root workflow. The n>=4 restricted comparison and record 30001169 remain unresolved. This report makes no historical novelty, human peer-review, or formal proof-assistant claim.
