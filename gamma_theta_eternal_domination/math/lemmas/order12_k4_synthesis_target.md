# Exact order-12, parameter-four synthesis target

## Status and claim boundary

This note derives, from the one-guard-moves definition, an exact SAT target
for the **connected** \((n,k)=(12,4)\) slice and sound structural reductions
for later search.  The mathematical equivalences and counts below are
proved.  The proposed branch partition and resource gates have not yet been
implemented or certificate-audited.

Nothing here says that the target formula is satisfiable or unsatisfiable.
In particular, this note does not exclude the \((12,4)\) slice and does not
resolve the \(\gamma\)--\(\theta\) conjecture.

Throughout, \(G\) is a finite simple graph on 12 vertices,
\[
 H=\overline G,
\]
and \(e_{uv}=1\) means \(uv\in E(H)\).  Attacks are made only at
unoccupied vertices, and exactly one guard moves along one edge of \(G\) to
the attacked vertex.

## 1. Static complement characterization

### Theorem 1

The following are equivalent, up to relabeling the vertices.

1. \(\gamma(G)=\alpha(G)=4\).
2. In \(H\):

   - vertices \(0,1,2,3\) form a \(K_4\);
   - \(H\) has no \(K_5\); and
   - every three-set \(A\subseteq V(H)\) has a common \(H\)-neighbor
     outside \(A\).

**Proof.**  Suppose first that \(\gamma(G)=\alpha(G)=4\).  A maximum
independent four-set of \(G\) is a \(K_4\) in \(H\); relabel it as
\(\{0,1,2,3\}\).  The equality \(\alpha(G)=4\) says exactly that \(H\) has
no \(K_5\).

No three-set \(A\) dominates \(G\).  Thus some \(x\notin A\) is adjacent in
\(G\) to no member of \(A\), equivalently \(x\) is adjacent in \(H\) to all
three members of \(A\).

Conversely, the anchored \(K_4\) and absence of a \(K_5\) give
\(\alpha(G)=4\).  The common-neighbor condition says that no three-set
dominates \(G\).  Since domination is upward closed, no set of size at most
three dominates, so \(\gamma(G)\ge4\).  The anchored \(K_4\) is an
independent four-set of \(G\).  It is maximum, hence maximal independent,
and every maximal independent set dominates.  Therefore
\(\gamma(G)\le4\), proving \(\gamma(G)=4\). \(\square\)

For a conjectural parameter-four counterexample, equality collapse supplies
\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G).
\]
Consequently Theorem 1 loses no target.

The anchor is only a relabeling convention for one chosen maximum
independent set.  It is not a claim that a graph has a distinguished
four-set before relabeling.

## 2. Exact one-guard CNF

Let
\[
 \mathcal Q=\binom{V}{4}.
\]
The proposed exact formula uses four variable families.

| role | variables | count |
|---|---|---:|
| complement edges | \(e_{uv}\), \(u<v\) | \(\binom{12}{2}=66\) |
| common-neighbor witnesses | \(w_{A,x}\), \(|A|=3,\ x\notin A\) | \(\binom{12}{3}9=1,980\) |
| selected guard states | \(f_D\), \(D\in\mathcal Q\) | \(\binom{12}{4}=495\) |
| one-guard responses | \(m_{D,r,u}\), \(D\in\mathcal Q,\ r\notin D,\ u\in D\) | \(\binom{12}{4}8\cdot4=15,840\) |
| **total** |  | **18,381** |

The clauses are as follows.

### 2.1 Static clauses

1. **No \(K_5\).**  For every five-set \(B\),
   \[
     \bigvee_{\{u,v\}\in\binom B2}\neg e_{uv}.
   \tag{2.1}
   \]

2. **Every triple has a common neighbor.**  For every three-set \(A\),
   \[
     \bigvee_{x\notin A}w_{A,x},
   \tag{2.2}
   \]
   and, for \(a\in A\) and \(x\notin A\),
   \[
     \neg w_{A,x}\vee e_{ax}.
   \tag{2.3}
   \]

3. **Anchored \(K_4\).**  Append the six positive units
   \[
     e_{01},e_{02},e_{03},e_{12},e_{13},e_{23}.
   \tag{2.4}
   \]

4. **Connectedness of \(G\).**  For every nonempty proper
   \(S\subset V\) containing vertex \(0\),
   \[
     \bigvee_{\substack{u\in S\\v\notin S}}\neg e_{uv}.
   \tag{2.5}
   \]
   A negative \(H\)-edge literal is a crossing edge of \(G\), so these are
   exactly the usual cut clauses for connectedness of \(G\), not \(H\).

### 2.2 Eternal-family clauses

5. **Selected states dominate \(G\).**  For every \(D\in\mathcal Q\) and
   \(x\notin D\),
   \[
     \neg f_D\vee\bigvee_{u\in D}\neg e_{ux}.
   \tag{2.6}
   \]

6. **The family is nonempty.**
   \[
     \bigvee_{D\in\mathcal Q}f_D.
   \tag{2.7}
   \]

7. **One-guard closure.**  For \(D\in\mathcal Q\) and \(r\notin D\),
   \[
     \neg f_D\vee\bigvee_{u\in D}m_{D,r,u}.
   \tag{2.8}
   \]
   For every candidate moving guard \(u\in D\), put
   \[
     \neg m_{D,r,u}\vee\neg e_{ur}
   \tag{2.9}
   \]
   and
   \[
     \neg m_{D,r,u}\vee
     f_{(D-\{u\})\cup\{r\}}.
   \tag{2.10}
   \]

Clause (2.9) requires \(ur\notin E(H)\), equivalently
\(ur\in E(G)\).  Clause (2.10) changes only the named guard and selects the
resulting state.  The quantifier represented by (2.8)--(2.10) is exactly
\[
 \forall D\in\mathcal D\ \forall r\notin D\ \exists u\in D.
\]
Move variables attached to an unselected source may be set arbitrarily
without changing the projected family; setting them false gives a canonical
realization.

8. **Every \(H\)-\(K_4\) is selected.**  For every \(D\in\mathcal Q\),
   \[
     \left(
       \bigvee_{\{u,v\}\in\binom D2}\neg e_{uv}
     \right)\vee f_D.
   \tag{2.11}
   \]

This last family is redundant but sound.  A \(K_4\) in \(H\) is an
independent four-set in \(G\); no \(K_5\) makes it maximum.  Independent-set
forcing puts every such set in every eternal four-family.

### Theorem 2

The clauses (2.1)--(2.11) are satisfiable exactly when their decoded graph
is connected, satisfies
\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=4,
\]
and has the anchored \(H\)-\(K_4\).

**Proof.**  Given such a graph, Theorem 1 supplies every static clause.
Assign the \(w\)-variables using one actual common neighbor per triple.
Assign \(f_D\) from an actual nonempty eternal four-family, and choose one
legal response for every selected state and unoccupied attack.  The
independent-set-forcing lemma supplies (2.11).

Conversely, Theorem 1 gives \(\gamma(G)=\alpha(G)=4\).  Clauses
(2.6)--(2.10) project to a nonempty family of dominating four-sets closed
under every unoccupied attack by one guard moving along one \(G\)-edge.
Hence \(\gamma^\infty(G)\le4\).  The general inequality
\(\alpha(G)\le\gamma^\infty(G)\) gives equality.  Clauses (2.5) give
connectedness. \(\square\)

## 3. Exact anchored four-coloring bank

Since \(H\) contains the anchored \(K_4\), every proper four-coloring uses
four distinct colors on vertices \(0,1,2,3\).  Color names may therefore be
normalized uniquely by
\[
 c(0)=0,\quad c(1)=1,\quad c(2)=2,\quad c(3)=3.
\tag{3.1}
\]

For each of the \(4^8=65,536\) assignments of colors to vertices
\(4,\ldots,11\), append
\[
 C_c=\bigvee_{\substack{u<v\\c(u)=c(v)}}e_{uv}.
\tag{3.2}
\]
This clause is false exactly when \(c\) is a proper coloring of \(H\).
Conversely, every proper four-coloring of \(H\) has exactly one color
renaming satisfying (3.1).  Thus, relative to the anchored \(K_4\),
\[
 \bigwedge_c C_c
 \quad\Longleftrightarrow\quad
 \chi(H)>4
 \quad\Longleftrightarrow\quad
 \theta(G)\ge5.
\tag{3.3}
\]

The bank has exactly 65,536 clauses.  Every free vertex contributes one
same-color pair with its anchor.  A fixed pair of free vertices has the same
color in \(4^7\) assignments.  Therefore its exact literal count is
\[
 8\cdot4^8+\binom82\,4^7
 =524,288+458,752
 =983,040.
\tag{3.4}
\]

Combining this bank with Theorem 2 gives an exact, anchored, connected
\((12,4)\) counterexample formula.

## 4. Exact clause and literal census

The formula before the coloring bank has the following exact census.

| clause family | clauses | literals |
|---|---:|---:|
| no \(K_5\) | \(792\) | \(7,920\) |
| triple-witness existence | \(220\) | \(1,980\) |
| triple-witness implications | \(5,940\) | \(11,880\) |
| anchored \(K_4\) units | \(6\) | \(6\) |
| connected cuts | \(2,047\) | \(67,584\) |
| selected-state domination | \(3,960\) | \(19,800\) |
| family nonempty | \(1\) | \(495\) |
| legal-edge and successor implications | \(31,680\) | \(63,360\) |
| attack-response disjunctions | \(3,960\) | \(19,800\) |
| \(K_4\)-to-family strengthening | \(495\) | \(3,465\) |
| **base total** | **49,101** | **196,290** |

For the cut literals, each unordered vertex pair crosses exactly
\(2^{10}\) of the cuts represented by the side containing vertex \(0\), so
the total is
\[
 \binom{12}{2}2^{10}=67,584.
\]

The cumulative counts are:

| formula | variables | clauses | literals |
|---|---:|---:|---:|
| exact one-guard base | 18,381 | 49,101 | 196,290 |
| base plus complete anchored coloring bank | 18,381 | 114,637 | 1,179,330 |
| base, bank, and the \(S_8\) breaker below | 18,381 | 114,742 | 1,180,016 |

These are exact combinatorial counts for the proposed clause order, not
hashes of an implemented DIMACS file.  An implementation must reconstruct
and independently audit the actual bytes before any solve can support a
claim.

## 5. Sound \(S_8\) signature ordering

For an outer vertex \(v\in X=\{4,\ldots,11\}\), define its four-bit anchor
signature
\[
 s(v)=(e_{0v},e_{1v},e_{2v},e_{3v})
\]
in that coordinate order.  Let \(S_8\) require
\[
 s(4)\le_{\rm lex}s(5)\le_{\rm lex}\cdots\le_{\rm lex}s(11),
\tag{5.1}
\]
with \(0<1\).

Every permutation of \(X\), fixing the four anchor vertices, acts on all
edge, witness, family, and move variables.  It preserves every base clause.
It also preserves the complete coloring bank: permuting outer vertices maps
each normalized row to another normalized row with the same fixed anchor
colors.  Hence every model has an orbit representative satisfying (5.1).

For two four-bit signatures, forbid each unique first difference \(1,0\).
Writing the left and right signatures as
\(a=(a_0,\ldots,a_3)\) and \(b=(b_0,\ldots,b_3)\), the clause for first
difference \(t\) and common prefix \(p\in\{0,1\}^t\) is
\[
 \left(
   \bigvee_{\substack{q<t\\p_q=0}}(a_q\vee b_q)
 \right)
 \vee
 \left(
   \bigvee_{\substack{q<t\\p_q=1}}(\neg a_q\vee\neg b_q)
 \right)
 \vee\neg a_t\vee b_t.
\tag{5.2}
\]
It is false exactly when both signatures have prefix \(p\) and their first
difference is \(a_t=1,b_t=0\).
There are
\[
 \sum_{t=0}^3 2^t=15
\]
auxiliary-free clauses per adjacent comparator and
\[
 \sum_{t=0}^3 2^t(2t+2)=98
\]
literals.  Seven adjacent comparators therefore add exactly 105 clauses,
686 literals, and no variables, giving the final row of the census above.

This symmetry proof applies to the untemplated anchored formula and to any
additional constraint invariant under the full outer \(S_8\) action.  It
does **not** automatically apply after forcing one particular labeled SPGT
template.

## 6. SPGT reduction at parameter four

For a target graph,
\[
 \omega(H)=4<\chi(H),
\]
so \(H\) is imperfect.  By the Strong Perfect Graph Theorem, \(H\) contains
an induced odd hole or odd antihole.

### Lemma 3: odd-cycle value

For \(m\ge2\),
\[
 \gamma^\infty(C_{2m+1})=m+1.
\tag{6.1}
\]

**Proof.**  A partition into \(m\) edges and one singleton gives the upper
bound \(m+1\).  For the lower bound, suppose \(m\) guards suffice.  The
maximum independent set
\[
I=\{0,2,4,\ldots,2m-2\}
\]
must belong to every eternal \(m\)-family.  Attack vertex \(1\).  Moving the
guard at \(0\) leaves vertex \(2m\) undominated.  The only other possible
response moves the guard at \(2\), producing
\[
 \{0,1,4,6,\ldots,2m-2\}.
\]
For \(m=2\), this state is \(\{0,1\}\) and already leaves vertex \(3\)
undominated.  For \(m\ge3\), attack \(3,5,\ldots,2m-3\) in order.  At each
step, the only adjacent guard is the even guard immediately ahead, so the
response is forced.  The last forced move leaves
\[
 \{0,1,3,5,\ldots,2m-3\},
\]
which does not dominate vertex \(2m-1\).  Thus the last attack has no legal
dominating response, a contradiction.  Every attack used here is
unoccupied, and each proposed response moves only one adjacent guard.
\(\square\)

### Odd-antihole branch

An induced odd antihole \(\overline{C_{2q+1}}\) in \(H\) has clique number
\(q\), so \(q\le4\).  Its possible lengths are \(5,7,9\).

- The five-antihole is \(C_5\), already an odd hole.
- An induced \(\overline{C_9}\) in \(H\) induces \(C_9\) in \(G\).
  Lemma 3 and induced-subgraph monotonicity give
  \(\gamma^\infty(G)\ge5\), contradicting the target value four.
- The induced \(\overline{C_7}\) branch is not eliminated:
  its complement induces \(C_7\), whose one-guard eternal number is exactly
  four.

Thus the only additional antihole template is
\(\overline{C_7}\).

### Lemma 4: excluding an induced \(C_{11}\) in \(H\)

Under the triple-common-neighbor condition of Theorem 1, \(H\) has no
induced \(C_{11}\).

**Proof.**  Suppose the rim is
\(v_0v_1\ldots v_{10}v_0\), and let \(x\) be the sole vertex outside it.
Apply the triple-common-neighbor condition to
\(\{x,v_0,v_3\}\).  Any common neighbor must be a rim vertex adjacent to
both \(v_0\) and \(v_3\).  No such rim vertex exists in an induced cycle:
vertices at cycle distance three have no common rim neighbor.  The only
outside vertex is already in the triple and cannot be its own neighbor.
This is a contradiction. \(\square\)

Consequently, every target complement contains at least one of the four
possibly overlapping templates
\[
 C_5,\qquad C_7,\qquad C_9,\qquad\overline{C_7}.
\tag{6.2}
\]

Unlike the parameter-three case, these holes are **not** known to be
hub-free.  Indeed, the complement of an odd wheel is
\(K_1\mathbin{\dot\cup}\overline{C_{2q+1}}\), whose one-guard eternal
number is \(1+3=4\).  The parameter-three odd-wheel contradiction therefore
does not carry over, and no no-hub clauses may be added here.

## 7. The anchor/template orbit-intersection caveat

It is unsound to fix the \(K_4\) at vertices \(0,1,2,3\) and independently
fix an SPGT witness at a second preferred list of labels merely because
each object can separately be relabeled there.  The intersection size and
incidence pattern of a chosen \(K_4\) and chosen hole or antihole are
invariants of the pair.  The two separate relabelings need not be
simultaneously realizable.  For example, forcing four consecutive vertices
of an induced hole also to be the anchored \(K_4\) is immediately
inconsistent, even though a target may contain both objects elsewhere.

Any template refinement must therefore use one of the following sound
routes.

1. Keep the anchored formula and encode the **existence** of a template over
   all labeled vertex subsets and cyclic orders, preserving the outer
   \(S_8\) action.
2. Enumerate all orbits of pairs \((A,T)\), where \(A\) is a chosen
   \(H\)-\(K_4\) and \(T\) is a chosen SPGT witness, under the full vertex
   action.  Supply a separate coverage proof and manifest for every
   intersection/incidence orbit.
3. Fix the template first and encode existence of an \(H\)-\(K_4\) with
   selector variables, rather than fixing its labels independently.
4. Do not force a template in the SAT formula; use (6.2) only for
   post-model classification or sound learned cuts.

Until an orbit-intersection coverage proof exists, a single formula with
both independently chosen labeled anchors is heuristic only and cannot
support a negative finite claim.  Likewise, the full \(S_8\) breaker must be
replaced by the stabilizer of a fixed pair \((A,T)\), or re-proved for an
invariant template-existence encoding.

## 8. Connectedness scope

The exact formula above is a connected target.  Connected reduction by
itself does not prove that every order-12 parameter-four counterexample is
connected.

Indeed, let the components of a parameter-four counterexample have
\[
 a_j=\gamma(G_j),\quad b_j=\gamma^\infty(G_j),\quad
 c_j=\theta(G_j).
\]
Additivity and equality of the total \(\gamma\) and \(\gamma^\infty\)
force \(a_j=b_j\) componentwise.  At least one component is a
counterexample, and every counterexample has parameter at least three.
There are exactly two possibilities.

1. The counterexample component has parameter four.  It consumes the whole
   domination budget, so the original graph is connected.
2. The counterexample component has parameter three.  The remaining
   domination budget is one, so there is exactly one other component, with
   \(\gamma=\gamma^\infty=1\).  The parameter chain gives
   \(\alpha=1\), hence this other component is a complete graph \(K_t\).

Conversely, the disjoint union of a parameter-three counterexample \(Q\)
and \(K_t\) is a parameter-four counterexample by additivity.  Therefore the
full disconnected \((12,4)\) slice is covered only after separately
excluding parameter-three counterexamples on orders \(12-t\), \(t\ge1\),
or after importing an accepted theorem/certificate that does so.  The
order-12, parameter-three result alone does not discharge these smaller
orders.

## 9. M1 Pro partition and resource gates

The following are proposed execution gates, not mathematical results.

1. **Byte-construction gate.**  Independently reconstruct the variable map,
   all 49,101 base clauses, the 65,536-row bank, and the 105-clause
   comparator suffix.  Require exact hashes and exhaustive comparator
   truth tables before any solver run.
2. **Semantic gate.**  Independently decode SAT models and verify
   Theorem 1, connectedness, \(\theta(G)\ge5\), and the complete
   one-guard family directly.  Inject occupied-attack, all-guards,
   \(G/H\)-sign, and missing-successor faults and require rejection.
3. **Pilot gate.**  On the 16-GB M1 Pro, run at most one solver or checker
   child at a time.  A first exploratory run should be deterministic,
   proof-free, bounded by 600 wall seconds and 4 GiB address space, and
   leave at least 4 GiB of disk free.  An exploratory `UNSAT` is a
   nonclaim.
4. **Partition gate.**  If the parent formula does not terminate in the
   pilot budget, use the proved \(S_8\) ordering and split on the minimum
   outer signature \(s(4)\).  The value \(1111\) is impossible because it
   would extend the anchored \(K_4\) to a \(K_5\).  The other 15 four-bit
   values therefore give 15 disjoint, exhaustive cubes.  If a cube remains
   too large, refine by the maximum signature \(s(11)\); the ordered
   minimum/maximum pairs from those 15 values give at most
   \(\binom{16}{2}=120\) disjoint cases.  Record every cube, formula hash,
   and parent-coverage identity in a resumable manifest.
5. **Certificate gate.**  Run only one memory-heavy proof producer or
   checker, keep its address-space cap at or below 4 GiB, cap each initial
   proof artifact at 512 MiB, and preflight both that cap and a 4-GiB free
   disk reserve.  Exceeding a cap triggers finer partitioning, not a
   conclusion.
6. **Promotion gate.**  Every UNSAT leaf needs a warning-fatal,
   proof-producing replay and an independent checker.  A separate coverage
   audit must prove that the accepted leaves exhaust the parent formula.
   SAT candidates must be checked against the unrestricted anchored target.

These caps deliberately leave substantial memory for macOS and concurrent
lightweight research.  They may be lowered if the live machine reports less
headroom; they must not be raised past the campaign's 75-percent physical
memory ceiling merely to avoid partitioning.

## 10. Precisely delimited next claim

After independent implementation audit, the only immediate proved
computational target would be:

> A satisfying assignment of the exact anchored formula is equivalent, up
> to relabeling one maximum independent four-set, to a connected 12-vertex
> graph satisfying
> \(\gamma=\alpha=\gamma^\infty=4<\theta\).

No negative \((12,4)\) claim is available unless the untemplated parent
formula, or a mathematically complete and certificate-backed partition of
it, is checked UNSAT.
