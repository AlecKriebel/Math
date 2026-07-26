# Hostile review of the order-13 strategy

**Review date:** 2026-07-26  
**Reviewer scope:** independent mathematical, counting, byte-reconstruction,
and claim-boundary audit; no production solve  
**Strategy SHA-256:**
`eca21b547641f5f205bf9f5325d49f6c8edb6e6c778ff9fefacc7d1449e6b5c8`  
**Pilot-record SHA-256:**
`331630a55b5d35d27f92e4104172811ab9e8ccac6aa14bb84de538dbc2b7148c`

## Verdict

**`ACCEPT_BOUNDED_STRATEGY_WITH_THREE_DOCUMENTATION_CORRECTIONS`**

The mathematical reductions, template covers, complement translations, and
every reported combinatorial or DIMACS census are correct relative to the
stated accepted campaign inputs.  I found no mathematical, complement-sign,
one-guard-model, coverage, or arithmetic defect.

The document is exactly a strategy and sizing note.  It is not an order-13
exclusion, and the pilot's proofless solver return remains only
`OBSERVED`.  This review does not promote that return to evidence of UNSAT.

Three documentation corrections are warranted:

1. Lines 5--7 give an inaccurate dependency ledger for Proposition 1.
   Component additivity, C-003, is used essentially at lines 35--37 but is
   omitted; C-051 is listed but is not used in the parameter reduction.
   The proposition itself is valid.
2. Lines 17--18 report `0.021` seconds, which is not the ordinary rounding
   of the pilot record's `0.020179042010568082` seconds.  Section 3.3's
   `0.0202` seconds is accurate.
3. The exploratory pilot record omits the exact command/argv, CPU time, and
   an explicit solver-version field.  It also retains no stdout/stderr
   transcript.  The campaign's run-ledger discipline asks for those fields.
   Consequently the historical invocation cannot itself be replayed,
   although this review independently bound the exact formula, source, and
   solver bytes and queried the bound solver binary as version 3.0.1.

These are documentation and exploratory-ledger defects, not defects in a
proved or certified claim.  They should be corrected before treating the
note as a frozen production plan.

## 1. Frozen scope and accepted dependencies

The target bytes and their recorded sizes are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `math/lemmas/order13_strategy.md` | 14,643 | `eca21b547641f5f205bf9f5325d49f6c8edb6e6c778ff9fefacc7d1449e6b5c8` |
| `results/logs/order13_strategy_k3_template_pilot.json` | 3,177 | `331630a55b5d35d27f92e4104172811ab9e8ccac6aa14bb84de538dbc2b7148c` |

I checked the following accepted dependency bytes directly:

| dependency | SHA-256 |
|---|---|
| order-12 frontier C-049--C-050 | `adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75` |
| independent-antineighborhood projection C-051 | `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620` |
| independent C-051 review | `4da9ddf1b9d1f4087e5617dc6f6ae2428c0dd1ec576b8f89a3166418e4b7f7cb` |
| C-051 acceptance record | `791de946d25442b02ada35f950cd20d5abe3497141224e340364c30818a1b5a2` |
| parameter-three antihole elimination C-017 | `9e572203c09e082c3cbdfc0cdae8e4166007af3f909b73f7d8d2e196f04ddc4f` |
| C-017 hostile review | `7837fb360328533ea58a31d1a0eb60ef279a67d1e610144eb5206661ef38f5e3` |
| parameter-four structural split | `a28a544325549972191f40e087131316f5cd1a52b4f27d9a9ea617a31a4f5e5f` |
| structural-split hostile review | `cdc698b64c5796ce5323e803b0400a426a536bf44e04bbc5c9138154af93f322` |
| DoubleLex theorem C-045 | `d5be9b6373d7aa7c49dec32c18c6202698b35fe05a1f58b2b97dcc98d9114a76` |
| DoubleLex hostile review | `4cf3c5012a8b0ecfdcbad82c0fd2c283c2aebbd3396eaba9b232902956f86d8f` |
| half-order exclusion C-036 | `5d5e054305d97bf8e40f84073abd5236c6d726d66205b5e309ccfe39dd7d5f50` |
| core reductions, including C-003 and C-006 | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |

The through-order-12 premise remains explicitly relative to the published
MacGillivray--Mynhardt--Virgile computation through order 11.  The strategy
does not relabel that premise as a campaign-only certificate.

## 2. Proposition 1

Relative to C-050, an order-13 counterexample is minimum-order.  If it were
disconnected, additivity and equality of the sums
\(\gamma(G)=\gamma^\infty(G)\) make every component an equality graph, while
the strict total clique-cover gap forces at least one proper component to
retain a strict gap.  That component would be a smaller counterexample.
Thus the connectedness step is valid.

C-006 gives \(k\geq3\).  C-036 gives
\(13\geq2k+1\), hence \(k\leq6\).  C-049 applies to the minimum
counterexample and gives
\[
 13\geq\left\lceil\frac{5k}{2}\right\rceil,
\]
which excludes \(k=6\) but permits \(k=3,4,5\).  The exact possible set is
therefore \(\{3,4,5\}\).  No parameter is omitted.

The proof is mathematically sound.  The sole issue is the opening dependency
list described in the verdict.

## 3. C-051 complement dictionary

For a \(t\)-clique \(A\) of \(H=\overline G\), the same vertices form an
independent \(t\)-set in \(G\), and
\[
 V(G)-N_G[A]=\bigcap_{a\in A}N_H(a)=N_H(A).
\]
Since an order-13 counterexample is minimum relative to C-050, C-051 gives
\[
 \chi(H[N_H(A)])=\omega(H[N_H(A)])=k-t
\]
and nonemptiness for every \(1\leq t<k\).

Every entry of the table in lines 72--76 is the direct substitution
\(k-t\).  The interpretations are also exact:

- value one means a nonempty independent graph;
- value two means a bipartite graph with an edge;
- a clique of size \(t<k\) extends to a \(K_k\), because the common
  neighborhood has a clique of size \(k-t\);
- an odd cycle cannot be complete to a \((k-2)\)-clique;
- for \(k=3\), every open neighborhood of \(H\) is bipartite.

No statement confuses a coloring of \(H\) with one of \(G\), or a clique
partition of \(G\) with a coloring of \(G\).

## 4. Complete parameter-three template cover

For \(k=3\),
\(\omega(H)=3<\chi(H)\), so the Strong Perfect Graph Theorem supplies an
induced odd hole or odd antihole.  An odd antihole on \(2q+1\) vertices has
clique number \(q\), hence \(q\leq3\).  Its only possible lengths are five
and seven.  The five-antihole is \(C_5\); C-017 excludes
\(\overline{C_7}\).  Therefore \(H\) has an odd hole.

C-051 makes every vertex neighborhood bipartite, so no outside vertex can
be complete to that odd rim.  The possible hole lengths on 13 vertices are
\(5,7,9,11,13\).  A spanning induced \(C_{13}\) would make
\(H=C_{13}\), whose clique number is two rather than three.  Thus exactly
the overlapping cover
\[
 C_5,\quad C_7,\quad C_9,\quad C_{11}
\]
remains.

For every rim edge \(uv\), C-051 at \(t=2\) gives a common neighbor.
Inducedness of a cycle of length at least five means no rim vertex is
adjacent to both \(u\) and \(v\), so the witness is external.  Relabeling
one such witness after labeling the rim is orbit-complete and fixes no
unrelated anchor.  The four-template coverage proof is sound.

## 5. Independent formula-byte reconstruction

The standard-library-only script `audit.py` imports no campaign encoder,
coloring-bank generator, or search code.  It independently allocates every
edge, pair-witness, family, and move variable; emits every static,
connectedness, domination, one-guard transition, and independent-state
forcing clause; adds the exact hole, hub-free, and named-witness clauses;
enumerates all template-compatible restricted-growth three-color rows; and
serializes canonical DIMACS.

It reconstructed every exploratory formula byte for byte:

| branch | variables | base clauses | rows | full clauses | literals | bytes | SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| `hole5` | 9,802 | 29,791 | 10,935 | 40,726 | 493,820 | 1,805,539 | `8df56270f1abf3a9a8e5d088a78680dcde0198292eaa51da78a7fce9179d2fb5` |
| `hole7` | 9,802 | 29,800 | 5,103 | 34,903 | 349,248 | 1,372,338 | `3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340` |
| `hole9` | 9,802 | 29,813 | 2,295 | 32,108 | 281,028 | 1,168,197 | `3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea` |
| `hole11` | 9,802 | 29,830 | 1,023 | 30,853 | 250,664 | 1,076,723 | `1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901` |

As a separate closed-form check, an odd \(\ell\)-cycle has
\(2^\ell-2\) labeled proper three-colorings.  Its named common neighbor of
rim edge \(01\) is forced to the third color, and the remaining
\(12-\ell\) vertices are free.  Dividing
\[
 (2^\ell-2)3^{12-\ell}
\]
by the six color-name permutations gives respectively
\(10{,}935,5{,}103,2{,}295,1{,}023\) restricted-growth rows.  This agrees
with the direct enumeration.

The proposed signature-breaker census is also exact.  A comparator on
\(b\) bits has
\[
 \sum_{t=0}^{b-1}2^t=2^b-1
\]
clauses and
\[
 \sum_{t=0}^{b-1}2^t(2t+2)
\]
literals.  Applying this to the stated numbers of adjacent free-vertex
comparators reproduces all four rows of lines 144--149.

This byte reconstruction strengthens the sizing audit, but it does not
substitute for the graph-to-CNF, symmetry, mutation, and proof gates listed
by the strategy.

## 6. Generic anchored counts

For \(n=13\), the independent counts use
\[
\begin{aligned}
s&=\binom{13}{k},\\
m&=\binom{13}{k}(13-k)k,\\
w&=\binom{13}{k-1}(14-k),\\
v&=\binom{13}{2}+w+s+m.
\end{aligned}
\]
The base clauses were summed independently from the ten stated families:
no \(K_{k+1}\), witness existence, witness implications, anchor units,
connected cuts, domination, nonemptiness, two move implications, attack
response, and independent-state forcing.  The coloring bank contributes
\(k^{13-k}\) rows.

The row and column comparator counts were then added independently.  The
result exactly matches every entry in lines 204--208:

| \(k\) | states | moves | variables | base clauses | color clauses | DoubleLex clauses | DoubleLex literals |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 286 | 8,580 | 9,802 | 29,774 | 59,049 | 90,932 | 1,740,356 |
| 4 | 715 | 25,740 | 29,393 | 79,320 | 262,144 | 343,117 | 5,109,628 |
| 5 | 1,287 | 51,480 | 59,280 | 157,116 | 390,625 | 548,978 | 5,916,975 |

These are exact counts for the proposed encodings, not implemented
order-13 formula claims.  The strategy states that boundary correctly.

## 7. Parameter-four and parameter-five lanes

For \(k=4\), C-051 gives
\[
\chi(H[N_H(v)])=\omega(H[N_H(v)])=3
\]
and, for every edge \(uv\),
\[
\chi(H[N_H(u)\cap N_H(v)])
=\omega(H[N_H(u)\cap N_H(v)])=2.
\]
The latter common neighborhood is exactly bipartite and contains an edge.

The accepted large-hole theorem uses only the three-set common-neighbor
property and connectedness and is independent of order.  It requires at
least four vertices outside any induced odd hole.  At order 13, holes are
therefore limited to \(C_5,C_7,C_9\).  Clique number four limits odd
antiholes to lengths five, seven, and nine; the five-antihole is \(C_5\),
and an induced \(\overline{C_9}\) in \(H\) induces \(C_9\) in \(G\), which
would force \(\gamma^\infty(G)\geq5\).  Thus
\[
 C_5,\quad C_7,\quad C_9,\quad\overline{C_7}
\]
is the exact SPGT cover stated in Section 5.

The warning against independently fixing both a template and an anchor is
correct.  For the whole anchored formula, a newly audited DoubleLex action
would make the first row nondecreasing.  Excluding `1111` by no \(K_5\)
leaves exactly the four disjoint rows `0000`, `0001`, `0011`, and `0111`.
The strategy expressly treats the order-13 action as not yet audited.

For \(k=5\), all four C-051 hierarchy bullets are direct instances of
\(k-t\).  Under a newly proved five-column DoubleLex action, the
nondecreasing rows other than the forbidden `11111` are exactly
`00000`, `00001`, `00011`, `00111`, and `01111`.  Again, the document
properly makes the symmetry proof a future gate.

## 8. Pilot JSON and nonpromotion boundary

The pilot JSON is valid strict UTF-8 JSON with no duplicate keys and no
nonfinite numbers.  It binds:

- the exact source at 15,071 bytes and SHA-256
  `fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6`;
- the exact `hole11` formula hash independently reconstructed above;
- the exact 1,571,160-byte solver binary with SHA-256
  `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6`;
- seed zero, 30-second internal limit, exit code 20, wall time, maximum RSS,
  hardware, timestamp, and repository head.

The bound solver binary reports version 3.0.1.  The JSON labels the run
`OBSERVED`, labels the result `UNSAT_UNCERTIFIED`, and states explicitly
that there is no retained proof and no mathematical claim.  The strategy
repeats this limitation at lines 167--169 and 345--349.  There is no
promotion of a proofless UNSAT return.

The missing historical-run metadata listed in the verdict prevents replay
of that invocation and should be repaired in future exploratory records.
It does not invalidate the independently reconstructed formula census or
the bounded strategy.

## Final scope

Accepted here:

- Proposition 1 relative to C-050 and the accepted classical/campaign
  inputs;
- every C-051 complement translation;
- the complete overlapping \(k=3\) four-template cover;
- the parameter-four SPGT cover;
- all formula, coloring-bank, comparator, and generic counts;
- the resource and certificate gates as a sound production policy.

Not accepted or claimed here:

- UNSAT of any order-13 formula;
- coverage of any implemented order-13 generator;
- a certified \((13,3)\), \((13,4)\), or \((13,5)\) exclusion;
- a counterexample or a universal resolution.

The next rigorous action is exactly the strategy's Gate A/B work, not
production solving based only on the pilot.
