# Repaired anchor-universe audit

## Verdict

The former anchor-universe condition is closed. No mandatory correction was
found.

## Non-four derivation

- `anchor_universe/generate_non_four_anchor_universe.py` imports the active
  graph grammar but not the 176-row contract. It enumerates 13,440 primitive
  cycle directions, 536,364 cycle restorations, and 2,946,240 theta-2
  directions, deriving exactly `1+36+96=133` rows.
- `anchor_universe/independent_non_four_core.py` contains its own literal
  primitive grammar, graph construction, validity predicates, root
  suppression, exact mixed-graph relation test, and restoration enumeration.
  It performs no file read and imports neither producer nor atlas.
- `verify_non_four_anchor_universe.py` completes that independent derivation
  before opening the producer artifact and compares all 133 semantic rows and
  both graph hashes. Only afterward does the final crosswalk open the frozen
  contract as a regression target.

The two implementations necessarily encode the same mathematical five-core
grammar. They do so in separate files with no shared module or result. This is
adequate implementation independence, though not an independent proof of the
handwritten primitive-core theorem.

## Four-port handoff

- The independent full-four core reconstructs all 405,216 presentations
  before opening the frozen contract.
- `verify_complete_anchor_crosswalk.py` reuses that independent core (so this
  is not a third implementation) and exhausts all 144 raw equality parents.
- Exact graph-pair transport maps those parents to 26 direct seeds.
- All 1,260 first-restoration requests map to 161 existing one-port rows.
- The 12 equality continuations generate 96 second requests and 64 unique
  two-port keys; every request is separated there.
- Eight additional physical five-port presentations outside the 17 restored
  serialization rows are four triangle one-port descendants, represented
  twice each. They are explicitly bound rather than omitted.
- Total descendant obligations are `1,260+96=1,356`, with zero unmatched.

Thus the 43 rows are correctly described as 26 direct plus 17 restored
**designated serialization rows** and as a complete generating handoff. The
paper does not falsely claim they are a quotient of every raw presentation.

An independent pairwise exact-map spot check found nine direct graph-pair
classes with sizes `[2,2,2,2,3,3,4,4,4]`. The crosswalk asserts the count but
does not explicitly assert pairwise distinctness of its nine chosen IDs at
lines 853-856; adding that assertion would be optional hardening because the
count is not load-bearing for coverage.

## Marginalized-incoming theta reconciliation

The clean-room core enumerates all 176 excluded parents and every 424 fully
physical path, with restoration-depth census `56+176+192`. It checks 984
nonempty prefixes, restricts each terminal after removal of the incoming
label, and obtains 15 canonical seed-pair classes. The separate reconciliation
then transports attachment endpoints through the frozen candidate profiles
and requires 66 exact isomorphic one-port ledger rows and 66 relation classes.
All 424 paths map; none is discarded or unmatched.

The reconciliation reuses the clean-room core and the four-port crosswalk
reuses the independent full-four core. These shared-code boundaries are
accurately disclosed and do not undermine the producer-versus-verifier
independence actually claimed.
