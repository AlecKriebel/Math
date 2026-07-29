# Hostile review: supported pair fans in the completion layer

## Verdict

**UNCONDITIONAL PASS**

Review date: 2026-07-28 PDT

Candidate commit:

```text
f7eb54c7099d71d25e3804977101fa68586135c1
```

Candidate package:

```text
math/working/full_list_completion_coupling/
```

I reconstructed both proposed theorems from the literal one-guard
definition, independently checked the uses of accepted C-010, C-170, and
C-172, and found no missing case or model error.  Every attack is at an
unoccupied vertex, every response moves one adjacent guard, and every
claimed successor lies in the same arbitrary eternal family.

The first theorem is genuinely stronger than accepted C-172 for a
family-supported pair.  C-172 alone gives a retained-fan-or-reciprocal
alternative for an edge; co-occupancy in a retained triple forces the
retained-fan side even when the third guard is not itself a common
nonneighbor of the pair.

The second theorem has the correct exact “if and only if” for domination
of the cross state.  A trapped fan member supplies the independent source
for reverse activity, while fullness supplies the forward activity.  No
family omission is interpreted as a graph nonedge, and the conclusion is
reciprocity only—not retention or a deletion-rank bound for the cross
state.

A clean-room verifier using immutable neighbor sets and frozenset guard
states independently reproduces the three equality controls and the
gamma-two boundary.  It also checks every applicable greatest eternal
triple-family over all 33,867 labeled graphs through order six, and every
applicable arbitrary eternal triple-subfamily through order five.

This pass promotes only the local supported-fan and
fan--reciprocity statements and their C-170 corollary.  It does not prove a
safe color, complete parameter three, exclude a finite order, or resolve
the gamma--theta conjecture.

## 1. Assumptions and family quantifier

The universal statements assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and an arbitrary nonempty eternal family \(\mathcal F\) of dominating
triples.  They do not require the greatest family.

Accepted C-010 applies with exactly this quantifier: every independent
triple belongs to every eternal triple-family.  The usual forcing proof
starts at any family state and attacks unoccupied vertices of the target
independent triple.  A guard already on that independent triple cannot
move to another one of its vertices, so each response increases the
intersection by one and remains within the same family.

The equality \(\gamma(G)=3\) also makes

\[
 W_{ab}=\{z\notin\{a,b\}:az,bz\notin E(G)\}
\]

nonempty for every distinct pair \(a,b\): otherwise the pair dominates.
This is the only nonemptiness input.  The clique and retention conclusions
use eternal closure.

## 2. Reconstruction of supported-pair saturation

Let \(D=\{a,b,c\}\in\mathcal F\), and fix \(z\in W_{ab}\).

If \(z=c\), then \(\{a,b,z\}=D\) is already retained.  The candidate
correctly makes no attack at \(z\) in this collision case.

If \(z\ne c\), the retained dominating state \(D\) covers \(z\).
The guards at \(a,b\) both miss \(z\), so necessarily \(cz\in E(G)\).
The attack at \(z\) is unoccupied and has exactly one physically eligible
guard:

\[
 \{a,b,c\}\xrightarrow{c\to z}\{a,b,z\}\in\mathcal F.
\]

For distinct \(z,z'\in W_{ab}\), the newly retained state
\(\{a,b,z\}\) dominates \(z'\).  Again \(a,b\) miss \(z'\), so
\(zz'\in E(G)\).  Thus \(W_{ab}\) is a clique and the entire central fan
is retained.

This proof does not assume that \(ab\) is an edge or nonedge, nor that
\(c\in W_{ab}\).  In particular, it supplies content not obtainable by
merely selecting one alternative in C-172:

- if \(ab\) is a nonedge, C-010 already retains every independent central
  state;
- if \(ab\) is an edge, C-172 permits either a retained fan or an omitted
  fan with reciprocal activity;
- the co-occupied state \(D\) forces retention in both cases, including
  when \(c\notin W_{ab}\).

Verdict on fan uniformity, clique scope, family quantifier, and novelty
relative to C-172: **PASS**.

## 3. Exact cross-state identity

Use the candidate notation: \(S=\{u,v,t\}\) is an independent retained
root, \(x\) is full at \(S\), \(xr,xd,rd\notin E(G)\), and

\[
 D_t(d)=\{d,t,r\}\in\mathcal F.
\]

The state \(I=\{x,r,d\}\) is an independent triple, hence retained by
C-010.  Put \(B=N_{\overline G}(x)\) and
\(X_t(d)=\{x,d,t\}\).

A vertex is missed by \(X_t(d)\) exactly when it misses all three guards.
Missing \(d,t\) places it in \(W_{dt}\); missing \(x\) places it in
\(B\).  The definitions already exclude the occupied vertices:
\(W_{dt}\) excludes \(d,t\), \(B\) excludes \(x\), and \(x\notin W_{dt}\)
because fullness gives \(xt\in E(G)\).  Therefore

\[
 V(G)-N_G[X_t(d)]=W_{dt}\cap B.
\]

Consequently,

\[
 X_t(d)\text{ dominates}\quad\Longleftrightarrow\quad
 W_{dt}\cap B=\varnothing.
\]

This is an exact set identity, not a one-way implication.  Closed
neighborhood domination is used correctly; no endpoint or loop is
accidentally counted.

Verdict on the cross-state “if and only if”: **PASS**.

## 4. Reconstruction of both activity directions

Suppose \(e\in W_{dt}\cap B\).  The triple

\[
 J_e=\{x,d,e\}
\]

is independent because \(xd,de,xe\notin E(G)\), and so C-010 puts it in
\(\mathcal F\).  The attack at \(t\) is unoccupied:

- \(t\ne x\) because \(x\notin S\);
- \(t\ne d\) because \(xt\) is an edge while \(xd\) is not;
- \(t\ne e\) because \(e\in W_{dt}\).

The guard at \(x\) is adjacent to \(t\), and its successor is the fan
state

\[
 J_e-x+t=\{d,t,e\},
\]

which supported-pair saturation already retained.  Thus this is a legal
one-guard response witnessing
\(x\mathrel{\triangleright_{\mathcal F}}t\).  The activity definition
requires existence of this retained response; it does not require it to
be the only possible response.

Conversely, fullness at the independent root explicitly retains

\[
 S-t+x,
\]

so the unoccupied attack at \(x\) from \(S\) witnesses
\(t\mathrel{\triangleright_{\mathcal F}}x\).  Hence a trapped fan member
forces reciprocal activity of the physical edge \(xt\).

The collision \(e=r\) is harmless when it occurs: \(J_e=I\), the attack
is still at the unoccupied vertex \(t\), and the endpoint is the assumed
branch \(D_t(d)\).  No occupied attack is introduced.

Verdict on source independence, activity directions, and collision
handling: **PASS**.

## 5. C-170 corollary

Accepted C-170 supplies the retained terminal state

\[
 E=\{v,t,r\}
\]

and the completion clique

\[
 C_{xr}=\{d:dx,dr\notin E(G),\ d\notin\{x,r\}\}.
\]

For every \(d\in C_{xr}\), the attack at \(d\) from \(E\) is unoccupied:
fullness gives \(xv,xt\in E(G)\), while \(dx\notin E(G)\), so
\(d\ne v,t\); the definition gives \(d\ne r\).  The guard at \(r\) is
ineligible because \(rd\notin E(G)\).  Eternal closure therefore retains
at least one physical response:

\[
 v\to d:\{d,t,r\},\qquad
 t\to d:\{v,d,r\}.
\]

Applying the general theorem to the selected branch, with anchor \(t\)
or \(v\), gives its complete supported fan and the exact alternative:
the corresponding cross state dominates, or the target--anchor edge is
reciprocal.  If neither \(xv\) nor \(xt\) is reciprocal, the branch
selected for each completion must be in the dominating-cross case.

The corollary does not require both branches to be physical.  It chooses
one branch actually supplied by the attack.  A different branch may also
belong to the family for unrelated dynamic reasons; the candidate
correctly avoids interpreting that membership as a terminal-entry move.

Verdict on the C-170 specialization and its quantifiers over the whole
completion clique: **PASS**.

## 6. Complete attack and inference ledger

| source | attack | occupancy and eligible guards | conclusion |
|---|---|---|---|
| \(\{a,b,c\}\) | \(z\in W_{ab}-\{c\}\) | unoccupied; \(a,b\) miss \(z\); domination forces and uniquely permits \(c\to z\) | \(\{a,b,z\}\in\mathcal F\) |
| \(\{x,d,e\}\) | \(t\) | unoccupied; \(x\to t\) is an edge and has an already-retained fan endpoint | \(x\triangleright_{\mathcal F}t\) |
| \(S=\{u,v,t\}\) | \(x\) | unoccupied; fullness explicitly retains \(t\to x\) | \(t\triangleright_{\mathcal F}x\) |
| \(E=\{v,t,r\}\) | \(d\in C_{xr}\) | unoccupied; \(r\) misses \(d\); closure uses \(v\) or \(t\) | at least one completion branch retained |

No proof step:

- attacks an occupied vertex;
- moves two or more guards;
- uses an edge of the complement as a move edge;
- confuses omission from \(\mathcal F\) with a graph nonedge;
- assumes a retained branch was physically used when first created;
- assumes a fresh witness;
- infers retention or a restricted deletion rank for a dominating cross
  state.

Verdict on exact one-guard semantics and inference discipline: **PASS**.

## 7. Independent fixed controls

The clean-room verifier decodes graph6 without campaign code and
independently computes \(\gamma,i,\alpha,\gamma^\infty,\theta\), the
greatest eternal triple-family, the supported fans, activity, and cross
domination.

For

```text
OYifur}UO]}iTij]tpo]v
```

it obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
 \qquad |\mathcal F^\star|=304.
\]

It reproduces all three claimed sharp cases:

1. \(W_{1,7}=\{5,14\}\), with trapped member \(5\); the cross state
   \(\{1,6,7\}\) is nondominating and omitted, and \(6,1\) are active
   in both directions.
2. \(W_{0,7}=\{12\}\), with no trapped member; the cross state
   \(\{0,6,7\}\) dominates and is retained.
3. \(W_{1,7}=\{5,14\}\), with no member trapped relative to target 12;
   the cross state \(\{1,7,12\}\) dominates but is omitted.

The third case confirms that domination cannot be strengthened to family
membership.

For

```text
HF~mdfj
```

it obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3),
 \qquad |\mathcal F^\star|=76,
\]

and verifies that the retained branch \(\{2,5,8\}\) has
\(W_{2,8}=\varnothing\).  Thus \(\gamma=3\) is genuinely needed for fan
nonemptiness.

## 8. Independent bounded census

The verifier represents graphs by immutable neighbor sets and
configurations by frozensets.  It imports neither the candidate checker
nor any campaign evaluator.  Greatest families are recomputed by literal
synchronous fixed-point deletion, and arbitrary subfamilies are checked
directly against every unoccupied attack.

Across all 33,867 labeled graphs through order six it finds 2,162
applicable equality graphs and independently checks:

- 44,679 supported pair-fans;
- 65,631 fan witnesses;
- 31,992 physically unique noncollision fan exchanges.

Across all 1,099 labeled graphs through order five it finds 107 applicable
graphs and 197 arbitrary eternal triple-subfamilies, checking:

- 2,559 supported pair-fans;
- 2,991 fan witnesses;
- 1,152 physically unique noncollision fan exchanges.

No full-target completion instance satisfying the general second
theorem occurs in these small censuses; its three logical boundary cases
are instead independently exercised by the exact 16-vertex control.  The
census is a regression test, not a proof of the universal statements.

## 9. Promoted scope

Promoted as proved:

- every pair co-occupied in a retained triple has its whole
  non-domination witness fan retained and that fan is a clique;
- for every retained completion branch at a full target, the cross state
  dominates exactly when the supported fan avoids the target-ban region;
- any trapped fan member forces reciprocal target--anchor activity;
- every C-170 completion has a retained supported-fan branch whose cross
  state dominates or whose target--anchor edge is reciprocal.

Promoted as exact controls:

- nondominating/reciprocal, dominating/retained, and
  dominating/omitted cross branches in the 16-vertex equality graph;
- the gamma-two empty-fan boundary.

Not promoted:

- family membership or a deletion-rank bound for every dominating cross
  state;
- a safe color or strict rank descent;
- any finite exclusion;
- the complete \(k=3\) theorem;
- the universal gamma--theta conjecture.

Reproduce this review from the campaign root with:

```text
sh reviews/full_list_completion_coupling_hostile/verify_strict.sh
```
