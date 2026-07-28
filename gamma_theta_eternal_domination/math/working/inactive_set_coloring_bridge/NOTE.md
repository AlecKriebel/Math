# The inactive-set coloring bridge at \(k=3\)

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** model.  It does not resolve
the \(\gamma\)--\(\theta\) conjecture or the complete \(k=3\) case.

The proved conclusions are:

1. for every deletion three-coloring, a ridge component's responder-color
   set is exactly the complement of the colors used by inactive vertices
   in that component's support;
2. globally,
   \[
      \boxed{\displaystyle
      \bigcap_C A_C^\kappa
      =\{1,2,3\}\setminus\kappa(R)};
   \]
3. the common-responder-color target is therefore exactly a proper
   three-coloring of \(H'=\overline{G-x}\) using at most two colors on
   \(R\);
4. \(H'[R]\) is always triangle-free, and a successful coloring would in
   particular make \(H'[R]\) bipartite;
5. equality, well-coveredness, a full static target, all one-step
   domination checks, and exact ridge covariance still do not force the
   desired coloring.  An explicit 12-vertex control satisfies
   \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4)
   \]
   and fails **only** at multi-step eternal closure.

No actual full-target eternal-family countercontrol was found.  The final
gap therefore remains genuinely dynamic.

## 1. Setup

Assume the equality-critical deletion branch

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=\theta(G-x)=3.
\tag{1.1}
\]

Let \(\mathcal F\) be an eternal family of triples of \(G\), and assume
that every maximum independent triple avoiding \(x\) belongs to
\(\mathcal F\).  This last assertion is the accepted
maximum-independent-state theorem.

Put

\[
 H'=\overline{G-x}.
\]

For a maximum independent triple \(T\) avoiding \(x\), let

\[
 L_T(x)=
 \{v\in T:vx\in E(G),\ T-v+x\in\mathcal F\}.
\tag{1.2}
\]

Eternal closure makes \(L_T(x)\) nonempty.  The literal two-attack argument
below makes the physical active set well-defined:

\[
 A_x=\{v\ne x:v\in L_T(x)
                  \text{ for some maximum independent }T\ni v\},
\qquad
 R=V(G-x)\setminus A_x.
\tag{1.3}
\]

### Lemma 1.1 (vertex-star propagation)

If maximum independent triples \(T,T'\) avoiding \(x\) both contain
\(v\), then

\[
 v\in L_T(x)\iff v\in L_{T'}(x).
\tag{1.4}
\]

#### Proof

Suppose first that

\[
 T=\{v,u,p\},\qquad T'=\{v,u,q\}.
\]

From \(v\in L_T(x)\), the state \(\{u,p,x\}\) is retained.  Attack \(q\).
The guard \(u\) is nonadjacent to \(q\).  Moving \(x\) would leave
\(\{u,p,q\}\), which misses \(v\), since all three vertices are
nonadjacent to \(v\).  Closure therefore forces \(p\to q\), retaining
\(\{u,q,x\}=T'-v+x\).

Now suppose that

\[
 T=\{v,a,b\},\qquad T'=\{v,p,q\}
\]

share only \(v\).  From the retained state \(\{a,b,x\}\), attack \(p\).
The guard \(x\) cannot answer because \(\{a,b,p\}\) misses \(v\).
After relabeling \(a,b\), closure retains \(\{b,p,x\}\).  Attack \(q\).
The guard \(p\) is nonadjacent to \(q\), and moving \(x\) would leave
\(\{b,p,q\}\), again missing \(v\).  Thus \(b\to q\), retaining
\(\{p,q,x\}=T'-v+x\).  Symmetry gives the reverse implication. \(\square\)

Consequently

\[
 L_T(x)=T\cap A_x\ne\varnothing
\tag{1.5}
\]

for every maximum independent triple \(T\) avoiding \(x\).

Let \(\Gamma_x\) be the graph on these triples, adjacent when two triples
share two vertices.  Its connected components are called ridge
components.  Fix a proper three-coloring

\[
 \kappa:V(H')\to\{1,2,3\}.
\]

Every triangle of \(H'\) is rainbow.  If \(C\) is a ridge component, put

\[
 A_C^\kappa=\kappa(T\cap A_x),\qquad T\in C.
\tag{1.6}
\]

This is independent of \(T\).  Indeed, if
\(T=\{u,v,p\}\) and \(T'=\{u,v,q\}\), vertex-star propagation fixes the
status of \(u,v\), while

\[
 T-p+x=T'-q+x=\{u,v,x\}
\]

shows that \(p\) and \(q\) have the same active status.  They also have
the same color, because \(u,v\) already use the other two colors.

## 2. Exact component and global identities

Write \(\operatorname{supp}(C)\) for the union of the triples in \(C\).

### Theorem 2.1 (exact component identity)

For every ridge component \(C\),

\[
 \boxed{
 A_C^\kappa
 =
 \{1,2,3\}\setminus
 \kappa\bigl(R\cap\operatorname{supp}(C)\bigr).
 }
\tag{2.1}
\]

#### Proof

If \(c\in A_C^\kappa\), take any support vertex \(r\) of color \(c\) and
a facet \(T\in C\) containing it.  Componentwise constancy says that the
unique \(c\)-colored vertex of \(T\), namely \(r\), is active.  Thus no
such \(r\) lies in \(R\).

Conversely, if color \(c\) is absent from
\(R\cap\operatorname{supp}(C)\), the unique \(c\)-colored vertex of any
\(T\in C\) is active.  Hence \(c\in A_C^\kappa\). \(\square\)

The parameter chain applied to (1.1) gives

\[
 i(G-x)=\alpha(G-x)=3.
\tag{2.2}
\]

Every vertex extends to a maximal independent set, and every such set has
size three by (2.2).  Therefore every vertex of \(H'\) lies in the support
of at least one ridge component.

### Corollary 2.2 (exact global identity)

\[
 \boxed{
 \bigcap_C A_C^\kappa
 =
 \{1,2,3\}\setminus\kappa(R).
 }
\tag{2.3}
\]

#### Proof

Intersect (2.1) over all components and use that their supports cover
\(V(H')\). \(\square\)

Thus a common responder color exists if and only if

\[
 |\kappa(R)|\le2.
\tag{2.4}
\]

When \(w\notin\kappa(R)\), every \(w\)-colored vertex is active and hence
adjacent to \(x\) in \(G\).  Giving \(x\) color \(w\) therefore extends
\(\kappa\) to a proper coloring of \(\overline G\).  The precise
active-set target is consequently:

> Find a proper three-coloring of \(H'\) whose restriction to \(R\) uses
> at most two colors.

This is a sufficient extension mechanism.  It is not claimed to be the
only way that a positive graph with \(\theta(G)=3\) can be colored, because
a dynamically inactive vertex can still be adjacent to \(x\) in \(G\).

## 3. Rigorous consequences

### Proposition 3.1 (the inactive graph is triangle-free)

\[
 \boxed{\omega(H'[R])\le2.}
\tag{3.1}
\]

Equivalently,

\[
 \alpha((G-x)[R])\le2.
\tag{3.2}
\]

#### Proof

A triangle of \(H'\) is a maximum independent triple of \(G-x\).
Equation (1.5) says that it contains an active response to the attack at
\(x\).  It therefore cannot lie entirely in \(R\). \(\square\)

In particular, a successful coloring makes \(H'[R]\) two-colorable, so

\[
 H'[R]\text{ bipartite}
\tag{3.3}
\]

is necessary.  It is not by itself sufficient: vertices outside \(R\) can
force all three colors to occur on a bipartite induced subgraph.

There is also an exact local description of every inactive edge.  The
static characterization of \(\gamma(G-x)=\alpha(G-x)=3\) says that every
pair of vertices has a common neighbor in \(H'\).  Hence every edge
\(uv\in E(H'[R])\) lies in a triangle \(\{u,v,a\}\).  Proposition 3.1
forces \(a\in A_x\), and the ridge component containing this triangle has
the singleton responder-color set consisting of \(\kappa(a)\).

If the active-set route fails in a hypothetical counterexample, then for
**every** proper deletion coloring,

\[
 \kappa(R)=\{1,2,3\}.
\tag{3.4}
\]

Thus \(R\) is a rainbow transversal for every deletion coloring, even
though it contains no triangle.

## 4. A sharp static boundary control

The following control shows why (3.4) cannot be contradicted using only
static equality, one-step domination, facet hitting, and ridge covariance.

Let \(H'\) have vertex set \(\{0,\ldots,10\}\) and edge set

```text
01 04 07 08 12 17 1A 23 26 28 29 2A
34 35 3A 45 48 56 57 67 69 89
```

where `A` denotes vertex \(10\).  A proper three-coloring has parts

\[
 \{0,2,5\}\mid\{1,3,6,8\}\mid\{4,7,9,10\}.
\tag{4.1}
\]

Put

\[
 A=\{5,6,7,8,9,10\},
\qquad
 R=\{0,1,2,3,4\}.
\tag{4.2}
\]

The induced graph \(H'[R]\) is exactly

\[
 0\,1\,2\,3\,4\,0\cong C_5.
\tag{4.3}
\]

The eight triangles of \(H'\) are

\[
\begin{array}{c}
017,\ 048,\ 12A,\ 23A,\ 269,\ 289,\ 345,\ 567.
\end{array}
\tag{4.4}
\]

Their ridge components, in the order displayed, are

\[
 \{017\},\ \{048\},\ \{12A,23A\},\
 \{269,289\},\ \{345\},\ \{567\}.
\tag{4.5}
\]

The active-color set is constant on each component.  The last component
contains the full active state

\[
 S=\{5,6,7\}.
\tag{4.6}
\]

Every pair of vertices of \(H'\) has a common neighbor.  Since \(H'\) is
three-colorable and contains a triangle, for

\[
 G'=\overline{H'}
\]

the exact parameter chain collapses to

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G')
 =(3,3,3,3,3).
\tag{4.7}
\]

The labeled graph6 string is

```text
JUZeppVvS^_
```

Now add a target \(x=11\) adjacent in the complement to every vertex of
\(R\) and to no vertex of \(A\), and put \(G=\overline H\).  Thus the only
guards physically able to move to \(x\) are the vertices of \(A\).
For every triangle \(T\) in (4.4), the exact static response list is

\[
 L_T^{\rm static}(x)=T\cap A.
\tag{4.8}
\]

Every successor in (4.8) dominates \(G\), and (4.6) has a full static
response list.  Hence this graph passes every one-step response test used
to define the proposed active pattern.

The subgraph \(H[R\cup\{x\}]\) is the join \(x\vee C_5\), so
\(\chi(H)\ge4\).  A fourth color on \(x\) extends (4.1), giving equality.
Exact evaluation yields

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G)
 =(3,3,3,4,4).
 }
\tag{4.9}
\]

Its labeled graph6 string is

```text
KUZeppVvS^_~
```

The greatest eternal triple-family is empty, while the greatest eternal
four-family has 427 states.  Thus this is **not** a counterexample.  It
fails precisely because the statically legal responses cannot be closed
under arbitrary future attacks.

The standalone verifier reconstructs both graphs, exhaustively evaluates
all five parameters, enumerates all 12 deletion three-colorings, checks
the static lists, checks ridge covariance, and replays the greatest fixed
points:

```text
python3 verify_control.py
```

Its output is `control_result.json`, whose SHA-256 is

```text
1a891b0e65fd8ef363007869ad3797191b8fca96912e11a1b41ab02d82fd2faa
```

## 5. Bounded dynamic attempt and remaining gap

Two bounded exploratory searches were made.

1. Random explicitly three-clique-coverable equality graphs with balanced
   color classes of sizes \(3,3,3\) and \(4,4,4\) were tested for an actual
   greatest-family full target whose physical inactive set uses all three
   colors in every deletion coloring.
2. Proper subfamilies were sought by banning all target-successor states
   for one selected vertex of each planted color and recomputing the
   greatest restricted kernel.  At least 70,000 deterministic random
   tripartite candidates were screened in this second exploratory lane;
   only candidates passing the exact equality filters were searched for
   the required family.

No actual eternal-family control was found.  These searches are
`OBSERVED`, not exhaustive finite results.

The sharp control (4.9) says exactly what a proof must add:

> use multi-step one-guard closure to rule out a covariant inactive odd
> cycle, or more generally to force a deletion coloring that omits one
> color on \(R\).

Triangle-freeness alone cannot do this, and the active-set target should
not be replaced by the weaker assertion that \(H'[R]\) is bipartite.
