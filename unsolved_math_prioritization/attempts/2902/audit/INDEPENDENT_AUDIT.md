# Independent audit of KP-4.26

**Verdict: PASS as an unresolved five-approach research attempt.** The elementary propositions and the stated limits of the constructions withstand this review. No universal smooth embedding theorem or counterexample has been established. There is no basis to change the problem's status from **unsolved** or to claim a novel resolution.

Audit date: 2026-10-03. Problem ID: 2902. The review covers the frozen nine-file author package, its cited mathematical sources in the scope specified below, and independently implemented finite controls. This is a mathematical review, not proof-assistant certification or journal peer review. No correction to the frozen mathematical text is required by the findings below.

## 1. Identity, integrity, and source scope

The exact problem and all three accompanying remarks were checked in text and in rendered images of printed pp. 211–212 of [K3: A New Problem List in Low-Dimensional Topology](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf). The target is the compact puncture of every integral homology 3-sphere, embedded smoothly in standard S4. Deleting a point, embedding a closed manifold, changing to the locally flat category, or replacing the ambient sphere by a homology or homotopy sphere would change the question. C. Livingston's attribution is correct.

The reviewed SHA256SUMS file has SHA-256:

    842b53a6183ae4cb86ea61fedef111cb75d1729c4aabad088aa4eeb6f7fa9ae2

The reviewed PROOF.md has SHA-256:

    4a7e8b3e58fadf0278e3b32f85757335bb719c1beb320f50861dbfc639878080

All eight entries in the author manifest matched before and after the review. All four PDF fingerprints and byte counts in SOURCE_HASHES.json match the inspected source copies. No author file was changed. The separate audit manifest binds the reviewed files and this audit's deliverables.

Primary-source reading included Zeeman's branched-cover setup and proofs in §§5–7, including Lemmas 1–6 and the concluding equivariance check; Hillman's §2.9; and Larson's §5.1 statements and arguments. The review does not certify every dependency of Larson's article. Larson's thesis proof was not inspected and contributes no premise to this verdict. Neither an exhaustive literature search nor the author's historical repository-search results are independently certified here. A bounded public search found no verified universal resolution; search absence is not a theorem of openness.

## 2. Doubling and the closed-manifold obstruction

Proposition 1 is valid in the smooth category. The relative fundamental class makes H3(Y) to H2(S2) an isomorphism, so the puncture F is acyclic. Removing the ball leaves the fundamental group unchanged. The oriented normal line of a smooth F in oriented S4 is trivial. A collar-compatible regular neighborhood, with rounded corners, therefore has boundary the oriented double of F, diffeomorphic to Y # (-Y). Conversely, that double contains a shortened copy of F. This proves both implications without a smooth Schoenflies assertion.

The manifold F × I is a smooth homology ball with group G. Its boundary inclusion maps each of the two free factors of G * G isomorphically to G. Doubling this particular filling by the identity gives the pushout of two fold maps and consequently retains G. Thus the proposed filling does not furnish a standard ambient sphere when G is nontrivial.

The closed-manifold obstruction is also applied correctly. A connected two-sided closed homology 3-sphere in a smooth integral homology 4-sphere separates, and the orientation map in Mayer–Vietoris is a unit. Its complementary closures are integral homology balls. Such a ball is spin and has zero signature, so a nonzero Rokhlin invariant obstructs the closed embedding. But Y # (-Y) already bounds F × I for every Y. Homology-cobordism invariants vanishing on homology-ball boundaries therefore give no obstruction through this reduction.

The explicit smooth arguments are important: the title of [Hillman's manuscript](https://www.maths.usyd.edu.au/u/jonh/embkDec24.pdf) does not license silently replacing a smooth question by a locally flat one. Its §2.9, pp. 25–26, records the same doubling and boundary-connected-sum observations; the packet proves the needed smooth versions itself.

## 3. Ordinary spin and preservation of the puncture

Proposition 2 is valid. The union (S1 × F) ∪ (D2 × S2) contains the slice F, including its boundary after rounding. The boundary longitude kills the S1 factor in Z × G and kills nothing further in G. In integral Mayer–Vietoris the H1 map to S1 × F and the H2 map to D2 × S2 are units. This yields homology (Z, 0, 0, 0, Z) and fundamental group G.

The construction explicitly removes a ball from the slice. Its new S2 boundary is not automatically capped by a disjoint smooth 3-ball. Supposing such a cap existed universally would give a smooth closed-Y embedding in a homology 4-sphere and contradict the preceding homology-ball obstruction. The note correctly declines to use the source's unqualified spinning sentence as such a theorem. This is a caution about a stronger smooth interpretation, not a claim about what the source intended topologically.

## 4. Diagonal surgery, its quotient, and framing

Proposition 3 is valid. The graph of a loop representing g is an embedded circle even if the loop in Y self-intersects. Taking the loop constant near one parameter value allows a product neighborhood of its unique intersection with the selected Y slice. After removing that neighborhood, the surviving slice is the required compact puncture. Oriented rank-three bundles over a circle are trivial, so the required framing exists. This operation does not claim to preserve the deleted 3-ball.

The exterior-to-ambient map induces an isomorphism on fundamental groups: loops and two-dimensional homotopies can avoid a one-dimensional core in four dimensions by general position. The longitude represents tg, so van Kampen gives

    (Z × G) / normal(tg) = G / normal({[g,x] : x in G}).

Eliminating t makes g central; it does not impose g = 1. This distinction is essential. For example, a nonidentity central element of G imposes no new commutator relation even though its own normal closure is nontrivial.

Set C = normal([g,G]) and N = normal(g). Then C is contained in N. If G/C is trivial, N = G. Conversely, if N = G, the image of g centrally normally generates G/C, so that quotient is cyclic. Since G is perfect, so is every quotient; a perfect cyclic group is trivial. The perfectness hypothesis is genuinely needed: a transposition normally generates S3 but its centralizing quotient is C2. This supplies an additional negative control beyond C5.

The integral homology argument is sound. Excision gives relative groups Z in degrees 3 and 4. The top map is the orientation isomorphism, and the degree-3 map is multiplication by the intersection number of the graph with the slice, which is +1 up to convention. Thus the exterior has the homology of S1. Its longitude is primitive in H1; the other filling map is a unit on H2. Surgery therefore produces an integral homology 4-sphere. Changing the normal framing does not change these unit calculations or the normal-closure quotient. It may change smooth geometric information, which these calculations do not determine.

A simply connected homology 4-sphere is a homotopy 4-sphere by the Hurewicz and Whitehead argument stated in the packet. No step identifies it diffeomorphically with standard S4. Universal normal generation and smooth standardness remain separate missing inputs. Even proving the former would not supply the latter.

## 5. Twist-spun positive examples and connected sums

[Zeeman, *Twisting spun knots*](https://www.lms.ac.uk/sites/default/files/1965%20Twisting%20spun%20knots.pdf), Main Theorem part 2, p. 486, explicitly supplies a smooth compact fiber closure. Corollary 4, p. 487, gives the punctured embedding consequence. Corollary 2 on that page instead concerns the ±1-twist unknot. The packet's locator distinction is correct; it need not assert that K3's reference cannot enter a different derivation.

The relevant proof was checked beyond its statement. Lemma 3 constructs the ambient sphere by extending the boundary rotation over a ball. For n = 3, these are smooth ball rotations, and the rounded boundary of D3 × D2 is standard S4. The bundle maps are constructed in Lemmas 4–5. Lemma 6 identifies the compact closure with the punctured cyclic cover, and the smooth-fiber statement is explicit. Thus no unproved smooth homotopy-sphere identification is imported here. The 5-twist trefoil example supplies the punctured Poincaré sphere; its closed obstruction is consistent with the absence of a disjoint smooth cap.

Proposition 4 is valid. Each compact Fi misses a point of S4 and therefore lies in a standard R4 chart; translation and dilation place the copies in disjoint small balls. The complement of their disjoint union is connected, since its third cohomology vanishes and Alexander duality applies. Local exterior collars can consequently be joined by an embedded arc in the complement. A small, suitably framed 3-dimensional 1-handle realizes the boundary connected sum. Conversely, the boundary-connected-sum model contains shortened copies of both Fi. No assertion about connected-sum factors of an arbitrary closed embedding is needed.

These constructions prove a substantial family of positive examples, not that every homology 3-sphere is in that family. A general branched-cover presentation need not be a cyclic cover over one knot.

[Larson, *Surgery on tori in the 4-sphere*](https://arxiv.org/pdf/1502.06834), §5.1, confirms the scope distinction: Corollary 5.5 has S2 × S2 or the nontrivial S2-bundle as ambient manifold. Theorem 5.6 imposes ribbon or slice hypotheses and distinguishes general slice coefficients from even denominators. Its arguments do not authorize dropping these hypotheses. K3's separate arbitrary-knot 1/n-surgery statement is attributed to Larson's thesis, whose proof remains uninspected here. The packet does not rely on that uninspected proof.

## 6. Additional circle surgeries

Proposition 5 is valid under its stated H1(X; Z) = 0 hypothesis. Surgery quotients the fundamental group and hence leaves its abelianization zero. Euler characteristic increases by 2 because S1 × D3 has characteristic 0 and D2 × S2 has characteristic 2, with common boundary of characteristic 0. Poincaré duality gives b3 = b1 = 0, so b2 increases by 2. The torsion statement follows from integral duality and the universal coefficient theorem; H1 = 0 implies H2 is torsion-free.

Compactness gives finitely many group generators, which may be represented by disjoint embedded loops. Killing them produces a simply connected ambient manifold with b2 = 2r. For r > 0 it cannot be S4, independently of framing or any conjecture about exotic spheres. This is an ambient computation: the packet explicitly does not claim that arbitrary additional surgery loops or later cancellations preserve F. Removing the new second homology while retaining F would require genuine relative smooth geometry, not rank arithmetic.

## 7. Computational replay and independent controls

The supplied verify.py exits successfully. Its 14,701 asserted checks reproduce verification.json byte-for-byte. Its scope is correctly limited: most checks are finite group operations; neither a large count nor exact arithmetic proves a smooth embedding theorem.

The separately written independent_verify.py builds the binary icosahedral group from permutations of the 24 nonzero vectors over F5, generated by two elementary shears. It independently obtains order 120, derived subgroup order 120, and nine conjugacy classes. The seven noncentral classes, comprising 118 elements, normally generate and have trivial centralizing quotient. The identity and central involution have centralizing quotient of order 120; the latter's own normal closure has order 2.

For every conjugacy class, the independent script also constructs the normal closure of (1,g) directly in C_order(g) × G and checks the diagonal quotient. This finite replacement of Z is exact for the quotient because the relation t = g^-1 already forces t^order(g) = 1. S3 and C5 provide nonperfect negative controls. Separate exact computations check all four sign choices for the primitive Mayer–Vietoris unit maps and the abelianization determinant -1. Results are saved in independent_verification.json.

These finite calculations test the stated algebra. They do not prove that every relevant infinite group has weight one, locate a suitable framing, perform a relative handle cancellation, or certify a diffeomorphism to S4.

## 8. Final disposition and limits

- Fatal mathematical defects found: none.
- Required corrections to the frozen packet: none.
- Valid partial results: smooth doubling equivalence; surviving ordinary-spin group; the diagonal centralizing quotient and perfect-group weight-one criterion; connected-sum closure and restriction; the b2 = 2r additional-surgery cost.
- Established positive examples: appropriately attributed finite cyclic branched covers and their connected sums.
- Five distinct approaches are documented. Their count is not evidence for either answer to the universal question.
- Outcome remains **unsolved, 5/5**, with no full-resolution or novelty claim.
- The remaining requirement is a construction in standard smooth S4 for arbitrary Y, or an obstruction genuinely applicable to its compact puncture. Nothing in the replay or this audit closes that gap.

## Reproduction

Run the author verifier in its own directory and compare its output with verification.json. Run independent_verify.py in the audit directory and compare its output with independent_verification.json. Run `sha256sum -c audit/SHA256SUMS` from the parent directory containing public and audit. Both scripts require only Python 3's standard library and make no network calls.
