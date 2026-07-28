# Hostile review: the order-13 no-full response-type decomposition

## Verdict

**PASS, WITH THE CLAIM BOUNDARY IN THE SOURCE NOTE ENFORCED LITERALLY.**

The current source bytes prove Theorem 2.1, Corollary 2.2, Theorem 3.1,
Lemma 4.1, Theorem 4.2, and Corollary 4.3.  In particular, a hypothetical
order-13, parameter-three counterexample in the no-full branch has

\[
 |A|\geq5,\qquad |Q|\leq5,
\]

and if all three two-list types occur then

\[
 |A|\geq6,\qquad |Q|\leq4.
\]

When \((|A|,|Q|)=(5,5)\), the asserted signature normal form and the
universal complement adjacency from the neutral set to its exceptional
vertex are also correct.

These are structural reductions only.  They do **not** exclude the complete
order-13 no-full branch, raise the global certified frontier, prove the
parameter-three conjecture, or resolve the universal conjecture.

The earlier assertion

\[
 |A|\geq7,\qquad |Q|\leq3
\]

is false for the reason stated in the note: when testing a pair of anchors,
the third anchor already witnesses nondomination.  The false assertion
appears in the reviewed source only inside an explicit retraction.  It is
absent from every accepted theorem, the final remaining-branch split, and
the supported `residual` generator mode.

The legacy `tight-*` and `six-*` UNSAT files encode consequences of that
false extra assumption.  Whether or not their particular DRAT streams
verify, they have **no coverage meaning**.  The two `a4-*` modes are also
deliberately nonexhaustive controls and cannot be combined into an
order-13 coverage claim.

## Reviewed bytes

| artifact | SHA-256 |
|---|---|
| `math/working/order13_no_full_decomposition/NOTE.md` | `9f5d2cd405b5466ffad88b68aebc10db189e445f731fb0c3a0335c257546a03c` |
| `math/working/order13_no_full_decomposition/decompose.py` | `041c438c8bee5f14775f54eb8db096676021e8048737e30e6f37378607dac0fd` |
| `math/working/order13_no_full_probe/search.py` | `88e958358612ffd15823b8e315db2cc4c824c341557f59e37543a816ee8d6328` |
| `math/working/order13_no_full_probe/instance.cnf` | `5d6d9bccb80c3ccab222a095819d50b58bb9f1fc22652b2d0bad8013681fd007` |
| frozen-projection prerequisite | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| singleton-safety prerequisite | `ed88c3ace73acc061bab41e8d7ab9a7a74ede1d739ef9c3aae9ed05b38aa0772` |
| physical-representative prerequisite | `a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279` |
| this review's independent checker | `b24e8566231ec3f2c65cea93ba3be83223fa07c6f0349bdeea9d125b1d41822e` |
| independent result | `577679eab2d0ee62c06f8bca6a698e4be16065203fbf36037ffbe760c64b82ff` |

The prerequisite rows refer respectively to
`math/working/k3_cross_state_attack.md`,
`math/working/universal_complement_local_balance_attack.md`, and
`math/working/separated_core_n14_attack/NOTE.md`.

## 1. Exact model and response lists

The argument uses the standard one-guard-moves model throughout.  The
reference triple \(S=\{a,b,c\}\) is independent and belongs to the eternal
family \(\mathcal F\).  For an outside attack \(x\), closure at \(S\)
moves exactly one adjacent guard \(u\in S\) and retains the successor
\(S-u+x\).  Therefore every list

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}
\]

is nonempty.

Although the displayed definition does not repeat the move-edge condition,
membership still forces it.  In the retained state \(S-u+x\), neither of
the other two anchors is adjacent in \(G\) to the omitted anchor \(u\).
Because that state dominates, \(x\) must be adjacent to \(u\).  Hence

\[
 u\in L(x)\Longrightarrow ux\in E(G),
\qquad
 L(x)\subseteq S-\sigma(x).
\]

This is the only direction used.  No proof converts absence from a family
list into a graph nonedge.

The no-full hypothesis says \(1\leq |L(x)|\leq2\) for every outside
vertex.  Its lower bound is genuine family closure; its upper bound is a
separate assumption.  Attacks in the proofs are always made at vertices
outside the current state, and all successor states invoked are retained
dominating triples.

## 2. One two-list type gives an ordinary coloring

Suppose at most one exact two-list type occurs, and choose \(c\) to be its
omitted color if it exists.  A vertex outside \(W_c\) has \(c\in L(x)\).
If its no-full list had size two, that pair would omit \(a\) or \(b\), not
\(c\), producing a second type.  Thus every such vertex has the singleton
list \(\{c\}\).

This gives the disjoint vertex partition

\[
 V(H)=
 \bigl((S-\{c\})\cup W_c\bigr)
 \mathbin{\dot\cup}
 \bigl(\{c\}\cup\{x:L(x)=\{c\}\}\bigr).
\]

The first induced graph is bipartite by the accepted family-list
frozen-projection theorem.  The second is independent in \(H\):
membership makes every \(x\) adjacent to \(c\) in \(G\), and accepted
singleton safety makes two distinct vertices with list \(\{c\}\) adjacent
in \(G\).  Two colors on the first part and a third color on the second
therefore give an ordinary proper 3-coloring of all of \(H\).

This argument correctly ignores response-list color constraints inside the
bipartite part.  It proves an ordinary coloring, which is exactly what is
needed for \(\theta(G)\leq3\).  Consequently \(\theta(G)>3\) forces at
least two distinct two-list types.

## 3. Pure-signature doubling

For an occurring omitted color \(i\), the accepted physical-representative
lemma supplies \(z_i\) with

\[
 L(z_i)=S-\{i\},\qquad \sigma(z_i)=\{i\}.
\]

Since \(\gamma(G)\geq3\), the pair \(\{i,z_i\}\) is not dominating.  A
common \(H\)-neighbor \(w_i\) exists.  It is outside \(S\): every other
anchor belongs to \(L(z_i)\) and hence is adjacent to \(z_i\) in \(G\).

If \(w_i\) also had a second anchor \(r\) in its signature, let \(h\) be
the remaining anchor.  Since \(h\in L(z_i)\), the retained state

\[
 S-h+z_i=\{i,r,z_i\}
\]

would miss \(w_i\) at all three guards.  This contradicts domination of
every family state.  Thus

\[
 \sigma(w_i)=\{i\},\qquad z_iw_i\in E(H).
\]

The two vertices are distinct, and pure signature classes for different
anchors are disjoint.  Therefore each occurring type costs two distinct
vertices of \(A\), proving \(|A|\geq2t\).  The proof does not assert that
\(w_i\) has the same exact two-list, so it does not make an invalid
iteration.

## 4. Neutral coverage, the count, and the tight form

For \(q\in Q\) and \(i\in S\), the pair \(\{q,i\}\) is nondominating.
Any common \(H\)-neighbor \(x_{q,i}\):

- is not an anchor, because \(q\) is \(G\)-complete to \(S\);
- is not neutral, because it is \(H\)-adjacent to \(i\); and
- therefore lies in \(A\), has \(i\in\sigma(x_{q,i})\), and is
  \(H\)-adjacent to \(q\).

Hence if \(Q\ne\varnothing\), the signatures present in \(A\) cover all
three anchors.

At order 13 there are ten outside vertices.  If \(t=3\), doubling
immediately gives \(|A|\geq6\).  If \(t=2\), doubling gives four vertices
with two pure signatures.  Were these all of \(A\), then \(Q\) would be
nonempty while the union of signatures in \(A\) missed the third anchor,
contradicting neutral coverage.  Thus \(|A|\geq5\).

The independent checker's finite truth table enumerated the relevant
multisets of nonempty proper signatures under precisely these two accepted
consequences.  It independently recovered minima five for \(t=2\) and six
for \(t=3\).

In the tight case \(|A|=5\), exactly two types occur.  Four vertices are the
two pure pairs.  The fifth vertex \(r\) is the unique signature containing
the third anchor \(h\), so every neutral vertex is \(H\)-adjacent to \(r\).
If \(\sigma(r)=\{h\}\), then the pair \(\{h,r\}\) has no common
\(H\)-neighbor:

- the two other anchors are \(G\)-adjacent to \(r\);
- neutral vertices are \(G\)-adjacent to \(h\); and
- the four pure \(i/j\) vertices are \(G\)-adjacent to \(h\).

That would make \(\{h,r\}\) a dominating pair in \(G\).  Therefore, after
interchanging \(i,j\),

\[
 \sigma(r)=\{h,i\}.
\]

The already proved inclusion
\(\varnothing\ne L(r)\subseteq S-\sigma(r)\) then forces
\(L(r)=\{j\}\).  This verifies the complete stated normal form.

## 5. Independent no-full formula reconstruction

`checker.py` imports neither discovery wrapper nor transition core.  It
starts from the previously clean-room, independently audited formula
builder in `reviews/order13_full_target_hostile/checker.py`, removes exactly
the six units that singled out vertex 3 as a full target, and appends the
ten clauses forbidding all three direct successor states at each outside
target.

The reconstruction is byte-for-byte identical to the retained DIMACS:

\[
\begin{array}{c|r}
\text{variables}&9802\\
\text{clauses}&85413\\
\text{bytes}&4808989\\
\text{SHA-256}&
\texttt{5d6d9bccb80c3ccab222a095819d50b58bb9f1fc22652b2d0bad8013681fd007}.
\end{array}
\]

It contains no duplicate clause, tautology, or unused variable.  The
independent clause census recovers:

- 10 no-full clauses;
- 960 pivoted signature-sort clauses; and
- \(3^{10}=59049\) anchored non-3-colorability clauses.

All 2,048 assignments to every adjacent four-bit signature pair were
truth-tabled, confirming that the sorter permits exactly nondecreasing
signatures.

The formula has the claimed mathematical semantics:

1. the fixed \(H\)-triangle and no \(H\)-\(K_4\) clauses give
   \(\alpha(G)=3\);
2. common-\(H\)-neighbor witnesses for every pair, together with domination
   of the retained anchor state, give \(\gamma(G)=3\);
3. literal response variables require one adjacent guard, one changed
   vertex, and a retained successor for every unoccupied attack, giving an
   eternal family of triples;
4. closure at the retained anchor state makes every direct list nonempty;
5. a retained direct successor necessarily dominates the omitted anchor,
   so the ten ternary clauses express exactly that no target has all three
   responses; and
6. the anchored coloring clauses are exhaustive because the fixed
   \(H\)-triangle can be assigned colors \(0,1,2\) after permuting color
   names.

The pivoted \(S_9\) sorter is safe after the six units are removed.  Given
any labeling of the ten outside vertices, choose any one as label 3; the
remaining nine are interchangeable and can be sorted by their adjacencies
to \(\{0,1,2,3\}\).  Omitting connectedness and the redundant forcing of
all independent triples only relaxes the formula, so it is safe for a
future UNSAT exclusion.

The recorded 120-second solver timeout supplies neither SAT nor UNSAT and
remains a **NONCLAIM**.  The deleted partial proof stream could not have
certified anything.

## 6. Splitter and artifact-boundary audit

The current `decompose.py` replaces the pivoted sorter by a full \(S_{10}\)
sort of the three-bit anchor signatures.  Adjacent-inversion clauses
correctly force the ten outside signatures into nondecreasing order.
Because signature zero is exactly neutrality, the `residual` unit saying
that vertex 8 has a nonzero signature is equivalent to at most five neutral
vertices, hence at least five nonneutral vertices.  This is the complete
theorem-supported remaining branch.

The two `a4-*` modes add much stronger named signature and response-list
conditions.  They do not enumerate all formal four-nonneutral patterns.
Their two stored DRAT proofs replay successfully for their exact CNFs, but
that is merely a redundant control below the human-proved floor and has no
coverage consequence.  These `a4-*` CNFs, proofs, cores, and logs are local
discovery controls and are intentionally excluded from the publication
staging set.  The accepted artifacts for this review are the source note,
splitter, retained no-full instance, hostile review, independent checker,
and deterministic result.

The `tight-*` and `six-*` files are even more restricted: their construction
used the retracted double-signature premise.  Their UNSAT status cannot be
lifted to any valid branch of the conjecture.  They must remain excluded
from certified finite claims, manifests purporting to cover the no-full
branch, and any statement of the order-13 frontier.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/order13_no_full_decomposition_hostile/checker.py
```

The command writes a deterministic `result.json` and prints `PASS`.
