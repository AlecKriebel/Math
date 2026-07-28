# Dynamic-type sparsity strengthens to universal physicality

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor remains in the eternal family.

The requested sparsity statement strengthens as follows.

> **PROVED CANDIDATE, pending hostile review.**  Let
> \(\mathcal F\) be an eternal family of triples, let
> \(S=\{a,b,c\}\in\mathcal F\) be independent, assume
> \(\gamma(G)=3\), and assume every outside response list at \(S\) has
> exact size two.  Then every outside vertex is physically nonadjacent in
> \(G\) to its unique omitted anchor.  Equivalently, there are no dynamic
> exact-two-list ports of any omitted-color type.

Thus the initially proposed conclusion—dynamic ports cannot occur in all
three types—holds with “all three” replaced by “even one.”

This is a theorem about physical anchor incidences.  It does **not** prove
that the response 2-CNF is satisfiable, transport a complement edge
supporting a clause, prove the complete \(k=3\) case, or resolve the
gamma--theta conjecture.

The accepted dependencies are C-079 (the arbitrary odd physical fan
exclusion), C-082 (dynamic connector-edge caps), C-094 (same-sign literal
physicalization), and the sealing setup used in C-110.  The elementary
single-cap contradiction below strengthens the three-sealed-positive
lemma of C-110 in the exact-two-list branch.

No literature-priority claim is made.

## 1. Definitions and branch hypotheses

Put \(H=\overline G\).  For \(t\notin S\), write

\[
  L(t)=\{i\in S:S-i+t\in\mathcal F\}.
\tag{1.1}
\]

Membership \(i\in L(t)\) forces

\[
  it\in E(G),
\tag{1.2}
\]

because the retained direct-swap state must dominate the omitted anchor
\(i\).

Closure from \(S\) makes every outside list nonempty.  In the unit-free
no-full branch, singleton and three-element lists are absent, so

\[
   |L(t)|=2
   \qquad(t\notin S).
\tag{1.3}
\]

If

\[
   L(t)=S-\{i\},
\]

call \(t\) a **type-\(i\)** port.  It is:

- **physical** if \(it\in E(H)\);
- **dynamic** if \(it\in E(G)\).

For \(i\in S\), put

\[
   W_i=\{t\notin S:i\notin L(t)\},
   \qquad
   P_i^+=\{t\notin S:i\in L(t)\}.
\tag{1.4}
\]

## 2. One sealed positive cap is impossible

### Lemma 2.1 (single sealed-positive exclusion) — PROVED CANDIDATE

Assume \(\gamma(G)=3\) and (1.3).  There is no outside vertex \(z\) and
anchor \(i\in S\) satisfying

\[
   i\in L(z),
   \qquad
   N_H(z)\cap P_i^+=\varnothing.
\tag{2.1}
\]

#### Proof

Since \(L(z)\) has exact size two, write

\[
   L(z)=\{i,j\},
   \qquad
   S=\{i,j,k\}.
\tag{2.2}
\]

The pair \(\{j,z\}\) does not dominate \(G\), so
\(\gamma(G)=3\) supplies a vertex \(w\notin\{j,z\}\) with

\[
   jw,zw\in E(H).
\tag{2.3}
\]

Suppose first that \(w\notin S\).  The edge \(jw\in E(H)\), together with
(1.2), gives

\[
   j\notin L(w).
\]

The edge \(zw\in E(H)\) and the sealing condition in (2.1) give

\[
   i\notin L(w).
\]

Thus \(L(w)\subseteq\{k\}\), contradicting the exact size-two hypothesis.
Hence \(w\in S\).

The witness is not \(j\), because \(j\) is an endpoint of the pair.  It
is not \(i\), because \(i\in L(z)\) forces \(iz\in E(G)\).  Therefore

\[
   w=k,
   \qquad
   kz\in E(H).
\tag{2.4}
\]

Now apply \(\gamma(G)=3\) to the pair \(\{k,z\}\).  Let
\(w'\notin\{k,z\}\) be a common \(H\)-neighbor.

If \(w'\notin S\), then \(kw'\in E(H)\) gives
\(k\notin L(w')\), while \(zw'\in E(H)\) and (2.1) give
\(i\notin L(w')\).  Again \(L(w')\) has size at most one, a
contradiction.

If \(w'\in S\), then:

- \(w'\ne k\), since \(k\) is an endpoint;
- \(w'\ne i\), since \(iz\in E(G)\);
- \(w'\ne j\), since \(jz\in E(G)\) by \(j\in L(z)\).

No anchor remains.  This final contradiction proves the lemma.
\(\square\)

Every complement edge used in this proof is literal.  The only direction
used from response membership is (1.2); no missing response is converted
into a graph nonedge.

### Relation to C-110

C-110 proved that sealed positive caps for all three anchor colors cannot
coexist, including all collision patterns.  Lemma 2.1 shows that, under
the same global exact-two-list hypothesis, the gamma obligations at the
two pairs \(\{j,z\}\) and \(\{k,z\}\) already exclude one sealed cap.
The three-color collision analysis is therefore unnecessary for this
stronger corollary.

## 3. Dynamic ports create a forbidden sealed cap

### Theorem 3.1 (universal physicality of exact two-list ports)

Under the hypotheses in the status statement, every type-\(i\) port
\(t\) satisfies

\[
   it\in E(H).
\tag{3.1}
\]

#### Proof

Suppose instead that \(t\) is dynamic:

\[
   L(t)=S-\{i\},
   \qquad
   it\in E(G).
\tag{3.2}
\]

Apply accepted C-094 in its dynamic case.  It supplies distinct outside
vertices \(y,r\) such that

\[
   ty,yr,iy,ir\in E(H),
\tag{3.3}
\]

with \(t-y-r\) a length-two path in \(H[W_i]\) and \(r\) the same-sign
physical representative of \(t\).  Only the first edge \(ty\) is needed
below.  In particular,

\[
   t,y\in W_i,
   \qquad
   ty\in E(H),
\tag{3.4}
\]

and the endpoint \(t\) is adjacent to \(i\) in \(G\).

Apply accepted C-082 to the connector edge \(ty\).  Because one endpoint
is dynamic to \(i\), C-082 supplies an outside common complement neighbor
\(z\) satisfying

\[
   tz,yz\in E(H),
   \qquad
   i\in L(z).
\tag{3.5}
\]

We claim that \(z\) is sealed:

\[
   N_H(z)\cap P_i^+=\varnothing.
\tag{3.6}
\]

Indeed, if \(p\in P_i^+\) and \(pz\in E(H)\), then accepted C-079 applies
with

\[
  \text{positive tail }p,\quad
  \text{common port }z,\quad
  \text{odd path }t-y\subseteq H[W_i].
\]

The four required complement edges are

\[
  pz,\ zt,\ zy,\ ty.
\]

All four vertices are distinct: open-neighborhood incidences exclude
equal endpoints, and the positive/omitted-\(i\) lists separate \(p\) from
\(t,y\).  This is exactly the forbidden length-one C-079 fan, proving
(3.6).

Equations (3.5)--(3.6) contradict Lemma 2.1.  Therefore the dynamic
alternative (3.2) is impossible, proving (3.1). \(\square\)

The assumptions \(\alpha(G)=\gamma^\infty(G)=3\) are automatic from the
independent state \(S\) and the eternal triple-family:

\[
  3\leq\alpha(G)\leq\gamma^\infty(G)\leq3.
\]

They are recorded explicitly to match the equality branch, but the proof
uses them only through the accepted dependencies and the stated family
setup.

## 4. Exact structural consequence for the response formula

### Corollary 4.1 (anchor incidence equals response membership)

For every \(t\notin S\),

\[
   \boxed{L(t)=N_G(t)\cap S.}
\tag{4.1}
\]

#### Proof

The inclusion \(L(t)\subseteq N_G(t)\cap S\) is (1.2).  The exact
two-list hypothesis gives a unique omitted anchor \(i\).  Theorem 3.1
gives \(it\in E(H)\), while both anchors in \(L(t)\) are joined to \(t\)
in \(G\).  Hence equality holds. \(\square\)

Consequently:

- every response 2-CNF port is already a physical representative of its
  literal;
- C-094 may take the representative to be the port itself;
- the outside vertices split by their unique complement-neighbor anchor.

This does **not** make the response 2-CNF automatically satisfiable.
Cross clauses are still supported by complement edges among outside
ports, and C-095 warns that clause-edge transport is a separate issue.
No coloring or clique partition is produced here.

## 5. Small exact sharpness control

The six-vertex graph

```text
EFnG
```

has complement-edge set

```text
01 02 12 14 25 35
```

and exact parameters

\[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\tag{5.1}
\]

At the reference state \(S=\{0,1,2\}\), its 12-state eternal family has

\[
\begin{array}{c|c|c}
\text{vertex}&L(v)&\text{omitted-anchor incidence}\\ \hline
3&\{1,2\}&03\in E(G)\quad\text{(dynamic type 0)}\\
4&\{0,2\}&14\in E(H)\quad\text{(physical type 1)}\\
5&\{0,1\}&25\in E(H)\quad\text{(physical type 2)}.
\end{array}
\tag{5.2}
\]

The standalone verifier checks all 36 unoccupied-attack obligations, a
greatest eternal triple kernel of size 18, the response lists, and every
parameter in (5.1).  This control has the minimum possible order for a
reference triple plus one displayed port of each of the three types.

It proves that the hypothesis \(\gamma(G)=3\) in Theorem 3.1 is
essential.  It is not a gamma--theta counterexample because
\(\gamma(G)=2<3=\gamma^\infty(G)=\theta(G)\).

## 6. Bounded discovery observations

Before the proof was found, the direct family SAT encoding gave:

\[
\begin{array}{c|c|c}
\text{forced dynamic types}&\text{orders tested}&\text{observed status}\\ \hline
\{a\}&6\text{--}16&\mathrm{UNSAT}\\
\{a,b\}&6\text{--}18&\mathrm{UNSAT}.
\end{array}
\]

Every run imposed \(\gamma\geq3\), an independent retained reference
triple, exact two-lists at every outside vertex, and a nonempty displayed
port of each type.  These are **OBSERVED** discovery runs without a
certificate package or finite coverage claim.  Theorem 3.1 supersedes
them mathematically.

## 7. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/dynamic_type_sparsity/verify.py \
  --check math/working/dynamic_type_sparsity/control.json \
  --output /tmp/dynamic-type-sparsity-check.json
```

The verifier imports no search or campaign evaluator.  It reconstructs
the graph from the displayed complement edges, verifies the selected
eternal family and all attack obligations, computes the exact parameters,
recomputes the greatest triple kernel, and checks the unique dynamic type.

Theorem 3.1 and Corollary 4.1 are the mathematical candidates awaiting
hostile review.  The SAT scans are proof-discovery evidence only.
