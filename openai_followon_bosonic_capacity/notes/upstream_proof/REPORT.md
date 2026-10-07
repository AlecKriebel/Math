# Independent analytical audit of family 273

Audit date: 2026-10-06 (America/Los_Angeles). Auditor: independent subagent `upstream_proof`. Pinned read-only checkout: `/Users/alec/Desktop/math`, commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

## Scope and verdict

The required input is, for every finite integer n>=1, every n-mode state rho with finite expectation of the total number operator, and every t in [0,1],

`S(L_t^{tensor n}(rho))/n >= g(t g^{-1}(S(rho)/n))`,

with natural logarithms, independent vacuum environment, and arbitrary correlations and entanglement inside rho.

I read the entire analytical EPnI proof (sections 01–05), independently rederived its pivotal coefficient and trace identities, and actively sought counterexamples to the sharp interpolation construction. **No substantive mathematical gap or counterexample was found in that proof in this audit.** The desired vacuum bound follows from Theorem 1 by substituting the n-mode vacuum in the second independent port. The vacuum has zero entropy and energy, and g^{-1}(0)=0; applying increasing g proves the stated bound.

This is an analytical audit of a specific pinned source, not conventional human peer review or a reproduced Lean kernel check. The formal build and broader semantic audit belong to a separate agent. Follow-on coding theorems and their infinite-dimensional operational reductions are outside this subtask.

## Pin and evidence

Manuscript: `preprints/The-entropy-photon-number-inequality-September-24-2026/paper.pdf`.

| File | SHA-256 |
|---|---|
| paper.pdf | d826f8ebe18596419871100e79611868dff2a45a4aa157433c58e6f49a234d82 |
| build/sections/02-interpolation.tex | fa0efd354ad4de0c006c259d638bb443e8d2a67b66aef372881379521ddf04ee |
| build/sections/03-minimization.tex | 1c8b906076233a4457610751d47ca3b884116c48c003dbaef336aa59e4228d5b |
| build/sections/04-metric.tex | 78647b07afec54d8bd45dc7afd6ead24ac2bd8c5e903ff5bd51cd6b2029c60cb |
| build/sections/05-stationarity.tex | f0e23fdd40c3a25deccf1faf0df0f60d5374208018876cb571e57df908abf717 |

The family README supplies author OpenAI, title *The entropy photon-number inequality*, year 2026, and BibTeX key `OAI:The-entropy-photon-number-inequality-September-24-2026`; use its exact manuscript-specific citation. Public path history was checked through the GitHub read-only API at `2026-10-07T04:14:10Z`. It showed only the pinned initial commit and no later family correction; response saved in `upstream_current_history.json`. This did not update the pin.

## Dependency ledger

Line references are to pinned `build/sections/` sources.

| Dependency | Assumptions and result | Checked source | Remaining gap |
|---|---|---|---|
| Energy compactness/entropy continuity | Fixed finite n and common finite total-number bound; compact trace-norm energy ball, continuous entropy, S<=n g(E/n) | 01-preliminaries.tex:47–78; cutoff tail mass <=E/(K+1), tail entropy <=q n g(E/(qn)) ->0 | None found; oscillator Hamiltonian essential |
| Four-weight interpolation | Diagonal positive weights, finite source parameter values, multiplier-invariant tests; four comparisons imply sharp F comparison | 02-interpolation.tex:32–44,51–106,149–336,338–430; independent reconstruction below | None found |
| Regularized minimum | Positive thermal references, thermal slack port, output replacement, relative-entropy and fourth-moment penalties | 03-minimization.tex:9–102,178–277; coercivity/majorant check | None found |
| Gibbs regularity | kW^4+W^{1/2}BW^{1/2}, k>0 and bounded B>=0; faithful Gibbs state with seventh moment | 03-minimization.tex:109–174; inverse form and number-coordinate identity | None found |
| Component Hessian comparison | At minimizing states only; finite eigenblock perturbations and centered finite eigenblock output tests | 03-minimization.tex:279–429; independent coefficient/duality check | None found; no universal channel contraction asserted |
| Product-port arithmetic comparisons | Independent ports, arbitrary internal states; centered one-port projections orthogonal | 04-metric.tex:35–57 | None found |
| Defect norm/convolution | Finite energy for weak identities; seventh moments and fourth-order log bound for logarithmic sums at minima | 04-metric.tex:137–239,241–291; independent trace-order check | None found |
| Generator covariance/stationarity | Seventh moments, H<=CW^4; weighted generator trace class | 05-stationarity.tex:23–153,155–256; independent cutoff/algebra checks | None found |

The analytical proof does not import an unproved EPnI or multimode minimum-output theorem. The nontrivial Stieltjes ingredient is proved within the manuscript. Prior entropy-power and Gaussian-optimizer papers provide context, not the missing sharp step.

## Interpolation reconstruction

Set f(x)=x/sinh(x), b(x)=x coth(x), with value 1 at zero. The four weights are m f(x)e^{+/-x}, m f(y)e^{+/-y}. Positive sums and parallel sums preserve comparison for arbitrary maps: split source tests into coordinatewise parallel-sum minimizers, which remain admissible by multiplier invariance, and use unrestricted target minima. Finite source parameter values permit pointwise source limits, while target limits use Fatou. Logarithmic-mean and reciprocal-logarithmic-mean integrals give comparisons for m, m f(x)^2 and m f(y)^2. No multiplication of two known comparisons is used.

Define B(f(x)^2)=b(x). Its extension uses s=(u/sin u)^2 and B(s)=u cot u. On u=p+iq, q>0, 0<p<p_*(q), p_* tan p_*=-q tanh q, sin(u)/u is in the fourth quadrant. The manuscript's numerator signs are correct; p tan p has strictly positive derivative on (pi/2,pi). Boundary pieces map to axes. The bound |sin(u)/u|>=sinh(q)/sqrt(pi^2+q^2) prevents escape at infinity, giving properness. The formula

`Im(u cot u)=[q sin(2p)-p sinh(2q)]/[cosh(2q)-cos(2p)]<0`

rules out critical points: a'=0 would imply u cot u=1. A connected proper unbranched cover of the simply connected quadrant is one-sheeted. This constructs the holomorphic anti-Pick B. Positive-axis boundary inversions are unique; the u^2 expansion handles s=1, giving B(1)=1, B'(1)=-1.

Herglotz applied to -B gives the Stieltjes representation of G=(B-1)/(1-s). H=sG has nonnegative imaginary part and positive real-axis values, hence no upper-half-plane zero. R=1/H is positive and anti-Pick. Herglotz applied to -R, positivity at infinity, and monotone convergence eliminate its linear coefficient and give an ordinary Stieltjes representation. Finally -B'(s)=(1/2)(1/s+R(s)) has the asserted positive Stieltjes representation.

The weight E=m(t-s)/(2(B(s)-B(t))), continuously E=-m/(2B'(s)) when s=t, is therefore constructed using comparison-preserving sums and parallel sums. Adding E|phi|^2 to the four-form scalar quadratic and minimizing gives precisely m f(x)f(y)/f(x+y). The paper explicitly checks y=x, y=-x and x=y=0. No division by zero is concealed in the special metric frequencies.

`check_interpolation.py` is a seeded exploratory falsification program using only Python's standard library (seed 27320261006). It checks 50,000 arbitrary real 2x2 map/weight cases: the largest sharp-target/four-hypothesis norm ratio was 0.9895938309000101, with no sampled failure. It also checks 50,000 complex-domain samples of the actual u-parametrization, q from 0.001 to 100, with no failure of Im(s)>0, Im(B)<0, or Im(-B')<=0. Saved JSON explicitly labels this numerical evidence, not proof or interval certification. The analytical reconstruction above is the verification basis.

## Variational and stationarity checks

A strict finite-energy violation survives normalized number cutoffs by entropy continuity under common input/output energy bounds (03:9–14). If both input entropies vanish, no violation occurs because the claimed lower bound is zero. Thus the output reference has a positive finite limiting mean in the contradiction setup. Zero input-entropy references are approached from above; g(r)/h(r)->0. Faithfulness is imposed only on regularized minima, not on the original states.

The thermal slack port precedes epsilon, allowing both (1+epsilon)sum lambda_i r_i<=r0 and (1+epsilon)sum lambda_i(r_i+1)<=r0+1. Replacement kappa is chosen afterward, with its bound depending on fixed references; only zeta tends to zero at the end. No simultaneous limit is required.

Negative entropies grow logarithmically with energy while the positive epsilon term grows linearly, yielding a uniform energy bound for minimizing sublevels even as zeta decreases. For each fixed zeta>0, the moment term gives a fourth-moment bound. Entropy continuity and lower semicontinuity give attainment. Replacement implies rho0>=kappa tau_r0 and H0<=CW0; positive slices satisfy T_iH0<=C_iW_i. Replacing output entropy by cross entropy is a majorant with equality at the minimum. Its Gibbs free energy therefore identifies the actual input minimum as a faithful Gibbs state with seventh moment and the exact log identity. This does not assume differentiable infinite-dimensional entropy.

The relative-entropy difference identity yields Hessian duality with alpha=(1+epsilon)w_i h0/hi. I rechecked the normalization: Dout<=alpha Din, its output Gibbs variational lower bound gives source dual coefficient (1-kappa)^2/(alpha hi), hence (1-kappa)^2||T_iZ-centered||_i^2<=(1+epsilon)w_i||Z||_0^2. Dividing by lambda_i produces the stated component estimate. No missing h0 factor occurs.

The product-port arithmetic comparisons and thermal slack provide precisely the four interpolation hypotheses. Source frequency multipliers preserve centering even with the identity tail, since all diagonal entries have frequency zero. F is bounded above/below for fixed positive references, permitting completion and bounded number-basis tests independently of the varying eigenbases.

For v=log(p_l/p_r)/h and K=(r+1)p_r-rp_l, the coordinate coefficient of q is K conjugate(d'_{lr}). The identity K/(h ell)=(1-v)F gives dual norm sum (1-v)K|d'|^2. Its difference from entropy-production sum -vK|d'|^2 is e'-nr; the CCR contributes exactly n. The log/moment estimates give absolute convergence.

The raw defect convolution uses sum lambda_s r_s=r0; discarded weak commutators have zero trace after number cutoffs. Centering the replacement correctly adds kappa(1-kappa) conjugate(mu_gamma)Tr[(gamma-tau_r0)Z]. Generator covariance is valid before product restriction: coefficient-1 damping is rotation invariant and discarded heat commutators vanish under partial trace. Seventh moments justify W^2-sandwiched trace convergence; H<=CW^4 allows pairing the log identity with generators algebraically, without a two-sided positive path rho+t delta.

Substituting entropy production, number drift and centered energy gives exactly

`0=||q0||_*^2-(1+epsilon)A_*^2-epsilon M_*^2-kappa(1-kappa)|mu_gamma|^2+zeta P`.

Signs and constants agree. The fourth-moment drift has leading coefficient -4, so P has a uniform upper bound. The defect comparison gives A_*^2+M_*^2=O(zeta). Uniform-energy trace-norm compactness gives a limit. Finite number-basis tests make d^dagger Z and Z d^dagger bounded finite rank, so uncentered identities pass to the limit without energy or unbounded-mean convergence. Their recurrence eliminates off-diagonal entries and all internal correlations, forcing the fixed product thermal states. Entropy convergence makes the entropy objective tend to zero; the remaining penalties are nonnegative, contradicting the strict negative minima.

## Boundaries and limits of the conclusion

- n is fixed finite in each application; no uniform cutoff rate in n is assumed.
- t=0 and t=1 are exact equality; vacuum and entropy-zero states are included.
- Convert natural-log results to bits by dividing every entropy, g and information quantity by log(2), consistently. Photon-number inverse values then agree.
- No stronger photon constraint is used. The theorem requires finite total mean energy of the individual state. Ensemble applications must separately establish almost-sure finite energy and average-energy control.
- Environment independence is essential; entanglement within the signal is allowed, memory correlated with the environment is outside scope.
- This proves no thermal-channel quantum capacity, amplifier entropy bound, two-way-assisted capacity, or confidential-broadcast formula beyond a separately established coding model.
- The EPnI breakthrough belongs to the supplied OpenAI manuscript. Dynamic-capacity reduction must be attributed to the original coding/converse sources; this audit establishes no priority for that implication.

## Formalization caveat

Actual declaration: `OAI.EntropyPhotonNumber.entropy_photon_number_inequality`, `lean/OAI/InformationTheory/PhotonNumber/Inequality.lean:689–702`. Its explicit hypotheses match finite energy on full untruncated lp Fock space and actual beam-splitter partial trace. Basic.lean uses nonnegative energy summability and continuous functional calculus for entropy; it does not encode a finite truncation as the original state.

`MutuallyUnbiased/.../Canonical273.lean` files are unrelated naming coincidences. The Comparator challenge ends in intentional sorry and is not the proof. Textual search found no sorry, axiom, admit or unsafe within PhotonNumber. No build was run on the read-only source checkout; no kernel-check claim is made here.
