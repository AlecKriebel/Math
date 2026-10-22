# Survival and spatial percolation in the nearest-neighbor contact process

## Disposition and scope

Problem 30004594 / OWR-4990373-008 remains **unresolved by this investigation**. The target is the strict inequality between survival and spatial-percolation thresholds on each nearest-neighbor lattice Z^d, d >= 2. Five approach families were investigated. This note proves elementary comparison results, exact identities, counterexamples to proposed inference steps, and an obstruction to one particular finite-radius criterion. It contains no proof or disproof of the target, no novelty claim, and no claim of independent or human peer review.

We use total attempted-infection rate lambda: each infected vertex recovers at rate 1 and sends an arrow to each of its 2d nearest neighbors at rate a = lambda/(2d). In a per-edge convention with parameter b, lambda = 2d b, and both thresholds scale by the same factor. The strict inequality is invariant under this change of units.

Let xi_t^A be the contact process started with infected set A. Write

rho(lambda) = P_lambda(xi_t^{\{0\}} is nonempty for every t >= 0),

lambda_c = sup {lambda : rho(lambda) = 0}.

The upper invariant measure mu_lambda is the limit of the law started with every vertex infected. Standard graphical duality gives mu_lambda(eta(0)=1) = rho(lambda). In its two-sided graphical construction, eta(x)=1 exactly when the backwards infection cluster from (x,0) survives for all backwards times. Let Perc denote existence of an infinite nearest-neighbor component of occupied vertices in the single time-0 configuration, and define

lambda_p = sup {lambda : mu_lambda(Perc)=0}.

This is spatial connectivity, not existence of an infection path in space-time. Percolation at a distinguished root and existence somewhere have equivalent zero-probability statements, by translation invariance and a countable union. The definition does not assert what happens at lambda_p. The standard contact-process critical-extinction theorem does give mu_{lambda_c}=delta_0. These classical facts are inputs, not new results here. They imply lambda_c <= lambda_p. The classical large-rate lower domination theorem gives lambda_p < infinity when d >= 2. Strictness is the remaining issue.

### Source normalization

The source is Valesin's contribution with Rath, printed pp. 174-175 of OWR 4/2021. Its actual question is the classical nearest-neighbor model; the surrounding theorem uses an infection ball in the infinity norm while retaining nearest-neighbor spatial connectivity. In particular its R=1 model still has diagonals when d >= 2, so it is not the classical model. The full Rath-Valesin paper uses the closed infinity-norm ball, including the origin and thus ineffective self-arrows, in its spread-out normalization. This detail is immaterial asymptotically but matters in finite-R comparisons. The exact classical normalization above is their equation (1).

The journal version of Liggett-Steif places the original question in Section 8, Question 2, printed p. 242. Some later citations refer to Section 6 of a preprint. All source citations and inspected locations are recorded separately in SOURCE_VERIFICATION.json.

## Approach 1: graphical upper domination

**Proposition 1.** For every lambda > 0, mu_lambda is stochastically dominated by independent site percolation with parameter p = lambda/(1+lambda). Consequently

lambda_p >= p_c(d)/(1-p_c(d)),

where p_c(d) is the independent nearest-neighbor site-percolation threshold.

**Proof.** For each vertex x, inspect the most recent mark before time 0 among its recovery marks and all arrows directed into x. The recovery rate is 1 and the total incoming-arrow rate is lambda. Let Z_x indicate that this mark is an arrow. The variables Z_x are independent: different destinations use disjoint directed-arrow processes and distinct recovery processes. Each has probability lambda/(1+lambda).

An infected x at time 0 cannot have a recovery as its most recent such mark. Therefore eta(x) <= Z_x simultaneously for all x in the upper stationary graphical construction. Equivalently one can start fully infected at time -T and let T tend to infinity; for every finite set, the probability that some site has no relevant mark in [-T,0] tends to zero. This proves domination. If p < p_c(d), the dominating field does not percolate. Letting lambda increase up to p_c/(1-p_c) proves the asserted non-strict lower bound; no assumption about percolation at p_c is needed. QED.

This comparison is already present in Rath-Valesin, Remark 1.5 and the discussion after Claim 2.5, credited there to Stein Andreas Bethuelsen. The proof above is an authored exposition, not a new result. It does not compare this lower bound with the nearest-neighbor lambda_c. The spread-out application instead combines it in dimension two with the distinct theorem lambda_c(R) -> 1. Substituting nearest-neighbor lambda_c for that limit is invalid.

**Boundary case d=1.** At every finite lambda the dominating Bernoulli parameter is below 1. Independent percolation on Z then has no infinite component: each half-line has infinitely many vacant sites almost surely. Hence lambda_p(Z)=infinity. This does not address the source's d >= 2 question.

## Approach 2: stationary moments and path estimates

For a finite set A define f_A(eta)=product_{x in A} eta(x), with f_empty=1. Let m(A)=E_mu[f_A].

**Proposition 2.** Stationarity gives the exact hierarchy

|A| m(A) = (lambda/(2d)) sum_{x in A} sum_{y adjacent to x} [m((A minus {x}) union {y}) - m(A union {y})].

For A={0}, translation and lattice symmetry give, whenever rho(lambda)>0,

P_mu(eta(e)=1 | eta(0)=1) = 1 - 1/lambda

for every nearest neighbor e of 0.

**Proof.** A recovery at a site of A contributes -f_A, and recoveries elsewhere contribute zero. An infection arrow y -> x with x in A contributes

(1-eta(x)) eta(y) product_{z in A minus {x}} eta(z)
= f_{(A minus {x}) union {y}} - f_{A union {y}}.

Sum the generator terms and integrate against an invariant measure. Bounded cylinder functions are in the generator domain for this finite-range process. For a singleton the identity reduces to rho=lambda(rho-m({0,e})); division by positive rho proves the formula. QED.

The formula exhibits strong dependence relative to rho as rho tends to zero near criticality. It does not control conditional probabilities after an entire previously exposed path.

**Proposition 3 (a sufficient path condition).** Let mu be a translation-invariant measure on {0,1}^{Z^d}. Suppose that for every self-avoiding nearest-neighbor path (x_0,...,x_n),

mu(eta(x_i)=1 for 0 <= i <= n) <= C q^n

with fixed finite C and q < 1/(2d-1). Then mu(Perc)=0.

**Proof.** There are at most 2d(2d-1)^{n-1} self-avoiding paths of n edges from a fixed root. A union bound makes the probability of an occupied such path tend to zero. An infinite component in a locally finite graph supplies self-avoiding paths of every length. Finally use a countable union over roots. QED.

The pair formula in Proposition 2 is not the hypothesis of Proposition 3: multiplying a two-site conditional probability down a path silently imposes an unproved spatial Markov property. In particular, positive association gives lower bounds on intersections of increasing events, not the needed upper bounds. The following construction supplies an exact failure of that multiplication inference in a symmetric, ergodic, positively associated field.

## Approach 3: vanishing density and weak convergence

**Proposition 4 (an inference counterexample, not a contact process).** For every d >= 2 there are translation-invariant, lattice-symmetric, ergodic, positively associated site fields with arbitrarily small positive density that percolate almost surely and converge locally weakly to delta_0 as their density tends to zero.

**Proof.** Let H_{j,k}, 1 <= j <= d and k in Z, be independent Bernoulli(epsilon) variables, with 0 < epsilon < 1. Set

eta_epsilon(x) = max_{1 <= j <= d} H_{j,x_j}.

A selected H_{j,k}=1 occupies the entire coordinate hyperplane {x:x_j=k}. Each such hyperplane is infinite and nearest-neighbor connected because d >= 2, and almost surely there are selected hyperplanes. Thus the field percolates. Its density is 1-(1-epsilon)^d, tending to zero.

The law is invariant under translations, sign changes and coordinate permutations. Increasing cylinder events are increasing functions of finitely many independent H variables, so Harris's inequality proves positive association; the usual cylinder approximation extends it. Translation along the diagonal vector (1,...,1) acts as a product of d Bernoulli shifts. Two cylinder events depend on disjoint H variables after a sufficiently large diagonal shift, so this transformation is mixing. Therefore the full translation action is ergodic. Finally, on each finite F, P(some occupied site in F) <= |F|[1-(1-epsilon)^d] -> 0, proving local weak convergence. QED.

For a concrete path-factorization check take d=2, epsilon=1/4, and sites (0,0),(1,0),(2,0). Direct enumeration gives

rho = 7/16, pair probability = 19/64, triple probability = 67/256.

The triple probability exceeds pair_probability^2/rho, since

triple_probability * rho - pair_probability^2 = 27/1024 > 0.

Thus the pair conditional cannot simply be repeated. This construction does not satisfy contact-process stationarity and is not a counterexample to the source problem. It isolates why small density, positive association, symmetries, ergodicity and weak convergence alone do not prove the desired gap. The construction is not spatially mixing in every direction; no such stronger assertion is made.

## Approach 4: finite-radius dual exploration

This approach gives a precise finite criterion and then proves it too weak at every potentially supercritical rate.

For an integer L >= 1 let I_x(L)={z: ||z-x||_infinity < L}. Starting at (x,0), explore the backwards infection cluster only while it lies in this finite interior. Stop with success at the first time an infection ancestor reaches its exterior; stop with failure if the cluster dies before that. Let Y_x(L) be the success indicator and h_L(lambda)=P(Y_x(L)=1).

Only recovery processes at vertices in I_x(L) and directed-arrow processes whose target lies in I_x(L) are needed. An arrow from outside to inside counts as success when traversed backwards, without revealing recovery marks or outgoing history at its external source. This target-based assignment of Poisson primitives is important for independence.

**Lemma 5.** The following hold.

1. eta(x) <= Y_x(L) almost surely in the stationary backwards construction.
2. The Y_x(L) variables within each residue class modulo m=2L-1 in all d coordinates are independent.
3. h_L(lambda) is continuous in lambda > 0. It can be computed from a finite absorbing continuous-time Markov chain and is rational at every rational lambda.
4. h_1(lambda)=lambda/(1+lambda).

**Proof.** An infection confined forever to a finite set dies almost surely. For example, over consecutive unit intervals there is a uniformly positive probability that all interior vertices recover and no interior-infecting arrows occur; independent intervals force such an event. Therefore survival backwards forever requires exiting the interior, proving (1). Interiors belonging to distinct centers in one residue class are disjoint. Their destination-assigned Poisson primitives are disjoint too, proving joint independence in (2).

For (3), the states are subsets A of the finite interior, together with a success state. Recoveries remove occupied sites; interior infection adds sites at rates linear in lambda; a birth to any exterior neighbor absorbs at success. The empty state is failure. Every transient state has a positive chance to reach failure before any birth within a bounded time, so all transient states are indeed transient, including on compact positive-lambda intervals. Hitting probabilities solve an invertible finite linear system with coefficients affine in lambda. Matrix inversion gives continuity and rational values at rational lambda. For L=1 there is just one active interior site, and the first recovery versus incoming arrow decides the outcome, proving (4). QED.

**Theorem 6 (color-class criterion).** If

h_L(lambda) < (2d-1)^[-(2L-1)^d],

then mu_lambda(Perc)=0.

**Proof.** There are M=(2L-1)^d residue classes. Among n+1 vertices of any self-avoiding path, one class contains at least ceil((n+1)/M) vertices. If the entire path is occupied under mu_lambda, all corresponding Y variables equal one, an event of probability at most h_L^{ceil((n+1)/M)}. The union bound in Proposition 3 now tends to zero whenever (2d-1) h_L^{1/M}<1. QED.

**Theorem 7 (this criterion cannot separate the thresholds).** For every d >= 2, every lambda >= 1, and every integer L >= 1, the strict inequality in Theorem 6 fails.

**Proof.** If L=1 then h_1(lambda)>=1/2>1/(2d-1). If L>=2, retain only the successive infection arrows along one prescribed straight path of L edges. At each newly reached vertex, require that the next specified arrow occur before the next recovery of that vertex. Do not impose recovery restrictions on vertices already left behind: reaching the exterior by one infection path suffices. The strong Markov property and independent Poisson increments give success probability

[a/(1+a)]^L = [lambda/(2d+lambda)]^L.

Other arrows may be ignored and cannot destroy this path. Thus

h_L(lambda) >= (2d+1)^(-L) for lambda >= 1.

For L>=2 and d>=2, (2L-1)^d >= (2L-1)^2 >= 3L, and (2d-1)^3 > 2d+1. It follows that

(2d-1)^{(2L-1)^d} > (2d+1)^L,

so (2d+1)^(-L) is strictly larger than the cutoff in Theorem 6. QED.

**Why lambda >= 1 covers the target.** The contact process started from one site is bounded by a continuous-time branching process with birth rate lambda per individual and death rate 1. Failed infection attempts and coalescence only decrease the contact population. The branching process becomes extinct almost surely for lambda <= 1; at equality its embedded jump chain is a simple symmetric walk on nonnegative integers absorbed at zero. Hence lambda_c >= 1. In particular every lambda > lambda_c lies in the range ruled out by Theorem 7.

At criticality h_L(lambda_c) does tend to zero as L tends to infinity, using classical critical extinction and the fact that a finite-lifetime finite-rate process visits only finitely many sites almost surely. This fact alone cannot meet a cutoff that deteriorates exponentially in L^d. Theorem 7 is stronger: the specific singleton-path coloring criterion never succeeds in the desired regime at any radius. This is not a no-go result for more sophisticated block crossings, multiscale renormalization, or other exploration algorithms.

## Approach 5: transfer from trees, spread-out models, and sharpness

The September 2026 Fernley-Jacob preprint proves strict separation on regular trees and explicitly retains the lattice problem as open. Its Section 6 factors events for successive path blocks using tree components cut off by boundary vertices. The same disjoint-domain argument is unavailable for a straight segment in Z^d, d>=2: external routes connect separated pieces.

**Proposition 8 (a geometric limitation).** No infinite rooted b-ary tree, b>=2, admits an injective map into Z^d taking its root to 0 and every tree edge to a nearest-neighbor lattice path of at most K edges, for a fixed finite K.

**Proof.** The b^n vertices at tree depth n would all have distinct images in the lattice ball of infinity radius Kn. That ball has (2Kn+1)^d vertices. Exponential growth eventually exceeds this polynomial, a contradiction. QED.

This rules out a bounded-length injective embedding shortcut, not every tree-based comparison. More directly, for the finite segment S={(i,0,...,0):0<=i<=n}, its complement is connected when d>=2. One can move off its axis in the second coordinate, travel past either endpoint, and return; any point off the axis has a route to this detour layer without hitting S. In particular, (i,1,0,...,0) and (j,1,0,...,0) are joined outside S for all i,j. Consequently the putative side branches of distinct path blocks are not disjoint domains. Their graphical explorations may use common marks. Tree independence cannot be carried across unchanged.

Similarly, the spread-out theorem's limit in R supplies a small collision parameter absent for a fixed nearest-neighbor kernel. It proves no monotonic implication from large R back to the nearest-neighbor threshold gap. A coupling that adds infection arrows orders upper invariant measures but orders both survival and percolation thresholds in the same direction; it does not preserve a strict gap between them.

The valid two-dimensional sharpness theorem of van den Berg establishes exponential cluster-size tails in a nonpercolating interval strictly above the survival threshold if such parameters are available. It does not prove that this interval is nonempty. The all-dimensional Beekenkamp preprint arXiv:1807.05591 is withdrawn and is not used as a theorem input.

## Exact remaining gap

To settle the target affirmatively for a given d>=2 one must establish mu_lambda(Perc)=0 for at least one lambda>lambda_c in the actual nearest-neighbor model. Monotonicity then gives lambda_p>=lambda>lambda_c. Equivalently, a genuine subcritical spatial-connectivity estimate at such a rate would suffice. None of Propositions 1-8 supplies this missing estimate. The counterexample in Proposition 4 is outside the contact-process family, and Theorem 7 obstructs only its explicitly stated criterion. No numerical simulation, finite test, source status statement, or alternate-graph result is treated as an infinite-lattice proof.
