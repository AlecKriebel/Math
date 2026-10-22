# Independent adversarial audit: assembly and moments

**Frozen submission:** PR 218, problem 30006020, head `dc457c741c779fbf90fbfdcdc73f750b3716f561`.

**Disposition within this family's scope:** no blocking analytic defect found. The ideal assembly's mesoscopic PPP limit and all fixed joint compact-window moment limits follow from the submitted argument. The transfer to the actual geometric law is valid **conditional on the precise credited geometric hypotheses** below. This report makes no novelty or priority judgment and does not certify external source numbering or scope.

## Independence and evidence

The independent derivation was sealed in `INDEPENDENT_SEAL.json` before access to inherited reviews, root reconstruction/conclusions, source-checker outputs, or sibling reports. None of those materials has been read in this family. The sole submitted text read was frozen `CANDIDATE.md`, pinned by SHA-256 in `SOURCE_PINS.json`. No external papers or third-party full texts were fetched. All fresh files are confined to this family's assigned folder. No provider, repository, index, ref, deposit, tracker, or outreach mutation was performed.

The checkable proof reconstruction is `INDEPENDENT_DERIVATION.md`. Fresh exact finite tests and explicitly nonvalidated floating diagnostics are in `fresh_checks.py` and `FRESH_CHECK_RESULTS.json`.

## Results by attempted falsification route

| Mechanism / attempted defect | Evidence and boundary cases | Status / exact gap |
| --- | --- | --- |
| Ordered-composition normalization loses repeated-size factors | k!/prod C_j! orderings exactly cancel the submitted 1/k!, yielding prod a_j^C_j/C_j!. Exact rational normalization checked for n=1,...,10 by literal ordered enumeration. | Verified analytic identity; no missing symmetry factor. |
| Dirichlet integration or D prefactor introduces a k-dependent mismatch | Factorial integral yields 1/(2j) per part; division by 2^k k! yields the stated D/k!. Direct factorial cancellation gives (8); 1,225 exact cases checked, g=2,...,50 and 1<=k<g. | Correct conditional on the submitted starting polynomial (5) and exact mixture conventions. |
| D flattening fails at cutoff rounding | log successive ratio=O((k+1)/g); accumulated error O(k_cut^2/g)=o(1). Small inadmissible k need not be used; comparison starts at k=1. | Verified. |
| H product or fractional analytic branch is invalid | Normally convergent canonical logarithm defines B and B^t on |z|<4. Telescoping product gives B(1)=sqrt(2). Convolution with generalized binomial coefficients gives the stated constants for every fixed t>0. | Verified, including t=1.1. |
| Residual coefficient ratio is used beyond its regime | Global square-root envelope handles residual zero; uniform convergence to 1 is used only for r=o(n). Large selected totals in the moment bound are controlled by Gamma tails instead. | Verified; no hidden uniformity near r=n. |
| Exact factorial moments miss tuples with repeated j | Falling factorials select distinct parts even when sizes coincide. Literal exact checks cover 422 selectors, 261 with repeated selected size. Residual size zero is included. | Verified. |
| Joint moment limits do not imply joint count / point-process limits | Higher fixed moments give tightness and uniform integrability; any subsequential limit has independent-Poisson mixed moments, determined by the Poisson total count's exponential moments. Local expected counts give vague tightness. | Valid standard argument; fuller justification supplied in independent derivation. |
| Arbitrarily slow q -> infinity defeats marking | Middle contribution O(q^-1/2); small-j contribution O(log(q+2) exp(-a(1-log2)q)); large-j contribution exponential in j. The potential sqrt(n) coefficient loss occurs only above n/2 and is beaten there. | Verified for every q -> infinity with q=o(n), without q/log n -> infinity. |
| Random normalization invalidates the point-process limit | T~Gamma(2n,1) exactly; T/(2n)->1 in probability. Positive dilation is jointly continuous in the vague topology. No independence is needed for Slutsky. | Verified. |
| Marked/normalized count moments are not uniformly integrable | Split selected total at n/2. Large totals force one j>=n/(2r), with exp(-c_r n) marking probability. Total-normalization exceptions contribute <=n^r exp(-cn). Uniform higher moments follow for every fixed order and finite union of windows. | Verified; constants may depend on the fixed order, as allowed. |
| Polynomially rare bad mass still carries unbounded moments | At t=1.1, eta=.6 log(1.1)-.05=.00718610788259>1/220. Splitting Chernoff tails at L log n yields E K^p=O((log n)^p); Cauchy-Schwarz gives O((log n)^r n^(-c/2)) bad moment mass. | Correct conditional on actual K generating and graph-excess inputs. Cutoff rounding changes a constant only. |
| Uniform latent RN comparison does not justify moments, or is misused for signed tests | Positive uniform unnormalized weight ratios remain uniform after conditional normalization. It applies to the nonnegative moment statistics used here. Its error multiplies a uniformly bounded model conditional moment. Signed tests would need an additive E|f| bound, but no multiplicative signed claim is used. | Verified conditional on the starting uniform correlator comparison. |

## Conditional geometric inputs retained as an exact gap

These are not established by this analytic family:

1. The exact positive latent one-vertex area mixture, including polynomial (5), height weighting, graph symmetry factors and Dirichlet total 2n (CANDIDATE lines 61–85).
2. The uniform relative correlator error (6) throughout all positive compositions and k<=floor(.6 log(2n)) (lines 70–72).
3. The actual cylinder-count bound E[1.1^K]=O(n^.05), in the specified principal-stratum ensemble and iterated sampling law (lines 106–108, 125).
4. The uniform low-k multivertex relative excess O((log g)^25 g^-1 2^k) (lines 117–125).
5. The exact fixed-genus area-law and multicurve/surface correspondence used to identify the actual law.

If these inputs hold in precisely the stated scope, they imply the claimed total-variation approximation and actual-law moment transfer. In fact the submitted bounds allow the actual bad probability to be O(n^-eta): the graph-error exponent 1-.6 log 2 approximately .58411 is much larger than eta, even after its logarithmic factor. No sharpened rate is required for the theorem.

## Fresh computation and its limits

All exact finite checks passed. The rational checker cancels common powers of pi using Bernoulli-number formulas for zeta(2j), then directly enumerates ordered compositions; it did not import submitted code. The floating coefficient recurrence diagnostics at n=4096 give:

- h_n / [sqrt(2/pi)n^(-1/2)] approximately 1.0000152681.
- [z^n]H^1.1 / [2^.55 n^(-.45)/Gamma(.55)] approximately 1.0000151151.
- E[1.1^K]/n^.05 approximately 1.1354071316.

These finite, nonvalidated numerical diagnostics support constants and do not establish asymptotics or geometric hypotheses. The proofs above provide the asymptotic justification.

**Strongest independently verified result:** the full ideal-model analytic theorem, plus the logical actual-law transfer under the five explicit geometric inputs. **Remaining gap in this family:** independent source verification of those geometric inputs and scope. No source-priority claim is assessed.
