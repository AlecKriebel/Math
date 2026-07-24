# Frozen K9 support: exact K10 size audit

No full frozen-support K10 obstruction is claimed here.

The exact orbit-size verifier computes the automorphism group of every one
of the 51 stored K9 representatives by enumerating all \(9!\) vertex
permutations.  It also computes a canonical packed representative, proving
that the 51 orbits are distinct.  Their union has exactly 16,057,440
labeled K9 matrices:

\[
1(90{,}720)+12(181{,}440)+38(362{,}880)=16{,}057{,}440.
\]

If records are grouped by their common K8 restriction, let the group sizes
be \(n_g\).  A complete face-gluing search has
\(\sum_g n_g^2\) ordered pairs.  Since
\(\sum_g n_g^2\geq\sum_g n_g=16{,}057{,}440\), trying the seven colors of
the remaining edge requires at least
\[
112{,}402{,}080
\]
color trials.

The exact packed representation already needs 256,919,040 bytes
(245 MiB) for the support alone.  The K9 implementation pattern would also
need a comparably sized overlap-record array and a large prefix membership
index.  In accordance with the K10 task's growth-control instruction, the
full gluing enumeration was therefore skipped and effort was directed to
the exact direct K10 construction.

This is a precise computational bottleneck, not evidence of extension or
nonextension.  In particular, `frozen_support_size.json` is not a Farkas
certificate and proves no upper bound for spherical codes.

Reproduce with:

```sh
PYTHONPATH=. .venv/bin/python \
  experiments/centered_quarter_k6_rank/k10/verify_frozen_support_size.py
```
