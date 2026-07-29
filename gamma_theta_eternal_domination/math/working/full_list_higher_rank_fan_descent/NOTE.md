# Higher-rank completion-fan exits: descending petals and target hubs

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting independent hostile
review**.  It continues accepted C-173--C-175 and the hostile-passed
rank-one anchor-exit theorem at commit `ffb16daa`.

The rank-one shell is already rigid: C-175 and the rank-one exit theorem
reduce it to one attacked-anchor restoration.  This note treats the
remaining case in which a minimum state of the second completion fan has
restricted rank

\[
 h\ge2.
\]

The result is a finite exit normal form, not an exclusion.  Every
retained response at a deleting attack descends in rank and has a unique
reverse response back to the fan state.  A one-neighbor attack transfers
to a lower-rank neighboring completion fan.  A multi-neighbor attack
forces one or two complete supported repair fans.  The classification
has a list of 18 formal labeled \((A,M)\) patterns; no claim is made that
all 18 are realizable.  At the full target, the alternatives
collapse further to either lower-rank reversible petals or one common
lower-rank hub.

This does **not** force a restricted kernel.  A reverse move from a
lower-rank state to a higher-rank state is compatible with synchronous
deletion.  No equal-rank induction is used, no dominating state is
declared retained, and no family omission is interpreted as a graph
nonedge.

No complete \(k=3\) theorem, finite exclusion, counterexample, or
resolution of the gamma--theta conjecture is claimed.

## 1. General deletion-petal lemma

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{1.1}
\]

and let \(\mathcal F\) be any eternal family of dominating triples.
Fix distinct vertices \(v,t\), a nonempty set

\[
 B\subseteq V(G)\setminus\{v,t\},
\tag{1.2}
\]

and the source-form ban

\[
 \mathcal B=\{\{v,t,b\}:b\in B\}.
\tag{1.3}
\]

Synchronously peel all dominating triples outside \(\mathcal B\), and
write \(\rho(D)\) for finite deletion rank.  The convention is

\[
 \rho(D)=j
 \quad\Longleftrightarrow\quad
 D\in\Omega_j\setminus\Omega_{j+1}.
\tag{1.4}
\]

Let

\[
 I=\{a,b,c\}\in\mathcal F
\tag{1.5}
\]

be an independent triple containing neither \(v\) nor \(t\), with

\[
 \delta_{\mathcal B}(I)=2,\qquad \rho(I)=h<\infty.
\tag{1.6}
\]

Let \(z\notin I\) be a deletion-witness attack.  Put

\[
 A=N_G(z)\cap I
\tag{1.7}
\]

and let

\[
 M=\{g\in A:I-g+z\in\mathcal F\}
\tag{1.8}
\]

be the retained mover set.

### Theorem 1.1 (descending petal normal form) — PROVED CANDIDATE

Under (1.1)--(1.8):

1. \(A\ne\varnothing\), and \(M\) is a nonempty subset of \(A\).
2. For every \(g\in M\), put
   \[
   D_g=I-g+z.
   \tag{1.9}
   \]
   Then \(D_g\) is unbanned, has finite rank
   \[
   \boxed{\rho(D_g)<h,}
   \tag{1.10}
   \]
   and the attack at the unoccupied vertex \(g\) from \(D_g\) has the
   unique response
   \[
   D_g\xrightarrow{z\to g}I.
   \tag{1.11}
   \]
3. Its Johnson distance is exactly
   \[
   \boxed{
   \delta_{\mathcal B}(D_g)
    =3-\mathbf 1_{\{z\in\{v,t\}\}}
       -\mathbf 1_{\{D_g\cap B\ne\varnothing\}}.}
   \tag{1.12}
   \]
   Consequently
   \[
   \rho(D_g)\ge
   2-\mathbf 1_{\{z\in\{v,t\}\}}
      -\mathbf 1_{\{D_g\cap B\ne\varnothing\}}.
   \tag{1.13}
   \]
4. For every \(s\in A-\{g\}\), the edge \(zs\) is supported by \(D_g\).
   Hence its entire central repair fan is retained:
   \[
   \{z,s,d\}\in\mathcal F
   \qquad(d\in W_{zs}),
   \tag{1.14}
   \]
   and \(W_{zs}\) is a \(G\)-clique.
5. If \(|A|=1\), then \(M=A=\{g\}\), the endpoint \(D_g\) is independent,
   and \(I,D_g\) are two members of the same completion fan over the
   stationary independent pair \(I-\{g\}\).  Their exchange
   \(g\leftrightarrow z\) is unique in both directions.

#### Proof

The retained state \(I\) dominates the attacked vertex \(z\), so
\(A\ne\varnothing\).  Eternal closure supplies a retained physical
response, so \(M\ne\varnothing\).

A one-guard move changes Johnson distance by at most one.  Since
\(\delta_{\mathcal B}(I)=2\), every \(D_g\) has positive distance from
the ban.  It dominates because it belongs to \(\mathcal F\).  Because
\(z\) witnesses deletion of the rank-\(h\) state \(I\), every unbanned
dominating response lies below \(\Omega_h\).  Therefore each retained
response has finite rank strictly below \(h\), proving (1.10).

Return from \(D_g\) by attacking \(g\).  The inserted guard \(z\) hits
\(g\), since \(g\in A\).  The other two guards are the stationary
vertices of the independent source \(I\), so both miss \(g\).
Therefore \(z\to g\) is the unique physical response and returns to
\(I\).  This proves (1.11), including all occupancy and collision
claims.

The endpoint \(D_g\) contains at most one ban anchor: the source contains
none, so only the attacked vertex \(z\) can introduce one.  A banned
state has its two fixed anchors and one vertex of \(B\).  Maximizing the
intersection independently chooses the introduced anchor, if present,
and a member of \(D_g\cap B\), if present.  This gives (1.12).
The accepted Johnson-distance floor C-173 gives (1.13).

For \(s\in A-\{g\}\), the endpoint \(D_g\) co-occupies the edge \(zs\).
The supported-pair saturation theorem C-174 applies and proves (1.14)
and the clique conclusion.

Finally, if \(A=\{g\}\), then \(z\) misses both stationary guards.
Thus \(D_g\) is independent.  The mover \(g\) misses both stationary
guards because \(I\) is independent.  Hence \(g,z\) lie in the same
common-nonneighbor completion set of the stationary pair.  The exchange
is unique in both directions by the same adjacency argument. \(\square\)

The theorem does not assert that a physically possible endpoint omitted
from \(\mathcal F\) is nondominating.  The retained mover set \(M\) may
be any nonempty subset of \(A\).

### Corollary 1.2 (rank-two shell restriction) — PROVED CANDIDATE

If \(h=2\), then every retained endpoint \(D_g\) satisfies

\[
 \boxed{
 z\in\{v,t\}
 \quad\text{or}\quad
 D_g\cap B\ne\varnothing.}
\tag{1.15}
\]

Equivalently, a rank-two state cannot be deleted through a retained
response that stays three Johnson steps from the ban.

In particular, suppose \(z\notin B\cup\{v,t\}\), the source contains a
unique vertex of \(B\), and that vertex is the mover.  Such a response
cannot be retained.

#### Proof

Every retained response has rank at most one by (1.10).  The
Johnson-distance floor and (1.12) rule out distance three.  This is
exactly (1.15). \(\square\)

This restriction is special to rank two.  It is not an equal-rank
recurrence.

## 2. Application to the minimum second completion fan

Return to the accepted C-171/C-173 notation.  The source-color ban is

\[
 \mathcal B_u(x)=\{\{v,t,b\}:b\in B\},
\qquad B=N_{\overline G}(x),
\tag{2.1}
\]

and

\[
 C=C_{ry}
 =V(G)\setminus\bigl(N_G[r]\cup N_G[y]\bigr)
\tag{2.2}
\]

is a nonempty \(G\)-clique.  Every

\[
 K_e=\{r,y,e\}\qquad(e\in C)
\tag{2.3}
\]

is a retained maximum independent triple.  Here

\[
 r\in B,\qquad y\notin B,
\tag{2.4}
\]

and \(K_e\) contains neither ban anchor.  Its Johnson distance is exactly
two.

Assume the source restricted kernel is empty and choose \(e\in C\) of
minimum fan rank

\[
 h=\rho_u(K_e)\ge2.
\tag{2.5}
\]

### Theorem 2.1 (finite higher-rank fan exit) — PROVED CANDIDATE

Let \(z\) be any deletion-witness attack at \(K_e\), and put

\[
 A=N_G(z)\cap\{r,y,e\}.
\tag{2.6}
\]

Then

\[
 A\in
 \bigl\{
 \{r\},\{y\},\{r,y\},\{r,e\},\{y,e\},\{r,y,e\}
 \bigr\}.
\tag{2.7}
\]

For each actual exit, its retained mover set is **some** nonempty subset
\(M\subseteq A\).  Thus every exit belongs to the following list of at
most 18 formal labeled pairs \((A,M)\):

\[
 1+1+3+3+3+7=18
\tag{2.8}
\]

labeled local response forms.  Every retained response has rank below
\(h\) and uniquely returns to \(K_e\).

More structurally:

- If \(A=\{r\}\) or \(A=\{y\}\), the unique response is a lower-rank
  independent state in a neighboring completion fan sharing the other
  two guards with \(K_e\).
- If \(|A|\ge2\), every retained response supports exactly
  \(|A|-1\) incident edges, and each such edge carries its complete
  retained repair fan.

#### Proof

By the minimum-rank choice and the clique exchange inside \(C\), no
attack in \(C-\{e\}\) can witness deletion of \(K_e\).  Every vertex
outside \(C\) is adjacent to \(r\) or \(y\).  Thus

\[
 A\cap\{r,y\}\ne\varnothing.
\tag{2.9}
\]

The six nonempty subsets in (2.7) are exactly the subsets of
\(\{r,y,e\}\) satisfying (2.9).  Eternal closure permits any nonempty
actual retained subset of the physical movers, so the formal list has
the 18 pairs counted in (2.8).
All rank, reverse, singleton-fan, and supported-edge conclusions are
Theorem 1.1. \(\square\)

This is a finite normal form.  It does not claim that every formal pair
in the 18-entry list is realizable under the full C-171 setup.

## 3. Exact target specialization

Put

\[
 R_x=\{x,r,y\},
\qquad
 X_e=\{x,r,e\}.
\tag{3.1}
\]

Accepted C-175 gives the exact static target split

\[
 R_x\text{ dominates}
 \quad\Longleftrightarrow\quad
 C\cap B=\varnothing.
\tag{3.2}
\]

At the attack on \(x\) from \(K_e\), the \(r\)-guard is ineligible,
the \(y\)-guard is always eligible, and the \(e\)-guard is eligible
exactly when \(e\notin B\):

\[
\begin{array}{c|c}
y\to x&X_e,\\
e\to x&R_x\quad(e\notin B).
\end{array}
\tag{3.3}
\]

### Theorem 3.1 (target petals or a common target hub) — PROVED CANDIDATE

The target attack has the following exact family normal form.

1. If \(C\cap B\ne\varnothing\), then \(R_x\) is nondominating and
   \[
   \boxed{X_e\in\mathcal F^\star\quad\text{for every }e\in C.}
   \tag{3.4}
   \]
   For \(e\in B\), \(y\to x\) is the only physical response.  For
   \(e\notin B\), the competing physical endpoint is the nondominating
   state \(R_x\).
2. If \(C\cap B=\varnothing\), then all \(e\in C\) hit \(x\), and
   \(R_x\) dominates.
   - If \(R_x\in\mathcal F^\star\), it supplies the common response
     \(e\to x\) from every \(K_e\).
   - If \(R_x\notin\mathcal F^\star\), then
     \[
     \boxed{X_e\in\mathcal F^\star\quad\text{for every }e\in C.}
     \tag{3.5}
     \]
   Membership of \(X_e\) is unrestricted in the first subcase.
3. Every retained target response has a unique reverse:
   \[
   X_e\xrightarrow[\text{attack }y]{x\to y}K_e,
   \tag{3.6}
   \]
   and, in the second branch,
   \[
   R_x\xrightarrow[\text{attack }e]{x\to e}K_e.
   \tag{3.7}
   \]
4. If \(x\) is a deletion-witness attack at the minimum-rank state
   \(K_e\), then every retained state among \(X_e,R_x\) has rank below
   \(h\) and remains at Johnson distance exactly two.

#### Proof

If \(C\cap B\ne\varnothing\), (3.2) makes \(R_x\) nondominating.  When
\(e\in B\), the edge \(xe\) is absent and \(y\to x\) is the sole
physical response.  When \(e\notin B\), the other physical response
lands at \(R_x\), which cannot belong to the eternal family because it
does not dominate.  Eternal closure therefore forces \(X_e\) in both
cases.

If \(C\cap B=\varnothing\), every \(e\) hits \(x\), so (3.3) lists two
physical responses at every fan state.  If the fixed state \(R_x\) is
retained, it answers all of them.  If it is omitted, closure forces the
other endpoint \(X_e\) for every \(e\).  No conclusion about domination
alone is used to infer family membership.

For (3.6), the guards \(r,e\) miss \(y\), while \(xy\) is an edge.
For (3.7), the guards \(r,y\) miss \(e\), while \(xe\) is an edge.
Thus both reverse moves are unique and all attacks are unoccupied.

Finally, a deletion-witness attack permits no retained unbanned response
of rank at least \(h\).  Both displayed endpoints contain neither ban
anchor and retain the vertex \(r\in B\), so both have distance exactly
two. \(\square\)

The theorem exposes why the two-cycle does not force kernel survival:
the forward target response descends from rank \(h\), while its unique
reverse response is allowed to rise back to rank \(h\).

## 4. Exact finite audit and sharp boundary

The standalone verifier independently exhausts every labeled graph
through order six.  In every graph with

\[
 \gamma=\alpha=\gamma^\infty=3,
\]

it tests every source-form ban (1.3), every retained independent
distance-two state containing neither anchor, and every deletion-witness
exit.  The exact coverage is:

\[
\begin{array}{c|r}
\text{labeled graphs}&33{,}864\\
\text{equality graphs}&2{,}162\\
\text{source-form bans}&469{,}486\\
\text{distance-two retained-state incidences}&207{,}540\\
\text{rank-at-least-two state incidences}&33{,}660\\
\text{deletion exits}&100{,}980\\
\text{singleton / multi-neighbor exits}&67{,}140/33{,}840.
\end{array}
\tag{4.1}
\]

Every higher-rank state in this bounded audit has rank two.  All
100,980 exits satisfy Theorem 1.1, Corollary 1.2, and the singleton or
supported-fan split.

The exact 13-vertex boundary

```text
LEhbtnm~D]xln{
```

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4).
\tag{4.2}
\]

For source anchors \(v=0,t=5\), target-ban set

\[
B=\{3,7,9,10\},
\tag{4.3}
\]

and

\[
K=\{1,10,12\},
\tag{4.4}
\]

the restricted kernel is empty and \(\rho(K)=2\).  Its deletion-witness
attacks have neighbor signatures

\[
\begin{array}{c|c}
z&N(z)\cap K\\ \hline
0&\{10,12\}\\
3&\{1,12\}\\
5&\{1,10,12\}.
\end{array}
\tag{4.5}
\]

Every physical response in these rows is retained at rank one, uniquely
returns to \(K\), and supports respectively one, one, or two complete
repair fans.  This realizes both multi-neighbor forms and shows that
rank-descending reversible petals do not by themselves force a kernel.

The target \(x=8\) is not a deleting attack at \(K\).  Both target
responses are retained:

\[
\rho(\{8,10,12\})=3,\qquad
\rho(\{1,8,10\})=2.
\tag{4.6}
\]

The second is the dominating cross state.  This is the necessary
C-136/C-137 boundary: a dominating or retained target response has no
rank consequence unless the target is the selected deletion-witness
attack.

The control violates \(\gamma=3\), so it is not an instance of the
candidate equality theorem and is not a gamma--theta counterexample.

## 5. Exact remaining gate

The higher-rank exit is now reduced to two finite mechanisms:

1. a lower-rank independent state in a neighboring completion fan; or
2. a lower-rank state supporting one or two complete repair fans.

At the target, these specialize to reversible petals \(X_e\) or a
single common hub \(R_x\).  What remains is to couple the lower-rank
petal/hub deletion witness back to the other two source colors or to the
C-165 anchor-restoration terminal.  This note supplies no valid
induction that repeats the original fan setup at the lower-rank state.

### PROVED CANDIDATE

- The descending-petal theorem and exact distance formula.
- The finite higher-rank second-fan exit, with at most 18 formal
  \((A,M)\) patterns.
- The rank-two shell restriction.
- The exact target-petal/common-hub family split and unique reverse
  responses.

### CERTIFICATE-BACKED FINITE AUDIT

- All 33,864 labeled graphs through order six and all 469,486
  source-form ban instances, with the coverage in (4.1).
- The exact 13-vertex sharp boundary.

### OPEN

- Force one lower-rank petal or hub into the C-165 restoration geometry.
- Couple supported repair fans across all three source colors.
- Prove a surviving restricted kernel, complete \(k=3\), or resolve the
  universal conjecture.
