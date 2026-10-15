# Controlled affine obstruction to sparse jointly periodic growth

Problem 4600045 / AMR-045-0045. Approach 1 of 5.

**UNRESOLVED: no strict-growth example has been constructed.** This packet records an accepted partial exclusion theorem for scalar affine fibres over a shifting finite-symbol control track. Its original target is a surjective one-dimensional cellular automaton with all-period upper exponential jointly periodic growth strictly below its alphabet size.

For every nonempty finite B of size s, every finite field F_q of characteristic p and arbitrary finite-range control functions c,d, the rule

F(a,b)_i = (a_(i+1), b_i + c(sigma^i a)b_(i+1) + d(sigma^i a))

is surjective on the bi-infinite full shift. For each rooted control word a of length k, let r(a) be the zero multiplicity of product_i(t-c_i)-1. The exact count is J_k(F)=sum_a q^(k-r(a)), independent of d. The bound r(a)<=(q-1)p^(v_p(k)) implies nu(F)=sq=N, excluding every map in this family from the requested strict-growth construction.

The full proof includes compactness surjectivity, the shift adjustment fixing control fibres, the affine Fitting decomposition, small rings, extension fields, the positive-characteristic derivative issue, an ordinary-limit refinement for nonconstant one-site coefficients, exact constant-coefficient lower and upper limits, and the binary liminf trap. The independent audit retains a supplementary sharpness argument for q-1.

## Reading order

- [PROOF.md](PROOF.md): complete accepted mathematical argument, attribution and exact remaining gap.
- [AUDIT.md](AUDIT.md): complete mathematical audit and scoped acceptance.
- [SCOPE_REPAIR_LEDGER.md](SCOPE_REPAIR_LEDGER.md): the closed TeX and citation-scope repairs and all adversarial safeguards.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public citations, PDF identities and recorded retrieval/inspection history.
- [PROVENANCE.md](PROVENANCE.md): authorship, editorial changes and acceptance boundary.
- [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): scoped disposition and exact distributed inventory.

The proof and audit are AI-assisted and unrefereed. No novelty, exhaustive literature coverage, external human peer review or proof-assistant certification is claimed. Boyle–Lee's literal cyclic-alphabet linear result is credited; the broader extension-field and controlled-alphabet conclusions rely on the self-contained proof. Arbitrary nonlinear surjective cellular automata remain outside the accepted theorem.

This is a proof-only edition. It preserves Approach 1/5, introduces no additional proof-search turn and changes no queue entry or historical accounting.
