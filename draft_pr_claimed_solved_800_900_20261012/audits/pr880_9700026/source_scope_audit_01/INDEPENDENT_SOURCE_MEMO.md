# Independent source memo (before inherited proof, verdict, catalog, or prior report)

Created UTC: 2026-10-15T09:29:38.999954+00:00

## Reading scope and pins

Read the entire supplied 2007 draft PDF pages 1-9 and 39-41 in layout-preserving text, including the complete section 6.4 and Conjecture 32 on printed/PDF page 40. Searched the complete 41-page text for general-position, parameter, and associated-system conventions; no second general-position definition occurs. Visually inspected complete pages 2, 4, and 40. Read all 11 pages of the supplied arXiv:1209.5120v1 text, including model scope, remarks, heuristic assumptions, critical case, all captions, discussion, references, and visual inspection of model pages 2-3 plus the plot-only page 8. The draft is internally dated April 25, 2007; the later paper's header identifies v1, 23 September 2012. Byte/hash pins are in PRIVATE_SOURCE_PINS.json. This is a statement audit, not a historical novelty search.

## Exact original deterministic target

Let D=[0,1]^2. Fix finite n city sites x_i in D. For z in the probability simplex and alpha,beta>0, set
S_i(z)={y in D: z_i^alpha |y-x_i|^(-beta) = max_j z_j^alpha |y-x_j|^(-beta)},
A_i(z)=area(S_i(z)), and dz_i/dt=A_i(z)-z_i.
The conjecture supposes both sites and positive initial values to be in unspecified general position. There is no supplied definition of that phrase. Distinct sites and generic strictly positive weights are the natural nondegenerate reading. Pairwise tie loci of distinct sites have zero planar area, so their allocation does not change A_i. The model is hard maximum allocation; no influence-sum or logit probability occurs in this ODE.

The 2007 global parameter declaration permits every alpha>0, beta>0 (and a positive finite c0 that cancels from the cells). It says the notes focus on alpha<1; that is a focus, not a domain exclusion. Page 4 explicitly treats alpha>1 and lists it in the unbalanced parameter region. The complete Conjecture 32(a) claims convergence to a simplex vertex when alpha>1 OR 0<beta<2alpha. Part (b) claims an initial-condition-independent, strictly positive coordinatewise limit when 0<alpha<1 and beta>2alpha. The sites remain fixed in this claim.

## Model boundaries

The full stochastic process has a new-city event and allocates an immigrant at y to the maximizer city only after deciding against founding a city. The associated ODE is introduced after freezing the city set; the notes describe the approximation informally and do not establish a stochastic/ODE equivalence theorem. Consequently, a deterministic counterexample does not by itself refute stochastic Conjecture 1 or establish stochastic balanced growth.

The later 2012 paper studies a stochastic model with the same hard-maximum influence rule but explicitly restricts its parameter declaration to 0<alpha<=1, beta>0. It gives heuristics and simulations, not Conjecture 32 or a frozen-city ODE convergence theorem. Its comment dismissing alpha>1 does not retroactively rewrite the 2007 domain. It cannot be used to claim a counterexample at alpha=2,beta=8 lies within the 2012 stated parameter range.

## Falsifiable success criterion for the offered counterexample family

For some finite n>=2, admissible generic distinct sites and positive generic initial weights, choose alpha>1 and beta>2alpha, for example alpha=2,beta=8. A proof that each z_i stays uniformly bounded away from zero for all sufficiently large t rules out convergence of any coordinate to one. If that proof applies to all distinct sites and all positive initial weights, the undefined general-position qualifier cannot remove its counterexamples under any nonempty usual generic interpretation. A symmetric nongeneric equilibrium alone would not satisfy this criterion.

This would refute the literal unrestricted part (a), hence any catalog assertion formed as the conjunction (a) and (b). It would not prove (b), nor refute collapse restricted to beta<2alpha, settle beta=2alpha, or settle the stochastic growing-city model. A catalog containing only alpha<=1 collapse would not be answered by alpha=2,beta=8.

## Independent source consistency check

The ODE depends only on alpha/beta, because cells are the minimizers of |y-x_i|/z_i^(alpha/beta). Multiplying both exponents by a positive constant leaves every cell unchanged. Thus alpha=2,beta=8 gives exactly the same ODE as alpha=1/2,beta=2. The former falls in 32(a), while the latter falls in 32(b). These incompatible predictions are an immediate source-level warning, not a proof of persistence or of part (b). The 2007 alpha>1 clause cannot be an invariant phase distinction for this frozen hard-cell system.

## Remaining gate

Independent mathematical verification must still establish that the inherited claimed persistence is valid, uses this exact ODE, and is uniform enough to defeat the genericity loophole. The exact catalog record and prior report have not yet been read. No priority verdict is made.
