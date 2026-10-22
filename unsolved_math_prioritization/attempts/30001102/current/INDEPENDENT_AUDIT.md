# Independent mathematical audit: rational mixed-integer bipartite optimization

Date: 9 October 2026 UTC.

## Disposition and exact scope

**Accepted for the stated finite binary-input target.** The frozen candidate proves polynomial-time exact linear optimization, including an improving integral recession witness in the unbounded case, and polynomial-time strong separation and exact convex-hull membership. No fatal or substantive mathematical gap was found.

The reviewed candidate is `authored/CANDIDATE_PROOF.md`, 19,460 bytes, SHA256 `8b492c49dbe0b7bd337ea183a51d44a345613c69ff38c6c81d613d7c0b9e167a`. Its original bytes were not edited. A separate one-sentence clarification patch narrows an ancillary generalization in Section 3; the exact target theorem does not depend on that generalization.

The target has explicitly given finite bipartition classes, rational binary demands, unrestricted-sign variables, an arbitrary selected subset of integer coordinates, and explicitly encoded rational objectives or query vectors. Dimension and denominators are variable. This audit does not establish a polynomial-size formulation, a facet characterization, the separate subtree-hull conjecture, a strongly polynomial overall algorithm, or novelty. It does not certify a production implementation of the invoked optimization algorithms.

## 1. Source identification and boundaries

The actual formulation and Problem 1 were checked in Michele Conforti, *Combinatorial Mixed-Integer Programming*, Oberwolfach Report 51/2008, printed pp. 2904–2905. The model is exactly the unrestricted-sign system used by the candidate. The report's Conjecture 2 is the different assertion about intersection of subtree hulls. Its informal optimization/membership equivalence is not used as a substitute for the candidate's oracle argument.

Primary source: [Oberwolfach Report 51/2008](https://ems.press/content/serial-article-files/46195).

The inspected [network-formulation manuscript](https://www.math.uwaterloo.ca/~bico/bellairs/network.pdf) distinguishes mixed network flows, with incidence columns having two nonzeros, from the row-sparse network-dual class. Its Corollary 8 has polynomial dependence on the numerical denominator, which is insufficient for the target's binary encoding. Neither that hardness result nor that complexity bound refutes or proves the present theorem.

The [projected-formulation manuscript](https://personal.lse.ac.uk/Zambelli/papers/mix-tree.pdf), November 2009 revision, uses the same free-sign model and describes a denominator-dependent formulation. Its introductory general-complexity question and its special-set results were distinguished. These bounded source checks are not a current worldwide openness or originality certificate.

## 2. Feasibility, sign change, and unboundedness

The diagonal sign map on one bipartition is integral, invertible, and preserves the selected-coordinate integrality condition in both directions. A row becomes a difference inequality with coefficient pattern `(1,-1)`; the objective changes by the same diagonal map.

The initial feasibility claim is valid even for negative demands: assigning every original coordinate the integer `M=max(0,max ceil(b_e))` satisfies every edge. The input representation of M is polynomial. Empty edge sets and isolated vertices do not require any exceptional feasibility assumption.

The recession cone is obtained by replacing demands by zero. If the continuous objective is unbounded below, the rational feasibility system consisting of recession inequalities and `a^T r<=-1` has a polynomial-bit rational solution. Multiplying by the product or least common multiple of its coordinate denominators produces an integral improving ray of polynomial bit length. Starting from the integral feasible point, every nonnegative integer multiple remains mixed-feasible. This proves the nontrivial direction of equivalence of continuous and mixed unboundedness; the reverse direction follows from containment.

When finite, rational LP returns a polynomial-bit optimum even though the relaxation has lineality. The candidate never assumes that the unanchored relaxation has a vertex. Zero objectives, no integer coordinates, all integer coordinates, disconnected graphs, and the zero-dimensional case are covered.

## 3. Proximity and attainment

The signed threshold decomposition is correct. Positive thresholds contribute nested positive indicators; negative thresholds contribute nested negative indicators. For every ordered coordinate pair, all nonzero layer differences have the sign of the total coordinate difference. Tied coordinates therefore have identical entries in every layer. In the opposite-sign case, the positive and negative layers still have the same direction of contribution to the difference. There are at most n layers in total, rather than n of each sign.

Fix a mixed-feasible z and put d=z-y*. In each constraint row, the change from y* to y*+lambda r has the same sign as the full change from y* to z and magnitude no larger. Hence the new row value lies between two feasible row values. This is a rowwise argument; a common interpolation coefficient across all rows is unnecessary. LP optimality and lambda>0 imply a^T r>=0.

For lambda>=1, subtraction of the integral layer r from z likewise leaves every row between its values at the two endpoints. The coordinate domination inequality implies that subtraction cannot cross y* in any affected coordinate. Each affected coordinate moves by one, at least one moves, and the L1 distance strictly decreases. Selected integer coordinates remain integral, including when the layer has negative entries. Cost cannot increase. The threshold lambda=1 is permitted; removing a layer with lambda<1 would not be justified.

Attainment is not assumed circularly. T is closed. Its intersection with a closed objective sublevel set is closed and nonempty. The L1-distance minimum exists after restricting to a closed ball through a known feasible point; points outside that ball cannot improve the distance. A distance minimizer cannot have any layer coefficient at least one. Summing fewer than or equal to n coefficients, each strictly less than one, gives the strict sup-norm bound n.

Thus every mixed-feasible point has a no-more-expensive representative in one fixed compact box. The closed mixed subset of that box has an objective minimizer, which is globally optimal. Applying the same distance argument to an optimal sublevel set supplies a global optimum with the strict proximity bound if desired. Arbitrarily small fractional spacings and arbitrarily large numerical denominators do not change this argument.

### Nonblocking clarification

The first paragraph of Section 3 says the argument works for any nonempty system of difference inequalities. For this broader remark, both mixed feasibility and a finite LP optimum are required. Mere continuous feasibility is insufficient: the two inequalities imposing `y1-y2=1/2`, with both coordinates integral, have an empty mixed set. The candidate's actual bipartite model is mixed-feasible by Section 2, and Section 3 is already within the finite-LP-optimum case. The separate patch makes those conditions explicit. This counterexample does not invalidate the target theorem.

## 4. Finite assignments and exact partial minimization

For each selected integer coordinate, the interval endpoints have polynomial bit length, and its width is at most 2n. Enumerating its thresholds costs O(n), regardless of the absolute location of the interval. The algorithm does not enumerate the Cartesian product of intervals.

The projection onto the fixed integer coordinates is exactly the rounded integer-integer edge system. Sufficiency requires the original covering orientation: after converting fixed coordinates back, choose a common sufficiently large integer for all remaining coordinates. It simultaneously satisfies integer-continuous and continuous-continuous edges. There are no hidden path-induced upper bounds in this model. A corresponding projection assertion for arbitrary directed difference systems would need additional work; the candidate does not use one.

Every feasible slice has a finite attained LP minimum because it is nonempty and its cost is bounded below by the unsliced LP optimum. A polynomial-size rational LP describes each slice. An exact LP solver returns a polynomial-bit value and an optimizing completion; uniqueness and pointedness are not required. Uniformity follows because every assignment has polynomial-length coordinates, and the number and coefficient sizes of slice constraints are uniformly polynomial in the original input and objective length.

Coordinatewise minimum and maximum preserve each difference inequality. Minimizing completions for two assignments can therefore be met and joined to give feasible completions of the met and joined assignments. The coordinatewise modular identity for a linear objective proves the submodular inequality, with its direction as stated. No sign restriction on objective coefficients is needed in this step. The value function is used only on its finite-valued domain; it is never supplied as an uncontrolled infinity-valued oracle.

## 5. Ring-family interface and complexity

The threshold encoding is bijective between bounded integer assignments and prefix sets. Downward chain arcs enforce prefixes. The base condition on each integer-integer edge is indispensable because the lower endpoint of a coordinate has no corresponding threshold node. Each higher threshold produces the correctly oriented implication from the v-coordinate to the u-coordinate with shift ceil(b_uv).

Targets below the represented interval are tautologies. Targets above it forbid the source threshold. Forced nodes, forbidden nodes, and ordinary implications describe the exact domain. Closure of forced nodes gives its minimum; closure after adding one node gives its minimum containing that node, unless a forbidden node is reached. Forced nodes reaching a forbidden node certify emptiness. The proven proximity lemma guarantees that this does not happen for the actual constructed domain.

There are at most 2n|I| ground elements and O(n^2+n|E|) arcs. Closure uses finite graph reachability. The smallest member, infeasible nodes, and equal containing-member closures permit the standard deletion and identification steps before minimization. In particular, absent nodes and a nonempty forced minimum do not violate the imported algorithm's interface.

The actual [Schrijver manuscript](https://homepages.cwi.nl/~lex/files/minsubm6.pdf), especially Sections 3–6, was inspected. Section 6 requires exactly these minimum-member data and a submodular value oracle. It reduces ring-family minimization to ordinary submodular minimization. This established algorithm is imported; the finite checker is not its implementation.

Polynomial arithmetic-operation count alone would not generally prove binary complexity. Here all oracle values have a uniform polynomial bit bound. In the inspected algorithm, greedy vectors have polynomial-size entries; auxiliary linear systems have polynomial dimension and polynomial-size entries. Their solutions consequently have polynomial size. Redistribution and clipping of convex-combination weights, after cancelling the clipping factor, are rational linear transformations of the previous weights with polynomial-size coefficients. Affine-dependence reductions have the same property. Tracking one common denominator across polynomially many such transformations gives polynomial bit growth, rather than repeated unconstrained squaring. Ring reduction adds only polynomially many values. Hence the imported procedure with the exact LP oracle is a polynomial-bit algorithm.

The output assignment is decoded from the minimizing prefix set. One final exact slice LP reconstructs a mixed-feasible optimum. The inverse sign change gives the required original-coordinate solution and objective value.

## 6. Uniform bounded core

The recession cone's lineality consists exactly of vectors constant on each connected component. Any objective bounded below must vanish on this subspace. Anchoring one coordinate in each component therefore preserves the continuous optimal value and produces a nonempty pointed polyhedron. The anchor is only an LP device; no potentially nonintegral translation of a mixed solution is used.

At an anchored vertex, tight difference rows together with anchors span the full coordinate space. The tight graph must therefore connect each original component to its anchor. Selecting spanning trees shows that every coordinate is a sum of at most n-1 signed edge demands. Consequently an LP optimum exists with sup-norm at most nB, where B bounds all absolute demands. Proximity gives a mixed optimum in the box of radius H=nB+n.

This existence argument also applies to a real separating objective: rationality of the objective is needed for algorithmic input encoding, but not for the vertex-existence or proximity arguments. Thus the later separation argument does not smuggle in an unsupported rationality assumption on a hypothetical separator.

## 7. The actual convex hull and facet encoding

The bounded mixed set has finitely many integer-coordinate assignments, even though their number may be exponential or larger as a numerical quantity. For each assignment, its continuous slice within the box is a bounded rational polytope. Their finite convex hull K is a rational polytope. This finite-union construction is existential and is not executed by the polynomial algorithm.

For every recession vector, the signed threshold decomposition uses only integral recession indicators. For an integral recession indicator d and a mixed-feasible point z, interpolation between z+kd and z+(k+1)d puts z+td in conv(T) for every real t>=0. Applying this to each term in a finite convex combination extends the property to every point of conv(T). Finite sums of the indicators establish K+R contained in conv(T), with no closure operation added.

K+R is a closed rational polyhedron. A point of T outside it would admit a strict separating objective nonnegative on R. Such an objective is bounded below on the continuous polyhedron; the uniform bounded-core argument gives the same minimum on T and K. This contradicts strict separation. Therefore conv(T)=K+R exactly. The argument proves closedness rather than assuming that a general convex hull of a closed set is closed.

For the encoding bound, the difference rows, coordinate-fixing rows, and box rows form a totally unimodular matrix. Every slice vertex lies on the grid (1/k)Z^n, where k is the least common multiple of demand denominators, and has norm at most H. The logarithm of k is bounded by the sum of input denominator lengths; no residue enumeration is used.

All recession generators have entries in {-1,0,1}. Homogenizing points and rays and scaling each point generator by k gives integer homogeneous generators bounded in magnitude by k(H+1). The original hull contains a translated positive orthant and is full-dimensional. Its facet face has n linearly independent homogeneous generators. Cofactors of the corresponding rank-n matrix yield a nonzero integral normal, with each coefficient bounded by n![k(H+1)]^n. Points on the facet, recession generators, and both directions of lineality can all be used; lineality does not impair the rank argument.

The resulting coefficient bit bound is O(n(log n+log k+log(H+1))); multiplying by n+1 coefficients is polynomial. The displayed phi in the candidate safely dominates it, including sign/constant overhead. If E is empty and the hull is the whole space, phi also exceeds the conventional minimum encoding bound; no facets need be generated. The argument bounds the size of each inequality, not the number of inequalities.

## 8. Exact optimization, separation, and membership

The actual [GLS book available from Grötschel's author page](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf) was retrieved and inspected. The inspected edition is 1988: Definitions 6.2.1–6.2.2 and Theorem 6.4.9 with its proof, printed pp. 162–163 and 179–180. The candidate cites the later edition; the verified earlier statement already supplies the required result.

The strong optimization interface permits an exact optimizing point, not necessarily a vertex, and covers unbounded polyhedra using improving recession directions. A ray can be scaled further if a chosen normalization is required. The theorem converts strong optimization to strong separation for a rational polyhedron with a supplied facet-complexity bound.

All those hypotheses have been checked here: exact closed hull, rational polyhedrality, computable polynomial phi, polynomial-bit rational optimization outputs, and improving recession witnesses. Composing the oracle reduction with the candidate's algorithm has polynomial total cost in the original data and query lengths. Strong separation either certifies actual membership or gives a strict separating inequality. Boundary points are decided exactly; this is not a weak-membership approximation.

## 9. Independent diagnostics and adversarial controls

The frozen original checker was copied byte-for-byte to a read-only snapshot and rerun in normal, `-O`, and `-OO` modes. Each run reproduced its reported counts: 24 instances, 5,380 slice LPs, 65,014 submodular pairs, 1,723 removal checks, 1,000 threshold vectors, 1,692 ring checks, and nine negative controls.

A separately authored exact-Fraction checker was also run in all three modes. It covers exhaustive signed/tied four-coordinate threshold vectors, very large rational encodings, zero-cost and isolated-coordinate cases, all integrality subsets on small stars, independently enumerated slice vertices, all-subset ring recognition including empty families, the actual closure-based ring reduction on a nonlinear slice value, exact near-boundary examples, and explicit unbounded rays. Counts and execution identities are recorded in the accompanying receipts.

The independent checks reject actual decomposition and ring-function mutations: positive-only layers, reversed negative layers, missing base conditions, missing prefix chains, and reversed implication shifts. Additional exact counterexample controls reject floor rounding, omitted sign changes, subunit removal, replacing the hull with the relaxation, and replacing the hull with the mixed set itself. An explicit exception guard remains active in optimized Python modes.

All independent executions require effective UID different from zero and recorded UID 1000. Each attempts to append to both read-only frozen inputs and to create a new file in their read-only directory; all three operations must raise PermissionError. Successful reads and hash verification precede these probes. No root-mode inference from permission bits is used.

These tests are finite diagnostics. They do not establish polynomial complexity, replace the mathematical proof, independently implement SFM or GLS separation, or certify every conceivable software implementation.

## 10. Final acceptance boundary

The exact target theorem is accepted by this independent audit, on the frozen proof hash above. The separate scope-clarification patch is recommended for precision about a broader remark, and the direct 1988 GLS source can be added to citations without changing any mathematical argument. No additional substantive approach was initiated, and the first-route budget remains 1/5.

Standard imported results are rational LP bit complexity, polynomial submodular minimization with its ring-family interface, elementary rational polyhedral recession/separation facts, and exact GLS optimization/separation. The application steps specific to this target have been independently checked above. No GitHub or queue action is part of this audit. Original proof, checker, sources, and manifest-listed inputs were preserved.
