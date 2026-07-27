# Hostile review: minimal 2-SAT bicycles at \(k=3\)

Date: 2026-07-26 (PDT)

## Verdict

**PASS.**

The four statements labeled `PROVED` are correct at their stated
boundaries.  I found no illegal occupied attack, all-guards move, omitted
one-guard response, graph/complement reversal, unsound quantifier change, or
promotion of the order-eight observation to a finite theorem.

The exact accepted boundary is:

1. the normalized inclusion-minimal 2-CNF terminal trichotomy is proved;
2. the internal component-connector and singleton-terminal parity signs are
   correct;
3. the two displayed local geometries are impossible in an arbitrary
   specified one-guard eternal triple-family;
4. `GFznc{` is a valid \((2,3,3,3)\) counterboundary to automatic gluing,
   including a genuinely nontrivial independent-state ridge; and
5. the order-eight zero count remains `OBSERVED` for exact two-list
   restrictions only.

This review does **not** accept a theorem excluding arbitrary subdivisions
or longer bicycles, a reduction of every two-unit chain to the mixed
\(P_4\), a result for the full-list slice, a proof of the \(k=3\) slice, a
finite-frontier advance, or a resolution of the universal
\(\gamma\)--\(\theta\) conjecture.  The source note makes none of those
claims.

## Frozen review object

| artifact | SHA-256 |
|---|---|
| `math/working/k3_twosat_bicycle/NOTE.md` | `6d088edf77d6e0eee3491d2631db8ea0cebf614d112776ef8e719ffc90e6639a` |
| `math/working/k3_twosat_bicycle/evidence.py` | `052f7d55602b702935afa7dffb25f056b61d70d868606f5c4e91d1dce1b0f97c` |
| `math/working/k3_twosat_bicycle/evidence.json` | `f2025f12a1455e3cf44643ecf3e57324d9b5b2c1a183506a34299c04e63a4307` |
| `math/working/k3_twosat_bicycle/RESEARCH_LOG.md` | `fc7e55b3a1fa81677b201d236f857d389c82cf0495af179c894c1772db1dac78` |
| clean-room `independent_audit.py` | `0806fc076c0e2485ebbece7dd8474b018a0234d4d8e103914bb05d2d24dd96ac` |
| clean-room `independent_result.json` | `6de1f254a1c306aef2713a51927baef0fb606feb73eb03af9c9a1b3bc5217640` |
| generator replay `generator_rerun.json` | `fe47bbca42458aa7fc578a2789c843650e7eb5180496d94ab9c12d94b65a3822` |

The generator replay differs from the frozen evidence only in
`elapsed_seconds`.  Deleting that field from both JSON objects gives the
same SHA-256:

`92a7a163ff9167ac1f32ef9ff1b12a1cf1cc5fea95ea3e667983253caef35140`.

The clean-room checker imports no target search, transition, formula, or
parameter code.  It uses a fresh graph6 codec, ordinary Python sets, direct
truth tables, exhaustive subset/coloring routines, and its own literal
greatest-fixed-point deletion routine.

## Prerequisite audit

The response formula is built on the previously accepted frozen-color
projection and exact no-full-list gluing theorem.  I checked the current
bytes and their hostile reviews:

| prerequisite | SHA-256 |
|---|---|
| `math/working/k3_cross_state_attack.md` | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| `reviews/frozen_color_projection_hostile/REVIEW.md` | `cc8273ea5737562502af4991a5933e38b4eeb15de29c811bd1a3c4bb4fd7580e` |
| `math/working/k3_projection_gluing.md` | `fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907` |
| `reviews/k3_projection_gluing_hostile/REVIEW.md` | `f797870e45e2f8a0c0e6691a2b5e418ec1148043389fe2049c4453a0cfaf98d3` |
| `math/working/cross_state_response_exchange.md` | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| `reviews/cross_state_exchange_hostile/REVIEW.md` | `bc5011d85d333fb66fce3ea563e4cc80cf016090cc3427e44187b2e40fb5f9f8` |
| `math/working/k3_mixed_p4_attack.md` | `3af645890638f07fa38b294def7967679e280a6447173aa320e8715da714d92c` |
| `reviews/k3_mixed_p4_hostile/REVIEW.md` | `16740f59dc69d65f9b2d38cb1253a884f2997802e7d1d005da5e1b444d9d1d1c` |
| `math/working/k3_mixed_witness_followup.md` | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| `reviews/k3_mixed_witness_followup_hostile/REVIEW.md` | `2f029f856fa1d3c989f2e6e7e246185edceb7d3af2a2d269f154ba241d30e616` |

The prerequisite scope is sufficient.  In particular, for an arbitrary
eternal triple-family containing an independent triple, the frozen
projection has

\[
  \alpha=\gamma^\infty=2.
\]

The accepted parameter-two result therefore makes its complement
bipartite; the target note does not need to assume
\(\gamma(G)=3\) for this step.  The gluing theorem then gives the exact
2-CNF formula only under the explicitly retained no-full-list hypothesis.
No full-list vertex is silently encoded.

The note also cites the concurrent
`math/working/forced_c5_contradiction/NOTE.md`, SHA-256
`0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb`,
for the separate mixed-\(P_4\) conclusion
\(P_L\cap P_R=\varnothing\).  The target's comparison matches the literal
statement of that note and is not used to prove any of the four theorems
under review here.

## 1. Minimal-unsatisfiable 2-CNF trichotomy

Theorem 2.1 is sound after the normalization stated in its hypothesis.
Repeated-variable binary clauses reduce to units or tautologies, and
duplicate clauses and tautologies are removed.

Let \(U\) be the units and \(B\) the remaining binary formula.

- If \(B\) is unsatisfiable, inclusion minimality forces \(U=\varnothing\).
  The usual implication-graph criterion supplies opposite directed paths.
  Their clause union is already unsatisfiable, so minimality forces that
  union to cover every binary clause.
- If \(B\) is satisfiable but \(B\cup U\) is not, close all unit literals
  under reachability in \(I(B)\).  A complement-free implication-closed
  set of forced literals extends to a satisfying 2-SAT assignment, so the
  closure must contain \(x,\bar x\).  Hence two unit roots \(p,q\), possibly
  the same root, give
  \[
    p\leadsto x\leadsto\bar q.
  \]
  Those one or two units and the path clauses are already unsatisfiable.
  Inclusion minimality therefore leaves at most two units and forces the
  path to use every binary clause.

The cases are disjoint by \(|U|=2,1,0\).  A path can be trivial, as in the
normalized formula consisting only of the contradictory units
\(p,\bar p\); this is the standard reflexive reachability convention.

Two independent falsifiers agreed:

| variables | minimal unsatisfiable formulas | two-unit | one-unit | unit-free |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 |
| 2 | 11 | 6 | 4 | 1 |
| 3 | 148 | 39 | 60 | 49 |

The clean-room checker also generated 5,000 deterministic random formulas
on four through eight variables, shrank 3,806 unsatisfiable draws to
inclusion-minimal cores, and found zero formulas outside the trichotomy.
These computations are falsifiers only; the argument above proves the
theorem.

## 2. Port and connector parity

The signs in Theorem 3.1 are correct.  A port event is

\[
P(x,w): z=\pi(x)\oplus\iota(w).
\]

To continue an implication path after arriving at
\(\neg P(x,w)\), the next tail \(P(y,w')\) must be the complementary
literal.  Thus

\[
\pi(x)\oplus\pi(y)
=1\oplus\iota(w)\oplus\iota(w').
\]

Because the component is bipartite, this is exactly the path-length parity.
Equal collision colors give odd connectors and different collision colors
give even connectors.  At a singleton terminal, equality with the forced
unit cancels the common flip and gives

\[
\pi(s)\oplus\pi(x)=\iota(d)\oplus\iota(w),
\]

so equal terminal/port colors give an even connector and different colors
an odd connector.

The clean-room truth table checked all eight complement-event cases and all
eight terminal-agreement cases.  The type-turn reformulation is also
correct: at a \(v,u,t\) turn the two collision colors agree exactly when
\(v=t\).

The note appropriately does not infer that the whole expanded walk is
induced, that different component connectors are disjoint, or that a
logical core forces two physical end-witness systems to overlap.

## 3. One-guard audit of the lollipop exclusion

For Theorem 4.1, family membership of a direct swap is equivalent to the
corresponding positive response-list entry because \(S\) is independent.
The proof uses that equivalence in the correct direction.

Starting at \(D_0=\{b,c,p\}\), the attack at \(r\) has only the two
potential retained branches

\[
\{b,p,r\},\qquad \{c,p,r\};
\]
the \(p\)-move is the forbidden direct swap.  In the first branch, attack
\(s\).  The \(r\)-move is blocked by \(rs\in E(H)\), the \(b\)-move
produces a state failing to dominate \(q\), and the optional \(p\)-move
leads to a state unable to answer the unoccupied attack at \(c\).  The
second branch is the exact \(b/c\) reflection.  Every successor shape is
covered, and the dependency decreases rather than cycling.

As a clean-room check, I varied all nine unspecified edges consistent with
the hypotheses, covering 512 labelled graph completions.  I banned only
the four direct swaps forced absent by

\[
L(p)=\{a\},\qquad L(r)=L(s)=\{b,c\},
\]

and imposed no condition at all on \(L(q)\).  In every completion, the
greatest safe family avoiding those swaps deletes \(S\).  This computation
even relaxes the theorem by not requiring the positive direct swaps to be
retained.  It independently confirms that the source evidence's canonical
choice \(L(q)=\{a,b\}\) is not being used by the proof.

## 4. One-guard audit of the two-variable bicycle exclusion

Theorem 5.1 also exhausts its branches.

- From \(S\), attack \(q\).  The forbidden \(c\)-swap leaves the two
  branches \(A=\{a,c,q\}\) and \(B=\{b,c,q\}\).
- From \(A\), attack \(y\).  The \(q\)-move is a forbidden direct swap.
  Both remaining states fail at the subsequent attack on \(p\), because
  any response produces \(\{p,q,y\}\), which misses \(z\).
- From \(B\), attack \(z\).  The \(q\)-move is blocked.  In
  \(\{b,q,z\}\), the attack at \(r\) has exactly the three branches listed
  in the note; they respectively fail domination at \(p\), fail after the
  attack at \(p\), or end in two forbidden direct swaps at the attack on
  \(a\).  In \(\{c,q,z\}\), the attack at \(y\) either produces a state
  missing \(p\) or a state unable to answer the attack at \(a\).

All attacks are unoccupied, every candidate successor replaces exactly one
guard, and every graph move is either forced by a positive list entry or
explicitly conditional on the edge existing.

The clean-room checker varied all eight unspecified edges, covering 256
labelled graph completions.  It banned only the five direct swaps excluded
by (5.1), again without requiring the positive swaps as a membership
condition.  The reference state survived in none of the 256 greatest safe
families.

This accepts only the exact five-outside-vertex pattern with the seven
required complement edges.  It does not exclude subdivided connectors or
bicycles on at least three component variables.

## 5. `GFznc{` counterboundary

An independent graph6 decoder and the pinned nauty `showg` utility both
give order eight, size nineteen, and exactly the displayed graph and
complement edges.  The 35 listed triples are distinct, dominate, and meet
all

\[
35(8-3)=175
\]

unoccupied state/attack obligations through one adjacent guard move.

Direct exhaustive checks give

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

The family-response lists at \(012\) and \(127\) match (6.3) and (6.4).
Both have no full list and zero direct compatible list colorings.  The graph
has exactly the two independent triples \(012,127\), both in the family,
and the five covariance identities under \((0\ 7)\) hold literally.
Thus covariance is genuinely nonvacuous here and transports the
unsatisfiable no-full-list obstruction.

The one-guard/model distinctions are explicit:

- only 175 unoccupied attacks are obligations, not the 280 pairs obtained
  by incorrectly attacking every vertex;
- each accepted successor has symmetric difference two with its source and
  moves along one graph edge;
- every retained state is independently checked for domination; and
- the complement is used for list-color conflicts and \(\theta\), while
  guard movement and clique parts use \(G\).

A negative mutation adding the nondominating state \(017\) is rejected by
the clean-room checker.

The record `GFznc{` is a valid labelled graph6 record but is not a canonical
graph6 representative: pinned nauty `shortg` returns `G@~~fc`.  The note
does not call it canonical, and this graph is not a conjecture candidate
because \(\gamma=2\), so the campaign's canonical-certificate requirement
is not implicated.  The distinction should be preserved if the example is
later moved into a certificate manifest.

## 6. Order-eight scan and scope labels

The target generator reran successfully and reproduced its JSON payload
exactly apart from elapsed time.  A separate implementation then reproduced:

| \(\gamma\) | eligible graphs | reference states | restrictions | surviving exact two-list families |
|---:|---:|---:|---:|---:|
| 2 | 4,779 | 1,373 | 18,985 | 14,372 |
| 3 | 140 | 0 | 0 | 0 |

The pinned generator produced all 11,117 connected unlabeled graphs of
order exactly eight, and both implementations found zero uncolorable
retained exact-two-list instances.

The source labels this correctly:

- it is order **exactly** eight, not a theorem through order eight;
- it is restricted to
  \(\alpha=\gamma^\infty=3\), \(\gamma\in\{2,3\}\);
- it tests independent reference triples and exact two-list restrictions,
  not full-list or singleton-list instances;
- it is a single-order computational observation, not proof-log-backed
  coverage; and
- it neither raises the certified counterexample frontier nor proves the
  \(k=3\) slice.

The `OBSERVED BOUNDED FALSIFICATION` label is therefore accurate.

## Nonblocking editorial clarifications

No correction is required for acceptance.  Two small additions would make
future reuse safer:

1. state explicitly after Theorem 2.1 that directed paths may have length
   zero, covering the two contradictory-unit formula with no binary clause;
2. when discussing physical origins of terminal units, mention that after
   fixed anchor-component substitution a cross clause can also simplify to
   a unit.  The current parity theorem is only an internal-connector law
   plus a singleton-terminal law and does not falsely claim an exhaustive
   terminal taxonomy.

These are explanatory clarifications, not gaps in any theorem proved by the
reviewed bytes.

## Reproduction

From the repository root:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/k3_twosat_bicycle_hostile/independent_audit.py
```

The frozen output is `independent_result.json`.

## Revised-byte addendum

The verdict was rechecked against the revised `NOTE.md`, SHA-256

`8a934a8194913633821223b070a013dda8e0cd8c0d6870616b32a882e8b2fd59`.

Relative to the reviewed note
`6d088edf77d6e0eee3491d2631db8ea0cebf614d112776ef8e719ffc90e6639a`,
the revision makes exactly the two nonblocking clarifications requested
above:

1. implication paths are explicitly allowed to have length zero; and
2. fixed anchor-component substitution is explicitly recorded as another
   possible physical source of a unit.

Deleting only those two inserted passages from the revised bytes
reconstructs the prior 24,778-byte note literally, including its prior
SHA-256.  No theorem statement, proof step, example, computation, or claim
boundary changed.

The unchanged `evidence.py`, SHA-256
`052f7d55602b702935afa7dffb25f056b61d70d868606f5c4e91d1dce1b0f97c`,
was rerun against the revised note.  The refreshed `evidence.json` has
SHA-256

`e744f4f60cd4648c4d9537db0f0c5790d0f9ecae2746d7de65ef966aaa88cce6`

and binds the revised note hash correctly.  After deleting
`elapsed_seconds` and `source_binding.note_sha256`, its payload is identical
to the previously reviewed generator replay, with common normalized
SHA-256

`6c8bd8d608dba23ce70100bf39b97a5b7cd82a32cad1fa071ff758dd4fcaee68`.

**Final revised-byte verdict: PASS.**
