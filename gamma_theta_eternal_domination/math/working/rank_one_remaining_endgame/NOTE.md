# The rank-one QQ0 and AQ0 collisions are impossible

## Status and exact boundary

Date: 2026-07-28 (PDT)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\tag{0.1}
\]

let \(\mathcal K\) be the literal greatest eternal family of dominating
triples in the one-guard-moves model, and suppose

\[
 u\triangleright x,\qquad x\not\triangleright u.
\tag{0.2}
\]

Let

\[
 T=\{x,p,q\},\qquad B=\{u,p,q\},
\tag{0.3}
\]

where \(T\) is maximum independent and \(B\) has deletion rank one.
Suppose an attack \(r\) deleting \(B\) satisfies

\[
 ur\notin E(G),\qquad pr,qr\in E(G).
\tag{0.4}
\]

Thus \(r\) is in one of the two still-open \(ur=0\) rows of accepted
C-150:

\[
\begin{array}{c|c}
\text{row}&N(r)\cap T\\ \hline
\mathrm{QQ0}&\{p,q\},\\
\mathrm{AQ0}&\{x,p,q\}.
\end{array}
\tag{0.5}
\]

The new conclusion is:

> **Theorem (rank-one QQ0/AQ0 exclusion) — PROVED.**
> No configuration satisfying (0.1)--(0.5) exists.

For each of the two non-dominating successors at the deleting attack,
accepted C-150 supplies a private witness.  Independent completion and
the active orientation first force two mixed witness states into
\(\mathcal K\).  From one of them, attack the other witness.  Every
possible one-guard successor is either already non-dominating or has an
unoccupied attack at \(u\) whose only possible response lands in one
common state that misses \(r\).

The proof deliberately does **not** infer a graph nonedge from an omitted
family transition.  It does not require the two private witnesses to be
adjacent, nor does it use the QQ/AQ value of \(xr\).  Consequently it
proves both rows at once.

This closes only the rank-one QQ0 and AQ0 rows.  Together with accepted
C-150 it eliminates every rank-one row with \(ur\notin E(G)\); together
with the separately reviewed XQ1 exclusion it leaves only QQ1 and AQ1 at
rank one.  It does not close any higher-rank collision, greatest-family
reciprocity, the complete \(k=3\) case, or the gamma--theta conjecture.

## 1. Accepted data and collision audit

The legal movers from \(B\) at \(r\) are \(p,q\).  Since \(B\) has rank
one, both successors

\[
 C_p=\{u,r,q\},\qquad C_q=\{u,p,r\}
\tag{1.1}
\]

are non-dominating.  Let

\[
 y=y_p,\qquad z=y_q
\tag{1.2}
\]

be their private witnesses from accepted C-150.  Their exact required
incidence is

\[
\begin{array}{c|c|ccc}
 &\text{private edge}&\multicolumn{3}{c}{\text{missed successor}}\\ \hline
y&yp&yu&yr&yq\\
z&zq&zu&zr&zp
\end{array}
\tag{1.3}
\]

where each private edge is present and every entry in the last three
columns is absent.  We will not prescribe \(yz\).

### Lemma 1.1 (named vertices are distinct) — PROVED

The seven vertices

\[
 u,x,p,q,r,y,z
\tag{1.4}
\]

are pairwise distinct.

#### Proof

The vertices \(u,x,p,q\) are distinct by the two states in (0.3), and
\(r\) is an unoccupied attack on \(B\).  Moreover \(r\ne x\), because
\(rp\in E(G)\) while \(xp\notin E(G)\).

The witness \(y\) lies outside \(C_p=\{u,r,q\}\).  It differs from \(p\)
because \(pr\in E(G)\) while \(yr\notin E(G)\), and it differs from
\(x\) because \(yp\in E(G)\) while \(xp\notin E(G)\).  Similarly \(z\)
lies outside \(C_q=\{u,p,r\}\), differs from \(q\) because
\(qr\in E(G)\) while \(zr\notin E(G)\), and differs from \(x\) because
\(zq\in E(G)\) while \(xq\notin E(G)\).  Finally \(y\ne z\), since
\(yp\in E(G)\) while \(zp\notin E(G)\).  This exhausts all possible
named collisions. \(\square\)

## 2. Every private witness gives a retained mixed state

The next lemma is useful beyond the two rows, so it is stated in the
exact local generality used here.

### Lemma 2.1 (private-witness transfer) — PROVED

Let \(g\in\{p,q\}\), let \(t\) be the other member of \(\{p,q\}\), and
suppose a vertex \(y_g\) satisfies

\[
 uy_g,ty_g\notin E(G).
\tag{2.1}
\]

Then

\[
 M_g=T-g+y_g=\{x,t,y_g\}\in\mathcal K.
\tag{2.2}
\]

In particular, the private witnesses in (1.3) force

\[
 M_p=\{x,y,q\}\in\mathcal K,\qquad
 M_q=\{x,p,z\}\in\mathcal K.
\tag{2.3}
\]

#### Proof

The parameter chain applied to (0.1) gives

\[
 i(G)=\alpha(G)=3.
\tag{2.4}
\]

The pair \(\{u,y_g\}\) is independent.  Because \(i(G)=3\), it is not a
maximal independent pair; because \(\alpha(G)=3\), it extends to a
maximum independent triple

\[
 I=\{u,y_g,s\}.
\tag{2.5}
\]

Accepted C-010 puts every independent triple in every eternal
three-family, so \(I\in\mathcal K\).  The edge \(ux\) implies
\(x\notin I\).  Transporting the active response \(u\to x\) to \(I\)
by accepted C-108 gives

\[
 J=I-u+x=\{x,y_g,s\}\in\mathcal K.
\tag{2.6}
\]

If \(s=t\), this is already \(M_g\).  Otherwise \(t\) is unoccupied in
\(J\).  The state \(J\) dominates \(t\), while

\[
 xt,y_gt\notin E(G).
\tag{2.7}
\]

Therefore \(st\in E(G)\), and \(s\) is the unique guard eligible to
answer the unoccupied attack at \(t\).  Eternal closure forces

\[
 J-s+t=\{x,y_g,t\}=M_g\in\mathcal K.
\tag{2.8}
\]

Every move above is one guard along one edge, and each attacked vertex
is unoccupied. \(\square\)

The direct-completion case in this lemma is \(s=t\), not \(s=g\).
The latter collision is impossible anyway because \(gy_g\in E(G)\).

## 3. One witness attacks the other

### Proof of the theorem

Use Lemma 2.1 for \(g=q\), obtaining

\[
 M_q=\{x,p,z\}\in\mathcal K.
\tag{3.1}
\]

By Lemma 1.1, \(y\) is unoccupied in \(M_q\).  Attack \(y\).  There are
only three possible movers, and each possible successor is excluded
without making any assumption about whether its move edge exists.

1. **The \(z\)-successor.**  If \(zy\in E(G)\), moving \(z\to y\)
   gives
   \[
   A=\{x,p,y\}.
   \tag{3.2}
   \]
   This state misses the unoccupied vertex \(q\), because
   \[
   qx,qp,qy\notin E(G).
   \tag{3.3}
   \]
   Hence \(A\) is non-dominating and \(A\notin\mathcal K\).  If
   \(zy\notin E(G)\), then \(z\) is simply not an eligible mover.

2. **The \(p\)-successor.**  The private edge \(py\) is present, and
   moving \(p\to y\) gives
   \[
   W=\{x,y,z\}.
   \tag{3.4}
   \]
   This state cannot belong to \(\mathcal K\).  Indeed, attack the
   unoccupied vertex \(u\).  The witnesses \(y,z\) both miss \(u\),
   while \(ux\in E(G)\), so the only eligible response is
   \[
   x\to u,\qquad
   H=\{u,y,z\}.
   \tag{3.5}
   \]
   But \(H\) misses the unoccupied vertex \(r\), because
   \[
   ru,ry,rz\notin E(G).
   \tag{3.6}
   \]
   Thus \(H\) is non-dominating and cannot be retained.  The attack at
   \(u\) has no retained response, proving \(W\notin\mathcal K\).

3. **The \(x\)-successor.**  If \(xy\in E(G)\), moving \(x\to y\)
   gives
   \[
   X=\{p,y,z\}.
   \tag{3.7}
   \]
   Attack the unoccupied vertex \(u\).  Both witnesses miss \(u\).
   If \(pu\notin E(G)\), there is no eligible mover.  If
   \(pu\in E(G)\), the only eligible move is
   \[
   p\to u,
   \tag{3.8}
   \]
   and it again lands in the non-dominating state \(H\) from (3.5).
   In either subcase \(X\notin\mathcal K\).  If \(xy\notin E(G)\), then
   \(x\) is not an eligible mover at the original attack.

These are all guards of \(M_q\).  Thus the retained state \(M_q\) has no
retained response to the unoccupied attack at \(y\), contradicting
eternal closure.  The proof used only (0.4), not the value of \(xr\), so
it applies simultaneously to QQ0 and AQ0. \(\square\)

## 4. Dependency and model audit

The symbolic proof depends on:

1. the equality collapse \(i=\alpha=3\);
2. accepted C-010, which retains every independent triple;
3. accepted C-108 star transport for the active orientation
   \(u\triangleright x\); and
4. the rank-one private witnesses supplied by accepted C-150.

It does not use C-064 ridge covariance, the paired-witness adjacency
conclusion of C-150, any complement coloring, or any computational
UNSAT claim.

There are three logical levels in Section 3.

- A missing graph edge makes a guard ineligible to move.
- A present graph edge whose successor is non-dominating cannot furnish
  a retained response.
- The states \(W\) and \(X\) are excluded dynamically by a further
  unoccupied attack; their omission is never converted into a graph
  nonedge.

The common terminal state \(H=\{u,y,z\}\) is not rejected merely because
it is omitted.  It is rejected because the named unoccupied vertex \(r\)
is graph-nonadjacent to all three of its guards.

## 5. Independent finite bookkeeping audit

`verify_implication.py` is an ordinary-set audit of the proof's finite
incidence core.  For both QQ0 and AQ0 it enumerates all assignments to
the five graph pairs left optional by the argument:

\[
 up,\ uq,\ xy,\ xz,\ yz.
\tag{5.1}
\]

For each assignment it checks:

- the forced edge/nonedge table is consistent;
- every named attack is unoccupied;
- the two branches of Lemma 2.1 have the displayed unique response;
- every adjacency-eligible successor at the attack \(M_q\to y\) falls
  into exactly one of the three cases above;
- \(A\) misses \(q\);
- the \(u\)-attack from \(W\) has exactly the one response \(x\to u\);
- the \(u\)-attack from \(X\) has either no response or only
  \(p\to u\); and
- both possible moves land in \(H\), which misses \(r\).

The checker is not a search for a graph and does not re-prove C-010,
C-108, or C-150.  The discovery-only SAT script `probe_cases.py`
independently reports UNSAT at its tested orders, but those runs have no
proof certificates and are not used in the theorem.

## 6. Reproduction

From the campaign root:

```text
sh math/working/rank_one_remaining_endgame/verify_strict.sh
```

The script reruns the checker in isolated Python mode and requires an
exact byte match with `expected_result.json`.
