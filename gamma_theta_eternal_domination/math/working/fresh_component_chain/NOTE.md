# Fresh-component chains: one-hub no-return and the separated-port boundary

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model:
attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor remains in the specified eternal
family.

This note continues the accepted C-129, C-133, and C-140 odd--odd
anchor-only bridge geometry.  Let

\[
 S=\{u,v,w\}\in\mathcal F
\]

be independent.  The singleton terminals and a selected two-list bridge
vertex satisfy

\[
 L(s)=\{v\},\qquad L(t)=\{u\},\qquad
 L(z)=\{u,w\},
\tag{0.1}
\]

and

\[
 sz,tz\in E(\overline G).
\tag{0.2}
\]

The bridge orientation forced by the two original singleton components
assigns \(z\) the shared color \(w\).  An active shared-\(w\) clause from
\(z\) therefore enters a free component of the frozen-\(u\) projection.

The rigorous conclusions are:

1. **PROVED: global bridge side-purity.**  The C-133 bridge is
   complement-side-pure not only toward the two original support
   components, but toward every connected component of the
   \(u\)-omitting projection.  Once \(z\) has a complement neighbor on
   one side of such a component, it is \(G\)-complete to the other side.
   Thus the same physical bridge vertex cannot supply both the entering
   clause and an opposite-side return.
2. **PROVED: turning-ridge separation.**  The C-140 ridge
   \(R_z=N_{\overline G}(w)\cap N_{\overline G}(z)\) is disjoint from
   every free component of the frozen-\(u\) projection.  Its singleton
   members lie in the fixed anchor component, while its exact two-list
   members do not belong to the \(u\)-omitting projection at all.
3. **PROVED: exact binary first-return normal form.**  If a shortest
   Boolean propagation trace returns to a component variable already
   visited on that trace, then every proper step before the first return
   visits a new component variable.  A same-literal return is removable,
   while an opposite-literal return is the terminal conflict.  When that
   return is made by a binary cross clause between exact-two-list
   endpoints, it has exactly the two cyclically symmetric list/color
   forms recorded in Theorem 3.2.  This does not cover a two-unit
   conflict with a separately pinned component.
4. **PROVED: bridge-to-bridge returns force a retained boundary.**  If
   the terminal source in the shared-\(w\) return is another
   \(\{u,w\}\)-vertex of the C-133 bridge ridge, then the two clause
   boundaries cannot both be absent from \(\mathcal F\).  This is an
   exact application of the accepted C-103 two-projection parity theorem.
   Thus a dead-boundary return must leave the original bridge ridge.
5. **EXACT EQUALITY SCOPE CONTROL.**  In `HEhbtjK`, two individually
   exposed vertices with the same exact list see opposite sides of one
   target component even though all five parameters equal three.  The two
   sources are joined in the complement and therefore receive opposite
   source colors.  This refutes raw cross-hub side synchronization, but
   does not realize an active same-color return.
6. **EXACT GAMMA-TWO ACTIVE-RETURN BOUNDARY.**  The graph `HFzvvn{` has a new checked
   52-state no-full singleton eternal family whose exact lists are
   \[
     \{0\},\{0,1\},\{0\},\{0,1\},\{1,2\},\{1,2\}.
   \]
   It realizes a separated-port one-unit lollipop.  Both source ports are
   individually exposed and side-pure, are \(G\)-adjacent, have the same
   exact list, and occupy the same side of their component, yet they see
   opposite sides of the target component.  Its parameters are
   \[
     (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
   \]
   Hence side-purity of each individual hub does not synchronize
   different hubs.  Any such synchronization theorem must use
   \(\gamma=3\) in a way not present in the local C-079 argument.

The result is a local propagation theorem and two sharp scope controls,
not an
exclusion of arbitrary chains.  A separated source outside the original
bridge ridge can still return, and a retained boundary state is not yet a
contradiction.  Complete singleton-branch exclusion, complete \(k=3\),
and the universal gamma--theta conjecture remain open.

No literature-priority claim is made.

## 1. Imported bridge geometry

Put \(H=\overline G\).  Let \(K\) be the original free component of the
frozen-\(u\) projection containing \(s\), and let \(M\) be the original
free component of the frozen-\(v\) projection containing \(t\).  In the
C-133 anchor-only case,

\[
 W=N_H(s)\cap N_H(t)
\tag{1.1}
\]

is a nonempty \(G\)-clique.  Every \(\{s,t,q\}\), \(q\in W\), is
retained.  Its \(\{u,w\}\)-part satisfies

\[
 W_{uw}=\{q\in W:L(q)=\{u,w\}\}\subseteq M-K.
\tag{1.2}
\]

The selected vertex \(z\in W_{uw}\) lies on the \(w\)-colored side of
\(M\).  The literal edge

\[
 tz\in E(H),\qquad u\in L(t),
\tag{1.3}
\]

is the positive tail which exposes \(z\) to C-079 side-purity for the
color \(u\).

For the frozen-\(u\) outside projection, write

\[
 W_u=\{x\notin S:u\notin L(x)\}.
\tag{1.4}
\]

Each connected component of \(H[W_u]\) is bipartite.  A component is
**free** when it is disjoint from the fixed component containing the
anchor edge \(vw\) in the full frozen projection

\[
 B_u=H[\{v,w\}\cup W_u].
\tag{1.5}
\]

The accepted C-120 exact-two component theorem says that every vertex
with list \(\{v,w\}\) lies in a free component of \(B_u\).  Thus a
genuine cross clause from \(z\) enters a Boolean component variable, not
the fixed anchor component.

## 2. The bridge is side-pure in every future \(u\)-component

### Theorem 2.1 (global bridge side-purity)

Let \(C\) be any connected component of \(H[W_u]\), with bipartition

\[
 C=C_0\mathbin{\dot\cup}C_1.
\]

Then

\[
 \boxed{
 N_H(z)\cap C\subseteq C_0
 \quad\hbox{or}\quad
 N_H(z)\cap C\subseteq C_1.
 }
\tag{2.1}
\]

In particular, if an active clause has

\[
 zr\in E(H),\qquad L(r)=\{v,w\},\qquad r\in C_0,
\tag{2.2}
\]

then

\[
 zq\in E(G)\qquad(q\in C_1).
\tag{2.3}
\]

#### Proof

Apply the accepted C-079 side-purity theorem with positive color \(u\),
positive tail \(p=t\), and physical hub \(q=z\).  Equation (1.3) supplies
both hypotheses

\[
 u\in L(t),\qquad tz\in E(H).
\]

C-079 applies separately to every connected component of \(H[W_u]\),
and gives (2.1).  The edge \(zr\) in (2.2) selects \(C_0\) as the
permitted side, so no vertex of \(C_1\) is an \(H\)-neighbor of \(z\).
This is (2.3). \(\square\)

The theorem is stronger than merely saying that the next clause cannot
return through the original component \(K\).  It controls every future
component entered by this **same physical bridge vertex**.  It does not
compare the permitted sides selected by two different bridge vertices.

### Corollary 2.2 (one-hub opposite return is impossible)

Assume (2.2).  The clause \(zr\) shares color \(w\), so the forced
bridge assignment \(z=w\) makes \(r=v\).  The induced orientation of
\(C\) colors

\[
 C_0\ \hbox{by }v,\qquad C_1\ \hbox{by }w.
\tag{2.4}
\]

No later clause using the same physical source \(z\) can hit a vertex of
\(C_1\).  Therefore a shared-\(w\) return which tries to force a
\(C_1\)-vertex to color \(v\) must use a source vertex different from
\(z\).

This is a genuine no-return statement for one physical hub.  It is not a
no-return theorem for the component variable.

### Theorem 2.3 (turning ridges avoid the entered projection)

Let

\[
 R_z=N_H(w)\cap N_H(z)
\tag{2.5}
\]

be the nonempty C-140 turning ridge.  Then

\[
 \boxed{
 R_z\cap C=\varnothing
 }
\tag{2.6}
\]

for every free component \(C\) of \(B_u\).

More exactly, every outside \(q\in R_z\) has

\[
 L(q)=\{v\}\quad\hbox{or}\quad L(q)=\{u,v\}.
\tag{2.7}
\]

In the first case \(q\) lies in the fixed anchor component of \(B_u\);
in the second case \(q\notin W_u\).

#### Proof

The fixed component of \(B_u\) contains the anchor \(w\).  A different
component has no \(H\)-edge to \(w\).  Every member of \(R_z\), however,
is an \(H\)-neighbor of \(w\), proving (2.6).

The list alternatives (2.7) are C-140.  If \(L(q)=\{v\}\), then
\(q\in W_u\), while \(wq\in E(H)\) joins \(q\) directly to the fixed
anchor component.  If \(L(q)=\{u,v\}\), then \(u\in L(q)\), so
\(q\notin W_u\). \(\square\)

Thus the forced turning ridge cannot itself be a hidden vertex of the
fresh \(u\)-component.  This separation still does not prevent one of
its exact two-list vertices from participating later in a component of a
different frozen projection.

## 3. Exact first-return normal form

### Lemma 3.1 (a shortest trace is component-simple before first re-entry)

Represent a frozen free-component orientation by a Boolean literal
\((C,\varepsilon)\).  Let

\[
 \ell_0\longrightarrow\ell_1\longrightarrow\cdots
 \longrightarrow\ell_m
\tag{3.1}
\]

be a shortest implication trace from one forced literal to a conflict.
If the trace returns to a component variable previously visited on the
trace, truncate it at the first such re-entry.  Then the proper prefix
before that re-entry contains no component variable twice.

More precisely:

1. if \(\ell_i=\ell_j\) for \(i<j<m\), deleting the closed segment from
   \(i\) to \(j\) gives a shorter trace;
2. if \(\ell_i\) and \(\ell_j\) are opposite literals of one variable,
   the conflict already occurs at \(j\), so no later step belongs to a
   shortest trace.

#### Proof

An implication arc depends only on its tail literal.  If
\(\ell_i=\ell_j\), the outgoing arc used after \(\ell_j\) is also
available after \(\ell_i\), so the intervening segment can be removed.
If the two literals are opposite, unit propagation has assigned both
values to one variable at the second occurrence, which is already the
terminal contradiction. \(\square\)

This gives strict component growth along the proper prefix of a chosen
minimal first-reentry trace.  It is a logical normalization, not a
graph-theoretic acyclicity theorem.  A terminal return is precisely what
a lollipop contains, but a two-unit contradiction may instead hit a
separately pinned component without repeating any variable on the
propagation trace.

### Theorem 3.2 (two binary terminal-return color directions)

Use the orientation (2.4).  Suppose a terminal step is a binary cross
clause between exact-two-list endpoints, its target \(r'\) lies in
\(C\), and it forces the opposite orientation of \(C\).  Then it has
exactly one of the following two forms.

\[
\begin{array}{c|c|c|c}
\text{return target}&L(\text{source }y)&
 \text{forced source color}&\text{wrong target color}\\ \hline
r'\in C_1&\{u,w\}&w&v\\
r'\in C_0&\{u,v\}&v&w
\end{array}
\tag{3.2}
\]

In the first row the clause edge \(yr'\) has shared color \(w\).  In the
second row it has shared color \(v\).

#### Proof

Every binary cross clause under consideration has a target of exact
two-list type \(\{v,w\}\).  To force the target away from color \(w\),
the source must be assigned the shared color \(w\), and the only
distinct exact-two-list type meeting \(\{v,w\}\) exactly in \(w\) is
\(\{u,w\}\).  This gives the first row.

To force the target away from \(v\), the source must be assigned the
shared color \(v\), and the unique distinct two-list type meeting the
target list exactly in \(v\) is \(\{u,v\}\).  This gives the second row.
The desired wrong target colors follow because each target has exactly
two available colors. \(\square\)

Corollary 2.2 says that the first row necessarily has \(y\ne z\).
The second row already has a different response-list type from \(z\).
Thus every binary exact-two-list terminal return is physically separated
from the entering clause, even though it returns to the same Boolean
component.  Singleton-source terminal clauses are outside this theorem.

## 4. A second bridge cannot make a dead-boundary return

The next theorem uses the accepted C-103 boundary parity synchronization
theorem exactly as stated.  It does not assume that an absent family
state is a graph nonedge.

### Theorem 4.1 (bridge-to-bridge retained-boundary alternative)

Assume the first row of (3.2), and suppose in addition that the terminal
source is another bridge vertex

\[
 y\in W_{uw},\qquad y\ne z.
\tag{4.1}
\]

Let \(r'\in C_1\) be its terminal target, so

\[
 zr,yr'\in E(H).
\tag{4.2}
\]

Then

\[
 \boxed{
 \{w,z,r\}\in\mathcal F
 \quad\hbox{or}\quad
 \{w,y,r'\}\in\mathcal F.
 }
\tag{4.3}
\]

In fact, if either displayed state is absent, the other one is retained.

#### Proof

Both bridge vertices are \(H\)-adjacent to the singleton terminal \(t\).
Because \(W\) is a \(G\)-clique, \(zy\in E(G)\), so

\[
 P:z-t-y
\tag{4.4}
\]

is a length-two complement path.  Every vertex of \(P\) omits \(v\):

\[
 L(z)=L(y)=\{u,w\},\qquad L(t)=\{u\}.
\]

Choose a shortest \(r\)--\(r'\) path \(Q\) in \(C\).  Its length is odd,
because \(r\in C_0\) and \(r'\in C_1\), and every vertex of \(Q\)
omits \(u\).

The two paths are vertex-disjoint.  Indeed, all three vertices of \(P\)
have \(u\) in their lists, while every vertex of \(Q\) omits \(u\).
Apply C-103 with

\[
 a=u,\qquad b=w,\qquad c=v,
\tag{4.5}
\]

the path \(P\subseteq W_v\), and the path \(Q\subseteq W_u\).  Its
positive endpoint hypotheses are

\[
 u\in L(z),\qquad v\in L(r).
\]

If both boundary states in (4.3) were absent, C-103 would force the
lengths of \(P,Q\) to have equal parity.  They have lengths even and odd,
respectively, a contradiction.  Reversing both paths proves the stronger
last sentence. \(\square\)

The theorem rules out a purely dead-gate return through a second member
of the original bridge ridge.  It does not exclude a return through a
same-type source outside that ridge, nor does it show that either retained
state in (4.3) is impossible.

## 5. Equality does not synchronize arbitrary exposed hubs

The equality graph

```text
HEhbtjK
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{5.1}
\]

Its greatest eternal triple-family has 48 states.  At \(S=012\),

\[
\begin{array}{c|cccccc}
x&3&4&5&6&7&8\\ \hline
L(x)&01&02&12&12&02&01.
\end{array}
\tag{5.2}
\]

For frozen color \(u=0\), the target component is the complement edge

\[
 5-6.
\tag{5.3}
\]

The same-list sources 3 and 8 are each individually exposed by a
0-positive complement neighbor:

\[
\begin{aligned}
 &N_H(3)\cap P_0^+\supseteq\{4,8\},\\
 &N_H(8)\cap P_0^+\supseteq\{3,7\}.
\end{aligned}
\tag{5.4}
\]

Nevertheless their target neighborhoods are opposite:

\[
 N_H(3)\cap\{5,6\}=\{5\},\qquad
 N_H(8)\cap\{5,6\}=\{6\}.
\tag{5.5}
\]

This is fully compatible with C-079 because

\[
 38\in E(H).
\tag{5.6}
\]

The two sources occupy opposite sides of their own frozen-\(2\)
component and therefore receive opposite source colors.  They can never
be the two simultaneously active same-color hubs of the terminal return
in Theorem 3.2.

Thus even full parameter equality does not make a source's response-list
type determine one global side choice in another component.  What remains
open is the narrower, dynamically relevant assertion for distinct
same-color sources.  The next control shows that this narrower assertion
is false when \(\gamma=2\).

## 6. Exact separated-port boundary at \(\gamma=2\)

The local side-purity mechanism cannot synchronize distinct hubs by
itself.  The following no-full singleton control realizes exactly the
failure.

### 6.1 Graph and eternal family

Use \(S=\{0,1,2\}\) and let the complement edges be

\[
\begin{split}
E(H)=\{&
01,02,12,\\
&34,45,56,68,78,47\}.
\end{split}
\tag{6.1}
\]

The labeled graph6 record of \(G=\overline H\) is

```text
HFzvvn{
```

Ban every direct swap from \(S\) not permitted by the target lists

\[
\begin{array}{c|cccccc}
x&3&4&5&6&7&8\\ \hline
L(x)&0&01&0&01&12&12.
\end{array}
\tag{6.2}
\]

Starting with all remaining dominating triples and applying greatest
fixed-point deletion gives a 52-state family.  The deletion-round sizes
are

\[
 15,\ 4,\ 4.
\tag{6.3}
\]

All 312 unoccupied-attack obligations pass, and recomputation recovers
the exact lists (6.2).  The family therefore is a literal eternal family;
it is not merely a static list assignment.

Its exact parameters are

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
 }
\tag{6.4}
\]

The family proves \(\gamma^\infty\le3\), while
\(\alpha\le\gamma^\infty\) proves equality.  The graph is not a
gamma--theta counterexample because \(\gamma=2\).

### 6.2 The separated lollipop

In the frozen-\(2\) projection, the free component

\[
 K:3-4-5-6
\tag{6.5}
\]

is a complement path.  The singleton markers 3 and 5 both demand color
0, so C-124 polarization forces

\[
 4=6=1.
\tag{6.6}
\]

In the frozen-\(0\) projection, the free component is the complement edge

\[
 C:7-8.
\tag{6.7}
\]

The cross edges

\[
 4\,7,\qquad 6\,8
\tag{6.8}
\]

both have shared color 1.  Starting from (6.6), the first edge forces

\[
 7=2.
\]

The internal edge (6.7) then forces

\[
 8=1,
\]

and the returning edge \(6\,8\) is monochromatic.  Equivalently, the
response 2-CNF has one pinned component literal and two clauses which
force both orientations of the second component.  Exhaustive list-color
enumeration returns zero compatible colorings.

The two source ports are physically separated:

\[
 4\ne6,\qquad46\in E(G).
\]

They have the same list, occupy the same side of \(K\), and are both
forced to the same collision color.  Each is individually exposed for
C-079 side-purity:

\[
\begin{aligned}
&0\text{-positive marker }3,\quad 34\in E(H),\\
 &0\in L(5),\quad45,56\in E(H).
\end{aligned}
\]

Nevertheless

\[
 N_H(4)\cap C=\{7\},\qquad
 N_H(6)\cap C=\{8\},
\tag{6.9}
\]

which are opposite sides of \(C\).  Thus individual side-purity is exact,
but there is no cross-hub side coherence.

This is the sharp warning for C-140: a proof may use the same bridge hub
only once, but it cannot silently identify all later hubs or orient their
neighborhoods coherently.  The missing ingredient in the control is
precisely the target equality \(\gamma=3\); it has 26 dominating pairs.

## 7. Discovery census

The discovery script `scan_propagation_cycles.py` was also run on all
261,080 connected unlabeled graphs produced by the pinned
`nauty 2.9.3` command `geng -cq 9`.  It found:

\[
\begin{array}{c|r}
\text{static }\gamma=\alpha=3\text{ graphs}&2,949\\
\text{eternal-equality graphs}&1,380\\
\text{independent references checked}&16,122\\
\text{references with a free singleton unit}&92\\
\text{references with a cross clause}&6\\
\text{references having both}&0.
\end{array}
\tag{7.1}
\]

Consequently it found no unit-reachable implication cycle.  This is
**OBSERVED discovery data only**.  It has not received an independent
coverage or implementation audit and proves no finite exclusion beyond
the campaign's already certified results.

## 8. Reproduction and claim boundary

Run the exact boundary checker from the campaign directory:

```text
python3 -I -B -W error \
  math/working/fresh_component_chain/verify_boundary.py

python3 -I -B -W error \
  math/working/fresh_component_chain/verify_equality_control.py
```

The two standalone programs independently reconstruct the graphs and
families.  They check 600 one-guard obligations in total, exact response
lists, all five graph parameters, the relevant projection components,
the exposed positive mates, and the claimed side incidences.  The
gamma-two checker additionally reconstructs both cross clauses, the
forced color trace, and every dominating pair.

The rigorous advance is:

- one bridge hub is side-pure toward every future component of the
  relevant projection;
- its turning ridge cannot hide in one of those free components;
- if a minimal trace returns to a previously visited component, it grows
  through distinct component variables until that first return, whose
  binary exact-two-list form is classified;
- a return through another original bridge vertex forces a retained
  boundary state; and
- distinct exposed hubs can nevertheless produce a separated return
  when \(\gamma=2\).

What remains open is exactly the gamma-three separated-source branch:
show that a first terminal source outside the original bridge ridge yields
a dominating pair or a forbidden retained state, or construct an equality
control realizing it.  No such theorem or control is claimed here.
