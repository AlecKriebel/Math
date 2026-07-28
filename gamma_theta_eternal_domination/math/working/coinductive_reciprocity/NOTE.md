# Coinductive normal form for greatest-family reciprocity

## Status and exact boundary

Date: 2026-07-28 (PDT)

Let \(G\) satisfy

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and let \(\mathcal K\) be the literal greatest eternal family of dominating
triples in the standard one-guard-moves model.  The universal
greatest-family reciprocity statement remains **OPEN**:

\[
 S-u+x\in\mathcal K
 \quad\stackrel{?}{\Longleftrightarrow}\quad
 T-x+u\in\mathcal K
\tag{0.2}
\]

for maximum independent triples \(S,T\), \(u\in S-T\), and \(x\in T-S\).
No counterexample to (0.2) is claimed here, and the gamma--theta conjecture
is not resolved.

This note proves a rigid normal form for any hypothetical failure of
(0.2).  Every one-sided active edge produces:

1. a nonempty \(G\)-clique of common nonneighbors;
2. a uniquely linked retained ridge over that clique;
3. domination of every complementary reverse state, closing the
   deletion-rank-zero base case;
4. an induced four-cycle carrying exactly two opposite one-sided active
   edges and two reciprocal edges; and
5. an external greatest-kernel blocker with one of two exact response-list
   types; and
6. in the nonadjacent-pivot paired-singleton branch, a third maximum
   independent base making four surrounding active pairs reciprocal.

The remaining gap is to show that the external blocker either produces a
strict descent among omitted-corner deletion ranks or yields a dominating
pair.  Neither conclusion is asserted below.

## 1. Active directed edges

For distinct vertices \(p,q\), write

\[
 p\mathrel{\triangleright}q
\tag{1.1}
\]

if a maximum independent triple \(I\) containing \(p\) can answer an attack
at \(q\) by moving \(p\), with

\[
 I-p+q\in\mathcal K.
\tag{1.2}
\]

The accepted C-108 vertex-star theorem makes (1.1) independent of the
chosen maximum independent triple containing \(p\).  Membership in (1.2)
also forces \(pq\in E(G)\): the successor must dominate the vacated vertex
\(p\), while the other two members of \(I\) are nonadjacent to \(p\).

The parameter chain in (0.1) gives

\[
 i(G)=3,
\tag{1.3}
\]

so every maximal independent set is a triple.  Every independent triple
belongs to every eternal triple-family.

## 2. The common-nonneighbor ridge

Assume

\[
 u\mathrel{\triangleright}x,
\qquad
 x\not\mathrel{\triangleright}u.
\tag{2.1}
\]

Put \(H=\overline G\) and

\[
 W=N_H(u)\cap N_H(x).
\tag{2.2}
\]

Equivalently, \(W\) is the set of vertices missed by the pair
\(\{u,x\}\) in \(G\).

### Lemma 2.1 (clique of missed vertices) — PROVED

The set \(W\) is nonempty and induces a clique in \(G\).

#### Proof

The pair \(\{u,x\}\) does not dominate because \(\gamma(G)=3\), so
\(W\ne\varnothing\).

Suppose distinct \(w,w'\in W\) were nonadjacent in \(G\).  Then both

\[
 \{u,w,w'\},
 \qquad
 \{x,w,w'\}
\tag{2.3}
\]

would be independent triples.  They therefore both belong to
\(\mathcal K\).  The second state can answer an attack at \(u\) by the
unique possible mover \(x\), producing the first state.  Thus
\(x\mathrel{\triangleright}u\), contrary to (2.1).  Hence every two
vertices of \(W\) are adjacent in \(G\). \(\square\)

### Lemma 2.2 (retained common-nonneighbor ridge) — PROVED

For every \(w\in W\),

\[
 R_w=\{u,x,w\}\in\mathcal K.
\tag{2.4}
\]

Moreover, if \(w,w'\in W\) are distinct, then the attack at \(w'\) from
\(R_w\) has the unique legal response

\[
 w\longrightarrow w',
\qquad
 R_w-w+w'=R_{w'}.
\tag{2.5}
\]

#### Proof

Extend the independent pair \(\{x,w\}\) to a maximal independent set.
By (1.3) it has the form

\[
 T=\{x,w,z\}.
\tag{2.6}
\]

Attack the unoccupied vertex \(u\).  The guard at \(w\) cannot respond
because \(w\in W\).  A response by \(x\) would produce
\(T-x+u\in\mathcal K\), contradicting
\(x\not\mathrel{\triangleright}u\).  Eternal closure therefore forces

\[
 z\longrightarrow u,
\qquad
 T-z+u=\{u,x,w\}=R_w\in\mathcal K.
\tag{2.7}
\]

In particular, \(uz\in E(G)\).

For (2.5), Lemma 2.1 gives \(ww'\in E(G)\), whereas both \(u\) and \(x\)
are nonadjacent to \(w'\) by (2.2).  Hence \(w\) is the unique guard that
can answer the attack.  The successor is \(R_{w'}\), already retained by
(2.4). \(\square\)

The symmetric completion statement will be used below:

\[
\begin{array}{ll}
\{x,w,z\}\text{ independent}&\Longrightarrow uz\in E(G),\\
\{u,w,a\}\text{ independent}&\Longrightarrow xa\in E(G).
\end{array}
\tag{2.8}
\]

The first line was proved in (2.7).  For the second, if \(xa\notin E(G)\),
then \(\{x,w,a\}\) would be independent.  The attack at \(u\) from that
state would be forced to move \(x\) to \(u\), again contradicting
\(x\not\mathrel{\triangleright}u\).

### Theorem 2.3 (every complementary reverse state dominates) — PROVED

Let

\[
 T=\{x,p,q\}
\tag{2.9}
\]

be any maximum independent triple containing \(x\).  Then

\[
 O_T=T-x+u=\{u,p,q\}
\tag{2.10}
\]

dominates \(G\), even though
\(x\not\mathrel{\triangleright}u\) implies
\(O_T\notin\mathcal K\).

#### Proof

Suppose that \(O_T\) misses a vertex \(r\).  Thus

\[
 ru,rp,rq\notin E(G).
\tag{2.11}
\]

The independent triple \(T\) dominates \(r\).  Its guards \(p,q\) miss
\(r\), so necessarily

\[
 rx\in E(G).
\tag{2.12}
\]

Extend the independent pair \(\{u,r\}\) to a maximal independent set.
By well-coveredness it has the form

\[
 I=\{u,r,a\}.
\tag{2.13}
\]

The active orientation \(u\triangleright x\) retains

\[
 D=I-u+x=\{x,r,a\}\in\mathcal K.
\tag{2.14}
\]

If \(a=p\), the state \(D=\{x,r,p\}\) misses \(q\), because
\(xq,rq,pq\notin E(G)\).  The case \(a=q\) is symmetric.  Hence

\[
 a\notin\{p,q\}.
\tag{2.15}
\]

The retained state \(D\) must dominate both \(p\) and \(q\).  The guards
\(x,r\) miss both vertices, by independence of \(T\) and (2.11).
Therefore

\[
 ap,aq\in E(G).
\tag{2.16}
\]

Now attack the unoccupied vertex \(p\) from \(D\).  Only \(a\) is adjacent
to \(p\), so the unique possible move is

\[
 a\longrightarrow p,
\qquad
 D-a+p=\{x,r,p\}.
\tag{2.17}
\]

But this successor misses \(q\), again because
\(xq,rq,pq\notin E(G)\).  It cannot be retained.  Thus \(D\) has no legal
answer to the attack at \(p\), contradicting
\(D\in\mathcal K\). \(\square\)

This theorem closes the rank-zero base case for **every** reverse state of
an inactive orientation, not only the shared-pivot corners constructed
below.  It is a two-attack consequence of eternal closure: domination
forces the temporary guard \(a\) to cover both \(p\) and \(q\), and moving
it to either one immediately exposes the other.

## 3. The five-state repair square

Fix \(w\in W\), and choose maximum independent completions

\[
 S=\{u,w,a\},
\qquad
 T=\{x,w,z\}.
\tag{3.1}
\]

The vertices \(a\) and \(z\) are distinct.  Indeed, if \(a=z\), then
\(S\) and \(T\) share two vertices and the two exchanged endpoint states
are simply \(T\) and \(S\), so both orientations are active.

Define

\[
\begin{array}{lll}
 D=\{x,w,a\},&
 O=\{u,w,z\},&
 R=\{u,x,w\},\\[2mm]
 P=\{a,z,w\}.&&
\end{array}
\tag{3.2}
\]

### Theorem 3.1 (repair-square normal form) — PROVED

Under (2.1), the four vertices \(u,x,a,z\) induce exactly the cycle

\[
 u-x-a-z-u
\tag{3.3}
\]

in \(G\).  The greatest family satisfies

\[
 S,T,D,R,P\in\mathcal K,
\qquad
 O\notin\mathcal K.
\tag{3.4}
\]

On the four cycle edges, the active relation is

\[
\begin{array}{c|c}
\text{edge}&\text{activity}\\ \hline
ux&u\triangleright x,\quad x\not\triangleright u,\\
az&z\triangleright a,\quad a\not\triangleright z,\\
xa&x\triangleright a,\quad a\triangleright x,\\
zu&z\triangleright u,\quad u\triangleright z.
\end{array}
\tag{3.5}
\]

Thus the original asymmetry propagates to the opposite edge, while the
other two cycle edges are reciprocal.

#### Proof

The endpoint states \(S,T\) are independent and hence retained.  The
definition \(u\triangleright x\) gives

\[
 D=S-u+x\in\mathcal K,
\tag{3.6}
\]

while \(x\not\triangleright u\) gives

\[
 O=T-x+u\notin\mathcal K.
\tag{3.7}
\]

We already know \(ux\in E(G)\).  Equation (2.8) gives

\[
 xa,uz\in E(G).
\tag{3.8}
\]

The state \(D\) must dominate \(z\).  Both \(x\) and \(w\) are
nonadjacent to \(z\), because \(T\) is independent.  Hence

\[
 az\in E(G).
\tag{3.9}
\]

The only possible response to an attack at \(z\) from \(D\) is therefore
\(a\to z\), and its successor is \(T\).

Now attack \(u\) from \(T\).  The responders allowed by graph adjacency
are \(x\) and \(z\).  The \(x\)-successor is the omitted state \(O\), so
closure forces \(z\to u\) and retains

\[
 R=T-z+u=\{u,x,w\}.
\tag{3.10}
\]

Likewise, attack \(z\) from \(S\).  The \(a\)-successor is \(O\), so
closure forces \(u\to z\) and retains

\[
 P=S-u+z=\{a,z,w\}.
\tag{3.11}
\]

Independence of \(S\) and \(T\) gives the two missing diagonals

\[
 ua,xz\notin E(G).
\tag{3.12}
\]

Equations (3.8)--(3.9) and (3.12) prove the induced cycle (3.3).

Finally, each active orientation in (3.5) is read from the corresponding
retained mixed state:

\[
\begin{array}{c|cc}
&\text{forward state}&\text{reverse state}\\ \hline
u,x&D&O\\
z,a&D&O\\
x,a&P&R\\
z,u&R&P.
\end{array}
\tag{3.13}
\]

For example, \(T-z+a=D\) proves \(z\triangleright a\), while
\(S-a+z=O\notin\mathcal K\) proves
\(a\not\triangleright z\).  The other entries follow identically.
\(\square\)

### Corollary 3.2 (exact response-list polarization) — PROVED

With family-response lists based at \(S,T\),

\[
\begin{array}{c|cc}
&S&T\\ \hline
\text{target }x\text{ or }u&
L_S(x)=\{u,a\}&L_T(u)=\{z\}\\
\text{target }z\text{ or }a&
L_S(z)=\{u\}&L_T(a)=\{x,z\}.
\end{array}
\tag{3.14}
\]

Here the first entry in a row is the target for the \(S\)-column and the
second is the target for the \(T\)-column.

#### Proof

The four sets in (3.14) are exactly the four pairs of successor states in
(3.13), together with the graph nonadjacencies forced by independence of
\(S\) and \(T\). \(\square\)

## 4. Reduction of arbitrary endpoint pairs

### Theorem 4.1 (every failure has a shared-pivot square) — PROVED

If greatest-family complementary-exchange reciprocity fails anywhere
under (0.1), then it has a representation satisfying Theorem 3.1 for
every choice of

\[
 w\in N_H(u)\cap N_H(x)
\tag{4.1}
\]

and every pair of maximum-independent completions (3.1).

#### Proof

A failed complementary exchange gives an active orientation
\(u\triangleright x\) without \(x\triangleright u\), by C-108.  The pair
\(\{u,x\}\) is not dominating, so choose \(w\) from (4.1).  Each of the
independent pairs \(\{u,w\}\) and \(\{x,w\}\) extends to a maximal
independent set, and (1.3) makes both completions triples.  If their third
vertices coincided, the two independent triples would share a ridge and
both orientations would be retained.  Therefore they are distinct, and
Theorem 3.1 applies. \(\square\)

This reduces the all-pairs statement, including disjoint original
endpoints, to a rank-two exchange system over one shared pivot.

## 5. The exact greatest-kernel blocker

Retain the notation of Theorem 3.1.  First, the omitted state cannot fail
merely because it is non-dominating.

\[
 O=\{u,w,z\}
\tag{5.1}
\]

### Lemma 5.1 (the omitted corner dominates) — PROVED

The configuration \(O\) dominates \(G\).  Consequently its
greatest-kernel deletion rank is positive rather than zero.

#### Proof

Suppose a vertex \(r\) were undominated by \(O\).  Then \(r\) is
nonadjacent to each of \(u,w,z\).  In particular,

\[
 S_r=\{u,w,r\}
\tag{5.2}
\]

is an independent triple, hence a retained maximum independent state.
The active edge \(u\triangleright x\) then retains

\[
 D_r=S_r-u+x=\{x,w,r\}.
\tag{5.3}
\]

The state \(D_r\) must dominate \(z\).  But \(xz,wz\notin E(G)\) because
\(T=\{x,w,z\}\) is independent.  Therefore \(rz\in E(G)\), contradicting
the assumption that \(r\) is undominated by \(O\). \(\square\)

The internal unoccupied vertices \(x\) and \(a\) of \(O\)
already have retained responses:

\[
 x:u\to T,
\qquad
 a:z\to S.
\tag{5.4}
\]

Because \(\mathcal K\) is the greatest fixed point and \(O\notin\mathcal K\),
there is therefore some

\[
 r\notin\{u,x,w,a,z\}
\tag{5.5}
\]

such that no legal response to \(r\) from \(O\) has its successor in
\(\mathcal K\).  Lemma 5.1 ensures that at least one guard of \(O\) is
adjacent to \(r\), so this is a genuine losing attack rather than a
failure of domination.

The three forbidden possible successors are

\[
 O-u+r=\{r,w,z\},\qquad
 O-w+r=\{u,r,z\},\qquad
 O-z+r=\{u,w,r\}.
\tag{5.6}
\]

### Lemma 5.2 (blocker-list dichotomy) — PROVED

For the family-response lists at \(r\),

\[
 a\notin L_S(r),
\qquad
 x\notin L_T(r),
\tag{5.7}
\]

and exactly one of the following holds:

1. **shared-pivot active:** \(w\in L_S(r)\cap L_T(r)\);
2. **paired singletons:**
   \[
   L_S(r)=\{u\},
   \qquad
   L_T(r)=\{z\}.
\tag{5.8}
   \]

#### Proof

The \(a\)-successor from \(S\) is \(O-z+r\), while the \(x\)-successor
from \(T\) is \(O-u+r\).  Both are excluded by (5.6), proving (5.7).

The shared guard \(w\) belongs to \(L_S(r)\) if and only if it belongs to
\(L_T(r)\), by C-108.  If it belongs to both, item 1 holds.  Otherwise it
belongs to neither.  Eternal closure makes each response list nonempty;
after (5.7), the only remaining positions are respectively \(u\) and
\(z\).  This gives (5.8). \(\square\)

The same exclusions also force the retained mixed states \(R\) and \(P\)
to answer the attack at \(r\) without moving \(x\) and \(a\), respectively.
This duplicates the two sides of Lemma 5.2 but does not yet force one of
the forbidden states (5.6).

### Lemma 5.3 (minimum-rank blocker adjacency) — PROVED

Let \(\mathcal K_0\) be the set of dominating triples and define
\(\mathcal K_{j+1}\) to consist of the states in \(\mathcal K_j\) having,
for every unoccupied attack, a one-edge successor in \(\mathcal K_j\).
Give every non-dominating triple rank zero and every dominating triple
in \(\mathcal K_{h-1}-\mathcal K_h\) rank \(h\).  The stable intersection
is \(\mathcal K\).

Among all omitted corners supplied by Theorem 3.1, choose \(O\) with
minimum rank \(h\).  Let \(r\) be an attack deleting \(O\) at round \(h\).
Then:

\[
\begin{array}{rcl}
ur\in E(G)&\Longrightarrow&wr\in E(G)\text{ or }ar\in E(G),\\
wr\in E(G)&\Longrightarrow&
ur\in E(G)\text{ or }xr\in E(G)\text{ or }zr\in E(G),\\
zr\in E(G)&\Longrightarrow&xr\in E(G)\text{ or }wr\in E(G).
\end{array}
\tag{5.9}
\]

#### Proof

Every legal successor of the deleting attack has rank strictly below
\(h\).

Suppose first that \(ur\in E(G)\) while
\(wr,ar\notin E(G)\).  Then

\[
 J=\{a,w,r\}
\tag{5.10}
\]

is independent.  The opposite one-sided edge from Theorem 3.1 is

\[
 z\triangleright a,
\qquad
 a\not\triangleright z.
\tag{5.11}
\]

Therefore

\[
 J-a+z=\{r,w,z\}=O-u+r
\tag{5.12}
\]

is another omitted repair-square corner.  It is a legal successor of the
deleting attack, so its rank is below \(h\), contradicting the choice of
\(O\).  Lemma 5.1 excludes rank zero for this new corner.

Next suppose \(wr\in E(G)\) while \(ur,xr,zr\notin E(G)\).  Then

\[
 J=\{x,z,r\}
\tag{5.13}
\]

is independent.  Here \(r\) is a common nonneighbor of \(u,x\), so the
original inactive orientation gives the shared-pivot omitted corner

\[
 J-x+u=\{u,z,r\}=O-w+r.
\tag{5.14}
\]

This is again a lower-rank omitted corner, a contradiction.

Finally, if \(zr\in E(G)\) while \(xr,wr\notin E(G)\), then
\(\{x,w,r\}\) is independent and

\[
 \{x,w,r\}-x+u=\{u,w,r\}=O-z+r
\tag{5.15}
\]

is a lower-rank omitted corner.  This gives the third implication.
\(\square\)

Combining Lemmas 5.2 and 5.3 gives a finite local endgame for a
minimum-rank failure.  In the paired-singleton branch,

\[
 ur,zr\in E(G),
\tag{5.16}
\]

so (5.9) forces

\[
 (wr\lor ar)\ \land\ (xr\lor wr).
\tag{5.17}
\]

In the shared-pivot-active branch \(wr\in E(G)\), and (5.9) forces

\[
 ur\in E(G)\text{ or }xr\in E(G)\text{ or }zr\in E(G).
\tag{5.18}
\]

### Lemma 5.4 (paired-singleton, nonadjacent-pivot propagation) — PROVED

Keep the minimum-rank choice of Lemma 5.3.  Suppose the blocker is in the
paired-singleton branch of Lemma 5.2 and

\[
 wr\notin E(G).
\tag{5.19}
\]

Then

\[
 ur,zr,ar,xr\in E(G).
\tag{5.20}
\]

For every maximum independent completion

\[
 U=\{r,w,c\},
\tag{5.21}
\]

closure at the attacks \(x\) and \(a\) is forced to use \(c\):

\[
\begin{array}{lll}
x:&c\longrightarrow x,&U-c+x=\{r,w,x\}\in\mathcal K,\\
a:&c\longrightarrow a,&U-c+a=\{r,w,a\}\in\mathcal K.
\end{array}
\tag{5.22}
\]

In particular,

\[
 c\triangleright x,
\qquad
 c\triangleright a.
\tag{5.23}
\]

#### Proof

The paired-singleton lists give \(ur,zr\in E(G)\).  Under (5.19), the
first and third implications of (5.9) force \(ar,xr\in E(G)\), proving
(5.20).

The pair \(\{r,w\}\) is independent and therefore extends, by
well-coveredness, to a triple \(U\) as in (5.21).  Consider its attack at
\(x\).  The guard at \(w\) is nonadjacent to \(x\).  If the guard at \(r\)
had a retained response, then

\[
 r\triangleright x.
\tag{5.24}
\]

But Lemma 5.2 gives \(x\notin L_T(r)\), so C-108 gives
\(x\not\triangleright r\).  The complementary omitted corner based at
\(T=\{x,w,z\}\) would then be

\[
 T-x+r=\{r,w,z\}=O-u+r.
\tag{5.25}
\]

This is a legal lower-rank successor of the deleting attack because
\(ur\in E(G)\), contradicting the minimum choice of \(O\).  Therefore
\(r\) cannot answer at \(x\).  Eternal closure forces \(c\to x\), and its
successor is the first state in (5.22).

The argument at \(a\) is symmetric.  Lemma 5.2 gives
\(a\not\triangleright r\).  A retained response \(r\to a\) would make

\[
 S-a+r=\{u,w,r\}=O-z+r
\tag{5.26}
\]

a lower-rank omitted corner; this is a legal successor because
\(zr\in E(G)\).  Hence closure forces \(c\to a\), giving the second state
in (5.22). \(\square\)

These caps are a genuine rank descent: they compare only the omitted
corner with its strictly lower-rank successors and do not assert the false
equality of complementary deletion ranks.  What remains is to eliminate
the adjacency patterns (5.17)--(5.18), or to show that each produces a
different lower-rank corner.

### Lemma 5.5 (third-base reciprocal completion) — PROVED

Under the hypotheses of Lemma 5.4, put

\[
 A_r=\{r,w,z\}=O-u+r,
 \qquad
 C_r=\{u,w,r\}=O-z+r.
\tag{5.27}
\]

Then

\[
 A_r,C_r\notin\mathcal K.
\tag{5.28}
\]

For every maximum independent completion

\[
 U=\{r,w,c\},
\tag{5.29}
\]

the two further states

\[
 \{u,w,c\},\qquad \{z,w,c\}
\tag{5.30}
\]

belong to \(\mathcal K\).  Consequently the following four active pairs
are reciprocal:

\[
 \boxed{
 r\leftrightarrow u,\qquad
 r\leftrightarrow z,\qquad
 c\leftrightarrow a,\qquad
 c\leftrightarrow x.
 }
\tag{5.31}
\]

#### Proof

The blocker \(r\) deletes \(O\) at its finite greatest-kernel rank.
Lemma 5.4 gives

\[
 ur,zr\in E(G).
\tag{5.32}
\]

Thus \(A_r\) and \(C_r\) are legal successors of the deleting attack.
By the definition of a deleting attack neither successor belongs to
\(\mathcal K\), proving (5.28).

The state \(U\) is an independent triple and hence belongs to
\(\mathcal K\).  Attack the unoccupied vertex \(u\).  The guard \(w\)
cannot answer because \(uw\notin E(G)\).  A move \(c\to u\), if its graph
edge exists, has successor

\[
 U-c+u=C_r\notin\mathcal K.
\]

The edge \(ru\in E(G)\) from (5.32) leaves one possible retained answer.
Closure therefore forces

\[
 r\to u,\qquad U-r+u=\{u,w,c\}\in\mathcal K.
\tag{5.33}
\]

The attack at \(z\) is symmetric.  Here \(wz\notin E(G)\), a possible
\(c\)-move lands in \(A_r\notin\mathcal K\), and \(rz\in E(G)\).
Therefore

\[
 r\to z,\qquad U-r+z=\{z,w,c\}\in\mathcal K.
\tag{5.34}
\]

The paired-singleton responses give

\[
 S-u+r=\{r,w,a\}\in\mathcal K,\qquad
 T-z+r=\{r,w,x\}\in\mathcal K.
\tag{5.35}
\]

Equations (5.33)--(5.35), read from the independent bases \(S,T,U\),
prove both directions of \(r\leftrightarrow u\) and
\(r\leftrightarrow z\).  Lemma 5.4 already proves
\(c\triangleright a\) and \(c\triangleright x\).  Their reverse
directions follow from

\[
 S-a+c=\{u,w,c\}\in\mathcal K,\qquad
 T-x+c=\{z,w,c\}\in\mathcal K.
\tag{5.36}
\]

Every active direction in (5.31) is thus witnessed from a maximum
independent base.  No equality of deletion ranks is used. \(\square\)

The lemma turns the hardest nonadjacent-pivot paired-singleton blocker
into a rigid three-base exchange system.  It does not yet force the
missing corner \(O\), eliminate the shared-pivot-active branch, or
establish greatest-family reciprocity.

## 6. Why this is not yet reciprocity

One stronger coinductive simulation is already false.  It is not true that
an active edge \(u\triangleright x\) permits replacing \(x\) by \(u\) in
**every** greatest-family state containing \(x\).  A dependent replay of
the accepted complete order-nine equality census tested 220,086 such
whole-kernel transforms and found 4,108 failures.  The first is
`HCOeuqr`: \(3\triangleright7\) is active and `057` survives, but replacing
7 by 3 gives the non-dominating state `035`.

This does not refute complementary-exchange reciprocity.  That statement
only replaces \(x\) inside a maximum independent endpoint state.  The
observation rules out even the weaker premise that every such translated
kernel state merely dominates, and hence rules out proving reciprocity by
a global statewise substitution map on \(\mathcal K\).  On the sharp
greatest-family boundary graph `GEjbug`, where
\((\gamma,\alpha,\gamma^\infty)=(2,3,3)\), the asymmetric active edge
\(0\triangleright4\) has four further non-dominating translations:

\[
134\mapsto013,\qquad
147\mapsto017,\qquad
347\mapsto037,\qquad
457\mapsto057.
\tag{6.1}
\]

The special complementary reverse state `035` in that graph does dominate
but is deleted at rank one.  This contrast is exactly why Theorem 2.3 is
restricted to maximum-independent endpoints rather than arbitrary kernel
states.

A second tempting rank shortcut also fails without using the forward-active
hypothesis.  One might hope that, whenever \(x\not\triangleright u\), the
minimum deletion rank among all reverse states \(T-x+u\) is attained by an
endpoint \(T\) containing a common nonneighbor of \(u,x\).  Such an
endpoint would furnish a shared-pivot square and would let the minimum-rank
argument use the stronger middle implication
\[
 wr\in E(G)\Longrightarrow xr\in E(G)\text{ or }zr\in E(G).
\tag{6.2}
\]
A dependent complete-order-nine replay refutes this unconditional
surrogate 422 times among 16,366 inactive oriented edges.  The first
control is ``HCOe`Z{`` with \((u,x)=(8,0)\): the reverse ranks over all
five maximum-independent endpoints containing \(x\) are
\[
 1,1,2,0,0,
\tag{6.3}
\]
whereas the sole shared-pivot endpoint has rank \(2\).

By C-138 there is no genuinely one-sided active edge in the order-nine
equality census, so this does **not** refute a transport theorem that uses
both \(u\triangleright x\) and \(x\not\triangleright u\).  It does show
that inactivity alone cannot justify moving the minimum-rank choice from
an arbitrary reverse state to a shared-pivot corner.  This is the exact
reason the middle implication in Lemma 5.3 retains the additional
alternative \(ur\in E(G)\).

The repair square is locally closed without its sixth corner.  Indeed, the
five states

\[
 S,T,D,R,P
\tag{6.4}
\]

answer every attack at one of the other four displayed cycle vertices
without using \(O\).  Consequently the missing corner must be repaired
using the external blocker \(r\), not by a purely four-cycle argument.

The equality graph `FCXfO` and the accepted sixteen-state proper eternal
family give a sharp control:

\[
\begin{gathered}
 u=1,\quad x=4,\quad w=0,\quad a=2,\quad z=5,\\
 S=012,\quad T=045,\quad
 D=024,\quad O=015,\quad R=014,\quad P=025.
\end{gathered}
\tag{6.5}
\]

That proper family contains all five states in (6.4) and omits \(O\).
Its blocker is the attack at \(3\), which is of the shared-pivot-active
type.  The literal greatest family of `FCXfO` adds both `015` and `135`,
restoring reciprocity.  Thus Theorem 3.1 is sharp for an arbitrary eternal
family and cannot itself be promoted to the open greatest-family theorem.

The remaining proposed descent is:

> choose a blocker for \(O\) at its positive finite greatest-kernel deletion
> rank; use Lemma 5.2 and the five survivor states to produce a new repair square
> whose omitted corner is one of the strictly lower-rank successors in
> (5.6), or else produce a dominating pair.

This would be well founded without requiring the false equal-rank
induction refuted by C-137.  The required mapping from every blocker type
to a lower-rank omitted corner has not been proved.  It remains the exact
coinductive gap.
