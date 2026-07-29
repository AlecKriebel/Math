# Hostile review: adjacent-pair repair dichotomy

## Verdict

**UNCONDITIONAL PASS**

Review date: 2026-07-28 PDT

Candidate commit:

```text
9c07f284af010e7ba9508e7039138ffff57c4de1
```

Candidate package:

```text
math/working/adjacent_pair_repair_dichotomy/
```

I reconstructed the proposed theorem from the literal one-guard
definition for an arbitrary eternal family of triples.  The common
nonneighbor set is nonempty exactly where the proof uses it; the clique
conclusion for an edge is made only in the retained-central-fan branch;
central-fan membership is uniform; and every displayed exchange is
physically unique.  In the omitted branch, independent completions
force both orientations of the edge without converting a missing
family state into a graph nonedge.

Every attack in the proof is at an unoccupied vertex, every move changes
one guard along one established graph edge, and all possible vertex
collisions have been excluded.  The theorem permits repeated witnesses
and therefore does not rely on the freshness assumption refuted by
C-169.

A clean-room verifier using neighbor sets and frozenset configurations
independently reproduces both fixed controls, every labeled-graph
greatest-family obligation through order six, and every arbitrary
eternal triple-subfamily obligation through order five.  It also audits
an immediate all-pairs corollary requested during review.

The discovery-only order-26 UNSAT observation remains unpromoted.  This
verdict does not eliminate QQ1, prove the complete parameter-three
case, or resolve the gamma--theta conjecture.

## 1. Exact assumptions and the forced-state lemma

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and let \(\mathcal F\) be any nonempty one-guard eternal family of
dominating triples.  The proof does not assume that \(\mathcal F\) is
the greatest family.

The candidate correctly uses the following fact.

> Every independent triple \(I\) belongs to every such
> \(\mathcal F\).

To verify it, begin at any \(D\in\mathcal F\).  If a vertex of \(I\) is
unoccupied, attack it.  No guard already placed on another vertex of
\(I\) can respond, because \(I\) is independent.  Thus one guard outside
\(I\) moves into \(I\), and \(|D\cap I|\) strictly increases.  Repeating
at most three times ends at \(I\).  Eternal closure keeps every
intermediate state in the same family.  The attacks are unoccupied by
construction, and exactly one guard moves at each step.

For any two vertices \(a,b\), the equality \(\gamma(G)=3\) says that
\(\{a,b\}\) is not a dominating set.  Its missed vertex is necessarily
outside the pair and is adjacent to neither endpoint.  Therefore

\[
 W_{ab}=\{w\notin\{a,b\}:aw,bw\notin E(G)\}
\]

is nonempty.  This argument is valid whether \(ab\) is an edge or a
nonedge.

## 2. Reconstruction of the retained-fan branch

Assume \(ab\in E(G)\) and

\[
 R_w=\{a,b,w\}\in\mathcal F
\]

for one \(w\in W_{ab}\).  Let \(z\in W_{ab}-\{w\}\).

The retained state \(R_w\) dominates \(z\).  By the definition of
\(W_{ab}\), neither \(a\) nor \(b\) hits \(z\).  Consequently
\(wz\in E(G)\).  This is the sole reason the proof concludes that
\(W_{ab}\) is a clique; it makes no clique claim in the omitted-fan
branch.

Now attack the unoccupied vertex \(z\) from \(R_w\).  The guards at
\(a,b\) are physically ineligible, while \(w\) is eligible.  Hence the
only physical response is

\[
 w\to z,\qquad R_w-w+z=\{a,b,z\}.
\]

Closure retains this successor.  Since \(z\) was arbitrary, every
central state is retained and every ordered pair of distinct witnesses
has the claimed unique exchange.

This also proves uniformity: if any central state is retained, then all
are retained.  Because \(W_{ab}\ne\varnothing\), if this branch does not
hold, every central state is omitted.  Thus the two family-membership
branches are exhaustive and mutually exclusive.  Reciprocal activity
is a different property and may occur in either branch, as the
candidate correctly states.

## 3. Reconstruction of both omitted-fan orientations

Assume \(ab\in E(G)\), fix \(w\in W_{ab}\), and suppose

\[
 R_w=\{a,b,w\}\notin\mathcal F.
\]

The pair \(\{a,w\}\) does not dominate because \(\gamma(G)=3\).  Choose
a missed vertex \(s\).  Then \(s\notin\{a,w\}\) and

\[
 as,ws\notin E(G).
\]

Moreover \(s\ne b\): the edge \(ab\) means that \(b\) is covered by
\(\{a,w\}\).  Thus

\[
 S=\{a,w,s\}
\]

is an independent triple in \(\mathcal F\), and the attack at \(b\)
from \(S\) is unoccupied.

Exactly the following response analysis is needed:

- \(a\) is eligible because \(ab\in E(G)\);
- \(w\) is ineligible because \(w\in W_{ab}\);
- \(s\) may or may not be eligible;
- if \(s\) is eligible, its successor is precisely the omitted state
  \(R_w\).

Therefore the only response whose endpoint can lie in
\(\mathcal F\) is

\[
 a\to b,\qquad \{b,w,s\}\in\mathcal F.
\]

This proves \(a\mathrel{\triangleright_{\mathcal F}}b\).  Interchanging
\(a,b\), choosing a missed vertex for \(\{b,w\}\), and repeating the
same argument proves
\(b\mathrel{\triangleright_{\mathcal F}}a\).

The proof works for every \(w\in W_{ab}\), although one witness suffices
for the stated activity conclusion.  It does not require different
missed completions for the two orientations and makes no assumption
that witnesses encountered elsewhere in an iteration are fresh.

## 4. Attack, collision, and inference audit

The complete proof-level attack ledger is:

| source state | attack | why unoccupied | possible responders | retained conclusion |
|---|---|---|---|---|
| \(\{a,b,w\}\) | \(z\in W_{ab}-\{w\}\) | \(z\) is distinct from \(a,b,w\) | only \(w\), because \(a,b\) miss \(z\) and domination forces \(wz\) | \(\{a,b,z\}\) |
| \(\{a,w,s\}\) | \(b\) | \(b\ne a,w\), and \(b\ne s\) because \(ab\) | \(a\), optionally \(s\); \(w\) misses \(b\) | the \(a\to b\) endpoint |
| \(\{b,w,s'\}\) | \(a\) | symmetric | \(b\), optionally \(s'\); \(w\) misses \(a\) | the \(b\to a\) endpoint |

No attack is made at an occupied vertex.  No response moves more than
one guard.  All retained endpoints are triples because the attacked
vertex is not already occupied.

The omitted central state is used only as a family-membership fact: it
rules out the optional \(s\to b\) endpoint.  It is never used to infer
that \(s\) and \(b\) are nonadjacent.  If \(sb\) is a nonedge, that
physical branch is absent; if \(sb\) is an edge, the branch exists but
its endpoint is omitted.  In both cases closure forces \(a\to b\).

Verdict on model fidelity, collisions, and omission-to-nonedge risk:
**PASS**.

## 5. Immediate all-pairs corollary

The following consequence is valid and was independently audited.  It
is not needed for the candidate theorem.

> **All-pairs corollary.**  Under the same assumptions, for every
> unordered pair \(\{a,b\}\), at least one of the following holds:
>
> 1. every state \(\{a,b,w\}\), \(w\in W_{ab}\), is retained, and
>    \(W_{ab}\) is a clique with the unique witness exchanges; or
> 2. \(ab\in E(G)\) and the edge is family-active in both directions.

The “or” is inclusive: a reciprocal edge may also have a retained
central fan.

For a nonedge \(ab\), every \(\{a,b,w\}\) with \(w\in W_{ab}\) is an
independent triple and hence retained.  If two witnesses \(w,z\) were
nonadjacent, then \(\{a,b,w,z\}\) would be an independent four-set,
contradicting \(\alpha(G)=3\).  Equivalently, the retained central state
\(\{a,b,w\}\) must dominate \(z\).  The same one-guard uniqueness audit
then gives \(w\to z\).  For an edge, the candidate dichotomy supplies
the stated inclusive alternative.

The clean-room census checked this corollary on 20,338 nonedge pair-fans
and 18,792 directed nonedge exchanges in the applicable greatest
families through order six.  It also checked 1,273 pair-fans and 432
directed exchanges across all applicable arbitrary eternal
triple-subfamilies through order five.

## 6. Applicability to the C-169 boundary

The actual C-169 order-18 graph has \(\gamma=2\); in particular
\(\{u,14\}\) is a dominating pair.  The theorem therefore does not apply
to that fixed graph and does not contradict its exact certificate.

Its correct use is conditional and all-order.  In a hypothetical
\(\gamma=3\) realization with an analogous adjacent auxiliary escape
\(ua\), the pair \(\{u,a\}\) has a nonempty common-nonneighbor set.
Applying the theorem to that arbitrary adjacent pair yields:

\[
 u\mathrel{\triangleright_{\mathcal F}}a
 \text{ and }
 a\mathrel{\triangleright_{\mathcal F}}u,
 \quad\text{or}\quad
 W_{ua}\text{ is a retained central-token clique.}
\]

The conclusion quantifies over the entire common-nonneighbor set.  It
allows witness recycling and survives the exact two-cycles exhibited
by C-169.  It is not itself a contradiction and does not show which
branch occurs in QQ1.

Verdict on the candidate's stated C-169 application: **PASS**.

## 7. Independent finite replay

The hostile verifier represents a graph by immutable neighbor sets and
a guard state by a `frozenset`.  It imports neither the candidate's
integer-bitset checker nor any campaign evaluator.  Greatest families
are recomputed by literal synchronous deletion from all dominating
configurations.  Arbitrary subfamilies are tested directly against
every unoccupied attack.

It independently obtains:

- 33,867 labeled graphs examined through order six;
- 2,162 applicable greatest eternal triple-families;
- edge obligations
  \(7,086\) omitted-reciprocal,
  \(3,120\) retained-nonreciprocal, and
  \(1,320\) retained-reciprocal;
- 45,264 explicit omitted-branch orientation constructions;
- 197 applicable arbitrary eternal triple-subfamilies on 107 graphs
  through order five;
- arbitrary-family edge obligations
  \(306\), \(240\), and \(120\), respectively;
- 1,224 explicit arbitrary-family orientation constructions.

For `EpQ?`, the verifier reconstructs edge set

\[
 \{01,02,05,14,23\},
\]

connectedness, eight greatest-family triples, branch counts
\((3\text{ omitted-reciprocal},2\text{
 retained-nonreciprocal})\), and exact parameter vector

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

For `D]?`, it reconstructs \(K_{2,2}\) plus an isolated vertex, six
greatest-family triples, four retained-reciprocal edge obligations, and
the same exact parameter vector.  These examples establish that both
principal membership branches occur and that retained-fan membership
does not imply nonreciprocity.

All finite results exactly match the candidate audit.  The census is a
regression test and sharpness check; the universal theorem rests on the
human proof above.

## 8. Scope discipline

The candidate research log reports an equality-plus-closure discovery
formula retaining the induced boundary as UNSAT through order 26.  It
also explicitly states that those runs have no proof logs or coverage
theorem.  The fixed audit result does not contain that observation, and
this review does not promote it.

Promoted scope:

- the adjacent-pair repair dichotomy for any eternal triple-family under
  \(\gamma=\alpha=\gamma^\infty=3\);
- the immediate all-pairs inclusive corollary proved in Section 5;
- the two exact sharp controls and finite regression censuses.

Not promoted:

- any order-26 finite exclusion;
- elimination of canonical QQ1;
- reciprocity of every edge;
- the complete \(k=3\) theorem;
- the universal gamma--theta conjecture.

Reproduce this hostile review from the campaign root with:

```text
sh reviews/adjacent_pair_repair_dichotomy_hostile/verify_strict.sh
```
