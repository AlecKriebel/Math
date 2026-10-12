# Independent cross-review: GROUP_2 first five metadata patches

Checkpoint: 2026-10-10 14:10 PDT (21:10 UTC). Completion estimate for these five content/patch cross-reviews: **100%**. Conclusion: **PASS for all five**, with no correction requested. Application and final remote invariance checks remain outstanding in the parent workflow.

I read the complete exact deposited-PDF text for each of the five records below, including bibliography and scope/disclosure sections, and compared every proposed metadata field and keyword with the old metadata. The catalog records local PDF checksum matches. The longer Vlasov–Maxwell output was reread across the output-truncation boundary. This is an independent metadata alignment check, not certification of the mathematics or upstream external proofs. No patch, remote record, code, DOI, version, file or git state was modified.

## 23204176 — Rational Hodge classes on mixed products of K3 moduli spaces — PASS

Evidence: `papers/23204176/paper.txt`, all 177 lines / 4 PDF pages. Theorem 1 and §1 specify projective complex K3 bases, smooth projective Gieseker-stable twisted-sheaf or eligible generic Bridgeland-stable moduli, and arbitrary mixed/repeated bases. Proposition 2 and §2 explicitly use rational algebraic correspondences, Tate-twisted Chow-motive splittings and cycle-class pull-push. §3 explicitly withholds arbitrary deformations, singular/semistable or abelian-surface moduli, integral/generalized Hodge and finite-dimensional motives.

Every keyword is supported:

- `rational Hodge conjecture`, `K3 surfaces`, `moduli spaces`, `Hilbert schemes`, `Gieseker-stable sheaves`, `twisted sheaves`, `Bridgeland stability`, `moduli spaces of sheaves`, `mixed products`: exact Theorem 1 objects and quantifiers.
- `Chow motives`, `Hodge classes`, `algebraic cycles`, `Tate twists`, `algebraic correspondences`: definitions and Proposition 2's explicit transfer mechanism.
- `Kuga–Satake`: §1's dependency/provenance account and §3's sharply limited Lean-scope disclosure; the term names a discussed input, not a new theorem by this author.
- `complex algebraic geometry`: the entire complex projective setting.

Added `language: eng` agrees with the deposited manuscript. The title and description are unchanged. Their smoothness/projectivity/stability, inherited-source, mixed-product, no-priority/novelty, AI/unrefereed and no-formalization caveats remain intact.

All three added related links use `references`, which is appropriately modest: Bülles DOI `10.1007/s00229-018-1086-0` is bibliography [3] and the exact motive-splitting input; Arapura DOI `10.1016/j.aim.2006.01.005` is bibliography [2] and credited prior Hodge transfers; pinned OpenAI commit URL exactly matches the existing reference [4] and §1's principal snapshot. They neither attribute coauthorship nor assert formal verification. The old record has no related-identifiers array, so no preexisting relations are dropped. The existing free-text references are untouched.

## 23203732 — L2-acyclicity and cost for a rank-100 amalgam — PASS

Evidence: `papers/23203732/paper.txt`, all 298 lines / 6 PDF pages. §2 gives the rank-100 amalgam and Bernoulli/finite-height actions. Lemma 2 and Proposition 3 give the direct regular-tree convolution, cellular boundary, finite two-dimensional classifying space and all-degree L2-acyclicity independently of cost. §§4–6 clearly retain the upstream positive Bernoulli-cost input and distinguish action cost from group infimum cost.

Every keyword is supported:

- `cost`, `fixed price`, `orbit equivalence`, `measured group theory`, `probability-measure-preserving equivalence relations`: §1 definitions and the relation-level versus group-infimum distinctions.
- `L2-Betti numbers`, `L2-acyclicity`, `asphericity`, `classifying spaces`, `von Neumann dimension`, `regular trees`: Lemma 2/Proposition 3 and Theorem 5.
- `amalgamated free products`, `Bernoulli actions`: exact §2 group/action construction.
- `Fox derivatives`: explicit completed cellular boundary computation in §3, credited to Fox.

English addition is correct. No title or description changes. The existing description retains the independent all-degree invariant calculation, inherited positive-cost proof, intermediate-source warning, prior triage/classical implication, no independent discovery/firstness and AI/unrefereed/nonformal caveats.

Related identifiers are unchanged. Their `references` relations fit bibliography [5] (pinned OpenAI rank-100 cost input), [2] (Gaboriau action invariance), [6] (Popa–Shlyakhtenko–Vaes known implication), and [9] (author's public preliminary triage). The relations do not claim that the new independent cellular proof is inherited from the cost input.

## 23203334 — Finite multispecies relativistic Vlasov–Maxwell — PASS

Evidence: `papers/23203334/paper.txt`, all 595 lines / 10 PDF pages. Theorem 1.1 and §1 specify fixed finite species, strictly positive masses, arbitrary charges, nonnegative compact smooth phase data and compatible `C_b^∞ ∩ L2` fields. They expressly impose no smallness, symmetry or neutrality. §§2–5 keep positive mass-weighted energy, signed source/receiver coefficients and the simultaneous support bootstrap. §6 proves local theory/continuation and §7 states the no-massless/no-noncompact-tail limits.

Every keyword is supported:

- `relativistic Vlasov-Maxwell`, `multispecies`, `global classical solutions`, `kinetic theory`, `partial differential equations`, `collisionless plasma`, `global existence`, `large initial data`, `Cauchy problem`: the exact equation, theorem and no-smallness statement; collisions are explicitly excluded.
- `signed impulse estimates`, `angular occupation`: §§3–5's substantive transfer argument.
- `momentum support`, `continuation criterion`: Theorem 1.1 and §§5–6's finite-time support/continuation mechanism.
- `mass normalization`, `charge-to-mass ratio`: equation (1.1) and §1's distinction between equal-ratio inherited cases and distinct-ratio transfer.
- `energy estimates`: §2's mass-weighted positive spatial/cone budgets.

English addition is correct. Title and description unchanged. Large-data/global terminology does not erase the explicit compact-support, positive-mass, fixed-species and bounded-field-derivative assumptions in the description. The description keeps inherited universal cancellation, distinct-ratio coefficient transfer, source attribution, AI/unrefereed/no-firstness and no formalization.

The unchanged pinned OpenAI snapshot with `isDerivedFrom` is consistent with §1/[1]'s exact one-species analytic dependency. No link implies that the fixed finite-species coefficient transfer was already in that source.

## 23203323 — A priori estimates across the subcritical Lane–Emden hyperbola — PASS

Evidence: `papers/23203323/paper.txt`, all 225 lines / 5 PDF pages. Theorem 1 requires n≥3, p,q>1 and the strict subcritical hyperbola for the unweighted classical system. Its conclusions include proper-domain/gradient/exterior estimates, zero-Dirichlet half-space nonexistence and fixed bounded C2-domain strong compactness in precisely stated spaces. §§2–4 reconstruct the inherited doubling and boundary blow-up machinery and prove strong compactness using Sobolev and Schauder estimates; §5 explicitly withholds critical/supercritical, weighted, weak-solution and parabolic claims.

Every keyword is supported:

- `Lane–Emden system`, `elliptic systems`, `subcritical Lane–Emden hyperbola`, `semilinear elliptic equations`: equations (1)–(2) and exact strict scope.
- `a priori estimates`, `Liouville theorems`, `gradient estimates`, `exterior decay`: Theorem 1 and §§2–3.
- `Dirichlet problem`, `half-space nonexistence`, `boundary blow-up`, `doubling lemma`: exact established reductions discussed in §§2–4.
- `strong compactness`, `Sobolev estimates`, `Schauder estimates`: exact function-space conclusions and §4's norm-convergence proof.

Removing the generic original `consequence note` keyword does not remove its status from the unchanged description. English addition is correct. The title/description retain strict exponent/dimension scope, inherited Liouville and reduction inputs, no first-priority or independent-solution claim, exact spaces, Lean rebuild limits and AI/unrefereed status.

Existing relations are unchanged: the source manuscript is `isDerivedFrom` and PQS/Quittner–Souplet links are `references`, matching [1]–[3] and their distinct roles. The arXiv DOI targets an existing cited source; the patch adds no stronger semantic relationship.

## 23203270 — Explicit complex polynomial retract in five variables — PASS

Evidence: `papers/23203270/paper.txt`, all 292 lines / 6 PDF pages. Theorem 1 and §§2–3 supply split complex-algebra homomorphisms, a five-component idempotent polynomial endomorphism and a smooth integral transcendence-degree-four image. The nonpolynomiality is an explicitly external cancellation theorem. §1 and the dependency account discuss locally nilpotent derivations; §4 separates exact symbolic identities from written nonpolynomiality and unreproduced Lean build. Ambient dimension four is expressly not settled.

Every keyword is supported:

- `Costa retract question`, `polynomial retracts`, `algebra retracts`, `retracts of polynomial rings`, `split algebra homomorphisms`: §1's definition and Theorem 1's split maps.
- `affine-space cancellation`, `Zariski cancellation problem`, `polynomial cylinder`: the stated inherited cancellation problem and `A[w] ≅ C[5]` input. Zariski cancellation is the standard name for this precise affine-space cancellation problem.
- `complex affine geometry`, `complex affine five-space`, `smooth affine varieties`, `idempotent polynomial map`: exact complex ambient space and image conclusion; direct smoothness proof and zero-fiber computation in §3.
- `locally nilpotent derivations`: §1's pivotal input mechanism and §2's cylinder-coordinate exponential derivation.
- `exact symbolic verification`: §4's polynomial-identity certificates, correctly distinct from proof of nonpolynomiality.

English addition is correct. Title/description unchanged, including the inherited nonpolynomiality and classical Nagamine implication, five-variable limitation, no four-variable solution, priority audit limits, AI/unrefereed/no complete formal-verification and original-versus-third-party licensing disclosures.

Related links unchanged: `isDerivedFrom` for the pinned explicit cancellation input, and `cites` for Nagamine's prior classical cylinder-to-retract implication, agree with bibliography [6] and [2]. No relation confuses newly written transport formulas with the upstream construction.

## Overall conclusion

All five patches are content-aligned and preserve mathematical scope and attribution. Every tag names an actual theorem object, method, problem synonym or explicitly discussed dependency; no tag advertises an excluded extension. Only 23204176 adds related links, all already documented in its deposited bibliography and existing metadata references. No genuine issue found. **PASS**.
