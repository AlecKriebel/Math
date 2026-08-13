# Disposition of the independent adversarial review

The read-only adversarial review returned `ACCEPT_PRIMITIVE_GATE`, with no P0
or P1 finding. Its original report is preserved verbatim in
`ADVERSARIAL_REVIEW.md`.

The four P2 observations were handled as follows:

1. The ambiguous `root_edge_indices` field was replaced by intrinsic mixed
   edge records in `root_edges`. These records are independent of any
   separately serialized edge ordering.
2. The p7 tensor-probe scope is now explicit in `EXHAUSTIVENESS.md` and the
   manifest. The exact complete-coordinate compiler remains available; no
   complete-tensor commitment is claimed for p6 or p7.
3. `mutation_tests.py` now accepts `--fixture-port-count`; release replay runs
   it against both p4 and p7 certificates.
4. Parameter-permutation witness verification now recomputes and binds the
   source/target reticulation normalizers and checks that the switching map is
   induced by their permutation/flip actions.

The strengthened mutation suite also changes relation edge transports and
inheritance-parent transports. Each mutation must be rejected after all
superficial record hashes are resealed.

