# The mixed \(P_4\) after the external witness: saturation and a forced \(C_5\)

## Status

Date: 2026-07-26 (PDT)

This note continues `k3_mixed_p4_attack.md` under

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and for an **arbitrary specified** eternal three-family
\(\mathcal F\).  The family is never assumed to be greatest.  The exact
family-response lists at the independent state \(S=\{a,b,c\}\) are

\[
\begin{array}{c|cccc}
x&x_0&x_1&x_2&x_3\\ \hline
L_S^{\mathcal F}(x)&
\{a\}&\{a,c\}&\{b,c\}&\{b\},
\end{array}
\tag{0.1}
\]

and \(x_0x_1x_2x_3\) is an induced path in \(H=\overline G\).
Thus

\[
x_0x_1,x_1x_2,x_2x_3\notin E(G),\qquad
x_0x_2,x_0x_3,x_1x_3\in E(G).
\tag{0.2}
\]

Every attack below is explicitly at an unoccupied vertex.  Every displayed
response moves exactly one occupied guard along one edge.  A successor is
rejected only because it is a named absent direct swap, it violates the
accepted arbitrary-state restoration lemma, or it fails domination.

The main new theorem is that the mixed path forces an external clique \(Z\)
whose every vertex closes the path to an induced complement \(C_5\).  The
external witness clique \(W\) from the preceding note also satisfies
strictly stronger response and adjacency constraints than were previously
recorded.

## 1. Reusable restoration filter

For every \(D\in\mathcal F\), the accepted restoration lemma gives

\[
 S-D\subseteq\bigcup_{v\in D-S}L_S^{\mathcal F}(v).
\tag{1.1}
\]

We also use the following point about negative list entries.  If
\(S-u+x\in\mathcal F\), that state must dominate the missing vertex \(u\).
No member of \(S-\{u\}\) is adjacent to \(u\), because \(S\) is
independent.  Hence \(xu\in E(G)\), and therefore

\[
 S-u+x\in\mathcal F\quad\Longleftrightarrow\quad
 u\in L_S^{\mathcal F}(x).
\tag{1.2}
\]

The forward implication supplies the graph edge from domination; the
reverse implication is the definition of the family list.  Thus a negative
list entry really does exclude the corresponding one-swap **state**, even
when the missing edge was not known in advance.

We repeatedly use the following immediate exclusions:

\[
\begin{array}{c|c|c}
D&S-D&\displaystyle\bigcup_{v\in D-S}L_S(v)\\ \hline
\{c,x_2,x_3\}&\{a,b\}&\{b,c\}\\
\{c,x_0,x_1\}&\{a,b\}&\{a,c\}\\
\{b,x_0,x_3\}&\{a,c\}&\{a,b\}.
\end{array}
\tag{1.3}
\]

None of the three states in (1.3) belongs to \(\mathcal F\).

The positive entries in (0.1) put the six one-swap states in
\(\mathcal F\).  In particular,

\[
 A_0=\{b,c,x_0\}\in\mathcal F.
\tag{1.4}
\]

Starting from \(S\), attack the unoccupied vertex \(x_0\).  Exactness of
\(L_S(x_0)=\{a\}\) says that the only retained response is
\(a\to x_0\), giving \(A_0\).

Now attack the unoccupied vertex \(x_2\) from \(A_0\).  All three guards
are adjacent to \(x_2\): the edges \(bx_2,cx_2\) come from (0.1), and
\(x_0x_2\) comes from (0.2).  The response \(x_0\to x_2\) would give

\[
 \{b,c,x_2\}=S-a+x_2\notin\mathcal F
\tag{1.5}
\]

because \(a\notin L_S(x_2)\).  Therefore every retained response to this
attack has one of the two shapes

\[
 D_c=\{c,x_0,x_2\}\quad(b\to x_2),\qquad
 D_b=\{b,x_0,x_2\}\quad(c\to x_2).
\tag{1.6}
\]

Closure requires at least one of \(D_c,D_b\) to lie in \(\mathcal F\).
This two-branch fork is the engine for the next three lemmas.

## 2. The original witness clique is response-saturated

Put

\[
 W=N_H(x_1)\cap N_H(x_2).
\tag{2.1}
\]

The preceding accepted note proves that \(W\ne\varnothing\), \(G[W]\) is a
clique, and

\[
 T_w=\{w,x_1,x_2\}\in\mathcal F
\tag{2.2}
\]

is an independent state for every \(w\in W\).

### Lemma 2.1 (both end colors respond at every witness) — PROVED

For every \(w\in W\),

\[
 \boxed{\{a,b\}\subseteq L_S^{\mathcal F}(w).}
\tag{2.3}
\]

Consequently \(aw,bw\in E(G)\), and both

\[
 \{b,c,w\},\qquad \{a,c,w\}
\tag{2.4}
\]

belong to the same specified family \(\mathcal F\).  The only remaining
possibilities are

\[
 L_S(w)=\{a,b\}\quad\text{or}\quad L_S(w)=\{a,b,c\}.
\tag{2.5}
\]

#### Proof

Fix \(w\in W\) and suppose first that \(a\notin L_S(w)\).  Use the
unoccupied attacks \(x_0,x_2\) from \(S,A_0\) described in Section 1.

If the \(x_2\)-attack retains \(D_c=\{c,x_0,x_2\}\), attack the
unoccupied vertex \(w\).  The guard at \(x_2\) cannot respond because
\(wx_2\notin E(G)\).  There are at most two response shapes:

1. \(c\to w\) gives \(\{w,x_0,x_2\}\), which does not dominate \(x_1\),
   since \(wx_1,x_0x_1,x_2x_1\notin E(G)\);
2. \(x_0\to w\) gives \(\{c,w,x_2\}\), which violates restoration:
   the missing positions are \(a,b\), while
   \[
   L_S(w)\cup L_S(x_2)
   \subseteq \{b,c\}.
   \]

If the \(x_2\)-attack instead retains
\(D_b=\{b,x_0,x_2\}\), attack the unoccupied vertex \(w\) again.
The guard at \(x_2\) still cannot respond.  The response \(b\to w\) gives
the same nondominating state \(\{w,x_0,x_2\}\); the response
\(x_0\to w\) gives \(\{b,w,x_2\}\), whose outside lists again omit the
missing position \(a\).  Thus neither branch in (1.6) can answer \(w\),
contradicting closure.  Hence \(a\in L_S(w)\).

Apply the reflection

\[
 a\leftrightarrow b,\qquad
 x_0\leftrightarrow x_3,\qquad
 x_1\leftrightarrow x_2,\qquad c\mapsto c
\tag{2.6}
\]

to the same argument.  It proves \(b\in L_S(w)\).  Every positive
family-list membership includes the corresponding graph edge and direct
successor, proving (2.3)--(2.5). \(\square\)

### Lemma 2.2 (the witnesses see both path ends) — PROVED

For every \(w\in W\),

\[
 \boxed{wx_0,wx_3\in E(G).}
\tag{2.7}
\]

#### Proof

Suppose \(wx_0\notin E(G)\).  At either possible state in (1.6), attack
the unoccupied vertex \(x_1\).  From \(D_c\), the guards at \(x_0,x_2\)
are nonadjacent to \(x_1\), so the unique possible response is
\(c\to x_1\).  From \(D_b\), the only possible response is \(b\to x_1\)
(and if \(bx_1\) is absent, there is no response at all).  In either
retained branch the successor must be

\[
 E=\{x_0,x_1,x_2\}.
\tag{2.8}
\]

But \(E\) does not dominate \(w\): by the supposition and the definition
of \(W\), all three of \(x_0,x_1,x_2\) miss \(w\).  Thus neither branch
in (1.6) can answer \(x_1\), contradicting closure.  Therefore
\(wx_0\in E(G)\).  Reflection (2.6) proves \(wx_3\in E(G)\).
\(\square\)

### Lemma 2.3 (uniform endpoint response roles) — PROVED

There are nonempty role sets

\[
 I_0\subseteq\{\mathrm{witness},x_2\},\qquad
 I_3\subseteq\{\mathrm{witness},x_1\},
\tag{2.9}
\]

independent of the choice of \(w\in W\), such that

\[
\begin{split}
 L_{T_w}^{\mathcal F}(x_0)
  &=\{w:\mathrm{witness}\in I_0\}
    \cup\{x_2:x_2\in I_0\},\\
 L_{T_w}^{\mathcal F}(x_3)
  &=\{w:\mathrm{witness}\in I_3\}
    \cup\{x_1:x_1\in I_3\}.
\end{split}
\tag{2.10}
\]

If the witness role occurs at \(x_0\), its successor is the common state
\(\{x_0,x_1,x_2\}\); if the \(x_2\)-role occurs, its successor is
\(\{w,x_0,x_1\}\).  The symmetric statements hold at \(x_3\).

#### Proof

At \(T_w\), the attack at \(x_0\) is unoccupied.  The guard at \(x_1\)
cannot move because \(x_0x_1\notin E(G)\), so the only possible guards are
\(w,x_2\).  Lemma 2.2 and (0.2) make both graph moves legal, although one
or both successors may be absent from the specified family.

For distinct \(w,z\in W\), ridge covariance between the independent states
\(T_w,T_z\) transports the entire response list by \((w\ z)\), while
fixing \(x_0,x_1,x_2\).  Thus the two response roles occur uniformly over
all \(w\).  Closure makes the role set nonempty.  The proof at \(x_3\) is
identical.  Every attack is outside \(T_w\), and every successor replaces
exactly the displayed guard. \(\square\)

Lemma 2.3 does **not** prove that both roles occur.  That ambiguity survives
the present attack.

## 3. Path-end saturation and a forced co-state ridge

### Lemma 3.1 (the middle color sees both ends) — PROVED

\[
 \boxed{cx_0,cx_3\in E(G).}
\tag{3.1}
\]

#### Proof

It suffices by reflection (2.6) to prove \(cx_3\in E(G)\).  Suppose
otherwise and use the fork (1.6).

From \(D_c=\{c,x_0,x_2\}\), attack the unoccupied vertex \(x_3\).
The guards at \(c,x_2\) are nonadjacent to \(x_3\) under the supposition
and (0.2), so the unique possible move is \(x_0\to x_3\).  Its successor
is \(\{c,x_2,x_3\}\), the first restoration-forbidden state in (1.3).
Hence \(D_c\) cannot be retained.

From \(D_b=\{b,x_0,x_2\}\), attack the unoccupied vertex \(x_1\).
The guards at \(x_0,x_2\) miss \(x_1\), so a response, if one exists, is
uniquely \(b\to x_1\), producing \(E=\{x_0,x_1,x_2\}\).
Now attack the unoccupied vertex \(c\).  There are at most three response
shapes:

1. \(x_2\to c\) gives \(\{c,x_0,x_1\}\), forbidden by (1.3);
2. \(x_1\to c\) gives \(D_c\), which has just been shown unable to answer
   \(x_3\);
3. \(x_0\to c\), if \(cx_0\in E(G)\), gives
   \(\{c,x_1,x_2\}\).  Attack the unoccupied vertex \(x_3\) there.
   Under \(cx_3\notin E(G)\), only \(x_1\to x_3\) can respond, again
   producing the forbidden state \(\{c,x_2,x_3\}\).

Thus \(D_b\) also cannot be retained.  This contradicts the required
response to the \(x_2\)-attack at \(A_0\).  Hence \(cx_3\in E(G)\), and
reflection proves \(cx_0\in E(G)\). \(\square\)

### Lemma 3.2 (three states on the end ridge) — PROVED

The following three configurations all belong to \(\mathcal F\):

\[
\boxed{
 R_c=\{c,x_0,x_3\},\qquad
 R_1=\{x_0,x_1,x_3\},\qquad
 R_2=\{x_0,x_2,x_3\}.
}
\tag{3.2}
\]

#### Proof

Start at \(A_0=\{b,c,x_0\}\) and attack the unoccupied vertex \(x_3\).
The three possible one-guard response shapes are:

\[
\begin{array}{c|c}
\text{move}&\text{successor}\\ \hline
b\to x_3&\{c,x_0,x_3\}=R_c\\
c\to x_3&\{b,x_0,x_3\}\\
x_0\to x_3&\{b,c,x_3\}=S-a+x_3.
\end{array}
\]

The second state is forbidden by (1.3), and the third is absent because
\(a\notin L_S(x_3)\).  Hence the retained response is uniquely
\(b\to x_3\), proving \(R_c\in\mathcal F\).

From \(R_c\), attack the unoccupied vertex \(x_1\).  Only \(c,x_3\) are
adjacent to \(x_1\).  The move \(x_3\to x_1\) gives
\(\{c,x_0,x_1\}\), forbidden by (1.3), so closure uniquely retains
\(c\to x_1\), giving \(R_1\).

Similarly, attack the unoccupied vertex \(x_2\) afresh from \(R_c\).
Only \(c,x_0\) can respond.  The move \(x_0\to x_2\) gives
\(\{c,x_2,x_3\}\), forbidden by (1.3), so closure uniquely retains
\(c\to x_2\), giving \(R_2\). \(\square\)

The states in (3.2) need not be independent: \(x_0x_3\in E(G)\).
Accordingly, no ridge-covariance claim is made for them.  The applicable
mechanism is the accepted co-occupied-ridge lemma.

## 4. Main theorem: an external clique of induced-\(C_5\) closers

Define

\[
 Z=N_H(x_0)\cap N_H(x_3).
\tag{4.1}
\]

### Theorem 4.1 (forced induced complement \(C_5\)) — PROVED

The set \(Z\) is nonempty, lies outside

\[
 S\cup\{x_0,x_1,x_2,x_3\}\cup W,
\tag{4.2}
\]

and \(G[Z]\) is a clique.  For every \(z\in Z\),

\[
 cz,\ x_1z,\ x_2z\in E(G),\qquad
 \{x_0,x_3,z\}\in\mathcal F,
\tag{4.3}
\]

and

\[
 c\in L_S^{\mathcal F}(z).
\tag{4.4}
\]

For distinct \(z,z'\in Z\), an attack at \(z'\) from
\(\{x_0,x_3,z\}\) is unoccupied and has the unique response
\(z\to z'\).

Consequently,

\[
 z\,x_0\,x_1\,x_2\,x_3\,z
\tag{4.5}
\]

is an induced \(C_5\) in \(H=\overline G\) for every \(z\in Z\).

#### Proof

Because \(\gamma(G)=3\), the pair \(\{x_0,x_3\}\) does not dominate
\(G\).  Hence \(Z\ne\varnothing\).

Every named vertex is excluded from \(Z\):

- \(a\) is adjacent to \(x_0\), and \(b\) is adjacent to \(x_3\);
- \(c\) is adjacent to both endpoints by Lemma 3.1;
- \(x_1\) is adjacent to \(x_3\), and \(x_2\) is adjacent to \(x_0\);
- \(x_0,x_3\) themselves are not in their open common complement
  neighborhood; and
- every \(w\in W\) is adjacent to both endpoints by Lemma 2.2.

This proves (4.2).

Apply the accepted co-occupied-ridge lemma to each state in (3.2), with
the common ridge \(\{x_0,x_3\}\).  For \(z\in Z\), the attack at \(z\)
is unoccupied in each state, and neither endpoint guard can respond.
Thus the third guard moves uniquely:

\[
\begin{array}{c|c}
\text{source state}&\text{unique move and common successor}\\ \hline
R_c&c\to z\\
R_1&x_1\to z\\
R_2&x_2\to z
\end{array}
\qquad\Longrightarrow\qquad
\{x_0,x_3,z\}\in\mathcal F.
\tag{4.6}
\]

This proves all three graph edges in (4.3) and the common successor.

For distinct \(z,z'\in Z\), the family state
\(\{x_0,x_3,z\}\) must dominate \(z'\).  Both endpoint guards miss
\(z'\), so \(zz'\in E(G)\).  The attack at the unoccupied vertex \(z'\)
therefore has the unique response \(z\to z'\), proving the clique and
transition claims.

Apply restoration (1.1) to \(\{x_0,x_3,z\}\).  All three reference
positions are missing, while

\[
 L_S(x_0)\cup L_S(x_3)=\{a,b\}.
\]

The missing position \(c\) must therefore belong to \(L_S(z)\), proving
(4.4).

Finally, (0.2) gives the three path edges of \(H\), and \(z\in Z\) gives
the two closing edges \(zx_0,zx_3\) of \(H\).  The only possible chords
are \(x_0x_2,x_0x_3,x_1x_3,zx_1,zx_2\); all five are edges of \(G\) by
(0.2) and (4.3).  Thus (4.5) is induced. \(\square\)

Under the already accepted odd-wheel exclusion, this induced \(C_5\) has
no complement hub.  Theorem 4.1 does not exclude a mixed \(P_4\); it
canonically embeds every such realization into the live hub-free-\(C_5\)
branch.

## 5. A second external layer from the original witness

The following consequence is not needed for Theorem 4.1, but it records
what direct use of the witness clique \(W\) buys beyond the induced
\(C_5\).

For \(w\in W\), define

\[
 Y_w=N_H(c)\cap N_H(w).
\tag{5.1}
\]

### Proposition 5.1 (the \(c,w\) co-state clique) — PROVED

For every \(w\in W\), the set \(Y_w\) is nonempty and lies outside

\[
 S\cup\{x_0,x_1,x_2,x_3\}\cup W.
\tag{5.2}
\]

It is a clique in \(G\).  Every \(y\in Y_w\) satisfies

\[
 ay,by\in E(G),\qquad \{c,w,y\}\in\mathcal F,
\tag{5.3}
\]

and

\[
 yx_0\in E(G)\quad\text{or}\quad yx_3\in E(G).
\tag{5.4}
\]

For distinct \(y,y'\in Y_w\), the attack at \(y'\) from
\(\{c,w,y\}\) is unoccupied and has the unique response \(y\to y'\).

#### Proof

The pair \(\{c,w\}\) dominates all of the displayed core and \(W\):
\(w\) sees \(a,b,x_0,x_3\) and every member of \(W\), while \(c\) sees
\(x_1,x_2\).  Since \(\gamma(G)=3\), this pair misses some vertex, so
\(Y_w\ne\varnothing\), and every such vertex is external as in (5.2).

By Lemma 2.1, both

\[
 \{a,c,w\}=S-b+w,\qquad
 \{b,c,w\}=S-a+w
\]

belong to \(\mathcal F\).  At either state, an attack at
\(y\in Y_w\) is unoccupied.  The guards at \(c,w\) are nonadjacent to
\(y\), so the only possible response is respectively \(a\to y\) or
\(b\to y\).  This proves the two edges and the common successor
\(\{c,w,y\}\).

That successor must dominate any distinct \(y'\in Y_w\).  Since \(c,w\)
miss \(y'\), the edge \(yy'\) is forced, as is the unique move
\(y\to y'\).  Finally, \(R_c=\{c,x_0,x_3\}\) must dominate \(y\), and
\(cy\notin E(G)\), proving (5.4). \(\square\)

In particular, the pair \(\{x_0,x_3\}\) dominates every \(Y_w\); hence
the clique \(Z\) in Theorem 4.1 is disjoint from all of these second-layer
sets.

## 6. Serious iterations and rejected strengthenings

### Iteration A — endpoint attacks at \(T_w\)

The first attempt attacked \(x_0,x_3\) directly from the independent
witness states \(T_w\).  Ridge covariance proved the uniform role law
in Lemma 2.3.  Restoration gives

\[
x_2\in L_{T_w}(x_0)\Longrightarrow b\in L_S(w),\qquad
x_1\in L_{T_w}(x_3)\Longrightarrow a\in L_S(w),
\tag{6.1}
\]

while witness responses give the common bridge states
\(\{x_0,x_1,x_2\}\) and \(\{x_1,x_2,x_3\}\).
This was a genuine cross-state constraint, but it stopped at a two-role
ambiguity.  The fork in Section 1 was needed to prove both end colors
without assuming either endpoint role.

### Iteration B — saturating \(W\), then the co-state layer \(Y_w\)

The attack tree in Lemma 2.1 proved
\(\{a,b\}\subseteq L_S(w)\), and Proposition 5.1 then produced the
external clique \(Y_w\).  A tempting strengthening was

\[
 L_S(y)=\{a,b\}\quad\text{for every }y\in Y_w.
\tag{6.2}
\]

This is **not proved**.  From \(\{c,w,y\}\), attacks at \(a\) or \(b\)
may simply move the guard at \(y\) back to the corresponding co-state;
closure is allowed to retain that two-state cycle.

A direct nine-vertex ordinary-set diagnostic also warns that equality must
be used again for any proof of (6.2).  Take graph6 `HFzvvf]`, namely the
graph with every edge present except

\[
ab,ac,bc,\quad
x_0x_1,x_1x_2,x_2x_3,\quad
wx_1,wx_2,\quad
yc,yw.
\tag{6.3}
\]

Assign the target lists in (0.1), together with
\(\Lambda(w)=\{a,b,c\}\) and \(\Lambda(y)=\{b\}\).  Start with all
dominating triples \(D\) satisfying

\[
 S-D\subseteq\bigcup_{v\in D-S}\Lambda(v)
\]

and take their greatest one-guard-closed subfamily.  It has 55 states.
Verifier B's direct ordinary-set family checker accepts all
\(55(9-3)=330\) state/attack obligations.  The resulting exact family
lists are the four lists in (0.1),
\(L_S(w)=\{a,b,c\}\), and \(L_S(y)=\{b\}\).
Its parameters are

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{6.4}
\]

This is a finite diagnostic, not an accepted campaign certificate.  Its
role is only to show that full closure, restoration, \(\alpha=3\), and the
first two witness layers do not force (6.2) without another use of
\(\gamma=3\).

### Iteration C — switch to the co-occupied end ridge

The decisive simplification was to stop trying to choose between the two
covariant endpoint roles at \(T_w\).  Exact restoration instead forces the
three states in (3.2) on the common ridge \(\{x_0,x_3\}\).  The absence of
a dominating pair then creates \(Z\), and three unique co-state attacks
force the induced complement \(C_5\).  This avoids any greatest-family
lifting and any order-\(14\) or heavy computation.

## 7. Exact stopping boundary

The remaining mixed \(P_4\) is not contradicted.  What is now proved for
an arbitrary specified eternal family is:

1. every original middle-pair witness \(w\) has both end colors
   \(a,b\) in its response list and is adjacent to both path ends;
2. the middle color \(c\) is adjacent to both path ends;
3. three family states share the co-occupied ridge \(\{x_0,x_3\}\);
4. the common complement neighborhood \(Z\) of that ridge is a nonempty
   external clique of uniquely interchangeable family states;
5. every \(z\in Z\) has \(c\in L_S(z)\) and closes the mixed path to an
   induced complement \(C_5\); and
6. each \(w\) separately creates a nonempty external co-state clique
   \(Y_w\), but the full response lists on \(Y_w\) are not determined.

The exact unresolved step is therefore no longer merely the abstract
four-vertex list obstruction.  It is the compatibility of that obstruction
with the forced hub-free complement \(C_5\), the independent ridge clique
\(W\), and the two co-state clique systems \(Y_w,Z\).  No argument here
forces an additional color on \(x_0,x_1,x_2,x_3\), colors the graph, or
proves the universal conjecture.

## 8. Research log

- **2026-07-26 16:58 PDT.** Read the three predecessor notes and the
  accepted C-058, C-059, C-063, C-064, C-067/C-068 hostile reviews in
  full.  Frozen the arbitrary-family and one-guard quantifiers; rejected
  any greatest-projected-family lift.
- **2026-07-26 17:07 PDT.** Derived the uniform endpoint role law at
  \(T_w\).  It was rigorous but stopped at one-or-both role ambiguity.
- **2026-07-26 17:16 PDT.** Found the two-branch attack fork
  \(S\to A_0\to\{D_c,D_b\}\).  It forces both end colors at every witness
  and both witness-to-end edges using only unoccupied one-guard attacks.
- **2026-07-26 17:22 PDT.** Derived the \(Y_w\) co-state clique.  A local
  nine-vertex diagnostic refuted the attempted unconditional conclusion
  \(L_S(y)=\{a,b\}\); the failure again has \(\gamma=2\).
- **2026-07-26 17:27 PDT.** Forced the three end-ridge states and obtained
  Theorem 4.1: every equality realization of the mixed path contains an
  external induced-complement-\(C_5\) closer clique \(Z\).
