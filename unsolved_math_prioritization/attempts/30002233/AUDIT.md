# Independent audit of the component group counterexample

## Verdict

**Accept as a verified existing negative answer, with the expanded hypothesis checks in `PROOF.md`.** The frozen candidate's numerical conclusion and its application to the stated geometric question are correct in the specified tame characteristic-zero setting. The negative answer is already present in the cited original workshop report and was subsequently published by Amini–Baker–Brugallé–Rabinoff. It is not an unresolved question on the evidence inspected, and this audit makes no novelty claim.

The source's transposed group orders are a local error in Example 8.6. They are not evidence that the lifting theorem or component-group comparison is false. A literal order-eight-to-order-four comparison would not by itself imply failure of surjectivity, but the graph labels determine the actual order-four-to-order-eight situation unambiguously.

## Reviewed object and preservation

The reviewed candidate contains 4,166 bytes and has SHA-256 `c70f5de22f74e37b4d8fbf5f01bf38f8bd043ef025078f636c8a13e762f27546`.

Its size and hash matched before the audit and again during publication preparation. All seven original candidate/source input pins match. The prior audit and acceptance report said six, a counting error corrected here. The reviewed candidate remains unchanged; the expanded proof and audit are separate authored works.

## Exact target and historical status

The target asks about the covariant homomorphism between the component groups of the Néron models of the Jacobians of a finite map of smooth, proper, geometrically connected curves over a complete discretely valued field. Its geometric restrictions are a source whose minimal regular model has a special fiber of two transverse rational components, and a Mumford target of genus at least two.

Question 21 in Rabinoff's contribution begins on printed p. 3247 and states its two restrictions on p. 3248. The subsequent paragraphs on that same page give the banana-graph construction and explicitly conclude with a negative answer. Therefore a status assessment that read only the lead-in misses the result on the immediately following page.

ABBR Example 8.6 is on p. 50 of arXiv:1303.4812v3, dated 15 April 2014. The published paper is *Research in the Mathematical Sciences* 2, article 7, published 10 June 2015; its Example 8.6 is on PDF p. 65. The publisher's example poses a slightly broader semistable-target question, but its construction has a split totally degenerate genus-two target, so it also meets the original Mumford restriction.

The wording about two components must refer to the special fiber. A model over a discrete valuation ring is a two-dimensional scheme, not itself a union of two rational curves.

## Claim by claim findings

### Harmonic graph morphism

**Pass.** The domain is the four-edge banana with all lengths one; the target has three metric edges with lengths one, two, two. At each source endpoint, the slope sums above the three target directions are two, two, two. Interior points satisfy the same harmonicity condition. The global degree is two. No edges are contracted. The genera are three and two.

### Critical groups

**Pass.** The source reduced Laplacian is `[4]`. The target's unit-edge subdivision has reduced Laplacian

\[
\begin{pmatrix}3&-1&-1\\-1&2&0\\-1&0&2\end{pmatrix}.
\]

Its determinant is eight and its first two determinantal divisors are one, one, hence its Smith invariants are one, one, eight. Thus the groups are cyclic of orders four and eight, in source-to-target order. The independent cycle-length pairing determinants are also four and eight.

**Convention checked.** These finite groups are the regularized graph Jacobians, rather than the real-torus Jacobians of metric graphs. Subdividing the two target length-two edges is essential. Ignoring their lengths would give the wrong group.

### Induced homomorphism and cokernel

**Pass.** With `S = [u' - v']` and `A = [a - v]`, the target Laplacian relations give `[u - v] = 2A`, with `A` of order eight. Covariant divisor pushforward sends `S` to `[u - v]`. Thus the map is `j mod 4 -> 2j mod 8`, is injective, and has cokernel `Z/2Z`.

**Convention checked.** Pushforward of a point has coefficient one. Multiplication by local degree belongs to pullback and must not be inserted into this calculation. ABBR Lemma 8.3 and Theorem 8.4 identify the computed map with the intended covariant component-group homomorphism.

### Metrized complex and tameness

**Pass.** At every vertex attach a projective line, mark the source points `1, -1, 0, infinity`, and mark the target points `1, 0, infinity`. The two residue maps `z -> z^2` have exactly the prescribed ramification indices `1, 1, 2, 2`, contain every preimage of every target marking, and have degree two. All ramification is marked. The graph ramification coefficient is zero at the two vertices and at all interior points. Thus this is a tame covering, with no punctures, satisfying the stronger version of the lifting theorem directly.

**Boundary checked.** In residue characteristic two, the markings at `1` and `-1` collide and the degree-two residue maps are inseparable. The supplied tame construction does not establish that case. A single characteristic-zero example already answers the universal question negatively.

### Discrete field and rationality

**Pass after making the implicit construction explicit.** Work over `C((t))`, not an algebraically closed discretely valued field. The algebraically closed field used for the intermediate Berkovich formulation is a different, nondiscretely valued extension.

The target is constructed from two projective lines meeting at the three rational markings. Independent stable-curve smoothing parameters are sent to `t, t^2, t^2`. This gives a split semistable model over `C[[t]]` with exactly the required skeleton. The source lengths are one and belong to the original value group. Consequently every fixed-ground-field hypothesis in ABBR Remark 7.13 holds.

**Dependency distinction.** Theorem 3.24 over an algebraically closed field, or descent merely to an unspecified finite extension, is not sufficient by itself for the exact two-component regular-model claim. A ramified extension changes normalized thicknesses. The proof uses the split target over the original field and Remark 7.13 to avoid that gap.

### Geometry of both curves

**Pass.** The target stable special fiber has two rational components and three rational nodes, all branches split, so it is totally degenerate of genus two. Mumford's Theorem 4.20 identifies its generic fiber as a Mumford curve.

The source has two rational components and four thickness-one nodes. Its completed node rings are regular. Each source component has self-intersection minus four, so no exceptional curve of the first kind can be contracted. Its regular model is minimal. Its genus is three. The lifted map is finite; its source and target are smooth, proper curves, and the source is geometrically connected. In fact it is an étale double cover, consistently with the genus calculation.

### Semistable model comparison

**Pass.** The finite lifted map respects the original semistable vertex sets. ABBR Theorem 5.13 supplies the associated finite map of semistable models, and Theorem 8.4 applies to those models. The target model is permitted to have thickness-two singularities. There is no need, and it would be incorrect here, to assume a compatible map between both regular semistable models.

## Source errors and their exact extent

1. **ABBR arXiv v3 p. 50 and published p. 65:** the stated orders are attached to the wrong graph symbols. Correct only the assignments to `|Jac_reg(Gamma')| = 4` and `|Jac_reg(Gamma)| = 8`. The construction and negative conclusion survive.
2. **Oberwolfach printed p. 3248:** the second graph in the pair of definitions is mistakenly labeled with a prime. It is the target graph without a prime.
3. **Candidate exposition:** the core claims need no mathematical reversal. The expanded proof specifies the ground field, split target construction, all marked-fiber and generic-étaleness checks, the fixed-field lifting dependency, and the minimality calculation. These are explanatory completions of a valid cited argument.

The PDF pages containing the two source errors were rendered and visually inspected, so these findings do not rely on a text-extraction mistake involving primes or subscripts.

## Imported theorem ledger

The audit does not claim to reprove the following geometric results from first principles.

- **Stable-curve deformation and algebraization:** the proof of Conrad's Theorem B.2 in Baker (2008), printed pp. 648–649, supplies independent node parameters and algebraization. In the construction, the two rational components are stable, every node is split, and the chosen parameters are nonzero.
- **Metrized-complex compatibility and tameness:** ABBR Definitions 2.19 and 2.21 specify the exact conditions verified above; the graph ramification coefficient is their formula (2.14.1).
- **Node thickness and skeleton length:** ABBR Section 5.9. Parameters of valuations one, two, two give the target lengths, and unit source lengths give thickness one.
- **Lifting:** ABBR Theorem 7.4(1), alternatively Theorem 7.7. There are no loop edges, no punctures, and the morphism is a tame covering of metrized complexes, not merely a graph map with unverified residue covers.
- **Fixed discrete ground field:** ABBR Remark 7.13, arXiv pp. 47–48 and published p. 62. Completeness, algebraically closed residue field, split rational target model, and source lengths in the original value group are all checked.
- **Model extension:** ABBR Theorem 5.13, arXiv p. 31, published p. 42; the source vertex set is the inverse image of the target vertex set.
- **Component groups and functoriality:** ABBR Theorem 8.2, Lemma 8.3, and Theorem 8.4, arXiv p. 49, published p. 64. The curves are semistable over the original complete DVR with algebraically closed residue field.
- **Mumford property:** Mumford (1972), Theorem 4.20, printed p. 174. The target stable curve has smooth generic fiber and split degenerate closed fiber.
- **Minimality:** Stacks Project Definition 55.8.4, Lemma 55.8.5, and Lemma 55.10.1. The proper source model is regular, the generic genus is positive, and its two components have self-intersection minus four.

The auxiliary facts that a proper flat curve family has constant arithmetic genus and that a principal fiber has zero intersection with its components are standard algebraic-geometric facts. Finite-group arithmetic, the genus counts, the local map compatibility, and the intersection calculation are written out in the proof.

## Reproducibility and limits

The original exact-arithmetic verification used Python's standard library and rational arithmetic. Its unoptimized run checked the candidate/source input hashes, reduced Laplacians, determinant divisors, element orders, explicit target relations, image and cokernel, independent cycle-pairing determinants, harmonic degree, graph ramification coefficient, and graph genera, and returned `PASS`.

That verifier uses assertion statements. Python's optimization options `-O` and `-OO` disable those assertions, so its optimized success outputs do not establish that the mathematical obligations or input comparisons passed. They are not counted as successful optimized verification.

A separate exact-arithmetic implementation reproduced every finite obligation with explicit failures that remain active under optimization. It uses permutation determinants and Cramer's rule independently of the original recursive-determinant and elimination implementation. Normal, `-O`, and `-OO` runs each passed the same 52 checks. Input preservation was also verified separately by explicit size-and-hash comparisons. The complete mathematical calculation remains in `PROOF.md`; aggregate verification outcomes are recorded in `CHECK_RESULTS.json`.

These computations are consistency checks for the explicit finite argument. They do not prove the analytic lifting theorem, model algebraization, Mumford uniformization, or Raynaud comparison by computation. Those are precisely the imported dependencies listed above. No external review of those entire foundational papers is claimed.

Full bibliographic links are in `PROOF.md`, and exact PDF byte counts and SHA-256 hashes are in `SOURCE_MANIFEST.json`. The explicitly versioned arXiv v3 PDF was re-retrieved and byte-compared with the frozen unversioned arXiv download; the hashes match. The publisher PDF was retrieved separately and inspected as a distinct version.
