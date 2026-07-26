# Hostile review of the hole9 orphan-UNSAT recovery

## Verdict

**ACCEPT WITH TWO VALIDATED ERRATA**, for the narrow claim that the exact
preserved `hole9` base-plus-170-cut CNF is unsatisfiable.

The first audit pass found two correction blockers:

1. ART-115 truncated the `cuts.json` SHA-256 to 63 hexadecimal characters.
2. The soundness note said the runner generated the CNF twice, although it
   generated it once and ran two CaDiCaL passes against the same path.

Neither defect changes the CNF, proof, RUP argument, or sealed package bytes.
Both are now corrected by explicit, non-destructive, independently validated
errata:

- `results/logs/synthesis-k3-hole9-batch-004-checker-incident-erratum.json`,
  SHA-256
  `6bfb1cc799977d96fe5058b13c1dd08e8c0cbb8b86c3a58a30c3c9a6233ee135`;
- `results/logs/synthesis-k3-hole9-recovery-soundness-erratum.json`, SHA-256
  `f6135a4121cafaca5275d1f1f707e7c82626d61caec94d908704aaec92400e90`.

There is no unresolved mathematical, proof-replay, source-reconstruction, or
package-integrity defect.  Acceptance requires the two errata, outer
certificate hash, this review, and the standalone probe to be committed and
publication-bound together.  The original ART-115 record, frozen run tree,
and sealed recovery package must remain byte-identical.

This verdict does **not** retroactively create a CEGAR terminal marker, certify
another template, establish template coverage, or prove the complete
\((n,k)=(12,3)\) slice.

## Independent implementation boundary

The review probe is
`reviews/hole9_orphan_recovery_hostile/probe.py`, SHA-256
`cf4d6e261787d1130a139ecd5cb89db81a71c6e61a0a1a06624a7b481653c49b`.
It uses only the Python standard library.  It imports neither
`verifier_b.hole9_orphan_recovery` nor any `synthesis_k3` module, including
`cegar` and `encoding`.  Its isolated-mode execution (`python3 -I`) passed.

The probe independently implements strict JSON, DIMACS, and proof parsers; a
direct mathematical CNF builder; checkpoint history hashing; gzip/raw
artifact checks; deterministic deletion removal; and a mutable
two-watched-literal RUP engine.  It reads project source files only as hashed
evidence and never executes or imports them.

## Exact bindings

| Role | SHA-256 |
|---|---|
| Recovery verifier | `52da8c235eaffe46b5bcc4b7178f6b522629b8e683f8c3fc945b76464b0da075` |
| Recovery tests | `9855eab623f5eb14fc99880f1295f9e709b537e5b5645b1417e33ee015c58a22` |
| Soundness note / package copy | `3c341560cb46e8a10ad0eb89ea8aa0e7e4131ea8c6d1dbaf7f1634282a2fa4bc` |
| Outer certificate | `1a2d4f7fd3efe0138bb7a7a7f0975d3c60a7ed4d6f994157c5383f18e4b5806c` |
| Run manifest | `73869e60bdefc547a91139ab3bfb0673ee8168acada62485089eb371a9d7c15d` |
| 170-cut checkpoint | `9cc9cdee08fb1fcd7a8772b09cdf9ba9ced802cb0b31be35ab292244e5f286b7` |
| Exact cut payload | `a3c7bd3591b71c310cfe0bd5711b8e672b75136f3598bb1505ae11cda3c2193b` |
| Orphan generator | `e492e06a0265f176df9a3e76f15b14a17f9873354dc9b6da4020347e1c95dbb4` |
| Exact CNF | `2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d` |
| Original proof | `3cdd686fb2af82e41ff06aa13901d4706618170eb1dc4e74a870831e7fbde8ef` |
| Addition-only proof | `24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab` |
| Both exact UNSAT result files | `bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162` |
| Pinned DRAT-trim binary | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| Pinned DRAT-trim source archive | `2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108` |
| Frozen run tree | `bd13c4fdc3629ee02fa510eda09bd503234daf4318a33c562e0ab3427d89fd8b` |
| Sealed package tree | `dab03e8f53ae975cfa0da32433df9c0838f8c279b9f756be59637017d0cd69b2` |

The frozen run tree is exactly 1,205 files and 6,946,580 bytes.  The sealed
package is exactly 23 files and 1,486,583 bytes.  Both tree digests were
identical before and after every review replay.  The package certificate lists
the other 22 files exactly; the certificate itself receives the outer binding
shown above.

## Source chronology and reconstruction

The checkpoint contains exactly 170 attempt references and 170 cuts, indexed
0 through 169.  Every outcome is `coloring_cut_committed`; every cut points to
the same-index attempt manifest.  The run contains exactly 171 attempt
directories.  `000170.akmx9xl0` is the only unreferenced directory, has no
`attempt.json`, and the run root has neither `candidate.freeze.json` nor
`unsat.verified.json`.

The independently recomputed history chain is:

- initial:
  `9e0bbac4b7d0dc1bbdce64a4a6757659d8a173705d55f26d07ecd45608f82b07`;
- final:
  `f174e43a531f4a1fbd857ab334d2ec4f7fa3c9b4c2cd0902eb37d887ccc51c99`.

All 170 checkpoint-predecessor and history-predecessor links match.  Every
coloring is canonical and distinct.  Each same-color edge clause and its two
hashes were rederived from the independently allocated edge variables.

Every removed historical `cuts.json` and CNF prefix was regenerated
byte-for-byte.  The `present_attempt_artifact_hash_checks` count is exactly
2,210: for each of 170 attempts, three retained files, six compressed/raw
bindings, and four reconstruction bindings were checked.  Attempt-manifest
and cut-source hashes were also checked directly.

The independent base builder produced:

- 6,886 variables;
- 20,030 base clauses and 114,619 base literals;
- base DIMACS SHA-256
  `cf555f359dc887c89f84e35a40ee649e77ef805b2690ec34e72cc4ef75e5d5c7`.

Appending the 170 validated cuts produced 20,200 clauses and 117,841
literals.  The serialization is byte-identical to the 530,053-byte orphan
CNF.

Git independently confirms that commit `31586830f1ee671baa349f3687d8bdfd1d3c23df`
contains the same frozen run tree and is reachable from `origin/main`.
Intermediate Git checkpoints reproduce the 1/33/65/129/170-cut history.

## Strict deletion stripping

The 512,071-byte original proof has exactly:

- 16,388 lines;
- 4,705 additions;
- 11,683 deletions;
- zero comments;
- one empty addition, physically last;
- maximum variable 6,886;
- maximum instruction size 220 literals.

The standalone parser required LF-terminated canonical ASCII, canonical signed
integers, one final zero, no duplicate or complementary literals, nonempty
deletions, no control bytes or blank lines, and a unique final empty addition.
It preserved every addition byte and removed only successfully parsed
`d <nonempty clause> 0` lines.

The result is the exact 65,906-byte stored addition-only proof: 4,705 lines,
zero deletions, maximum addition size 218, and SHA-256
`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.
A second strict parse returned the same bytes and the same addition sequence.

## Fresh RUP replay and soundness

The standalone watched-literal engine parsed the exact CNF itself and checked
all 4,705 additions in chronological order.  It performed 4,988,551 watched
clause visits and 7,546,525 assignment enqueues; the largest propagation trail
had 6,160 literals.  Every addition was RUP, and the 4,705th was the empty
clause.

The mathematical implication is direct.  If unit propagation refutes
\(F\land\neg C\), then \(F\models C\), because each propagated unit and the
final conflict are sound unit-resolution consequences.  Inductively, adding
each verified clause preserves satisfiability.  The review checker uses the
actual monotonically growing, deletion-free history, so it depends on no
semantics for DRAT deletions and on no RAT step.  When the verified final
addition is \(C=\bot\), a satisfiable starting formula is impossible.
Therefore the exact preserved CNF is unsatisfiable.

For the intended graph universe, each recorded coloring cut is also sound:
if \(H\) is not three-colorable, every three-color assignment has some
same-color H-edge, so its positive same-color edge clause is true.  Thus
UNSAT of the exact base-plus-cut formula excludes the intended `hole9`
template without assuming that the recorded source models remain relevant.

The pinned checker source independently confirms the documented flags:
`-f` selects forward UNSAT checking, `-U` returns failure after a failed RUP
test instead of trying RAT, `-p` sets deletion ignoring, and `-W` exits with
the hard-warning code 80.

## Hostile mutations

All eleven decisive mutations were rejected:

1. Removing base clause `(-67, 2)` made the first proof addition `-67`
   non-RUP.
2. Replacing the first addition by syntactically valid `-66` was non-RUP.
3. Making the same replacement in the original proof changed both bound
   hashes and failed the first RUP check.
4. Mutating the stored addition-only proof changed its hash and failed RUP.
5. Removing the final empty clause was rejected.
6. Appending an instruction after the empty clause was rejected.
7. A deletion missing its zero terminator was rejected.
8. A deletion with a duplicate literal was rejected.
9. An empty-clause deletion was rejected.
10. A deletion with an extra zero was rejected.
11. A deletion with doubled spacing was rejected.

These controls exercise distinct syntax, binding, reconstruction, and logical
failure paths; they are not merely expected-hash comparisons.

## Commands and measured resources

Primary independent run:

```text
/usr/bin/time -lp python3 -I \
  reviews/hole9_orphan_recovery_hostile/probe.py --compact
```

Result: `accepted_with_validated_errata`; RUP replay 2.879 seconds, complete
audit 4.412 seconds, wall time 4.50 seconds, maximum RSS 74,285,056 bytes.

Author-test cross-check:

```text
/usr/bin/time -lp env PYTHONPATH=src \
  python3 -m unittest -v tests.test_hole9_orphan_recovery
```

Result: 12/12 passed in 1.033 seconds; wall time 1.11 seconds; maximum RSS
48,218,112 bytes.

Pinned checker, explicit addition-only RUP:

```text
tools/drat_trim_2023_05_22/drat-trim \
  certificates/synthesis_k3_hole9_orphan_000170_recovery/source/orphan-attempt-000170/instance.cnf \
  certificates/synthesis_k3_hole9_orphan_000170_recovery/proof/addition-only.rup.drat \
  -I -f -W -U -t 60
```

Result: exit 0, exactly one `s VERIFIED`, zero warnings, 0 RAT lemmas,
verification time 0.084 seconds.

Redundant original-proof cross-check:

```text
tools/drat_trim_2023_05_22/drat-trim \
  certificates/synthesis_k3_hole9_orphan_000170_recovery/source/orphan-attempt-000170/instance.cnf \
  certificates/synthesis_k3_hole9_orphan_000170_recovery/source/orphan-attempt-000170/proof.drat \
  -I -f -p -W -U -t 60
```

Result: exit 0, exactly one `s VERIFIED`, zero warnings, 0 RAT lemmas,
verification time 0.084 seconds.

Installed package audit:

```text
env PYTHONPATH=src python3 -m verifier_b.hole9_orphan_recovery audit \
  --package certificates/synthesis_k3_hole9_orphan_000170_recovery \
  --drat-trim tools/drat_trim_2023_05_22/drat-trim
```

Result: `audit_passed_pending_hostile_review`, exit 0, package tree
`dab03e8…69b2`, exact verified-line count 1, warning count 0.

Frozen-run Git check:

```text
git -C .. diff --exit-code 31586830 -- \
  gamma_theta_eternal_domination/results/synthesis_k3_runs/hole9
git -C .. branch -r --contains 31586830
```

Result: no diff; `origin/main` contains the incident commit.

The complete audit stayed well within the 16 GB / M1 Pro envelope.  More
hardware would not materially improve this recovery audit.

