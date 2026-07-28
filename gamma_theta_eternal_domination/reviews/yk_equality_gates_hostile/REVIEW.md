# Hostile review: the two \(Y_k\) equality gates

## Verdict

Date: 2026-07-28 PDT

**PASS AFTER REQUIRED CORRECTION.**

The original frozen candidate contained one unsupported conclusion:
Lemma 5.1 asserted that a dirty private-buffer carrier always inherits the
entire exact family-response \(Y_3\) pattern.  That proof repeated the
C-121 restoration argument at

\[
U=Z\cup C
\]

even though \(U\) may be nonindependent through edges between \(C\) and
\(Z\).  Restoration relative to the original independent state \(S\)
constrains the original lists \(L_S^{\mathcal F}\); it does not imply
membership of every direct state \(U-\rho(v)+x_i\).

The candidate was revised during this audit.  The unsupported conclusion
is retracted, a correct conditional version is proved, and a
clean-room symbolic kernel records a sharp falsifier for the invalid
inference.  I find no remaining correction required in the revised note
at SHA-256

```text
9c874711a469eca96d790b9680c975f143bede945ee6624ebc9fc860b9f3a785
```

The exact accepted scope is:

| Statement | Verdict | Scope |
|---|---|---|
| Mandatory singleton contamination | **PROVED** | Every \(z_d\) has a graph neighbor in \(S-\{d\}\), and every such wrong-role edge forces a closed-private buffer. |
| Clean \(Y_4\) exclusion | **PROVED** | A base-clean exact static \(Y_4\) cannot occur.  This does not exclude a dirty \(Y_4\). |
| Clean contamination cycle and external buffers | **PROVED** | For \(k\ge5\), a simple directed cycle supplies at least two distinct buffers outside the clean equality-three projection. |
| Endpoint survive-or-count lemma | **PROVED** | One original endpoint defect is new whether it survives in \(J\) or is repaired outside \(J\). |
| Clean-pattern floor \(n\ge2k+9\) | **PROVED, CONDITIONAL PATTERN THEOREM** | Requires equality, \(k\ge5\), and a base-clean exact static \(Y_k\) realization.  It is not a global counterexample-order frontier. |
| Two-defect floor \(n\ge2k+10\) | **PROVED, CONDITIONAL** | Requires two distinct vertices in the union of the two original endpoint defect sets. |
| Dirty carrier is retained and has nonempty \(Y_3\) response caps | **PROVED** | The endpoint caps are exact and every intended cap role is a graph edge. |
| Exact shifted \(Y_3\) at the dirty carrier | **PROVED ONLY IF \(E_G(C,Z)=\varnothing\)** | Then \(U\) is independent and the \(Z\)-fixed triple-family admits the C-121 family-cap argument. |
| Exact shifted \(Y_3\) from caps/restoration/closure when \(U\) is nonindependent | **REFUTED INFERENCE** | The independent symbolic control has a 34-state eternal kernel and omits the \(c\)-role at \(x_1\).  It is a proof-method falsifier, not a full original \(Y_k\) realization. |
| Arbitrary dirty-branch exclusion, \(\mathsf{GL}(k)\), complete \(k=3\), or the universal conjecture | **OPEN** | None follows here. |

## Frozen inputs

| Artifact | SHA-256 |
|---|---|
| revised candidate note | `9c874711a469eca96d790b9680c975f143bede945ee6624ebc9fc860b9f3a785` |
| revised candidate research log | `1af30ae0237f40ca8988e297632d1b509d460ae2ad65a0bde1e39023fbac17a3` |
| revised candidate manifest | `3f44e5aae91b014d884d88e54ad98110ecda6beb3f6a8a42a4fc85262b5649ea` |
| C-125 source | `98a56786a8db1f78c4f6328871b1926795928997389f441e4637e6e3d801d6e0` |
| C-121 source | `ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9` |
| C-072 source | `0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb` |
| C-070 source | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| independent checker | `822f8c7f81650ecc265bff71e2fb881cbd24f27eccb67b6025d782cd1bac99eb` |
| captured checker output | `a328c98d91337e4d1cfd061e5f19abc283d1ad03a379fe01c8b68ddc8fc3609f` |

The candidate manifest is valid JSON, its two artifact hashes match, and
its base commit

```text
24134aaadbfabd7c07bc144b6571c9907313db97
```

exists in the repository.

## 1. Mandatory contamination and the \(Y_4\) gate

Fix \(d\in D\).  For every path vertex \(x_i\), the positive static role

\[
d\in L_S^{\rm stat}(x_i)
\]

means that \(S-d+x_i\) dominates \(G\).  The vertex \(z_d\) is not
occupied in this state and is a graph nonneighbor of \(x_i\), because
\(H[Z\cup X]\) is a join.  Hence some member of \(S-\{d\}\) must be a
graph neighbor of \(z_d\).  This proves

\[
A(d)=N_G(z_d)\cap(S-\{d\})\ne\varnothing.
\]

For \(u\in A(d)\), the edge \(uz_d\) exists but
\(u\notin L_S^{\rm stat}(z_d)=\{d\}\).  Therefore \(S-u+z_d\) fails
domination.  Any missed vertex \(p\) is nonadjacent to \(z_d\) and to
\(S-\{u\}\).  Since \(S\) dominates and \(p\ne u\) (the edge \(uz_d\)
would otherwise dominate it after the swap), \(p\) is adjacent to \(u\).
Thus

\[
p\in P_S(u)\cap N_H(z_d).
\]

Under base-cleanliness, no member of \(B\) can lie in \(A(d)\), so

\[
A(d)\subseteq D-\{d\}.
\]

If \(k=4\), then \(|D|=1\), and the right side is empty.  The clean
\(Y_4\) branch is therefore impossible.  For \(k\ge5\), the directed
graph on \(D\) with \(d\to e\) when \(z_de\in E(G)\) is loopless and has
positive outdegree at every vertex.  Following arcs gives a directed
cycle of length at least two.  The checker exhausts all such loopless
digraphs through four vertices as a corroborative finite test; the human
argument is length-independent.

## 2. Cycle buffers are distinct and outside \(J\)

For a simple directed cycle

\[
d_0\to d_1\to\cdots\to d_{\ell-1}\to d_0,
\]

choose

\[
p_j\in P_S(d_{j+1})\cap N_H(z_{d_j}).
\]

The heads \(d_{j+1}\) are pairwise distinct, and closed-private blocks
for different anchors are disjoint.  Hence the \(p_j\) are pairwise
distinct.

The externality ledger is complete:

- \(p_j\notin S\): the head itself is adjacent to \(z_{d_j}\), while all
  other members of \(S\) have the wrong closed-private intersection;
- \(p_j\notin X\): every \(x_i\) is graph-adjacent to every member of
  \(D\), and the clean branch has \(|D|\ge2\);
- \(p_j\notin Z\): if \(p_j=z_f\), its graph edge to \(f\) forces
  \(f=d_{j+1}\), but mandatory contamination gives \(z_f\) a second
  neighbor in \(D-\{f\}\), contradicting privacy; and
- \(p_j\notin B\) is already part of \(p_j\notin S\).

The retained state \(T=B\cup Z\) dominates \(p_j\).  Because \(p_j\) is
private to an anchor in \(D\), it is nonadjacent to every member of
\(B\); because it lies outside \(T\), closed domination cannot come from
occupancy.  Some member of \(Z\) must therefore be graph-adjacent to
\(p_j\).  By the definition

\[
J=G[\{v\notin Z:E_G(v,Z)=\varnothing\}],
\]

this proves \(p_j\notin J\).  A simple cycle supplies at least two such
vertices, all outside \(J\cup D\cup Z\).

## 3. The endpoint survive-or-count dichotomy

C-125 gives an equality-three projection \(J\) with an exact
**family-response** \(Y_3\) at \(B=\{a,b,c\}\).  Accepted C-070 therefore
gives

\[
cx_0,cx_3\in E(G).
\]

The original exact **static** lists omit \(c\) at both endpoints, so
\(S-c+x_0\) and \(S-c+x_3\) fail domination.  Any endpoint defect \(q\)
is external to the failed state, is nonadjacent to
\(D\cup\{a,b,x_i\}\), and is adjacent to \(c\).  Thus

\[
q\in P_S(c).
\]

If \(q\notin J\), then \(q\) is adjacent to \(Z\).  It cannot itself lie
in \(Z\), since every \(z_d\) is adjacent to the occupied \(d\), and it
cannot lie in \(D\), since \(D\) is occupied.  It is distinct from every
cycle buffer because those buffers lie in private blocks belonging to
members of \(D\), whereas \(q\in P_S(c)\).  This is a genuinely new
outside vertex.

If \(q\in J\), it is a genuine projected endpoint defect.  It is
distinct from each of the five selected C-072 witness systems:

- \(w\) has positive \(a\)- and \(b\)-roles;
- \(p_L\) has a positive \(b\)-role;
- \(p_R\) has a positive \(a\)-role; and
- \(y\) has graph edges to both \(a\) and \(b\).

All four exclusions are valid graph-incidence exclusions, while \(q\)
is nonadjacent to \(a,b\).

For the fifth witness

\[
z\in N_H(x_0)\cap N_H(x_3),
\]

equality \(q=z\) would make \(q\) a common endpoint defect in \(J\).
The C-121 local double-defect kernel excludes this.

### Why the C-121 local kernel applies here

The full theorem statement C-121 starts from exact projected static
lists, but its local Lemma 4.1 has strictly weaker inputs.  It needs:

1. equality \(\gamma(J)=\alpha(J)=\gamma^\infty(J)=3\);
2. the exact **family-response** \(Y_3\);
3. endpoint saturation \(cx_0,cx_3\in E(G)\); and
4. one vertex missing \(a,b,x_0,x_3\).

All four are present.  In particular, a common defect \(q\) makes
\(\{a,b,q\}\) a maximum independent triple, so independent-state forcing
gives the direct \(c\)-role at \(q\), and ridge covariance gives the
needed edges from \(q\) to \(x_1,x_2\).  The 16-completion local kernel
then applies.  No equality of the projected static lists is used at this
step.

Thus a surviving \(q\) is a thirteenth vertex beyond the selected
twelve-vertex C-072 system inside \(J\); a repaired \(q\) is a new vertex
outside \(J\).  This proves the survive-or-count lemma without assuming
static-list functoriality.

## 4. Order counts and collision audit

Choose the twelve mutually distinct vertices supplied in \(J\) by C-072.
The following sets are disjoint from those twelve and from one another:

1. \(D\), of size \(k-3\);
2. \(Z\), of size \(k-3\);
3. at least two cycle buffers; and
4. one endpoint defect, counted inside or outside \(J\) according to
   Section 3.

Therefore

\[
|V(G)|\ge12+2(k-3)+2+1=2k+9.
\]

This requires \(k\ge5\), equality, and a base-clean exact static \(Y_k\).
It is not an order floor for arbitrary counterexamples.

If the union of the two endpoint defect sets has at least two vertices,
the same collision audit applies to each.  Two distinct defects give

\[
|V(G)|\ge12+2(k-3)+2+2=2k+10.
\]

If the endpoint contribution is only one vertex, both nonempty defect
sets equal the same singleton.  A common defect inside \(J\) is excluded
by the local kernel, so the only residual form is one common repaired
defect outside \(J\), adjacent to \(Z\).  No existence claim is made for
that residual form.

## 5. Required correction to the dirty carrier

Let \(u\in B\) be adjacent to \(z_d\), choose

\[
p\in P_S(u)\cap N_H(z_d),
\]

and set \(C=(B-\{u\})\cup\{p\}\).  Attacking \(p\) from \(S\) uniquely
moves \(u\).  Attacking \(p\) from \(T=B\cup Z\) also forces \(u\):
if \(z_e\) moved, the outside original-list union

\[
(D-\{e\})\cup\{u\}
\]

would omit the missing color \(e\).  Thus \(U=Z\cup C\) is retained.

For an attack at \(x_i\), no guard in \(Z\) can move.  Restoration
relative to \(S\) gives the sound cap

\[
\varnothing\ne R_i\subseteq\rho(A_i).
\]

Every intended cap role is also a graph edge.  Original base roles are
positive static incidences.  If the intended role is \(p=\rho(u)\), the
dominating state \(S-u+x_i\) must dominate \(p\); privacy excludes all
members of \(S-\{u\}\), forcing \(px_i\in E(G)\).  The singleton caps
therefore give exact endpoint response lists.

The original candidate then asserted equality in every cap.  This was
not justified.  When \(U\) is nonindependent, the arbitrary-state
restoration theorem cannot be re-based at \(U\).  Restoration relative
to \(S\) may say that the original color \(c\) occurs in
\(L_S^{\mathcal F}(x_1)\), but this does not place
\(U-\rho(c)+x_1\) in the family.

The corrected conditional is sound: if \(E_G(C,Z)=\varnothing\), then
\(U\) is independent.  Freezing \(Z\) gives an eternal triple-family
containing \(C\), and the nonempty direct caps satisfy restoration
relative to \(C\).  The family-cap attack underlying C-121 then forces
all four exact lists.

### Independent symbolic falsifier for the invalid inference

The checker reconstructs, rather than imports, the nine-vertex graph on

\[
Z=\{z_0,z_1\},\quad C=\{p,b,c\},\quad
X=\{x_0,x_1,x_2,x_3\}
\]

specified in revised Section 5.1.  It verifies:

- \(Z\) and \(C\) are separately independent;
- \(Z\) is anticomplete to \(X\);
- \(X\) is an induced complement \(P_4\);
- \(U=Z\cup C\) is nonindependent only through the displayed
  \(z_1p\) edge;
- every intended cap role is a graph edge;
- all retained states dominate the displayed graph and satisfy the
  assigned original-palette restoration inclusion;
- after forbidding \(U-c+x_1\), the greatest one-guard kernel has
  34 states and all \(34(9-5)=136\) unoccupied attacks have a one-edge,
  one-guard successor; and
- the direct lists at \(U\) are
  \[
  \{p\},\quad\{p\},\quad\{b,c\},\quad\{b\},
  \]
  so the intended \(c\)-role at \(x_1\) is absent.

This refutes the exact logical inference used in the original proof.
Because the assigned palette lists are symbolic and are not claimed to
arise from one original \(S\) in the same nine-vertex graph, it does not
refute a stronger theorem using the complete original \(Y_k\) setup or
the equality hypothesis.  Those possible strengthenings remain open.

## 6. Reproduction and publication boundary

Run from the campaign root:

```text
python3 -I -B -W error \
  reviews/yk_equality_gates_hostile/independent_check.py
```

The captured output is `independent_check.stdout`.  The checker also
pins all revised candidate and dependency hashes, validates the candidate
manifest, exhausts the elementary positive-outdegree digraph assertion
through four vertices, and checks both counting identities for
\(5\le k\le50\).

The accepted result is a conditional exact-pattern theorem.  It does not
show that an arbitrary counterexample contains \(Y_k\), does not force
base-cleanliness, and does not eliminate the repaired common endpoint
defect.  The global finite frontier, the complete \(k=3\) case,
\(\mathsf{GL}(k)\), and the universal gamma--theta conjecture all remain

\[
\boxed{\text{OPEN}.}
\]
