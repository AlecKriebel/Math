# Independent adversarial audit: SIS stationary virulence thresholds

Problem 30003676 / OWR-15962-002. Audit date: 2026-10-05.

## Verdict

**Frozen package alone: REVISE_REQUIRED.** Three presentation corrections are mandatory: fixed complete-graph weights, an explicit conclusion quantifier order, and unambiguous fast-vanishing immigration wording. They are supplied in AUTHORITATIVE_CORRECTIONS.md without changing the freeze.

**Frozen package read together with that authoritative overlay: PASS for the stated partial-results scope.** No invalid retained proof was found. This is a mathematical reading and reproducible finite audit, not formal proof-assistant certification. The general mathematical outcome remains **NO RESOLUTION**. A PASS does not certify novelty, exhaustive literature review, a universal immigration scale, or a solution/counterexample to Aldous's conjecture. Publishing the frozen report alone, or ignoring the overlay, does not inherit this PASS.

## 1. Object and source identity

The archive is 22,001 bytes, SHA-256 70191b3887e8863701651cdb54382958e1f8190fd889889a2ed81c46f16ee6a6. Its manifest SHA-256 is bb24c27fef83fcc14106cbcc068a02f740c0b35385b79e6c7799371764ea9bdb. All ten archive members match the supplied safe directory byte for byte: nine payload files plus the manifest. The freeze was not edited.

The official EMS report, both author slide decks, and both author problem/status pages were independently retrieved anew. All five byte counts and hashes match the supplied source metadata. The official report's printed p. 3435, the 2017 slide defining the probability notion, and the 2018 conjecture slide were rendered locally and visually inspected. The web screenshot route failed for the first two PDFs; fresh official downloads and local rendering succeeded. No denied catalog access was retried or bypassed. Source PDFs, renders, extracted text, and raw responses are outside this deliverable.

The task's rank/ID association is supplied identification, not an independently audited raw-dataset claim. The primary mathematical source is directly verified. No raw dataset or its contents was needed for this mathematical audit.

## 2. Recovered target and probability conventions

The [official 2017 report](https://ems.press/content/serial-article-files/46721), p. 3435, uses a finite connected weighted network, vertex-specific recovery mu_v, transmission multiplier theta, and immigration epsilon at each susceptible vertex. Its premise has fixed positive endpoints theta_*<theta^* and both endpoint assertions for every sufficiently slowly decreasing immigration sequence. Its conclusion puts the existence of theta_n before the universal slow-immigration and fixed-delta assertions. C2 restores that ordering explicitly in the summary. The source allows possible additional weak assumptions and does not specify a universal slow scale. No kappa is present.

The [2017 slides](https://www.stat.berkeley.edu/~aldous/Talks/SIS_talk_short.pdf), PDF page 13, define the upper regime by lim_(a down to 0) limsup_n P(Y_n<=a)=0. For Y_n=X_n/n in [0,1], this implies a positive limiting lower bound on the mean. Its converse fails, as Bernoulli(1/2) shows. A fixed Uniform(0,1) distribution satisfies this bounded-away definition but does not satisfy P(Y_n>=a)->1 for any one fixed a>0. Thus the report's distinction between these notions is correct. The [2018 slides](https://www.stat.berkeley.edu/~aldous/Talks/columbia2018.pdf), PDF pages 7 and 25, explicitly identify the networks as undirected.

The proof hypotheses mu_v>0, symmetric finite nonnegative weights, and no self-loops are stated rather than falsely recovered as universal uniform bounds from the source. They suffice for all retained results. Fixed-n stationary distributions, epsilon=0 stationary distributions, quasistationary distributions, ODE equilibria, and joint n/epsilon limits are correctly kept distinct.

## 3. Proof-by-proof adversarial review

### Section 0: finite chains — PASS

External births and positive recoveries give communication among every pair of subsets. A uniformization rate strictly above every exit rate introduces self-loops, and finite irreducible aperiodic chains are primitive. This justifies convergence and the stationary limiting couplings used later. The normalized stationary linear system is nonsingular; rational/analytic dependence holds on the irreducible region. At epsilon=0 every nonempty state can reach the empty state through recoveries, leaving only the empty closed class. Compactness plus stationary-equation continuity correctly gives the fixed-n epsilon-down-to-zero limit. No stationary nonzero finite-n phase transition is asserted.

### Section 1: attractiveness, drift, resolvent — PASS

The Poisson construction preserves subset inclusion at births, deaths, and infection arrows. Adding transmission or immigration, or thinning recovery, preserves the ordering. There is no independence closure in this proof.

For H(A)=sum_(v in A) a_v, the positive-vector inequality controls the infection contribution indexed by its infected source. Symmetry makes the displayed index orientation correct. Dropping susceptible restrictions is an upper bound. Stationarity gives E[H]<=epsilon*sum(a)/c; H>=a_min X yields the normalized count bound. Along sequences its entire right side must tend to zero. Merely having a positive c for each n is not enough, and the report does not claim otherwise.

The first-moment inequality yields p<=epsilon D^-1 1+Bp. Under rho(B)<1, B^m p tends to zero on a fixed finite graph and the Neumann series is nonnegative. The matrix identity with (D-theta W)^-1 is correct despite noncommutativity. This is only an upper certificate; losing it proves no supercritical lower bound.

### Section 2.1: exact complete graph — PASS; summary correction C1 required

The proof itself fixes weights a/N and puts beta=theta*a. The birth rate has both the susceptible factor (N-k) and the correct k/N contact term. The stationary product telescopes exactly to equation (2.3), including k=1. Zero beta is correctly handled separately.

The delicate uniformity at both k=0 and k=N is valid. For beta>0 and eventual epsilon_N<1, let q_N=epsilon_N/beta and R=beta/mu. A direct envelope for the asserted uniform error is

E_N = [|log epsilon_N| + 2 log N + |log mu| + |log R| + 1]/N
      + log(1+q_N) + q_N log(1+1/q_N).

For k>=1 the prefactor has the stated logarithmic bound. The missing one log R contributes |log R|/N. For g(t)=-log(1-t), the partial left Riemann sum is below the integral; monotonicity telescopes its error, and the final interval has integral (log N+1)/N. Therefore the same bound holds through k=N. For the immigration factor, the decreasing function log(1+q/t) bounds the sum by its integral from 0 to 1; this integral tends to zero. At k=0 the error is exactly zero. Consequently E_N tends to zero under the two stated hypotheses. No interchange of uncontrolled limits occurs.

The limiting potential is continuous on the closed interval. Its strict concavity and derivative identify a unique maximizer at zero for R<=1 and at 1-1/R for R>1. At criticality, although the derivative at zero vanishes, the maximizer is still unique. A fixed excluded neighborhood has a strictly positive potential gap. One grid point near the maximizer bounds the denominator; at most N+1 excluded terms bound the numerator. This proves concentration without an unproved Laplace theorem. Uniformity in moving theta_N is not established or claimed; every theta used in the restricted threshold assertions is fixed.

### Section 2.2: fast-vanishing immigration — PASS; wording correction C3 required

The bound b_k/d_(k+1)<=N(1+beta)/mu is valid for epsilon<=1. The first nonempty weight contributes N epsilon/mu. With epsilon=exp(-N^2), the log of the full upper bound is -N^2+O(N log N), giving stationary emptiness. The example invalidates the proposed strengthening to every decreasing immigration sequence. It does not meet the retained slow condition and therefore does not refute the source conjecture. Its rate is super-exponentially small in N, not fast seeding.

### Section 3.1: exact dimer — PASS

Count weights (1,2h,h(h+theta)) give the stated marginal h(1+h+theta)/[(1+h)^2+h theta]. At every fixed theta it vanishes with h. In particular a bounded component can exceed its linearized inverse spectral threshold while contributing no limiting prevalence under vanishing immigration.

### Section 3.2: connected obstruction — PASS

For n=4m, the clique has N=n/2 and weights (1/2)/N; a varies neither with theta nor with immigration. The dimer blocks have unit internal weight. A path of edges of weight n^-2 makes the graph connected and admits a per-vertex weak-degree bound of two.

Deleting weak arrows is a lower coupling. Turning each incoming weak arrow into an unconditional infection mark is an upper coupling: target processes have independent Poisson marks because oriented arrows are independent. Topping up rates gives h_n=epsilon_n+2 theta n^-2. Both h_n and epsilon_n vanish and both obey the subexponential logarithmic condition on the clique scale N. No relation epsilon_n>>n^-2 is required. The dimer upper expectation vanishes after normalization, so Markov's inequality removes the dimer contribution. The clique lower/upper limits agree, which suffices for convergence in probability of the full count without a global correlation estimate.

The disconnected matrix has spectral radius one. For the symmetric perturbation, row sums at most 2n^-2 bound its Euclidean operator norm. A dimer-supported vector supplies Rayleigh quotient one. Hence 1<=rho(W_n)<=1+2n^-2. The limiting inverse spectral value is one, but the actual normalized prevalence is zero at theta<=2 and equals (1/2)(1-2/theta) at theta>2. In particular the endpoints 1/2 and 4 give zero and 1/4, so the endpoint premise is genuinely satisfied on a stated slow class. The sequence itself has a sharp separating threshold at two: it is not a conjecture counterexample.

The extension to every integer n is valid: attach up to three vertices by a weak path, keep maximum weak incidence two, and use n'=4 floor(n/4) for the core. The clique fraction tends to 1/2, n'/n tends to one, and all errors remain negligible. The independent script checks this construction for every n from 4 to 36, including all remainders modulo four.

### Section 4: graphical duality — PASS

Backward arrows add sources and recovery marks remove ancestors. Symmetry is exactly what makes the reversed arrow rates match the original network; heterogeneous recoveries do not require transposition. Finite positive recoveries and a no-arrow interval give uniformly positive extinction probability per time block, proving finite expected integrated ancestral size on each fixed graph. No graph-uniform extinction estimate is inferred.

Conditional on arrows and recoveries, the external marks intersect the ancestral space-time set as a Poisson process with intensity epsilon times its volume. Starting empty in the past and then taking the time horizon to infinity establishes the stationary susceptibility formula by bounded convergence. This passage is at fixed n, theta, epsilon. It does not exchange n and epsilon limits.

The killed equation has killing rate epsilon|A|, not epsilon. Its empty boundary and positive killing yield uniqueness by a maximum principle. Inclusion-exclusion gives the covariance identity with the displayed sign. Single-vertex transforms determine the mean but leave the joint transforms needed for variance/lower-tail control; the report correctly stops there. An independent directed-network negative control confirms that omitting transposition breaks self-duality when symmetry is removed.

### Section 5: abstract Bernoulli obstruction — PASS within its declared non-SIS scope

For Bernoulli variables the source's upper-regime definition is equivalent to success probability tending to one. A convergent subsequence of proposed thresholds and continuity of g force g(t-delta)=0 and g(t+delta)=1 for all small fixed delta; sending delta down to zero is contradictory. The endpoints and monotonicity are valid. The construction is independent of n and epsilon and is expressly not an SIS realization. Thus it blocks a purely order-theoretic inference without overclaiming a stochastic-network counterexample.

## 4. Independent computation and negative controls

The author's standard-library verifier was rerun unmodified. Its output is byte-identical to the frozen result: 436 checks. Its five wrong-formula rejection controls and two additional logical/setup checks are correctly distinguished. Both of its integrity negative controls reject their mutations.

The new independent_checks.py does not import author code. It builds subset transitions using sets and obtains stationary probabilities from Markov-chain-tree principal cofactors using integer fraction-free Bareiss determinants. This differs from the author's normalized linear-system solver. Exact full stationary residuals validate the independent weights. Cramer's rule supplies a separate resolvent calculation.

Its **1,407 exact assertions pass**, including all upper-set monotonicity tests on the small heterogeneous graphs, a nonconstant positive-vector drift, the zero-immigration stationary empty law, all susceptible-subset dual equations, covariance identities, complete-graph product/lumping tests, 33 connected structural witnesses, and every one of the 168 increasing events in the connected four-vertex sandwich.

Eight explicit wrong-model/formula controls are rejected: omitted immigration, globally shared instead of per-susceptible immigration, theta-scaled recovery, incorrect edge normalization, a mean-field independent stationary law, omitted susceptible multiplicity, omitted dual cardinality, and untransposed directed duality. These are witnesses, not exhaustive mutation coverage.

Sixty floating log-weight diagnostics use N=25,100,400,1600,6400, four R values including criticality, and three admissible immigration schedules. All stay within the analytic uniform-error envelope. Three further fast-decay diagnostics agree with the analytic mass bound. Their values are labeled as diagnostics, never counted as exact checks, and cannot prove the asymptotic conclusions. The proofs in section 3 of this audit carry that burden.

## 5. Literature and historical checks

The [author's problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/epidemic.html) links to the 2018 conjecture. His [index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html) still lists it and expressly warns that updating is incomplete. This supports a bounded public-listing statement, not a global open-status certificate.

The [2026 Cantwell–Moore publisher page](https://journals.aps.org/pre/abstract/10.1103/385j-2f29) independently confirms the authors, date, DOI, and focus on an approximation and quasistationary prevalence. Its advertised conclusions do not provide the quantified arbitrary-network stationary-with-immigration result. Full text was not audited.

Additional relevant publisher abstracts checked in this audit include [Van Mieghem–Cator 2012](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.86.016116), [Van Mieghem 2020](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.101.032303), [Achterberg–Prasse–Van Mieghem 2022](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.105.054305), and [He–Luczak–Ross 2025](https://doi.org/10.1017/apr.2025.16). They establish important prior epsilon-SIS, complete-graph, approximation, and mixing-time context. The 2020 abstract distinguishes its complete-graph analysis from a claim about other graphs. None of the inspected abstracts establishes the full conjecture. No full-text non-resolution assertion is inferred. These are useful additions for future exposition; the package already makes no novelty claim. The abstracts' access limitations were respected.

At repository commit 73300d9223ca6175983c78cb2370f99ffdd4b59c, the attempts directory was independently read: 62 entries and no exact ID or SIS/virulence/Aldous name match. The exact problem subdirectory returned 404. Read-only code, PR, and commit searches for 30003676 each returned no matches. Search indexes and inspected locations are bounded evidence. No current branch, PR, or repository was changed. Historical private-context search claims were not independently re-audited and are not required for the mathematical verdict.

## 6. Release boundary and stopping condition

The original freeze, this audit, and the authoritative correction overlay together form the reviewed object. A publication or summary must retain NO RESOLUTION and the distinction between theorem, restricted-family result, and shortcut obstruction. No source bytes, source extracts, raw datasets, private-source material, or private coordination are part of this audit payload. No remote writes were performed.

The unresolved task is a graph-uniform mechanism giving the source's full lower-tail conclusion with its quantified sufficiently-slow immigration requirement. This audit neither proves that mechanism nor starts an unreported sixth approach. No further correction to the retained mathematical proofs is required by the evidence found here.
