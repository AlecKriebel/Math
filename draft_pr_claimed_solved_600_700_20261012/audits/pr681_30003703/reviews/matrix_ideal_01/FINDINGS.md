# Matrix/ideal adversarial findings

**PASS. Mandatory findings: 0. Optional findings: 0.**

The universal matrix identity, degree accounting, actual ideal-power memberships in Satoh's component-function algebra, source definitions, and all-entry action bridge are valid as written. No completion-to-ideal, trace-only-to-component, degree-index, rank, or rational-to-integral substitution was found. The proof depends on commutative coefficients for its matrix identity and arbitrary associative coefficients only for the filtered commutator lemma; those uses are correctly separated.

A harmless strengthening emerged: the degree-five identity holds for every 2×2 matrix X, Y, Z, without a traceless restriction. Cayley–Hamilton gives X[X,Y]+[X,Y]X=tr(X)[X,Y], which yields the same cancellation. The existing traceless proof is sound and needs no change. This observation is recorded as additional mathematics, not an optional correction.

Twenty-one independent exact controls pass in normal and optimized Python with byte-identical outputs. They use a fresh Gauss-coordinate universal finite quotient and SymPy polynomial arithmetic; neither original verifier is imported or executed. All four component entries of w vanish modulo the sixth augmentation power, all four entries of v modulo the seventh, and every next-degree entry is nonzero in the universal model. The controls reject premature truncation, omitted/replaced brackets, size-three extensions, and noncommutative coefficient generalizations. The symbolic identities are over the integers and apply to nilpotent/nonreduced and positive-characteristic bases without division.

Fresh primary PDFs were obtained and hashed. Complete printed OWR pages 88–89 were visually inspected after new rendering. arXiv v2 sections 2–4 and Theorem 6.3 were checked against both downloaded PDF text and primary HTML. The exact function algebra and plus-one indexing agree. No literature priority audit was performed; no current-openness or novelty certification follows.

Strongest verified conclusion: the full displayed counterexample theorem is valid in the stated rational SL2 component-algebra setting; the principal independently computed artifact here is the universal identity/ideal bridge. Exact remaining gap in this family: none. Historical priority remains outside this task and must be separately audited before promotion.

See DERIVATION.md for every ring map and inference, MATRIX_CONTROLS.normal.json for exact output, REPRODUCTION.json for execution bindings, and SOURCE_BINDINGS.json for sources and inspection limits. No native file was changed, no PR/Git/cloud mutation occurred, and no person or other shard was contacted.
