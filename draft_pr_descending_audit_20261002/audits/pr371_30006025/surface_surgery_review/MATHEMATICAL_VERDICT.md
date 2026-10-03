# Independent mathematical verdict, sealed before computation/results

PR 371, frozen head `51fddd150e8da33f4cf17b1a642a0ffd3466bf5d`. This seal follows the complete reading of TURN_1.md through TURN_5.md and the relevant primary source statements/proofs. No candidate program, generated check, state, final result, historical review, root review or sibling conclusion has been read at this point. `SEALS.json` binds the time and SHA-256. This document is immutable after sealing; later computational/post-seal findings go in separate documents.

## Verdict

**Accept the five TURN claims as scoped partial results. No mathematical defect was found in their universal arguments under their stated hypotheses. Do not promote them to a solution or a universal negative answer to OWR Question 4.** In particular, the intrinsic one-face perimeter obstruction and its adaptive sparse repair consequences survive the geometric edge cases. The regular dessin model is a valid smooth realization but fails a specific WP short-curve law. The algebraic-angle claims use valid classical transcendence input and genuinely exclude only their stated palettes/classes.

The strongest geometry independently verified here is:

> Every finite one-face cellular graph with positive embedded piecewise geodesic edges and positive incident sectors in a smooth closed orientable genus-g curvature -1 surface, g>=2, has face perimeter `P>=4pi sqrt(g(g-1))`. Thus source perimeter 12g fails for all g>=12. Any same-edge-correspondence realization has relative total absolute length change at least `delta_g=(pi/3)sqrt(1-1/g)-1`, when this is positive.

Under the conditional uniform simplex length law, uniformly over adaptive repairs changing at most k edges and multiplying each changed length by at most C, their success probability is at most

`min(1, ((C-1)/delta_g)*(k/E)*(1+H_E-H_k))`, `E=6g-3`, `g>=12`.

These follow from credited geometry and elementary deterministic/probability deductions, not from finite computation. Their historical novelty is unverified.

## Reconstruction of the universal arguments

### 1. Analytic and algebraic framed closure

Choose the upward frame at i in the upper half-plane. The diagonal matrix T(l) translates that frame by l; the rotation matrix `R(beta)=[c s;-s c]`, with c=cos(beta/2), s=sin(beta/2), fixes i and rotates its tangent by beta. Its derivative at i has argument beta. Right multiplication therefore follows successive local moves. A closed oriented polygon returns to the original frame, and the PSL2 action on frames is free; its SL2 product is ±I. Trace squared minus 4 is necessary but not sufficient, as parabolics demonstrate. The candidate only uses necessity.

At equal lengths P/N, the fixed 120-degree case reduces to A^N. Cayley-Hamilton with det A=1 gives `tr(A^N)=C_N(tr A)`, with monic integer C_N. The trace is `sqrt(3) cosh(P/(2N))`. For positive algebraic P, Hermite-Lindemann excludes an algebraic exponential, hence an algebraic cosine hyperbolic (the exponential would solve `q^2-2cq+1=0`). Multiplication by nonzero algebraic sqrt(3) preserves transcendence. Thus the closure scalar is nonzero at the barycenter and its analytic restriction is not identically zero. The open simplex is connected, dimension E-1>0 in the stated genus range. Its zero set is null. Finite side-word choices preserve nullness, even if selected adaptively; conditional absolute continuity is sufficient.

For variable simple-polygon angles alpha in (0,2pi), beta=pi-alpha lies in (-pi,pi), so c>0. Algebraic cos(alpha) gives algebraic c and signed s. In the trace's cyclic binary-index expansion, the exponent is `sum epsilon_i l_i/2`. With all l_i>0, its maximum `sum l_i/2` occurs once, at the all-positive index sequence, and has coefficient `product c_i>0`. Grouping coincident exponents cannot remove it. All exponents are algebraic when all lengths are. Including the proposed constant ±2 at exponent zero leaves a nontrivial relation, forbidden by Lindemann-Weierstrass linear independence over the algebraic numbers. For a fixed continuous profile, the equal-length specialization instead gives a Laurent polynomial in a transcendental q with a surviving highest term. Countably many algebraic-cosine profiles give a countable union of null sets. Freely varying real profiles are uncountable and cannot be excluded by this reasoning.

This directly reconstructs TURN 1 and 2. Half-angle signs, concave corners, straight alpha=pi, repeated side lengths, repeated signed sums and reversal of orientation do not break the argument. Positive lengths and strict angle endpoints do matter.

### 2. Smooth regular-polygon construction and its curve law

Euler and trivalence give V=4g-2, E=6g-3, N=12g-6. Bisect a regular polygon through its center and each edge midpoint. The resulting 2N triangles have angles pi/N, pi/3, pi/2. The hyperbolic right-triangle cosine law yields `cosh(l_N/2)=2cos(pi/N)/sqrt(3)`, with real positive l_N exactly when N>6. Side gluing from the orientable map pairs equal lengths and produces the topological map; every cubic vertex has total angle 3*(2pi/3)=2pi. The same is true at midpoints and center. There are no cone points. Its area is `(N-2)pi-N*(2pi/3)=4pi(g-1)`.

The clean dessin has N edges (twice the original E), degrees 2 and 3, and one face of dessin degree N. This face degree counts half the subdivided boundary edge occurrences; confusing it with 2N would give the wrong triangle group. All cycles of the order-2, order-3 and order-N generators have full respective length. A point stabilizer in the transitive degree-N representation consequently meets no conjugate of a nontrivial power of an elliptic vertex generator. The triangle group's finite-order elements are conjugate to such powers, giving a torsion-free subgroup. Equivalently, the local angle proof already shows a smooth quotient. The group is orientation preserving, and its orbifold area is `2pi*(1-1/2-1/3-1/N)`; area division gives index N.

Using Philippe's exact p=3 corollary, every hyperbolic element in the surface subgroup has translation length at least `2 arcosh(2cos^2(pi/N)-1/2)`. This is a lower bound, not a claimed attained surface systole. For N>=18, monotonicity of cosine on (0,pi) and comparison with N=12 give argument greater than `(1+sqrt(3))/2>4/3`. The positive Taylor tail gives `cosh(1/2)<=53/47<4/3`, so every surface systole exceeds one. The interval [1/2,1] count is identically zero.

WP primitive-curve counts on that interval converge to a Poisson variable of positive mean `mu=int_(1/2)^1 (cosh t-1)/t dt`. Weak convergence of integer-valued counts implies convergence of their zero mass (evaluate the CDF at 1/2). Total variation from a point mass at zero is exactly 1 minus that mass. Since `mu>3/16` and `1-e^(-x)>x/(1+x)` for x>0, the limit exceeds 3/19. This excludes this fixed geometry under **every** input map distribution. Finite support alone would not exclude an asymptotic approximation. Marking recovery, CFF copy multiplicity and pushforward weights are correctly separated from the WP measure.

### 3. Intrinsic cut disk and perimeter obstruction

Cut along the graph and retain every local sector as a separate boundary occurrence. Cellular one-face topology says the cut surface is a disk, rather than merely asserting that the developed boundary word is planar. Every original edge interior has exactly two sides, including a bridge. Subdividing finitely many bends creates ordinary sector corners and leaves total graph length unchanged. The graph is a finite union of arcs and has area zero. Therefore disk area equals closed-surface area and disk boundary length is twice graph total length.

At vertices of the smooth ambient surface, the incident sector angles are positive and sum to 2pi. A leaf has one sector of angle 2pi, intrinsically a disk with a slit terminating at the tip. Developing its two boundary rays into the plane makes them coincide; this does not identify them in the cut metric. Every interior point retains curvature -1, with **no interior cone point**. Reentrant angles, repeated boundary vertices and a noninjective development therefore do not violate Izmestiev's disk assumptions. A planar simple-polygon proof would be insufficient; the candidate instead cites the intrinsic theorem correctly.

Substitute `A=4pi(g-1)` into `P^2>=4pi A+A^2` to obtain `P^2>=16pi^2 g(g-1)`. At P=12g the condition is `pi^2(g-1)<=9g`. At g=12 it fails already using pi>157/50; the difference increases with g because pi^2>9. At g=11 it holds using pi<22/7, and monotonicity settles all smaller g>=2. This is a threshold for exclusion by this bound, not an existence threshold. Both square-root sides are nonnegative, so no sign reversal is hidden.

Write L=sum input=6g and L'=sum output. Then `L'/L>=s_g` and `sum differences>=L delta_g`. The triangle inequality gives total absolute change; the ratio L'/L is a weighted mean of positive edge ratios, giving a lower bound on their maximum. Finally, total absolute change is at most E times maximum absolute change. Uniform scaling attains the elementary deterministic inequalities, but geometric realizability is not inferred. Negative delta gives vacuous bounds. The claimed positive limit is `pi/3-1`, and the g>=100 rational comparison `s_g>26/25` is correct.

### 4. Adaptive sparse repair

The normalized exponential change of variables has Jacobian S^(E-1), so S and X are independent and E[S]=E. Ordered exponentials have mean spacings 1/E,...,1 by memorylessness. Thus their jth largest mean is H_E-H_(j-1), and the mean top-k sum is k*(1+H_E-H_k). It equals S times the top-k sum of X. Independence proves `E[T]=(k/E)*(1+H_E-H_k)`. This also handles k=E (T=1), k=0 (T=0), and E=1.

For any adaptively chosen changed-edge set I, `sum output-input<= (C-1)*L*sum_I X<= (C-1)*L*T`. This is pointwise and makes no independent-selection assumption. Success implies T>=delta/(C-1); Markov gives the displayed bound. The necessary event is measurable even if geometric existence is not, supporting the outer-probability wording. At C=1 or k=0 all changes are nonpositive, so positive delta forbids success. The harmonic sum is bounded by log(E/k), and r*(1+log(1/r)) tends to zero. The limit is uniform in all allowed rules because the same bound controls every rule. With random maximum C(X), the pointwise inequality gives C>=1+delta/T; Jensen on positive T supplies the expected stretch bound, including infinite expectation.

## Falsification attempts and boundaries

| Attempt | Outcome before code inspection |
|---|---|
| Treat boundary angle below pi as forbidden positive curvature | Rejected: reference defect is pi-alpha at boundary, but Theorem 1 restricts interior cones only. |
| Use full-turn leaf or reentrant boundary to break disk applicability | Does not break it: positive finite intrinsic sectors are allowed, including 2pi. |
| Use zero sector or coincident tangent branches | Outside stated positive-sector class; such a collapsed sector need not be a cone disk. |
| Invoke planar inequality on overlapping development | Invalid proof route. Candidate cites the intrinsic theorem, whose scope includes development overlap. |
| Let a graph quotient preserve continuum distances | Unsupported: identification shortcuts and filled-face paths are additional. Candidate draws no such conclusion. |
| Apply disk theorem to disjoint components as one disk | Invalid as stated. For components individually satisfying it, componentwise sums give a coarser total bound; one-face argument itself has one disk. |
| Allow negative cone defects on glued graph vertices | Potential escape: closed area becomes `4pi(g-1)+sum defects`, so the smooth-area substitution is unavailable. |
| Change curvature to -kappa | Bound rescales to `P>=4pi sqrt(g(g-1))/sqrt(kappa)`; fixed units are essential. |
| Change to several faces | Sum component inequalities retains a global lower bound when all face interiors qualify, but no unproved equivalence with a one-face construction is asserted. |
| Claim perimeter feasibility for g<=11 | Rejected: necessary inequality alone supplies no realization. |
| Claim sparse bound proves impossibility without a cap | Rejected: one edge can supply the necessary length mass if unbounded stretch is allowed. Geometric sufficiency is still unknown. |
| Claim thick-model count disagreement rules out arbitrary GH coupling | Rejected: the candidate explicitly avoids that claim. |

Local Chapuy surgery provides another exact boundary: merging k distinct vertices while conserving face geometry decreases V by k-1 and total cone defect by 2pi(k-1), exactly matching Euler genus change. Starting with k smooth vertices gives total glued angle 2pi*k. Its reverse cannot divide one smooth angle into k positive smooth angles. This blocks a pure sector-conserving smooth local recipe, not all global geometric adaptations. Allowing new faces, changed area or unrestricted cone defects changes the mechanism.

For Euclidean cone disk of radial radius R and total cone angle Theta>0, `A=Theta R^2/2` and `P=Theta R`. Thus `P^2/(4pi A)=Theta/(2pi)`. Positive interior defect (Theta<2pi) gives an explicit failure of the unmodified theorem, smooth Theta=2pi gives equality, and negative defect Theta>2pi gives strict inequality. A hyperbolic radial disk has `A=Theta(cosh R-1)`, `P=Theta sinh R`; the same computation shows the sign of `P^2-4pi A-A^2` equals the sign of Theta-2pi. These checkable constructions identify exactly why the interior hypothesis cannot be replaced by a statement about ambient face curvature alone.

## Source credit, provenance and exact remaining gap

Established external inputs are Chapuy/CFF combinatorial correspondences; classical Hermite-Lindemann and Lindemann-Weierstrass (Delaygue introductory Theorems A/C); uniform dessin Fuchsian representation (Girondo-Gonzalez-Diez-Hidalgo, Section 2 and Lemma 1); Philippe's orientation-preserving triangle-group systole classification; Mirzakhani-Petri WP Poisson limit; the BGL conditional simplex law; and Izmestiev's intrinsic disk inequality (earlier Alexandrov/Bol/Weil inputs explicitly credited). Classification/transcendence/Poisson/isoperimetric theorems are used as established theorems, not re-proved by this audit or by checker enumeration.

Relevant source statements, source proofs of the local constructions and full candidate proofs were read. The 35-page Philippe classification and MP asymptotic theorem are external established inputs, not independently rederived in their entirety. Independently acquired PDF hashes for OWR, Izmestiev, CFF, Janson-Louf, MP, Philippe, uniform dessins, Delaygue and arXiv Chapuy2010 match the candidate's routed hashes where applicable. BGL's journal download is dynamically stamped and its bytes differ from the author's dated copy; the theorem, exact law, Sections 1.2/6, DOI and pagination agree. The originally acquired BGL v1 and alternate Chapuy author PDF are retained as alternate versions, not silently represented as hash matches.

The remaining discovery gap is a mathematically specified geometric tree/map-to-surface construction, or asymptotic coupling, with a controlled random hyperbolic polygon or surface law compatible with WP random surfaces. The TURN packet supplies neither a sufficient realization theorem nor a density/Jacobian or probability comparison for a viable deformed construction. Rejecting direct constructions does not close that gap. Original Question 4 remains unresolved **by these results**; no assertion is made that no unrelated later solution exists.
