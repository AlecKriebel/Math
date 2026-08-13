# Adversarial review of the fixed-full inventory certificate

## Verdict

**VERIFIED**: finite combinatorial grammar, exact normalized crosswalk of all
5,476 frozen roots, and exact use by the frozen hard-cover streams.

**UNRESOLVED IN THIS PACKAGE**: independent exhaustiveness of the upstream
Fourier-signature collision selection.  The permitted inputs expose only an
opaque source-signature hash; this audit is forbidden to regenerate Fourier
polynomials.

No mismatch was found in the locked source supports, target-completion
grammar, incoming-boundary handling, relative port transports, root object
hashes, or hard-cover root forests.

## Checks performed

1. The verifier imports no project module and uses only the Python standard
   library.
2. The five core records are loaded as data and checked for the exact locked
   core set.
3. Source automorphisms are recomputed from the directed segment multigraph;
   no stored automorphism or topology identifier is trusted.
4. The source-support quotient independently regenerates exactly eight `n3`
   supports and three `theta-2 n4` supports.
5. The target grammar independently generates every choice of core, incoming
   mode, sink mask, minimum repair, ordered segment occupancy, required dummy
   repair/sink role, and relative tensor-port permutation.  Every frozen
   target lies in that grammar.
6. Every root case is rebuilt from its grammatical data, its exact object hash
   is replayed, normalized relation keys are unique, and opaque primitive ids
   are checked for functional consistency in both directions.
7. Every hard-cover relation state belongs to a known root forest.  Forest
   entry states agree exactly with all 5,344 and 132 stored root records.
8. Decompressed stream hashes and independent normalized mathematical-record
   hashes are fixed in the verifier.
9. A complete deterministic crosswalk maps every root id to the full
   normalized decorated relation and forest entry states.

## Adversarial finding

The initial clean-room implementation incorrectly assumed that
`target_dummy_roles` had the canonical order stored inside target provenance.
The first frozen root disproved that assumption.  The role *multiset* is
forced by the completion grammar, but the restoration order is part of the
decorated directed root relation.  The corrected verifier therefore checks
the forced multiset and retains the order in the normalized relation key.
This is exactly the distinction needed to prevent target-only canonicalization
from collapsing nonretaining source-target relations.

## Mutation sensitivity

The mandatory in-memory mutations are all rejected:

- omitted primitive core;
- omitted minimum repair;
- altered selected/marginalized incoming role;
- altered relative port transport;
- duplicated root; and
- deleted root.

See `MUTATION_TRANSCRIPT.txt` for the deterministic transcript.

## Precise limitation

The frozen root schema contains an opaque `selected_signature_sha256`.  Under
the task's prohibition on regenerating Fourier polynomials, no clean-room
inventory verifier can independently decide which members of the complete
combinatorial target grammar should survive that algebraic filter.  This
package therefore reports that exact selection-exhaustiveness claim as
**UNRESOLVED**.  It
instead fixes a normalized mathematical commitment to the selected roots and
proves that their structural grammar and downstream coverage are exhaustive.

This limitation is not a root-id or byte/hash mismatch.  All root ids replay.
Exact byte-level decompressed
stream hashes are checked, and the complete root dictionaries replay their
stored ids.  It is a deliberate separation between combinatorial
exhaustiveness (verified here) and Fourier/pullback exhaustiveness (verified,
if at all, by a separate independent algebra implementation).
