# Hostile review: future-stable colors and the cumulative kernel

## Verdict

**PASS ON THE REVISED BYTES.**

The reviewed theorem package is
`math/working/full_list_safe_color_proof/NOTE.md` at SHA-256

`a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d`

with manifest SHA-256

`8a09e4c9c932caeebea257f7ac8c3e9ece51d1a4dbd444cfa562a55dc86de3f4`.

At this revision, I found Theorem 2.1, Corollary 3.1, Proposition 4.1,
Theorem 4.2, Proposition 5.1, and Proposition 5.2 sound at their stated
strict scopes.

The package proves reductions, not the missing existence statements:

- it does not prove that any color-restricted kernel is nonempty;
- it does not prove that any residual exact 2-CNF is satisfiable;
- it does not prove complete \(k=3\); and
- it does not resolve the gamma--theta conjecture.

No literature-priority conclusion is reviewed here.

## Correction history

The initially frozen note at SHA-256

`0a260426900ea972ab3070a897f5702fa4f139cd6543fcbcf9887ee09992eac3`

had two local presentation defects found during this hostile audit.

1. The original proof of Theorem 2.1 applied an outside-vertex response
   list to every \(b\in B_x=N_H(x)\), although \(B_x\) can contain
   anchors in \(S-\{u\}\).  The revised proof first excludes
   \(u\in B_x\), treats \(B_x\cap(S-\{u\})\) as projection base vertices,
   and invokes response lists only for \(B_x-S\).
2. The original corridor description called a root entry a “singleton
   response.”  That is false if it means a one-color response list.  In
   the equality control, several such root entries have two-color lists.
   The revised note correctly calls it only a direct \(u\)-response.

Both corrections are mathematically complete in the revised bytes.
Equation references (2.3)--(2.7) remain consistent after the edit.

## Frozen artifacts

| artifact | SHA-256 |
|---|---|
| revised candidate note | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| revised candidate manifest | `8a09e4c9c932caeebea257f7ac8c3e9ece51d1a4dbd444cfa562a55dc86de3f4` |
| candidate control verifier | `34f3d2cfe9026af493d943773ea8c0c5f729c20d90c0214555e330d8cea54811` |
| candidate expected result | `2e413f103f73d5da4afcf0960b15a384bff6ae2e3c1699d2df1be1f2e41e0b0b` |
| C-010 source | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| C-006 source | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| current C-063 source | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| current C-063 hostile review | `cc8273ea5737562502af4991a5933e38b4eeb15de29c811bd1a3c4bb4fd7580e` |
| clean-room checker | `f10fb55401ba639a61d1aef6c04208df3c11ca1e5df8f8ea9c366d926bef909a` |
| clean-room evidence | `dd98027a5e73551e1f5db356f8c2e257bbe5a44bf95de74790e8b872d5fd30af` |

The clean-room checker imports no candidate transition, coloring, or
parameter code.  It uses packed integer configurations, reconstructs the
one-guard fixed point directly, and separately generates the exact 2-CNF.

## 1. Quantifiers and greatest-family semantics

The note distinguishes the three relevant families correctly.

- \(\mathcal F^\star\) is the literal greatest unrestricted eternal family
  of dominating triples.
- \(\mathcal E\) in Theorem 2.1 is an arbitrary nonempty eternal family;
  it need not be greatest.
- \(\mathcal K_u(x)\) and \(\mathcal K_f\) are greatest eternal families
  after specified states have been forbidden.

These greatest families exist literally: the union of any collection of
eternal families on the same configuration universe is eternal.  For a
state in the union, choose one constituent family containing it; all its
required responses remain in that constituent and hence in the union.
Equivalently, the usual descending deletion operator computes this union.

Under \(\alpha=\gamma^\infty=3\), C-010 applies to every nonempty eternal
triple-family, greatest or not.  Therefore every independent triple,
including the fixed root \(S\), lies in \(\mathcal E\), every nonempty
restricted kernel, and \(\mathcal F^\star\).

The list

\[
L_S^{\mathcal E}(z)
=\{u\in S:uz\in E(G),\ S-u+z\in\mathcal E\}
\]

uses \(G\)-edges as move edges and records membership in the same specified
family.  It is not a static list, and no proof step silently replaces
family nonmembership by graph nonadjacency.

## 2. Theorem 2.1: ban-avoidance forcing

Fix \(x\notin S\), \(u\in S\), and

\[
B_x=N_H(x),\qquad
\mathcal B_u(x)=\{S-u+b:b\in B_x\}.
\]

Let \(\mathcal E\) be a nonempty eternal family avoiding this ban, and
suppose for contradiction that

\[
u\notin L_S^{\mathcal E}(x).
\]

The revised anchor handling is necessary and correct.

First, \(u\notin B_x\).  If \(u\in B_x\), then the member indexed by
\(b=u\) in the ban is

\[
S-u+u=S,
\]

contradicting both \(S\in\mathcal E\) and ban avoidance.

For \(b\in B_x-S\), the direct state \(S-u+b\) is banned, so

\[
u\notin L_S^{\mathcal E}(b).
\]

For \(b\in B_x\cap(S-\{u\})\), no outside response list is needed: \(b\)
is already one of the fixed base vertices in the frozen projection

\[
Q_u=G[(S-\{u\})\cup W_u],\qquad
W_u=\{z\notin S:u\notin L_S^{\mathcal E}(z)\}.
\]

The assumed failure puts \(x\in W_u\).  These three cases give exactly

\[
\{x\}\cup B_x\subseteq V(Q_u).
\]

C-063 applies to the arbitrary family \(\mathcal E\), not merely to a
greatest family, and gives

\[
\alpha(Q_u)=\gamma^\infty(Q_u)=2.
\]

C-006 therefore gives \(\theta(Q_u)=2\), so
\(H[V(Q_u)]\) is bipartite.

The final triangle argument is complete:

- \(B_x\ne\varnothing\), since \(B_x=\varnothing\) would make \(x\) a
  dominating vertex of \(G\), contradicting \(\gamma(G)=3\);
- choose \(b\in B_x\);
- the pair \(\{x,b\}\) is not dominating, again because
  \(\gamma(G)=3\);
- a vertex \(c\) missed by this pair is adjacent in \(H\) to both \(x\)
  and \(b\); and
- since \(c\in B_x\), all of \(x,b,c\) lie in \(Q_u\).

Thus \(xb,xc,bc\in E(H)\), a triangle in a bipartite graph.  This proves

\[
u\in L_S^{\mathcal E}(x).
\]

The argument uses the exact one-guard model only through C-010, C-063, and
the family-list definition.  It neither assumes \(x\) is full nor assumes
\(\mathcal E\) is greatest.

The clean-room equality control contains explicit cases where
\(B_x\cap(S-\{u\})\ne\varnothing\) and the restricted kernel is nonempty.
For example, at target \(4\), color \(u=3\), anchor \(2\) lies in \(B_x\);
the revised base-vertex branch handles it, and the 64-state restricted
kernel forces response list \(\{3\}\) at \(x\).

## 3. Corollary 3.1

For a full target \(x\), the equivalence

\[
u\text{ safe at }(S,x)
\quad\Longleftrightarrow\quad
\mathcal K_u(x)\ne\varnothing
\]

is exact.

The forward implication is definitional.  Conversely, a nonempty
\(\mathcal K_u(x)\) is an eternal family avoiding
\(\mathcal B_u(x)\).  Theorem 2.1 puts

\[
S-u+x\in\mathcal K_u(x)
\]

and includes the move edge \(ux\in E(G)\).  C-010 independently puts
\(S\in\mathcal K_u(x)\).  These are precisely the two state-membership
conditions in the safe definition.

This proves only the equivalence.  It does not prove that one of the three
restricted kernels is nonempty.

## 4. Proposition 4.1 and cumulative bans

Let \(X\) be the vertices having full response list in
\(\mathcal F^\star\), let \(f:X\to S\), and forbid

\[
\mathcal B_f
=\bigcup_{x\in X}
\{S-f(x)+b:b\in N_H(x)\}.
\]

If \(\mathcal K_f\ne\varnothing\), then it avoids each individual ban.
Theorem 2.1 therefore forces, simultaneously,

\[
f(x)\in L_S^{\mathcal K_f}(x)
\qquad(x\in X).
\]

For \(b\in N_H(x)\), the only direct \(f(x)\)-state at \(b\) is
\(S-f(x)+b\), and that state is in the cumulative ban.  Hence

\[
f(x)\notin L_S^{\mathcal K_f}(b).
\]

The union ban is retained throughout one fixed-point calculation, so no
sequential recomputation can reintroduce an earlier forbidden state.

Because every \(x\in X\) is full, it is adjacent in \(G\) to all three
anchors.  Consequently \(N_H(x)\cap S=\varnothing\) in the cumulative and
terminal-entry sections; every banned set there is genuinely a triple.

## 5. Domain and exact 2-CNF audit

For \(Y=V(G)-(S\cup X)\), nonemptiness of \(\mathcal K_f\) gives:

1. \(S\in\mathcal K_f\) by C-010;
2. every \(y\in Y\) has a nonempty response list, by attacking \(y\) from
   \(S\); and
3. \(\lvert L_S^{\mathcal K_f}(y)\rvert\le2\), because
   \(\mathcal K_f\subseteq\mathcal F^\star\) and \(y\notin X\).

Thus the domains are exactly:

\[
D_f(s)=\{s\},\quad
D_f(x)=\{f(x)\},\quad
D_f(y)=L_S^{\mathcal K_f}(y),
\]

with all sizes one or two.

A two-element domain is one Boolean variable.  For each \(H\)-edge and
each color common to its endpoint domains, forbidding simultaneous use of
that color gives:

- a binary clause if both endpoints have two choices;
- a unit clause if one endpoint is fixed; or
- an empty clause if two fixed endpoints conflict.

These clauses are necessary and sufficient because a proper coloring
fails exactly when some \(H\)-edge has equal endpoint colors.  There are no
other coloring constraints after each vertex chooses exactly one member of
its domain.

The clean-room checker generated this 2-CNF independently and compared its
satisfying-assignment count with direct list coloring on every

\[
2^3\cdot6^3=1{,}728
\]

combination of a three-vertex graph and nonempty one- or two-element
domains over three colors.  All 1,728 counts agreed; 1,470 instances were
satisfiable and there were zero mismatches.

## 6. Theorem 4.2, forward direction

Suppose \(f\) is proper on \(H[X]\), \(\mathcal K_f\ne\varnothing\), and
\(\Phi_f\) is satisfiable.  A satisfying assignment chooses one domain
color at every vertex and violates no equal-color edge clause.  It is
therefore a proper three-coloring of \(H\).

This first proves \(\theta(G)=\chi(H)\le3\).  Under the standing hypothesis
\(\alpha(G)=3\), the three vertices of \(S\) form a triangle in \(H\), so
\(\chi(H)\ge3\).  Hence \(\theta(G)=3\) exactly.

No eternal-strategy existence is inferred from the 2-CNF: it is already
supplied separately by the nonempty-kernel condition.

## 7. Theorem 4.2, reverse direction

Suppose \(\theta(G)=3\), choose a proper three-coloring \(\kappa\) of
\(H\), and relabel its colors so that \(\kappa(s)=s\) for \(s\in S\).
This relabeling is valid because the independent triple \(S\) in \(G\) is
a triangle in \(H\) and therefore uses all three colors.

Set \(f=\kappa|_X\).  It is proper on \(H[X]\).

For each color, its vertices form an independent set in \(H\), equivalently
a clique in \(G\).  Let \(\mathcal T_\kappa\) be all triples containing one
vertex of each color.

- Every transversal dominates \(G\): each graph vertex is occupied or is
  adjacent in its same-color \(G\)-clique to the selected guard.
- At an unoccupied attacked vertex, move the unique guard of the same
  color along that \(G\)-edge.  The successor is again a transversal.
- Thus \(\mathcal T_\kappa\) is an eternal family in the exact one-guard
  model.

If \(b\in N_H(x)\), then
\(\kappa(b)\ne\kappa(x)=f(x)\).  The state \(S-f(x)+b\) duplicates
\(\kappa(b)\)'s color and omits \(f(x)\)'s color, so it is not a
transversal.  Therefore \(\mathcal T_\kappa\) avoids
\(\mathcal B_f\), and greatestness gives

\[
\mathcal T_\kappa\subseteq\mathcal K_f.
\]

In particular \(\mathcal K_f\ne\varnothing\).  For every \(y\in Y\), the
transversal \(S-\kappa(y)+y\) belongs to \(\mathcal K_f\), and the
same-color anchor is adjacent to \(y\) in \(G\).  Hence

\[
\kappa(y)\in L_S^{\mathcal K_f}(y).
\]

The coloring \(\kappa\) respects every domain and satisfies \(\Phi_f\).
This proves the reverse implication without presuming that a suitable
\(f\), kernel, or Boolean assignment exists under equality alone.

On the named equality control, the clean-room checker reconstructed the
one surviving color assignment, its 64-state kernel, its unique compatible
coloring, and the complete 64-state clique-fiber family.  Every fiber state
dominates, all one-guard responses stay in the fiber, the family avoids the
cumulative ban, and it is contained in the restricted greatest kernel.

## 8. Proposition 5.1: retained rank descent

Assume \(\mathcal K_u(x)=\varnothing\).  Start with all dominating triples
outside \(\mathcal B_u(x)\) and delete synchronously.  Since the terminal
kernel is empty, every initial state has a finite rank, numbered by its
deletion round.

Let \(D\in\mathcal F^\star-\mathcal B_u(x)\).  It is a dominating allowed
triple and therefore has a rank.  Choose an unoccupied attack witnessing
its deletion.  Greatest-family closure supplies at least one retained
successor in \(\mathcal F^\star\).

- If that successor is banned, the trace has reached its terminal state.
- If it is not banned, it is a dominating allowed triple.  Since it was
  absent from the active set at the stage deleting \(D\), its deletion
  rank is strictly smaller.

Repeating gives a finite retained trace with strictly decreasing
nonterminal ranks and a final state in
\(\mathcal F^\star\cap\mathcal B_u(x)\).

For a full target, \(S-u+x\in\mathcal F^\star\), and it is not banned
because \(x\notin N_H(x)\).  Hence the stated “in particular” case is
valid.

The clean-room checker verified this descent from all 124 states of
\(\mathcal F^\star-\mathcal B_u(x)\) for each of the two annihilated
colors in the equality control.  In both cases the restricted deletion
round sizes were

\[
16,\ 40,\ 56,\ 12.
\]

Every constructed trace stayed in \(\mathcal F^\star\), strictly decreased
rank until its final step, and ended in a retained banned state.

## 9. Proposition 5.2: terminal gates and diamonds

Write \(A=S-\{u\}\).  A final banned state is

\[
A\cup\{b\},\qquad b\in B_x.
\]

Because \(x\) is full here, \(B_x\cap S=\varnothing\), so \(b\notin A\).
The attacked vertex must be a member of the successor absent from the
predecessor.  There are exactly two cases.

1. If the attack is at \(b\), deleting \(b\) from the successor leaves
   \(A\), so the predecessor is \(A\cup\{q\}\) and the move is
   \(q\to b\).  Since the predecessor is not banned,
   \(q\notin B_x\).
2. If the attack is not at \(b\), it is one of the two anchors
   \(a\in A\).  Writing \(A=\{a,c\}\), the predecessor is
   \(\{c,b,q\}\) and the move is \(q\to a\).

These are mutually exclusive and exhaust all three successor vertices.
All attacks are unoccupied and all moves replace exactly one guard.

For a nonroot corridor, \(q\ne u\).  The four vertices \(x,u,q,b\) are
distinct, and the five required \(G\)-edges are:

\[
qb\quad\text{(the move)},\qquad
qx\quad(q\notin B_x),\qquad
ux\quad\text{(fullness)},
\]

\[
qu\quad\text{(the retained predecessor dominates \(u\))},\qquad
bu\quad\text{(the retained successor dominates \(u\))}.
\]

The sixth pair \(xb\) is a \(G\)-nonedge because \(b\in B_x\).  Thus the
induced graph is exactly \(K_4-xb\).

If \(q=u\), the predecessor is \(S\), and the statement now correctly says
only that this is a direct \(u\)-response.  It does not claim the response
list at \(b\) is a singleton.

As an exhaustive control, the clean-room checker examined every retained
one-guard transition from an allowed \(\mathcal F^\star\)-state into a
banned retained state for the two empty kernels of the equality graph:
31 terminal entries for each color, 62 total.  Every entry had one of the
two stated forms, and every nonroot corridor induced the claimed diamond.
The root-entry lists also reproduce why the original “singleton” wording
needed correction: all six checked direct-root entries had two-color
greatest-family lists.

## 10. Independent finite controls

The candidate control output is semantically identical to
`expected_result.json` after JSON parsing and normalization.  It is not
byte-identical because array formatting differs; the candidate manifest
does not claim byte equality.

The clean-room checker independently reconstructed:

### Equality control `Ksv\`f\knJVis`

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3),
\]

root \(\{1,2,3\}\), and full core \(\{0\}\).

- color \(1\): empty restricted kernel;
- color \(2\): empty restricted kernel;
- color \(3\): 64-state restricted kernel and one compatible coloring.

The direct domain-coloring count and independently generated 2-CNF count
both equal one in the surviving case.

### MMV-001 `IEhbtj{ro`

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4),
\]

root \(\{0,1,2\}\), full core \(\{8\}\), and all three restricted kernels
empty.

This is outside Theorem 2.1 because \(\gamma=2\).

### MMV-021 `JEhbtj{rv~?`

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4),
\]

root \(\{0,1,2\}\), full core \(\{8,10\}\), and all nine cumulative
assignments with empty kernels.  Nevertheless, target \(10\) individually
has a surviving 128-state kernel at color \(2\), while its target-fixed
coloring problem has no solution.

This confirms that one individually safe color does not imply a compatible
cumulative coloring.

The independent MMV catalog scan reproduced:

| quantity | count |
|---|---:|
| graphs with \(\alpha=3\) | 55 |
| full greatest-family incidences | 581 |
| individual color tests | 1,743 |
| unsafe colors | 1,688 |
| unsafe colors with nonempty restricted kernel | 0 |

These catalog counts remain experimental controls outside the
\(\gamma=3\) theorem and are not used in its proof.

## 11. Exact stopping boundary

The revised note states its limits correctly.  The package gives the exact
dichotomy:

- every proposed proper full-core assignment annihilates its cumulative
  kernel; or
- some cumulative kernel survives, but its ordinary exact residual 2-CNF
  may still be unsatisfiable.

It does not show that either obstruction is impossible.  In particular,
Theorem 4.2 is an exact characterization of \(\theta(G)=3\), not a proof
that its right-hand side follows from
\(\gamma=\alpha=\gamma^\infty=3\).

Subject to this strict scope, the revised theorem package is ready for
promotion.
