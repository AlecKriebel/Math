# First pass integration and acceptance

## Accepted mathematical scope

The main fully labeled rectangular corner-start Hamiltonian-path complexity problem remains unresolved. This edition consolidates exactly one newly documented substantive pass; the lifetime count before this continuation is unknown.

The [orientation proof](ORIENTATION_STRUCTURE.md) establishes unique physical-edge pinning, the invariant phase and three-color projection, absence of projected four-cycles, the necessary area congruence, and singleton/domino residual ambiguity after endpoint-conditioned propagation. Its Boolean formulation is an equivalence only when connectedness of the selected graph is included. The [independent review](INDEPENDENT_STRUCTURE_REVIEW.md) accepts these statements and supplies the delicate rail-cell forcing justification explicitly.

The [4 × 5 obstruction](CONNECTIVITY_OBSTRUCTION.md) proves that even a connected candidate graph plus feasible local orientation and degree constraints need not admit a corner-rooted complete path. Its nonexistence argument is graph-theoretic and covers selectable initial orientation. The [2 × 5 cap obstruction](FILLER_OBSTRUCTION.md) gives a direct alternate traversal that defeats an endpoint-neutral hole-filling claim. The cap is an exact authored counterexample to that local proposal; it is not a general impossibility theorem for all no-hole reductions.

The independent structural review accepts the orientation theorem and 4 × 5 graph proof. The cap's two explicit paths are checked directly from the same roll permutations and included in the exact certificate. This edition's assembly check also verifies the full small-board certificate; it does not present editorial validation as a second independent mathematical review.

## Essential model distinctions

- The rectangle is completely and explicitly labeled. Every cell is compulsory and visited once, including the start.
- The start is a specified corner. The singleton/domino argument is not asserted for two arbitrary endpoint positions.
- The initial state is fixed within each branch; selectable initial orientation means enumeration of the four matching orientations of the specified chirality.
- The other endpoint and its final orientation are fixed before the stated propagation. The unconditioned path problem permits any other endpoint.
- A phase-projected path need not have consistent full orientations at its shared vertices. A projected six-cycle is not a physical rolling cycle.
- Connectedness of all candidate edges differs from connectedness of the chosen solution edges. The latter is indispensable in the exact formulation.
- A fixed-orientation field does not imply a unique global traversal. The older Figure 4 example already disproves that inference.
- Filler preserving one intended transition is only a forward witness. A reduction needs both implications and complete boundary and endpoint control.

## Source attribution and status

The [source audit](SOURCE_MODEL_AUDIT.md) credits Buchin and coauthors for the existing parity and state-graph framework and distinguishes their author-hosted 30-page full version from the CCCG 2007 four-page short version. The landing page's `unrefereed = 1` field is reported as metadata, not promoted to an independent assessment of conference refereeing. No refereed journal status is asserted for the full version.

De Biasi's PDF is dated May 2012, Version 0.03; the author post is dated November 3, 2012. His October 27, 2017 public statement described it as a blog draft not yet cleaned up and submitted for journal review. No later publication status was established by the bounded audit. Its Figure 4 nonuniqueness example is prior literature, independently physically checked here; its blocked-cell cycle reduction was not certified in all interface cases and does not classify the present no-hole path target.

All 270 Figure 4 dash directions in each drawing are reversed relative to the manuscript's definition, while the labels and two cycles pass full-state replay. The convention mismatch is explained without copying a source-derived board or path into this edition. No priority, worldwide novelty, or worldwide openness certificate is claimed.

## Evidence boundary

The authored proof texts and exact small-board certificate are complete. [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json) separates finite proof corroboration, source Figure 4 replay, and negative searches. Exhaustive small tests and bounded generated-board probes establish neither a stronger arbitrary-rectangle theorem nor attainment of residual ambiguity.

[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) binds the public edition except itself. It includes only public-file identities and public-source metadata. Programs, copied third-party texts and PDFs, source-derived board arrays or routes, operational streams, and private coordination are not part of this edition. Public recovery requires only these files and the cited public sources for source-specific claims. Editorial normalization is reversible in separately retained records; it changes no accepted mathematical assertion.
