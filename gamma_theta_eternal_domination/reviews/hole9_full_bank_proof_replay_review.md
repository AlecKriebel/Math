# Independent review of the retained `hole9` full-bank proof replay

## Verdict

**ACCEPT.**  The retained complete-bank `hole9` CNF with SHA-256
`baea72050aaec8f41bad4e245fff8409489a9270f76ab0ffc97f0271f49dca01`
is certified UNSAT by direct replay of the previously accepted addition-only
RUP proof.  The pinned DRAT-trim checker returned exit code 0, emitted exactly
one `s VERIFIED`, emitted no warning, wrote an empty stderr, and reported zero
RAT lemmas.

No SAT solver was run.  This is a proof replay against a strengthened formula,
not a new search.

The exact machine-readable binding is
`results/synthesis_k3_template_bank_proof_replays/hole9/replay.json`, SHA-256
`d23bf016cf2bdd4c4e23763d3f32068af91d4151205d0eb6a0e3ea93a5a394b0`.

## Provenance established before replay

The retained package manifest has SHA-256
`e36e7ab02bdc001c09fe0f9d12f8257483a695c758c1f29dd4a3ac2cb4d0ab83`.
It binds:

- template `hole9`, order 12;
- 6,886 variables, 20,795 clauses, and 129,559 literals;
- a 20,030-clause frozen base followed by all 765 canonical
  template-compatible coloring clauses;
- the coloring bank SHA-256
  `d4361c57730765112c80e9348561a063a2ad7eae9ad00d3986dcb111446b5ef7`;
- source commit `2e68a6396735381ee634a572dda409610b40891f`;
- seven runtime-source hashes, all matching that commit.

A standard-library-only checker, independent of the bank generator and frozen
encoding transition core, reconstructed the base and all 765 clauses.  It
exhausted all \(3^{12}=531{,}441\) named color assignments and obtained
exactly 4,590 compatible assignments, hence 765 free \(S_3\)-orbits.  Its
retained output is `preflight-audit.json`, SHA-256
`3aae86467e15c040cde289f1551d44a74895da0f891e55128bd6cf97360cc32d`;
stderr is empty.

The same audit compared the accepted earlier formula with the complete-bank
formula as clause multisets.  It verified:

- the same exact 20,030-clause base;
- all 170 accepted coloring cuts occur verbatim in the complete bank;
- the earlier 20,200 clauses are a multiset subset of the complete 20,795
  clauses;
- the strengthening consists of exactly 595 additional bank clauses.

Thus the full-bank CNF provenance and its relationship to the previously
certified CNF do not rest on filename coincidence or prose.

## Proof provenance

The replayed proof is
`certificates/synthesis_k3_hole9_orphan_000170_recovery/proof/addition-only.rup.drat`,
SHA-256
`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.
It is bound by:

- recovery certificate SHA-256
  `1a2d4f7fd3efe0138bb7a7a7f0975d3c60a7ed4d6f994157c5383f18e4b5806c`;
- accepted review record SHA-256
  `ebede11b90e6e0b73d75f57c7706ba2e62e699281fcd8c15a208886dd53db291`.

An independent byte parser confirmed 4,705 addition lines, no deletion line,
and a final empty clause.

There is also a mathematical reuse argument.  RUP is monotone under adding
initial clauses: every unit-propagation contradiction used for a proof step
from the old formula and preceding additions remains available in a stronger
formula.  The exact clause-subset audit therefore already justifies reuse.
The present artifact goes further and replays the proof directly against the
complete formula, so its acceptance does not rely only on that argument.

## Checker identity and exact replay

The checker is the pinned DRAT-trim source snapshot dated 2023-05-22:

| artifact | SHA-256 |
|---|---|
| binary | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| source archive | `2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108` |
| retained help output | `0fb0bbb58764ef4e622b31dce9a6f91c2539f75e8b34743a6ee9a778e21bb36c` |

The binary exposes no semantic-version string; the snapshot date and exact
binary/source hashes are the version identity.

The decisive checker command was:

```text
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/tools/drat_trim_2023_05_22/drat-trim
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/results/synthesis_k3_template_bank_packages/hole9/instance.cnf
/Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination/certificates/synthesis_k3_hole9_orphan_000170_recovery/proof/addition-only.rup.drat
-I -f -W -U -t 60
```

Here `-I` forces ASCII proof parsing, `-f` requests forward UNSAT checking,
`-W` exits on the first warning, and `-U` forbids non-RUP additions.

The retained results are:

| artifact or measurement | value |
|---|---|
| exit code | 0 |
| stdout SHA-256 | `ba921cba6d4f3ea5478e8a370625869d0631d9e86bbe8a6183dd1d9a84294819` |
| stderr SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| exact `s VERIFIED` lines | 1 |
| warnings in combined logs | 0 |
| RAT lemmas reported | 0 |
| checker wall time | 0.08 s |
| checker user/system CPU | 0.07 s / 0.00 s |
| maximum resident set size | 53,264,384 bytes |

The checker itself reported parsing 6,886 variables and 20,795 clauses.  The
stdout, stderr, and resource record are retained unchanged alongside the JSON
binding.

## Independent post-replay checks

The reviewer reparsed both CNFs, the proof, and both checker logs without
importing the bank generator.  The checks required:

1. exact DIMACS dimensions;
2. old-to-new clause-multiset inclusion with exactly 595 added clauses;
3. exactly 4,705 well-formed addition-only proof lines ending in `0`;
4. exactly one standalone `s VERIFIED`;
5. no case-insensitive `warning` substring in either checker log;
6. empty checker stderr; and
7. the checker statement `0 RAT lemmas`.

All checks passed, and every hash and byte size in `replay.json` was then
recomputed from the named artifact.

## Certificate boundary

This replay certifies UNSAT only for the exact complete `hole9` template
formula.  It does not by itself settle `hole5`, `hole7`, the complete
\((n,k)=(12,3)\) slice, or the universal \(\gamma\)--\(\theta\) conjecture.
It also does not change the already accepted graph-theoretic scope of the
`hole9` exclusion; it supplies a cleaner complete-coloring-bank formula
binding for that same template.
