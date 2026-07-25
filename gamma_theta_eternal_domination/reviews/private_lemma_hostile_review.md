# Independent hostile review of the maximum-independent-state lemma

**Review date:** 2026-07-25 13:39 PDT  
**Files reviewed:**

- `math/lemmas/maximum_independent_states.md`
  (`sha256:f819ca28edc2e1809707876d2531347629bdd2137903d2763c6e2bfdb7c1568d`)
- `src/search/private_obstruction.py`
  (`sha256:dba30b4a28989893146148d4aeccb188acd24e1e32f7c253cd23b1713c222adf`)
- `tests/test_private_obstruction.py`
  (`sha256:12ab9fb2bed807aca23ad2cbc75971e4f940289fec1c4f87d98e09bbf6ef0ca8`)

## Verdict

**ACCEPT the mathematics.** Lemmas 1 and 3, Theorem 4, and Corollaries 2 and
5 are correct in the stated one-guard-moves model. In particular, the
apparently strong quantifier in Corollary 2 is valid: every independent
\(k\)-set belongs to every eternal family of \(k\)-sets, not merely to the
greatest family or to some minimum strategy.

**ACCEPT `find_private_obstruction` on valid `BitGraph` inputs.** It implements
exactly the local predicate in Corollary 5. Exhaustive comparison found no
false positive or false negative relative to that predicate.

**ACCEPT the mathematical soundness of certificates produced by the
finder, but harden `verify_private_obstruction` before treating it as a
strict hostile-input certificate checker.** Two input-validation defects are
described below. Neither defect produces a false mathematical lower bound
from a finder-generated certificate, but one makes the checker raise on
malformed input and the other lets it ignore a superfluous duplicate record.

No critical or high-severity mathematical defect was found.

## 1. Exact model and quantifier audit

I audited against

\[
 \forall D\in\mathcal F\ \forall r\in V(G)\setminus D\
 \exists u\in D\cap N(r):
 (D-\{u\})\cup\{r\}\in\mathcal F,
\]

where \(\mathcal F\) is nonempty, every member is a dominating \(k\)-set,
the attacked vertex is unoccupied, and exactly one guard traverses one edge.
No occupied-attack, all-guards-move, or merely-reachable-state convention was
used.

### Lemma 1: every independent \(k\)-set is in every \(k\)-family

The proof has the correct order of quantifiers. Fix an arbitrary eternal
family \(\mathcal F\), an arbitrary starting state \(D\in\mathcal F\), and an
arbitrary independent \(k\)-set \(S\). At a stage with \(s\in S-D\), the
attack at \(s\) is unoccupied. Closure supplies at least one responding guard.
No responding guard can lie in \(D\cap S\), because such a guard would be a
distinct vertex of the independent set \(S\) adjacent to \(s\). Hence every
response that closure can supply removes a guard outside \(S\) and inserts
one in \(S\). The intersection size rises by exactly one and the successor
remains in the same family. After exactly \(k-|D\cap S|\) iterations, the
state is \(S\).

This argument does not use minimality of \(\mathcal F\), the greatest-fixed-
point family, maximum independent sets, or a predetermined defender choice.
It therefore proves the literal “every family” assertion in Corollary 2.
The equality \(\alpha(G)=k\) is needed in Corollary 2 only to identify every
maximum independent set as an independent set of the same size as the
family.

### Lemma 3: closed private neighborhoods and the swap iff

The definition

\[
 P_D(u)=\{x:N[x]\cap D=\{u\}\}
\]

is the required **closed** private neighborhood. For a dominating \(D\),
every \(x\notin P_D(u)\) has a dominator in \(D-\{u\}\), while every
\(x\in P_D(u)\) loses its sole old dominator. Thus the successor dominates
if and only if the new guard at \(r\) dominates all of \(P_D(u)\), namely
if and only if \(P_D(u)\subseteq N[r]\).

The separate hypothesis \(u\in D\cap N(r)\) is essential for a general
dominating set \(D\): if guards in \(D\) are adjacent, \(u\) need not itself
belong to \(P_D(u)\), so the containment alone need not certify that the move
\(u\to r\) is along an edge. The document retains this hypothesis in Lemma
3. In Theorem 4, where \(D=S\) is independent, one has
\(u\in P_S(u)\); consequently the displayed containment forces
\(u\in N[r]\), and since \(r\notin S\), it forces \(ur\in E(G)\). The
omission of an explicit \(u\in N(r)\) from Theorem 4 is therefore sound.

Using an open private neighborhood here would be wrong. The prose,
formulae, finder, and checker all use closed neighborhoods.

### Theorem 4 and occupied attacks

Corollary 2 forces each maximum independent set \(S\) into the chosen
eternal \(k\)-family. The theorem then considers only \(r\in V-S\), so its
attack is unoccupied. The family response moves one adjacent guard and its
successor is a member of the family, hence dominates. Lemma 3 applies
directly. This is exactly the secure-dominating-set condition.

### Corollary 5 and the lower bound

For a maximum independent set \(S\), maximality ensures that every
\(r\notin S\) has at least one neighbor in \(S\). Thus the quantified set of
possible defenders in Corollary 5 is nonempty (although the stated
implication would remain sound if it were empty). A witness
\(x_u\in P_S(u)-N[r]\) is undominated by
\((S-\{u\})\cup\{r\}\), so every legal one-guard response fails.

The contrapositive of Theorem 4 gives
\(\gamma^\infty(G)\ne\alpha(G)\). The displayed numerical conclusion then
also uses the already proved general bound
\(\alpha(G)\leq\gamma^\infty(G)\) and integrality. This dependency is valid
but is not stated in the corollary's text; see finding L1.

## 2. Severity-ranked findings and exact corrections

### Critical and high severity

None.

### Medium implementation finding I1: an invalid attack index raises

`verify_private_obstruction` uses `obstruction.attack` in a shift at line 99
and as an adjacency-tuple index at lines 105 and 116 without first checking
that it is a vertex. On the valid \(C_5\) certificate generated by the
finder, replacing the attack by `-1` raises `ValueError: negative shift
count`; replacing it by `5` or `12` raises `IndexError: tuple index out of
range`. A certificate checker should reject malformed data with `False`,
not terminate.

**Exact correction:** before any shift or indexing involving the attack, add
the equivalent of

```python
attack = obstruction.attack
if not isinstance(attack, int) or not 0 <= attack < graph.n:
    return False
```

and use `attack` thereafter. Add regression cases for `-1`, `graph.n`, and a
larger index, plus the order-zero graph.

This defect does not affect certificates returned by
`find_private_obstruction`, whose attacks are obtained by scanning
`graph.full`.

### Low implementation finding I2: duplicate guard records are ignored

Line 107 constructs a dictionary keyed by `record.guard`. Duplicate records
are silently collapsed. For the finder-generated \(C_5\) certificate, I
prepended a duplicate record for guard \(0\) with an out-of-range witness;
because the later valid record overwrote it, the checker returned `True`.
The accepted data still contains one valid witness for every possible guard,
so the mathematical lower-bound conclusion remains sound, but the checker
does not strictly validate every supplied record or the intended one-record-
per-guard schema.

**Exact correction:** reject duplicates before or while building the
dictionary. For example, require

```python
if len(obstruction.failed_guards) != len(possible):
    return False
```

in addition to the existing key-set equality, or explicitly reject a guard
already present while constructing `records`. Add a test containing both
orders of a valid/invalid duplicate.

### Low mathematical-exposition finding L1: name the bound used by
Corollary 5

Calling Corollary 5 simply “the contrapositive” suppresses one dependency.
The contrapositive alone proves only
\(\gamma^\infty(G)\ne\alpha(G)\). The lower bound
\(\gamma^\infty(G)\geq\alpha(G)+1\) additionally uses
\(\alpha(G)\leq\gamma^\infty(G)\).

**Exact correction:** add a one-sentence proof after the hypothesis:

> Theorem 4 gives \(\gamma^\infty(G)\ne\alpha(G)\); combining this with the
> general bound \(\alpha(G)\leq\gamma^\infty(G)\) and integrality yields
> \(\gamma^\infty(G)\geq\alpha(G)+1\).

This is a dependency/exposition correction, not a gap in the campaign's
mathematics, because the general bound is already proved in
`math/reductions.md`.

### Low test-coverage finding T1: the three focused tests do not exercise
the quantifiers or hostile certificates

The existing focused tests check one positive obstruction, four examples
with no obstruction, and two published near-misses. They do not directly
test:

1. all maximum independent sets rather than the first one;
2. equivalence with a transparent local swap oracle;
3. soundness against both eternal evaluators at \(k=\alpha\);
4. a graph that passes every local maximum-independent-state test but still
   has \(\gamma^\infty>\alpha\);
5. occupied, out-of-range, missing, extra, duplicated, or tampered records.

**Exact additions:** retain \(C_5\), add malformed-certificate tests covering
I1 and I2, and add ``FCp`_`` as a documented incompleteness example:
\(\alpha=3\), both eternal evaluators give \(\gamma^\infty=4\), yet the
finder correctly returns `None`. A bounded exhaustive test through order 6
or 7 should compare the finder with a direct successor-domination oracle and
assert that every reported obstruction makes both size-\(\alpha\) eternal
decisions false.

## 3. Implementation audit

### `maximum_independent_masks`

The function first obtains the exact cardinality and then enumerates every
subset of that size, retaining exactly the independent ones. It does not
confuse maximum with maximal independent sets. A transparent exhaustive
oracle agreed on every unlabeled graph through order 8.

### `private_region`

For each vertex `vertex`, the test

```python
closed & dominating == guard_bit
```

is parsed as `(closed & dominating) == guard_bit` and is exactly
\(N[\text{vertex}]\cap D=\{u\}\). It includes the guard vertex itself when
the state is independent. The later expression

```python
private_region(...) & ~graph.closed[attacked]
```

is safe despite Python's unbounded signed complement because it is first
intersected with a finite graph mask.

### `find_private_obstruction`

The loops have the intended quantifiers:

\[
 \exists S\text{ maximum independent}\ \exists r\notin S\
 \forall u\in S\cap N(r)\ \exists x_u\in P_S(u)-N[r].
\]

`possible` contains exactly adjacent occupied guards. If one guard has no
uncovered private vertex, the `break` correctly rejects this attack as an
obstruction because one valid response is enough. The `while ... else`
returns a certificate only after every possible guard has received a
witness. Iterating `graph.full ^ independent` considers exactly unoccupied
attacks. A maximum independent set is maximal and hence dominating, so an
outside attacked vertex always has a possible adjacent guard.

### `verify_private_obstruction`

For well-formed, in-range data, the checker proves everything needed:

- the named set is independent and has cardinality \(\alpha(G)\);
- the attack is unoccupied;
- the record keys are exactly the guards in \(S\cap N(r)\);
- each witness has the named guard as its unique closed-neighborhood
  dominator in \(S\);
- the new guard at \(r\) does not dominate the witness; and
- the explicit one-guard successor is nondominating.

The use of `graph.closed[attack]` to test whether the witness is in \(N[r]\)
is equivalent to testing `graph.closed[witness]` for `attack`, because
`BitGraph` enforces a simple undirected graph. The checker does not call an
eternal-domination procedure. It does share the `BitGraph` representation
and exact `alpha` implementation with verifier A, so it is transition-core
independent but not a fully separate graph/invariant implementation.

## 4. Independent exhaustive falsification attempts

These computations support, but do not replace, the proofs.

1. **All unlabeled graphs through order 8.** Using nauty `geng` 2.9.3, I
   checked all 13,599 unlabeled graphs of orders \(0,\ldots,8\). A transparent
   subset oracle independently enumerated all maximum independent sets and,
   for every outside attack, directly tested each swapped set for domination.
   It agreed exactly with `find_private_obstruction`: zero false positives
   and zero false negatives relative to the stated local predicate. Every
   generated certificate passed `verify_private_obstruction`.

2. **Both eternal evaluators.** On the same 13,599 graphs, the bitset
   greatest-fixed-point evaluator and the explicit colored-configuration-
   digraph evaluator agreed at \(k=\alpha\), including equality of their
   greatest surviving families. No graph with a reported private obstruction
   had a size-\(\alpha\) eternal family. Every maximum independent set was
   present in both greatest families whenever such a family existed.

3. **Contrapositive lower bounds.** There were 442 graphs with a reported
   obstruction. Both independent eternal evaluators gave
   \(\gamma^\infty-\alpha=1\) for every one of the 442, so all certified
   lower bounds were confirmed independently.

4. **Expected incompleteness, not false negatives of the implementation.**
   There were 142 graphs through order 8 with no local obstruction but no
   size-\(\alpha\) eternal family. For example, graph6 ``FCp`_`` has
   \(\alpha=3\) and \(\gamma^\infty=4\) in both evaluators while passing
   every maximum-independent-state one-step test. This confirms the warning
   in Section 4: absence of the obstruction is not a positive eternal
   certificate.

5. **Literal “every family” quantifier.** Independently of the greatest-
   fixed-point algorithms, I enumerated every nonempty subset of dominating
   \(k\)-configurations and directly checked family closure for every
   unlabeled graph through order 5. Across 565 actual eternal families for
   values of \(k\) admitting an independent \(k\)-set, every independent
   \(k\)-set belonged to every family. Thus the test covered proper eternal
   subfamilies as well as greatest families.

6. **Swap iff and closed-private-region implementation.** For every unlabeled
   graph through order 7, every dominating set \(D\), every \(u\in D\), and
   every unoccupied \(r\in N(u)\), a direct set oracle checked both sides of
   Lemma 3. All 532,138 legal swap instances agreed. The independently
   computed closed private regions also agreed with `private_region`.

7. **Repository test suite.** `python3 -m unittest discover -s tests -v`
   passed all 44 tests. The two malformed-certificate cases in I1 and I2 are
   currently absent and were reproduced separately.

The category counts in item 1 partition the 13,599 graphs as follows:
13,015 have a size-\(\alpha\) eternal family, 442 have a private obstruction,
and 142 fail size-\(\alpha\) eternity only after later non-independent states.

## 5. Final accept/reject table

| Item | Decision | Reason |
|---|---|---|
| Lemma 1 | **ACCEPT** | Every closure response raises \(|D\cap S|\) by one; the proof applies to every family. |
| Corollary 2 | **ACCEPT** | Exact specialization \(k=\alpha\); no greatest-family assumption. |
| Lemma 3 | **ACCEPT** | Correct iff with closed private neighborhoods and an explicit edge-move hypothesis. |
| Theorem 4 | **ACCEPT** | Uses only unoccupied attacks and one legal guard move; adjacency follows from closed privateness for independent \(S\). |
| Corollary 5 | **ACCEPT**, with L1 wording correction | The lower bound is the contrapositive plus \(\alpha\leq\gamma^\infty\). |
| Search limitation in Section 4 | **ACCEPT** | The obstruction is necessary, not sufficient; exhaustive examples confirm the distinction. |
| `find_private_obstruction` | **ACCEPT** | Exact implementation of the local predicate on valid graphs. |
| Finder-produced certificates | **ACCEPT** | Independently confirmed on every reported case through order 8. |
| `verify_private_obstruction` as a hostile-input checker | **REVISE, THEN ACCEPT** | Add attack bounds/type rejection and duplicate-record rejection. |
| Existing focused tests | **REVISE** | Add hostile certificate and bounded exhaustive quantifier tests. |

The mathematical document is ready for promotion to `PROVED` after recording
the minor dependency sentence in L1. The finder is safe as a rejection
filter now. The two checker hardening fixes should be made before advertising
the certificate format as robust against arbitrary external input.

## 6. Fix-verification addendum — 2026-07-25 13:50 PDT

This addendum audits the revisions made in response to findings I1, I2, L1,
and T1. It supersedes the corresponding “revise” decisions above.

**Revised-file hashes:**

- `math/lemmas/maximum_independent_states.md`
  (`sha256:08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e`)
- `src/search/private_obstruction.py`
  (`sha256:7814d8d247030009f2cb6a394ec6adc75f1d4e540118c203a687ffac78649f8b`)
- `tests/test_private_obstruction.py`
  (`sha256:66036ca3d473aa9e15c22fa51e049200f82caa5cae0b04cdd7e185f4542e6987`)

### I1 resolved: attack and field validation fail closed

The checker now validates the certificate class, independent-set mask,
attack type and range, record container, record class, guard type and range,
and witness type and range before using the corresponding values in shifts
or graph indexing. In particular, attacks `-1`, `graph.n`, larger integers,
and `True` now return `False`; the order-zero malformed certificate also
returns `False`. No shift or tuple-index exception remains on ordinarily
constructed malformed `PrivateObstruction` data.

I independently exercised 36 targeted malformed cases, including:

- a wrong certificate object;
- Boolean, nonintegral, negative, out-of-range, nonmaximum, and dependent
  independent-set masks;
- Boolean, nonintegral, negative, out-of-range, and occupied attacks;
- non-tuple, missing, extra, and non-`FailedGuard` record collections;
- Boolean, nonintegral, negative, out-of-range, and nonresponding guards; and
- Boolean, nonintegral, negative, and out-of-range witnesses.

Every case returned `False` without raising. A deterministic 20,000-case
malformed-dataclass fuzz probe likewise produced no exception.

**Updated decision for I1:** **RESOLVED / ACCEPT.**

### I2 resolved: duplicates are strictly rejected

The checker now requires the record-tuple length to equal the number of
possible guards and explicitly rejects a guard already present in the
record dictionary. A duplicate containing an invalid witness is rejected
whether placed before or after the valid record. Replacing a required guard
by a duplicate is also rejected by the key-set check.

**Updated decision for I2:** **RESOLVED / ACCEPT.**

### Finder/checker compatibility retained

The stricter checks do not reject legitimate finder output. I reran
`find_private_obstruction` on all 13,598 nonempty unlabeled graphs of orders
1 through 8. All 442 generated obstruction certificates passed the revised
checker. Together with the original order-zero audit, this preserves the
earlier 13,599-graph conclusion.

### L1 resolved: Corollary 5 now records its full dependency

Lines 99–102 now state that Theorem 4 first excludes equality and that the
general bound
\(\alpha(G)\leq\gamma^\infty(G)\), together with integrality, yields
\(\gamma^\infty(G)\geq\alpha(G)+1\). This is exactly the missing logical
sentence requested in L1.

**Updated decision for L1:** **RESOLVED / ACCEPT.**

### C7 insufficiency example verified

The added graph6 record ``FCp`_`` has order 7, size 7, degree sequence
\((2,2,2,2,2,2,2)\), and is connected; hence it is a relabeling of \(C_7\).
The private-obstruction finder returns `None`. Independently:

- verifier A gives
  \(\alpha(C_7)=3\) and \(\gamma^\infty(C_7)=4\);
- verifier B gives the same two values.

Thus the new statement in Section 4 is exact and is a clean witness that the
maximum-independent-state local condition is not sufficient for eternal
domination.

### Revised tests

The five focused private-obstruction tests all pass, including the
fail-closed and \(C_7\) cases. The full repository suite now passes all 58
tests:

```text
Ran 58 tests in 0.574s
OK
```

The original suggestion to make a bounded transparent-oracle comparison a
permanent regression test remains a useful future enhancement, but it is no
longer required to accept these fixes: the exhaustive 13,599-graph audit is
already recorded above, and the specific regressions that motivated I1 and
I2 are now in the focused suite.

### Final revised verdict

| Item | Revised decision |
|---|---|
| Mathematical results, including Corollary 5 | **ACCEPT** |
| `find_private_obstruction` | **ACCEPT** |
| Finder-produced certificates | **ACCEPT** |
| `verify_private_obstruction` on constructed certificate data | **ACCEPT** |
| Focused regression coverage for the reported defects | **ACCEPT** |
| \(C_7\) insufficiency statement | **ACCEPT** |

All findings from the original review are now either resolved or reduced to
an optional test-suite enhancement. No source or mathematics file was edited
as part of this re-audit.
