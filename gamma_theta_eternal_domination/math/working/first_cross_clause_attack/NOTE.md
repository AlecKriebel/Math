# The first cross clause: parity types and disjoint defect ridges

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained configuration dominates.

Let \(\mathcal F\) be an arbitrary specified eternal family of triples,
let

\[
 S=\{u,v,w\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(q\notin S\), write

\[
 L(q)=\{a\in S:S-a+q\in\mathcal F\}.
\tag{0.1}
\]

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.2}
\]

and that every outside response list is nonempty and proper.  The accepted
frozen-projection theorem and the parameter-two theorem make

\[
 B_i
 =
 H[(S-\{i\})\cup W_i],
 \qquad
 W_i=\{q\notin S:i\notin L(q)\},
\tag{0.3}
\]

bipartite for each \(i\in S\).

This note studies the first positive-length two-unit chain remaining after
C-119, C-120, and C-124.  Its one genuine binary clause has ports

\[
 L(x)=\{v,w\},\qquad
 L(y)=\{u,w\},\qquad
 xy\in E(H).
\tag{0.4}
\]

The port \(x\) lies in a free component \(K\) of \(B_u\), and \(y\) lies
in a free component \(M\) of \(B_v\).  Singleton markers \(s\in K\) and
\(t\in M\) pin the two component orientations so that both ports receive
the shared color \(w\).  The selected unit--clause--unit core is therefore
false.

The new conclusions are:

1. **PROVED: exact parity classification.**  If
   \(p=\operatorname{dist}_{B_u}(s,x)\bmod2\) and
   \(q=\operatorname{dist}_{B_v}(t,y)\bmod2\), then
   \[
   L(s)=
   \begin{cases}
   \{w\},&p=0,\\
   \{v\},&p=1,
   \end{cases}
   \qquad
   L(t)=
   \begin{cases}
   \{w\},&q=0,\\
   \{u\},&q=1.
   \end{cases}
   \tag{0.5}
   \]
   Every intersection vertex of \(K\) and \(M\) has singleton list
   \(\{w\}\).  In particular, coincident physical pins are possible only
   in the even--even type.
2. **PROVED: first-clause component separation from defects.**  The shared
   anchor \(w\) is adjacent in \(G\) to every vertex of \(K\cup M\).
3. **PROVED: odd-pin defect ridge.**  In the odd--odd type, put
   \[
   Z_s=N_H(w)\cap N_H(s),\qquad
   Z_t=N_H(w)\cap N_H(t).
   \tag{0.6}
   \]
   Both sets are nonempty \(G\)-cliques.  Every \(z\in Z_s\) gives a
   retained state \(\{w,s,z\}\); if \(z\notin S\), then
   \[
   u\in L(z),\qquad w\notin L(z).
   \tag{0.7}
   \]
   Symmetrically, every outside \(z\in Z_t\) satisfies
   \(v\in L(z)\) and \(w\notin L(z)\).
4. **PROVED: the two odd defect ridges are disjoint.**
   \[
   \boxed{Z_s\cap Z_t=\varnothing.}
   \tag{0.8}
   \]
   Moreover,
   \[
   Z_s\cap(S\cup K\cup M)\subseteq\{u\},
   \qquad
   Z_t\cap(S\cup K\cup M)\subseteq\{v\}.
   \tag{0.9}
   \]
   Thus each odd terminal either uses its own omitted anchor as its sole
   local defect, or creates a genuinely external response ridge; the two
   ridges can never merge.
5. **EXACT BOUNDARY:** when both support paths have one edge, the odd--odd
   family-list sequence is exactly
   \[
   \{v\},\{v,w\},\{u,w\},\{u\}.
   \tag{0.10}
   \]
   It is the C-121 static \(Y_3\) only if the four vertices induce the
   displayed complement \(P_4\) and their **static** response lists are
   also exactly (0.10).  Otherwise C-121 cannot be invoked.

The theorem does **not** eliminate the first cross clause.  Even arms do
not supply the unique occupied third-anchor response used below.
Anchor-only defect ridges are also allowed.  The exact graph `FDzro`
realizes the literal one-edge/one-edge obstruction with
\(\gamma=2\), and both defect ridges consist only of the corresponding
omitted anchors.  The equality graph `FCZbg` realizes the forced
singleton-ridge exchange mechanism itself, showing that the ridge
conclusion is not a contradiction without the rest of the first-clause
geometry.

No literature-priority claim is made.

## 1. Exact logical and physical geometry

The cross edge in (0.4) contributes the clause forbidding both ports from
receiving their only common color \(w\).  By C-120, the two variables are
free component variables; neither port lies in an anchor component.

Let

\[
 P:s=p_0p_1\ldots p_m=x\subseteq B_u[K],
\qquad
 Q:t=q_0q_1\ldots q_n=y\subseteq B_v[M]
\tag{1.1}
\]

be arbitrary paths supporting the two selected units.  They need not be
induced in the full complement, and no family omission is treated as a
graph nonedge.

### Lemma 1.1 (four parity types)

The terminal lists are exactly

\[
\begin{array}{c|cc}
&\text{even support}&\text{odd support}\\ \hline
P&\{w\}&\{v\}\\
Q&\{w\}&\{u\}.
\end{array}
\tag{1.2}
\]

#### Proof

The available colors in \(B_u\) are \(v,w\).  C-124 polarizes the whole
free component from the singleton marker: the oriented projection color
is unchanged across an even path and exchanged across an odd path.  Since
the port \(x\) is forced to \(w\), its singleton marker is \(w\) at even
distance and \(v\) at odd distance.  The proof in \(B_v\), whose colors
are \(u,w\), is identical. \(\square\)

### Lemma 1.2 (component overlap is singleton-\(w\))

For every

\[
 r\in K\cap M
\]

one has

\[
 \boxed{L(r)=\{w\}.}
\tag{1.3}
\]

Consequently \(r\) has even parity from both ports.  If \(s=t\), then
\(L(s)=\{w\}\) and both support paths are even.

#### Proof

Membership in \(K\subseteq W_u\) gives \(u\notin L(r)\), while membership
in \(M\subseteq W_v\) gives \(v\notin L(r)\).  Lists are nonempty, so
(1.3) follows.  Applying C-124 in each component, a singleton-\(w\)
marker lies on the same side as a port forced to \(w\).  The last
assertion is immediate. \(\square\)

### Lemma 1.3 (the shared color sees both components)

\[
 \boxed{wz\in E(G)\quad\text{for every }z\in K\cup M.}
\tag{1.4}
\]

#### Proof

The anchor \(w\) belongs to the anchor component of \(B_u\), whereas
\(K\) is a different component.  There is no complement edge between
different components, so \(w\) is \(G\)-adjacent to all of \(K\).
The same argument in \(B_v\) proves adjacency to all of \(M\).
\(\square\)

This is the first genuinely physical consequence of the selected binary
clause: both of its supporting components are complete to the same
anchor.

## 2. A singleton creates a retained defect ridge

The next lemma is stated independently because it is the exact one-guard
engine used at both odd terminals.

### Lemma 2.1 (odd singleton defect ridge)

Let

\[
 L(s)=\{v\},\qquad \{u,v,w\}=S,
\tag{2.1}
\]

and assume \(\gamma(G)=3\).  Put

\[
 Z_s=N_H(w)\cap N_H(s).
\tag{2.2}
\]

Then:

1. \(Z_s\ne\varnothing\);
2. for every \(z\in Z_s\),
   \[
   \{w,s,z\}\in\mathcal F;
   \tag{2.3}
   \]
3. \(G[Z_s]\) is a clique, and for distinct \(z,z'\in Z_s\), the attack
   at \(z'\) from \(\{w,s,z\}\) uniquely moves \(z\to z'\);
4. the only possible anchor in \(Z_s\) is \(u\); and
5. every \(z\in Z_s-S\) satisfies
   \[
   u\in L(z),\qquad w\notin L(z).
   \tag{2.4}
   \]

#### Proof

The pair \(\{w,s\}\) does not dominate \(G\), because \(\gamma(G)=3\).
Its missed set is exactly \(Z_s\), proving nonemptiness.

The singleton response gives the retained direct swap

\[
 D_s=S-v+s=\{u,w,s\}\in\mathcal F.
\tag{2.5}
\]

If \(z=u\), equation (2.3) is just (2.5).  Otherwise \(z\notin S\):
\(z=v\) is impossible because \(vs\in E(G)\), \(z=w\) is excluded by
the open neighborhood, and \(u\) is the only remaining anchor.

Attack the unoccupied vertex \(z\) from \(D_s\).  The guards at \(w,s\)
cannot move because \(z\) misses both.  Hence the only possible response
is

\[
 u\to z,
\]

and one-guard closure forces both \(uz\in E(G)\) and (2.3).

For distinct \(z,z'\in Z_s\), the retained state \(\{w,s,z\}\) must
dominate \(z'\).  The first two guards miss \(z'\), so \(zz'\in E(G)\).
The same observation makes \(z\to z'\) the unique response to the
unoccupied attack at \(z'\), proving the clique and exchange assertions.

Finally apply arbitrary-state restoration to \(\{w,s,z\}\).  The missing
reference positions are \(u,v\), while \(L(s)=\{v\}\).  Therefore
\(u\in L(z)\).  Since \(wz\in E(H)\), response membership cannot contain
\(w\).  This proves (2.4). \(\square\)

No missing family response was converted into a graph nonedge.  The
negative entry \(w\notin L(z)\) comes from the literal complement edge
\(wz\).

## 3. Odd--odd terminals force two disjoint ridges

Assume now that both paths in (1.1) are odd.  Lemma 1.1 gives

\[
 L(s)=\{v\},\qquad L(t)=\{u\}.
\tag{3.1}
\]

Define \(Z_s,Z_t\) as in (0.6).

### Theorem 3.1 (disjoint first-clause defect ridges)

Both \(Z_s,Z_t\) are nonempty \(G\)-cliques with the retained exchange
states described in Lemma 2.1, and

\[
 \boxed{Z_s\cap Z_t=\varnothing.}
\tag{3.2}
\]

Furthermore,

\[
 Z_s\cap(S\cup K\cup M)\subseteq\{u\},
\qquad
 Z_t\cap(S\cup K\cup M)\subseteq\{v\}.
\tag{3.3}
\]

#### Proof

Apply Lemma 2.1 to \(s\), and its \(u\leftrightarrow v\) reflection to
\(t\).

By Lemma 1.3, every vertex of \(K\cup M\) is adjacent in \(G\) to \(w\),
so none belongs to either common complement neighborhood.  Within \(S\),
the only possible member of \(Z_s\) is \(u\), and the only possible
member of \(Z_t\) is \(v\).  This proves (3.3).

Suppose \(z\in Z_s\cap Z_t\).  It is not an anchor:

- \(u\notin Z_t\) because \(ut\in E(G)\);
- \(v\notin Z_s\) because \(vs\in E(G)\); and
- \(w\) belongs to neither open neighborhood.

Thus \(z\notin S\).  Lemma 2.1 and its reflection give

\[
 u,v\in L(z),\qquad w\notin L(z),
\]

so

\[
 L(z)=\{u,v\}.
\tag{3.4}
\]

The vertices \(s,t,z\) all belong to the frozen-\(w\) projection \(B_w\),
and

\[
 sz,tz\in E(B_w).
\tag{3.5}
\]

Hence \(s\) and \(t\) lie in the same component and on the same
bipartition side.  If this is the anchor component, C-120 says every
singleton demand is aligned with its fixed orientation.  If it is a free
component, C-124 says all singleton markers on one side have the same
color.  Both alternatives contradict

\[
 L(s)=\{v\}\ne\{u\}=L(t).
\]

Therefore the intersection is empty. \(\square\)

The proof is independent of the lengths and internal chords of the two
support paths.  It uses their odd parity only to identify the two
singleton colors in (3.1).

### Corollary 3.2 (anchor-only versus external escape)

Each odd terminal has exactly two possibilities:

\[
\begin{array}{c|c|c}
\text{terminal}&\text{anchor-only ridge}&\text{external alternative}\\ \hline
s&Z_s=\{u\}&Z_s-\{u\}\ne\varnothing,\\
t&Z_t=\{v\}&Z_t-\{v\}\ne\varnothing.
\end{array}
\tag{3.6}
\]

In an external alternative the entire nonempty external part is a
retained \(G\)-clique whose lists contain the corresponding omitted
anchor and omit \(w\).

This is a classification, not a proof that an external alternative must
occur.

## 4. Relation to C-121 and the exact escape cases

Suppose \(m=n=1\).  Odd parity is forced, so the four family lists along

\[
 s-x-y-t
\tag{4.1}
\]

are exactly

\[
 \{v\},\{v,w\},\{u,w\},\{u\}.
\tag{4.2}
\]

The three displayed consecutive pairs are complement edges.  This is the
family-list \(Y_3\) pattern.  It falls under C-121 only after two additional
hypotheses are checked:

1. the four vertices induce the path, so there are no complement chords;
2. the four **static** response lists, not merely their family-response
   lists, are exactly (4.2).

When both hold, C-121 gives the conditional order floor \(n\ge14\).
Without either, the C-121 restoration-rigidity and static-defect count
cannot be imported.

The exact unresolved escape ledger for one logical clause is therefore:

1. an even support path, including the coincident-pin even--even case;
2. an odd--odd core with one or both defect ridges anchor-only;
3. longer or intersecting physical support paths;
4. complement chords in the literal four-vertex core;
5. a family omission whose corresponding static response remains viable.

Theorem 3.1 survives items 3--5, but it does not turn its two disjoint
ridges into a contradiction.

## 5. Exact controls

### 5.1 Literal one-clause control at \(\gamma=2\)

The graph

```text
FDzro
```

has

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{5.1}
\]

The explicit 21-state proper eternal family recorded by the verifier has,
at \(S=\{0,1,2\}\), the exact lists

\[
 L(3)=\{0\},\quad
 L(4)=\{0,2\},\quad
 L(5)=\{1,2\},\quad
 L(6)=\{1\}.
\tag{5.2}
\]

The complement induced by \(3,4,5,6\) is the path

\[
 3-4-5-6.
\]

The shared color is \(w=2\), and the two free supporting components are
\(\{3,4\}\subseteq B_1\) and
\(\{5,6\}\subseteq B_0\).  Its defect ridges are exactly

\[
 N_H(2)\cap N_H(3)=\{1\},\qquad
 N_H(2)\cap N_H(6)=\{0\}.
\tag{5.3}
\]

Thus both ridges are anchor-only.  This is the sharp reason the first
clause does not yield a local contradiction without a further use of
\(\gamma=3\).

### 5.2 The ridge mechanism occurs under equality

The equality graph

```text
FCZbg
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{5.4}
\]

Its 18-state greatest family has, at \(S=\{3,4,5\}\),

\[
 L(0)=\{3\},\quad L(6)=\{5\}.
\tag{5.5}
\]

For the test color \(w=4\),

\[
 N_H(4)\cap N_H(0)=\{6\},\qquad
 N_H(4)\cap N_H(6)=\{0\},
\tag{5.6}
\]

and the common state

\[
 \{0,4,6\}\in\mathcal F
\tag{5.7}
\]

is the forced exchange state in both directions.  The two outside lists
contain exactly the opposite omitted anchors predicted by Lemma 2.1.

This control does not contain the first-clause port geometry.  Its purpose
is narrower: retained singleton defect ridges are compatible with full
equality and are not themselves a contradiction.

## 6. Reproduction and claim boundary

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/first_cross_clause_attack/verify.py
```

The verifier independently decodes both graph6 records, recomputes the
listed graph parameters and greatest kernels, checks every attack
obligation of the two displayed families, reconstructs the response lists
and frozen components, and checks (5.3), (5.6), and (5.7).

The separate discovery script `search_subfamilies.py` was used only to
look for small equality controls with dynamically thinned eternal
subfamilies.  Its negative outputs have no coverage status and are not used
in any proof.

The rigorous conclusion is:

> The first genuine clause has four exact parity types.  Its odd--odd type
> forces two disjoint retained defect ridges, but the ridges may be
> anchor-only.  Therefore this step narrows the first-clause obstruction;
> it does not eliminate it, prove complete \(k=3\), or resolve the
> gamma--theta conjecture.

