# Literal primary-source and mathematical gate: PR154 / 30000229 / OWR-829-001

**Verdict: PASS_ENDPOINT_COUNTEREXAMPLE_IN_ORIGINAL_SOURCE_SCOPE.** The original candidate genuinely refutes the endpoint of Stevenson's existence conjecture for piecewise-constant data approximation. No source-scope or mathematical correction is mandatory. This gate does not certify novelty, historical priority, or publication readiness.

Assigned original head: `58bee8514677549ee5a7cd699028a5f3a616c5bc` (the assignment's provenance, not independently re-resolved here). Reviewed original `COUNTEREXAMPLE.md` SHA-256: `dfe3713adae5e5beda588087f3b3e0c4f2c3e809749aee3330730edf8b5cb705`. The supplied literal label is `claimed_solved`, `2/5`; no label or tracker was changed.

## Independence and primary inputs

I first read the actual [Stevenson OWR24/2005 contribution](https://ems.press/content/serial-article-files/45998?nt=1), printed pp.1306-1307 / PDF pp.8-9, and the complete [Cohen-DeVore-Nochetto author preprint](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf), dated April 20, 2011, PDF pp.1-41. Only then did I read the original candidate. `FIRST_ASSESSMENT.md` was written at 2026-10-12 04:50:31 UTC, before opening any historical `independent_review`, curated `source_record`, or prior adjudication.

The OWR contribution does not itself spell out the dual test space or full initial-mesh definition. I closed that attribution gap from the actual [Stevenson preprint 1329](https://www.math.uu.nl/publications/preprints/1329.pdf) explicitly referenced by OWR [8]: Sections 2-3, pp.4-6; the solution class on p.11; the data class and RHS procedure on p.18. Relevant complete pages were rendered and inspected. The historical `independent_review/REVIEW.md`, its exact-control output, and its checker were read afterward only for discrepancy checking. Their verdict was not a premise of this audit.

## Exact claim, assumptions, and quantifiers

For a bounded polygonal domain Omega in R^2, let P0 be a fixed conforming triangulation with at least two triangles and compatible newest-vertex choices. Let P(P0) consist of its newest-vertex-bisection descendants, including the nonconforming partitions allowed in Stevenson Section 3. Define

```
S_P  = {continuous piecewise-affine v subordinate to P : v in H^1_0(Omega)},
S^0_P = {all real piecewise-constant functions subordinate to P},

sigma_n(u) = inf_{P in P(P0), #P <= n} inf_{v in S_P} ||grad(u-v)||_L2,
eta_n(f)   = inf_{P in P(P0), #P <= n} inf_{g in S^0_P} ||f-g||_H^-1.

u in A^s       <=> sup_{n >= #P0} n^s sigma_n(u) < infinity,
f in Abar^s    <=> sup_{n >= #P0} n^s eta_n(f)   < infinity.
```

The weak homogeneous-Dirichlet problem is

```
f(v) = integral_Omega grad u . grad v,  v in H^1_0(Omega),
||f||_H^-1 = sup_{0 != v in H^1_0(Omega)} |f(v)| / ||grad v||_L2.
```

These are Stevenson's actual definitions (preprint pp.4, 6, 11, 18), not an imported abstract-level interpretation. In particular this is the dual of H^1_0 with its gradient norm, rather than the dual of unconstrained H^1. For this fixed Dirichlet problem the Laplacian is an isometry: Cauchy-Schwarz gives the upper bound, and testing with u gives equality.

OWR p.1307 and preprint p.3 conjecture, for each `0 < s <= 1/2`, that `u in A^s` implies `f in Abar^s` for `f=-Delta u`. The implied constants may depend on the fixed data, domain, mesh and s; no uniform coefficient bound on g is required. The approximation mesh for f may be different from that for u. A single valid domain, initial mesh, exponent and u violating this implication defeats the universal conjecture.

The existence claim is weaker than having an s-optimal RHS routine, whose mesh-growth and work bounds are additional requirements (preprint p.18). Both sources allow general H^-1 data and separately explain that L2 data already satisfy the relevant rate by uniform refinement. Thus the counterexample must, and does, use H^-1 data outside L2. Endpoint failure suffices; no failure for all subcritical exponents is asserted.

## What the later preprint does and does not prove

CDN's setup is a polygonal Dirichlet problem with a symmetric, uniformly positive definite coefficient matrix piecewise constant on an initial conforming mesh (p.2). Poisson is its special case A=I. It fixes compatible NVB labels and conforming descendants (pp.6-8); its H^1_0 norm is the gradient norm (p.3). Its data class is different:

```
D(f,T)^2 = sum_{z in N(T)} ||f||_{H^-1(omega_z)}^2,
delta_N(f) = min_{T conforming NVB, #T <= N} D(f,T),
f in B^s <=> sup_N N^s delta_N(f) < infinity.
```

Here the local norms test H^1_0(omega_z); they are not global best P0 approximation errors. Theorem 6.1 (p.24) gives `u in A^s => f in B^s` only for `0<s<1/2`. Section 6.4 (pp.29-31, equation 6.19) supplies the very multiscale u used in this submission and an endpoint obstruction for B^(1/2). Section 6.5 (pp.31-32) is an existence procedure using unavailable minimal meshes/local norms. Practical results impose extra data information: Lp with p>1, or a Lipschitz-curve distribution with Lp density (Sections 7.1, 7.3-7.4, pp.32-38). They do not establish the endpoint implication for arbitrary H^-1 data.

A constant nonzero f already has zero best P0 error on a fixed mesh while D(f,T) is positive. Consequently CDN's endpoint result alone cannot prove the required P0 lower bound. That is the precise bridge the candidate must supply.

## Independent audit of the decisive bridge

For any interior edge e=AB of a conforming shape-regular mesh, on either adjacent triangle K use

```
psi_e = 4 lambda_A lambda_B - 20 lambda_A lambda_B lambda_C.
```

Its element integral is zero because each term integrates to |K|/3. Its trace on e is the same from both triangles; the trace on every other support edge is zero. Extension by zero belongs to H^1_0 even when an endpoint lies on the domain boundary. Its edge integral is 2|e|/3. Affine scaling in two dimensions yields a uniform energy bound depending only on shape regularity.

Given an edge distribution S=sum J_e delta_e, select any subset E and set v=sum_{e in E} J_e |e| psi_e. At most three selected bubbles occur on a triangle, so

```
||grad v||^2 <= 3 C_b sum_{e in E} J_e^2 |e|^2,
<S-g,v> = (2/3) sum_{e in E} J_e^2 |e|^2  for every g in P0(T).
```

Elementwise zero means annihilate arbitrary real coefficients of g. Zero traces prevent other edges from changing the pairing. The signs of jumps cause no cancellation. Dividing proves the candidate's mesh-uniform global H^-1 lower bound; the zero-sum case is trivial. No local-estimator identification enters this reasoning.

## Construction, admissibility, and all-mesh quantifiers

The initial four-triangle square mesh is allowed by Stevenson. Choosing the center as newest vertex makes each boundary side its reference side; the compatibility condition in preprint p.5 is satisfied. The candidate's Q_j are dyadic squares with disjoint interiors. Each center hat vanishes on its support boundary, including any portion on the domain boundary. With 4^j hats of amplitude 4^-j at level j, energy orthogonality gives

```
||grad u||^2 = 4/3,
||grad(u-V_n)||^2 = (4/3) 4^-n,
||f-(-Delta V_n)||_H^-1 = (2/sqrt(3)) 2^-n.
```

The O(j) path-to-square refinement cost and dyadic base-pattern construction are stated in CDN p.29. Their completion/overlay bounds appear in Section 2 (pp.7-8). The required fill cost is O(4^j); a robust direct count is 4(4^j-1) bisections for j pairs of uniform NVB generations. Summing path and fill costs through n is at most 8*4^n before completion. Thus a conforming admissible T_n with V_n in S_Tn and #T_n<=C0*4^n exists. The exact leading constant in the source's informal fill count is unnecessary. Monotonicity between geometric budgets proves u in A^(1/2); the Galerkin error is the same best energy error for Poisson.

Now fix an arbitrary conforming T with #T<=4^n, not just one of the constructed meshes. Its overlay T*=T overlay T_n remains conforming and has at most C1*4^n triangles. Every g in P0(T) stays in P0(T*), while S_n=-Delta V_n is a constant-jump edge distribution on T*.

In each small square at levels j<=n, select the center-to-lower-left segment. Its length is 4^-j/sqrt(2), its jump magnitude is 2sqrt(2), and their product is 2*4^-j. Those segment interiors are disjoint and contain no contribution from another hat. They may have been subdivided in T_n or T*, which the argument explicitly permits.

If m_sigma counts fine edges on a selected segment, distinct segments use distinct edges, hence sum m_sigma<=3#T*<=3C1*4^n. The total absolute jump-length weight is exactly 2n. Two Cauchy-Schwarz steps give

```
sum_{selected fine e} J_e^2 |e|^2
  >= sum_sigma J_sigma^2 |sigma|^2 / m_sigma
  >= (2n)^2 / (3C1*4^n).
```

The bubble bound on T* therefore gives ||S_n-g||>=c*n*2^-n for every original g. Subtracting the exact tail gives, uniformly in T and g,

```
eta_conforming(4^n,f) >= (c*n - 2/sqrt(3)) 2^-n.
```

Normalizing by (4^n)^(1/2) tends to infinity. Uniformity justifies both infima, and constants are independent of n, T and g. The original nonconforming convention cannot restore the rate: complete each such partition with a fixed cardinality factor (Stevenson Theorem 3.2, p.6); its P0 function remains P0 on the completion. A hypothetical O(N^-1/2) nonconforming rate would yield the same rate on conforming meshes at a constant-rescaled budget, contradicting the lower bound.

Finally f is not L2: inside any one small square, a short open portion of its selected diagonal has a nonzero gradient jump, so the distributional Laplacian restricts there to a nonzero line measure. This cannot be represented by a two-dimensional L2 density. Hence the L2 caveat is respected.

## Checks, prior-coverage flags, and exact remaining gap

The new independent `verify_scope.py` passed 214 exact rational assertions on bubble means/traces, jump weights, tails, a valid geometric mesh-cost upper bound, and the nonnegative algebraic identity behind the allocation inequality. These controls supplement the uniform written proof. They do not enumerate all meshes, certify historical receipts, or replace the functional analysis.

Explicit prior coverage encountered: CDN Section 6.4 already supplies this exact multiscale construction and endpoint estimator failure. CDN p.4 also explicitly states that the older L2/P0 data assumptions are not consequences of solution-class membership; that sentence is a priority flag, not by itself the P0 all-mesh proof. The candidate correctly credits the construction and mesh inputs, and its distinctive mathematical step is the zero-mean P0-annihilating test. A full literature/priority audit must determine whether that bridge or its consequence was already established elsewhere. No novelty inference follows from this gate.

**Strongest verified claim:** on the unit square and the stated fixed compatible NVB family, there exists u in A^(1/2) with f=-Delta u in H^-1 outside L2 for which the best global P0 H^-1 error is not O(N^-1/2); along N=4^n it satisfies the displayed uniform lower bound. This is a complete negative answer to the endpoint-inclusive universal conjecture.

**Exact remaining gap:** no mathematical or literal-source gap was found for that claim. Historical novelty, broader priority, and publication readiness remain unassessed. No assertion about all subcritical exponents, unrestricted anisotropic meshes, or optimality of a particular algorithm is verified here.

Primary copyrighted PDFs, complete text extracts, and rendered pages are private cache inputs, excluded by `.gitignore` and explicitly excluded from public redistribution in the manifests. No external individual was contacted and no Git, index, branch, PR, tracker, release or publication state was changed.
