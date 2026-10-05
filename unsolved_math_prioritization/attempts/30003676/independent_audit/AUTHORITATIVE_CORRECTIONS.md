# Authoritative audit correction overlay: SIS 30003676

This overlay takes precedence over the specified passages in the frozen REPORT.md. The frozen files and archive must remain unchanged. These corrections concern presentation and quantifier recovery; they do not change the retained proofs or turn the investigation into a solution.

## C1. Fixed complete-graph network

Replace the complete-graph summary in REPORT.md, section 3, item 2, by:

For each N, fix w_uv=a/N for u distinct from v, with a>0 and recovery rate mu>0 independent of theta. Write beta=theta*a. If epsilon_N tends to zero and log(1/epsilon_N)=o(N), the exact stationary process satisfies K_N/N -> (1-mu/beta)_+ in probability, with value zero at beta=0. The critical parameter is theta=mu/a and the critical normalized prevalence tends to zero. The proof includes the critical case and the exact finite-N distribution.

The notation w_uv=beta/(theta*N) must not be read with beta fixed while theta varies: that would vary the network, cancel the transmission multiplier, and be undefined at theta=0. PROOFS.md, section 2, already uses the correct fixed-network setup.

## C2. Preserve the source's quantifier order

The conclusion in REPORT.md, section 1, is to be read as follows:

Under the fixed-endpoint premise, possibly with further weak assumptions as contemplated by the source, there exists a deterministic sequence theta_n in [theta_*,theta^*] such that, for every sequence epsilon_n decreasing to zero sufficiently slowly, and every fixed delta>0, the normalized stationary infected count tends to zero at theta_n-delta and is bounded away from zero in probability at theta_n+delta. The lower-parameter assertion is used only where theta_n-delta is positive, for example for 0<delta<theta_*.

The threshold sequence is chosen before the universal immigration-sequence and fixed-gap assertions. It is not chosen anew for each immigration sequence or each gap. Networks, weights, and recovery rates may depend on n but remain fixed when theta varies. No kappa parameter occurs in the recovered SIS statement. The source does not define a universal numerical slow scale, or explicitly resolve every possible dependency of such a scale; this audit does not supply a missing universal scale. The condition log(1/epsilon_n)=o(n) is proved only for the restricted constructions in this package.

Primary source: David Aldous, “Epidemics on general networks: a conjecture,” in Network Models: Structure and Function, Oberwolfach Report 57/2017, printed p. 3435. [Official report](https://ems.press/content/serial-article-files/46721). The [April 2018 slides](https://www.stat.berkeley.edu/~aldous/Talks/columbia2018.pdf), slide 24, agree.

## C3. Unambiguous immigration wording

Replace REPORT.md's “exponentially-fast-seeding negative control” by “fast-vanishing immigration negative control, epsilon_N=exp(-N^2).” The example's immigration decays super-exponentially in N. It describes extremely rare external seeding, not a high seeding rate. PROOFS.md, section 2.2, states and proves the correct example already.

## Scope retained after correction

NO RESOLUTION of the general conjecture. No novelty claim. The spectral construction refutes inverse-adjacency-spectral-radius equivalence, and the Bernoulli construction refutes an abstract monotonicity argument. Neither is a counterexample to the original SIS conjecture.
