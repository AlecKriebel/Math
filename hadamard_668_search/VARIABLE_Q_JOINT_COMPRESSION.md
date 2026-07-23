# Joint primitive-7 and primitive-14 compression

This necessary-condition layer strengthens the factor-12 compression in
`VARIABLE_Q_COMPRESSION.md` without constructing a large search table.

For each source sequence `X`, define two length-seven vectors

```text
U_r = sum_(i = r mod 7) X_i,
V_r = sum_(i = r mod 7) (-1)^i X_i.
```

The length-83 sequences are padded by a zero at index 83 in both formulas.
`U` is the existing primitive-seventh-root compression.  `V` is the same
compression after global coordinate alternation; it exposes primitive
fourteenth roots because evaluating `(-1)^i X_i` at a seventh root is the
same as evaluating `X` at a fourteenth root.

## Exact cell coupling

The two layers cannot be chosen independently.  In a residue cell, split the
source signs between even and odd original coordinates and call their sums
`E` and `O`.  Then exactly

```text
U_r = E + O,
V_r = E - O.
```

Every long cell and the first six short cells contain six coordinates of each
parity.  The last short cell contains six even and five odd coordinates; the
missing twelfth position is the padded zero.  Enumerating the possible sums
of those two tiny groups gives a complete finite table for each pair
`(U_r,V_r)`, with no relaxation.

If `(A;B;C;D)` is an exact `BS(84,83)`, both compressed quadruples obey

```text
sum_X PAF_UX(k) = (334,0,0,0)_k,
sum_X PAF_VX(k) = (334,0,0,0)_k,   0 <= k <= 3.
```

The second system is valid because coordinate alternation sends every
aperiodic residual `R_k` to `(-1)^k R_k`, preserving its zero set.  The eight
selected shard margins are simply `sum(U)` and `sum(V)`.

## Implementations and scope

`variable_q_joint_compression.py` builds a small CP-SAT relaxation with only
56 cell-sum variables, exact two-column cell tables, and the two compressed
PAF systems.  Shards are processed sequentially with one worker and a default
256 MiB solver cap.  A feasible cell witness proves only that this relaxation
survives; it is not a lift to 334 signs.  An `INFEASIBLE` result would rule out
the selected full margin shard.

The full 334-sign CP model exposes the primitive-14 layer independently via
`--compression-7-alternating`; it can be combined with `--compression-7`.
Both options are exact redundant propagation and remain off by default until
their low-memory benchmark is complete.

A first one-worker shard-213 benchmark used the command below and ended
`UNKNOWN` after 30.005 seconds with 2,640,159 branches.  It peaked at 111 MB
RSS with no swaps.  The run found neither a feasible compressed witness nor
an infeasibility result, so it makes no mathematical elimination claim.

Run one joint shard safely with:

```sh
../tmp/hadamard-env/bin/python variable_q_joint_compression.py \
  --shards 213 --time-limit 30 --max-memory-mb 256
```

The all-representative command is deliberately sequential:

```sh
../tmp/hadamard-env/bin/python variable_q_joint_compression.py \
  --shards all --time-limit 30 --max-memory-mb 256 \
  --output ../tmp/hadamard_668_runs/joint_compression_7_14.json
```

The all-representative scan has not yet been run.  No shard-elimination claim
is made until finite models complete and their decoded witnesses or
infeasibility statuses have been recorded.
