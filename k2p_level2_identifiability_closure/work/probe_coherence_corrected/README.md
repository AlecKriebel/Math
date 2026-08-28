# Corrected all-primitive probe coherence

This directory is the promotion candidate for the one-/two-port probe theorem.
The earlier package in `work/probe_coherence_closure` is retained only as
revoked counterexample evidence after its rooted restriction oracle was shown
to misclassify exact graph relations.

The build here consumes only clean corrected primitive releases and the
independently replayed 176-anchor input contract.  No rooted three-leaf type is
permitted to select or certify a separator.

## Referee replay

From the repository root, run:

```bash
.venv/bin/python work/probe_coherence_corrected/build_probe_coherence_corrected.py
.venv/bin/python work/probe_coherence_corrected/verify_probe_coherence_corrected.py
.venv/bin/python work/probe_coherence_corrected/verify_site_transport_partition.py
.venv/bin/python work/probe_coherence_corrected/run_probe_coherence_mutations.py --output /tmp/k2p-probe-mutations.json
```

The first command is the full primitive-graph regeneration (about 46 minutes
and 0.45 GiB RSS on the reference M1 run). The verifier streams every primary
ledger and independently replays stored exact Bernstein algebra in about 17
seconds and 0.07 GiB RSS. The mutation suite targets omissions, parents,
transports, order, the global triangle, algebra, optimized mode, hash-seed
stability, same- and conflicting-valued duplicate JSON names, and
noncanonical compressed rows. The separate site-transport audit reconstructs the unique edge-map
partition directly from the frozen input contract and exact transport ledger;
it proves that every incompatible site pair is quartet-separated and that
every compatible pair is either an exact relation or a direct full-map
`T_i` separation.

The mutation runner requires a caller-owned output outside the project tree.
Maintainers may reseal only its exact canonical report by naming that path
with `--output` and adding `--allow-authoritative-output`; routine referee
replays should always use a disposable external path such as the one above.

Primary artifacts are the summary certificate, one-port ledger, two-port
parent inventory and ledger, exact-transport ledger, parent-restriction
ledger, and separation-proof registry. `PROOF.md` states the theorem and the
segment/order/one-global-triangle assembly argument.
