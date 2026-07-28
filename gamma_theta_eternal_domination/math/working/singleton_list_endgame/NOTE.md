# Singleton-list endgame: exact logical split and buffered dynamic ports

## Status and exact scope

Date: 2026-07-28 (PDT)

All graph-game statements use the standard one-guard-moves model.  Attacks
are made only at unoccupied vertices, exactly one adjacent guard moves,
and the successor remains in the specified eternal family.

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, put \(H=\overline G\), and assume

\[
 \gamma(G)=3,\qquad 1\leq |L(x)|\leq2
 \quad(x\notin S),
\tag{0.1}
\]

where

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{0.2}
\]

The branch studied here has at least one singleton response list and no
full response list.

The outcomes are:

1. **EXACT RECONSTRUCTION:** after the frozen projection parities are
   contracted, every singleton supplies two parity pins, while every
   cross-type complement edge supplies a binary collision clause, a unit,
   a tautology, or a false constant according to whether its endpoint
   projection components are free or anchor-fixed.  The exact terminal
   inventory has three branches: an immediate false
   constant/projection-internal certificate, a one-/two-unit obstruction,
   or a unit-free bicycle on unpinned component variables.
2. **PROVED CANDIDATE:** an exact-two positive vertex that is sealed
   against all other vertices positive in one of its colors forces a
   singleton buffer of its other color at an explicit complement
   \(2\)-path.
3. **PROVED CANDIDATE:** every dynamic exact-two port forces a sealed cap.
   In the no-full branch that cap is either a singleton of the recovered
   color, or an exact-two cap whose relevant complement incidences are
   absorbed by the singleton buffer from item 2.
4. **EXACT SHARP CONTROLS:** `EEv?` realizes the sealed exact-two/buffer
   normal form with
   \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\).
   `LFzJbZYhdrDZdM` realizes dynamic exact-two ports in genuinely
   unpinned projection components, again with all five parameters equal
   to three.

Thus the singleton branch does **not** inherit C-111 physicality, even
after restricting attention to unpinned projection components.  The new
theorem instead identifies the exact singleton buffer that screens every
sealed cap created by a dynamic port.

This does not prove that the response formula is satisfiable, eliminate
immediate fixed-component certificates or arbitrary one-/two-unit chains,
finish \(k=3\), or resolve the universal \(\gamma\)--\(\theta\)
conjecture.

The accepted dependencies used below are C-069, C-075, C-079, C-082, and
C-094.  C-111 and C-114 are used only to mark the all-exact-two boundary;
their hypotheses are not imported into the singleton branch.

No literature-priority claim is made.

## 1. Exact response 2-CNF with singleton pins

For \(u\in S\), put

\[
 W_u=\{x\notin S:u\notin L(x)\},
\qquad
 B_u=H[(S-\{u\})\cup W_u].
\tag{1.1}
\]

The accepted frozen-color theorem makes every \(B_u\) bipartite.  Fix a
bipartition coordinate on every component.  The component containing the
anchor edge on \(S-\{u\}\) has a fixed orientation; every other component
has one Boolean flip variable.

### Proposition 1.1 (complete clause inventory)

After the component parities are contracted, the no-full response-list
coloring problem consists exactly of the following constraints.

1. If \(L(s)=\{d\}\), then for each
   \(u\in S-\{d\}\), the vertex \(s\in W_u\) demands color \(d\).
   This is:
   - a unit on the flip variable of the component \(K_u(s)\), if that
     component is free; or
   - a satisfied or false constant, if \(K_u(s)\) is the anchor
     component.
2. If \(xy\in E(H)\) and
   \[
     L(x)=S-\{u\},\qquad L(y)=S-\{v\},\qquad u\ne v,
   \]
   then their only common color is the third anchor \(w\).  The edge
   forbids the simultaneous events \(x=w\) and \(y=w\).  Substitution of
   the two component orientations makes this:
   - one binary 2-CNF clause if both components are free;
   - a unit or tautology if exactly one endpoint event is fixed; or
   - a false constant or tautology if both are fixed.
3. Every other complement edge is already separated inside one frozen
   bipartition, or joins disjoint lists, and contributes no additional
   constraint.

Hence a family-compatible anchored coloring exists if and only if the
resulting simplified 2-CNF is satisfiable.

#### Proof

This is the accepted C-069 gluing theorem with its substitutions written
out for the singleton branch.  A singleton omits exactly the two colors
other than its demanded color and therefore appears in exactly those two
frozen projections.  Two exact-two lists of distinct types intersect in
one color, giving the displayed collision clause.  If two endpoints share
an omitted color, their edge lies in a common bipartite projection.  If a
singleton and an exact-two list share no omitted color, their lists are
disjoint.  These cases exhaust the complement edges. \(\square\)

### Proposition 1.2 (unit-propagated terminal split)

Simplify the formula of Proposition 1.1 and propagate all units.
Exactly one of the following occurs.

1. Fixed-component substitution has already produced a false constant.
   This is an immediate projection-internal parity certificate from a
   singleton demand, or an immediate fixed/fixed collision certificate
   from a cross edge.  It has no Boolean variable or implication path and
   lies outside the C-075 chain/bicycle trichotomy.
2. No false constant occurs, but propagation reaches a contradiction.  An
   inclusion-minimal contradiction has either:
   - one unit and a path from that literal to its complement; or
   - two units and an implication path from one to the complement of the
     other.
3. No false constant occurs and propagation stops without contradiction.
   Every remaining variable is unpinned.  If the residual binary formula
   is unsatisfiable, it contains a unit-free pair of opposite implication
   paths.

Singleton vertices can remain elsewhere in the graph in case 3, but none
of their two marker pins lies on a residual variable.

#### Proof

If fixed-component substitution yields \(\bot\), the singleton parity
demand or fixed/fixed collision that produced it is already the complete
certificate; C-075 explicitly treats such a fixed-component failure
separately.  Assume henceforth that no false constant occurs.  If the
binary part is satisfiable but the units make the whole formula
unsatisfiable, the accepted minimal-2-CNF terminal theorem C-075 gives the
one-unit lollipop or two-unit chain.  If the binary part itself is
unsatisfiable, the ordinary implication-graph criterion gives a literal
and its complement in one strongly connected component, hence the two
opposite paths of a unit-free bicycle.  Unit propagation deletes every
variable it assigns, proving the final sentence. \(\square\)

This split is exact, but not by itself a contradiction.  In particular,
the word “unit-free” describes the residual Boolean variables; it does not
say that the original graph has no singleton-list vertex.

## 2. Sealed exact-two caps force singleton buffers

For an anchor \(i\in S\), write

\[
 P_i^+=\{x\notin S:i\in L(x)\}.
\tag{2.1}
\]

Call an \(i\)-positive outside vertex \(z\) **\(i\)-sealed** when

\[
 N_H(z)\cap P_i^+=\varnothing.
\tag{2.2}
\]

### Lemma 2.1 (sealed exact-two buffer)

Assume (0.1), let

\[
 L(z)=\{i,j\},
\qquad S=\{i,j,k\},
\tag{2.3}
\]

and suppose \(z\) is \(i\)-sealed.  Then there is an outside vertex \(p\)
such that

\[
 \boxed{L(p)=\{j\},\qquad kp,zp\in E(H).}
\tag{2.4}
\]

Moreover, if \(kz\in E(G)\), there is an outside vertex \(q\) with

\[
 \boxed{L(q)=\{k\},\qquad jq,zq\in E(H).}
\tag{2.5}
\]

The witnesses \(p,q\), when both are required, are distinct because their
singleton lists differ.

#### Proof

The pair \(\{k,z\}\) does not dominate \(G\), since \(\gamma(G)=3\).
Choose a common complement neighbor \(p\).  It cannot be an anchor:
\(k\) is an endpoint, while \(i,j\in L(z)\) force
\(iz,jz\in E(G)\).  Thus \(p\notin S\).

The edge \(kp\in E(H)\) gives \(k\notin L(p)\), because response
membership always forces the corresponding graph edge.  The edge
\(zp\in E(H)\), together with \(i\)-sealing, gives
\(i\notin L(p)\).  Lists are nonempty, so the no-full hypothesis leaves
exactly

\[
 L(p)=\{j\}.
\]

This proves (2.4).

Now suppose \(kz\in E(G)\).  Apply the same no-dominating-pair condition
to \(\{j,z\}\), and choose a common complement neighbor \(q\).  The
anchors \(i\) and \(k\) are adjacent to \(z\) in \(G\), while \(j\) is
an endpoint, so \(q\notin S\).  The edges \(jq,zq\in E(H)\) exclude
\(j\) and, by sealing, \(i\) from \(L(q)\).  Nonemptiness gives
\(L(q)=\{k\}\), proving (2.5). \(\square\)

If \(kz\in E(H)\), the anchor \(k\) itself can witness the pair
\(\{j,z\}\), so (2.5) is not forced.  The six-vertex control in Section 4
realizes exactly this sharp alternative.

### Corollary 2.2 (the buffer absorbs the cap)

Under Lemma 2.1, \(z\) has exact-two type \(k\).  The vertices \(p,z\)
both lie in \(W_k\), and \(pz\in E(H)\).  In every family-compatible
anchored coloring,

\[
 p=j,\qquad z=i.
\tag{2.6}
\]

Consequently every complement edge from \(z\) to a vertex \(v\in W_i\)
is already safe after the singleton pin is imposed: \(v\) cannot receive
color \(i\), while \(z\) is forced to color \(i\).

#### Proof

The singleton list fixes \(p=j\).  In the \(k\)-omitting bipartite
projection, the edge \(pz\) forces \(z\) to the other available color
\(i\).  Every \(v\in W_i\) has \(i\notin L(v)\), proving the final
claim. \(\square\)

Thus the singleton buffer does not transmit a new implication back into
the \(i\)-omitting connector.  It screens the cap.

## 3. Replacement for C-111 in the singleton branch

An exact-two type-\(i\) port \(t\), with

\[
 L(t)=S-\{i\},
\tag{3.1}
\]

is **dynamic** when \(it\in E(G)\).

### Theorem 3.1 (dynamic-port buffer alternative)

Assume (0.1) and let \(t\) be a dynamic exact-two type-\(i\) port.
Then there are distinct outside vertices \(y,r\) such that

\[
 t-y-r
\tag{3.2}
\]

is a length-two path in \(H[W_i]\), with \(r\) a same-sign physical
representative of \(t\).  The first edge \(ty\) has an outside common
complement neighbor \(z\) satisfying

\[
 i\in L(z),\qquad
 N_H(z)\cap P_i^+=\varnothing.
\tag{3.3}
\]

Exactly one of the following list alternatives holds.

1. \(L(z)=\{i\}\): the dynamic connector creates a sealed singleton of
   the recovered color.
2. \(L(z)=\{i,j\}\) for one \(j\ne i\): writing
   \(S=\{i,j,k\}\), Lemma 2.1 supplies a singleton buffer
   \(p\) with
   \[
     L(p)=\{j\},\qquad kp,zp\in E(H),
   \]
   and Corollary 2.2 forces \(z=i\).  All cap incidences from \(z\) back
   into \(W_i\), including \(zt\) and \(zy\), are color-safe after that
   pin.

#### Proof

Accepted C-094, in its dynamic case, gives the path (3.2), with
\(t,y,r\in W_i\).  Accepted C-082 applies to the complement edge
\(ty\).  Because the endpoint \(t\) is adjacent to \(i\) in \(G\), every
cap is outside and \(i\)-positive; choose one and call it \(z\).

If an outside \(i\)-positive vertex \(p'\) were adjacent to \(z\) in
\(H\), accepted C-079 would apply to:

\[
 \text{positive tail }p',\quad
 \text{common port }z,\quad
 \text{odd path }t-y\subseteq H[W_i].
\]

The required complement edges are

\[
 p'z,\ zt,\ zy,\ ty.
\]

Positive versus omitted-\(i\) lists keep the vertices distinct.  C-079
therefore forbids \(p'z\), proving (3.3).

The no-full hypothesis and \(i\in L(z)\) leave only a singleton
\(\{i\}\) or an exact two-list \(\{i,j\}\).  The latter case is Lemma
2.1 followed by Corollary 2.2. \(\square\)

This is the exact replacement for the failed attempt to extend C-111.
C-111 derives a contradiction because every outside list has size two;
here the gamma witnesses are allowed to be singleton buffers, and the
two controls below show that they really occur.

## 4. Two sharp equality controls

### 4.1 A sealed exact-two cap with its forced buffer

The graph

```text
EEv?
```

has order six, size seven, and

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{4.1}
\]

At \(S=012\), the following eight triples form an eternal family:

```text
012 023 024 025 123 124 235 245
```

All \(8(6-3)=24\) unoccupied attack obligations pass.  The exact lists
are

\[
 L(3)=L(4)=\{0,1\},\qquad L(5)=\{1\}.
\tag{4.2}
\]

Both \(3\) and \(4\) are sealed \(0\)-positive exact-two vertices.
Vertex \(5\) is the singleton buffer forced by Lemma 2.1:

\[
 25,35,45\in E(H).
\tag{4.3}
\]

Here the omitted anchor \(2\) itself can witness the other pair, showing
why the additional singleton in (2.5) requires the stated
\(2z\in E(G)\) hypothesis.  There is exactly one response-list coloring.

This control proves that the sealed-positive exclusion used in C-111
cannot be extended from the all-exact-two branch to the singleton branch.

### 4.2 Dynamic ports can remain in unpinned components

The connected graph

```text
LFzJbZYhdrDZdM
```

has order thirteen, size forty-three, and

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{4.4}
\]

Its greatest eternal triple-family has 142 states and satisfies all
\(142(13-3)=1420\) unoccupied attack obligations.  At \(S=012\), the
exact lists are

\[
\begin{array}{c|cccccccccc}
x&3&4&5&6&7&8&9&10&11&12\\ \hline
L(x)&01&12&01&12&12&01&02&02&2&0 .
\end{array}
\tag{4.5}
\]

The ports \(3\) and \(4\) are dynamic:

\[
 23,04\in E(G).
\tag{4.6}
\]

Nevertheless their omitted-color projection components are

\[
 \{3,5,8\}\subseteq W_2,\qquad
 \{4,6,7\}\subseteq W_0,
\tag{4.7}
\]

and neither component contains a singleton marker.  The corresponding
sealed singleton caps are

\[
 L(11)=\{2\},\qquad L(12)=\{0\}.
\tag{4.8}
\]

The response-list instance has exactly two colorings.

This refutes both proposed strengthenings:

- “every exact-two port is physical when at least one singleton exists”;
- “every exact-two port in an unpinned component is physical.”

The graph was already accepted as the C-095 equality control for failure
of clause-edge transport.  The verifier here independently recomputes the
different singleton-buffer features used in this note.

## 5. Exact remaining obstruction

After Proposition 1.2 and Theorem 3.1, the singleton/no-full branch has
the following honest endgame.

1. A false constant created by anchor-component substitution is an
   immediate projection-internal singleton-parity or fixed/fixed
   collision certificate.  It remains a separate physical branch; it is
   not silently reclassified as a chain or bicycle.
2. A contradiction reached during pin propagation is a physical
   one-unit lollipop or two-unit chain only after every derived logical
   unit has been traced back through its actual complement edges.  C-079
   excludes the common-port odd fan, but separated ports and arbitrary
   two-unit chains remain.
3. If no false constant occurs and pin propagation is consistent, an
   unsatisfiable residual is a unit-free bicycle on unpinned projection
   variables.  Dynamic exact-two ports can still occur there, as (4.7)
   shows.  C-094 physicalizes their literals, but C-095 forbids
   transporting the original clause edges to those representatives.
4. The sealed cap created by each dynamic port is not a missing shortcut:
   Theorem 3.1 says it is absorbed by a singleton buffer.  A proof must
   use the original clause incidences or a genuinely global attack, not
   treat the cap as a new implication edge.

Thus the next decisive singleton-branch lemma must do one of the
following:

- eliminate every immediate fixed-component parity/collision certificate
  by a literal one-guard attack;
- eliminate arbitrary separated-port one-/two-unit chains under
  \(\gamma=3\); or
- prove that a unit-free residual containing a dynamic port can be
  replaced by a strictly smaller obstruction while preserving the
  original supporting edges.

None of these statements is proved here.

## 6. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/singleton_list_endgame/verify.py \
  --check math/working/singleton_list_endgame/controls.json
```

The verifier imports no campaign evaluator or search code.  It decodes
both graph6 records, recomputes exact parameters, checks the selected
eight-state family and the 142-state greatest kernel, replays all 1,444
one-guard obligations, reconstructs every response list, identifies the
sealed caps and unpinned components, and counts the response-list
colorings.

`search_sealed_cap.py` is a discovery-only SAT builder that was used to
falsify the overstrong claim that sealed exact-two caps are impossible in
the singleton branch.  Its SAT outputs are not used as proof.
