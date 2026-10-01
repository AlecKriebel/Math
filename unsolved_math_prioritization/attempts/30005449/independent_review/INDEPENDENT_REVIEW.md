# Independent review: 30005449, trace-reinforced ant partials

**Verdict: PASS_SCOPED_PARTIALS. The original general-graph deterministic-limit question and the several-food question remain unsolved after 5/5 author turns.** No substantive mathematical correction is required. An edgeless-core boundary case is made explicit below. This review does not certify novelty or priority.

Reviewed 2026-10-01. Frozen author manifest SHA-256: `2cf4c498dfc172dc81b3fbd92d225b78c8660bb432008dba99627b5cb220d723`. Tree theorem `TURN_4.md`: `0282c8aa44365e23e9d859fc1d0959688fa8a2c68c51609337ae5bf0194996f5`. Cyclic-core theorem `TURN_5.md`: `eadd8859086487746abda027e0a0f4e4638929cce736ae5db7777224683f24c0`.

All eighteen manifest entries and four primary PDF hashes were verified. Frozen mathematical files were not changed. The reviewer did not contribute to the author proof turns. The author's exact checker was inspected and replayed, reproducing its 1,073-assertion receipt byte-for-byte. A separately written standard-library rational checker independently reconstructed first-step and electrical calculations and passed 4,220 exact assertions. The sixty ODE experiments were treated as inconclusive diagnostics and were not used as evidence of convergence or uniqueness.

## 1. Exact source and model

The original OWR contribution, printed pp. 645–646 of [OWR 12/2023](https://doi.org/10.4171/owr/2023/12), concerns both a deterministic normalized-limit question for trace reinforcement and a separate several-food modeling question. The definitive full source is [Kious–Mailler–Schapira, JEP 9 (2022), 505–536](https://www.numdam.org/articles/10.5802/jep.188/). Its model and Conjecture 1.1 on printed p. 507 were read, and the conjecture page independently rendered and visually inspected.

Every ant starts at N, uses conductances frozen for its entire walk, stops on first hitting F, and then adds exactly one to each edge in the trace. Repeated crossings during that walk do not produce repeated reinforcement. The source starts all weights at one. Parallel edges incident to food are excluded by the qualification immediately before Conjecture 1.1; the known parallel-edge Dirichlet example is therefore not an admissible counterexample. Parallel nonterminal edges in the cyclic-core theorem cause no problem. The proofs explicitly use loop-free undirected graphs and connectivity to food.

The ordinary-tree theorem is distinguished correctly from the source's tree-like graphs formed by wiring several leaves to food. The 2026 [two-nest paper](https://arxiv.org/abs/2601.22855) uses a different loop-erased update and does not settle the present trace model.

The stronger positivity sentence in the paper is not silently included in the imported deterministic-convergence target. A source-qualified consequence concerning that sentence is recorded separately in Section 7 below.

## 2. Exact trace drift and occupation-time representation

The killed-edge matrix is correct. The ordinary Dirichlet conductance Laplacian includes an off-diagonal -w_e and endpoint diagonal contributions w_e. Adding w_e J_e removes the transition across the queried edge while retaining precisely the two success-killing rates. The right-hand side w_e(1_u+1_v) records absorption into success. Every component after deleting the edge meets food or a success endpoint, so the killed matrix is positive definite. Terminal edges require only the one-sided flux formula; the packet makes that distinction.

The rank-two inversion numerator and determinant denominator were checked independently. The determinant ratio is positive for positive weights, so no denominator branch is hidden. The terminal probabilities sum to one because precisely one food edge is the terminal transition. Scaling all conductances changes holding times but not the stopped discrete walk.

For a fixed edge, run the continuous-time conductance walk with that edge deleted. An independent exponential killing mechanism of rate t while at its endpoints has survival probability exp(-t L_e), where L_e is endpoint occupation before food. A deleted bridge can create a closed component; on that event occupation at an accessible endpoint is infinite. The infinity convention then gives success probability one, as required. This is a representation of first crossing, not of the number of crossings. Differentiation at every t>0 is valid because the damped moments are bounded. Strict decrease of p_e(t)/t holds exactly when positive occupation has positive probability, including an infinite-occupation atom.

Coordinate uniqueness and negative diagonal derivatives therefore follow, but no global stability follows from them alone. The packet retains that distinction. The triangle curl and its dependence on the third conductance correctly rule out the proposed C2 potential and every fixed positive diagonal weighting of that specific per-capita field. They do not exclude all Lyapunov functions or state-dependent metrics.

## 3. Finite-tree theorem

Each N–F path edge is crossed by every ant and hence has weight n+1 exactly. Components that can only be reached after food remain unvisited. For a reachable off-path branch, crossing a selected edge is equivalent to reaching its farther endpoint before F. Excursions away from the path between those absorbing endpoints return before either endpoint is reached and do not alter the harmonic equation. The resistance ratio in TURN_4 is therefore exact, including arbitrary positive finite-time branch weights.

The scalar stochastic-approximation lemma has both necessary components. Its limiting scalar drift has only equilibria zero and beta, with the stated sign on the intervening intervals. Bounded martingale differences, square-summable step sizes and uniformly vanishing adapted drift error give the standard one-dimensional asymptotic-pseudotrajectory conclusion. Its connected internally chain-transitive limit set is one of the two equilibria; there is no interval of equilibria being overlooked.

The boundary-zero exclusion is valid and essential. A harmonic conditional lower bound makes the unnormalized count diverge by conditional Borel–Cantelli. The centered logarithmic increments have the stated variance bound. Dividing them by log(n+2) produces a square-summable martingale series, and Kronecker's lemma makes their cumulative contribution o(log n). On a putative zero-limit event the conditional logarithmic drift would yield growth exponent d>1, contradicting the elementary upper bound n+1. Random eventual coefficient bounds can be localized by countably many deterministic bounds and starting indices.

For d=1 the nonnegative-supermartingale argument correctly gives limit zero, and nesting of trace events transfers this to descendants. For d>=2 induction along each finite branch has a positive denominator limit and yields exactly ((d-1)/d)^k. The argument proves actual almost-sure limits, rather than merely identifying equilibria.

## 4. Cyclic core and effective conductances

The one-attachment geometry is used precisely. All food-stem weights are n+1, so in normalized units the food path has conductance 1/d. Before first crossing the queried core edge, replacing it with two success edges to a common absorbing vertex gives the correct success event. Eliminating both networks at their sole common vertex N produces p_e=d C_e/(1+d C_e).

The Dirichlet minimum proves continuity, concavity, homogeneity and coordinate monotonicity of C_e even at zero weights. Potentials can be clipped to [0,1]; ordinary-edge energy coefficients are at most one and the two success contributions sum to at most two. This gives the asserted global Lipschitz bound. Thus the drift genuinely is cooperative on this class. The strict subhomogeneity follows from the scalar conductance fraction for positive vectors.

The spanning-tree lower vector is legitimate. Adding non-tree edges cannot lower a tree-edge success conductance. For a non-tree edge, retaining one tree path to an endpoint and one success edge gives the displayed series-conductance lower bound. A sufficiently small common delta therefore yields a positive subsolution. Monotone iteration is bounded by one, hence converges to a positive fixed point. The max-ratio comparison proves uniqueness without assuming a global potential.

The radial identity (5) and the signs of its lower and upper scalar comparisons are correct. Positivity of solutions follows from w'_e>=-w_e. The logistic subsolution and supersolution give convergence to chi, uniformly on compact subsets of the positive orthant, and stability there. Mere uniqueness has not been substituted for global attraction.

**Degenerate core:** if H consists only of N and has no edge, the graph is just the deterministic food path and the theorem is immediate; the positive core vector is the empty vector. The displayed minimum over chi is used only when H has at least one edge. This harmless zero-dimensional case is understood separately and does not require altering the frozen nonempty-core argument.

## 5. Stochastic persistence and ODE-to-process passage

Persistence is proved edge by edge along a spanning tree and then on the remaining edges. The series-path lower bound has the increasing scalar form dX/[1+(R+d)X], with d>1, so the scalar lemma provides a positive lower normalized limit. Correlation of different trace-edge indicators is irrelevant to each one-coordinate monotone coupling.

For rigor, the random eventual bound should be read through localization, not conditioning on a non-stopping future event: for every deterministic R and starting index T construct the scalar coupling and stop its domination at the first violation of the ancestor bound. On the event that the bound holds for all n>=T, the stopping never occurs. Countably many integer R,T cover the almost-sure eventual-bound event. Each scalar comparison theorem holds with probability one independently of that event. This validates the frozen proof's stated countable-union localization and avoids an illicit future-conditioned law.

Finiteness of H then gives a random positive lower bound on every coordinate of the limit set. The exact stochastic approximation has bounded noise and square-summable steps; the explicit conductance drift is Lipschitz even on the closed cube. The primary paper's Theorem 2.5 and Corollary 2.6, printed p. 513, were checked. Global attraction and stability on positive compact sets, combined with persistence, force the internally chain-transitive limit set to be the singleton chi. The stochastic convergence conclusion is therefore justified separately from the ODE calculation.

## 6. Independent finite checks

The separate `independent_check.py` uses only Python's standard library and exact fractions. It builds normalized discrete-time first-step equations, solves them by rational Gaussian elimination, and independently computes effective conductances by Kirchhoff voltage equations and root flux. It does not import the author checker or its killed-matrix implementation.

Its 4,220 assertions cover terminal and inaccessible edges, parallel nonterminal edges, bridges, trees with food at an interior vertex, cyclic cores, homogeneity, the rank-two formula, rational own-edge concavity controls, resistance probabilities, scalar drift signs, and the radial comparison identity. The written proofs supply the universal concavity, stochastic and comparison arguments; finite checks are not substitutes. The author's exact output was independently replayed byte-for-byte. The numerical floor and finite ODE diagnostics remain expressly inconclusive.

## 7. Secondary source qualification: the additional positivity sentence

The literal second sentence of the published Conjecture 1.1 asserts positivity of every limiting edge weight when dist(N,F)>=2. The reviewed ordinary-tree theorem has an immediate counterexample to that extra assertion as worded: take the three-edge tree N–a–F and a pendant edge a–b. The pendant is accessible before absorption, has attachment distance d=1, and its normalized weight tends to zero by TURN_4; meanwhile dist(N,F)=2. The exact trace probability is X/(1+X), independently checked.

The model statement inspected contains no general exclusion of such accessible dangling edges. An additional intended restriction to edges on an N–F simple path would change the positivity assertion, so any discussion of this consequence must retain that qualification. This observation is a direct consequence of the frozen tree theorem, not a new author search turn or a resolution of the imported deterministic-limit question. It does not establish novelty, and it is not used to relabel the overall target as solved.

## Final disposition

All scoped analytic reductions and both special-class almost-sure convergence theorems pass. Keep the general finite-graph and several-food questions **unsolved at 5/5**. The cooperative conductance argument depends on the fresh food stem attached at N and does not extend automatically to competing food routes. Preserve the no-parallel-food qualification, frozen proof history, exact receipts and classical stochastic-approximation/electrical-network credit. Publication remains under the parent gate.
