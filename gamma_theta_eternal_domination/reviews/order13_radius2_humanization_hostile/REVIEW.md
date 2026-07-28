# Hostile review: anchored radius-two order-13 residual exclusion

Date: 2026-07-28 PDT

## Verdict

**PASS.**

The exact finite statement certified here is:

> In the normalized order-13, parameter-three, no-full residual branch used
> by C097, the formula is already inconsistent when one-guard closure is
> imposed only at selected triples \(D\) satisfying
> \(D\cap S\ne\varnothing\), where \(S=\{0,1,2\}\) is the distinguished
> independent triple.

This is an unconditional audit verdict for the retained formula and proof.
Using it as a graph-level order-13 exclusion has the same previously
accepted structural prerequisites as C097: C090 for the full-response
branch, C093 for the two-type/pure-pair reduction, and C096 for the
four-neutral obstruction.

This result does not extend the order frontier beyond C097.  It is a strict
finite strengthening of the mechanism inside C097: closure after all three
original anchors have left is unnecessary.  It does not prove the
arbitrary-order \(k=3\) case or the universal gamma--theta conjecture.

## Reviewed artifacts

| artifact | SHA-256 |
|---|---|
| radius-two CNF | `8bd4ae50e2ac06deb6560c4ff482eb19d7b64a4769029284da4660ccbefd1b55` |
| addition-only proof | `f5fcbe26885ab229636d511d2b1ee47203478002fb22ce34407f1182d1c1eeea` |
| two-slice model \(R=\{0,1\}\) | `6cb2f5951c4c1526d0162d4df156e9cf023196567070f0827034ce485a5cffd9` |
| two-slice model \(R=\{0,2\}\) | `d9472ab2debd3d52367e155ce5fd62540646c111f232c212f469b01e280efb05` |
| two-slice model \(R=\{1,2\}\) | `ac1e61b65661ef8a60094ebf93eae629993805113ceb227e60d9157b89792c57` |
| independent checker | `e5d802bb17fad1b5736ed582d2bac29de687ebea68e77ea820b386a0cf9fdbe4` |
| checker result | `1ba4a9f64c3f1fc4b8e55b1e7f0a9229c7c1b9334c5b5b83cc2d51e62d105782` |

The source note was normalized during review to remove a stray formatting
character after one Graph6 string.  Its original reviewed hash was
`df0a9e967ed56643ed5b80e9d0ed69ffabcc793fcc61d0a5221d5eb4fbf013db`.
The post-audit status update described below supersedes that source-note
hash.  No CNF, proof, model, or mathematical claim changed.

## Post-audit status-language addendum

After the initial unconditional `PASS`, the source note's status language
was promoted from “candidate” to “certified” and the pending-audit paragraph
was replaced by the now-true statement that an independent reconstruction
and hostile audit had accepted the result.  The current complete source note
is frozen at:

```text
34c9ce6c2756e7ee5b791cf2ff7dc7edb9272307ced43e729b4d68edcbea8a28
```

The note was still untracked, so no repository diff against the earlier
bytes was available.  This addendum therefore does not rely merely on the
reported edit count.  The checker reads and pins the complete current note
and verifies directly that:

- each of the three new certified-status passages occurs exactly once;
- all three pre-audit pending phrases are absent;
- the decisive CNF and proof hashes are unchanged;
- the 9,802-variable, 76,214-clause, 168,880-line, and 9,367,094-byte
  censuses are unchanged;
- all three control Graph6 strings are unchanged; and
- the explicit no-universal-proof and no-counterexample caveats remain.

The formula, proof, and all three model hashes were independently rechecked,
and the full strict RUP replay again passed.  The checker result was made
deterministic by excluding only the proof checker's wall-time line.  Two
consecutive complete runs produced the identical result hash
`1ba4a9f64c3f1fc4b8e55b1e7f0a9229c7c1b9334c5b5b83cc2d51e62d105782`.

**Post-audit verdict: PASS.**  The edits correctly update certification
status and do not alter the theorem, formula, proof, controls, scope, or
limitations.

## 1. Independent formula reconstruction

`checker.py` imports no campaign generator, transition implementation,
model verifier, or earlier hostile checker.  It allocates all 9,802
variables and emits the clauses directly from the definitions, retaining
the production variable and clause order only so exact bytes can be
compared.

As a baseline, its full-closure output is byte-for-byte identical to the
accepted C097 residual formula:

```text
variables: 9,802
clauses: 84,614
bytes: 4,784,714
SHA-256:
76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1
```

The clean-room radius-two output is then byte-for-byte identical to the
retained candidate:

```text
variables: 9,802
clauses: 76,214
bytes: 4,667,702
SHA-256:
8bd4ae50e2ac06deb6560c4ff482eb19d7b64a4769029284da4660ccbefd1b55
```

The radius-two formula is a strict clause subset of C097.  The exact
difference is 8,400 clauses:

\[
  \binom{10}{3}\cdot 10\cdot 7
  =120\cdot 10\cdot 7
  =8{,}400.
\]

The 120 affected states are exactly the triples disjoint from \(S\).  For
each such state and each of its ten unoccupied attacks, the omitted seven
clauses are the three move-edge implications, three retained-successor
implications, and one response disjunction.  Every other clause is
unchanged.

Equivalently, closure remains at all

\[
  \binom{13}{3}-\binom{10}{3}=166
\]

triples meeting \(S\), for 1,660 state-attack obligations.  The retained
closure block contains 4,980 move-edge implications, 4,980 successor
implications, and 1,660 response clauses.  The 3,600 move variables attached
only to omitted obligations remain allocated but unused; this is harmless
and explains why the variable census does not change.

The radius-two DIMACS has no duplicate clauses, tautologies, malformed
literals, or out-of-range variables.  A complete 128-row truth table,
existentially eliminating the three move bits, verifies that each retained
gadget means exactly

\[
  \neg f_D\ \lor\
  \bigvee_{u\in D}
  \bigl(ur\in E(G)\land f_{D-u+r}\bigr).
\]

Thus attacks are only at unoccupied vertices, exactly one guard moves along
one edge, and the successor is selected.  This is the one-guard model.

## 2. Strict proof replay

The decisive proof has:

```text
168,880 lines
9,367,094 bytes
0 deletion lines
terminal empty clause: yes
SHA-256:
f5fcbe26885ab229636d511d2b1ee47203478002fb22ce34407f1182d1c1eeea
```

Pinned `drat-trim`
(`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`)
replayed it with ASCII parsing, forward checking, warnings fatal, and RAT
additions forbidden:

```text
-I -f -W -U
c 0 RAT lemmas in core
s VERIFIED
```

There were no warnings.  The proof therefore certifies UNSAT by
addition-only RUP.

## 3. Independent audit of all two-slice controls

For each two-element \(R\subset S\), the checker independently reconstructed
the corresponding 73,064-clause formula.  Each has 121 closure states and
1,210 encoded state-attack obligations.  The reconstructed formula hashes
are:

| retained \(R\) | formula SHA-256 |
|---|---|
| \(\{0,1\}\) | `14bfba6998ef348a1884a88a2b092325d08beb81f5b64b600bba8e44c10d1e72` |
| \(\{0,2\}\) | `90604d16600b51f0ae9a178300b0e17b44eaea6d0f428d1ee2549ad5ea624c87` |
| \(\{1,2\}\) | `bb2720da0ab48e2279c30ce3661a711009d9ee114f01ad8bcd8a49d7e02bf328` |

Every retained model is a total assignment of all 9,802 variables and
satisfies every clause of its independently rebuilt formula.  Ignoring all
SAT move variables, the checker then reconstructed \(G\), its selected
triple family, and replayed the response rule directly from the definition.

| \(R\) | Graph6 | family | required selected-state attacks | full-closure failures | omitted single-anchor failures |
|---|---|---:|---:|---:|---:|
| \(\{0,1\}\) | `LBZ]ditl\jtoq}` | 142 | 640 | 47 | 13 |
| \(\{0,2\}\) | ``LBZMbqjntjJp`}`` | 160 | 600 | 22 | 5 |
| \(\{1,2\}\) | `LBZ]b\|j\rpufme` | 153 | 570 | 30 | 6 |

All required partial-closure attacks have a legal one-edge, one-guard
response into the selected family.  Every full-closure failure lies outside
the retained slices, and every control has at least one failure in the
omitted single-anchor slice.

For each graph, independent exhaustive routines give

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

Specifically, the greatest eternal triple kernel is empty.  The first
nonempty kernel occurs at size four, with respectively 581, 632, and 607
configurations.  Independent complement-coloring searches reject three
colors and return explicit four-colorings.  The Graph6 strings were encoded
independently from the reconstructed \(G\)-adjacency matrices.

The exact no-full lists, named pure signatures, named complement mate edges,
residual signature sorting, and label-10 nonneutral cut also hold in every
control.

Therefore the proposed two-slice strengthening is genuinely refuted:
closure through any two original-anchor slices does not force the residual
contradiction.  The three-way depth-two interaction is necessary for these
finite formulas.  These controls are not gamma--theta counterexamples,
because each has \(\gamma=3<4=\gamma^\infty\).

## 4. Scope relative to C097

This proof can replace the full-closure residual proof inside the accepted
C097 composition, because every actual eternal family satisfies all
radius-two obligations.  It does not change the normalization, structural
coverage, or graph universe of C097.  Its value is mechanistic:

- the first replacement layer alone is insufficient;
- any two of the three second-layer anchor slices are insufficient;
- all three second-layer slices together are inconsistent; and
- play after all three members of the original state have moved is not used.

That is a rigorous finite localization result and a useful universal-proof
target, but it is not a new global frontier or a resolution of the
conjecture.
