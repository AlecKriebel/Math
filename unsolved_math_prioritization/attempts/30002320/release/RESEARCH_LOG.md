# Five substantive approaches and their outcomes

These are mathematical methods and verifiable outcomes, not a claim of five independent solutions. The complete all-density conjecture was not established. The fixed model throughout is uniform simple G(n,⌊dn/2⌋), except where an alternate ensemble is explicitly compared.

## 1. First moments and the placement of the root

Started from the designated problem page; access returned HTTP 403. The pinned problem record was compared with the official original OWR report. The rendered p.1098 shows the root inside the expectation, whereas the catalog's displayed formula places it outside. The source's Conjecture 4 refers back to that inside-root formula.

Derived exact finite-n first-moment sums by color-class sizes, bounded them from above by the balanced type's allowed-edge probability, and from below by its multinomial multiplicity. This proves the outside-root rate k(1−1/k)^(d/2) without independence approximations. Jensen gives only an upper bound for the source quantity. Markov gives the strict high-density zero region d>−2 log k/log(1−1/k).

Decisive control: for k=3,d=6, the annealed rate is 8/9 but the expected-root limit is zero. Hence the source cannot be “solved” by relocating the root. The same computation in G(n,d/n) yields k exp(−d/(2k)), further exposing the model dependence of exponential moments.

## 2. Component factorization below the giant-component threshold

Used a cycle-plus-path witness count to bound the expected number of vertices in cyclic components for d<1. A finite-size union bound then excludes complex components with probability tending to one. Trees and unicyclic components are k-colorable for k≥3; their coloring counts multiply. The cyclic contribution is O_P(1) in the logarithm, while the forest contributes n log k+m log(1−1/k). Boundedness of the nth root gives expectation convergence.

This supplies a self-contained proof of an established low-density case. The witness series ceases to be summable at d≥1, and a linear-size cyclic core can no longer be discarded. No extension beyond that obstruction is claimed. The 2018 condensation theorem independently gives a much larger known range for all k≥3.

## 3. Finite-temperature interpolation and zero-energy counts

Matched the cited Bayati–Gamarnik–Tetali theorem to its precise coloring objective and finite weight parameter. Their zero-temperature objective is the maximal number of satisfied edges, not the number of exact proper colorings. A finite-temperature pressure limit by itself does not justify exchanging n→∞ and β→∞.

Constructed a bounded-degree deterministic sequence alternating an empty graph with a fixed K_{k+1} plus isolates. Its normalized pressure tends to log k at every finite β, while its hard-coloring root alternates between k and zero. Also checked the one-edge annihilation example K_{k+1}−e to K_{k+1}. These refute the proposed generic implications; neither is a random-ensemble counterexample to the conjecture.

Clamping log Z removes infinities but destroys the disjoint-union additivity needed by the most immediate interpolation proposal. A graph-specific or probabilistic replacement is still required.

## 4. Sharp thresholds as a route to uniqueness of the limit

Applied the Achlioptas–Friedgut theorem and elementary inequalities P(Z>0)≤E[Z^(1/n)]≤kP(Z>0). If the sharp-threshold sequence oscillates between two degree values, an intermediate fixed degree produces a subsequence with expected root tending to zero and another with liminf at least one. Thus the desired all-density convergence would force threshold convergence.

This is a necessary implication, already recognized in the literature. It does not prove threshold convergence. Even threshold convergence would leave the conditional entropy and the exact transition point untreated. A limiting exponential rate for colorability probability does not help when that rate is zero: probabilities can then tend to zero subexponentially, remain bounded away from zero, or approach one.

## 5. Conditioning, changing ensembles, and current exact results

Factored the target as colorability probability times the conditional expectation of exp((log Z)/n). Proved that convergence of both the colorability probability and conditional entropy to a deterministic constant is sufficient. The unconditioned E log Z is −∞ for every sufficiently large n because a prescribed finite (k+1)-clique has positive probability, even below d=1; convergence in probability is therefore kept distinct from convergence of that expectation.

Derived both monotone graph-process sandwiches between G(n,m) and G(n,d/n). They transfer known formulas at continuity points and open zero regions, but do not settle an unknown discontinuity or critical endpoint. Conditioning a with-replacement graph on simplicity cannot be treated as an automatic transfer of arbitrary expectation limits; loops can annihilate proper colorings.

Checked the 2018 all-k condensation theorem, its hard-constraint discussion, and later interpolation upper bounds. Below condensation the known deterministic formula transfers to the fixed-edge model. Above condensation an exponential deficit relative to the first moment is not a full limiting formula. No theorem checked closes the all-density gap.

## Stopping disposition

Five substantive routes completed. The appropriate result is partial, with an important statement correction and credited known regimes. No complete proof, counterexample in the specified ensemble, novelty claim, paper, DOI, or publication action is supplied. The public files are frozen for a fresh independent audit.
