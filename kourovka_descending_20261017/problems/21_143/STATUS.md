# Kourovka 21.143 — unsolved in this effort

Checkpoint: 2026-10-17 UTC. Best-guess discovery completion: **8%**.
This subjective estimate is not a probability of either mathematical answer.

The exact question is whether standard finite dyadic Thompson F is
automatic. The official 6 October edition, p.198, and the proposer's
8 October list retain it as open. The bounded priority audit found no
complete resolution; inaccessible or unindexed work cannot be excluded.

Substantial independent constructive, geometric, algebraic and
language-theoretic routes have not resolved the question. No regular
automatic structure or proof excluding every such structure was obtained.

## Strongest partial deductions and attempted mechanisms

- Regular Guba–Sapir normal forms have adjacent representatives with
  length difference 2n+3, synchronous separation at least n+2, and
  asynchronous separation at least (n+2)/2. Exact PL support arguments
  establish the family for all n, separately corroborated computationally.
- The root's rational-recoding proposition excludes any total
  evaluation-preserving rational recoding of that complete language into
  a rational-multiplier presentation, including a graph automatic one.
  Arbitrary new languages and nonrational algorithms remain possible.
- Unary infinite-index codes have a nonregular multiplier; binary index
  compression repairs a small successor slice but cannot be decoded
  semantically to generator representatives by a total rational relation.
  The elementary breakpoint bound |x_i|>=i supplies that obstruction.
- Two naive preorder tree-pair domains and the naive separated ranked-tree
  domain are not regular. Slot-frontier insertion requires a nonregular
  first-return test in the unchanged stream. Local binary/zipped repairs
  do not yet align all canonical blocks or validate all diagrams.
- Bounded prefix rewrites can converge with arbitrarily many steps;
  finite-state tests for individual rules do not supply automatic
  multipliers for the final normal forms.
- Geodesic/near-geodesic obstructions, almost convexity, abelian rank,
  cohomological dimension, centralizers, wreath subgroups, ordinary and
  higher filling, and cyclic distortion were independently investigated.
  No valid general automaticity contradiction was obtained. In particular
  ordinary automaticity does not require geodesic representatives or pass
  to arbitrary finitely generated subgroups. Infinite abelian rank alone
  is not an established exclusion theorem here.

The detailed mechanisms, proofs, exact gaps and primary source scopes are
in approach_constructive.md, approach_obstructions.md,
rational_recoding_obstruction.md, tree_language_audit.md and
priority_20261017.md. No novelty claim is made for these partial deductions.

## Verification

Root independently reran both exact programs successfully: 64 parameters
in each PL family, 8,188 dyadic point checks, 1,365 short words, 203,456
tree pairs and 5,461 negative-exponent vectors. These are finite checks
of formulas and conventions, not a test deciding automaticity. Independent
approach agents reviewed the parametric proofs; a fresh comprehensive
partial-result adversary completed reviews/partial_adversary01.md with no
outstanding substantive objection to the corrected partial claims. Its
independent extra checks used 8,066 direct branch points and 40 quotient
matching cases; all 19 retained source hashes also reproduced.

No candidate was promoted to solved_verified. There is no preprint,
Zenodo upload, DOI or tracker entry for 21.143. No human peer review or
formal proof-assistant verification is claimed.

## Exact remaining obstruction

A positive answer needs a genuinely regular whole-group language and all
exact synchronous equality/right-multiplier relations, or an equivalent
uniform fellow-traveller proof. A negative answer needs a mechanism
applying to every possible regular combing, including nongeodesic ones.
None of the restricted failures supplies that universal step. These
routes are blocked until a materially new mechanism is available.
