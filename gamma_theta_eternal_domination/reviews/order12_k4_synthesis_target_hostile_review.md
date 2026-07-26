# Hostile review of the order-12, parameter-four synthesis target

## Verdict

### Mathematical note

**`ACCEPT_EXACT_CONNECTED_ORDER12_K4_TARGET`.**

The reviewed note correctly derives an exact anchored CNF whose models,
after projecting the auxiliary variables, are connected 12-vertex graphs
\(G\) satisfying
\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\]
The fixed \(H=\overline G\) four-clique is a sound relabeling of one
maximum independent four-set of \(G\).  Conversely, every such connected
graph has a model after fixing an anchor and permuting the outer labels to
satisfy the optional signature order.  The one-guard clauses quantify only
unoccupied attacks, move one named guard along one edge of \(G\), and force
the exact one-swap successor into the same dominating family.

The exact final census is
\[
 18{,}381\text{ variables},\qquad
 114{,}742\text{ clauses},\qquad
 1{,}180{,}016\text{ literals}.
\]
In particular, the earlier estimate of 840 signature-order clauses and
115,477 total clauses is not the encoding in the note.  The proved
first-difference comparator needs 15 clauses per adjacent pair, hence 105
clauses for seven comparators.  The note's smaller count is correct.

The SPGT branch list
\[
 C_5,\quad C_7,\quad C_9,\quad\overline{C_7}
\]
is exhaustive for the connected target.  The note also correctly refuses
to impose hub-free hole clauses and correctly warns that independently
fixing the labels of an anchor and a template is unsound.

This acceptance is a theorem about the exact synthesis target.  It is not a
SAT or UNSAT result and does not exclude the \((12,4)\) slice.

### Implementation

**`ACCEPT_EXACT_CONSTRUCTOR_IN_NO_CLAIM_MODE`.**

The reviewed implementation emits exactly the clauses proved in the note.
A clean-room reconstruction that imported none of `synthesis_k4` was
byte-identical to every emitted mode.  The supplied nine-test suite passes,
and the additional independent exhaustive and mutation checks described
below found no semantic or serialization defect.

**`REJECT_DECISIVE_CERTIFICATION_USE_AT_THIS_STAGE`.**

This second verdict is a scope boundary, not an encoding defect.  No solver
has been run, no proof has been produced, and no independent proof checker
or exhaustive cube-coverage package is attached.  The in-module decoded
candidate validator is useful defense in depth but is not independent of
the search encoder and cannot be the sole checker of a decisive artifact.

Review date: 2026-07-26 PDT.

## 1. Reviewed working-tree bytes

The audit applies to these exact, then-uncommitted bytes:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `math/lemmas/order12_k4_synthesis_target.md` | 19,489 | `5421357c5095113ac598afa22fa5a4e3623ef19d3c3a7a348b6c6c9a29945671` |
| `src/synthesis_k4/__init__.py` | 58 | `05e51b8d8a86f51f045db00dc10f4042dcf25218448473193b620fc87fe76d3d` |
| `src/synthesis_k4/encoding.py` | 18,036 | `193d3e4984cd2fcfa327cc693d518221ba51544bf8ea9e0cbca37c693e34e2e0` |
| `src/synthesis_k4/generate.py` | 6,757 | `7f257a47e3a59a226aa1e46bcba42eb3a2cc18e0059a1e906eb93b8960158bcc` |
| `tests/test_synthesis_k4_encoding.py` | 9,582 | `b800ac630dbf16dbd88e0c7cdccf7511dd3c8f8c29f508a73a901237d63595b4` |
| `reviews/order12_k4_synthesis_target_hostile_probe.py` | 39,803 | `04b355c28b93a7e45c9161699924a192b1c06df10cfd9e6da6115374099c9709` |
| `reviews/order12_k4_synthesis_target_hostile_probe_log.json` | 6,087 | `a1166ec3c1afbfd0d2020bf69f46c6af5ee2457ca296de8be7dc9b3dc0589d1a` |

These hashes must be refreshed if any reviewed source changes.  They are not
a substitute for a Git freeze or a production run manifest.

## 2. Static complement theorem

Put \(H=\overline G\).  The three static conditions are:

1. a fixed \(K_4\) on vertices \(0,1,2,3\);
2. no \(K_5\) in \(H\); and
3. for every triple \(A\), an \(x\notin A\) adjacent in \(H\) to every
   member of \(A\).

They are equivalent, up to the anchor relabeling, to
\(\gamma(G)=\alpha(G)=4\).

For the forward implication, \(\alpha(G)=4\) gives an \(H\)-\(K_4\) and no
\(H\)-\(K_5\).  Since \(\gamma(G)=4\), no triple dominates.  A triple
\(A\) fails to dominate exactly when some outside vertex is nonadjacent in
\(G\), hence adjacent in \(H\), to all of \(A\).

For the reverse implication, the first two conditions give
\(\alpha(G)=4\).  The third says no triple dominates, so
\(\gamma(G)\geq4\).  The anchored four-set is a maximum independent set in
\(G\), hence a maximal independent and therefore dominating set, giving
\(\gamma(G)\leq4\).

The note does not replace \(\gamma=\alpha\) by well-coveredness.  This is
important: well-coveredness alone is not a valid search target.  Here the
static conditions prove the explicit endpoint equality
\(\gamma=\alpha=4\); the parameter chain then gives \(i=4\), so
well-coveredness follows.

Two proposed structural leads are also correct, although not needed by the
CNF:

- Every pair \(a,b\) has at least two distinct common \(H\)-neighbors.
  Choose a third vertex \(c\); a witness \(x\) for \(\{a,b,c\}\) is one
  common neighbor.  A witness \(y\) for \(\{a,b,x\}\) is outside that
  triple, so \(y\ne x\), and is a second common neighbor.
- Every maximal clique of \(H\) has size four.  A triangle extends directly
  by the triple condition.  An edge extends first to a triangle by applying
  the triple condition to its endpoints and any third vertex, then to a
  \(K_4\).  A singleton first extends to an edge by applying the condition
  to any triple containing it.  No clique can exceed four because \(K_5\)
  is forbidden.

As a bounded independent check, all 512 labeled six-vertex graphs
containing the fixed anchor \(K_4\) were enumerated.  Exactly 58 satisfied
the three static conditions, and in all 512 cases those conditions agreed
with an independent exhaustive computation of
\(\gamma(G)=\alpha(G)=4\).  This finite check supports but is not used in
the proof above.

## 3. Eternal-family clauses

There are \(\binom{12}{4}=495\) possible four-guard states.  A selected
state \(D\) is required to dominate \(G\) by
\[
 \neg f_D\vee\bigvee_{u\in D}\neg e_{ux}
\]
for every \(x\notin D\).  Because \(e_{ux}\) denotes an \(H\)-edge,
\(\neg e_{ux}\) is exactly a \(G\)-edge.  Thus this clause rejects a selected
state precisely when an outside vertex is adjacent in \(H\) to every guard,
equivalently undominated in \(G\).

For every \(D\), every \(r\notin D\), and every \(u\in D\), the move
variable \(m_{D,r,u}\) has the implications
\[
 m_{D,r,u}\Longrightarrow \neg e_{ur},
 \qquad
 m_{D,r,u}\Longrightarrow
 f_{(D-\{u\})\cup\{r\}}.
\]
The attack-response clause is
\[
 f_D\Longrightarrow\bigvee_{u\in D}m_{D,r,u}.
\]
Consequently:

- \(r\notin D\), so occupied vertices are never attacked;
- \(\neg e_{ur}\) means \(ur\in E(G)\);
- the successor removes exactly \(u\) and adds exactly \(r\);
- the selected successor dominates by the selected-state clauses; and
- the response disjunction is existential.  More than one true move
  variable records several available one-guard responses; it does not mean
  several guards move simultaneously.

The family-nonempty clause completes the definition.  Conversely, any
eternal four-family extends to the move variables by choosing one legal
response for each state/attack pair.  The optional implication from every
\(H\)-\(K_4\) to \(f_D\) is sound because every independent four-set of
\(G\) is forced into every four-guard eternal family.  No \(K_5\) makes
every such four-set maximum.

The clauses therefore give \(\gamma^\infty(G)\leq4\), while the already
proved \(\alpha(G)=4\) and the general inequality
\(\alpha\leq\gamma^\infty\) give equality.

## 4. Independent census

The variable count recomputes as follows:

| family | count |
|---|---:|
| \(H\)-edge variables | \(66\) |
| triple/common-neighbor witnesses | \(220\cdot9=1,980\) |
| selected four-states | \(495\) |
| move witnesses | \(495\cdot8\cdot4=15,840\) |
| **total** | **18,381** |

The base-clause census was independently regenerated:

| family | clauses | literals |
|---|---:|---:|
| no \(K_5\) | 792 | 7,920 |
| triple-witness existence | 220 | 1,980 |
| triple-witness implications | 5,940 | 11,880 |
| anchor units | 6 | 6 |
| connected \(G\)-cuts | 2,047 | 67,584 |
| selected-state domination | 3,960 | 19,800 |
| family nonempty | 1 | 495 |
| move-edge and successor implications | 31,680 | 63,360 |
| attack-response disjunctions | 3,960 | 19,800 |
| \(H\)-\(K_4\)-to-family strengthening | 495 | 3,465 |
| **base** | **49,101** | **196,290** |

The cut count is \(2^{11}-1=2,047\).  Each unordered pair crosses exactly
\(2^{10}\) represented cuts, including pairs incident with vertex zero, so
the cut literal total is
\(\binom{12}{2}2^{10}=67,584\).

## 5. Complete four-coloring bank

The anchored \(H\)-\(K_4\) uses all four colors in any proper
four-coloring.  There is a unique color-name permutation making the anchor
colors \(0,1,2,3\), so exactly
\[
 4^8=65,536
\]
normalized rows suffice.

For one normalized coloring \(c\), the positive clause
\[
 \bigvee_{c(u)=c(v)}e_{uv}
\]
is false exactly when no same-color pair is an edge of \(H\), which is
exactly when \(c\) is proper.  Requiring every row therefore says
\(\chi(H)>4\), equivalently \(\theta(G)\geq5\).  The sign is positive
because the bank is coloring \(H\), not \(G\).

Across all rows, the eight anchor/outer equal-color pairs contribute
\(8\cdot4^8\) literals.  Each of the 28 outer pairs is same-colored in
\(4^7\) rows.  Hence the bank has
\[
 8\cdot4^8+28\cdot4^7=983,040
\]
literals.  Adding it to the base gives 114,637 clauses and 1,179,330
literals.

The implementation audit enumerated every one of the 65,536 emitted rows,
not a sample.  Every row was exactly the set of same-color \(H\)-edge
variables.  For each row, the graph containing all cross-color pairs and no
same-color pair falsified the clause and admitted that coloring; adding one
named same-color edge satisfied the clause and invalidated that coloring.
No row error occurred.

## 6. Outer-signature ordering

For one adjacent pair of outer vertices, the proposed clauses forbid a
first differing bit \(1,0\).  At first-difference coordinate \(t\), there
are \(2^t\) possible equal prefixes and each clause has \(2t+2\) literals.
Thus one comparator has
\[
 \sum_{t=0}^3 2^t=15\text{ clauses},\qquad
 \sum_{t=0}^3 2^t(2t+2)=98\text{ literals}.
\]
Seven adjacent comparators add 105 clauses and 686 literals.

An independent truth table checked all \(16^2=256\) pairs of four-bit
signatures for each of the seven emitted comparator blocks, for 1,792
block/input combinations.  Every block accepted exactly the pairs
\(s(\mathrm{left})\leq_{\rm lex}s(\mathrm{right})\).

Permuting the eight outer vertices while fixing the anchor maps every edge,
witness, family, and move variable to a variable of the same role.  It also
permutes the complete normalized coloring bank.  Every orbit therefore has
a representative with nondecreasing signatures.  No assumption about the
graph is added.

The previously suggested count of 840 is the size of a different,
uncompressed construction with 120 explicit forbidden ordered signature
pairs for each of seven adjacent comparators.  It is not required.  The
15-clause first-difference construction is equivalent and yields the
correct final total of 114,742 clauses.

This \(S_8\) action is not automatically retained after forcing a
particular labeled SPGT template.  The note states this limitation
correctly.

## 7. SPGT and template audit

For a target, \(\omega(H)=4<\chi(H)\), so SPGT supplies an induced odd hole
or odd antihole.

An induced \(\overline{C_{2q+1}}\) in \(H\) has clique number \(q\), so
\(q\leq4\) and only lengths \(5,7,9\) need consideration.  The length-five
antihole is \(C_5\).  A length-nine antihole in \(H\) gives an induced
\(C_9\) in \(G\); the self-contained cycle argument proves
\(\gamma^\infty(C_9)=5\), and induced-subgraph monotonicity contradicts
\(\gamma^\infty(G)=4\).  A length-seven antihole remains possible because
\(\gamma^\infty(C_7)=4\).

The general cycle proof in the note was checked attack by attack.  Starting
from the forced maximum independent set
\(\{0,2,\ldots,2m-2\}\), the attack at 1 either immediately loses
domination or forces the guard at 2 to 1.  The attacks
\(3,5,\ldots,2m-3\) then have a unique adjacent guard and the final move
leaves \(2m-1\) undominated.  Every attack is unoccupied and exactly one
guard is moved.  The clique-cover strategy supplies the matching upper
bound \(m+1\).  An independent fixed-point evaluator additionally returned
\[
\begin{array}{c|rrrr}
n&5&7&9&11\\ \hline
\gamma^\infty(C_n)&3&4&5&6\\
\gamma^\infty(\overline{C_n})&3&3&3&3
\end{array}
\]
as a bounded consistency check.

An induced \(C_{11}\) in \(H\) has one outside vertex \(x\).  For two rim
vertices \(v_0,v_3\) at cycle distance three, no rim vertex is adjacent to
both.  A common neighbor of \(\{x,v_0,v_3\}\) cannot be \(x\) itself and
would have to be such a rim vertex, contradicting the triple-common-neighbor
condition.  This correctly eliminates \(C_{11}\).

Thus the only remaining possibly overlapping templates are
\(C_5,C_7,C_9,\overline{C_7}\).

No hub-free restriction is justified at \(k=4\).  An odd wheel in \(H\)
complements to
\[
 K_1\mathbin{\dot\cup}\overline{C_{2q+1}}
\]
in \(G\), whose eternal domination number is \(1+3=4\).  Induced
monotonicity therefore gives only the already known lower bound four, not a
contradiction.  The note correctly adds no no-hub clauses.

## 8. Anchor/template orbit caveat

A chosen anchor \(K_4\) and a chosen induced hole or antihole have an
intersection size and incidence pattern that are invariant under a common
relabeling.  Separate statements that each object can be moved to a
preferred label set do not imply they can both be moved to two independently
preferred label sets.

Accordingly, a certified template split must either encode template
existence invariantly, enumerate and cover all pair orbits, fix the template
while existentially selecting the anchor, or use the template only after
model extraction.  If a pair orbit is fixed, only its stabilizer may be
used for further symmetry breaking.  All four safe routes in the note are
sound.  No implemented template instance is audited here.

## 9. Connected and disconnected scope

The cut clauses say that every proper cut has a negative \(H\)-edge,
equivalently a \(G\)-edge, so the encoded graph \(G\) is connected.

This does not by itself cover every disconnected order-12 graph with total
parameter four.  Additivity and componentwise equality leave two cases:

1. a parameter-four counterexample component, which consumes the full
   domination budget and hence is the whole graph; or
2. a parameter-three counterexample component \(Q\) plus one component
   having \(\gamma=\gamma^\infty=1\).

The latter component has \(\alpha=1\) by the parameter chain and is
therefore a complete graph \(K_t\).  Conversely,
\(Q\mathbin{\dot\cup}K_t\) is a parameter-four counterexample whenever
\(Q\) is a parameter-three counterexample.  Thus the connected formula plus
separate, accepted exclusions of parameter-three counterexamples on orders
\(12-t\) is needed for a full disconnected \((12,4)\) claim.  The note
states this gap exactly and does not misuse the general connected reduction.

## 10. Clean-room implementation reconstruction

The standard-library-only probe
`reviews/order12_k4_synthesis_target_hostile_probe.py` allocated the
variables independently in the documented order and regenerated every
clause without importing `synthesis_k4` or `synthesis_k3`.  Its canonical
output is frozen at
`reviews/order12_k4_synthesis_target_hostile_probe_log.json`.  A fresh run
was byte-identical to that log.

The reconstructed DIMACS streams were byte-identical to the generator
output:

| mode | variables | clauses | literals | bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| base | 18,381 | 49,101 | 196,290 | 1,008,612 | `df2bb53af5e3fd63bf51846ae85c5d133d5dca58ff6181924a0077deb363df17` |
| bank | 18,381 | 114,637 | 1,179,330 | 3,990,501 | `33f208024840c17b2068f804d9924c31a969d2c5dccf601533b1958a14cc8c42` |
| full | 18,381 | 114,742 | 1,180,016 | 3,992,947 | `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac` |

A second generation in a separate temporary directory reproduced all three
hashes.  Independent DIMACS parsing confirmed each header, clause count,
literal count, variable bound, terminating zero, and absence of internal
zeroes.  The 18,381 generated variable names were all distinct.

The source manifest in the audited full-mode run independently rebound all
four named sources and had source-set SHA-256
`8df9cc832d3b9d46ccc9eb314498a0f68b81d7fdd986e894abd01cc752c07162`.
The manifest's normalized invocation replayed successfully from its named
normalized working directory under an otherwise empty environment and
reproduced the same CNF and JSON.

The generator's path defenses rejected:

- identical output and manifest paths;
- distinct paths that were hard links to the same file; and
- an output path aliasing a trusted source.

The generator writes both files atomically and rehashes the installed CNF.
Its claim status is exactly `NO_MATHEMATICAL_CLAIM`.

The permanent no-claim full instance was also compared byte-for-byte with
the clean-room reconstruction:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `instances/order12_k4_connected_parent/instance.cnf` | 3,992,947 | `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac` |
| `instances/order12_k4_connected_parent/manifest.json` | 4,113 | `621a0878c117dc8b4d6dbd0ba14c8402a8c24e8339d2f85cb23d61ffd74fbb61` |
| `instances/order12_k4_connected_parent/README.md` | 1,012 | `7aaf80399e62a9e9ed227a66c63e8cea5190253228f28a13911c682f93207ead` |

The permanent manifest passed the same independent field, source-set,
clause-family, and byte-binding checks.  Its README contains both the exact
CNF hash and the explicit `NO_MATHEMATICAL_CLAIM` boundary.

## 11. Independent mutation checks

Seven targeted in-memory faults were injected into a parsed copy of the
full DIMACS and compared with the clean-room schema.  Every mutation was
detected:

| mutation | semantic error admitted | result |
|---|---|---|
| change \(\neg m\vee\neg e_{ur}\) to \(\neg m\vee e_{ur}\) | move along an \(H\)-edge, hence a \(G\)-nonedge | killed |
| point a move at the wrong one-swap state | missing the named successor | killed |
| point a move at a state differing in several guards | all-guards-style jump | killed |
| substitute a response variable tied to an occupied target in the source state | occupied-vertex attack confusion | killed |
| delete one successor implication | successor need not remain selected | killed |
| reverse all \(H/G\) signs in one domination clause | an undominated outside vertex is accepted | killed |
| reverse one coloring-bank row | complement-coloring confusion | killed |

The independent variable-key scan also confirmed that all 15,840 move
variables have \(r\notin D\) and \(u\in D\).  For every move key, the emitted
successor is exactly \((D-\{u\})\cup\{r\}\).

The supplied tests passed:

```text
.........
----------------------------------------------------------------------
Ran 9 tests

OK
```

The supplied tests alone peaked at about 118 MB resident memory.  The full
clean-room probe, including two generator passes per mode, all exhaustive
semantic checks, cycle fixed points, and the supplied tests, peaked at about
137 MB.  Both are far below the campaign's M1 Pro limit.  No SAT solver was
invoked.

## 12. Exact promotion blockers

No correction to the mathematical target or emitted CNF is required by
this review.  The following are nevertheless blockers to a stronger claim:

1. **No computational result.**  Construction of a CNF is neither SAT nor
   UNSAT and supports no exclusion claim.
2. **Connected-only universe.**  A full order-12, parameter-four result
   also needs accepted coverage of the disconnected
   parameter-three-plus-\(K_t\) cases.
3. **No labeled-template shortcut.**  A template-based partition needs an
   anchor/template pair-orbit coverage proof or an invariant existence
   encoding before it is exhaustive.
4. **No production proof stack.**  Any UNSAT result needs frozen source and
   instance hashes, proof-producing runs, strict independent proof replay,
   and a coverage audit for every cube.
5. **No independent decisive candidate verifier.**  The validator in
   `encoding.py` shares the encoder module.  A SAT candidate must be checked
   by a compact implementation with no shared transition or coloring core.
6. **Source-stability gate.**  A certificate-producing runner must bind a
   frozen commit or rehash every runtime source before and after generation
   and solving.  The present one-pass construction manifest is sufficient
   for `NO_MATHEMATICAL_CLAIM`, not by itself for a decisive run.

Within these explicit boundaries, both the mathematics and its current
implementation are accepted.
