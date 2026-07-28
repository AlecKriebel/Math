# Independent evidence: signed-balance endgame

Date: 2026-07-28 PDT

## Strict clean-room replay

Command:

```text
python3 -I -B -W error \
  reviews/signed_balance_hostile/independent_check.py
```

Run from `gamma_theta_eternal_domination/`, the command exits zero and
prints a JSON object with verdict `PASS`.

- stdout bytes: `18079`
- stdout SHA-256:
  `e235d75088be80ca4ecd2a2f2bb58cab39bb538c8d0072a26ed1d92e84af78e7`
- checker SHA-256:
  `cdc73dbb22584dc385055c89c1283c1232bf6ba8dfd6b768de4ae2cf9e89883f`

The checker imports no candidate module.  It:

1. reads the frozen candidate and accepted dependencies only to bind
   their exact hashes;
2. reconstructs type orbits using first-occurrence normalization rather
   than the candidate's type-permutation implementation;
3. removes small words by directly testing projection bipartiteness and
   universal side-purity on the literal cycle;
4. checks all chirality/color rows, including all 48 ordered
   transversal-triangle rows;
5. verifies the length-six equality pattern on all 27 assignments and
   checks that the qualified-pair equality graph is connected at every
   length from 7 through 200;
6. reconstructs all six attack branches in a semantic maximal-response
   model; and
7. independently checks the complete witness-collision partitions.

## Frozen candidate replay

Command:

```text
python3 -I -B -W error \
  math/working/signed_balance_endgame/verify_symbolic.py
```

- stdout bytes: `23135`
- stdout SHA-256:
  `da17105109964985501a0bd36aef4013f90b01db2f88d1542d2ed9b18138015e`

This matches the value frozen in the candidate manifest.

## Independently reconstructed finite outputs

The unbalanced type-word orbits are:

```text
length 3: 000, 001
length 4: 0012
length 5: 00000, 00001, 00011, 00101, 00102, 00121
```

Direct semantic bipartiteness and side-purity tests leave:

```text
0012, 00011, 00101, 00102, 00121
```

The independently replayed attack branches are:

```text
0012
00011
00121
00102
00101 with coincident transversal witnesses
00101 with distinct transversal witnesses
```

In the coincident `00101` branch, the attack at `u` has no legal
retained response: its only unblocked successor shape is `{q,u,r}`, and
that triple misses the coincident witness `t`.  This is semantically
equivalent to the candidate's reductio wording “closure forces the
shape, which is nondominating.”

## Monotonicity boundary

The independent attack audit treats every unspecified template pair as a
graph edge in \(G\), hence as a permitted guard move.  This maximizes the
set of possible responses.  Every blocked move and every missed-vertex
certificate uses a displayed literal complement edge.  Replacing an
unspecified \(G\)-edge by an extra complement edge can only remove a
guard move; it cannot invalidate any displayed miss.  Therefore the
symbolic attack trees are robust under every allowed set of extra edges.

