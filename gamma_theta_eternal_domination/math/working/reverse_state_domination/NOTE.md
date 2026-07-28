# Active exchanges have dominating reverse endpoints

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note proves an all-parameter static consequence of a dynamically
retained one-guard move.  Let \(i(G)=\alpha(G)=k\), and let
\(\mathcal F\) be any one-guard eternal family of dominating \(k\)-sets.
If \(u\) can answer an attack at \(x\) from a maximum independent
\(k\)-set, then replacing \(x\) by \(u\) in **every** maximum independent
\(k\)-set containing \(x\) produces a dominating set.

Under the campaign equality

\[
 \gamma(G)=\gamma^\infty(G)=k,
\]

the parameter chain gives \(i(G)=\alpha(G)=k\), so the theorem applies to
the literal greatest eternal family.  Every omitted reverse endpoint then
has positive finite deletion rank; it cannot be missing merely because it
is non-dominating.

The theorem does **not** prove that a reverse state survives in the
greatest family.  It therefore does not prove greatest-family
reciprocity, the gamma--theta conjecture at any parameter, or the
universal conjecture.

## 1. Family-relative activity

Fix distinct vertices \(u,x\).  Write

\[
 u\mathrel{\triangleright_{\mathcal F}}x
\tag{1.1}
\]

if some maximum independent \(k\)-set \(S\) containing \(u\) can answer
the unoccupied attack at \(x\) by moving \(u\), so

\[
 S-u+x\in\mathcal F.
\tag{1.2}
\]

This entails \(ux\in E(G)\), both because the guard must move along an
edge and because the successor must dominate the vacated vertex \(u\).

Every independent \(k\)-set belongs to every eternal \(k\)-family when
\(\alpha(G)=k\).  Indeed, start at any family state and attack the
currently unoccupied vertices of the independent set one at a time.  A
guard already installed on that independent set cannot move to a later
attacked vertex, so every attack permanently increases the number of its
occupied vertices.  The process ends at the independent set itself.

The accepted all-\(k\) C-108 vertex-star theorem now shows that (1.1) is
independent of the chosen maximum independent \(k\)-set containing \(u\):
if (1.2) holds for one such set, it holds for all of them.

## 2. The all-\(k\) theorem

### Theorem 2.1 (reverse endpoint domination) — PROVED

Let \(k\ge1\), let \(G\) satisfy

\[
 i(G)=\alpha(G)=k,
\tag{2.1}
\]

and let \(\mathcal F\) be a one-guard eternal family of dominating
\(k\)-sets.  Suppose

\[
 u\mathrel{\triangleright_{\mathcal F}}x.
\tag{2.2}
\]

Then for every maximum independent \(k\)-set \(J\) containing \(x\),

\[
 J-x+u
\tag{2.3}
\]

dominates \(G\).

#### Proof

For \(k=1\), the source singleton \(\{u\}\) is maximal independent and
therefore dominates \(G\); it is exactly the reverse set in (2.3).
Assume henceforth that \(k\ge2\).

Write

\[
 J=\{x\}\mathbin{\dot\cup}Q,
\qquad |Q|=k-1.
\tag{2.4}
\]

Because \(J\) is independent,

\[
 xq\notin E(G)\quad(q\in Q),
\qquad
 qq'\notin E(G)\quad(q\ne q'\in Q).
\tag{2.5}
\]

Suppose for a contradiction that

\[
 O=J-x+u=\{u\}\cup Q
\tag{2.6}
\]

does not dominate \(G\).  Choose a vertex \(r\) missed by \(O\).  Thus

\[
 ru\notin E(G),
\qquad
 rq\notin E(G)\quad(q\in Q).
\tag{2.7}
\]

The active move (2.2) gives \(ux\in E(G)\), so \(r\ne x\).  The maximum
independent set \(J\) is maximal and hence dominates \(r\).  Its members
in \(Q\) all miss \(r\) by (2.7), so

\[
 xr\in E(G).
\tag{2.8}
\]

The pair \(\{u,r\}\) is independent.  Extend it to a maximal independent
set.  The hypothesis \(i(G)=\alpha(G)=k\) says that every maximal
independent set has size exactly \(k\), so this extension has the form

\[
 I=\{u,r\}\mathbin{\dot\cup}A,
\qquad |A|=k-2.
\tag{2.9}
\]

The vertex \(x\) is not in \(I\), since it is adjacent to both \(u\) and
\(r\) by (2.2) and (2.8).  By C-108, the active response (2.2)
transports to \(I\), retaining

\[
 D=I-u+x=\{x,r\}\mathbin{\dot\cup}A\in\mathcal F.
\tag{2.10}
\]

Put

\[
 t=|A\cap Q|.
\tag{2.11}
\]

The state \(D\) initially occupies the \(t\) vertices of \(A\cap Q\).
Attack the remaining vertices of

\[
 Q-A
\tag{2.12}
\]

one at a time, in any order.  There are

\[
 |Q-A|=k-1-t
\tag{2.13}
\]

such attacks.

At every stage, the next target is unoccupied: it was not in \(A\), and
earlier moves landed only on earlier, distinct targets.  No guard at
\(x\) can answer, by (2.5), and no guard at \(r\) can answer, by (2.7).
Nor can a guard already occupying a vertex of \(Q\) answer, because
\(Q\) is independent.  Therefore every retained response must move a
guard from the as-yet-unmoved part of

\[
 A-Q.
\tag{2.14}
\]

Exactly one such guard is consumed by each successful attack.  But there
are only

\[
 |A-Q|=k-2-t
\tag{2.15}
\]

such guards, exactly one fewer than the targets in (2.13).  After they
have all moved, one vertex of \(Q-A\) remains unoccupied.  At the attack
on that final vertex, the \(k\) guards consist of \(x\), \(r\), and
\(k-2\) vertices of \(Q\).  Equations (2.5) and (2.7) say that none of
them is adjacent to the target.  There is no legal one-guard response,
contradicting eternal closure of \(\mathcal F\).

Thus \(O\) dominates \(G\). \(\square\)

### Corollary 2.2 (campaign equality and positive rank) — PROVED

Suppose

\[
 \gamma(G)=\gamma^\infty(G)=k
\tag{2.16}
\]

and let \(\mathcal K\) be the literal greatest eternal \(k\)-family.  If

\[
 u\mathrel{\triangleright_{\mathcal K}}x,
\tag{2.17}
\]

then \(J-x+u\) dominates for every maximum independent \(k\)-set \(J\)
containing \(x\).

If additionally

\[
 x\not\mathrel{\triangleright_{\mathcal K}}u,
\tag{2.18}
\]

then C-108 says that every such reverse state is outside \(\mathcal K\).
Theorem 2.1 says it is nevertheless dominating.  Hence it is deleted at
a positive finite round of the descending greatest-fixed-point
calculation.

#### Proof

The equality collapse gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k.
\]

Apply Theorem 2.1 with \(\mathcal F=\mathcal K\).  Under (2.18), C-108
makes \(J-x+u\notin\mathcal K\) for every maximum independent \(J\)
containing \(x\).  The full initial state space of the kernel calculation
is the family of all dominating \(k\)-sets, so a dominating state outside
the greatest fixed point has positive finite deletion rank. \(\square\)

## 3. Exact scope and proof consequence

Theorem 2.1 converts one half of the order-nine rank pattern into an
all-order theorem.  A surviving active exchange can never be paired with
a rank-zero reverse endpoint under equality.  The only possible failure
of greatest-family reciprocity has the form

\[
\text{survivor}\quad\text{versus}\quad\text{positive finite rank}.
\]

This is stronger than the earlier shared-pivot repair-square lemma, which
proved positive rank only after choosing a common nonneighbor of the
active edge.  No shared-pivot or parameter-three hypothesis is needed
here.

The remaining gap is genuinely coinductive.  Domination of all reverse
endpoints does not itself build a closed eternal family through them, and
finite deletion ranks on complementary configurations need not be equal.
Any proof of reciprocity must still construct a winning simulation,
produce a strict well-founded descent, or derive a forbidden smaller
dominating set.

## 4. Local \(k=3\) sanity check

`verify_local_core.py` exhausts the six-vertex specialization of the proof
at \(k=3\), including the possible identities between the completion
vertex and the two endpoint vertices.  It imposes only necessary local
domination and one-guard closure conditions and finds no surviving edge
assignment.

This is a finite sanity check of the smallest nontrivial specialization,
not a certificate for the all-\(k\) theorem.  The theorem is established
by the counting proof above.

Run from the campaign root:

```text
python3 -I -B -W error \
  math/working/reverse_state_domination/verify_local_core.py
```
