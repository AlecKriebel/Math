# Descriptor-cache scope failure

Status: **FALSE AS GRAPH-BOUND CERTIFICATES**

The first complete schema-3 `n=3` hard cover cached a Fourier descriptor by
`(selected_port_count, standard_mixed_code)`.  Distinct rooted presentations
can share that semi-directed code while inducing different raw edge-variable
orders.  A state then cited a sign-equivalent but variable-permuted sparse
polynomial generated from another presentation.

The strengthened primary replay found the first substantive mismatch at:

- state `009adfdae5bb372e37afb5eed5cfd97b60a872afef0a6fa09c0c3eeef492980c`;
- target graph `83fbeab153b433dea88528707b25a74898a924b90b1eff000c5a7c10257c8dd8`;
- six selected tensor ports, quartet chunk `5`, invariant `50`;
- stored polynomial `3b0d0cacc30fe4eec7f5db9927c1f6f7d69f5192de9743db4c99e9c66a41cae6`;
- regenerated exact hash
  `07014184f631b5e7bc9dca1a8c93a0ae25ac0a0a7e9aa89295a43bb89bc09e29`;
- stored exact hash
  `e53478b6c8595bbdf39dcafea73bf788327aaca0ebf6702eef7d3677c77e9b44`.

Both polynomials have two terms and are related by presentation-dependent
variable transport; that observation does not repair the required chain from
the recorded graph to the recorded polynomial.  All four generated `n=3`
shards, their merge, and compact-probe runs started from the superseded base
are preserved here and may not be consumed by an active verifier.

The producer correction keys the descriptor cache by the exact rooted graph
content ID.  All affected artifacts must be regenerated and independently
replayed.

## Superseded bulk-stream retention policy

The following large, deterministically generated bodies were removed on
2026-08-10 to protect active exact computations from disk exhaustion.  They
were already quarantined by the failure above, are not inputs to any active
verifier, and can be reproduced only by deliberately checking out the
superseded producer.  Their SHA-256 digests preserve an unambiguous audit
record:

```text
8255a37ff62554f2c98ae57771778b7a469e1a423b0b7cda917aab54f7384090  schema3_n3/hard_cover_n3_schema3_n3_full.jsonl.gz
7836bc63958b2ca9704b284518b1797598c13770304f542aaf6855125a32e7c2  schema3_n3/hard_cover_n3_schema3_n3_s0.jsonl.gz
2722b4b801212c9f758f01b647314c2a83b1c62e6b5f51eae205a69b6f950ac7  schema3_n3/hard_cover_n3_schema3_n3_s1.jsonl.gz
f22b2e01da00d0778d9d754b54d29d565e727328e2fed22c24dbf6e2f885acba  schema3_n3/hard_cover_n3_schema3_n3_s2.jsonl.gz
9363ccb42155a9ed719bfc9d48f0aea267698ea516e6a71edb68a87f3787be4c  schema3_n3/hard_cover_n3_schema3_n3_s3.jsonl.gz
ef87bd729749bcc50f694b01bce91f5050da62230137e1a800c6a403d679bfee  superseded_probe_outputs/probe_extension_bindings_theta2_schema3.jsonl.gz
0b9513a5462c2893171f273933c2ed25d669cee493731d8ecb0199578fb5b862  superseded_probe_outputs/probe_extension_states_theta2_schema3.jsonl.gz
```

The small summaries, graph inventories, polynomial dictionaries, and this
failure witness remain preserved.  Absence of the listed bulk bodies is
therefore intentional and must not be interpreted as a successful replay.
