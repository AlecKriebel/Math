# Exact-zero constructor for the LP(333) order-three profile gate

## Status and scope

The constructor now searches the 24 ten-state profile variables with the
strongest exact quotient equation available:

```text
D_j = 0,                         j=1,...,6.
```

The other six nonzero invariant parts are their Eisenstein conjugates under
lag reversal.  Thus these six Eisenstein equations, or twelve scalar integer
equations, are the complete profile zero gate.  The primitive-nine ideal and
the complete characteristic-37 transfer remain in the model as redundant
consistency cuts; the solver no longer relies on the CRT norm gap to infer
zero.

This is a CP-SAT discovery constructor.  It is not a proof-producing SAT/PB
exhaustion.  In particular, even if its operational queue eventually reports
every cube infeasible, that status is not a publication-grade UNSAT
certificate.  Every positive survivor is instead checked by a detached exact
verifier.

No profile survivor, labelled lift, `LP(333)`, or `H(668)` is asserted here.
No long search was run while hardening this version.

## 1. Exact finite state model

There are two profile words of length twelve.  Each letter is one of the ten
compositions

```text
(p_0,p_1,p_2),                   p_0+p_1+p_2=3.
```

The model has 24 primary profile IDs.  Each ID is connected by an exact table
to its signed Eisenstein coefficient and norm.  All nonzero correlations are
then reconstructed in integer Eisenstein coordinates.

Only off-diagonal products need product tables:

```text
2 channels * C(12,2)                         = 132 tables
132 tables * 100 profile-ID pairs            = 13,200 rows.
```

Diagonal products are the already-present norm variables.  This removes 24
unnecessary product tables without changing any correlation.

For the first catalog target, whose fixed-target stabilizer is just `C_6`, the
current exact model has:

```text
integer/Boolean variables                     747
allowed tables                                162
linear constraints                            838
total constraints                           1,000
exact zero scalar equations                    12
primitive-nine ideal parts                     12
characteristic-37 scalar equations             26
```

Targets fixed by one coefficient star receive six additional orbit images in
their lex-leader and consequently have a slightly larger model.

## 2. Sharp correlation coordinates

For `D=a+b*omega`,

```text
4 Norm(D) = (2a-b)^2 + 3b^2
          = (2b-a)^2 + 3a^2.
```

The energy-167 Cauchy disk gives `Norm(D)<=167^2`.  Therefore

```text
|a|, |b| <= 192.
```

The constructor uses exactly `[-192,192]` for both correlation coordinates,
not the former conservative `[-400,400]` box.  At model construction it checks
that 192 is the largest integer not excluded by the displayed coordinate
inequality.

## 3. Quartet coarse layer

The variable order completes one opposite-class quartet at a time:

```text
A_j, A_(j+6), B_j, B_(j+6).
```

An exhaustive local table enforces the opposite-pair signature equality.
Out of the `10^4` possible ID quartets, exactly

```text
3,334
```

are legal.  Recording only their four aggregate increments and energy
increment produces exactly

```text
1,409
```

coarse states.  Every model contains six exact 3,334-row tables mapping the
four IDs to one of these states.

Layered cumulative variables propagate the four aggregate coordinates and
energy from quartet to quartet, with forward and backward coordinate bounds
from the remaining state catalogs.  This is the useful MDD-style coarse layer
without materializing a very large transition graph.

As an independent census, the first two quartet layers with partial energy at
most 54 contain:

```text
96,104 distinct coarse sums,
10,934,035 legal ordered ID prefixes.
```

The self-test recomputes all four numbers (`3,334`, `1,409`, `96,104`, and
`10,934,035`) from the ten-state catalog.

## 4. Exact and redundant correlation layers

For each of the twelve nonzero invariant parts, the model reconstructs the
exact integer pair for `D_t`.  It then imposes:

```text
D_j = 0 in Z[omega],                         j=1,...,6;
D_t in 3(1-omega) Z[omega],                  t!=0;
all 13 characteristic-37 transfer outputs = 0 mod 37.
```

The first line alone is the exact gate because

```text
D_(j+6) = conjugate(D_j).
```

The last two lines deliberately duplicate necessary consequences.  They
provide propagation and an internal cross-check against the independently
verified local-global theorem:

```text
37 * 3(1-omega) has least nonzero norm 37^2*27 = 36,963
                                               > 167^2 = 27,889.
```

## 5. Fixed-target symmetry and orbit emission

Common even-class rotation gives `C_6` at every fixed target.  If coefficient
star on A or B also fixes that target, the constructor uses the full
fixed-target subgroup of order twelve.  The lex leader is imposed with the
verified source-index convention and the exact ten-state conjugation map.

This extra star reduction is safe for profile discovery because every
survivor is emitted with both:

```text
its full formal C_6 x C_2(A-star) x C_2(B-star) orbit,
its lift-compatible C_6 x C_2(B-star) orbit.
```

Thus an A-star image discarded by the fixed-target lex leader is restored
explicitly for later independent labelled-lift testing.  The seven formal
target representatives remain complete for the profile equation, while the
twelve lift-compatible target representatives remain available as a separate
mode.

## 6. Resumable enumeration

The checkpoint begins with one empty prefix cube per selected target.  A cube
that reaches its wall-clock budget is replaced by its ten disjoint children.
The queue is saved atomically.

Finding a survivor no longer stops the campaign.  Instead the runner:

1. performs the detached exact replay;
2. records the survivor and both symmetry orbits;
3. adds an exact 24-variable no-good;
4. continues enumerating the same cube;
5. persists the no-good semantically through the survivor catalog if the cube
   is later subdivided.

Candidate hashes prevent duplicate emission after resumption.  A fully fixed
cube that times out is retained rather than silently dropped.

The checkpoint fingerprint covers:

```text
the constructor source,
the detached verifier and every mathematical source dependency,
the complete profile/quartet/product/transfer tables,
the OR-Tools version,
the selected targets, variable order, symmetry setting, and exact layers.
```

A source, table, dependency, or solver-version change therefore requires a
new checkpoint path.  JSON loading rejects duplicate keys, non-finite
numbers, booleans in integer fields, floats, numeric strings, malformed
prefixes, and inconsistent candidate hashes.

## 7. Memory semantics

The solver is configured with:

```text
one worker,
fixed variable/value order,
randomization disabled,
max_memory_in_mb <= 4096.
```

OR-Tools' `max_memory_in_mb` is a solver parameter, not an operating-system
hard RSS limit.  The checkpoint records this fact explicitly.  External
process monitoring is still required for a strict machine-wide 16 GB limit.

The fixed-fixture self-test and the complete constructor unit suite each
remain below 140 MB maximum RSS on the reference machine.  No long or
multi-gigabyte solve is part of the test procedure.

## 8. Mandatory detached replay

The candidate verifier imports no solver package and strictly parses every
serialized integer.  It checks:

```text
the target and exact aggregate;
energy 54 in the normalized profile variables;
all six opposite-pair signatures;
the primitive-nine profile ideal;
all thirteen characteristic-37 transfer coefficients;
exact D_t=0 on all thirteen invariant parts.
```

It performs three correlation reconstructions:

1. all 37 physical residuals through the local-global verifier;
2. the independent thirteen-part profile correlation table;
3. all 37 physical correlations through the prime-167 arithmetic, requiring
   origin `(167,0)`, zero modulo 167 at every lag, exact zero at every nonzero
   lag, and exact agreement after origin subtraction.

Passing this replay certifies only the 24-profile zero gate.  The 54 placement
phases, exact row margins, full 333 correlations, and final order-668 matrix
remain separate obligations.

## Reproduction

From the repository root, using the project environment:

```text
tmp/hadamard-env/bin/python \
  hadamard_668_search/search_lp333_order3_profile_crt.py \
  --self-test --max-memory-mb 512

(cd hadamard_668_search && \
  ../tmp/hadamard-env/bin/python -m unittest -v \
  test_search_lp333_order3_profile_crt.py)
```

A bounded resumable discovery invocation is:

```text
tmp/hadamard-env/bin/python \
  hadamard_668_search/search_lp333_order3_profile_crt.py \
  --target-mode formal \
  --checkpoint hadamard_668_search/output/profile_crt_v2_checkpoint.json \
  --candidate hadamard_668_search/output/profile_crt_v2_survivors.json \
  --time-limit 60 \
  --cube-time-limit 15 \
  --max-memory-mb 4096
```

If a survivor catalog appears, replay every entry without OR-Tools:

```text
python3 \
  hadamard_668_search/verify_lp333_order3_profile_crt_candidate.py \
  hadamard_668_search/output/profile_crt_v2_survivors.json
```
