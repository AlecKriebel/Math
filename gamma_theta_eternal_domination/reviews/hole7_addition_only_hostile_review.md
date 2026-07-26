# Hostile review of the `hole7` full-bank UNSAT recovery

## Verdict

**ACCEPT the v2 recovery without mathematical reservation.**

The exact 6,886-variable, 21,718-clause full-bank `hole7` CNF with SHA-256

`6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7`

is unsatisfiable.  The accepted proof is the retained addition-only RUP
proof with SHA-256

`e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9`.

Pinned DRAT-trim replayed that proof twice with
`-I -f -W -U -t 600`.  Both replays exited zero, emitted exactly one
warning-free `s VERIFIED`, and reported `0 RAT lemmas in core`.  The
normalizer preserves every addition byte-for-byte and in order and removes
only deletion records.

Relative to the separately accepted graph-to-CNF and template-coverage
proofs bound below, this certifies the finite graph theorem:

> There is no connected graph \(G\) on 12 vertices such that
> \[
> \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)
> \]
> and \(\overline G\) contains a hub-free induced \(C_7\).

By the accepted odd-wheel obstruction, any induced \(C_7\) in the complement
of a parameter-three counterexample is automatically hub-free.  Combining
this result with the already accepted `hole9` exclusion and the accepted
three-template reduction leaves only the `hole5` branch of the
\((n,k)=(12,3)\) slice.  The slice is **not** complete until `hole5` has its
own accepted negative certificate.

Review date: 2026-07-25 PDT.

## Authoritative recovery package

The authoritative package is

`certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2/`.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `certificate.json` | 10,064 | `c38002e16190065ed13453f9013a294f013846b5ed3651fde64aaa927e2f888e` |
| `proof/addition-only.rup.drat` | 18,093,724 | `e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9` |
| `repro/hole7_deletion_strip_auditor.py` | 45,495 | `7bf67c205ca7f33e2109a5997e1b7015b18e383a8bf1ce0919992f437c945fd2` |
| `checker/strict.stdout` | 412 | `62e3c5d3d39954139ea3a988a18a3cb62563f20daf901fb1beccbe153b00a3aa` |
| `checker/strict.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `checker/original-warning.stdout` | 12,391 | `b97edcc8af5943614eba3c1c5e2243e913a74edf53cd56fb7be02308f57f0e22` |
| `checker/original-warning.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `SOUNDNESS.md` | 2,246 | `206a4b60f48b8b36ab29842a8dad9664a5ce8f2f581e6fabfc2d11bc0a4017e9` |

The sorted eight-file tree contains 18,164,332 bytes.  Hashing, for each
file, the eight-byte big-endian length of its UTF-8 relative path, the path,
the eight-byte big-endian payload length, and the payload gives tree
SHA-256

`de67bfb55ba879a7d99ea498bbe0222b01a958ac8aa0fd47020674600ed0910a`.

All package files have mode `0444` and all package directories mode `0555`.
The installed independent auditor under `reviews/` is byte-identical to the
packaged copy.

The earlier unsuffixed recovery directory is **not authoritative**.  Its
post-install audit intentionally failed because v1 required byte-identical
checker stdout on fresh replay, although DRAT-trim embeds an elapsed-time
number.  That directory was left sealed and unmodified.  V2 normalizes only
that one numeric timing field and requires every logical counter and verdict
line to remain byte-identical.

## Immutable source binding

No source run or input package file was edited.  The recovery binds:

| source artifact | bytes | SHA-256 |
|---|---:|---|
| full-bank `instance.cnf` | 621,864 | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` |
| `coloring_bank.json` | 156,495 | `371ab3b01ce2add1138e0c0c78d267a796bcc536c79f95050face4bfcd4d11a7` |
| package `manifest.json` | 3,140 | `7c46b015dd58e321428c7d0bb8b896d27ae8ce0fb4bc9566199e43f86fa17185` |
| original `proof.drat` | 35,285,574 | `7ceb4a63d393d8ff6fec33569c6284fee61533be4f15fd733777b85b08ee2b85` |
| original `run_config.json` | 3,570 | `8cce1b89c3381e6b685b4d351c22b9edf2aaa17b42d1374631e878f323472dc9` |
| original `outcome.json` | 5,592 | `ffb19de770a003341b7050941531fca845626fe4cd086b727287122c57d510ff` |
| original `solver.result` | 16 | `bde6e1eede96772c07c8ce29fd18088863815bd043aa59a06f11f5838cf8a162` |
| pinned DRAT-trim executable | 70,088 | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| pinned `drat-trim.c` | 59,498 | `f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26` |

The original run remains correctly labeled
`UNSAT_UNVERIFIED_CHECKER_EXIT` / `NO_MATHEMATICAL_CLAIM`.  Its solver exit
20 and 11.381-second runtime are historical facts, not the certificate.  The
separate v2 recovery is the accepted certificate.

## Exact benign warning mechanism

The original wrapper used

```text
$CHECKER $CNF $ORIGINAL_PROOF -I -f -W -t 600
```

and exited 80 before printing `s VERIFIED`.  A retained read-only diagnostic
used the same inputs with `-v` and reproduced:

```text
c WARNING: ignoring deletion instruction 90747: [8166] -741 -17 -12 -1 0
```

The corresponding source-proof records are:

```text
line 2374: -741 0
line 2375: d -741 -1 -12 -17 0
```

This is not a failed RUP or RAT inference and is not a warning caused by
every deletion.  In the pinned `drat-trim.c`:

- line 54 defines `HARDWARNING` as exit code 80;
- lines 806--814 detect deletion of a nonunit clause that is currently the
  reason for a pseudo-unit;
- line 808 says to ignore that deletion outside `FORWARD_SAT`;
- line 811 exits if warnings are hard; and
- line 1409 maps `-W` to `HARDWARNING`.

Thus forward checking deliberately keeps the reason clause and ignores the
optimization request; `-W` converts the ignored request into the wrapper's
exit 80.  The original output SHA-256 is
`b97edcc8af5943614eba3c1c5e2243e913a74edf53cd56fb7be02308f57f0e22`.

## Independent deletion-strip audit

`reviews/hole7_deletion_strip_auditor.py` uses only the Python standard
library.  It imports neither the search code, the CNF generator, nor an
author proof-wrapper core.  It:

1. binds every immutable input by SHA-256 and validates the original
   no-claim outcome;
2. strictly parses canonical ASCII DRAT, rejecting comments, control bytes,
   malformed spacing or integers, out-of-range variables, duplicates,
   tautologies, nonfinal empty clauses, and deletion-free output containing
   any deletion;
3. streams every addition byte-for-byte and in order while discarding only
   syntactically valid `d ` records;
4. reparses the generated proof independently;
5. checks the CNF header, all 21,718 nonempty clauses, 148,551 literals, and
   the exact CNF hash;
6. rehashes the CNF, proof, and checker before and after each replay;
7. requires warning-fatal, forward, RUP-only replay; and
8. installs a new package only after the first successful replay, then
   performs a fresh strict replay against the sealed proof.

The exact transformation census is:

| quantity | original | addition-only |
|---|---:|---:|
| records | 547,479 | 284,317 |
| additions | 284,317 | 284,317 |
| deletions | 263,162 | 0 |
| addition literals | 4,720,044 | 4,720,044 |
| deletion literals | 4,336,626 | 0 |
| bytes | 35,285,574 | 18,093,724 |

The original addition stream and the entire retained proof have the same
SHA-256,
`e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9`.
There is exactly one empty addition, and it is the final retained record.

The parser mutation suite rejected all ten malformed cases: carriage return,
missing final LF, comment, empty deletion, duplicate literal, tautology,
leading zero, out-of-range variable, nonfinal empty clause, and doubled
space.

Deleting proof-deletion instructions is sound for RUP: it only retains more
clauses in the proof database, so unit propagation cannot lose a
contradiction.  The acceptance does not rely on this monotonicity argument
alone.  DRAT-trim option `-U` makes a failed RUP check fail instead of
falling back to RAT, and the complete addition-only stream passed twice.

## Strict replay

The decisive normalized checker command was

```text
$CHECKER $CNF $ADDITION_ONLY_PROOF -I -f -W -U -t 600
```

The retained first replay reported:

```text
c 15124 of 21718 clauses in core
c 191918 of 284318 lemmas in core using 12572468 resolution steps
c 0 RAT lemmas in core; 0 redundant literals in core lemmas
s VERIFIED
```

Its stdout SHA-256 is
`62e3c5d3d39954139ea3a988a18a3cb62563f20daf901fb1beccbe153b00a3aa`;
stderr is empty.  After removal of carriage-return progress controls and
replacement only of the elapsed-time number, the stable transcript SHA-256
is
`eaea93a339d1070056bb5806e980c17e482f5be3ed50b6a2691aff4a9ab518a2`.
The sealed-package replay matched that stable transcript exactly.

The generation-and-double-replay command was:

```text
python3 reviews/hole7_deletion_strip_auditor.py recover \
  --validation-gate-open \
  --output certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2
```

It returned `generated_and_verified`, used 267.32 wall seconds, and reached
87,392,256 bytes maximum resident set size.  A subsequent no-replay package
audit and the packaged ten-mutation self-test both passed.  A further third
checker replay was deliberately not launched because it would duplicate the
two decisive strict passes.

## Graph-to-CNF implication audit

The full-bank package was independently reconstructed without importing the
synthesis encoder by
`reviews/template_coloring_bank_hostile_probe.py`, SHA-256
`0a55ea60334be110b4b45998078d0050e726f7b1ff223a6d87250778bbe1cb26`.
The exact `hole7` audit command reported `PASS` and established:

- 531,441 labeled three-color assignments exhausted;
- exactly 10,206 assignments compatible with the forced positive
  \(H=\overline G\) edges;
- exactly 1,701 first-use canonical color partitions, all orbit size six;
- all 521,235 omitted assignments already killed by a forced positive edge;
- an independently reconstructed 20,017-clause base;
- the exact 1,701-clause complete bank appended after that base; and
- byte-identical CNF, bank, manifest, source hashes, and source-set binding.

The graph implication is as follows.  Suppose \(G\) lies in the theorem's
claimed universe and put \(H=\overline G\).

1. Orient and label the assumed induced \(C_7\) by \(0,\ldots,6\).
   Since \(\gamma(G)=3\), no pair dominates \(G\), so every pair in \(H\)
   has an external common neighbor.  A rim edge has no common neighbor on an
   induced cycle of length at least five; label a common neighbor of \(0,1\)
   as vertex 7.  Hub-freeness and arbitrary labels for vertices 8--11
   satisfy every template clause.
2. Use the actual edges of \(H\) for the edge variables.
   \(\alpha(G)=3\) gives no \(K_4\) in \(H\), the common-neighbor choices
   satisfy all witness clauses, and connectedness of \(G\) satisfies every
   negative-\(H\)-edge cut clause.
3. Use an actual eternal three-family for the family variables and choose
   one actual one-guard response to every unoccupied attack.  The move
   clauses encode exactly one guard moving along one edge of \(G\) to the
   attacked vertex, with the successor selected and dominating.  Every
   triangle of \(H\) is a maximum independent triple of \(G\), so the
   accepted maximum-independent-state theorem validates the redundant
   triangle-selection clauses.
4. Finally, \(\theta(G)=\chi(H)>3\).  Every one of the 1,701
   template-compatible coloring assignments therefore has an \(H\)-edge
   inside a color block, satisfying its same-color clause.

This constructs a model of the exact certified-unsatisfiable CNF from any
graph in the claimed universe, a contradiction.

The dependency bytes checked in this audit are:

| dependency | SHA-256 |
|---|---|
| `math/reductions.md` | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| `math/lemmas/maximum_independent_states.md` | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| `math/lemmas/complement_k3_dictionary.md` | `54d7cafdc7047d75ed58739f6a773344a2f780aaecd0eafde8ed01a0692c6256` |
| `math/lemmas/k3_structural_day1.md` | `00d6fb851a3cb50ed907a593b0379376571251f8604974b5b67e05e2b0705d6e` |
| `math/lemmas/k3_antihole_elimination.md` | `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f` |
| `math/synthesis_k3_cegar_design.md` | `57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8` |
| `math/lemmas/template_coloring_bank.md` | `abc9568d70eee6b792e4220b58c12f5e7c069a13e37dbd3265025abe02cd6f50` |
| encoding hostile review | `0bf04808405e92392a61da4157daa6fc5e7ddb4ec36fe6ba8f24df907703b947` |
| bank-theorem hostile review | `2fa68d7c36598c73ca0f27a83ec3904e1bca7e2ce6d9c927b52c7cce0a6a79c7` |
| production-bank hostile review | `159cc01ccf4b5bdb0137a23dff5248ff94d90902fb6c150747fb811e7416959f` |
| antihole hostile review | `7837fb360328533ea58a31d1a0eb60ef279a67d1e610144eb5206661ef38f5e3` |
| structural hostile review | `f2b0ce3d551576d5050bb03c7e8699bdffdb3ae35fbf5d3cf4b28c4e4ab270bc` |

## Exact claim boundary

What is certified:

- the exact full-bank `hole7` CNF is UNSAT;
- no connected order-12, parameter-three counterexample has a hub-free
  induced \(C_7\) in its complement;
- using the accepted odd-wheel theorem, no survivor has any induced \(C_7\)
  in its complement; and
- using the accepted three-template reduction and accepted `hole9`
  exclusion, every remaining \((12,3)\) survivor must fall in `hole5`.

What is not certified:

- `hole5`;
- the complete \((n,k)=(12,3)\) slice;
- any larger order or other guard parameter;
- the existence of a counterexample; or
- the universal gamma--theta conjecture.

