# Two-response replication and the order-14 separated-port boundary

## Status and exact scope

Date: 2026-07-27 (PDT)

All family statements use the standard one-guard-moves eternal domination
model.  Let \(H=\overline G\).

The human results in this note are:

1. **PROVED:** a vertex that is \(G\)-complete to an independent reference
   state and has two retained direct responses forces a second vertex with
   the same two responses and a genuine graph nonedge to the omitted
   anchor.  The forcing is witnessed by a pure two-vertex complement
   spoke.
2. **PROVED:** two, possibly equal, neutral vertices carrying the
   overlapping response pairs \(\{a,b\}\) and \(\{b,c\}\) force at least
   six vertices outside the reference state and its neutral set.
3. **PROVED:** consequently, the exact separated-port response pattern
   has order at least \(15\).  This conclusion does not need its full
   response vertex; the two overlapping old two-lists already suffice.
4. **CERTIFIED-FINITE CONTROL:** the 14-vertex graph
   `MFzvvn{feBKbM{gZ_` realizes every static equality and exact direct-list
   condition with
   \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
   \]
   but the selected direct states fail on their first required attacks.
   It shows exactly why domination of all direct swaps cannot replace
   literal family closure.

The six-vertex count for the special case of one full-response vertex was
independently proved by the stronger disjoint-witness theorem in
`math/working/full_response_disjoint_witnesses/NOTE.md`.  The contribution
here is the extension to two possibly distinct overlapping two-response
vertices, together with an exact physical terminal produced by each pair.

Nothing in this note excludes all order-14 response patterns, proves the
complete \(k=3\) case, or resolves the gamma--theta conjecture.

## 1. Setup

Let

\[
 S=\{a,b,c\}
\]

be an independent member of an eternal dominating family
\(\mathcal F\) of triples in \(G\).  For \(t\notin S\), define its
family-response list

\[
 L(t)=\{i\in S:S-i+t\in\mathcal F\}.
\tag{1.1}
\]

Every membership \(i\in L(t)\) forces \(it\in E(G)\), since the successor
state must dominate the omitted anchor \(i\).

Put

\[
 Q_S=\{t\in V(G)-S:ts\in E(G)\text{ for every }s\in S\}
\tag{1.2}
\]

and

\[
 A=V(G)-(S\cup Q_S).
\tag{1.3}
\]

Because \(S\) dominates, every \(t\in A\) has a nonempty proper anchor
signature

\[
 \sigma(t)=N_H(t)\cap S.
\tag{1.4}
\]

Throughout the proofs below, assume

\[
 \gamma(G)\geq3.
\tag{1.5}
\]

Thus every pair of vertices has a common neighbor in \(H\).

## 2. Two-response replication

### Lemma 2.1 (pure omitted-color pair)

Let \(x\in Q_S\), and suppose

\[
 a,b\in L(x).
\tag{2.1}
\]

Then there are distinct \(y,z\in A\) such that

\[
\begin{aligned}
 &\sigma(y)=\sigma(z)=\{c\},\\
 &xy,cy,cz,yz\in E(H),\\
 &xz\in E(G),\\
 &a,b\in L(z).
\end{aligned}
\tag{2.2}
\]

In particular, the partial response \(\{a,b\}\subseteq L(x)\) at the
neutral vertex \(x\) produces a physical two-list terminal \(z\) whose
omission of \(c\) is the graph nonedge \(cz\in E(H)\).

#### Proof

The pair \(\{c,x\}\) does not dominate.  Choose

\[
 y\in N_H(c)\cap N_H(x).
\tag{2.3}
\]

Since \(x\) is \(G\)-complete to \(S\), the vertex \(y\) is outside \(S\);
since \(cy\in E(H)\), it is outside \(Q_S\).  Hence \(y\in A\).

The two retained states

\[
 D_a=S-a+x=\{b,c,x\},
 \qquad
 D_b=S-b+x=\{a,c,x\}
\tag{2.4}
\]

both dominate \(y\).  The first two members \(c,x\) of each relevant
obstruction already miss \(y\).  Therefore \(by,ay\in E(G)\), and

\[
 \sigma(y)=\{c\}.
\tag{2.5}
\]

Apply (1.5) to the pair \(\{c,y\}\), and choose

\[
 z\in N_H(c)\cap N_H(y).
\tag{2.6}
\]

Neither \(a\) nor \(b\) can be \(z\), because (2.5) makes both adjacent
to \(y\) in \(G\); neither \(c\) nor \(y\) can be \(z\) by the absence of
loops.  No member of \(Q_S\) can be \(z\), because every such vertex is
adjacent to \(c\) in \(G\).  Thus \(z\in A-\{y\}\), and

\[
 c\in\sigma(z).
\tag{2.7}
\]

Since \(S\) dominates, the only possibilities are

\[
 \sigma(z)\in\bigl\{\{c\},\{a,c\},\{b,c\}\bigr\}.
\tag{2.8}
\]

Suppose first that \(\sigma(z)=\{a,c\}\).  The state \(D_b\) dominates
\(z\), while both \(a\) and \(c\) miss \(z\); hence \(xz\in E(G)\).
Attack the unoccupied vertex \(z\) from \(D_a=\{b,c,x\}\).

- The guard at \(c\) cannot move.
- Moving \(x\) gives \(\{b,c,z\}\), which misses \(a\).
- Moving \(b\) gives \(\{c,x,z\}\), which misses \(y\), by
  \(cy,xy,zy\in E(H)\).

Thus closure fails, a contradiction.

If \(\sigma(z)=\{b,c\}\), use the symmetric argument.  Domination of
\(D_a\) forces \(xz\in E(G)\), and attack \(z\) from
\(D_b=\{a,c,x\}\).  The guard at \(c\) cannot move; moving \(x\) leaves
\(\{a,c,z\}\), which misses \(b\); and moving \(a\) leaves
\(\{c,x,z\}\), which misses \(y\).  This is again impossible.

Consequently

\[
 \sigma(z)=\{c\}.
\tag{2.9}
\]

Now attack \(z\) from each state in (2.4).  In both cases the guard at
\(c\) cannot move.  Moving the other anchor leaves
\(\{c,x,z\}\), which misses \(y\).  Closure therefore forces the guard
at \(x\) to move in both attacks.  Hence

\[
 xz\in E(G),\qquad
 S-a+z,\ S-b+z\in\mathcal F,
\]

which is exactly \(a,b\in L(z)\). \(\square\)

### Remark 2.2

The lemma uses family absence nowhere.  Every rejected successor is
rejected because an explicitly named vertex is undominated.  Thus no
missing response has been converted into a graph nonedge.

The conclusion is also more than a count: it turns a dynamic omission at
a neutral vertex into a genuine physical omission at \(z\), while
preserving both positive response colors.

### Corollary 2.3 (physical representative of every two-list)

If a vertex \(t\notin S\) has the exact response list

\[
L(t)=\{a,b\},
\tag{2.10}
\]

then there is a vertex \(z\notin S\) with

\[
L(z)=\{a,b\},
\qquad
N_H(z)\cap S=\{c\}.
\tag{2.11}
\]

#### Proof

Membership of \(a,b\) in \(L(t)\) forces \(at,bt\in E(G)\).  If
\(ct\in E(H)\), take \(z=t\).  Otherwise \(t\in Q_S\), and Lemma 2.1
supplies a vertex \(z\) with
\(\{a,b\}\subseteq L(z)\) and \(cz\in E(H)\).  The latter nonedge makes
\(c\notin L(z)\), proving equality in (2.11). \(\square\)

This closes one precise gap in the earlier 2-SAT geometry: every dynamic
two-list type has at least one physical representative whose omitted color
is certified by a graph nonedge.  It does **not** say that logical
connector edges between several variables survive when those variables
are replaced by their physical representatives.

## 3. Overlapping response pairs force six witnesses

### Theorem 3.1 (overlapping-pair six-witness bound)

Suppose \(q,v\in Q_S\), not necessarily distinct, satisfy

\[
 \{a,b\}\subseteq L(q),
 \qquad
 \{b,c\}\subseteq L(v).
\tag{3.1}
\]

Then

\[
 |A|\geq6,
\qquad
 |V(G)|\geq |Q_S|+9.
\tag{3.2}
\]

#### Proof

Apply Lemma 2.1 to \(q\) with omitted anchor \(c\).  It gives two
distinct vertices

\[
 y_c,z_c\in A,
\qquad
 \sigma(y_c)=\sigma(z_c)=\{c\}.
\tag{3.3}
\]

Apply the cyclic version of Lemma 2.1 to \(v\), whose displayed responses
omit \(a\).  It gives two distinct vertices

\[
 y_a,z_a\in A,
\qquad
 \sigma(y_a)=\sigma(z_a)=\{a\}.
\tag{3.4}
\]

The four vertices in (3.3)--(3.4) are pairwise distinct.

The pair \(\{b,q\}\) does not dominate.  Choose

\[
 p_q\in N_H(b)\cap N_H(q).
\tag{3.5}
\]

The vertex \(p_q\) lies in \(A\).  Since the state
\(\{b,c,q\}=S-a+q\) dominates \(p_q\), the anchor \(c\) sees \(p_q\) in
\(G\).  Therefore

\[
 \sigma(p_q)\in\bigl\{\{b\},\{a,b\}\bigr\}.
\tag{3.6}
\]

Similarly choose

\[
 p_v\in N_H(b)\cap N_H(v).
\tag{3.7}
\]

The state \(\{a,b,v\}=S-c+v\) forces \(ap_v\in E(G)\), so

\[
 \sigma(p_v)\in\bigl\{\{b\},\{b,c\}\bigr\}.
\tag{3.8}
\]

Both \(p_q,p_v\) are distinct from the four vertices in
(3.3)--(3.4), because their signatures contain \(b\).

If \(p_q\ne p_v\), these are already six distinct members of \(A\).
Suppose instead that

\[
 p_q=p_v=p.
\]

Equations (3.6) and (3.8) give

\[
 \sigma(p)=\{b\}.
\tag{3.9}
\]

The pair \(\{b,p\}\) does not dominate, so choose

\[
 r\in N_H(b)\cap N_H(p).
\tag{3.10}
\]

The pure signature (3.9) excludes every anchor as \(r\), and membership
in \(N_H(b)\) excludes every member of \(Q_S\).  Thus \(r\in A\).  Its
signature contains \(b\), so it is distinct from the four pure
\(a\)- and \(c\)-vertices, and it is distinct from \(p\).  Again there
are six distinct members of \(A\).

Finally, \(V(G)\) is the disjoint union of \(S,Q_S,A\), giving the order
bound in (3.2). \(\square\)

### Corollary 3.2 (full response)

If one \(x\in Q_S\) has

\[
 L(x)=S,
\]

then Theorem 3.1 applies with \(q=v=x\), and \(|A|\geq6\).

This recovers the count in
`math/working/full_response_disjoint_witnesses/NOTE.md`, although that
note proves the stronger pairwise disjointness of all three chosen
second-layer witness sets.

### Corollary 3.3 (order-14 pattern exclusion)

If

\[
 |V(G)|\leq14,\qquad |Q_S|\geq6,
\tag{3.11}
\]

then no two, possibly equal, vertices of \(Q_S\) can satisfy (3.1).

This is broader than excluding a single full response: it also rules out
two distinct overlapping two-lists.

### Corollary 3.4 (exact separated-port floor)

In the exact separated-port pattern, the six old outside vertices

\[
 x,r,s,q,v_0,v_1
\]

all belong to \(Q_S\), while

\[
 L(q)=\{a,b\},
\qquad
 L(v_1)=\{b,c\}.
\]

Theorem 3.1 therefore gives

\[
 |V(G)|\geq15.
\tag{3.12}
\]

Unlike the full-response proof, this argument does not use the fullness
of \(x\).  It survives in a separated-port branch in which that full
response is deleted but the two terminal overlapping lists remain.

## 4. Exact tight static control

Use labels

\[
\begin{array}{c|cccccccccccccc}
v&0&1&2&3&4&5&6&7&8&9&10&11&12&13\\ \hline
 &a&b&c&x&r&s&q&v_0&v_1&z_{bc}&y_c&y_a&z_{ab}&y_b .
\end{array}
\tag{4.1}
\]

The graph

```text
MFzvvn{feBKbM{gZ_
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\tag{4.2}
\]

Its six old outside vertices form exactly \(Q_S\), and the five remaining
anchor signatures are

\[
\begin{array}{c|ccccc}
t&z_{bc}&y_c&y_a&z_{ab}&y_b\\ \hline
\sigma(t)&bc&c&a&ab&b.
\end{array}
\tag{4.3}
\]

Every selected direct swap in the exact old list table

\[
\begin{array}{c|cccccc}
t&x&r&s&q&v_0&v_1\\ \hline
L_{\rm seed}(t)&abc&ab&ab&ab&bc&bc
\end{array}
\tag{4.4}
\]

dominates.  Thus all static list and equality conditions are realized on
14 vertices.  The selected seed is not an eternal family.

For example, attack \(z_{bc}=9\) from

\[
 \{a,c,q\}=\{0,2,6\}.
\]

The guard at \(c\) cannot move.  Moving \(a\) leaves
\(\{c,q,z_{bc}\}\), which misses \(y_c=10\); moving \(q\) leaves
\(\{a,c,z_{bc}\}\), which misses \(b\).  There is no legal dominating
successor.

Likewise, attack \(z_{ab}=12\) from

\[
 \{a,c,v_1\}=\{0,2,8\}.
\]

The guard at \(a\) cannot move.  Moving \(c\) leaves
\(\{a,v_1,z_{ab}\}\), which misses \(y_a=11\); moving \(v_1\) leaves
\(\{a,c,z_{ab}\}\), which misses \(b\).

The independent verifier `verify.py` checks (4.2)--(4.4), both attack
certificates, all exact parameters, and the complete one-guard kernels.
There are 200 dominating triples; 140 are deleted in the first kernel
round and the remaining 60 in the second.  At four guards, 856
configurations survive.

This control is the tight boundary of the proof: replacing literal
one-guard closure by domination of the direct swaps permits five
nonneutral witnesses and a clique-cover gap.  The first required attack
destroys that apparent order-14 realization.

## 5. Remaining boundary

Theorem 3.1 handles a common neutral core with two overlapping two-lists.
It does not handle:

- disjoint two-lists in larger \(k\);
- a \(k=3\) branch in which every \(Q_S\)-list is a singleton;
- separated logical terminals whose physical vertices do not lie in
  \(Q_S\); or
- global 2-SAT bicycles after all neutral overlapping pairs have been
  eliminated.

The useful terminal-alignment output is (2.2): a neutral two-response
vertex always creates a physical two-list vertex with the same positive
colors and a genuine nonedge to the omitted anchor.  A next proof should
use those physical terminals rather than infer graph nonedges from other
dynamic list omissions.
