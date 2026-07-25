# Adversarial audit: odd triangle-free deficit lemma

Status: **CLEAN AUDIT.**  No counterexample or algebraic gap was found in
the lemma

\[
|V(F)|=2a+1,\quad F\ \hbox{triangle-free},\quad
\alpha(F)\leq a
\quad\Longrightarrow\quad
e(F)\leq a^2+1
\]

for \(a\geq2\).

This audit checks the lemma in
`proofs/antipodal_deep_graph_coupling.md`.  It does not independently
reprove the imported geometric assertion \(\alpha(H)\leq20\).

## Deficit proof audit

The proof's quantities and inequalities survive direct reconstruction:

1. Every neighborhood is independent, so \(d(x)\leq a\) and each
   \(\delta_x=a-d(x)\) is nonnegative.
2. If \(e(F)\geq a^2+2\), then
   \[
   D=\sum_x\delta_x=a(2a+1)-2e(F)\leq a-4.
   \]
3. Some vertex \(v\) has degree \(a\).  Otherwise
   \(2e(F)\leq(2a+1)(a-1)<2(a^2+2)\).
4. With \(A=N(v)\), \(B=V(F)\setminus(A\cup\{v\})\), and
   \(m=e(F[B])\), one has \(|A|=|B|=a\), \(A\) independent, \(v\)
   anticomplete to \(B\), and \(\delta_v=0\).  The two degree counts give
   \[
   e(A,B)=a(a-1)-D_A,\qquad
   a^2-D_B=e(A,B)+2m.
   \]
   Hence
   \[
   m+D_B+1=\frac{a+D}{2}+1\leq a-1
   \]
   and
   \[
   m=\frac{a+2D_A-D}{2}\geq\frac{a-D}{2}\geq2.
   \]
5. For an edge \(yz\in F[B]\), triangle-freeness makes the
   \(A\)-neighborhoods of \(y,z\) disjoint.  Writing \(q_y,q_z\) for
   their degrees inside \(B\) therefore gives
   \[
   q_y+q_z+\delta_y+\delta_z\geq a.
   \]
   But the \(B\)-edges incident with \(y\) or \(z\) form
   \(q_y+q_z-1\) distinct edges, so \(q_y+q_z\leq m+1\), while
   \(\delta_y+\delta_z\leq D_B\).  Their sum is at most
   \(m+D_B+1\leq a-1\), a contradiction.

No step uses regularity, connectedness, maximality, symmetry, or a strict
independence inequality.

For \(a=2,3\), the stated handshake argument is also correct:
\[
e(F)\leq
\left\lfloor\frac{a(2a+1)}2\right\rfloor=a^2+1.
\]

## Small-case exhaustive checks

Two different exact enumerators were used.  The discovery program tests all
labeled edge masks for \(a=2,3\).  The verifier instead generates only
triangle-free graphs recursively and performs an exact independent-set
search at every leaf.

| \(a\) | vertices | all labeled graphs | triangle-free labeled graphs | feasible \(\alpha\leq a\) | maximum edges |
|---:|---:|---:|---:|---:|---:|
| 2 | 5 | 1,024 | 388 | 12 | 5 |
| 3 | 7 | 2,097,152 | 133,501 | 13,842 | 10 |

The full feasible edge histograms are:

- \(a=2\): 12 graphs with 5 edges;
- \(a=3\): 252, 2,880, 6,300, 3,780, and 630 graphs with
  6, 7, 8, 9, and 10 edges, respectively.

Thus the bound is attained in both cases.

For \(a=4\), a violation would have at least 18 edges.  Since
\(\Delta\leq4\) on nine vertices, it would be 4-regular with exactly 18
edges.  Relabeling safely fixes \(v=0\) and
\(N(v)=\{1,2,3,4\}\).  If \(B\) is the other four vertices, the degree
equations force exactly two \(B\)-edges and a \(4\times4\) \(A\)-to-\(B\)
incidence matrix with row sums three.  All 15 choices of two \(B\)-edges
and all \(15\cdot2^{16}=983{,}040\) incidence masks were checked.  Exactly
216 satisfy the degree equations and none is triangle-free.

The verifier obtains the same 216 count independently from missing-neighbor
multiplicities: 72 cases have two disjoint \(B\)-edges and 144 have adjacent
\(B\)-edges.  For each \(B\)-edge, its endpoint \(A\)-degrees sum to six or
five, so the two endpoints necessarily share an \(A\)-neighbor and form a
triangle.

## Minor presentation recommendation

The manuscript proves the \(r=19,20\) antipodal branches impossible after
displaying the lemma's consequence.  Since the lemma is stated only for
\(a\geq2\), it would be slightly cleaner to move that two-line exclusion
before “Applying the lemma,” or to write “for \(r\leq18\).”  This is an
ordering issue, not a logical defect: the \(r=19,20\) exclusions are
independent of the lemma.

## Reproduction

From the repository root:

```sh
./.venv/bin/python \
  experiments/antipodal_deep_graph_audit/audit_small_cases.py

./.venv/bin/python \
  experiments/antipodal_deep_graph_audit/verify.py

./.venv/bin/python -O \
  experiments/antipodal_deep_graph_audit/verify.py

./.venv/bin/python -m unittest \
  experiments/antipodal_deep_graph_audit/test_audit.py -v
```

Pinned result:

```text
9cdce88d4e6d2492c69424020d42d7956c55ffacf2eb8f2140bf5041c9a0869b  results/small_case_audit.json
```
