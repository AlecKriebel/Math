# Distance from Eliahou's published seed

The published 64-modular quadruple has only 13 nonzero correlation lags, but
its base-sequence margins are far from the exact norm shell.  This note gives
a mechanically checked local result without fixing `q`, choosing a canonical
margin shard, or applying a distance-changing symmetry quotient:

> No exact `BS(84,83)` lies within raw labeled Hamming distance 18 of
> Eliahou's published base quadruple.

This is a finite local exclusion, not a nonexistence result for `BS(84,83)` or
`H(668)`.

## The first radius-eight obstruction

For one sequence, ordinary and alternating sums `(S,T)` determine the sums on
its even and odd coordinate classes:

```text
E = (S+T)/2,   O = (S-T)/2.
```

Changing a sign changes exactly one of `E,O` by two.  Therefore the minimum
number of flips needed to reach a target pair `(S,T)` is determined exactly
by the two class-sum differences.

`verify_variable_q_seed_radius.py` enumerates every raw labeled image of all
288 exhaustive canonical margin shards under independent sequence negations,
the two equal-length swaps, and the safe even-sequence reversals.  Among all
such necessary exact margin vectors, the unique closest target is the raw
image of shard 287

```text
A (-18,18),  B (0,0),  C (3,1),  D (-1,-3),
```

at Hamming distance eight from the published base quadruple.  It changes only
the odd-coordinate sum of `A`, from `-2` to `-18`, so every minimum repair
must flip eight positive odd coordinates of `A` and no other signs.

Eliahou's base quadruple already satisfies all 83 standard base-sequence quad
products exactly.  Each paired-endpoint long quad contains exactly one odd
coordinate of `A`; hence those eight forced flips occupy eight distinct quads
and toggle eight correct products.  The unique minimum margin pattern is
therefore parity-impossible.  Reproduce this first obstruction with:

```sh
python3 verify_variable_q_seed_radius.py
```

## Dependency-free margin-plus-quad radius

`verify_variable_q_seed_quad_radius.py` generalizes the preceding argument.
For each raw margin target within a requested radius, it computes the minimum
number of flips that attains the eight coordinate-class sums while preserving
every mandatory endpoint-quad product.  Its dynamic program processes the 42
long and 41 short endpoint quads independently; the two unpaired central
short signs are correctly left unrestricted.

The transition from the seed to any exact base sequence must flip an even
number of signs in each endpoint quad because the seed already has the exact
quad products.  For a local delta, retaining only its cheapest realization is
safe because the question concerns a Hamming ball.  Long and short minimum
costs then add.

The standard-library calculation gives:

```text
radius 13: 85 raw margin targets, 0 margin-plus-quad survivors
radius 14: 235 raw margin targets, 18 survivors in shards 0, 6, and 24
```

The radius-14 survivors all have margin distance and quad-preserving distance
exactly 14.  They are only necessary-condition objects, not base sequences.
The implementation is checked against exhaustive brute force on small even-
and odd-length fixtures.  Run the maximal dependency-free exclusion with:

```sh
python3 verify_variable_q_seed_quad_radius.py --radius 13
```

## Layered frontier certificates through radius 18

`search_variable_q_seed_frontier.py` decomposes the remaining finite frontier
by raw margin target.  Every model fixes all ordinary and alternating sums,
keeps the raw seed-distance interval, retains every endpoint-quad product, and
adds the exact norm identity at primitive 3rd, 4th, and 6th roots.

The small quadratic norms are encoded by exact allowed-value tables rather
than general multiplication constraints.  Rows with norm above 334 are
impossible because four nonnegative contributions sum to 334.  Fixed margins
also expose exact classwise flip-direction budgets.  For the unique hard
shard-287 radius-16 target, a checked consequence states its rigid structure:
eight positive odd `A` signs flip, and exactly one partner in each selected
quad flips.

The completed finite runs are:

| Scope | Margin-plus-quad models | Result | Peak RSS |
|---|---:|---|---:|
| complete raw ball, radius 16 | 197 | all `INFEASIBLE` | 148 MB |
| exact distance-17 shell | 276 | all `INFEASIBLE` | 164 MB |
| exact distance-18 shell | 823 | 811 root-infeasible; 12 root survivors eliminated by length 7/14 | 176 MB |

The final JSON SHA-256 digests are:

```text
4b38d392d9b48e9ee3d9466813863d4ab9ca59c513245469fa5afeb39ef39a0f  radius16
a0c842a2bb01696874cb911ac8d2ba41d1fd5467323b1e9e58d833a24d51bf8e  shell17
```

The shell calculation skips 161 even-parity targets because a fixed margin
vector fixes Hamming-distance parity; those targets cannot occur at odd
distance 17.  Combining the complete radius-16 result with the exact shell
therefore excludes the complete raw ball through radius 17.

At exact distance 18, 823 parity-compatible margin-plus-quad targets remain.
A sequence of compatibility-checked, one-worker root-layer runs classifies
them completely:

| Stage | Selected targets | New `INFEASIBLE` | Root witnesses in stage | Remaining timeouts |
|---|---:|---:|---:|---:|
| initial 0.5-second screen | 823 | 525 | 7 | 291 |
| unresolved targets, 2 seconds | 298 | 209 | 11 | 78 |
| timeouts, 5 seconds | 78 | 37 | 1 | 40 |
| modulo-12 bit symmetry, 5 seconds | 40 | 2 | 0 | 38 |
| exact quad-orbit quotient, 5 seconds | 38 | 32 | 0 | 6 |
| final quotient models, 30-second cap | 6 | 6 | 0 | 0 |

Thus the root layer proves 811 targets infeasible and decodes exactly 12
root witnesses.  Ordinary length-seven compression proves 9 of those target
models infeasible.  Primitive-14 compression—equivalently length-seven
compression after coordinate alternation—proves the remaining 3 infeasible.
Every exact `BS(84,83)` must satisfy all of these identities, so the complete
distance-18 shell is empty.

The orbit-count encoding is an exact quotient, not an added necessary
condition.  At the root-only layer, margins and primitive 3rd/4th/6th roots
distinguish coordinates only modulo 12.  Endpoint quads having the same
oriented seed signs and endpoint residues are interchangeable.  The quotient
stores counts of their eight even-flip patterns, eliminating all permutations
inside an orbit.  A decoded quotient witness is rebuilt as 334 signs and
checked by the same independent integer verifier used for bit-level models.

The nine pinned shell-18 artifact digests are:

```text
2a93ac19108cee6705743f21f8d60e5f0f17a7de2389539141a8a091ef2670ba  root initial
13956042c216c2a28815d2002599a6f0ebcd11921252cfd98ae6859b08156cc7  root unresolved 2s
db7aaa9127a81877c14d8da943736a1390be921c481ff81060481b72defc130e  root timeouts 5s
6b641bbf58f3adc7277522c624a7371c3105884dfbb2f0a16344312c0dc40085  root bit symmetry
6ebb2e43a254881923ace02801a93a62938fc9b1aecf586bcca6866f41024f82  root orbit quotient
10342117cbcb70d39498fd77e7aa206f23fbc69560506e239491124f852f1808  root final six
7730a740560337d1baf6716078d28e99e8f69fc0dea4dacb3775ef0a161a55db  length-7 filter
908b5571034ab2e1542e555281c7ea610903e5d41b5a06792e5986dcbca19f65  length-14 old witnesses
a22c5f51abc466a8ce7cfa46cb44057a5ccedc2e3dc610b8503c3a6f0ae94c6e  length-14 new witness
```

Reproduce the two certificates sequentially with one worker:

```sh
../tmp/hadamard-env/bin/python search_variable_q_seed_frontier.py \
  --radius 16 --small-root-encoding table \
  --time-limit-per-target 2 --max-memory-mb 256 \
  --output output/variable_q_seed_frontier_radius16_root_table.json

../tmp/hadamard-env/bin/python search_variable_q_seed_frontier.py \
  --radius 17 --minimum-distance 17 --small-root-encoding table \
  --time-limit-per-target 30 --max-memory-mb 256 \
  --output output/variable_q_seed_frontier_shell17_root_table.json
```

The final shell artifact was regenerated in one direct run with no resume
dependency.  Its 276 models used 149.806 total solver-seconds; the hardest
model took 9.862 seconds.  The script also supports compatibility-checked
`--resume-from` for future larger shells.  CP-SAT's `INFEASIBLE` statuses
solve exact finite integer models, although this workflow does not emit
independently replayable SAT proof transcripts.

`verify_variable_q_seed_frontier_artifacts.py` independently reconstructs both
selected frontier sets, checks target uniqueness and completeness, validates
all recorded statuses and layer/resource metadata, and pins the JSON hashes.
It checks artifact integrity and aggregation; it does not replay CP-SAT's
infeasibility search.

`verify_variable_q_seed_shell18_artifacts.py` performs the layered shell-18
check.  It reconstructs all 823 targets, verifies every checksum and parent
selection edge, independently rechecks all 12 decoded witnesses, and confirms
that the compression layers eliminate exactly those 12 targets:

```sh
python3 verify_variable_q_seed_shell18_artifacts.py
```

The verifier uses standard integer arithmetic, ran at 39 MB peak RSS, and
does not import OR-Tools.  As above, it does not replay CP-SAT's infeasibility
search or turn the solver statuses into independently replayable SAT proofs.

## Superseded diagnostics

`variable_q_seed_distance.py` minimizes distance in an unsharded relaxation
containing the two margin norms and all quad products.  A 300-second run found
a checked distance-14 relaxation witness, but ended `FEASIBLE` with objective
lower bound zero.  That witness fails all three small-root identities, both
length-seven compression signatures, and most full correlations.  It gives no
optimality bound.

`search_variable_q_seed_ball.py` instead includes all 83 exact aperiodic
equations.  Its initial raw radius-10 run ended `UNKNOWN` after 300 seconds at
251 MB peak RSS.  The decomposed radius-18 certificates above supersede that
undecided diagnostic; the timed-out monolithic run is not cited as evidence.

Primitive-7 and primitive-14 compression layers remain available on the
frontier script and are essential to the shell-18 exclusion.  No exact
candidate has been produced by any seed-
distance calculation.  Any future survivor must still pass all 83 exact base
correlations and full `668 x 668` Hadamard verification.
