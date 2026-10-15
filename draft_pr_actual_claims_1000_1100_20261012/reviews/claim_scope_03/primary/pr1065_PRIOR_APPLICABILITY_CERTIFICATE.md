# Attracting edges under reciprocal summability

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed. It is an audit of the prior Cotar–Thacker result, whose journal publication is bibliographically verified. The report itself has no journal peer review or proof-assistant certification.

## Result and credit

**Problem 30000773, alias OWR-1543-004, queue rank 1226, has an affirmative credited resolution in its original bounded-degree, ordinary-initialization setting.** Codina Cotar and Debleena Thacker established the general attracting-edge result in *Edge- and vertex-reinforced random walks with super-linear reinforcement on infinite graphs*, Annals of Probability 45(4) (2017), 2655–2706, DOI [10.1214/16-AOP1122](https://doi.org/10.1214/16-AOP1122). The inspected full text is [arXiv:1509.00807v3](https://arxiv.org/abs/1509.00807v3), dated 2 June 2016; it is not asserted byte-identical to the journal version.

Theorem 2.4, manuscript p.9, applies directly to the triangle. Theorem 1.1, manuscript p.3, supplies the infinite connected bounded-degree statement with the initial-state conditions specified below. Neither theorem assumes that reinforcement is nondecreasing. This certificate records an existing result, not a new solution. **New proof-search turns: 0.**

A separate proof audit checks the finite theorem and the ordinary-initialization infinite conclusion in full using the authors' count-vector/order-statistic strategy. It also records a demonstrably incorrect displayed estimate in the inspected manuscript's Lemma 2.7. The repaired estimate below is restricted to the scope actually checked. The journal's corresponding proof was not obtained for comparison, and no defect in that uninspected version is asserted.

## Original question and restored scope

Pierre Tarrès's contribution with Vlada Limic, *What is the difference between a square and a triangle?*, appears on printed p.1553 of Oberwolfach Report 27/2007, PDF p.33. The [official report](https://ems.press/content/serial-article-files/46113?nt=1) describes undirected **edge** reinforcement: a nearest-neighbor transition selects an incident edge with probability proportional to a positive function of its previous traversal count. It recalls the reciprocally summable result on bounded-degree graphs without odd cycles, then asks for the corresponding behavior on general graphs, explicitly including a triangle. It already credits the nondecreasing-weight case to Limic–Tarrès.

The relevant generalization retains bounded degree; the context does not license arbitrarily unbounded-degree graphs. The report does not introduce unrestricted real edge-dependent initial offsets. The ordinary reading counts previous traversals, with a fixed positive initial reinforcement value, equivalently a common finite integer offset after reindexing the weight sequence. This initialization convention is stated rather than silently supplied as an arbitrary-state theorem. The report and DOI identify the 2007 workshop.

## Exact model and conclusion

Let G be a connected simple undirected graph with at least one edge. Start at a fixed vertex. For edge e, put

\[
N_e(n)=\#\{1\le t\le n:\{I_{t-1},I_t\}=e\},\qquad X_e(n)=\ell_e+N_e(n),
\]

where every initial offset \(\ell_e\ge0\) is finite. Let \(w:[0,\infty)\to(0,\infty)\) take finite values. The transition from x to its neighbor y has probability

\[
\frac{w(X_{\{x,y\}}(n))}{\sum_{z\sim x}w(X_{\{x,z\}}(n))}.
\]

Only the values on the sampled offset lattices matter. For integer offsets, w may equally well be given only on the nonnegative integers. Fixation means

\[
\mathbb P\bigl(\exists\hbox{ edge }e_*,\ \exists T<\infty:\{I_n,I_{n+1}\}=e_*\ \forall n\ge T\bigr)=1.
\]

It is almost-sure eventual alternation along one random undirected edge. It is stronger than a positive trapping probability or an assertion that only one edge is traversed infinitely often without a finite-range argument.

## Matching the published theorem's hypotheses

The manuscript's two initial-state conditions are

\[
S:=\sup_{e\in E(G)}\sum_{j=1}^{\infty}\frac1{w(\ell_e+j)}<\infty \tag{6}
\]

and

\[
M:=\sup_{e\in E(G)}w(\ell_e)<\infty. \tag{8}
\]

Condition (6) is a **uniform bound on the shifted reciprocal sums**. It is not merely separate convergence for each edge. Condition (8) bounds the initial reinforcement values, not all later reinforcement values.

- **Finite graph with at least three edges:** Theorem 2.4 requires (6). The triangle has exactly three edges and is covered directly. Since there are finitely many edges, (8) is automatic, and (6) is equivalent to convergence of each shifted reciprocal series. The accompanying audit also checks the one- and two-edge cases directly.
- **Infinite graph:** Theorem 1.1 assumes connectedness, a finite maximum degree, (6), and (8). No bipartiteness or monotonicity condition appears.
- **Common finite integer offset \(\ell_e=L\):** If \(\sum_{k=1}^{\infty}1/w(k)<\infty\), then
  \(S=\sum_{j\ge1}1/w(L+j)\le\sum_{k\ge1}1/w(k)<\infty\), and \(M=w(L)<\infty\). This is the primary accepted application to the original question.
- **Finitely many allowed real offsets:** Check the shifted reciprocal sum separately for every allowed offset. Finiteness of the set then supplies all the uniform bounds used in the scoped audit. Integer reciprocal summability alone says nothing about a nonintegral offset lattice.
- **Arbitrary nonnegative integer offsets with (8):** Integer reciprocal summability implies \(w(k)\to\infty\). Consequently (8) confines all offsets to a finite set of integers. This case is also covered by the finite-offset audit. This deduction does not use monotonicity of w.
- **Arbitrary real edge-dependent offsets under (6),(8):** These fall within the cited theorem's stated scope, but the present proof audit does not certify this full generality. The manuscript estimate discussed in PROOF_AUDIT.md cannot be used as printed. No replacement theorem for unrestricted real offsets is claimed here.

## Exact acceptance boundary

Accept the original bounded-degree attracting-edge question, including the triangle and arbitrary positive reciprocally summable, possibly nonmonotone reinforcement, as **resolved by Cotar–Thacker**, under ordinary common finite integer initialization. The scoped audit supplies a complete verification for this application. Do not present it as independent novelty, credit an already-known nondecreasing special case as new, or retain a dated assertion that the triangle remains unresolved.

The following are outside this certificate: vertex reinforcement; directed-edge reinforcement; arbitrary unbounded-degree graphs; a general theorem for unrestricted initial offsets inferred solely from unshifted integer summability; quantitative attraction-time moments; the whole vertex-reinforcement section of the paper; and a claim that every displayed proof line in the published article has been audited. No source text or source PDF is part of the authored public packet.

## References

1. Pierre Tarrès, joint work with Vlada Limic, contribution in *Non-Classical Interacting Random Walks*, Oberwolfach Report 27/2007, p.1553. [Official report](https://ems.press/content/serial-article-files/46113?nt=1), [report DOI](https://doi.org/10.4171/owr/2007/27).
2. Codina Cotar and Debleena Thacker, *Edge- and vertex-reinforced random walks with super-linear reinforcement on infinite graphs*, Annals of Probability 45(4) (2017), 2655–2706. [DOI](https://doi.org/10.1214/16-AOP1122), [inspected arXiv v3](https://arxiv.org/abs/1509.00807v3), [institutional publication record](https://discovery.ucl.ac.uk/id/eprint/1482663/).
3. Codina Cotar and Vlada Limic, *Attraction time for strongly reinforced walks*, Annals of Applied Probability 19 (2009), 1972–2007. This is the credited origin of the finite count-vector bound recalled as Proposition 2.1 in reference 2. Its separate full text was not inspected; the bound needed here is proved explicitly in PROOF_AUDIT.md.
