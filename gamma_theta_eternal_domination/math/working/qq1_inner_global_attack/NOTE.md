# A cross-layer QQ1 bridge and the exact two-witness boundary

## Status and exact scope

Date: 2026-07-28 (PDT)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and let \(\mathcal K\) be the literal greatest one-guard eternal family
of dominating triples.  Retain the accepted C-158 canonical rank-one
QQ1 normal form:

\[
 T=\{x,p,q\}\in\mathcal K,\qquad
 B=\{u,p,q\}\notin\mathcal K,\qquad \rho(B)=1,
\tag{0.2}
\]

\[
 u\mathrel{\triangleright}x,\qquad
 x\not\mathrel{\triangleright}u,
\tag{0.3}
\]

and

\[
\begin{array}{c|l}
\text{\(G\)-edges}
 &ux,ur,pr,qr,pb,qc,xb,xc,bc,up,uq,\\
\text{\(G\)-nonedges}
 &xp,xq,pq,xr,\ bu,br,bq,\ cu,cr,cp.
\end{array}
\tag{0.4}
\]

The state

\[
 U=\{u,b,c\}
\tag{0.5}
\]

is retained.  Fix a common nonneighbor

\[
 d\in C_{xr}
 =\{v\notin\{x,r\}:vx,vr\notin E(G)\}.
\tag{0.6}
\]

Accepted C-158 makes \(d\) adjacent to \(p,q\), and accepted C-143
makes

\[
 O=\{u,r,d\}
\tag{0.7}
\]

dominating.  The inactive orientation in (0.3) makes \(O\) omitted.

This note proves one global coupling that was absent from the first
hot-layer analysis.

> **Cross-layer bridge theorem — PROVED CANDIDATE.**  For every
> \[
> w\in W_{ud}
>   =\{v\notin\{u,d\}:vu,vd\notin E(G)\}
> \]
> and every
> \[
> z\in W_{ux}
>   =\{v\notin\{u,x\}:vu,vx\notin E(G)\},
> \]
> one has
> \[
> \boxed{\{u,w,z\}\in\mathcal K.}
> \tag{0.8}
> \]

Both sets are nonempty under \(\gamma(G)=3\).  Thus the two global
pair-witness layers cannot be chosen independently: their full Cartesian
product is coupled by retained states.

The theorem does **not** eliminate QQ1.  Two independently checked
16-vertex graphs prove the sharp boundary:

1. the first realizes the canonical QQ1 core, the \(ud\)-edge hot
   witness, the original \(ux\)-witness, (0.8), and the saturated outer
   bow tie, but \(\{p,w\}\) dominates;
2. the second additionally supplies a common nonneighbor of
   \(\{p,w\}\), but has other dominating pairs.

Both controls have

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3).
\tag{0.9}
\]

They are not counterexamples.  They refute only the proposed shortcut
that the two most obvious \(\gamma=3\) witness obligations, even with one
further pair repair, already contradict the local QQ1 dynamics.

## 1. Retaining the completion and hot states

Put

\[
 I=\{x,r,d\}.
\tag{1.1}
\]

This is an independent triple, hence \(I\in\mathcal K\).  The reverse
state \(O=I-x+u\) dominates by C-143 and is omitted by (0.3) and C-108.
Since \(u,r\) both miss \(b,c\), domination by \(O\) forces

\[
 db,dc\in E(G).
\tag{1.2}
\]

### Lemma 1.1 (retained completion state) — PROVED CANDIDATE

The state

\[
 A=\{u,x,d\}
\tag{1.3}
\]

belongs to \(\mathcal K\).

#### Proof

Attack the unoccupied vertex \(d\) from \(U=\{u,b,c\}\).  The guards
\(b,c\) are eligible by (1.2).  If \(u\) is eligible, its successor
\(\{d,b,c\}\) misses \(r\); if \(u\) is ineligible, that branch is
absent.  Closure therefore retains at least one of

\[
 \{u,d,c\},\qquad \{u,b,d\}.
\tag{1.4}
\]

Attack \(x\) from a retained state in (1.4).  The guard \(d\) is
ineligible.  The \(u\)-successor misses \(r\), while the remaining side
guard moves to \(x\) and produces \(A\).  Hence \(A\in\mathcal K\).
\(\square\)

Now let \(w\in W_{ud}\).  Since \(A\) dominates \(w\), while \(u,d\)
miss it,

\[
 wx\in E(G).
\tag{1.5}
\]

At the attack \(w\) from \(A\), the unique eligible guard is \(x\).
Consequently

\[
 K_w=\{u,d,w\}\in\mathcal K.
\tag{1.6}
\]

These two short derivations are included here so that the bridge theorem
does not depend on the still-separate hot-layer candidate.

## 2. The cross-layer bridge

### Theorem 2.1 (cross-layer retained product) — PROVED CANDIDATE

For every \(w\in W_{ud}\) and \(z\in W_{ux}\),

\[
 D_{w,z}=\{u,w,z\}\in\mathcal K.
\tag{2.1}
\]

#### Proof

If \(z=d\), then \(D_{w,z}=K_w\), so (2.1) is (1.6).  Assume
\(z\ne d\).  The retained state \(A=\{u,x,d\}\) dominates \(z\).
Since \(z\) misses \(u,x\),

\[
 dz\in E(G).
\tag{2.2}
\]

Attack the unoccupied vertex \(z\) from \(K_w=\{u,d,w\}\).  The guard
\(u\) is ineligible, \(d\) is eligible by (2.2), and \(w\) may or may
not be eligible.  The two possible successors are

\[
\begin{array}{rcl}
 d\to z&:&D_{w,z}=\{u,w,z\},\\
 w\to z&:&C_z=\{u,d,z\}.
\end{array}
\tag{2.3}
\]

Suppose for contradiction that \(D_{w,z}\notin\mathcal K\).  Closure
of \(K_w\) forces \(C_z\in\mathcal K\); in particular, the edge \(wz\)
must exist if this second branch is used.

Attack the unoccupied vertex \(r\) from \(C_z\).  The guard \(d\)
misses \(r\).  Moving \(u\) produces

\[
 C_z-u+r=\{r,d,z\},
\tag{2.4}
\]

which misses \(x\), because \(xr,xd,xz\notin E(G)\).  If \(z\) is
adjacent to \(r\), moving \(z\) produces

\[
 C_z-z+r=\{u,d,r\}=O\notin\mathcal K.
\tag{2.5}
\]

If \(z\) misses \(r\), the second move is simply graph-ineligible.
Thus \(C_z\) has no retained response at \(r\), contradicting
\(C_z\in\mathcal K\).  Therefore \(D_{w,z}\in\mathcal K\).
\(\square\)

Every attack in this proof is at an unoccupied vertex.  Every displayed
transition moves exactly one guard along one graph edge.  The omission
of \(O\) is used only as a family obstruction in (2.5); it is never
converted into a graph nonedge.

### Corollary 2.2 (side coverage) — PROVED CANDIDATE

For every \(w\in W_{ud}\) and \(z\in W_{ux}\),

\[
 (wb\in E(G)\ \lor\ zb\in E(G))
 \quad\text{and}\quad
 (wc\in E(G)\ \lor\ zc\in E(G)).
\tag{2.6}
\]

Indeed, \(D_{w,z}\) dominates \(b,c\), while \(u\) misses both.

This couples the two witness cliques.  For example, if one hot witness
\(w\) misses \(b\), then every \(ux\)-witness \(z\) hits \(b\).
It does not force all cross edges \(wz\).

### Corollary 2.3 (the \(ud\)-edge inner geometry) — PROVED CANDIDATE

Assume \(ud\in E(G)\), take \(w\in W_{ud}\), and
\(z\in W_{ux}\).  Then \(z\ne d\), and:

1. if \(wz\in E(G)\), the five vertices
   \[
   u,d,z,w,x
   \]
   induce the cycle
   \[
   u-d-z-w-x-u;
   \tag{2.7}
   \]
2. if \(wz\notin E(G)\), the bridge state \(D_{w,z}\) is an independent
   triple.

For item 1, the five cycle edges are \(ud,dz,zw,wx,xu\).  The five
nonconsecutive pairs \(uz,uw,dw,dx,zx\) are all nonedges by the
definitions of \(W_{ud},W_{ux},C_{xr}\).  Item 2 is immediate because
\(u\) misses both \(w,z\).

The first control below realizes item 1.  A separate discovery model
realizes item 2, so neither branch is contradictory from the displayed
data alone.

## 3. First exact boundary: both global witness layers

The labeled graph

```text
OslallyN]z~r|^{~|^|~^
```

has order \(16\), size \(90\), and uses

\[
 u,x,p,q,r,b,c,d,w,z=0,1,\ldots,9.
\tag{3.1}
\]

The standalone verifier recomputes

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3),
\qquad |\mathcal K_3|=371.
\tag{3.2}
\]

It verifies:

\[
\begin{aligned}
W_{ux}&=\{z\},&
W_{ud}&=\{w\},&
ud,wz&\in E(G),\\
\rho(B)&=1,&
\rho(O)&=3,&
D_{w,z}&\in\mathcal K.
\end{aligned}
\tag{3.3}
\]

The outer completion sets are

\[
 \mathcal S_w=\{b\},\qquad
 \mathcal T_w=\{11\},
\tag{3.4}
\]

and the mixed state \(\{b,w,11\}\) is retained.  Thus this graph also
realizes the saturated outer bow tie from the hot-layer candidate.

Nevertheless,

\[
 \{p,w\}=\{2,8\}
\tag{3.5}
\]

dominates.  The graph has 29 dominating pairs in total.  Hence it lies
at the exact \(\gamma=2\) boundary and proves:

\[
\boxed{
W_{ux}\ne\varnothing,\quad W_{ud}\ne\varnothing,\quad
\text{and the cross-layer bridge do not force }\gamma=3.
}
\tag{3.6}
\]

## 4. Second exact boundary: repairing \(\{p,w\}\)

The labeled graph

```text
OslallyN]fv|y~v^}n}{n
```

also has order \(16\), now with size \(87\).  Under the same labels
(3.1), the verifier recomputes

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3),
\qquad |\mathcal K_3|=347,
\tag{4.1}
\]

as well as the same data

\[
W_{ux}=\{z\},\qquad W_{ud}=\{w\},\qquad
\rho(B)=1,\qquad \rho(O)=3.
\tag{4.2}
\]

This time

\[
 N_{\overline G}(p)\cap N_{\overline G}(w)=\{15\},
\tag{4.3}
\]

so \(\{p,w\}\) no longer dominates.  The same vertex \(15\) is the
unique completion of \(\{d,w\}\), while
\(\mathcal S_w=\{b\}\), and \(\{b,w,15\}\) is retained.

The repair does not produce equality.  There are 21 dominating pairs.
Those with at least one endpoint among the ten named vertices are

\[
\begin{split}
 &(q,14),\\
 &(b,11),(b,13),(c,12),\\
 &(d,12),(d,13),\\
 &(w,11),(w,13),(w,14),\\
 &(z,10),(z,12),(z,15).
\end{split}
\tag{4.4}
\]

In particular, \(\{q,14\}\) is an explicit dominating pair.  Equation
(4.4) is a fixed-graph fact, not a claim that any one of these pairs is
universally forced.

The second control proves that adding the first natural pair repair to
(3.6) still does not force \(\gamma=3\).  A universal proof must couple
the resulting witness obligations globally rather than selecting one
more pair in isolation.

## 5. Discovery ledger and what is not certified

The two displayed graphs are **independently exact fixed controls**:
the verifier decodes their graph6 strings and recomputes all five
parameters, greatest triple kernels, deletion ranks, named witness sets,
retained states, outer completion sets, clique partitions, and every
dominating pair without importing the discovery encoder.

The route by which they were found remains only **OBSERVED**:

1. a one-solver SAT probe first found a simultaneous \(W_{ux},W_{ud}\)
   model at order 16;
2. blocking \(\{p,w\}\) found the second order-16 model;
3. a discovery-only CEGAR run at order 16 reached `UNSAT` after adding
   13 pair constraints; reverse deletion left the order-specific set
   consisting of \(\{u,x\}\) and all \(\{p,v\},\{q,v\}\) for
   \(10\le v\le15\);
4. the analogous order-17 trace used a different 21-step set.

There are no proof logs, independent CNF reconstruction, or all-order
coverage theorem for those UNSAT traces.  They are not finite
exclusions and do not prove an infinite ladder.  The changing CEGAR
cores are evidence against promoting an order-specific pattern to a
universal lemma.

## 6. Exact remaining gate

The proved candidate advance is the retained product

\[
 W_{ud}\times W_{ux}
 \longrightarrow \mathcal K,\qquad
 (w,z)\longmapsto\{u,w,z\}.
\tag{6.1}
\]

The controls delimit what remains:

1. the two primary pair-witness layers can coexist;
2. their inner bridge and outer bow ties can all be retained;
3. one additional dominating pair can be repaired without destroying
   the QQ1 dynamics; and
4. the escape moves to a collection of new dominating pairs involving
   the auxiliary layer.

Thus the next universal step must prove a well-founded global
obstruction—rank descent, a finite-cycle contradiction, or a
simultaneous pair-cover theorem.  Merely demanding the two most visible
common nonneighbors, or iterating an empirically selected dominating
pair, is insufficient.

From the campaign root, reproduce the exact audit with

```text
sh math/working/qq1_inner_global_attack/verify_strict.sh
```

