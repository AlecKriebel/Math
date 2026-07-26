# Hostile review of the `hole5` signature-order symmetry breaker

## Verdict

**ACCEPT the mathematical construction for the retained complete-bank
formula; implementation binding remains pending.**  Ordering vertices
\(6,\ldots,11\) by their six-bit \(H\)-adjacency signatures to the fixed
vertices \(0,\ldots,5\) is a sound label-symmetry breaker.  The independently
derived auxiliary-free encoding has exactly 315 clauses and 3,210 literals,
and adjoining it to the retained 6,886-variable, 23,653-clause complete-bank
CNF preserves satisfiability.

This verdict does not yet accept the author's implementation or note.  At the
start of this audit,
`src/synthesis_k3/hole5_signature_breaker.py` and
`math/lemmas/hole5_signature_symmetry.md` were untracked.  They were
deliberately neither read nor imported, so their hashes are not bound here.
After they are frozen, their generated clause multiset must be compared with
the independent construction below.

No SAT solver was run, and this review makes no SAT or UNSAT claim for
`hole5`.

## Independently audited objects

The frozen inputs were:

- complete `hole5` CNF SHA-256
  `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7`;
- coloring-bank SHA-256
  `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00`;
- package-manifest SHA-256
  `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402`.

The standalone probe is
`reviews/hole5_signature_symmetry_hostile_probe.py`, SHA-256
`3515adc846e961738b86c572a90aa0f42945cfa6794e3700986c392999c4ab66`.
It uses only the Python standard library and imports none of the synthesis
code.  Its exact canonical output is
`reviews/hole5_signature_symmetry_hostile_probe_log.json`, SHA-256
`f1d8f6d8d6f85bdffadcf39e5d4c4504b9cf0d1b8a609d8e5fe540523091b9de`.

## Independent variable reconstruction

The variable allocation was recreated by the documented nested
combinatorial order, without reading the author breaker:

| role | variables | count |
|---|---:|---:|
| \(H\)-edges \(e_{uv}\) | 1--66 | 66 |
| common-neighbor witnesses \(w_{uv,z}\) | 67--726 | 660 |
| eternal-family triples \(f_T\) | 727--946 | 220 |
| moves \(m_{T,r,u}\) | 947--6886 | 5,940 |

As an independent anchor on the edge-variable convention, rebuilding the
same-color clause for every one of the 3,645 retained bank rows reproduced
the last 3,645 CNF clauses exactly, including row order and literal order.
The parsed formula counts were independently confirmed as 6,886 variables,
23,653 clauses, and 188,959 literals, with 20,008 base clauses.

For a vertex permutation \(\pi\) fixing \(0,\ldots,5\), the full semantic
variable action is
\[
\begin{aligned}
e_{uv}&\longmapsto e_{\pi(u)\pi(v)},\\
w_{uv,z}&\longmapsto
  w_{\{\pi(u),\pi(v)\},\pi(z)},\\
f_T&\longmapsto f_{\pi(T)},\\
m_{T,r,u}&\longmapsto m_{\pi(T),\pi(r),\pi(u)}.
\end{aligned}
\]
Unordered pairs and triples are sorted back into their canonical key order.
Each resulting map was verified to be a bijection of all 6,886 variables.

## Exact \(S_6\) invariance

The five adjacent transpositions
\[
(6\ 7),(7\ 8),(8\ 9),(9\ 10),(10\ 11)
\]
generate \(S_{\{6,\ldots,11\}}\).  For each generator, the probe applied the
semantic action above and compared multisets of canonical clauses.

All five checks gave exact equality separately for:

- the 20,008-clause base;
- the 3,645-clause complete coloring bank;
- the full 23,653-clause CNF.

Each generator moved 20 edge variables, 290 witness variables, 90 family
variables, and 3,330 move variables.  Every one of the 3,645 bank rows mapped
back into the bank after color-name recanonicalization, and its mapped
same-color clause exactly equaled the clause of the transformed row.

Checking these generators suffices: invariance under generators is closed
under composition, so the full CNF is invariant under every permutation of
vertices \(6,\ldots,11\).  Vertex 5 is not included.  It is distinguished by
the template units making it the selected common neighbor of rim edge
\(01\).

## Independent comparator derivation

For an outer vertex \(v\), define its signature
\[
s(v)=(e_{0v},e_{1v},e_{2v},e_{3v},e_{4v},e_{5v})\in\{0,1\}^6.
\]
For adjacent outer labels \(x,y\), write
\[
A=s(x)=(a_0,\ldots,a_5),\qquad
B=s(y)=(b_0,\ldots,b_5).
\]
The desired condition is \(A\leq_{\rm lex}B\), with \(0<1\).

For every pivot \(i\in\{0,\ldots,5\}\) and prefix
\(p\in\{0,1\}^i\), use the clause
\[
\neg a_i\ \vee\ b_i\ \vee\
\bigvee_{\substack{j<i\\p_j=0}}(a_j\vee b_j)\ \vee\
\bigvee_{\substack{j<i\\p_j=1}}(\neg a_j\vee\neg b_j).
\tag{1}
\]
Clause (1) is false exactly when the two signatures share prefix \(p\)
and then have \(a_i=1,b_i=0\).  Therefore:

- if \(A>B\), take their first differing coordinate \(i\); the clause for
  their common prefix is false;
- if \(A\leq B\), no clause has the falsifying pattern.

Thus these clauses encode lexicographic order exactly, without auxiliary
variables.

For one adjacent pair, the number of clauses is
\[
\sum_{i=0}^{5}2^i=63,
\]
and the literal count is
\[
\sum_{i=0}^{5}2^i(2i+2)=642.
\]
The five adjacent comparisons consequently contribute exactly 315 clauses
and 3,210 literals.  Their clause-length distribution is
\[
2{:}5,\quad4{:}10,\quad6{:}20,\quad8{:}40,\quad
10{:}80,\quad12{:}160.
\]
The independently generated header-free DIMACS clause stream is 11,424
bytes and has SHA-256
`ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.

For each of the five adjacent pairs, all \(64^2=4,096\) ordered signature
pairs were evaluated.  In every case the CNF accepted exactly 2,080 pairs
and rejected 2,016, with zero disagreements from \(A\leq_{\rm lex}B\).
Every one of the 63 clauses had a violating assignment rejected uniquely by
that clause.

## Coverage proof

Let \(M\) satisfy the complete-bank formula \(F\).  Read the six signatures
of vertices \(6,\ldots,11\) from its edge variables and choose a permutation
\(\pi\in S_{\{6,\ldots,11\}}\) that places those signatures in nondecreasing
lexicographic order.  Equal signatures may be ordered arbitrarily.

Relabel the entire assignment, not merely its graph-edge projection:
\[
M^\pi(\pi(x))=M(x)
\]
for every edge, witness, family, and move variable \(x\), using the semantic
action above.  Since the fixed vertices are fixed, the signature appearing
at a new outer label is exactly the old signature of the vertex moved there;
outer-to-outer edges do not enter the signature.  The exact \(S_6\)
invariance proves \(M^\pi\models F\), while the chosen ordering gives
\(M^\pi\models S\), where \(S\) is the 315-clause breaker.

Hence every model of \(F\) has a relabeled model of \(F\land S\).  The reverse
direction is immediate, so
\[
F\text{ is satisfiable}\quad\Longleftrightarrow\quad
F\land S\text{ is satisfiable}.
\]
An independently checked UNSAT proof for the strengthened formula would
therefore prove the original complete-bank formula UNSAT.

This is label symmetry of the encoding.  It does not assert that an
individual graph has \(S_6\) as its automorphism group.

## Hostile mutations

The probe distinguishes genuinely unsound variants from merely different or
weaker sound conventions.

| variant | result |
|---|---|
| coordinatewise \(a_i\leq b_i\) | **reject**: accepts only 729 pairs, disagrees on 1,351, and neither orientation accepts `000001`/`000010` |
| one prefix literal instead of both literals in (1) | **reject**: same loss of orbit coverage |
| descending lex order | wrong stated orientation, but still sound if documented consistently; 4,032 disagreements from the ascending specification and no coverage loss |
| compare only the first coordinate | sound but strictly weaker; accepts 3,072 pairs and disagrees on 992 |
| permute edge variables but leave auxiliaries fixed | **reject**: 3,080 missing and 3,080 extra full-CNF clause occurrences; first mismatch is `-71 6` versus `-71 7` |
| fail to sort an unordered witness pair after relabeling | **reject**: \(w_{6,7,0}\) would be sent to the nonexistent ordered key \(w_{7,6,0}\) |

Naively sorting signatures that include coordinates indexed by other outer
vertices is also unsupported by this proof: those coordinates themselves
change under the simultaneous permutation.  Such a stronger canonical form
would need a separate argument or a genuine graph-canonicalization method.

## Coloring-orbit representative conflation

The accepted symmetry breaker performs one global relabeling of the graph
and all auxiliary data.  It does not justify replacing each orbit of
coloring cuts by one representative, because different colorings generally
require different graph relabelings to reach their representatives.

The probe supplies a concrete retained countermodel to that conflation.
Attempt 1's compressed SAT model has SHA-256
`e7e4d1f547a167d61aae301fd6e1ccc1d0ab5696e20894a9a087076693a33e75`;
its decompressed model payload has SHA-256
`ff0591d3cff245fb7277d0d310e8037d80cfef03a019782cf8dc117d0bb806aa`.
The independently parsed 6,886-variable assignment satisfies every one of
the 20,008 base clauses and the first CEGAR cut.  Its decoded \(H\) agrees
exactly with the first 66 model variables.

This \(H\) has bank row 739 as its unique proper bank coloring.  Nevertheless
it satisfies all 72 lexicographically minimum representatives under
\[
\langle(0\ 1)(2\ 4)\rangle\times S_{\{6,\ldots,11\}}.
\]
Row 739 belongs to the size-30 orbit represented by row 733.  The row-733
cut is true on this \(H\), witnessed by edge \(4\,10\), while the row-739 cut
is false.  Thus representative cuts are not equivalent to the full bank
even in the presence of the symmetric base.

Color-name canonicalization is different: permuting the three color names
does not change the equality relation and therefore produces the identical
same-color clause.  Graph-label images usually produce distinct clauses and
must remain unless a single global graph canonicalization is proved.

## Scope and production obligations

This review proves equisatisfiability for the retained **complete-bank** CNF.
It does not automatically prove formula-level equisatisfiability for the
non-orbit-closed 448-cut CEGAR prefix.  A semantic target argument using the
validity of every coloring cut may still justify a breaker there, but that is
a different claim and must not be silently substituted for CNF invariance.

Before a proof-producing `hole5` run relies on this breaker:

1. Freeze the author source and note and record their SHA-256 hashes.
2. Require the author's 315 generated clauses to equal the independent
   clause multiset above.  Exact stream equality should give SHA-256
   `ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`;
   a different clause order requires an explicit multiset comparison.
3. Verify the strengthened CNF has exactly 6,886 variables, 23,968 clauses,
   and 192,169 literals, with the retained complete CNF as its exact prefix
   or exact clause submultiset.
4. Rerun the standalone probe and require byte-for-byte agreement with its
   retained JSON log.
5. Independently verify any resulting UNSAT proof against the exact
   strengthened-CNF hash.

Subject to those implementation bindings, the signature ordering is a sound
and worthwhile proof-size experiment.
