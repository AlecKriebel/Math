# Independent corrected-probe audit

This directory is a clean-room consumer audit of the frozen corrected probe
package in `work/probe_coherence_corrected`.  It never imports the probe
producer or its verifier.  The graph audit imports only the separately frozen
primitive-input reconstructor, rebuilds every physical graph, and then applies
the public ledgers as untrusted claims.

## Result

`independent_probe_graph_audit_certificate.json` is **PASS**, semantic payload

`65160636abfa33de47136a222081ac70bd7b6fae0e029b7a7c379e2d8653df74`.

It certifies:

- 176 primitive anchor paths, 39 graph-pair-plus-transport classes, and 2,206
  physical sites on each side;
- all 29,964 one-port rows and all 544,571 two-port rows;
- the exact site-map partitions
  `27758 incompatible quartet / 2206 compatible` and
  `511266 incompatible quartet / 33305 compatible`;
- all 67,741 stored exact transports, 4,379 parent restrictions, 638 quartet
  certificates, 156 direct full-map `T_i` certificates, and 118 exact
  Bernstein strict-sign polynomials;
- all 32,729 reverse-order marginals and all inherited ordinary-triangle
  transports, with zero new triangle, unresolved row, or incoherence; and
- 12/12 adversarial mutations rejected, including omission, wrong parent or
  site, wrong reverse map, broken triangle, reassigned quartet or `T_i`
  certificate, bad restriction/map/hash, and a revoked rooted-cache field.

The primary source payload is
`674853fa730c4f54b9ba264d539a51591c8b926ad444195e68df086c26f83825`.
Exact byte hashes are recorded in the certificate and `AUDIT_REPORT.md`.

## Resource distinction

The official reproducibility path remains the low-memory package path: its
builder used 451,903,488 bytes peak RSS (about 0.452 GB) and its verifier used
about 72 MB (about 0.072 GB).  This auxiliary clean-room audit deliberately
holds 67,741 public map records plus 2,107 reconstructed equality parents and
canonical-class graphs in memory so it can apply every map to independently
rebuilt graphs.  Its measured peak was 2,181,349,376 bytes (2.181 GB decimal)
and runtime was 617.91 seconds on the M1 reference machine.  It is an
additional adversarial audit, not the referee package's required replay path.

The audit enforces a streaming Fourier cache: graph-specific pullbacks and
switch states are discarded after each parent.  This prevents linear growth
and keeps the run safely below the 4 GB audit guard.

## Run

```text
python3 work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py
```

The output JSON must have `"status":"PASS"`; any missing row, hash drift,
wrong relation precedence, broken witness, orphan record, nonzero unresolved
gate, or surviving mutation fails closed.
