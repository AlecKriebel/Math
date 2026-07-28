# Free singleton components are family-saturated and polarized

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{u,d,e\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(x\notin S\), write

\[
 L(x)=\{a\in S:S-a+x\in\mathcal F\}.
\tag{0.1}
\]

Fix the frozen-\(u\) projection

\[
 Q_u=G[(S-\{u\})\cup W_u],
 \qquad
 W_u=\{x\notin S:u\notin L(x)\},
\tag{0.2}
\]

and its projected pair-family

\[
 \mathcal P_u
 =
 \{A\in {V(Q_u)\choose2}:\{u\}\cup A\in\mathcal F\}.
\tag{0.3}
\]

The accepted frozen-projection theorem says that \(\mathcal P_u\) is an
eternal family of pairs.  In the \(k=3\) equality setting,

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\tag{0.4}
\]

the accepted parameter-two theorem makes

\[
 B_u=\overline{Q_u}
   =H[(S-\{u\})\cup W_u]
\tag{0.5}
\]

bipartite.

Suppose a singleton marker

\[
 L(s)=\{d\}
\tag{0.6}
\]

lies in a **free** component \(K\) of \(B_u\), meaning that \(K\) is
different from the component containing the anchor edge \(de\).

The new conclusions are:

1. **PROVED:** the singleton marker polarizes the whole component.
   Every vertex on the side of \(s\) has \(d\) in its response list, and
   every vertex on the opposite side has \(e\) in its response list.
2. **PROVED:** every complement edge \(xy\) of \(K\) lifts to the retained
   triple
   \[
     \{u,x,y\}\in\mathcal F.
   \]
   Thus every internal edge of a physical unit-supporting connector is a
   literal family transition, not merely a graph edge whose corresponding
   state might be dynamically absent.
3. **PROVED:** every singleton marker in \(K\) agrees with one common
   orientation: markers on the side of \(s\) have list \(\{d\}\), while
   markers on the opposite side have list \(\{e\}\).  Hence contradictory
   free units on one projection variable are impossible.
4. **EXACT SHARP CONTROL:** the equality graph `FCZbg` has two free
   singleton incidences in one two-vertex component.  Their demands are
   opposite and parity-compatible, and its unique complement edge lifts
   to the predicted retained triple.

Consequently the zero-binary-clause case of the C-075 two-unit chain is
empty in the C-119/C-120 singleton regime.  Every remaining one-unit
lollipop or two-unit chain must cross at least one genuine binary clause
between distinct free projection variables.

This is a strict reduction, not a proof that arbitrary cross-component
one-/two-unit chains are impossible.  It does not eliminate a separated
mixed \(P_4\), a longer lollipop, a residual bicycle, the full-list branch,
the complete \(k=3\) case, or the universal gamma--theta conjecture.

No literature-priority claim is made.

## 1. The pair transversal fact

We restate the accepted C-120 lemma in the exact form used below.

### Lemma 1.1 (retained pairs cross a complement component)

Let \(J\) be a graph whose complement is bipartite, and let
\(\mathcal P\) be an eternal family of dominating pairs in \(J\).
If a retained pair lies in one connected component of \(\overline J\),
then its two vertices occupy opposite bipartition sides.

#### Proof

Suppose not, and choose a retained same-side pair \(x,y\) for which a
shortest complement path

\[
 x=v_0,v_1,\ldots,v_{2r}=y
\tag{1.1}
\]

has minimum positive even length.

If \(r=1\), the pair does not dominate \(v_1\) in \(J\), because both
incident edges in (1.1) belong to \(\overline J\).

If \(r\ge2\), attack the unoccupied vertex \(v_2\).  The successor
\(\{x,v_2\}\) does not dominate \(v_1\), while
\(\{v_2,y\}\) is a retained same-side pair joined by a shorter even
complement path.  The first successor is invalid and the second
contradicts minimality.  Hence the attack has no retained response.
Both cases contradict eternity. \(\square\)

The proof uses domination of retained states and exactly-one-guard
closure.  It needs neither \(\gamma(J)=2\) nor connectedness of
\(\overline J\).

## 2. Free-component polarization

Fix the bipartition

\[
 V(K)=K_0\mathbin{\dot\cup}K_1
\]

so that

\[
 s\in K_0.
\tag{2.1}
\]

Because \(K\) and the anchor component of \(B_u\) are distinct, there is
no complement edge between them.  Therefore every vertex of \(K\) is
adjacent in \(G\) to both \(d\) and \(e\).

The singleton response (0.6) gives

\[
 \{e,s\}\in\mathcal P_u,
\qquad
 \{d,s\}\notin\mathcal P_u.
\tag{2.2}
\]

Indeed, the lifted states are respectively

\[
 \{u,e,s\}=S-d+s\in\mathcal F,
\qquad
 \{u,d,s\}=S-e+s\notin\mathcal F.
\]

### Theorem 2.1 (free singleton component polarization)

For every \(x\in V(K)\),

\[
\begin{array}{c|c|c}
\text{side of }x&\text{retained projected pair}&\text{list consequence}\\
\hline
x\in K_0&\{e,x\}\in\mathcal P_u&d\in L(x),\\
x\in K_1&\{d,x\}\in\mathcal P_u&e\in L(x).
\end{array}
\tag{2.3}
\]

#### Proof

Let

\[
 s=v_0,v_1,\ldots,v_m=x
\tag{2.4}
\]

be a shortest path in \(K\).

First suppose \(m=2r\) is even.  We prove inductively that

\[
 \{e,v_{2j}\}\in\mathcal P_u
 \qquad(0\le j\le r).
\tag{2.5}
\]

The case \(j=0\) is (2.2).  From
\(\{e,v_{2j}\}\), attack the unoccupied vertex \(v_{2j+2}\).
Both guards are adjacent to the attacked vertex in \(Q_u\):

- \(e\) lies in the different anchor component of \(B_u\); and
- \(v_{2j},v_{2j+2}\) lie on the same bipartition side, so they cannot
  be adjacent in the bipartite complement.

Moving \(e\) would produce the same-side pair
\(\{v_{2j},v_{2j+2}\}\), which Lemma 1.1 forbids.  Closure therefore
forces \(v_{2j}\to v_{2j+2}\), retaining
\(\{e,v_{2j+2}\}\).  This proves (2.5), and hence
\(\{e,x\}\in\mathcal P_u\).

Now suppose \(m=2r+1\) is odd.  Attack \(v_1\) from the retained pair
\(\{e,s\}\).  The guard at \(s\) cannot move because
\(sv_1\in E(B_u)\), while \(e\) is adjacent in \(Q_u\) to \(v_1\).
Thus closure uniquely retains

\[
 \{s,v_1\}\in\mathcal P_u.
\tag{2.6}
\]

Attack the unoccupied anchor \(d\) from (2.6).  Both component vertices
are adjacent to \(d\) in \(Q_u\).  Moving \(v_1\) would give the absent
pair \(\{d,s\}\) from (2.2), so closure forces

\[
 \{d,v_1\}\in\mathcal P_u.
\tag{2.7}
\]

Apply the even two-step induction from (2.5), with \(d,v_1\) in place
of \(e,s\).  It gives

\[
 \{d,v_{2j+1}\}\in\mathcal P_u
 \qquad(0\le j\le r),
\]

and therefore \(\{d,x\}\in\mathcal P_u\).

Finally, lifting the two projected pairs gives

\[
 \{u,e,x\}=S-d+x\in\mathcal F
 \quad\Longleftrightarrow\quad d\in L(x),
\]

\[
 \{u,d,x\}=S-e+x\in\mathcal F
 \quad\Longleftrightarrow\quad e\in L(x).
\]

This proves the list consequences in (2.3). \(\square\)

The proof is length-independent.  It does not infer a graph nonedge from
a missing family response: every graph adjacency used above follows
either from separation of complement components or from equality of
bipartition sides.

## 3. Every complement edge is a retained state

### Theorem 3.1 (family saturation of a pinned component)

For every edge

\[
 xy\in E(B_u[K]),
\tag{3.1}
\]

one has

\[
 \boxed{\{x,y\}\in\mathcal P_u}
\tag{3.2}
\]

and hence

\[
 \boxed{\{u,x,y\}\in\mathcal F.}
\tag{3.3}
\]

#### Proof

The edge \(xy\) joins opposite bipartition sides.  Suppose first that
\(x\in K_0\).  Theorem 2.1 gives
\(\{e,x\}\in\mathcal P_u\).  Attack \(y\).  The guard at \(x\) cannot
move because \(xy\in E(B_u)\), while \(e\) is adjacent in \(Q_u\) to
every vertex of the free component \(K\).  The unique response is
\(e\to y\), giving (3.2).

If \(x\in K_1\), use the retained pair \(\{d,x\}\) instead.  The same
argument forces \(d\to y\).  Lifting (3.2) through (0.3) gives (3.3).
\(\square\)

Thus a path used to support a free singleton unit has literal retained
edge-pairs at every step.  This is stronger than knowing only that the
path lies in a frozen bipartite projection.

## 4. Consequences for the response 2-CNF

### Corollary 4.1 (all singleton pins in one component agree)

If \(t\in K\) has a singleton list, then

\[
 L(t)=
 \begin{cases}
  \{d\},&t\in K_0,\\
  \{e\},&t\in K_1.
 \end{cases}
\tag{4.1}
\]

#### Proof

Theorem 2.1 puts \(d\) in \(L(t)\) on \(K_0\) and \(e\) in \(L(t)\)
on \(K_1\).  A singleton list contains exactly one color. \(\square\)

### Corollary 4.2 (the zero-clause two-unit terminal is empty)

In the C-119/C-120 no-full singleton regime, two free singleton units on
the same projection variable cannot demand opposite Boolean values.
Therefore the length-zero two-unit chain in the C-075 terminal
trichotomy cannot occur.

Every remaining unit contradiction contains at least one genuine
cross-type binary clause between distinct free variables.

#### Proof

A projection flip variable is the orientation of one free bipartite
component.  Corollary 4.1 says that every singleton marker in that
component demands the same orientation.  Hence its unit equations are
identical after parity is included, never contradictory.

C-120 says every cross-type collision clause has two distinct free
projection variables.  With the zero-clause unit collision removed, a
remaining unit contradiction must traverse at least one such clause.
\(\square\)

This corollary does not shorten an arbitrary clause path.  In particular,
one must still preserve the original complement edges supporting every
implication before applying a one-guard attack.

## 5. Exact equality control

The connected graph

```text
FCZbg
```

has order seven, size ten, and

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{5.1}
\]

Its greatest eternal triple-family has eighteen states and satisfies all

\[
 18(7-3)=72
\]

unoccupied attack obligations.  At the independent reference state

\[
 S=\{3,4,5\},
\]

the exact family-response lists are

\[
 L(0)=\{3\},\qquad
 L(1)=L(2)=\{4,5\},\qquad
 L(6)=\{5\}.
\tag{5.2}
\]

In the projection frozen at \(u=4\), the component

\[
 K=\{0,6\}
\tag{5.3}
\]

is disjoint from the anchor component \(\{3,5\}\), and

\[
 06\in E(H).
\]

The two singleton markers lie on opposite sides and demand the two
opposite anchor colors:

\[
 L(0)=\{3\},\qquad L(6)=\{5\}.
\]

The predicted edge-pair lift is present:

\[
 \{0,4,6\}\in\mathcal F.
\tag{5.4}
\]

Thus free singleton components genuinely occur under full equality, and
opposite singleton colors can genuinely share one component.  What the
theorem forces is parity coherence, not anchor-fixity or a single
singleton per component.

## 6. Discovery boundary

Two bounded discovery probes were used only to test stronger statements.

1. A direct same-marker two-arm encoding showed the parity pattern
   expected from a stronger attack theorem through both path lengths six:
   all tested cases with an even arm were UNSAT, while all odd/odd cases
   were SAT.  No proof logs or all-length proof were produced, so this is
   **OBSERVED**, not a claim.
2. Direct arbitrary-family synthesis found no gamma-three realization of
   the exact mixed family-list \(P_4\) at the tested orders
   \(12,13,14,15,16,18,20\).  These were discovery solver outputs without
   a coverage theorem or retained proof certificates.  They are not
   finite exclusions.

One CEGAR leaf at order twenty was terminated after the imposed
ten-minute discovery cap and remains **TIMEOUT/OBSERVED**.

The next theorem-grade target is therefore precise:

> propagate Theorems 2.1 and 3.1 through the first genuine cross-type
> clause, preserving its literal supporting edge, and prove an
> all-length two-arm parity theorem; or exhibit an equality control where
> that propagation fails.

Nothing in this section is used to prove Sections 1--5.

## 7. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/free_unit_chain_attack/verify.py \
  --check math/working/free_unit_chain_attack/controls.json
```

The verifier imports no campaign module.  It decodes `FCZbg`, recomputes
all five parameters and the greatest eternal triple-family, replays every
one-guard obligation, reconstructs the exact response lists and all three
frozen bipartite projections, and checks the polarization and
edge-saturation conclusions at every free singleton incidence in the
control.

