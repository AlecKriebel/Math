# Three-gate odd holonomy: a forced witness type and the domination boundary

## Status and exact scope

Date: 2026-07-28 (PDT)

All graph statements use the standard one-guard-moves eternal-domination
model.  Attacks are made only at unoccupied vertices, exactly one adjacent
guard moves, and every retained state dominates.

This lane does **not** prove the universal \(k=3\) case and does not resolve
the gamma--theta conjecture.  It has two rigorous outcomes.

1. **PROVED:** in the shortest cyclic three-gate boundary geometry, an
   outside common complement neighbor of one critical cross-gate pair is
   forced to contain both colors other than the corresponding connector
   type in its family-response list.  In the unit-free no-full branch,
   where every outside list is an exact two-list, the witness therefore has
   the unique third type.  The proof is a finite one-guard attack tree and
   does not infer a graph nonedge from a missing family response.
2. **EXACT COUNTERCONTROL:** the graph
   `KBn]r]vj]lnZ` has
   \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)
   \]
   and its greatest eternal triple-family realizes the entire odd
   three-boundary cycle with exact two-lists.  Its three critical pairs are
   dominating pairs.  Thus closure, exact two-list typing, and the three
   dead gate boundaries do **not** alone force even holonomy; the hypothesis
   \(\gamma\geq3\) is genuinely essential.

Exact SAT probes additionally found the expected even/odd parity split after
imposing \(\gamma\geq3\), for the tested three-, four-, and five-gate
cycles and subdivisions.  Those runs are **OBSERVED discovery evidence**,
not a theorem and not a finite certificate claim.

The remaining gap is precise.  The forced witness is an almost-cap.  If its
nonedge to the corresponding anchor is literal, it supplies a physical gate
chord.  If that anchor incidence is dynamic, accepted literal
physicalization supplies a same-sign physical representative, but accepted
C-095/C-098 show that the two critical clause edges need not transport to
that representative.  No strict descent measure for the resulting new
tight gates has yet been proved.

No literature-priority claim is made.

## 1. The shortest cyclic boundary

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, put \(H=\overline G\), and define

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{1.1}
\]

Membership in \(L(x)\) forces the corresponding \(G\)-edge to the anchor,
because the retained direct-swap state must dominate the omitted anchor.
The converse is never used.

Use three vertices of each exact two-list type:

\[
\begin{array}{c|ccc}
\text{type}&\text{connector endpoints}&\text{cap}\\ \hline
a& a_0,a_1&a_\ast\\
b& b_0,b_1&b_\ast\\
c& c_0,c_1&c_\ast
\end{array}
\tag{1.2}
\]

where

\[
\begin{aligned}
L(a_0)=L(a_1)=L(a_\ast)&=\{b,c\},\\
L(b_0)=L(b_1)=L(b_\ast)&=\{a,c\},\\
L(c_0)=L(c_1)=L(c_\ast)&=\{a,b\}.
\end{aligned}
\tag{1.3}
\]

The three length-one projection connectors are

\[
 a_0a_1,\qquad b_0b_1,\qquad c_0c_1\in E(H).
\tag{1.4}
\]

The three physical cap boundaries are

\[
\begin{array}{c|ccc}
\text{cap}&\text{anchor incidence}&\text{two cap arms}\\ \hline
b_\ast&bb_\ast&b_\ast a_0,\ b_\ast c_1\\
c_\ast&cc_\ast&c_\ast a_1,\ c_\ast b_0\\
a_\ast&aa_\ast&a_\ast b_1,\ a_\ast c_0
\end{array}
\quad\subseteq E(H).
\tag{1.5}
\]

The connector endpoints are physical:

\[
 aa_0,aa_1,\quad
 bb_0,bb_1,\quad
 cc_0,cc_1\in E(H).
\tag{1.6}
\]

Each row of (1.5) makes one boundary state nondominating:

\[
 \{b,a_0,c_1\},\qquad
 \{c,a_1,b_0\},\qquad
 \{a,b_1,c_0\}
 \notin\mathcal F.
\tag{1.7}
\]

The three critical cross-gate pairs are

\[
 P_a=\{b_0,c_1\},\qquad
 P_b=\{c_0,a_1\},\qquad
 P_c=\{a_0,b_1\}.
\tag{1.8}
\]

The subscript is the third type absent from the pair.

## 2. A critical-pair witness has the third type

### Theorem 2.1 (forced witness type) — PROVED

In the setup of Section 1, let \(q\) be an outside vertex, distinct from
all displayed vertices, such that

\[
 qb_0,qc_1\in E(H).
\tag{2.1}
\]

Then

\[
 \boxed{b,c\in L(q).}
\tag{2.2}
\]

Consequently, if every outside response list has size exactly two, then

\[
 L(q)=\{b,c\};
\tag{2.3}
\]

that is, \(q\) has type \(a\).  The cyclic versions hold for \(P_b\) and
\(P_c\).

#### Proof that \(b\in L(q)\)

Assume for a contradiction that

\[
 \{a,c,q\}=S-b+q\notin\mathcal F.
\tag{2.4}
\]

Because \(b\in L(c_0)\), the direct state

\[
 D=\{a,c,c_0\}\in\mathcal F.
\tag{2.5}
\]

Attack the unoccupied vertex \(q\).

- Moving \(c_0\) gives the absent state (2.4).
- A successor \(\{c,c_0,q\}\) does not dominate \(c_1\), because
  \[
  cc_1,\ c_0c_1,\ qc_1\in E(H).
  \]

Closure therefore forces

\[
 A=\{a,c_0,q\}\in\mathcal F.
\tag{2.6}
\]

Attack \(b_1\) from \(A\).  We show that all three successor shapes are
absent.

First,

\[
 \{a,c_0,b_1\}\notin\mathcal F,
\tag{2.7}
\]

because it does not dominate \(a_\ast\), by the three complement edges in
the last row of (1.5).

Second,

\[
 \{a,b_1,q\}\notin\mathcal F.
\tag{2.8}
\]

Indeed, attack the unoccupied anchor \(c\).  The guard at \(a\) cannot
move because \(S\) is independent.  Moving \(b_1\), if legal, gives
\(\{a,c,q\}\), absent by (2.4).  Moving \(q\), if legal, gives
\(\{a,c,b_1\}=S-b+b_1\), absent because \(b\notin L(b_1)\).
Thus no response exists.

Third,

\[
 \{c_0,b_1,q\}\notin\mathcal F.
\tag{2.9}
\]

Suppose otherwise and attack \(b_0\).  The guards at \(b_1\) and \(q\)
cannot move, by \(b_0b_1,qb_0\in E(H)\).  The only possible successor is
\(\{b_0,b_1,q\}\).  This successor is itself absent: attack \(c\).
Every possible response has one of the forms

\[
 \{c,b_1,q\},\qquad
 \{c,b_0,q\},\qquad
 \{c,b_0,b_1\}.
\tag{2.10}
\]

Each state in (2.10) is dead under an attack at \(a\).  The guard at \(c\)
cannot move because \(S\) is independent, and every other possible
successor is either the assumed-absent state \(\{a,c,q\}\) or one of

\[
 \{a,c,b_0\}=S-b+b_0,\qquad
 \{a,c,b_1\}=S-b+b_1,
\]

both absent because the type-\(b\) lists omit \(b\).  This proves (2.9).

Equations (2.7)--(2.9) exhaust the possible one-guard responses to the
attack at \(b_1\) from the retained state \(A\), a contradiction.  Hence
\(b\in L(q)\).

#### Proof that \(c\in L(q)\)

This is the reflected attack tree; it is included to avoid hiding a
symmetry mismatch.  Assume

\[
 \{a,b,q\}=S-c+q\notin\mathcal F.
\tag{2.11}
\]

Because \(c\in L(b_1)\),

\[
 D'=\{a,b,b_1\}\in\mathcal F.
\]

Attack \(q\).  The state \(\{b,b_1,q\}\) misses \(b_0\), by

\[
 bb_0,\ b_1b_0,\ qb_0\in E(H),
\]

while moving \(b_1\) gives the absent state (2.11).  Closure forces

\[
 A'=\{a,b_1,q\}\in\mathcal F.
\tag{2.12}
\]

Attack \(c_0\) from \(A'\).

- The state \(\{a,b_1,c_0\}\) misses \(a_\ast\).
- The state \(\{a,c_0,q\}\) is dead under an attack at \(b\): the anchor
  \(a\) cannot move, and the other successors are (2.11) and the absent
  direct swap \(S-c+c_0\).
- The state \(\{b_1,c_0,q\}\) is dead as follows.  Attack \(c_1\).
  The guards at \(c_0,q\) cannot move, so the only possible successor is
  \(\{c_0,c_1,q\}\).  Attack \(b\) there.  Its three successor shapes are
  dead under an attack at \(a\), using (2.11) and the absent type-\(c\)
  direct swaps \(S-c+c_0,S-c+c_1\).

Again all response shapes are absent, contradicting closure.  Therefore
\(c\in L(q)\), proving (2.2).

Every attack above is made at an unoccupied vertex.  Every possible
successor changes exactly one guard.  A missing move edge only removes a
candidate response.  No list omission is interpreted as a graph nonedge.
\(\square\)

### Lemma 2.2 (displayed-witness collisions) — PROVED

Assume the setup of Section 1 and \(\gamma(G)\geq3\).  A common
complement neighbor of \(P_a=\{b_0,c_1\}\) supplied by the
no-dominating-pair condition has one of the following two forms:

1. it is outside the displayed configuration, so Theorem 2.1 applies; or
2. it has type \(a\) and is already physical to \(a\), hence is a literal
   cap for the boundary \(\{a,b_0,c_1\}\).

In particular, no displayed vertex of type \(b\) or \(c\) is a common
complement neighbor of \(P_a\).  The cyclic versions hold for \(P_b\) and
\(P_c\).

#### Proof

No anchor is a common complement neighbor.  Indeed, membership in the
displayed exact lists gives graph edges from \(b_0\) to \(a,c\) and from
\(c_1\) to \(a,b\).  The endpoints themselves are excluded because the
graph has no loops.

Every displayed type-\(a\) vertex is complement-adjacent to \(a\), by
(1.5)--(1.6).  If such a vertex also sees \(b_0,c_1\) in \(H\), it is
already the literal cap in alternative 2.

For \(q=b_\ast\) or \(q=c_\ast\), the two attack trees in Theorem 2.1
remain valid verbatim: neither label occurs in any of their fixed auxiliary
roles.  They would force \(b,c\in L(q)\), contradicting the displayed
type of \(q\).

It remains to exclude the two collisions \(q=b_1\) and \(q=c_0\).  We
give the first attack tree; the second is its reflection interchanging
\(b\) and \(c\).  Suppose \(b_1c_1\in E(H)\), so that \(b_1\) is a common
complement neighbor of \(b_0,c_1\).  The direct state

\[
 D=\{a,c,c_0\}\in\mathcal F
\]

is retained.  Attack \(b_\ast\).

- Moving \(c_0\) gives the absent direct swap
  \(\{a,c,b_\ast\}=S-b+b_\ast\).
- A successor \(\{c,c_0,b_\ast\}\) does not dominate \(c_1\), by
  \(cc_1,c_0c_1,b_\ast c_1\in E(H)\).

Closure therefore forces

\[
 A=\{a,c_0,b_\ast\}\in\mathcal F.
\]

Attack \(b_1\) from \(A\).  All three successor shapes are absent:

- \(\{a,c_0,b_1\}\) does not dominate \(a_\ast\);
- \(\{a,b_1,b_\ast\}\) is dead under an attack at \(c\), because \(a\)
  cannot move and the other successors are the absent direct swaps
  \(S-b+b_1\) and \(S-b+b_\ast\); and
- \(\{c_0,b_1,b_\ast\}\) does not dominate \(c_1\), using
  \(c_0c_1,b_1c_1,b_\ast c_1\in E(H)\).

This contradicts closure.  Thus \(b_1\) cannot be the witness, and the
reflected tree excludes \(c_0\).  These cases exhaust the displayed
vertices. \(\square\)

### Corollary 2.3 (almost-cap transition) — PROVED

In the unit-free no-full two-list branch, an outside common complement
neighbor of \(P_a\) is a type-\(a\) port joined in \(H\) to the type-\(b\)
and type-\(c\) endpoints.  Cyclically, common complement neighbors of
\(P_b,P_c\) have types \(b,c\), respectively.

If additionally \(aq\in E(H)\), then \(q\) is a literal physical cap for
the boundary \(\{a,b_0,c_1\}\).  Theorem 2.1 does **not** prove this anchor
incidence.  If \(aq\in E(G)\), the response omission \(a\notin L(q)\) is
dynamic.

This is the exact point at which a shortening proof must use more than the
boundary attack tree.

## 3. Why the dynamic almost-cap is still open

Accepted literal physicalization applies to the dynamic case.  It supplies
a same-sign type-\(a\) representative \(r\) with

\[
 ar\in E(H)
\]

and an even path from \(q\) to \(r\) inside the \(a\)-omitting projection.
At the Boolean level, \(q\) and \(r\) name the same chirality event.

One cannot conclude

\[
 rb_0,rc_1\in E(H).
\tag{3.1}
\]

Accepted C-095 gives an equality control where a physical representative
loses a specified original edge.  Accepted C-098 gives an equality control
where one representative loses two specified edges and proves that every
failed joint incidence is repaired by another virtual-rainbow cap.  Thus a
descent based on (3.1) would be unsound.

Lemma 2.2 ensures that a common neighbor supplied by \(\gamma(G)\geq3\)
does not disappear into an unhandled displayed-vertex collision.  The
remaining proposed step is:

> Starting with a minimum odd tight-gate cycle, apply Theorem 2.1 at a
> critical pair.  Prove that either the forced third-type witness yields a
> strictly shorter odd cycle, or the C-098 repair gates decrease a separate
> well-founded measure.

No such measure is proved here.  In particular, “number of physicalization
steps,” component distance, and number of failed incidences have not yet
been shown to decrease under the repair operation.

## 4. Exact gamma-dropped countercontrol

Use the numerical identification

\[
\begin{aligned}
(a,b,c)&=(0,1,2),\\
(a_0,b_0,c_0,c_1,a_1,b_1,b_\ast,c_\ast,a_\ast)
&=(3,4,5,6,7,8,9,10,11).
\end{aligned}
\tag{4.1}
\]

Let \(H\) have exactly the edges

```text
01 02 03 07 0-11
12 14 18 19
25 26 2-10
37 39
48 4-10
56 5-11
69 7-10 8-11
```

where a hyphen only disambiguates a two-digit label.  The corresponding
graph \(G=\overline H\) has graph6 record

```text
KBn]r]vj]lnZ
```

and 45 edges.

The standalone verifier reconstructs

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
 }
\tag{4.2}
\]

The greatest eternal triple-family has 181 states and satisfies all

\[
 181(12-3)=1629
\]

unoccupied attack obligations.  Its direct response lists are exactly
those in (1.3), and all three gate boundaries (1.7) are nondominating.
The three length-one connectors give odd total parity.

The critical pairs

\[
 \{b_0,c_1\}=\{4,6\},\quad
 \{c_0,a_1\}=\{5,7\},\quad
 \{a_0,b_1\}=\{3,8\}
\]

all dominate \(G\).  Therefore none has the common \(H\)-neighbor that
\(\gamma(G)\geq3\) would require.  This makes the control sharp for the
role of the domination lower bound.

The control is not a gamma--theta counterexample:

\[
 \gamma(G)=2<3=\gamma^\infty(G)=\theta(G).
\]

It is also a boundary control, not a realization of three complete
C-098 virtual-rainbow gates: the original cross clauses and their
same-sign physicalization paths are not asserted.  Its purpose is to refute
the stronger claim that dead boundaries and exact two-list connector
closure alone force even holonomy.

## 5. Discovery observations, not claims

`probe_boundary_cycle.py` encodes:

- an independent retained anchor triple;
- literal one-guard closure for an arbitrary selected triple-family;
- exact two-list gate terminals and caps;
- the physical dead-boundary incidences;
- vertex-disjoint omitted-color connector paths;
- optional exact two-list typing of every outside vertex;
- optional \(\gamma\geq3\), encoded as a common \(H\)-neighbor for every
  pair; and
- optionally, one original clause plus an even same-sign physicalization
  path for each full tight gate.

The tested boundary formulas had the following discovery behavior:

\[
\begin{array}{c|c|c}
\text{total connector parity}&\gamma\geq3&\text{observed}\\ \hline
\text{even}&\text{yes}&\mathrm{SAT}\\
\text{odd}&\text{no}&\mathrm{SAT}\\
\text{odd}&\text{yes}&\mathrm{UNSAT}.
\end{array}
\]

The odd/UNSAT row was observed for several type words with three, four, and
five gates and for several subdivisions.  The same parity split persisted
when complete minimal physical gate gadgets were added.  These runs guide
the proposed descent in Section 3; no proof-log package or coverage theorem
is claimed, and they must not be cited as an arbitrary-cycle exclusion.

## 6. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/three_gate_odd_holonomy/verify.py \
  --check math/working/three_gate_odd_holonomy/result.json
```

The verifier imports no campaign evaluator or search core.  It:

- reconstructs the graph independently from the explicit \(H\)-edge table
  and cross-checks the graph6 record in both directions;
- computes exact \(\gamma,i,\alpha,\theta\);
- computes the greatest one-, two-, and three-guard families by
  simultaneous fixed-point deletion;
- replays all 1,629 retained unoccupied-attack obligations;
- reconstructs every response list at \(S\);
- checks the three dead boundaries, three odd connector edges, and three
  critical dominating pairs; and
- checks the frozen hashes of the greatest family and complete response
  table.

The deterministic result is `result.json`.
