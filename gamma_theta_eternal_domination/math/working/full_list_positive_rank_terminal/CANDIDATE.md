# Positive-rank full-list terminals: rank drop and the exact residual obstruction

## Status and exact scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It uses
the standard one-guard-moves model: attacks are made only at unoccupied
vertices, exactly one adjacent guard moves, and a retained successor stays
in the same eternal family.

The package proves three limited advances beyond C-149 and C-157.

1. Every positive-rank terminal predecessor, at either C-149 gate, has a
   legal dominating unbanned response to its terminal attack of strictly
   smaller restricted rank.  Positive rank itself forces this; a
   nonsingleton palette is not needed.  At a corridor, each secondary
   palette color gives a specified legal alternate: if it dominates it
   has smaller rank, and otherwise it has the same private-witness
   structure found at rank zero in C-157.
2. At a minimum-rank retained terminal entry, a nonsingleton direct-root
   corridor is impossible.  Thus the direct-root part of the positive-rank
   problem can be bypassed completely.  At a minimum-rank nonroot corridor,
   every dominating secondary alternate must already be absent from the
   unrestricted greatest family.
3. Anchor restoration has a different and exact positive-rank form.  The
   alternate is forced to move the old terminal vertex to the attacked
   anchor.  It dominates, is unbanned, and has smaller rank, but need not
   be retained.  Whether the attacked anchor belongs to the terminal root
   palette is irrelevant to the move edge; a missing family incidence is
   never treated as a graph nonedge.

Combined with C-154, if all three restricted kernels are empty and one
chooses a minimum-rank terminal entry for each color, at least one chosen
entry is nonsingleton and is either a nonroot corridor or anchor
restoration.  At positive rank its compulsory lower-rank alternate is
already absent from the unrestricted greatest family; at rank zero the
accepted C-157 witness applies to a nonroot corridor, while rank-zero
anchor restoration remains open.

This does **not** prove that a restricted kernel survives, does not force a
minimum-rank predecessor to have rank zero, does not promote a lower-rank
state into the unrestricted greatest family, and does not prove the
\(k=3\) case or the gamma--theta conjecture.  No literature-priority claim
is made.

## 1. Setup and restricted rank

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples, and let

\[
 S=\{s_0,s_1,s_2\}\in\mathcal F^\star
\tag{1.2}
\]

be independent.  Fix a full target \(x\notin S\), so, for every
\(u\in S\),

\[
 ux\in E(G),\qquad S-u+x\in\mathcal F^\star.
\tag{1.3}
\]

Put

\[
 B=N_H(x)
\tag{1.4}
\]

and use the greatest-family root palette

\[
 Q(z)=L_S^{\mathcal F^\star}(z)
 =\{u\in S:uz\in E(G),\ S-u+z\in\mathcal F^\star\}.
\tag{1.5}
\]

For a fixed color \(u\in S\), ban

\[
 \mathcal B_u(x)=\{S-u+b:b\in B\}.
\tag{1.6}
\]

Let \(\Omega_0\) be all dominating triples outside this ban, and define
synchronously

\[
 \Omega_{j+1}=
 \left\{
 D\in\Omega_j:
 \begin{array}{l}
 \text{for every }z\notin D\text{ there is }g\in D\cap N_G(z)\\
 \text{such that }D-g+z\in\Omega_j
 \end{array}
 \right\}.
\tag{1.7}
\]

If \(D\in\Omega_j-\Omega_{j+1}\), write

\[
 \rho_u(D)=j.
\tag{1.8}
\]

An attack \(z\notin D\) witnessing \(D\notin\Omega_{j+1}\) is a
**deletion-witness attack** at \(D\).  Assume throughout the terminal
analysis that the restricted greatest kernel is empty.  Hence every state
of \(\Omega_0\) has a finite rank.

### Lemma 1.1 (one-step rank rule) — PROVED

Let \(\rho_u(D)=h\), and let \(z\) be a deletion-witness attack at \(D\).
If \(D'=D-g+z\) is a legal, dominating successor outside
\(\mathcal B_u(x)\), then

\[
 \boxed{\rho_u(D')<h.}
\tag{1.9}
\]

In particular, when \(h=0\), no legal successor to the witness attack can
both dominate and avoid the ban.

#### Proof

The state \(D'\) belongs to \(\Omega_0\).  Since \(z\) witnesses deletion
of \(D\) from \(\Omega_h\), no legal successor at \(z\) belongs to
\(\Omega_h\).  Therefore \(D'\) was deleted in a round strictly earlier
than \(h\), which is (1.9). \(\square\)

This elementary rule concerns the restricted peeling.  It does not imply
that \(D'\in\mathcal F^\star\).

### Lemma 1.2 (every positive-rank terminal has an alternate) — PROVED

Suppose \(\rho_u(T)=h>0\), and a deletion-witness attack at \(z\) has a
selected retained successor in \(\mathcal B_u(x)\).  Then the same attack
has a legal dominating successor

\[
 R\notin\mathcal B_u(x),\qquad \rho_u(R)<h.
\tag{1.10}
\]

#### Proof

Since \(h>0\), the state \(T\) survives the first peeling round and
belongs to \(\Omega_1\).  Thus every unoccupied attack at \(T\), including
the selected terminal attack at \(z\), has some legal successor in
\(\Omega_0\).  A banned state is excluded from \(\Omega_0\), so this
successor is different from the selected banned successor and is
unbanned and dominating.  Lemma 1.1 gives its strict rank drop. \(\square\)

This alternate belongs to the restricted initial state space, not
necessarily to \(\mathcal F^\star\).

## 2. Corridor terminals at arbitrary rank

C-149 says that a retained decreasing-rank trace can enter the ban through
a corridor.  Write

\[
 A=S-\{u\}.
\tag{2.1}
\]

The final predecessor and retained banned successor then have the form

\[
 T=A+q,\qquad
 E=A+r,\qquad
 q\to r,
\tag{2.2}
\]

where \(r\in B\), \(q\notin B\), the attack is at \(r\), and
\(T\in\mathcal F^\star-\mathcal B_u(x)\),
\(E\in\mathcal F^\star\cap\mathcal B_u(x)\).  The direct-root case is
\(q=u\), hence \(T=S\).  Otherwise \(q\notin S\cup B\cup\{x\}\), and
C-149 gives the corridor diamond

\[
 G[\{x,u,q,r\}]\cong K_4-xr.
\tag{2.3}
\]

The attack at \(r\) is assumed to be a deletion-witness attack at \(T\).

### Theorem 2.1 (positive-rank corridor dichotomy) — PROVED

Let \(h=\rho_u(T)\), and let

\[
 v\in Q(r)-\{u\}.
\tag{2.4}
\]

Define the secondary alternate

\[
 A_v=T-v+r.
\tag{2.5}
\]

Then \(v\to r\) is legal and \(A_v\notin\mathcal B_u(x)\).

1. If \(q=u\), then

   \[
   A_v=S-v+r\in\mathcal F^\star,
   \qquad
   \rho_u(A_v)<h.
\tag{2.6}
   \]

   Consequently a direct-root corridor with nonsingleton \(Q(r)\) has
   positive predecessor rank.

2. If \(q\ne u\), exactly one of the following holds.

   - The state \(A_v\) dominates \(G\), in which case

     \[
     \rho_u(A_v)<h.
\tag{2.7}
     \]

     Membership of \(A_v\) in \(\mathcal F^\star\) is not automatic.

   - The state \(A_v\) does not dominate \(G\).  Then there is a vertex
     \(w_v\) such that

     \[
     vw_v\in E(G),
     \qquad
     N_G[w_v]\cap A_v=\varnothing,
\tag{2.8}
     \]

     and

     \[
     w_v\notin S\cup\{x,q,r\}.
\tag{2.9}
     \]

     If \(Q(r)=S\), the two secondary colors have distinct witnesses.

3. Independently of \(Q(r)\), if \(h>0\), at least one anchor
   \(v\in A\) gives a legal dominating unbanned alternate \(A_v\) with
   \(\rho_u(A_v)<h\).  This anchor need not belong to \(Q(r)\).

#### Proof

Membership \(v\in Q(r)\) gives \(vr\in E(G)\), so the move in (2.5) is
legal.  Every banned state contains all of \(A=S-u\), whereas \(A_v\)
omits \(v\in A\).  Thus \(A_v\) is unbanned.

If \(q=u\), then \(T=S\), so (2.5) is exactly the retained root response
\(S-v+r\) from the definition of \(Q(r)\).  It dominates and belongs to
\(\mathcal F^\star\).  Lemma 1.1 gives (2.6).

Suppose \(q\ne u\).  If \(A_v\) dominates, Lemma 1.1 gives (2.7).
Otherwise choose \(w_v\) missed by \(A_v\).  The retained predecessor
\(T\) dominates, and

\[
 T-A_v=\{v\}.
\]

Therefore \(v\) must dominate \(w_v\).  The possibility \(w_v=v\) is
excluded because \(r\in A_v\) and \(vr\in E(G)\), proving (2.8).

The witness is not in \(A_v\), and hence is not \(q,r\), or the remaining
anchor in \(A-\{v\}\).  It is not \(v\), as just observed.  The corridor
diamond gives \(uq,xq\in E(G)\), while \(q\in A_v\), so the missed vertex
is neither \(u\) nor \(x\).  This proves (2.9).

If \(Q(r)=S\), let the two secondary colors be \(v\) and \(t\).  The
witness \(w_v\) misses \(t\in A_v\), whereas \(w_t\) is adjacent to \(t\)
by (2.8).  Thus \(w_v\ne w_t\).

Finally, suppose \(h>0\).  Lemma 1.2 supplies a dominating unbanned
alternate to the attack at \(r\).  The selected mover \(q\) leads to the
banned state \(E\), so the alternate mover must be one of the two anchors
in \(A\).  Its state is the corresponding \(A_v\), and Lemma 1.1 gives
the strict rank drop.  The move edge and domination do not imply
\(v\in Q(r)\), because that palette also requires a different root state
to belong to \(\mathcal F^\star\). \(\square\)

At \(h=0\), part 1 is impossible and every nonroot secondary alternate
falls into the witness branch.  Thus Theorem 2.1 recovers exactly the
corridor content of C-157.

## 3. Minimum-rank retained terminal entries

For the fixed color \(u\), consider every retained terminal entry into
\(\mathcal B_u(x)\) whose predecessor attack is a deletion witness.
This set is nonempty by the accepted C-149 retained descent.  Choose one
whose predecessor rank is minimum.

### Corollary 3.1 (direct-root bypass) — PROVED

At a minimum-rank retained terminal entry:

1. a direct-root corridor has

   \[
   Q(r)=\{u\};
\tag{3.1}
   \]

2. at a nonroot corridor, every \(v\in Q(r)-\{u\}\) has either a private
   witness (2.8)--(2.9), or \(A_v\) is a dominating state of smaller
   restricted rank that does **not** belong to \(\mathcal F^\star\);

3. if that nonroot predecessor has positive rank, at least one anchor,
   whether or not it lies in \(Q(r)\), gives a dominating smaller-rank
   alternate absent from \(\mathcal F^\star\).

#### Proof

Suppose first that the entry is direct-root and \(v\) is secondary.
Theorem 2.1 gives a retained unbanned state \(A_v\) with smaller rank.
Apply the accepted C-149 retained descent starting at \(A_v\).  Its final
predecessor is a retained terminal entry of rank at most
\(\rho_u(A_v)\), strictly smaller than the selected minimum.  This is a
contradiction, proving (3.1).

For a nonroot corridor, Theorem 2.1 gives the witness branch or a
dominating smaller-rank alternate.  If that alternate also belonged to
\(\mathcal F^\star\), the same retained-descent argument would produce a
smaller terminal predecessor.  Hence every dominating alternate in the
minimum-rank case is absent from \(\mathcal F^\star\).  If the predecessor
has positive rank, Theorem 2.1(3) guarantees that at least one such
dominating alternate exists.  This last alternate need not be indexed by
\(Q(r)\), but the same nonretention argument applies because it uses only
that the state is retained, unbanned, and lower-rank. \(\square\)

This is the strongest valid normalization supplied by rank alone.
Direct-root nonsingleton entries disappear, but a dominating
lower-rank nonroot alternate need not be retained and therefore cannot
automatically restart the C-149 trace.

## 4. Anchor restoration is a separate gate

Write

\[
 S=\{u,a,c\}.
\tag{4.1}
\]

An anchor-restoration terminal has

\[
 T=\{c,r,q\},\qquad
 E=\{a,c,r\}=S-u+r,
\tag{4.2}
\]

where the deletion-witness attack is at the unoccupied anchor \(a\), the
selected retained move is \(q\to a\), and \(r\in B\).

As at every retained terminal ban, \(u\in Q(r)\).

### Theorem 4.1 (positive-rank anchor restoration) — PROVED

If

\[
 h=\rho_u(T)>0,
\tag{4.3}
\]

then all of the following hold:

\[
 ar\in E(G),\qquad q\notin B,
\tag{4.4}
\]

\[
 R=T-r+a=\{a,c,q\}=S-u+q
\tag{4.5}
\]

is a legal dominating unbanned successor, and

\[
 \rho_u(R)<h.
\tag{4.6}
\]

The move and the rank drop do not require \(a\in Q(r)\).  At a
minimum-rank retained terminal entry, \(R\notin\mathcal F^\star\).

#### Proof

The guards of \(T\) are \(c,r,q\).  The selected response \(q\to a\)
leads to the banned state \(E\).  Since \(S\) is independent,
\(ca\notin E(G)\), so \(c\) cannot answer the attack at \(a\).

Because \(h>0\), Lemma 1.2 supplies a legal dominating unbanned alternate
to this same attack.  The only remaining guard that can move is \(r\).
Therefore \(ar\in E(G)\), and the alternate state is exactly (4.5).
That state has the banned shape \(S-u+q\), so its being unbanned is
equivalent to \(q\notin B\).  Lemma 1.1 gives (4.6).

If \(R\) belonged to \(\mathcal F^\star\) at a minimum-rank retained
terminal entry, the accepted C-149 descent from \(R\) would end at a
retained terminal predecessor of rank at most \(\rho_u(R)<h\), contrary
to the selected minimum. \(\square\)

At rank zero, any of the three failures

\[
 ar\notin E(G),\qquad q\in B,\qquad
 R\text{ is nondominating}
\tag{4.7}
\]

is compatible with the deletion-witness condition.  If \(ar\in E(G)\),
\(q\notin B\), and \(R\) is nondominating, the same private-witness
argument as before gives a vertex \(w\) with

\[
 rw\in E(G),\qquad N_G[w]\cap R=\varnothing,
\tag{4.8}
\]

where

\[
 w\notin\{a,c,q,r,x\};
\tag{4.9}
\]

the witness may equal \(u\).

Crucially, \(a\notin Q(r)\) does not imply \(ar\notin E(G)\).  The
palette condition also requires the root state \(S-a+r\) to be retained.
Theorem 4.1 uses the move edge forced by positive rank and makes no
negative graph inference from a missing family incidence.

## 5. Consequence for three empty kernels

Assume all three color-restricted kernels are empty.  For each
\(u\in S\), choose a retained terminal entry whose predecessor rank is
minimum for that color.

### Corollary 5.1 (minimum-terminal normal form) — PROVED

At least one of the three chosen terminal palettes is nonsingleton.  For
any chosen nonsingleton entry, the gate is not a direct-root corridor.
It is therefore one of the following.

1. **Rank-zero nonroot corridor.**  Every secondary palette color has a
   private missed witness as in (2.8)--(2.9).
2. **Positive-rank nonroot corridor.**  At least one anchor gives a
   dominating lower-rank alternate absent from
   \(\mathcal F^\star\).  Each secondary palette color separately gives
   either such a nonretained lower-rank alternate or a private witness.
3. **Rank-zero anchor restoration.**  The three failures in (4.7) remain
   possible.  In the subcase \(ar\in E(G)\), \(q\notin B\), and \(R\) is
   nondominating, (4.8)--(4.9) gives a private witness.
4. **Positive-rank anchor restoration.**  The unique possible alternate
   is the dominating unbanned lower-rank state (4.5), and it is absent
   from \(\mathcal F^\star\).

#### Proof

Each selected successor is a retained ban state
\(S-u+r_u\) with \(r_u\in B\) and \(u\in Q(r_u)\).  Theorem 3.1 of
C-154 is predecessor-independent and rules out three such states with
the respective palettes \(Q(r_u)=\{u\}\).  Thus at least one is
nonsingleton.  Corollary 3.1 excludes a direct-root corridor for every
such entry.  Splitting the remaining two gate types by rank and applying
Theorem 2.1, Corollary 3.1, and Theorem 4.1 gives the four exhaustive
alternatives. \(\square\)

This replaces the open phrase “positive-rank predecessor” by four exact
subbranches.  Rank alone closes none of them beyond the direct-root gate.

## 6. Exact controls and the obstruction boundary

The ordinary-bitmask verifier in this directory reconstructs three
controls directly from graph6, recomputes \(\gamma,\alpha,\gamma^\infty\),
and \(\theta\), reconstructs unrestricted and restricted greatest
kernels, and checks every named state, attack, palette, rank, ban, and
family-membership assertion.

### 6.1 Equality control: a genuine positive-rank anchor drop

For

```text
Ksv`f\knJVis
```

with \(S=\{1,2,3\}\), \(x=0\), and banned color \(u=1\), the verifier
recomputes

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
\]

The rank-one predecessor

\[
 T=\{3,5,8\}
\]

has a deletion-witness attack at \(2\).  The retained move \(5\to2\)
enters the ban at \(\{2,3,8\}\), whose palette is \(\{1,2\}\).
The secondary move \(8\to2\) reaches the retained unbanned state
\(\{2,3,5\}\) of rank zero.  Positive-rank anchor restoration is
therefore genuine even under equality, and the strict drop in
Theorem 4.1 can occur sharply.

### 6.2 Gamma-two boundary: lower rank need not mean retained

For MMV-006

```text
JEhbtj{rvf?
```

the verifier recomputes

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4).
\]

At \(S=\{4,5,10\}\), \(x=8\), and color \(u=4\), the rank-two nonroot
corridor predecessor \(\{0,5,10\}\) enters the ban by \(0\to9\).
The terminal palette is \(\{4,5\}\).  Its secondary alternate
\(\{0,9,10\}\) dominates and has restricted rank one, but it is absent
from \(\mathcal F^\star\).

This is not an equality counterexample because \(\gamma=2\).  It proves
that the inference

\[
 \text{dominating lower-rank alternate}
 \Longrightarrow
 \text{retained lower-rank alternate}
\]

is not a fixed-point or one-guard tautology.  Any theorem eliminating
this branch must use domination equality or another genuinely stronger
hypothesis.

### 6.3 Missing palette membership is not a missing move edge

For MMV-007

```text
JEhbtj{ruv?
```

the exact parameters are again \((2,3,3,4)\).  At
\(S=\{1,4,7\}\), \(x=9\), and color \(u=1\), the rank-one predecessor
\(\{6,7,10\}\) restores anchor \(4\) by \(6\to4\), entering the retained
ban state \(\{4,7,10\}\).  Its terminal palette is \(\{1,7\}\): the
secondary color is the other anchor \(7\), not the attacked anchor \(4\).
Nevertheless \(10\to4\) is a legal alternate, and it reaches the
retained unbanned state \(\{4,6,7\}\) of rank zero.

Again \(\gamma=2\), so this does not rule out an equality-specific
elimination.  It gives a concrete audit trap: missing the attacked anchor
from \(Q(10)\) cannot be converted into the graph nonedge \(4\,10\).
The missing palette entry says that a different root swap is not retained;
the physical move edge still exists.

Replay:

```text
python3 -I -B -W error \
  math/working/full_list_positive_rank_terminal/probe_positive_rank.py \
  --verify-controls
```

The proof uses absent family transitions only as absent family
transitions.  The only graph nonedges used are those from the independent
root, membership in \(B=N_H(x)\), or the defining property of a chosen
missed witness.

## 7. Exact remaining target

For the all-three-empty full-list branch, it is now enough to eliminate,
under \(\gamma=3\), the four cases in Corollary 5.1.  The highest-leverage
next statement is one of:

\[
\begin{array}{l}
\text{a compulsory dominating lower-rank alternate is retained;}\\
\text{or it forces a dominating pair;}\\
\text{or rank-zero anchor restoration is impossible.}
\end{array}
\]

The gamma-two controls show why each conclusion must use the full equality
hypothesis.  No such conclusion is asserted here.
