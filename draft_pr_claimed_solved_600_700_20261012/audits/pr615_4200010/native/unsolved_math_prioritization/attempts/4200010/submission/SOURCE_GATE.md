# Source and repository gate

## Target identity

- Numeric upstream ID: 4200010
- Catalogue identifier: AMR-041-0010
- Catalogue title: The good, the bad, and the ugly
- Queue rank at inspection: 643; live queue showed `queued`, `0/5`.
- Primary source: Oliver Knill's talk *Some intriguing open problems in Hamiltonian dynamics*, dated 19 October 2000, item 10.
- HTML: https://people.math.harvard.edu/~knill/seminars/intr/
- Primary two-page PDF: https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf ; target on PDF page 2.

The upstream catalogue URL https://www.unsolvedmath.com/problems/4200010 was tried first but was inaccessible through the web retrieval tool. Identity was therefore checked against the pinned corpus and the author's primary HTML and visually rendered PDF. The complete pinned record and prior report were read locally; neither is redistributed here.

## Authored target summary and exact interpretation

The requested example is a Hamiltonian flow having positive Liouville volume outside both its almost-periodic invariant region and its region with a positive Lyapunov exponent. The primary wording imposes no Euclidean phase-space, analyticity, mechanical-Hamiltonian, contact-type, or genericity hypothesis. The source distinguishes its existential question from a subsequent guess about weak mixing.

The candidate uses the standard Koopman meaning of an almost-periodic measure-preserving system: every L2 orbit is precompact. This is consistent with the source's cited 1998 spectral paper. The source's reference to KAM suggests possible attention to ergodic components; the candidate establishes failure of almost periodicity on each energy component as well, so it does not rely merely on averaging continuously varying integrable frequencies.

A nontrivial discrete-spectrum factor is not the same as a positive invariant region whose entire Koopman representation is almost periodic. The construction has clock eigenfunctions, but its positive invariant regions also carry a concrete infinite orthogonal orbit. This distinction is material.

## Repository duplicate gate (4 October 2026)

The repository root and queue AGENTS instructions and READMEs were read. The live main branch was `2b18c9302f69afc94288a6dd9135bf0cba87ae28` at the final pre-freeze read. The selected row remained queued 0/5. The state ledger had no ID 4200010 entry. `unsolved_math_prioritization/attempts/4200010` returned HTTP 404. All-state PR search for the numeric ID, title-keyword PR search, and branch search returned no matches. The related-target group file had no matching entry.

These are bounded duplicate checks, not proof that no off-repository prior work exists. No queue command, state mutation, merge, release, DOI action, or outreach was performed.

## Literature and novelty limits

The pinned prior report called the problem open but did not provide a direct proof or a verified complete literature resolution. That report is not a mathematical premise.

Searches checked the exact title and author, 'Hamiltonian ugly set', Hamiltonian skew-shift suspensions, and symplectic mapping-torus constructions. The standard suspension geometry and skew-shift mechanism are classical. The initial alternative route uses classical weakly-mixing area-preserving disk maps; the final proof does not depend on their existence theorem.

Knill's 1998 cited spectral paper was privately downloaded and inspected for context. It does not supply the specific four-dimensional example proved here. No inspected source was found explicitly presenting the target as resolved by this construction. This is a limited search result, not a priority claim or a guarantee that the construction has not appeared before.

The appropriate proposed status is `claimed_solved`: a complete authored candidate for the unrestricted printed formulation, awaiting independent audit. `already_solved` is not asserted on the basis of an unlocated prior exact resolution.
