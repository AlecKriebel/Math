# Independent adversarial audit: toric movable cycle cones

Problem ID 30003592; catalogue code OWR-15586-003; audit date 4 October 2026.

## Verdict

**PASS as an explicitly unsolved research checkpoint.** No mathematical defect requiring correction was found in the stated partial results. There is one minor, non-blocking projectivization-notation ambiguity, recorded in CORRECTIONS.md. This verdict does not mean that the universal question has been solved, that the work is novel, or that the packet has received journal peer review.

The audited object is exactly the 12-file submission with tree SHA-256

`ca255f65291a748c56f579a4ebac4a12c420feed5f27c71d449d217d58c83026`

and archive SHA-256

`f254cee4b067f6e7b7aa95599cb6e22776e7182fc528705665345c3a22ff5603`.

All input hashes were independently bound before mathematical reading. The ZIP contains exactly the same 12 files, with no extra members. The input files were not edited. This audit is a separate authored-only supplement; its integrity manifest is AUDIT_SHA256SUMS.json.

The source problem and the disclosed smooth-projective complex scope are correctly distinguished. All five proposed approaches remain unsuccessful as universal solutions. The notebook's completion estimate of zero is consistent with its stated meaning: no yes/no resolution, rather than a measured percentage of mathematical work.

## 1. Source, scope, and literature gate

The original Problem 1(3), printed page 2633 of OWR 43/2017, was independently retrieved and inspected both as text and as a rendered page. It asks for rational polyhedrality of a closed numerical cone of torus-moving subvarieties. Projectivity and a base field are not stated in that local sentence. The surrounding report discusses projective cycle theory and records the divisor and curve cases as known. The notebook clearly narrows its deductions to smooth projective varieties over C, and does not use that narrowing to claim success for the broader wording. This is an appropriate scope disclaimer. [OWR](https://doi.org/10.4171/OWR/2017/43)

The 2025 Mori-dream-space theorem was checked in the publisher's version of record, including the definitions surrounding Theorem 1.1. Its polyhedral cones consist of divisors, and its moving curves still have dimension one. Its index is not the dimension of arbitrary cycles. The stated publication date, 27 February 2025, is correct. Payne's paper likewise cannot be read as a theorem about all higher-dimensional movable-cycle cones. [BDPSS](https://link.springer.com/article/10.1007/s00209-025-03699-6), [Payne](https://web.ma.utexas.edu/users/sampayne/pdf/Stable-base-loci-toric-varieties.pdf)

The newer realizability results require an irreducible subvariety, up to scaling, and do not identify that generally nonconvex set with the closed convex movable cone. Definition 1.5 and Theorems 1.6 and 1.8 were checked in version 2, dated 14 June 2025. [HHMWW](https://arxiv.org/html/2505.08881v2)

The Fulger–Lehmann family definitions, nef-intersection and dominant-pushforward lemmas, birational basepoint-free description, and scroll formulas have the needed hypotheses here. In particular, the projective morphism in the product argument is dominant, the hyperplane class is nef, and the birational formula retains its closure and its quantification over all models. Example 7.4 already contains the scroll witness. The displayed author-page erratum concerns symmetrized M_0,7 calculations, which are not used. The Nef/BPF separation in Positive cones, Example 5.12, supports the notebook's caution and no stronger Mov conclusion. [Zariski decompositions](https://sites.bc.edu/lehmann/wp-content/uploads/sites/36/2019/12/zardecomcycles.pdf), [Positive cones](https://content.algebraicgeometry.nl/2017-1/2017-1-001.pdf), [author research page](https://sites.bc.edu/lehmann/research/)

Seven scholarly PDFs were independently downloaded for private examination and their digests agreed with SOURCE_MANIFEST.json. No PDF, extracted full text, or rendered source page is part of this audit deliverable. A bounded current literature search found no verified full resolution; neither this search nor the author's search establishes completeness of the literature.

Repository-history and queue assertions in SOURCE_GATE.md were not independently repeated against remote private state. They are provenance assertions, not dependencies of the mathematical conclusions. No remote writes or external correspondence were performed by this audit.

## 2. Definitions and the torus-moving interpretation

The dimension/codimension bookkeeping is sound: on a smooth projective n-fold, N^d is dual to N_d, and cap product identifies it with N_{n-d}. The notebook does not confuse the effective complementary-cycle dual with a movable cone outside the curve case.

For an integral Z meeting the torus, the universal translate incidence is the image of T x Z under (t,z) -> (t,tz) in T x X. It is isomorphic to T x Z, proper and flat over T, with irreducible total space. Evaluation dominates X because its image contains T. Connectedness of T gives a constant numerical class. Hence each such Z supplies a legitimate strongly movable family in the terminology used by the notebook.

For the converse at the cone level, dominance of every universal component implies that a general fiber has no component lying in the finite toric boundary. The dimension estimate is elementary: the inverse image of a boundary Cartier divisor is a proper divisor on each dominating universal component, and its general fiber has dimension at most d-1. After the usual flat restriction, every integral component of a general d-cycle therefore meets T. Decomposing that cycle and taking nonnegative sums and limits gives the stated equality of cones. This explains why a chosen invariant representative need not itself move.

Neither this argument nor the definition requires the evaluation map to be flat. That stronger condition belongs to the basepoint-free construction. The distinction is necessary in the scroll example below.

## 3. Approach 1: degeneration and the convex warning

The F_1 arithmetic is correct. Against E and F, aE+bF has pairings b-a and a. Movability forces both to be nonnegative. The ruling fibers and strict transforms of lines avoiding the blown-up point realize the two boundary classes F and E+F in dominating families, so the cone is exactly their nonnegative span. Here "cover" is understood as dominance, as in the notebook's definition: the subfamily of lines avoiding the point need not pass through every point of E.

Toric degeneration establishes finite generation of the effective cone by invariant orbit closures; it does not establish finite generation of its movable subcone. The convex control is valid. For K={x,y,z >= 0: y^2 <= xz}, the functional t^2 x-2ty+z is nonnegative for every t>=0. Its zero set in K is the ray through (1,t,t^2). Distinct t produce distinct exposed rays, so K is nonpolyhedral although it lies in a polyhedral orthant. This is a convex diagnostic only.

## 4. Approach 2: boundary outer bound

On a smooth projective toric variety, every invariant prime divisor is Cartier. For a covering family, a general fiber has no component in a fixed such divisor, so the divisor intersection is an effective cycle or zero. Passage to sums and limits is justified because the intersection map is linear and continuous and the effective cone is closed.

Every effective divisor class is a nonnegative combination of invariant prime-divisor classes. Testing those finitely many classes therefore tests all effective divisors. The effective cycle cones in the two relevant dimensions are rational polyhedral by toric degeneration; the preimages under rational linear intersection maps and their finite intersection remain rational polyhedral. This proves precisely Mov_d(X) contained in P_d(X). No step proves the converse for general X. Repeating the test after the first intersection would require fresh movability, which is not supplied by effectivity alone.

The all-real cone reasoning is valid independently of the author's finite grid. The new checker provides an exact change-of-coordinates certificate for the specific scroll envelope, rather than inferring a universal inequality from sampling.

## 5. The fourfold, rebuilt independently

Set X=P_{P^1}(O^2 plus O(1)^2) using one-dimensional quotients. It is smooth, projective, toric, and four-dimensional. With f the point pullback and xi the tautological divisor, the projective-bundle relation is xi^2(xi-f)^2=0, hence xi^4=2xi^3 f because f^2=0. Also the integral of xi^3 f is one. Thus e=xi^2 and q=xi f have Gram matrix [[2,1],[1,0]].

The fan has two base rays and four relative rays. A cone uses at most one base ray and fewer than all four relative rays. Independent enumeration gives 14 codimension-two orbit closures and 16 codimension-three orbit closures. Their distinct numerical classes are respectively

- (e, e-q, e-2q, q), and
- (xi^3-xi^2 f, xi^3-2xi^2 f, xi^2 f).

The effective surface and curve cones consequently have the stated extremal rays. For alpha=ae+bq, the effective constraints are a>=0 and b+2a>=0. Multiplication by f, xi, and xi-f yields the additional strongest condition b+a>=0. The change of coordinates s=a, t=a+b identifies their combined cone with s,t>=0; its rays are e-q and q. This proves the outer-envelope formula for all real coefficients.

The two lower-bound families are genuine:

1. A plane in a P^3 fiber varies in the relative Grassmannian and the base P^1. Its class is q and its incidence dominates X.
2. Let S parametrize one-dimensional quotients of each of A and B, where E=(A tensor O) plus (B tensor O(1)). Over S x P^1, the two universal quotient line bundles give a rank-two quotient of E. Projectivizing it gives a proper flat family over S; every fiber is the integral surface P(O plus O(1)). Its total space is an irreducible projective bundle. The kernel has one degree-zero and one degree-one summand, so the fiber class is xi(xi-f)=e-q.

At a point of X, write the quotient functional as its A and B components. Each nonzero component fixes the required quotient line; a zero component allows an arbitrary quotient line. Therefore evaluation is surjective. The independent finite-field incidence controls test every such point, including both zero-component edge cases; the argument over C does not depend on those finite tests.

This also clarifies why the family is not basepoint free: evaluation has zero-dimensional fibers where both components are nonzero and a one-dimensional fiber on either zero-component locus. The evaluation is not flat. Every member in the e-q family meets the fixed subscroll P(O^2), of class e-2q, in a curve; this is an excess intersection, so dominance does not force a nonnegative surface pairing.

It follows that Mov_2(X)=cone(e-q,q). Direct integration gives (e-q)(e-2q)=-1, while the effective-cone dual is cone(e,q). This is a valid counterexample to the naive higher-cycle duality and to the fixed-model complete-intersection equality, not to rational polyhedrality. The independent specialization of the published Harder–Narasimhan formula has epsilon_1=-2 and maximal slope 1, giving sigma_2=-1, in agreement with the direct construction.

## 6. Approach 3: fixed-model and birational constructions

Multilinear expansion of products of finitely generated nef divisor classes gives a finite set of monomial generators for the fixed-model complete-intersection cone. Approximating nef divisors by ample rational divisors and taking general complete intersections puts that cone inside Mov. The argument uses the closed-cone definition and does not assert that every boundary class has one actual complete-intersection representative.

For the scroll, xi and f are globally generated. Testing a fiber line and a section associated to an O quotient shows that a nef divisor axi+bf must satisfy a,b>=0. Its codimension-two monomials are e,q,0. Thus e-q is genuinely missed.

The birational BPF formula is correctly used only as a reduction. Flattening a family's evaluation may require a model dependent on that family. No finite toric list, finite image cone, or equality with divisor complete intersections follows from the cited result. The notebook does not import the finite divisor chamber structure of a Mori dream space into that stronger claim.

## 7. Approach 4: Hodge obstruction and convexification

On (P^1)^4, independent multiplication in the truncated hyperplane ring gives the displayed Gram matrix for gamma=[A]+[B]. On the span of h_1+h_2 and h_3+h_4 the form is 2 times the 2-by-2 identity, so it has a positive definite two-plane.

If an integral surface represented c gamma for any c>0, a projective resolution exists over C. Pulling back the four divisor classes to that smooth projective surface preserves their pairings by the projection formula. The Hodge index theorem allows at most one positive direction on their span. No injectivity assumption on restriction is needed: the positive definite two-plane itself certifies the requisite independence. The contradiction is valid even for singular integral surfaces and for every positive multiple.

Each coordinate surface moves by varying its fixed coordinates, and the convex sum is allowed in Mov. Thus the failure of irreducible representability does not give a nonpolyhedral Mov cone. Indeed, pairing coordinate surfaces with complementary hyperplane monomials reads their six coefficients, and the six coordinate families generate the nonnegative orthant. The nonlinear realization theorem is not being used to replace this convex cone.

## 8. Approach 5: product formula, including edge cases

For smooth projective X, the Chow projective-bundle formula descends to numerical groups for X x P^m. The external-product map is well-defined on numerical classes, and the coefficient maps below show independence. Write alpha=sum_l beta_l x [P^l] in dimension d, retaining only 0<=d-l<=dim(X).

For j in [0,m], multiplication by the projective-space hyperplane H^j and proper pushforward to X gives exactly beta_j. A term with l<j vanishes upon intersection, a term with l>j has strictly smaller-dimensional image and thus has zero cycle pushforward, and the l=j term has projective-space degree one. The index is j, not m-j; the latter exponent occurs only when writing [P^j] as a codimension class.

Nef intersection can be iterated because each step preserves movability, in contrast to the arbitrary effective intersections of Approach 2. Proper dominant pushforward also preserves movability, including a zero image. These statements apply to closed cones by continuity. Thus every coefficient of a movable class is movable.

Conversely, a product of a covering cycle family on X with the Grassmannian family of j-planes covers the product, with each universal component dominating. This gives the other inclusion first for generators and then for nonnegative sums and limits. Only finitely many j occur, so the direct sum of the closed cones is closed. The cases j=0, j=m, m=0, d=0, and d=dim(X)+m cause no exception; infeasible dimensions contribute zero.

The external-product and coefficient maps preserve the rational structures. A finite product of rational polyhedral cones is rational polyhedral, and a rational linear image of one is rational polyhedral. This proves the claimed equivalence. Iteration gives the stated examples with toric surfaces and products of projective spaces, without reducing arbitrary toric varieties to products.

## 9. Computation and integrity assessment

The supplied verifier completed with 1,877 controls, and the supplied manifest verifier checked 11 files with its self-exclusion disclosed. The scripts were inspected before execution and contain no network or remote-state action. They supplement, rather than certify, geometry. In particular, the original projective-factor test inputs the identity matrix and checks its action; it is a useful regression but not an independent derivation of coefficient extraction.

The new checker uses separately written truncated-ring multiplication and pushforward, orbit enumeration, an all-real linear inequality certificate, complete finite incidence enumerations, Hodge restrictions, and supporting functionals for the convex diagnostic. It also validates the frozen source directory, exact ZIP membership and bytes, and this audit's allowlist and digests. TEST_RESULTS.json records the run; its count is not a mathematical confidence score.

The source packet still says that an independent audit was pending when frozen. That accurately dates its creation; this supplement is the later audit. There is no need to edit the frozen status to attach this verdict. If any original byte is changed, its new digest is outside this audit's immutable binding and must be reviewed separately.

## 10. Limits and disposition

- Required mathematical corrections: none.
- Non-blocking clarification: use an explicit quotient-Grassmannian notation in the covering-family parameter space, or explain the projective-space convention locally.
- Source provenance and claimed prior status are not a proof of literature exhaustiveness or novelty.
- The arithmetic checks do not formalize algebraic geometry or prove a universal movability criterion.
- No sixth proof-search approach was undertaken; the added work is verification and clarification of the existing five approaches.
- No full-resolution, first-priority, or publication-ready-peer-review claim is authorized by this audit.

The checkpoint may be described as independently checked partial mathematics with an unsolved target, accompanied by this exact hash-bound audit.
