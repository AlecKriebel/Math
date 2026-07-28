# Hostile review: free singleton component polarization

## Verdict

**PASS, with the candidate's stated narrow scope.**

The universal statements in Sections 1--4 of the frozen candidate note are
valid under their displayed hypotheses and accepted dependencies.  The
seven-vertex control `FCZbg` was reconstructed independently and matches
every claimed exact value.  No step confuses a family-relative response
list with a static legal-move list.

This review accepts only the following new conclusions:

1. A singleton family-response marker in a free component of a frozen
   bipartite projection polarizes the component.
2. Every complement edge in that component lifts to a retained frozen
   family state.
3. All singleton markers on one such component are parity-coherent.
4. Consequently, given the already accepted C-119/C-120 clause inventory,
   the two-unit terminal containing zero binary clauses is impossible.

It does **not** accept an exclusion of a positive-length unit chain,
lollipop, residual bicycle, the whole singleton branch, all of \(k=3\),
or the universal gamma--theta conjecture.

## Frozen candidate audited

Candidate manifest:

```text
math/working/free_unit_chain_attack/MANIFEST.json
SHA-256 2d87b2b440c33574da4546f298864d33cc19ff8e6ebdc1d7541cff980bc8350e
```

Every hash named by that manifest was recomputed and matched:

```text
NOTE.md          3dbccd2aa69cfc45b1c5e518e05165594e27f06b1741fcd1ec7a2b8b0d02fb39
RESEARCH_LOG.md  c281a64c009c600f3adfba73c723a0b67a0ab3d27f357a5d283dad61f77c29db
controls.json    354cbc0bc3e37c6bc02bc71354fc1024d1924af03e786f8bbcad9090a947b21b
verify.py        579dd42cdf8e591717e8c5a7cb96b5e239bec1ae6a623c3d8c77b0d83bdaf2ef
```

The candidate verifier was also replayed.  Its exact stdout hash was

```text
7aed6bb4463ee4b67d47c5cd4d679c518a4bae6c4ce6be27ac309e0fe3c2ed18
```

as frozen in the candidate manifest.  This replay is corroborative only;
the clean-room audit below does not import that verifier.

## Independent proof audit

Throughout, \(J\) is the projected graph, \(B=\overline J\) is bipartite,
and retained states belong to the projected eternal pair-family.

### 1. Pair transversal lemma

Suppose a retained pair \(x,y\) lies on one side of a single component of
\(B\).  A shortest \(B\)-path between them has positive even length
\(2r\).

- If \(r=1\), its middle vertex is adjacent in \(B\), hence nonadjacent in
  \(J\), to both guards.  The retained pair is nondominating.
- If \(r\geq2\), the vertex \(v_2\) is unoccupied.  It is on the same
  \(B\)-side as both guards, so both guards are adjacent to it in \(J\).
  The successor \(\{x,v_2\}\) does not dominate \(v_1\).  If the other
  successor \(\{v_2,y\}\) were retained, the suffix of the path would
  contradict the minimal choice of the retained same-side pair.

Thus an unoccupied attack has no retained one-edge response.  This proves
the lemma.  The argument does not assume that a missing retained response
is a graph nonedge.

### 2. Component separation

For the candidate notation \(S=\{u,d,e\}\), the anchor edge \(de\) lies
in one component of \(B_u\).  A free component \(K\) is a different
component.  Therefore no vertex of \(K\) has a complement edge to \(d\)
or \(e\); every such vertex is adjacent in \(G\) to both anchors.  This is
the only cross-component adjacency fact used later, and it is valid.

### 3. Even-side propagation

The singleton condition \(L(s)=\{d\}\) supplies the retained projected
pair \(\{e,s\}\).  Along
\(s=v_0,v_1,\ldots,v_{2r}=x\), assume
\(\{e,v_{2j}\}\) is retained and attack the distinct, unoccupied vertex
\(v_{2j+2}\).

- The anchor \(e\) is adjacent to the target by component separation.
- The vertices \(v_{2j}\) and \(v_{2j+2}\) lie on the same side of a
  bipartite complement, so they are adjacent in \(G\).
- Moving \(e\) would leave a retained same-side pair in \(K\), forbidden
  by the pair transversal lemma.

One-guard closure therefore forces
\(\{e,v_{2j+2}\}\).  The induction is sound for arbitrary path length.

### 4. Odd-side propagation

From \(\{e,s\}\), attack \(v_1\).  The guard at \(s\) cannot move across
the complement edge \(sv_1\); component separation makes \(e\) adjacent
to \(v_1\).  Hence \(\{s,v_1\}\) is retained.

Now attack the unoccupied anchor \(d\).  Both component guards are
adjacent to it.  Moving \(v_1\) would leave \(\{d,s\}\), whose lift is
\(S-e+s\).  It is absent from the family because \(e\notin L(s)\).
Therefore closure forces \(\{d,v_1\}\), after which the even-side
argument propagates through every odd-indexed vertex.

The use of the absent pair here is legitimate: it excludes one
**retained-family successor** and does not assert a graph nonedge or a
nondominating state.

### 5. Translation back to lists

The retained pair \(\{e,x\}\) lifts to
\(\{u,e,x\}=S-d+x\), exactly the statement \(d\in L(x)\).
Similarly, \(\{d,x\}\) lifts to \(S-e+x\), exactly
\(e\in L(x)\).  There is no reversal error in the anchor labels.

### 6. Edge saturation

If \(xy\) is a complement edge of \(K\), use the polarized retained pair
containing \(x\) and the appropriate anchor.  Attack the unoccupied
vertex \(y\).  The guard at \(x\) cannot traverse \(xy\), while the anchor
can reach \(y\) by component separation.  The unique response is
\(\{x,y\}\), which lifts to \(\{u,x,y\}\).  This proves saturation of
every complement edge, not merely the edges of a chosen path.

### 7. Coherence of singleton pins

Every vertex of a free component lies outside \(S\), so its response list
is defined and omits the frozen anchor.  Polarization places \(d\) in
every same-side list and \(e\) in every opposite-side list.  If such a
list is a singleton, it must equal the corresponding one-element set.
Thus two singleton units on the same component variable demand the same
orientation after bipartition parity is included.

### 8. Exact logical consequence

The accepted C-120 result leaves only singleton units on free component
variables and genuine binary cross-type clauses whose endpoints are
distinct free variables.  A minimal two-unit contradiction with zero
binary clauses would consist of complementary unit literals on one
variable.  Section 7 rules this out.  A remaining two-unit chain must
therefore contain a binary clause.  A one-unit path from a literal to its
complement also has positive clause length.  Under C-120, every such
clause is a genuine cross-type clause.

This proves exactly the candidate's zero-binary-clause reduction.  It
does not shorten or eliminate a chain containing even one clause.

## One-guard and family/static audit

Every proof attack is at a vertex distinct from the two occupied
projected guards.  Every successor changes exactly one guard, and every
move asserted to be possible uses a graph edge.  Domination is used only
for retained states or to reject the length-two base successor.

The clean-room control exposes the most dangerous possible hidden
assumption.  At the reference state \(S=\{3,4,5\}\), it finds

```text
family-relative lists:  L(0)={3},   L(6)={5}
static legal lists:     Ls(0)={3,5}, Ls(6)={3,5}.
```

Thus each missing second response is dynamically absent even though it
is an adjacent, dominating one-step move.  The proof remains valid in
this strict setting because it uses absence only as absence from the
specified eternal family.  This directly rules out the suspected
family-relative/static-list slippage.

## Clean-room reconstruction of `FCZbg`

`independent_check.py` reads no candidate file and imports no campaign
module.  It starts from the explicit ten-edge graph

```text
03 05 14 15 16 24 25 26 36 56
```

and independently verifies that its short graph6 encoding is `FCZbg`.
Set-based exhaustive searches return

```text
(gamma, i, alpha, gamma-infinity, theta) = (3,3,3,3,3).
```

In detail:

- complete subset searches prove \(\gamma=i=\alpha=3\);
- a complete canonical clique-partition search proves \(\theta=3\) and
  finds the partition `03 | 14 | 256`;
- the dominating-triple fixed point has stage sizes `22, 19, 18`;
- its final eighteen states answer all
  \(18(7-3)=72\) unoccupied attacks;
- since \(\gamma=3\), this family proves
  \(\gamma^\infty=3\);
- all three frozen projected pair-families independently satisfy
  domination and every one-guard obligation;
- the frozen-4 complement components are exactly
  `06` and `35`;
- the free component `06` has the two opposite, parity-compatible
  singleton incidences claimed; and
- its sole complement edge lifts to retained state `046`.

The frozen result is `result.json`, and an exact replay is:

```text
python3 -I -B -W error \
  reviews/free_unit_chain_hostile/independent_check.py
```

Its stdout must equal `result.json` byte for byte after the final newline.

## Status ledger

### PROVED

- Pair transversal lemma under bipartite complement.
- Free singleton component polarization.
- Complement-edge family saturation in a pinned free component.
- Parity coherence of all singleton pins in that component.
- Elimination of the zero-binary-clause two-unit terminal, conditional
  only on the already accepted C-119/C-120 exact clause inventory.

### EXACT CONTROL

- `FCZbg`, with all five parameters equal to three, an eighteen-state
  greatest eternal family, seventy-two checked unoccupied-attack
  obligations, two free singleton incidences, and retained lift `046`.

### OBSERVED ONLY

- Same-marker two-arm solver outcomes through the bounded path lengths
  reported by the candidate.
- Mixed-\(P_4\) synthesis outcomes at the reported tested orders.
- The timed-out order-20 CEGAR leaf.

Those solver observations were not needed for, and were not promoted by,
this review.

### OPEN

- Any one-unit lollipop or two-unit chain using a genuine binary clause.
- Arbitrary separated or subdivided connectors.
- Residual unit-free bicycles.
- The full-response-list branch.
- The complete \(k=3\) theorem.
- The universal gamma--theta conjecture.

No counterexample-order bound follows from this candidate.
