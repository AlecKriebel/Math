# Quantifier controls for the priority audit

This is root-authored logic for testing proposed implications, not a counterexample to the iid RWRE theorem. It was prepared while three independent priority families were still investigating primary sources. No novelty disposition is assigned here.

## Even almost-sure convergence does not supply the requested tail rate

Let alpha_N be the endpoint law of a simple symmetric N-step walk, h_N=alpha_N([0,infinity)), and nu_N=alpha_N conditioned on [0,infinity). Let B_N be Bernoulli with probability r_N=N^-2, for N>=2. Define a random probability measure

    mu_N=nu_N                                      if B_N=1,
    mu_N=(alpha_N-r_N nu_N)/(1-r_N)                 if B_N=0.

These are probability measures: h_N>=1/2>r_N guarantees nonnegativity of the second case. The true averaged law E mu_N is exactly alpha_N. By the first Borel–Cantelli lemma, B_N=1 only finitely often almost surely, irrespective of dependence among the B_N. On every later good event the full-lattice L1 distance to alpha_N is at most 2r_N/(1-r_N). Thus mu_N has even almost-sure full-lattice L1 convergence to its reference law, much stronger than a weak invariance principle, while retaining the exact homogeneous annealed law.

Take equal cells of length floor(N^(1/4)), aligned deterministically with a boundary at zero. Every cell is wholly nonnegative or wholly negative. On B_N=1 the coarse L1 difference between mu_N and alpha_N equals

    2(1-h_N).

Here h_N tends to 1/2, so this distance tends to 1. On B_N=0 the coarse L1 distance is r_N/(1-r_N) times that value. For fixed epsilon=1/2 the failure probability is therefore exactly N^-2 eventually, which is not O(N^-3). The construction does not arise from a claimed space-time iid walk; it establishes that almost-sure quenched convergence, or any unquantified local-limit approximation, cannot by itself logically imply the requested superpolynomial environmental estimate, even with an exact homogeneous annealed law. An actual quantitative theorem might supply further hypotheses excluding this example; those must be checked rather than assumed.

## Spatial block convergence does not automatically give a time-horizon rate

A stationary mean-one corrector whose block average converges as M tends to infinity can yield an expected coarse error tending to zero. A bound depending only on M_N, even a high moment O(M_N^-k) for each fixed k, does not alone give O(N^-K) for arbitrarily slowly divergent M_N. For example M_N=floor(log log N) makes any fixed power of M_N decay more slowly than every negative power of N. The candidate avoids this implication by establishing a separate fresh-environment concentration argument at a fixed polynomial auxiliary scale. To classify an older weighted local limit theorem as full prior coverage, one must identify the corresponding quantitative amplification or a stronger directly applicable bound.

## Spatial dimension lifting has hypotheses

Adjoining independent extra spatial coordinates to a one-dimensional directed walk cannot silently import a static uniformly elliptic iid theorem. The deterministic directed-time coordinate violates ordinary all-direction ellipticity; projecting extra coordinates can introduce reuse or correlation not present in the original process. A valid reduction must specify a common product environment, admissible transitions in the older theorem's model, and an exact projection identity for the quenched laws and coarse event. Absent that construction, a claimed implication transfers the difficulty and is not accepted.

## Interpretation limits

Law-special earlier results may be relevant to a negative conjecture even if they do not establish the strongest general theorem in the candidate. The priority audit must separately ask what exact conjecture they answered and what generality remains. Neither these logical controls nor a bounded negative literature search proves novelty.
