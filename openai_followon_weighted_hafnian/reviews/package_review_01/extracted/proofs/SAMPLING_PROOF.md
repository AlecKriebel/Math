# A bounded-bit sampler from an unweighted counting FPRAS

This is a self-contained application of established approximate-counting self-reduction, not a claim that the self-reduction framework is new. The pinned family-113 manuscript already gives an edge-deletion version in its subsection “A deletion sampler for perfect matchings”, lemma `lem:deletion-sampler` (its `build/main.tex`, lines 3195–3290 in the inspected copy). That proof cites Jerrum, Valiant, and Vazirani, *Random generation of combinatorial structures from a uniform distribution*, Theoretical Computer Science 43 (1986), 169–188, DOI 10.1016/0304-3975(86)90174-X, Section 6. Its application corollary explicitly excludes compressed edge weights. The argument below uses a vertex-pairing reduction, then an exact gadget pushforward. It depends on the unweighted FPRAS; it does not independently validate that pivotal dependency.

## Exact hypotheses and statement

For a finite simple undirected graph H, let Z(H) be its number of perfect matchings, with Z(empty)=1. Assume these two algorithmic primitives:

1. A deterministic polynomial-bit-time procedure P(H) returns a perfect matching of H, or an infeasibility answer exactly when Z(H)=0. In particular it returns the empty matching on the empty graph. This is the standard perfect-matching existence/witness theorem.
2. For every H and rational 0<a,g<1, a uniform randomized procedure C(H,a,g) returns a nonnegative rational A on every execution, with Pr[(1-a)Z(H) <= A <= (1+a)Z(H)] >= 1-g. Its bit time on **every** execution is at most a polynomial T in the full graph/parameter encoding length, a^{-1}, and log(g^{-1}). Consequently its output encoding length is polynomially bounded even on unsuccessful executions. Calls use fresh independent randomness.

The sampler described here, for an explicit graph H0 with N=2s vertices and rational 0<eta<1, answers infeasibility exactly if Z(H0)=0. Otherwise it returns a perfect matching of H0 on every execution and has output law nu satisfying TV(nu,U(H0)) < eta, where TV is one half the sum of absolute probability differences. The sampler uses at most s^2 count calls, at most s^2+1 witness calls, and at most s*b fair bits **in addition to the counting oracles' own bits**. Its bit running time on every execution is polynomial in the full input encoding length and eta^{-1}. The case N=0 returns the empty matching and uses no counting calls or sampling bits. An odd-order graph is infeasible and can be handled directly by P.

## Parameters and explicit algorithm

Run P(H0) first. On infeasibility stop with that answer; on N=0 return its empty matching. Otherwise write

    Cmax = s^2,
    a = eta/(4s),
    g = eta/(4Cmax),
    b = min{j >= 0 : 2^j * eta >= 4Cmax},
    R = 2^b.

Compute b by integer doubling and exact rational comparison. Maintain a partial matching S, a feasible residual induced graph H, and an exact witness W_H supplied by P. Initially S is empty and H=H0.

At a nonempty residual graph, choose its least vertex u in a fixed input ordering. For every neighbor v, run P on H-{u,v}. Discard precisely the infeasible children. At least one child survives: the edge incident to u in W_H gives one. Let surviving neighbors be v1,...,vk in fixed order, with child graphs Hi and stored child witnesses Wi.

If k=1, select that child with certainty and make no counting calls or sampling-bit draws. Otherwise call C(Hi,a,g) freshly for every i, obtaining Ai. If all Ai are zero, return S union W_H immediately; this is the **witness fallback**. If their sum is positive, compute exact rational cumulative probabilities

    Fi = (A1+...+Ai)/(A1+...+Ak),  F0=0, Fk=1,
    Bi = floor(R*Fi),             B0=0, Bk=R.

Draw exactly b independent fair bits to obtain uniform J in {0,...,R-1}. Choose the least i with J<Bi. Append uv_i to S and replace H,W_H by Hi,Wi. Repeat. When H is empty, return S.

Every selected child has an exact witness, including children whose estimates vanish or fail. The fallback also has an exact witness. Thus output feasibility is deterministic and needs no event of successful estimation. Every ordinary step removes exactly two vertices; fallback terminates immediately. There are at most s decisions. There is no rejection loop, rational Bernoulli loop, or random convergence test.

## Ideal law

For a residual H and its feasible children, put zi=Z(Hi)>0. Every perfect matching of H pairs u with exactly one vi, and deleting that edge gives a bijection to a matching of Hi. Therefore

    Z(H) = sum_i zi,                 pi = zi/Z(H).

The ideal sampler chooses child i with probability pi. Along the sequence leading to a complete matching M, the product of conditional probabilities telescopes to Z(empty)/Z(H0)=1/Z(H0). Hence the ideal output law is uniform. Forced children have probability one and do not change this identity.

## Relative-estimate normalization bound

If all current estimates succeed, write Ai=zi(1+ei), |ei|<=a and put ebar=sum_i pi*ei. Then the normalized estimates satisfy

    qi = Ai/sum_j Aj = pi*(1+ei)/(1+ebar),
    TV(q,p) = [sum_i pi*|ei-ebar|]/[2(1+ebar)]
            <= a/(1-a).

Indeed |ei-ebar|<=2a, and 1+ebar>=1-a. In particular all successful estimates are positive. The all-zero fallback is impossible when all current estimates succeed, regardless of how small the positive true probabilities are.

## Fixed-bit rounding bound

For any categorical law q on k outcomes, let F be its cumulative law and let its dyadic implementation have probabilities

    q'_i = (floor(R*Fi)-floor(R*F_{i-1}))/R.

For di=floor(R*Fi)/R-Fi, d0=dk=0 and |di|<1/R for internal boundaries. Consequently

    TV(q',q) = (1/2)sum_i |di-d_{i-1}|
             <= sum_{i=1}^{k-1}|di| < (k-1)/R <= k/R.

Repeated equal boundaries have zero interval length, so a zero estimated probability is never accidentally selected. The final boundary is R, so the draw always chooses some feasible child. This construction handles arbitrarily tiny rational probabilities with a bounded number of bits: they may round to zero, and the displayed TV bound pays for that loss.

## Adaptive failures and cumulative TV

Fix **any full history before the current decisions**, including prior estimator outputs and sampling bits, which yields the current feasible residual graph. Each current count call has a fixed valid graph input; fresh oracle randomness ensures its failure probability conditional on that history and all earlier calls is at most g. The conditional probability that any of the k current calls fails is therefore at most k*g. No independence of the success events is needed for the union bound.

Conditional on every current call succeeding, each possible estimate vector gives a next-child law within a/(1-a)+k/R of the ideal child law. Fresh draw bits are independent of that vector. Convexity of TV gives the same bound for the mixture over successful estimate vectors. On the failure event the entire transition law, including an immediate fallback output, can differ by at most one. Thus at every adaptive history the conditional next-transition TV is bounded by

    a/(1-a) + k*g + k/R.

Forced choices have zero error and need no calls. Formalize transitions on partial matchings with residual graphs, together with absorbing finished-output states; pad both algorithms to s stages. Couple the two processes until their states first differ, using the preceding conditional TV bound at each common history. The ideal process has the same exact branch probabilities conditional on that history because they depend only on the current residual graph. The probability of any divergence bounds their final output TV.

At stage with 2r residual vertices, k is at most 2r-1. Along any ordinary history the sum of these stage bounds is at most

    sum_{r=1}^s (2r-1) = s^2 = Cmax.

A fallback only shortens the history. Hence, uniformly over adaptive histories,

    TV(nu,U(H0)) <= s*a/(1-a) + Cmax*g + Cmax/R.

Since a<1/4, Cmax*g=eta/4 and Cmax/R<=eta/4, this is strictly below

    eta/3 + eta/4 + eta/4 = 5eta/6 < eta.

This argument does **not** condition the final output on the event that every oracle call succeeds; doing so could bias the deletion history. It bounds every next-step kernel conditional on each actual past history and integrates the failure mass directly.

## Call budget and polynomial bit time

There is one initial witness call, and at stage with 2r residual vertices at most 2r-1 child witness tests. Thus there are at most Cmax+1 witness calls. Counting is performed only on feasible children at nonforced stages, so at most Cmax calls occur. All oracle graph inputs are induced subgraphs of H0 and have encodings polynomially bounded by H0's explicit input length. The oracle parameters satisfy

    a^{-1}=4s/eta,
    log(g^{-1})=log(4s^2/eta),
    b=O(log(s/eta)).

If B bounds the encoding length of a count estimate, including unsuccessful ones, the sum of at most N rational estimates can be represented with O(N*B) numerator/denominator bits by taking the product of their denominators. Reduction to lowest terms is optional. Cumulative ratios, integer floors and comparisons therefore use polynomial bit arithmetic. The parameter eta's own encoding length must also be included; a rational near one can have a long input encoding despite bounded eta^{-1}.

For full graph/parameter input length L, a representative explicit oracle budget is

    Cmax * T(poly(L), 4s/eta, log(4s^2/eta))

plus (Cmax+1) deterministic polynomial witness computations and polynomial arithmetic in L, N, B and b. The exact polynomial degree is inherited from the two primitives. This gives a uniform polynomial bound on **every** execution, including every failure history. At most s draws use s*b bits; the counting calls' own random bits are bounded by their worst-case bit times. No claim of exact uniformity or pointwise relative sampling error is made.

## Pushforward to nonnegative rational weighted matchings

Let A have order 2m with nonnegative rational off-diagonal entries. Delete zero-weight edges. Choose an exact common denominator D and integer weights W_e=D*A_e. Suppose the proved integer-weight gadget reduction produces an explicit finite simple graph G_A such that the natural map phi from its perfect matchings to original perfect matchings has

    |phi^{-1}(M)| = product_{e in M} W_e.

Its total count is D^m*haf(A). For positive haf(A), the pushforward of the uniform matching law on G_A is exactly

    Pr[M] = product_{e in M} A_e / haf(A).

Apply the sampler above to G_A with accuracy eta and output phi of its matching. For any two laws nu,mu and deterministic map phi,

    TV(phi_*nu,phi_*mu)
      = (1/2)sum_y |sum_{x:phi(x)=y}(nu(x)-mu(x))|
      <= TV(nu,mu).

Thus the weighted law is approximated within eta. If N_A is the expanded graph order, use s=N_A/2 in all displayed budgets. The exact gadget's polynomial-size bound then makes the sampler's bit time polynomial in the original matrix's full binary input length and eta^{-1}. This remains valid for disconnected support, weights below one, large denominators, and arbitrarily small positive hafnians. Feasibility is checked exactly by P on the original support or on G_A; no relative-error operation is used to infer whether a positive hafnian is zero. For m=0, phi maps the unique empty matching to itself and the weighted law is a point mass.

## Executable finite validation and its limits

`code/sampling.py` implements the exact rational sampler with explicit interfaces for C, P and fixed-bit draws. Its `exact_matchings` and `exact_witness` helpers are exponential reference enumerators, **only for small-instance testing**. They are not the polynomial witness algorithm and do not implement or certify family 113's FPRAS.

Run `python3 code/test_sampling.py` from the project root. It writes `data/sampling_verification.json`. The suite integrates output laws exactly over dyadic draw intervals and all synthetic independent zero-estimate failure patterns. It includes adaptive residual-dependent successful error endpoints, all simple graphs on 0, 2 and 4 vertices, seeded six-vertex instances, complete graphs, disconnected instances, empty and infeasible inputs, tiny probabilities, witness fallback and worst-case call/bit caps. Exact finite tests support the implementation and catch boundary mistakes; the proof, rather than these tests, establishes the uniform asymptotic and TV guarantees.

The checked run comprised 203 graph instances, 1827 exact output-law integrations, 1218 imperative executions, and 243 exercised all-zero fallback events. Five actual rational-matrix gadget expansions were tested under three synthetic-oracle scenarios each: their exact projected laws had TV at most the expanded-graph TV and at most eta. These include the empty matrix, integer weights, a weight 1/2, and disconnected support with a weight 1/3. The data retain exact rational errors; finite observations are not claimed to certify the general theorem or the upstream oracle.
