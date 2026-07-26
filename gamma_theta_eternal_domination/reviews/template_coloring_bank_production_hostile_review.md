# Production hostile audit of retained template-coloring-bank packages

## Verdict

**ACCEPT** all three retained packages as exact, exhaustive,
source-bound production inputs.

The audit was completed at `2026-07-26T03:34:04Z` against committed `HEAD`

`2e68a6396735381ee634a572dda409610b40891f`

on `main`.  The same commit was present at `origin/main`.  No package file was
altered and no SAT solver was launched.

## Independent audit boundary

The decisive audit used
`reviews/template_coloring_bank_hostile_probe.py`, SHA-256
`0a55ea60334be110b4b45998078d0050e726f7b1ff223a6d87250778bbe1cb26`.
That standard-library probe imports neither
`synthesis_k3.template_color_bank` nor the synthesis encoder/search code.  It
independently:

1. reconstructed the forced-positive \(H=\overline G\) edges;
2. enumerated the first-use canonical coloring partitions;
3. exhausted all \(3^{12}=531{,}441\) labeled assignments per template;
4. reconstructed the edge-variable map, all 6,886 variables, every base
   clause, and every same-color bank clause;
5. required canonical byte-exact bank JSON and DIMACS;
6. checked the complete manifest, artifact hashes and sizes, base and bank
   clause-stream bindings, source-set hash, and canonical JSON; and
7. replayed each recorded source hash directly from the recorded Git commit.

All checks passed independently for `hole5`, `hole7`, and `hole9`.

## Exact retained artifacts

| template | bank rows | full clauses / literals | bank SHA-256 | CNF SHA-256 | manifest SHA-256 |
|---|---:|---:|---|---|---|
| `hole5` | 3,645 | 23,653 / 188,959 | `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00` | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` | `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402` |
| `hole7` | 1,701 | 21,718 / 148,551 | `371ab3b01ce2add1138e0c0c78d267a796bcc536c79f95050face4bfcd4d11a7` | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` | `7c46b015dd58e321428c7d0bb8b896d27ae8ce0fb4bc9566199e43f86fa17185` |
| `hole9` | 765 | 20,795 / 129,559 | `d4361c57730765112c80e9348561a063a2ad7eae9ad00d3986dcb111446b5ef7` | `baea72050aaec8f41bad4e245fff8409489a9270f76ab0ffc97f0271f49dca01` | `e36e7ab02bdc001c09fe0f9d12f8257483a695c758c1f29dd4a3ac2cb4d0ab83` |

The package-tree digests, using the campaign's sorted relative-path,
big-endian-length, file-byte convention, are:

| template | tree SHA-256 | files / bytes |
|---|---|---:|
| `hole5` | `48220656e20c7740effca29005c3cf746e8db0d29484a23474582eb48b4b2ed2` | 3 / 1,081,321 |
| `hole7` | `e2cee17b3417a1c5b85f37ebb70f7c4b2db01d43b156f1e08696bfc75615ebb8` | 3 / 781,499 |
| `hole9` | `4de791e930bbb0fd516ab673f7bf0c18bf360f89414e600c72fbfc45849a1a1d` | 3 / 638,660 |

The combined nine-file tree has SHA-256
`71cbee54f028419570cdf11ad4116ed7202243c99fcc4c681558c70e4764a6a5`
and size 2,501,480 bytes.

## Exhaustive semantics

For `hole5`, `hole7`, and `hole9`, respectively, the independent enumeration
found exactly 3,645, 1,701, and 765 partitions.  The exhaustive labeled
compatible counts were 21,870, 10,206, and 4,590.  Every partition had
exactly six color-name representatives.  Every one of the remaining labeled
assignments violated a forced-positive \(H\)-edge, so its generic
same-color clause was already satisfied by a template unit.

Each retained CNF was byte-for-byte identical to the independently
reconstructed base followed by the exact complete bank:

| template | base clauses / literals | base-CNF SHA-256 |
|---|---:|---|
| `hole5` | 20,008 / 114,601 | `6bc1d90cb355aa167105cb7adbd2ef226ac68c73594b62b3944abbf376dd10a0` |
| `hole7` | 20,017 / 114,612 | `88585f4f23571eda09b1941fa773c77b23b328e5f140ca78cec6c6efe3101ae1` |
| `hole9` | 20,030 / 114,619 | `cf555f359dc887c89f84e35a40ee649e77ef805b2690ec34e72cc4ef75e5d5c7` |

Thus there is no complement-sign reversal, forced-nonedge coloring
constraint, missing partition, duplicate partition, clause-offset error, or
shared transition-core dependency in this acceptance.

## Manifest and source provenance

Every manifest records:

- `head_commit` equal to
  `2e68a6396735381ee634a572dda409610b40891f`;
- `runtime_sources_match_head=true`;
- an empty `runtime_source_mismatches` list; and
- runtime source-set SHA-256
  `71b36c6d44b50e31406b437fedf093ae1e60cb1a7823ed4ced2a429fa8dd9c08`.

The audit independently fetched every recorded source with `git show` from
that exact commit and matched it both to the manifest digest and the current
worktree byte stream.  In particular, the committed author source and
mathematical note remain:

- `template_color_bank.py`:
  `dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838`;
- `template_coloring_bank.md`:
  `abc9568d70eee6b792e4220b58c12f5e7c069a13e37dbd3265025abe02cd6f50`.

No uncommitted runtime-source substitution is present.

## Path and filesystem audit

The retained root resolves inside
`gamma_theta_eternal_domination/results/` and outside the protected `src`,
`math`, and `tools` trees.  Every path component from `/Users` downward is a
real directory, not a symlink.  Each package contains exactly:

- `coloring_bank.json`;
- `instance.cnf`; and
- `manifest.json`.

All nine artifacts are regular, non-symlink files with link count one.
There are no hidden or extra package entries.  Files currently have mode
`0644` and package directories mode `0755`; integrity is supplied by the
exact manifest, tree, Git, and prospective run-input hashes rather than by an
immutable filesystem bit.

## Production consequence

The packages are suitable for preservation and bounded production use.  The
already accepted 4,705-addition `hole9` proof was previously replayed
successfully against the identical retained CNF hash
`baea72050aaec8f41bad4e245fff8409489a9270f76ab0ffc97f0271f49dca01`;
therefore no new `hole9` SAT search is needed.  Any `hole5` or `hole7` solve
must bind the exact hashes above and retain its own proof and checker
artifacts.  Package acceptance alone does not claim either remaining formula
unsatisfiable.
