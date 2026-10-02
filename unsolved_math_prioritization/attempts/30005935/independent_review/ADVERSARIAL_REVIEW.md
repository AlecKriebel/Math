# Independent full five-turn mathematical review: 30005935

## Verdict

**PASS_SCOPED_FIVE_TURN_PACKET. No mandatory revision found.**

The packet proves a negative result for the intended superlinear unconditional mean-square assertion: in its admissible one-dimensional example, the actual coupled mean-square error is infinite at every grid index at least two. It also proves a positive, compatible bounded-Lipschitz path-law bound of order [log(eM)]^(-2). Its finite unbounded-linear-test obstruction is sound and must remain distinguished from bounded-test convergence.

The broader source weak-rate question is not fully disposed of: the packet neither establishes a positive algebraic weak order nor a higher-dimensional sup-norm/path-law theorem. A broad-source disposition of **unresolved/unsolved after 5/5 author turns**, retaining the proved strong-error refutation and the scoped weak theorem, accurately represents the work. This review does not certify novelty or publication priority.

## Frozen evidence

The review binds the 45-file author packet to FINAL_AUTHOR_MANIFEST.json SHA-256

    421c94fc9b79cd27dfdc8a99baba57f941788a3a2b42dd704611ae892f44a10a

The supplied final author commit is 7738d03d0e2b80d5ae55f435eb5c3e183264c27b. All 44 entries in the final manifest and the manifest itself were independently checked locally. The 87 historical entries in the first four turn manifests remain exact. Eight primary/dependency PDF hashes match their manifests. All five author checkers were replayed without modification; their stdout matches the saved receipts byte-for-byte, totaling 62,188 exact assertions.

Two separately written review checkers import none of the author code. They add 31,770 symbolic/rational controls: 18,578 for the stochastic/algebraic identities and 13,192 for cutoff scaling and bounded-test rate bookkeeping. These controls supplement, rather than replace, the analytic review below. FROZEN_BINDINGS.json records the proof/source bindings, and AUTHOR_REPLAY.json records the complete replay receipt.

## 1. Primary-source match and formula fidelity

The full Cohen contribution in [OWR 26/2024, printed pp.1495–1498](https://ems.press/content/serial-article-files/49484) was read. The critical p.1496 display and question were visually checked. The cited [time-noise paper](https://arxiv.org/abs/2304.11064), Sections 2–3 and its displayed geometric-Brownian substep on PDF p.4, was independently inspected, including the image.

The intended update includes multiplication by the old value. The report's equation (2) and the time-noise paper's equation (5) omit that factor, while the latter's equations (6)–(8), initialization of the stochastic substep, and linear exactness statement require it. The packet explicitly uses this substep-defined method. This is a justified reconciliation, rather than an unnoticed change of algorithm.

The selected setting is one common real Brownian motion in the Itô sense, homogeneous Dirichlet data and g(v)=v^(5/4) on nonnegative states. The later space-time-white-noise discussion is a different question. The source separately raises a weak-SPDE rate without fixing a test class or exponent. The cited Bossy–Jabir–Martínez proposition uses bounded C4 tests and additional moment/dissipativity assumptions; these cannot be imported wholesale for the present drift-free superlinear coefficient. The packet preserves these boundaries.

The raw problem record reconstructs a conjunction containing the strong half-order assertion and an additional weak-rate request. The strong member is refuted by the packet's d=1 example. Treating that refutation as an answer to every possible bounded weak question would overstate the source, and the author does not do so.

## 2. Turn 1: finite paths and infinite second moment

The nonlinear map v exp(v^(1/4)z−tau v^(1/2)/2) is continuous at zero and bounded for each fixed finite z and positive tau. Setting a=v^(1/4) makes the log derivative 4/a+z−tau a; its stated positive maximizing root is correct. Heat positivity and the Dirichlet semigroup then give finite continuous iterates, with strict interior positivity for a nonzero nonnegative initial profile. Nothing in this argument supplies a uniform moment bound, and the proof does not assert one.

The conditional first-moment identity is valid by the Gaussian exponential identity and conditional Tonelli. The noise is shared across space. Consequently the conditional second moment has the cross factor exp(tau V(y)^(1/4)V(z)^(1/4)), rather than a product appropriate to independent pointwise noises. This common-noise calculation was checked directly.

The interior heat-kernel minimum over compact intervals is strictly positive. It produces V(y)≥C exp(bZ_0) on a deterministic receiving interval when Z_0≥0. Substituting in the cross-moment integral gives a positive double-exponential term in Z_0, which dominates the Gaussian density's quadratic decay. The conditional integral is finite for every fixed Z_0, but its average is infinite. The proof correctly uses this analytic tail argument rather than finite sampling.

## 3. Turn 2: moments above one and the exact coupled error

### Uniform kernel ratio and all later indices

The small receiving interval can be chosen uniformly over the first Gaussian increment. The ratio is controlled before integration, on a compact product where K_tau(y_0,z)>0, and all input weights are nonnegative. Thus V(y)/V(y_0) stays in [1−eta,1+eta] for every first increment, with a deterministic interval.

Log-Jensen on the normalized outer kernel is legitimate because V is positive and bounded above and below on that compact interval for each fixed first increment. Integrating the next Gaussian produces the stated coefficient

    (tau/2)[p² sqrt(1−eta)−p sqrt(1+eta)].

Its positivity is exactly equivalent to p²(1−eta)>1+eta. The selected eta satisfies it. This yields infinite numerical moments for every p>1 at the second step. For later steps, conditional first moments and conditional Jensen reduce to the same formula with a longer positive outer heat kernel. This extension does not require an unjustified independence of the intermediate fields.

### Scalar comparison and SPDE construction

The Itô transform R=4Y^(-1/4) gives diffusion coefficient −1 and drift 5/(2R), hence Bessel dimension six. This was recalculated both forward and backward. The radial Gaussian representation and nonhitting-zero property were checked against Lawler's cited notes. The radial density calculation gives integrability for p<3/2, with no estimate on the expected running maximum being presumed.

The cutoff construction is sufficient for a canonical global local mild solution. For each globally Lipschitz cutoff, the positive part of u^K−Y^K has zero boundary trace even though the scalar comparison process itself does not satisfy Dirichlet data: u^K has boundary zero and Y^K is nonnegative. Therefore integration by parts gives the claimed dissipative term. The quadratic variation term is bounded by the cutoff Lipschitz constant times the positive-part energy. Localization, globally Lipschitz moments and Gronwall justify the comparison.

This C1/Lipschitz energy argument does not invoke the older cited positivity theorem's stronger C2 noise assumption. It supplies the needed comparison directly. Until the scalar process reaches K, the exact cutoff solutions agree and stay below Y. Since Y is finite and continuous on every compact time interval, the cutoff exit times exhaust every finite horizon. Patching is therefore valid, and the stochastic convolution is used locally, not under an unproved global L2 condition.

For any r>1, choose 1<p<min(r,3/2). The exact solution has a finite p-th moment at the fixed positive time, while the numerical value does not. The triangle inequality excludes a finite p-th moment of their difference, and L^r containment then excludes the r-th moment. In particular the coupled mean-square error is infinite. This is a valid comparison of random variables; no subtraction of two infinite expectations occurs.

## 4. Turn 3: strict loss of the exact weighted mass

The principal eigenfunction phi=(pi/2)sin(pi x) is positive, integrates to one, and has eigenvalue −pi². Testing the locally stopped mild equation gives the weighted stochastic equation. Jensen yields sigma_t≥exp(−lambda t/4)V_t^(5/4), while sigma_t/V_t≤||u(t)||_infinity^(1/4) on positivity. Defining the ratio at zero and using the linear stochastic-exponential equation proves strict positivity of V. The local pathwise boundedness needed for this step follows from the scalar comparison, not an unstated integrable maximum.

The time change is valid with a_t=sigma_t/V_t^(5/4). Its clock is strictly increasing, finite at each finite physical time and at least c_T=2(1−exp(−lambda T/2))/lambda. A_T is a stopping time in the inverse-clock filtration: the event that it has been reached is determined by the inverse clock. It is not assumed independent of the resulting scalar process. The finite-lifetime extension is covered by the cited DDS construction, whose Theorems 5.8–5.9 and enlargement discussion were checked directly.

The optional-sampling inequality has the correct direction. For n≥c_T, A_T wedge n is a bounded stopping time no earlier than c_T. Apply the supermartingale inequality to the nonnegative CEV process and then Fatou, obtaining E Y_(A_T)≤E Y_(c_T). This does not require uniform integrability at the random terminal clock.

The six-dimensional Gaussian Laplace integral was reconstructed independently. With q=h/(1−2th), the full Jacobian-weight product reduces exactly to h and the exponent becomes −r²h. Integrating from zero to 1/(2t) yields

    E Y_t=v[1−(1+b)exp(−b)], b=8/(t sqrt(v)).

The lost mass is strictly positive for each positive time. Consequently the exact weighted SPDE mass has a strict deficit relative to the heat value, while the numerical mean retains the heat value at every step. The lower bound is independent of the mesh at fixed T. Both expectations are finite. The resulting expected L1-field and scalar Wasserstein-1 lower bounds are valid consequences, with the correct normalization by ||phi||_infinity where appropriate.

## 5. Turn 4: analytic cutoff estimates and probability convergence

The derivative formulas use h(v)=v f'(v)=g'(v)−f(v), not an assumed bounded f' at zero. Because g is C1 with g(0)=0, h tends to zero at the origin and the displayed derivatives extend continuously there. For each fixed Gaussian increment the scalar maps have bounded derivatives, so the Sobolev chain rule is applicable to the H_0^1 input.

The tilted-Gaussian derivative moments were independently derived from differentiation of the Gaussian moment generating function. Both brackets and their bounds by exp(9L²s), including negative f/h and mixed-sign g' cases, are correct. The H_0^1 boundary condition is preserved because the scalar maps vanish at zero. Heat contraction and conditional Tonelli then give the stated pointwise-in-time Sobolev estimates.

The maximal linear stochastic heat estimate on H_0^1 follows from a spectral approximation, dissipativity, BDG and Young's inequality; its constants need no derivatives of g beyond the bounded first derivative. The author correctly avoids claiming that the nonlinear map is globally Lipschitz on H_0^1. The H-based Picard construction has uniformly bounded V energies, weak Sobolev limits identify the H solution, and the chain rule puts g(u) in the V stochastic-integrability class. The resulting linear convolution has a continuous V version. This justifies the regularity and maximal estimates used subsequently.

The four-term coefficient-defect decomposition is an exact identity. The two heat differences cost sL²||v'||², while each frozen-noise difference costs sL4 exp(sL²)||v||². With the earlier Sobolev bound, their expectation is of order tau times a polynomial in L times exp(C L²). H-energy, BDG and Gronwall propagate this to the maximal H error of order tau. The one-dimensional interpolation inequality converts it to a maximal squared sup-norm error of order tau^(1/2). The distinction between root-mean-square H order 1/2 and sup-norm order 1/4 is maintained.

For tangent cutoffs, L_K=(5/4)K^(1/4). The nonnegative-supermartingale maximal bound for Y and Markov's inequality for the cutoff error control the bad event. Induction identifies the original and cutoff grid schemes because each coefficient is frozen at a grid input at most K. Intermediate substep overshoots do not invalidate this argument. First letting tau decrease for fixed K, then K increase, proves the stated probability convergence. It is compatible with failure of uniform integrability.

## 6. Turn 5: the logarithmic bounded-test rate

The dependence on the cutoff is explicit enough for optimization: L_K²=(25/16)sqrt(K) and L_K4=(625/256)K, hence B_K≤C0(1+K)exp(C1 sqrt(K)). The good event identifies entire interpolated paths as well as their grid values, because once the input values agree the frozen stochastic and heat substeps agree throughout that interval.

For each bounded 1-Lipschitz path functional, the bad-event contribution is at most twice its probability; on the good event the difference is controlled by the cutoff path error. This yields the three displayed terms without demanding an integrable norm of the uncut scheme.

Choosing K=kappa log(eM)^2 with C1 sqrt(kappa)≤1/8 gives powers M^(-3/16) for the cutoff root-mean-square term and M^(-3/8) for the additional exit term. Their polynomial logarithmic factors are smaller than the retained log(eM)^(-2) tail term. Finitely many small M are absorbed using d_BL≤2. The cutoff is an analytical device and does not alter the algorithm. No positive algebraic weak order or optimality follows, and none is claimed.

## 7. Accepted conclusions and limits

Accepted: positivity and pathwise finiteness; finite numerical first moments but infinite numerical moments above one after two steps; a global nonnegative local mild exact solution; infinite coupled mean-square error; a strictly positive finite linear weak-error lower bound; and the one-dimensional logarithmic bounded-Lipschitz path-law convergence rate.

Still outside this packet: a sharp/optimal algebraic weak rate, higher-dimensional sup-norm or path-space variants, arbitrary unbounded-test convergence, and the separate space-time-white-noise question. The rare-tail and bounded-test conclusions must continue to be presented together, so a reader does not infer either that all weak convergence fails or that the numerical moments become uniformly integrable.

No mandatory mathematical correction was identified. The source/current-literature access and read scopes remain those explicitly recorded; this review is not an exhaustive priority search. Standard source results, Bessel/DDS facts and Hilbert-space stochastic estimates retain their existing credit.
