# Exact CEGAR/SAT design for the \((n,k)=(12,3)\) slice

## Status

Design checkpoint, 2026-07-25.  No solver result is claimed here.  The
three-branch coverage statement depends on the hostile review of
`k3_antihole_elimination.md`; until that review is accepted, the earlier
four-branch split in `k3_structural_day1.md` remains the certified fallback.

The unknown graph in this note is \(H=\overline G\) on the fixed vertex set
\(\{0,\ldots,11\}\).  A Boolean variable \(e_{uv}\), \(u<v\), says that
\(uv\in E(H)\).  For every triple \(T\), a Boolean \(f_T\) says that \(T\)
belongs to a proposed eternal three-guard family in \(G\).

## 1. Static exact target

The base CNF enforces the following.

1. **No four-clique.**  For every four-set \(Q\), include
   \[
     \bigvee_{\{u,v\}\in {Q\choose2}}\neg e_{uv}.
   \]
2. **Every pair has a common neighbor.**  For each pair \(a,b\) and each
   possible witness \(c\notin\{a,b\}\), introduce \(w_{ab,c}\).  Add
   \(w_{ab,c}\Rightarrow e_{ac}\), \(w_{ab,c}\Rightarrow e_{bc}\), and
   \(\bigvee_c w_{ab,c}\).  Reverse implications are unnecessary: a true
   witness variable already certifies a real common neighbor.
3. **A fixed triangle.**  Each odd-hole template forces rim edge \(01\) and
   a chosen external common neighbor \(z\), hence
   \(e_{01}=e_{0z}=e_{1z}=1\).  The fallback
   \(\overline{C_7}\) template instead directly forces the triangle
   \(\{0,2,4\}\).
4. **Connected complement.**  For every nonempty proper set
   \(S\subset V\) containing vertex \(0\), add
   \[
     \bigvee_{u\in S,\ v\notin S}\neg e_{uv}.
   \]
   This says that some edge of \(G\) crosses every cut.  Taking only the side
   containing \(0\) represents every cut exactly once.

Items 1 and 3 give \(\omega(H)=3\), while item 2 gives
\(\gamma(G)=3\) by the complement dictionary.  Item 4 is a sound use of the
connected-counterexample reduction, not a heuristic.

## 2. Eternal-family encoding

Require \(\bigvee_T f_T\).  A selected triple must dominate \(G\).  In the
complement dictionary this is the clause
\[
  \neg f_T\ \vee\ \neg e_{xa}\ \vee\ \neg e_{xb}\ \vee\ \neg e_{xc}
\]
for every \(T=\{a,b,c\}\) and \(x\notin T\).

For every selected state \(T\), unoccupied attack \(r\notin T\), and
prospective moved guard \(u\in T\), introduce \(m_{T,r,u}\).  With
\(T'=(T-\{u\})\cup\{r\}\), add
\[
  m_{T,r,u}\Rightarrow\neg e_{ur},\qquad
  m_{T,r,u}\Rightarrow f_{T'},
\]
and
\[
  f_T\Rightarrow\bigvee_{u\in T}m_{T,r,u}.
\]
Thus one guard traverses one edge of \(G\) to the unoccupied attacked vertex,
and the successor remains a dominating member of the same family.  No
all-guards move, occupied-attack, or nondominating successor is admitted.

The maximum-independent-state lemma gives the optional strengthening
\[
  (e_{ab}\wedge e_{ac}\wedge e_{bc})\Rightarrow f_{\{a,b,c\}}
\]
for every triple.  It is redundant for correctness but can materially
improve propagation.

These clauses are existential.  Together with the static clauses they prove
\[
  \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]
for any satisfying graph and family.

## 3. Exhaustive SPGT templates

For each \(\ell\in\{5,7,9\}\), make one separate instance.  Force vertices
\(0,\ldots,\ell-1\) to induce the cycle
\[
  01,12,\ldots,(\ell-2)(\ell-1),(\ell-1)0,
\]
with every other rim pair a nonedge.  For every external vertex \(x\), add
\[
  \bigvee_{v=0}^{\ell-1}\neg e_{xv},
\]
so no external vertex is a hub.  Finally choose \(z=\ell\) and force it
adjacent to rim vertices \(0,1\).

This labeling is sound.  In any target graph, choose the required induced
hole, orient and label its rim, and then label as \(z\) any common neighbor
of the rim edge \(01\).  Such a neighbor exists by the common-neighbor
condition and lies outside an induced cycle.  Remaining vertices can be
labeled arbitrarily.  The three instances may overlap; they are exhaustive,
not disjoint.

If the pending odd-antihole audit fails, add the certified fourth instance
forcing an induced \(\overline{C_7}\), as specified in
`k3_structural_day1.md`.

## 4. Non-three-colorability by coloring cuts

Non-three-colorability of \(H\) is the only nonexistential condition.  It is
handled by a proof-producing CEGAR loop.

1. Solve the current CNF.
2. If it is unsatisfiable, retain the final CNF and a DRAT/LRAT-checkable
   proof.  Unsatisfiability under even a subset of valid coloring cuts rules
   out every non-three-colorable target in that template.
3. If it is satisfiable, extract \(H\) and run an independent exact
   three-coloring oracle.
4. If the oracle finds a coloring \(c\), add the valid cut
   \[
     \bigvee_{\substack{u<v\\c(u)=c(v)}} e_{uv}.
   \]
   This excludes that coloring: every graph for which \(c\) is proper has
   all same-color edge variables false.
5. If the oracle proves that \(H\) is not three-colorable, freeze the graph
   and family before continuing.  It is then a counterexample candidate and
   enters the full independent certificate protocol.

At a final `UNSAT`, the accumulated coloring clauses are all logical
consequences of “\(H\) is not three-colorable.”  Therefore the proof excludes
the intended universe even though not every possible coloring need have
been listed.

## 5. Coverage and certificate boundary

A certified negative result for \((12,3)\) requires all of:

- an accepted proof of the three template branches (or all four certified
  fallback branches);
- the exact CNF generator and a mathematical clause audit;
- instance and iteration manifests with input, model, coloring, CNF, and
  solver hashes;
- the final proof log for every unsatisfiable template and successful replay
  by an independent proof checker;
- an independent audit that every learned coloring cut has the stated form
  and is valid for its recorded coloring;
- no unproved symmetry breaking beyond the template relabeling proved above.

A timeout, a long sequence of colorable models, or an unlogged solver
`UNSAT` is exploratory evidence only.
