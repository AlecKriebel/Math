# Tournament symmetry and endpoint incidence

Row 1754 / problem 3276 / OPG-1808. 12 October 2026 UTC.

Status: unsolved. This is the fourth confirmed substantive pass in the current sequence: at least four confirmed passes, with lifetime count unknown. It is not a final pass. Preparation, audit, editing, and integration add no substantive pass.

The target says that every nonempty finite tournament with at most three arc colors contains a directed cyclic rainbow triangle or has an outgoing vertex reaching every other vertex by a monochromatic directed path, whose color may depend on the destination.

## New accepted partial results

- Every colorwise balanced tournament has every vertex as a monochromatic source. A color-preserving vertex-transitive tournament has one spanning strongly connected monochromatic color when its palette has at most three colors, or at most the least prime divisor of its order. Sharp affine examples and a genuinely nonregular action accompany the proof.
- An explicit family of every odd order at least seven is cyclic-rainbow-free, colored-prime, and full incidence-core, yet has a monochromatic Hamilton cycle. For any fixed bound, sufficiently large members lie outside the prior bounded recursive quotient-core criterion.
- A hypothetical induced-minimal counterexample with fully vertex-transitive global-color-permuting symmetry must have odd order divisible by nine and a strict three-periodic obstruction-cycle word. The structural proof retains the independently accepted through-nine premise yielding order at least 27. Arbitrary periodic words need not induce whole-tournament symmetry.
- Separately, endpoint-incidence propagation and complete general reduced searches establish the target through order ten. Both closure engines cover all 1,002 canonical order-ten words and agree on 9,944,675 DFS states and zero completions. These expensive full runs are distinguished from the three-mode targeted verification suite.
- The accepted parameterized whole-core and recursive quotient-core results now apply at bound ten. This application is a [separate corollary](BOUND_TEN_DEDUCTION.md); earlier proofs and their historical premises remain intact.

## Complete proofs and reviews

The [structural proof](STRUCTURAL_PROOFS.md), [full structural audit](STRUCTURAL_AUDIT.md), and [independent structural proof review](STRUCTURAL_PROOF_REVIEW.md) retain their complete arguments and boundaries. The [finite proof](FINITE_PROOFS.md), [candidate evidence](FINITE_CANDIDATE_REPORT.md), [full finite audit](FINITE_AUDIT.md), and [independent finite proof review](FINITE_PROOF_REVIEW.md) distinguish credited reduction, sound pruning, completed enumeration, and independent checks. [Examples](EXAMPLES.md) give all six fixed structural fixtures, while [verification scope](VERIFICATION_SCOPE.md) reconciles execution modes and incomplete searches.

Read [acceptance and dependencies](ACCEPTANCE_AND_DEPENDENCIES.md) and [source credit](SOURCE_CREDIT.md) for exact attribution and historical boundaries. The [earlier second edition](../3276_tournament_partials_20261012/README.md) and [third edition](../3276_interval_composition_20261012/README.md) are unchanged companion dependencies, not duplicated here. Their historical finite bounds remain correct for their own editions; the current fourth-edition finite bound is ten.

## Remaining scope

General order eleven and above and strict periodic length twelve and above remain outside the completed exclusions. The periodic-twelve feasibility run was incomplete, so it provides no exclusion. Fully symmetric order 27 and above and asymmetric colored-prime full-core cases remain unresolved. No counterexample, novelty, priority, human-review, proof-assistant, or whole-source-proof certification is claimed. This public edition distributes authored mathematical prose, full audits and proof reviews, examples, public scholarly metadata, and identities of these distributed files. It contains no programs, raw enumeration output, or copied third-party source documents.
