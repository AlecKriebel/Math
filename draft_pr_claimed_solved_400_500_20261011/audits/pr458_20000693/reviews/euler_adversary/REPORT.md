# Independent adversarial Euler/arithmetic review

Reviewer `/root/pr458_euler_adversary`; PR458; problem20000693; frozen head `87a39f7b4e5ef81aacf98464f86586cc95684d7f`.

## Verdict and exact scope

The defined exponent and constants withstand this independent review. One literal statement in the frozen derivation needs correction before publication: §5 identifies a finite-cutoff hybrid local mean with the full Euler local mean. This is H1, a narrowly repairable clarification; raw blocking issues1 and required repairs1 are retained. There are zero discovered central mathematical gaps in the arithmetic constant or in the heuristic's declared application. The proposed correction changes no formula and adds no unsupported central application beyond the explicitly stated model hypotheses.

This review does not certify the general critical-line moment asymptotic, priority, novelty, a complete publication package, or any repository/publication action. The source asks for a heuristic. The author's fixed-modulus, unshifted, nonnegative-weight formulation is openly a model prediction. Its higher-moment asymptotic remains unproved in general.

The exact primary AIM Problem5.3 body was fetched independently by direct HTTP after the web fetch failed. It requests a heuristic for imprimitive L-functions or products of degree-one factors, with different powers. No numerical exponent range, negative-power requirement, growing-conductor theorem or full lower-order polynomial occurs in that request. `PRIMARY_RECEIPT.json` records the independently captured primary hashes and references. Foreign HTML/PDFs/images are private and excluded from the public file list.

## Independence and inputs

The analytic reconstruction in `INDEPENDENT_RECONSTRUCTION.md` preceded any historical peer report or new peer conclusion. I read the frozen author HEURISTIC, README, SOURCE_GATE and verify.py in full, plus the exact source receipt. I did not read the historical peer review or its conclusion, nor make a priority determination.

After deriving the local identities, convergence and H1 correction independently, I read the root's entire proposed clarification, model reconstruction and claim ledger. These root notes mention other families' ancillary findings; those are not my independently reproduced findings. `ROOT_LAYER_READBACK.json` binds the root layer actually considered and records its limited conceptual acceptance. This is not a clean rereview of repaired PR bytes: the frozen and actual PR sources remain untouched. A new whole-candidate adversary is still required for any later promotion.

`INPUT_BINDINGS.json` confirms all four read author files match the frozen source receipt. There were zero source edits, remote mutations, checkout/index actions, outside communications, or new original proof-search attempts.

## Multiplicities, conductors and exact deletion signs

The primitive inducer is unique. Characters sharing it have the same primitive L-factor and primitive zero component, so their weights add to M before taking one matrix expectation. The diagonal prime exponent is E=sum M^2. Splitting repeated primitive constituents into independent matrices would instead sum the squares of the original weights and is wrong. Conductor-one principal characters are included in this rule.

For an imprimitive character modulo q, its primitive Euler factors at p|q are deleted by multiplying by `(1-psi(p)p^-s)`. To lift to Q=lcm(q_i), additional primes are deleted; restoring the original character requires the inverse factors at p|Q,p not dividing q_i. The frozen identities (3) and (4) have the correct signs. The restoration is generally not a finite Dirichlet polynomial. Each critical-line denominator has modulus bounded away from zero because |psi(p)|/sqrt(p)<1.

Different modulus deletions are retained in J_p using the actual chi_i(p), including zero. All factors at one prime share its phase p^-it. Their expectations cannot be multiplied as separate independent phases. For two identical unit values, weight one each and x=1/p, the joint local mean is `(1+x)/(1-x)^3`; separate means would give `(1-x)^-2`. They differ at every prime. The correction ratio `product_{p|Q}J_p/J_p^*` is an exact identity between the defined arithmetic constants; transporting it to actual critical-line moments remains heuristic.

A nonreal character and its conjugate remain distinct unless they are equal as characters. A quartic primitive character modulo five and its conjugate have E=2 for weights one, and their quotient is the nonprincipal quadratic square. Conjugation relates opposite-t values through the functional equation, not equality of the two positive-t factors. Distinct primitive characters cannot have a principal quotient on a common modulus: that would give the same induced character and contradict uniqueness of the primitive inducer. The model's independence between genuinely distinct primitive constituents is still a hypothesis.

## Analytic branch, Parseval and uniform tails

Each local factor has an analytic logarithm on the unit disk, normalized at zero; its real power has an unambiguous analytic branch there. For A=sum a_i>0, nonnegative binomial convolution bounds the coefficient absolute values by `(A)_r/r!`. This grows polynomially. Consequently the coefficient-square sum at x=1/p<=1/2 converges, and Parseval gives exactly the single-phase integral in (1). Its constant coefficient is one, hence J_p>=1.

The first coefficient is b_p(1)=sum a_i chi_i(p). The tail from r>=2 has the uniform bound

    sum_{r>=2}|b_p(r)|^2 p^-r
        <= p^-2 sum_{r>=2}((A)_r/r!)^2 2^{-(r-2)}.

The sum on the right is finite and depends only on the fixed weights. This proves (6); it is not numerical evidence promoted to a universal estimate. Zero local character values and fractional weights create no singularity inside the unit disk. Every local mean, exceptional-prime factor and absolute-value regularizing factor is strictly positive.

## Regularization, ordered convergence and positivity

At good primes, grouping the primitive values expands the first coefficient square into E plus `2 sum M_psi M_phi Re(psi*conj(phi))`. Multiplication by the positive power `|1-rho(p)/p|^(2 M_psi M_phi)` cancels the cross coefficient. The opposite sign would double it. Thus H_p=1+O_a(p^-2) and the product of H_p converges absolutely to a strictly positive finite value. Taking the wrong reciprocal of the cross L-value would likewise contradict the local identity.

For each nonprincipal quotient rho, the fixed-modulus prime number theorem in progressions gives a summable partial-summation bound for sum rho(p)/p. The higher-degree logarithmic Euler terms converge absolutely. The same bounds are uniform as the real Euler parameter decreases from >1 to1, so the increasing-prime boundary product equals L(1,rho). Nonprincipal L(1,rho) is finite and nonzero; [DLMF25.15.9](https://dlmf.nist.gov/25.15.E9) independently corroborates nonvanishing. The full argument, including boundary-value identification rather than a mere unnamed product, is recorded in `INDEPENDENT_RECONSTRUCTION.md`.

Deleting finitely many primes gives nonzero partial L-values. Combining them with the absolutely convergent positive H product and finitely many positive exceptional factors proves (8) and the existence of A in increasing prime order. Conditional ordering is not silently replaced by unconditional or arbitrary-order convergence. This theorem about the defined constant proves no prime/zero or constituent statistical independence.

## Benchmarks and edge cases

The weight-one mean square gives E=1, Barnes factor1 and A=phi(q)/q. The weight-two fourth moment gives E=4, Barnes factor1/12 and arithmetic factor `zeta(2)^-1 product_{p|q}(1-1/p)^3/(1+1/p)`, hence leading coefficient `(2pi^2)^-1` times the finite correction. Visual inspection of Topacogullari v1 printed p.2 confirms its fourth-moment coefficient is algebraically identical.

For two unit local values u,v with rho=u*conj(v), direct algebra gives

    J_p=(1-x^2)/[(1-x)^2|1-rho*x|^2], x=1/p.

Distinct primitive factors therefore have E=2, H_p=1-x^2 at good primes and a positive power |L(1,rho)|^2. At a prime dividing one modulus, its correction relative to the removed zeta(2) factor is 1/(1+x); when it divides both moduli the correction is `(1-x)/(1+x)`. These coincide with the totient and p/(p+1) factors in Topacogullari's Theorem1.3, printed p.3. Its cross character is conjugated in the opposite order, which changes no absolute L-value. The full relevant printed pages were inspected, not just an abstract or OCR omission of the conjugation.

For zeta times the principal character modulo two, the common primitive total is2 and E=4. The sole changed local ratio is1/6, giving predicted coefficient1/(12pi^2). Individual prime coincidences do not merge distinct global primitive classes. The explicit examples include overlapping differing moduli and multiple deleted primes, not merely equal moduli.

Zero weights are omitted, including at zeros, and commute with grouping and all local definitions. All-zero input has integrand1, A=G=1 and the exact integralT. Adding an otherwise irrelevant zero-weight modulus may enlarge an auxiliary exceptional set but cannot change the defined constant. Negative powers, shifting/unbalanced moments and weights or conductors growing with T are not asserted. Their absence creates no contradiction with the literal, unquantified source request.

For fractional nonnegative weights the local analysis remains rigorous. Keating–Snaith's [primary paper](https://people.maths.bris.ac.uk/~mancs/papers/RMTzeta.pdf), printed pp.59–60, states the finite CUE gamma identity in equation6 and Barnes limit in equation15. Set its parameter s=2m. The range Re(s)>-1 includes every m>=0. Our own finite integer telescoping and fractional N=1 integrals check the normalization. Independently fixed real weights in critical-line moments still require the model assumptions; integer moments do not prove them by analytic continuation.

## H1: the one required clarification

The frozen §5 says the hybrid prime component has local phase mean (1), the full J_p. The actual [Sahay v3](https://arxiv.org/pdf/2103.13542v3) definition on printed pp.5–6 uses a sharp exponential sum over n<=X, with finite primitive deletions. Its exact finite-cutoff local mean is J_(p,X), which is not J_p. The smoothing u_X in that theorem belongs to the zero kernel, not a v_X weight in the displayed prime sum.

Concrete check: at X=p=2, a single zeta factor has local function exp(z), mean `sum (1/2)^r/(r!)^2 <=13/8 <2=J_2`. This is an elementary boundary definition. X=3,p=2 gives the same factor and lies within the cited theorem's X>2 range. Thus the concern does not rely on claiming the theorem holds at its excluded endpoint.

The exact replacement is in `TRUNCATED_PHASE_REPAIR.md`: distinguish the actual truncated analytic function and J_(p,X) from full B_p and J_p; fixed-cutoff equidistribution averages the former. At each fixed prime J_(p,X)->J_p. Their first coefficients agree, and a uniform polynomial coefficient majorant gives a p^-2 difference. Dominated convergence of logarithmic prime ratios proves `product_{p<=X}J_(p,X)/J_p ->1`. Mertens' theorem then supplies the same ideal-phase arithmetic normalization. This is a rigorous repair of the Euler-phase interpretation, not a joint X(T)/time-average theorem.

I independently reconstructed that bridge before reading the root's entire proposal. The root proposal is conceptually sound and changes neither the exponent, constant, finite deletion correction nor remaining model hypotheses. Raw H1 remains1 because no frozen/actual source has been repaired; conceptual verification of a proposed interpretation is not retroactive clean acceptance or a fresh whole-candidate package review.

## Computational evidence and its limits

The standard-library `check_euler.py` uses ordinary runtime guards rather than assert. The final normal and optimized runs each passed18078 guards. The outputs match after dropping only the optimization-mode field. These are 18078 finite guards, not that many independent proofs.

- 160 row/prime cases checked exact Gaussian-rational coefficients through degree10, inverse lifts, primitive aggregation and coefficient majorants.
- 640 row/prime/truncation cases at K=1,2,4,10 checked the actual sharp hybrid coefficients and their uniform majorant; coefficients through K agree with the full local function.
- All15 distinct pairs from six explicit primitive characters were tested as nonprincipal quotient characters on their actual common moduli; quotient multiplicativity was checked on every pair of unit residues.
- 40 numerical local Parseval checks included zero, fractional and overlapping-modulus cases; the largest relative difference was3.572894273193572e-16. Series degree240 and a16384-point phase mesh were used. These are floating-point corroboration, not interval certificates.
- Eight fractional matrix cases compared the N=1 phase integral to its gamma expression and normalized products at N=10,100,1000,10000. The largest N=1 relative difference was5.963310067969019e-9. N=10000 was explicitly not treated as the limiting Barnes value.
- Five finite p^-2 regularization diagnostics corroborated the analytic cancellation.
- Twelve deliberately wrong mathematical predicates were rejected in actual child processes in each Python mode, at the intended explicit guard, with no success output. The controls include wrong lift/deletion signs, separate local phases, primitive/conjugate collisions, regularization and cross-L signs, omitted bad primes, mishandled zero weights, zero exceptional factors, principal quotient confusion and finite-cutoff/full-Euler equality.

These computations do not evaluate actual high critical-line moments. Universal convergence, positivity and the sharp-phase limit are justified by the written derivations, not finite grids.

A static observation in the frozen author verify.py is retained: it contains13 assert nodes, which Python optimization elides. I did not run that dependency-based author script or claim its invalid-source behavior was independently reproduced. My guarded verifier is new evidence, not a source repair. The reproduction family must separately decide and document publication effects of that observation.

## Remaining gap and disposition boundary

The strongest independently verified result is a coherent arithmetic constant, with positive finite ordered product, correct multiplicities and deleted factors, correct benchmark normalizations, and a source-responsive model heuristic. H1 requires a literal derivation clarification before publishing the frozen wording. Its proposed correction leaves no additional central model gap.

Growing-cutoff/time averaging, zero replacement by CUE, distinct-constituent independence, and weighted prime/zero splitting remain declared hypotheses. General L-function high moments remain unproved. No priority audit result, status correction, merge, close, comment, preprint, DOI upload, tracker append or publication action is authorized by this family report.
