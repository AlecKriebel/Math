# Hostile review of the exact template-compatible coloring banks

## Verdict

**ACCEPT the frozen author source, tests, and mathematical note for commit and
post-commit package generation.**  I found no mathematical, enumeration,
complement-sign, clause-construction, or deterministic-generation defect.

This is not approval to solve a development fixture.  Before any production
solve, the frozen runtime sources must be committed, the three retained
packages must be regenerated from that commit, and the independent manifest
audit must confirm `runtime_sources_match_head=true`.  The disposable review
fixtures honestly record `false` because the new source and note were
uncommitted at their recorded `HEAD`.

No SAT solver or proof checker was launched by this hostile review.

## Frozen objects

| object | SHA-256 |
|---|---|
| `src/synthesis_k3/template_color_bank.py` | `dc69687f01e85bea643b73f713b1afca51b3911b3fee4a857da3fb07cc979838` |
| `tests/test_template_color_bank.py` | `cc89c89133593a986a77d683ec253bf7db49e53f3ba27ede03e4fcee89fccdf7` |
| `math/lemmas/template_coloring_bank.md` | `abc9568d70eee6b792e4220b58c12f5e7c069a13e37dbd3265025abe02cd6f50` |
| independent hostile probe | `0a55ea60334be110b4b45998078d0050e726f7b1ff223a6d87250778bbe1cb26` |

The author reported a stable-tree 12/12 test pass in 60.876 seconds.  I
independently reran the 11 tests that do not invoke the live solver smoke:
11/11 passed in 62.153 seconds, with peak RSS 62,308,352 bytes.  Compilation
and whitespace checks also passed.

## Independent mathematical audit

The probe imports no campaign module and reconstructs the mathematical object
from the written convention \(H=\overline G\).  Edge variables are independently
assigned as

\[
e_{01}=1,\ldots,e_{10,11}=66
\]

in lexicographic pair order.  For `holeℓ`, the forced-positive \(H\)-edges are
the rim of \(C_\ell\), together with \(0\ell\) and \(1\ell\).  In particular,
\(\{0,1,\ell\}\) is a forced triangle.

The chromatic polynomial gives \(2^\ell-2\) labeled proper colorings of the
odd rim.  Vertex \(\ell\) is forced to the third color and the remaining
\(11-\ell\) vertices are free.  Since the forced triangle makes the action of
the six color-name permutations free, the exact number of first-use
partitions is

\[
\frac{(2^\ell-2)3^{11-\ell}}6.
\]

This gives 3,645, 1,701, and 765 for `hole5`, `hole7`, and `hole9`.

The probe did not rely only on this formula.  For each template it separately:

1. recursively enumerated all restricted-growth strings;
2. exhausted all \(3^{12}=531{,}441\) labeled assignments;
3. canonicalized every compatible assignment;
4. proved that each bank row has exactly six labeled representatives; and
5. checked that every incompatible assignment's same-color clause contains a
   forced-true \(H\)-edge and is therefore already satisfied by a template
   unit.

The compatible labeled counts were 21,870, 10,206, and 4,590, respectively.
Thus the bank is neither missing a color partition nor importing an assignment
that is improper on a forced edge.

For every row \(c\), the probe independently constructed exactly

\[
\bigvee_{u<v,\ c_u=c_v} e_{uv}.
\]

Every literal is positive.  No clause contains a forced-true template edge.
Forced-false rim-chord literals are retained, as required for the exact
uniform clause definition.

## Independent formula and artifact audit

The probe independently allocated all 6,886 variables and reconstructed the
complete base encoding from the mathematical specification, including the
no-\(K_4\), pair-witness, template, connectivity, domination, one-guard
transition, nonempty-family, and maximum-independent-state clauses.  It does
not import either the author module or `synthesis_k3.encoding`.

| template | base clauses/literals | full clauses/literals | bank SHA-256 | full CNF SHA-256 |
|---|---:|---:|---|---|
| `hole5` | 20,008 / 114,601 | 23,653 / 188,959 | `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00` | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |
| `hole7` | 20,017 / 114,612 | 21,718 / 148,551 | `371ab3b01ce2add1138e0c0c78d267a796bcc536c79f95050face4bfcd4d11a7` | `6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7` |
| `hole9` | 20,030 / 114,619 | 20,795 / 129,559 | `d4361c57730765112c80e9348561a063a2ad7eae9ad00d3986dcb111446b5ef7` | `baea72050aaec8f41bad4e245fff8409489a9270f76ab0ffc97f0271f49dca01` |

For all three fixtures, the bank JSON and full DIMACS bytes were identical to
the independent reconstruction.  A second fixture generation in a separate
resolved temporary directory produced identical bank, CNF, and manifest
hashes.  The author's own exhaustive package audit also passed for all three.

The manifest was independently checked through its identity, forced-edge
list, count identity, base hash and clause interval, header-free bank-clause
stream hash, artifact sizes and hashes, runtime source hashes, source-set
hash, Git object replay, generation recipe, and canonical JSON bytes.  It
reached only the deliberately stronger production gate: the two new runtime
files are not yet present at development `HEAD`
`f667fb289fed6c9cfe380645140133ecb4a29b14`.

## Accepted `hole9` proof reuse

The accepted recovery stream contains 170 distinct first-use `hole9`
colorings.  Every one is an exact member of the new 765-row bank.  The
accepted CNF with SHA-256
`2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d`
has the independently reconstructed 20,030-clause base followed by exactly
those 170 clauses.  Therefore it is a clause subset of the complete-bank CNF.

The previously accepted addition-only proof has 4,705 RUP additions and
SHA-256
`24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab`.
RUP is monotone under adding axioms: unit propagation from the negation of a
candidate addition can only gain implications when clauses are added.
Consequently the already verified proof remains a valid RUP derivation from
the stronger complete-bank formula.

As an executable confirmation, pinned DRAT-trim
`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`
replayed that addition-only proof directly against the 20,795-clause
complete-bank fixture with flags `-I -f -W -U`.  It exited zero, emitted one
warning-free `s VERIFIED`, used no RAT lemma in the core, and completed in
0.083 seconds.  No new SAT solve is needed for the `hole9` bank.

## Mutation audit

The independent probe rejected all eight deliberate semantic mutations:

- a missing row;
- a duplicate row;
- a non-first-use color permutation;
- a negative/complement-sign-flipped cut literal;
- deletion of a forced-nonedge literal from an exact cut;
- replacement of a forced rim edge by a rim chord;
- admission of a row whose clause contains a forced-true edge; and
- an edge-variable endpoint/offset confusion.

The author tests separately exercise malformed and mutated bank artifacts,
deterministic bytes, existing-output refusal, protected and symlinked paths,
hostile resource types, validation gates, and explicit nonclaim outcomes.

## Remaining gate

After committing the frozen runtime sources:

1. generate retained packages for all three templates from the new `HEAD`;
2. run this probe on each bank, CNF, and manifest;
3. require `runtime_sources_match_head=true` and no source mismatch;
4. preserve the successful checker-only `hole9` replay with the retained
   post-commit package; and
5. only then consider proof-producing work for `hole5` and `hole7`.

The review does not claim that either remaining template is unsatisfiable and
does not elevate a solver timeout or absent candidate to a mathematical
result.
