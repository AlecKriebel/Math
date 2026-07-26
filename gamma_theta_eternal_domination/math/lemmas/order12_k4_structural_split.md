# Order-12, parameter-four structural split

**Status:** `PROVED`, relative only to the already accepted campaign
reductions cited below.

**Claim boundary.**  This note does not prove the \(\gamma\)--\(\theta\)
conjecture and does not exclude the complete \((n,k)=(12,4)\) slice.  It
removes the previously surviving induced-\(C_9\) branch and reduces every
connected order-12 parameter-four counterexample to three SPGT templates.

## 1. Standing target and accepted inputs

Let \(G\) be a connected graph of order \(12\) satisfying

\[
 \gamma(G)=\gamma^\infty(G)=4<\theta(G),
\]

and put \(H=\overline G\).  The accepted parameter chain gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=4.
\]

We use the following consequences, all proved and adversarially accepted
elsewhere in the campaign.

1. \(\omega(H)=4<\chi(H)\).
2. Every three-set \(A\subseteq V(H)\) has a common \(H\)-neighbor outside
   \(A\):

   \[
     \tag{P3}
     \forall A\in {V(H)\choose 3}\quad
     \exists x\in V(H)\setminus A\quad
     A\subseteq N_H(x).
   \]

   Indeed, otherwise \(A\) would dominate \(G\), contrary to
   \(\gamma(G)=4\).
3. One-guard eternal domination is monotone on induced subgraphs and
   additive over components.
4. For odd \(r\geq5\),

   \[
     \gamma^\infty(\overline{C_r})=3.
   \]

Items 1--2 are proved in
`math/lemmas/order12_k4_synthesis_target.md`.  Items 3--4 are Lemmas 5, 8,
and 9 of `math/reductions.md`; their clean-room audit is
`reviews/reductions_hostile_review.md`.  We also use the proved formula

\[
 \gamma^\infty(C_{2m+1})=m+1,
\]

from `math/lemmas/order12_k4_synthesis_target.md`, whose proof is checked in
`reviews/order12_k4_synthesis_target_hostile_review.md`.

Throughout, a **hub for an induced cycle \(C\) in \(H\)** means a vertex
outside \(C\) adjacent in \(H\) to every vertex of \(C\).

## 2. A general large-hole exclusion

**Lemma 1 (rim triples require an outside witness).**  Let \(C\) be an
induced cycle of length at least \(5\) in a graph \(H\) satisfying (P3), and
let \(X=V(H)\setminus V(C)\).  Every three-set of rim vertices is contained
in \(N_H(x)\) for some \(x\in X\).

**Proof.**  Apply (P3) to three distinct rim vertices.  A rim vertex has
exactly its two cyclic neighbors among the other rim vertices, so no rim
vertex can be adjacent to all three.  The common neighbor supplied by (P3)
therefore lies in \(X\). \(\square\)

**Lemma 2 (at most three outside vertices force a hub).**  Under the
hypotheses of Lemma 1, if \(1\leq |X|\leq3\), then \(C\) has a hub.

**Proof.**  Suppose that no member of \(X\) is a hub.  For each \(x\in X\),
choose a rim vertex \(t_x\notin N_H(x)\).  The set of chosen vertices has
size at most \(3\); extend it, if necessary, to a three-set \(T\) of rim
vertices.  Every \(x\in X\) misses a member of \(T\), while Lemma 1 says that
some \(x\in X\) contains all of \(T\) in its neighborhood.  This is a
contradiction. \(\square\)

**Theorem 3 (large-hole exclusion).**  Let \(H\) satisfy (P3), and suppose
that \(G=\overline H\) is connected.  If \(C\) is an induced cycle of length
at least \(5\) in \(H\), then

\[
 |V(H)\setminus V(C)|\geq4.
\]

**Proof.**  Put \(X=V(H)\setminus V(C)\) and \(r=|X|\).

- If \(r=0\), Lemma 1 is already impossible.
- If \(r=1\), Lemma 2 gives a hub \(a\).  It is universal in \(H\), hence
  isolated in \(G\), contradicting connectedness.
- Suppose \(r=2\), with \(X=\{a,b\}\), and choose the hub \(a\) supplied by
  Lemma 2.  Connectedness of \(G\) forces \(ab\notin E(H)\), since \(a\) is
  already complete in \(H\) to the rim.  Let \(uv\) be a rim edge.  The
  adjacent rim vertices \(u,v\) have no common rim neighbor because \(C\)
  is induced and has length at least \(5\).  The only possible outside
  witness for (P3) applied to \(\{a,u,v\}\) is \(b\), but \(b\) is not
  adjacent to \(a\), a contradiction.
- Suppose \(r=3\), with \(X=\{a,b,c\}\), and again choose a hub \(a\).
  Connectedness of \(G\) forces \(a\) to have an \(H\)-nonneighbor in
  \(X\); relabel so that \(ac\notin E(H)\).  For every rim edge \(uv\),
  apply (P3) to \(\{a,u,v\}\).  There is no rim witness, and \(c\) cannot
  witness because \(ac\notin E(H)\).  Thus the sole remaining outside
  vertex \(b\) must witness.  Consequently

  \[
    ab\in E(H)
    \quad\text{and}\quad
    \{u,v\}\subseteq N_H(b)
  \]

  for every rim edge \(uv\).  Hence \(b\) is also a hub.

  Now \(b\) is \(H\)-adjacent to \(a\) and to the entire rim.  Its only
  possible neighbor in the connected graph \(G\) is therefore \(c\), so
  \(bc\notin E(H)\).  Apply (P3) to \(\{c,u,v\}\) for any rim edge \(uv\).
  Neither \(a\) nor \(b\) is adjacent in \(H\) to \(c\), and \(u,v\) have
  no common rim neighbor.  No witness exists, a contradiction.

All cases \(r\leq3\) are impossible. \(\square\)

The \(r=3\) case also has a useful independent one-guard audit.  As soon as
the proof forces the adjacent hubs \(a,b\), the induced subgraph on
\(V(C)\cup\{a,b\}\) is, in \(G\),

\[
  2K_1\mathbin{\dot\cup}\overline C.
\]

When \(C=C_9\), accepted component additivity and
\(\gamma^\infty(\overline{C_9})=3\) give eternal domination number
\(1+1+3=5\).  Accepted induced-subgraph monotonicity would then imply
\(\gamma^\infty(G)\geq5\), independently contradicting the parameter-four
target.  This second argument is not needed for Theorem 3, but it audits the
step at exactly the one-guard model boundary.

**Corollary 4.**  The complement \(H\) of a connected order-12
parameter-four target contains no induced \(C_9\) and no induced \(C_{11}\).

**Proof.**  Either cycle would leave at most three vertices outside it,
contrary to Theorem 3. \(\square\)

## 3. The sharpened SPGT partition

**Theorem 5 (three-template split).**  Every connected order-12 graph
satisfying

\[
 \gamma(G)=\gamma^\infty(G)=4<\theta(G)
\]

has a complement \(H=\overline G\) containing at least one of

\[
 \boxed{C_5,\qquad C_7,\qquad \overline{C_7}}
\]

as an induced subgraph.

**Proof.**  Since \(\omega(H)=4<\chi(H)\), the Strong Perfect Graph Theorem
gives an induced odd hole or odd antihole in \(H\).

By Corollary 4, an odd hole in the 12-vertex graph \(H\) can only have
length \(5\) or \(7\).

If \(H\) contains an induced odd antihole
\(\overline{C_{2q+1}}\), then its clique number is \(q\).  The inequality
\(\omega(H)=4\) therefore gives \(2q+1\leq9\).  A five-antihole is \(C_5\).
An induced \(\overline{C_9}\) in \(H\) is an induced \(C_9\) in \(G\), but

\[
 \gamma^\infty(C_9)=5>\gamma^\infty(G)=4,
\]

contrary to induced-subgraph monotonicity.  The only remaining antihole is
\(\overline{C_7}\). \(\square\)

This improves the previously accepted four-way split
\(C_5,C_7,C_9,\overline{C_7}\) by rigorously deleting the \(C_9\) branch.
It is a structural reduction, not a finite nonexistence certificate.

## 4. Search consequence

An exact connected \((12,4)\) synthesis may now be partitioned into the
following complete, overlapping cases:

1. an induced \(C_5\) in \(H\);
2. no induced \(C_5\), but an induced \(C_7\) in \(H\);
3. neither induced hole above, but an induced \(\overline{C_7}\) in \(H\).

The negative conditions in cases 2--3 make the cases disjoint.  They are
not needed for coverage, and any implementation that omits them merely
creates overlap.  Template labels still require an orbit-complete
placement argument; fixing both an anchored \(K_4\) and a template on
arbitrary labels is not justified by this theorem.

