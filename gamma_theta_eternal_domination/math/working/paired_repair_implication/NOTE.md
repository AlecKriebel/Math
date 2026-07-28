# Paired repair in a response bicycle: exact logic and a sharp gamma-two obstruction

## Status and exact scope

Date: 2026-07-28 (PDT)

All graph statements use the standard one-guard-moves eternal-domination
model.  Attacks are made only at unoccupied vertices, exactly one adjacent
guard moves, and every retained state dominates.

The proposed automatic paired-repair descent is **false** at the level of
one selected critical-pair witness plus local eternal closure.

1. **PROVED:** the two almost-cap arms replace a marked implication-path
   segment of length \(d\) by a segment of length two.  The opposite
   contradiction path is retained, but strict shortening occurs only for
   \(d>2\).  Choosing shortest contradiction paths does not force this
   inequality.
2. **PROVED:** when the almost-cap resolvent and the opposite signed route
   yield Boolean endpoint units, those units are resolution consequences,
   not unit clauses or singleton response lists.  Accepted C-079 cannot
   be invoked without an additional physical terminal-support theorem;
   C-094 does not supply that theorem because it does not transport
   clause edges.
3. **EXACT GAMMA-TWO COUNTERCONTROL:** the 19-vertex graph
   `RBn]r]vj]lnZ~^~n~z~^z|~nz~^j~w` has
   \[
      (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)
   \]
   and a checked 703-state eternal triple-family in which every outside
   list is an exact two-list.  It realizes three complete tight gates with
   odd holonomy and an external dynamic almost-cap at one critical pair.
   The two almost-cap clauses resolve to an already essential clause of
   the bicycle.  Replacing that clause by the two arms increases a shortest
   marked path from four arcs to five and produces another
   inclusion-minimal **unit-free** bicycle.

The control has \(\gamma=2\), so it does not refute a theorem that
essentially uses the global condition \(\gamma\geq3\) at more than the
selected critical pair.  It is not a gamma--theta counterexample.  The
universal \(k=3\) case and the gamma--theta conjecture remain open.

No literature-priority claim is made.

## 1. The exact path-replacement lemma

Let \(F\) be a binary 2-CNF, and suppose two directed implication paths

\[
 P:p\leadsto\bar p,\qquad
 R:\bar p\leadsto p
\tag{1.1}
\]

witness a unit-free bicycle.  Let \(X,Y\) occur in this order on \(P\),
and let the \(X\)--\(Y\) segment of \(P\) have \(d\) implication arcs.

An exact third-type almost-cap introduces a new variable \(Q\) and the two
clauses

\[
 A=\bar X\lor Q,\qquad B=Y\lor\bar Q.
\tag{1.2}
\]

Their implication arcs are

\[
 X\longrightarrow Q\longrightarrow Y,\qquad
 \bar Y\longrightarrow\bar Q\longrightarrow\bar X,
\tag{1.3}
\]

and their resolvent on \(Q\) is

\[
 C=\boxed{\bar X\lor Y}.
\tag{1.4}
\]

### Lemma 1.1 (oriented replacement) — PROVED

Replacing the \(X\)--\(Y\) segment of \(P\) by the first path in (1.3)
gives a new path

\[
 P':p\leadsto\bar p
\]

of length

\[
 |P'|=|P|-d+2.
\tag{1.5}
\]

The opposite path \(R\) is unchanged.  Consequently the replacement:

- strictly shortens the marked bicycle if \(d>2\);
- preserves its marked length if \(d=2\); and
- lengthens it if \(d=1\).

#### Proof

Concatenate the prefix of \(P\) ending at \(X\), the two arcs in (1.3),
and the suffix of \(P\) beginning at \(Y\).  This deletes exactly \(d\)
arcs and adds exactly two.  No clause or arc of \(R\) is changed.
\(\square\)

The contraposed arm in (1.3) gives the identical replacement in the
contraposed copy of the marked segment.  It does not improve the numerical
bound (1.5).

### Corollary 1.2 (shortest paths do not imply descent)

If the resolvent \(C\) is already an essential clause of the selected
core, then one marked path can use its arc \(X\to Y\) with \(d=1\).
Replacing that physical clause by the two almost-cap arms subdivides the
arc and makes the path one step longer.  Orienting the critical pair along
shortest contradiction paths cannot change this.

This is exactly what happens in the graph control of Section 3.

## 2. Resolution-derived units are not physical terminals

Suppose an odd signed route between \(X\) and \(Y\) supplies the two
inequality clauses

\[
 \bar X\lor\bar Y,\qquad X\lor Y.
\tag{2.1}
\]

Resolving these separately with (1.4) gives

\[
 \bar X,\qquad Y.
\tag{2.2}
\]

At the Boolean level the complementary even route can now be described
as a chain between two forced literals.  This is useful proof bookkeeping,
but it does **not** turn the response formula into the two-unit case of the
minimal-2-CNF trichotomy.  The clauses in (2.2) need not occur in the
formula.  In fact an inclusion-minimal core containing (1.2) can remain
entirely binary and therefore remain a unit-free bicycle.

The distinction is decisive for the graph argument.

- A unit clause in the response formula is supported by a fixed projection
  orientation, often through a singleton response list or a clause meeting
  an already fixed component.
- A resolution-derived unit is supported by a tree of binary clauses.  Its
  physical ports may be distinct vertices in the same projection
  component.
- C-079 requires a literal positive response at one terminal port, an odd
  path in one omitted-color projection, and one physical complement
  neighbor incident with that port and both path ends.
- C-094 supplies a same-sign physical representative for an exact
  two-list literal, but C-095 shows that it need not retain even one
  specified clause edge.  C-098 repairs a failed incidence by another
  virtual gate, not by manufacturing a singleton response vertex.

Thus a resolution derivation of (2.2) supplies none of the missing
incidences required by C-079.  Accepted C-086 gives cap-location and
side-purity restrictions; it does not exclude an arbitrary long
two-unit chain.  Treating C-079/C-086 as an automatic exclusion of the
logical units in (2.2) would exceed their proved hypotheses.

A sufficient future lemma would have to be a **physical terminal-support
lemma**: at least one derived unit must admit a single physical port and
the common terminal incidence required by C-079, or an independently
proved physical two-unit attack geometry.  No such lemma follows from
shortest-path orientation alone.

## 3. A full gamma-two response-bicycle control

Let \(H=\overline G\) on vertices \(0,\ldots,18\), with anchor state

\[
 S=\{0,1,2\}.
\]

The complement edges are

```text
01 02 03 07 0-11
12 14 18 19
25 26 2-10
37 39 3-15
48 4-10 4-16 4-18
56 5-11 5-17
69 6-12 6-18
7-10 7-13
8-11 8-14
12-15 13-16 14-17
```

where hyphens only disambiguate two-digit labels.  The corresponding
graph6 record is

```text
RBn]r]vj]lnZ~^~n~z~^z|~nz~^j~w
```

and \(G\) has 139 edges.

### 3.1 The canonical restricted eternal family

Prescribe the exact response lists

\[
\begin{array}{c|l}
\text{list}&\text{vertices}\\ \hline
\{1,2\}&3,7,11,12,15,18\\
\{0,2\}&4,8,9,13,16\\
\{0,1\}&5,6,10,14,17.
\end{array}
\tag{3.1}
\]

Start with all dominating triples except the sixteen forbidden direct
swaps \(S-u+v\) for which \(u\notin L(v)\).  Repeatedly delete every
triple having an unoccupied attack with no retained one-guard successor.
The simultaneous deletion rounds have sizes

\[
 51,\ 37,\ 63,\ 29,\ 10
\]

and stabilize at a 703-state family \(\mathcal F\).  Its manifest hash is

```text
c116c4a60299fea35d30bf09bda9b1faa31b39533caac8eb265818cd1347874d
```

The verifier checks all

\[
 703(19-3)=11{,}248
\]

unoccupied attack obligations and reconstructs the lists (3.1).  In
particular there is no singleton response list.

Independent exhaustive checks give

\[
 \boxed{(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)}.
\tag{3.2}
\]

The family proves \(\gamma^\infty\leq3\), while the independent state
\(S\) proves \(\gamma^\infty\geq\alpha\geq3\).  The anchor triangle in
\(H\) and the displayed three-coloring in `result.json` certify
\(\theta=3\).

### 3.2 Three complete tight gates

The three length-one same-type connectors are

\[
 3\,7,\qquad4\,8,\qquad5\,6\in E(H).
\tag{3.3}
\]

For \(i=0,1,2\), the five columns below are respectively the left
physical port, right physical port, cap, original right port, and the
middle vertex of its length-two physicalization path:

\[
\begin{array}{c|ccccc}
i&\ell_i&r_i&z_i&o_i&m_i\\ \hline
0&6&3&9&12&15\\
1&7&4&10&13&16\\
2&8&5&11&14&17.
\end{array}
\tag{3.4}
\]

For every row,

\[
 \ell_i z_i,\ r_i z_i,\ \ell_i o_i,\ o_i m_i,\ m_i r_i
 \in E(H),
\qquad
 \ell_i r_i\in E(G).
\tag{3.5}
\]

The original clause \(\ell_io_i\), the even same-type path
\(o_i-m_i-r_i\), and the two cap arms form the complete tight gate.
Each gate preserves chirality, while every connector in (3.3) reverses
it.  The three reversals give odd holonomy, so the anchored response
formula is uncolorable.

### 3.3 The dynamic almost-cap

The critical pair is

\[
 \{4,6\}.
\]

Its unique common complement neighbor is \(q=18\), and

\[
 4q,6q\in E(H),\qquad
 0q\in E(G),\qquad
 L(q)=\{1,2\}.
\tag{3.6}
\]

Thus \(q\) is an exact third-type **dynamic** almost-cap: it supplies both
arm clauses, but it is not physically incident in \(H\) with the omitted
anchor \(0\).

The graph has 93 dominating pairs, for example \(\{0,11\}\).  Hence
\(\gamma=2\); the local witness (3.6) does not extend to the global
common-complement-neighbor condition for every pair.

## 4. Exact response formula and failure of strict descent

Deterministic bipartitioning of the free omitted-color components gives
seven Boolean variables:

\[
\begin{array}{c|c|c}
\text{variable}&\text{omitted color}&\text{component vertices}\\ \hline
1&0&3,7,12,15\\
2&0&11\\
3&0&18\\
4&1&4,8,13,16\\
5&1&9\\
6&2&5,6,14,17\\
7&2&10.
\end{array}
\tag{4.1}
\]

The eleven cross clauses, with their literal supporting complement edges,
are

\[
\begin{array}{c|c|c}
j&\text{clause}&H\text{-edge}\\ \hline
0&\bar1\lor\bar5&3\,9\\
1&4\lor7&4\,10\\
2&\bar4\lor\bar3&4\,18\\
3&\bar6\lor2&5\,11\\
4&\bar6\lor5&6\,9\\
5&6\lor1&6\,12\\
6&6\lor3&6\,18\\
7&\bar1\lor\bar7&7\,10\\
8&1\lor\bar4&7\,13\\
9&4\lor\bar2&8\,11\\
10&\bar4\lor6&8\,14.
\end{array}
\tag{4.2}
\]

Clauses 2 and 6 are exactly the almost-cap arms.  Resolving them on
variable 3 gives

\[
 \operatorname{Res}_3(2,6)=\bar4\lor6,
\tag{4.3}
\]

which is already clause 10, supported elsewhere by the physical edge
\(8\,14\).

There is a unique minimum unsatisfiable core:

\[
 I_0=\{0,1,3,4,5,7,8,9,10\},
\qquad |I_0|=9.
\tag{4.4}
\]

The unique smallest inclusion-minimal core containing both almost-cap
arms is

\[
 I_q=\{0,1,2,3,4,5,6,7,8,9\},
\qquad |I_q|=10.
\tag{4.5}
\]

Thus \(I_q\) is obtained from \(I_0\) by replacing clause 10 with its
two-clause subdivision 2,6.  Every clause in both cores is binary.
Consequently both cores are unit-free bicycles under the accepted
minimal-2-CNF trichotomy.

For a concrete marked literal, the shortest paths in \(I_0\) have
lengths four and five.  One forward path is

\[
 4\longrightarrow1\longrightarrow\bar5
 \longrightarrow\bar6\longrightarrow\bar4,
\tag{4.6}
\]

where the last arc is clause 10.  In \(I_q\) its direct replacement is

\[
 4\longrightarrow1\longrightarrow\bar5
 \longrightarrow\bar6\longrightarrow3\longrightarrow\bar4,
\tag{4.7}
\]

using clauses 6 and 2.  The opposite marked path is retained:

\[
 \bar4\longrightarrow7\longrightarrow\bar1
 \longrightarrow6\longrightarrow2\longrightarrow4.
\tag{4.8}
\]

The verifier reconstructs shortest path lengths

\[
\begin{array}{c|cc}
&4\leadsto\bar4&\bar4\leadsto4\\ \hline
I_0&4&5\\
I_q&5&5.
\end{array}
\tag{4.9}
\]

This is the promised sharp obstruction.  The one-sided chord does not
lose the reverse path, but it also does not shorten the forward path or
create an actual unit clause.  It merely replaces one essential physical
clause by two different physical clauses having the same resolvent.

## 5. Consequence for the gamma-three proof target

The following proposed inference is invalid:

> choose a shortest bicycle, apply \(\gamma\geq3\) to one critical pair,
> resolve its third-type almost-cap arms, and conclude that the selected
> bicycle strictly shortens or becomes a C-079/C-086 terminal.

Sections 1 and 4 show the exact logical failure; Section 2 shows the exact
physical-support failure.  The control shows that the selected pair
witness and all local one-guard obligations can coexist with the failure.

A viable gamma-three argument must use more of the global hypothesis:
after an almost-cap merely subdivides an essential clause, one must apply
common-neighbor witnesses to additional pairs and prove either

1. a genuinely shorter unsatisfiable core;
2. a physical C-079 terminal with one common port;
3. an independently excluded physical two-unit geometry; or
4. a finite recurrence that yields a dominating pair.

Any descent measure must charge the new two-clause subdivision and remain
well founded under the C-095/C-098 incidence-repair operation.  Raw path
length, gate count, and the number of original clauses do not yet meet
that requirement.

## 6. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/paired_repair_implication/verify.py \
  --check math/working/paired_repair_implication/result.json
```

The verifier imports no campaign evaluator.  It reconstructs the graph,
restricted fixed-point family, all 11,248 one-guard obligations, exact
parameters, response lists, projection components, all eleven clauses,
both minimal cores, the resolvent identity, and the shortest marked paths.

