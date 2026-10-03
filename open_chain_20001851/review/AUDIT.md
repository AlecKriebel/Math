# Independent adversarial audit: rank 459 / problem 20001851

Date: 2026-10-03. Frozen author packet: 10 files listed in AUTHOR_MANIFEST.json. Associated WIP commit: b09f622694858eafe7ae440de4dbcb4e0cecf63d (remote commit contents were not independently retrieved in this audit).

## Verdict

PASS for the stated five-partial-attempt packet, retaining UNSOLVED / 5 of 5. No mandatory mathematical repair found. This is not a pass for universal connectivity, an all-six-bar theorem, a locked equilateral chain, or a component computation; the packet claims none of these. No public or remote file was changed. Audit computations do not constitute another proof attempt.

All 10 public files match the frozen SHA-256 hashes and byte counts. The supplied Python verifier reproduces checks.json byte for byte. Independent_checks.py additionally checks the rational examples through exact segment-distance minimization, proves the circle identities symbolically, and rechecks every eight-bar lower bound with an independently written dyadic interval implementation.

## 1. Model and target

The AIM problem-list Item 2 asks connectedness for equilateral open arms in R3, and the workshop report Working Group 2 explicitly asks straightening of arbitrary unit-bar chains by noncrossing motions. The packet uses the correct universal-joint, positive fixed-length, zero-thickness model: nonadjacent closed bars disjoint; adjacent bars intersect only at their joint; forward straight joints permitted; overlap/backtracking forbidden. It appropriately discloses that the terse AIM wording itself does not separately spell out contact conventions. Biedl et al.'s introductory definition explicitly matches the packet's strict simplicity convention.

In edge coordinates the strict free set is open in (S2)^n and locally path connected. All straight configurations lie in one component, and translation adds a connected factor. Thus connectedness and universal straightening are equivalent in the stated model. Fixed angles, thick bars and permitted self-contact must remain excluded.

## 2. Attempt 1: scalar interval characterization

PASS. The orientation propagated from I1<I3 yields Ii<I(i+2), and hence all strict middle increments. The endpoint inequalities follow from the first and final separated pairs. Sufficiency explicitly requires n>=4 for x2<=x(n-2); this boundary is handled correctly. The system has n inequalities: n-2 middle directions plus two terminal two-edge sums.

Strict positive feasibility is exactly exclusion of zero from the finite convex hull. Strong separation and Caratheodory in R3 give an obstruction using at most four vectors. Rational feasibility/obstructions and rescaling positive inequalities to >=1 are valid. The separate n=3 strong-separation statement is correct for disjoint compact segments. No axis failure is interpreted as locking.

## 3. Attempt 2: permitted cap paths and interpolation

PASS. Each first-endpoint cap keeps the entire rotating bar strictly below every nonadjacent stationary bar. The only adjacent-overlap direction is the ray toward p2; removing its one endpoint-sphere point leaves a path-connected cap. The south-pole target is safe. The symmetric final-endpoint move has the analogous protection. For unequal lengths the initially strict-simple assumption is inherited from SOURCE_GATE; the scalar nonadjacent-interval conditions alone would not exclude adjacent overlap. This is a useful exposition caveat, not a defect under the stated conventions.

Once all directions have positive u product, normalized interpolation has nonvanishing denominator, preserves each individual bar length and keeps height strictly increasing along the parameterized chain. This excludes all self-contact, including adjacent overlap. The n=3 cap thresholds work as written. No global continuous choice of cap paths or deformation retraction is claimed.

## 4. Attempt 3: exact unlocked axis obstructions

PASS. Independent exact computations verify all 11 lengths, both positive dependencies, both displayed projections and all 16 nonadjacent projected pairs. Minimum squared projected separation is 16/625 for the five-bar example and 6718464/869265625 for the six-bar example. Adjacent projected pairs are nondegenerate and never backtrack.

For the six-bar middle tetrahedron, an independent affine determinant is -1179648/390625. The normalized positive barycentric coefficients are 75/256, 125/512, 125/512 and 7/32. Consequently zero is genuinely interior, so failure of the scalar criterion persists under small three-dimensional unit-direction perturbations. Strict simplicity and the exhibited simple projection also persist. The rank-two map (x-z/10,y) has the stated kernel and differs from the corresponding orthogonal projection only by a plane isomorphism. Biedl et al., Theorem 2.1, applies. Extending the leftward final ray preserves the claims.

## 5. Attempt 4: local motion, rational reduction, component algorithms

PASS. Normalization moves each direction by less than 2 epsilon; a corresponding bar point moves less than 2n epsilon. Therefore the nonadjacent distance lower bound delta-4n epsilon and adjacent-vector lower bound eta-4 epsilon are both valid. The normalized interpolation ends exactly at the chosen nearby unit-direction data. It is a same-component motion, not merely a static clearance estimate.

Rational stereographic points are dense on S2, so each strict component contains rational directions and rational vertices. The reduction preserves bar count and does not cross the self-contact boundary. Locked components are relatively open. The quantified segment-intersection formula is exact, includes closed segment endpoints, and combines correctly with unit equations and the adjacent-antiparallel exclusions. Quantifier elimination followed by a general semialgebraic component algorithm decides fixed n in principle. Basu-Pollack-Roy Theorem 10.2 directly covers general quantifier-free semialgebraic sets, including strict inequalities. No actual component count/CAD run is asserted. Enumeration only semidecides existence of some locked count.

## 6. Attempt 5: exact eight-bar restricted-motion barrier

PASS. The generic two-circle algebra gives |Q-A|^2=r^2 and |Q-B|^2=1 exactly; adding the vertical contribution gives the two spatial unit lengths. The stem identity and regular pentagon chord identities are exact. All eight lengths therefore follow algebraically rather than from numerical enclosures.

An independent interval implementation using rational endpoints and 160-bit dyadic outward-rounded square roots validates all 40 strict inequalities and every rational lower bound in checks.json. In particular, minimum unit-ball slack is greater than 20794989/100000000, minimum origin-side margin exceeds 8602387/781250, and minimum other-vertex side margin exceeds 760845213/50000000. All necessary radicands and denominators are certified positive.

The open ring's endpoints are spatially distinct at t=99/100: |q0-q5|^2 = 9/160000 + sqrt(5)/100000 > 0. Their central/radial images coincide. The strictly convex central projection is otherwise injective on the ring and gives a genuine simple closed radial curve. The argument does not incorrectly infer spatial embedding by perturbing the self-touching t=1 limit: endpoint separation and the projected polygon prove embedding separately. Positive/negative y and height separation prove that both stem bars and ON avoid the ring and each other except for allowed joints. Convexity of the open unit ball places every ring segment inside it.

The Jordan curve is wholly in the upper hemisphere, surrounds N there, and separates N from the equator. Every one of its directions is forbidden because it hits an actual ring point at radius strictly between zero and one. With the tail fixed, first-joint straightness requires the endpoint -b on the equator, so every endpoint path crosses this forbidden curve. This is a valid failure of first-endpoint-only induction. Allowing the seven-bar tail to move invalidates the fixed-barrier premise; no full-chain locking result follows or is claimed.

## Source checks and scope

Primary pages checked directly:
- https://aimath.org/pastworkshops/linkagesproblems.pdf (Item 2)
- https://aimath.org/pastworkshops/linkagesrep.pdf (Working Group 2)
- https://arxiv.org/pdf/cs/9910009 (strict simplicity definition, Theorem 2.1, Section 6 Question 5 and CJ98 reference)
- https://arxiv.org/pdf/math/0603248 (Theorem 10.2)

A small additional search found no primary resolution, but this does not certify a complete current literature search. Remote queue/PR history and the supplied WIP hash were not re-audited. Those provenance limitations do not affect the mathematical partial-results verdict. No finite test, interval enclosure, certificate failure or fixed-tail obstruction is accepted as a universal connectivity/locking proof.
