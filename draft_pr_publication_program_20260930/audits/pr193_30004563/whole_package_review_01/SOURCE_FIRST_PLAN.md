# Sealed source-first interpretation and attack plan

No package manuscript, verifier, certificate, or prior review was read before this plan.

## Primary target
MRT Definition 2.1 says AB^alpha+CD^alpha=AD^alpha+BC^alpha for finite nonzero alpha; quads need not be convex or proper. Definition 2.4 allows any vertex map whose faces are alpha-quads; Definition 2.5 requires six distinct boundary points and separately noncollinear alternating triples. Incoming faces are A1 A2 A3 A0, A3 A4 A5 A0, A5 A6 A1 A0. Outgoing faces are A2 A3 A4 A7, A4 A5 A6 A7, A6 A1 A2 A7. The unique flip property requires uniqueness of each center if they exist; existence for alpha>1 is already proved.

Published p811 Remark 4.8 expects at most three intersections of two construction curves with a common focus for alpha>1. It is a simulation-based expectation, not a proved bound. OWR35/2020 p1785 explicitly conjectures three as the maximum number of possible central points, for immersions allowing crossing edges. A single fixed admissible boundary at alpha=16 with an incoming center and at least five distinct outgoing centers refutes that expectation and that maximum-center conjecture. It does not on its own refute a claim about proper embeddings or establish a full replacement upper bound.

For squared norm Q_i(X)=||X-A_i||^2, alpha=16 means Q_i(X)^8. Incoming equations are Q_1(A0)^8-Q_3(A0)^8=|A1A2|^16-|A2A3|^16, cyclically. Outgoing equations are Q_2(A7)^8-Q_4(A7)^8=|A2A3|^16-|A3A4|^16, cyclically. Boundary balance makes the third dependent once two hold. All boundary constants must be fixed independently of the candidate center; interval uncertainty may enclose one fixed algebraic coefficient, not supply distinct coefficients at separate roots.

## Independent adversarial families
1. Reconstruct the actual powered equations and signs from the published combinatorics, check all six identities independently, and test incoming and outgoing labels.
2. Attack existence and multiplicity: root branches, derivative/global-domain arguments, IVT signs, rational endpoint certificates, zero/negative-base and root enclosure validity. Seek alternate elimination/numerical reconstruction as corroboration, without treating numerics as proof.
3. Attack geometry: six distinct points, noncollinearity of each alternating triple, distinctness of centers from each other/boundary, adjacency collapse, crossing/proper-embedding scope, limiting alpha=2 or symmetric degeneracies.
4. Attack quantifiers: one fixed six-point configuration, fixed-vs-interval coefficients, common-focus curves genuinely matching original Definition 2.7; avoid arbitrary nonpower phi substitutions.
5. Inspect code before running an owned copy, reconstruct certificate arithmetic, guard against self-confirming checks, root bisection termination and count semantics, and check code/proof/data/PDF consistency.
6. Audit frozen package seal and allowlist, complete ZIP membership and hashes, history versus publication endpoint (10^17 versus 10^16), metadata scope, authorship/AI/unrefereed disclosure, attribution and the explicitly qualified priority route. Independently inspect the three older-family primary references after core assessment. No demand to prove absence of unknown literature.

Success requires all material mathematical and package claims survive, with every remaining uncertainty stated. A failure will be recorded with severity, concrete evidence, and minimal repair. No shared repairs or publication.
