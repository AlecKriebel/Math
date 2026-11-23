# Interval composition and general order-nine verification

Row 1754 / problem 3276 / OPG-1808. 12 October 2026 UTC.

Status: unsolved. This records at least three confirmed substantive passes; the lifetime attempt count is unknown. Audit, recovery, editorial preparation and integration do not add substantive passes. This is not a final-pass claim.

The target concerns a nonempty finite tournament colored with at most three colors: either a directed cyclic rainbow triangle, or a vertex from which every other vertex is reachable by a directed monochromatic path. The path color may depend on the destination. A transitive rainbow triple does not meet the triangle alternative. The universal vertex is an outgoing source.

The accepted new results are:

- General finite verification through order nine. General order nine covers all 369 rotation/global-color cycle-word orbits and every surviving chord branch, using independently reviewed interval-safe propagation. General orders ten and above remain outside the finite conclusion.
- All-size soundness and termination of a necessary interval-propagation rule that distinguishes possible actual interval arcs from global virtual paths.
- Exact color-by-color reachability and universal-source formulas for uniform colored substitution, including positive-length monochromatic quotient return cycles.
- Exact cyclic-rainbow transfer, substitution closure, colored-primeness of every induced-minimal counterexample, and recursive quotient-core sufficient classes.
- A separately labeled deduction combining the accepted finite bound nine with the already accepted parameterized whole-core and recursive quotient-core theorems. Empty quotient cores need no finite computation.

The periodic result remains only the previously covered lengths 3, 6 and 9. No new periodic-length exclusion is claimed; length twelve and above remain outside scope. The unrestricted target, a general maximum order of a minimal counterexample, and the strict three-color-periodic source problem remain unresolved here. There is no novelty, priority, human peer-review, literature-exhaustiveness or formal proof-assistant claim.

## Reading guide

- [Complete structural proofs](STRUCTURAL_PROOFS.md), [complete structural audit](STRUCTURAL_AUDIT.md), and [complete structural proof review](STRUCTURAL_PROOF_REVIEW.md)
- [Complete finite-search proofs](FINITE_PROOFS.md), [complete finite audit](FINITE_AUDIT.md), and [complete finite proof review](FINITE_PROOF_REVIEW.md)
- [Separate bound-nine deduction](BOUND_NINE_DEDUCTION.md), [dependencies and historical scope](ACCEPTANCE_AND_DEPENDENCIES.md), [verification limits](VERIFICATION_SCOPE.md), and [examples](EXAMPLES.md)
- [Unchanged second-edition introduction](../3276_tournament_partials_20261012/README.md), [prior core proof](../3276_tournament_partials_20261012/STRUCTURAL_PROOFS.md), and [complete scholarly source ledger](../3276_tournament_partials_20261012/SOURCE_LEDGER.md)

The earlier public edition remains unchanged in the companion directory. Its order-eight and two-pass statements describe that historical edition. Current bounds and pass accounting are stated here. The original new structural proof itself used only bound eight, and that premise is preserved in full. It has not been silently rewritten to claim it established order nine.

Only new authored prose, audits, examples, public scholarly metadata and identities of files actually distributed here are included. Source PDFs and copied third-party source text are not distributed. The public manifest records this edition's actual files; programs, raw search datasets, operational receipts and undistributed identities are excluded. The preparation has not changed a repository, draft pull request or queue.
