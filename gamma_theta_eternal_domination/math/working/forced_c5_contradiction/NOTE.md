# End-edge witness separation beyond the forced \(C_5\)

## Status and scope

Date: 2026-07-26 (PDT)

This note continues:

- `math/working/k3_mixed_p4_attack.md`;
- `math/working/k3_mixed_witness_followup.md`; and
- `math/working/k3_projection_gluing.md`.

Their hostile reviews were read in full before the arguments below were
written.  All statements in Sections 1--4 concern the standard
one-guard-moves model and an **arbitrary specified** eternal family
\(\mathcal F\).  The family is never assumed to be greatest.

Let

\[
 S=\{a,b,c\}
\]

be an independent state and let \(x_0x_1x_2x_3\) be an induced path in
\(H=\overline G\).  Assume

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and the exact family-response lists

\[
\begin{array}{c|cccc}
x&x_0&x_1&x_2&x_3\\ \hline
L_S^{\mathcal F}(x)&
\{a\}&\{a,c\}&\{b,c\}&\{b\}.
\end{array}
\tag{0.2}
\]

The outcome is a strictly stronger human reduction, not a contradiction:

1. two new nonempty witness cliques \(P_L,P_R\) are forced on the two end
   edges of the path;
2. \(P_L\cap P_R=\varnothing\);
3. every co-state witness set \(Y_w\) is disjoint from both \(P_L\) and
   \(P_R\); and
4. consequently every equality realization of the exact mixed path has
   order at least \(12\).

No finite search is used in these proofs.  The result does not eliminate
the mixed path at order \(12\) or above, prove the \(k=3\) slice, or resolve
the universal gamma--theta conjecture.  No literature-priority claim is
made.

## 1. Accepted state and edge ledger

The predecessor notes prove all of the following in the same specified
family \(\mathcal F\).

The complement-path relations are

\[
x_0x_1,x_1x_2,x_2x_3\notin E(G),\qquad
x_0x_2,x_0x_3,x_1x_3\in E(G).
\tag{1.1}
\]

The six positive one-swap states belong to \(\mathcal F\).  In particular,

\[
\{a,b,x_1\},\qquad \{a,b,x_2\}\in\mathcal F.
\tag{1.2}
\]

The two Hall-tight end edges force

\[
Q_L=\{b,x_0,x_1\},\qquad
Q_R=\{a,x_2,x_3\}\in\mathcal F.
\tag{1.3}
\]

Put

\[
W=N_H(x_1)\cap N_H(x_2).
\tag{1.4}
\]

Then \(W\ne\varnothing\), \(G[W]\) is a clique, and for every \(w\in W\),

\[
\{w,x_1,x_2\}\in\mathcal F,\qquad
wx_0,wx_3,wa,wb\in E(G).
\tag{1.5}
\]

The middle color sees both path ends, and the three end-ridge states

\[
R_c=\{c,x_0,x_3\},\qquad
R_1=\{x_0,x_1,x_3\},\qquad
R_2=\{x_0,x_2,x_3\}
\tag{1.6}
\]

belong to \(\mathcal F\).

The common complement neighborhood

\[
Z=N_H(x_0)\cap N_H(x_3)
\tag{1.7}
\]

is a nonempty clique of \(G\), external to the reference state, path, and
\(W\).  Every \(z\in Z\) satisfies

\[
zx_1,zx_2,zc\in E(G),\qquad
\{x_0,x_3,z\}\in\mathcal F,\qquad
c\in L_S^{\mathcal F}(z).
\tag{1.8}
\]

For each \(w\in W\), the set

\[
Y_w=N_H(c)\cap N_H(w)
\tag{1.9}
\]

is nonempty, is a clique of \(G\), and is external to the reference state,
path, and \(W\).  It is disjoint from \(Z\).  Every \(y\in Y_w\) satisfies

\[
ya,yb\in E(G),\qquad
\{c,w,y\}\in\mathcal F,
\tag{1.10}
\]

and sees at least one of \(x_0,x_3\).

We use arbitrary-state restoration in the form

\[
S-D\subseteq
\bigcup_{v\in D-S}L_S^{\mathcal F}(v)
\qquad(D\in\mathcal F),
\tag{1.11}
\]

and exact response covariance only between independent family states that
share a two-vertex ridge.

## 2. Two bridge alternatives

### Lemma 2.1 (the anchors cross at least one edge at each end) — PROVED

\[
\boxed{
 ax_2\in E(G)\ \text{or}\ ax_3\in E(G),
 \qquad
 bx_0\in E(G)\ \text{or}\ bx_1\in E(G).
}
\tag{2.1}
\]

#### Proof

Start with the positive state

\[
D=\{a,b,x_1\}=S-c+x_1\in\mathcal F
\]

and attack the unoccupied vertex \(x_3\).

The guard at \(x_1\) cannot be retained as the responder: its successor is

\[
\{a,b,x_3\}=S-c+x_3\notin\mathcal F
\]

because \(c\notin L_S(x_3)\).

If \(a\) responds, then the move itself proves \(ax_3\in E(G)\).  If \(b\)
responds, the successor

\[
\{a,x_1,x_3\}\in\mathcal F
\]

must dominate \(x_2\).  Both \(x_1\) and \(x_3\) miss \(x_2\) by (1.1), so
this is possible only if \(ax_2\in E(G)\).  Closure requires one of these
two alternatives.

Reflecting

\[
a\leftrightarrow b,\qquad
x_0\leftrightarrow x_3,\qquad
x_1\leftrightarrow x_2,\qquad c\mapsto c
\]

gives the second alternative.  Every attack is unoccupied, and the
reflection is only a relabeling of the argument, not a claimed
automorphism. \(\square\)

## 3. The two end-edge witness cliques

Define

\[
P_L=N_H(x_0)\cap N_H(x_1),\qquad
P_R=N_H(x_2)\cap N_H(x_3).
\tag{3.1}
\]

### Lemma 3.1 (end-edge saturation) — PROVED

Both \(P_L\) and \(P_R\) are nonempty cliques of \(G\).  For every
\(p\in P_L\) and \(q\in P_R\),

\[
\{p,x_0,x_1\},\ \{q,x_2,x_3\}\in\mathcal F,
\tag{3.2}
\]

and

\[
\boxed{
b\in L_S^{\mathcal F}(p),\qquad
a\in L_S^{\mathcal F}(q).
}
\tag{3.3}
\]

Each of \(P_L,P_R\) is disjoint from

\[
S\cup\{x_0,x_1,x_2,x_3\}\cup W\cup Z.
\tag{3.4}
\]

For distinct \(p,p'\in P_L\), the attack at \(p'\) from
\(\{p,x_0,x_1\}\) uniquely moves \(p\to p'\); the symmetric statement
holds in \(P_R\).  Hence response covariance applies nonvacuously along
either witness ridge whenever that clique has at least two vertices.

#### Proof

The pair \(\{x_0,x_1\}\) cannot dominate \(G\), because \(\gamma(G)=3\).
A vertex missed by this pair lies in \(P_L\), proving nonemptiness.
For every \(p\in P_L\), the triple \(\{p,x_0,x_1\}\) is independent.
It is maximum because \(\alpha(G)=3\), so independent-state forcing puts it
in every eternal three-family, including \(\mathcal F\).

If distinct \(p,p'\in P_L\) were nonadjacent in \(G\), then
\(\{p,p',x_0,x_1\}\) would be an independent four-set.  Thus \(G[P_L]\)
is a clique.  At \(\{p,x_0,x_1\}\), neither path guard can respond to an
attack at \(p'\), so the unique move is \(p\to p'\).  This also proves the
stated ridge exchange.  The proof for \(P_R\) is symmetric.

Apply restoration (1.11) to \(\{p,x_0,x_1\}\).  Once externality is
established below, all three reference positions are missing, while

\[
L_S(x_0)\cup L_S(x_1)=\{a,c\}.
\]

The missing color \(b\) must lie in \(L_S(p)\).  Symmetrically,

\[
L_S(x_2)\cup L_S(x_3)=\{b,c\}
\]

forces \(a\in L_S(q)\).

It remains to check (3.4).  For \(P_L\):

- \(a,c\) each see both \(x_0,x_1\);
- Lemma 2.1 says that \(b\) sees at least one of them;
- \(x_2\) sees \(x_0\), while \(x_3\) sees \(x_1\);
- every \(w\in W\) sees \(x_0\); and
- every \(z\in Z\) sees \(x_1\).

Open neighborhoods exclude \(x_0,x_1\) themselves.  This removes every
vertex named in (3.4).  The reflected argument proves the assertion for
\(P_R\), and also justifies the restoration applications above.
\(\square\)

### Theorem 3.2 (the two end-edge witness cliques are disjoint) — PROVED

\[
\boxed{P_L\cap P_R=\varnothing.}
\tag{3.5}
\]

#### Proof

Suppose \(p\in P_L\cap P_R\).  Then the three configurations

\[
D_0=\{p,x_0,x_1\},\qquad
D_1=\{p,x_1,x_2\},\qquad
D_2=\{p,x_2,x_3\}
\tag{3.6}
\]

are independent triples, hence all belong to \(\mathcal F\).

The first two share the independent ridge \(\{p,x_1\}\), and the second
two share \(\{p,x_2\}\).  Applying response covariance along this ridge
path transports response incidence from \(D_0\) to \(D_2\) by

\[
\sigma=(x_0\ x_2)(x_1\ x_3),
\tag{3.7}
\]

which fixes \(p,a,b,c\).

Lemma 3.1 gives \(pb\in E(G)\).  At \(D_0\), attack the unoccupied vertex
\(b\).  Moving \(p\to b\) has successor

\[
D_0-p+b=\{b,x_0,x_1\}=Q_L\in\mathcal F
\]

by (1.3).  Thus \(p\) is literally a retained response role at
\((D_0,b)\).

Covariance along (3.6) fixes both the attack \(b\) and the role \(p\).
It therefore puts \(p\) in the response list at \((D_2,b)\), forcing

\[
D_2-p+b=\{b,x_2,x_3\}\in\mathcal F.
\tag{3.8}
\]

But restoration at the last state is impossible:

\[
S-\{b,x_2,x_3\}=\{a,c\},
\qquad
L_S(x_2)\cup L_S(x_3)=\{b,c\},
\tag{3.9}
\]

and the right side omits \(a\).  This contradiction proves (3.5).
\(\square\)

The proof is genuinely dynamic.  Static nonadjacency of one vertex to all
four path vertices does not by itself contradict \(\alpha=3\).  What fails
is the transported **family membership** of the known Hall-tight response.

## 4. Separation from every \(Y_w\)

### Theorem 4.1 (co-state witnesses cannot be end-edge witnesses) — PROVED

For every \(w\in W\),

\[
\boxed{
Y_w\cap P_L=\varnothing,\qquad
Y_w\cap P_R=\varnothing.
}
\tag{4.1}
\]

#### Proof

Suppose first that \(y\in Y_w\cap P_L\).

The independent family state

\[
T_w=\{w,x_1,x_2\}
\]

must dominate \(y\).  The guards at \(w,x_1\) both miss \(y\), by the
definitions of \(Y_w,P_L\).  Hence

\[
yx_2\in E(G).
\tag{4.2}
\]

Likewise \(R_c=\{c,x_0,x_3\}\) must dominate \(y\).  The guards at
\(c,x_0\) miss \(y\), so

\[
yx_3\in E(G).
\tag{4.3}
\]

Now put

\[
E_0=\{y,x_0,x_1\},\qquad
E_1=\{y,w,x_1\},\qquad
E_2=\{w,x_1,x_2\}=T_w.
\tag{4.4}
\]

The first state is independent and hence belongs to \(\mathcal F\).
Attack the unoccupied vertex \(w\) there.  Both \(y,w\) and \(x_1,w\)
are nonedges of \(G\), while \(x_0w\in E(G)\).  The unique response is

\[
x_0\to w,
\]

which forces \(E_1\in\mathcal F\).  The state \(E_1\) is independent.
From it, attack the unoccupied vertex \(x_2\).  The guards at \(w,x_1\)
miss \(x_2\), while (4.2) holds, so the unique response is

\[
y\to x_2,
\]

giving \(E_2\).

Thus (4.4) is a two-step path of independent ridge exchanges.  Response
covariance transports incidence from \(E_0\) to \(E_2\) by

\[
\tau=(x_0\ w)(y\ x_2),
\tag{4.5}
\]

which fixes \(x_3\).

At \(E_0\), attack the unoccupied vertex \(x_3\).  Equation (4.3) makes
\(y\to x_3\) a graph move, and its successor is the already forced state

\[
E_0-y+x_3=\{x_0,x_1,x_3\}=R_1\in\mathcal F.
\]

Therefore \(y\) is a retained response role at \((E_0,x_3)\).
Covariance transports that role to \(x_2=\tau(y)\) at
\((E_2,x_3)\).  This is impossible because

\[
x_2x_3\notin E(G).
\]

Hence \(Y_w\cap P_L=\varnothing\).

Reflecting the entire proof exchanges \(P_L,R_1,x_2,x_3\) with
\(P_R,R_2,x_1,x_0\), respectively, and proves
\(Y_w\cap P_R=\varnothing\).  The reflection again relabels an argument;
it asserts no graph automorphism. \(\square\)

### Corollary 4.2 (human order bound for the mixed pattern) — PROVED

Every equality realization of (0.2) has

\[
\boxed{|V(G)|\ge 12.}
\tag{4.6}
\]

#### Proof

The reference state and path contribute seven distinct vertices.
Choose:

\[
w\in W,\quad z\in Z,\quad
p\in P_L,\quad q\in P_R,\quad y\in Y_w.
\]

The accepted externality statements separate \(w,z\) from the original
seven and from each other.  Lemma 3.1 separates \(p,q\) from the original
seven, \(W\), and \(Z\); Theorem 3.2 separates \(p\) from \(q\).
The predecessor theorem separates \(y\) from the original seven, \(W\),
and \(Z\), while Theorem 4.1 separates it from \(p,q\).

Thus the five displayed witnesses are mutually distinct and external to
the original seven, giving \(7+5=12\). \(\square\)

This is an analytic bound for realization of one exact arbitrary-family
response pattern.  It is not a new counterexample-order frontier: a
counterexample could fail to realize this particular pattern, and the
campaign already has stronger certificate-backed finite information about
counterexamples.

## 5. Refuted strengthenings and finite falsifiers

The new separation theorems do not determine the full response lists on
the surviving witness cliques.

The clean-room ordinary-set diagnostic for

\[
G=\texttt{HFzvvf]}
\]

in
`reviews/k3_mixed_witness_followup_hostile/independent_diagnostic_check.py`
verifies a 55-state eternal family and all 330 unoccupied attack
obligations.  It has the exact mixed path, a middle witness \(w\), and a
co-state witness \(y\), but

\[
L_S(w)=\{a,b,c\},\qquad L_S(y)=\{b\}.
\tag{5.1}
\]

Its parameters are

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

Thus the equality-free strengthenings

> every \(Y_w\)-vertex has both end colors in its family list,

and

> the first \(W/Y\) layers forbid full lists,

remain refuted.  The graph is used only as a falsifier for those
strengthenings; it is not evidence against Theorems 3.2 or 4.1.  Its
displayed \(y\) is not an end-edge witness, and its dominating pair means
that the nonempty external witness cliques used in those theorems are not
forced by the hypotheses.

The following tempting claims are **not proved**:

1. \(P_L\) is complete or anticomplete to \(P_R\);
2. a vertex in \(P_L\) or \(P_R\) has a uniquely determined response list;
3. \(Y_w\) is disjoint from \(Y_{w'}\) for distinct witnesses;
4. the five external witness cliques force a thirteenth vertex; or
5. the forced twelve-vertex skeleton is itself inconsistent.

No negative finite search is used to promote any of these assertions.

## 6. Exact stopping boundary

The mixed \(P_4\) has not been eliminated.  The exact current structure is:

1. the middle edge has the nonempty witness clique \(W\);
2. the co-occupied end ridge has the nonempty closer clique \(Z\), and each
   \(z\in Z\) closes the path to a hub-free induced complement \(C_5\);
3. every \(w\in W\) has its nonempty co-state clique \(Y_w\);
4. the two end edges have nonempty witness cliques \(P_L,P_R\);
5. \(P_L\cap P_R=\varnothing\) and
   \((P_L\cup P_R)\cap Y_w=\varnothing\) for every \(w\in W\), with no
   assertion that distinct \(Y_w\)-sets are disjoint; and
6. these facts force at least twelve vertices.

The next proof step must use interaction **between** the now-separated
cliques, rather than trying to identify their witnesses.  High-value
targets are:

- transport a response role through a ridge path joining different witness
  systems;
- show that an edge/nonedge choice between \(P_L\) and \(P_R\) creates a
  new witness outside the twelve-vertex skeleton;
- combine the closer clique \(Z\) with a full-list reduction; or
- classify the exact-order-12 equality skeleton and extract a human
  contradiction if one exists.

Merely observing that the original 2-SAT formula remains inconsistent is
not progress beyond the already exact gluing theorem.

## 7. Research log

- **2026-07-26 18:05 PDT.** Read the three predecessor notes and every file
  in their three hostile-review directories in full.  Reconstructed the
  exact arbitrary-family state ledger.
- **2026-07-26 18:22 PDT.** Derived the bridge alternatives in Lemma 2.1
  from attacks at the two positive \(c\)-swap states.
- **2026-07-26 18:34 PDT.** Introduced the end-edge common-neighbor cliques
  \(P_L,P_R\), proved their externality and forced third response colors.
- **2026-07-26 18:39 PDT.** Initially found that a common end witness would
  force full lists on the closer clique.  A second attack found the stronger
  conclusion: transporting the known Hall-tight \(p\to b\) response makes
  the common end witness impossible outright.
- **2026-07-26 18:44 PDT.** Propagated a hypothetical
  \(Y_w\cap P_L\) vertex through two unique independent ridge exchanges.
  The transported \(y\to x_3\) response would require the nonedge
  \(x_2x_3\) to be a guard move.  Reflection handles \(P_R\).
- **2026-07-26 18:45 PDT.** Counted the now genuinely distinct witnesses
  and obtained the human lower bound \(n\ge12\) for this exact mixed
  arbitrary-family pattern.
