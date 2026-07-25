# Final half-turn catalog and two-shell lifts

## Final strict-aggregate extension

The completed strict production aggregate contains 18 exact canonical `h=0`
profile orbits.  Automatic stabilizer discovery finds exactly six profiles
fixed by the six-class half-turn.  Every one has stabilizer `{0,12}`, orbit
size 12, and first-lift split `36=21+15`:

| digest | coverage source | anti code | two lowest shells |
|---|---|---:|---:|
| `0x81065cf5084f39f1` | original baseline | `[27,15,4]` | `6,14` |
| `0x86b13a0388d98a5e` | final extension | `[27,15,4]` | `8,6` |
| `0xaa1c4c148acc5b86` | final extension | `[27,15,4]` | `2,6` |
| `0x5b160dfa076231eb` | frozen v1 | `[27,15,4]` | `8,12` |
| `0xfdb6a5c865468e1f` | frozen v1 | `[27,15,5]` | `12,146` |
| `0xac3483a00651e7ce` | frozen v1 | `[27,15,4]` | `8,16` |

The two profiles absent from the v1 certificate have now had both lowest
positive anti shells exhausted:

| digest | shell | signed words | digit-two points | row-margin points | best digit-three defect |
|---|---:|---:|---:|---:|---:|
| `0x86b13a0388d98a5e` | 4 | 8 | 212 | 0 | 7 |
| `0x86b13a0388d98a5e` | 5 | 6 | 168 | 0 | 9 |
| `0xaa1c4c148acc5b86` | 4 | 2 | 194 | 0 | 9 |
| `0xaa1c4c148acc5b86` | 5 | 6 | 178 | 0 | 7 |

This final extension adds 22 signed words and 752 digit-two points, with no
row-margin or full digit-three point.  Combining without double counting:

| coverage class | profiles | signed words | consistent slices | digit-two points |
|---|---:|---:|---:|---:|
| original baseline | 1 | 20 | 20 | 658 |
| prior three-profile v1 | 3 | 202 | 200 | 5,768 |
| two-new final extension | 2 | 22 | 22 | 752 |
| **combined** | **6** | **244** | **242** | **7,178** |

All 7,178 points miss the exact row-margin corpus and full digit three.  The
combined best digit-three defect is six.

## Frozen v1 three-profile computation

The complete production shard `h0-p00-p02` contains three exact `h=0`
profiles fixed by the six-class half-turn.  For every one, the first
placement lift has affine dimension 36 and its translation space splits as

```text
V = V+ direct-sum V-,       dim(V+), dim(V-) = 21, 15.
```

Projecting `V-` to the 27 opposite-class pairs gives three different ternary
codes:

| profile digest | anti code | two lowest positive shells |
|---|---:|---:|
| `0x5b160dfa076231eb` | `[27,15,4]` | `A4=8`, `A5=12` |
| `0xfdb6a5c865468e1f` | `[27,15,5]` | `A5=12`, `A6=146` |
| `0xac3483a00651e7ce` | `[27,15,4]` | `A4=8`, `A5=16` |

The middle profile is structurally distinct: its anti code has no
weight-four word.  This is the profile that had the largest exact
row-margin transfer mass in the preliminary ten-orbit audit.

Every signed word in the two displayed shells was lifted completely.  For a
fixed anti word, the six half-turn-odd second-digit equations are linear in
the 21 symmetric coordinates.  Each consistent affine slice was then
exhausted through all 18 active second-digit equations, and every resulting
point was replayed through the exact Eisenstein evaluator, the exact
row-margin corpus, and the next placement digit.

| digest | shell | signed anti words | consistent slices | digit-two points | row-margin points | best digit-three defect |
|---|---:|---:|---:|---:|---:|---:|
| `0x5b160dfa076231eb` | 4 | 8 | 8 | 296 | 0 | 7 |
| `0x5b160dfa076231eb` | 5 | 12 | 12 | 310 | 0 | 7 |
| `0xfdb6a5c865468e1f` | 5 | 12 | 12 | 344 | 0 | 7 |
| `0xfdb6a5c865468e1f` | 6 | 146 | 144 | 4,142 | 0 | 6 |
| `0xac3483a00651e7ce` | 4 | 8 | 8 | 226 | 0 | 8 |
| `0xac3483a00651e7ce` | 5 | 16 | 16 | 450 | 0 | 7 |

Across 202 signed anti words, 200 consistent symmetric slices contain 5,768
exact digit-two points.  None is compatible with any of the 96 exact
row-margin fibers, and none reaches digit three.  The best point leaves six
nonzero digit-three rows.

Thus the priority profile's large first-digit transfer mass does not convert
into a physical lift in either of its two nearest half-turn-breaking shells.

## Verification

The lightweight final-catalog and artifact-chain audit is:

```text
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/h0_new_halfturn_lifts/verify_final_halfturn_extension.py
```

It passed in 2.2 seconds with semantic hash
`9745f32ab864df7c34de70fab72da9002c173d2d84dab8443189c662037bac86`.

The prepared one-core command that additionally reruns the two new anti
codes, checks each through the dual MacWilliams transform, and exhausts all
22 new slices is:

```text
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/h0_new_halfturn_lifts/verify_final_halfturn_extension.py \
  --full-extension
```

That full extension replay has deliberately not been launched while the
separate eight-worker Eliahou census is active.

The earlier three-profile v1 replay remains:

```text
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/h0_new_halfturn_lifts/verify_new_halfturn_lifts.py
```

The verifier:

1. reconstructs each pinned profile and checks all 37 correlations directly
   in integer Eisenstein arithmetic;
2. reconstructs the `36=21+15` eigenspace split;
3. enumerates each complete `3^15` anti code;
4. independently enumerates its `3^12` dual and recovers the same full weight
   enumerator by the ternary MacWilliams transform;
5. exhausts every selected symmetric digit-two slice;
6. directly replays every digit-two hit and tests exact row-margin membership
   and digit-three defect.

The full replay uses one CPU, peaks below 300 MB, and takes roughly twenty
minutes on the 10-core M1 Pro while the production census is also active.

## Scope boundary

The automatic classification of six half-turn-fixed profiles is complete
relative to the final strict 18-orbit aggregate.  The numerical result is a
complete exclusion of only the two lowest positive antisymmetric weight
shells for those six profiles.  It is not an exclusion of any full profile,
the remaining anti weights, `LP(333)`, or `H(668)`.

The next shells contain 124, 306, and 106 signed words respectively.  They
are finite extensions of this calculation, but the complete remaining lift
still grows to almost all `3^15` anti words per profile.  The present result
therefore retracts one prioritized local lane; it does not provide evidence
that an unrestricted lift is close.
