# Hostile review: mixed-\(P_4\) witness saturation and the forced \(C_5\)

## Verdict

**ACCEPT.**

The proof in `math/working/k3_mixed_witness_followup.md` is correct in the
standard one-guard-moves model.  It applies to an **arbitrary specified**
eternal family \(\mathcal F\) having the displayed exact response lists; it
does not assume that \(\mathcal F\) is greatest.  Every attack used in the
proof is at an unoccupied vertex, every retained transition moves one
occupied guard along one graph edge, and every excluded successor is
excluded for one of the three stated reasons:

1. exact family-list absence;
2. failure of the accepted arbitrary-state restoration condition; or
3. failure to dominate a named vertex.

The only recursive dead-state argument, in Lemma 3.1, has an acyclic
dependency graph and is valid.  The sets \(W,Y_w,Z\) are separated from all
claimed named vertices.  The five-cycle produced by Theorem 4.1 is induced
in \(H=\overline G\), not merely a cycle.  The cited odd-wheel theorem then
does make this \(C_5\) hub-free.

A clean-room ordinary-set computation independently reproduces the
nine-vertex diagnostic:

\[
 \texttt{HFzvvf]},\qquad
 (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3),
\]

together with the 55-state restoration-filtered eternal family, all 330
unoccupied state/attack obligations, and the six claimed exact response
lists.  Thus the diagnostic correctly isolates the missing equality
hypothesis: it satisfies the closure and response-list mechanisms but has a
dominating pair.

No universal conclusion follows from this note.  Its accepted boundary is
exactly the forced \(W\)-saturation, the co-state cliques \(Y_w\), and the
external induced-\(C_5\) closer clique \(Z\), conditional on a mixed
family-list \(P_4\) in a \(k=3\) equality graph.

## Reviewed bytes

| artifact | SHA-256 |
|---|---|
| `math/working/k3_mixed_witness_followup.md` | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| `reviews/k3_mixed_witness_followup_hostile/independent_diagnostic_check.py` | `414bbd0e0a344906a6e7bfdd31a45699bea59cc863a79b6a2652a988f0aa1410` |
| `reviews/k3_mixed_witness_followup_hostile/independent_diagnostic_result.json` | `e4bc01fbecfabccaf6b9bb9efb29fdeac749efcda5e9e75d253bc9b883a6ace7` |

The independent checker imports no campaign evaluator or transition helper.
It constructs the graph from the stated nonedges, encodes graph6 directly,
checks domination and independence by exhaustive subsets, computes
\(\theta\) by a separate complement-coloring backtrack, and computes eternal
families by ordinary-set greatest-fixed-point deletion.

## 1. Model and negative-list filter

Write

\[
 S=\{a,b,c\},\qquad
 L(x_0)=\{a\},\quad L(x_1)=\{a,c\},\quad
 L(x_2)=\{b,c\},\quad L(x_3)=\{b\}.
\]

Here \(L=L_S^{\mathcal F}\) is the family-response list.  If
\(S-u+x\in\mathcal F\), that state must dominate the missing vertex \(u\).
The other two vertices of \(S\) miss \(u\), since \(S\) is independent, so
\(xu\in E(G)\).  Therefore membership of \(S-u+x\) is equivalent to
\(u\in L(x)\).  The note is consequently entitled to reject a named direct
swap from a negative exact-list entry; it is not silently replacing a family
list by a static viable list.

The three restoration exclusions are correct:

\[
\begin{array}{c|c|c}
D&S-D&\bigcup_{v\in D-S}L(v)\\ \hline
\{c,x_2,x_3\}&\{a,b\}&\{b,c\}\\
\{c,x_0,x_1\}&\{a,b\}&\{a,c\}\\
\{b,x_0,x_3\}&\{a,c\}&\{a,b\}.
\end{array}
\]

Each union omits a required missing reference position, so none of these
states can lie in \(\mathcal F\).

From \(S\), the unoccupied attack at \(x_0\) has the unique family response
\(a\to x_0\), giving

\[
 A_0=\{b,c,x_0\}.
\]

From \(A_0\), attack \(x_2\).  The path being induced in \(H\) gives
\(x_0x_2\in E(G)\), and the positive lists give \(bx_2,cx_2\in E(G)\).
The move \(x_0\to x_2\) has the forbidden successor
\(S-a+x_2\), because \(a\notin L(x_2)\).  Thus closure must retain at least
one of

\[
 D_c=\{c,x_0,x_2\},\qquad D_b=\{b,x_0,x_2\}.
\]

This is an exhaustive fork.

## 2. Audit of the \(W\)-saturation lemmas

Let \(W=N_H(x_1)\cap N_H(x_2)\).  The predecessor result correctly gives:

- \(W\ne\varnothing\);
- \(W\) is external to \(S\cup\{x_0,x_1,x_2,x_3\}\);
- \(G[W]\) is a clique; and
- every \(T_w=\{w,x_1,x_2\}\) is an independent state in the same arbitrary
  family \(\mathcal F\).

The last point uses the independent-state forcing lemma, which applies to
every eternal family of three-sets.  It is not a greatest-family lift.

### Both end colors

Fix \(w\in W\) and suppose \(a\notin L(w)\).  In either fork state, the
attack at \(w\) is unoccupied and \(x_2\) cannot respond because
\(wx_2\notin E(G)\).

From \(D_c\):

- \(c\to w\), if that edge exists, gives \(\{w,x_0,x_2\}\), which fails to
  dominate \(x_1\);
- \(x_0\to w\), if that edge exists, gives \(\{c,w,x_2\}\), whose outside
  lists omit the missing reference position \(a\).

From \(D_b\):

- \(b\to w\), if that edge exists, gives the same state failing to dominate
  \(x_1\);
- \(x_0\to w\), if that edge exists, gives \(\{b,w,x_2\}\), whose outside
  lists again omit \(a\).

These lists include all possible responders.  Thus neither fork state could
belong to an eternal family, contradicting the required response from
\(A_0\).  Hence \(a\in L(w)\).  The stated reflection

\[
 a\leftrightarrow b,\quad x_0\leftrightarrow x_3,\quad
 x_1\leftrightarrow x_2,\quad c\mapsto c
\]

preserves every hypothesis and proves \(b\in L(w)\).  It is a relabeling of
the proof, not an assertion that the graph has this automorphism.

### Both path ends

Suppose \(wx_0\notin E(G)\).  Attack \(x_1\) from either fork state.  The
guards at \(x_0,x_2\) cannot move to \(x_1\).  The only possible remaining
move is \(c\to x_1\) from \(D_c\), or \(b\to x_1\) from \(D_b\) if the
latter graph edge exists.  Both give

\[
 E=\{x_0,x_1,x_2\}.
\]

The state \(E\) fails to dominate \(w\), since \(w\) misses
\(x_0,x_1,x_2\).  If \(bx_1\) is absent, \(D_b\) has no response at all;
either way both fork branches are dead.  Thus \(wx_0\in E(G)\), and
reflection proves \(wx_3\in E(G)\).

The uniform endpoint-role statement then follows legitimately from ridge
response-covariance.  The states \(T_w,T_z\) are independent and share
\(\{x_1,x_2\}\); the transposition \((w\ z)\) fixes each endpoint attack.
Closure proves only that at least one of the witness and opposite-middle
roles occurs.  The note correctly does not claim that both occur.

## 3. Audit of the end-ridge fork

### The \(c\)-to-end edges

Assume \(cx_3\notin E(G)\).

1. From \(D_c\), attack the unoccupied \(x_3\).  Only \(x_0\) can move, and
   its successor \(\{c,x_2,x_3\}\) is restoration-forbidden.  Hence \(D_c\)
   is dead.
2. Therefore the original fork would have to retain \(D_b\).  Attack its
   unoccupied \(x_1\).  If \(bx_1\) is absent there is no response; otherwise
   the unique successor is \(E=\{x_0,x_1,x_2\}\).
3. From \(E\), attack the unoccupied \(c\).  The three possible successor
   shapes are:

   - \(\{c,x_0,x_1\}\), restoration-forbidden;
   - \(D_c\), already dead by step 1;
   - \(\{c,x_1,x_2\}\), which at the unoccupied attack \(x_3\) can only move
     \(x_1\to x_3\), producing the restoration-forbidden
     \(\{c,x_2,x_3\}\).

Thus \(E\) is dead, then \(D_b\) is dead, while \(D_c\) was already dead.
The dependency order is

\[
 \text{base exclusions}\longrightarrow
 \{D_c,\{c,x_1,x_2\}\}\longrightarrow E\longrightarrow D_b,
\]

so there is no circular use of closure.  This contradicts the exhaustive
fork and proves \(cx_3\in E(G)\).  Reflection proves \(cx_0\in E(G)\).

### The three common-ridge states

From \(A_0\), attack the unoccupied \(x_3\).  All three guards have graph
edges to \(x_3\), but:

- \(c\to x_3\) gives the restoration-forbidden
  \(\{b,x_0,x_3\}\);
- \(x_0\to x_3\) gives the negative-list direct swap \(S-a+x_3\); and
- \(b\to x_3\) gives \(R_c=\{c,x_0,x_3\}\).

Therefore \(R_c\in\mathcal F\).  From \(R_c\), an attack at \(x_1\) has
only \(c,x_3\) as possible responders; the \(x_3\)-successor is forbidden,
so \(c\to x_1\) forces

\[
 R_1=\{x_0,x_1,x_3\}.
\]

Likewise an attack at \(x_2\) has only \(c,x_0\) as possible responders;
the \(x_0\)-successor is forbidden, so \(c\to x_2\) forces

\[
 R_2=\{x_0,x_2,x_3\}.
\]

All three attacks are unoccupied.  The states need not be independent, and
the note correctly invokes no ridge covariance here.

## 4. Audit of \(Z\) and the induced \(C_5\)

Put

\[
 Z=N_H(x_0)\cap N_H(x_3).
\]

Because \(\gamma(G)=3\), the two-set \(\{x_0,x_3\}\) does not dominate.
Every vertex it misses is nonadjacent in \(G\) to both endpoints, so
\(Z\ne\varnothing\).

The externality check is complete:

- \(a\) sees \(x_0\), \(b\) sees \(x_3\), and \(c\) sees both;
- \(x_1\) sees \(x_3\), while \(x_2\) sees \(x_0\);
- open neighborhoods exclude \(x_0,x_3\) themselves; and
- every \(w\in W\) sees both endpoints.

Thus no member of \(S\), the path, or \(W\) lies in \(Z\).

Fix \(z\in Z\).  In each of \(R_c,R_1,R_2\), the attack at \(z\) is
unoccupied.  Neither ridge guard can respond, so domination and closure
force the unique third-guard moves

\[
 c\to z,\qquad x_1\to z,\qquad x_2\to z.
\]

They all have the common successor

\[
 R_z=\{x_0,x_3,z\}\in\mathcal F
\]

and prove \(cz,x_1z,x_2z\in E(G)\).  For distinct \(z,z'\in Z\), the state
\(R_z\) must dominate \(z'\).  Its endpoint guards miss \(z'\), hence
\(zz'\in E(G)\), and the unoccupied attack at \(z'\) uniquely moves
\(z\to z'\).  This proves both that \(G[Z]\) is a clique and that its
exchange claim is family-level.

Restoration applied to \(R_z\) must cover all of \(a,b,c\).  Since

\[
 L(x_0)\cup L(x_3)=\{a,b\},
\]

it forces \(c\in L(z)\), as claimed.

Finally, in \(H\), the five proposed rim edges are

\[
 zx_0,\ x_0x_1,\ x_1x_2,\ x_2x_3,\ x_3z.
\]

The five possible chords

\[
 x_0x_2,\ x_0x_3,\ x_1x_3,\ zx_1,\ zx_2
\]

are all absent from \(H\), because they are graph edges of \(G\).
Therefore \(zx_0x_1x_2x_3z\) is an induced \(C_5\).  The accepted
odd-wheel obstruction forbids an outside vertex adjacent in \(H\) to its
whole rim, so the follow-on “hub-free” statement is also sound.

## 5. Audit of the \(Y_w\) layer

For fixed \(w\in W\), put

\[
 Y_w=N_H(c)\cap N_H(w).
\]

The pair \(\{c,w\}\) dominates all displayed core vertices and all of \(W\):
\(w\) sees \(a,b,x_0,x_3\) and its clique \(W\), while \(c\) sees
\(x_1,x_2\).  Since \(\gamma(G)=3\), this pair misses some vertex and
\(Y_w\ne\varnothing\).

The claimed exclusions are exhaustive:

- \(a,b,x_0,x_3\) see \(w\);
- \(x_1,x_2\) see \(c\);
- every member of \(W-\{w\}\) sees \(w\); and
- open neighborhoods exclude \(c,w\) themselves.

Lemma 2.1 puts both \(\{a,c,w\}\) and \(\{b,c,w\}\) in \(\mathcal F\).
For \(y\in Y_w\), an unoccupied attack at \(y\) from these states cannot be
answered by \(c\) or \(w\).  The unique responses are therefore

\[
 a\to y,\qquad b\to y,
\]

with common successor \(\{c,w,y\}\).  This forces \(ay,by\in E(G)\).
Domination of another \(y'\in Y_w\) by that successor forces
\(yy'\in E(G)\), and then the attack at \(y'\) uniquely moves \(y\to y'\).
Finally \(R_c=\{c,x_0,x_3\}\) dominates \(y\), while \(cy\notin E(G)\);
therefore \(y\) sees at least one endpoint.  This proves both (5.4) and
\(Y_w\cap Z=\varnothing\).

The note correctly declines to infer \(L(y)=\{a,b\}\).  The co-state
two-cycle does not supply that stronger family-list conclusion.

## 6. Independent diagnostic recomputation

The clean-room checker labels

\[
 (a,b,c,x_0,x_1,x_2,x_3,w,y)=(0,1,2,3,4,5,6,7,8)
\]

and constructs the graph with exactly the ten stated nonedges.  Independent
graph6 encoding returns `HFzvvf]`, with order \(9\) and size \(26\).

Exhaustive ordinary-set checks give:

- no dominating singleton and 21 dominating pairs, including
  \(\{0,3\}\), so \(\gamma=2\);
- independent triples \(\{0,1,2\}\) and \(\{4,5,7\}\), and no independent
  four-set, so \(\alpha=3\);
- clique partition
  \[
    \{0,3,5,8\}\mid\{1,4,6\}\mid\{2,7\},
  \]
  while \(\alpha\le\theta\), so \(\theta=3\); and
- a nonempty closed family of triples, while \(\alpha\le\gamma^\infty\),
  so \(\gamma^\infty=3\).  The checker also directly fixed-point deletes
  every dominating one- and two-guard candidate.

There are 58 dominating triples satisfying the stated restoration filter.
Greatest-fixed-point deletion removes two states in the first round and one
in the second, leaving 55 states.  A separate literal pass verifies that all
55 states dominate and that every one of

\[
 55(9-3)=330
\]

unoccupied attacks has a one-edge, one-guard successor in the same family.
The manifest hash is

`cc4369d5a9ca646c7f06de917ea2c8fe7135b069b7aeca51e4ba112a51a9ebe1`.

Direct family membership at \(S=\{0,1,2\}\) gives

\[
\begin{array}{c|c}
3&\{0\}\\
4&\{0,2\}\\
5&\{1,2\}\\
6&\{1\}\\
7&\{0,1,2\}\\
8&\{1\}.
\end{array}
\]

This matches the note exactly.  In particular \(w=7\) is the original
middle-pair witness, \(y=8\in Y_w\), and the co-state
\(\{c,w,y\}=\{2,7,8\}\) belongs to the family.  The pair
\(\{x_0,x_3\}=\{3,6\}\) dominates this diagnostic graph, so \(Z\) is empty:
that is precisely where the theorem's \(\gamma=3\) hypothesis fails.

## 7. Accepted boundary

This review accepts the following conditional theorem:

> In a graph with
> \(\gamma=\alpha=\gamma^\infty=3\), if an arbitrary specified eternal
> three-family realizes the exact mixed response-list \(P_4\), then every
> middle-pair witness is response-saturated and sees both path ends, the
> middle reference color sees both ends, and the graph contains a nonempty
> external \(G\)-clique \(Z\) whose vertices each close the path to a
> hub-free induced \(C_5\) in the complement.

The review does not accept any claim that this eliminates the mixed pattern,
colors the complement, resolves the \(k=3\) slice, or resolves the universal
\(\gamma\)--\(\theta\) conjecture.
