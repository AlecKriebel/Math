# An adjacent-pair repair dichotomy at parameter three

## Status and scope

Date: 2026-07-28 (PDT)

Let \(G\) satisfy

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and let \(\mathcal F\) be any one-guard eternal family of dominating
triples.  For a \(G\)-edge \(ab\), put

\[
 W_{ab}=\{w\notin\{a,b\}:aw,bw\notin E(G)\}.
\tag{0.2}
\]

The condition \(\gamma(G)=3\) makes \(W_{ab}\) nonempty.  This note
proves an exact dichotomy for the way an eternal family can repair the
non-dominating pair \(\{a,b\}\).

> **Theorem (adjacent-pair repair dichotomy) — PROVED CANDIDATE.**
> Exactly one of the following two family-state alternatives holds.
>
> 1. **Retained central fan.**  For every \(w\in W_{ab}\),
>    \[
>      \{a,b,w\}\in\mathcal F.
>    \]
>    Moreover \(W_{ab}\) is a clique in \(G\), and attacks within this
>    clique uniquely exchange the witness guard:
>    \[
>      \{a,b,w\}\xrightarrow{\,w\to z\,}\{a,b,z\}
>      \qquad(w,z\in W_{ab},\ w\ne z).
>    \]
> 2. **Omitted central fan.**  For every \(w\in W_{ab}\),
>    \[
>      \{a,b,w\}\notin\mathcal F.
>    \]
>    Then the physical edge \(ab\) is family-active in both directions:
>    \[
>      a\mathrel{\triangleright_{\mathcal F}}b
>      \quad\text{and}\quad
>      b\mathrel{\triangleright_{\mathcal F}}a.
>    \]

The two alternatives refer to membership of the central fan and are
therefore mutually exclusive.  Activity need not distinguish them:
an edge in the retained-fan branch may also be reciprocal.

Equivalently, every nonreciprocal edge has a nonempty retained central
fan whose witness set is a \(G\)-clique.  This is the size-independent
piece missing from the first auxiliary escape in the order-18 C-169
boundary control.  It does **not** eliminate canonical QQ1, prove
greatest-family reciprocity, prove the complete \(k=3\) case, or resolve
the gamma--theta conjecture.

## 1. Definitions used in the proof

For distinct adjacent vertices \(a,b\), write

\[
 a\mathrel{\triangleright_{\mathcal F}}b
\tag{1.1}
\]

when some independent triple \(S\in\mathcal F\) containing \(a\) and
avoiding \(b\) can answer the attack at \(b\) by moving the guard at
\(a\), with the successor retained in \(\mathcal F\).

Every independent triple belongs to \(\mathcal F\).  This is the
standard maximum-independent-state forcing argument: start from any
family state and attack the unoccupied vertices of the independent
triple one at a time.  A guard already installed on one of those
vertices cannot move to another, so the process finishes at the
independent triple.

No inference below turns an omitted family response into a graph
nonedge.  Whenever a possible response is discarded, its successor is
the explicitly assumed omitted central state.

## 2. One retained center saturates the whole fan

### Lemma 2.1 (central-fan saturation)

If

\[
 R_w=\{a,b,w\}\in\mathcal F
\tag{2.1}
\]

for one \(w\in W_{ab}\), then \(W_{ab}\) is a \(G\)-clique and

\[
 R_z=\{a,b,z\}\in\mathcal F
\qquad(z\in W_{ab}).
\tag{2.2}
\]

For distinct \(w,z\in W_{ab}\), the attack at \(z\) from \(R_w\) has
the unique response \(w\to z\).

#### Proof

Fix \(z\in W_{ab}-\{w\}\).  The retained state \(R_w\) must dominate
the unoccupied vertex \(z\).  Both \(a\) and \(b\) miss \(z\) by the
definition of \(W_{ab}\).  Hence

\[
 wz\in E(G).
\tag{2.3}
\]

At the attack on \(z\), the guards at \(a,b\) are graph-ineligible and
the guard at \(w\) is eligible by (2.3).  Eternal closure therefore
uniquely retains

\[
 R_w-w+z=R_z.
\tag{2.4}
\]

Since \(z\) was arbitrary, all central states are retained and every
two distinct members of \(W_{ab}\) are adjacent. \(\square\)

An immediate consequence is that central-fan membership cannot be
mixed: either every \(R_w\) is retained or none is.

## 3. Omitting the fan forces reciprocity

### Lemma 3.1 (omitted center forces the forward orientation)

Fix \(w\in W_{ab}\).  If

\[
 R_w=\{a,b,w\}\notin\mathcal F,
\tag{3.1}
\]

then

\[
 a\mathrel{\triangleright_{\mathcal F}}b.
\tag{3.2}
\]

#### Proof

The pair \(\{a,w\}\) does not dominate because
\(\gamma(G)=3\).  Choose a vertex \(s\) missed by that pair.  Then

\[
 S=\{a,w,s\}
\tag{3.3}
\]

is an independent triple, hence \(S\in\mathcal F\).

Attack the unoccupied vertex \(b\) from \(S\).  The guard at \(a\) is
eligible because \(ab\in E(G)\), while the guard at \(w\) is
ineligible because \(w\in W_{ab}\).  If the guard at \(s\) is
eligible, its successor is exactly

\[
 S-s+b=\{a,b,w\}=R_w,
\tag{3.4}
\]

which is omitted by hypothesis.  If \(s\) is ineligible, that branch
is simply absent.  Eternal closure therefore forces the remaining
response

\[
 a\longrightarrow b,\qquad
 S-a+b=\{b,w,s\}\in\mathcal F.
\tag{3.5}
\]

The source \(S\) is independent, so (3.5) is precisely
\(a\triangleright_{\mathcal F}b\). \(\square\)

Interchanging \(a\) and \(b\) gives the reverse orientation.  Hence if
one central state is omitted and no central state is retained, the edge
is reciprocal.  Lemma 2.1 rules out a mixture of retained and omitted
central states, proving the theorem.

## 4. Consequence for the C-169 auxiliary escape

The exact order-18 C-169 control has a dominating pair \(\{u,14\}\).
That graph has \(\gamma=2\), so it lies outside the theorem.  In any
hypothetical equality realization in which an analogous auxiliary edge
\(ua\) is protected by full \(\gamma=3\), its common-nonneighbor set
\(W_{ua}\) cannot remain an unstructured collection of newly introduced
vertices.  The theorem forces one of two outcomes:

\[
\boxed{
 u\leftrightarrow a
 \quad\text{or}\quad
 W_{ua}\text{ is a retained central-token clique.}}
\tag{4.1}
\]

This conclusion is independent of the size of \(W_{ua}\), permits
witness reuse, and makes no freshness assumption.  It therefore
survives the exact two-cycles that refuted the fixed-anchor descent.

The conclusion is still not a contradiction.  Both branches occur in
small equality graphs, and the retained-fan branch can occur with or
without reciprocal activity.  A future QQ1 argument must couple (4.1)
to the already saturated hot and cross-witness layers.

## 5. Exact controls and finite audit

The standalone checker in this directory:

1. exhausts every labeled graph through order six, constructs its
   literal greatest eternal triple-family, and checks every applicable
   edge;
2. through order five, additionally exhausts every nonempty subfamily
   of dominating triples and checks every subfamily that is itself
   eternal; and
3. verifies sharp fixed controls.

The connected six-vertex graph

```text
EpQ?
```

with edge set

\[
 \{01,02,05,14,23\}
\tag{5.1}
\]

has exact

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{5.2}
\]

In its greatest family, edge \(01\) realizes the retained-fan,
nonreciprocal branch, while edge \(05\) realizes the omitted-fan,
reciprocal branch.  Thus neither branch can be deleted from the theorem.

The five-vertex graph

```text
D]?
```

is \(K_{2,2}\) plus an isolated vertex and has the same exact parameter
vector.  Its greatest family realizes a retained central fan on
reciprocal edges, proving that retained-fan membership does not imply
nonreciprocity.

Run from the campaign root:

```text
sh math/working/adjacent_pair_repair_dichotomy/verify_strict.sh
```
