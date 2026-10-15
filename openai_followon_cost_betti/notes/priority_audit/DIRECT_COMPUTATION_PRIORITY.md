# Final bounded priority check of the direct invariant calculation

Checkpoint: October 6, 2026, 9:46 p.m. America/Los_Angeles (October 7, 04:46 UTC). Completion estimate for this bounded priority audit: 100%. This adds to, and does not revise, `AUDIT.md` and `PUBLICATION_ELIGIBILITY_ADDENDUM.md`. It assesses attribution and duplication; mathematical validity is governed by the separate proof audits.

## Exact proposed contribution inspected

I read `notes/classical_bridge/DIRECT_BETTI.md`, `notes/classical_bridge/special_s/PROOF.md`, and the manuscript's direct-calculation section. The reviewed versions and hashes are pinned in `direct_computation_source_manifest.json`. For OpenAI's exact group

\[
\Gamma=F(a,b_1,\ldots,b_{99})*_{J}(J\times\langle t\rangle),
\qquad J=\langle b_1,\ldots,b_{99},w\rangle,
\qquad w=ab_1ab_2\cdots ab_{99}a,
\]

the additional proof establishes injectivity of the displayed presentation's cellular boundary, asphericity of its 101-generator/100-relator presentation complex, and \(\beta_n^{(2)}(\Gamma)=0\) for every \(n\geq0\). It uses an elementary 100-regular-tree proof of injectivity of \(S=1+u_1+\cdots+u_{99}\), an explicit triangular Fox boundary, and von Neumann dimension. It does not use either cost estimate. This is substantively a different proof from the earlier public limit \(0\leq\beta_1^{(2)}(\Gamma)\leq99/M\to0\).

## Attribution and already available mathematics

| Component | Prior record and attribution | Assessment of the note's contribution |
|---|---|---|
| Exact group, word, amalgam, and both action constructions | OpenAI family 259, Theorem 1.1 and group definition | Inherited construction; no new group or fixed-price discovery |
| Free basis \(a,u_1,\ldots,u_{99}\), with \(u_i=u_{i-1}ab_i\) and \(b_i=a^{-1}u_{i-1}^{-1}u_i\) | **Already explicitly proved** in OpenAI `build/finite-models.tex`, proof of `models:sequence`, section 5.2, lines 222–229 of the pinned clone | Recall and check this source observation; do not identify it as new |
| Injectivity of nonzero \(S\in\mathbb CF_{99}\) on \(\ell^2(F_{99})\) | A special case of Linnell's 1992 analytic zero-divisor result for right-orderable groups, hence free groups | The elementary tree argument is a self-contained verification of a known special case, not a new general operator theorem |
| Fox boundary formulas | Fox's free differential calculus, 1953–1954 | Concrete calculation for the specified relators; no new calculus |
| Kernel/dimension argument and passage from a contractible universal cover to group invariants | Classical Hilbert-module and CW-complex facts | Explicit application and complete dependency record |
| First-Betti vanishing and relation-level strictness by the cost limit | Explicitly public in Kriebel's October 6 preliminary triage; comparison/action invariance due to Gaboriau; general fixed-price implication already in PSV Remark 6.6 (2018) | No new theorem-chain deduction or priority for that implication |
| Cost-independent full-degree vanishing and asphericity via this triangular boundary and tree proof | No identical group-specific calculation found in the inspected source/corpus/primary chain or bounded current searches | Additional checkable proof content, without a certified originality claim |

The source basis observation is visible at this [pinned source location](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-group-without-fixed-price-October-5-2026/build/finite-models.tex#L222). The manuscript now expressly credits it.

For the operator comparison, [Linnell, *Zero divisors and L²(G)*](https://personal.math.vt.edu/linnell/research/zerol2.pdf), *C. R. Acad. Sci. Paris* **315** (1992), 49–53, Theorem 2, printed p. 50, proves that the analytic zero-divisor property passes through a right-orderable quotient; taking the kernel trivial yields the right-orderable case. This covers the free subgroup used here and then transfers to the ambient group by the coset decomposition. The paper records submission March 3, 1992 and acceptance April 22, 1992; those are not inferred public-release dates. The alternative citation does not become a dependency of the elementary proof. [Fox II](https://www.maths.ed.ac.uk/~v1ranick/papers/fox2.pdf), *Ann. of Math.* **59** (March 1954), 196–210, section 2, develops the presentation matrix, and section 7 connects it to topology. Fox I is *Ann. of Math.* **57** (May 1953), 547–560, [DOI 10.2307/1969736](https://doi.org/10.2307/1969736). The classic inputs must not be advertised as new machinery.

The full-degree conclusion also should not be advertised as a newly discovered invariant property solely because the source lacks the words “Betti” or “aspherical.” Standard aspherical graph-of-spaces arguments apply to this injective amalgam and supply a finite two-dimensional classifying space of Euler characteristic zero. Combined with the already available first-Betti vanishing from the cost upper bound and Gaboriau, this gives all-degree vanishing by the L² Euler formula. Thus the all-degree result is effectively available by another predictable combination of known arguments. The direct proof adds independence from **both** cost estimates, and explicitly verifies the particular presentation, rather than creating priority by changing the degree range.

## Current sources and search limits

The OpenAI public `main` and `HEAD` remained `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in the final read-only remote check. Family 259's source, README, INPUTS and bibliography were inspected; they contain no Fox calculation, L²-Betti computation, or asphericity assertion. Precise corpus searches for the identifying \(b_{99}\) word locate only family 259's introduction, group-actions and finite-models files. General cost/Betti and adjoining subject searches were already recorded in `AUDIT.md`; they did not identify the same group-specific direct calculation. The final web searches included the exact manuscript title, “rank-100 amalgam,” the proposed note title, and combinations with Betti/Fox. They found the public release catalogue and unrelated material, not the concrete proof. This is a bounded negative search, not proof that no other unpublished, unindexed, or differently named argument exists.

The researcher's public [checkpoint `982e42b5c7b7027506696bbf34855ad83d51c1c6`](https://github.com/AlecKriebel/Math/commit/982e42b5c7b7027506696bbf34855ad83d51c1c6), committed October 7 at 04:31:09 UTC, contains the initial audit ledgers and project skeleton, but neither direct-proof file nor a manuscript. The earlier triage commit and exact disclosed conditional proof remain acknowledged as described in the eligibility addendum. Publishing the finished version is continuation of that same public research record, not a fresh independent claim.

The final API and primary-PDF retrieval timestamps and SHA-256 values are in `direct_computation_web_manifest.json`. In particular Linnell's PDF hashes to `1561bc878d8c2587660c8fb080b63bff617922565683f79986c6b5bcc388ec76`, and Fox II to `db9dc64a872fb13720768fd5fa62595dd8637ac173a6f47901086d76056cab0f`. Full third-party PDF inspection copies remain excluded from publication by the audit directory's ignore rules.

## Concrete recommendation

**Qualified go for the expanded, accurately attributed consequence and verification note, provided the positive cost input and final package independently pass their mathematical reviews.** The direct proof meets the extra-content condition identified in the prior addendum: the final proposed proof package is not merely a restatement of the publicly disclosed three-line consequence. Its concrete additional product is a complete cost-independent cellular/operator computation for the exact group, an asphericity verification for the exact presentation, and an auditable all-degree statement. These are useful recorded proofs even though their methods and the general consequences are classical. The rational η and source-validation certificates are supporting reproducibility contributions.

This is a contribution assessment for the user's requested consequence note, **not** a certification of first priority, a new general theorem, or an independent solution of fixed price. Use “direct computation,” “alternative proof,” “expanded consequence and verification note,” and explicit attribution. The current title and introduction are consistent with that scope; retain the earlier triage citation and source basis citation. A useful description is: “We explicitly verify L²-acyclicity and asphericity for OpenAI's amalgam without cost inputs, and record the cost–Betti consequence of its Bernoulli cost estimate.” No “first” claim is justified by this audit.

If the Bernoulli lower bound fails or has an unresolved material gap, the full claimed cost–Betti solution must be withheld; the separately verified invariant computation survives as a narrower theorem. The direct calculation cannot validate a cost lower bound. No external communication, repository mutation, release, or deposit was performed by this audit.
