# Independent audit of finite WARM threshold results

## Verdict and scope

**Accepted as a partial mathematical result, subject to the exact accepted manuscript identity recorded below.** The proof establishes the almost-sure forest conclusion for every alpha > 4/3 and arbitrary positive vertex rates, and the almost-sure whisker-forest conclusion for equal positive rates and every alpha >= 17/4. The equal-rate triangle establishes the sharp lower obstruction 4/3. The bundled target remains **OPEN** because the equal-rate whisker assertion for 4/3 < alpha < 17/4 is not proved. No conclusion at alpha = 4/3, infinite-graph extension, or novelty claim is accepted.

The audited model is a finite simple undirected loopless graph, unit initial edge counts, independent positive-rate vertex firing clocks, and reinforcement n^alpha. Isolated vertices are discarded and an edgeless graph is trivial. Loop and multigraph models are outside this stated scope. In particular, removing the loopless assumption is unsafe: a graph consisting of a single vertex and one loop retains that loop for every exponent.

The accepted source manuscript has SHA-256 c4392936cfff2b7a3e2762ff4d8804a96f8dc30e60f66aab16da24f207ac53b4 and 16,977 bytes. Every section, including the unequal-rate appendix, was read in that exact version. This publication edition changes only the opening problem-label sentence; every mathematical paragraph, equation, example, reference and appendix is unchanged. The exact distributed identities are recorded in ACCEPTANCE.json and MANIFEST.json.

## Published source bridge

Hirsch, Holmes, and Kleptsyn, *Infinite WARM graphs III: strong reinforcement regime*, Nonlinearity 36 (2023), 3013–3042, supplies the stochastic inputs. Theorem 1 on printed page 3016 covers finite graphs, alpha > 1, and arbitrary positive firing rates; it gives almost-sure convergence to stable or critical equilibria and positive probability of each strictly stable equilibrium. Unit initial counts are specified on printed pages 3014–3015. Proposition 1 on printed page 3021, with Conditions 1 and 3 automatic for a finite graph, identifies infinitely reinforced and positive-growth edges. These results are imported, not re-proved. The paper's normalization footnote on printed page 3015 is consistent with the explicit scaling below. [Published PDF](https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf), [DOI](https://doi.org/10.1088/1361-6544/acc9a0).

Holmes and Kleptsyn's 2017 paper supplies the prior >25 bound and the credited least-weight leaf argument. The latter appears as Lemma 4 and Corollary 7 on author-manuscript pages 19–20. Its older stochastic statements are not used in place of the stronger published 2023 theorem. [Author manuscript](https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf), [DOI](https://doi.org/10.1063/1.4978683).

The two finite-graph questions and the 4/3 obstruction are stated on printed page 655, PDF page 17, of Oberwolfach Reports 12/2023. This is the problem provenance; it is not a proof of the new upper bounds. [Report DOI](https://doi.org/10.4171/owr/2023/12).

## Normalization and boundary checks

1. With Lambda = sum_v lambda_v, x = a/Lambda, and p_v = lambda_v/Lambda, the fields obey F_lambda(a) = Lambda F_p(a/Lambda). Their Jacobians at corresponding equilibria are identical. This verifies that the counts-per-time convention does not change the stability test used in the source.
2. Each vertex's incident tally sum dominates its firing count. At a limiting equilibrium its incident positive weights therefore sum to at least lambda_v. Every denominator on the retained support is positive.
3. For alpha > 1, zero-edge coordinates give a -I block in the full Jacobian. Both off-diagonal blocks between zero and positive coordinates vanish. Positive-support instability is therefore genuine full-system instability.
4. The support may be disconnected; the deterministic restriction is componentwise. No unjustified claim that stochastic processes conditioned on their support are independent is needed.
5. For a common rate c > 0, time rescaling to unit rates multiplies limiting weights by c and leaves support and the relevant Jacobian signs unchanged. The numerical weight bounds 1 and 3/2 are used only after this normalization.

## Hessian and cycle proof

The identity F = diag(a) grad L holds on the positive face. At equilibrium, DF = diag(a) Hess L is similar to diag(sqrt(a)) Hess L diag(sqrt(a)). A positive Hessian direction gives a positive real Jacobian eigenvalue. The change y_e = a_e^alpha is invertible on that face; its Hessian transformation is a congruence because the equilibrium gradient vanishes.

Independent differentiation confirms

alpha^2 Hess Phi[w,w] = (alpha-1) sum_e a_e^(1-2alpha) w_e^2 - alpha sum_v (lambda_v/S_v^2) (sum_{e incident to v} w_e)^2.

The relative-coordinate formula and the diagonal necessary condition follow with the stated signs and factors. These are necessary conditions for every equilibrium having no positive eigenvalue, including critical equilibria.

On a simple cycle, the equilibrium identity gives the exact rearrangement of sum D_e into endpoint b_v terms. The inequalities S_v >= A_previous + A_next and (A_previous + A_next)^2 >= 4 A_previous A_next prove 4 sum c_v <= sum D_e. Extra incident edges and chords only increase S_v; perturbations on every noncycle edge are zero.

For an even cycle, the alternating direction annihilates every incidence sum and gives a positive value for all alpha > 1. For an odd cycle of length m, the two real Fourier directions are cyclically consistent. Their squared edge values sum to one, and their squared vertex sums add to 4 sin^2(pi/(2m)). Adding their quadratic forms yields the lower bound [alpha cos^2(pi/(2m)) - 1] sum D_e. Strict positivity therefore holds at the asserted strict threshold. At least one of the two real directions is positive; neither direction is incorrectly required to be individually positive.

Since every finite nonforest simple graph has a cycle and the largest odd-cycle threshold is 4/3 at m = 3, Theorem A is valid. The stochastic bridge then applies to the original finite graph.

## Whisker proof and all exponent intervals

The least positive weight in a component cannot have two nonleaf endpoints when alpha > 2: both endpoint selection probabilities would be at most 1/2, contradicting the diagonal necessary condition. Its leaf endpoint contributes one unit of rate, so every retained weight in that component is at least one.

For a nonleaf edge with 1 <= a <= 3/2, each endpoint has a competitor of weight at least one. Hence q,r <= s_alpha(a), q+r = a, and convexity gives the extreme-split upper bound f(a,s_alpha(a)). Feasibility implies s_alpha(a) >= a/2, exactly the region where f increases in its second argument.

The revised symbolic argument is self-contained. For 3 <= B <= 7, the lower bound s_B(a)/a >= 1/2 follows from (a-1)(1+a-a^2) >= 0 on [1,3/2]. The upper bound follows from the minimum of R(a) = 2a^7-3a^6+2 at 9/7, where R = 52763/823543 > 0. Independent differentiation verifies

d/da f(a,s_B(a)) = 1-2z^2+2(2z-1)s_B'(a) >= 1/9,

with z = s_B(a)/a. Thus the whole weight interval reduces to its endpoint a = 3/2.

All five closed exponent intervals meet exactly and cover [17/4,7]. The displayed endpoint margins were independently recomputed with exact rational arithmetic:

- [17/4,13/3]: 1/1734
- [13/3,9/2]: 163/65598
- [9/2,5]: 5399/1361250
- [5,6]: 74117/6288490
- [6,7]: 527104/16077675

The fractional-power upper bounds were checked by cubing and squaring, respectively: their exact positive differences are 504313/1024000 and 317/512. Therefore the inequalities hold uniformly on all five intervals, including alpha = 17/4. No Bernstein coefficient table, numerical sampling, or omitted generated certificate is needed.

For alpha >= 7, the quadratic necessary condition is negative at r_0 = 1/2 and positive at zero, so the allowed r_0 in [0,1/2] lies below its smaller root. With C = 3-sqrt(2), the identity C^2+C = 7(C-1) gives r_0 <= C/alpha. The exponential-series calculation is exact: the partial sum 9067/1875 plus tail bound 4096/34375 equals 510973/103125 < 6. Hence both endpoint probabilities would be strictly below 1-1/alpha, a contradiction. This covers the entire unbounded tail, with overlap at 7.

Every nonleaf edge consequently has weight strictly greater than 3/2. Two such edges cannot meet, since each would take more than half the shared vertex's selection probability. In a tree of diameter at least four, the two middle edges of a length-four path are adjacent nonleaf edges. This establishes Theorem C for stable and critical equilibria alike.

## Exact controls and rejected extrapolations

- The equal-rate unit-weight triangle has spectrum {-1, 3alpha/4-1, 3alpha/4-1}. At alpha = 5/4 the two transverse eigenvalues are -1/16; at 4/3 they are zero; at 3/2 they are 1/8. These controls confirm the lower obstruction, the excluded endpoint, and the Hessian sign convention. Strict-stability attainability is not misapplied at the endpoint.
- At alpha = 3/2 the triangle passes the diagonal necessary condition but is unstable. This verifies that the diagonal test alone cannot replace the Fourier argument below 2.
- An exact unequal-weight, unequal-rate triangle at alpha = 2, with weights (1,3/2,5/4) and rates (697/480,169/120,427/480), satisfies the equilibrium equations and the Jacobian/Hessian relation. The sum of the two scaled Fourier quadratic forms is 8246303/8440875 > 0.
- A unit-weight triangle with one additional pendant edge and rates (3/2,1,1,1/2) is an equilibrium at alpha = 4/3. The summed scaled Fourier forms equal 1/9 > 0. This checks the attached-edge terms explicitly and does not assert that all bare triangles are unstable at that endpoint.
- A unit-weight four-cycle with an added diagonal and endpoint rates equal to half their degrees verifies the even-cycle cancellation even with a chord, at alpha = 5/4.
- For a unit-rate triangle with retained weights (3/2,3/2) and one zero edge, at alpha = 2 the full Jacobian is the direct sum of [[-2/3,-1/3],[-1/3,-2/3]] and [-1]. This is an exact boundary-block control.
- The appendix's unequal-rate four-edge path at alpha = 2 was independently recomputed from its given weights and rates. Direct differentiation agrees with its matrix K, whose four leading principal minors are exactly 4752/5, 421632/25, 782336/125, and 4194304/18225. They are all positive, establishing a strictly stable non-whisker outside the equal-rate hypothesis. This is consistent with the stated scope.
- The reported finite tree search is exploratory only. Its stated 175 trees equal 1+3+8+19+43+101; its seeded starts and finite integration cannot establish a global or stochastic nonexistence claim. No theorem in this audit relies on it.

The proof author's exact arithmetic verifier was also run successfully in ordinary, -O, and -OO modes. In each mode, all seven supplied negative controls were rejected: an inadequate power cap, altered rational margin, interval-coverage defect, unsupported sharp whisker interval, false strict stability at the critical triangle, false forest exclusion below 4/3, and reversed definiteness sign. These runs corroborate the independently checked mathematics; they are not proof dependencies.

## Acceptance boundaries

The accepted proof includes all finite algebra needed for the 17/4 bound. The stochastic conclusion remains conditional on the correctly cited published theorem, as explicitly acknowledged in the proof. Mathematical acceptance does not claim peer review, novelty, publication, completion of the combined target, or permission to distribute other files. No source PDF, extracted source text, dataset, generated certificate, or exploratory code is part of the mathematical deliverable identified by this audit.
