# Independent hostile review of the \(k=3\) complement dictionary

**Review date:** 2026-07-25 13:57 PDT  
**File reviewed:** `math/lemmas/complement_k3_dictionary.md`
(`sha256:9b8e9a45e8f5665b24a8c672c05ca4c365eda0fbf63fcdaec54ab5f37dc44bd2`)

## Verdict

**ACCEPT the mathematics.** Both propositions, all five necessary
complement-side conditions, and the final converse are correct for finite
simple graphs in the stated one-guard-moves model. Every displayed
equivalence has been checked in both directions. The note consistently uses
open neighborhoods in \(H\), attacks only unoccupied vertices, and translates
a legal edge of \(G\) into a nonedge of \(H\) only when the two vertices are
distinct.

No critical-, high-, or medium-severity defect was found. There is one
low-severity omitted dependency in the explanation of the connected search
target; the dependency is already proved elsewhere in the repository and
does not invalidate the target or the converse.

## 1. Severity-ranked findings and exact corrections

### Critical, high, and medium severity

None.

### Low severity L1: condition (4) uses two earlier reductions without
naming them

The sentence saying that a \(k=3\) counterexample yields an \(H\) satisfying
\(\overline H\) connected is true, but it is not a consequence of
Propositions 1 and 2 alone. It also uses component additivity/connected
reduction and the previously proved exclusion of counterexamples with
parameter below three.

Indeed, equality of the additive quantities
\(\gamma(G)=\gamma^\infty(G)=3\) forces equality on every component. A
positive summed clique-cover gap occurs on some component \(C\), so \(C\)
is itself a counterexample. The minimum-parameter theorem gives
\(\gamma(C)\geq3\). Since the domination numbers of all nonempty components
are positive and sum to three, \(C\) is the only component. Thus \(G\) is
connected.

**Exact correction:** immediately before the five-item target, add:

> By Corollary 6 and Corollary 11 of `math/reductions.md`, every
> parameter-three counterexample is connected: its counterexample component
> already has domination number at least three, which exhausts the total
> domination number.

Alternatively, weaken the introductory sentence to “After the connected
reduction, a \(k=3\) counterexample may be chosen so that …”. The first
version preserves the stronger fact that every parameter-three
counterexample is connected.

This is a dependency/exposition correction, not a mathematical gap. Moreover,
condition (4) is not used in the final parameter converse; it restricts the
search to the connected universe.

## 2. Proposition 1: line-by-line static-parameter audit

### Item (1): \(\alpha(G)=\omega(H)\) and \(\theta(G)=\chi(H)\)

For each vertex subset \(S\), all pairs in \(S\) are nonedges of \(G\) if
and only if they are edges of \(H=\overline G\). Thus independent sets of
\(G\) and cliques of \(H\) are the same subsets, proving the first equality.
A part in a clique partition of \(G\) is an independent color class of \(H\),
and conversely. Minimizing the number of nonempty parts/colors proves the
second equality. There is no reversal of \(G\) and \(\overline G\).

### Item (2): domination and open neighborhoods in \(H\)

The exclusion \(x\notin D\) is essential and is present. Such an \(x\) is
undominated by \(D\) in \(G\) exactly when

\[
  xd\notin E(G)\quad\text{for every }d\in D.
\]

Because \(x\ne d\), complementation gives
\(xd\in E(H)\) for every \(d\in D\), equivalently
\(D\subseteq N_H(x)\). The neighborhood in \(H\) must be open here, and the
note uses the open neighborhood. Vertices inside \(D\) need not be tested
because closed-neighborhood domination makes them self-dominated in \(G\).
Negating the existence of such an outside vertex gives the stated iff.

### Item (3): dominating pairs and common neighbors

For a two-element set \(D=\{u,v\}\), the witness in item (2) is precisely a
vertex in \(N_H(u)\cap N_H(v)\). In a simple graph neither \(u\) nor \(v\)
can belong to this intersection: each would have to be adjacent to itself.
Thus “outside the pair” is automatic, and the stated iff is exact for every
pair of distinct vertices, whether or not that pair is an edge of \(H\).

### Item (4): \(\gamma(G)=3\) and the common-neighbor property

Both directions are sound:

1. If \(\gamma(G)=3\), no pair dominates. Item (3) therefore supplies a
   common neighbor in \(H\) for every pair.
2. If every pair has a common neighbor, item (3) says that no pair dominates.
   A dominating singleton is also impossible, because any pair containing
   it would dominate. Hence \(\gamma(G)\geq3\).
3. The hypothesis \(\omega(H)=3\) supplies a triangle of \(H\), hence an
   independent triple of \(G\). It is maximum and therefore maximal
   independent, so it dominates \(G\). Thus \(\gamma(G)\leq3\).

Combining the last two bounds gives equality. The hypothesis
\(\omega(H)=3\), not merely \(\omega(H)\leq3\), is used correctly to obtain
the dominating triple.

### Item (5): well-coveredness and maximal cliques

Maximal independent sets of \(G\) and maximal cliques of \(H\) are exactly
the same vertex subsets. Under \(\omega(H)=3\), \(H\) has a triangle, so the
maximum size of such a clique is three. Therefore all maximal independent
sets of \(G\) have the same size if and only if every maximal clique of \(H\)
has size three. Calling each such clique a triangle is exact. The statement
does not confuse maximal and maximum cliques.

## 3. Proposition 2: exact one-guard translation

The definition of externally uncontained is exactly the negation in
Proposition 1(2), separately for every \(x\notin D\). Thus condition (1) says
precisely that the family is nonempty and every configuration dominates
\(G\).

For condition (2), the quantifier order is the required

\[
 \forall D\in\mathcal F\ \forall r\notin D\ \exists u\in D.
\]

The restriction \(r\notin D\) makes the attack unoccupied and also ensures
\(u\ne r\). For these distinct vertices,

\[
 ur\notin E(H)\quad\Longleftrightarrow\quad ur\in E(G),
\]

so exactly one named guard traverses exactly one edge of \(G\). Replacing
\(u\) by \(r\) gives the displayed successor, and requiring that successor
to lie in \(\mathcal F\) supplies both family closure and, through condition
(1), domination of the successor. There is no stationary response, occupied
attack, simultaneous movement, or all-guards-move interpretation hidden in
the translation.

When \(k=\alpha(G)=3\), every triangle of \(H\) is an independent three-set
of \(G\). The cited maximum-independent-state lemma applies to any eternal
family of three-sets, without requiring that family to be greatest or
minimal. Hence every triangle belongs to every such family, as claimed.

## 4. Necessary target and final converse

For a parameter-three counterexample \(G\), equality collapse gives
\(\alpha(G)=3\) and well-coveredness. Consequently:

1. complementing gives
   \(\omega(H)=\alpha(G)=3<\theta(G)=\chi(H)\);
2. Proposition 1(4) translates \(\gamma(G)=3\) into the common-neighbor
   condition;
3. Proposition 1(5) translates well-coveredness into the maximal-triangle
   condition;
4. the component and minimum-parameter reductions give connectedness, as
   detailed in finding L1; and
5. an eternal family witnessing \(\gamma^\infty(G)=3\) translates through
   Proposition 2 and contains every triangle by the cited lemma.

No condition is inferred from merely having \(\omega(H)=3<\chi(H)\).

For the converse, let \(H\) satisfy conditions (1), (2), (4), and (5), and
write \(G=\overline H\). Then:

\[
\begin{aligned}
 \alpha(G)&=\omega(H)=3,\\
 \theta(G)&=\chi(H)>3,\\
 \gamma(G)&=3
   &&\text{by Proposition 1(4) and condition (2)},\\
 \gamma^\infty(G)&\leq3
   &&\text{by Proposition 2 and condition (5)},\\
 \gamma^\infty(G)&\geq\alpha(G)=3
   &&\text{by the general parameter chain}.
\end{aligned}
\]

Thus
\(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)\), exactly as stated.
Condition (4) is not needed for these numerical equalities; it ensures that
the resulting counterexample is connected. Once
\(\gamma(G)=\gamma^\infty(G)\) is established, equality collapse gives
well-coveredness, and Proposition 1(5) then gives condition (3). This is not
circular: condition (3) is neither assumed nor used to prove the equality.
The assertion that the family in condition (5) necessarily contains every
triangle is likewise a proved consequence, not an additional unverified
static replacement for eternal closure.

## 5. Independent computational falsification attempts

These checks support, but do not replace, the proofs above.

- I enumerated all labeled graphs \(H\) through order six. Among the graphs
  with \(\omega(H)=3\), I checked Proposition 1(2) for every vertex subset,
  item (4) by an independent exhaustive domination-number calculation, and
  item (5) by independently enumerating maximal independent sets of
  \(\overline H\) and maximal cliques of \(H\). There were no discrepancies.
  The numbers of \(\omega=3\) graphs checked at orders \(3,4,5,6\) were
  \(1,22,570,21837\), respectively.
- On all \(33{,}867\) labeled graphs of orders one through six and every
  \(1\leq k\leq n\), I independently constructed the greatest fixed point
  once from dominating configurations and legal edges in \(G\), and again
  from externally uncontained configurations and nonedges in \(H\).
  The complete surviving families agreed in every case.

## 6. Final audit conclusion

The note is safe to use as an exact formulation of the connected
\((n,k)=(12,3)\) synthesis target. In particular:

1. domination uses closed neighborhoods in \(G\) but translates to a test
   against open neighborhoods of outside vertices in \(H\);
2. “every pair” means every two-element vertex set and includes both edges
   and nonedges of \(H\);
3. the common-neighbor and well-covered equivalences both require, and
   correctly use, the exact hypothesis \(\omega(H)=3\);
4. the eternal-family condition retains the full
   \(\forall D\,\forall r\,\exists u\) game quantifiers; and
5. the final converse is complete and does not use condition (3)
   circularly.

Subject only to the low-severity dependency citation in L1, no mathematical
correction is required.

## Fix-confirmation addendum

**Rechecked 2026-07-25.** The revised note
(`sha256:54d7cafdc7047d75ed58739f6a773344a2f780aaecd0eafde8ed01a0692c6256`)
now cites Corollaries 6 and 11 of `math/reductions.md` and states the exact
reason a parameter-three counterexample is connected: its counterexample
component has domination number at least three and therefore exhausts the
total domination number. This is the correction requested in L1, with no
change to the propositions or converse; the revised status accurately
records this hostile review. Finding L1 is resolved, so the acceptance
verdict is now unconditional.
