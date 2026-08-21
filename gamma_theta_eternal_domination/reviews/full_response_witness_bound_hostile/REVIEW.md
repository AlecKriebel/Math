# Hostile review: full-response five-witness bound

Date: 2026-07-27 (PDT)

Target:

`math/working/full_response_witness_bound/NOTE.md`

Target SHA-256:

`e491852cebec719d9296473ef3987298009d2759efab893865fb4d7e206666f1`

## Verdict

**PASS, subsequently superseded by the stronger six-witness theorem.**

The target note's human proof is correct under its stated hypotheses.  The
later cross-spoke disjointness result strengthens the numerical conclusion,
so the five-witness theorem should be retained as valid provenance rather
than presented as the sharp current bound.

## Independent reconstruction

For distinct vertices \(p,q\), the pair \(\{p,q\}\) fails to dominate
\(G\) exactly when some third vertex is nonadjacent in \(G\) to both,
equivalently when \(N_{\overline G}(p)\cap N_{\overline G}(q)\ne
\varnothing\).  Thus \(\gamma(G)\geq3\) supplies each \(u_i\) and each
\(z_i\) used in the proof.

For \(i\in S\), a witness \(u_i\in N_H(x)\cap N_H(i)\) cannot lie in
\(S\): \(u_i=i\) is excluded by looplessness, while \(u_i\in S-\{i\}\)
would contradict the assumed \(G\)-adjacency from \(x\) to every anchor.
It also cannot lie in \(Q_S\).  If \(j\in S-\{i\}\) and \(u_ij\in E(H)\),
then \(u_i\) is missed in \(G\) by the assumed dominating triple
\(\{x,i,j\}\).  Hence
\[
N_H(u_i)\cap S=\{i\}.
\]
This identity makes \(u_a,u_b,u_c\) pairwise distinct.

A witness \(z_i\in N_H(i)\cap N_H(u_i)\) is outside \(S\), outside
\(Q_S\), distinct from \(x\), and distinct from all three \(u_j\):
membership in \(S\) or equality to a different \(u_j\) contradicts the
displayed anchor-neighborhood identity, while equality to \(i,u_i\), or
\(x\) is excluded by looplessness or \(xi\in E(G)\).  Therefore the
three \(u_i\) and every \(z_i\) lie in
\(A=V(G)-(S\cup Q_S)\), with all \(z_i\) outside the three-element
\(u\)-set.  If \(|A|\leq4\), every \(z_i\) must be the same sole
remaining vertex.  It is then \(H\)-adjacent to all of \(a,b,c\), contrary
to domination by \(S\).  Hence \(|A|\geq5\), and the partition
\(V=S\mathbin{\dot\cup}Q_S\mathbin{\dot\cup}A\) gives
\(|V|\geq |Q_S|+8\).

## Eternal-family quantifiers

The specialization does not infer a graph nonedge from a missing response.
For \(\alpha=\gamma^\infty=3\), attacking the vertices of a maximum
independent triple successively shows that triple belongs to every eternal
triple-family.  A *full response* at \(x\) then explicitly means that all
three legal successor states are retained.  Legality supplies the three
\(G\)-edges from \(x\) to \(S\), and family membership supplies domination
of the successor triples.  These are exactly the hypotheses of the static
theorem.

In the exact nine-vertex separated-port core, the prescribed old
complement contains no anchor-to-outside edge, so all six old outside
vertices belong to \(Q_S\).  The target theorem therefore correctly gives
\(n\geq3+6+5=14\).  This is only a bound for that exact response pattern,
as the note states.

## SAT corroboration

The command mode `--order 13 --only-full-x --omit-closure` was inspected.
It fixes the exact old complement, enforces a common complement neighbor
for every pair, retains \(S\) and the three full-response successors, and
requires every retained state to dominate.  It does not use eternal
closure or omitted old response lists.  I regenerated its 5,412-clause
CNF byte-for-byte:

`382f17843fb46082c8790ad326dbf431fb8ae2bc9fada401d8e1ae5ad50e4490`

The existing solver log reports UNSAT and the existing `drat-trim` log
reports `VERIFIED` (233 input clauses and 98 lemmas in the reduced core).
This is consistent discovery provenance, not a premise of the verdict.

## Minor editorial observation

The sentence proving \(u_i\notin S\) is implicit in the target note rather
than written out.  The argument above supplies it immediately, so this is
not a mathematical defect.

