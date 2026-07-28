# Hostile review: one endpoint defect excludes the exact static mixed \(P_4\)

## Verdict

**PASS.**

The universal local exclusion in
`math/working/mixed_p4_infinite_descent/NOTE.md` is rigorous at candidate
SHA-256

`c58271538d6253ec4ac56d8df7edb7a067d67453dcf8393352a5bf394ed71d34`.

The exact accepted statement is:

> Let
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), let
> \(\mathcal F\) be an arbitrary one-guard eternal family of triples, and
> let \(S=\{a,b,c\}\in\mathcal F\) be independent.  Put
> \(H=\overline G\).  There is no induced path
> \(x_0x_1x_2x_3\) in \(H\) whose four **static**
> dominating-swap lists at \(S\) are exactly
> \[
> \{a\},\qquad \{a,c\},\qquad \{b,c\},\qquad \{b\}.
> \]

This excludes the exact static \(Y_3=P_4\) obstruction at every graph
order.  It does not exclude the same four **family** lists when one or
more static lists are larger, a longer subdivided chain, a lollipop, a
bicycle, the full-list branch, all of \(k=3\), or the universal
gamma--theta conjecture.

I found no correction required.

## Frozen inputs

| artifact | SHA-256 |
|---|---|
| candidate note | `c58271538d6253ec4ac56d8df7edb7a067d67453dcf8393352a5bf394ed71d34` |
| candidate ordinary-set verifier | `527b15ce630e9466acd8241f0edbb3f74a25f67a4cdf9985ff8f88871346a4de` |
| candidate packed-bitset verifier | `b428401b7f48bd7027b1054c37748bbca779f445389aa6d4b80138264ce28692` |
| candidate research log | `dff14dc1990b67a542a2eb8550dffded4d12af102b01c8489469aa1e31dd2047` |
| candidate result summary | `2af0b6048347f8dcb612c1256081a5a4c3ec667f4ac543eced18646d76c13ea3` |
| candidate discovery probe | `1dbfa8fde2bf072a4938c1406f073a55c56bca4bbdef48b63ca43f51fe640a8c` |
| candidate manifest | `7729b8f1e1d41e58f45a13f68e126d8427d082d902687e7ad203be47bd51438d` |
| accepted C-121 source | `ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9` |
| accepted C-070 source | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| clean-room checker | `0a3bc281aba15bf1be964f2e50a881c8dc8b2a22a29cc1a4a393ddf97368bc73` |
| clean-room evidence | `29bba18f3b06ed427415f6cc4041ad2306110732f8a78d352286960c33fe5eb2` |

The clean-room checker imports no candidate or campaign code.  It derives
the pair ledger from the hypotheses, uses an independently constructed
configuration/attack incidence table, and separately decodes the two
graph6 controls.

## 1. Dependency and hypothesis audit

The candidate uses accepted C-121 and C-070 at their proved scopes.

Accepted C-121 starts with the same independent retained state, the same
induced complement path, and the same four exact **static** lists.  It
proves that the family-response lists in the specified arbitrary eternal
family are also exactly

\[
\begin{array}{c|cccc}
v&x_0&x_1&x_2&x_3\\ \hline
L_S^{\mathcal F}(v)&
\{a\}&\{a,c\}&\{b,c\}&\{b\}.
\end{array}
\tag{1.1}
\]

Accepted C-070 applies to this exact family-list pattern under
\(\gamma=\alpha=\gamma^\infty=3\), for an arbitrary specified family.
Its endpoint-saturation lemma gives

\[
cx_0,cx_3\in E(G).
\tag{1.2}
\]

No greatest-family assumption is introduced.  The only greatest fixed
point in the new argument is an overapproximating finite local kernel, not
an assumption about \(\mathcal F\).

The candidate also uses the accepted arbitrary-state restoration
condition

\[
S-D\subseteq
\bigcup_{v\in D-S}L_S^{\mathcal F}(v)
\qquad(D\in\mathcal F).
\tag{1.3}
\]

It is used only as a necessary filter.  Hence allowing every core triple
that passes (1.3), including triples that might not dominate outside the
core, enlarges the candidate state set and makes the exclusion stronger,
not unsound.

## 2. Independent derivation of the single defect

Because \(c\notin L_S^{\rm stat}(x_0)\) but \(cx_0\in E(G)\), the direct
swap

\[
S-c+x_0=\{a,b,x_0\}
\]

fails domination.  Choose a missed vertex \(d\).  Then

\[
da,db,dx_0\notin E(G).
\tag{2.1}
\]

The collision exclusions are complete:

- \(d\notin\{a,b,x_0\}\), because a vertex in the failed state is
  dominated by occupation;
- \(d\ne c\), because \(cx_0\in E(G)\);
- \(d\ne x_1\), because the positive \(a\)-role at \(x_1\) gives
  \(ax_1\in E(G)\);
- \(d\ne x_2\), because the positive \(b\)-role at \(x_2\) gives
  \(bx_2\in E(G)\); and
- \(d\ne x_3\), because the positive \(b\)-role at \(x_3\) gives
  \(bx_3\in E(G)\).

Thus \(d\) is a genuinely eighth vertex.

The retained state \(S\) dominates \(d\).  Since \(a\) and \(b\) miss
\(d\), this forces

\[
cd\in E(G).
\tag{2.2}
\]

The triple \(\{a,b,d\}\) is independent.  Since \(\alpha(G)=3\), it is a
maximum independent set.  For completeness, its membership in every
eternal triple-family has a direct proof: starting from any family state,
successively attack unoccupied vertices of \(\{a,b,d\}\).  A guard already
on that independent set cannot respond to an attack at another one of its
vertices, so the number of occupied vertices in the set strictly
increases.  After at most three attacks the retained state is exactly
\(\{a,b,d\}\).

It is the direct \(c\)-replacement of \(S\), so \(c\) is a family-response
role at \(d\).  The graph nonedges \(ad,bd\) exclude the other two roles:

\[
L_S^{\mathcal F}(d)=\{c\}.
\tag{2.3}
\]

Finally, (1.1) puts both c-swaps

\[
\{a,b,x_1\},\qquad \{a,b,x_2\}
\]

in \(\mathcal F\).  Each must dominate \(d\), while \(a,b\) miss \(d\).
Therefore

\[
dx_1,dx_2\in E(G).
\tag{2.4}
\]

Every edge and nonedge involving \(d\) that the candidate fixes follows
from (2.1)--(2.4).  The remaining pair \(dx_3\) is correctly left free.

## 3. Complete eight-vertex pair ledger

The clean-room checker generated the ledger from the preceding
hypotheses rather than copying the candidate arrays.

| pair class | fixed \(G\)-edges | fixed \(G\)-nonedges | undecided |
|---|---:|---:|---:|
| three anchor pairs | 0 | 3 | 0 |
| twelve anchor--path pairs | 8 | 0 | 4 |
| six path pairs | 3 | 3 | 0 |
| seven pairs incident with \(d\) | 3 | 3 | 1 |
| **total** | **14** | **9** | **5** |

The eight fixed anchor--path edges are the six positive static incidences
and the two C-070 endpoint-saturation edges.  Inducedness of
\(x_0x_1x_2x_3\) in \(H\) gives the three consecutive \(G\)-nonedges and
the three nonconsecutive \(G\)-edges.

The five and only five undecided pairs are

\[
bx_0,\quad bx_1,\quad ax_2,\quad ax_3,\quad dx_3.
\tag{3.1}
\]

Thus

\[
14+9+5=28=\binom82
\]

and the \(2^5=32\) completion count is exact.  Negative static roles at
the other optional anchor--path pairs may impose additional external
defect witnesses when their graph edge is present.  The local computation
deliberately omits those extra restrictions, thereby considering a
superclass of completions.  This cannot create a false exclusion.

## 4. Local-kernel soundness and external-state audit

Let

\[
C=\{a,b,c,x_0,x_1,x_2,x_3,d\}.
\]

For one fixed completion, let \(\mathcal A_0\) be every triple contained
in \(C\) that

1. dominates \(G[C]\); and
2. satisfies restoration (1.3) using the five exact family lists in
   (1.1) and (2.3).

Suppose a global family \(\mathcal F\) existed and define

\[
\mathcal F_C=\{D\in\mathcal F:D\subseteq C\}.
\]

Then \(S\in\mathcal F_C\) and
\(\mathcal F_C\subseteq\mathcal A_0\).  The first inclusion follows from
the theorem hypothesis.  The second follows because a global dominating
state dominates the induced core and every global family state satisfies
restoration.

The decisive external-leakage point is sound.  If \(D\subseteq C\) is
attacked at an unoccupied \(r\in C\), every legal one-guard successor has
the form

\[
(D-\{u\})\cup\{r\}
\]

for an occupied \(u\in D\).  Both \(D-\{u\}\) and \(r\) lie in \(C\), so
the successor is again a core triple.  No external vertex can enter this
single move, and there is no external guard in \(D\) that could respond.
Therefore global eternal closure makes \(\mathcal F_C\) closed under all
displayed attacks used by the finite calculation.

Define \(\mathcal A_{t+1}\) by synchronously deleting from
\(\mathcal A_t\) every state having some unoccupied displayed attack with
no one-edge, one-guard successor in \(\mathcal A_t\).  Inductively,

\[
\mathcal F_C\subseteq\mathcal A_t
\qquad(t\ge0).
\]

Indeed, if \(D\in\mathcal F_C\), every displayed attack has a successor
in \(\mathcal F_C\), and by the induction hypothesis that successor lies
in \(\mathcal A_t\).  Thus \(D\) is never deleted.  Consequently an empty
terminal \(\mathcal A_t\) contradicts \(S\in\mathcal F_C\).

Outside attacks are omitted from the local calculation.  That omission
only enlarges the local survivor set.  Outside states also cannot repair a
displayed attack from a core-only source state, for the one-move reason
above.  Hence the local empty-kernel certificate is valid for graphs of
arbitrary order.

## 5. Clean-room enumeration

`independent_check.py` uses string-labeled vertices, a Boolean adjacency
matrix, and an explicit configuration/attack incidence table.  It imports
neither candidate checker and shares no transition core with them.

It independently obtained:

- \(14\) fixed edges, \(9\) fixed nonedges, and \(5\) optional pairs;
- all \(32\) optional-edge completions;
- initial local overapproximations of sizes \(28\) through \(32\);
- an empty terminal local kernel in all \(32\) completions; and
- root-state deletion ranks between \(2\) and \(5\).

Its initial-size multiset is

```text
28,
29,29,29,29,29,29,
30,30,30,30,30,30,30,30,30,30,30,30,
31,31,31,31,31,31,31,31,31,31,
32,32,32
```

and its root-rank multiset is

```text
2,2,2,2,2,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,
4,4,4,4,4,4,4,4,4,
5,5,5,5
```

The clean-room completion-record digest is

`6621477df0e2de87951a86fa43ff66723e5e39be6fb40ca8fd5b3aff6ec2d560`.

The independent checker orders the five mask bits lexicographically,
whereas the candidate orders them as displayed in (3.1).  After mapping
each mask by its actual set of optional edges, all \(32\) records agree
exactly with the candidate ordinary-set verifier in:

- initial size;
- every synchronous deletion-round size;
- root deletion rank;
- first fatal attack at the root; and
- terminal size zero.

The candidate replays also reproduced their frozen output hashes:

| replay | observed SHA-256 |
|---|---|
| ordinary-set stdout | `9205772909698ba5aa21f05a3d6ac20a9911543160703157a54d0db0425ef9dc` |
| packed-bitset stdout | `9e5f6003aeb212a17ba80c7eab5204c9ae1a9c67479701bb8050c043c0f80f11` |

This is a finite proof of the local lemma, not an empirical graph search.
The human argument in Section 4 proves why the finite object covers every
possible external continuation.

## 6. One-guard model audit

All three replays implement the requested model:

- attacks at occupied vertices are skipped;
- each successor removes exactly one occupied guard;
- that guard must be adjacent in \(G\) to the attacked vertex;
- the attacked vertex is inserted;
- the successor remains a triple in the same live family; and
- every initial state dominates at least the displayed induced core.

The local verifier does not permit simultaneous moves, guard teleportation,
occupied-vertex attacks, complement edges as move edges, or a successor
outside the retained set.

The root \(S\) is independent by its three fixed \(G\)-nonedges.  The path
edges are interpreted in \(H\), then complemented correctly when building
the \(G\)-move graph.

## 7. Boundary controls

### `FDzro`

The clean-room checker independently decoded `FDzro` and obtained

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

After forbidding precisely the negative direct family swaps, its greatest
allowed triple kernel contains \(21\) states, including the independent
root \(S=\{0,1,2\}\), and discharges all

\[
21(7-3)=84
\]

unoccupied attack obligations.  Its family lists are exactly

\[
\{0\},\quad\{0,2\},\quad\{1,2\},\quad\{1\},
\]

while its static lists are strictly larger:

\[
\{0,2\},\quad
\{0,1,2\},\quad
\{0,1,2\},\quad
\{1,2\}.
\]

Thus an exact **family-list** mixed \(P_4\) is possible when the static
lists are larger.  The candidate correctly excludes this graph by its
static-list hypothesis and by \(\gamma=2\).

### `HCOceRy`

The clean-room checker independently decoded `HCOceRy` and obtained

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

Its greatest eternal triple-family has \(24\) states and contains the
independent root \(S=\{0,1,2\}\).  Vertices \(3\) and \(6\) are adjacent
in \(G\), both have family list \(\{0\}\), and both miss anchors
\(\{1,2\}\).

Therefore two adjacent pure same-color singleton vertices are compatible
with full equality.  This correctly refutes the tempting singleton-cascade
argument.  The candidate theorem instead uses the complete mixed-\(P_4\)
incidence and exact-static system.

## 8. Strict stopping boundary

The candidate's scope language is accurate.  What is now proved is a
universal exclusion of one exact static minimal obstruction.  Nothing in
the local kernel shows that:

- a family-list mixed \(P_4\) has exact static lists;
- every longer unsatisfiable response 2-CNF contracts to this \(P_4\);
- dynamic nonmembership can be replaced by graph nonadjacency;
- arbitrary lollipops or bicycles contain this core;
- the full-response-list branch is colorable;
- every \(k=3\) equality graph has \(\theta=3\); or
- the universal gamma--theta conjecture holds.

Subject to that strict scope, the theorem is ready for promotion as a
proved campaign claim.
