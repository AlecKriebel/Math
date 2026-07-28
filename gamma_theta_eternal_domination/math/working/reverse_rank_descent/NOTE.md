# Finite-horizon star transport and exact single-hit rank descent

## Status and exact boundary

Date: 2026-07-28 (PDT)

This frozen candidate note proves a finite-horizon strengthening of the
accepted C-108 vertex-star theorem.  Kernel deletion rank is
Lipschitz along the maximum-independent-set star of a fixed responder and
target.  Combined with C-143, this gives an exact rank-descent rule for a
single-hit deleting attack at any hypothetical nonreciprocal reverse
endpoint.

The result does **not** prove survivor-to-survivor reciprocity.  It shows
instead that every rank-one or minimum-rank obstruction must be a
genuine collision: its deleting attack is adjacent to at least two guards
of the independent endpoint state.  The two-guard collision branch is
not eliminated here.  No complete parameter case and no form of the
gamma--theta conjecture is claimed.

No literature-priority claim is made.

## 1. Greatest-kernel horizons and rank

Fix a graph \(G\) and a guard number \(k\).  Let

\[
 \mathcal K_0
 =
 \{D\in {V(G)\choose k}:D\text{ dominates }G\},
\tag{1.1}
\]

and, recursively,

\[
 \mathcal K_{h+1}
 =
 \left\{
 D\in\mathcal K_h:
 \begin{array}{l}
 \text{for every }r\notin D\text{ there is }d\in D\cap N(r)\\
 \text{such that }D-d+r\in\mathcal K_h
 \end{array}
 \right\}.
\tag{1.2}
\]

The sets are nested.  Their stable intersection is the literal greatest
one-guard eternal \(k\)-family \(\mathcal K_\infty\).

Give every \(k\)-set \(D\) the extended deletion rank

\[
 \rho(D)=
 \begin{cases}
 0,&D\notin\mathcal K_0,\\
 h,&D\in\mathcal K_{h-1}-\mathcal K_h,\quad h\ge1,\\
 \infty,&D\in\mathcal K_\infty.
 \end{cases}
\tag{1.3}
\]

Thus rank zero is non-domination, a positive finite rank is a literal
synchronous deletion round, and infinite rank is greatest-family
survival.

## 2. Finite-horizon vertex-star transport

### Theorem 2.1 (horizon transport) — PROVED

Let \(T,T'\) be independent \(k\)-sets, let

\[
 v\in T\cap T',
 \qquad
 x\notin T\cup T',
\tag{2.1}
\]

and put

\[
 m=|T-T'|=|T'-T|.
\tag{2.2}
\]

For every \(j\ge0\),

\[
 \boxed{
 T-v+x\in\mathcal K_{j+m}
 \quad\Longrightarrow\quad
 T'-v+x\in\mathcal K_j.
 }
\tag{2.3}
\]

#### Proof

Put

\[
 A=(T\cap T')-\{v\},
 \qquad
 O=T-T',
 \qquad
 B=T'-T.
\tag{2.4}
\]

Then \(|O|=|B|=m\).  Order

\[
 B=\{b_1,\ldots,b_m\}.
\]

Start at

\[
 D_0=T-v+x
   =\{x\}\cup A\cup O
   \in\mathcal K_{j+m}.
\tag{2.5}
\]

Attack \(b_1,\ldots,b_m\) in that order.  We prove inductively that after
the first \(\ell\) attacks there is a state

\[
 D_\ell
 =
 \{x\}\cup A
 \cup\{b_1,\ldots,b_\ell\}
 \cup O_\ell
 \in\mathcal K_{j+m-\ell},
\tag{2.6}
\]

where \(O_\ell\subseteq O\) and

\[
 |O_\ell|=m-\ell.
\tag{2.7}
\]

Suppose \(D_{\ell-1}\) has been obtained.  The next target \(b_\ell\) is
unoccupied.  Membership in
\(\mathcal K_{j+m-\ell+1}\) supplies a legal response whose successor is
in \(\mathcal K_{j+m-\ell}\).

No guard in

\[
 A\cup\{b_1,\ldots,b_{\ell-1}\}
\tag{2.8}
\]

can move to \(b_\ell\), because all those vertices belong to the
independent set \(T'\).  The guard at \(x\) cannot supply the retained
response either.  If it moved, the successor would be contained in

\[
 (T\cup T')-\{v\}.
\tag{2.9}
\]

Every vertex of (2.9) is nonadjacent to \(v\), since it belongs to one of
the two independent sets containing \(v\).  The successor would therefore
miss \(v\), so it would not even lie in \(\mathcal K_0\), much less in
\(\mathcal K_{j+m-\ell}\).

The retained response is consequently forced to move one guard from
\(O_{\ell-1}\).  Removing that mover gives \(O_\ell\) and establishes
(2.6)--(2.7).  At \(\ell=m\), the set \(O_m\) is empty and

\[
 D_m=T'-v+x\in\mathcal K_j.
\]

This proves (2.3). \(\square\)

### Corollary 2.2 (rank is star-Lipschitz) — PROVED

Under the hypotheses of Theorem 2.1, put

\[
 D=T-v+x,
 \qquad
 D'=T'-v+x.
\tag{2.10}
\]

Then:

1. \(\rho(D)=\infty\) if and only if \(\rho(D')=\infty\);
2. if both ranks are finite, then
   \[
   \boxed{
   |\rho(D)-\rho(D')|\le m.
   }
   \tag{2.11}
   \]

#### Proof

If \(D\) survives, it belongs to \(\mathcal K_{j+m}\) for every \(j\).
Theorem 2.1 therefore puts \(D'\) in every \(\mathcal K_j\).  Interchanging
\(T,T'\) proves the converse.

Suppose now that \(r=\rho(D)\) and \(s=\rho(D')\) are finite.  If
\(r\ge m+1\), then

\[
 D\in\mathcal K_{r-1}
   =\mathcal K_{(r-m-1)+m}.
\]

Theorem 2.1 gives

\[
 D'\in\mathcal K_{r-m-1},
\]

and hence \(s\ge r-m\).  If \(r\le m\), the same inequality
\(r-s\le m\) follows merely from \(s\ge0\).  Thus \(r-s\le m\).
Interchanging the two states gives \(s-r\le m\), proving (2.11).
\(\square\)

### Remarks on scope

Taking one rank to be infinite recovers C-108.  The finite statement is
strictly more informative than survival propagation, but it does not say
that the two finite ranks are equal.  Equality is false even under the
campaign parameter equalities; the exact controls in Section 5 attain
both the one-step and two-step bounds in (2.11).

The theorem compares states in one fixed vertex-star: the responder
\(v\) and target \(x\) are unchanged.  Complementary-exchange reciprocity
compares opposite orientations, so Corollary 2.2 cannot by itself turn a
surviving \(u\to x\) move into a surviving \(x\to u\) move.

## 3. The C-143 reverse-rank landscape

Assume now

\[
 \gamma(G)=\gamma^\infty(G)=k,
\tag{3.1}
\]

let \(\mathcal K_\infty\) be the greatest eternal \(k\)-family, and use
the family-relative active notation

\[
 u\triangleright x.
\]

The equality collapse gives

\[
 i(G)=\alpha(G)=k.
\tag{3.2}
\]

Suppose

\[
 u\triangleright x,
 \qquad
 x\not\triangleright u.
\tag{3.3}
\]

For every maximum independent \(k\)-set \(T\) containing \(x\), define

\[
 B_T=T-x+u.
\tag{3.4}
\]

Accepted C-143 says that every \(B_T\) dominates.  C-108 and the second
part of (3.3) say that no \(B_T\) survives.  Thus

\[
 1\le\rho(B_T)<\infty.
\tag{3.5}
\]

### Corollary 3.1 (reverse ranks form a Lipschitz potential) — PROVED

For any two maximum independent \(k\)-sets \(T,T'\) containing \(x\),

\[
 \boxed{
 |\rho(B_T)-\rho(B_{T'})|
 \le |T-T'|
 \le k-1.
 }
\tag{3.6}
\]

In particular, across a ridge step of the maximum-independent-set
complex, reverse deletion rank changes by at most one.

#### Proof

Apply Corollary 2.2 with fixed responder \(v=x\), fixed target \(u\), and
the two independent source states \(T,T'\).  The edge \(ux\) ensures
that both source states avoid \(u\).  Equation (3.5) excludes both zero
and infinite rank. \(\square\)

For \(k=3\), let \(w\) be a common nonneighbor of the asymmetric edge
\(\{u,x\}\), and complete \(\{x,w\}\) to a maximum independent triple
\(T_w\).  Every other endpoint triple \(T\) containing \(x\) differs
from \(T_w\) in at most two vertices, so

\[
 |\rho(B_T)-\rho(B_{T_w})|\le2.
\tag{3.7}
\]

This is the sound replacement for the false shortcut that the minimum
reverse rank must itself be attained at a shared-pivot endpoint.  The
minimum need not be attained there; it is only within two deletion rounds.

## 4. Exact descent at a single-hit blocker

Retain (3.1)--(3.4), write

\[
 T=\{x\}\mathbin{\dot\cup}Q,
 \qquad |Q|=k-1,
 \qquad B=B_T=\{u\}\cup Q,
\tag{4.1}
\]

and let

\[
 h=\rho(B).
\tag{4.2}
\]

An attack at \(r\notin B\) **deletes \(B\) at round \(h\)** if every
legal one-guard successor of \(B\) at \(r\) has rank strictly below
\(h\).  Such an attack exists by the definition of rank.

### Theorem 4.1 (single-hit descent or collision) — PROVED

Let \(r\) delete \(B\) at round \(h\).  Then

\[
 Q\cap N(r)\ne\varnothing.
\tag{4.3}
\]

If the independent endpoint \(T\) has exactly one neighbor at the
deleting attack,

\[
 N(r)\cap T=\{q\},
\tag{4.4}
\]

then \(q\in Q\), the set

\[
 J=T-q+r
\tag{4.5}
\]

is a maximum independent \(k\)-set containing \(x\), and the legal
successor

\[
 C=B-q+r=J-x+u
\tag{4.6}
\]

has the exact rank

\[
 \boxed{\rho(C)=h-1.}
\tag{4.7}
\]

Consequently:

1. every deleting attack at a rank-one reverse endpoint satisfies
   \[
   |N(r)\cap T|\ge2;
   \tag{4.8}
   \]
2. if \(B_T\) has minimum rank among all reverse endpoints in (3.4),
   then every deleting attack at \(B_T\) also satisfies (4.8).

#### Proof

First suppose that \(Q\cap N(r)=\varnothing\).  Since \(B\) dominates,
the attack at \(r\) must be adjacent to \(u\).  Moving \(u\) gives

\[
 B-u+r=Q\cup\{r\}.
\tag{4.9}
\]

The set in (4.9) is independent: \(Q\) is independent and, by the
supposition, \(r\) misses all of \(Q\).  It has size \(k=\alpha(G)\), so
it belongs to every eternal \(k\)-family, in particular
\(\mathcal K_\infty\).  Thus (4.9) is a legal surviving response to the
deleting attack, a contradiction.  This proves (4.3).

Now assume (4.4).  By (4.3), its unique member \(q\) lies in \(Q\).
The vertex \(r\) misses \(x\) and every member of \(Q-\{q\}\).
Therefore \(J=T-q+r\) is an independent \(k\)-set, proving (4.5).

The move \(q\to r\) is legal from \(B\), and its successor is exactly
the reverse endpoint \(C\) in (4.6).  Since \(r\) deletes \(B\) at round
\(h\),

\[
 \rho(C)<h.
\tag{4.10}
\]

C-143 applied to the active edge \(u\triangleright x\) and the endpoint
\(J\) says that \(C\) dominates.  The inactive reverse orientation
\(x\not\triangleright u\), together with C-108, says that \(C\) does not
survive.  Hence \(1\le\rho(C)<\infty\).

The two endpoint states \(T,J\) share \(x\) and differ by one vertex.
Corollary 3.1 gives

\[
 |\rho(B)-\rho(C)|\le1.
\tag{4.11}
\]

Combining (4.10)--(4.11) gives (4.7).  In particular \(h\ge2\), proving
(4.8) when \(h=1\).

Finally, if \(B\) is a minimum-rank reverse endpoint, (4.7) would produce
another reverse endpoint of smaller rank.  Thus (4.4) is impossible for
a deleting attack at \(B\), proving the second consequence. \(\square\)

### Exact remaining obstruction

Theorem 4.1 makes the rank-descent route well founded along every
single-hit deleting attack.  It also identifies exactly where that route
can stop:

\[
 \boxed{
 \text{a rank-one or minimum-rank blocker must hit at least two guards of }
 T.
 }
\tag{4.12}
\]

For \(k=3\), this is the two-list collision/bicycle geometry appearing in
the current structural proof lane.  Nothing proved here eliminates an
attack adjacent to both inactive-endpoint guards, or to one such guard
and \(x\).  Treating a collision as if it could be shortened to a
single-hit attack would be unsound.

## 5. Exact controls and sharpness

`verify_controls.py` is a standalone ordinary-set evaluator.  It decodes
each graph6 string, computes \(\gamma,i,\alpha,\gamma^\infty\), constructs
the literal greatest triple kernel, assigns exact deletion ranks, and
checks every finite-horizon star pair in each displayed graph.

The frozen controls are:

1. ``HCOe`Z{`` satisfies
   \[
   \gamma=i=\alpha=\gamma^\infty=3.
   \]
   With \(v=0,x=8\), the independent triples `012` and `017` differ by
   one vertex.  Their exchanged states `128` and `178` have ranks one and
   two.  Thus the unit bound in (2.11) is sharp under full campaign
   equality, and equal-rank transport is false.
2. `HCRdnat` also satisfies
   \[
   \gamma=i=\alpha=\gamma^\infty=3.
   \]
   With \(v=2,x=8\), the independent triples `012` and `234` differ by
   two vertices.  Their exchanged states `018` and `348` have ranks three
   and one.  Thus the distance-two bound is also sharp.
3. `HEjejrr` gives an exact single-hit descent outside the equality
   boundary.  The active exchange
   \[
   S=012,\quad T=458,\quad u=0,\quad x=4
   \]
   has reverse state `058` of rank two.  Attack \(r=3\) has the unique
   neighbor \(8\) in \(T\), and the ridge successor `035` has rank one.
   This realizes (4.7) exactly.
4. `GEjbug` has
   \[
   (\gamma,i,\alpha,\gamma^\infty)=(2,2,3,3).
   \]
   Its active exchange
   \[
   S=012,\quad T=345,\quad u=0,\quad x=4
   \]
   has reverse `035` of rank one.  The deleting attack \(r=7\) hits two
   endpoint guards, \(3\) and \(5\), and all legal successors are
   non-dominating.  This is the sharp collision control.  It is not an
   equality graph and does not refute a theorem using
   \(\gamma=i=\alpha=3\); it does refute any attempt to finish (4.12)
   from rank arithmetic alone.

Run from the campaign root:

```text
python3 -I -B -W error \
  math/working/reverse_rank_descent/verify_controls.py
```

The output must match `expected_result.json`.

## 6. What changed after C-143

C-143 closes rank zero for every reverse maximum-independent endpoint.
Theorems 2.1 and 4.1 now show that:

- finite reverse ranks cannot jump arbitrarily between adjacent facets;
- a single-hit deleting attack is not merely suggestive of descent—it
  moves to an adjacent reverse endpoint of **exactly** one lower rank;
- every minimal obstruction is therefore forced into the multi-hit
  collision branch.

The next proof obligation is precise: rule out, or recursively resolve,
the multi-hit blocker in (4.12) without shortening it by deleting one of
its genuine adjacencies.  That is a smaller statement than unrestricted
reciprocity, but it remains open.
