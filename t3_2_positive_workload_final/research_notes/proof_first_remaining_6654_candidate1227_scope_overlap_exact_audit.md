# Independent exact scope audit: candidate 1,227 versus the remaining 6,654

**Audit date:** 2026-08-12 PDT.

## 1. Frozen finite certificate and verdict

The audited finite certificate and its dedicated test are

~~~text
src/remaining_6654_candidate1227_scope_overlap_certificate.py
312098a7405a406b54e915084117b2c7f6b6ee426e8625b9204cbd6475561e46
238 lines / 9675 bytes

tests/test_remaining_6654_candidate1227_scope_overlap_certificate.py
8c5bc306340fc2c2553caf1e69d72ab5e6618780ba7cf6f13b570014dd96361d
39 lines / 1555 bytes
~~~

The verdict on these exact bytes is **STRICT PASS AS A FINITE SCOPE
CERTIFICATE**.  The certificate compares supports, symmetry orbits, feasible
failure descriptors, and normalized one-active templates.  It does not
enumerate orientations, rates, populations, reaction histories, or
communicating classes, and it makes no recurrence claim.

The analytic conclusion is negative and load-bearing: the old
candidate-1,227 population fourth-power theorem does **not** cover any of
the remaining 6,654 failure pairs, either literally or after the full
species-permutation/linkage-reversal orbit.  A B/B or B/F0 profile label by
itself is not a valid scope-extension theorem.

## 2. Pinned dependencies and replay

The certificate checks these exact dependency hashes before doing any set
comparison:

~~~text
src/active_invariant_orbit_gap_432_certificate.py
31fa24a20e18546e9c623d3aaf6d3b845c1708d5782f86333c02417fa366cd53

src/one_active_phase_shape.py
781c1e6b5106cc6785ec6902d932fb319ef2078fb40b4e4f983fdc6f7bc45be4

src/one_active_relative_debt_cegar.py
32d2313f428663c09a3d14e658f4c72a6ccbcaeb99c2b0cbf92dcce3c8b843ba

src/one_active_remaining_structure.py
ce1ff5e872cf4b93e085d56743b90c660eabf01f80491310c55955f2ca107e24

src/outside_mixed_remaining_18496_certificate.py
314f378664052cabe23910e118c9a43acf99884ccb5c63b61daf014a206e4c63
~~~

The five dedicated tests pass independently:

~~~text
Ran 5 tests in 90.643s
OK
~~~

The canonical summary payload has SHA-256

~~~text
4163d9adefa525663a75afc797774e3028e38cee2aa7b04d82343eb80b8daf2b
~~~

## 3. Exact disjointness result

The old selector contains 1,227 unordered support pairs, with canonical
pair fingerprint

~~~text
3ab28358663c45a089a5bdf4144c28573718b0c4f8b05472a0af208ca919fcf8
~~~

Its complete species-permutation and linkage-reversal orbit contains 6,546
pairs, with fingerprint

~~~text
7bfe8bc085e29d864fb26da7a6f81906feed5cae03458fafb9190ce584bb4410
~~~

Both intersections are empty, not only with the 6,654 failure pairs but
with the entire 18,496-pair remainder:

~~~text
direct candidate intersection with 6,654       0
candidate orbit intersection with 6,654        0
direct candidate intersection with 18,496      0
candidate orbit intersection with 18,496       0
~~~

The 6,654 failure pairs have fingerprint

~~~text
036f9cb8f00f99f78be9cb6c2303208a8ca8b25be8c1bd350b8fac6b35582eed
~~~

Thus no symmetry normalization can turn a remaining pair into a pair in the
old theorem's certified selector.

## 4. Exact normalized-template comparison

The old candidate rows have 727 normalized support types and 1,599
support-plus-cap types.  The new one-active failure rows have 1,275
normalized support types and 3,163 support-plus-cap types.  Both exact
intersections are empty:

~~~text
old/new normalized support-type intersection       0
old/new normalized support-plus-cap intersection   0
~~~

Among the 6,654 pairs, exactly 1,596 have an AA failure and 5,058 have only
one-active failures.  The old theorem's finite exhaustion begins with a
one-active-only premise, so the 1,596 AA-containing pairs already lie
outside that premise.  The remaining 5,058 are still outside the exact
support and cap templates, as the zero intersections above show.

## 5. Why syntactic routing is not theorem transfer

For diagnostic purposes only, the certificate applies the old finite
category router to all 18,822 one-active failure rows.  It obtains 16,986
syntactic successes and 1,836 assertion failures.  The failures occur in
396 pairs; 4,662 one-active-only pairs happen to route syntactically on all
their rows.

This diagnostic cannot be promoted to recurrence.  The router is only a
case-label function.  The old population-fourth-power estimates,
establishment kernels, expectation ledgers, and common-potential handoff
were proved for the old exact selector and its exact normalized supports.
Neither a broad label such as `family_i_origin_down_0` nor agreement of the
profile string supplies those analytic hypotheses for a new support.

The literal first failed row is

~~~text
pair                 {0,2A,2B} | {A,AB,AC}
active weight         (0,0,1)       [C active]
caps                  (0,0,2)
profile               B/F0
normalized supports   {0,2A,2B} | {A,AB,AC}
normalized caps       (0,0)
~~~

It reaches the old Family-II branch and violates that branch's exact support
assertion.  This is an explicit support/descriptor witness against a
profile-only extension; it is not an orientation or population
counterexample.

The successful-row histogram is

~~~text
B/B   family_iii_origin_down_0             612
B/B   family_iii_origin_no_history         138
B/B   mixed_C_source_direct_down_0        2868
B/F0  family_i_origin_down_0              2760
B/F0  family_i_origin_no_history          1080
B/F0  mixed_C_source_direct_down_0        9528
~~~

These numbers describe only where old assertions happened not to fire.
They establish no analytic overlap.

## 6. Publication boundary

The exact conclusion available for composition is therefore:

1. the old candidate-1,227 theorem and its complete symmetry orbit cover
   zero pairs in the 18,496 remainder;
2. all normalized old and new one-active support/cap template sets are
   disjoint;
3. 396 one-active-only pairs even refute literal reuse of the old router;
   and
4. the remaining syntactic router successes cannot be cited as recurrence
   without a new support-uniform analytic theorem.

Any completion of the 6,654 branch must prove a new population-Foster or
unconditional killed-completion theorem on the new exact support family.
It may not cite the candidate-1,227 theorem merely from B/B or B/F0 profile
agreement, and it may not use a terminal chart-exit shortcut.
