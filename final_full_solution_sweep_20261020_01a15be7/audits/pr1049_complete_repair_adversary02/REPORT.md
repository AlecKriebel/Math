# Fresh adversarial review of the complete PR1049 repair

Review completed 2026-10-22 UTC. Target: PR1049 / 2304015 / Hayman–Lingham Problem 4.15. This review did not consult the earlier review's verdict or execute its program. It read the two repair notes in full, all eight current PR files and the PR body, and all fourteen pages of the pinned Yakir v2 text. The original problem page was inspected visually. Existing source files were reused; no PDF mirror was created.

## Verdict and exact scope

**No remaining material mathematical objection was found to the combined repair.** The analytic reconstruction, joined to the corrected Jensen deduction, proves the exact original assertion for the open disk and algebraic multiplicity, as every integer n tends to infinity. This is an independently checked mathematical derivation from two explicitly stated classical background theorems. It does not assume Yakir's central Lemma 1.3 or his false pointwise Lemma 3.2.

For independent symmetric signs, let P(z)=sum_{j=0}^{n-1} X_j z^j and let N(P) count its zeros in |z|<1 with multiplicity. The strongest verified conclusion is, for all sufficiently large integers n,

Pr(|N(P)-n/2| >= n^(9/10)) <= C n^(-1/10) log^2 n.

The constant and the sufficiently-large cutoff need not be effective here. For the exact original family H(z)=sum_{k=1}^n epsilon_k z^k=zP(z), one has N(H)=N(P)+1 for every sign vector. Hence all but o(2^n) of the 2^n polynomials satisfy |N(H)-n/2| < n^(9/10)+1=o(n). There is no parity restriction.

The original arXiv proof **does not pass as written**: its Lemma 3.2 is false at real and conjugate-angle resonances, and its p.5 deduction contains the already identified sign and reciprocal-definition errors. The present pass applies to the identified combination of repair notes, not to every literal estimate or dependency of the uncorrected paper, and not to an uninspected journal typesetting.

This is an AI-assisted independent adversarial check, not independent human peer review, formal verification, a novelty certification, or a claim of current global firstness. The existing journal DOI is 10.4064/sm201117-28-1. A new upload, release, DOI, or journal-text-identity claim is not justified by this review.

## Immutable bindings and fresh state

The analytic repair reviewed is ANALYTIC_INPUT_REPAIR.md, SHA-256 79f263395ce93f11c9b80902bc3c718463af92b6440416631b0f6e8e54f013ac. The Jensen repair is PR1049_JENSEN_STEP_REPAIR.md, SHA-256 6f3e0dbc1b2f01533f08ea8fe1d6af5bfa8fc5992e0a74cba70e654ce78978c6.

The earlier 35-file SEALED_MANIFEST.json was located and independently rehashed. Its SHA-256 is f661ea18e22af3c081f6cce90a35471039616efe1688d11d29dfaaa81c4f00bd; all 35 recorded file sizes and hashes match. No author's verifier was run.

A fresh GitHub read confirmed open/draft PR1049, head 810d5bced8059fb0324c3d7d43b8e1d5f29449fa, with the same eight added files. Each file was fetched by that immutable head and compared character-for-character with the pinned UTF-8 input read here. All match. The PR body also matches the reviewed prior-resolution scope. No Git, index, ref, comment, merge, or provider write occurred.

The first substantive external operation was a fresh GWS CLI read: spreadsheet 1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20, numeric gid 1254632077, resolved tab Math Puzzles, complete A:AQ. The response has 191 rows including the header; all 43 requested columns were considered, with 39 trailing blank columns omitted by the values API. Target ID, DOI, arXiv, title, author and PR aliases were absent. Six generic Hayman matches identify other problems. The private raw response is sealed with a private flag and is not reproduced here. This is a contemporaneous snapshot, not an append lock or permission to mutate the ledger.

## 1. Original statement, all-n scope, and boundary conventions

The rendered Hayman–Lingham p.76 / PDF p.77 states the no-constant-term family with sum from k=1 to n and exceptional size o(2^n). No coefficient conditioning, parity subsequence, distinct-root convention, or per-polynomial little-oh tolerance is introduced.

The transfer uses the same n signs, not n+1 signs. Because P(0)=±1, H=zP adds exactly one simple root at zero. Repeated nonzero roots keep their multiplicities; roots on |z|=1 stay on that boundary. Thus N_open(H)=N_open(P)+1 is exact. Uniform probability gives |E_n|=2^n Pr(E_n), not an informal analogy between randomness and counting.

The repair establishes a deterministic tolerance n^(9/10)+1 shared by every nonexceptional vector. Its ratio to n tends to zero. All estimates are stated for sufficiently large integer n with constants uniform over the whole radial interval. Finitely many small n do not affect the asserted limit.

## 2. Foundational background: statements and hypotheses

The two nontrivial classical inputs are acceptable foundational results of a different scope from the random-polynomial theorem being audited. Their complete classical proofs were not rederived. Their primary statements and the application hypotheses were independently checked.

**Nazarov.** The primary Russian journal abstract gives the measurable-set inequality for h exponential terms with complex coefficients and exponents. Its factor is exp(|I| max |Re lambda_k|)(A|I|/|E|)^(h-1), with A absolute. Theorem I on printed p.5 of the primary PDF confirms an interval I and measurable E subset I of positive measure. For lambda_k=i m_k, the exponential factor is one. The theorem has no lower/upper coefficient-size assumption. The repair uses h<=20 after combining equal frequencies. Its E={|T'|<=b} is measurable. The zero-measure case needs no theorem. Thus neither changing r nor allowing coefficients larger than one violates an input hypothesis.

Primary references: [journal abstract](https://m.mathnet.ru/php/archive.phtml?jrnid=aa&option_lang=rus&paperid=397&wshow=paper), [primary PDF, Theorem I](https://www.mathnet.ru/links/4d5794739fc1cf305cbb78f8f4243cca/aa397.pdf). Fresh search exposed both statements; repeated direct archive opens timed out. No local background PDF is claimed.

**Bentkus.** The primary SIAM abstract states the convex-set bound for independent centered, potentially nonidentically distributed R^d vectors, with invertible covariance C^2 of the sum and error at most absolute constant times d^(1/4) sum E|C^(-1)Y_j|^3. In the application d=2 or 4 is fixed; the corrected good set gives covariance eigenvalues in [1/4,3/4] for sufficiently large n. Each summand has norm O(n^(-1/2)). Disks and Cartesian products of disks are convex Borel sets, including degenerate radii by limits. This provides the claimed rate for the actual events used.

Primary reference: [Bentkus, A Lyapunov-type Bound in R^d](https://epubs.siam.org/doi/abs/10.1137/S0040585X97981123). The abstract's nonidentical-summand and covariance requirements were read directly.

No dependency on Konyagin–Schlag's circle-root theorem is needed for the combined proof.

## 3. Uniform radial bounds, angular zeros, and Fubini

For |r-1|<=n^(-11/10), one has |j log r|<=C n^(-1/10) uniformly for 0<=j<n. Therefore all r^j and r^(-j) are bounded above and below by fixed positive constants, and c n<=S_r=sum r^(2j)<=C n. Cauchy–Schwarz yields |P(r e^(i theta))|/sqrt(S_r)<=sqrt(n) for every sign vector.

The Cauchy root bound applied to P and its reversal gives 1/2<|beta|<2. In logarithmic modulus the omitted leading sign contributes zero, so the repaired factorization with (n-1)log r-log sigma_r is correct. For a in a fixed annulus, circular distance t from theta to arg a gives

|e^(i theta)-a|^2=(1-|a|)^2+4|a|sin^2(t/2).

Thus the negative logarithmic singularity is bounded by C+|log |t||, uniformly even as a crosses the circle or repeated roots occur. The positive part is uniformly bounded. Minkowski gives ||log|p_r|||_4<=C n, hence integral |log|p_r||^4<=C n^4.

There are only finitely many sign samples. This absolute product-space bound justifies the angular/expectation and double-angular interchanges. Values at the finitely many angular zeros may be redefined on a null set. It is unnecessary and generally false that the pointwise expectation at theta=0 or pi is finite. The repair never uses that false assertion.

## 4. Small values: attacks on cancellations, constant phases, and exponents

The smoothing inequality follows by applying K(u)=(sin u/u)^2 to Y/a and using its nonnegative triangular Fourier transform. It applies to discrete Y; no density or nonlattice assumption occurs. Passing from complex modulus to the real part only enlarges the event.

The elementary cosine inequalities imply

|g_theta(lambda)| <= exp(-n/pi^2) exp(H_lambda(theta)/pi^2),
H_lambda=sum_j cos(2 lambda r^j cos(j theta)).

For H_lambda<n/2 the integrand is exponentially small uniformly. On H_lambda>=n/2, its tenth power is nonnegative, so Markov legitimately uses integral H_lambda^10. Expanding produces real phases T=2 sum_{ell=1}^{10} s_ell r^(k_ell)cos(k_ell theta), not arbitrary complex phases.

A constant phase forces every nonzero index to have balanced positive and negative signs. All nonzero multiplicities are even. Because ten is even, the zero-index multiplicity is even too, although its signs need not balance. This proves O(n^5), including constant nonzero phases. An independent pairing proof bounds their number by 945*2^10*n^5: pair opposite signs at each nonzero index, pair the remaining zeros arbitrarily, choose one index for each of five pairs, then choose ten signs. Counting only identically zero phases would be wrong.

For a nonconstant phase, combine identical Fourier frequencies first. A coefficient of T' then has size at least c: it is a nonzero integer multiple of k r^k, with integer k>=1. Uniform radial bounds provide c independently of n,r,tuple. Parseval consequently gives sup|T'|>=c. There are h<=20 distinct terms and h>=2 because a nonzero real periodic derivative has paired frequencies.

With b=n^(-120), Nazarov gives mu{|T'|<=b}<=C b^(1/(h-1))<=C n^(-120/19)<=C n^(-6). T'' is not identically zero. The equations T''=0 and T'=±b each have O(n) roots per period because a nonzero trigonometric polynomial of degree at most n has at most 2n zeros. Splitting at these points produces O(n) pieces on which T' has fixed sign, is monotone, and |T'|>=b. Integration by parts on each gives O(1/(|lambda|b)); the variation term is the variation of 1/T', at most 2/b. The claimed bound

|integral exp(i lambda T)dmu| <= C(n^(-6)+n^(121)/|lambda|)

therefore has the right dependence and applies to all the relevant phases. Zero or repeated Fourier coefficients, negative lambda, radial coefficients outside [1/2,1], tangential level contacts and wrapping the angular endpoint cause no loss beyond the stated constants.

Dividing the tenth-moment bound by (n/2)^10 gives C(n^(-5)+n^(121)/|lambda|), capped by 1. Smoothing over |lambda|<=1 contributes O(a), and integrating 1/|lambda| from 1 to 2/a contributes O(a log(1/a)). Thus

q_r(a)<=C[n^(-5)+a+n^(121)a log(1/a)].

At a=n^(-400), the final term is n^(-279)O(log n), uniformly dominated by n^(-5). No desired moment lemma has been assumed or hidden in this step.

## 5. Four covariance resonances and the Gaussian comparison

For d(eta)=distance to 2pi Z, the exact geometric sum yields

W_r(eta)=(1-r^(2n)e^(i n eta))/(S_r(1-r^2 e^(i eta))),
|W_r(eta)|<=C/(n d(eta)).

The denominator identity (1-r^2)^2+2r^2(1-cos eta)>=c d(eta)^2 is valid uniformly, including r=1 off the resonance. This avoids unstable subtraction.

The complete bad set excludes d(2theta), d(2phi), d(theta-phi), and d(theta+phi) <= n^(-1/2). These respectively cover real-axis points (including pi and wraparound), the diagonal, and conjugate angles. Each strip has measure O(n^(-1/2)); their finite union does too.

Product-to-sum formulas express every covariance error through these four W_r values. Outside the bad set V=(1/2)I_d+O(n^(-1/2)) in operator norm. The uniform covariance lower bound is therefore valid, and the sum of normalized third moments is O(n^(-1/2)); nonidentical coefficient vectors are permitted by Bentkus.

For completeness the Gaussian interpolation derivative contains both the determinant/trace and quadratic terms. Since every V_s eigenvalue lies in [1/4,3/4],

integral |d f_s/ds| <= 8 d ||V-(1/2)I_d||.

Integrating s gives O(n^(-1/2)) total variation. Hence the disk/product-disk CDF approximation is uniform over all nonnegative thresholds. For negative thresholds one simply defines the exponential CDF to be zero. This is the intended harmless domain convention for the repair's displayed suprema.

The source's omitted exclusions are substantive, not cosmetic. At theta=pi/2 and phi=-pi/2, the squared moduli are identical. For n divisible by four their marginal tends to Exp(1), so the joint-minus-product CDF at (1,1) tends to e^(-1)-e^(-2)>0. At theta=pi the marginal is one-dimensional real rather than circular complex. The corrected set removes both failures at a negligible angular cost.

## 6. Tails, endpoint atoms, BV truncation, and moments

Put f=log|p_r| and A_theta={|P(r e^(i theta))|<=n^(-400)}. The deterministic L^4 bound and q_r<=C n^(-5) give, by Cauchy–Schwarz on the actual product spaces,

E integral |f|1_A <= C n q_r^(1/2)=O(n^(-3/2)),
E integral integral |f(theta)f(phi)|1_A_theta
 <= [E(integral f^2)^2]^(1/2)q_r^(1/2)
 <= C n^2 q_r^(1/2)=O(n^(-1/2)).

The union of A_theta and A_phi is controlled by summing these absolute bounds. No independence between angles or samples is used here.

For v=n^(-800)/S_r and U=|p_r|^2, g(x)=(1/2)log x 1_{v<x<=n} exactly equals f1_A^c at U, because U<=n. In particular the lower threshold is for the unnormalized P; v is of order n^(-801), not n^(-400). Both endpoint conventions matter for a discrete law.

An explicit atom-safe proof of the BV step is

g(x)=(log v)/2 * 1_{x>v}
     + integral_v^n 1_{x>t} dt/(2t)
     -(log n)/2 * 1_{x>n}.

This is valid at x=v and x=n as well as elsewhere. The signed measure in t on the right has total mass zero and total variation log(n/v)=O(log n). Thus a univariate CDF error epsilon controls the expectation by epsilon TV(g). For the product, write each g in this form. The upper-tail joint probability is 1-F_theta(s)-F_phi(t)+F_joint(s,t). Total mass zero annihilates its constant and marginal terms, leaving the joint CDF error bounded by epsilon TV(g)^2. All inequalities use probabilities of <= events exactly, so endpoint atoms require no density assumption or informal integration-by-parts convention.

For independent exponential comparison variables, the expectation factorizes. Removing [0,v] and (n,infinity) costs O(v|log v|+e^(-n)log n)=O(n^(-800)); the logarithmic integral is -gamma. The excluded-angle contribution is at most bad-set measure times O(log n), or O(log^2 n) for the product. Adding the proven tails yields the two centered moments with O(n^(-1/2)log^2 n), uniformly over the stated radial interval.

This verifies the central analytic input rather than transferring it to a new unsupported uniform-integrability or two-point lemma.

## 7. Jensen deduction with boundary roots retained

Use t=log r, delta=(1/10)n^(-11/10), J(t)=integral log|P(e^(t+i theta))|dmu, and psi(t)=(1/2)log sum_j e^(2jt). The radii exp(±delta) lie within the analytic interval for all sufficiently large n.

Direct differentiation gives psi'(0)=(n-1)/2 and psi''(t)=2 Var_t(j)<=(n-1)^2/2. Each forward/backward secant differs from n/2 by at most n^(9/10)/20 once n^(9/10)>=20. The fixed factor 1/10 is essential to this convenient numerical margin.

The exact Jensen hinge formula is

J(t)=log|P(0)|+sum_alpha max(0,t-log|alpha|).

It is valid at circle roots by angular logarithmic integrability. The left derivative at zero is the open-disk count; the right derivative additionally includes every boundary multiplicity. Convexity therefore gives

[J(0)-J(-delta)]/delta <= N_open <= [J(delta)-J(0)]/delta.

No reciprocal polynomial or boundary-root probability estimate is needed. An upper count deviation forces L(delta)-L(0)>=(19/20)delta n^(9/10); a lower count deviation forces L(0)-L(-delta)<=-(19/20)delta n^(9/10). The signs are correct.

Each difference has second moment O(n^(-1/2)log^2 n), by the already proved centered moments and (u-v)^2<=2u^2+2v^2. Squared Markov divides by a threshold of order n^(-2/5), giving n^(-1/10)log^2 n. Dependence between radii is immaterial. Combining both tails and the exact H=zP transfer proves the asserted full target.

## Independent controls and limits

finite_controls.py is newly written, read-only, and was run successfully. It does not import, call or mirror the author's verifier. Its checks include:

- Exhaustive enumeration of 4^10 signed frequency choices for n=2: 184756 constant phases, of which 121252 are nonzero constant phases. This catches the incorrect practice of treating only identically zero phases separately.
- Exact binomial CDF calculations at conjugate angles for n=16,64,256: joint-minus-product gaps stay above 0.23; exact real-axis CDF at n=256 is about 0.712 versus 0.632 for Exp(1).
- Exact rational Jensen secants for roots of log radii -1,0,0,1. The near-zero backward secant is 1, forward secant 3, open count 1 and closed count 3. Repeated boundary multiplicity is explicit.
- The strict-upper-tail BV representation checked at both endpoints and on joint discrete laws with endpoint atoms.
- Exact rational arithmetic for the Turan exponent -120/19, second tail exponent -1/2, Jensen threshold exponent -1/5, and final probability exponent -1/10.

These finite controls are falsification diagnostics, not a numerical proof of an asymptotic theorem. The mathematical derivations above carry the asymptotic conclusion.

No material mathematical gap remains in the combined repair at the stated scope. Administrative promotion, if considered later, must retain the existing-paper credit, the false source-lemma disclosure, the independent reconstruction's actual scope, and the lack of journal-text comparison. It must re-read the live ledger immediately before any accounting write. This review performs no such write.

