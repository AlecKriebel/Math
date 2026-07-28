# Physical response ports reduce arbitrary \(k=3\) bicycles to five short signed cycles

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor remains in the eternal family.

This note assumes the accepted exact-two-list physicality theorem C-111:
if

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

at an independent retained state \(S=\{a,b,c\}\), and every outside
response list has size two, then

\[
 L_S^{\mathcal F}(x)=N_G(x)\cap S
 \qquad(x\notin S).
\tag{0.1}
\]

Relative to C-111 and the already accepted frozen-projection and C-079
side-purity theorems, the main conclusions here are:

1. **PROVED CANDIDATE:** every outside port has a same-type complement
   neighbor.  Consequently C-079 side-purity is no longer conditional:
   every outside vertex has a side-pure neighborhood in every component
   of every omitted-color projection.
2. **PROVED CANDIDATE:** every cross-type complement edge belongs to a
   literal transversal complement triangle, one vertex of each response
   type.  Thus an original response clause is already a two-sided
   chirality equality; no representative or clause-edge transport is
   needed.
3. **PROVED CANDIDATE:** proper three-coloring of \(\overline G\) is
   exactly a signed \(2\)-coloring of the outside complement graph:
   same-type edges flip chirality and cross-type edges preserve it.
4. **PROVED CANDIDATE:** if this signed system is inconsistent, it has a
   chordless unbalanced cycle of length at most five.  Frozen
   bipartiteness and universal side-purity remove all length-three
   cycles and two of the six length-five type words.  Up to type
   relabeling and dihedral symmetry, only the following five skeletons
   remain:
   \[
      0012;\qquad
      00011,\quad00101,\quad00102,\quad00121.
   \tag{0.2}
   \]

This is a sound shortening theorem for the **actual signed edge system**.
It is not a contraction of a physical connector path and does not infer a
graph edge from a missing family response.  It also does not prove that
the five residual skeletons are impossible.  Hence it does not prove the
complete \(k=3\) case or resolve the gamma--theta conjecture.

Two exact controls delimit the remaining step.

- The 12-vertex graph \(G_-\), with exact ASCII graph6 record

  ```text
  KBjB\z[^||Z[
  ```

  (the graph6 record contains one literal backslash) has
  \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4).
  \]
  All 163 dominating triples form its greatest eternal family, every
  outside list is exact two and physical, and it contains a separated
  literal three-gate ring with odd holonomy and no C-079 fan.  Thus
  physicality plus full eternal closure does not suffice when
  \(\gamma=2\).
- Adding exactly three complement edges gives \(G_+\), with exact ASCII
  graph6 record

  ```text
  KBjB\j[Z||ZW
  ```

  with
  \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
  \]
  It satisfies all static physical-type, side-purity, transversal-gate,
  common-neighbor, and coloring-gap conditions.  Its 136 dominating
  triples are deleted in simultaneous rounds \(34,56,46\), leaving an
  empty three-guard kernel.  Thus the remaining short-cycle exclusion
  must use multi-step eternal closure.

No literature-priority claim is made.

## 1. Setup and dependencies

Let \(\mathcal F\) be an eternal family of dominating triples, let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, put \(H=\overline G\), and assume

\[
 \gamma(G)=3,\qquad |L(x)|=2\quad(x\notin S).
\tag{1.1}
\]

For an outside vertex \(x\), its **type** is its omitted anchor:

\[
 \tau(x)=S-L(x).
\tag{1.2}
\]

C-111 gives the exact identity

\[
 \tau(x)x\in E(H),
 \qquad
 sx\in E(G)\quad(s\in S-\{\tau(x)\}).
\tag{1.3}
\]

For \(t\in S\), write

\[
 W_t=\{x\notin S:\tau(x)=t\}.
\tag{1.4}
\]

The accepted frozen-color theorem makes each \(H[W_t]\) bipartite.
Indeed, in the usual frozen projection

\[
 B_t=H[(S-\{t\})\cup W_t],
\]

the anchor edge on \(S-\{t\}\) is disconnected from \(W_t\), by (1.3).
Thus every component on \(W_t\) is a free flip component.  There are no
singleton-list units and no anchor-component units.

The other accepted dependency is the C-079 side-purity theorem:
if an outside hub \(q\) has an \(H\)-neighbor \(p\) with \(t\in L(p)\),
then all neighbors of \(q\) in any one component of \(H[W_t]\) lie on
one bipartition side.

The proofs below use no C-094 representative.  C-111 makes the original
port itself physical, so the identity map is always the appropriate
representative.

## 2. Universal side-purity

### Lemma 2.1 (same-type mate)

Every \(q\in W_t\) has a vertex

\[
 p\in W_t-\{q\}
\]

such that

\[
 pq\in E(H).
\tag{2.1}
\]

#### Proof

The pair \(\{t,q\}\) does not dominate \(G\), because
\(\gamma(G)=3\).  Hence it has a common complement neighbor \(p\),
distinct from \(t,q\):

\[
 tp,pq\in E(H).
\tag{2.2}
\]

No anchor in \(S-\{t\}\) can be \(p\), since both of those anchors are
adjacent to \(q\) in \(G\) by (1.3).  Thus \(p\notin S\).  The exact
identity (0.1) and \(tp\in E(H)\) give \(t\notin L(p)\).  Since
\(|L(p)|=2\), one has \(\tau(p)=t\), proving the claim. \(\square\)

### Theorem 2.2 (universal projection side-purity)

Fix \(t\in S\), a component \(K\) of \(H[W_t]\), and an outside vertex
\(q\).  For either bipartition \(U_K\mid V_K\),

\[
 N_H(q)\cap K\subseteq U_K
 \quad\text{or}\quad
 N_H(q)\cap K\subseteq V_K.
\tag{2.3}
\]

#### Proof

If \(q\in W_t\), either \(q\notin K\) and it has no neighbor in \(K\),
or \(q\in K\) and all of its neighbors lie on the side opposite \(q\).

Suppose \(\tau(q)=r\ne t\).  Lemma 2.1 gives a same-type mate
\(p\in W_r\) with \(pq\in E(H)\).  Because \(r\ne t\), the exact
two-list identity gives \(t\in L(p)\).  The accepted C-079 side-purity
theorem applies to \(p,q,K\) and gives (2.3). \(\square\)

This is the first place where C-111 changes the arbitrary-bicycle
endgame.  Before C-111, the mate supplied by \(\gamma=3\) could be a
dynamic omission and need not provide the positive response required by
C-079.  Equation (0.1) removes that ambiguity.

## 3. Every cross edge is a literal tight gate

### Theorem 3.1 (transversal completion)

Let

\[
 xy\in E(H),\qquad
 \tau(x)=r,\quad\tau(y)=s,\quad r\ne s,
\tag{3.1}
\]

and let \(t\) be the third anchor.  Every common complement neighbor of
\(x,y\) lies in \(W_t\).  In particular, \(\gamma(G)=3\) supplies a
vertex \(z\in W_t\) such that

\[
 xy,xz,yz\in E(H).
\tag{3.2}
\]

Thus every cross edge lies in a literal transversal \(H\)-triangle.

#### Proof

The pair \(\{x,y\}\) has a common \(H\)-neighbor \(z\).
No anchor can be \(z\):

- \(r\) misses \(x\) in \(G\) but sees \(y\);
- \(s\) sees \(x\) but misses \(y\); and
- \(t\) sees both \(x,y\).

Hence \(z\notin S\).

Suppose \(\tau(z)=r\).  The same-type edge \(xz\) places \(x,z\) on
opposite sides of one component of \(H[W_r]\).  But \(y\) is adjacent
in \(H\) to both, contradicting Theorem 2.2.  The case
\(\tau(z)=s\) is symmetric.  The only remaining type is \(t\), proving
the theorem. \(\square\)

The triangle in (3.2) is a maximum independent triple of \(G\), hence it
also belongs to every eternal triple-family by the accepted
maximum-independent-state theorem.  Family membership is not needed for
the coloring equivalence below, but it will be available in a future
attack on the five residual skeletons.

### Why C-094--C-105 and C-107 no longer block this step

C-094 previously replaced a dynamic port by a same-sign physical
representative.  C-095 and C-099 correctly showed that a clause edge need
not move to that representative.  Under C-111 no move is made:

\[
 x\longmapsto x,\qquad y\longmapsto y.
\]

The original edge \(xy\) therefore remains literal.

C-105 and C-107 remain correct.  Two arms through a third-type
almost-cap still give only one implication when the endpoint edge is
missing.  Theorem 3.1 does not turn such a \(V\)-shape into an equality.
Instead, it says that every **existing cross edge** belongs to an actual
three-edge transversal triangle.  The three literal edges together give
the two-sided equality.  The shortening argument in Section 5 uses only
such actual edge equations; it never substitutes an almost-cap resolvent
for a missing endpoint edge.

## 4. Exact signed-coloring dictionary

Identify \(a,b,c\) cyclically with \(\mathbb Z_3\).  For an outside
vertex \(x\) of type \(t\), define its chirality under an allowed color
\(\kappa(x)\in S-\{t\}\) by

\[
 \chi(x)=
 \begin{cases}
 0,&\kappa(x)=t-1,\\
 1,&\kappa(x)=t+1.
 \end{cases}
\tag{4.1}
\]

For an outside complement edge \(xy\), put

\[
 \epsilon(xy)=
 \begin{cases}
 1,&\tau(x)=\tau(y),\\
 0,&\tau(x)\ne\tau(y).
 \end{cases}
\tag{4.2}
\]

### Theorem 4.1 (signed parity equivalence)

The following are equivalent.

1. \(H\) has a proper three-coloring extending the three distinct colors
   on \(S\).
2. There is a function
   \[
     \chi:V(H)-S\longrightarrow\{0,1\}
   \]
   satisfying every outside edge equation
   \[
     \chi(x)\oplus\chi(y)=\epsilon(xy).
   \tag{4.3}
   \]

#### Proof

For a same-type edge, both endpoints have the same two allowed colors.
Proper coloring is therefore exactly chirality inequality, the
\(\epsilon=1\) equation.

For a cross-type edge, Theorem 3.1 supplies a transversal triangle.
The three vertices must receive three distinct colors.  The accepted
tight-gate calculation, or a direct check of the two allowed
permutations, gives equal chirality at all three vertices.  In particular
the edge satisfies the \(\epsilon=0\) equation.

Conversely, opposite chiralities on a same-type edge give its two
different allowed colors.  Equal chiralities at vertices of distinct
types also give different colors.  Thus (4.3) makes every outside
complement edge proper.  Equation (0.1) says a type-\(t\) vertex is
adjacent in \(H\) to exactly anchor \(t\), whose color is excluded from
its allowed pair; all anchor spokes are proper as well. \(\square\)

Consequently the response formula is satisfiable exactly when the signed
outside graph is balanced:

\[
 \bigoplus_{e\in C}\epsilon(e)=0
\tag{4.4}
\]

for every cycle \(C\).  An inconsistent response formula has a simple
**unbalanced** cycle, one containing an odd number of same-type edges.

This replaces the directed minimal-2-SAT bicycle by an undirected signed
cycle only because Theorem 3.1 upgraded every cross clause to a literal
tight gate.  Without C-111 and Theorem 3.1, C-105/C-107 prohibit this
replacement.

## 5. Gamma-shortening to length at most five

### Lemma 5.1 (typed diameter two)

If outside vertices \(x,y\) have distinct types, there is an outside
vertex \(z\) with

\[
 xz,yz\in E(H).
\tag{5.1}
\]

#### Proof

The pair \(\{x,y\}\) has a common complement neighbor because
\(\gamma(G)=3\).  No anchor is common: the anchor of either endpoint
misses that endpoint but sees the other in \(G\), while the third anchor
sees both in \(G\).  Hence the common neighbor lies outside \(S\).
\(\square\)

Every edge of the two-edge path in (5.1) carries the two-sided parity
equation from Theorem 4.1.  Its signed parity is therefore well-defined
even when \(z\) has the type of one endpoint.

### Theorem 5.2 (short unbalanced cycle)

If the signed outside graph is unbalanced, it contains a chordless
unbalanced cycle of length at most five.

#### Proof

Choose a shortest simple unbalanced cycle

\[
 C=x_0x_1\ldots x_{\ell-1}x_0.
\]

A chord would split \(C\) into two shorter cycles.  The xor of their
signed parities is the parity of \(C\), so exactly one would be
unbalanced.  Thus \(C\) is chordless.

Assume \(\ell\ge6\).  We first find two vertices of different types whose
two cyclic distances are both at least three.

- If \(\ell=6\) and every opposite pair has the same type, the type word
  repeats after three positions.  Every same-type edge is then repeated
  twice, so \(C\) is balanced, a contradiction.
- If \(\ell\ge7\) and every pair at cyclic distance from \(3\) through
  \(\ell-3\) has the same type, then in particular
  \[
    \tau(x_i)=\tau(x_{i+3})=\tau(x_{i+4})
  \]
  for every \(i\), with indices read cyclically.  Hence consecutive
  vertices \(x_{i+3},x_{i+4}\) have the same type, so the whole word is
  constant.  A one-type cycle lies in one bipartite \(H[W_t]\) and is
  balanced, again a contradiction.

Choose the asserted different-type vertices \(x,y\), and let \(P,Q\) be
the two \(x\)--\(y\) arcs of \(C\).  Both have length at most
\(\ell-3\).  Lemma 5.1 supplies a two-edge path
\(R=xzy\) entirely in \(V(H)-S\).  Its middle vertex is distinct from
\(x,y\), because \(H\) is simple.  It also lies outside \(C\): if
\(z\in V(C)\), chordlessness forces both \(xz\) and \(yz\) to be cycle
edges, putting \(x,y\) at cyclic distance two, contrary to their choice.
Therefore \(P\cup R\) and \(Q\cup R\) are simple cycles.  The xor of
their signed parities is the parity of \(C\), so exactly one is
unbalanced.  Its length is at most

\[
 (\ell-3)+2=\ell-1.
\]

This is strictly less than \(\ell\), a contradiction.  Therefore
\(\ell\le5\). \(\square\)

This is the valid shortening promised by C-111.  It shortens via an
actual gamma-supplied two-edge path whose edge equations have already
been proved two-sided.  It does not contract a connector or transport a
clause to a different port.

## 6. Exact residual type words

For a cyclic type word, an edge contributes one to the signed parity
exactly when its two consecutive symbols agree.  Exhaustion of words of
length at most five, modulo permutation of the three types, cyclic
rotation, and reversal, gives:

\[
\begin{array}{c|l}
\ell&\text{unbalanced type words}\\ \hline
3&000,\ 001\\
4&0012\\
5&00000,\ 00001,\ 00011,\ 00101,\ 00102,\ 00121.
\end{array}
\tag{6.1}
\]

The independent verifier enumerates this table directly.

Four classes are already impossible.

1. `000` and `00000` are odd cycles inside one bipartite
   \(H[W_t]\).
2. In `001`, the different-type vertex sees both ends of a same-type
   edge, hence both sides of one component, contrary to Theorem 2.2.
3. In `00001`, the unique different-type vertex sees both ends of the
   displayed three-edge path in one type component.  Those ends are on
   opposite bipartition sides, again contradicting Theorem 2.2.

This leaves exactly (0.2).  Each cross edge of a residual cycle has at
least one retained third-type triangle witness by Theorem 3.1.  The
remaining proof target is therefore finite at the level of **type
skeletons**, though witness collisions and arbitrary extra edges still
require a complete attack audit.  Neither the word classification nor
the bounded controls below discharge those cases.

## 7. Two exact boundary controls

Use vertices

\[
 S=(0,1,2)
\]

and three transversal gates

\[
 T_0=(3,4,5),\quad
 T_1=(6,7,8),\quad
 T_2=(9,10,11),
\tag{7.1}
\]

where the positions in every gate have types \(0,1,2\), respectively.

Let \(H_-\) have:

- the anchor triangle;
- the nine physical anchor spokes
  \(0-\{3,6,9\}\), \(1-\{4,7,10\}\),
  \(2-\{5,8,11\}\);
- all three edges of each \(T_i\); and
- the three same-type ring edges
  \[
    3\,6,\qquad7\,10,\qquad11\,5.
  \tag{7.2}
  \]

Thus \(|E(H_-)|=24\).  The three gates preserve chirality and the three
ring edges flip it, proving \(\chi(H_-)=4\).

Let

\[
 H_+=H_-+\{3\,9,4\,7,8\,11\}.
\tag{7.3}
\]

The added edges give the unused gate ports same-type mates and make every
vertex pair have a common complement neighbor.  They also create a
shorter unbalanced five-cycle, for example

\[
 3-4-7-10-9-3
\tag{7.4}
\]

with type word `01110`, equivalent to `00011`.

The standalone verifier checks:

\[
\begin{array}{c|ccccc|c|c}
&\gamma&i&\alpha&\gamma^\infty&\theta&
 |\mathcal K_3|&\text{deletion rounds}\\ \hline
G_-=\overline{H_-}&2&2&3&3&4&163&\text{none}\\
G_+=\overline{H_+}&3&3&3&4&4&0&34,56,46.
\end{array}
\tag{7.5}
\]

For \(G_-\), all 163 dominating triples form the greatest eternal
family and satisfy all

\[
 163(12-3)=1467
\]

one-guard obligations.  At \(S\), the response lists are exactly

\[
\begin{array}{c|ccc}
\text{type}&0&1&2\\ \hline
\text{vertices}&3,6,9&4,7,10&5,8,11\\
L(x)&\{1,2\}&\{0,2\}&\{0,1\}.
\end{array}
\tag{7.6}
\]

Every omission is physical, and there is no C-079 fan in the finite
graph.  The nine failed common-neighbor pairs are exactly the nine
dominating pairs of \(G_-\).

For \(G_+\), all eighteen positive direct swaps in (7.6) dominate and
all nine omitted swaps fail, so the static root lists remain exact and
physical.  The graph has no dominating pair, every cross edge lies in a
transversal triangle, all projection neighborhoods are side-pure, and
the complement is still not three-colorable.  Nevertheless every
dominating triple is deleted from the one-guard kernel.

Together the controls isolate the missing interaction sharply:

\[
\begin{array}{c|c|c}
&\text{full eternal closure}&\gamma=3\\ \hline
G_-&\checkmark&\text{fails}\\
G_+&\text{fails}&\checkmark
\end{array}
\tag{7.7}
\]

Any proof of the five residual skeletons must use both columns.

## 8. What C-079 does and does not finish

C-079 is essential twice:

1. through Theorem 2.2, it makes every outside neighborhood side-pure;
2. that side-purity forces every cross-edge gamma witness into the third
   type, upgrading each clause to a literal tight gate.

But C-079 does **not** itself exclude all odd subdivisions.  Its physical
fan requires one hub adjacent to both ends of an odd path and to one
positive tail.  A separated bicycle need not display that common hub.
The exact graph \(G_-\) has physical exact-two lists, a full eternal
family, an odd separated three-gate ring, and no C-079 fan.

The arbitrary-length advance instead comes from Theorem 5.2: once every
actual edge has a two-sided signed meaning, the global
no-dominating-pair condition supplies actual two-edge shortcuts.  The
remaining obstacle is no longer an arbitrary subdivision, but the five
short type skeletons in (0.2).

## 9. Reproduction

Run:

```text
python3 -I -B -W error \
  math/working/physicality_bicycle_endgame/verify.py \
  --check math/working/physicality_bicycle_endgame/controls.json
```

The verifier uses ordinary Python sets and imports neither the campaign
evaluators nor the SAT discovery script.  It checks:

- both graph6 records and explicit complement edge sets;
- exact \(\gamma,i,\alpha,\gamma^\infty,\theta\);
- all kernel rounds and all 1,467 obligations of \(G_-\);
- exact family lists for \(G_-\) and exact dominating-swap lists for
  \(G_+\);
- physical anchor incidences, type bipartitions, universal side-purity,
  transversal completion of every cross edge, and absence of \(K_4\);
- common-neighbor coverage and dominating-pair counts;
- the literal gates, odd ring, shortest unbalanced cycles, and absence
  of a C-079 fan in both controls;
- explicit complement four-colorings and exhaustive rejection of three
  colors; and
- the complete type-word classification (6.1).

`search_static.py` records the independent SAT discovery formulation for
\(H_+\).  It is not used by the verifier or by any proof above.
