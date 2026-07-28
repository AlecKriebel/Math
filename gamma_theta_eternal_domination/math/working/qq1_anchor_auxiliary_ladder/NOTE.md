# The QQ1 anchor–auxiliary ladder is not an all-order obstruction

## Status and exact scope

Date: 2026-07-28 (PDT)

The order-\(16\) and order-\(17\) discovery probes suggested the
following possible all-order shortcut in the canonical rank-one QQ1
normal form:

> protect the original pair \(\{u,x\}\), and require every pair
> \(\{p,v\},\{q,v\}\) with \(v\) outside the ten named core vertices to
> be non-dominating.

That shortcut is **false**.  This note freezes an exact order-\(18\)
control which satisfies a strictly stronger anchor-protection condition:

\[
 \boxed{
 \text{no dominating pair has an endpoint in }
 T=\{x,p,q\}.
 }
\tag{0.1}
\]

The graph also realizes the complete named QQ1 collision, the retained
hot-layer corners and outer bow tie of C-166, and the cross-layer bridge.
Nevertheless it has thirty dominating pairs away from \(T\), including
\(\{u,14\}\).  Its exact parameter vector is

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3).
\tag{0.2}
\]

Thus this graph is a sharp \(\gamma=2\) boundary control, not a
counterexample to the gamma--theta conjecture.  It refutes only the
proposed inference from protected distinguished anchors to
\(\gamma=3\).  The order-\(16\) and order-\(17\) solver outcomes remain
uncertified finite observations.

## 1. The fixed graph

Use the labeled graph6 record

```text
QslallyN\~Y^v^|^z~~V|ve~^}G
```

on vertices \(0,\ldots,17\), with

\[
 u,x,p,q,r,b,c,d,w,z=0,1,\ldots,9.
\tag{1.1}
\]

Pinned nauty 2.9.3 `labelg` gives the canonical graph6 identifier

```text
QpMu]qnvvJb~Tz]mnx~nnZ~|~~W
```

The graph has order \(18\), size \(114\), labeled-graph6 SHA-256

```text
99ddf436936152440c778efb79270a89e10feb8dd95d7033052e571a1bc3142c
```

and sorted edge-list SHA-256

```text
6a6256204cff1a80d67e16be7efa67377f02b5c9d7c6a924cf6bbfc4ec7b738e
```

The standalone verifier decodes the labeled graph6 string and emits the
complete 114-edge list.  It does not import the discovery encoder or a
campaign evaluator.

## 2. Exact parameter audit

Direct subset enumeration gives

\[
 \gamma=2,\qquad i=3,\qquad \alpha=3.
\tag{2.1}
\]

For one and two guards the literal greatest one-guard eternal kernels
are empty.  Every one of the thirty dominating pairs is deleted in the
first synchronous round.  For three guards, the greatest kernel has
\(473\) configurations.  Its deletion-wave sizes are

\[
 2,8,11,28,33,18,17,34,18.
\tag{2.2}
\]

Therefore \(\gamma^\infty=3\).  The independent triple
\[
 T=\{x,p,q\}
\tag{2.3}
\]
proves \(\alpha\ge3\), while exhaustive rejection of independent
four-sets proves \(\alpha=3\).  Since an independent set meets every
clique part at most once, \(\theta\ge\alpha=3\).  The following
three-clique partition proves the reverse inequality:

\[
\begin{split}
 &(0,3,7,10,11,12,13,14),\\
 &(2,4,8,9,15),\\
 &(1,5,6,16,17).
\end{split}
\tag{2.4}
\]

Hence (0.2) is exact.

## 3. The complete named QQ1 boundary survives

The graph has all canonical QQ1 edges

\[
\begin{split}
 ux,up,uq,ur,\ pr,qr,\ pb,qc,\ xb,xc,bc
\end{split}
\tag{3.1}
\]

and nonedges

\[
 xp,xq,pq,xr,\ ub,br,bq,\ uc,cr,cp.
\tag{3.2}
\]

For

\[
 B=\{u,p,q\},
\tag{3.3}
\]

the unoccupied attack at \(r\) has exactly the three graph-eligible
successors.  They miss \(x,b,c\), respectively, so \(B\) has literal
deletion rank one.  The retained independent endpoint
\[
 T=\{x,p,q\}
\]
has the \(u\to x\) activity root
\[
 \{u,b,w\}\longrightarrow\{x,b,w\},
\tag{3.4}
\]
while the reverse \(x\to u\) endpoint is exactly the omitted state
\(B\).

For the completion \(d\), hot witness \(w\), and \(ux\)-witness \(z\),
the exact witness sets are

\[
 W_{ux}=\{z\},\qquad W_{ud}=\{w\},\qquad
 W_{pw}=\{16\}.
\tag{3.5}
\]

The states

\[
\begin{array}{lll}
 U=\{u,b,c\},&R=\{r,b,c\},&I=\{x,r,d\},\\
 A=\{u,x,d\},&K=\{u,d,w\},&E=\{x,d,w\},\\
 F=\{r,d,w\},&&
\end{array}
\tag{3.6}
\]

all belong to the literal greatest family.  The state
\[
 O=\{u,r,d\}
\tag{3.7}
\]
dominates but has deletion rank three.  The C-167 bridge

\[
 \{u,w,z\}
\tag{3.8}
\]

is retained.  The two outer completion sets are

\[
 C_{uw}=\{b\},\qquad C_{dw}=\{16\},
\tag{3.9}
\]

and the outer bow-tie state \(\{b,w,16\}\) is retained.  Thus the
order-\(18\) escape does not discard the previously proved local
dynamic structure.

## 4. Strong anchor protection and the actual escape

The discovery core required only \(\{u,x\}\) and the sixteen pairs

\[
 \{p,v\},\{q,v\}\qquad(10\le v\le17)
\tag{4.1}
\]

to be non-dominating.  The fixed graph satisfies much more.  Exhaustive
pair checking gives

\[
 \forall\,t\in\{x,p,q\},\ \forall\,v\ne t:
 \quad \{t,v\}\text{ is non-dominating}.
\tag{4.2}
\]

In particular, not one of the thirty dominating pairs touches the
distinguished maximum independent endpoint \(T\).

There are twenty core--auxiliary dominating pairs and ten
auxiliary--auxiliary dominating pairs.  The first few are

\[
 \{u,14\},\quad \{u,17\},\quad \{r,14\},\quad
 \{b,10\},\quad \{d,12\},\quad \{w,10\},\quad \{z,11\},
\tag{4.3}
\]

and the verifier emits and checks the complete list.  Thus the exact
failure is not at either distinguished QQ1 anchor \(p,q\), nor even at
the full independent endpoint \(T\): domination migrates to pairs
formed entirely in \(V(G)\setminus T\).

This also explains why a naive fresh-witness descent fails.  Witnesses
can recycle in short finite cycles.  For example,

\[
\begin{array}{lll}
 C_{\overline G}(p,11)=\{16\},&
 C_{\overline G}(p,16)=\{11\},\\[2mm]
 C_{\overline G}(p,14)=\{17\},&
 C_{\overline G}(p,17)=\{14\},\\[2mm]
 C_{\overline G}(q,5)=\{15\},&
 C_{\overline G}(q,15)=\{5\}.
\end{array}
\tag{4.4}
\]

Consequently a complement-signature argument relative only to
\(\{x,p,q\}\) has no well-foundedness: the common-nonneighbor
obligations need not create new vertices.

## 5. Audit of the discovery encoding

The discovery probe did **not** encode full \(\gamma\ge3\).  Its exact
ingredients at order \(n\) were:

1. the canonical QQ1 incidence and saturated core;
2. \(\alpha\le3\);
3. the independent-pair extension condition \(i\ge3\);
4. one arbitrary nonempty family of dominating triples with literal
   one-guard, one-edge closure at every unoccupied attack;
5. the retained endpoint \(T\), omitted reverse state \(B\), and the
   activity clauses witnessing \(u\triangleright x\);
6. the completion/hot incidences for \(d,w,z\);
7. seven additional retained states \(U,R,I,A,K,E,F\), and the omitted
   state \(O\); and
8. only the selected pair-nondomination clauses (4.1) together with
   \(\{u,x\}\).

The finite order-\(16\) ablation audit is explicitly
**OBSERVED_DISCOVERY_ONLY**.  Removing the independent-pair extension
clauses, all family-closure clauses, or the activity clauses separately
produces a SAT model.  Removing \(\alpha\le3\), all seven additional
retained-state unit clauses, the four hot-state units, any one such unit,
or the single omitted-\(O\) unit leaves that particular formula UNSAT.
These outcomes have no proof logs and are not promoted as finite
theorems.  Their only role is to identify that the order-\(16\)
contradiction was carried by the interaction of extension, activity,
and dynamic closure, not by one manually asserted hot state.

At order \(18\), the complete formula itself is SAT.  The SAT run is
only the provenance of the fixed graph; every mathematical statement
about the displayed graph is recomputed independently.

## 6. Consequence for the proof program

The proposed all-order anchor--auxiliary obstruction is refuted.
Neither

\[
 \text{``protect \(p,q\) against every auxiliary partner''}
\]

nor the stronger condition

\[
 \text{``protect every pair touching \(T=\{x,p,q\}\)''}
\]

forces \(\gamma=3\), even with the full accepted local QQ1 dynamics.
The next universal argument must use the non-domination of pairs wholly
outside \(T\), or another genuinely global consequence of
\(\gamma=3\).  Iterating witnesses only relative to the three original
anchors cannot close QQ1.

This result does not eliminate canonical QQ1 under equality, prove
complete \(k=3\), or resolve the gamma--theta conjecture.

## 7. Reproduction

From the campaign root:

```text
sh math/working/qq1_anchor_auxiliary_ladder/verify_strict.sh
```
