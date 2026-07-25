# Hostile review of the order-12, parameter-three synthesis stack

**Review date:** 2026-07-25 PDT  
**Review scope:** exact base CNF, complement translation, four SPGT
templates, coloring cuts, decoded semantic validation, DSATUR coloring, and
deterministic instance generation.  No CEGAR search was run.

## Final narrow repair re-review

**Re-review date:** 2026-07-25 PDT

### Frozen repaired files

| File | SHA-256 |
|---|---|
| `src/synthesis_k3/__init__.py` | `fbc5ca4211eb97b498e0eecd692333596bba409c26629623f8d547a48a379e86` |
| `src/synthesis_k3/encoding.py` | `fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6` |
| `src/synthesis_k3/coloring.py` | `9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713` |
| `src/synthesis_k3/generate.py` | `456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1` |
| `tests/test_synthesis_k3_encoding.py` | `da1cd28cfa8c9e594621d41e12f3ce00ea2958ff7b429ed546053c019139de89` |
| `tests/test_synthesis_k3_coloring.py` | `8aaabc68a3656f933e6f47221e505f8c0c626b94e03f53e90aeff9191143f06e` |
| `math/synthesis_k3_cegar_design.md` | `57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8` |

The revised independent probe is
`reviews/synthesis_k3_encoding_hostile_probe.py`, SHA-256
`0b241af3abaaea316e653dd5a61ae5669b918ac2ac0611a7f4bf23585cfc5aba`.

### Final verdict

**ACCEPT the repaired CNF encoding, decoder-domain semantic validator,
template coverage, coloring cuts, and DSATUR implementation without a
mathematical reservation.**  The complete clause reconstruction still
matches exactly and all base DIMACS hashes are unchanged.

**ACCEPT the H1, M1, M2, L1, L2, L3, and T1 repairs.**  Direct, symbolic-link,
hard-link, input, and trusted-source collisions now fail before any write.
The exact coloring bytes used are read once, hashed before output, parsed
strictly in memory, and rehashed for stability.  The installed CNF is
rehashed.  Equivalent color partitions are canonicalized and rejected as
duplicates.  The decoder boundary rejects Boolean/float vertices, wrong
arities, reverse duplicates, and out-of-range records.  The design now gives
the correct distinct triangle for the antihole branch.

**R1 is closed.**  The manifest records the absolute campaign working
directory, the required absolute `PYTHONPATH`, and a normalized invocation
whose first entries are `/usr/bin/env`, that `PYTHONPATH` assignment, and the
absolute Python executable.  The hostile probe executed the exact recorded
argv from the recorded working directory under `env={}`.  It returned zero,
its stdout decoded to the recorded manifest, and the regenerated CNF,
manifest, and coloring input were byte-for-byte identical to their
pre-replay versions.  The focused regression independently performs the
same empty-environment replay.

The generator source-set hash for the reviewed bytes is
`e48f1b430cfa5d1421bb8e7c856d70db8fc634b27d6cbd51d7d22e11f16d30bd`.
There is no remaining finding in the requested review scope.

### Repair replay

The revised probe obtained:

- successful execution of the exact manifest-recorded normalized invocation
  under an empty environment, with byte-identical regenerated artifacts;
- nine path-role rejections, including direct output/manifest/input aliases,
  a symbolic output/manifest alias, an output/manifest hard link, direct,
  symbolic, and hard-link aliases of `generate.py`, and a hard-link
  output/input alias; all protected bytes remained unchanged;
- rejection of ten hostile JSON payloads, including duplicate keys,
  `NaN`, positive/negative infinity, invalid UTF-8, a BOM, Boolean/float
  colors, a short row, and an out-of-range color;
- rejection of a globally color-permuted duplicate partition;
- detection of an injected post-install CNF mutation;
- detection of an input-coloring mutation after CNF installation but before
  report construction;
- exact verification of every source-manifest record and its aggregate hash;
  and
- rejection of the formerly accepted Boolean endpoint in a valid decoded
  base model.

The mathematical probes were repeated unchanged: 1,024 labeled
five-vertex complements, 10,240 checks each of pair, triple, and move
translations, 1,024 connectivity equivalences, all local auxiliary truth
tables, 400 template relabelings, every one of the 1,100 labeled graphs
through order five against transparent coloring enumeration, and 1,400
additional varied-color deterministic cases.  There was no discrepancy.

The 12 focused synthesis tests and the full 144-test repository suite pass.
No full CEGAR search was run.  The repaired generator and its manifest are
accepted for audited instance construction and self-contained one-command
replay on the reviewed source tree and runtime.

## Initial review snapshot (superseded by the final re-review above)

| File | SHA-256 |
|---|---|
| `src/synthesis_k3/encoding.py` | `fef89f213554786bc3e1b89c3d25fc3b69d31e8a1bdb3413c05c92b13945c988` |
| `src/synthesis_k3/coloring.py` | `9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713` |
| `src/synthesis_k3/generate.py` | `69238ba6e27619d46d619dea628776a479fd4fb517c28c2e51833cd93a34aafe` |
| `tests/test_synthesis_k3_encoding.py` | `5b4a2373c69c32b30e8cc022685a6561b0237db74fae92ed042db368c9d56df8` |
| `tests/test_synthesis_k3_coloring.py` | `8aaabc68a3656f933e6f47221e505f8c0c626b94e03f53e90aeff9191143f06e` |
| `math/synthesis_k3_cegar_design.md` | `f61114df8bd8d44614d9a78dff7da7cbbc48b494563d16cd4acca2809a52e833` |

The initial independent probe was
`reviews/synthesis_k3_encoding_hostile_probe.py`, SHA-256
`33114fb1b093ffdb05df5c5c2186959c01fd8ef94c4eb56e225aef9722728ad6`.
It imports neither eternal-domination verifier and no search engine.

## Verdict

**ACCEPT the mathematical base CNF, all four template encodings and their
coverage/relabeling argument, the coloring-cut logic, and the DSATUR
algorithm.**  I reconstructed the complete clause multiset independently;
there was no missing, extra, or sign-reversed clause in any template.  The
existential witness and move gadgets project exactly to the intended graph
and one-guard-family predicates.

**ACCEPT `validate_decoded_candidate` on values produced by
`decode_edges`/`decode_family`, subject to a low-severity hostile-input
hardening defect.**  It directly checks every nonredundant base semantic
condition.  Non-three-colorability is intentionally outside its scope and
must remain a separately certified step.

**DO NOT USE `generate.py` for durable certificate production until finding
H1 is fixed.**  Normal, nonaliased generation is byte-correct, but path-role
collisions can destroy inputs or replace the CNF with its manifest while
returning a manifest whose CNF hash is false.  Findings M1 and M2 must also be
fixed before treating its manifest as the campaign's required reproducibility
record.

No critical mathematical defect and no DSATUR completeness defect was found.

## Severity-ranked findings

### H1 — High: generation path collisions corrupt or destroy artifacts

`generate()` does not require `output`, `manifest`, and `colorings_path` to
be distinct, and it does not protect checker sources or other trusted inputs.
The defect has two direct reproductions:

1. With `output == manifest`, the function first installs the DIMACS bytes,
   then replaces the same path with JSON.  It returns successfully.  The
   resulting manifest's `cnf_path` names the JSON file, while
   `cnf_sha256` is the hash of the vanished DIMACS bytes.
2. With `output == colorings_path`, the coloring JSON is parsed and then
   replaced by DIMACS before `colorings_sha256` is computed.  The input is
   destroyed and the manifest hashes the CNF as though it were the coloring
   input.

The analogous `manifest == colorings_path` case destroys the input after
hashing it.  A caller can also point either output at a source, checkpoint,
or prior certificate.  Atomic replacement makes each individual write
well-formed; it does not make these role collisions safe.

**Required correction:** resolve all paths before any write; reject every
read/write and write/write alias, including symlink aliases and existing
same-file/hard-link aliases.  Protect the generator/checker source set
explicitly.  Read and hash the coloring input before creating any output.
Add regression tests for all three direct collisions, symlink aliases,
trusted-source aliases, and unchanged input bytes after both success and
failure.

### M1 — Medium: the manifest does not bind the generator

The manifest binds the CNF and optional coloring file, but not
`encoding.py`, `generate.py`, the variable-map implementation, Python
runtime, command line, or a generator source-set digest.  Thus it cannot
serve as the source-bound instance manifest required by the campaign
protocol.  The CNF hash still identifies the precise SAT instance and a
proof checker can validate a proof against those bytes, so this is a
reproducibility/coverage defect rather than a false SAT formula.

**Required correction:** add an exact source manifest and source-set hash,
runtime/version, normalized invocation, template-proof/design hash, and
generator schema/version.  Rehash the installed CNF and write the report only
after the installed bytes match.  The eventual CEGAR manifest must separately
bind each model, coloring, learned clause, solver binary, proof, and proof
checker.

### M2 — Medium: coloring bytes are parsed and hashed in separate reads

`load_colorings()` parses the file, but `generate()` hashes the path later,
after generating and installing the CNF.  Even when paths are distinct, a
concurrent change can make `colorings_sha256` describe bytes different from
those used to construct the cuts.  H1 gives a deterministic version of this
time-of-check/time-of-use problem.

**Required correction:** read the input once as bytes, hash those exact bytes,
strictly parse that in-memory payload, and optionally verify at the end that
the path still has the same hash.  Reject duplicate JSON keys/nonfinite
constants under the campaign's normal strict-JSON policy.

### L1 — Low: the fixed-triangle explanation is false for `antihole7`

Section 1, item 3 of `math/synthesis_k3_cegar_design.md` says the template
constraints force rim edge \(01\) and an external common neighbor \(z\),
hence a triangle.  This is true for `hole5`, `hole7`, and `hole9`.  The
`antihole7` template instead forces \(e_{01}=0\) and chooses no external
vertex.  It nevertheless forces many triangles, for example
\(\{0,2,4\}\), so the conclusion \(\omega(H)=3\) and the encoder are sound.

**Exact correction:** split the explanation by branch: the hole templates
force \(\{0,1,\ell\}\), while the complement-\(C_7\) template forces
\(\{0,2,4\}\).

### L2 — Low: decoded validation accepts non-integer vertex aliases

`validate_decoded_candidate` checks numeric ranges but not exact endpoint
types.  Python therefore accepts `True` as vertex `1`, and integral floats
similarly alias integers.  Replacing endpoint `1` in a valid decoded base
model by `True` was accepted.  Wrong-arity or noniterable records can also
escape as `TypeError` instead of a controlled `ValueError`.

This cannot invalidate a graph produced by the two decoder methods, whose
vertices are genuine integers, and the interpreted edge set in the Boolean
reproduction was unchanged.  It is still inappropriate for a strict
hostile-input certificate boundary.

**Required correction:** parse records explicitly, require tuples/lists of
the exact arity, and require `type(vertex) is int` before sorting or
normalizing.  Add Boolean, float, wrong-arity, noniterable, duplicate, and
out-of-range tests.

### L3 — Low: color permutations produce duplicate logical cuts

`load_colorings()` rejects identical rows but not color permutations.
For example, `c(v)=v mod 3` and `c'(v)=c(v)+1 mod 3` produce identical
same-color clauses, yet both are appended and counted.  This is sound but
inflates the CNF and makes `coloring_cut_count` count rows rather than
distinct clauses.

**Suggested correction:** canonicalize each coloring by first occurrence of
its color classes, or deduplicate the generated clauses.  If retained,
document that the count is an input-row count.

### T1 — Low: focused tests omit the generator and decoded validator

The supplied focused tests correctly check the main clause shapes and DSATUR
through order four.  They contain no normal or hostile test of `generate()`
and no call to `validate_decoded_candidate`.  They therefore do not detect
H1, M1, M2, or L2.

Add generation round trips, exact installed-file hash checks, collision
tests, source-manifest checks, direct validation of SAT-decoded base models,
and semantic mutations for every validator branch.

## Clause-by-clause mathematical audit

### Complement and static parameters

An edge variable is true exactly for an edge of \(H=\overline G\).

- Each four-set clause is the negation of its six-edge conjunction, hence
  enforces \(\omega(H)\leq3\).
- For a pair \(a,b\), the witness disjunction plus
  \(w_{ab,c}\Rightarrow e_{ac}\) and
  \(w_{ab,c}\Rightarrow e_{bc}\) is satisfiable over the auxiliary variables
  exactly when \(a,b\) have an external common neighbor in \(H\).  Reverse
  implications are unnecessary.
- In \(G\), a pair fails to dominate exactly when such a common neighbor
  exists.  Exhaustive comparison on all 1,024 labeled five-vertex graphs
  checked all 10,240 pair instances without discrepancy.
- The selected-triple clause
  \(\neg f_T\vee\neg e_{xa}\vee\neg e_{xb}\vee\neg e_{xc}\)
  is false exactly when selected \(T\) leaves outside vertex \(x\)
  undominated in \(G\).  All 10,240 triple instances on the same graphs
  agreed with direct closed-neighborhood domination.

Every template supplies a triangle, so \(\omega(H)=3\).  Together with the
common-neighbor condition, no pair dominates \(G\), while a maximum
independent triple does; hence \(\gamma(G)=\alpha(G)=3\).

### Connectivity cuts

For each proper cut \(S\mid\bar S\) with \(0\in S\), the disjunction of
\(-e_{uv}\) over crossing pairs requires a crossing edge of \(G\).  Such
cuts represent every unordered cut exactly once.  The generated masks are
exactly the 2,047 proper sides containing zero, with no duplicate crossing
literal.  On all 1,024 five-vertex \(H\), the conjunction of the analogous
cut predicates agreed with a direct breadth-first traversal of \(G\).

### One-guard response variables

For fixed selected state \(T\) and unoccupied attack \(r\), existentially
quantifying the three move variables gives

\[
 \neg f_T\ \lor\
 \bigvee_{u\in T}
 \bigl(\neg e_{ur}\land f_{(T-\{u\})\cup\{r\}}\bigr).
\]

The probe exhausted all 128 primary truth rows and all eight auxiliary move
assignments per row.  The gadget was satisfiable exactly under this formula.
Thus:

- \(r\notin T\) is enforced by variable construction;
- the named guard traverses one edge of \(G\), represented by a nonedge of
  \(H\);
- only that guard is replaced;
- the successor is selected and is therefore subject to every domination
  clause; and
- more than one true response variable merely records several legal choices,
  not simultaneous guard movement.

Move variables attached to an unselected state need not be forced false.
This creates nonunique auxiliary models but no false graph/family projection:
they may always be set false, and if set true they only add restrictions.

### Maximum-independent strengthening

The clause

\[
 \neg e_{ab}\vee\neg e_{ac}\vee\neg e_{bc}\vee f_{\{a,b,c\}}
\]

is precisely “every triangle of \(H\) is selected.”  Since the four-clique
clauses and each template give \(\omega(H)=3\), these triangles are exactly
the maximum independent triples of \(G\).  The already proved
maximum-independent-state lemma says every such triple belongs to every
eternal family of three-sets.  The strengthening is therefore redundant and
does not remove a target.

## Four-template coverage and relabeling audit

For a hole of length \(\ell\in\{5,7,9\}\), the unit clauses force exactly the
rim cycle and exclude all rim chords.  Each external-vertex clause forbids
that vertex from being complete to the rim, exactly the odd-wheel
obstruction.  The endpoints of a rim edge have no common neighbor on an
induced cycle of length at least five.  The global pair condition therefore
gives an external common neighbor; choosing one and labeling it \(\ell\)
makes the two fixed positive units sound.  The remaining labels are free.

At order 12, a hole cannot have length 11: its sole external vertex would
have to be a common neighbor for every rim edge and hence a forbidden hub.
The only possible odd-hole lengths are therefore 5, 7, and 9.

The `antihole7` units correctly force the complement of the labeled cycle:
the seven cycle pairs are nonedges of \(H\), and all 14 other rim pairs are
edges.  Any induced \(\overline{C_7}\) can be oriented and relabeled into
this form, with the other five labels arbitrary.  This is the certified
fourth fallback branch if odd-antihole elimination is not used.

The probe built 100 independently permuted abstract witnesses for each of
the four templates, constructed the theorem's relabeling, and checked all
fixed constraints.  All 400 passed.  The four branches are overlapping but
exhaustive relative to SPGT and the previously accepted structural lemmas.

## Coloring-cut audit

For a fixed assignment \(c:V\to\{0,1,2\}\), the returned clause is

\[
 \bigvee_{u<v,\ c(u)=c(v)}e_{uv}.
\]

It is false exactly when \(c\) is a proper coloring of \(H\).  Every
non-three-colorable graph satisfies it for every assignment \(c\), whether
or not \(c\) arose from the current model.  Therefore every accumulated cut
is a consequence of the target condition.  If base CNF plus any subset of
these valid cuts is UNSAT, no non-three-colorable target exists in that
template.  Conversely, a proper coloring returned for a SAT model makes its
cut false and excludes that graph.

The probe reconstructed every literal for three differently shaped
colorings and checked 768 local edge truth rows.  The sign and use of \(H\),
not \(G\), are correct.

## DSATUR completeness audit

`find_coloring` maintains the invariant that used color labels form the
initial interval \(0,\ldots,m\).  At each selected vertex it tries every
allowed used color and at most the single new label \(m+1\).  Any proper
extension using a differently named new color can be relabeled to \(m+1\).
The DSATUR vertex key depends on the number of distinct neighbor colors, the
fixed degree, and vertex index, all invariant under such a color-label
permutation.  Hence the symmetry restriction cannot remove a color
partition.  Exhausting these branches is a complete decision procedure.

An independent transparent assignment oracle agreed on all 1,100 labeled
graphs through order five.  An additional 1,400 deterministic random cases
covered orders 0 through 6 and color counts 1 through 4.  Every returned
coloring was checked directly.  No discrepancy occurred.

`None` remains an internal exhaustive-search result, not a portable
noncolorability certificate.  The design correctly requires a separately
frozen/certified candidate rather than treating DSATUR's `None` alone as a
publication result.

## Exact reconstruction and base probes

The independent clause reconstruction matched the actual clause multiset
exactly:

| Template | Variables | Clauses | Literals | Base DIMACS SHA-256 |
|---|---:|---:|---:|---|
| `hole5` | 6,886 | 20,008 | 114,601 | `6bc1d90cb355aa167105cb7adbd2ef226ac68c73594b62b3944abbf376dd10a0` |
| `hole7` | 6,886 | 20,017 | 114,612 | `88585f4f23571eda09b1941fa773c77b23b328e5f140ca78cec6c6efe3101ae1` |
| `hole9` | 6,886 | 20,030 | 114,619 | `cf555f359dc887c89f84e35a40ee649e77ef805b2690ec34e72cc4ef75e5d5c7` |
| `antihole7` | 6,886 | 20,010 | 114,575 | `4f6e5a260b6719f3258ee4f0b35de7f685ab6622bfe462a67680b7728762009c` |

With local CaDiCaL 3.0.1, binary SHA-256
`51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6`,
the three hole bases were SAT.  Their decoded models had respectively
23/42, 26/54, and 29/60 edges/family states; every model literal satisfied
the reconstructed CNF and each graph/family passed direct semantic
validation.  All three graphs were three-colorable, as expected before
coloring cuts.  The `antihole7` base returned UNSAT, consistent with the
induced-\(C_7\) obstruction in \(G\).  These were subsecond base probes, not
a CEGAR run; no solver outcome here is promoted to a certified finite
theorem.

The supplied eight focused tests passed.  The independent probe and the full
repository suite should be rerun after H1–M2 are corrected, because every
source hash and all generated artifact hashes will then change.
