# Hostile review: QQ1 bow-tie global coupling

## Verdict

**EXACT DEFECT IN THE FINITE-AUDIT SCOPE; MATHEMATICAL THEOREMS PASS.**

Theorem 1.1 and Corollaries 2.1 and 3.1 are correct on the frozen
candidate bytes at commit `5c8cff86`.  I found no quantifier gap,
collision error, one-guard model error, family-omission/nonedge
confusion, or illicit three-factor product.

The package nevertheless does not receive an unconditional pass because
its verifier says it audits the “H-by-Z cell normal form,” while the
nonedge branch only counts cells.  It neither requires the asymmetric
activity hypothesis of C-177 nor checks any polarized-bow-tie
conclusion.  This defect is exact and limited to the claimed scope of the
finite audit.  It does not invalidate any proof in the note.

Review date: 2026-07-28 PDT.

Frozen candidate:

```text
commit 5c8cff86fbd207645eb7ff0bf667330ca73f019e
NOTE.md SHA-256 65f19d2bcdb194a4f715cd40e23e5d448d5ee1b0468c33f9dcc12ab104e3f8c1
```

## 1. Theorem 1.1: family quantifier and the C-174 obstruction

The theorem fixes an arbitrary eternal family \(\mathcal F\) of
dominating triples.  Accepted C-174 has the same quantifier: if any
state in that family co-occupies \(a,b\), then every
\(\{a,b,z\}\), \(z\in W_{ab}\), belongs to that family and \(W_{ab}\)
is a clique.

For distinct \(d,d'\in C\), the clique hypothesis gives
\(dd'\in E(G)\).  Since \(C\subseteq W_{xr}\), both \(x\) and \(r\)
miss both \(d,d'\), so

\[
 x,r\in W_{dd'}.
\]

The hypothesis \(xr\notin E(G)\) makes \(W_{dd'}\) nonclique.  Therefore
C-174 proves that no state of \(\mathcal F\) contains both \(d,d'\).
This is a family-membership obstruction, not an inference that a move
edge is absent.

The argument is valid for every pair in \(C\), including when the third
guard in a hypothetical retained state is \(x\), \(r\), or neither.
The conclusion depends only on co-occupancy and the two fixed blockers.

## 2. Completion transport: all collisions and responses

Fix \(w\in H_d\) and \(d'\in C-\{d\}\).  All vertices in
\(\{u,d,w,d'\}\) that must be distinct are indeed distinct:

- \(w\notin\{u,d\}\) by \(w\in W_{ud}\);
- \(u\notin C\), since \(ux\) is an edge and every member of \(C\)
  misses \(x\);
- \(w\ne d'\), since otherwise the clique edge \(dd'\) would contradict
  \(w\in W_{ud}\).

Thus \(d'\) is an unoccupied attack from the literal triple
\(\{u,d,w\}\).  The guard at \(d\) is graph-eligible because
\(dd'\in E(G)\), and its endpoint is \(\{u,d',w\}\).

There are at most two competing endpoints:

\[
\begin{array}{c|c}
u\to d'&\{d,w,d'\},\\
w\to d'&\{u,d,d'\}.
\end{array}
\]

Whether those moves are graph-eligible is immaterial.  Both endpoints
contain \(d,d'\), so the C-174 obstruction excludes both from
\(\mathcal F\).  Eternal closure therefore forces the \(d\to d'\)
endpoint and makes it the unique **retained** response.  The proof never
declares \(ud'\) or \(wd'\) absent.

Transporting each seed \(w\in H_d\) to every \(d'\in C\), and keeping
the seed case \(d'=d\), proves the full \(C\times H\) family

\[
 \{u,d,w\}\in\mathcal F\qquad(d\in C,\ w\in H).
\]

This product is literal because \(H\cap C=\varnothing\): if
\(w\in H_d\) equaled a different completion, its clique edge to \(d\)
would contradict \(w\in W_{ud}\).

For distinct \(w,y\in H\), choose \(d\) with \(y\in H_d\).  The
transported state \(\{u,d,w\}\) is retained and must dominate the
unoccupied vertex \(y\).  The vertex \(y\) misses \(u,d\), so \(wy\)
is forced.  This proves that the entire union \(H\), not merely each
fiber \(H_d\), is a clique.

Verdict on Theorem 1.1: **PASS**.

## 3. Canonical \(C,H,Z\) skeleton

In canonical QQ1, the accepted dependencies supply exactly the inputs
used by the corollary:

- C-158 makes \(C=C_{xr}\) a nonempty clique;
- C-166 retains \(\{u,x,d\}\) and every seed
  \(\{u,d,w\}\), \(w\in W_{ud}\);
- C-167 retains \(\{u,w,z\}\) for each seed hot vertex and every
  \(z\in Z=W_{ux}\);
- C-143 makes \(\{u,r,d\}\) dominating.

The global transport theorem extends the C-167 bridges from each
original fiber to every \(w\in H\), yielding the full \(H\times Z\)
product.  This is valid because each \(w\) has at least one original
fiber to which C-167 applies.

The union \(C\cup Z\) is a clique.  The set \(Z\) is the C-174 fan of
the supported pair \(ux\), hence a clique.  For
\(d\in C,z\in Z-\{d\}\), the retained dominating state
\(\{u,x,d\}\) must cover \(z\); since \(z\) misses \(u,x\), the edge
\(dz\) is forced.  The exclusion of \(z=d\) is exactly the harmless
overlap case, not an omitted adjacency.

The remaining incidence claims also have the advertised scope:

- every hot vertex misses \(u\) by its defining fiber;
- \(\{u,x,d\}\) forces \(x\) complete to \(H_d\);
- the C-143 dominating state \(\{u,r,d\}\) forces \(r\) complete to
  \(H_d\);
- \(x\) misses \(C\cup Z\) by definition;
- for \(d\in C\), membership in \(Z\) is equivalent to \(ud\) being
  absent;
- \(H\cap C=\varnothing\) by the collision argument above, and
  \(H\cap Z=\varnothing\) because \(x\) is complete to \(H\) and misses
  \(Z\).

The two retained products are

\[
 \{u,d,w\}\quad(C\times H),\qquad
 \{u,w,z\}\quad(H\times Z).
\]

They share the fixed guard \(u\) and the coordinate \(w\).  Nothing in
the proof asserts \(\{d,w,z\}\in\mathcal K\), let alone a
\(C\times H\times Z\) family.  The note's “two coupled products”
language is accurate.

Verdict on Corollary 2.1, disjointness, and product scope: **PASS**.

## 4. The \(H\times Z\) matrix split

Fix \(w\in H,z\in Z\).  Their disjointness makes
\(\{u,w,z\}\) a literal retained triple, and their graph adjacency has
exactly two cases.

If \(wz\notin E(G)\), then \(uw\notin E(G)\) as well, so
\(w\in W_{uz}=P_z\).  Canonical QQ1 already has
\(u\triangleright_{\mathcal K}x\) and
\(x\not\triangleright_{\mathcal K}u\); therefore accepted C-177 applies
to this very cell and supplies the entire polarized bow tie, including
\(x\leftrightarrow_{\mathcal K}w\).

If \(wz\in E(G)\), the retained bridge co-occupies and supports that
edge.  Accepted C-174 therefore retains every
\(\{w,z,e\}\), \(e\in W_{wz}\), and makes \(W_{wz}\) a clique.  Since
\(u\) misses both \(w,z\), it belongs to this fan.  No activity premise
is needed in the edge branch.

The split is per cell.  A zero anywhere in a fixed row forces
\(x\leftrightarrow w\), while an all-one row consists of supported fan
edges.  It does not couple different rows into a three-coordinate
family, prohibit mixed rows, or reverse the original activity.

Verdict on Corollary 3.1: **PASS**.

## 5. Exact finite-audit defect

The candidate verifier's bridge block begins when it has a nonempty
\(Z\), the \(\{u,x,d\}\) states, and the \(H\times Z\) bridge states.
It does **not** test

\[
 u\triangleright_{\mathcal K}x,\qquad
 x\not\triangleright_{\mathcal K}u.
\]

For an edge cell it correctly checks the supported C-174 fan.  For a
nonedge cell its entire branch is:

```python
else:
    counts["HZ_nonedges"] += 1
```

Nevertheless the emitted JSON says:

```text
The audit verifies the global C-by-H transport and H-by-Z cell normal form
```

That statement is false for the nonedge half of the normal form.  The
12,480 reported census cells are all nonedges, so none of those counts
checks \(w\in P_z\), either activity direction, the mixed retained
states, the omitted fan, or any other C-177 conclusion.

The fixed `FCQe_` control makes the issue concrete.  It has four
\(H\times Z\) cells, one edge and three nonedges, but the exact greatest
family has neither
\(u\triangleright x\) nor \(x\triangleright u\) for the displayed
\((u,x)=(5,0)\).  Its edge cell is a valid C-174 control; its three
nonedge cells are not polarized C-177 controls.

The repair is small and does not alter the theorem:

1. narrow the census description to “bridge cells, with full C-174
   checking on edge cells”; or
2. require the two activity statuses before counting canonical matrix
   applications and audit every C-177 conclusion in the nonedge branch.

Verdict on the candidate's finite-audit scope statement:
**EXACT DEFECT**.

## 6. Independent computation

`independent_verify.py` uses immutable neighbor sets and frozenset guard
states, with a separately written greatest-fixed-point routine.  It
independently reconstructs:

- all 33,864 labeled graphs of orders three through six;
- 2,162 equality graphs;
- 17,640 transport instances;
- 2,520 instances with \(|C|\ge2\);
- 2,520 instances with \(|H|\ge2\);
- 22,680 retained \(C\times H\) incidences;
- 5,040 unique retained completion-transport attacks.

Every count agrees with the candidate for the part the candidate really
checks.

The verifier also reconstructs `FCQe_`, its exact parameter vector
\((3,3,3,3,3)\), 12-state greatest family, fibers

\[
 H_1=\{3\},\qquad H_4=\{3,6\},
\]

and transported nonseed state \(\{5,1,6\}\).

Finally it independently checks one complete polarized nonedge cell in
the equality control `D]?`, including both bow-tie sides, their complete
join, all mixed retained/omitted states, reciprocal activities, and the
entire supported and omitted fans.  This confirms that the imported
C-177 mechanism behaves as used; it does not retroactively turn the
candidate's 12,480 bare nonedge counts into C-177 checks.

## 7. Final scope

No mathematical proof step:

- attacks an occupied vertex;
- moves more than one guard;
- uses a complement edge as a guard move;
- infers graph nonadjacency from family omission;
- overlooks \(C\cap Z\);
- permits \(H\) to collide with \(C\) or \(Z\);
- asserts a three-factor retained product;
- forces \(x\triangleright u\);
- eliminates QQ1 or resolves parameter three.

The theorem package may be promoted after correcting the finite-audit
scope statement or strengthening that audit.  The theorem text itself
needs no mathematical repair.

Hostile-review completion: **100%**.
