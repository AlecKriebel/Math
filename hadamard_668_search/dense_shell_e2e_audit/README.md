# Connected dense-shell end-to-end audit

## Result

This folder closes the gap between the earlier arithmetic microbenchmark
and one genuine production work unit.  It does **not** classify either
dense shell and does not construct a Legendre pair or `H(668)`.

The bounded representative is the complete production prefix

```text
h0-p01-p13.
```

Its first two legal quartet states have weights two and zero.  The remaining
four quartets must all have weight four, so the prefix has one unsigned
support and exactly

```text
1,296 legal signed skeletons
42 canonical decorated skeletons
600 raw-equivalent decorated skeletons.
```

The connected C++ audit then selects a real canonical skeleton and real
aggregate target from that prefix.  It:

1. reconstructs the 27 legal local states and the complete prefix;
2. canonicalizes every decoration under the order-24 group;
3. constructs the actual 12-dimensional affine phase fiber;
4. derives the genuine six-coordinate modulo-nine quadratic map from exact
   Eisenstein correlations;
5. factorizes all 729 additive-character pencils;
6. checks the factorized character sums against exhaustive enumeration and
   inverts all 729 characters back to all 729 fiber counts;
7. recovers the unique point in this skeleton/target that also passes the
   following lambda digit; and
8. recomputes all 37 physical correlations for the recovered point and its
   full-assignment canonical image.

All stages pass.

## Exact representative counts

For the selected support/canonical skeleton/target:

```text
support mask                         15,978,365
support cell (r,d,rho,nu)            (5,12,12,0)
lower affine points                  3^12 = 531,441
actual modulo-nine zero fiber        729
exact-target points                  21,702
exact-target and modulo-nine points  34
following-lambda points              1
```

The last count is one only **inside this selected skeleton and target**.
The full 42-decoration prefix has seven following-lambda hits.

The recovered point is:

```text
target index   2
target         (-3,0,-3,-3)
A profile IDs  (8,5,8,7,4,1,4,5,7,2,2,7)
B profile IDs  (5,5,4,6,8,4,5,5,1,8,2,2)
correlations   (0,0);(18,9);(27,0);(9,18);(-18,18);(-18,-9)
digest         0xc8ac157d026d3025
orbit size     24
```

This is a profile-character lift through modulo nine and the next lambda
digit.  It is **not** an exact profile: the displayed correlations are
nonzero.  It also fails the independent characteristic-two quotient, so it
cannot be a physical placement seed, a length-333 Legendre pair, or a
Hadamard matrix.

## The old character rate is not an end-to-end rate

The earlier `scratch_dense_shell_benchmark` uses real supports and the
published `F_27 x F_27` pencil, but it supplies synthetic affine targets.
On this connected work unit, its restricted polar matrices disagree with
the production modulo-nine polynomial in

```text
459 of 6*12*12 = 864 entries.
```

This does not invalidate that benchmark as arithmetic for its stated
quadratic family.  It proves that its `12,668,666` characters/second/core
number cannot be multiplied by the current production workload and called
an end-to-end classifier estimate.

The same exact factorization code, applied to the **actual fitted
modulo-nine family** in this one representative, ran three pinned batches
of `11,943,936` character evaluations at:

```text
15,625,895
15,672,112
15,641,863  characters/second/core.
```

The median is `15,641,863`.  This establishes feasibility for this one
family; it does not establish support-level reuse or a shell-wide rate
distribution.

## Production replay bug and correction

The declared production scope reconstructs upper exact correlations only
on

```text
characteristic-two AND modulo-nine.
```

Before this audit, a diagnostic witness fallback remained active in
production even though production never stores those diagnostic witnesses.
Consequently every non-modulo-nine exact-target point was reconstructed and
sent through the all-37-lag replay.

On the representative complete prefix:

| measurement | before | after |
|---|---:|---:|
| detached replays | 554,008 | 0 |
| classifier wall seconds | 2.615347 | 0.771325 |
| maximum RSS | 1.44 MiB | 1.47 MiB |

The redundant work cost `1.844022` seconds, or about `3.329` microseconds
per replay, and inflated this shard by `3.391x`.

The corrected trigger is mathematically sufficient.  In production,
exact correlations are reconstructed when both necessary gates hold:

```text
char2 && mod9.
```

Every exact-zero profile necessarily satisfies both gates.  The separate
fallback that reconstructs the first marginal target and characteristic-two
witnesses is now restricted to bounded diagnostic mode.

The regression test pins this entire positive-work prefix, including:

```text
19,131,876 primitive phase leaves
554,761 exact-target hits
284 characteristic-two hits
753 modulo-nine hits
0 characteristic-two/modulo-nine intersections
0 production detached replays.
```

Bounded mode independently repeats the same lower counters, performs 755
diagnostic replays, recovers the displayed following-lambda witness, and
checks its digest.

## Corrected direct-stream extrapolation

The original post-fix measurement below belongs to the frozen v1 discovery
source. It remains useful provenance for the replay bug:

The fixed prefix processes

```text
286,978,140 raw-equivalent primitive leaves / 0.771325 s
 = 372,058,652 raw-equivalent leaves/s/core.
```

Applying that single measured rate to the rigorous primitive-leaf upper
bounds gives:

| scope | upper work | projected single-core time |
|---|---:|---:|
| `h=0` | 26,743,335,560,064 | 19.97 hours |
| `h=1` | 45,036,129,993,984 | 33.62 hours |
| combined | 71,779,465,554,048 | 53.59 hours |

The ideal ten-core arithmetic quotient would be `5.36` hours. These remain
an extrapolation, not a runtime certificate: the prefix is a rare
`(5,12,12,0)` support cell, `h=1` has high-position work, and workload,
canonicalization, survivor density, and scheduling vary across the other
728 prefixes.

The exhaustive v2 source was subsequently benchmarked on the same prefix
with the actual production flag `--enumerate-exact-orbits`. Five runs gave:

```text
wall seconds: 0.745499, 0.744369, 0.742056, 0.763598, 0.743341
median raw-equivalent leaves/s/core: 385,532,181
maximum RSS: 1,540,096 bytes
exact canonical orbits retained in this prefix: 0
```

The operational v2 one-cell projection is therefore:

| scope | projected single-core time |
|---|---:|
| `h=0` | 19.27 hours |
| `h=1` | 32.45 hours |
| combined | 51.72 hours |
| ideal ten-core quotient | 5.17 hours |

The conservative conclusion is therefore:

- direct exhaustive classification still looks computationally plausible;
- the old `46.681` core-hour projection is superseded by this first
  nontrivial complete-prefix measurement;
- neither the current `51.72` core-hours nor the actual-family character
  rate is yet a shell-wide guarantee.

## Reproduction

From the repository root:

```text
python3 \
  hadamard_668_search/dense_shell_e2e_audit/verify_dense_shell_e2e.py

python3 -m unittest -v \
  hadamard_668_search/dense_shell_classifier_pilot/test_dense_shell_production.py
```

The verifier compiles both warning-clean C++ programs in a temporary
directory.  It pins all mathematical counts, the actual-character
checksum, the recovered witness, bounded/production counter agreement, and
zero redundant production replays.

The measured standalone connected audit used about `1.55 MiB` maximum RSS.
All work is far below the 4 GiB task cap and the machine's 16 GiB physical
memory.
