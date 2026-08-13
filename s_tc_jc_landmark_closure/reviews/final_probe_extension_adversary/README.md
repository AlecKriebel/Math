# Independent adversarial review: terminal probe extension

This directory is intentionally independent of both `primary/` and
`reviews/final_hard_cover_cleanroom/`.  Its Python modules import only the
Python standard library.  They do not import either research implementation.

The verifier implements the path-bound terminal-extension contract in
`reviews/final_theorem_logic/TERMINAL_EXTENSION_AUDIT.md`:

1. read every raw allowed base relation, not merely canonical terminal states;
2. recompute every admissible internal blob arc on both sides;
3. require the full Cartesian family of `p` insertions;
4. continue every allowed `p` relation through the full Cartesian family of
   `q` insertions;
5. delete the new label and subdivision vertex and compare with the exact
   parent relation;
6. independently enumerate displayed trees and regenerate exact JC quartet
   Fourier pullbacks;
7. verify graph-bound algebraic witnesses and modular Jacobian-rank
   certificates; and
8. require every allowed child isomorphism or ordinary-triangle map to
   restrict to the single map fixed by its parent.

Following the quarantined primary `n=4` failure, raw state identity also
contains the fixed-full root-case id and exact source and target rooted-graph
hashes.  Child sets are regenerated per raw path; equal semi-directed codes
never authorize a merge across those identities.

The implementation is parameterized by a self-contained JSON relation
stream.  An adapter for the eventual `n=3` and `n=4` hard-cover streams can
emit this schema without sharing enumeration or algebra code with this
review.  Until those final streams exist, `make_fixture.py` creates a complete
two-level triangle fixture that exercises every structural and algebraic
check.

Run:

```sh
python3 reviews/final_probe_extension_adversary/make_fixture.py
python3 reviews/final_probe_extension_adversary/verify_probe_extension.py \
  reviews/final_probe_extension_adversary/certificates/fixture.json
python3 reviews/final_probe_extension_adversary/mutation_tests.py
```

The fixture is a test of the verifier and schema, not evidence for the final
`n=3+n=4` theorem.  The final status therefore remains fail-closed until the
actual hard-cover terminal streams are supplied and pass unchanged.
