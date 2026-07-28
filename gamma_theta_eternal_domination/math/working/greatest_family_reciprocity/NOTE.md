# Greatest-family complementary-exchange reciprocity

## Status and exact boundary

Date: 2026-07-28 (PDT)

The proposed equality theorem remains **OPEN**:

> If
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=k\), must complementary
> exchanges between two maximum independent \(k\)-sets be reciprocal in
> the greatest eternal \(k\)-family?

No proof of that statement and no equality countermodel was found here.
The universal gamma--theta conjecture is not resolved.

This checkpoint does establish three useful facts.

1. It separates pairwise reciprocity, mutual base exchange, and matroid
   basis exchange precisely; these are not interchangeable.
2. It proves that the proposed reciprocity theorem would make the
   family-relative active-response relation of C-108 undirected.
3. It gives an exact eight-vertex countermodel showing that **greatestness
   alone is insufficient**.  The missing hypothesis is
   \(\gamma=\alpha\): the countermodel has
   \[
   (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
   \]

The equality hypothesis must therefore do genuine mathematical work in any
proof.  Replacing an arbitrary eternal family by the greatest family does
not by itself establish reciprocity.

## 1. Three different exchange properties

Let \(\mathcal K\) be the greatest eternal \(k\)-family and let \(S,T\)
be independent \(k\)-sets.  Put

\[
 A=S-T,\qquad B=T-S.
\]

Define the directed one-step relation

\[
 E_{S,T}=\{(u,x)\in A\times B:S-u+x\in\mathcal K\}.
\tag{1.1}
\]

Its reverse-direction counterpart, written on the same bipartition, is

\[
 E^{\leftarrow}_{S,T}
 =\{(u,x)\in A\times B:T-x+u\in\mathcal K\}.
\tag{1.2}
\]

The following properties have different strengths.

### Pairwise complementary-exchange reciprocity

\[
 \boxed{E_{S,T}=E^{\leftarrow}_{S,T}.}
\tag{PR}
\]

This asks for **every** directed exchange to be reversible at the
complementary state.  This is the statement tested in this checkpoint.

### Mutual matching and family base orderability

A **mutual matching** is a perfect matching contained in

\[
 E_{S,T}\cap E^{\leftarrow}_{S,T}.
\tag{1.3}
\]

This only asks for one reciprocal partner per member of \(A\), not for all
edges to be reciprocal.

A **family base ordering** is a bijection \(\phi:A\to B\) such that

\[
 (S-U)\cup\phi(U)\in\mathcal K
 \qquad\text{for every }U\subseteq A.
\tag{1.4}
\]

Every family base ordering supplies a mutual matching: the singleton
choice \(U=\{u\}\) gives \(S-u+\phi(u)\), while the complementary choice
\(U=A-\{u\}\) gives \(T-\phi(u)+u\).  The converse need not follow when
\(|A|\ge4\), because (1.3) controls only the first and last nontrivial
levels of the Boolean exchange cube.

When \(|A|\le3\), a mutual matching does supply all nontrivial cube levels,
so mutual matching and family base orderability coincide in that limited
rank.  Pairwise reciprocity is still stronger: it requires equality of the
whole two relations, not just one perfect matching in their intersection.

### Matroid basis exchange

Neither (PR) nor (1.4) is a matroid assertion.  Matroid basis exchange
requires the mixed sets to remain members of a specified collection of
**independent bases**.  Here the mixed configurations are required only to
belong to an eternal family of dominating configurations; they can have
internal graph edges.  Even a family base ordering therefore does not make
the maximum independent sets of \(G\) into matroid bases.

This distinction matters: the proved adversarial exchange theorem C-064
is an online transition statement inside an eternal family, not a basis
exchange axiom.

## 2. The open equality statement

The exact proposed theorem is:

> **Greatest-family reciprocity conjecture.**  
> Let
> \[
> \gamma(G)=\alpha(G)=\gamma^\infty(G)=k,
> \]
> and let \(\mathcal K\) be the greatest eternal \(k\)-family.  For every
> two independent \(k\)-sets \(S,T\), every \(u\in S-T\), and every
> \(x\in T-S\),
> \[
> S-u+x\in\mathcal K
> \quad\Longleftrightarrow\quad
> T-x+u\in\mathcal K.
> \tag{2.1}
> \]

The distinction between greatest and arbitrary families is essential.
C-065 already gives an equality graph and a proper eternal family in which
(2.1) fails.  In that same graph, taking the greatest family restores the
missing reverse state.  That observation motivated (2.1), but it is not a
proof.

The greatest fixed point is the union of all eternal \(k\)-families.
Consequently, proving (2.1) requires constructing some complete eternal
strategy through the reverse state.  It is not enough to reverse one legal
move, because closure quantifies over every future unoccupied attack.

## 3. What reciprocity would prove about C-108

Under
\[
\alpha(G)=\gamma^\infty(G)=k,
\]
C-108 defines a family-relative active set \(A_x\).  Equivalently, for
distinct vertices \(u,x\), write

\[
 u\mathrel{\triangleright}x
\]

when a maximum independent state containing \(u\) can answer an attack at
\(x\) by moving \(u\), with the successor retained in the greatest family.
C-108 proves that this does not depend on which maximum independent state
containing \(u\) is chosen.

### Proposition 3.1 (conditional active-edge symmetry) — PROVED

If the greatest-family reciprocity conjecture holds for \(G\), then

\[
\boxed{
u\mathrel{\triangleright}x
\quad\Longleftrightarrow\quad
x\mathrel{\triangleright}u.
}
\tag{3.1}
\]

#### Proof

Assume \(u\mathrel{\triangleright}x\).  Choose a maximum independent set
\(S\) containing \(u\); the active move implies \(ux\in E(G)\), so
\(x\notin S\).  Equality makes \(G\) well-covered.  Extend the singleton
\(\{x\}\) to a maximal independent set \(T\), which therefore has size
\(k\).  Again \(ux\in E(G)\) gives \(u\notin T\).

By definition,
\[
S-u+x\in\mathcal K.
\]
Apply (2.1) to \(S,T,u,x\).  It gives
\[
T-x+u\in\mathcal K,
\]
so \(x\mathrel{\triangleright}u\).  The reverse implication follows by
interchanging \(u\) and \(x\). \(\square\)

Thus (2.1) would turn the directed active-response relation into an
ordinary undirected spanning subgraph of \(G\).  At a fixed independent
reference state \(S\), it would identify

\[
u\in L_S^{\mathcal K}(x)
\quad\Longleftrightarrow\quad
x\mathrel{\triangleright}u.
\tag{3.2}
\]

This is material global consistency, but it does **not by itself** finish
either current gluing branch:

- in the singleton/no-full branch, it supplies the reverse retained
  exchange but does not eliminate a positive-length cross-component
  2-SAT chain, lollipop, or bicycle;
- in the full-list branch, it does not force the responder-color sets of
  different ridge components to have a common color, which is the missing
  intersection in C-108.

It nevertheless gives a strong concrete full-list consequence.  At
\(k=3\), if \(S=\{s_1,s_2,s_3\}\) is full at \(x\) and
\(T=\{x,b,c\}\) is any maximum independent triple, then (2.1) would put

\[
\{s_i,b,c\}=T-x+s_i\in\mathcal K
\qquad(i=1,2,3).
\tag{3.3}
\]

Moreover, for two disjoint triples, C-064 supplies a perfect matching in
the directed response relation.  Pairwise reciprocity makes that matching
mutual, and at rank three a mutual matching is equivalent to one complete
eight-state family base-ordering cube.  These conclusions could materially
squeeze the current anchorless full-list boundary when combined with its
other geometry.  They remain conditional: reciprocity itself is not proved
here and is not presently a replacement for the remaining gluing theorem.

## 4. Exact greatest-family countermodel without \(\gamma=\alpha\)

Let

\[
G=\texttt{GEjbug}
\tag{4.1}
\]

with vertices \(0,\ldots,7\) and edge set

\[
\begin{split}
\{&
03,04,05,07,\;
13,15,16,17,\;
24,25,26,\\
&36,37,\;46,\;57
\}.
\end{split}
\tag{4.2}
\]

Independent recomputation gives

\[
\boxed{
(\gamma,i,\alpha,\gamma^\infty,\theta)
=(2,2,3,3,3).
}
\tag{4.3}
\]

For example, \(\{0,6\}\) is an independent dominating pair, while
\[
\{2,4,6\},\quad\{0,3,7\},\quad\{1,5\}
\]
is a three-clique partition.  The independent triple \(012\) gives the
matching lower bound \(\theta\ge3\).

The greatest eternal triple-family has 41 states.  Its canonical
serialization hash is

```text
59b74f7c52c11f9672407c5c05d6ab9a0131904787742e3715c68e1b39c9eace
```

All \(41(8-3)=205\) attack obligations have been replayed, with 296 legal
retained moves in total.

Take

\[
S=012,\qquad T=345,\qquad u=0,\qquad x=4.
\tag{4.4}
\]

Both endpoints are maximum independent states, \(04\in E(G)\), and

\[
S-0+4=124\in\mathcal K.
\tag{4.5}
\]

But

\[
T-4+0=035\notin\mathcal K.
\tag{4.6}
\]

This is not a static failure: \(035\) dominates \(G\).  Its attack at
vertex \(7\), however, has no dominating one-guard successor:

\[
\begin{array}{c|c|c}
\text{mover}&\text{successor}&\text{undominated vertex}\\ \hline
0&357&4\\
3&057&6\\
5&037&2
\end{array}
\tag{4.7}
\]

Thus \(035\) is deleted in the first kernel round, while \(124\) survives
in the literal greatest fixed point.  This proves:

> **Boundary proposition — PROVED.**  
> Maximum-independent endpoints and use of the greatest eternal family do
> not force pairwise complementary-exchange reciprocity under
> \(\alpha=\gamma^\infty=3\).  The additional equality
> \(\gamma=\alpha\) cannot be omitted.

The graph is not a gamma--theta counterexample because
\(\gamma=2<3=\gamma^\infty\).

## 5. Exact and exploratory finite probes

### Complete two-vertex extension class

The deterministic program `exhaustive_two_vertex_extension.py` fixes the
eight old vertices of `GEjbug` as an induced subgraph and adds vertices
8 and 9 with all \(17\) incident/new-edge bits free.  It exhausts all

\[
2^{17}=131{,}072
\]

labeled extensions.

The exact stage counts are:

\[
\begin{array}{l|r}
\text{condition}&\text{count}\\ \hline
\alpha=3&65{,}410\\
\gamma=\alpha=3&210\\
\gamma=\alpha=\gamma^\infty=3&36\\
\text{independent-state pairs tested in those 36 graphs}&3{,}136\\
\text{pairwise reciprocity violations}&0
\end{array}
\]

This is a complete result only for that fixed induced-extension class.  It
does not cover old-edge edits, substitutions, or arbitrary order-ten
graphs.  Pending an independent implementation replay, it is classified
as **OBSERVED**, not a certified finite theorem.

### Exact-kernel SAT formulation

`build_exact_kernel_cnf.py` gives a separate discovery encoding.  It fixes
disjoint independent triples \(S=012,T=345\), fixes \(u=0,x=3\), enforces
\(\alpha=\gamma=3\), and unfolds the greatest triple-kernel for
\(\binom n3\) rounds.  A descending chain on \(\binom n3\) states must
stabilize within that many strict deletion rounds, so the encoded survivor
and nonsurvivor conditions are exact rather than an arbitrary-family
approximation.

Discovery instances at \(n=6,7,8,9\) were reported UNSAT by CaDiCaL
3.0.1.  No proof logs were retained for independent checking, and the
formulation fixes disjoint endpoints, so these solver outcomes are
**exploratory only**.  The campaign's broader ordinary-set order-nine scan
is independent of this encoding.

### Random falsification

The discovery generator `search_countermodel.py` samples graphs with a
displayed partition into three \(G\)-cliques.  In two recorded trial
batches it tested 32,141 equality graphs and over 20 million independent
state pairs with no violation.  These graphs already have
\(\theta=3\), so the result is only a stress test; it is not evidence that
can distinguish the conjectured theorem from a consequence of the known
clique partition.

## 6. Proof attempts that did not close

Three tempting arguments fail.

1. **Reverse the move.**  
   From \(S-u+x\), an attack at \(u\) indeed forces \(x\to u\) back to
   \(S\).  This says nothing about the future attacks from
   \(T-x+u\).  The failed attack (4.7) is the concrete obstruction.

2. **Use that the greatest family is a union.**  
   A state belongs to the greatest family only if some complete eternal
   strategy contains it.  A winning strategy through the forward state
   cannot be time-reversed when the two exchanged guards have different
   neighborhoods.

3. **Invoke C-108 directly.**  
   C-108 transports the activity of a fixed responder across independent
   states that contain that responder and avoid the fixed target.  The
   desired reverse move changes both roles: \(u\) is the original
   responder, while \(x\) must become the responder.  C-108 does not make
   that orientation switch.

The most precise remaining proof target is therefore to use
\(\gamma=\alpha\) to rule out the complete future-attack obstruction that
separates (4.5) from (4.6).  Any successful argument must use more than
greatest-fixed-point maximality.

## 7. Reproduction

From the campaign root:

```text
python3 math/working/greatest_family_reciprocity/verify_countermodel.py
python3 math/working/greatest_family_reciprocity/exhaustive_two_vertex_extension.py \
  --output math/working/greatest_family_reciprocity/extension_result.json
```

The first command is the rigorous graph-specific verifier.  The second
replays the delimited extension experiment.
