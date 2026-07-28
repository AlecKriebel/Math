# Four neutral vertices and two overlapping response ports at order 13

## Status and exact boundary

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor remains in the selected family.

The main result of this note is **certificate-backed finite**, pending its
campaign-ledger promotion after hostile review:

> **Four-neutral/two-port exclusion.** There is no graph \(G\) of order
> \(13\), eternal family \(\mathcal F\) of triples, and independent state
> \(S=\{h,i,j\}\in\mathcal F\), with \(\gamma(G)\geq3\), four distinct
> vertices \(q_1,\ldots,q_4\) outside \(S\) that are \(G\)-complete to
> \(S\), and two further distinct vertices \(x,y\) such that
> \[
>   \{h,j\}\subseteq L_S^{\mathcal F}(x),
>   \qquad
>   \{h,i\}\subseteq L_S^{\mathcal F}(y).
> \]

No hypothesis about \(\theta\), connectivity, no-full lists, negative list
memberships, anchor signatures of \(x,y\), an exceptional vertex, mate
edges, or the other four vertices is encoded.  There is no separate
\(\alpha\leq3\) block: the independent triple and an eternal
triple-family already force
\(\alpha(G)=\gamma^\infty(G)=3\).

This excludes the C-093 tight \(5+5\) normal form, and more.  In the
order-13 no-full counterexample branch, C-093 forces at least two distinct
two-list types and C-091 gives distinct physical representatives of them
outside the neutral set.  If \(|Q|\geq4\), choose four neutral vertices and
map the two types to the displayed overlapping pairs.  The certified
formula then applies.  Consequently this new finite result gives

\[
  \boxed{|A|\geq7,\qquad |Q|\leq3}
\]

for the surviving order-13 no-full branch.

This numerical conclusion is **not** the retracted static argument in
`order13_no_full_decomposition/NOTE.md`.  It depends essentially on the
two positive response pairs and full literal eternal-family closure.
Dropping the entire \(\gamma\geq3\) block, any one of the four positive
response memberships, or one whole neutral-vertex condition makes the
formula satisfiable.

The result does not exclude the remaining \((|A|,|Q|)=(7,3),(8,2),(9,1)\),
or \((10,0)\) cases, complete order 13 at parameter three, the universal
\(k=3\) case, or the gamma--theta conjecture.

## 1. CNF semantics

Variables encode \(H=\overline G\), a selected family of triples, and
common-\(H\)-neighbor selectors:

\[
\begin{array}{c|r}
\text{kind}&\text{count}\\ \hline
H\text{-edge variables}&\binom{13}{2}=78\\
\text{family-state variables}&\binom{13}{3}=286\\
\text{common-neighbor selectors}&
  \binom{13}{2}(13-2)=858\\ \hline
\text{total}&1222.
\end{array}
\]

The anchors are \(S=(0,1,2)=(h,i,j)\), the two ports are \(x=3,y=5\),
and vertices \(8,9,10,11\) are the four named neutral vertices.  Vertices
\(4,6,7,12\) are unrestricted.

### 1.1 Domination lower bound

For every pair \(\{u,v\}\), one selector \(w\notin\{u,v\}\) is true, and a
true selector forces

\[
 uw,vw\in E(H).
\]

Thus every pair has a common open \(H\)-neighbor and no pair dominates
\(G\), proving \(\gamma(G)\geq3\).  The block has

\[
 \binom{13}{2}\bigl(1+2(13-2)\bigr)=1794
\]

clauses.

### 1.2 Exact one-guard closure

For a triple \(D\), unoccupied target \(r\), and guard \(g\in D\), the
response conjunction is

\[
  gr\in E(G)
  \quad\text{and}\quad
  D-g+r\in\mathcal F.
\]

Because edge variables encode \(H\), its two literals are

\[
  \neg e^H_{gr},\qquad f_{D-g+r}.
\]

The implication from \(f_D\) to the disjunction of the three response
conjunctions is expanded distributively.  Choosing one of the two
conjuncts for each of three guards gives exactly eight clauses:

\[
 \neg f_D\ \lor\ \ell_1\ \lor\ \ell_2\ \lor\ \ell_3.
\]

This is an exact CNF equivalence, not a relaxation.  The all-move-edge
choice is precisely the domination clause for \(r\).  Hence closure also
forces every selected state to dominate and no duplicate domination block
is needed.  There are

\[
 \binom{13}{3}(13-3)2^3=22880
\]

closure clauses.

The three anchor \(H\)-edge units and \(f_S\) make \(S\) an independent
selected state.  Therefore the formula gives

\[
 \gamma(G)\leq3,\qquad
 \alpha(G)\geq3,\qquad
 \gamma^\infty(G)\leq3.
\]

Together with the common-neighbor block and the general
\(\alpha\leq\gamma^\infty\) inequality, every model would satisfy

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

### 1.3 Neutral vertices and response ports

The twelve units

\[
 e^H_{s q}=0
 \qquad(s\in S,\ q\in\{8,9,10,11\})
\]

make the four named vertices \(G\)-complete to \(S\).

Four positive family-state units encode

\[
 \{0,2\}\subseteq L(3),\qquad
 \{0,1\}\subseteq L(5).
\]

For an independent reference state, selected direct-swap membership also
forces the required move edge: attack the omitted anchor from the selected
successor.  The other two anchors cannot answer, so the new port guard must
move.  Thus the four units have exactly the claimed response-list meaning.
No negative membership is imposed.

The total clause count is

\[
 1794+22880+4+12+4=24694.
\]

The independent reconstructor confirms that all 24,694 clauses are unique
and none is tautological.

## 2. Coverage of the C-093 branch

Assume the tight C-093 normal form.  Its two omitted colors are \(i,j\);
write \(h\) for the remaining anchor.  By the accepted physical
representative theorem C-091, type \(i\) has a representative

\[
 x\in A,\qquad \{h,j\}=L(x),
\]

and type \(j\) has a distinct representative

\[
 y\in A,\qquad \{h,i\}=L(y).
\]

They are distinct from every neutral vertex.  Label them \(3,5\), label
any four of the five neutral vertices \(8,9,10,11\), and label all
remaining vertices arbitrarily.  This is a model of every CNF assumption.
There is no symmetry breaker and no omitted orbit.

The same relabeling argument applies to any order-13 no-full candidate with
at least four neutral vertices: two distinct response types exist by
C-093, and C-091 physicalizes them outside \(Q\).  This proves the
\(|Q|\leq3\) implication once the certificate is accepted.

## 3. Certificate and replay

The retained production artifacts are:

```text
micro_search.py
micro-instance.cnf
micro-proof.additions.drat
replay.py
replay-result.json
```

Their critical hashes are:

```text
micro_search.py
15c159737a7c3987aed7e6ab488e1744ee0b6252bbed555388f6832f1db56c79

micro-instance.cnf
3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0

micro-proof.additions.drat
c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee
```

The proof contains exactly 78,697 ASCII additions, no deletions, and ends
with the empty clause.  From the campaign directory, run:

```text
python3 -I -B -W error \
  math/working/order13_no_full_tight_five_five/replay.py \
  --result math/working/order13_no_full_tight_five_five/replay-result.json
```

The independent reconstruction is byte-identical to the retained CNF.
Pinned DRAT-trim then checks the retained proof with

```text
-I -f -W -U -t 60
```

and reports `s VERIFIED`, zero RAT lemmas, and exit zero.

The backward proof core has 10,833 input clauses and 46,840 retained proof
lemmas.  It uses every one of the 13 vertex labels, all 78 edge variables,
all 286 family variables, and 825 of 858 common-neighbor selectors.  No
short human attack chain was extracted.  The result is therefore
classified as certificate-backed finite, not as a human proof.

## 4. Sharp three-neutral control

Deleting one whole neutral-vertex condition gives the three-neutral
formula.  It is satisfiable.  The retained model has labeled graph6

```text
LDZZa^g|fkw[iH
```

and canonical graph6

```text
L][DKgF@zZjum{
```

The standalone verifier checks the complete model and obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3).
\]

Its greatest eternal triple-kernel has 139 states; the selected SAT family
is exactly those 139 states, all 1,390 unoccupied-attack obligations pass,
vertices \(8,9,10\) are neutral, and

\[
 L(3)=\{0,2\},\qquad L(5)=\{0,1\}.
\]

Replay with:

```text
python3 -I -B -W error \
  math/working/order13_no_full_tight_five_five/verify_q3_control.py \
  --result \
  math/working/order13_no_full_tight_five_five/q3-control-result.json
```

The model is colorable and is not a gamma--theta counterexample.  It proves
that four, rather than three, named neutral vertices are necessary for the
present order-13 finite obstruction.

## 5. Assumption audit

Exact solver ablations at order 13 gave:

\[
\begin{array}{c|cccccc}
\text{number of named neutral vertices}&0&1&2&3&4&5\\ \hline
\text{status}&\mathrm{SAT}&\mathrm{SAT}&\mathrm{SAT}&\mathrm{SAT}&
\mathrm{UNSAT}&\mathrm{UNSAT}.
\end{array}
\]

Further single-block ablations of the four-neutral formula gave:

- remove all common-neighbor clauses encoding \(\gamma\geq3\): SAT;
- remove any one of the four positive response units: SAT;
- remove all three anchor-adjacency units for any one named neutral
  vertex: SAT;
- add no \(\alpha\)-block: still UNSAT (the production formula);
- add no negative list units: still UNSAT (the production formula).

For four neutral vertices, the same generalized formula is UNSAT through
order 13 and SAT at order 14.  This order sweep is diagnostic; only the
retained order-13 UNSAT certificate and the independently verified
three-neutral control are promoted here.

