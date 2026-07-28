# Hostile review: global witness cascade

Review date: 2026-07-28 PDT

Accepted candidate:
`math/working/global_witness_cascade/NOTE.md`

Accepted source SHA-256:
`1f0e2b5fce583dbc5a485ec7aa767204cd1c581a737cd6256e77224d4cdb2a32`

Manifest SHA-256:
`aaa33cb40012a250ddff56dc23a573d132f7cdabbe1ff1fa22069ce11e6566ec`

## Verdict

**UNCONDITIONAL PASS.**

Theorem 2.1, Corollary 2.2, Lemma 3.1, and Theorem 3.2 are correct in the
stated one-guard-moves model and at the stated scope.  The physical-witness
attack tree is complete, the displayed-collision coverage needed by the
corollary is complete, C-079/C-082/C-104 are invoked within their accepted
hypotheses, and the sealed-cap contradiction covers distinct, doubly
coincident, and triply coincident caps.

The exact scope is important and is stated correctly: this excludes the
canonical complete three-gate boundary with connector lengths
\((1,1,1)\), under \(\gamma(G)=3\), in the unit-free no-full branch where
every outside response list is an exact two-list.  It does not contract an
arbitrary subdivision, exclude a longer odd boundary, handle unit or full
lists, prove all of \(k=3\), or resolve the gamma--theta conjecture.

The frozen 21-vertex control also passes a clean-room reconstruction.  Its
parameters, selected family, 15,174 attack obligations, response data,
three complete gates, three dynamic critical witnesses, 114 dominating
pairs, and 1,237-state greatest triple kernel are exact.

## 1. Exact one-guard semantics

I audited every argument against

\[
 \forall D\in\mathcal F\ \forall r\notin D\
 \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal F,
\]

with every state in \(\mathcal F\) dominating.  Each displayed response
changes one guard, the mover must be adjacent in \(G\) to the attacked
vertex, and every attack used is at an unoccupied vertex.

When the proof examines all three successor *shapes*, an unavailable move
edge only deletes one of those shapes.  It cannot create a fourth
one-guard successor.  Consequently it is sound to rule out every shape by
family absence or nondomination without asserting unlisted move edges.
No missing family response is converted into a graph nonedge.

A state that misses a vertex \(w\) is legitimately rejected immediately:
\(w\) is unoccupied, no guard is adjacent to it in \(G\), and the legal
attack at \(w\) has no mover.

## 2. Line-by-line audit of Theorem 2.1

All twelve symbols

\[
 a,b,c,x,u,v,y,s,t,o,m,q
\]

are distinct.  This makes every attack below unoccupied exactly where
claimed.

The hypothesis \(c\in L(u)\) retains
\(A_0=\{a,b,u\}\).  On attacking \(x\):

- the \(u\)-replacement is the absent direct swap
  \(\{a,b,x\}\);
- the \(a\)-replacement \(\{b,u,x\}\) misses \(s\), using
  \(bs,us,xs\in E(H)\);
- therefore closure forces the only remaining shape
  \(A_1=\{a,u,x\}\).

On attacking \(t\) from \(A_1\):

- the \(x\)-replacement \(\{a,u,t\}\) misses \(v\), using
  \(av,uv,tv\in E(H)\);
- the \(u\)-replacement \(\{a,x,t\}\) is dead under the unoccupied attack
  at \(b\): \(a\) has no move edge because \(ab\in E(H)\), and the other
  successors are the two absent direct swaps
  \(\{a,b,t\}\) and \(\{a,b,x\}\);
- closure therefore forces \(A_2=\{u,x,t\}\).

The dead-state ladder used next is complete.

1. For \(r,s\in\{y,o,m\}\), the state \(\{c,r,s\}\) is dead under an
   attack at \(a\).  The guard at \(c\) is frozen by \(ac\in E(H)\);
   the other two shapes are direct swaps excluded by
   \(b\notin L(r)\cup L(s)\).
2. The state \(\{y,o,m\}\) is dead under an attack at \(c\), because all
   three successors are states from item 1.
3. Each of \(\{y,t,o\}\) and \(\{u,y,o\}\) is dead under an attack at
   \(m\).  The \(y\)- and \(o\)-guards are frozen by
   \(ym,om\in E(H)\), and the only remaining shape is
   \(\{y,o,m\}\).
4. The state \(\{u,t,o\}\) misses \(v\), using
   \(uv,tv,ov\in E(H)\).
5. Hence \(\{u,y,t\}\) is dead under an attack at \(o\): its three
   shapes are exactly \(\{y,t,o\}\), \(\{u,t,o\}\), and
   \(\{u,y,o\}\).

Attack \(y\) from \(A_2\).  The \(t\)-guard is frozen because
\(ty\in E(H)\), and the \(x\)-replacement is the dead state
\(\{u,y,t\}\).  Closure therefore forces
\(A_3=\{x,y,t\}\).

Finally attack \(a\) from \(A_3\).

- The \(y\)-replacement is the already dead state \(\{a,x,t\}\).
- The \(t\)-replacement \(\{a,x,y\}\) misses \(q\), using
  \(aq,xq,yq\in E(H)\).
- The \(x\)-replacement \(\{a,y,t\}\) is dead under an attack at \(o\).
  Its \(a\)-replacement is the dead state \(\{y,t,o\}\), its
  \(y\)-replacement \(\{a,t,o\}\) misses \(v\), and its
  \(t\)-replacement \(\{a,y,o\}\) is dead under an attack at \(c\).
  In that last attack the \(a\)-guard is frozen by \(ac\in E(H)\), while
  the other shapes are the absent direct swaps
  \(\{a,c,y\}\) and \(\{a,c,o\}\).

Thus all three possible responses to the final attack are absent.  The
independent symbolic checker reconstructed 11 dead-state attacks, five
nondomination certificates, and all three forced transitions, with no
uncovered successor.

## 3. Collision coverage in Corollary 2.2

For \(P_a=\{b_0,c_1\}\), the exact map from the canonical complete
geometry to Theorem 2.1 is

\[
\begin{aligned}
 x&=c_1,&u&=a_0,&v&=a_1,&y&=b_0,\\
 s&=b_\ast,&t&=c_\ast,
\end{aligned}
\]

with \(o,m\) the type-\(b\) original port and physicalization midpoint
on the \(a_1\)--\(b_0\) gate.

The type data give

\[
 c\in L(a_0),\quad
 c\notin L(c_1)\cup L(c_\ast),\quad
 b\notin L(b_0)\cup L(o)\cup L(m),
\]

and the two adjacent full gates plus the length-one \(a\)-connector give
every complement edge in (1.4).  Thus Theorem 2.1 applies literally to
this critical pair and cyclically to the other two.

The no-dominating-pair consequence of \(\gamma(G)=3\) supplies a common
complement neighbor of every critical pair.  Accepted C-104 divides the
possibilities as follows:

- a nondisplayed neighbor has the exact missing-anchor type;
- a displayed type-\(b\) or type-\(c\) collision is impossible;
- a displayed type-\(a\) collision is physical to \(a\).

The two adjacent type-\(a\) connector endpoints cannot be the common
neighbor: \(a_0c_1\) and \(a_1b_0\) are the two failed direct incidences
and therefore are \(G\)-edges.  Any other physical type-\(a\) candidate
that is distinct from the local auxiliary roles is excluded by Theorem
2.1.  The local cap roles \(b_\ast,c_\ast\) are the already excluded
wrong types, while \(o,m\) omit \(b\) and so cannot simultaneously have
the exact type \(a\) forced by C-104.  Anchors, critical endpoints, and
loops were already exhausted in C-104.

This covers the displayed collisions needed for the corollary.  A
remaining common neighbor is therefore dynamic to the missing anchor and
has the exact third-type list.  The cyclic witnesses have lists
\(\{b,c\},\{a,c\},\{a,b\}\), so they are necessarily distinct.

No arbitrary collision or subdivision theorem is being smuggled into this
step; the coverage uses the vertex-distinct canonical complete geometry.

## 4. C-082 and C-079 in the cascade

For the dynamic type-\(a\) witness \(q_a\), the pair
\(\{a,q_a\}\) does not dominate because \(\gamma(G)=3\).  Its common
complement neighbor \(r_a\) cannot be \(b\) or \(c\), since
\(b,c\in L(q_a)\) force \(bq_a,cq_a\in E(G)\).  Also
\(a\notin L(r_a)\), because \(ar_a\in E(H)\).  Exact two-list typing
therefore gives \(L(r_a)=\{b,c\}\).

The edge \(q_ar_a\in E(H)\) has two endpoints omitting \(a\), so accepted
C-082 applies.  Its “outside positive cap” conclusion is available
because at least one endpoint, namely the dynamic witness \(q_a\), is
adjacent to \(a\) in \(G\).  Hence it supplies an outside vertex \(z_a\)
with

\[
 q_az_a,r_az_a\in E(H),\qquad a\in L(z_a).
\]

To prove sealing, suppose an outside \(a\)-positive vertex \(p\) were
adjacent to \(z_a\) in \(H\).  Accepted C-079 applies with

\[
 \text{positive tail}=p,\quad
 \text{common port}=z_a,\quad
 (v_0,v_1)=(q_a,r_a).
\]

All four vertices are distinct: the open-neighborhood incidences exclude
equal endpoints, and the positive/omitted-\(a\) lists separate \(p\) from
\(q_a,r_a\).  The required complement edges are

\[
 pz_a,\ z_aq_a,\ z_ar_a,\ q_ar_a.
\]

This is exactly the forbidden length-one odd fan.  Therefore
\[
 N_H(z_a)\cap P_a^+=\varnothing.
\]

The same argument applies cyclically.  It uses literal complement edges
and family-list membership only in the directions proved by the accepted
dependencies.

## 5. Sealed-cap incompatibility, including coincidences

For distinct \(z_i,z_j\), \(\gamma(G)=3\) gives a common complement
neighbor \(w\).

- If \(w\) is outside \(S\), sealing at \(z_i\) and \(z_j\) makes
  \(i,j\notin L(w)\).  An exact two-subset of a three-element anchor set
  cannot omit two colors.
- If \(w\in S\), it cannot equal \(i\) or \(j\), because
  \(i\in L(z_i)\) and \(j\in L(z_j)\) force the corresponding \(G\)-edges.
  Thus \(w=k\).  The two complement incidences to \(k\) exclude \(k\)
  from both cap lists, so exact size two forces
  \[
  L(z_i)=L(z_j)=\{i,j\}.
  \]

If the three caps are pairwise distinct, applying the last identity to
\((z_a,z_b)\) and \((z_b,z_c)\) gives incompatible lists for \(z_b\).

If all three caps coincide, the common list contains \(a,b,c\), contrary
to exact size two.

If exactly two collide, say \(z_i=z_j=z\ne z_k\), then
\(L(z)=\{i,j\}\).  A common complement neighbor of the distinct pair
\(\{z,z_k\}\) cannot be outside: the two sealing conditions at the
single collided vertex would make it omit both \(i\) and \(j\).  It
cannot be an anchor either: \(i,j\in L(z)\) block the first two anchors
by \(G\)-edges, and \(k\in L(z_k)\) blocks the third.  This is a complete
contradiction.

These are all set-partition patterns of three labeled caps.  The proof
does not assume the caps are distinct.

## 6. Exact-two-list and theorem scope

From the retained independent anchor state \(S\), every outside vertex is
a legal unoccupied attack and therefore has a nonempty response list.
The unit-free branch excludes singleton lists and the no-full branch
excludes three-element lists.  Thus every outside list is an exact
two-subset of \(S\), exactly as required by Lemma 3.1 and the uses of
C-104.

The proof also needs all three full gate gadgets, not only the three dead
boundaries.  The original-port and physicalization-midpoint data are used
inside Theorem 2.1.  The note correctly limits Theorem 3.2 to the complete
canonical length-\((1,1,1)\) geometry.  The bounded SAT rows in Section 4
are labeled discovery/control evidence; no mathematical conclusion here
depends on trusting their UNSAT outputs.

## 7. Independent reconstruction of the 21-vertex control

The checker
`reviews/global_witness_cascade_hostile/independent_check.py` imports no
candidate verifier, search implementation, NetworkX routine, or campaign
evaluator.  It independently decodes

```text
TBn]r]vj]lnZ~^~n~z~^z|~nz~^j~~t~~n^~
```

from the graph6 bitstream and verifies that its complement edge set equals
the explicit JSON data.

The reconstruction found:

| quantity | independently checked value |
|---|---:|
| order | 21 |
| size | 174 |
| \(\gamma\) | 2 |
| \(i\) | 2 |
| \(\alpha\) | 3 |
| \(\gamma^\infty\) | 3 |
| \(\theta\) | 3 |
| dominating pairs | 114 |
| independent dominating pairs | 24 |
| selected eternal triples | 843 |
| unoccupied-attack obligations | 15,174 |
| retained legal responses | 25,764 |
| greatest one-guard kernel | 0 |
| greatest two-guard kernel | 0 |
| greatest triple kernel | 1,237 |

For the parameters:

- there is no dominating singleton and there are 114 dominating pairs;
- 24 of those pairs are independent, proving \(i=2\);
- \(\{0,1,2\}\) is independent and no independent four-set exists;
- the supplied complement coloring is a proper three-coloring, while
  \(\{0,1,2\}\) is a complement triangle;
- the one- and two-guard greatest kernels are empty, while the selected
  843-state triple-family is eternal.

The checker verified every selected state dominates and replayed every
one-guard response obligation.  It computed the response lists directly
from selected-family membership and obtained exact two-lists on all 18
outside vertices.

It also reconstructed the three full gates:

\[
\begin{array}{c|ccccc}
&\text{left}&\text{right}&\text{cap}&\text{original}&\text{middle}\\ \hline
0&6&3&9&12&15\\
1&7&4&10&13&16\\
2&8&5&11&14&17,
\end{array}
\]

including every anchor incidence, cap arm, original two-edge path, and
failed direct \(G\)-incidence, plus the three length-one connectors
\((3,7),(4,8),(5,6)\).

The critical pairs have the unique displayed common complement neighbors

\[
 \{4,6\}\mapsto18,\qquad
 \{5,7\}\mapsto19,\qquad
 \{3,8\}\mapsto20,
\]

with exact lists \(\{1,2\},\{0,2\},\{0,1\}\), respectively.  Each witness
is adjacent in \(G\) to its missing anchor.  The next three pairs
\(\{0,18\},\{1,19\},\{2,20\}\) have no common complement neighbor and
are dominating pairs, precisely exhibiting the advertised
\(\gamma=2\) stopping boundary.

## 8. Reproduction and hashes

Run:

```text
python3 -I -B -W error \
  gamma_theta_eternal_domination/reviews/global_witness_cascade_hostile/independent_check.py
```

The command is deterministic and warning-free under Python 3.14.6.
Exact source, dependency, checker, and control hashes are recorded in
`evidence.json`.
