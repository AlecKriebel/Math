# Independent audit of singular value basin checkpoint

## Recommendation

Accept this packet as an **unresolved research checkpoint with minor clarifications**. Do not label it a solution of either unrestricted source question. I found no fatal mathematical defect in its polynomial argument, its carefully restricted applications of published theorems, or its component capture equivalence. The finite controls reproduce their reported output, but are not evidence of a general analytic resolution.

This audit concerns rank 617, ID 30001393, OWR-4137-010. It is bound to submission MANIFEST.json SHA-256 `b2075d407c7c8549feb69e16fa6ca33dad6d65a57873291da59dda37ce7f0653` and RESULT.md SHA-256 `073340a7e505d58912b40e4bca9f4d18fead1362346d336bb7ccffa176d5b3c7`. The original files were read, not edited. The audit is a separate original deliverable dated 2026-10-04 UTC.

## Source statement and logical scope

An independently retrieved institutional copy of Oberwolfach Report 54/2009 was text-extracted and its printed page 2959 was rendered and visually inspected. Problem 4 specifies an entire function and the immediate basin of an **attracting fixed point**. Its second question uses an arbitrary region. Both require containment of critical and asymptotic values, with no additional closure, boundedness, or simple connectivity condition. The submission correctly preserves these distinctions. [Primary report, DOI 10.4171/owr/2009/54](https://doi.org/10.4171/owr/2009/54)

Use T = CV(f) union AV(f), where AV denotes finite asymptotic values, and S = closure(T) in the plane. Since D is open, T contained in D does not imply S contained in D. Nor does S contained in D imply S compact. A compact set in a multiply connected D need not fit in a simply connected subdomain of D. Each of these is a separate restriction; the submission does not silently identify them.

An affirmative general connected-preimage theorem would settle the fixed-basin question: D lies in f^-1(D), while f^-1(D) is contained in the full basin of the same fixed point. A connected pullback therefore lies in the basin component D. A negative answer for arbitrary regions would not, by itself, settle the dynamical question. A dynamical counterexample would also refute the non-dynamical assertion, because its pullback contains D and at least one other component. The submitted direction of implication is correct.

The term completely invariant is used here in the stated inverse-image sense f^-1(D) = D. One should not silently strengthen this to surjectivity onto D: an entire function can omit a value of an invariant basin.

## Audit of the polynomial proof

The finite-degree proof is correct, subject to ordinary foundational results such as the argument principle and Riemann–Hurwitz. It is self-contained as a derivation from those tools, not a formal proof of those tools themselves.

1. A finite set of critical values in a plane region can be joined by finitely many polygonal arcs. Subdivide their intersections and choose a spanning tree. A sufficiently thin smooth regular neighborhood is a Jordan domain G with closure in D. This construction uses finiteness and does not prove a corresponding assertion for arbitrary compact sets.
2. Polynomial properness makes P^-1(closure(G)) compact. Each component V of P^-1(G) maps properly to G and onto G. To check the latter carefully, a component is closed relative to P^-1(G); hence its intersection with the inverse image of a compact subset of G is compact. Its image is open by holomorphicity and closed by properness. Therefore it equals G. In particular, every component has positive finite degree, there are at most deg(P) components, and their degrees sum to deg(P).
3. For a Jordan curve gamma in V and w outside G, the image loop P(gamma) has index zero about w because G is simply connected. The argument principle excludes any point of P^-1(w) in the bounded interior of gamma. Varying w shows that the entire interior is in P^-1(G). It lies in the same component as gamma: a small neighborhood of gamma is already in V and meets the interior. Thus V is simply connected. Smooth curves suffice for the standard plane-domain characterization, avoiding unnecessary regularity questions about arbitrary wild Jordan curves.
4. The boundary conclusion can be made explicit. Since the critical values avoid boundary(G), P^-1(boundary(G)) is a compact smooth one-dimensional manifold, hence a finite union of circles. The bounded simply connected component V has one such boundary circle, so its closure is a topological disc. Riemann–Hurwitz for the proper map V to G gives ramification deg(P|V)-1.
5. All deg(P)-1 zeros of P', with their multiplicities, occur in these components. The ramification identity gives deg(P)-1 = deg(P)-k and therefore k = 1. Multiplicity, not merely the number of distinct critical points, is essential.
6. For any larger D, every component of P^-1(D) maps onto D by the same properness argument, and so meets the connected set P^-1(G). Thus there is only one component.

The constant and affine boundary cases are harmless under the explicit conventions in RESULT.md. In a constant map every point is critical and the constant value must belong to D. A nonconstant affine map is a plane homeomorphism. The transcendental obstruction is genuine: there is no finite degree or global finite ramification budget to substitute into the displayed identity.

## Published results and their actual hypotheses

The BFR paper was independently downloaded from EMS; its definition on printed page 800 and Proposition 2.9 on page 814 were visually checked, and the proof on page 815 was read. Here S is the **closed** singular set. Proposition 2.9 inherits a simply connected domain from Proposition 2.8 and requires its intersection with S to be compact. Part (2) gives connectedness when S is contained in that domain. Hyperbolicity of f is not an extra hypothesis of this proposition. The submission's sufficient specialization is accurate. [Bergweiler–Fagella–Rempe-Gillen 2015](https://doi.org/10.4171/CMH/371)

The accepted Rempe-Gillen–Sixsmith version was independently downloaded from arXiv. Corollary 8.5 assumes a transcendental entire f, simply connected G, and compact G intersection S, and then characterizes connected pullbacks by S contained in G. Lemma 8.3 enlarges a connected set having at least two points and connected full preimage to any containing domain. Theorem 1.2 constructs disjoint simply connected domains with connected pullbacks for exp(z)+z; it supplies no target counterexample with disconnected pullback. Section 7 describes the invalid topological step in Baker's proof. The submission uses these statements in their permitted directions. [Accepted version](https://arxiv.org/abs/1801.06359v3), [published paper](https://doi.org/10.1007/s00039-019-00488-2)

The compact-set basin application also passes. To make its independent maximum-principle argument explicit, choose r and q < 1 with |f(z)-a| <= q|z-a| on the closed r-disc around a. Convergence to a is locally uniform throughout its basin: any compact subset has a uniform entry time into that contracting disc by a finite-cover argument. Thus, for a curve gamma in the immediate basin, some iterate sends gamma into the disc; the maximum principle sends its interior there too. The interior, together with gamma, is connected and belongs to the full basin, hence to D. Consequently D is simply connected and the compact closed-singular-set theorem applies.

For the finite-singular-set non-dynamical application, a finite tree neighborhood provides G inside the arbitrary region D and the enlargement lemma finishes the argument. The compact-but-not-finite version in RESULT.md explicitly assumes the existence of an appropriate simply connected subdomain; it is not asserted for every arbitrary D. The circle-in-an-annulus objection is correctly retained.

## Audit of the remaining routes

### Monodromy

For nonconstant f and finite S, f^-1(S) is closed discrete and its complement in the plane is connected. The covering over the punctured target thus has a transitive action on a regular fibre. The puncture generators can be based in a tree neighborhood of S inside D. This validates the stated finite-type mechanism. In the general case, replacing S by only T does not give an open regular-value target around an omitted accumulation point. Continuation of selected inverse germs does not supply the required lifting of arbitrary homotopies. RESULT.md identifies this gap instead of assuming it away.

### Counterexample screening

For z^n, a small disc about 1 avoiding 0 has n disjoint root branches, but misses the critical value. For exp(z), a disc avoiding 0 has separate logarithmic branches, while any region containing 0 contains a small disc with half-plane pullback; the enlargement lemma then applies. The exp(z)+z critical calculation is correct: z = (2j+1)pi i and f(z) = -1+(2j+1)pi i. The cited disjoint-domain construction is not a disconnected-pullback example. None of these is a counterexample under the source's hypotheses.

### Trapping-disc exhaustion and component capture

Set m = 0,1,2,... and choose a disc B about a on whose closure the contraction estimate above holds. Define W_m = f^-m(B), and let U_m be the component containing a. Then the W_m and U_m are increasing, and their unions are the full basin A(a) and the immediate component D, respectively. For the latter equality, any point in D can be joined to a by a compact path in D; finitely many members of the increasing open cover (W_m) cover that path, so one W_M contains it.

The asserted component-capture equivalence is correct, including its nonuniform quantifiers. If D is completely invariant, any component V of W_m is contained in D. Pick x in V and N with x in U_N, then take M at least m and N. The entire connected V lies in W_M and intersects U_M, so V is contained in U_M. This does **not** apply a compactness argument to the possibly noncompact V. Conversely, capture of every component of every W_m gives A(a) = D. Since f^-1(A(a)) = A(a), D is completely invariant.

The submitted proof correctly allows M to depend on V. It does not say that all W_m are connected or that a fixed stage captures all subsequent pullbacks. The explicit example below shows why these stronger substitutions are wrong.

## Independent discriminating analytic controls

### Early disconnected pullbacks can merge

Let P(z) = z^2 + 3/16, a = 1/4, and B = B(a,1/32). Then P(a) = a and P'(a) = 1/2. For |h| <= 1/32,

    |P(a+h)-a| <= (1/2 + 1/32)|h| < |h|.

The critical value c = 3/16 is outside B, since a-c = 1/16. Therefore W_1 has exactly two components, containing a and -a. But for real x in [-a,a], P(x) belongs to [c,a], and P^2(x) belongs to [57/256,a]. Since a-57/256 = 7/256 < 1/32, the whole interval [-a,a] lies in W_2. It connects the two W_1 components inside U_2. By nesting and maximal connectedness, both whole components of W_1 are captured by U_2.

Moreover, [0,a] lies in the attracting basin: for x < a in this interval, P(x)-x = (x-1/4)(x-3/4) > 0, and P(x) <= a, so iteration increases to a. Thus the critical value lies in D and the audited polynomial theorem makes D completely invariant.

Despite this, **every finite W_m, m >= 1, is disconnected**. The critical values of P^m are P^k(0), 1 <= k <= m, with total multiplicity 2^(m-k) over P^k(0). The orbit of 0 is strictly increasing toward a, with only its first positive value outside B. Distinct critical fibres do not collide since 0 never returns to 0. Hence ramification inside W_m is 2^(m-1)-1, whereas degree(P^m) = 2^m. Applying the already justified disc calculation yields exactly 2^(m-1)+1 components. None of the critical values is on boundary(B). This distinguishes eventual capture of a fixed component from connectedness of every finite-stage full pullback.

The arithmetic script checks this formula for m <= 10, but the preceding analytic argument, not those checks, establishes the all-m statement.

### The fixed-point qualification matters

For Q(z) = z^2-1, 0 and -1 form a superattracting 2-cycle. The immediate basin component of -1 for Q^2 contains the sole finite critical value of Q, namely -1. It cannot be completely invariant under Q: it contains -1 but its image contains 0, which converges to 0, not -1, under Q^2. Thus replacing the source's attracting fixed point with an arbitrary individual component of an attracting periodic basin is invalid. This is not a counterexample to the correctly stated source question.

### Singleton enlargement is unsafe

For F(z) = exp(z^2), the omitted value 0 has empty full preimage, a connected set under the usual convention. Nevertheless

    F^-1(B(0,exp(-1))) = {x+iy : y^2-x^2 > 1}

has exactly two components. Each is the region above or below one branch of a hyperbola, and any path from positive to negative imaginary part would cross y = 0, which is excluded. Consequently the at-least-two-points hypothesis in the enlargement lemma must not be dropped. Also, the disc misses F's critical value 1, so the example is excluded by the source hypothesis. This is an analytic set identity and separation argument, not an image-based inference.

## Precise clarifications recommended

These are refinements to the exposition, not repairs of a false main conclusion. Preserve the frozen submission and apply any edits only in a separately versioned successor.

1. In section 1, expand the boundary step with the compact smooth-preimage-manifold justification given above. State that smooth Jordan curves suffice in the argument-principle test. Severity: low, proof detail.
2. In section 5, state m >= 0 and explicitly select B with a contraction estimate. This directly justifies both eventual entry and uniform convergence arguments used elsewhere. Severity: low, proof detail.
3. Replace the unsupported-looking existence sentence about infinite sequences of singular values having entry times tending to infinity with: “Pointwise membership of each singular value in some U_m does not by itself establish a uniform index for the entire singular-value set; no such uniform bound, or general component-capture theorem, has been proved here.” No example realizing unbounded entry times under all the source hypotheses is supplied. The original wording can be read as an actual existence claim, so this change avoids overstatement. Severity: low, claim precision.
4. Consider adding the delayed-capture example above. It explains why disconnected numerical pullbacks are not evidence against complete invariance, even when disconnection persists at every finite stage. Severity: explanatory improvement, not required for correctness.
5. Retain “unresolved by this attempt” and the bounded-search qualification. Neither this audit nor a finite web search certifies the present literature-wide open status, novelty, or priority.

## Verification and limitations

All nine files indexed by the frozen manifest match both their byte sizes and hashes; all ten SHA256SUMS entries pass, including the manifest. Re-running verify_controls.py exactly reproduces control_results.json and its 8,233 assertion count. The independent audit adds 350 finite assertions, plus 33 provenance/replay assertions. It checks all 126 subsets of path-graph branch generators of sizes 2 through 7, the exact constants in the delayed-capture example, the finite-stage ramification formula through m = 10, the period-two mutation, and rational cross-sections of the singleton-enlargement example.

The original 8,233 count mainly consists of elementary composition and orbit identities; it is not 8,233 independent confirmations of the target. Similarly, the new finite tests cannot certify continuum connectivity, existence or completeness of asymptotic-value sets, infinite homotopy lifting, or either unrestricted entire-function assertion. Those distinctions are deliberately preserved.

Independent searches on 2026-10-04 using the exact source wording and related basin/preimage phrases located the primary report, the cited papers, and narrower related work. No full resolution was identified in this bounded audit. Search-index dates were not treated as publication dates. Repository duplicate triage and the original chronological log were not independently re-certified; this mathematical audit does not validate an external queue state or historical priority.

The portable audit contains only this original report, original finite-control code and results, bibliography/provenance, and manifests. Privately read PDFs, page images, extracted full texts, raw research corpora, and coordination records are excluded. No remote files or repositories were changed.

## Reproduction

Place this audit directory beside the bound submission directory and run:

    python3 audit/verify_audit.py

Or supply the frozen location explicitly:

    python3 verify_audit.py --submission /path/to/submission

The script is read-only and prints its JSON result. Compare that result with audit_test_results.json. AUDIT_MANIFEST.json binds all audit deliverables and the exact frozen target; SHA256SUMS additionally binds the audit manifest. SOURCE_CHECKS.json records independently retrieved source digests without redistributing the sources.
