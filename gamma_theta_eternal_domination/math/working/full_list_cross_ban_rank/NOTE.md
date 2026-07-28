# A trapped rank-zero corridor witness forces an unbanned escape

## Status and scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It uses
the exact one-guard model and continues accepted C-149, C-157, C-163,
C-165, and the reviewed rank-zero corridor transfer theorem in
`full_list_three_color_coupling/NOTE.md`.

The new result resolves one part of the open cross-ban gate.  If the
rank-zero corridor transfer supplied by a missed witness lands inside the
root-swap ban, the transfer cannot remain there.  One additional physical
alternate produces a new witness outside the ban, and two forced attacks
put the **source color** back at that new vertex.

The conclusion is an unbanned retained source-color root state.  If the
source restricted kernel is empty, that state has a finite source-color
deletion rank.  There is no strict rank decrease: the exact MMV-027
control has all three restricted kernels empty and gives rank zero both
before and after the escape.  It has \(\gamma=2\), so it does not satisfy
the equality hypothesis and is not a counterexample to the gamma--theta
conjecture.

The theorem does not prove that a color-restricted kernel survives, close
the all-three-empty branch, prove the complete \(k=3\) case, or resolve
the universal conjecture.  No literature-priority claim is made.

## 1. Exact setup

Assume the parameter-three equality setting

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\qquad
\mathcal F^\star=
\text{the literal greatest eternal family of dominating triples}.
\tag{1.0}
\]

Let

\[
 S=\{u,v,t\}\in\mathcal F^\star
\tag{1.1}
\]

be an independent triple in the literal greatest eternal family of
dominating triples.  Let \(x\notin S\) be full at \(S\), put

\[
 B=N_{\overline G}(x),
\tag{1.2}
\]

and use the root palette

\[
 Q(z)=
 \{s\in S:sz\in E(G),\ S-s+z\in\mathcal F^\star\}.
\tag{1.3}
\]

Fix the source color \(u\).  Assume its C-149 restricted peeling has a
rank-zero nonroot corridor predecessor

\[
 T=\{v,t,q\}=S-u+q
\tag{1.4}
\]

whose deleting attack is the unoccupied vertex \(r\in B\).  The selected
retained response is

\[
 q\longrightarrow r,\qquad
 E=\{v,t,r\}=S-u+r\in\mathcal F^\star,
\tag{1.5}
\]

where

\[
 q\notin S\cup B\cup\{x,r\}.
\tag{1.6}
\]

Let \(v\in Q(r)-\{u\}\).  The accepted C-157 theorem says that the
alternate

\[
 A_v=T-v+r=\{t,q,r\}
\tag{1.7}
\]

is legal and unbanned but nondominating.  Choose any missed witness
\(w\):

\[
 N_G[w]\cap A_v=\varnothing.
\tag{1.8}
\]

Thus

\[
 wt,wq,wr\notin E(G),\qquad
 vw\in E(G),
\tag{1.9}
\]

and the reviewed corridor-transfer theorem further gives

\[
 uw\in E(G)
\tag{1.10}
\]

and retains

\[
 \{w,t,q\},\quad \{w,t,r\}.
\tag{1.11}
\]

We now study the apparently trapped case

\[
 w\in B,\qquad\text{equivalently }xw\notin E(G).
\tag{1.12}
\]

No palette nonmembership is converted into a graph nonedge anywhere
below.

## 2. Ban-escape theorem

### Theorem 2.1 (trapped-witness escape) — PROVED

Under (1.0)--(1.12), the state

\[
H=\{v,q,r\}
\tag{2.1}
\]

is nondominating.  Its missed set is nonempty, and **every** vertex \(y\)
in that missed set satisfies

\[
 y\notin S\cup\{x,q,r,w\}
\tag{2.2}
\]

\[
 yv,yq,yr\notin E(G),
\qquad
 yt,yx,yu\in E(G),
\tag{2.3}
\]

and

\[
 \boxed{S-u+y=\{v,t,y\}\in\mathcal F^\star.}
\tag{2.4}
\]

Consequently

\[
 u\in Q(y),\qquad y\notin B.
\tag{2.5}
\]

In particular, if the reviewed palette transfer is routed through \(w\)
(for example, if \(v\notin Q(q)\)), its banned root state \(S-v+w\)
forces a retained **unbanned** root state for the original source color
\(u\).

If the color-\(u\) restricted kernel is empty, then \(S-u+y\) has a
finite color-\(u\) deletion rank.

#### Proof

Because \(x\) is full at \(S\), the source-color response

\[
 X_u=S-u+x=\{v,t,x\}
\tag{2.6}
\]

is retained.  Attack the unoccupied vertex \(w\) from \(X_u\).  The
guards \(t,x\) miss \(w\) by (1.9) and (1.12), while \(v\) hits \(w\).
Thus the unique response is

\[
 v\longrightarrow w,\qquad
 M=\{w,t,x\}\in\mathcal F^\star.
\tag{2.7}
\]

The retained state \(M\) dominates \(r\).  Both \(w\) and \(x\) miss
\(r\), by (1.8) and \(r\in B\).  Hence

\[
 tr\in E(G).
\tag{2.8}
\]

Return to the rank-zero deleting attack \(r\) from \(T=\{v,t,q\}\).
Equation (2.8) makes \(t\to r\) a physical response, with endpoint

\[
 H=T-t+r=\{v,q,r\}.
\tag{2.9}
\]

The state \(H\) is unbanned for the source color \(u\): a banned state
has the fixed pair \(\{v,t\}\), whereas \(H\) contains \(q\) in place of
\(t\).  At deletion rank zero, every physical unbanned response to a
deleting attack is outside the initial restricted universe.  Since that
universe contains every unbanned dominating triple, \(H\) is
nondominating.

Let \(y\) be an arbitrary vertex missed by \(H\).  Then

\[
 yv,yq,yr\notin E(G).
\tag{2.10}
\]

The retained predecessor \(T\) dominates \(y\); its guards \(v,q\) miss
\(y\), so

\[
 ty\in E(G).
\tag{2.11}
\]

All stated distinctness is literal.  The missed vertex \(y\) is not in
\(H\).  It is not \(t\), because \(tr\) is an edge; not \(u\), because
\(uq\) and \(ur\) are corridor-diamond edges; not \(x\), because \(xq\)
is a corridor-diamond edge; and not \(w\), because \(vw\) is an edge.
Together with the C-149 occupancies, this proves (2.2).

We next prove that \(y\) lies outside \(B\).  Suppose instead that
\(xy\notin E(G)\).  Attack the unoccupied \(r\) from the retained state
\(X_u=\{v,t,x\}\).  The guard \(x\) misses \(r\), while \(v,t\) hit
\(r\) by \(v\in Q(r)\) and (2.8).  These are the only two physical
responses:

\[
\begin{array}{rcl}
 v\to r&:&\{t,x,r\},\\
 t\to r&:&\{v,x,r\}.
\end{array}
\tag{2.12}
\]

The first endpoint misses \(w\), since \(w\) misses \(t,x,r\).  The
second misses \(y\), since \(y\) misses \(v,r\) and we assumed it misses
\(x\).  Neither endpoint dominates, contradicting eternal closure of
\(X_u\).  Therefore

\[
 xy\in E(G),\qquad y\notin B.
\tag{2.13}
\]

We now force the edge \(uy\).  Suppose \(uy\notin E(G)\) and attack the
unoccupied \(y\) from \(M=\{w,t,x\}\).  The physical endpoints are:

\[
\begin{array}{rcl}
 t\to y&:&D_t=\{w,x,y\},\\
 x\to y&:&D_x=\{w,t,y\},\\
 w\to y&:&D_w=\{x,t,y\}\quad\text{if }wy\in E(G).
\end{array}
\tag{2.14}
\]

There are no others.  The endpoint \(D_t\) misses \(r\), because
\(wr,xr,yr\) are all nonedges.  The state \(D_x\) cannot be retained:
at its unoccupied attack \(u\), only \(w\) can move, and the unique
endpoint

\[
 D_x-w+u=\{u,t,y\}
\tag{2.15}
\]

misses \(v\), since \(uv,tv,yv\) are nonedges.  The same argument excludes
\(D_w\) when it is physical: at attack \(u\), only \(x\) can move, again
giving the nondominating endpoint (2.15).  Thus \(M\) would have no
retained response to the attack \(y\), a contradiction.  Hence

\[
 uy\in E(G).
\tag{2.16}
\]

Finally reconsider the attack \(y\) from \(M\).  The endpoint \(D_t\)
is still nondominating, so closure retains at least one of \(D_x,D_w\).
If \(D_x=\{w,t,y\}\) is retained, attack the unoccupied \(v\).  The
guards \(t,y\) miss \(v\), while \(w\) hits it, so the unique response
is

\[
 w\to v,\qquad \{v,t,y\}.
\tag{2.17}
\]

If instead \(D_w=\{x,t,y\}\) is retained, the same attack \(v\) has the
unique responder \(x\), and it has the same endpoint:

\[
 x\to v,\qquad \{v,t,y\}.
\tag{2.18}
\]

Therefore (2.4) holds in every case.  Equations (2.16), (2.4), and the
definition of \(Q\) give \(u\in Q(y)\).  Equation (2.13) makes this
root swap unbanned for color \(u\).  If the restricted kernel is empty,
every retained unbanned dominating triple has a finite deletion rank.
\(\square\)

### Corollary 2.2 (full-terminal witness polarization) — PROVED

Suppose additionally that \(Q(r)=S\).  The two secondary alternates have
nonempty missed-witness sets

\[
\begin{aligned}
W_v&=V(G)\setminus N_G[\{t,q,r\}],\\
W_t&=V(G)\setminus N_G[\{v,q,r\}].
\end{aligned}
\tag{2.19}
\]

Then

\[
\boxed{\text{at most one of }W_v,W_t\text{ meets }B.}
\tag{2.20}
\]

More precisely, if \(W_v\cap B\ne\varnothing\), then every
\(y\in W_t\) lies outside \(B\) and satisfies

\[
uy\in E(G),\qquad S-u+y\in\mathcal F^\star.
\tag{2.21}
\]

The symmetric statement holds with \(v,t\) exchanged.

#### Proof

Choose \(w\in W_v\cap B\) and apply Theorem 2.1.  Its arbitrary-witness
quantifier applies to every \(y\in W_t\), proving (2.21) and
\(W_t\cap B=\varnothing\).  The other implication follows by exchanging
the two secondary colors. \(\square\)

### Collision and one-guard audit

Every displayed attack is unoccupied:

- \(w\notin S\cup\{x,q,r\}\);
- \(r\notin S\cup\{x,q,w\}\);
- every new witness \(y\) satisfies the full distinctness statement (2.2);
- \(u,v\in S\) are absent from the states at which they are attacked.

Every response replaces exactly one occupied guard by the attacked
vertex, and every move edge is explicitly established before use.  The
proof never uses an unrestricted-family attack as a deletion witness for
a different ban.  Restricted rank is invoked only once: rank zero says
that the physical unbanned endpoint \(H\) is nondominating.

## 3. Exact sharp control

Take MMV-027,

```text
JEhbtnm~D]_
```

with

\[
\begin{aligned}
S&=\{0,5,6\},&x&=8,\\
u&=6,&v&=0,&t&=5,\\
q&=2,&r&=10,&w&=3,&y&=1.
\end{aligned}
\tag{3.1}
\]

The standalone checker recomputes

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4),
\qquad |\mathcal F^\star|=122.
\tag{3.2}
\]

It finds

\[
B=\{3,7,9,10\},
\tag{3.3}
\]

so \(r,w\in B\), while \(q,y\notin B\).  The exact palettes are

\[
\begin{aligned}
Q(q)&=\{5,6\},&
Q(r)&=\{0,5,6\},\\
Q(w)&=\{0,6\},&
Q(y)&=\{5,6\}.
\end{aligned}
\tag{3.4}
\]

The source predecessor \(\{0,2,5\}\) has color-6 rank zero.  Its
secondary alternate \(\{0,2,10\}\) misses exactly \(y=1\), and the
original C-157 alternate \(\{2,5,10\}\) misses exactly \(w=3\).
The banned witness endpoint is

\[
S-v+w=\{3,5,6\},
\tag{3.5}
\]

while the theorem's unbanned source-color escape is

\[
S-u+y=\{0,1,5\}.
\tag{3.6}
\]

All three restricted kernels are empty.  Their deletion-round sizes,
in color order \(0,5,6\), are

\[
\begin{array}{c|c}
0&(27,28,32,27,4)\\
5&(18,17,29,50,5)\\
6&(15,28,48,27,1).
\end{array}
\tag{3.7}
\]

Crucially,

\[
\operatorname{rank}_6(\{0,2,5\})
=
\operatorname{rank}_6(\{0,1,5\})
=0.
\tag{3.8}
\]

Thus even all-three-empty peeling permits a rank-preserving trapped
escape.  Any strict-descent theorem must use a hypothesis absent from
this graph, such as \(\gamma=3\); local one-guard closure and the three
empty kernels do not suffice.

The graph has \(\gamma=2\), so (3.2) is a boundary control, not a
gamma--theta counterexample.

## 4. Exact frontier after the theorem

### PROVED in this candidate

- A rank-zero corridor witness inside \(B\) forces the third-anchor edge
  \(tr\).
- The resulting physical alternate has a second missed witness \(y\).
- One-guard closure forces every second witness \(y\notin B\),
  \(uy\in E(G)\), and the
  retained unbanned source-color state \(S-u+y\).
- At a full terminal, the two secondary missed-witness sets cannot both
  meet \(B\).
- Under an empty source kernel, the escape state has finite source rank.

### REFUTED by exact control

- The escape need not have strictly smaller rank.
- Even with all three restricted kernels empty, the source rank can stay
  exactly zero through the escape.

### OPEN

- A strict comparison that genuinely uses \(\gamma=3\).
- A contradiction obtained by iterating the unbanned escape states.
- The positive-rank and anchor-restoration terminal branches.
- Existence of a safe color, the complete \(k=3\) theorem, and the
  universal gamma--theta conjecture.

## 5. Discovery-only evidence

The scripts `scan_catalog.py`, `search_single_trapped_transfer.py`, and
`cegar_trapped_pairs.py` were used only to falsify candidate shortcuts
and locate the proof above.  Their solver-only outcomes are
**OBSERVED**, have no proof logs, and are not used in Theorem 2.1.

In particular, the bounded single-trap equality search reported no model
through order 15.  The order-16 run was stopped at the five-minute gate
without a result; no higher order was attempted.  These statuses are not
finite exclusions.
